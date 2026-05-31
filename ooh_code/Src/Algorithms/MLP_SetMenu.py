"""MLP_SetMenu: MLP-Menu baseline algorithm for DRT service menu design.

Subclasses DSPO_Menu to replace per-candidate cost prediction with a simple
MLP (MLPMenuNet) while keeping the parent's CNN_2d for ETA/IVT predictions.
No set-attention, no CNN spatial encoding — serves as an ablation baseline
to isolate the contribution of set-attention in CNN-SetMenuNet.

Design:
  - Keeps parent's self.supervised_ml = CNN_2d for ETA/IVT (NOT replaced)
  - Adds self.mlp_model = MLPMenuNet for cost prediction
  - Overrides build_menu_candidates() to use MLP for cost + CNN_2d for ETA/IVT
  - Overrides update() to train MLP with Huber loss
  - Inherits get_prediction(), menu selection, Lambert-W pricing, evaluation
"""

import numpy as np
import torch
from torch import float32

from Src.Algorithms.DSPO_Menu import DSPO_Menu
from Src.Utils.MLPMenuNet import MLPMenuNet


# ---------------------------------------------------------------------------
# MLPMemoryBuffer — ring buffer for option-feature-only transitions
# ---------------------------------------------------------------------------

class MLPMemoryBuffer:
    """Ring buffer storing (option_features, option_mask, true_costs) per transition.

    Simpler than SetMenuMemoryBuffer — no grid/aux tensors needed since the
    MLP only consumes per-candidate option features.
    """

    def __init__(self, max_len, K, device):
        self.max_len = max_len
        self.K = K
        self.device = device

        self.option_features = torch.zeros(
            (max_len, K, 6), dtype=float32, device=device,
        )
        self.option_mask = torch.zeros(
            (max_len, K), dtype=torch.bool, device=device,
        )
        self.true_costs = torch.zeros(
            (max_len, K), dtype=float32, device=device,
        )
        self.length = 0

    def add(self, opt_feat, opt_mask, costs):
        """Store one transition. Wraps around when buffer is full."""
        pos = self.length
        if self.length < self.max_len:
            self.length += 1
        else:
            pos = np.random.randint(self.max_len)

        self.option_features[pos] = opt_feat.to(self.device)
        self.option_mask[pos] = opt_mask.to(self.device)
        self.true_costs[pos] = costs.to(self.device)

    def sample(self, batch_size):
        """Random sample of transitions as a 3-tuple."""
        count = min(batch_size, self.length)
        indices = np.random.choice(self.length, count, replace=False)
        return (
            self.option_features[indices],
            self.option_mask[indices],
            self.true_costs[indices],
        )

    def batch_sample(self, batch_size, randomize=True):
        """Yield batches over the full buffer."""
        if randomize:
            indices = np.random.permutation(self.length)
        else:
            indices = np.arange(self.length)
        for ids in [indices[i:i + batch_size] for i in range(0, self.length, batch_size)]:
            yield (
                self.option_features[ids],
                self.option_mask[ids],
                self.true_costs[ids],
            )


# ---------------------------------------------------------------------------
# MLP_SetMenu — algorithm subclass
# ---------------------------------------------------------------------------

