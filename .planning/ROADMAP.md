# Roadmap: CNN-SetMenuNet Experiment Suite

## Overview

This roadmap takes Work 2 from a mature Work 1 codebase (DSPO_Menu with CNN_2d) to a full CNN-SetMenuNet experiment suite with 6 baseline comparisons. The journey: consolidate baseline policies (Phase 1) and build option features (Phase 2) in parallel, then stack the model layers -- SetMenuNet (Phase 3), CNN-SetMenuNet (Phase 4), algorithm integration (Phase 5) -- while MLP-Menu runs alongside (Phase 6), finally wiring the experiment pipeline (Phase 7) and running the main results (Phase 8). Eight phases, 37 requirements, one coherent delivery.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

**Parallelization:** Phase 01 and Phase 02 can run simultaneously. Phase 06 can run in parallel with Phases 03-05.

- [ ] **Phase 1: Baseline Consolidation** - Add home_only and cost_l_heuristic policies and verify all 4 baselines produce valid output on RC
- [ ] **Phase 2: Option Feature Extractor** - Build per-candidate 6-dim feature vectors with masking for variable-size candidate sets
- [ ] **Phase 3: SetMenuNet Model** - Self-attention model over candidate sets with permutation invariance and batch masking
- [ ] **Phase 4: CNN-SetMenuNet Model** - Hybrid CNN encoder + SetMenuNet with optional warm-start from Work 1 weights
- [ ] **Phase 5: Algorithm Integration** - CNN_SetMenu algorithm class subclassing DSPO_Menu with config and parser wiring
- [ ] **Phase 6: MLP-Menu Baseline** - Feature-only MLP baseline (no set-attention) as ablation comparison point
- [ ] **Phase 7: Experiment Pipeline** - YAML manifest, metrics collection (prediction/ranking/operational/passenger), and results table generation
- [ ] **Phase 8: Run Main Experiment** - Execute 6-method comparison on RC with K=10, L=3, 3 seeds, output paper-ready CSV

## Phase Details

### Phase 1: Baseline Consolidation
**Goal**: All 4 baseline menu policies produce valid, comparable results on RC instance, establishing the comparison framework for the main experiment table
**Depends on**: Nothing (uses existing Work 1 code)
**Requirements**: BASE-01, BASE-03, BASE-04, BASE-05, BASE-06, BASE-07 (BASE-02 merged into BASE-03)
**Success Criteria** (what must be TRUE):
  1. Two new menu policies (home_only, cost_l_heuristic) exist in DSPO_Menu and are callable via menu_policy parameter
  2. Each of the 4 baselines (home_only, Nearest-L, Cost-L, CNN-Menu) completes a full episode on RC instance without error
  3. Each baseline produces CSV output containing all standard operational metrics (net profit, total cost, quit rate, runtime)
  4. Smoke test passes: 3 seeds x 4 baselines = 12 runs complete without error
**Plans**: 1 plan

Plans:
- [x] 01-01-PLAN.md — Update run_baseline_smoke.py to native policy names and run 3x5 smoke verification

### Phase 2: Option Feature Extractor
**Goal**: A reusable feature extractor produces per-candidate 6-dimensional feature tensors with proper masking, ready for consumption by any downstream model (SetMenuNet, MLP, etc.)
**Depends on**: Nothing (uses existing Work 1 state/customer data)
**Requirements**: FEAT-01, FEAT-02, FEAT-03, FEAT-04
**Success Criteria** (what must be TRUE):
  1. build_option_features(state, pps, customer) returns a Tensor[K, 6] with correct feature dimensions (walk_distance, predicted_ivt, remaining_capacity, distance_to_destination, option_type, arrival_time)
  2. Variable-size candidate sets are handled via option_mask: Tensor[K] where valid candidates are True and padding is False
  3. Unit test confirms K=10 input produces output shape [10, 6] and mask shape [10]
  4. Feature values are numerically reasonable (no NaN/inf, bounded range) for typical RC instance states
**Plans**: 2 plans

