# Phase 03 Plan 02: Profit, Acceptance, and Welfare Tradeoff Summary

Profit decomposition table, consumer surplus appendix, and tradeoff framing integrated into results, managerial, and limitations sections.

## Files Created

| File | Description |
|------|-------------|
| `ooh_code/artifacts/tables/profit_decomposition_summary.tex` | LaTeX booktabs table with fare revenue, discount cost, travel cost, service cost, failure cost, net profit, and accepted requests per policy |

## Files Modified

| File | Changes |
|------|---------|
| `ooh_code/scripts/build_artifacts.py` | Added `build_profit_decomposition_artifacts()` function and wired it into `build_single_study_artifacts()` for `rc_main_optout` |
| `ooh_code/manuscript/sections/results.tex` | Added profit-gap decomposition paragraph after RC Outside-Option Benchmark subsection; added welfare caveat paragraph after Uptake-Regime Menu Value subsection |
| `ooh_code/manuscript/sections/appendix.tex` | Added `\section{Consumer Surplus Computation}` (Appendix label `app:consumer_surplus`) with MNL surplus formula, all-request vs accepted-user definitions, and outside-option treatment |
| `ooh_code/manuscript/sections/managerial.tex` | Added four-dimension tradeoff narrative paragraph referencing profit decomposition table and consumer surplus appendix |
| `ooh_code/manuscript/sections/limitations.tex` | Added surplus-formula caveat and acceptance-change selection-effect interpretation note after MNL parameters paragraph |

## Decisions

- Used the latest RC opt-out run (20260423T032100Z) for the decomposition table values; all seven policies included (3 headline + 4 secondary)
- Placed the welfare caveat in the Uptake-Regime subsection rather than its own subsection, to maintain section flow
- Consumer surplus appendix uses `\section{}` level (consistent with other appendix sections in the file)

## Deviations from Plan

None - plan executed exactly as written.

## Duration

Approximately 2 minutes.

## Self-Check: PASSED

All 6 files verified present. Cross-references confirmed: `tab:profit_decomposition` (defined in table, referenced in results.tex line 55, managerial.tex line 11), `app:consumer_surplus` (defined in appendix.tex line 201, referenced in managerial.tex line 11, limitations.tex line 11).
