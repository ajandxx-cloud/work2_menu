# Repository Audit: Work2 Menu Time-Window Assortment Optimization RC

## Status

- Artifact status: diagnostic
- Phase: Phase 1 - Repository Audit
- Date: 2026-06-13
- Runtime root: `work2_coding/`
- Phase status: passed

This is an audit-only artifact for the new GSD project
`Work2_Menu_TimeWindow_Assortment_Optimization_RC`. It does not modify product
logic, experiment logic, study behavior, generated rows, or paper artifacts.

## Runtime Verification

| Field | Value |
| --- | --- |
| Working directory | repository root |
| Command | `python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"` |
| Result | `IMPORT_OK` |
| Status | passed |

`work2_coding/` is confirmed as the active importable runtime root. The audit
does not rely on file presence alone.

## Current Module Map

| File or directory | Responsibility | V1 reuse status |
| --- | --- | --- |
| `work2_coding/Src/Algorithms/DSPO_Menu.py` | Main Work2 service-menu algorithm. It defines menu candidate construction, ETA/window filtering, greedy/exact selection paths, expected-profit policies, random/top-k baselines, pricing modes, and metadata diagnostics. | Reusable, but Phase 2/3 must verify explicit `no_time_window`, `fixed_window`, `adaptive_window`, `no_menu`, `fixed_menu`, and `product_mode` contracts. |
| `work2_coding/Src/Algorithms/DSPO.py` | Base DSPO cost-prediction, insertion-cost, pricing, and route-cost machinery. | Reusable as cost-prediction/reference component, not the main V1 comparison axis. |
| `work2_coding/Src/parser.py` | CLI/runtime options. Existing menu flags include `menu_policy`, `menu_k`, `max_candidates`, `menu_selection_solver`, `menu_objective_mode`, `menu_time_filtering`, `menu_eta_filter_mode`, window widths, pricing modes, service guardrails, and attention flags. | Reusable; missing explicit product/time-window/menu mode names required by the new project contract. |
| `work2_coding/Src/config.py` | Builds environments and algorithm class wiring; passes `outside_option_util` and `service_mode` into environments. | Reusable; Phase 2 should verify config exposes new contract fields without breaking legacy scripts. |
| `work2_coding/Src/policy_adapters.py` | Maps manifest policy tags to parser overrides. Current robust-menu tags include `full_display`, `home_only`, `nearest_heuristic`, `top_k_cheapest`, `min_lateness`, `hard_filter`, `no_filter_diagnostic`, `robust_risk_adjusted`, `robust_service_guarded`, and optional `random_top_k`. | Reusable for baseline/adaptor pattern; needs new adapter family for required V1 product-design comparisons. |
| `work2_coding/Src/study_execution.py` | Actual/contract row generation, checkpoint prerequisite checks, blocked-row handling, and summary stats from replay execution. | Reusable; currently reports acceptance, opt-out, home share, meeting-point uptake, revenue, discount, service-time, and checkpoint metadata. |
| `work2_coding/Src/paired_replay.py` | Paired settings, manifest hashing, trace identity, checkpoint metadata, normalized row schema, row validation, and attention pair annotation. | Reusable; schema must be expanded for the requested V1 fields. |
| `work2_coding/Src/artifact_builder.py` | Robust-menu artifact builder for normalized rows, tables, figures, metadata, and claim status. | Reusable for Work2 robust-menu artifacts; V1 needs additional tables/figures for time-window, menu, and product ablations. |
| `work2_coding/Src/attention_artifacts.py` | Attention-vs-original artifact helper and claim guard. | V2/diagnostic only; not V1 ranking evidence. |
| `work2_coding/Environments/OOH/containers.py` | Domain dataclasses. `ServiceBundle` already has `window_start`, `window_end`, `window_center`, `window_width`; `MenuOffer` has bundle, price, ETA, IVT, walk distance, time deviation, utility, profit, metadata; `ChoiceResult` separates `accepted_home`, `accepted_meeting_point`, and `opted_out`. | Strong reusable product-contract base. |
| `work2_coding/Environments/OOH/customerchoice.py` | Choice model with explicit outside option when `outside_option_util` is not `None`; menu choice returns `ChoiceResult`. | Reusable; Phase 2 must make the time-window utility term explicit and auditable in planning and row metadata. |
| `work2_coding/Environments/OOH/Parcelpoint_py.py` | Simulator state, choice application, counters, route mutation, and stats metadata. Counters include `count_opted_out`, `count_accepted_home`, and `count_accepted_meeting_point`. | Reusable; verify all required service metrics and failed-row behavior in later phases. |

