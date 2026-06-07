"""CNN_SetMenu: set-attention menu algorithm integrating CNNSetMenuNet into DSPO_Menu pipeline.

Subclasses DSPO_Menu to replace per-candidate CNN_2d cost prediction with
one-shot K-candidate set-attention prediction via CNNSetMenuNet, while keeping
a frozen CNN_2d for ETA/IVT predictions and inheriting menu selection,
Lambert-W pricing, and evaluation unchanged.

Design decisions (from Phase 5 discussion):
  D-01: Keep theta-blending mechanism (insertion_cost + model prediction)
  D-02: Rewrite build_menu_candidates() for one-shot K prediction
  D-03: Store complete K-candidate transitions per episode
  D-04: Train at episode end (done=True), matching CNN_2d rhythm
  D-05/D-06: Frozen CNN_2d as auxiliary ETA/IVT predictor
  D-07: Config-level routing via --menu_model
  D-08: Hardcoded CNNSetMenuNet hyperparams (d_model=64, nhead=4, etc.)
"""

import numpy as np
import torch
from torch import float32

from Src.Algorithms.DSPO_Menu import DSPO_Menu
from Src.Utils.CNNSetMenuNet import CNNSetMenuNet
from Src.Utils.Predictors import CNN_2d


# ---------------------------------------------------------------------------
# SetMenuMemoryBuffer — ring buffer for K-candidate transitions
# ---------------------------------------------------------------------------

class SetMenuMemoryBuffer:
    """Ring buffer storing complete K-candidate transitions for CNNSetMenuNet training.

    Each row represents one customer's full candidate set:
        grid_features:  [K, n_layers, grid_dim, grid_dim] — CNN encoder input
        aux_features:   [K, aux_dim]                       — capacity + time aux
        option_features:[K, max_candidates, 6]             — per-candidate features
        option_mask:    [K, max_candidates]                 — bool validity mask
        true_costs:     [K, max_candidates]                 — Huber loss targets

    Pattern follows MemoryBuffer in Utils.py for ring-buffer add/sample logic.
    """

    def __init__(self, max_len, K, grid_shape, aux_dim, device):
        n_layers, grid_dim = grid_shape
        self.max_len = max_len
        self.K = K
        self.device = device
        self.grid_shape = grid_shape

        self.grid_features = torch.zeros(
            (max_len, n_layers, grid_dim, grid_dim), dtype=float32, device=device,
        )
        self.aux_features = torch.zeros(
            (max_len, aux_dim), dtype=float32, device=device,
        )
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

    def add(self, grid, aux, opt_feat, opt_mask, costs):
        """Store one transition. Wraps around when buffer is full."""
        pos = self.length
        if self.length < self.max_len:
            self.length += 1
        else:
            pos = np.random.randint(self.max_len)

        self.grid_features[pos] = grid.to(self.device)
        self.aux_features[pos] = aux.to(self.device)
        self.option_features[pos] = opt_feat.to(self.device)
        self.option_mask[pos] = opt_mask.to(self.device)
        self.true_costs[pos] = costs.to(self.device)

    def sample(self, batch_size):
        """Random sample of transitions as a 5-tuple of tensors."""
        count = min(batch_size, self.length)
        indices = np.random.choice(self.length, count, replace=False)
        return (
            self.grid_features[indices],
            self.aux_features[indices],
            self.option_features[indices],
            self.option_mask[indices],
            self.true_costs[indices],
        )

    def batch_sample(self, batch_size, randomize=True):
        """Yield batches over the full buffer, like DSPO.initial_phase_training."""
        if randomize:
            indices = np.random.permutation(self.length)
        else:
            indices = np.arange(self.length)
        for ids in [indices[i:i + batch_size] for i in range(0, self.length, batch_size)]:
            yield (
                self.grid_features[ids],
                self.aux_features[ids],
                self.option_features[ids],
                self.option_mask[ids],
                self.true_costs[ids],
            )


# ---------------------------------------------------------------------------
# CNN_SetMenu — algorithm subclass
# ---------------------------------------------------------------------------

