---
status: diagnostic_provisional_blocked
claim_ready: false
baseline_validation_status: passed
artifact_root: artifacts\work2_robust_menu\phase8_sensitivity
generated_at_utc: 2026-06-15T16:08:53+00:00
source_run_ids:
  - phase8_sensitivity_eta_filter-20260615T160033Z-a1a3724c
  - phase8_sensitivity_guardrail-20260615T160036Z-9276956f
  - phase8_sensitivity_menu_k-20260615T160029Z-1dfd3737
  - phase8_sensitivity_uptake_regime-20260615T160035Z-663b4ce0
---

# Phase 8 Sensitivity Summary

This file is generated from Phase 8 normalized rows and manifest snapshots. It is a diagnostic conditional boundary map, not claim-ready evidence.

## Baseline Gate

Baseline validation status is `passed`; diagnostic sensitivity artifacts were generated with `claim_ready: false`.

## Must-Have Axis Table

| sensitivity_axis | sensitivity_value | rows | acceptance_rate | optout_rate | net_profit | boundary |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| menu_k | 2 | 5 | 0.64 | 0.36 | -1315 | failure_or_lower_profit |
| menu_k | 3 | 5 | 0.6 | 0.4 | -1104 | center_value |
| menu_k | 4 | 5 | 0.64 | 0.36 | -1321 | failure_or_lower_profit |
| eta_filter_mode | chance_constraint | 5 | 0.6 | 0.4 | -1104 | no_observed_change |
| eta_filter_mode | hard | 5 | 0.6 | 0.4 | -1104 | no_observed_change |
| eta_filter_mode | interval_overlap | 5 | 0.6 | 0.4 | -1104 | center_value |
| uptake_regime | low | 5 | 0.6 | 0.4 | -1339 | failure_or_lower_profit |
| uptake_regime | medium | 5 | 0.6 | 0.4 | -986 | center_value |
| guardrail | 0.35 | 5 | 0.6 | 0.4 | -1104 | center_value |
| guardrail | 0.40 | 5 | 0.6 | 0.4 | -1104 | no_observed_change |

## Conditional Boundary Map

- `menu_k=2` is classified as `failure_or_lower_profit` relative to center `3`.
- `menu_k=3` is classified as `center_value` relative to center `3`.
- `menu_k=4` is classified as `failure_or_lower_profit` relative to center `3`.
- `eta_filter_mode=chance_constraint` is classified as `no_observed_change` relative to center `interval_overlap`.
- `eta_filter_mode=hard` is classified as `no_observed_change` relative to center `interval_overlap`.
- `eta_filter_mode=interval_overlap` is classified as `center_value` relative to center `interval_overlap`.
- `uptake_regime=low` is classified as `failure_or_lower_profit` relative to center `medium`.
- `uptake_regime=medium` is classified as `center_value` relative to center `medium`.
- `guardrail=0.35` is classified as `center_value` relative to center `0.35`.
- `guardrail=0.40` is classified as `no_observed_change` relative to center `0.35`.

## Deferred Nice-To-Have Dimensions

- `max_candidates`: candidate pool size sensitivity is deferred.
- `fleet_capacity_stress`: fleet and capacity stress sensitivity is deferred.
- `pricing_bounds`: price-bound sensitivity is deferred.
- `price_sensitivity`: pricing response sensitivity is deferred.

## Claim Boundary

No abstract, conclusion, or managerial claim upgrade is authorized by Phase 8. Results remain `diagnostic_provisional_blocked` with `claim_ready: false`.

## Source Artifacts

- `aggregate-csv_metadata`: `artifacts/work2_robust_menu/phase8_sensitivity/aggregates/sensitivity_axis_summary.csv.metadata.json`
- `aggregate-json_metadata`: `artifacts/work2_robust_menu/phase8_sensitivity/aggregates/sensitivity_axis_summary.json.metadata.json`
- `aggregate_csv`: `artifacts/work2_robust_menu/phase8_sensitivity/aggregates/sensitivity_axis_summary.csv`
- `aggregate_json`: `artifacts/work2_robust_menu/phase8_sensitivity/aggregates/sensitivity_axis_summary.json`
- `axis_table`: `artifacts/work2_robust_menu/phase8_sensitivity/tables/sensitivity_axis_summary.tex`
- `boundary_table`: `artifacts/work2_robust_menu/phase8_sensitivity/tables/sensitivity_boundary_map.tex`
- `latex-axis-table_metadata`: `artifacts/work2_robust_menu/phase8_sensitivity/tables/sensitivity_axis_summary.tex.metadata.json`
- `latex-boundary-table_metadata`: `artifacts/work2_robust_menu/phase8_sensitivity/tables/sensitivity_boundary_map.tex.metadata.json`
- `optout_acceptance_by_axis`: `artifacts/work2_robust_menu/phase8_sensitivity/figures/optout_acceptance_by_axis.png`
- `optout_acceptance_by_axis_metadata`: `artifacts/work2_robust_menu/phase8_sensitivity/figures/optout_acceptance_by_axis.png.metadata.json`
- `profit_service_tradeoff`: `artifacts/work2_robust_menu/phase8_sensitivity/figures/profit_service_tradeoff.png`
- `profit_service_tradeoff_metadata`: `artifacts/work2_robust_menu/phase8_sensitivity/figures/profit_service_tradeoff.png.metadata.json`
- `status`: `artifacts/work2_robust_menu/phase8_sensitivity/ARTIFACT_STATUS.json`
- `status_metadata`: `artifacts/work2_robust_menu/phase8_sensitivity/ARTIFACT_STATUS.json.metadata.json`
