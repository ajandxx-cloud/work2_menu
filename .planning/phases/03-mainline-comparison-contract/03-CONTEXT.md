# Phase 3: Mainline Comparison Contract - Context

**Gathered:** 2026-06-14
**Status:** Ready for planning
**Language:** Chinese
**Source:** Phase 2 closeout + repository audit + current `work2_coding/` inspection + user discussion

<domain>
## Phase Boundary

Phase 3 将 Phase 2 已验证的服务产品合同推广为 `work2_robust_menu` 的 V1 主线比较合同。它负责让 smoke/pilot/formal manifests、policy adapters、paired replay schema、row tests、study status tests 和轻量 artifact eligibility tests 都围绕同一组主线比较轴工作。

Phase 3 不负责生成论文表图，不宣称正式结果，不手改 generated result rows 或 manuscript 正文。Phase 4 才消费 Phase 3 的 normalized-row-v2 合同与 smoke/pilot/formal manifest，继续做 artifact pipeline、claim gate、表图和 manuscript frame。

</domain>

<decisions>
## Implementation Decisions

### Mainline Comparison Family
- **D-01:** Phase 3 主线比较族保留 7 个 tag，而不是压缩为 4 个或 5 个。
- **D-02:** 7 个主线 tag 为：
  - `mainline_no_menu`
  - `mainline_fixed_menu`
  - `mainline_random_menu`
  - `mainline_optimized_m`
  - `mainline_optimized_mw`
  - `mainline_optimized_fixed_window`
  - `mainline_optimized_adaptive`
- **D-03:** 主线 primary method 是 `mainline_optimized_adaptive`，合同组合为 `m+w+p / adaptive_window / optimized_menu / lambertw`，运行策略为 `service_guarded_expected_profit`。
- **D-04:** `mainline_fixed_menu` 的主固定菜单基线是 nearest/top-k proximity；`top_k_cheapest` 不作为主线 fixed-menu baseline。
- **D-05:** `mainline_random_menu` 必须从同一 candidate pool 中 seeded deterministic 抽取，并使用相同 `menu_k`。
- **D-06:** `mainline_no_menu` 是单一 default home product 加 outside option；opt-out 仍然不是 accepted home pickup。
- **D-07:** `mainline_optimized_m` 和 `mainline_optimized_mw` 用于产品消融，并且因为产品不包含完整 `p`，normalized row 中的 `pricing_mode` 必须落到 `no_pricing`。
- **D-08:** `mainline_optimized_fixed_window` 与 `mainline_optimized_adaptive` 用于区分固定时间窗与自适应/robust 时间窗。

### Suite And Manifest Migration
- **D-09:** 直接迁移现有 `work2_robust_menu` suite，作为 V1 论文主线。也就是 `smoke_robust_menu.yaml`、`pilot_robust_menu.yaml`、`formal_robust_menu.yaml` 都切到 7-tag 主线比较族。
- **D-10:** 旧 robust-policy 轴继续在 adapter 层保留兼容，但不再作为 `work2_robust_menu` 主线 manifest 的 required policy family。若后续还需要旧轴，应另开 diagnostic/legacy manifest。
- **D-11:** `work2_robust_menu` suite 继续包含 smoke、pilot、formal 三层，不另起新的主线 suite 名。
- **D-12:** 三个主线 manifests 都使用 `normalized-row-v2`，并显式列出 product/time-window/menu/pricing/method/candidate/status/profit/service fields。

### Formal And Checkpoint Boundary
- **D-13:** Phase 3 只声明 formal 合同，不训练 formal checkpoint，也不跑 formal actual replay。
- **D-14:** `formal_robust_menu.yaml` 必须声明至少 5 个 paired splits/seeds，并覆盖 low 与 medium uptake regimes。
- **D-15:** Formal 固定主设定 `menu_k=3`，不在 formal 层展开 `{1,2,3,5}` 菜单大小矩阵。
- **D-16:** Formal manifest 必须保持 `shared_checkpoint.required=true` 与 `base_args.require_checkpoint=true`。checkpoint 文件缺失时，只验证 blocked-row / claim-gate 行为，不允许随机权重作为证据。

