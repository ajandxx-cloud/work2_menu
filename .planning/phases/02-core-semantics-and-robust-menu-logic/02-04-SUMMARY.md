---
phase: 02-core-semantics-and-robust-menu-logic
plan: 04
subsystem: robust-menu-logic
tags: [eta, robust-filtering, objective, solver-diagnostics, tests]
requires:
  - phase: 02-core-semantics-and-robust-menu-logic
    provides: 02-02 opt-out accounting
  - phase: 02-core-semantics-and-robust-menu-logic
    provides: 02-03 checkpoint provenance
provides:
  - canonical robust ETA filter modes
  - candidate-level ETA diagnostics
  - soft ETA risk objective penalty
  - service-guarded fallback diagnostics
  - exact-small and greedy-large solver diagnostics
  - robust menu logic regression tests
affects: [phase-03, paired-replay, experiment-contracts, approximation-evidence]
tech-stack:
  added: []
  patterns: [candidate diagnostics metadata, objective risk penalty, exact/greedy solver telemetry]
key-files:
  created:
    - work2_coding/scripts/test_robust_menu_logic.py
  modified:
    - work2_coding/Src/Algorithms/DSPO_Menu.py
    - work2_coding/Src/parser.py
key-decisions:
  - "ETA filter modes emit canonical names while preserving the legacy `interval` alias."
  - "`none` disables ETA pruning only; capacity and routing feasibility checks remain outside the ETA filter."
  - "`soft_penalty` retains ETA-risky candidates and applies the risk through objective value metadata."
  - "Threshold-based exact-to-greedy fallback is recorded explicitly; no separate time-budget fallback control was introduced."
patterns-established:
  - "Per-candidate ETA diagnostics include pass/fail, uncertainty, violation probability, source, risk, and retention fields."
  - "Menu objective evaluation writes ETA risk penalty fields into offer metadata."
  - "Solver paths report requested/effective solver, candidate count, enumeration count, and fallback reason."
requirements-completed: [ETA-01, ETA-02, ETA-03, ETA-04, MENU-01, MENU-03, MENU-04]
duration: 35min
completed: 2026-06-11
---

# Phase 02 Plan 04: Robust Menu Logic Summary

**Robust ETA filtering, objective risk penalties, and solver diagnostics are now locked behind deterministic script tests**

## Performance

- **Duration:** 35 min
- **Started:** 2026-06-11T05:35:00Z
- **Completed:** 2026-06-11T06:10:00Z
- **Tasks:** 4
- **Files modified:** 3

## Accomplishments

- Added parser controls for ETA sigma, sigma source, chance threshold, soft-penalty weight, and pricing mode aliases.
- Replaced ad hoc display-window pruning with `_eta_filter_result()` supporting `hard`, `calibrated`, `interval_overlap`, `chance_constraint`, `soft_penalty`, and `none`.
- Recorded candidate-level diagnostics for predicted/filter ETA, uncertainty interval, preferred/display windows, pass/fail, prune reason, violation probability, source/variant, oracle ETA, risk score, and objective retention.
- Applied `eta_soft_penalty` in `evaluate_menu()` so soft ETA risk changes objective values without pruning candidates.
- Preserved risk-adjusted and service-guarded policies as candidate methods, including service-guard fallback metadata.
- Added unified solver diagnostics for requested/effective solver, candidate count, enumerated count, exact threshold fallback, and exact-vs-greedy gap metadata where computed.
- Added deterministic regression coverage in `test_robust_menu_logic.py`.

## Task Commits

1. **Tasks 1-4: Robust ETA/objective/solver logic** - `5c868dc` (feat)

**Plan metadata:** pending in docs commit

## Files Created/Modified

- `work2_coding/Src/Algorithms/DSPO_Menu.py` - Added robust ETA helper, candidate diagnostics, ETA risk objective penalty, and solver telemetry.
- `work2_coding/Src/parser.py` - Added robust ETA parameters and pricing alias choices.
- `work2_coding/scripts/test_robust_menu_logic.py` - Added script-style tests for ETA modes, soft penalty, service guard fallback, and exact/greedy diagnostics.

## Decisions Made

- `interval` remains accepted as a backward-compatible alias but diagnostics emit `interval_overlap`.
- `soft_penalty` uses nearest display-window assignment and stores `eta_soft_penalty`, `eta_risk_score`, and weighted objective penalty metadata.
- Solver fallback reasons use `above_exact_threshold` for threshold-based greedy fallback.

## Deviations from Plan

- A separate time-budget fallback control was not introduced because the current code has threshold-based exact/greedy switching but no existing time-budget path. The implemented diagnostics cover exact-small, greedy-large, relative gap, overlap, build time, candidate count, enumeration count, and threshold fallback.

## Issues Encountered

- Initial testing exposed that hard/chance failed ETA filters could still return an adjacent display window. The helper now clears the display window whenever non-soft ETA filtering fails.

## User Setup Required

None.

## Verification

- `cd work2_coding; python scripts/test_robust_menu_logic.py` -> `PASS: 6 robust menu logic tests`
- `cd work2_coding; python scripts/test_menu_runtime_contract.py` -> `PASS: 5 menu runtime contract tests`
- `cd work2_coding; python scripts/test_optout_accounting.py` -> `PASS: 5 opt-out accounting tests`
- `cd work2_coding; python scripts/test_checkpoint_provenance.py` -> `PASS: 6 checkpoint provenance tests`
- `cd work2_coding; python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` -> `IMPORT_OK`
- `cd work2_coding; python -m py_compile Src/Algorithms/DSPO_Menu.py Src/parser.py scripts/test_robust_menu_logic.py` -> passed
- `rg -n "interval_overlap|chance_constraint|soft_penalty|violation_probability|relative_optimality_gap|menu_overlap_rate|menu_selection_solver_effective|solver_fallback_reason" work2_coding/Src work2_coding/scripts/test_robust_menu_logic.py` -> implementation and test coverage found.

## Next Phase Readiness

Ready for Phase 3 paired replay and manifest work. Phase 2 now exposes the metadata needed to keep opt-out accounting, ETA filtering, checkpoint provenance, and solver approximation evidence explicit in downstream experiment rows.

---
*Phase: 02-core-semantics-and-robust-menu-logic*
*Completed: 2026-06-11*
