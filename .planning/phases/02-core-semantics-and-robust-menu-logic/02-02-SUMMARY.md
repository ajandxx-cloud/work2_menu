---
phase: 02-core-semantics-and-robust-menu-logic
plan: 02
subsystem: simulator-accounting
tags: [opt-out, choice-result, simulator, accounting, script-tests]
requires:
  - phase: 02-core-semantics-and-robust-menu-logic
    provides: 02-01 menu runtime dataclasses and tests
provides:
  - ChoiceResult outcomes for accepted_home, accepted_meeting_point, and opted_out
  - menu choice adapter that returns structured results
  - simulator mutation guard for non-mutating opt-out outcomes
  - opt-out, acceptance, and route-state regression tests
affects: [phase-02, robust-menu-logic, experiment-contracts]
tech-stack:
  added: []
  patterns: [structured choice result, legacy tuple adapter, stats metadata extension]
key-files:
  created:
    - work2_coding/scripts/test_optout_accounting.py
  modified:
    - work2_coding/Environments/OOH/containers.py
    - work2_coding/Environments/OOH/customerchoice.py
    - work2_coding/Environments/OOH/Parcelpoint_py.py
key-decisions:
  - "Kept legacy tuple returns working by normalizing them inside Parcelpoint_py.step()."
  - "Exposed opt-out metrics through environment attributes and stats[8] metadata without shifting legacy stats[1..7]."
  - "Opted-out choices do not append route data, mutate fleet routes, decrement capacity, add service time, or count as home delivery."
patterns-established:
  - "Simulator mutation is guarded by ChoiceResult.route_mutates and outcome."
  - "Menu choice uses ChoiceResult while legacy offer/pricing paths can still return tuples."
requirements-completed: [ACCT-01, ACCT-02, ACCT-03]
duration: 30min
completed: 2026-06-11
---

# Phase 02 Plan 02: Opt-Out Accounting Summary

**Passenger outcomes are now structured so outside-option opt-out is accounted separately from accepted home or meeting-point service**

## Performance

- **Duration:** 30 min
- **Started:** 2026-06-11T04:39:00Z
- **Completed:** 2026-06-11T05:09:00Z
- **Tasks:** 4
- **Files modified:** 4

## Accomplishments

- Added `ChoiceResult` with explicit `accepted_home`, `accepted_meeting_point`, and `opted_out` constructors.
- Added a menu-choice MNL path returning structured outcomes while preserving legacy tuple compatibility.
- Updated `Parcelpoint_py.step()` to skip route/capacity/service mutation for opt-out and to log outcome metadata.
- Added deterministic script tests covering forced opt-out, accepted home, accepted meeting point, mixed rates, and legacy stats preservation.

## Task Commits

1. **Tasks 1-4: Opt-out accounting semantics** - `b4bafad` (feat)

**Plan metadata:** pending in docs commit

## Files Created/Modified

- `work2_coding/Environments/OOH/containers.py` - Added `ChoiceResult`.
- `work2_coding/Environments/OOH/customerchoice.py` - Added `customerchoice_menu()` returning structured outcomes.
- `work2_coding/Environments/OOH/Parcelpoint_py.py` - Added legacy adapter, mutation guard, opt-out counters, acceptance rates, and stats metadata.
- `work2_coding/scripts/test_optout_accounting.py` - Added deterministic accounting regression tests.

## Decisions Made

- `stats[1]` through `stats[7]` remain compatible with existing `run.py` and `run_ppo.py` consumers.
- New opt-out details are available through `env.count_opted_out`, `env.acceptance_rate()`, `env.choice_log`, `env.last_choice_result`, and `stats[8]`.
- `last_selected_offer` is populated only for route-mutating accepted menu choices; opt-out leaves it `None`.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Adjusted route mutation assertion for legacy fleet list sharing**
- **Found during:** Task 4 test execution
- **Issue:** Existing `reset_fleet()` assigns the same initial route list to multiple vehicles, so one insertion can increase aggregate route length by more than one.
- **Fix:** The test now asserts accepted service causes route mutation and route-data id count increases by exactly one, while opt-out route/data counts remain exactly unchanged.
- **Files modified:** `work2_coding/scripts/test_optout_accounting.py`
- **Verification:** `cd work2_coding; python scripts/test_optout_accounting.py`
- **Committed in:** `b4bafad`

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** The test now captures the accounting contract without refactoring unrelated legacy fleet internals.

## Issues Encountered

None beyond the route-length assertion refinement above.

## User Setup Required

None - no external service configuration required.

## Verification

- `cd work2_coding; python scripts/test_menu_runtime_contract.py` -> `PASS: 5 menu runtime contract tests`
- `cd work2_coding; python scripts/test_optout_accounting.py` -> `PASS: 5 opt-out accounting tests`
- `python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"` -> `IMPORT_OK`
- `python -c "import sys; sys.path.insert(0, 'work2_coding'); import Environments.OOH.Parcelpoint_py; print('PARCELPOINT_OK')"` -> `PARCELPOINT_OK`
- `rg -n "opted_out|accepted_home|accepted_meeting_point|route_mutates" work2_coding/Environments/OOH` -> structured outcome coverage found.

## Next Phase Readiness

Ready for checkpoint provenance work in Plan 03. Later robust menu tests can rely on accepted and opted-out choices having distinct simulator side effects.

---
*Phase: 02-core-semantics-and-robust-menu-logic*
*Completed: 2026-06-11*
