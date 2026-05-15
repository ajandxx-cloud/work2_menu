---
phase: 01-claim-and-filter-reliability-tightening
plan: 01
subsystem: manuscript-claims
tags: [softening, outside-option, mnl-sensitivity, claim-tightening, stable-to-directionally-consistent]

# Dependency graph
requires:
  - phase: none
    provides: "Base manuscript with v1.1 changes applied"
provides:
  - "Softened all stable/stability claims to directionally consistent or not obviously brittle"
  - "CLAIM-02 requirement satisfied"
affects: [02-operational-baseline-uptake-decision, 03-pdf-polish-and-final-response]

# Tech tracking
tech-stack:
  added: []
  patterns: ["Bounded claim language: directionally consistent for stress-test findings, not obviously brittle for robustness framing"]

key-files:
  created: []
  modified:
    - ooh_code/manuscript/sections/results.tex
    - ooh_code/manuscript/sections/limitations.tex
    - ooh_code/manuscript/sections/appendix.tex

key-decisions:
  - "Used directionally consistent as primary replacement for stable in results findings"
  - "Used not obviously brittle within this RC stress test in limitations.tex paragraph 4 (per review language)"
  - "Used directional consistency in limitations.tex paragraph 7 and appendix.tex"
  - "Left calibration-scope paragraph in results.tex unchanged (per D-02 decision)"

patterns-established:
  - "Bounded claim language: stress-test findings use directionally consistent; robustness framing uses not obviously brittle"

requirements-completed: [CLAIM-02]

# Metrics
duration: 2min
completed: 2026-05-15
---

# Phase 01 Plan 01: Claim Softening Summary

**Replaced all stable/stability overclaiming with directionally consistent and not obviously brittle bounded language across results, limitations, and appendix sections**

## Performance

- **Duration:** 2 min
- **Started:** 2026-05-15T02:14:15Z
- **Completed:** 2026-05-15T02:16:03Z
- **Tasks:** 1
- **Files modified:** 3

## Accomplishments
- Softened "stable" to "directionally consistent" in results.tex at lines 53 (MNL sensitivity) and 64 (outside-option scan)
- Replaced "directional stability" with "not obviously brittle within this RC stress test" in limitations.tex paragraph 4
- Replaced "directional stability" with "directional consistency" in limitations.tex paragraph 7 and appendix.tex line 125
- Verified conclusion.tex contains no stable/stability references to outside-option or MNL findings
- Verified table captions use "stable" only in appropriate hedging context (not stable interval estimates)

## Task Commits

Each task was committed atomically:

1. **Task 1: Soften stable claims across manuscript** - `155b73c` (feat)

## Files Created/Modified
- `ooh_code/manuscript/sections/results.tex` - Replaced "stable" with "directionally consistent" at lines 53 and 64
- `ooh_code/manuscript/sections/limitations.tex` - Replaced "directional stability" with bounded language at lines 10 and 14
- `ooh_code/manuscript/sections/appendix.tex` - Replaced "directional stability" with "directional consistency" at line 125

## Decisions Made
- Used "directionally consistent" as the primary replacement for "stable" in results findings (lines 53, 64)
- Used the review's exact "not obviously brittle within this RC stress test" phrasing in limitations.tex paragraph 4
- Used "directional consistency" for remaining "directional stability" instances in limitations.tex paragraph 7 and appendix.tex
- Left calibration-scope paragraph in results.tex (line 67) unchanged per user decision D-02

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- CLAIM-02 requirement fully satisfied
- Manuscript language now consistently uses bounded framing for outside-option and MNL sensitivity findings
- Ready for plan 01-02 (FILT-04: large ETA/IVT error framing)

---
*Phase: 01-claim-and-filter-reliability-tightening*
*Completed: 2026-05-15*

## Self-Check: PASSED

- FOUND: ooh_code/manuscript/sections/results.tex
- FOUND: ooh_code/manuscript/sections/limitations.tex
- FOUND: ooh_code/manuscript/sections/appendix.tex
- FOUND: .planning/phases/01-claim-and-filter-reliability-tightening/01-01-SUMMARY.md
- FOUND: commit 155b73c