## Manifest And Test Inventory

### Studies

Robust-menu studies:

- `work2_coding/Experiments/studies/smoke_robust_menu.yaml`
- `work2_coding/Experiments/studies/pilot_robust_menu.yaml`
- `work2_coding/Experiments/studies/formal_robust_menu.yaml`
- `work2_coding/Experiments/studies/diagnostic_actual_menu.yaml`

Attention/V2 diagnostic studies:

- `work2_coding/Experiments/studies/smoke_attention_dspo.yaml`
- `work2_coding/Experiments/studies/pilot_attention_dspo.yaml`
- `work2_coding/Experiments/studies/formal_attention_dspo.yaml`
- `work2_coding/Experiments/studies/pilot_attention_ablation_strength_high.yaml`
- `work2_coding/Experiments/studies/pilot_attention_ablation_eta_feature_focus.yaml`
- `work2_coding/Experiments/studies/pilot_attention_ablation_shared_eta_stronger.yaml`

### Suites

- `work2_coding/Experiments/suites/work2_robust_menu.yaml`
- `work2_coding/Experiments/suites/work2_attention_dspo.yaml` (V2/diagnostic only)
- `work2_coding/Experiments/suites/work2_attention_ablation.yaml` (V2/diagnostic only)

### Relevant tests

- `work2_coding/scripts/test_optout_accounting.py`
- `work2_coding/scripts/test_paired_replay_contract.py`
- `work2_coding/scripts/test_policy_fairness_contract.py`
- `work2_coding/scripts/test_robust_menu_logic.py`
- `work2_coding/scripts/test_menu_runtime_contract.py`
- `work2_coding/scripts/test_experiment_contracts.py`
- `work2_coding/scripts/test_artifact_gates.py`
- `work2_coding/scripts/test_artifact_builder.py`
- `work2_coding/scripts/test_smoke_study_rows.py`
- `work2_coding/scripts/test_study_execution_status.py`
- `work2_coding/scripts/test_checkpoint_provenance.py`
- `work2_coding/scripts/test_shared_checkpoint_training.py`
- `work2_coding/tests/test_akkerman_rc_no_failure.py` (superseded planning context only)

### Missing or unclear coverage for new V1

- Explicit tests for `no_time_window`, `fixed_window`, and `adaptive_window` named modes.
- Explicit tests for `no_menu`, `fixed_menu`, `random_menu`, and `optimized_menu` named modes.
- Explicit tests for product-ablation modes `m`, `m+w`, and `m+w+p`.
- Schema tests for requested row fields such as `study_id`, `candidate_id`, `method`,
  `pricing_mode`, `menu_mode`, `time_window_mode`, `product_mode`, `status`,
  `error_type`, `error_message`, `net_profit`, `operational_cost`, `total_cost`,
  `served_count`, waiting/schedule deviation, menu utilization, and choice entropy.
- Failure-row tests for continuing batches after candidate failure with status and error metadata.

## Artifact Inventory

Artifact directories were summarized by root and file count; no generated rows,
figures, tables, or paper artifacts were edited.

