---
phase: 01-claim-and-filter-reliability-tightening
plan: 02
subsystem: manuscript-claims
tags: [filter-validity, eta-errors, ivt-errors, fn-pruning, key-limitation, operational-conservatism]

# Dependency graph
requires:
  - phase: 01-01
    provides: "Softened stable/stability claims to directionally consistent language"
provides:
  - "Results.tex explains why large ETA/IVT errors do not invalidate near-band FN finding via far-band concentration argument"
  - "Limitations.tex names large prediction errors as a key limitation explicitly"
  - "FILT-04 requirement satisfied"
affects: [03-pdf-polish-and-final-response]

# Tech tracking
tech-stack:
  added: []
patterns: ["Dual framing for filter errors: results explains mechanism (FN concentration), limitations names constraint (key limitation)"]

key-files:
  created: []
  modified:
    - ooh_code/manuscript/sections/results.tex
    - ooh_code/manuscript/sections/limitations.tex

key-decisions:
  - "Added 2 sentences after quantile error paragraph in results.tex with far-band FN concentration and near-band preservation argument"
  - "Added 1 key-limitation sentence in limitations.tex connecting large errors to incomplete operational reliability"
  - "Cited near-band FN rate below 0.04 matching filter_validity_summary.tex data"

patterns-established:
  - "Dual framing: results.tex explains the mechanism, limitations.tex names the constraint explicitly"

requirements-completed: [FILT-04]

# Metrics
duration: 1min
completed: 2026-05-15
---

# Phase 01 Plan 02: Filter-Error Framing Summary

**Added explicit large-error explanation in results (FN pruning concentrates in far band, nearby points preserved) and named large prediction errors as a key limitation in limitations section**

## Performance

- **Duration:** 1 min
- **Started:** 2026-05-15T02:18:16Z
- **Completed:** 2026-05-15T02:19:44Z
- **Tasks:** 1
- **Files modified:** 2

## Accomplishments
- Added 2 sentences after quantile error paragraph in results.tex explaining that FN pruning concentrates in the far distance band (>1500m), preserving nearby meeting points with near-band FN rate below 0.04
- Added key-limitation sentence in limitations.tex filter-validity paragraph naming large prediction errors as "a key limitation" and connecting to the FN concentration pattern argument
- Dual framing achieves both: results explains the mechanism (filtering remains useful because nearby points are preserved), limitations honestly names the constraint (operational reliability cannot be fully established)

## Task Commits

Each task was committed atomically:

1. **Task 1: Add large-error explanation to results.tex and key-limitation language to limitations.tex** - `a40399f` (feat)

## Files Created/Modified
- `ooh_code/manuscript/sections/results.tex` - Added 2 sentences after quantile error paragraph (line 26): FN concentration in far band, near-band FN rate below 0.04, operationally conservative framing
- `ooh_code/manuscript/sections/limitations.tex` - Added 1 sentence in filter-validity paragraph (line 6): large prediction errors as "a key limitation"

## Decisions Made
- Used "operationally conservative" in the new results.tex sentences to connect with the existing FN-pruning paragraph's language
- Cited near-band FN rate as "below 0.04" (matching filter_validity_summary.tex range of 0.011-0.035)
- Referenced Table~\ref{tab:filter_validity_summary} in new results.tex text for traceability
- The key-limitation sentence in limitations.tex explicitly connects to the FN concentration pattern argument from results.tex

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- FILT-04 requirement fully satisfied
- Phase 01 complete (both plans 01-01 and 01-02 done)
- Manuscript now has dual framing: softened claims (directionally consistent) and explicit filter-error limitation
- Ready for phase 02 (operational-baseline uptake decision)

---
*Phase: 01-claim-and-filter-reliability-tightening*
*Completed: 2026-05-15*

## Self-Check: PASSED

- FOUND: ooh_code/manuscript/sections/results.tex
- FOUND: ooh_code/manuscript/sections/limitations.tex
- FOUND: .planning/phases/01-claim-and-filter-reliability-tightening/01-02-SUMMARY.md
- FOUND: commit a40399f