### Menu Size Coverage
- **D-17:** `menu_k={1,2,3,5}` 放在 smoke 和 pilot 层覆盖。
- **D-18:** Smoke 需要便宜且实际可执行，用来快速证明 7-tag family 与 `menu_k` 矩阵能跑通。
- **D-19:** Pilot 也覆盖 `menu_k={1,2,3,5}`，用于提前暴露菜单大小鲁棒性问题。
- **D-20:** Formal 固定 `menu_k=3`，把正式合同成本控制在主线政策比较上。

### Artifact Gate Scope
- **D-21:** Phase 3 包含轻量 artifact eligibility 测试，但不生成表图，不深入调整 `artifact_builder.py` 的 ranking/table/figure 逻辑。
- **D-22:** Artifact eligibility 必须继续阻断 failed、blocked、placeholder-only、diagnostic-only、no-filter-only、checkpoint bad rows。
- **D-23:** Phase 4 再处理 mainline-aware artifact builder、mirrored artifact bundle、claim guard 和 manuscript-facing outputs。

### Scope Fences
- **D-24:** Phase 3 不修改 manuscript 正文、不手改 generated artifacts、不生成 formal claim-ready tables/figures。
- **D-25:** Phase 3 不引入 attention-based choice/scoring；attention remains V2/diagnostic only。
- **D-26:** Phase 3 不重写 HGS/routing semantics，不改变 opt-out 与 accepted-home 的分离语义。
- **D-27:** `.planning/PROJECT.md`、`.planning/REQUIREMENTS.md`、`.planning/ROADMAP.md` 和 `.planning/STATE.md` 当前在工作区中为删除状态，且 Phase 1 audit 说明旧文件属于 superseded Akkerman planning；Phase 3 不重建这些旧文件。

### the agent's Discretion
无。用户已明确选择所有 Phase 3 关键取舍。

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Planning And Prior Phase
- `.planning/repository_audit.md` - Phase 1 audit, active runtime root, stale path mapping, reusable robust-menu inventory, and formal evidence gaps.
- `.planning/phases/02-service-product-contract/02-CONTEXT.md` - Phase 2 service product, time-window, menu-mode, row-v2, and artifact gate decisions.
- `.planning/phases/02-service-product-contract/02-VERIFICATION.md` - Phase 2 verified commands and closeout.
- `.planning/phases/03-mainline-comparison-contract/03-DISCUSSION-LOG.md` - human audit trail for Phase 3 decisions.
- `AGENTS.md` - project guardrails, active runtime assumption, research guardrails, and verification baseline.

### Runtime And Contract Code
- `work2_coding/Src/policy_adapters.py` - adapter pattern, legacy robust tags, Phase 2 `contract_*` tags, and new Phase 3 mainline tags.
- `work2_coding/Src/experiment_contracts.py` - manifest loading, parser compatibility, required policy tags, paired-field validation, checkpoint gates, and uptake-regime gates.
- `work2_coding/Src/paired_replay.py` - normalized-row-v2 schema, method construction, checkpoint metadata, and row validation.
- `work2_coding/Src/study_execution.py` - blocked/completed/failed row generation and actual replay execution.
- `work2_coding/Src/Algorithms/DSPO_Menu.py` - product/time-window/menu/pricing metadata and menu policy implementations.
- `work2_coding/Src/artifact_status.py` - artifact eligibility and claim-ready classification.

