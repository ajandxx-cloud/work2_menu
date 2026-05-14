---
phase: 02-medium-evidence-expansion
plan: 01
subsystem: experiments
tags: [mnl, sensitivity, stress-test, phase27, behavioral]

# Dependency graph
requires:
  - phase: phase-1
    provides: Existing Phase 27 manifests and experiment infrastructure
provides:
  - Fresh MNL sensitivity data across low/medium/higher regimes
  - Updated mnl_sensitivity_summary.tex with 9-row data table
  - New results subsection addressing reviewer Critical 2
affects: [02-02, 02-03, manuscript-narrative]

# Tech tracking
tech-stack:
  added: []
  patterns: [regime-level sensitivity table, stress-test evidence tier]

key-files:
  created: []
  modified:
    - ooh_code/artifacts/tables/mnl_sensitivity_summary.tex
    - ooh_code/manuscript/sections/results.tex

key-decisions:
  - "Rebuilt MNL sensitivity table from fresh Phase 27 run data after suite completed; table expanded from 5 rows (1 low + 4 higher) to 9 rows (3 per regime) covering low, medium, and higher-uptake regimes"
  - "build_artifacts.py lacks a dedicated MNL sensitivity handler, so table was reconstructed directly from aggregate_variant_summary.json data"
  - "Manuscript uses conditional stress-test language per user decision D-MNL-Scope"

patterns-established:
  - "MNL sensitivity table format: Regime, Policy/pricing rule, Evidence status, Gap vs full, Acceptance, Non-home acc., Surplus, Floor hit"
  - "Results subsection pattern: subsection + label + tier label + ArtifactTable + narrative paragraph"

requirements-completed: [EVID-01]

# Metrics
duration: 100min
completed: 2026-05-14
---

# Phase 2 Plan 1: MNL Sensitivity Summary

**MNL parameter sensitivity evidence across 3 uptake regimes with 9-row stress-test table and Critical 2 manuscript response**

## Performance

- **Duration:** ~100 min (experiment-heavy)
- **Started:** 2026-05-14T07:07:07Z
- **Completed:** 2026-05-14T08:47:00Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- Ran all 3 Phase 27 MNL sensitivity studies (low/medium/higher) producing fresh experiment data across 6 split pairs each
- Rebuilt mnl_sensitivity_summary.tex from 5 stale rows to 9 fresh data rows covering all 3 regimes with strict-filter, no-filter, and flat-markdown variants
- Added new "MNL Parameter Sensitivity" subsection to results.tex with stress-test tier label, artifact table reference, and Critical 2 response paragraph

## Files Created/Modified
- `ooh_code/artifacts/tables/mnl_sensitivity_summary.tex` - Updated MNL sensitivity table with fresh Phase 27 data (9 rows: 3 regimes x 3 variants)
- `ooh_code/manuscript/sections/results.tex` - New subsection with Critical 2 evidence response

## Decisions Made
- Reconstructed MNL sensitivity table directly from run JSON data since build_artifacts.py has no dedicated Phase 27 handler
- Table uses same column format as original (Regime, Policy, Evidence status, Gap vs full, Acceptance, Non-home acc., Surplus, Floor hit) for consistency
- Manuscript narrative uses conditional language: "stress-test result conditional on the implemented parameterization"
- Deferred explicit outside-option utility scan noted in manuscript text

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Reconstructed MNL sensitivity table manually from run data**
- **Found during:** Task 1 (artifact rebuild)
- **Issue:** `build_artifacts.py` has no dedicated handler for the phase27_mnl_sensitivity suite -- the generic suite handler looks for rc_main/rc_menu_k_robustness members that don't exist in Phase 27. Running `build_artifacts.py --study phase27_mnl_sensitivity` does not update the MNL sensitivity table.
- **Fix:** Extracted aggregate_variant_summary.json from the latest run of each study (low/medium/high) and reconstructed the .tex table directly with the correct 9-row format
- **Files modified:** ooh_code/artifacts/tables/mnl_sensitivity_summary.tex
- **Verification:** Table has 9 data rows, correct label, all metrics populated

**2. [Rule 3 - Blocking] Ran Phase 27 studies individually instead of as suite**
- **Found during:** Task 1 (experiment run)
- **Issue:** The suite command `python scripts/run_study.py --study phase27_mnl_sensitivity` produced output buffering issues and did not complete all 3 members in a single invocation on Windows
- **Fix:** Ran each member study individually (phase27_mnl_sensitivity_low, phase27_mnl_sensitivity_medium, phase27_mnl_sensitivity_high)
- **Files modified:** None (only output data)
- **Verification:** All 3 study_summary.json files exist with complete variant data

---

**Total deviations:** 2 auto-fixed (2 blocking issues)
**Impact on plan:** Both auto-fixes were necessary for task completion. No scope creep.

## Issues Encountered
- Python output buffering on Windows made it difficult to monitor running experiments; used filesystem polling to track progress
- Each individual study took 8-15 minutes to complete due to 6 split pairs with multiple policy variants

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- MNL sensitivity evidence complete, ready for Phase 2 Plan 2 (filter validity diagnostics) and Plan 3 (operational baselines)
- The manuscript now has a direct Critical 2 response paragraph referencing the sensitivity table
- Future artifact rebuilds may need a dedicated MNL handler added to build_artifacts.py for pipeline consistency

---
*Phase: 02-medium-evidence-expansion*
*Completed: 2026-05-14*

## Self-Check: PASSED

- FOUND: ooh_code/artifacts/tables/mnl_sensitivity_summary.tex (9 data rows, label present)
- FOUND: ooh_code/manuscript/sections/results.tex (all 5 content checks passed)
- FOUND: .planning/phases/02-medium-evidence-expansion/02-01-SUMMARY.md
