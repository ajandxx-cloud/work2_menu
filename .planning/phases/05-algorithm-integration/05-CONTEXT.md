# Phase 5: Algorithm Integration - Context

**Gathered:** 2026-05-29
**Status:** Ready for planning

<domain>
## Phase Boundary

Create `CNN_SetMenu` algorithm class that subclasses `DSPO_Menu` and integrates `CNNSetMenuNet` into the existing menu construction pipeline. The subclass replaces CNN_2d's per-candidate cost prediction with CNNSetMenuNet's set-attention-based joint prediction of all K candidates, while inheriting menu selection, Lambert-W pricing, and metadata unchanged.

Specifically this phase delivers:
- `Src/Algorithms/CNN_SetMenu.py` with `CNN_SetMenu(DSPO_Menu)` subclass
- Override of prediction flow: one-shot K-candidate prediction via CNNSetMenuNet
- Override of training flow: Huber loss on full K-candidate transitions
- Frozen CNN_2d as auxiliary ETA/IVT predictor
- `--menu_model` CLI flag for config-level algorithm routing
- End-to-end smoke test on RC instance

Not in scope: MLP-Menu baseline (Phase 6), experiment pipeline (Phase 7), new model architectures.

</domain>

<decisions>
## Implementation Decisions

### 预测→菜单流程 (Prediction-to-Menu Flow)
- **D-01:** 保留 theta-blending 机制。CNNSetMenuNet 的成本预测通过 `(1-θ)*插入成本 + θ*模型预测` 公式混合，θ 从 `init_theta_cnn` 退火到 `cool_theta_cnn`。这样做的理由：(1) 训练初期有安全网（模型不准时依赖启发式），(2) 与其他方法公平比较（所有方法使用相同的 blending 机制），(3) 退火机制已存在于 DSPO_Menu 中。
- **D-02:** 重写 `build_menu_candidates()`。流程改为：先一次性构建所有 K 个候选的 option features → 一次性调用 CNNSetMenuNet forward 得到 [K] 成本预测 → 在候选构建循环中使用这些预测。这自然利用了模型的联合预测能力（集合注意力看到所有候选间的关系）。

### 训练数据与 Huber Loss (Training Data Format)
- **D-03:** 每次训练转换（transition）存储完整 K 候选组：`(grid_state, aux_features, option_features[K, 6], option_mask[K], true_costs[K])`。训练时随机批量抽取完整组，每次 forward 传入完整的 K 个候选。这与 CNNSetMenuNet 的设计匹配，且保留了候选间关系信息。
- **D-04:** 沿用 episode 结束时训练的时机（done=True 时收集数据并训练），与 CNN_2d 的训练节奏一致。

### ETA/IVT 来源 (ETA/IVT Source)
- **D-05:** 保留 CNN_2d 作为冻结的辅助预测器，仅提供 ETA 和 IVT 预测。CNNSetMenuNet 仅输出 cost [B, K]，菜单流程所需的 ETA/IVT（用于效用计算、展示窗口、时间过滤）由冻结的 CNN_2d 提供。
- **D-06:** CNN_2d 权重从 Work 1 的训练检查点加载后冻结（`requires_grad=False`），不参与梯度更新。CNNSetMenuNet 是唯一可训练模型。

### Config/Parser 配置 (Config & Parser Wiring)
- **D-07:** Config 级路由。在 `config.py` 中根据 `--menu_model` 参数选择算法类：`menu_model='cnn_setmenu'` → `CNN_SetMenu`，`menu_model='cnn_2d'`（默认）→ `DSPO_Menu`。新增 `--menu_model` 参数到 parser.py，choices 为 `['cnn_2d', 'cnn_setmenu']`。
- **D-08:** CNNSetMenuNet 超参数（d_model=64, nhead=4, num_layers=2, dim_feedforward=256）在 `CNN_SetMenu.__init__()` 内部硬编码为默认值，不在 parser 中暴露为 CLI 参数。这些值与 Phase 04 的模型设计一致，MVP 阶段不需要调参。

