---
phase: 02-medium-evidence-expansion
plan: 02
subsystem: evidence
tags: [bias, mae, filter-validity, eta-diagnostics, ivt-diagnostics]

# Dependency graph
requires:
  - phase: phase22
    provides: eta_compare.json with aggregate variant metrics
provides:
  - filter_validity.json with displayed_eta_bias and displayed_ivt_bias fields
  - filter_validity_summary.tex with ETA Bias and IVT Bias columns
  - Pipeline code changes enabling bias tracking for all future runs
affects: [phase03-manuscript-integration, filter-validity, reviewer-response]

# Tech tracking
tech-stack:
  added: []
  patterns: [signed-error-tracking-in-pipeline, bias-colocation-with-mae]

key-files:
  created: []
  modified:
    - ooh_code/run_menu_compare.py
    - ooh_code/Src/research_pipeline.py
    - ooh_code/scripts/extract_phase22_results.py
    - ooh_code/scripts/extract_phase28_results.py
    - ooh_code/scripts/build_artifacts.py
    - ooh_code/outputs/phase28/filter_validity.json
    - ooh_code/artifacts/tables/filter_validity_summary.tex

key-decisions:
  - "Pipeline modification required: raw signed errors were never persisted; modified run_menu_compare.py to track bias alongside MAE and re-ran phase22_eta_compare study"
  - "Bias columns placed before corresponding MAE columns in table for easy comparison of directional vs absolute error"

patterns-established:
  - "Signed-error tracking: displayed_eta_signed_errors / displayed_ivt_signed_errors tracked in parallel with abs_errors in extract_menu_metrics"
  - "Bias-MAE colocation: table shows Bias then MAE for each metric type, enabling immediate directional assessment"

requirements-completed: [EVID-02]

# Metrics
duration: 45min
completed: 2026-05-14
---

# Phase 2 Plan 02: Filter-Validity Bias Expansion Summary

**Added mean signed error (bias) diagnostics to filter-validity table by modifying pipeline to track signed errors alongside MAE and re-running phase22_eta_compare study**

## Performance

- **Duration:** ~45 min (includes ~35 min study re-run)
- **Started:** 2026-05-14T08:56:00Z
- **Completed:** 2026-05-14T09:41:00Z
- **Tasks:** 2
- **Files modified:** 7

## Accomplishments
- Computed displayed ETA bias and displayed IVT bias for all 4 ETA variants (deployed, heuristic, stronger, oracle)
- Added bias tracking to the simulation pipeline (run_menu_compare.py) for all future runs
- Updated filter_validity.json with bias fields (schema_version 2)
- Rebuilt filter_validity_summary.tex table with ETA Bias and IVT Bias columns
- Added build_filter_validity_artifacts() to build_artifacts.py for reproducible table generation
- Key finding: all ETA variants systematically over-predict ETA (positive bias) and under-predict IVT (negative bias), with |bias| = MAE indicating errors are consistently in one direction

## Task Commits

(No git commits -- workspace is not a git repository)

## Files Created/Modified
- `ooh_code/run_menu_compare.py` - Added signed error tracking alongside absolute errors; added avg_displayed_eta_bias and avg_displayed_ivt_bias to episode metrics output and aggregation keys
- `ooh_code/Src/research_pipeline.py` - Added avg_displayed_eta_bias and avg_displayed_ivt_bias to SUMMARY_NUMERIC_KEYS
- `ooh_code/scripts/extract_phase22_results.py` - Added avg_displayed_eta_bias and avg_displayed_ivt_bias extraction from study summary rows
- `ooh_code/scripts/extract_phase28_results.py` - Added bias fields to filter_validity.json rows; updated table rendering with ETA Bias and IVT Bias columns; updated caption with bias definition; bumped schema to version 2
- `ooh_code/scripts/build_artifacts.py` - Added build_filter_validity_artifacts() function for reproducible table generation; called from main()
- `ooh_code/outputs/phase28/filter_validity.json` - Updated with displayed_eta_bias and displayed_ivt_bias fields on all 4 rows
- `ooh_code/artifacts/tables/filter_validity_summary.tex` - Rebuilt with 10 columns including ETA Bias and IVT Bias

