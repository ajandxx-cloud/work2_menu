# Phase 11 Context: Attention Ablation And Design Fix

**Gathered:** 2026-06-11
**Status:** Ready for planning
**Mode:** Autonomous smart discuss.

## Phase Boundary

Phase 11 responds to the Phase 10 pilot NO-GO. It creates and runs pilot-only ablations to diagnose whether attention strength, feature weighting, or shared ETA variant changes can produce a positive paired signal while preserving replay fairness.

This phase either selects exactly one formal candidate or stops the superiority claim. It must not proceed to formal evidence from a failed/zero-signal pilot.

## Inputs

- Phase 10 pilot: completed, checkpoint-loaded, complete pairs, but primary delta `0.0`.
- Claim guard blocker: `primary_metric_not_positive`.
- Generated checkpoints from Phase 09 remain available under `work2_coding/outputs/shared_training/work2_attention_dspo/`.

## Decisions

- Add three pilot-only ablation manifests:
  - attention strength high.
  - eta-risk-focused feature weights.
  - shared stronger ETA variant.
- Keep paired replay fairness by varying only declared attention fields between `DSPO_original` and `DSPO_attention`. ETA variant is shared through `base_args`, not policy-specific.
- Pre-register selection criteria before running ablations.
- Run ablations with actual execution after committing manifests so run provenance is clean.
- Select a formal candidate only if exactly one ablation has positive primary delta and service constraints pass. Otherwise stop the superiority claim.