| Root | File count | Last modified | Trust status |
| --- | ---: | --- | --- |
| `work2_coding/artifacts/work2_actual_smoke` | 25 | 2026-06-11 16:43:29 | smoke/diagnostic |
| `work2_coding/artifacts/work2_attention_dspo` | 8 | 2026-06-11 18:55:15 | V2 diagnostic |
| `work2_coding/artifacts/work2_diagnostic_actual` | 27 | 2026-06-11 16:47:17 | diagnostic |
| `work2_coding/artifacts/work2_robust_menu` | 28 | 2026-06-11 15:39:34 | pilot/formal-style robust-menu evidence; must be revalidated for new V1 claims |
| `work2_coding/outputs/akkerman_rc_no_failure` | 18 | 2026-06-12 23:28:19 | superseded |
| `work2_coding/outputs/shared_training` | 4 | 2026-06-11 22:02:06 | checkpoint/run support; verify per manifest before formal evidence |
| `work2_coding/outputs/studies` | 67 | 2026-06-11 22:13:30 | mixed smoke/pilot/formal study outputs; must be classified by manifest/run |
| `work2_coding/outputs/studies_actual` | 21 | 2026-06-11 16:47:04 | diagnostic actual replay |
| `artifacts/work2_actual_smoke` | 25 | 2026-06-11 16:43:29 | smoke/diagnostic mirror |
| `artifacts/work2_attention_dspo` | 8 | 2026-06-11 22:06:26 | V2 diagnostic mirror |
| `artifacts/work2_diagnostic_actual` | 27 | 2026-06-11 17:00:21 | diagnostic mirror |
| `artifacts/work2_robust_menu` | 28 | 2026-06-11 16:28:40 | robust-menu mirror; revalidate before V1 claims |

The old `akkerman_rc_no_failure` outputs are not Work2 V1 evidence. Attention
artifacts are not Work2 V1 ranking evidence.

## Superseded Planning

Git-tracked old planning files were read from `HEAD` only:

- `.planning/PROJECT.md`
- `.planning/REQUIREMENTS.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`

Those files describe `Akkerman RC No-Failure-Cost Reproduction`, whose core value
was a Table-2-style Akkerman synthetic RC reproduction with home-delivery failure
cost removed. That objective is superseded by
`Work2_Menu_TimeWindow_Assortment_Optimization_RC`.

No old Akkerman reproduction task should be continued as the Work2 V1 objective.
The only reusable context is that `work2_coding/` was already identified as the
active runtime root and `ooh_code/` references were already considered stale.

## Stale Path Mapping

`.planning/codebase/` contains many stale `ooh_code/` references:

| Codebase map | `ooh_code` reference count |
| --- | ---: |
| `ARCHITECTURE.md` | 131 |
| `CONCERNS.md` | 43 |
| `CONVENTIONS.md` | 63 |
| `INTEGRATIONS.md` | 35 |
| `STACK.md` | 46 |
| `STRUCTURE.md` | 119 |
| `TESTING.md` | 51 |

Safe mappings:

| Stale reference | Current equivalent |
| --- | --- |
| `ooh_code/Src/parser.py` | `work2_coding/Src/parser.py` |
| `ooh_code/Src/config.py` | `work2_coding/Src/config.py` |
| `ooh_code/Src/Algorithms/DSPO_Menu.py` | `work2_coding/Src/Algorithms/DSPO_Menu.py` |
| `ooh_code/Src/Algorithms/DSPO.py` | `work2_coding/Src/Algorithms/DSPO.py` |
| `ooh_code/Environments/OOH/containers.py` | `work2_coding/Environments/OOH/containers.py` |
| `ooh_code/Environments/OOH/customerchoice.py` | `work2_coding/Environments/OOH/customerchoice.py` |
| `ooh_code/Environments/OOH/Parcelpoint_py.py` | `work2_coding/Environments/OOH/Parcelpoint_py.py` |
| `ooh_code/scripts/run_study.py` | `work2_coding/scripts/run_study.py` |
| `ooh_code/scripts/build_artifacts.py` | `work2_coding/scripts/build_artifacts.py` |
| `ooh_code/experiments/studies/*.yaml` | `work2_coding/Experiments/studies/*.yaml` |
| `ooh_code/experiments/suites/*.yaml` | `work2_coding/Experiments/suites/*.yaml` |
| `ooh_code/artifacts/` | `work2_coding/artifacts/` |
| `ooh_code/outputs/` | `work2_coding/outputs/` |