### Manifests And Tests
- `work2_coding/Experiments/studies/smoke_phase2_service_product_contract.yaml` - verified Phase 2 smoke contract and useful reference for `menu_k={1,2,3,5}`.
- `work2_coding/Experiments/studies/smoke_robust_menu.yaml` - to become smoke mainline V1 contract.
- `work2_coding/Experiments/studies/pilot_robust_menu.yaml` - to become pilot mainline V1 contract and cover `menu_k={1,2,3,5}`.
- `work2_coding/Experiments/studies/formal_robust_menu.yaml` - to become formal mainline V1 contract with 5+ splits and fixed `menu_k=3`.
- `work2_coding/Experiments/suites/work2_robust_menu.yaml` - suite membership contract.
- `work2_coding/scripts/test_menu_mode_adapters.py` - adapter composition tests.
- `work2_coding/scripts/test_policy_fairness_contract.py` - paired fairness and policy-only drift checks.
- `work2_coding/scripts/test_experiment_contracts.py` - manifest validation and suite checks.
- `work2_coding/scripts/test_paired_replay_contract.py` - row-v2 schema and method composition checks.
- `work2_coding/scripts/test_smoke_study_rows.py` - smoke actual row checks.
- `work2_coding/scripts/test_study_execution_status.py` - blocked/completed/failed row behavior.
- `work2_coding/scripts/test_artifact_gates.py` - lightweight artifact eligibility behavior.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `policy_adapters.py` already supports policy tag -> parser override mapping and manifest metadata. Phase 3 should extend this pattern, not create a parallel adapter path.
- `experiment_contracts.py` already supports manifest-level `required_policy_tags`; use this to move `work2_robust_menu` from legacy required tags to Phase 3 mainline required tags.
- `paired_replay.py` already builds canonical method strings from `product_mode`, `time_window_mode`, `menu_mode`, and `pricing_mode`.
- `study_execution.py` already emits failed rows and continues batch execution after candidate failure.
- `artifact_status.py` already implements most eligibility blockers needed by Phase 3.

### Established Patterns
- Use script-style tests under `work2_coding/scripts/`.
- Keep study definitions manifest-driven under `work2_coding/Experiments/studies/`.
- Keep generated outputs under `work2_coding/outputs/`; do not hand-edit output rows.
- Keep no-filter diagnostic rows out of formal ranking claims.

### Integration Points
- Add mainline tags in `policy_adapters.py`.
- Migrate `smoke_robust_menu.yaml`, `pilot_robust_menu.yaml`, and `formal_robust_menu.yaml`.
- Update `test_experiment_contracts.py`, `test_policy_fairness_contract.py`, `test_menu_mode_adapters.py`, `test_paired_replay_contract.py`, `test_smoke_study_rows.py`, `test_study_execution_status.py`, and `test_artifact_gates.py`.

</code_context>

<specifics>
## Specific Ideas

- Mainline tag family is exactly:
  - `mainline_no_menu`
  - `mainline_fixed_menu`
  - `mainline_random_menu`
  - `mainline_optimized_m`
  - `mainline_optimized_mw`
  - `mainline_optimized_fixed_window`
  - `mainline_optimized_adaptive`
- `work2_robust_menu` is the V1 mainline suite name.
- Smoke and pilot cover `menu_k={1,2,3,5}`.
- Formal uses fixed `menu_k=3`, declares 5+ paired splits/seeds, and requires checkpoint provenance.
- Phase 3 verifies smoke actual replay only.
- Phase 3 artifact work is eligibility-test-only; builder/table/figure work is deferred.

</specifics>

<deferred>
## Deferred Ideas

- Phase 4: mainline-aware artifact builder, mirrored artifact bundle, manuscript claim guard, generated tables/figures, and manuscript frame.
- Later phase: formal actual replay once checkpoint/runtime cost is acceptable.
- Optional later diagnostic: legacy robust-policy manifest/suite if old `full_display`, `hard_filter`, `robust_risk_adjusted`, `robust_service_guarded`, etc. are still useful.
- V2/later: attention-based choice/scoring.

</deferred>

---

*Phase: 03-mainline-comparison-contract*
*Context gathered: 2026-06-14*
