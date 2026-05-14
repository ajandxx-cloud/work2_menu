---
phase: 4
plan: 1
subsystem: manuscript-integration
tags: [narrative, terminology, captions, reader-facing]
dependency_graph:
  requires: [03-complete]
  provides: [manuscript-reader-facing-prose]
  affects: [experiments.tex, results.tex, appendix.tex, artifact-tables]
tech_stack:
  added: []
  patterns: [descriptive-label-aliases, journal-facing-captions]
key_files:
  created: []
  modified:
    - ooh_code/manuscript/sections/experiments.tex
    - ooh_code/manuscript/sections/results.tex
    - ooh_code/manuscript/sections/appendix.tex
    - ooh_code/artifacts/tables/phase29_exact_greedy_gap_summary.tex
    - ooh_code/artifacts/tables/phase30_robust_filtering_summary.tex
    - ooh_code/artifacts/tables/phase31_uptake_menu_value_summary.tex
    - ooh_code/artifacts/tables/phase32_operational_baselines_summary.tex
    - ooh_code/artifacts/tables/mnl_sensitivity_summary.tex
    - ooh_code/artifacts/tables/rc_main_optout_summary.tex
    - ooh_code/artifacts/tables/benchmark_bridge_summary.tex
decisions:
  - Keep original phase-numbered labels alongside new reader-facing labels for backward compatibility
  - Pipeline paragraph rewritten to use descriptive suite names instead of code directory names
  - Appendix section label app:split_uncertainty added alongside app:phase19_support
metrics:
  duration: "5 min"
  completed: "2026-05-14"
---

# Phase 4 Plan 1: Narrative, Terminology, and Caption Integration Summary

Replaced all internal phase-numbered references in manuscript prose with descriptive reader-facing labels, added a unifying three-tier study-structure paragraph, converted table captions to journal-facing language with first-use explanations, and added reader-facing code-variable descriptions.

## Tasks Completed

| Task | Description | Status |
|------|-------------|--------|
| 1 | Rewrite experiments.tex companion-studies and pipeline paragraphs | Done |
| 2 | Replace phase names in results.tex prose | Done (no prose changes needed; refs updated in Task 3) |
| 3 | Update artifact table labels for backward compatibility | Done |
| 4 | Fix appendix.tex prose phase references | Done |
| 5 | Update table captions to journal-facing language | Done |
| 6 | Add reader-facing descriptions for code variable names | Done |

## Changes by File

### experiments.tex
- Replaced "Companion studies" paragraph with a unifying "Study structure" paragraph organizing evidence into three tiers: mechanism diagnostics, behavioral stress tests, and descriptive external checks.
- Replaced pipeline paragraph code-name references (`phase27_mnl_sensitivity`, `phase29_exact_greedy_gap`, etc.) with descriptive labels (MNL sensitivity suite, exact-vs-greedy suite, robust-filtering suite, uptake-regime suite).
- Changed "the strict-filter heuristic (implementation policy \texttt{menu\_optimization})" to "the strict-filter menu-optimization policy (\texttt{menu\_optimization})" for first-use clarity.
- Changed "the no-filter heuristic (implementation policy \texttt{menu\_optimization\_v2})" to "the no-filter variant (\texttt{menu\_optimization\_v2})".

### results.tex
- Updated `\ref{tab:phase29_exact_greedy_gap}` to `\ref{tab:exact_greedy_gap}`.
- Updated `\ref{tab:phase30_robust_filtering}` to `\ref{tab:robust_filtering}`.
- Updated `\ref{tab:phase31_uptake_menu_value}` to `\ref{tab:uptake_menu_value}`.

### appendix.tex
- Replaced "Phase 19 uncertainty summary" with "split-level uncertainty summary" in prose.
- Added `\label{app:split_uncertainty}` alongside `\label{app:phase19_support}` for backward compatibility.
- Verbatim blocks (code commands) left unchanged as intended.

### Artifact table labels
- `phase29_exact_greedy_gap_summary.tex`: Added `\label{tab:exact_greedy_gap}`.
- `phase30_robust_filtering_summary.tex`: Added `\label{tab:robust_filtering}`.
- `phase31_uptake_menu_value_summary.tex`: Added `\label{tab:uptake_menu_value}`.
- `phase32_operational_baselines_summary.tex`: Added `\label{tab:operational_baselines_paired}`.
- `mnl_sensitivity_summary.tex`: Already reader-facing (`tab:mnl_sensitivity_summary`), no change needed.
- `operational_baselines_summary.tex`: Already reader-facing (`tab:operational_baselines`), no change needed.

### Table captions updated
- `rc_main_optout_summary.tex`: Replaced terse "RC Main Opt-out Validation policy comparison" with full explanation of outside-option setup and split-level evaluation.
- `benchmark_bridge_summary.tex`: Replaced jargon-heavy "benchmark-role bridge" with plain language explaining RC mechanism vs city impact roles and gate status.
- `mnl_sensitivity_summary.tex`: Removed "Phase 27 sensitivity manifests" internal reference from caption.

### Captions verified (no changes needed)
- `rc_main_optout_welfare_table.tex`: Caption already reader-facing.
- `policy_gap_uncertainty_summary.tex`: Caption already reader-facing (updated in Phase 3).
- `city_split_gap_table.tex`: Caption already reader-facing.

## Deviations from Plan

None -- plan executed exactly as written.

## Known Stubs

None.

## Self-Check: PASSED

All 11 modified/created files verified present. No phase-numbered prose references remain in experiments.tex, results.tex, or appendix.tex (only ArtifactTable file paths and verbatim code blocks retain phase numbers, as intended).
