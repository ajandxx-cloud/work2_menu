# Phase 12 Context: Formal Actual Replay Enablement

**Gathered:** 2026-06-11
**Status:** Ready for planning
**Mode:** Autonomous smart discuss.

## Phase Boundary

Phase 12 replaces the old unconditional formal actual replay block with strict-gated formal execution. It does not assert that the current attention design should proceed to a superiority claim; Phase 11 stopped that claim. This phase only hardens the runner so future valid formal candidates cannot rely on placeholder rows or random checkpoints.

## Existing Behavior

- `run_study.py` rejects contract-only formal placeholder rows.
- `study_execution.actual_rows_for_manifest(...)` unconditionally raises for formal manifests.
- `run_study.py` suite execution skips formal manifests.
- Missing required checkpoints already produce blockers.
- `paired_replay.validate_rows(...)` rejects formal placeholder normalized rows.

## Decisions

- Keep formal contract-only rejection.
- Remove the unconditional formal actual replay raise.
- Allow formal actual replay only through the existing prerequisite and checkpoint gates.
- Let actual suite execution include formal members; contract suite execution still skips formal placeholder generation.
- Add tests for:
  - formal contract-only rejection.
  - missing checkpoint blocker metadata.
  - loaded checkpoint formal actual execution using a tiny temporary manifest.
  - placeholder impossibility.

