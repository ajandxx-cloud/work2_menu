---
phase: 02-gate-cleanup-plan-without-destructive-changes
plan: 01
subsystem: planning-provenance-readiness
tags: [work2, tr-e, provenance, readiness, checkpoint, claim-guard]
requires:
  - phase: 01-repository-and-evidence-boundary-audit
    provides: current evidence boundary, blocker list, and diagnostic-leaning claim decision
provides:
  - Phase 2 non-destructive gate cleanup action matrix
  - checkpoint and formal-readiness provenance requirements
  - approval-required action register for cleanup, replay, artifacts, mirrors, and manuscript claims
affects: [phase-03, phase-04, formal-readiness, claim-ready-decision, manuscript-claim-boundary]
tech-stack:
  added: []
  patterns:
    - non-destructive blocker-to-action planning
    - fail-closed checkpoint provenance contract
    - approval-required evidence-generation register
key-files:
  created:
    - .planning/milestones/tr_e_completion/M2_GATE_CLEANUP_PLAN.md
    - .planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md
    - .planning/milestones/tr_e_completion/M2_USER_ACTIONS_REQUIRED.md
  modified:
    - .planning/milestones/tr_e_completion/M2_GATE_CLEANUP_PLAN.md
key-decisions:
  - "Dirty working-tree state is classified by risk category and must not be normalized without user approval."
  - "Checkpoint sidecar, checkpoint hash, load status, dependency snapshot, manifest hash, git SHA, dirty state, readiness JSON hash, and source-row checkpoint metadata are required before claim-supporting use."
  - "The four missing Phase 10 package entries are synthetic expected-pattern misses, not proof that specific real files were recently deleted."
  - "Empirical performance, tractability credibility, case validation, adaptive-window increment, and central superiority remain Not Phase 2 repairs."
patterns-established:
  - "Use a Blocker -> Action -> Approval -> Verification matrix for provenance and package cleanup planning."
  - "Keep command templates only inside approval-required or not-executed-in-Phase-2 sections."
requirements-completed: [GATE-01, GATE-02]
duration: 15 min
completed: 2026-06-16
---

# Phase 02 Plan 01: Gate Cleanup Plan Without Destructive Changes Summary

**Non-destructive Work2 gate cleanup plan with dirty-state risk categories, checkpoint/readiness provenance contract, and approval-required evidence actions**

## Performance

- **Duration:** 15 min
- **Started:** 2026-06-16T14:30:49Z
- **Completed:** 2026-06-16T14:45:42Z
- **Tasks:** 5/5 complete
- **Files created:** 3 milestone documents plus this summary

## Accomplishments

- Created `M2_GATE_CLEANUP_PLAN.md` with dirty-git risk categories and a `Blocker -> Action -> Approval -> Verification` cleanup matrix.
- Created `M2_PROVENANCE_REQUIREMENTS.md` with exact required fields for checkpoint, sidecar, load status, dependency snapshot, manifest hash, git provenance, readiness JSON hash, and source-row checkpoint metadata.
- Created `M2_USER_ACTIONS_REQUIRED.md` with destructive and evidence-generating commands routed to approval and marked `not executed in Phase 2`.
- Confirmed the current four missing package entries are synthetic expected-pattern misses from `paper_artifacts.py`.
- Verified active generated evidence roots were not modified by Phase 2 execution.

## Task Commits

Each documentation task was committed atomically:

1. **Task 02-01-01: Classify dirty git and current blocker state** - `00d12d0` (`docs(02-01): classify dirty-git gate state`)
2. **Task 02-01-02: Lock checkpoint and formal-readiness provenance requirements** - `d3ffbd3` (`docs(02-01): lock provenance requirements`)
3. **Task 02-01-03: Map package and claim blockers to cleanup actions** - `1969f75` (`docs(02-01): map blockers to cleanup actions`)
4. **Task 02-01-04: Write approval-required user action register** - `1cf7b32` (`docs(02-01): register approval-required actions`)
5. **Task 02-01-05: Run Phase 2 source assertions and import smoke** - recorded in this summary; no source/evidence modification commit required.

## Files Created/Modified

- `.planning/milestones/tr_e_completion/M2_GATE_CLEANUP_PLAN.md` - Dirty-git classification, source-gate inspection notes, package missing-entry explanation, cleanup matrix, and Not Phase 2 routing.
- `.planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md` - Formal checkpoint/readiness provenance contract and fail-closed blocker codes.
- `.planning/milestones/tr_e_completion/M2_USER_ACTIONS_REQUIRED.md` - Approval-required action register for git cleanup, checkpoint training, readiness, replay, artifacts, mirrors, case execution, and manuscript claims.
- `.planning/phases/02-gate-cleanup-plan-without-destructive-changes/02-SUMMARY.md` - This executor summary.

## Decisions Made

- Treated current regenerated planning and paper boundary modifications as active planning state, not as cleanup targets.
- Treated deleted legacy planning/results files as superseded unless Phase 3 identifies a specific readiness or claim blocker that depends on one legacy file.
- Required recomputed checkpoint file SHA-256 as authoritative; sidecar metadata cannot substitute for hashing the checkpoint file.
- Kept empirical performance, computational tractability, case validation, adaptive-window increment, and central superiority outside Phase 2 repair scope.

## Deviations from Plan

None - plan executed exactly as written.

**Total deviations:** 0 auto-fixed.
**Impact on plan:** No scope expansion. No generated rows, package status, claim guards, figures, tables, mirrors, replay outputs, readiness outputs, or checkpoint files were modified.

## Issues Encountered

- The safe-resume grep for `02-01` found old commits from superseded phase numbering. Inspection showed they touched an old `02-core-semantics-and-robust-menu-logic` phase or stale `ooh_code/` paths, not the current Phase 02 directory or M2 deliverables.
- `PACKAGE_INDEX.json` stores package entries under `entries`; extraction was adjusted before writing the missing-entry explanation.

## Verification

Allowed Phase 2 checks passed.

Import smoke from `work2_coding/`:

```text
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
```

Result:

```text
IMPORT_OK
```

File checks:

```text
Test-Path .planning/milestones/tr_e_completion/M2_GATE_CLEANUP_PLAN.md -> True
Test-Path .planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md -> True
Test-Path .planning/milestones/tr_e_completion/M2_USER_ACTIONS_REQUIRED.md -> True
```

Source assertions:

```text
M2_GATE_CLEANUP_PLAN.md contains Blocker, Action, Approval, Verification, .planning/data/case_studies/missing.yml, and Not Phase 2.
M2_PROVENANCE_REQUIREMENTS.md contains checkpoint_sha256, checkpoint_load_status, readiness_json_sha256, recomputed checkpoint SHA-256 is authoritative, and Phase 2 does not smoke-load checkpoints.
M2_USER_ACTIONS_REQUIRED.md contains run_study.py --execute, train_shared_checkpoint.py, check_formal_readiness.py, build_artifacts.py, build_phase10_paper_artifacts.py, and not executed in Phase 2.
```

Generated-evidence diff check:

```text
git diff --name-only -- work2_coding/outputs work2_coding/artifacts artifacts
```

Printed no paths.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Phase 3 can use the M2 cleanup plan and provenance contract to decide whether
frozen final settings and calibration/final-test separation justify a clean,
pre-registered final replay, or whether the paper should remain conditional
diagnostic.

---
*Phase: 02-gate-cleanup-plan-without-destructive-changes*
*Completed: 2026-06-16*