## Decisions Made
- **Pipeline modification required:** The existing pipeline (run_menu_compare.py) only tracked abs(predicted - actual) for displayed errors, discarding the sign. Raw signed errors were never persisted to disk. Modified the pipeline to track signed errors in parallel and re-ran the phase22_eta_compare study to generate new episode metrics with bias values.
- **Bias column placement:** Bias columns placed immediately before the corresponding MAE columns in the table, enabling easy comparison of directional error (bias) vs magnitude (MAE).
- **Table caption updated:** Caption now includes "Bias is mean signed error (predicted - actual); positive values indicate over-prediction" for clarity.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Pipeline modification required to compute bias from existing data**
- **Found during:** Task 1 (computing bias from existing episode-level data)
- **Issue:** The plan instructed to compute bias from existing episode-level data, but the simulation pipeline only stored MAE (mean absolute error), not signed errors. The abs() call in run_menu_compare.py line 161 discarded the sign of each prediction error. No raw per-offer prediction/actual pairs were persisted to disk.
- **Fix:** Modified run_menu_compare.py to also track displayed_eta_signed_errors and displayed_ivt_signed_errors lists in parallel with the existing abs_errors lists. Added avg_displayed_eta_bias and avg_displayed_ivt_bias to the episode metrics output and aggregation keys. Re-ran the phase22_eta_compare study (6 splits, 6 episodes each, 4 ETA variants) to generate new data with bias values.
- **Files modified:** run_menu_compare.py, Src/research_pipeline.py, scripts/extract_phase22_results.py, scripts/extract_phase28_results.py
- **Verification:** Verified bias values are computed correctly: heuristic variant shows ETA bias = 0.0 (no ETA prediction), deployed shows +2582.1 (systematic over-prediction), all IVT biases are negative (systematic under-prediction).

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** The deviation was necessary because the plan's assumption that bias could be computed from "existing episode-level data" was incorrect -- the data only contained MAE. The fix involved modifying 4 source files and re-running the study, which took ~35 minutes but produced accurate bias values rather than estimates.

## Bias Analysis Summary

| ETA Variant | ETA Bias | ETA MAE | IVT Bias | IVT MAE |
|---|---|---|---|---|
| deployed blended ETA | +2582.1 | 2582.1 | -2289.9 | 2289.9 |
| heuristic ETA | 0.0 | 0.0 | -1976.8 | 1976.8 |
| stronger calibrated ETA | +466.2 | 466.2 | -2058.6 | 2058.6 |
| oracle ETA filter proxy | +2237.8 | 2237.8 | -1948.0 | 1948.0 |

Key observations:
- |bias| = MAE for all variants, meaning errors are entirely one-directional (no cancellation)
- ETA predictions systematically over-estimate actual wait times (positive bias)
- IVT predictions systematically under-estimate actual in-vehicle times (negative bias)
- The stronger calibrated ETA variant has the smallest ETA bias (+466.2), 5.5x lower than deployed (+2582.1)

## Issues Encountered
- The plan assumed bias could be computed from existing persisted data, but the simulation pipeline only stored MAE (absolute errors). Required modifying the pipeline and re-running the study.

## Next Phase Readiness
- Filter-validity table now includes directional error information (bias) alongside magnitude (MAE)
- build_artifacts.py can regenerate the table reproducibly
- Ready for Phase 3 manuscript integration: the table caption, column headers, and data are all in place
- Note: the study re-run produced slightly different Gap vs full values (stochastic simulation), which should be noted in manuscript text

---
*Phase: 02-medium-evidence-expansion*
*Completed: 2026-05-14*

## Self-Check: PASSED

All 7 modified files verified present. SUMMARY.md verified present.
