# Phase 11 Verification

**Status:** Passed ablation execution; superiority claim stopped
**Date:** 2026-06-11

## Commands

| Check | Command | Result |
|---|---|---|
| Attention manifest contracts | `cd work2_coding; python scripts/test_attention_manifest_contracts.py` | PASS: 9 tests |
| Experiment contracts | `cd work2_coding; python scripts/test_experiment_contracts.py` | PASS: 12 tests |
| Strength ablation | `cd work2_coding; python scripts/run_study.py --study pilot_attention_ablation_strength_high --execute` | PASS: completed |
| Feature-weight ablation | `cd work2_coding; python scripts/run_study.py --study pilot_attention_ablation_eta_feature_focus --execute` | PASS: completed |
| Shared ETA variant ablation | `cd work2_coding; python scripts/run_study.py --study pilot_attention_ablation_shared_eta_stronger --execute` | PASS: completed |

## Requirement Evidence

| Requirement | Evidence | Status |
|---|---|---|
| ABLT-01 | Strength, feature, and shared ETA-variant pilot ablation manifests exist. | Passed |
| ABLT-02 | `11-ABLATION-PREREGISTRATION.md` records varied fields and selection criteria before execution. | Passed |
| ABLT-03 | `test_attention_manifest_contracts.py` verifies policy differences are subsets of each manifest's `varied_fields`; shared ETA variant is base-level, not policy-specific. | Passed |
| ABLT-04 | `11-FORMAL-CANDIDATE-DECISION.md` stops the superiority claim because zero candidates pass. | Passed |

## Claim Verification

All ablations failed the primary claim criterion:

```text
net_objective_proxy_delta_mean = 0.0
blocker = primary_metric_not_positive
```

No formal candidate is selected.