Obsolete or unsafe mappings:

- `ooh_code/Src/research_pipeline.py` has no direct same-name equivalent; current orchestration appears split across `work2_coding/Src/experiment_contracts.py`, `work2_coding/Src/paired_replay.py`, `work2_coding/Src/study_execution.py`, and `work2_coding/scripts/run_study.py`.
- `ooh_code/run_menu_compare.py` has no direct same-name equivalent in `work2_coding/`; current study execution should use `work2_coding/scripts/run_study.py` and the paired replay helpers.
- `ooh_code/manuscript/` and `ooh_code/docs/` do not have clear active equivalents in `work2_coding/` from this audit; treat as obsolete until a paper phase verifies manuscript paths.
- `artifacts/work2_cnn_setmenunet/` from stale maps is not the current root-level Work2 artifact family; current root artifact mirrors include `artifacts/work2_robust_menu`, `artifacts/work2_attention_dspo`, `artifacts/work2_actual_smoke`, and `artifacts/work2_diagnostic_actual`.

## Attention Inventory

Attention is V2/diagnostic only and must not be used as the V1 ranking claim.

Attention files:

- `work2_coding/Src/attention_artifacts.py`
- `work2_coding/scripts/build_attention_artifacts.py`
- `work2_coding/scripts/test_attention_artifact_gate.py`
- `work2_coding/scripts/test_attention_manifest_contracts.py`
- `work2_coding/scripts/test_attention_menu_logic.py`
- `work2_coding/scripts/test_attention_paired_rows.py`
- `work2_coding/scripts/test_attention_smoke_execution.py`

Attention manifests/suites:

- `work2_coding/Experiments/studies/smoke_attention_dspo.yaml`
- `work2_coding/Experiments/studies/pilot_attention_dspo.yaml`
- `work2_coding/Experiments/studies/formal_attention_dspo.yaml`
- `work2_coding/Experiments/studies/pilot_attention_ablation_strength_high.yaml`
- `work2_coding/Experiments/studies/pilot_attention_ablation_eta_feature_focus.yaml`
- `work2_coding/Experiments/studies/pilot_attention_ablation_shared_eta_stronger.yaml`
- `work2_coding/Experiments/suites/work2_attention_dspo.yaml`
- `work2_coding/Experiments/suites/work2_attention_ablation.yaml`

Attention artifacts:

- `work2_coding/artifacts/work2_attention_dspo`
- `artifacts/work2_attention_dspo`
- `work2_coding/outputs/studies` entries for attention studies

All of the above are marked `diagnostic` / `V2`. They may inform later design
discussion but are not evidence for the V1 claim that optimized `m+w+p` service
menus improve RC outcomes over structural baselines.

## Reusable Robust-Menu Inventory

Reusable robust-menu files:

- `work2_coding/Src/Algorithms/DSPO_Menu.py`
- `work2_coding/Src/policy_adapters.py`
- `work2_coding/Src/paired_replay.py`
- `work2_coding/Src/study_execution.py`
- `work2_coding/Src/experiment_contracts.py`
- `work2_coding/Src/artifact_builder.py`
- `work2_coding/Src/artifact_status.py`
- `work2_coding/Src/manuscript_claims.py`
- `work2_coding/scripts/run_study.py`
- `work2_coding/scripts/build_artifacts.py`
- `work2_coding/scripts/build_manuscript_frame.py`

Reusable robust-menu manifests:

- `work2_coding/Experiments/studies/smoke_robust_menu.yaml`
- `work2_coding/Experiments/studies/pilot_robust_menu.yaml`
- `work2_coding/Experiments/studies/formal_robust_menu.yaml`
- `work2_coding/Experiments/studies/diagnostic_actual_menu.yaml`
- `work2_coding/Experiments/suites/work2_robust_menu.yaml`

Reusable robust-menu capabilities:

- Manifest-driven study definitions with smoke/pilot/formal tiers.
- Paired fields for seed, data seed, instance, cost predictor/checkpoint path,
  menu size, candidate count, HGS timing, and uptake parameters.
- Policy adapters for full display, home-only cost bound, nearest/cheapest/lateness
  heuristics, hard filter, no-filter diagnostic, risk-adjusted robust menu,
  service-guarded robust menu, and random top-k.
- Explicit checkpoint status and manifest hash in normalized rows.
- Actual-row execution path that separates opt-out, accepted home, and accepted
  meeting-point counts.
- Artifact builders and gates for robust filtering, exact/greedy diagnostics,
  provenance/status, and claim readiness.

Reusable robust-menu artifacts:

- `work2_coding/artifacts/work2_robust_menu`
- `artifacts/work2_robust_menu`
- `work2_coding/outputs/studies` entries for robust-menu studies
- `work2_coding/outputs/shared_training` checkpoint support

Reuse limits:

- Existing robust-menu formal manifest has four formal splits, while the new V1
  prompt requires at least five formal seeds unless explicitly smoke/pilot.
- Existing policies do not yet map cleanly to the required comparison labels:
  `no_time_window`, `fixed_window`, `adaptive_window`, `no_menu`, `fixed_menu`,
  `random_menu`, `optimized_menu`, and product modes `m`, `m+w`, `m+w+p`.
- Existing normalized schema is `normalized-row-v1` but lacks several fields
  required by the new project prompt.

## Phase 2 Risks

- Product contract gap: `ServiceBundle` and `MenuOffer` support windows and prices,
  but the repository does not yet expose an explicit public contract for
  `j=(m,w,p)` with named product modes.
- Time-window mode gap: current runtime has window-width parameters, ETA filters,
  and display-window logic, but no explicit `no_time_window`, `fixed_window`, and
  `adaptive_window` mode names in parser/manifests.
- Menu-mode gap: current `menu_policy` values cover many operational policies,
  but the required `no_menu`, `fixed_menu`, `random_menu`, and `optimized_menu`
  comparison family needs a clean adapter/metadata layer.
- Normalized schema gap: current rows include manifest/checkpoint/filter/policy,
  acceptance/opt-out/home/meeting counts, revenue/discount/service time, and
  exact/greedy diagnostics. Missing or unclear fields include `study_id`,
  `manifest_path`, `candidate_id`, `method`, `pricing_mode`, `menu_mode`,
  `time_window_mode`, `product_mode`, `error_type`, `error_message`,
  `net_profit`, `operational_cost`, `total_cost`, `accepted_count`,
  `served_count`, `served_rate`, `average_waiting_deviation`,
  `average_schedule_deviation`, `menu_size`, `menu_utilization`,
  `choice_entropy`, failed-seed counts, and failure-row tracebacks.
- Formal evidence gap: existing formal robust-menu study has four splits; new V1
  formal evidence requires at least five seeds.
- Claim-guard gap: existing claim guards are robust-menu/attention oriented.
  V1 needs guards for optimized `m+w+p` against no-menu, fixed-menu, random-menu,
  no-window, fixed-window, and product-ablation baselines.
- Artifact trust gap: existing artifacts should be treated as reusable examples or
  prior evidence only until regenerated or revalidated under the new V1 manifest
  contract.
- Stale codebase-map risk: `.planning/codebase/` still references `ooh_code/`
  heavily. Phase 2 should rely on this audit's path mapping rather than stale
  paths.

