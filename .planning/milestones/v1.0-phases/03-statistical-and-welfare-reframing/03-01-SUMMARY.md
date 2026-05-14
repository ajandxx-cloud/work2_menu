# Phase 03 Plan 01: Conservative Split-Level Statistical Presentation Summary

## Summary

Relabeled the uncertainty table and all cross-instance statistical language so inference scope is crystal clear: RC has 6 split pairs (mechanism diagnostic with paired range), Austin/Seattle have 2 split pairs each (descriptive only, no interval or CI claims).

## Changes Made

### Task 1: Relabel policy_gap_uncertainty_summary.tex via build_artifacts.py

**Files modified:**
- `ooh_code/scripts/build_artifacts.py` -- Changed interval_kind labels from "split bootstrap interval" / "observed range" to "Split-level range (6 pairs)" / "Two-pair descriptive range". Changed caption from "uncertainty summary" to "gap summary" with added descriptive-only sentence. Changed column header from "Interval type" to "Range type" and "Split-level interval/range" to "Split-level range".
- `ooh_code/artifacts/tables/policy_gap_uncertainty_summary.tex` -- Directly updated to match the build_artifacts.py changes: new caption, new column headers, new range type labels for all 6 rows.

### Task 2: Add descriptive-only labels to results.tex cross-instance section

**File modified:** `ooh_code/manuscript/sections/results.tex`
- Added sentence after `[Descriptive external check.]` tier label: "Austin and Seattle each provide only two split-level evaluation pairs; the city results are reported as descriptive two-pair checks, not as stable generalization estimates."
- Strengthened city-gap sentence to read: "but do not constitute replication or external validation in the inferential sense; stable external validation requires additional city splits and demand calibration."
- Updated ArtifactTable caption from "uncertainty summary" to "gap summary" for consistency.

### Task 3: Add RC statistical context to results.tex

**File modified:** `ooh_code/manuscript/sections/results.tex`
- Added after Table~\ref{tab:policy_gap_uncertainty_summary} reference: "The RC benchmark provides six split-level evaluation pairs. Reported gaps are split-level paired means with the observed range; the percentage effect is computed relative to the full-display net profit."
- Added composition caveat: "When acceptance rates differ between policies (e.g., strict filtering reduces non-home acceptance), the profit gap partially reflects changed request composition rather than purely operational efficiency."

### Task 4: Update managerial.tex statistical language

**File modified:** `ooh_code/manuscript/sections/managerial.tex`
- Added closing sentence: "The cross-instance results are descriptive two-pair checks; the statistical evidence base for menu-optimization value comes from the six-pair RC benchmark and the uptake-regime stress tests."

## Deviations from Plan

None -- plan executed exactly as written.

## Verification

All four must-have criteria confirmed:
1. Austin and Seattle labeled as descriptive two-pair checks with no CI language
2. RC results report split-level mean, range, percentage effect, and acceptance tradeoff
3. Uncertainty table uses "Range type" column and split-level paired range language
4. Cross-instance section has explicit descriptive-only parenthetical after tier label

## Commit

- `8713218`: feat(03-01): relabel uncertainty table and add split-level descriptive language
