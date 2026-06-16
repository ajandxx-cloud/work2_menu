---
final_status: blocked_pending_gate_cleanup
phase: 05-calibration-and-robustness-without-p-hacking
created: 2026-06-15T16:45:00+08:00
timezone: Asia/Shanghai
requirements:
  - CAL-02
  - CAL-03
  - CAL-04
---

# Frozen Final Settings

## Final Status

`final_status: blocked_pending_gate_cleanup`

Final rerun is not authorized. Phase 5 has locked the calibration/final
contract shape, but current readiness and artifact gates still block final
claim evidence:

- `dirty_git` blocks formal readiness and clean provenance.
- Artifact status is blocked because current pilot/formal rows require
  generated `method_family` and `outside_option_util` metadata.
- Claim guard reports `claim_ready: false` and `formal_claim_ready: false`.

This document is a pre-run contract, not evidence. It does not upgrade
manuscript claims.

## Final Manifest Path

Final manifest path:
`work2_coding/Experiments/studies/final_robust_menu.yaml`

Final manifest hash:
`606403bf0160e67df63dfc4351d16c37148d8c1cfa21618bf3d851bb2afb8148`

## Calibration Manifest Path

Calibration manifest path:
`work2_coding/Experiments/studies/calibration_robust_menu.yaml`

Calibration manifest hash:
`d6e343b1b6f6744a40144160edf4d8fdeea708076a14c30808483a8ee9163e71`

## Seven Policy Tags

The calibration and final contracts preserve the seven policy tags:

1. `mainline_no_menu`
2. `mainline_fixed_menu`
3. `mainline_random_menu`
4. `mainline_optimized_m`
5. `mainline_optimized_mw`
6. `mainline_optimized_fixed_window`
7. `mainline_optimized_adaptive`

## Split IDs And Seeds

Calibration split IDs and seeds:

| Split ID | Seed | Data Seed | Data Seed Test | Uptake Regime |
| --- | ---: | ---: | ---: | --- |
| `calibration_mainline_low_seed0` | 401 | 0 | 1 | low |
| `calibration_mainline_low_seed1` | 402 | 1 | 0 | low |
| `calibration_mainline_medium_seed0` | 403 | 0 | 1 | medium |
| `calibration_mainline_medium_seed1` | 404 | 1 | 0 | medium |

Final split IDs and seeds:

| Split ID | Seed | Data Seed | Data Seed Test | Uptake Regime |
| --- | ---: | ---: | ---: | --- |
| `final_mainline_low_seed0` | 501 | 0 | 1 | low |
| `final_mainline_low_seed1` | 502 | 1 | 0 | low |
| `final_mainline_medium_seed0` | 503 | 0 | 1 | medium |
| `final_mainline_medium_seed1` | 504 | 1 | 0 | medium |
| `final_mainline_medium_seed2` | 505 | 0 | 1 | medium |

Proof of separation: calibration and final use distinct split IDs and distinct
seeds. Pilot rows must not become final claim evidence.

## Checkpoint Path And Hash

Calibration checkpoint path:
`outputs/shared_training/work2_robust_menu/calibration/supervised_ml.pt`

Calibration checkpoint hash:
`pending_gate_cleanup_not_available_before_training`

Final checkpoint path:
`outputs/shared_training/work2_robust_menu/final/supervised_ml.pt`

Final checkpoint hash:
`pending_gate_cleanup_not_available_before_training`

Checkpoint sidecar path requirement:

- `outputs/shared_training/work2_robust_menu/calibration/supervised_ml.pt.sidecar.json`
- `outputs/shared_training/work2_robust_menu/final/supervised_ml.pt.sidecar.json`

Checkpoint load-status requirement: `loaded`. The final checkpoint hash must be
recorded after checkpoint training and before final replay. A final replay with
missing, failed, or intentionally mismatched checkpoint status is not
claim-ready.

## Paired Fields

Paired fields:

- `seed`
- `data_seed`
- `data_seed_test`
- `instance`
- `load_data`
- `pricing`
- `hgs_reopt_time`
- `hgs_final_time`
- `reopt`
- `checkpoint_path`
- `require_checkpoint`
- `allow_checkpoint_mismatch`
- `menu_k`
- `max_candidates`
- `max_steps_r`
- `max_steps_p`
- `home_util`
- `base_util`
- `incentive_sens`

## Varied Fields

Varied fields:

- `algo_name`
- `menu_mode`
- `product_mode`
- `time_window_mode`
- `menu_contract_mode`
- `menu_pricing_mode`
- `menu_policy`
- `menu_eta_filter_mode`
- `menu_time_filtering`
- `menu_objective_mode`
- `menu_eta_chance_threshold`
- `menu_eta_soft_penalty_lambda`
- `service_quit_penalty`
- `service_quit_rate_guardrail`
- `menu_outside_penalty_lambda`
- `menu_optout_guardrail`
- `menu_selection_solver`
- `menu_use_exact_eval`

## Runtime Knobs

Selected pre-run defaults:

| Knob | Selected | Rejected Alternatives | Rationale |
| --- | --- | --- | --- |
| `menu_k` | `3` | `2`, `4` | Keeps the current central menu-size contract while allowing pilot sensitivity. |
| `max_candidates` | `10` | `8`, `12` | Preserves formal scale and candidate breadth. |
| `menu_eta_filter_mode` | `interval_overlap` | `hard`, chance thresholds `0.20`, `0.25` | Aligns with robust service-guarded optimized policy semantics. |
| `service_quit_rate_guardrail` | `0.35` | `0.40` | Keeps the existing service guardrail before any evidence-driven adjustment. |
| `menu_optout_guardrail` | `0.35` | `0.40` | Keeps opt-out accounting explicit and conservative. |

These defaults are not selected from final rows. If calibration pilot evidence
selects different settings under the protocol, this file must be updated with
new manifest hashes before final replay.

## Gate Commands

Commands are locked here for future execution, but this plan does not run
calibration or final replay:

```powershell
cd work2_coding
python scripts/train_shared_checkpoint.py --study final_robust_menu --checkpoint-path outputs/shared_training/work2_robust_menu/final/supervised_ml.pt
python scripts/check_formal_readiness.py --study final_robust_menu --output-root outputs/final_readiness
python scripts/run_study.py --study final_robust_menu --execute --output-root outputs/final_v1
python scripts/build_artifacts.py --run-dir <final-run-dir> --claim-ready --readiness-json outputs/final_readiness/final_robust_menu/FORMAL_READINESS.json
python scripts/build_manuscript_frame.py --artifact-root <final-artifact-root>
```

Final replay may start only after:

1. provenance cleanup resolves `dirty_git` for the evidence run;
2. final checkpoint exists, sidecar exists, and checkpoint hash is recorded;
3. readiness passes for `final_robust_menu`;
4. row-generation metadata includes `method_family`, `outside_option_util`,
   opt-out/home/meeting-point accounting fields, status fields, and error
   fields.

## Abort And Downgrade Rules

If the first final rerun fails to support a strong claim, one second
calibration round is allowed only with a new protocol documenting the mechanism
failure and scientific basis for another round.

If the second final rerun fails, force downgrade to conditional service-menu
design framing. The paper may report where optimized menus help or fail, but
must not claim universal superiority.

Guard phrase: conditional service-menu design framing.
