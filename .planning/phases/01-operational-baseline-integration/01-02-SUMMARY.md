---
phase: 01-operational-baseline-integration
plan: 02
subsystem: manuscript-results
tags: [latex, operational-baselines, results-section, limitations-section, dispatch-floor, artifact-table]

# Dependency graph
requires:
  - phase: 01-01
    provides: method.tex and experiments.tex with operational-baseline taxonomy and policy count updated
provides:
  - "Operational-baseline table placed in main Results section via \ArtifactTable with reader-facing caption"
  - "Interpretation paragraph framing dispatch-floor reference gap and stating what baselines do NOT prove"
  - "Scope note in limitations.tex restricting operational-baseline evidence to RC low-uptake regime"
affects: [04-manuscript-integration, 05-submission-qa-and-traceability]

# Tech tracking
tech-stack:
  added: []
  patterns: [dispatch-floor reference gap framing, honest-baseline-interpretation with explicit negation scope]

key-files:
  created: []
  modified:
    - ooh_code/manuscript/sections/results.tex
    - ooh_code/manuscript/sections/limitations.tex

key-decisions:
  - "Insert operational-baseline content after RC Outside-Option Benchmark and before Cross-Instance Evaluation (per D-08)"
  - "Use operational_baselines_summary.tex with label tab:operational_baselines (per D-06)"
  - "Interpretation explicitly states baselines do not establish service-quality bounds (per D-09)"
  - "Limitations scope note appended to existing instance-coverage paragraph, not as a new paragraph (per D-12)"

patterns-established:
  - "Operational-baseline evidence appears in main results narrative with interpretation, not as a standalone subsection"
  - "Honest-interpretation pattern: state what evidence does NOT prove alongside what it shows"
  - "Limitations scope notes appended to existing relevant paragraphs rather than creating new structural elements"

requirements-completed: [BASE-02]

# Metrics
duration: 2min
completed: 2026-05-14
---

# Phase 01 Plan 02: Operational-Baseline Results Integration Summary

**Placed operational-baseline table in main Results section with dispatch-floor interpretation paragraph and added evidence-scope limitation to limitations.tex**

## Performance

- **Duration:** 2 min
- **Started:** 2026-05-14T14:38:09Z
- **Completed:** 2026-05-14T14:40:45Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- results.tex now includes the operational-baseline table via \ArtifactTable referencing operational_baselines_summary.tex, placed after the RC Outside-Option Benchmark and before Cross-Instance Evaluation
- Reader-facing caption summarizes dispatch-floor reference points and key comparison context
- Interpretation paragraph frames the dispatch-floor reference gap, links to main results table (tab:rc_main_optout), and explicitly states the comparison does not establish service-quality bounds or generalize to higher-uptake regimes
- limitations.tex instance-coverage paragraph now includes a sentence noting the operational-baseline comparison covers only the RC low-uptake regime
- Round 2's "artifact exists but is not integrated" criticism is directly addressed by the table appearing in the main Results narrative with interpretation

## Task Commits

Each task was committed atomically:

1. **Task 1: Add operational-baseline table and interpretation to results.tex** - `04b49ec` (feat)
2. **Task 2: Add operational-baseline scope note to limitations.tex** - `b147d01` (feat)

## Files Created/Modified
- `ooh_code/manuscript/sections/results.tex` - Added \ArtifactTable call and interpretation paragraph between RC Outside-Option Benchmark and Cross-Instance Evaluation subsections
- `ooh_code/manuscript/sections/limitations.tex` - Appended operational-baseline evidence-scope sentence to existing instance-coverage paragraph

## Decisions Made
- Placed operational-baseline content after RC Outside-Option Benchmark and before Cross-Instance Evaluation per D-08, integrating into the existing narrative flow rather than creating a standalone subsection
- Used operational_baselines_summary.tex (label tab:operational_baselines) per D-06, the cleaner single-label version
- Interpretation explicitly states baselines do not establish service-quality bounds per D-09, framing honestly
- Limitations scope note appended to existing instance-coverage paragraph per D-12, matching existing limitations tone

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- Phase 01 (operational-baseline-integration) is now complete: method.tex has the baseline taxonomy, experiments.tex has the updated policy count, results.tex has the table with interpretation, and limitations.tex has the scope note
- The operational-baseline evidence chain is fully integrated from method description through results interpretation to limitations scoping
- Phase 02 (medium-evidence-expansion) can proceed to build additional evidence layers

## Self-Check: PASSED

- FOUND: ooh_code/manuscript/sections/results.tex
- FOUND: ooh_code/manuscript/sections/limitations.tex
- FOUND: .planning/phases/01-operational-baseline-integration/01-02-SUMMARY.md
- FOUND: commit 04b49ec
- FOUND: commit b147d01

---
*Phase: 01-operational-baseline-integration*
*Completed: 2026-05-14*
