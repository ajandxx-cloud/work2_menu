# M4A Final Replay Report

**Phase:** 04 - Execute Selected Claim Path  
**Status:** not_run  
**Reason:** pre-replay gate blocked  

## Replay Status

Final replay was not run.

The one authorized pre-replay readiness pass for `final_robust_menu` produced `status=blocked` and `claim_ready_allowed=false`. The blocking gate report is:

- `.planning/milestones/tr_e_completion/M4A_PRE_REPLAY_GATE_REPORT.md`

Blocking codes:

- `dirty_git`
- `missing_formal_checkpoint`

Because these pre-replay gates failed, Phase 4 did not execute:

```powershell
python scripts/run_study.py --study final_robust_menu --execute --output-root outputs/studies/final_rc
```

No same-settings technical rerun was attempted because replay never started.

## Invariant Accounting

| Field | Status |
| --- | --- |
| completed | `not_applicable_replay_not_run` |
| failed | `not_applicable_replay_not_run` |
| blocked | `pre_replay_gate_blocked` |
| incomplete | `not_applicable_replay_not_run` |
| missing | `final checkpoint missing before replay` |
| manifest hash | `606403bf0160e67df63dfc4351d16c37148d8c1cfa21618bf3d851bb2afb8148` |
| checkpoint | `outputs/shared_training/work2_robust_menu/final/supervised_ml.pt` |
| checkpoint load status | `missing` |
| policy tags | seven mainline tags preserved in manifest |
| split IDs | five final split IDs preserved in manifest |
| technical rerun | `not_attempted` |

## Path Decision

Artifact generation was not authorized. Phase 10 final package generation was not authorized. Phase 4 routes to Path B diagnostic lock.
