# M4A Pre-Replay Gate Report

**Phase:** 04 - Execute Selected Claim Path  
**Task:** 04-01-02 - one-pass pre-replay gate and formal readiness check  
**Status:** blocked  
**Routing decision:** Path B diagnostic lock (`04-01-03`)  

## Gate Decision

The one authorized Path A formal readiness pass was executed for `final_robust_menu`.

Final replay is not authorized because `FORMAL_READINESS.json` reports:

- readiness status: `blocked`
- claim_ready_allowed: `false`
- blocker codes: `dirty_git`, `missing_formal_checkpoint`
- checkpoint load status: `missing`
- git_dirty: `true`

Per Phase 3 and the Phase 4 plan, blocked readiness is not permission for a remediation loop. Phase 4 must route directly to the diagnostic Path B lock package.

## Commands Run

All commands were run from `work2_coding/`.

```powershell
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
```

Result:

```text
IMPORT_OK
exit_code: 0
```

```powershell
python scripts/test_calibration_manifests.py
```

Result:

```text
PASS: 5 calibration manifest tests
exit_code: 0
```

```powershell
python scripts/test_calibration_protocol.py
```

Result:

```text
PASS: 4 calibration protocol tests
exit_code: 0
```

```powershell
python scripts/test_frozen_final_settings.py
```

Result:

```text
PASS: 4 frozen final settings tests
exit_code: 0
```

```powershell
python scripts/check_formal_readiness.py --study final_robust_menu --output-root outputs/formal_readiness --diagnostic-ok
```

Result:

```json
{
  "blocker_codes": [
    "dirty_git",
    "missing_formal_checkpoint"
  ],
  "blocker_count": 2,
  "checkpoint_hash": null,
  "checkpoint_status": "missing",
  "claim_ready_allowed": false,
  "dependency_snapshot_hash": "b9de129de5266ea496d3ac2775cb1b3dc6db7ba14bf6d54fe8a4f64005f82c23",
  "git_dirty": true,
  "readiness_json": "outputs\\formal_readiness\\final_robust_menu\\FORMAL_READINESS.json",
  "readiness_markdown": "outputs\\formal_readiness\\final_robust_menu\\FORMAL_READINESS.md",
  "status": "blocked"
}
```

The command returned `exit_code: 0` because `--diagnostic-ok` was used. The JSON status is still blocked and controls routing.

## Readiness Artifacts

- FORMAL_READINESS.json: `work2_coding/outputs/formal_readiness/final_robust_menu/FORMAL_READINESS.json`
- readiness JSON sha256: `8D01AAB20F3DCD99DB0B2EFC59CFB4ACC655E0AA0192531F16C8B5FA41A21D10`
- dependency_snapshot: `work2_coding/outputs/formal_readiness/final_robust_menu/DEPENDENCY_SNAPSHOT.json`
- dependency_snapshot sha256: `B9DE129DE5266EA496D3AC2775CB1B3DC6DB7BA14BF6D54FE8A4F64005F82C23`
- readiness markdown: `work2_coding/outputs/formal_readiness/final_robust_menu/FORMAL_READINESS.md`

## Manifest Evidence

- final manifest path: `work2_coding/Experiments/studies/final_robust_menu.yaml`
- final manifest file sha256: `77278B816F6CCDFB9E260B5A29F4ED4118F7357690A5D82328D77402AAD29696`
- readiness manifest path: `work2_coding/experiments/studies/final_robust_menu.yaml`
- readiness manifest hash: `606403bf0160e67df63dfc4351d16c37148d8c1cfa21618bf3d851bb2afb8148`
- policy tags: `mainline_no_menu`, `mainline_fixed_menu`, `mainline_random_menu`, `mainline_optimized_m`, `mainline_optimized_mw`, `mainline_optimized_fixed_window`, `mainline_optimized_adaptive`
- setting_count: `35`
- split IDs: `final_mainline_low_seed0`, `final_mainline_low_seed1`, `final_mainline_medium_seed0`, `final_mainline_medium_seed1`, `final_mainline_medium_seed2`

## Git Provenance

- git SHA: `50798878f157936e56b9107ea117354d0696b882`
- git_dirty: `true`
- blocker: `dirty_git`

Readiness recorded a dirty working tree. Representative status entries include deleted legacy planning files, modified `.planning/config.json`, and modified paper planning documents. This dirty state is not repaired in Phase 4 because the plan permits only one strict readiness pass and prohibits destructive cleanup or result-chasing.

## Checkpoint Provenance

- checkpoint manifest path: `outputs/shared_training/work2_robust_menu/final/supervised_ml.pt`
- checkpoint resolved path: `work2_coding/outputs/shared_training/work2_robust_menu/final/supervised_ml.pt`
- checkpoint required: `true`
- checkpoint expected status: `loaded`
- checkpoint exists: `false`
- checkpoint hash: `missing`
- checkpoint sidecar path: `work2_coding/outputs/shared_training/work2_robust_menu/final/supervised_ml.pt.sidecar.json`
- checkpoint sidecar hash: `missing`
- checkpoint load status: `missing`
- row metadata probe: `not_run`
- blocker: `missing_formal_checkpoint`

The current filesystem contains `work2_coding/outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt`, but the final manifest requires the `final/` checkpoint path. Phase 4 does not retrain, substitute, or rewrite checkpoint policy.

## Blockers

| Code | Severity | Meaning |
| --- | --- | --- |
| `dirty_git` | blocking | Formal claim-ready readiness requires `git_dirty=false`; the current worktree is dirty. |
| `missing_formal_checkpoint` | blocking | The final manifest requires `outputs/shared_training/work2_robust_menu/final/supervised_ml.pt`, but the resolved file is missing. |

## Authorization Result

Path A gate result: blocked.

Final replay was not run. Artifact generation and Phase 10 final package generation were not run. The next authorized action is the Path B diagnostic manuscript lock package.