Plans:
- [x] 02-01-PLAN.md — Verify and commit pure feature functions (normalize_features, build_option_tensor) plus 5 unit tests
- [x] 02-02-PLAN.md — Verify and commit DSPO_Menu integration (build_option_features method) and parser --max_candidates argument

### Phase 3: SetMenuNet Model
**Goal**: A standalone set-attention model that processes candidate sets with permutation invariance, batch support, and variable-size masking -- the core architectural contribution
**Depends on**: Phase 2 (option feature format defines input contract)
**Requirements**: SMNET-01, SMNET-02, SMNET-03, SMNET-04, SMNET-05, SMNET-06
**Success Criteria** (what must be TRUE):
  1. SetMenuNet exists as Src/Utils/SetMenuNet.py with a valid nn.Module that accepts [B, K, D] input and produces [B, K] cost predictions
  2. Self-attention uses 2 layers and 4 heads as specified, and the attention mechanism is configurable
  3. Permutation invariance verified: shuffling candidate order in the input produces identical cost predictions
  4. Variable-size masking works: candidates beyond set size receive zero/ignored output via option_mask
  5. Smoke test passes: synthetic input [4, 10, 6] produces output [4, 10] without error
**Plans**: 2 plans

Plans:
- [x] 03-01-PLAN.md — Implement SetMenuNet nn.Module with TransformerEncoder, masking, and reset/save/load interface
- [x] 03-02-PLAN.md — Create test_setmenunet.py with 6 verification tests (shape, architecture, permutation, masking, all-masked, save/load)

### Phase 4: CNN-SetMenuNet Model
**Goal**: The full hybrid model combining CNN global state encoding with SetMenuNet set-attention, producing per-candidate cost predictions from both grid state and option features
**Depends on**: Phase 3 (uses SetMenuNet as set-attention backbone)
**Requirements**: CSMNET-01, CSMNET-02, CSMNET-03, CSMNET-04, CSMNET-05, CSMNET-06
**Success Criteria** (what must be TRUE):
  1. CNNSetMenuNet exists as Src/Utils/CNNSetMenuNet.py with a valid nn.Module
  2. CNN_Encoder reuses CNN_2d's conv1, conv2, avgpool, flatten, fc1, fc2 (skips fc3), outputting 128-dim z_t from grid input [B, 2, 11, 11]
  3. Global state embedding z_t [B, 128] concatenated with each option's feature embedding
  4. Optional warm-start works: loading a CNN_2d checkpoint populates conv+fc layers correctly (fc3 mismatch is handled gracefully)
  5. Smoke test passes: grid [B, 2, 11, 11] + options [B, 10, 6] produces cost predictions [B, 10]
**Plans**: 2 plans

Plans:
- [x] 04-01-PLAN.md — Implement CNN_Encoder and CNNSetMenuNet nn.Modules with warm-start
- [x] 04-02-PLAN.md — Create test_cnnsetmenunet.py with 7 verification tests

### Phase 5: Algorithm Integration
**Goal**: CNN_SetMenu algorithm is fully integrated into the existing pipeline -- selectable via CLI flags, training with Huber loss, and producing menus through the model prediction + Lambert-W pricing flow
**Depends on**: Phase 4 (needs CNN-SetMenuNet model)
**Requirements**: ALGO-01, ALGO-02, ALGO-03, ALGO-04, ALGO-05, ALGO-06
**Success Criteria** (what must be TRUE):
  1. CNN_SetMenu class in Src/Algorithms/CNN_SetMenu.py subclasses DSPO_Menu and overrides prediction/training while inheriting menu construction, pricing, and metadata
  2. get_action_menu() builds option features, runs model prediction, selects top-L candidates, and applies Lambert-W pricing -- producing valid ServiceBundle offers
  3. update() stores (option_features, true_costs) transitions and trains the model with Huber loss
  4. config.py routes --menu_model cnn_setmenu to the CNN_SetMenu algorithm class
  5. parser.py exposes --menu_model and updated policy choices via CLI
  6. End-to-end smoke test: CNN_SetMenu trains over multiple episodes and evaluates on RC with K=10, L=3, across 3 seeds without error
