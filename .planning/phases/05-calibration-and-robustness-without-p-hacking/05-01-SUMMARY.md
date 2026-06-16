---
phase: 05-calibration-and-robustness-without-p-hacking
plan: 01
subsystem: research-provenance
tags: [calibration, readiness, artifact-gates, no-p-hacking]
requires:
  - phase: 04-rc-result-diagnosis-and-paper-claim-validation
    provides: diagnostic formal RC claim classification and Phase 5 routing
provides:
  - Phase 5 blocker addendum
  - Locked calibration protocol
  - Calibration protocol guard test
affects: [phase-5, phase-6, final-rerun, manuscript-claims]
tech-stack:
  added: []
  patterns: [script-style Python assertions for research protocol guards]
key-files:
  created:
    - .planning/results/CALIBRATION_PROTOCOL.md
    - work2_coding/scripts/test_calibration_protocol.py
  modified:
    - .planning/results/FORMAL_BLOCKER_DIAGNOSIS.md
key-decisions:
  - "Treat Phase 5 as process integrity, not as a better-result phase."
  - "Do not authorize pilot/final execution while dirty-git and artifact gates remain blocked."
requirements-completed: [CAL-01, CAL-04]
duration: 25 min
completed: 2026-06-15
---

# Phase 5 Plan 1: Gate Cleanup And Calibration Protocol Lock Summary

**Calibration protocol and blocker snapshot locked before any pilot or final rerun**

## Performance

- **Duration:** 25 min
- **Started:** 2026-06-15T16:20:00+08:00
- **Completed:** 2026-06-15T16:45:00+08:00
- **Tasks:** 4
- **Files modified:** 3

## Accomplishments

- Added a Phase 5 addendum to `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md`.
- Created `.planning/results/CALIBRATION_PROTOCOL.md` with allowed knobs,
  prohibited tuning, pilot/final separation, second-round limit, and downgrade
  rule.
- Added `work2_coding/scripts/test_calibration_protocol.py` to guard the
  no-p-hacking boundary.
- Verified formal readiness, artifact gates, checkpoint provenance, and the new
  protocol guard test.

## Task Commits

No commits were created during this inline execution. The worktree already
contained extensive unrelated dirty state, and committing selected planning
files would risk mixing user/prior workflow changes into Phase 5 commits.

## Files Created/Modified

- `.planning/results/CALIBRATION_PROTOCOL.md` - Locked calibration protocol.
- `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md` - Phase 5 gate snapshot.
- `work2_coding/scripts/test_calibration_protocol.py` - Script-style guard test.

## Decisions Made

- Kept calibration design allowed but pilot/final execution blocked until
  provenance/readiness and artifact foundations are resolved.
- Treated current formal rows as diagnostic non-tuning input.

## Deviations from Plan

### Documented Deviations

**1. Commit protocol deferred because worktree is already broadly dirty**
- **Found during:** Close-out
- **Issue:** Existing unrelated dirty state spans planning, runtime, manuscript,
  and note files.
- **Fix:** Avoided staging or committing to preserve user/prior changes.
- **Files modified:** None beyond plan scope.
- **Verification:** `git status --short` was inspected only for categorization.

**Total deviations:** 1 documented, no auto-fix.
**Impact on plan:** Artifacts and tests are complete; git provenance remains
blocked as expected.

## Issues Encountered

None beyond the expected dirty-git gate.

## User Setup Required

None.

## Next Phase Readiness

Ready for Plan 2 manifest and frozen-settings lock. Pilot/final execution
remains unauthorized until gate cleanup passes.

---
*Phase: 05-calibration-and-robustness-without-p-hacking*
*Completed: 2026-06-15*
