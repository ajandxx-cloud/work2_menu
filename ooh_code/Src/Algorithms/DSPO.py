import numpy as np
import numpy.ma as ma
import torch
import torch.nn as nn
from math import e, exp, sqrt
from operator import itemgetter
from torch import float32

from hygese import AlgorithmParameters, Solver

from Src.Algorithms.Agent import Agent
from Src.Utils.MathUtils import lambertw
from Src.Utils.Predictors import CNN_2d, CNN_3d, LinReg
from Src.Utils.Utils import MemoryBuffer, extract_route_HGS, get_dist_mat_HGS, get_matrix


class DSPO(Agent):
    def __init__(self, config):
        super(DSPO, self).__init__(config)

        self.load_data = config.load_data
        self.k = config.k
        self.init_theta = config.init_theta_cnn
        self.cool_theta = config.cool_theta_cnn
        self.max_p = config.max_price
        self.min_p = config.min_price

        if self.config.pricing:
            self.get_action = self.get_action_pricing
        else:
            self.get_action = self.get_action_offer

        self.grid_dim = config.grid_dim
        self.initial_phase = True
        self.n_layers = config.n_input_layers
        self.output_dim = 1
        self.aux_dim = 1

        self.memory = MemoryBuffer(
            max_len=self.config.buffer_size,
            time_intervals=self.n_layers,
            matrix_dim=self.grid_dim,
            target_dim=self.output_dim,
            atype=float32,
            config=config,
            aux_dim=self.aux_dim,
        )

        if config.use3d_conv:
            self.supervised_ml = CNN_3d(self.grid_dim, self.n_layers, config.n_filters, config.dropout)
        elif config.linearModel:
            self.supervised_ml = LinReg(
                self.grid_dim * self.grid_dim * self.n_layers,
                aux_dim=self.aux_dim,
                output_dim=self.output_dim,
            )
        else:
            self.supervised_ml = CNN_2d(
                self.grid_dim,
                self.n_layers,
                config.n_filters,
                config.dropout,
                aux_dim=self.aux_dim,
                output_dim=self.output_dim,
            )

        self.features = np.empty((0, self.n_layers * self.grid_dim * self.grid_dim))
        self.cap_features = np.empty((0, self.aux_dim))
        self.interval = int(config.max_steps_r / max(config.n_input_layers, 1))

        self.optimizer = config.optim(self.supervised_ml.parameters(), lr=self.config.learning_rate)
        self.criterion = nn.HuberLoss(delta=1.0)
        self.modules = [('supervised_ml', self.supervised_ml)]
        self.init()
        self.device = config.device

        self.customer_cell = get_matrix(config.coords, self.grid_dim, config.hexa)
        self.dist_matrix = config.dist_matrix
        self.service_times = config.service_times
        self.adjacency = config.adjacency

        if self.load_data:
            self.first_parcelpoint_id = len(self.dist_matrix[0]) - config.n_parcelpoints - 1
            self.addedcosts = self.addedcosts_distmat
            self.dist_scaler = 1
            self.mnl = self.mnl_distmat
        else:
            self.first_parcelpoint_id = len(config.coords) - config.n_parcelpoints
            self.addedcosts = self.addedcosts_euclid
            self.dist_scaler = 1
            self.mnl = self.mnl_euclid

        self.base_util = config.base_util
        self.cost_multiplier = (config.driver_wage + config.fuel_cost) / 3600
        self.wage = config.driver_wage
        self.revenue = config.revenue
        self.depot = getattr(getattr(config, "env", None), "depot", config.coords[0])

        ap_final = AlgorithmParameters(timeLimit=config.hgs_final_time)
        self.hgs_solver_final = Solver(parameters=ap_final, verbose=False)

    @staticmethod
    def _safe_exp(val):
        return float(np.exp(np.clip(float(val), -700.0, 700.0)))

    def reset(self):
        super().reset()
        self.features = np.empty((0, self.n_layers * self.grid_dim * self.grid_dim))
        self.cap_features = np.empty((0, self.aux_dim))

    def _candidate_parcelpoints(self, state):
        if self.load_data:
            mask = ma.masked_array(state[2]["parcelpoints"], mask=self.adjacency[state[0].id_num])
            return mask[mask.mask].data
        return state[2]["parcelpoints"]

    def _theta(self, step):
        return max(0.0, self.init_theta - (step * self.cool_theta))

    def get_action_offer(self, state, training):
        if self.initial_phase:
            return self.get_action_offerall(state, training)

        theta = self._theta(state[3])
        mltplr = self.cost_multiplier
        pps = self._candidate_parcelpoints(state)
        if len(pps) == 0:
            return np.empty(0, dtype=int)

        pp_costs = np.full(len(pps), 1000000000.0)
        cur_feat = self.get_feature_rep_infer(state[1]["fleet"])
        costs = self.get_prediction(cur_feat, state[0].home, pps)

        for idx, pp in enumerate(pps):
            if pp.remainingCapacity > 0:
                pp_costs[idx] = mltplr * (
                    (1 - theta) * self.cheapestInsertionCosts(pp.location, state[1])
                    + theta * (costs[idx + 2] - costs[0])
                )

        top_k = min(self.k, len(pps))
        pp_sorted_args = pps[np.argpartition(pp_costs, top_k - 1)[:top_k]]
        return np.array([pp.id_num for pp in pp_sorted_args], dtype=int)

    def get_action_pricing(self, state, training):
        pps = self._candidate_parcelpoints(state)
        if self.initial_phase:
            return np.around(np.zeros(len(pps) + 1), decimals=2)

        pp_costs = np.full((len(pps), 1), 1000000000.0)
        cur_feat = self.get_feature_rep_infer(state[1]["fleet"])
        costs = self.get_prediction(cur_feat, state[0].home, pps)

        theta = self._theta(state[3])
        mltplr = self.cost_multiplier

        home_costs = state[0].service_time * mltplr + (
            (1 - theta) * self.cheapestInsertionCosts(state[0].home, state[1])
            + theta * (costs[1] - costs[0])
        )
        sum_mnl = self._safe_exp(
            self.base_util + state[0].home_util
            + (state[0].incentiveSensitivity * (home_costs - self.revenue))
        )

        for idx, pp in enumerate(pps):
            if pp.remainingCapacity > 0:
                util = self.mnl(state[0], pp)
                pp_costs[idx] = mltplr * (
                    (1 - theta) * self.cheapestInsertionCosts(pp.location, state[1])
                    + theta * (costs[idx + 2] - costs[0])
                )
                sum_mnl += self._safe_exp(
                    util + (state[0].incentiveSensitivity * (pp_costs[idx] - self.revenue))
                )

        lambertw0 = (lambertw(sum_mnl / e).real + 1) / state[0].incentiveSensitivity

        a_hat = np.zeros(len(pps) + 1)
        a_hat[0] = home_costs - self.revenue - lambertw0
        for idx, pp in enumerate(pps):
            if pp.remainingCapacity > 0:
                a_hat[idx + 1] = pp_costs[idx] - self.revenue - lambertw0

        a_hat = np.clip(a_hat, self.min_p, self.max_p)
        return np.around(a_hat, decimals=2)

    def get_action_offerall(self, state, training):
        pps = self._candidate_parcelpoints(state)
        action = np.empty(0, dtype=int)
        for pp in pps:
            if pp.remainingCapacity > 0:
                action = np.append(action, pp.id_num)
        return action

    def addedcosts_euclid(self, route, i, loc):
        costs = (
            self.getdistance_euclidean(route[i - 1], loc)
            + self.getdistance_euclidean(loc, route[i])
            - self.getdistance_euclidean(route[i - 1], route[i])
        )
        return costs / self.dist_scaler

    def addedcosts_distmat(self, route, i, loc):
        costs = (
            self.dist_matrix[route[i - 1].id_num][loc.id_num]
            + self.dist_matrix[loc.id_num][route[i].id_num]
            - self.dist_matrix[route[i - 1].id_num][route[i].id_num]
        )
        return costs / self.dist_scaler

    def cheapestInsertionCosts(self, loc, fleet):
        cheapest_costs = float("inf")
        for vehicle in fleet["fleet"]:
            for i in range(1, len(vehicle["routePlan"])):
                added_costs = self.addedcosts(vehicle["routePlan"], i, loc)
                if added_costs < cheapest_costs:
                    cheapest_costs = added_costs
        return cheapest_costs

    def getdistance_euclidean(self, a, b):
        return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

    def get_prediction(self, cur_feat, home, pps):
        time_int = min(int(home.time / max(self.interval, 1)), self.n_layers - 1)
        batch_size = 2 + len(pps)
        new_feat = cur_feat.repeat(batch_size, 1, 1, 1)
        aux = np.zeros((batch_size, self.aux_dim), dtype=np.float32)
        aux[0][0] = 1000000.0
        aux[1][0] = 1000000.0

        new_feat[1][time_int][self.customer_cell[home.id_num][0]][self.customer_cell[home.id_num][1]] += 1
        for idx, p in enumerate(pps):
            new_feat[idx + 2][time_int][self.customer_cell[p.location.id_num][0]][self.customer_cell[p.location.id_num][1]] += 1
            aux[idx + 2][0] = max(float(p.remainingCapacity - 1), 0.0)

        with torch.no_grad():
            aux_tensor = torch.tensor(aux, dtype=float32, device=self.device)
            outputs = self.supervised_ml(new_feat.to(self.device), aux_tensor)
        return outputs.detach().cpu().numpy().reshape(-1).tolist()

    def mnl_euclid(self, customer, parcelpoint):
        distance = self.getdistance_euclidean(customer.home, parcelpoint.location)
        beta_p = -exp(-distance / self.dist_scaler)
        return self.base_util + beta_p

    def mnl_distmat(self, customer, parcelpoint):
        distance = self.dist_matrix[customer.id_num][parcelpoint.id_num]
        beta_p = -exp(-distance / self.dist_scaler)
        return self.base_util + beta_p

    def update(self, data, state, done=False):
        if not done:
            self.features = np.vstack((self.features, self.get_feature_rep(data).flatten()))
            selected_cap = 1000000.0
            try:
                selected_id = int(data["id"][-1])
                pp_idx = selected_id - self.first_parcelpoint_id
                if 0 <= pp_idx < len(state[2]["parcelpoints"]):
                    selected_cap = float(state[2]["parcelpoints"][pp_idx].remainingCapacity)
            except Exception:
                selected_cap = 1000000.0
            self.cap_features = np.vstack((self.cap_features, np.array([[selected_cap]], dtype=np.float32)))
            return 0.0

        if self.load_data:
            data["distance_matrix"] = get_dist_mat_HGS(self.dist_matrix, data['id'])
        fleet, cost = self.reopt_HGS_final(data, fallback_fleet=state[1])

        target = sorted(self.get_per_customer_costs(fleet), key=itemgetter(0))
        max_count = min(len(target), len(self.features), len(self.cap_features))
        if max_count > 0:
            penalties = 20.0 / (self.cap_features[:max_count, [0]] + 0.1)
            adjusted_target = []
            for idx in range(max_count):
                adjusted_target.append([float(target[idx][1]) + float(penalties[idx][0])])
            self.memory.add(self.features[:max_count], self.cap_features[:max_count], adjusted_target)

        self.features = np.empty((0, self.n_layers * self.grid_dim * self.grid_dim))
        self.cap_features = np.empty((0, self.aux_dim))

        if self.initial_phase:
            if self.memory.length >= self.config.buffer_size:
                self.initial_phase_training(max_epochs=self.config.initial_phase_epochs)
        elif not self.config.only_phase_one:
            self.optimize()

        return cost

    def optimize(self):
        feat, cap_feat, target = self.memory.sample(batch_size=self.config.batch_size)
        loss = self.self_supervised_update(feat, cap_feat, target)
        print("Huber loss: ", loss)

    def self_supervised_update(self, feat, cap_feat, target):
        self.optimizer.zero_grad()
        outputs = self.supervised_ml(feat, cap_feat)
        loss = self.criterion(outputs, target)
        loss.backward()
        self.optimizer.step()
        return loss.item()

    def initial_phase_training(self, max_epochs=-1):
        initial_losses = []
        print("Inital training phase started...")
        for counter in range(max_epochs):
            losses = []
            for feat, cap_feat, target in self.memory.batch_sample(batch_size=self.config.batch_size, randomize=True):
                loss = self.self_supervised_update(feat, cap_feat, target)
                losses.append(loss)
            initial_losses.append(np.mean(losses))
            if counter % 1 == 0:
                print("Epoch {} Huber loss:: {}".format(counter, np.mean(initial_losses[-10:])))
                if self.config.only_phase_one:
                    self.memory.save(self.config.paths['checkpoint'] + 'initial_')
                    self.save()
                    print("Saved..")
            if len(initial_losses) >= 20 and np.mean(initial_losses[-10:]) + 1e-5 >= np.mean(initial_losses[-20:]):
                print("Converged...")
                break
        print('... Initial training phase terminated!')
        self.initial_phase = False
        self.memory.save(self.config.paths['checkpoint'] + 'initial_')
        self.save()

    def get_feature_rep(self, data):
        feature = np.zeros((self.n_layers, self.grid_dim, self.grid_dim))
        for i, t in zip(data["id"], data["time"]):
            time_int = min(int(t / max(self.interval, 1)), self.n_layers - 1)
            feature[time_int][self.customer_cell[i][0]][self.customer_cell[i][1]] += 1
        return feature

    def get_feature_rep_infer(self, fleet):
        feature = np.zeros((self.n_layers, self.grid_dim, self.grid_dim))
        for vehicle in fleet:
            for loc in vehicle["routePlan"]:
                time_int = min(int(loc.time / max(self.interval, 1)), self.n_layers - 1)
                feature[time_int][self.customer_cell[loc.id_num][0]][self.customer_cell[loc.id_num][1]] += 1
        return torch.tensor(feature, dtype=float32, requires_grad=False).unsqueeze(0)

    def reopt_HGS_final(self, data, fallback_fleet=None):
        customer_count = max(len(data['x_coordinates']) - 1, 0)
        if customer_count <= 1 and fallback_fleet is not None:
            return (
                self.fallback_fleet_without_depots(fallback_fleet),
                self.fallback_route_cost(fallback_fleet),
            )
        data["demands"] = np.ones(len(data['x_coordinates']))
        data["demands"][0] = 0
        result = self.hgs_solver_final.solve_cvrp(data)
        fleet = extract_route_HGS(result, data)
        return fleet, result.cost

    def fallback_route_cost(self, fleet_snapshot):
        total_cost = 0.0
        for vehicle in fleet_snapshot["fleet"]:
            route = list(vehicle["routePlan"])
            if len(route) == 0:
                continue
            has_depot_endpoints = (
                len(route) >= 2
                and route[0].id_num == self.depot.id_num
                and route[-1].id_num == self.depot.id_num
            )
            if has_depot_endpoints:
                for idx in range(len(route) - 1):
                    total_cost += self._edge_travel_time(route[idx], route[idx + 1])
            else:
                total_cost += self._edge_travel_time(self.depot, route[0])
                for idx in range(len(route) - 1):
                    total_cost += self._edge_travel_time(route[idx], route[idx + 1])
                total_cost += self._edge_travel_time(route[-1], self.depot)
        return float(total_cost)

    def fallback_fleet_without_depots(self, fleet_snapshot):
        normalized = {"fleet": []}
        for vehicle in fleet_snapshot["fleet"]:
            route = [
                loc for loc in vehicle["routePlan"]
                if loc.id_num != self.depot.id_num
            ]
            normalized["fleet"].append({"routePlan": route})
        return normalized

    def _edge_travel_time(self, a, b):
        if self.load_data:
            return float(self.dist_matrix[a.id_num][b.id_num])
        return float(self.getdistance_euclidean(a, b) / max(self.config.truck_speed, 1e-6) * 3600.0)

    def get_per_customer_costs(self, fleet):
        mltplr = self.cost_multiplier
        costs = []
        for vehicle in fleet["fleet"]:
            if len(vehicle["routePlan"]) == 1:
                costs.append([vehicle["routePlan"][0].time, mltplr * self._edge_travel_time(self.depot, vehicle["routePlan"][0])])
            else:
                for i in range(0, len(vehicle["routePlan"])):
                    if i == 0:
                        costs.append([
                            vehicle["routePlan"][i].time,
                            mltplr * (
                                0.5 * self._edge_travel_time(self.depot, vehicle["routePlan"][i])
                                + 0.5 * self._edge_travel_time(vehicle["routePlan"][i], vehicle["routePlan"][i + 1])
                            ),
                        ])
                    elif i == len(vehicle["routePlan"]) - 1:
                        costs.append([
                            vehicle["routePlan"][i].time,
                            mltplr * (
                                0.5 * self._edge_travel_time(vehicle["routePlan"][i - 1], vehicle["routePlan"][i])
                                + 0.5 * self._edge_travel_time(vehicle["routePlan"][i], self.depot)
                            ),
                        ])
                    else:
                        costs.append([
                            vehicle["routePlan"][i].time,
                            mltplr * (
                                0.5 * self._edge_travel_time(vehicle["routePlan"][i - 1], vehicle["routePlan"][i])
                                + 0.5 * self._edge_travel_time(vehicle["routePlan"][i], vehicle["routePlan"][i + 1])
                            ),
                        ])
        return costs