**Plans**: 2 plans

Plans:
- [ ] 05-01: TBD
- [ ] 05-02: TBD

### Phase 6: MLP-Menu Baseline
**Goal**: MLP-Menu provides an ablation baseline that uses option features but no set-attention, showing the contribution of attention over simple feature concatenation
**Depends on**: Phase 2 (needs option feature format)
**Requirements**: MLP-01, MLP-02
**Success Criteria** (what must be TRUE):
  1. MLP-Menu baseline exists: flattens option features and passes through MLP to predict per-candidate costs (no set-attention)
  2. MLP-Menu is selectable as a menu_model variant in parser.py and runs through the same training/evaluation pipeline as other methods
**Plans**: 2 plans

Plans:
- [ ] 06-01: TBD

### Phase 7: Experiment Pipeline
**Goal**: A complete experiment pipeline collects prediction, ranking, operational, and passenger experience metrics across all methods, producing paper-ready results tables
**Depends on**: Phase 1 (baselines) + Phase 5 (CNN-SetMenuNet algorithm) + Phase 6 (MLP-Menu)
**Requirements**: EXPR-01, EXPR-02, EXPR-03, EXPR-04, EXPR-05
**Success Criteria** (what must be TRUE):
  1. work2_main.yaml manifest defines the 6-method comparison experiment (Nearest-L, Cost-L, CNN-Menu, SetMenuNet, CNN-SetMenuNet, Oracle Menu) and is runnable via run_study.py
  2. Prediction/ranking metrics (MAE, RMSE, Spearman, Top-L overlap, NDCG@L, Menu regret) are computed and logged for learning-based methods
  3. Operational metrics (net profit, total cost, travel cost, service cost, discount cost, charge revenue, runtime) are collected for all methods
  4. Passenger experience metrics (quit rate, acceptance rate, MP share, home share, avg walk, avg IVT, avg price) are collected for all methods
  5. build_artifacts.py generates a Work 2 results table aggregating all metrics by method
**Plans**: 2 plans

Plans:
- [ ] 07-01: TBD
- [ ] 07-02: TBD

### Phase 8: Run Main Experiment
**Goal**: The main experiment produces paper-ready results: 6 methods x 3 seeds on RC instance with K=10, L=3, outputting a comprehensive CSV for the results table
**Depends on**: Phase 7 (needs complete experiment pipeline)
**Requirements**: EXPR-06, EXPR-07
**Success Criteria** (what must be TRUE):
  1. Main experiment completes on RC instance with K=10, L=3, 80 train episodes, 20 test episodes, 3 seeds (0, 1, 2) for all 6 methods
  2. Results CSV contains all prediction, operational, and passenger experience metrics for all 6 methods and 3 seeds, ready for paper table generation
**Plans**: 2 plans

Plans:
- [ ] 08-01: TBD

## Progress

**Execution Order:**
Phases execute in numeric order. Parallelization: Phase 01 || Phase 02; Phase 06 concurrent with Phases 03-05.

**Parallelization Groups:**
- Group A (parallel): Phase 1, Phase 2
- Group B (sequential): Phase 3 -> Phase 4 -> Phase 5
- Group C (parallel with B): Phase 6 (after Phase 2)
- Group D (sequential): Phase 7 (after Phase 1 + Phase 5 + Phase 6), Phase 8 (after Phase 7)

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Baseline Consolidation | 1/1 | Complete | 2026-05-28 |
| 2. Option Feature Extractor | 2/2 | Complete | 2026-05-29 |
| 3. SetMenuNet Model | 0/2 | Planned | - |
| 4. CNN-SetMenuNet Model | 0/2 | Planned | - |
| 5. Algorithm Integration | 0/? | Not started | - |
| 6. MLP-Menu Baseline | 0/? | Not started | - |
| 7. Experiment Pipeline | 0/? | Not started | - |
| 8. Run Main Experiment | 0/? | Not started | - |