### Claude's Discretion
- Memory buffer 批量处理细节（如何将多个 transition 的 option_features 组成 batch）
- 梯度裁剪策略（gradient clipping value）
- 优化器超参数（学习率、weight_decay 等）— 沿用 DSPO_Menu 的默认值
- Warm-start 检查点路径解析（从哪个目录加载 CNN_2d 权重）
- CNN_2d 冻结预测器的具体加载时机（__init__ 还是首次 forward）
- 新增训练转换的具体存储实现（复用现有 MemoryBuffer 还是新建）

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Algorithm Core (MUST override)
- `ooh_code/Src/Algorithms/DSPO_Menu.py` — DSPO_Menu class: __init__ (L18-111), get_action_menu (L907-964), build_menu_candidates (L502-645), update (L966-1016), get_prediction (L120-141), build_option_features (L647-714)
- `ooh_code/Src/Algorithms/DSPO.py` — DSPO base class: HuberLoss (L71-72), self_supervised_update (L295-301), memory buffer, theta annealing
- `ooh_code/Src/Algorithms/Agent.py` — Agent base class: modules registration (L5-65), save/load/train_mode/eval_mode

### Model Interfaces (MUST understand forward signatures)
- `ooh_code/Src/Utils/CNNSetMenuNet.py` — CNNSetMenuNet.forward(grid_input, capacity, option_features, option_mask) → [B, K] cost; CNN_Encoder.forward(x, capacity) → [B, 128]; load_cnn_weights() for warm-start
- `ooh_code/Src/Utils/Predictors.py` L31-92 — CNN_2d: forward(x, capacity) → [B, output_dim=3] (cost, ETA, IVT)
- `ooh_code/Src/Utils/option_features.py` — normalize_features() + build_option_tensor() → (Tensor[K,6], Tensor[K] mask)
- `ooh_code/Src/Utils/SetMenuNet.py` — SetMenuNet architecture reference (same hyperparams)

### Config & Parser (MUST modify)
- `ooh_code/Src/config.py` — self.algo routing at L100; self.__dict__.update(vars(args)) pattern
- `ooh_code/Src/parser.py` — --menu_policy (L109), --max_candidates (L127), finalize_args (L483-498)

### Data Structures (MUST preserve)
- `ooh_code/Environments/OOH/containers.py` — ServiceBundle, MenuOffer dataclass definitions
- `ooh_code/Environments/OOH/Parcelpoint_py.py` — Simulator interface, make_state()

### Pricing (MUST NOT modify)
- `ooh_code/Src/Utils/MathUtils.py` — Lambert-W pricing (lambertw function)

### Prior Phase Context
- `.planning/phases/02-option-feature-extractor/02-CONTEXT.md` — Option features interface decisions
- `.planning/phases/04-cnn-setmenunet-model/04-CONTEXT.md` — CNNSetMenuNet model decisions
- `.planning/REQUIREMENTS.md` — ALGO-01 through ALGO-06 requirements
- `.planning/ROADMAP.md` — Phase 5 goal and success criteria

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `DSPO_Menu.build_option_features()` (L647-714): Already builds [K, 6] option features + [K] mask. CNN_SetMenu can call this directly and unsqueeze for batching.
- `DSPO_Menu._select_menu_candidates()` (L829-905): Menu selection dispatch by policy string. Fully reusable — independent of cost predictor.
- `DSPO_Menu._price_menu_candidates()` (L327-381): Lambert-W pricing flow. Fully reusable — independent of cost predictor.
- `DSPO_Menu.evaluate_menu()` (L400-431): MNL choice probability, expected profit. Fully reusable.
- `DSPO_Menu._finalize_menu()` (L433-449): Two-pass pricing + scoring. Fully reusable.
- `DSPO.get_prediction()` (L120-141): CNN prediction call pattern — reference for override.
- `DSPO.self_supervised_update()` (L295-301): Huber loss training pattern — reference for override.
- `CNNSetMenuNet.load_cnn_weights()`: Warm-start mechanism already implemented in Phase 04.

