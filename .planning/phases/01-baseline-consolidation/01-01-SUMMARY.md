---
phase: 01-baseline-consolidation
plan: 01
subsystem: experiments
tags: [baseline, smoke-test, menu-policy, dsco_menu, csv]

# Dependency graph
requires: []
provides:
  - "Updated run_baseline_smoke.py with native policy names for all 4 baselines + reference"
  - "Validated baseline smoke CSV (15 rows: 5 methods x 3 seeds)"
  - "Verified YAML smoke_baselines study runs through research pipeline"
affects: [01-baseline-consolidation]

# Tech tracking
tech-stack:
  added: []
  patterns: ["Native policy dispatch instead of monkey-patching for baseline methods"]

key-files:
  created: []
  modified:
    - "ooh_code/scripts/run_baseline_smoke.py"

key-decisions:
  - "home_only uses native 'home_only' policy (D-05: only home pickup offer, no PP candidates)"
  - "cost_L_heuristic uses native 'cost_l_heuristic' policy (D-01: sorts by insertion_cost metadata, not predicted_cost)"
  - "cnn_menu uses 'top_k_cheapest' policy (BASE-05: CNN-prediction-based selection)"
  - "Removed monkey-patching in favor of native policy dispatch in DSPO_Menu._select_menu_candidates"

patterns-established:
  - "Baseline methods map directly to native menu_policy strings in DSPO_Menu"

requirements-completed: [BASE-01, BASE-03, BASE-04, BASE-05, BASE-06, BASE-07]

# Metrics
duration: 7min
completed: 2026-05-28
---

# Phase 01 Plan 01: Baseline Smoke Verification Summary

**Updated baseline smoke runner to use native policy names (home_only, cost_l_heuristic, top_k_cheapest) and verified all 15 runs (5 methods x 3 seeds) produce valid CSV output**

## Performance

- **Duration:** 7 min
- **Started:** 2026-05-28T14:39:18Z
- **Completed:** 2026-05-28T14:45:52Z
- **Tasks:** 2
- **Files modified:** 1

## Accomplishments
- Replaced monkey-patched home_only with native "home_only" policy dispatch in DSPO_Menu
- Corrected cost_L_heuristic to use native "cost_l_heuristic" policy (insertion_cost metadata sort) instead of "insertion_cost_greedy" (predicted_cost sort)
- Corrected cnn_menu to use "top_k_cheapest" (CNN-prediction sort) instead of "menu_optimization"
- All 15 runs (5 methods x 3 seeds) completed without error
- YAML-based smoke_baselines study also runs successfully through research pipeline

## Task Commits

Each task was committed atomically:

1. **Task 1: Update run_baseline_smoke.py to use native policy names** - `346d47d` (feat)
2. **Task 2: Run baseline smoke test and verify CSV output** - No separate commit (CSV output is gitignored; code change committed in Task 1)

## Files Created/Modified
- `ooh_code/scripts/run_baseline_smoke.py` - Replaced BASELINE_METHODS with native policy names, removed patch_home_only function and MethodType import

## Decisions Made
- home_only uses native "home_only" policy per D-05 (only home pickup offer, no PP candidates)
- cost_L_heuristic uses native "cost_l_heuristic" policy per D-01 (uses immediate insertion costs for sorting)
- cnn_menu uses "top_k_cheapest" policy per BASE-05 (CNN-prediction-based selection)
- Removed monkey-patching approach entirely since all policies are natively supported in DSPO_Menu._select_menu_candidates

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- All 4 baselines (home_only, nearest_L, cost_L_heuristic, cnn_menu) and the full_candidate_cnn reference are verified working
- Baseline smoke CSV schema validated with all standard metrics
- Ready for full-scale experiment runs at MVP scale (80 train / 20 test episodes)

## Self-Check: PASSED

- FOUND: ooh_code/scripts/run_baseline_smoke.py
- FOUND: .planning/phases/01-baseline-consolidation/01-01-SUMMARY.md
- FOUND: commit 346d47d

---
*Phase: 01-baseline-consolidation*
*Completed: 2026-05-28*
