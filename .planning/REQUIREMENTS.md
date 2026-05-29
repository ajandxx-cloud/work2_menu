# Requirements: CNN-SetMenuNet Experiment Suite

**Defined:** 2026-05-28
**Core Value:** 证明面向菜单结构的 Set-Attention 表征模型比传统 CNN 单点成本预测模型更适合 DRT 服务菜单设计

## v1 Requirements (MVP)

### Baseline Infrastructure

- [ ] **BASE-01**: Add `home_only` menu policy to DSPO_Menu (只展示 home pickup，下界 baseline)
- [ ] **BASE-02**: ~~Add `oracle_menu` menu policy to DSPO_Menu~~ **MERGED into BASE-03** — oracle_menu and cost_l_heuristic are one policy using immediate insertion costs
- [ ] **BASE-03**: Add `cost_l_heuristic` menu policy to DSPO_Menu (用即时插入成本选 L 个点; also serves as oracle baseline)
- [ ] **BASE-04**: Verify `nearest_heuristic` policy works as B1 baseline
- [ ] **BASE-05**: Verify `top_k_cheapest` with CNN prediction works as B5 (CNN-Menu)
- [ ] **BASE-06**: All 4 baselines produce valid CSV output with standard metrics on RC instance
- [ ] **BASE-07**: Smoke test: 3 seeds (0,1,2) × 4 baselines run without error

### Option Feature Engineering

- [ ] **FEAT-01**: Implement `build_option_features(state, pps, customer)` function
- [ ] **FEAT-02**: Feature vector: [walk_distance, predicted_ivt, remaining_capacity, distance_to_destination, option_type, arrival_time] (6维)
- [ ] **FEAT-03**: Returns `option_features: Tensor [K, 6]` and `option_mask: Tensor [K]`
- [ ] **FEAT-04**: Unit test: K=10 produces correct shape [10, 6]

### SetMenuNet Model

- [x] **SMNET-01**: Create `Src/Utils/SetMenuNet.py` with SetMenuNet(nn.Module)
- [x] **SMNET-02**: Multi-head self-attention (2 layers, 4 heads) over candidate set
- [ ] **SMNET-03**: Permutation-invariant: output does not depend on input order
- [ ] **SMNET-04**: Supports variable-size candidate sets via masking
- [x] **SMNET-05**: Output: per-candidate predicted marginal cost [B, K]
- [ ] **SMNET-06**: Smoke test: synthetic [4, 10, 6] input produces [4, 10] output

### CNN-SetMenuNet Model

- [x] **CSMNET-01**: Create `Src/Utils/CNNSetMenuNet.py` with CNNSetMenuNet(nn.Module)
- [x] **CSMNET-02**: CNN_Encoder reuses CNN_2d conv layers (conv1, conv2, avgpool, flatten, fc1, fc2), removes fc3, outputs 128-dim
- [x] **CSMNET-03**: Global state embedding z_t [B, 128] concatenated with each option's feature embedding
- [x] **CSMNET-04**: Combined embedding fed through SetMenuNet → output head → cost_pred [B, K]
- [x] **CSMNET-05**: Optional warm-start: load CNN_2d checkpoint weights (skip fc3 mismatch)
- [x] **CSMNET-06**: Smoke test: grid [B, 2, 11, 11] + options [B, 10, 6] → cost [B, 10]

### Algorithm Integration

- [ ] **ALGO-01**: Create `Src/Algorithms/CNN_SetMenu.py` with CNN_SetMenu(DSPO_Menu)
- [ ] **ALGO-02**: Override `get_action_menu()`: build option features → model predict → top-L select → Lambert-W price
- [ ] **ALGO-03**: Override `update()`: store (option_features, true_costs), train with Huber loss
- [ ] **ALGO-04**: Update `config.py` to support `--menu_model cnn_setmenu` routing
- [ ] **ALGO-05**: Update `parser.py` with new menu_model and policy choices
- [ ] **ALGO-06**: End-to-end smoke test: CNN_SetMenu trains and evaluates on RC with K=10, L=3, 3 seeds

### MLP-Menu Baseline

- [ ] **MLP-01**: Implement MLP-Menu baseline using option features without set-attention (flatten features → MLP → cost)
- [ ] **MLP-02**: MLP-Menu integrated as menu_model variant in parser.py

### Experiment Pipeline

