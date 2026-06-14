# Phase 3: Mainline Comparison Contract - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md; this log preserves the alternatives considered.

**Date:** 2026-06-14
**Phase:** 03-mainline-comparison-contract
**Areas discussed:** Mainline comparison family, suite migration, formal/checkpoint boundary, artifact gate scope, menu_k placement

---

## Mainline Comparison Family

| Option | Description | Selected |
| --- | --- | --- |
| 保留 7 个 tag | `no_menu / fixed_menu / random_menu / optimized_m / optimized_mw / optimized_fixed_window / optimized_adaptive`，解释力最强，适合作为论文主线合同。 | yes |
| 压缩到 4 个 tag | 只比较 `no_menu / fixed_menu / random_menu / optimized_adaptive`，产品和时间窗消融以后再做。 | |
| 折中 5 个 tag | 保留 4 个菜单模式，再加一个关键消融。 | |
| 自定义 | 用户指定必须保留和可删除的 tag。 | |

**User's choice:** 1
**Notes:** 主线比较族保留 7 个 tag，以支持菜单设计、产品维度、固定/自适应时间窗的分解解释。

---

## Suite Migration

| Option | Description | Selected |
| --- | --- | --- |
| 直接迁移现有 `work2_robust_menu` | 让这个 suite 成为论文 V1 主线；旧 robust-policy 轴以后另开 diagnostic/legacy manifest。 | yes |
| 新建 mainline manifest | 保留旧 `work2_robust_menu` 不动，新增例如 `work2_mainline_menu`。 | |
| 双轨并存 | 暂时保留旧轴并新增 mainline manifests，Phase 4 再决定谁进论文。 | |
| 自定义 | 用户指定 suite 和 manifest 命名/迁移方式。 | |

**User's choice:** 1
**Notes:** `smoke_robust_menu.yaml`、`pilot_robust_menu.yaml`、`formal_robust_menu.yaml` 直接迁移为 V1 主线 7-tag 比较。

---

## Formal And Checkpoint Boundary

| Option | Description | Selected |
| --- | --- | --- |
| Phase 3 只声明 formal 合同 | formal 5+ seeds、checkpoint required；不训练/不跑 formal，缺 checkpoint 就验证 blocked rows。 | yes |
| Phase 3 顺便训练 formal checkpoint | 更完整，但耗时和风险更高。 | |
| Phase 3 只做 smoke/pilot | 更轻，但不能完全定义主线 formal 合同。 | |
| 自定义 | 例如 formal 先 6 seeds、只训练 pilot checkpoint 等。 | |

**User's choice:** 1
**Notes:** Phase 3 不训练、不运行 formal；formal manifest 必须声明 5+ paired splits/seeds 和 checkpoint-required 合同。

---

## Artifact Gate Scope

| Option | Description | Selected |
| --- | --- | --- |
| 包含轻量 artifact gate 测试 | 不生成表图，只强化 `artifact_status.py` / `test_artifact_gates.py` 的 mainline eligibility 合同。 | yes |
| 不碰 artifact gate | Phase 3 只管 adapter、manifest、row schema、smoke replay。 | |
| 包含 artifact gate + builder 合同 | 除 eligibility 外，也调整 `artifact_builder.py` 的排名/summary 逻辑。 | |
| 自定义 | 用户指定 Phase 3 碰到 artifact 层的哪里。 | |

**User's choice:** 1
**Notes:** Phase 3 只做 eligibility/claim-readiness 合同，不生成表图，不深入改 builder；builder/table/figure 留给 Phase 4。

---

## Menu Size Placement

| Option | Description | Selected |
| --- | --- | --- |
| 只 smoke 覆盖 `{1,2,3,5}` | pilot/formal 固定 `menu_k=3`，Phase 3 最稳。 | |
| smoke 和 pilot 覆盖 `{1,2,3,5}` | 提前看 pilot 层菜单大小鲁棒性，formal 成本仍可控。 | yes |
| formal 也覆盖 `{1,2,3,5}` | 最完整，但 formal 成本大幅上升。 | |
| 拆成两个 manifest | 主线 formal 固定 `menu_k=3`，另建 `*_menu_k_robustness`。 | |

**User's choice:** 2
**Notes:** smoke 和 pilot 都覆盖 `menu_k={1,2,3,5}`；formal 固定 `menu_k=3`。

---

## the agent's Discretion

None. User selected all key Phase 3 decisions.

## Deferred Ideas

- Legacy robust-policy axis may be preserved later as a diagnostic/legacy manifest if needed.
- Mainline-aware artifact builder, tables, figures, and manuscript claim guard are deferred to Phase 4.
- Formal actual replay and checkpoint training are deferred until after Phase 3 contract verification.
