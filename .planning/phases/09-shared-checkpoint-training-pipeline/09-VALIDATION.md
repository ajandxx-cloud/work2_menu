# Phase 09 Validation

**Status:** Passed for checkpoint readiness; claim probe failed/not supported
**Date:** 2026-06-11

## Validation Question

Can the project proceed to checkpoint-backed pilot attention evidence without missing-checkpoint, random-weight, or unprovenanceable checkpoint blockers?

## Result

Passed for checkpoint readiness.

Pilot and formal shared checkpoint files now exist locally with sidecars. The pilot checkpoint loaded through `run_study.py`, produced non-placeholder rows, and reported `checkpoint_load_status=loaded`.

The attention-improves-DSPO claim remains unsupported. A small pilot load probe had primary delta `0.0`, so it is explicitly marked **FAILED / not_supported** for claim purposes.

## Validation Checks

| Risk | Validation |
|---|---|
| Checkpoint path missing | Both manifest-declared checkpoint paths exist locally. |
| Placeholder checkpoint | Sidecars record `placeholder=false`, `weights_changed=true`, and training loss reduction. |
| Missing provenance | Sidecars record sha256, command, seed, split, dataset, run_id, git commit, dirty state, args, architecture, timestamp. |
| Dirty training provenance | Both sidecars record `git_dirty=false` at training time. |
| Runner load path untested | Pilot actual replay completed through `run_study.py` with `checkpoint_statuses=["loaded"]`. |
| Fail-closed behavior regressed | `test_checkpoint_provenance.py` still passes. |
| Unsupported result softened | The small pilot probe is explicitly recorded as not supporting the attention claim. |

## Residual Risks

- Formal actual replay is still disabled until Phase 12, so formal checkpoint loading is verified by architecture/sidecar/model-path tests rather than formal runner execution.
- The checkpoints are trained from a deterministic synthetic proxy, not a full historical training run. This is sufficient for Phase 09 checkpoint contract readiness, but not sufficient by itself for the paper claim.

## Gate

Phase 10 may proceed to the checkpoint-backed pilot evidence run. If Phase 10 reproduces zero or negative attention delta, the go/no-go decision must stop or redirect the superiority claim.

