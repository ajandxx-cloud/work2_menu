---
phase: 3
phase_name: Mainline Comparison Contract
plan: 03-mainline-comparison-contract
type: implementation
wave: 1
depends_on:
  - phase: 2
    artifact: .planning/phases/02-service-product-contract/02-VERIFICATION.md
files_modified:
  - work2_coding/Src/policy_adapters.py
  - work2_coding/Experiments/studies/smoke_robust_menu.yaml
  - work2_coding/Experiments/studies/pilot_robust_menu.yaml
  - work2_coding/Experiments/studies/formal_robust_menu.yaml
  - work2_coding/Experiments/suites/work2_robust_menu.yaml
  - work2_coding/scripts/test_experiment_contracts.py
  - work2_coding/scripts/test_policy_fairness_contract.py
  - work2_coding/scripts/test_paired_replay_contract.py
  - work2_coding/scripts/test_menu_mode_adapters.py
  - work2_coding/scripts/test_smoke_study_rows.py
  - work2_coding/scripts/test_study_execution_status.py
  - work2_coding/scripts/test_artifact_gates.py
autonomous: true
must_haves:
  truths:
    - 'D-01: Phase 3 保留完整 7-tag 主线比较族。'
    - 'D-02: 7 个主线 tag 必须是 mainline_no_menu、mainline_fixed_menu、mainline_random_menu、mainline_optimized_m、mainline_optimized_mw、mainline_optimized_fixed_window、mainline_optimized_adaptive。'
    - 'D-03: Primary method 是 mainline_optimized_adaptive，组合为 m+w+p / adaptive_window / optimized_menu / lambertw，运行策略为 service_guarded_expected_profit。'
    - 'D-04: mainline_fixed_menu 使用 nearest/top-k proximity，top_k_cheapest 不作为主线 fixed-menu baseline。'
    - 'D-05: mainline_random_menu 从同一 candidate pool seeded deterministic 抽取，并保持相同 menu_k。'
    - 'D-06: mainline_no_menu 是单一 default home product 加 outside option，opt-out 不计作 accepted home pickup。'
    - 'D-07: mainline_optimized_m 和 mainline_optimized_mw 是产品消融；非完整 m+w+p 的 row 必须落到 pricing_mode=no_pricing。'
    - 'D-08: mainline_optimized_fixed_window 与 mainline_optimized_adaptive 区分固定时间窗和自适应/robust 时间窗。'
    - 'D-09: 直接迁移现有 work2_robust_menu suite 作为 V1 主线，三个 robust-menu manifests 都切到 7-tag 主线比较族。'
    - 'D-10: 旧 robust-policy 轴保留 adapter 兼容，但不再作为 work2_robust_menu 主线 manifest 的 required family。'
    - 'D-11: work2_robust_menu suite 继续包含 smoke、pilot、formal，不另起主线 suite 名。'
    - 'D-12: 三个主线 manifests 使用 normalized-row-v2，并显式列出产品、时间窗、菜单、定价、方法、候选、状态、利润和服务字段。'
    - 'D-13: Phase 3 只声明 formal 合同，不训练 formal checkpoint，也不运行 formal actual replay。'
    - 'D-14: formal_robust_menu.yaml 至少声明 5 个 paired splits/seeds，并覆盖 low 与 medium uptake regimes。'
    - 'D-15: Formal 固定 menu_k=3，不展开 {1,2,3,5} 菜单大小矩阵。'
    - 'D-16: Formal manifest 保持 shared_checkpoint.required=true 与 base_args.require_checkpoint=true；checkpoint 缺失时只验证 blocked-row / claim-gate 行为。'
    - 'D-17: menu_k={1,2,3,5} 覆盖放在 smoke 和 pilot 层。'
    - 'D-18: Smoke 必须便宜且实际可执行，用于快速证明 7-tag family 与 menu_k 矩阵能跑通。'
    - 'D-19: Pilot 也覆盖 menu_k={1,2,3,5}，用于提前暴露菜单大小鲁棒性问题。'
    - 'D-20: Formal 固定 menu_k=3，把正式合同成本集中在主线政策比较上。'
    - 'D-21: Phase 3 只包含轻量 artifact eligibility 测试，不生成表图，不深入调整 artifact_builder.py 排名/表格/图形逻辑。'
    - 'D-22: Artifact eligibility 必须阻断 failed、blocked、placeholder-only、diagnostic-only、no-filter-only、checkpoint bad rows。'
    - 'D-23: Phase 4 再处理 mainline-aware artifact builder、mirrored artifact bundle、claim guard 和 manuscript-facing outputs。'
    - 'D-24: Phase 3 不修改 manuscript 正文、不手改 generated artifacts、不生成 formal claim-ready tables/figures。'
    - 'D-25: Phase 3 不引入 attention-based choice/scoring；attention 保持 V2/diagnostic。'
    - 'D-26: Phase 3 不重写 HGS/routing semantics，不改变 opt-out 与 accepted-home 的分离语义。'
    - 'D-27: 当前删除状态的 .planning/PROJECT.md、.planning/REQUIREMENTS.md、.planning/ROADMAP.md、.planning/STATE.md 是 superseded Akkerman planning，Phase 3 不重建这些旧文件。'
