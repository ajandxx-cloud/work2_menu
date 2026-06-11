# Phase 09 Verification

**Status:** Passed for checkpoint pipeline; attention claim probe failed/not supported
**Date:** 2026-06-11
**Runtime root:** `work2_coding/`

## Commands

| Check | Command | Result |
|---|---|---|
| Import smoke | `cd work2_coding; python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` | PASS: `IMPORT_OK` |
| Shared checkpoint trainer test | `cd work2_coding; python scripts/test_shared_checkpoint_training.py` | PASS: 1 test |
| Checkpoint provenance tests | `cd work2_coding; python scripts/test_checkpoint_provenance.py` | PASS: 6 tests |
| Attention manifest contracts | `cd work2_coding; python scripts/test_attention_manifest_contracts.py` | PASS: 7 tests |
| Attention smoke execution tests | `cd work2_coding; python scripts/test_attention_smoke_execution.py` | PASS: 4 tests |
| Generate pilot checkpoint | `cd work2_coding; python scripts/train_shared_checkpoint.py --study pilot_attention_dspo` | PASS: checkpoint and sidecar written; `git_dirty=false` |
| Generate formal checkpoint | `cd work2_coding; python scripts/train_shared_checkpoint.py --study formal_attention_dspo` | PASS: checkpoint and sidecar written; `git_dirty=false` |
| Pilot load through runner | `cd work2_coding; python scripts/run_study.py --study pilot_attention_dspo --execute --max-policies 2` | PASS: completed, non-placeholder, 4 rows, checkpoint status `loaded` |

## Generated Local Checkpoints

Generated files are intentionally local/ignored under `work2_coding/outputs/`.

| Tier | Path | sha256 | Sidecar status |
|---|---|---|---|
| pilot | `work2_coding/outputs/shared_training/work2_attention_dspo/pilot/supervised_ml.pt` | `dd729cf63643e98272ada59287df033bfcd1182492a55a78650ce67b5a55e330` | completed, placeholder=false, weights_changed=true, git_dirty=false |
| formal | `work2_coding/outputs/shared_training/work2_attention_dspo/formal/supervised_ml.pt` | `4552fb9ddaf4189a83ef7fb30a5fe39d7f06a43ff709fbcd9bf73d6193a7c985` | completed, placeholder=false, weights_changed=true, git_dirty=false |

Sidecars record:
- sha256.
- command.
- seed.
- split ID.
- data seed and held-out data seed.
- dataset.
- run_id.
- git commit and dirty status.
- training args.
- timestamp.
- architecture.
- training data source.

## Runner Load Evidence

The pilot runner produced:

```text
execution_status = completed
placeholder_only = false
row_count = 4
checkpoint_statuses = ["loaded"]
git_dirty = false
```

This proves the pilot checkpoint loads through `run_study.py`'s actual replay path. Formal actual replay remains intentionally disabled until Phase 12, but the formal checkpoint matches the same `DSPO_Menu.supervised_ml` architecture and sidecar contract.

## Attention Claim Probe

The pilot load verification run is not a Phase 10 claim decision, but it produced a small paired result:

| Policy | Rows | Mean `net_objective_proxy` | Mean acceptance | Mean opt-out |
|---|---:|---:|---:|---:|
| `DSPO_original` | 2 | -8378.3 | 0.6428571428571429 | 0.35714285714285715 |
| `DSPO_attention` | 2 | -8378.3 | 0.6428571428571429 | 0.35714285714285715 |

Attention delta on the primary proxy is `0.0`. Therefore this probe **does not support** the desired attention-improves-DSPO conclusion. Claim status for this probe is **FAILED / not_supported**.

## Requirement Evidence

| Requirement | Evidence | Status |
|---|---|---|
| CKPT-01 | `scripts/train_shared_checkpoint.py` is the stable entry point. | Passed |
| CKPT-02 | Pilot/formal `.pt` files are trained state_dicts with `weights_changed=true`, not placeholders. | Passed |
| CKPT-03 | Sidecars contain hash, command, seed/split/dataset, run_id, git provenance, training args, timestamp, and architecture. | Passed |
| CKPT-04 | `test_shared_checkpoint_training.py` and pilot `run_study.py --execute` prove load through model/runner paths. | Passed |
| CKPT-05 | Existing checkpoint provenance tests still cover missing/mismatched/random-weight refusal; pilot/formal manifests require checkpoints. | Passed |

## Caveat

The generated checkpoints are trained with `training_data_source=deterministic_synthetic_proxy`. They are real non-placeholder weights and unblock the checkpoint contract, but they do not themselves validate the paper claim. Later Phase 10+ evidence must decide the claim honestly.

