---
status: diagnostic_provisional_blocked
claim_ready: false
phase9_gate_status: open
source_run_id: phase9_exact_greedy_tractability-20260616T032010Z-5bc184cd
artifact_root: artifacts/work2_robust_menu/phase9_tractability
generated_at_utc: 2026-06-16T03:22:21+00:00
---

# Phase 9 Computational Tractability Summary

This file is generated from Phase 9 normalized rows, manifest snapshots, and generated artifact status. It is diagnostic/provisional evidence with `claim_ready: false`.

## Status Gate

Prerequisite status context: `PHASE9_DSPO_FAMILY_VALIDATION.json` at `outputs/phase9_dspo_family_validation/PHASE9_DSPO_FAMILY_VALIDATION.json` reports `open`. This gate is prerequisite status context only; it does not authorize claim-ready manuscript language.

## 15-Row Coverage

| paired_group_id | scale_values | completed | blocked | total |
| --- | --- | ---: | ---: | ---: |
| phase9_tractability_low_seed401 | 12; 16; 8 | 3 | 0 | 3 |
| phase9_tractability_low_seed402 | 12; 16; 8 | 3 | 0 | 3 |
| phase9_tractability_medium_seed403 | 12; 16; 8 | 3 | 0 | 3 |
| phase9_tractability_medium_seed404 | 12; 16; 8 | 3 | 0 | 3 |
| phase9_tractability_medium_seed405 | 12; 16; 8 | 3 | 0 | 3 |

Completed rows: `15`; blocked rows: `0`; total rows: `15`.

## Exact-Greedy Table

| solver_scale_value | candidate count | exact_enumerated_menu_count | menu_build_time | relative_optimality_gap | menu_overlap_rate | effective solver | fallback reason |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| 8 | 2.36 | 2.28 | 0.005744 | NA | NA | exact | NA |
| 12 | 2.76 | 3.32 | 0.0037 | NA | NA | exact | NA |
| 16 | 2.76 | 3.32 | 0.003196 | NA | NA | exact | NA |

## Claim Boundary

Tractability interpretation is blocked or explicitly diagnostic because source rows or gates are blocked.
No claim-ready manuscript upgrade is authorized by Phase 9; `claim_ready: false` remains in force.

## Source Artifacts

- `aggregate-csv_metadata`: `artifacts/work2_robust_menu/phase9_tractability/aggregates/exact_greedy_tractability_summary.csv.metadata.json`
- `aggregate-json_metadata`: `artifacts/work2_robust_menu/phase9_tractability/aggregates/exact_greedy_tractability_summary.json.metadata.json`
- `aggregate_csv`: `artifacts/work2_robust_menu/phase9_tractability/aggregates/exact_greedy_tractability_summary.csv`
- `aggregate_json`: `artifacts/work2_robust_menu/phase9_tractability/aggregates/exact_greedy_tractability_summary.json`
- `gap_overlap_by_candidate_count_status`: `artifacts/work2_robust_menu/phase9_tractability/figures/gap_overlap_by_candidate_count.png.status.json`
- `gap_overlap_by_candidate_count_status_metadata`: `artifacts/work2_robust_menu/phase9_tractability/figures/gap_overlap_by_candidate_count.png.status.json.metadata.json`
- `latex-table_metadata`: `artifacts/work2_robust_menu/phase9_tractability/tables/exact_greedy_tractability.tex.metadata.json`
- `menu_build_time_by_candidate_count`: `artifacts/work2_robust_menu/phase9_tractability/figures/menu_build_time_by_candidate_count.png`
- `menu_build_time_by_candidate_count_metadata`: `artifacts/work2_robust_menu/phase9_tractability/figures/menu_build_time_by_candidate_count.png.metadata.json`
- `status`: `artifacts/work2_robust_menu/phase9_tractability/ARTIFACT_STATUS.json`
- `status_metadata`: `artifacts/work2_robust_menu/phase9_tractability/ARTIFACT_STATUS.json.metadata.json`
- `tractability_table`: `artifacts/work2_robust_menu/phase9_tractability/tables/exact_greedy_tractability.tex`

## Validation Notes

- `large_row_not_greedy`: Large solver-scale rows must use the greedy effective solver when completed.
- `large_fallback_reason_missing`: Completed large solver-scale rows must report above_exact_threshold fallback metadata.
- `large_row_not_greedy`: Large solver-scale rows must use the greedy effective solver when completed.
- `large_fallback_reason_missing`: Completed large solver-scale rows must report above_exact_threshold fallback metadata.
- `large_row_not_greedy`: Large solver-scale rows must use the greedy effective solver when completed.
- `large_fallback_reason_missing`: Completed large solver-scale rows must report above_exact_threshold fallback metadata.
- `large_row_not_greedy`: Large solver-scale rows must use the greedy effective solver when completed.
- `large_fallback_reason_missing`: Completed large solver-scale rows must report above_exact_threshold fallback metadata.
- `large_row_not_greedy`: Large solver-scale rows must use the greedy effective solver when completed.
- `large_fallback_reason_missing`: Completed large solver-scale rows must report above_exact_threshold fallback metadata.
- `large_row_not_greedy`: Large solver-scale rows must use the greedy effective solver when completed.
- `large_fallback_reason_missing`: Completed large solver-scale rows must report above_exact_threshold fallback metadata.
- `large_row_not_greedy`: Large solver-scale rows must use the greedy effective solver when completed.
- `large_fallback_reason_missing`: Completed large solver-scale rows must report above_exact_threshold fallback metadata.
- `large_row_not_greedy`: Large solver-scale rows must use the greedy effective solver when completed.
- `large_fallback_reason_missing`: Completed large solver-scale rows must report above_exact_threshold fallback metadata.
- `large_row_not_greedy`: Large solver-scale rows must use the greedy effective solver when completed.
- `large_fallback_reason_missing`: Completed large solver-scale rows must report above_exact_threshold fallback metadata.
- `large_row_not_greedy`: Large solver-scale rows must use the greedy effective solver when completed.
- `large_fallback_reason_missing`: Completed large solver-scale rows must report above_exact_threshold fallback metadata.
