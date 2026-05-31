# Work 2: CNN-SetMenuNet Experiment Suite

## What This Is

DRT (Demand Responsive Transit) 服务菜单设计研究的第二部分。Work 1 完成了基于 DSPO 的动态定价与菜单选择，Work 2 将 CNN 单点成本预测升级为基于集合注意力的结构化表征学习框架 CNN-SetMenuNet，用于动态服务菜单设计。目标期刊为 TR Part E。

核心转变：从"预测一个点的成本"升级为"理解一组候选服务选项之间的关系，并据此设计有限菜单"。

## Core Value

证明面向菜单结构的 Set-Attention 表征模型比传统 CNN 单点成本预测模型更适合 DRT 服务菜单设计，在菜单质量、运营收益和乘客体验之间取得最好平衡。

## Requirements

### Validated

- ✓ CNN-based cost prediction for DRT operations — Work 1 (CNN_2d in Predictors.py)
- ✓ Lambert-W dynamic pricing mechanism — Work 1 (MathUtils.py)
- ✓ MNL passenger choice model with outside option — Work 1 (customerchoice.py)
- ✓ HGS/Hygese route evaluation — Work 1 (Utils.py)
- ✓ Menu construction with 9 policy variants — Work 1 (DSPO_Menu.py)
- ✓ YAML manifest experiment framework — Work 1 (research_pipeline.py)
- ✓ State grid spatial feature encoding — Work 1 (Utils.get_matrix)
- ✓ MemoryBuffer with Huber loss training — Work 1 (Utils.py)
- ✓ Multiple instance support (RC, R, C) — Work 1 (HombergerGehring data)
- ✓ Option feature extractor: per-candidate 6-dim feature vectors — Phase 02 (option_features.py)
- ✓ SetMenuNet model: self-attention, permutation-invariant, batch+mask — Phase 03 (SetMenuNet.py)
- ✓ CNN-SetMenuNet model: CNN global state encoder + SetMenuNet hybrid, warm-start, 7/7 tests — Phase 04 (CNNSetMenuNet.py)

### Active
- [ ] CNN_SetMenu algorithm class: subclass of DSPO_Menu, override prediction and training
- [ ] 6 baselines for main comparison: Nearest-L, Cost-L, CNN-Menu, SetMenuNet, CNN-SetMenuNet, Oracle Menu
- [ ] Prediction/ranking metrics: MAE, RMSE, Spearman, Top-L overlap, NDCG@L, Menu regret
- [ ] Operational metrics: net profit, total cost, travel cost, service cost, discount cost, charge revenue, runtime
- [ ] Passenger experience metrics: quit rate, acceptance rate, MP share, home share, avg walk, avg IVT, avg price
- [ ] Main results experiment on RC instance (K=10, L=3, 3 seeds, 80 train / 20 test for MVP)
- [ ] CSV output and paper-ready results table

### Out of Scope

- SPO/decision-focused loss — Work 2 贡献在模型结构，不在 loss 函数
- GNN models — 候选菜单是动态集合而非固定图结构，Set-based encoder 更自然
- Beijing semi-real case — MVP 阶段只用 benchmark instances (RC, R, C)
- Ranking loss auxiliary — 第二版再加，第一版只用 Huber
- Menu size sensitivity / candidate pool sensitivity / demand sensitivity — 后续实验，不在 MVP 范围
- Cross-instance generalization / ablation — 后续实验

## Context

**Research framing (TR Part E):**
本文不是提出一个更复杂的神经网络，而是研究 DRT 平台如何进行 passenger-facing service menu design。CNN-SetMenuNet 是为这个运营决策问题服务的结构化表征工具。

**Three-layer contributions:**
1. 提出 choice-based dynamic service menu design 问题
2. 提出 CNN-SetMenuNet 结构化表征模型 (permutation invariance + option interaction + hybrid representation)
3. 闭环验证：menu design -> pricing -> passenger choice -> booking set -> routing cost

**Codebase state:**
- Work 1 code is mature and stable in `ooh_code/`
- DSPO_Menu.py (939 lines) handles menu construction, pricing, selection, training
- CNN_2d in Predictors.py has 2 conv layers + FC layers (output_dim=3: cost, ETA, IVT)
- CNN_2d's fc2 outputs 128-dim embedding before fc3 output head — this is what CNN_Encoder will reuse
- Existing experiment framework uses YAML manifests under `experiments/studies/`

**Existing baselines in DSPO_Menu:**
- offer_all_feasible_bundles, nearest_heuristic, top_k_cheapest, top_k_passenger_utility
- revenue_greedy, menu_optimization, insertion_cost_greedy, min_lateness, random_top_k
- Missing: home_only, oracle_menu (need to add)

**Model architecture (CNN-SetMenuNet):**
1. CNN global state encoder: reuse CNN_2d conv layers, remove fc3, output 128-dim z_t
2. Option embedding layer: per-candidate 6-dim feature -> MLP -> concat with z_t
3. Set-attention menu encoder: 2-layer, 4-head self-attention over candidate set
4. Output head: per-candidate predicted marginal cost
5. Training: Huber loss against true marginal insertion costs (no SPO)

**Key insight from experiment discussion:**
菜单不是越大越好。较小菜单限制乘客选择，较大菜单带来冗余和运营不稳定；L=3 或 L=4 通常取得最好利润-服务平衡。

## Constraints

- **Preserve pricing**: Lambert-W pricing module must not be modified
- **Preserve choice model**: MNL model in customerchoice.py must not be modified
- **Preserve routing**: HGS/Hygese routing must not be modified
- **Preserve data contracts**: MenuOffer and ServiceBundle dataclass structures must be maintained
- **YAML manifest compatibility**: New experiments must work with existing run_study.py pipeline
- **No SPO loss**: Training uses Huber loss only; contribution is model structure, not loss function
- **Python 3.10+ / PyTorch**: Must use existing tech stack
- **MVP scale**: 80 train episodes, 20 test episodes, 3 seeds (0,1,2) for initial validation

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| New model files (SetMenuNet.py, CNNSetMenuNet.py) | Separate concerns, easier to review/debug | — Pending |
| Subclass DSPO_Menu for CNN_SetMenu | Reuse all menu construction, pricing, metadata; only override prediction/training | — Pending |
| 6-dim option features for v1 | walk_dist, ivt, capacity, dist_to_dest, type, time — sufficient to start | — Pending |
| Main table: 6 methods | Nearest-L, Cost-L, CNN-Menu, SetMenuNet, CNN-SetMenuNet, Oracle | — Pending |
| MVP first, expand later | Run main results first (small scale), then add sensitivity/generalization/ablation | — Pending |
| Huber loss only (no SPO) | Work 2 contribution is model structure, not loss function | — Pending |
| CNN_Encoder reuses CNN_2d conv layers | Warm-start from Work 1 weights, only remove fc3 | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-29 after Phase 04*
