---
phase: 01-operational-baseline-integration
plan: 01
subsystem: manuscript-method
tags: [latex, baselines, operational-baselines, method-section, experiments-section]

# Dependency graph
requires:
  - phase: none
    provides: existing method.tex and experiments.tex with heuristic baselines
provides:
  - "Operational-baseline paragraph in method.tex sec:baselines naming insertion-cost greedy, minimum-lateness ranking, random-top-k"
  - "Updated policy count in experiments.tex from seven to ten policies"
  - "Operational-baseline evaluation note in experiments.tex Policies paragraph"
affects: [02-medium-evidence-expansion, 03-statistical-and-welfare-reframing, 04-manuscript-integration]

# Tech tracking
tech-stack:
  added: []
  patterns: [operational-baseline taxonomy distinct from heuristic baselines, dispatch-floor framing]

key-files:
  created: []
  modified:
    - ooh_code/manuscript/sections/method.tex
    - ooh_code/manuscript/sections/experiments.tex

key-decisions:
  - "Fold operational baselines into existing sec:baselines paragraph rather than creating a new subsection (per D-01)"
  - "Use dispatch-floor framing to structurally distinguish operational baselines from heuristic baselines (per D-10)"
  - "Update experiments.tex policy count to ten to reflect all evaluated policies including operational baselines (per D-02)"

patterns-established:
  - "Operational baselines described after heuristic baselines in a separate paragraph within the same subsection"
  - "Policy count in experiments.tex includes operational baselines and notes they use the same protocol without menu optimization"

requirements-completed: [BASE-01]

# Metrics
duration: 9min
completed: 2026-05-14
---

# Phase 01 Plan 01: Operational-Baseline Method Integration Summary

**Added three operational baselines (insertion-cost greedy, minimum-lateness ranking, random-top-k) to method.tex baseline taxonomy and updated experiments.tex policy count from seven to ten with dispatch-floor framing**

## Performance

- **Duration:** 9 min
- **Started:** 2026-05-14T14:26:44Z
- **Completed:** 2026-05-14T14:35:41Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- method.tex sec:baselines now names and describes insertion-cost greedy, minimum-lateness ranking, and random-top-k as operational baselines in a structurally distinct paragraph
- experiments.tex Policies paragraph updated from "seven policies" to "ten policies" with named operational baselines
- Operational baselines distinguished from heuristic baselines via dispatch-floor framing and explicit structural paragraph break
- Added sentence in experiments.tex noting operational baselines use k=3 and same pricing but bypass surrogate and filtering

## Task Commits

Each task was committed atomically:

1. **Task 1: Add operational-baseline paragraph to method.tex sec:baselines** - `ad71bf7` (feat)
2. **Task 2: Update experiments.tex policy count and add operational-baseline evaluation note** - `abc67db` (feat)

## Files Created/Modified
- `ooh_code/manuscript/sections/method.tex` - Added operational-baseline paragraph after heuristic baselines in sec:baselines
- `ooh_code/manuscript/sections/experiments.tex` - Updated policy count to ten, added operational-baseline names and evaluation note

## Decisions Made
- Folded operational baselines into existing sec:baselines rather than creating a new subsection (D-01 compliance)
- Used dispatch-floor framing to distinguish operational baselines from heuristic baselines (D-10 compliance)
- Updated policy count to ten to reflect all evaluated policies (D-02 compliance)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- method.tex and experiments.tex baseline taxonomy is now complete for Phase 01
- Plan 01-02 can proceed to place the operational-baseline table and connect it in the results narrative
- The "seven-policy comparison" reference in experiments.tex Study structure paragraph is intentionally unchanged (refers to Austin/Seattle reruns of the original seven policies, not the expanded set)

## Self-Check: PASSED

- FOUND: ooh_code/manuscript/sections/method.tex
- FOUND: ooh_code/manuscript/sections/experiments.tex
- FOUND: .planning/phases/01-operational-baseline-integration/01-01-SUMMARY.md
- FOUND: commit ad71bf7
- FOUND: commit abc67db

---
*Phase: 01-operational-baseline-integration*
*Completed: 2026-05-14*
