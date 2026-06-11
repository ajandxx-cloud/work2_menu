from copy import deepcopy
import numpy as np
import torch
import torch.nn as nn
from itertools import combinations
from time import perf_counter
from torch import float32

from Environments.OOH.containers import MenuOffer, ServiceBundle
from Src.Algorithms.DSPO import DSPO
from Src.Utils.MathUtils import lambertw
from Src.Utils.Predictors import CNN_2d, CNN_3d, LinReg
from Src.Utils.Utils import MemoryBuffer, get_dist_mat_HGS
from Src.Utils.option_features import normalize_features, build_option_tensor


class DSPO_Menu(DSPO):
    EXPECTED_PROFIT_POLICIES = {
        "expected_profit_enumeration",
        "service_constrained_expected_profit",
        "risk_adjusted_expected_profit",
        "min_quit_then_profit",
        "service_guarded_expected_profit",
        "profit_oracle",
    }
    REDESIGNED_PROFIT_POLICIES = {
        "risk_adjusted_expected_profit",
        "min_quit_then_profit",
        "service_guarded_expected_profit",
    }
    COST_ORACLE_POLICIES = {"cost_oracle"}

    def __init__(self, config):
        if not getattr(config, "menu_mode", False):
            raise ValueError("DSPO_Menu requires the work2 menu runtime configuration.")

        super(DSPO_Menu, self).__init__(config)

        self.menu_mode = True
        self.get_action = self.get_action_menu
        self.requested_menu_policy = config.menu_policy
        self.menu_policy = config.menu_policy
        self.menu_k = config.menu_k
        self.max_candidates = int(getattr(config, "max_candidates", 10))
        self.candidate_slots = self.max_candidates + 1
        self.menu_keep_home = config.menu_keep_home
        self.menu_use_exact_eval = config.menu_use_exact_eval
        self.menu_exact_threshold = config.menu_exact_threshold
        self.menu_selection_solver = str(getattr(config, "menu_selection_solver", "auto"))
        self.menu_exact_gap_threshold = int(getattr(config, "menu_exact_gap_threshold", self.menu_exact_threshold))
        self.menu_objective_mode = str(getattr(config, "menu_objective_mode", "current"))
        self.menu_time_filtering = bool(config.menu_time_filtering)
        self.pref_window_half_width = float(config.pref_window_half_width)
        self.display_window_half_width = float(config.display_window_half_width)
        self.menu_window_slots_each_side = int(config.menu_window_slots_each_side)
        self.menu_target_arrival_time = float(config.menu_target_arrival_time)
        self.menu_pref_buffer_seconds = float(config.menu_pref_buffer_seconds)
        self.menu_travel_time_weight = float(config.menu_travel_time_weight)
        self.menu_pickup_time_weight = float(config.menu_pickup_time_weight)
        self.menu_score_lambda_margin = float(config.menu_score_lambda_margin)
        self.menu_score_lambda_walk = float(config.menu_score_lambda_walk)
        self.menu_score_lambda_time = float(config.menu_score_lambda_time)
        self.menu_score_lambda_ivt = float(config.menu_score_lambda_ivt)
        self.menu_route_delay_lambda = float(config.menu_route_delay_lambda)
        self.menu_capacity_risk_lambda = float(config.menu_capacity_risk_lambda)
        self.menu_use_time_head = bool(config.menu_use_time_head)
        self.menu_time_prediction_blend = float(config.menu_time_prediction_blend)
        self.menu_time_scale = max(float(config.menu_time_scale), 1.0)
        self.eta_scale = float(config.eta_scale)
        self.menu_use_oracle_eta = bool(getattr(config, "menu_use_oracle_eta", False))
        self.menu_eta_variant = str(getattr(config, "menu_eta_variant", "deployed"))
        self.menu_stronger_eta_gamma = float(getattr(config, "menu_stronger_eta_gamma", 0.5))
        self.menu_pricing_mode = str(getattr(config, "menu_pricing_mode", "lambertw"))
        self.menu_pricing_constant = float(getattr(config, "menu_pricing_constant", -3.0))
        self.service_quit_penalty = float(getattr(config, "service_quit_penalty", 100.0))
        self.service_quit_rate_guardrail = float(getattr(config, "service_quit_rate_guardrail", 0.4))
        self.menu_outside_penalty_lambda = float(getattr(config, "menu_outside_penalty_lambda", 0.0))
        self.menu_quit_tolerance = float(getattr(config, "menu_quit_tolerance", 0.01))
        self.menu_profit_tolerance_fraction = float(getattr(config, "menu_profit_tolerance_fraction", 0.05))
        self.menu_optout_guardrail = float(getattr(config, "menu_optout_guardrail", 0.40))
        if self.menu_use_oracle_eta and self.menu_eta_variant == "deployed":
            self.menu_eta_variant = "oracle"
        if self.menu_eta_variant == "oracle":
            self.menu_use_oracle_eta = True
        self.menu_eta_filter_mode = self._canonical_eta_filter_mode(str(getattr(config, "menu_eta_filter_mode", "hard")))
        self._eta_sigma = float(getattr(config, "menu_eta_sigma", 5703.0))
        self._eta_sigma_source = str(getattr(config, "menu_eta_sigma_source", "global_config"))
        self.menu_eta_chance_threshold = float(getattr(config, "menu_eta_chance_threshold", 0.25))
        self.menu_eta_soft_penalty_lambda = float(getattr(config, "menu_eta_soft_penalty_lambda", 1.0))
        # Preserve legacy semantics: disabling menu_time_filtering must disable ETA pruning
        # even when the newer mode flag is left at its default value.
        if not self.menu_time_filtering:
            self.menu_eta_filter_mode = "none"
        if self.menu_eta_filter_mode == "none":
            self.menu_time_filtering = False
        self.output_dim = 3
        self.aux_dim = 4

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

        self.optimizer = config.optim(self.supervised_ml.parameters(), lr=self.config.learning_rate)
        self.criterion = nn.HuberLoss(delta=1.0)
        self.modules = [('supervised_ml', self.supervised_ml)]
        self.init()

        self.features = np.empty((0, self.n_layers * self.grid_dim * self.grid_dim))
        self.cap_features = np.empty((0, self.aux_dim))
        self.time_targets = np.empty((0, 2))
        self.last_menu = []
        self.last_menu_build_time = 0.0
        self.last_exact_gap_diagnostic = None
        self.last_policy_diagnostic = {}
        self.last_candidate_diagnostics = []
        self.freeze_learning = bool(getattr(config, "freeze_learning", False) or getattr(config, "eval_only", False))

    def reset(self):
        super().reset()
        self.time_targets = np.empty((0, 2))
        self.last_menu = []
        self.last_menu_build_time = 0.0
        self.last_exact_gap_diagnostic = None
        self.last_policy_diagnostic = {}
        self.last_candidate_diagnostics = []

    def _objective_uses_system_eval(self):
        return self.menu_policy == "menu_optimization" or self.menu_policy in self.EXPECTED_PROFIT_POLICIES

    def _pricing_uses_system_eval(self):
        if self.menu_policy in self.EXPECTED_PROFIT_POLICIES:
            return True
        return self.menu_policy == "menu_optimization" and self.menu_objective_mode == "system_profit"

    def _effective_menu_policy(self):
        if self.menu_policy in self.EXPECTED_PROFIT_POLICIES:
            return self.menu_policy
        if self.menu_policy in self.COST_ORACLE_POLICIES:
            return "cost_oracle"
        return self.menu_policy

    def _exact_threshold_for_policy(self):
        if self.menu_policy in self.EXPECTED_PROFIT_POLICIES:
            return max(int(self.menu_exact_threshold), int(self.max_candidates))
        return int(self.menu_exact_threshold)

    def _target_subset_size(self, pool):
        return min(int(self.menu_k), len(pool))

    def _evaluation_cost_kind(self, use_system_eval):
        return "system_eval_cost" if use_system_eval else "menu_eval_cost"

    def _record_offer_trace_costs(self, offer):
        if offer.metadata is None:
            offer.metadata = {}
        menu_cost = self._menu_eval_cost(offer)
        system_cost = self._system_eval_cost(offer)
        metadata = offer.metadata
        metadata["predicted_cost"] = float(offer.predicted_cost)
        metadata["system_minus_menu_cost"] = float(system_cost - menu_cost)
        metadata.setdefault("route_delay", float(metadata.get("route_delay", 0.0)))
        metadata.setdefault("remaining_capacity", float(getattr(offer.bundle, "remaining_capacity", 0.0)))
        return menu_cost, system_cost

    def _eta_risk_penalty_for_offer(self, offer):
        metadata = offer.metadata or {}
        return float(metadata.get("eta_soft_penalty", 0.0))

    def get_prediction(self, cur_feat, home, pps, aux_features=None):
        time_int = min(int(home.time / max(self.interval, 1)), self.n_layers - 1)
        batch_size = 2 + len(pps)
        new_feat = cur_feat.repeat(batch_size, 1, 1, 1)

        if aux_features is None:
            aux = np.zeros((batch_size, self.aux_dim), dtype=np.float32)
            aux[0][0] = 1000000.0
            aux[1][0] = 1000000.0
        else:
            aux = np.asarray(aux_features, dtype=np.float32).reshape(batch_size, self.aux_dim)

        new_feat[1][time_int][self.customer_cell[home.id_num][0]][self.customer_cell[home.id_num][1]] += 1
        for idx, p in enumerate(pps):
            new_feat[idx + 2][time_int][self.customer_cell[p.location.id_num][0]][self.customer_cell[p.location.id_num][1]] += 1
            if aux_features is None:
                aux[idx + 2][0] = max(float(p.remainingCapacity - 1), 0.0)

        with torch.no_grad():
            aux_tensor = torch.tensor(aux, dtype=float32, device=self.device)
            outputs = self.supervised_ml(new_feat.to(self.device), aux_tensor)
        return outputs.detach().cpu().numpy()

    def normalize_eta(self, eta):
        return (float(eta) - self.menu_target_arrival_time) / self.menu_time_scale

    def denormalize_eta(self, eta_norm):
        return float(eta_norm) * self.menu_time_scale + self.menu_target_arrival_time

    def normalize_ivt(self, ivt):
        return float(ivt) / self.menu_time_scale

    def denormalize_ivt(self, ivt_norm):
        return max(0.0, float(ivt_norm) * self.menu_time_scale)

    def derive_preferred_pickup_time(self, customer):
        t_pref = getattr(customer, "preferred_pickup_time", 0.0)
        if t_pref == 0.0:
            base_travel = self._travel_time_to_depot(customer.home)
            t_pref = self.menu_target_arrival_time - base_travel - self.menu_pref_buffer_seconds
            customer.preferred_pickup_time = float(t_pref)
            customer.earliest_pickup_time = float(t_pref - self.pref_window_half_width)
            customer.latest_pickup_time = float(t_pref + self.pref_window_half_width)
        return (
            float(customer.preferred_pickup_time),
            float(customer.earliest_pickup_time),
            float(customer.latest_pickup_time),
        )

    def _travel_time_to_depot(self, loc):
        return self._edge_travel_time(loc, self.depot)

    def _distance_between(self, a, b):
        if self.load_data:
            return float(self.dist_matrix[a.id_num][b.id_num])
        return float(self.getdistance_euclidean(a, b))

    def _default_menu_aux(self, customer, pps):
        center = self.normalize_eta(customer.preferred_pickup_time)
        width = (2.0 * self.display_window_half_width) / self.menu_time_scale
        aux = np.zeros((2 + len(pps), self.aux_dim), dtype=np.float32)
        aux[0] = np.array([1000000.0, center, width, 0.0], dtype=np.float32)
        aux[1] = np.array([1000000.0, center, width, 0.0], dtype=np.float32)
        for idx, pp in enumerate(pps):
            aux[idx + 2] = np.array(
                [max(float(pp.remainingCapacity - 1), 0.0), center, width, 0.0],
                dtype=np.float32,
            )
        return aux

    def _offer_aux_features(self, offer):
        slack_left = max(float(offer.predicted_eta) - float(offer.bundle.window_start), 0.0)
        slack_right = max(float(offer.bundle.window_end) - float(offer.predicted_eta), 0.0)
        slack = min(slack_left, slack_right)
        return np.array(
            [
                1000000.0 if offer.is_home else float(offer.bundle.remaining_capacity),
                self.normalize_eta(offer.bundle.window_center),
                float(offer.bundle.window_width) / self.menu_time_scale,
                float(slack) / self.menu_time_scale,
            ],
            dtype=np.float32,
        )

    def _canonical_eta_filter_mode(self, mode):
        aliases = {
            "interval": "interval_overlap",
            "no_filter": "none",
        }
        canonical = aliases.get(str(mode), str(mode))
        valid = {
            "hard",
            "calibrated",
            "interval_overlap",
            "chance_constraint",
            "soft_penalty",
            "none",
        }
        if canonical not in valid:
            raise ValueError("Unsupported menu_eta_filter_mode: " + str(mode))
        return canonical

    def _normal_cdf(self, x):
        import math
        return 0.5 * (1.0 + math.erf(float(x) / math.sqrt(2.0)))

    def _eta_violation_probability(self, eta, sigma, earliest, latest):
        sigma = max(float(sigma), 0.0)
        eta = float(eta)
        earliest = float(earliest)
        latest = float(latest)
        if sigma <= 1e-12:
            return 0.0 if earliest <= eta <= latest else 1.0
        p_before = self._normal_cdf((earliest - eta) / sigma)
        p_after = 1.0 - self._normal_cdf((latest - eta) / sigma)
        return float(np.clip(p_before + p_after, 0.0, 1.0))

    def _display_windows(self, customer):
        t_pref, _, _ = self.derive_preferred_pickup_time(customer)
        slot_step = max(2.0 * self.display_window_half_width, 1.0)
        centers = [
            t_pref + offset * slot_step
            for offset in range(-self.menu_window_slots_each_side, self.menu_window_slots_each_side + 1)
        ]
        return centers

    def _window_for_eta(self, customer, eta, allow_nearest=False):
        centers = self._display_windows(customer)
        for center in centers:
            if abs(float(eta) - center) <= self.display_window_half_width + 1e-9:
                return (
                    float(center - self.display_window_half_width),
                    float(center + self.display_window_half_width),
                    float(center),
                )
        if not allow_nearest:
            return None
        best_center = min(centers, key=lambda center: abs(float(eta) - center))
        return (
            float(best_center - self.display_window_half_width),
            float(best_center + self.display_window_half_width),
            float(best_center),
        )

    def _eta_filter_result(self, customer, filter_eta, predicted_eta=None, eta_variant="deployed", true_eta=None):
        _, earliest, latest = self.derive_preferred_pickup_time(customer)
        mode = self._canonical_eta_filter_mode(self.menu_eta_filter_mode)
        sigma = max(float(self._eta_sigma), 0.0)
        eta = float(filter_eta)
        predicted_eta = eta if predicted_eta is None else float(predicted_eta)
        true_eta_value = None if true_eta is None else float(true_eta)
        interval_low = eta - sigma
        interval_high = eta + sigma
        violation_probability = self._eta_violation_probability(eta, sigma, earliest, latest)
        soft_distance = max(float(earliest) - eta, 0.0, eta - float(latest))
        soft_penalty = float(self.menu_eta_soft_penalty_lambda * soft_distance / max(self.menu_time_scale, 1.0))
        risk_score = float(violation_probability + soft_penalty)

        eta_pass = True
        prune_reason = ""
        if mode == "hard":
            eta_pass = float(earliest) <= eta <= float(latest)
            prune_reason = "" if eta_pass else "outside_preferred_window"
        elif mode == "calibrated":
            z = 1.2816
            eta_pass = not (eta > float(latest) + z * sigma or eta < float(earliest) - z * sigma)
            prune_reason = "" if eta_pass else "outside_calibrated_window"
        elif mode == "interval_overlap":
            eta_pass = not (interval_high < float(earliest) or interval_low > float(latest))
            prune_reason = "" if eta_pass else "eta_interval_no_overlap"
        elif mode == "chance_constraint":
            eta_pass = violation_probability <= self.menu_eta_chance_threshold + 1e-12
            prune_reason = "" if eta_pass else "violation_probability_above_threshold"
        elif mode in ("soft_penalty", "none"):
            eta_pass = True
            prune_reason = ""

        allow_nearest = mode in ("soft_penalty", "none")
        display_window = self._window_for_eta(customer, eta, allow_nearest=allow_nearest)
        if not eta_pass and mode != "soft_penalty":
            display_window = None
        if display_window is None and eta_pass:
            eta_pass = False
            prune_reason = "outside_display_window"

        retained_in_objective = bool(eta_pass or mode == "soft_penalty")
        diagnostics = {
            "predicted_eta": float(predicted_eta),
            "filter_eta": float(eta),
            "eta_sigma": float(sigma),
            "eta_sigma_source": self._eta_sigma_source,
            "preferred_window_start": float(earliest),
            "preferred_window_end": float(latest),
            "window_start": None if display_window is None else float(display_window[0]),
            "window_end": None if display_window is None else float(display_window[1]),
            "window_center": None if display_window is None else float(display_window[2]),
            "eta_interval_lower": float(interval_low),
            "eta_interval_upper": float(interval_high),
            "eta_filter_passed": bool(eta_pass),
            "prune_reason": prune_reason,
            "violation_probability": float(violation_probability),
            "eta_filter_mode": mode,
            "eta_source": str(eta_variant),
            "eta_variant": str(eta_variant),
            "true_eta": true_eta_value,
            "oracle_eta": true_eta_value,
            "eta_soft_penalty": float(soft_penalty if mode == "soft_penalty" else 0.0),
            "eta_risk_score": float(risk_score),
            "retained_in_objective": retained_in_objective,
            "menu_eta_chance_threshold": float(self.menu_eta_chance_threshold),
        }
        return display_window, diagnostics

    def _choose_display_window(self, customer, eta):
        display_window, _ = self._eta_filter_result(customer, eta)
        return display_window

    def _estimate_in_vehicle_time(self, loc, pred_ivt_norm=None):
        heuristic_ivt = self._travel_time_to_depot(loc)
        if self.menu_use_time_head and (not self.initial_phase) and pred_ivt_norm is not None:
            pred_ivt = self.denormalize_ivt(pred_ivt_norm)
            blended = (1.0 - self.menu_time_prediction_blend) * heuristic_ivt + self.menu_time_prediction_blend * pred_ivt
            return float(max(blended, 0.0)), float(heuristic_ivt)
        return float(heuristic_ivt), float(heuristic_ivt)

    def _estimate_pickup_eta(self, insertion_cost, home_insertion_cost, heuristic_ivt, pred_eta_norm=None):
        route_delay = max(float(insertion_cost) - float(home_insertion_cost), 0.0)
        heuristic_eta = self.menu_target_arrival_time - heuristic_ivt - self.menu_pref_buffer_seconds - self.eta_scale * route_delay
        if self.menu_use_time_head and (not self.initial_phase) and pred_eta_norm is not None:
            pred_eta = self.denormalize_eta(pred_eta_norm)
            blended = (1.0 - self.menu_time_prediction_blend) * heuristic_eta + self.menu_time_prediction_blend * pred_eta
            return float(blended), float(heuristic_eta), float(route_delay)
        return float(heuristic_eta), float(heuristic_eta), float(route_delay)

    def _resolve_eta_variant(self, deployed_eta, heuristic_eta):
        variant = self.menu_eta_variant
        calibration_gamma = float(np.clip(self.menu_stronger_eta_gamma, 0.0, 1.0))
        learned_eta = float(deployed_eta)
        stronger_eta = float(float(heuristic_eta) + calibration_gamma * (float(deployed_eta) - float(heuristic_eta)))
        if variant == "heuristic":
            predicted_eta = float(heuristic_eta)
            filter_eta = float(heuristic_eta)
        elif variant == "stronger":
            predicted_eta = float(stronger_eta)
            filter_eta = float(stronger_eta)
        elif variant == "oracle":
            predicted_eta = float(deployed_eta)
            filter_eta = float(heuristic_eta)
        else:
            predicted_eta = float(deployed_eta)
            filter_eta = float(deployed_eta)
        return {
            "variant": variant,
            "predicted_eta": float(predicted_eta),
            "filter_eta": float(filter_eta),
            "learned_eta": float(learned_eta),
            "stronger_eta": float(stronger_eta),
            "heuristic_eta": float(heuristic_eta),
            "deployed_eta": float(deployed_eta),
            "stronger_weight": float(calibration_gamma),
        }

    def _menu_utility(self, customer, offer, include_price):
        base = self.base_util + (customer.home_util if offer.is_home else 0.0)
        utility = (
            base
            + self.menu_travel_time_weight * float(offer.predicted_in_vehicle_time)
            + self.menu_pickup_time_weight * float(offer.time_deviation)
            - (1.0 - np.exp(-float(offer.walk_distance) / max(self.dist_scaler, 1.0)))
        )
        if include_price:
            utility += customer.incentiveSensitivity * float(offer.price)
        return float(utility)

    def _home_failure_penalty(self):
        return float(self.config.home_failure) * float(self.config.failure_cost)

    def _menu_eval_cost(self, offer):
        eval_cost = float(offer.predicted_cost)
        if offer.is_home:
            eval_cost += self._home_failure_penalty()
        if offer.metadata is None:
            offer.metadata = {}
        offer.metadata["menu_eval_cost"] = float(eval_cost)
        return float(eval_cost)

    def _system_eval_cost(self, offer):
        system_cost = self._menu_eval_cost(offer)
        if not offer.is_home:
            metadata = offer.metadata if offer.metadata is not None else {}
            route_delay = float(metadata.get("route_delay", 0.0))
            capacity = max(float(offer.bundle.remaining_capacity), 0.0)
            route_penalty = self.menu_route_delay_lambda * self.cost_multiplier * route_delay
            capacity_penalty = self.menu_capacity_risk_lambda * 20.0 / (capacity + 0.1)
            system_cost += route_penalty + capacity_penalty
        if offer.metadata is None:
            offer.metadata = {}
        offer.metadata["system_eval_cost"] = float(system_cost)
        return float(system_cost)

    def _price_menu_candidates(self, customer, offers, use_system_eval=False):
        if len(offers) == 0:
            return offers

        sens = float(customer.incentiveSensitivity)
        pricing_mode = self.menu_pricing_mode
        if pricing_mode == "constant":
            pricing_mode = "flat_markdown"
        elif pricing_mode == "zero":
            pricing_mode = "no_pricing"
        cost_fn = self._system_eval_cost if use_system_eval else self._menu_eval_cost
        cost_kind = self._evaluation_cost_kind(use_system_eval)

        if pricing_mode == "cost_plus" or abs(sens) < 1e-8:
            for offer in offers:
                self._record_offer_trace_costs(offer)
                eval_cost = cost_fn(offer)
                offer.price = float(np.clip(eval_cost - self.revenue, self.min_p, self.max_p))
                offer.predicted_utility = self._menu_utility(customer, offer, include_price=True)
                offer.expected_profit = float(offer.price - eval_cost)
                if offer.metadata is None:
                    offer.metadata = {}
                offer.metadata["pricing_mode"] = pricing_mode
                offer.metadata["pricing_eval_cost_kind"] = cost_kind
                offer.metadata["pricing_constant"] = 0.0
                offer.metadata["p_min"] = float(self.min_p)
                offer.metadata["p_max"] = float(self.max_p)
            return offers

        if pricing_mode == "flat_markdown":
            constant_price = float(np.clip(self.menu_pricing_constant, self.min_p, self.max_p))
            for offer in offers:
                self._record_offer_trace_costs(offer)
                eval_cost = cost_fn(offer)
                offer.price = constant_price
                offer.predicted_utility = self._menu_utility(customer, offer, include_price=True)
                offer.expected_profit = float(offer.price - eval_cost)
                if offer.metadata is None:
                    offer.metadata = {}
                offer.metadata["pricing_mode"] = pricing_mode
                offer.metadata["pricing_eval_cost_kind"] = cost_kind
                offer.metadata["pricing_constant"] = float(constant_price)
                offer.metadata["p_min"] = float(self.min_p)
                offer.metadata["p_max"] = float(self.max_p)
            return offers

        if pricing_mode == "no_pricing":
            for offer in offers:
                self._record_offer_trace_costs(offer)
                eval_cost = cost_fn(offer)
                offer.price = 0.0
                offer.predicted_utility = self._menu_utility(customer, offer, include_price=True)
                offer.expected_profit = float(offer.price - eval_cost)
                if offer.metadata is None:
                    offer.metadata = {}
                offer.metadata["pricing_mode"] = pricing_mode
                offer.metadata["pricing_eval_cost_kind"] = cost_kind
                offer.metadata["pricing_constant"] = 0.0
                offer.metadata["p_min"] = float(self.min_p)
                offer.metadata["p_max"] = float(self.max_p)
            return offers

        sum_mnl = 1.0  # include outside option: exp(u_0) = exp(0) = 1
        for offer in offers:
            self._record_offer_trace_costs(offer)
            base_utility = self._menu_utility(customer, offer, include_price=False)
            eval_cost = cost_fn(offer)
            sum_mnl += self._safe_exp(base_utility + sens * (eval_cost - self.revenue))

        lambertw0 = (lambertw(sum_mnl / np.e).real + 1) / sens
        for offer in offers:
            eval_cost = cost_fn(offer)
            offer.price = float(np.clip(eval_cost - self.revenue - lambertw0, self.min_p, self.max_p))
            offer.predicted_utility = self._menu_utility(customer, offer, include_price=True)
            offer.expected_profit = float(offer.price - eval_cost)
            if offer.metadata is None:
                offer.metadata = {}
            offer.metadata["pricing_mode"] = pricing_mode
            offer.metadata["pricing_eval_cost_kind"] = cost_kind
            offer.metadata["pricing_constant"] = float(-lambertw0)
            offer.metadata["p_min"] = float(self.min_p)
            offer.metadata["p_max"] = float(self.max_p)
        return offers

    def score_candidate(self, offer, use_system_eval=False):
        cost_fn = self._system_eval_cost if use_system_eval else self._menu_eval_cost
        margin = float(offer.price - cost_fn(offer))
        walk_pen = float(offer.walk_distance) / max(self.dist_scaler, 1.0)
        time_pen = float(offer.time_deviation) / self.menu_time_scale
        ivt_pen = float(offer.predicted_in_vehicle_time) / self.menu_time_scale
        offer.score = float(
            self.menu_score_lambda_margin * margin
            - self.menu_score_lambda_walk * walk_pen
            - self.menu_score_lambda_time * time_pen
            - self.menu_score_lambda_ivt * ivt_pen
        )
        return offer.score

    def _clone_offers(self, offers):
        return [deepcopy(offer) for offer in offers]

    def evaluate_menu(
        self,
        customer,
        menu,
        return_priced=False,
        already_priced=False,
        use_system_eval=False,
        price_with_system_eval=None,
    ):
        if len(menu) == 0:
            if return_priced:
                return -np.inf, []
            return -np.inf

        priced_menu = list(menu) if already_priced else self._clone_offers(menu)
        price_with_system_eval = bool(False if price_with_system_eval is None else price_with_system_eval)
        if not already_priced:
            self._price_menu_candidates(customer, priced_menu, use_system_eval=price_with_system_eval)

        raw_utilities = np.array(
            [self._menu_utility(customer, offer, include_price=True) for offer in priced_menu],
            dtype=float,
        )
        max_u = np.max(raw_utilities)
        raw_utilities -= max_u
        # Include outside option (u_0=0, shifted by -max_u)
        outside_shifted = float(np.exp(np.clip(0.0 - max_u, -700.0, 700.0)))
        probs = np.exp(np.clip(raw_utilities, -700.0, 700.0))
        denom = max(np.sum(probs) + outside_shifted, 1e-12)
        probs = probs / denom
        outside_probability = float(outside_shifted / denom)

        total_value = 0.0
        cost_fn = self._system_eval_cost if use_system_eval else self._menu_eval_cost
        eval_cost_kind = self._evaluation_cost_kind(use_system_eval)
        for offer, utility, prob in zip(priced_menu, raw_utilities, probs):
            offer.predicted_utility = float(utility)
            self._record_offer_trace_costs(offer)
            eval_cost = cost_fn(offer)
            eta_risk_penalty = self._eta_risk_penalty_for_offer(offer)
            offer.expected_profit = float(prob * (offer.price - eval_cost - eta_risk_penalty))
            if offer.metadata is None:
                offer.metadata = {}
            offer.metadata["choice_probability"] = float(prob)
            offer.metadata["menu_outside_probability"] = float(outside_probability)
            offer.metadata["expected_profit"] = float(offer.expected_profit)
            offer.metadata["evaluation_cost_kind"] = eval_cost_kind
            offer.metadata["menu_objective_mode"] = self.menu_objective_mode
            offer.metadata["eta_risk_penalty"] = float(eta_risk_penalty)
            offer.metadata["eta_risk_penalty_weighted"] = float(prob * eta_risk_penalty)
            total_value += offer.expected_profit
        if return_priced:
            return float(total_value), priced_menu
        return float(total_value)

    def _evaluate_menu_for_objective(self, customer, menu, return_priced=False, already_priced=False):
        return self.evaluate_menu(
            customer,
            menu,
            return_priced=return_priced,
            already_priced=already_priced,
            use_system_eval=self._objective_uses_system_eval(),
            price_with_system_eval=self._pricing_uses_system_eval(),
        )

    def _finalize_menu(self, customer, menu):
        # Two-pass design (no circular dependency):
        # Pass 1 (inside evaluate_menu): price all candidates jointly via Lambert-W,
        #         using the full candidate set M. Prices depend on M.
        # Pass 2: score each candidate using margin = price - eval_cost, valid because
        #         Pass 1 has already set offer.price for every candidate in M.
        use_system_eval = self._objective_uses_system_eval()
        _, priced_menu = self.evaluate_menu(
            customer,
            menu,
            return_priced=True,
            already_priced=False,
            use_system_eval=use_system_eval,
            price_with_system_eval=self._pricing_uses_system_eval(),
        )
        for offer in priced_menu:
            offer.score = self.score_candidate(offer, use_system_eval=use_system_eval)
            if offer.metadata is None:
                offer.metadata = {}
            offer.metadata["menu_objective_mode"] = self.menu_objective_mode
        return priced_menu

    def _singleton_offer_utility(self, customer, home_offer, offer):
        menu = []
        if home_offer is not None and self.menu_keep_home:
            menu.append(home_offer)
        menu.append(offer)
        _, priced_menu = self.evaluate_menu(customer, menu, return_priced=True, already_priced=False)
        for priced_offer in priced_menu:
            if priced_offer.bundle_id == offer.bundle_id:
                return float(priced_offer.predicted_utility)
        return -np.inf

    def enumerate_candidate_subsets(self, candidates, max_size):
        n = len(candidates)
        for subset_size in range(1, min(max_size, n) + 1):
            for subset in combinations(candidates, subset_size):
                yield list(subset)

    def enumerate_fixed_candidate_subsets(self, candidates, subset_size):
        if subset_size <= 0:
            yield []
            return
        for subset in combinations(candidates, min(subset_size, len(candidates))):
            yield list(subset)

    def _build_home_offer(self, customer, home_cost, home_eta, home_ivt, eta_target, ivt_target):
        home_window, eta_diagnostic = self._eta_filter_result(
            customer,
            home_eta,
            predicted_eta=home_eta,
            eta_variant="home",
            true_eta=eta_target,
        )
        if home_window is None:
            home_window = (
                float(home_eta - self.display_window_half_width),
                float(home_eta + self.display_window_half_width),
                float(home_eta),
            )
        bundle = ServiceBundle(
            bundle_id=f"home_{int(home_window[0])}_{int(home_window[1])}",
            location=customer.home,
            is_home=True,
            parcelpoint_id=-1,
            window_start=home_window[0],
            window_end=home_window[1],
            window_center=home_window[2],
            window_width=float(home_window[1] - home_window[0]),
            remaining_capacity=1000000.0,
        )
        return MenuOffer(
            bundle=bundle,
            predicted_cost=float(home_cost),
            price=0.0,
            predicted_eta=float(home_eta),
            predicted_in_vehicle_time=float(home_ivt),
            walk_distance=0.0,
            time_deviation=abs(float(home_eta) - float(customer.preferred_pickup_time)),
            metadata={
                "heuristic_eta": float(eta_target),
                "heuristic_ivt": float(ivt_target),
                "route_delay": 0.0,
                **eta_diagnostic,
            },
        )

    def build_menu_candidates(self, state, training):
        customer = state[0]
        self.derive_preferred_pickup_time(customer)
        theta = self._theta(state[3])
        mltplr = self.cost_multiplier
        pps = self._candidate_parcelpoints(state)
        cur_feat = self.get_feature_rep_infer(state[1]["fleet"])
        outputs = np.asarray(
            self.get_prediction(cur_feat, customer.home, pps, aux_features=self._default_menu_aux(customer, pps))
        )
        if outputs.ndim == 1:
            outputs = outputs.reshape(-1, 1)

        home_insertion = self.cheapestInsertionCosts(customer.home, state[1])
        home_cost = customer.service_time * mltplr + (
            (1 - theta) * home_insertion + theta * (outputs[1][0] - outputs[0][0])
        )
        home_ivt, home_ivt_target = self._estimate_in_vehicle_time(
            customer.home,
            pred_ivt_norm=outputs[1][2] if outputs.shape[1] > 2 else None,
        )
        home_eta, home_eta_target, _ = self._estimate_pickup_eta(
            home_insertion,
            home_insertion,
            home_ivt_target,
            pred_eta_norm=outputs[1][1] if outputs.shape[1] > 1 else None,
        )
        home_eta_choice = self._resolve_eta_variant(home_eta, home_eta_target)

        home_offer_obj = self._build_home_offer(
            customer,
            home_cost=home_cost,
            home_eta=home_eta_choice["predicted_eta"],
            home_ivt=home_ivt,
            eta_target=home_eta_target,
            ivt_target=home_ivt_target,
        )
        if home_offer_obj.metadata is None:
            home_offer_obj.metadata = {}
        home_offer_obj.metadata.update({
            "eta_variant": home_eta_choice["variant"],
            "filter_eta": float(home_eta_choice["filter_eta"]),
            "deployed_eta": float(home_eta_choice["deployed_eta"]),
            "learned_eta": float(home_eta_choice["learned_eta"]),
            "stronger_eta": float(home_eta_choice["stronger_eta"]),
            "stronger_weight": float(home_eta_choice["stronger_weight"]),
        })
        candidates = [home_offer_obj]  # always include home so pricing reference is intact

        feasible_count = 0
        pruned_by_eta_count = 0
        fn_pruned_near = 0
        fn_pruned_mid = 0
        fn_pruned_far = 0
        candidate_diagnostics = []
        if home_offer_obj.metadata is not None:
            home_diag = dict(home_offer_obj.metadata)
            home_diag.update({
                "candidate_type": "home",
                "bundle_id": home_offer_obj.bundle_id,
                "parcelpoint_id": -1,
            })
            candidate_diagnostics.append(home_diag)

        for idx, pp in enumerate(pps):
            if pp.remainingCapacity <= 0:
                continue

            feasible_count += 1
            insertion_cost = self.cheapestInsertionCosts(pp.location, state[1])
            pp_cost = mltplr * (
                (1 - theta) * insertion_cost + theta * (outputs[idx + 2][0] - outputs[0][0])
            )
            ivt_pp, ivt_target = self._estimate_in_vehicle_time(
                pp.location,
                pred_ivt_norm=outputs[idx + 2][2] if outputs.shape[1] > 2 else None,
            )
            eta_pp, eta_target, route_delay = self._estimate_pickup_eta(
                insertion_cost,
                home_insertion,
                ivt_target,
                pred_eta_norm=outputs[idx + 2][1] if outputs.shape[1] > 1 else None,
            )
            eta_choice = self._resolve_eta_variant(eta_pp, eta_target)
            display_window, eta_diagnostic = self._eta_filter_result(
                customer,
                eta_choice["filter_eta"],
                predicted_eta=eta_choice["predicted_eta"],
                eta_variant=eta_choice["variant"],
                true_eta=eta_target,
            )
            eta_diagnostic.update({
                "candidate_type": "meeting_point",
                "parcelpoint_id": int(pp.id_num),
            })
            if display_window is None:
                pruned_by_eta_count += 1
                walk_dist_pruned = self._distance_between(customer.home, pp.location)
                eta_diagnostic.update({
                    "walk_distance": float(walk_dist_pruned),
                    "retained_in_objective": False,
                    "bundle_id": f"pp_{pp.id_num}_pruned_eta",
                })
                candidate_diagnostics.append(dict(eta_diagnostic))
                if walk_dist_pruned < 500:
                    fn_pruned_near += 1
                elif walk_dist_pruned < 1500:
                    fn_pruned_mid += 1
                else:
                    fn_pruned_far += 1
                continue

            walk_dist = self._distance_between(customer.home, pp.location)
            bundle = ServiceBundle(
                bundle_id=f"pp_{pp.id_num}_{int(display_window[0])}_{int(display_window[1])}",
                location=pp.location,
                is_home=False,
                parcelpoint_id=int(pp.id_num),
                window_start=display_window[0],
                window_end=display_window[1],
                window_center=display_window[2],
                window_width=float(display_window[1] - display_window[0]),
                remaining_capacity=float(pp.remainingCapacity),
            )
            candidates.append(
                MenuOffer(
                    bundle=bundle,
                    predicted_cost=float(pp_cost),
                    price=0.0,
                    predicted_eta=float(eta_choice["predicted_eta"]),
                    predicted_in_vehicle_time=float(ivt_pp),
                    walk_distance=float(walk_dist),
                    time_deviation=abs(float(eta_choice["predicted_eta"]) - float(customer.preferred_pickup_time)),
                    metadata={
                        "insertion_cost": float(insertion_cost),
                        "eta_variant": eta_choice["variant"],
                        "filter_eta": float(eta_choice["filter_eta"]),
                        "deployed_eta": float(eta_choice["deployed_eta"]),
                        "learned_eta": float(eta_choice["learned_eta"]),
                        "stronger_eta": float(eta_choice["stronger_eta"]),
                        "stronger_weight": float(eta_choice["stronger_weight"]),
                        "heuristic_eta": float(eta_target),
                        "heuristic_ivt": float(ivt_target),
                        "route_delay": float(route_delay),
                        "true_eta": float(eta_target),
                        "true_ivt": float(ivt_target),
                        **eta_diagnostic,
                    },
                )
            )
            candidate_diagnostics.append({
                **eta_diagnostic,
                "bundle_id": candidates[-1].bundle_id,
                "walk_distance": float(walk_dist),
            })

        deduped = {}
        for offer in candidates:
            deduped[offer.bundle_id] = offer

        fn_pruning_rate = float(pruned_by_eta_count) / float(feasible_count) if feasible_count > 0 else 0.0
        for offer in deduped.values():
            if offer.metadata is None:
                offer.metadata = {}
            offer.metadata.setdefault("fn_pruning_rate", fn_pruning_rate)
            offer.metadata.setdefault("feasible_candidate_count", feasible_count)
            offer.metadata.setdefault("pruned_by_eta_count", pruned_by_eta_count)
            offer.metadata.setdefault("fn_pruned_near", fn_pruned_near)
            offer.metadata.setdefault("fn_pruned_mid", fn_pruned_mid)
            offer.metadata.setdefault("fn_pruned_far", fn_pruned_far)
            offer.metadata.setdefault("candidate_diagnostic_count", len(candidate_diagnostics))

        self.last_candidate_diagnostics = candidate_diagnostics
        return list(deduped.values())

    def build_option_features(self, state, pps, customer):
        """Build per-candidate 6-dim feature tensors for downstream models.

        Feature vector per candidate [walk_distance, predicted_ivt,
        remaining_capacity, distance_to_destination, option_type,
        arrival_time].

        Args:
            state: [Customer, Fleet, ParcelPoints, steps]
            pps:   list of candidate ParcelPoint objects (already filtered
                   by adjacency and positive capacity).
            customer: Customer object (convenience, same as state[0]).

        Returns:
            features: Tensor[K, 6]  K = 1 (home) + len(pps)
            mask:     Tensor[K]     bool — True for valid candidates
        """
        self.derive_preferred_pickup_time(customer)

        walk_distances = []
        ivts = []
        capacities = []
        dest_distances = []
        option_types = []
        arrival_times = []

        # --- Home candidate (index 0) ---
        home_ivt = 0.0
        home_dest = self._travel_time_to_depot(customer.home)
        home_eta = self.menu_target_arrival_time - home_ivt - self.menu_pref_buffer_seconds
        walk_distances.append(0.0)
        ivts.append(home_ivt)
        capacities.append(1000000.0)
        dest_distances.append(home_dest)
        option_types.append(1.0)
        arrival_times.append(home_eta)

        # --- Parcel point candidates ---
        for pp in pps:
            if pp.remainingCapacity <= 0:
                continue
            loc = pp.location
            walk = self._distance_between(customer.home, loc)
            ivt = self._travel_time_to_depot(loc)
            eta = self.menu_target_arrival_time - ivt - self.menu_pref_buffer_seconds
            walk_distances.append(walk)
            ivts.append(ivt)
            capacities.append(float(pp.remainingCapacity))
            dest_distances.append(ivt)  # distance_to_depot == ivt for real data
            option_types.append(0.0)
            arrival_times.append(eta)

        k = len(walk_distances)
        if k == 0:
            features = torch.zeros((self.candidate_slots, 6), dtype=torch.float32, device=self.device)
            mask = torch.zeros(self.candidate_slots, dtype=torch.bool, device=self.device)
            return features, mask

        raw = {
            "walk_distance": np.array(walk_distances),
            "predicted_ivt": np.array(ivts),
            "remaining_capacity": np.array(capacities),
            "distance_to_destination": np.array(dest_distances),
            "option_type": np.array(option_types),
            "arrival_time": np.array(arrival_times),
        }
        normed = normalize_features(raw, self.menu_time_scale, self.menu_target_arrival_time)
        return build_option_tensor(normed, max_k=self.candidate_slots, device=self.device)

    def build_candidate_cost_labels(self, state, pps, customer=None, fill_value=0.0):
        """Build true insertion-cost labels aligned to option feature rows.

        Public K counts meeting-point candidates only. The returned tensor has
        candidate_slots = K + 1 rows: home at index 0, meeting points at
        indices 1..K, and padding filled with a harmless value that callers
        exclude via option_mask.
        """
        customer = customer or state[0]
        fleet_info = state[1]
        labels = [self.cost_multiplier * self.cheapestInsertionCosts(customer.home, fleet_info)]
        for pp in pps[: self.max_candidates]:
            if getattr(pp, "remainingCapacity", 0) > 0:
                labels.append(self.cost_multiplier * self.cheapestInsertionCosts(pp.location, fleet_info))
            else:
                labels.append(float(fill_value))
        while len(labels) < self.candidate_slots:
            labels.append(float(fill_value))
        return torch.tensor(labels[: self.candidate_slots], dtype=float32, device=self.device)

    def _split_menu_candidates(self, candidates):
        home_offer = None
        ooh_offers = []
        for offer in candidates:
            if offer.is_home:
                home_offer = offer
            else:
                ooh_offers.append(offer)
        return home_offer, ooh_offers

    def _solver_diagnostic(
        self,
        effective_solver,
        candidate_count,
        enumerated_count=0,
        fallback_used=False,
        fallback_reason="",
        selected_value=None,
    ):
        diagnostic = {
            "menu_selection_solver_requested": str(self.menu_selection_solver),
            "menu_selection_solver_effective": str(effective_solver),
            "effective_menu_selection_solver": str(effective_solver),
            "solver_candidate_count": int(candidate_count),
            "exact_gap_candidate_count": int(candidate_count),
            "exact_enumerated_menu_count": int(enumerated_count),
            "solver_fallback_used": bool(fallback_used),
            "solver_fallback_reason": str(fallback_reason),
            "exact_gap_logged": bool(enumerated_count > 0),
            "effective_menu_policy": self._effective_menu_policy(),
        }
        if selected_value is not None and selected_value > -np.inf:
            diagnostic["exact_menu_value"] = float(selected_value)
        return diagnostic

    def _merge_policy_diagnostic(self, diagnostic):
        merged = dict(self.last_policy_diagnostic or {})
        merged.update(diagnostic)
        self.last_policy_diagnostic = merged
        return merged

    def _select_menu_exact(self, customer, home_offer, ooh_candidates):
        base_menu = [home_offer] if home_offer is not None and self.menu_keep_home else []
        # When keep_home=False, home is an optional candidate counted toward menu_k
        optional_home = [] if (home_offer is None or self.menu_keep_home) else [home_offer]
        pool = optional_home + ooh_candidates
        if len(pool) == 0:
            return list(base_menu)

        best_menu = None
        best_value = -np.inf
        if self.menu_policy in self.EXPECTED_PROFIT_POLICIES:
            subset_iter = self.enumerate_fixed_candidate_subsets(pool, self._target_subset_size(pool))
        else:
            subset_iter = self.enumerate_candidate_subsets(pool, self.menu_k)
        enumerated_count = 0
        for subset in subset_iter:
            enumerated_count += 1
            menu = list(base_menu) + subset
            value = self._evaluate_menu_for_objective(customer, menu)
            if value > best_value:
                best_value = value
                best_menu = menu
        self._merge_policy_diagnostic(self._solver_diagnostic(
            "exact",
            len(ooh_candidates),
            enumerated_count=enumerated_count,
            selected_value=best_value,
        ))
        return best_menu if best_menu is not None else list(base_menu)

    def _select_menu_service_constrained(self, customer, home_offer, ooh_candidates):
        base_menu = [home_offer] if home_offer is not None and self.menu_keep_home else []
        optional_home = [] if (home_offer is None or self.menu_keep_home) else [home_offer]
        pool = optional_home + ooh_candidates
        if len(pool) == 0:
            self.last_policy_diagnostic = {
                "effective_menu_policy": self._effective_menu_policy(),
                "service_constrained_fallback_used": False,
                "service_constrained_fallback_reason": "no_non_home_candidates",
                "exact_enumerated_menu_count": 0,
                "exact_gap_candidate_count": int(len(ooh_candidates)),
            }
            return list(base_menu)

        best_feasible_menu = None
        best_feasible_value = -np.inf
        best_feasible_outside = None
        best_adjusted_menu = None
        best_adjusted_value = -np.inf
        best_adjusted_profit = -np.inf
        best_adjusted_outside = None
        enumerated_count = 0
        target_size = self._target_subset_size(pool)

        for subset in self.enumerate_fixed_candidate_subsets(pool, target_size):
            enumerated_count += 1
            menu = list(base_menu) + subset
            value, priced_menu = self._evaluate_menu_for_objective(customer, menu, return_priced=True)
            outside_probability = 1.0
            if priced_menu:
                metadata = priced_menu[0].metadata or {}
                outside_probability = float(metadata.get("menu_outside_probability", 1.0))
            adjusted_value = float(value) - self.service_quit_penalty * outside_probability
            if outside_probability <= self.service_quit_rate_guardrail + 1e-12 and value > best_feasible_value:
                best_feasible_value = float(value)
                best_feasible_menu = menu
                best_feasible_outside = outside_probability
            if adjusted_value > best_adjusted_value:
                best_adjusted_value = float(adjusted_value)
                best_adjusted_profit = float(value)
                best_adjusted_menu = menu
                best_adjusted_outside = outside_probability

        fallback_used = best_feasible_menu is None
        selected_menu = best_adjusted_menu if fallback_used else best_feasible_menu
        selected_value = best_adjusted_profit if fallback_used else best_feasible_value
        selected_adjusted_value = best_adjusted_value if fallback_used else (
            best_feasible_value - self.service_quit_penalty * float(best_feasible_outside or 0.0)
        )
        selected_outside = best_adjusted_outside if fallback_used else best_feasible_outside
        self.last_policy_diagnostic = {
            "effective_menu_policy": self._effective_menu_policy(),
            "exact_enumerated_menu_count": int(enumerated_count),
            "exact_gap_candidate_count": int(len(ooh_candidates)),
            "exact_menu_value": float(selected_value) if selected_value > -np.inf else None,
            "exact_gap_logged": True,
            "service_constrained_fallback_used": bool(fallback_used),
            "service_constrained_fallback_reason": "no_guardrail_feasible_menu" if fallback_used else "",
            "service_constrained_predicted_opt_out": float(selected_outside or 0.0),
            "service_constrained_adjusted_profit": float(selected_adjusted_value),
            "service_quit_rate_guardrail": float(self.service_quit_rate_guardrail),
        }
        self._merge_policy_diagnostic(self._solver_diagnostic(
            "exact",
            len(ooh_candidates),
            enumerated_count=enumerated_count,
            fallback_used=fallback_used,
            fallback_reason="no_guardrail_feasible_menu" if fallback_used else "",
            selected_value=selected_value,
        ))
        return selected_menu if selected_menu is not None else list(base_menu)

    def _redesign_family(self):
        if self.menu_policy == "risk_adjusted_expected_profit":
            return "risk_adjusted"
        if self.menu_policy == "min_quit_then_profit":
            return "min_quit_then_profit"
        if self.menu_policy == "service_guarded_expected_profit":
            return "service_guarded"
        return ""

    def _redesign_menu_components(self, customer, menu):
        value, priced_menu = self._evaluate_menu_for_objective(customer, menu, return_priced=True)
        outside_probability = 1.0
        system_eval_cost = 0.0
        eta_risk_penalty_total = 0.0
        if priced_menu:
            metadata = priced_menu[0].metadata or {}
            outside_probability = float(metadata.get("menu_outside_probability", 1.0))
            for offer in priced_menu:
                offer_metadata = offer.metadata or {}
                eta_risk_penalty_total += float(offer_metadata.get("eta_risk_penalty_weighted", 0.0))
                if offer_metadata.get("system_eval_cost") is not None:
                    system_eval_cost += float(offer_metadata.get("system_eval_cost"))
                else:
                    system_eval_cost += float(self._system_eval_cost(offer))
        risk_adjusted_score = float(value) - self.menu_outside_penalty_lambda * outside_probability
        return {
            "menu": menu,
            "predicted_expected_system_profit": float(value),
            "predicted_outside_probability": float(outside_probability),
            "risk_adjusted_score": float(risk_adjusted_score),
            "system_eval_cost": float(system_eval_cost),
            "eta_risk_penalty_total": float(eta_risk_penalty_total),
        }

    def _choose_redesigned_menu(self, evaluated):
        if not evaluated:
            return None, {}

        fallback_used = False
        fallback_reason = ""
        if self.menu_policy == "risk_adjusted_expected_profit":
            selected = max(
                evaluated,
                key=lambda item: (
                    item["risk_adjusted_score"],
                    item["predicted_expected_system_profit"],
                    -item["predicted_outside_probability"],
                ),
            )
        elif self.menu_policy == "min_quit_then_profit":
            min_outside = min(item["predicted_outside_probability"] for item in evaluated)
            outside_limit = min_outside + max(self.menu_quit_tolerance, 0.0)
            eligible = [
                item for item in evaluated
                if item["predicted_outside_probability"] <= outside_limit + 1e-12
            ]
            best_profit = max(item["predicted_expected_system_profit"] for item in eligible)
            tolerance = abs(best_profit) * max(self.menu_profit_tolerance_fraction, 0.0)
            near_best = [
                item for item in eligible
                if item["predicted_expected_system_profit"] >= best_profit - tolerance - 1e-12
            ]
            selected = min(
                near_best,
                key=lambda item: (
                    item["predicted_outside_probability"],
                    -item["predicted_expected_system_profit"],
                    item["system_eval_cost"],
                ),
            )
        elif self.menu_policy == "service_guarded_expected_profit":
            feasible = [
                item for item in evaluated
                if item["predicted_outside_probability"] <= self.menu_optout_guardrail + 1e-12
            ]
            if feasible:
                selected = max(
                    feasible,
                    key=lambda item: (
                        item["predicted_expected_system_profit"],
                        -item["predicted_outside_probability"],
                    ),
                )
            else:
                fallback_used = True
                fallback_reason = "no_guardrail_feasible_menu"
                selected = min(
                    evaluated,
                    key=lambda item: (
                        item["predicted_outside_probability"],
                        -item["predicted_expected_system_profit"],
                    ),
                )
        else:
            selected = max(evaluated, key=lambda item: item["predicted_expected_system_profit"])

        min_outside = min(item["predicted_outside_probability"] for item in evaluated)
        diagnostics = {
            "effective_menu_policy": self._effective_menu_policy(),
            "redesign_policy_family": self._redesign_family(),
            "redesign_fallback_used": bool(fallback_used),
            "redesign_fallback_reason": fallback_reason,
            "predicted_expected_system_profit": float(selected["predicted_expected_system_profit"]),
            "predicted_outside_probability": float(selected["predicted_outside_probability"]),
            "risk_adjusted_score": float(selected["risk_adjusted_score"]),
            "selected_predicted_expected_system_profit": float(selected["predicted_expected_system_profit"]),
            "selected_predicted_outside_probability": float(selected["predicted_outside_probability"]),
            "min_predicted_outside_probability": float(min_outside),
            "eta_risk_penalty_total": float(selected.get("eta_risk_penalty_total", 0.0)),
            "menu_outside_penalty_lambda": float(self.menu_outside_penalty_lambda),
            "menu_quit_tolerance": float(self.menu_quit_tolerance),
            "menu_profit_tolerance_fraction": float(self.menu_profit_tolerance_fraction),
            "menu_optout_guardrail": float(self.menu_optout_guardrail),
        }
        return selected["menu"], diagnostics

    def _select_menu_redesigned(self, customer, home_offer, ooh_candidates):
        base_menu = [home_offer] if home_offer is not None and self.menu_keep_home else []
        optional_home = [] if (home_offer is None or self.menu_keep_home) else [home_offer]
        pool = optional_home + ooh_candidates
        if len(pool) == 0:
            self.last_policy_diagnostic = {
                "effective_menu_policy": self._effective_menu_policy(),
                "redesign_policy_family": self._redesign_family(),
                "redesign_fallback_used": False,
                "redesign_fallback_reason": "no_non_home_candidates",
                "exact_enumerated_menu_count": 0,
                "exact_gap_candidate_count": int(len(ooh_candidates)),
            }
            return list(base_menu)

        target_size = self._target_subset_size(pool)
        evaluated = []
        enumerated_count = 0
        exact_used = len(ooh_candidates) <= self._exact_threshold_for_policy()
        if exact_used:
            subset_iter = self.enumerate_fixed_candidate_subsets(pool, target_size)
            for subset in subset_iter:
                enumerated_count += 1
                menu = list(base_menu) + subset
                evaluated.append(self._redesign_menu_components(customer, menu))
            selected_menu, diagnostics = self._choose_redesigned_menu(evaluated)
        else:
            current_menu = list(base_menu)
            remaining = list(pool)
            selected_menu = list(base_menu)
            diagnostics = {}
            for _ in range(target_size):
                step_evaluated = []
                for offer in remaining:
                    enumerated_count += 1
                    step_evaluated.append(self._redesign_menu_components(customer, current_menu + [offer]))
                step_menu, step_diagnostics = self._choose_redesigned_menu(step_evaluated)
                if step_menu is None:
                    break
                added_ids = {offer.bundle_id for offer in step_menu} - {offer.bundle_id for offer in current_menu}
                added = next((offer for offer in remaining if offer.bundle_id in added_ids), None)
                if added is None:
                    break
                current_menu.append(added)
                selected_menu = list(current_menu)
                diagnostics = step_diagnostics
                remaining = [offer for offer in remaining if offer.bundle_id != added.bundle_id]
                if not remaining:
                    break

        if selected_menu is None:
            selected_menu = list(base_menu)
        diagnostics.update({
            "exact_enumerated_menu_count": int(enumerated_count if exact_used else 0),
            "exact_gap_candidate_count": int(len(ooh_candidates)),
            "exact_gap_logged": bool(exact_used),
        })
        diagnostics.update(self._solver_diagnostic(
            "exact" if exact_used else "greedy",
            len(ooh_candidates),
            enumerated_count=enumerated_count if exact_used else 0,
            fallback_used=not exact_used,
            fallback_reason="" if exact_used else "above_exact_threshold",
            selected_value=diagnostics.get("predicted_expected_system_profit"),
        ))
        self.last_policy_diagnostic = diagnostics
        return selected_menu

    def _menu_bundle_ids(self, menu):
        return {offer.bundle_id for offer in menu if not offer.is_home}

    def _menu_overlap_rate(self, first_menu, second_menu):
        first = self._menu_bundle_ids(first_menu)
        second = self._menu_bundle_ids(second_menu)
        denom = max(len(first | second), 1)
        return float(len(first & second) / denom)

    def _maybe_log_exact_gap_diagnostic(self, customer, home_offer, ooh_candidates):
        self.last_exact_gap_diagnostic = None
        if self.menu_policy != "menu_optimization":
            return
        if len(ooh_candidates) == 0 or len(ooh_candidates) > self.menu_exact_gap_threshold:
            return

        exact_start = perf_counter()
        exact_menu = self._select_menu_exact(customer, home_offer, ooh_candidates)
        exact_time = perf_counter() - exact_start

        greedy_start = perf_counter()
        greedy_menu = self._select_menu_greedy(customer, home_offer, ooh_candidates)
        greedy_time = perf_counter() - greedy_start

        exact_value = float(self._evaluate_menu_for_objective(customer, exact_menu))
        greedy_value = float(self._evaluate_menu_for_objective(customer, greedy_menu))
        scale = max(abs(exact_value), 1e-9)
        relative_gap = max(0.0, (exact_value - greedy_value) / scale)

        self.last_exact_gap_diagnostic = {
            "exact_menu_value": exact_value,
            "greedy_menu_value": greedy_value,
            "relative_optimality_gap": float(relative_gap),
            "menu_overlap_rate": self._menu_overlap_rate(exact_menu, greedy_menu),
            "exact_build_time": float(exact_time),
            "greedy_build_time": float(greedy_time),
            "exact_gap_candidate_count": int(len(ooh_candidates)),
            "exact_gap_logged": True,
        }

    def _select_menu_greedy(self, customer, home_offer, ooh_candidates):
        base_menu = [home_offer] if home_offer is not None and self.menu_keep_home else []
        # When keep_home=False, home is an optional candidate counted toward menu_k
        optional_home = [] if (home_offer is None or self.menu_keep_home) else [home_offer]
        pool = optional_home + ooh_candidates
        if len(pool) == 0:
            return list(base_menu)

        best_offer = None
        best_value = -np.inf
        for offer in pool:
            trial_menu = list(base_menu) + [offer]
            trial_value = self._evaluate_menu_for_objective(customer, trial_menu)
            if trial_value > best_value:
                best_value = trial_value
                best_offer = offer

        current_menu = list(base_menu) + ([best_offer] if best_offer is not None else [])
        current_value = best_value
        if best_offer is None:
            return list(base_menu)
        remaining = [offer for offer in pool if offer.bundle_id != best_offer.bundle_id]

        def _menu_size_ok(menu):
            if self.menu_keep_home:
                return len([o for o in menu if not o.is_home]) < self.menu_k
            else:
                return len(menu) < self.menu_k

        while _menu_size_ok(current_menu) and len(remaining) > 0:
            best_offer = None
            best_delta = -np.inf
            for offer in remaining:
                trial_menu = current_menu + [offer]
                trial_value = self._evaluate_menu_for_objective(customer, trial_menu)
                delta = trial_value - current_value
                if delta > best_delta:
                    best_delta = delta
                    best_offer = offer
            # Always add the best remaining candidate to fill menu_k slots,
            # even if marginal value is negative.  This ensures the model's
            # ranking quality drives the selection rather than early stopping.
            if best_offer is None:
                break
            current_menu.append(best_offer)
            remaining = [offer for offer in remaining if offer.bundle_id != best_offer.bundle_id]
            current_value += best_delta
        return current_menu

    def _select_menu_candidates(self, customer, candidates):
        self.last_policy_diagnostic = {}
        home_offer, ooh_candidates = self._split_menu_candidates(candidates)

        if self.menu_policy == "offer_all_feasible_bundles":
            menu = list(candidates)
        elif self.menu_policy == "nearest_heuristic":
            selected = sorted(ooh_candidates, key=lambda offer: (offer.walk_distance, offer.time_deviation))[:self.menu_k]
            menu = ([home_offer] if home_offer is not None and self.menu_keep_home else []) + selected
        elif self.menu_policy == "top_k_cheapest":
            selected = sorted(ooh_candidates, key=lambda offer: offer.predicted_cost)[:self.menu_k]
            menu = ([home_offer] if home_offer is not None and self.menu_keep_home else []) + selected
        elif self.menu_policy == "top_k_passenger_utility":
            selected = sorted(
                ooh_candidates,
                key=lambda offer: self._singleton_offer_utility(customer, home_offer, offer),
                reverse=True,
            )[:self.menu_k]
            menu = ([home_offer] if home_offer is not None and self.menu_keep_home else []) + selected
        elif self.menu_policy == "revenue_greedy":
            # Revenue-greedy: select k bundles with highest pairwise expected revenue
            # pi(b|{b0,b}) * p_b, evaluated against home bundle.
            # Equivalent to score function with mu_w = mu_t = mu_v = 0.
            def _pairwise_revenue(offer):
                pair = []
                if home_offer is not None and self.menu_keep_home:
                    pair.append(home_offer)
                pair.append(offer)
                cloned = self._clone_offers(pair)
                self._price_menu_candidates(customer, cloned)
                raw_utils = [self._menu_utility(customer, o, include_price=True) for o in cloned]
                raw_utils_arr = [u - max(raw_utils) for u in raw_utils]
                probs = [max(0.0, u) for u in raw_utils_arr]
                import math
                exp_utils = [math.exp(max(u, -700.0)) for u in raw_utils_arr]
                denom = max(sum(exp_utils), 1e-12)
                for o, eu in zip(cloned, exp_utils):
                    if o.bundle_id == offer.bundle_id:
                        return (eu / denom) * o.price
                return -float('inf')
            selected = sorted(ooh_candidates, key=_pairwise_revenue, reverse=True)[:self.menu_k]
            menu = ([home_offer] if home_offer is not None and self.menu_keep_home else []) + selected
        elif self.menu_policy == "insertion_cost_greedy":
            # Dispatch heuristic: select k candidates with cheapest real-time insertion cost.
            selected = sorted(ooh_candidates, key=lambda offer: offer.predicted_cost)[:self.menu_k]
            menu = ([home_offer] if home_offer is not None and self.menu_keep_home else []) + selected
        elif self.menu_policy == "min_lateness":
            # Schedule-aware dispatch: select k candidates with minimum pickup time deviation.
            selected = sorted(ooh_candidates, key=lambda offer: offer.time_deviation)[:self.menu_k]
            menu = ([home_offer] if home_offer is not None and self.menu_keep_home else []) + selected
        elif self.menu_policy == "random_top_k":
            # Floor baseline: randomly sample k candidates for performance lower-bound context.
            import random
            k = min(self.menu_k, len(ooh_candidates))
            selected = random.sample(ooh_candidates, k=k)
            menu = ([home_offer] if home_offer is not None and self.menu_keep_home else []) + selected
        elif self.menu_policy == "home_only":
            menu = [home_offer] if home_offer is not None else []
        elif self.menu_policy == "cost_l_heuristic":
            selected = sorted(ooh_candidates, key=lambda offer: offer.metadata.get("insertion_cost", float("inf")))[:self.menu_k]
            menu = ([home_offer] if home_offer is not None and self.menu_keep_home else []) + selected
        elif self.menu_policy == "cost_oracle":
            selected = sorted(ooh_candidates, key=lambda offer: offer.metadata.get("insertion_cost", float("inf")))[:self.menu_k]
            menu = ([home_offer] if home_offer is not None and self.menu_keep_home else []) + selected
            self.last_policy_diagnostic = {"effective_menu_policy": self._effective_menu_policy()}
        elif self.menu_policy in self.REDESIGNED_PROFIT_POLICIES:
            menu = self._select_menu_redesigned(customer, home_offer, ooh_candidates)
        elif self.menu_policy == "service_constrained_expected_profit":
            menu = self._select_menu_service_constrained(customer, home_offer, ooh_candidates)
        elif self.menu_policy in {"expected_profit_enumeration", "profit_oracle"}:
            if len(ooh_candidates) <= self._exact_threshold_for_policy():
                menu = self._select_menu_exact(customer, home_offer, ooh_candidates)
            else:
                menu = self._select_menu_greedy(customer, home_offer, ooh_candidates)
                self.last_policy_diagnostic = self._solver_diagnostic(
                    "greedy",
                    len(ooh_candidates),
                    fallback_used=True,
                    fallback_reason="above_exact_threshold",
                )
        else:
            self._maybe_log_exact_gap_diagnostic(customer, home_offer, ooh_candidates)
            fallback_used = False
            fallback_reason = ""
            if self.menu_selection_solver == "greedy":
                menu = self._select_menu_greedy(customer, home_offer, ooh_candidates)
                effective_solver = "greedy"
            elif self.menu_selection_solver == "exact":
                if len(ooh_candidates) <= self._exact_threshold_for_policy():
                    menu = self._select_menu_exact(customer, home_offer, ooh_candidates)
                    effective_solver = "exact"
                else:
                    menu = self._select_menu_greedy(customer, home_offer, ooh_candidates)
                    effective_solver = "greedy"
                    fallback_used = True
                    fallback_reason = "above_exact_threshold"
            elif self.menu_use_exact_eval and len(ooh_candidates) <= self._exact_threshold_for_policy():
                menu = self._select_menu_exact(customer, home_offer, ooh_candidates)
                effective_solver = "exact"
            else:
                menu = self._select_menu_greedy(customer, home_offer, ooh_candidates)
                effective_solver = "greedy"
                if self.menu_use_exact_eval and len(ooh_candidates) > self._exact_threshold_for_policy():
                    fallback_used = True
                    fallback_reason = "above_exact_threshold"
            prior_diagnostic = self.last_policy_diagnostic or {}
            exact_enumerated = int(prior_diagnostic.get("exact_enumerated_menu_count", 0))
            selected_value = prior_diagnostic.get("exact_menu_value")
            self._merge_policy_diagnostic(self._solver_diagnostic(
                effective_solver,
                len(ooh_candidates),
                enumerated_count=exact_enumerated if effective_solver == "exact" else 0,
                fallback_used=fallback_used,
                fallback_reason=fallback_reason,
                selected_value=selected_value,
            ))

        if len(menu) == 0 and home_offer is not None:
            menu = [home_offer]
        if "menu_selection_solver_effective" not in (self.last_policy_diagnostic or {}):
            self._merge_policy_diagnostic(self._solver_diagnostic(
                "heuristic",
                len(ooh_candidates),
            ))
        return menu

    def get_action_menu(self, state, training=False):
        start_time = perf_counter()
        candidates = self.build_menu_candidates(state, training)
        _, feasible_ooh_candidates = self._split_menu_candidates(candidates)
        feasible_ooh_count = len(feasible_ooh_candidates)
        customer = state[0]
        if len(candidates) == 0:
            theta = self._theta(state[3])
            home_insertion = self.cheapestInsertionCosts(customer.home, state[1])
            home_cost = customer.service_time * self.cost_multiplier + (1 - theta) * home_insertion
            home_ivt, home_ivt_target = self._estimate_in_vehicle_time(customer.home)
            home_eta, home_eta_target, _ = self._estimate_pickup_eta(
                home_insertion,
                home_insertion,
                home_ivt_target,
            )
            menu = [
                self._build_home_offer(
                    customer,
                    home_cost=home_cost,
                    home_eta=home_eta,
                    home_ivt=home_ivt,
                    eta_target=home_eta_target,
                    ivt_target=home_ivt_target,
                )
            ]
        else:
            menu = self._select_menu_candidates(customer, candidates)

        self.last_menu_build_time = perf_counter() - start_time
        displayed_ooh_count = len([offer for offer in menu if not offer.is_home])
        exact_gap = self.last_exact_gap_diagnostic or {}
        policy_diagnostic = self.last_policy_diagnostic or {}
        for offer in menu:
            if offer.metadata is None:
                offer.metadata = {}
            offer.metadata["feasible_meeting_point_count"] = int(feasible_ooh_count)
            offer.metadata["displayed_meeting_point_count"] = int(displayed_ooh_count)
            offer.metadata["menu_selection_solver"] = self.menu_selection_solver
            offer.metadata["requested_menu_policy"] = self.requested_menu_policy
            offer.metadata["effective_menu_policy"] = self._effective_menu_policy()
            offer.metadata["menu_exact_threshold"] = int(self._exact_threshold_for_policy())
            offer.metadata["menu_exact_gap_threshold"] = int(self.menu_exact_gap_threshold)
            if policy_diagnostic:
                offer.metadata.update(policy_diagnostic)
            if exact_gap:
                offer.metadata.update(exact_gap)
        menu = self._finalize_menu(customer, menu)
        self.evaluate_menu(
            customer,
            menu,
            already_priced=True,
            use_system_eval=self._objective_uses_system_eval(),
            price_with_system_eval=self._pricing_uses_system_eval(),
        )
        for offer in menu:
            if offer.metadata is None:
                offer.metadata = {}
            offer.metadata["menu_policy"] = self.menu_policy
            offer.metadata["requested_menu_policy"] = self.requested_menu_policy
            offer.metadata["effective_menu_policy"] = self._effective_menu_policy()
            offer.metadata["menu_build_time"] = float(self.last_menu_build_time)
            offer.metadata["selected"] = True

        self.last_menu = list(menu)
        return list(menu)

    def update(self, data, state, done=False):
        if self.freeze_learning:
            if done:
                if self.load_data:
                    data["distance_matrix"] = get_dist_mat_HGS(self.dist_matrix, data['id'])
                _, cost = self.reopt_HGS_final(data, fallback_fleet=state[1])
                return cost
            return 0.0

        if not done:
            self.features = np.vstack((self.features, self.get_feature_rep(data).flatten()))
            selected_offer = getattr(self.config.env, "last_selected_offer", None)
            if selected_offer is None:
                raise ValueError("Menu mode requires env.last_selected_offer to be populated before update().")
            self.cap_features = np.vstack((self.cap_features, self._offer_aux_features(selected_offer)))
            eta_label = selected_offer.metadata.get("heuristic_eta", selected_offer.predicted_eta)
            ivt_label = selected_offer.metadata.get("heuristic_ivt", selected_offer.predicted_in_vehicle_time)
            self.time_targets = np.vstack((
                self.time_targets,
                np.array([[self.normalize_eta(eta_label), self.normalize_ivt(ivt_label)]], dtype=np.float32),
            ))
            return 0.0

        if self.load_data:
            data["distance_matrix"] = get_dist_mat_HGS(self.dist_matrix, data['id'])
        fleet, cost = self.reopt_HGS_final(data, fallback_fleet=state[1])

        target = sorted(self.get_per_customer_costs(fleet), key=lambda item: item[0])
        max_count = min(len(target), len(self.features), len(self.cap_features), len(self.time_targets))
        if max_count > 0:
            penalties = 20.0 / (self.cap_features[:max_count, [0]] + 0.1)
            adjusted_target = []
            for idx in range(max_count):
                adjusted_target.append([
                    float(target[idx][1]) + float(penalties[idx][0]),
                    float(self.time_targets[idx][0]),
                    float(self.time_targets[idx][1]),
                ])
            self.memory.add(self.features[:max_count], self.cap_features[:max_count], adjusted_target)

        self.features = np.empty((0, self.n_layers * self.grid_dim * self.grid_dim))
        self.cap_features = np.empty((0, self.aux_dim))
        self.time_targets = np.empty((0, 2))

        if self.initial_phase:
            if self.memory.length >= self.config.buffer_size:
                self.initial_phase_training(max_epochs=self.config.initial_phase_epochs)
        elif not self.config.only_phase_one:
            self.optimize()

        return cost
