# Phase 05 Research: Manuscript Framing And Claim Guard

**Date:** 2026-06-11
**Status:** Complete

## Goal

Identify the least risky way to produce paper-ready method/result framing while preserving the Phase 4 evidence boundary: the pipeline exists, but current pilot/formal artifacts are blocked because the required checkpoint is absent and formal evidence was skipped.

## Findings

### Evidence State

- Phase 4 verification passed for the artifact pipeline, not for empirical formal evidence.
- `work2_coding/artifacts/work2_robust_menu/ARTIFACT_STATUS.json` currently reports:
  - `status = blocked`
  - `claim_ready = false`
  - `pilot_claim_ready = false`
  - `formal_claim_ready = false`
  - `placeholder_only = true`
  - checkpoint status `failed`
  - blocker `missing_checkpoint_file`
  - formal blocker `formal_skipped`
- This means Phase 5 can safely describe methods, contracts, artifact families, provenance gates, and limitations, but cannot state effect-size superiority or operational recommendations.

### Best Implementation Shape

- Add a small status-driven manuscript support generator rather than a LaTeX manuscript tree.
- Keep generated files in the artifact bundle:
  - `method_outline.md`
  - `experiment_outline.md`
  - `result_outline.md`
  - `claim_checklist.md`
  - `CLAIM_GUARD.json`
- Mirror the same files to root `artifacts/work2_robust_menu/manuscript/`, matching Phase 4 artifact mirroring.
- Back the generator with tests so claim boundaries are not just prose conventions.

### Claim Categories

Allowed before claim-ready evidence:

- Framework implemented for robust time-window service-menu optimization.
- Robust ETA pruning modes and soft penalty behavior are implemented and tested.
- Exact-small and greedy-large menu construction diagnostics are recorded.
- Smoke/pilot/formal contracts and paired replay metadata are defined.
- Artifact pipeline reports blocked/incomplete status honestly.

Blocked before claim-ready evidence:

- Robust menu universally dominates baselines.
- No-filter is recommended for operations.
- Results validate real passenger behavior.
- The full dynamic DRT system is exactly optimized.
- Pilot/formal effect-size or significance claims are supported.

## Recommended Plan

Use one executable plan with four tasks:

1. Add reusable claim guard helpers.
2. Add a public manuscript-frame generator script.
3. Add deterministic tests for blocked and claim-ready statuses.
4. Generate and mirror the Phase 5 manuscript support artifacts.

## Verification

Minimum checks:

- `cd work2_coding; python scripts/test_manuscript_claim_guard.py`
- `cd work2_coding; python scripts/build_manuscript_frame.py --artifact-root artifacts/work2_robust_menu --mirror-root ../artifacts/work2_robust_menu`
- `cd work2_coding; python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"`

## RESEARCH COMPLETE