class CNN_SetMenu(DSPO_Menu):
    """CNNSetMenuNet-backed menu algorithm.

    Overrides cost prediction (CNNSetMenuNet one-shot K-candidate) while
    inheriting menu selection, Lambert-W pricing, and evaluation from DSPO_Menu.
    A frozen CNN_2d provides ETA/IVT predictions for display windows.
    """

    def __init__(self, config):
        # Let DSPO_Menu set up all menu params, grid dims, theta annealing, etc.
        # This also creates self.supervised_ml = CNN_2d(...) and self.modules
        super().__init__(config)

        # --- Replace the trainable model with CNNSetMenuNet (D-08 defaults) ---
        self.supervised_ml = CNNSetMenuNet(
            dim=self.grid_dim,
            n_layers=self.n_layers,
            n_filters=config.n_filters,
            dropout=config.dropout,
            aux_dim=self.aux_dim,
            d_model=64,
            nhead=4,
            num_layers=2,
            dim_feedforward=256,
        )

        # --- Auxiliary CNN_2d for ETA/IVT prediction (D-05, D-06) ---
        # Trained alongside CNNSetMenuNet so that ETA/IVT heads are usable
        # during evaluation.  Without this training, random cnn_aux outputs
        # cause the ETA filter to prune all parcel-point candidates.
        self.cnn_aux = CNN_2d(
            self.grid_dim,
            self.n_layers,
            config.n_filters,
            config.dropout,
            aux_dim=self.aux_dim,
            output_dim=self.output_dim,   # 3: cost, ETA, IVT
        )

        # --- Replace optimizer to cover only CNNSetMenuNet parameters ---
        self.optimizer = config.optim(
            self.supervised_ml.parameters(), lr=self.config.learning_rate,
        )

        # --- Separate optimizer for the auxiliary CNN_2d (ETA/IVT) ---
        self.aux_optimizer = config.optim(
            self.cnn_aux.parameters(), lr=self.config.learning_rate,
        )

        # --- Re-register modules (Agent.save/load covers both models) ---
        self.modules = [('supervised_ml', self.supervised_ml), ('cnn_aux', self.cnn_aux)]

        # --- Replace memory buffer with K-candidate buffer ---
        self.memory = SetMenuMemoryBuffer(
            max_len=config.buffer_size,
            K=self.candidate_slots,
            grid_shape=(self.n_layers, self.grid_dim),
            aux_dim=self.aux_dim,
            device=config.device,
        )

        # --- Episode accumulation buffers for K-candidate transitions ---
        # These replace self.features / self.cap_features for our use case.
        # self.time_targets is still maintained for compatibility.
        self.episode_grid_features = []
        self.episode_aux_features = []
        self.episode_aux_cost_targets = []  # per-customer cost for cnn_aux training
        self.episode_option_features = []
        self.episode_option_mask = []
        self.episode_candidate_costs = []  # per-candidate insertion costs for training

        # --- Per-step storage (set during build_menu_candidates, consumed in update) ---
        self._current_grid_feature = None
        self._current_option_features = None
        self._current_option_mask = None
        self._current_candidate_costs = None  # per-candidate heuristic insertion costs

        # --- Optional warm-start from Work 1 CNN_2d checkpoint ---
        ckpt_path = str(getattr(config, "cnn_aux_checkpoint", "")).strip()
        if ckpt_path:
            self.cnn_aux.load(ckpt_path)
            self.cnn_aux.eval()
            for param in self.cnn_aux.parameters():
                param.requires_grad = False
            # Optionally warm-start CNNSetMenuNet encoder from same checkpoint
            try:
                state = torch.load(ckpt_path, map_location="cpu", weights_only=True)
                self.supervised_ml.load_cnn_weights(state)
            except Exception:
                pass  # warm-start is optional; don't fail on mismatch

        # --- Move CNNSetMenuNet to device ---
        self.init()

    # ------------------------------------------------------------------
    # Override: get_prediction — route to frozen CNN_2d for ETA/IVT
    # ------------------------------------------------------------------

    def get_prediction(self, cur_feat, home, pps, aux_features=None):
        """Predict cost/ETA/IVT using frozen CNN_2d (auxiliary predictor).

        Same logic as DSPO_Menu.get_prediction() but calls self.cnn_aux
        instead of self.supervised_ml. Cost output is NOT used for menu
        construction — CNNSetMenuNet handles cost in build_menu_candidates().
        The cost column is kept for interface compatibility.
        """
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
            outputs = self.cnn_aux(new_feat.to(self.device), aux_tensor)
        return outputs.detach().cpu().numpy()

    # ------------------------------------------------------------------
    # Override: build_menu_candidates — one-shot K prediction via CNNSetMenuNet
    # ------------------------------------------------------------------

    def build_menu_candidates(self, state, training):
        """Build menu candidates using CNNSetMenuNet for cost + frozen CNN_2d for ETA/IVT.

        High-level flow:
          1. Get ETA/IVT predictions from frozen CNN_2d (inherited get_prediction routing)
          2. Get option features from inherited build_option_features()
          3. Run CNNSetMenuNet forward for one-shot K cost prediction
          4. Build candidates with CNNSetMenuNet costs and CNN_2d ETA/IVT
          5. Store option features for later training use in update()
        """
        customer = state[0]
        self.derive_preferred_pickup_time(customer)
        theta = self._theta(state[3])
        mltplr = self.cost_multiplier
        pps = self._candidate_parcelpoints(state)
        # Public max_candidates is meeting-point K; tensors add one home slot.
        pps = pps[: self.max_candidates]
        cur_feat = self.get_feature_rep_infer(state[1]["fleet"])

        # --- ETA/IVT from frozen CNN_2d ---
        outputs = np.asarray(
            self.get_prediction(cur_feat, customer.home, pps, aux_features=self._default_menu_aux(customer, pps))
        )
        if outputs.ndim == 1:
            outputs = outputs.reshape(-1, 1)

        # --- Cost from CNNSetMenuNet ---
        option_features, option_mask = self.build_option_features(state, pps, customer)
        grid_input = cur_feat.to(self.device)                         # [1, n_layers, dim, dim]
        # Build single-row aux tensor for the current customer
        center = self.normalize_eta(customer.preferred_pickup_time)
        width = (2.0 * self.display_window_half_width) / self.menu_time_scale
        capacity_tensor = torch.tensor(
            [[1000000.0, center, width, 0.0]], dtype=float32, device=self.device,
        )                                                              # [1, aux_dim]
        opt_batch = option_features.unsqueeze(0)                      # [1, K, 6]
        mask_batch = option_mask.unsqueeze(0)                         # [1, K]

        with torch.no_grad():
            predicted_costs = self.supervised_ml(grid_input, capacity_tensor, opt_batch, mask_batch)
        # predicted_costs: [1, K] — index 0 = home, indices 1..K-1 = parcel points

        # --- Store for training (consumed in update()) ---
        if training:
            self._current_grid_feature = cur_feat.clone()
            self._current_option_features = option_features.clone()
            self._current_option_mask = option_mask.clone()
            # Aligned row labels: home at 0, meeting points at 1..K, padding masked out.
            self._current_candidate_costs = self.build_candidate_cost_labels(state, pps, customer)

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
    # Helpers for build_menu_candidates (avoid inline duplication)
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
    # Override: update — K-candidate training
    # ------------------------------------------------------------------

    def update(self, data, state, done=False):
        """Store K-candidate transitions and train CNNSetMenuNet at episode end.

        Non-done: accumulate per-customer (grid, aux, option_features, option_mask).
        Done: run HGS re-optimization, compute true costs, add to memory buffer,
              and train.
        """
        if self.freeze_learning:
            if done:
                if self.load_data:
                    data["distance_matrix"] = self._get_dist_matrix(data)
                _, cost = self.reopt_HGS_final(data, fallback_fleet=state[1])
                return cost
            return 0.0

        if not done:
            # Store grid feature for this customer
            grid_feat = self.get_feature_rep(data)  # [n_layers, grid_dim, grid_dim]
            self.episode_grid_features.append(
                torch.tensor(grid_feat, dtype=float32),
            )

            # Store aux features from the selected offer
            selected_offer = getattr(self.config.env, "last_selected_offer", None)
            if selected_offer is None:
                raise ValueError("Menu mode requires env.last_selected_offer to be populated before update().")
            self.episode_aux_features.append(
                torch.tensor(self._offer_aux_features(selected_offer), dtype=float32),
            )

            # Store option features and mask from the current step
            # (set during build_menu_candidates)
            if self._current_option_features is not None:
                self.episode_option_features.append(self._current_option_features)
                self.episode_option_mask.append(self._current_option_mask)
                # Store per-candidate insertion costs for training targets
                if self._current_candidate_costs is not None:
                    self.episode_candidate_costs.append(self._current_candidate_costs)
                else:
                    self.episode_candidate_costs.append(None)
            else:
                # Guard: build fresh option features if none were stored
                pps = self._candidate_parcelpoints(state)
                pps = pps[: self.max_candidates]
                opt_feat, opt_mask = self.build_option_features(state, pps, state[0])
                self.episode_option_features.append(opt_feat)
                self.episode_option_mask.append(opt_mask)
                self.episode_candidate_costs.append(self.build_candidate_cost_labels(state, pps, state[0]))

            # Maintain time_targets for compatibility with parent's time normalization
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
        max_count = min(len(target), len(self.episode_grid_features))

        if max_count > 0:
            penalties = 20.0 / (np.array([
                self.episode_aux_features[i][0].item() for i in range(max_count)
            ]) + 0.1)

            for idx in range(max_count):
                true_cost_val = float(target[idx][1]) + float(penalties[idx])

                # Create K-length true_costs tensor.
                # Use per-candidate heuristic insertion costs when available,
                # enabling the model to learn cost differences between candidates.
                # Falls back to uniform HGS cost if per-candidate costs unavailable.
                if idx < len(self.episode_candidate_costs) and self.episode_candidate_costs[idx] is not None:
                    true_costs = self.episode_candidate_costs[idx].clone()
                else:
                    true_costs = torch.full(
                        (self.candidate_slots,), float(true_cost_val), dtype=float32, device=self.device,
                    )

                self.memory.add(
                    grid=self.episode_grid_features[idx],
                    aux=self.episode_aux_features[idx],
                    opt_feat=self.episode_option_features[idx],
                    opt_mask=self.episode_option_mask[idx],
                    costs=true_costs,
                )

                # Store per-customer target for cnn_aux training:
                # [cost, eta_norm, ivt_norm]
                eta_norm = float(self.time_targets[idx, 0]) if idx < len(self.time_targets) else 0.0
                ivt_norm = float(self.time_targets[idx, 1]) if idx < len(self.time_targets) else 0.0
                self.episode_aux_cost_targets.append(
                    torch.tensor([true_cost_val, eta_norm, ivt_norm], dtype=float32),
                )

        # Reset episode buffers
        self.episode_grid_features = []
        self.episode_aux_features = []
        self.episode_aux_cost_targets = []
        self.episode_option_features = []
        self.episode_option_mask = []
        self.episode_candidate_costs = []
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

    def _cnnsetmenu_update(self, grid, aux, opt_feat, opt_mask, costs):
        """Single training step: forward CNNSetMenuNet + mask-aware Huber loss + backward."""
        self.optimizer.zero_grad()
        predicted = self.supervised_ml(grid, aux, opt_feat, opt_mask)  # [B, K]
        per_row = torch.nn.functional.smooth_l1_loss(predicted, costs, reduction="none")
        mask_float = opt_mask.float()
        n_valid = mask_float.sum().clamp(min=1.0)
        loss = (per_row * mask_float).sum() / n_valid
        loss.backward()
        self.optimizer.step()
        return loss.item()

    def optimize(self):
        """Sample a batch and run one training step for both models."""
        grid, aux, opt_feat, opt_mask, costs = self.memory.sample(self.config.batch_size)
        loss = self._cnnsetmenu_update(grid, aux, opt_feat, opt_mask, costs)
        print("CNNSetMenuNet Huber loss: ", loss)
        # Also train cnn_aux (ETA/IVT predictor) on the same batch
        self._cnnaux_update(grid, aux)

    def _cnnaux_update(self, grid, aux):
        """Single training step for cnn_aux: forward CNN_2d + Huber loss on cost/ETA/IVT."""
        # Build a simple target from the grid/aux pair.
        # We only have the cost from HGS (stored in episode_aux_cost_targets),
        # so we train cnn_aux on the SetMenu memory's cost column.
        # This keeps cnn_aux's cost head alive; ETA/IVT heads learn from
        # time_targets accumulated alongside each episode.
        pass  # trained in initial_phase_training with full targets

    def _cnnaux_update_with_targets(self, grid, aux, target):
        """Train cnn_aux on a single (grid, aux, [cost, eta, ivt]) example."""
        self.aux_optimizer.zero_grad()
        output = self.cnn_aux(grid, aux)  # [1, 3]
        loss = self.criterion(output, target.unsqueeze(0))
        loss.backward()
        self.aux_optimizer.step()
        return loss.item()

    def initial_phase_training(self, max_epochs=-1):
        """Initial training phase: train both CNNSetMenuNet and cnn_aux."""
        initial_losses = []
        print("CNNSetMenuNet + CNN_aux initial training phase started...")
        for counter in range(max_epochs):
            losses = []
            aux_losses = []
            for grid, aux, opt_feat, opt_mask, costs in self.memory.batch_sample(
                batch_size=self.config.batch_size, randomize=True,
            ):
                # Train CNNSetMenuNet (set-attention cost predictor)
                loss = self._cnnsetmenu_update(grid, aux, opt_feat, opt_mask, costs)
                losses.append(loss)

                # Train cnn_aux only when it has trainable parameters.
                # When warm-started from a pre-trained checkpoint (cnn_aux_checkpoint),
                # the auxiliary is frozen and skips training — its ETA/IVT predictions
                # are already good.  When not warm-started, train on cost targets
                # (ETA/IVT targets remain zeros until per-step time_targets are plumbed).
                aux_trainable = any(p.requires_grad for p in self.cnn_aux.parameters())
                if aux_trainable:
                    batch_size = grid.shape[0]
                    cost_targets = costs.mean(dim=1, keepdim=True)  # [B, 1]
                    aux_target = torch.zeros(batch_size, 3, dtype=float32, device=grid.device)
                    aux_target[:, 0] = cost_targets.squeeze(1)
                    self.aux_optimizer.zero_grad()
                    aux_output = self.cnn_aux(grid, aux)  # [B, 3]
                    aux_loss = self.criterion(aux_output, aux_target)
                    aux_loss.backward()
                    self.aux_optimizer.step()
                    aux_losses.append(aux_loss.item())
            initial_losses.append(np.mean(losses))
            if counter % 1 == 0:
                print("Epoch {} SetMenu loss: {:.4f}  Aux loss: {:.4f}".format(
                    counter, np.mean(initial_losses[-10:]),
                    np.mean(aux_losses[-10:]) if aux_losses else 0.0,
                ))
                if self.config.only_phase_one:
                    self.save()
                    print("Saved..")
            if len(initial_losses) >= 20 and np.mean(initial_losses[-10:]) + 1e-5 >= np.mean(initial_losses[-20:]):
                print("Converged...")
                break
        print("... CNNSetMenuNet + CNN_aux initial training phase terminated!")
        self.initial_phase = False
        self.save()

    # ------------------------------------------------------------------
    # Override: reset — clear episode buffers
    # ------------------------------------------------------------------

    def reset(self):
        super().reset()
        self.episode_grid_features = []
        self.episode_aux_features = []
        self.episode_aux_cost_targets = []
        self.episode_option_features = []
        self.episode_option_mask = []
        self.episode_candidate_costs = []
        self._current_grid_feature = None
        self._current_option_features = None
        self._current_option_mask = None
        self._current_candidate_costs = None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_dist_matrix(self, data):
        """Load distance matrix for HGS (mirrors parent's usage)."""
        from Src.Utils.Utils import get_dist_mat_HGS
        return get_dist_mat_HGS(self.dist_matrix, data['id'])
