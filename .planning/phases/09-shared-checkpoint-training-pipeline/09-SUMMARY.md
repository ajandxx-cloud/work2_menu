# Phase 09 Summary

**Status:** Complete
**Date:** 2026-06-11

## Completed Work

- Added `work2_coding/scripts/train_shared_checkpoint.py`.
- Added `work2_coding/scripts/test_shared_checkpoint_training.py`.
- Generated local pilot and formal attention checkpoint files.
- Generated sidecars with hashes, commands, seeds/splits, dataset, run_id, git provenance, training args, architecture, timestamp, and warning text.
- Verified pilot checkpoint loading through `run_study.py`.
- Preserved fail-closed checkpoint tests.

## Generated Checkpoints

- Pilot: `work2_coding/outputs/shared_training/work2_attention_dspo/pilot/supervised_ml.pt`
- Formal: `work2_coding/outputs/shared_training/work2_attention_dspo/formal/supervised_ml.pt`

These files are intentionally local/ignored. Their sidecars report `git_dirty=false`, `placeholder=false`, and `weights_changed=true`.

## Claim Status

The Phase 09 checkpoint pipeline is complete, but the small pilot load probe does **not** support attention-improves-DSPO:

- `DSPO_original` mean `net_objective_proxy`: -8378.3
- `DSPO_attention` mean `net_objective_proxy`: -8378.3
- Delta: 0.0

Claim status: **FAILED / not_supported for this probe**.

## Gate

Phase 10 may proceed, but it must treat the checkpoint-backed pilot as a real go/no-go. No positive attention claim is allowed unless the completed pilot/formal evidence supports it.

