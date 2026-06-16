---
phase: 05-calibration-and-robustness-without-p-hacking
plan: 02
subsystem: experiment-contracts
tags: [calibration, final-settings, manifests, paired-replay]
requires:
  - phase: 05-calibration-and-robustness-without-p-hacking
    provides: CALIBRATION_PROTOCOL.md
provides:
  - calibration_robust_menu manifest
  - final_robust_menu manifest
  - frozen final settings contract
  - manifest and frozen-settings guard tests
affects: [final-rerun, artifact-gates, manuscript-claims]
tech-stack:
  added: []
  patterns: [manifest-level pilot/final separation, pre-run frozen setting document]
key-files:
  created:
    - work2_coding/Experiments/studies/calibration_robust_menu.yaml
    - work2_coding/Experiments/studies/final_robust_menu.yaml
    - .planning/results/FROZEN_FINAL_SETTINGS.md
    - work2_coding/scripts/test_calibration_manifests.py
    - work2_coding/scripts/test_frozen_final_settings.py
  modified:
    - .planning/PROJECT.md
    - .planning/ROADMAP.md
    - .planning/REQUIREMENTS.md
    - .planning/STATE.md
key-decisions:
  - "Create distinct calibration and final manifests rather than reusing pilot/formal manifests ambiguously."
  - "Mark final rerun blocked_pending_gate_cleanup until provenance, checkpoint, readiness, artifact metadata, and claim guard gates pass."
requirements-completed: [CAL-01, CAL-02, CAL-03, CAL-04]
duration: 35 min
completed: 2026-06-15
---

# Phase 5 Plan 2: Calibration Manifests And Frozen Final Settings Summary

**Separate calibration/final contracts and blocked frozen settings preserve pilot/final independence**

## Performance

- **Duration:** 35 min
- **Started:** 2026-06-15T16:45:00+08:00
- **Completed:** 2026-06-15T17:20:00+08:00
- **Tasks:** 5
- **Files modified:** 9

## Accomplishments

- Added `calibration_robust_menu.yaml` and `final_robust_menu.yaml` with the
  full seven-tag family, disjoint split IDs/seeds, checkpoint paths, paired
  fields, varied fields, and row provenance schema.
- Wrote `.planning/results/FROZEN_FINAL_SETTINGS.md` with manifest hashes,
  split separation, pending checkpoint hash status, gate commands, and
  downgrade rules.
- Added script-style tests for calibration manifest contracts and frozen final
  settings.
- Updated planning docs to mark Phase 5 as a completed process lock while
  preserving gate blockers before final replay.

## Task Commits

No commits were created during this inline execution. The worktree already
contained extensive unrelated dirty state, and committing selected planning
files would risk mixing user/prior workflow changes into Phase 5 commits.

## Files Created/Modified

- `work2_coding/Experiments/studies/calibration_robust_menu.yaml` - Calibration
  pilot contract.
- `work2_coding/Experiments/studies/final_robust_menu.yaml` - Final formal
  contract.
- `.planning/results/FROZEN_FINAL_SETTINGS.md` - Pre-run frozen settings.
- `work2_coding/scripts/test_calibration_manifests.py` - Manifest guard tests.
- `work2_coding/scripts/test_frozen_final_settings.py` - Frozen settings guard
  tests.
- `.planning/PROJECT.md`, `.planning/ROADMAP.md`,
  `.planning/REQUIREMENTS.md`, `.planning/STATE.md` - Phase 5 status updates.

## Decisions Made

- Used new manifest names to keep calibration rows distinct from existing pilot
  rows and final rows distinct from the prior formal diagnostic run.
- Kept checkpoint hashes pending rather than fabricating values before
  checkpoint training.
- Advanced Phase 5 as complete but did not authorize final rerun.

## Deviations from Plan

### Auto-fixed Issues

**1. Runtime parser rejected unrestricted `data_seed` values**
- **Found during:** Task 2 manifest test
- **Issue:** Initial calibration/final split seeds used unsupported
  `data_seed` values.
- **Fix:** Kept split IDs and `seed` values distinct while using allowed
  `data_seed` / `data_seed_test` values `0` and `1`.
- **Files modified:** `calibration_robust_menu.yaml`,
  `final_robust_menu.yaml`
- **Verification:** `python scripts/test_calibration_manifests.py`

### Documented Deviations

**2. Commit protocol deferred because worktree is already broadly dirty**
- **Found during:** Close-out
- **Issue:** Existing unrelated dirty state spans planning, runtime, manuscript,
  and note files.
- **Fix:** Avoided staging or committing to preserve user/prior changes.
- **Files modified:** None beyond plan scope.
- **Verification:** `git status --short` was inspected only for categorization.

**Total deviations:** 1 auto-fixed, 1 documented.
**Impact on plan:** Contract artifacts are valid; git provenance remains blocked
as expected.

## Issues Encountered

The frozen-settings guard initially failed because the downgrade phrase was
line-wrapped. The document now includes an explicit guard phrase.

## User Setup Required

None.

## Next Phase Readiness

Phase 5 is ready for verification. Phase 6 can be discussed next. Calibration
pilot and final replay remain blocked until gate cleanup conditions are
resolved.

---
*Phase: 05-calibration-and-robustness-without-p-hacking*
*Completed: 2026-06-15*
