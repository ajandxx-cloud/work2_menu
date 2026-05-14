from __future__ import print_function

import numpy as np
import sys

from Src.Utils.Utils import get_dist_mat_HGS, get_fleet
from Environments.OOH.containers import (
    Customer,
    Fleet,
    Location,
    MenuOffer,
    ParcelPoint,
    ParcelPoints,
    Vehicle,
)
from Environments.OOH.env_utils import utils_env
from Environments.OOH.customerchoice import customerchoicemodel


class Parcelpoint_py(object):
    def __init__(self,
                 model,
                 max_steps_r,
                 max_steps_p,
                 n_vehicles=2,
                 veh_capacity=100,
                 meeting_point_capacity=25,
                 fraction_capacitated=0.0,
                 incentive_sens=0.99,
                 base_util=0.2,
                 home_util=0.3,
                 reopt=2000,
                 load_data=False,
                 coords=[],
                 dist_matrix=[],
                 n_meeting_points=6,
                 adjacency=[],
                 service_times=[],
                 dissatisfaction=False,
                 hgs_time=3.0,
                 menu_target_arrival_time=8.5 * 3600,
                 menu_pref_window_half_width=600.0,
                 menu_pref_buffer_seconds=300.0,
                 menu_pref_noise_std=60.0,
                 menu_travel_time_weight=-0.002,
                 menu_pickup_time_weight=-0.0015,
                 outside_option_util=0.0):

        self.max_steps = 0
        self.max_steps_r = max_steps_r
        self.max_steps_p = max_steps_p

        self.n_vehicles = n_vehicles
        self.veh_capacity = veh_capacity
        self.pp_capacity = meeting_point_capacity
        self.fraction_capacitated = fraction_capacitated
        self.data = dict()

        self.coords = coords
        self.dist_matrix = dist_matrix
        self.n_parcelpoints = n_meeting_points
        self.adjacency = adjacency
        self.service_times = service_times

        self.load_data = load_data
        self.menu_mode = True
        self.menu_target_arrival_time = float(menu_target_arrival_time)
        self.menu_pref_window_half_width = float(menu_pref_window_half_width)
        self.menu_pref_buffer_seconds = float(menu_pref_buffer_seconds)
        self.menu_pref_noise_std = float(menu_pref_noise_std)

        self.n_unique_customer_locs = len(self.coords) - self.n_parcelpoints
        if self.load_data:
            print(
                "\n Note: hygese 0.0.0.8 can throw an assertion error for coordinates below zero; "
                "if that happens, remove the corresponding check in hygese.py.\n"
            )
            self.utils = utils_env(
                Location,
                Vehicle,
                Fleet,
                ParcelPoint,
                ParcelPoints,
                self.veh_capacity,
                self.n_vehicles,
                self.pp_capacity,
                self.fraction_capacitated,
                self.n_parcelpoints,
                self.data,
                self.dist_matrix,
                hgs_time,
            )
            self.depot = self.coords[0]
            self.parcelPoints = self.utils.get_parcelpoints_from_data(
                self.coords[-self.n_parcelpoints:],
                self.n_unique_customer_locs,
            )
            self.get_customer = self.get_new_customer_from_data
            self.num_cust_loc = len(self.dist_matrix) - len(self.parcelPoints["parcelpoints"]) - 1
            self.dist_scaler = np.amax(self.dist_matrix)
        else:
            if self.fraction_capacitated != 0.0:
                print("Generated toy data ignores capacity-limited meeting-point settings; falling back to unlimited capacity.")
                self.fraction_capacitated = 0.0
            self.depot = Location(50, 50, 0, 0)
            self.utils = utils_env(
                Location,
                Vehicle,
                Fleet,
                ParcelPoint,
                ParcelPoints,
                self.veh_capacity,
                self.n_vehicles,
                self.pp_capacity,
                self.fraction_capacitated,
                self.n_parcelpoints,
                self.data,
                self.dist_matrix,
                hgs_time,
            )
            self.parcelPoints = self.utils.get_parcelpoints()
            self.get_customer = self.generate_new_customer
            self.dist_scaler = 10

        self.home_util = home_util
        self.incentive_sens = incentive_sens
        self.dissatisfaction = dissatisfaction

        self.newCustomer = Customer
        self.fleet = get_fleet([self.depot, self.depot], self.n_vehicles, self.veh_capacity)

        self.customerchoice = customerchoicemodel(
            base_util,
            self.dist_scaler,
            travel_time_weight=menu_travel_time_weight,
            pickup_time_weight=menu_pickup_time_weight,
            outside_option_util=outside_option_util,
        )
        self.seed_value = None
        self.request_rng = np.random.RandomState()
        self.choice_rng = np.random.RandomState()
        self.request_trace_episodes = None
        self.request_trace_cursor = 0
        self.active_request_trace = None
        self.active_trace_cursor = 0
        self.customerchoice.set_rng(self.choice_rng)
        self.customerChoice = self.customerchoice.customerchoice_menu
        self.get_delivery_loc = self.get_delivery_loc_menu

        self.steps = 0
        self.reopt_freq = reopt
        self.current_menu = []
        self.last_selected_offer = None
        self.menu_history = []

        self.reset()

    def seed(self, seed):
        self.seed_value = int(seed)
        self.request_rng = np.random.RandomState(self.seed_value)
        self.choice_rng = np.random.RandomState(self.seed_value + 1)
        self.customerchoice.set_rng(self.choice_rng)

    def reset(self, training=True):
        """Reset the simulator state for a new episode."""
        if self.request_trace_episodes is not None:
            trace_idx = self.request_trace_cursor % len(self.request_trace_episodes)
            self.active_request_trace = self.request_trace_episodes[trace_idx]
            self.request_trace_cursor += 1
            self.active_trace_cursor = 0
            self.max_steps = max(len(self.active_request_trace) - 1, 0)
        else:
            self.active_request_trace = None
            self.active_trace_cursor = 0
            self.max_steps = int(self.request_rng.negative_binomial(self.max_steps_r, self.max_steps_p))

        self.fleet = self.utils.reset_fleet(self.fleet, [self.depot, self.depot])
        self.parcelPoints = self.utils.reset_parcelpoints(self.parcelPoints)

        self.steps = 0
        self.service_time = 0
        self.count_home_delivery = 0
        self.total_prices = []
        self.total_discounts = []
        self.current_menu = []
        self.last_selected_offer = None
        self.menu_history = []

        self.data['x_coordinates'] = self.depot.x
        self.data['y_coordinates'] = self.depot.y
        self.data['id'] = 0
        self.data['time'] = 0
        self.data['vehicle_capacity'] = self.veh_capacity
        self.data['num_vehicles'] = self.n_vehicles
        self.data['menu_logs'] = []

        self.count_dissatisfaction = 0

        self.curr_state = self.make_state()
        return self.curr_state

    def _distance_to_destination(self, loc):
        if self.load_data and len(self.dist_matrix) > 0:
            return float(self.dist_matrix[loc.id_num][self.depot.id_num])
        distance = self.utils.getdistance_euclidean(loc, self.depot)
        return float(distance)

    def _initialize_customer_time_preferences(self, customer, rng=None):
        base_travel = self._distance_to_destination(customer.home)
        noise = 0.0
        rng = self.request_rng if rng is None else rng
        if self.menu_pref_noise_std > 0:
            noise = float(rng.normal(0.0, self.menu_pref_noise_std))
        preferred = self.menu_target_arrival_time - base_travel - self.menu_pref_buffer_seconds + noise
        customer.preferred_pickup_time = float(preferred)
        customer.earliest_pickup_time = float(preferred - self.menu_pref_window_half_width)
        customer.latest_pickup_time = float(preferred + self.menu_pref_window_half_width)
        return customer

    def _copy_location(self, coord_index, step):
        base = self.coords[int(coord_index)]
        return Location(float(base.x), float(base.y), int(base.id_num), int(step))

    def _build_customer(self, coord_index, step, preferred_pickup_time=None, earliest_pickup_time=None, latest_pickup_time=None, rng=None):
        coord_index = int(coord_index)
        home = self._copy_location(coord_index, step)
        service_time = float(self.service_times[coord_index])
        customer = Customer(home, self.incentive_sens, self.home_util, service_time, coord_index)
        if preferred_pickup_time is None:
            return self._initialize_customer_time_preferences(customer, rng=rng)
        customer.preferred_pickup_time = float(preferred_pickup_time)
        customer.earliest_pickup_time = float(earliest_pickup_time)
        customer.latest_pickup_time = float(latest_pickup_time)
        return customer

    def _draw_customer(self, rng, step):
        if self.load_data:
            coord_index = int(rng.randint(1, self.num_cust_loc))
        else:
            coord_index = int(rng.randint(0, len(self.coords)))
        return self._build_customer(coord_index, step, rng=rng)

    def _serialize_customer(self, customer):
        return {
            "coord_index": int(customer.id_num),
            "service_time": float(customer.service_time),
            "preferred_pickup_time": float(customer.preferred_pickup_time),
            "earliest_pickup_time": float(customer.earliest_pickup_time),
            "latest_pickup_time": float(customer.latest_pickup_time),
        }

    def _customer_from_trace_entry(self, entry, step):
        return self._build_customer(
            coord_index=entry["coord_index"],
            step=step,
            preferred_pickup_time=entry["preferred_pickup_time"],
            earliest_pickup_time=entry["earliest_pickup_time"],
            latest_pickup_time=entry["latest_pickup_time"],
        )

    def generate_request_traces(self, episodes, seed=None):
        base_seed = self.seed_value if seed is None else int(seed)
        if base_seed is None:
            base_seed = 0
        trace_rng = np.random.RandomState(base_seed)
        traces = []
        for _ in range(int(episodes)):
            max_steps = int(trace_rng.negative_binomial(self.max_steps_r, self.max_steps_p))
            episode_trace = []
            for step in range(max_steps + 1):
                customer = self._draw_customer(trace_rng, step)
                episode_trace.append(self._serialize_customer(customer))
            traces.append(episode_trace)
        return traces

    def set_request_trace(self, traces):
        self.request_trace_episodes = [list(trace) for trace in traces] if traces is not None else None
        self.request_trace_cursor = 0

    def clear_request_trace(self):
        self.request_trace_episodes = None
        self.request_trace_cursor = 0
        self.active_request_trace = None
        self.active_trace_cursor = 0

    def get_new_customer_from_data(self):
        return self._draw_customer(self.request_rng, self.steps)

    def generate_new_customer(self):
        return self._draw_customer(self.request_rng, self.steps)

    def make_state(self):
        if self.active_request_trace is not None:
            self.newCustomer = self._customer_from_trace_entry(
                self.active_request_trace[self.active_trace_cursor],
                self.steps,
            )
            self.active_trace_cursor += 1
        else:
            self.newCustomer = self.get_customer()
        state = [self.newCustomer, self.fleet, self.parcelPoints, self.steps]
        return state

    def is_terminal(self):
        return 1 if self.steps > self.max_steps else 0

    def get_delivery_loc_menu(self, action):
        self.current_menu = list(action)
        return self.customerChoice(self.newCustomer, self.current_menu, self.parcelPoints["parcelpoints"])

    def set_current_menu(self, menu):
        self.current_menu = list(menu)

    def _log_menu_decision(self, displayed_offers, chosen_offer):
        serialized_offers = []
        for offer in displayed_offers:
            serialized_offers.append({
                "bundle_id": offer.bundle_id,
                "meeting_point_id": offer.parcelpoint_id,
                "is_home": offer.is_home,
                "window": offer.window,
                "window_center": float(offer.bundle.window_center),
                "window_width": float(offer.bundle.window_width),
                "remaining_capacity": float(offer.bundle.remaining_capacity),
                "predicted_eta": float(offer.predicted_eta),
                "predicted_in_vehicle_time": float(offer.predicted_in_vehicle_time),
                "walk_distance": float(offer.walk_distance),
                "time_deviation": float(offer.time_deviation),
                "predicted_cost": float(offer.predicted_cost),
                "price": float(offer.price),
                "score": float(offer.score),
                "expected_profit": float(offer.expected_profit),
                "metadata": dict(offer.metadata) if offer.metadata is not None else None,
            })

        chosen_serialized = None
        if chosen_offer is not None:
            chosen_serialized = {
                "bundle_id": chosen_offer.bundle_id,
                "meeting_point_id": chosen_offer.parcelpoint_id,
                "is_home": chosen_offer.is_home,
                "window": chosen_offer.window,
                "window_center": float(chosen_offer.bundle.window_center),
                "window_width": float(chosen_offer.bundle.window_width),
                "remaining_capacity": float(chosen_offer.bundle.remaining_capacity),
                "predicted_eta": float(chosen_offer.predicted_eta),
                "predicted_in_vehicle_time": float(chosen_offer.predicted_in_vehicle_time),
                "walk_distance": float(chosen_offer.walk_distance),
                "time_deviation": float(chosen_offer.time_deviation),
                "predicted_cost": float(chosen_offer.predicted_cost),
                "price": float(chosen_offer.price),
                "score": float(chosen_offer.score),
                "expected_profit": float(chosen_offer.expected_profit),
                "metadata": dict(chosen_offer.metadata) if chosen_offer.metadata is not None else None,
            }

        menu_log = {
            "customer_id": int(self.newCustomer.id_num),
            "preferred_pickup_time": float(self.newCustomer.preferred_pickup_time),
            "earliest_pickup_time": float(self.newCustomer.earliest_pickup_time),
            "latest_pickup_time": float(self.newCustomer.latest_pickup_time),
            "displayed_offers": serialized_offers,
            "chosen_offer": chosen_serialized,
            "opted_out": bool(
                chosen_offer is not None
                and chosen_offer.metadata is not None
                and chosen_offer.metadata.get("opted_out", False)
            ),
        }
        self.menu_history.append(menu_log)
        self.data['menu_logs'].append(menu_log)

    def reopt_for_eval(self, data):
        customer_count = max(len(data['x_coordinates']) - 1, 0)
        if customer_count <= 1:
            return self.utils.fleet_travel_cost(self.fleet, self.depot)
        if self.load_data:
            data["distance_matrix"] = get_dist_mat_HGS(self.dist_matrix, data['id'])
        _, cost = self.utils.reopt_HGS(data)
        return cost

    def _travel_distance_to_choice(self, loc):
        if self.load_data and len(self.dist_matrix) > 0:
            return self.dist_matrix[self.newCustomer.home.id_num][loc.id_num]
        return self.utils.getdistance_euclidean(self.newCustomer.home, loc)

    def step(self, action):
        self.steps += 1

        loc, accepted_pp, idx, price, chosen_offer = self.get_delivery_loc(action)
        self.last_selected_offer = chosen_offer
        self._log_menu_decision(action, chosen_offer)

        if price > 0:
            self.total_prices.append(price)
        else:
            self.total_discounts.append(price)
        self.data['x_coordinates'] = np.append(self.data['x_coordinates'], loc.x)
        self.data['y_coordinates'] = np.append(self.data['y_coordinates'], loc.y)
        self.data['id'] = np.append(self.data['id'], loc.id_num)
        self.data['time'] = np.append(self.data['time'], self.steps)

        if accepted_pp:
            self.parcelPoints["parcelpoints"][idx - self.n_unique_customer_locs].remainingCapacity -= 1
            self.service_time += 0
        else:
            self.service_time += self.newCustomer.service_time
            self.count_home_delivery += 1

        insertVeh, idx, costs = self.utils.cheapestInsertionRoute(loc, self.fleet)
        self.fleet["fleet"][insertVeh]["routePlan"].insert(idx, loc)

        if self.steps % self.reopt_freq == 0:
            if self.load_data:
                self.data["distance_matrix"] = get_dist_mat_HGS(self.dist_matrix, self.data['id'])
            self.fleet, _ = self.utils.reopt_HGS(self.data, fallback_fleet=self.fleet, depot=self.depot)

        stats = (
            self.steps,
            self.count_home_delivery,
            self.service_time,
            self.total_prices,
            self.parcelPoints["parcelpoints"],
            self._travel_distance_to_choice(loc),
            self.total_discounts,
            price,
            self.last_selected_offer,
            self.menu_history[-1] if len(self.menu_history) > 0 else None,
        )

        done = self.is_terminal()
        if done:
            next_state = [self.newCustomer, self.fleet, self.parcelPoints, self.steps]
        else:
            self.curr_state = self.make_state()
            next_state = self.curr_state.copy()
        return next_state, done, stats, self.data