### Established Patterns
- Config propagates all parser args via `self.__dict__.update(vars(args))` — new `--menu_model` arg automatically becomes `config.menu_model`
- DSPO_Menu.__init__ copies config attrs: `self.xxx = config.xxx` or `self.xxx = int(getattr(config, "xxx", default))`
- Agent.modules pattern: `self.modules = [('supervised_ml', model)]` — registered for save/load
- Memory buffer stores (features, targets), trains on done=True
- Theta annealing: `self.theta_cnn` starts at `init_theta_cnn`, decays to `cool_theta_cnn`

### Integration Points
- `config.py` L100: `self.algo = DSPO_Menu` → needs conditional: `self.algo = CNN_SetMenu if menu_model=='cnn_setmenu' else DSPO_Menu`
- `parser.py` L109: `--menu_policy` choices → add `--menu_model` as separate argument
- `parser.py` L494: `args.algo_name = "DSPO_Menu"` → needs conditional based on menu_model
- `DSPO_Menu.__init__` L82-98: `self.supervised_ml = CNN_2d(...)` → CNN_SetMenu replaces with CNNSetMenuNet + frozen CNN_2d
- `DSPO_Menu.build_menu_candidates()` L502-645: Per-candidate loop calling get_prediction() → rewrite to one-shot K prediction
- `DSPO_Menu.update()` L966-1016: Stores (features, [cost,eta,ivt]) → adapt to (grid, aux, option_features[K,6], mask[K], costs[K])

### Methods to OVERRIDE in CNN_SetMenu
| Method | Lines | Reason |
|--------|-------|--------|
| `__init__()` | 18-111 | Replace supervised_ml with CNNSetMenuNet + frozen CNN_2d |
| `build_menu_candidates()` | 502-645 | One-shot K prediction instead of per-candidate loop |
| `update()` (done path) | 966-1016 | Store K-candidate transitions, train CNNSetMenuNet |
| `get_prediction()` | 120-141 | Replace with CNNSetMenuNet forward call |

### Methods to INHERIT unchanged
| Method | Lines | Reason |
|--------|-------|--------|
| `get_action_menu()` | 907-964 | Orchestrates same flow, calls overridden methods |
| `_select_menu_candidates()` | 829-905 | Policy-independent menu selection |
| `_price_menu_candidates()` | 327-381 | Lambert-W pricing, independent of predictor |
| `evaluate_menu()` | 400-431 | MNL evaluation, independent |
| `_finalize_menu()` | 433-449 | Pricing + scoring pipeline |
| `build_option_features()` | 647-714 | Already produces correct tensors |

</code_context>

<specifics>
## Specific Ideas

- CNN_SetMenu 将维护两个模型实例：`self.supervised_ml`（CNNSetMenuNet，可训练）和 `self.cnn_aux`（CNN_2d，冻结）。`self.modules` 仅注册 CNNSetMenuNet。
- 重写后的 build_menu_candidates() 流程：(1) 调用 build_option_features() 得到 [K,6] + mask[K], (2) unsqueeze 为 batch dim, (3) 获取 grid_state 和 aux_features, (4) 一次性 CNNSetMenuNet.forward(grid, aux, options, mask) → [1, K] 成本, (5) 在候选循环中使用预测成本 + theta blending
- 训练转换的 true_costs[K] 来自 episode 结束时的 HGS re-optimization（与现有 DSPO_Menu 一致）
- CNN_2d 冻结预测器在 __init__ 中加载 Work 1 检查点，设置 `requires_grad=False`，用 `@torch.no_grad()` 保护 forward
- Warm-start CNNSetMenuNet: 可选地从 CNN_2d 检查点初始化 CNN_Encoder 部分（Phase 04 已实现 load_cnn_weights()）

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 05-algorithm-integration*
*Context gathered: 2026-05-29*
