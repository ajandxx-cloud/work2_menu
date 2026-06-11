# Phase 10 Context: Pilot Attention Evidence Run

**Gathered:** 2026-06-11
**Status:** Ready for planning
**Mode:** Autonomous smart discuss.

## Phase Boundary

Phase 10 runs the checkpoint-backed pilot comparison for `DSPO_original` versus `DSPO_attention`, rebuilds attention artifacts and claim guard, and records a go/no-go decision for formal evidence or ablation.

This phase must not soften unsupported results. If the pilot does not support attention improvement, the decision must be `NO-GO` for the superiority claim.

## Inputs

- Phase 09 generated local, ignored checkpoints:
  - `work2_coding/outputs/shared_training/work2_attention_dspo/pilot/supervised_ml.pt`
  - `work2_coding/outputs/shared_training/work2_attention_dspo/formal/supervised_ml.pt`
- Pilot manifest:
  - `work2_coding/Experiments/studies/pilot_attention_dspo.yaml`
- Artifact builder:
  - `work2_coding/scripts/build_attention_artifacts.py`

## Prior Probe

Phase 09's pilot load probe completed with loaded checkpoint and non-placeholder rows, but the primary mean delta was `0.0`. That probe did not support attention-improves-DSPO. Phase 10 will rerun/rebuild the pilot evidence and let the claim guard decide.

## Decisions

- Run `pilot_attention_dspo` with actual execution.
- Rebuild attention artifacts with `--allow-incomplete --default-mirror` so the claim guard is written even when the claim fails.
- Track lightweight artifact outputs under both `work2_coding/artifacts/work2_attention_dspo/` and `artifacts/work2_attention_dspo/`.
- Write an explicit `10-GO-NOGO.md`.
- Mark the pilot claim as failed/not supported if the primary paired delta is not positive.

