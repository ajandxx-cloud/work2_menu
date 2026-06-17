# Frozen Final Settings

final_status: blocked_pending_gate_cleanup

**Purpose:** current-state final freeze record for Phase 4 gate evaluation.

This document is derived from the current manifests and current filesystem state. It is a pre-run, non-tuning record. It does not authorize final replay while pre-replay gates remain blocked.

## Manifest Evidence

- final manifest path: `work2_coding/Experiments/studies/final_robust_menu.yaml`
- final manifest hash: `77278B816F6CCDFB9E260B5A29F4ED4118F7357690A5D82328D77402AAD29696`
- final manifest tier/run mode: `formal` / `formal`
- final output intent: `final_claim_candidate_after_gates`
- calibration manifest path: `work2_coding/Experiments/studies/calibration_robust_menu.yaml`
- calibration manifest hash: `6659DC8AE770C9A857F4B14E2914BD071E8EE7F728BEB41521A802F5D426135E`
- calibration manifest tier/run mode: `pilot` / `pilot`
- calibration output intent: `calibration_only`

## Frozen Runtime Settings

- product mode: `m+w+p`
- time-window mode: `adaptive_window`
- menu-contract mode: `optimized_menu`
- pricing mode: `lambertw`
- run mode: `formal`
- instance: `RC`
- `menu_k`: `3`
- `max_candidates`: `10`
- `menu_exact_threshold`: `8`
- `menu_exact_gap_threshold`: `8`
- ETA filter mode: `interval_overlap`
- service quit-rate guardrail: `0.35`
- menu opt-out guardrail: `0.35`
- HGS reopt time: `1.1`
- HGS final time: `1.5`
- maximum episodes: `10`
- maximum request steps: `100`
- maximum parcel steps: `0.55`

The final manifest states these selected runtime knobs came from the pre-run calibration protocol and were not selected from final rows.

## Seven Policy Tags

The final manifest preserves these seven policy tags:

1. `mainline_no_menu`
2. `mainline_fixed_menu`
3. `mainline_random_menu`
4. `mainline_optimized_m`
5. `mainline_optimized_mw`
6. `mainline_optimized_fixed_window`
7. `mainline_optimized_adaptive`

## Split IDs And Seeds

| split_id | seed | data_seed | data_seed_test | uptake_regime |
| --- | ---: | ---: | ---: | --- |
| `final_mainline_low_seed0` | 501 | 0 | 1 | low |
| `final_mainline_low_seed1` | 502 | 1 | 0 | low |
| `final_mainline_medium_seed0` | 503 | 0 | 1 | medium |
| `final_mainline_medium_seed1` | 504 | 1 | 0 | medium |
| `final_mainline_medium_seed2` | 505 | 0 | 1 | medium |

## Checkpoint Path And Status

- checkpoint path: `work2_coding/outputs/shared_training/work2_robust_menu/final/supervised_ml.pt`
- checkpoint hash: `missing`
- checkpoint sidecar path: `work2_coding/outputs/shared_training/work2_robust_menu/final/supervised_ml.pt.sidecar.json`
- checkpoint sidecar hash: `missing`
- checkpoint load status: `not_checked_missing_file`
- current observed shared-training file: `work2_coding/outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt`

The final manifest requires the `final/` checkpoint path. The current filesystem contains only the `formal/` checkpoint file under `work2_coding/outputs/shared_training/work2_robust_menu/formal/`. Phase 4 does not retrain or substitute checkpoints.

## Paired Fields

The final manifest paired fields are:

`seed`, `data_seed`, `data_seed_test`, `instance`, `load_data`, `pricing`, `hgs_reopt_time`, `hgs_final_time`, `reopt`, `checkpoint_path`, `require_checkpoint`, `allow_checkpoint_mismatch`, `menu_k`, `max_candidates`, `max_steps_r`, `max_steps_p`, `home_util`, `base_util`, `incentive_sens`.

## Varied Fields

The final manifest varied fields are:

`algo_name`, `menu_mode`, `product_mode`, `time_window_mode`, `menu_contract_mode`, `menu_pricing_mode`, `menu_policy`, `menu_eta_filter_mode`, `menu_time_filtering`, `menu_objective_mode`, `menu_eta_chance_threshold`, `menu_eta_soft_penalty_lambda`, `service_quit_penalty`, `service_quit_rate_guardrail`, `menu_outside_penalty_lambda`, `menu_optout_guardrail`, `menu_selection_solver`, `menu_use_exact_eval`.

## Gate Commands

Run from `work2_coding/`:

```powershell
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_calibration_manifests.py
python scripts/test_calibration_protocol.py
python scripts/test_frozen_final_settings.py
python scripts/check_formal_readiness.py --study final_robust_menu --output-root outputs/formal_readiness --diagnostic-ok
```

Final replay is not authorized unless the readiness JSON reports `status=passed`, `claim_ready_allowed=true`, and all Phase 3 pre-replay gates pass.

## Current Blockers

The final rerun is not authorized in the current state because these gates are blocked or unproven:

- `missing_final_checkpoint`: the final manifest checkpoint path is absent in the current filesystem.
- `missing_checkpoint_sidecar`: the final checkpoint sidecar path is absent.
- `dirty_git`: current working tree has 138 porcelain entries, so claim-supporting clean provenance is not available.
- `artifact status`: the current Phase 10 package reports `claim_ready=false`, `strict_claim_guard_claim_ready=false`, 108 blockers, and 4 missing artifacts.
- `readiness_not_yet_passed`: Phase 4 has not yet produced a passing `FORMAL_READINESS.json` for `final_robust_menu`.

## Replay Authorization

Final replay is not authorized while `final_status: blocked_pending_gate_cleanup` remains in effect. If the one-pass formal readiness gate remains blocked, Phase 4 must route to diagnostic lock rather than remediate in a loop.

## Second Final Failure Downgrade

If all gates later pass and final replay starts, a first technical failure permits only one same-settings technical rerun. A second final failure, timeout, or incomplete-row result downgrades the manuscript handoff to conditional service-menu design framing.

If regenerated strict `CLAIM_GUARD.json` remains `claim_ready=false`, the project also downgrades to conditional service-menu design framing without tuning, scale reduction, manifest narrowing, row deletion, or extra replay.