class MLP_SetMenu(DSPO_Menu):
    """MLP-Menu baseline algorithm.

    Keeps parent's CNN_2d (self.supervised_ml) for ETA/IVT predictions.
    Adds MLPMenuNet (self.mlp_model) for per-candidate cost prediction.
    Overrides build_menu_candidates() and update() only.
    """

    def __init__(self, config):
        # Parent creates self.supervised_ml = CNN_2d(...) for ETA/IVT
        # and sets up all menu params, grid dims, theta annealing, etc.
        super().__init__(config)

        # --- Add MLP model for cost prediction ---
        self.mlp_model = MLPMenuNet(
            input_dim=6,
            hidden_dim=64,
            dropout=config.dropout,
        )

        # --- Optimizer for MLP only (parent's CNN_2d is not retrained) ---
        self.optimizer = config.optim(
            self.mlp_model.parameters(), lr=self.config.learning_rate,
        )

        # --- Register MLP as the trainable module ---
        self.modules = [('mlp_model', self.mlp_model)]

        # --- Replace memory buffer with simpler version ---
        self.memory = MLPMemoryBuffer(
            max_len=config.buffer_size,
            K=self.max_candidates,
            device=config.device,
        )

        # --- Episode accumulation buffers ---
        self.episode_option_features = []
        self.episode_option_mask = []

        # --- Per-step storage (set in build_menu_candidates, consumed in update) ---
        self._current_option_features = None
        self._current_option_mask = None

        # --- Move MLP to device ---
        self.init()

    # ------------------------------------------------------------------
    # Override: build_menu_candidates — MLP cost + CNN_2d ETA/IVT
    # ------------------------------------------------------------------

    def build_menu_candidates(self, state, training):
        """Build menu candidates using MLPMenuNet for cost + inherited CNN_2d for ETA/IVT.

        Flow:
          1. Call inherited get_prediction() for ETA/IVT (via parent's CNN_2d)
          2. Call inherited build_option_features() for [K, 6] tensors
          3. Run MLPMenuNet forward for per-candidate cost prediction
          4. Build candidates with MLP costs and CNN_2d ETA/IVT
        """
        customer = state[0]
        self.derive_preferred_pickup_time(customer)
        theta = self._theta(state[3])
        mltplr = self.cost_multiplier
        pps = self._candidate_parcelpoints(state)
        # Cap PP candidates so total (home + PPs) fits within max_candidates
        pps = pps[: self.max_candidates - 1]
        cur_feat = self.get_feature_rep_infer(state[1]["fleet"])

        # --- ETA/IVT from inherited CNN_2d ---
        outputs = np.asarray(
            self.get_prediction(cur_feat, customer.home, pps, aux_features=self._default_menu_aux(customer, pps))
        )
        if outputs.ndim == 1:
            outputs = outputs.reshape(-1, 1)

        # --- Cost from MLPMenuNet ---
        option_features, option_mask = self.build_option_features(state, pps, customer)
        opt_batch = option_features.unsqueeze(0)      # [1, K, 6]
        mask_batch = option_mask.unsqueeze(0)          # [1, K]

        with torch.no_grad():
            predicted_costs = self.mlp_model(opt_batch, mask_batch)
        # predicted_costs: [1, K] — index 0 = home, indices 1..K-1 = parcel points

        # --- Store for training (consumed in update()) ---
        if training:
            self._current_option_features = option_features.clone()
            self._current_option_mask = option_mask.clone()

        # --- Build home candidate ---
        home_insertion = self.cheapestInsertionCosts(customer.home, state[1])
        home_cost = customer.service_time * mltplr + (
            (1 - theta) * home_insertion + theta * float(predicted_costs[0, 0])
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
        candidates = [home_offer_obj]

        # --- Build PP candidates ---
        feasible_count = 0
        pruned_by_eta_count = 0
        fn_pruned_near = 0
        fn_pruned_mid = 0
        fn_pruned_far = 0
        pp_opt_idx = 1  # option_features index 0 is home; PP indices start at 1

        for idx, pp in enumerate(pps):
            if pp.remainingCapacity <= 0:
                continue

            feasible_count += 1
            insertion_cost = self.cheapestInsertionCosts(pp.location, state[1])
            pp_cost = mltplr * (
                (1 - theta) * insertion_cost + theta * float(predicted_costs[0, pp_opt_idx])
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
            display_window = self._choose_display_window(
                customer,
                eta_choice["filter_eta"],
            )
            if display_window is None:
                pruned_by_eta_count += 1
                walk_dist_pruned = self._distance_between(customer.home, pp.location)
                if walk_dist_pruned < 500:
                    fn_pruned_near += 1
                elif walk_dist_pruned < 1500:
                    fn_pruned_mid += 1
                else:
                    fn_pruned_far += 1
                pp_opt_idx += 1
                continue

            walk_dist = self._distance_between(customer.home, pp.location)
            bundle = self._make_pp_bundle(pp, customer, display_window)
            candidates.append(
                self._make_pp_offer(
                    bundle, pp_cost, eta_choice, ivt_pp, eta_target, ivt_target,
                    walk_dist, insertion_cost, route_delay, customer,
                )
            )
            pp_opt_idx += 1

        # --- Dedup and metadata ---
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

        return list(deduped.values())

    # ------------------------------------------------------------------
    # Helpers for build_menu_candidates (reuse from CNN_SetMenu pattern)
    # ------------------------------------------------------------------

    def _make_pp_bundle(self, pp, customer, display_window):
        """Build a ServiceBundle for a parcel-point candidate."""
        from Environments.OOH.containers import ServiceBundle
        return ServiceBundle(
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

    def _make_pp_offer(self, bundle, pp_cost, eta_choice, ivt_pp, eta_target,
                       ivt_target, walk_dist, insertion_cost, route_delay, customer):
        """Build a MenuOffer for a parcel-point candidate."""
        from Environments.OOH.containers import MenuOffer
        return MenuOffer(
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
            },
        )

    # ------------------------------------------------------------------
    # Override: update — MLP training with K-candidate transitions
    # ------------------------------------------------------------------

    def update(self, data, state, done=False):
        """Store option features and train MLP at episode end."""
        if self.freeze_learning:
            if done:
                if self.load_data:
                    data["distance_matrix"] = self._get_dist_matrix(data)
                _, cost = self.reopt_HGS_final(data, fallback_fleet=state[1])
                return cost
            return 0.0

        if not done:
            # Store option features and mask from build_menu_candidates()
            if self._current_option_features is not None:
                self.episode_option_features.append(self._current_option_features)
                self.episode_option_mask.append(self._current_option_mask)
            else:
                pps = self._candidate_parcelpoints(state)
                pps = pps[: self.max_candidates - 1]
                opt_feat, opt_mask = self.build_option_features(state, pps, state[0])
                self.episode_option_features.append(opt_feat)
                self.episode_option_mask.append(opt_mask)

            # Maintain time_targets and parent's feature accumulation for CNN_2d
            selected_offer = getattr(self.config.env, "last_selected_offer", None)
            if selected_offer is None:
                raise ValueError("Menu mode requires env.last_selected_offer.")
            self.features = np.vstack((self.features, self.get_feature_rep(data).flatten()))
            self.cap_features = np.vstack((self.cap_features, self._offer_aux_features(selected_offer)))
            eta_label = selected_offer.metadata.get("heuristic_eta", selected_offer.predicted_eta)
            ivt_label = selected_offer.metadata.get("heuristic_ivt", selected_offer.predicted_in_vehicle_time)
            self.time_targets = np.vstack((
                self.time_targets,
                np.array([[self.normalize_eta(eta_label), self.normalize_ivt(ivt_label)]], dtype=np.float32),
            ))
            return 0.0

        # --- Done path: HGS re-optimization + training ---
        if self.load_data:
            data["distance_matrix"] = self._get_dist_matrix(data)
        fleet, cost = self.reopt_HGS_final(data, fallback_fleet=state[1])

        target = sorted(self.get_per_customer_costs(fleet), key=lambda item: item[0])
        max_count = min(len(target), len(self.episode_option_features))

        if max_count > 0:
            penalties = 20.0 / (np.array([
                float(self.cap_features[i][0]) for i in range(max_count)
            ]) + 0.1)

            for idx in range(max_count):
                true_cost_val = float(target[idx][1]) + float(penalties[idx])
                true_costs = torch.full(
                    (self.max_candidates,), float(true_cost_val), dtype=float32,
                )
                self.memory.add(
                    opt_feat=self.episode_option_features[idx],
                    opt_mask=self.episode_option_mask[idx],
                    costs=true_costs,
                )

        # Reset episode buffers
        self.episode_option_features = []
        self.episode_option_mask = []
        self.features = np.empty((0, self.n_layers * self.grid_dim * self.grid_dim))
        self.cap_features = np.empty((0, self.aux_dim))
        self.time_targets = np.empty((0, 2))

        # Training
        if self.initial_phase:
            if self.memory.length >= self.config.buffer_size:
                self.initial_phase_training(max_epochs=self.config.initial_phase_epochs)
        elif not self.config.only_phase_one:
            self.optimize()

        return cost

    # ------------------------------------------------------------------
    # Training helpers
    # ------------------------------------------------------------------

    def _mlp_update(self, opt_feat, opt_mask, costs):
        """Single training step: forward MLPMenuNet + Huber loss + backward."""
        self.optimizer.zero_grad()
        predicted = self.mlp_model(opt_feat, opt_mask)  # [B, K]
        loss = self.criterion(predicted, costs)
        loss.backward()
        self.optimizer.step()
        return loss.item()

    def optimize(self):
        """Sample a batch and run one training step."""
        opt_feat, opt_mask, costs = self.memory.sample(self.config.batch_size)
        loss = self._mlp_update(opt_feat, opt_mask, costs)
        print("MLPMenuNet Huber loss: ", loss)

    def initial_phase_training(self, max_epochs=-1):
        """Initial training phase: iterate over full buffer multiple times."""
        initial_losses = []
        print("MLPMenuNet initial training phase started...")
        for counter in range(max_epochs):
            losses = []
            for opt_feat, opt_mask, costs in self.memory.batch_sample(
                batch_size=self.config.batch_size, randomize=True,
            ):
                loss = self._mlp_update(opt_feat, opt_mask, costs)
                losses.append(loss)
            initial_losses.append(np.mean(losses))
            if counter % 1 == 0:
                print("Epoch {} Huber loss:: {}".format(counter, np.mean(initial_losses[-10:])))
                if self.config.only_phase_one:
                    self.save()
                    print("Saved..")
            if len(initial_losses) >= 20 and np.mean(initial_losses[-10:]) + 1e-5 >= np.mean(initial_losses[-20:]):
                print("Converged...")
                break
        print("... MLPMenuNet initial training phase terminated!")
        self.initial_phase = False
        self.save()

    # ------------------------------------------------------------------
    # Override: reset — clear episode buffers
    # ------------------------------------------------------------------

    def reset(self):
        super().reset()
        self.episode_option_features = []
        self.episode_option_mask = []
        self._current_option_features = None
        self._current_option_mask = None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_dist_matrix(self, data):
        """Load distance matrix for HGS."""
        from Src.Utils.Utils import get_dist_mat_HGS
        return get_dist_mat_HGS(self.dist_matrix, data['id'])