requirements:
  - phase2:D-01
  - phase2:D-03
  - phase2:D-05
  - phase2:D-10
  - phase2:D-17
  - phase2:D-24
  - phase3:D-01
  - phase3:D-02
  - phase3:D-03
  - phase3:D-04
  - phase3:D-05
  - phase3:D-06
  - phase3:D-07
  - phase3:D-08
  - phase3:D-09
  - phase3:D-10
  - phase3:D-11
  - phase3:D-12
  - phase3:D-13
  - phase3:D-14
  - phase3:D-15
  - phase3:D-16
  - phase3:D-17
  - phase3:D-18
  - phase3:D-19
  - phase3:D-20
  - phase3:D-21
  - phase3:D-22
  - phase3:D-23
  - phase3:D-24
  - phase3:D-25
  - phase3:D-26
  - phase3:D-27
---

<objective>
把 Phase 2 已验证的服务产品合同落成 `work2_robust_menu` 的 V1 主线比较设计：新增 7 个 mainline adapter tags，直接迁移 smoke/pilot/formal manifests 到 normalized-row-v2 与主线产品/时间窗/菜单比较轴，强化 paired fairness、row contract、failed-row、checkpoint、artifact eligibility 测试，并运行一次实际 smoke replay 证明合同可执行。

本计划不训练或运行 formal，不生成正式论文表图，不手改 generated result rows，不编辑 manuscript 正文，不把 attention 纳入 V1。
</objective>