- [ ] **EXPR-01**: Create `experiments/studies/work2_main.yaml` manifest for 6-method comparison
- [ ] **EXPR-02**: Add prediction/ranking metrics to research_pipeline.py: MAE, RMSE, Spearman correlation, Top-L overlap, NDCG@L, Menu regret
- [ ] **EXPR-03**: Verify operational metrics collected: net profit, total cost, quit rate, MP share, avg walk, avg price, runtime
- [ ] **EXPR-04**: Add passenger experience metrics: acceptance rate, home share, avg IVT, avg price/discount
- [ ] **EXPR-05**: Update `build_artifacts.py` to generate Work 2 results table
- [ ] **EXPR-06**: Run main experiment on RC (K=10, L=3, 3 seeds, 80 train / 20 test)
- [ ] **EXPR-07**: Output results CSV with all metrics for all 6 methods

## v2 Requirements (Post-MVP)

### Extended Experiments

- **SENS-01**: Menu size sensitivity (L in {1,2,3,4,5,6,8,10})
- **SENS-02**: Candidate pool size sensitivity (K in {5,8,10,15,20})
- **SENS-03**: Demand intensity sensitivity (N in {60,90,120,150})
- **SENS-04**: Outside option competition sensitivity (low/medium/high)
- **SENS-05**: Cross-instance generalization (train RC, test R/C)
- **SENS-06**: Ablation study (CNN only, Set only, CNN+MLP, full model, +ranking loss)

### Enhanced Features

- **ENH-01**: 7-dim option features (add CNN_predicted_cost as hybrid input)
- **ENH-02**: Ranking loss auxiliary (pairwise ranking loss with Huber)
- **ENH-03**: Menu score output head (alternative to cost prediction)
- **ENH-04**: Beijing semi-real case (Yanjiao-Guomao commuting corridor)
- **ENH-05**: Formal scale experiments (150-300 train / 50 test / 5 seeds)

## Out of Scope

| Feature | Reason |
|---------|--------|
| SPO/decision-focused loss | Work 2 贡献在模型结构，不在 loss 函数 |
| GNN models | 候选菜单是动态集合而非固定图结构 |
| Reinforcement learning training | Huber supervised loss sufficient for v1 |
| Real-time serving system | Research prototype only |
| Mobile/web UI | CLI-based experiment framework only |
| Beijing case in MVP | Benchmark instances sufficient for validation |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| BASE-01 | Phase 01 | Pending |
| BASE-02 | Phase 01 | Merged into BASE-03 |
| BASE-03 | Phase 01 | Pending |
| BASE-04 | Phase 01 | Pending |
| BASE-05 | Phase 01 | Pending |
| BASE-06 | Phase 01 | Pending |
| BASE-07 | Phase 01 | Pending |
| FEAT-01 | Phase 02 | Pending |
| FEAT-02 | Phase 02 | Pending |
| FEAT-03 | Phase 02 | Pending |
| FEAT-04 | Phase 02 | Pending |
| SMNET-01 | Phase 03 | Complete |
| SMNET-02 | Phase 03 | Complete |
| SMNET-03 | Phase 03 | Pending |
| SMNET-04 | Phase 03 | Pending |
| SMNET-05 | Phase 03 | Complete |
| SMNET-06 | Phase 03 | Pending |
| CSMNET-01 | Phase 04 | Complete |
| CSMNET-02 | Phase 04 | Complete |
| CSMNET-03 | Phase 04 | Complete |
| CSMNET-04 | Phase 04 | Complete |
| CSMNET-05 | Phase 04 | Complete |
| CSMNET-06 | Phase 04 | Complete |
| ALGO-01 | Phase 05 | Pending |
| ALGO-02 | Phase 05 | Pending |
| ALGO-03 | Phase 05 | Pending |
| ALGO-04 | Phase 05 | Pending |
| ALGO-05 | Phase 05 | Pending |
| ALGO-06 | Phase 05 | Pending |
| MLP-01 | Phase 06 | Pending |
| MLP-02 | Phase 06 | Pending |
| EXPR-01 | Phase 07 | Pending |
| EXPR-02 | Phase 07 | Pending |
| EXPR-03 | Phase 07 | Pending |
| EXPR-04 | Phase 07 | Pending |
| EXPR-05 | Phase 07 | Pending |
| EXPR-06 | Phase 08 | Pending |
| EXPR-07 | Phase 08 | Pending |

**Coverage:**
- v1 requirements: 37 total
- Mapped to phases: 37
- Unmapped: 0

---
*Requirements defined: 2026-05-28*
*Last updated: 2026-05-28 after initial definition*