<truths>
- Runtime root is `work2_coding/`.
- `work2_robust_menu` is the V1 mainline suite name.
- Mainline family has exactly 7 tags.
- Smoke and pilot cover `menu_k={1,2,3,5}`.
- Formal fixes `menu_k=3`, declares 5+ paired splits/seeds, and requires checkpoint provenance.
- Keep opt-out accounting separate from accepted home pickup.
- Preserve paired replay fairness across policy comparisons.
- Make checkpoint load status explicit in row metadata.
- Treat no-filter as diagnostic only.
- Keep attention-based choice/scoring out of V1 scope.
- Do not hand-edit generated result rows or paper artifacts.
- Existing `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, and `.planning/STATE.md` are deleted in the current worktree and were identified by Phase 1 as superseded Akkerman planning files; do not recreate them as part of Phase 3.

## Decision Coverage
- D-01: Phase 3 保留完整 7-tag 主线比较族。
- D-02: 7 个主线 tag 必须是 `mainline_no_menu`、`mainline_fixed_menu`、`mainline_random_menu`、`mainline_optimized_m`、`mainline_optimized_mw`、`mainline_optimized_fixed_window`、`mainline_optimized_adaptive`。
- D-03: Primary method 是 `mainline_optimized_adaptive`，组合为 `m+w+p / adaptive_window / optimized_menu / lambertw`，运行策略为 `service_guarded_expected_profit`。
- D-04: `mainline_fixed_menu` 使用 nearest/top-k proximity，`top_k_cheapest` 不作为主线 fixed-menu baseline。
- D-05: `mainline_random_menu` 从同一 candidate pool seeded deterministic 抽取，并保持相同 `menu_k`。
- D-06: `mainline_no_menu` 是单一 default home product 加 outside option，opt-out 不计作 accepted home pickup。
- D-07: `mainline_optimized_m` 和 `mainline_optimized_mw` 是产品消融；非完整 `m+w+p` 的 row 必须落到 `pricing_mode="no_pricing"`。
- D-08: `mainline_optimized_fixed_window` 与 `mainline_optimized_adaptive` 区分固定时间窗和自适应/robust 时间窗。
- D-09: 直接迁移现有 `work2_robust_menu` suite 作为 V1 主线，三个 robust-menu manifests 都切到 7-tag 主线比较族。
- D-10: 旧 robust-policy 轴保留 adapter 兼容，但不再作为 `work2_robust_menu` 主线 manifest 的 required family。
- D-11: `work2_robust_menu` suite 继续包含 smoke、pilot、formal，不另起主线 suite 名。
- D-12: 三个主线 manifests 使用 `normalized-row-v2`，并显式列出产品、时间窗、菜单、定价、方法、候选、状态、利润和服务字段。
- D-13: Phase 3 只声明 formal 合同，不训练 formal checkpoint，也不运行 formal actual replay。
- D-14: `formal_robust_menu.yaml` 至少声明 5 个 paired splits/seeds，并覆盖 low 与 medium uptake regimes。
- D-15: Formal 固定 `menu_k=3`，不展开 `{1,2,3,5}` 菜单大小矩阵。
- D-16: Formal manifest 保持 `shared_checkpoint.required=true` 与 `base_args.require_checkpoint=true`；checkpoint 缺失时只验证 blocked-row / claim-gate 行为。
- D-17: `menu_k={1,2,3,5}` 覆盖放在 smoke 和 pilot 层。
- D-18: Smoke 必须便宜且实际可执行，用于快速证明 7-tag family 与 `menu_k` 矩阵能跑通。
- D-19: Pilot 也覆盖 `menu_k={1,2,3,5}`，用于提前暴露菜单大小鲁棒性问题。
- D-20: Formal 固定 `menu_k=3`，把正式合同成本集中在主线政策比较上。
- D-21: Phase 3 只包含轻量 artifact eligibility 测试，不生成表图，不深入调整 `artifact_builder.py` 排名/表格/图形逻辑。
- D-22: Artifact eligibility 必须阻断 failed、blocked、placeholder-only、diagnostic-only、no-filter-only、checkpoint bad rows。
- D-23: Phase 4 再处理 mainline-aware artifact builder、mirrored artifact bundle、claim guard 和 manuscript-facing outputs。
- D-24: Phase 3 不修改 manuscript 正文、不手改 generated artifacts、不生成 formal claim-ready tables/figures。
- D-25: Phase 3 不引入 attention-based choice/scoring；attention 保持 V2/diagnostic。
- D-26: Phase 3 不重写 HGS/routing semantics，不改变 opt-out 与 accepted-home 的分离语义。
- D-27: 当前删除状态的 `.planning/PROJECT.md`、`.planning/REQUIREMENTS.md`、`.planning/ROADMAP.md`、`.planning/STATE.md` 是 superseded Akkerman planning，Phase 3 不重建这些旧文件。
</truths>

<tasks>

## Task 1 - Define Mainline Adapter Family

**Type:** code
**Files:**
- `work2_coding/Src/policy_adapters.py`
- `work2_coding/scripts/test_menu_mode_adapters.py`
- `work2_coding/scripts/test_policy_fairness_contract.py`

**Action:**
1. Add explicit known adapter tags:
   - `mainline_no_menu`
   - `mainline_fixed_menu`
   - `mainline_random_menu`
   - `mainline_optimized_m`
   - `mainline_optimized_mw`
   - `mainline_optimized_fixed_window`
   - `mainline_optimized_adaptive`
2. Keep existing legacy robust tags and Phase 2 `contract_*` tags available.
3. For each mainline tag, set `comparison_role`, `menu_mode`, and overrides for:
   - `menu_policy`
   - `menu_eta_filter_mode`
   - `menu_contract_mode`
   - `product_mode`
   - `time_window_mode`
   - `menu_pricing_mode` where needed
4. Ensure exact compositions:
   - `mainline_no_menu`: `m / no_time_window / no_menu / no_pricing`, runtime `home_only`
   - `mainline_fixed_menu`: `m+w+p / fixed_window / fixed_menu / lambertw`, runtime `nearest_heuristic`
   - `mainline_random_menu`: `m+w+p / fixed_window / random_menu / lambertw`, runtime `random_top_k`
   - `mainline_optimized_m`: `m / no_time_window / optimized_menu / no_pricing`, runtime `service_guarded_expected_profit`
   - `mainline_optimized_mw`: `m+w / adaptive_window / optimized_menu / no_pricing`, runtime `service_guarded_expected_profit`
   - `mainline_optimized_fixed_window`: `m+w+p / fixed_window / optimized_menu / lambertw`, runtime `service_guarded_expected_profit`
   - `mainline_optimized_adaptive`: `m+w+p / adaptive_window / optimized_menu / lambertw`, runtime `service_guarded_expected_profit`

**Verify:**
```powershell
cd work2_coding
python scripts/test_menu_mode_adapters.py
python scripts/test_policy_fairness_contract.py
```

**Acceptance Criteria:**
- Mainline tags are accepted by manifest validation.
- Adapter tests assert exact product/time-window/menu/pricing composition for every mainline tag.
- Legacy robust and Phase 2 `contract_*` tags still validate.

## Task 2 - Migrate Robust-Menu Manifests To Mainline Contract

**Type:** config
**Files:**
- `work2_coding/Experiments/studies/smoke_robust_menu.yaml`
- `work2_coding/Experiments/studies/pilot_robust_menu.yaml`
- `work2_coding/Experiments/studies/formal_robust_menu.yaml`
- `work2_coding/Experiments/suites/work2_robust_menu.yaml`
- `work2_coding/scripts/test_experiment_contracts.py`

**Action:**
1. Add `required_policy_tags` to each mainline manifest with the seven mainline tags from Task 1.
2. Replace the old robust-policy family in `smoke_robust_menu`, `pilot_robust_menu`, and `formal_robust_menu` with the mainline family.
3. Keep `no_filter_diagnostic` out of these mainline manifests unless it is explicitly moved to a separate diagnostic/legacy manifest.
4. Upgrade pilot and formal manifests to `normalized-row-v2` output schema fields.
5. Ensure smoke covers `menu_k={1,2,3,5}` cheaply.
6. Ensure pilot also covers `menu_k={1,2,3,5}` while keeping checkpoint and replay fairness.
7. Ensure formal fixes `menu_k=3`, declares at least 5 splits/seeds, includes both low and medium uptake regimes, and does not require Phase 3 to execute formal replay.
8. Preserve paired fields for seed, data seeds, instance, load_data, pricing, HGS times, reopt, checkpoint path, require_checkpoint, menu_k, max_candidates, max_steps, and utility parameters.
9. Keep only legitimate comparison knobs in `varied_fields`.

**Verify:**
```powershell
cd work2_coding
python scripts/test_experiment_contracts.py
python scripts/test_policy_fairness_contract.py
```

**Acceptance Criteria:**
- `load_manifest("smoke_robust_menu")`, `load_manifest("pilot_robust_menu")`, and `load_manifest("formal_robust_menu")` pass.
- All three manifests use normalized-row-v2.
- Smoke and pilot cover `menu_k={1,2,3,5}`.
- Formal has at least 5 splits and fixed `menu_k=3`.
- Suite members remain smoke, pilot, formal.
- Pairing tests prove non-comparison fields do not drift across policies.

## Task 3 - Strengthen Row, Failure, And Eligibility Contract Tests

**Type:** tests
**Files:**
- `work2_coding/scripts/test_paired_replay_contract.py`
- `work2_coding/scripts/test_smoke_study_rows.py`
- `work2_coding/scripts/test_study_execution_status.py`
- `work2_coding/scripts/test_artifact_gates.py`

**Action:**
1. Add row tests for every mainline method composition.
2. Assert non-`m+w+p` rows force `pricing_mode="no_pricing"`.
3. Assert aggregate rows use `candidate_id="aggregate"`.
4. Assert completed rows are not placeholder-only.
5. Assert failed rows carry `status="failed"`, `execution_status="failed"`, `error_type`, and `error_message`.
6. Assert artifact classification blocks failed, blocked, placeholder, no-filter-only, diagnostic-only, and bad-checkpoint rows.
7. Assert mainline synthetic pilot rows can be `claim_ready` only when checkpoint status and row status are valid.
8. Keep this task limited to lightweight eligibility tests; do not rewrite `artifact_builder.py` ranking, tables, or figures in Phase 3.

**Verify:**
```powershell
cd work2_coding
python scripts/test_paired_replay_contract.py
python scripts/test_smoke_study_rows.py
python scripts/test_study_execution_status.py
python scripts/test_artifact_gates.py
```

**Acceptance Criteria:**
- Tests cover all mainline tags.
- Tests preserve Phase 2 guarantees for opt-out, row-v2 fields, checkpoint metadata, and artifact gates.
- No paper-facing tables or figures are generated or hand-edited.

## Task 4 - Execute Mainline Smoke Replay

**Type:** validation
**Files:**
- `work2_coding/scripts/run_study.py`
- `work2_coding/Experiments/studies/smoke_robust_menu.yaml`
- generated local output under `work2_coding/outputs/phase3_verification/`

**Action:**
1. Run import smoke.
2. Run the complete script-style contract test set.
3. Run actual smoke replay:
   ```powershell
   python scripts/run_study.py --study smoke_robust_menu --execute --output-root outputs/phase3_verification
   ```
4. Inspect emitted `study_summary.json` and `normalized_rows.json`.
5. Record Phase 3 verification summary in `.planning/phases/03-mainline-comparison-contract/03-VERIFICATION.md`.

**Verify:**
```powershell
cd work2_coding
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_experiment_contracts.py
python scripts/test_policy_fairness_contract.py
python scripts/test_paired_replay_contract.py
python scripts/test_menu_mode_adapters.py
python scripts/test_smoke_study_rows.py
python scripts/test_study_execution_status.py
python scripts/test_artifact_gates.py
python scripts/run_study.py --study smoke_robust_menu --execute --output-root outputs/phase3_verification
```

**Acceptance Criteria:**
- Import smoke passes.
- All listed tests pass.
- Smoke actual replay completes or produces only explicitly explained failed rows. Preferred closeout is `execution_status="completed"` with all rows completed.
- All smoke rows use normalized-row-v2.
- Output includes all seven mainline policy tags across `menu_k={1,2,3,5}`.
- Checkpoint statuses are explicit; smoke may use `not_requested`.

## Task 5 - Close Phase 3 Without Paper Artifact Mutation

**Type:** docs
**Files:**
- `.planning/phases/03-mainline-comparison-contract/03-VERIFICATION.md`
- `.planning/phases/03-mainline-comparison-contract/03-REVIEW.md` if review notes are needed

**Action:**
1. Write verification summary with commands, pass/fail results, smoke output path, row count, policy tags, `menu_k` coverage, and checkpoint statuses.
2. State explicitly that Phase 3 did not edit generated paper artifacts or manuscript content.
3. List Phase 4 handoff items:
   - artifact pipeline consumes normalized-row-v2 mainline outputs
   - claim guard excludes diagnostic/failed/placeholder/bad-checkpoint rows
   - formal runs require checkpoint and dependency snapshot before claim-ready artifacts

**Verify:**
```powershell
git status --short
```

**Acceptance Criteria:**
- Phase 3 verification artifact exists.
- No manuscript source or generated result row was hand-edited.
- The next executable phase can start from Phase 3 verification and build artifacts in Phase 4.

</tasks>

<verification>
## Required Verification

Run from `work2_coding/`:

```powershell
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_menu_mode_adapters.py
python scripts/test_experiment_contracts.py
python scripts/test_policy_fairness_contract.py
python scripts/test_paired_replay_contract.py
python scripts/test_smoke_study_rows.py
python scripts/test_study_execution_status.py
python scripts/test_artifact_gates.py
python scripts/run_study.py --study smoke_robust_menu --execute --output-root outputs/phase3_verification
```

Optional if Phase 3 changes parser/runtime behavior beyond adapters/manifests:

```powershell
python scripts/test_menu_runtime_contract.py
python scripts/test_product_time_window_modes.py
python scripts/test_service_product_contract.py
```

</verification>

<success_criteria>
- Mainline adapter family exists and is tested.
- `smoke_robust_menu`, `pilot_robust_menu`, and `formal_robust_menu` all validate as normalized-row-v2 mainline manifests.
- Smoke and pilot cover `menu_k={1,2,3,5}`.
- Formal manifest declares at least five paired splits, covers low/medium uptake regimes, fixes `menu_k=3`, and requires checkpoint provenance.
- Paired fairness tests prevent policy-level drift in non-comparison fields.
- Row tests cover method/product/time-window/menu/pricing composition for every mainline tag.
- Artifact gate tests block diagnostic, failed, placeholder, no-filter-only, and bad-checkpoint evidence.
- Actual `smoke_robust_menu` replay runs successfully under `outputs/phase3_verification`.
- Phase 3 closes with `03-VERIFICATION.md`.
- No generated result rows, paper artifacts, or manuscript source are hand-edited.
</success_criteria>

## PLANNING COMPLETE
