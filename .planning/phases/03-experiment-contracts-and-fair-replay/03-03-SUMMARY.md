---
phase: 03-experiment-contracts-and-fair-replay
plan: 03
subsystem: policy-fairness
tags: [policy-adapters, baselines, fairness, uptake-regimes, no-filter]
requires:
  - phase: 03-experiment-contracts-and-fair-replay
    provides: 03-01 manifest contracts and 03-02 paired row schema
  - phase: 02-core-semantics-and-robust-menu-logic
    provides: robust ETA modes and menu policies
provides:
  - required baseline policy adapter table
  - policy-only drift guardrails
  - low/medium uptake regime manifest contracts
  - policy fairness regression tests
affects: [phase-03, phase-04, robust-policy-comparisons]
tech-stack:
  added: []
  patterns: [adapter table, allowed policy-only fields, split-level uptake regimes]
key-files:
  created:
    - work2_coding/Src/policy_adapters.py
    - work2_coding/scripts/test_policy_fairness_contract.py
  modified:
    - work2_coding/Src/experiment_contracts.py
    - work2_coding/Experiments/studies/smoke_robust_menu.yaml
    - work2_coding/Experiments/studies/pilot_robust_menu.yaml
    - work2_coding/Experiments/studies/formal_robust_menu.yaml
key-decisions:
  - "Policy adapters always set algo_name=DSPO_Menu and menu_mode=True."
  - "No-filter changes ETA pruning only and carries diagnostic=True."
  - "Uptake regimes vary at split level, not inside policy adapters."
patterns-established:
  - "Required policy tags map one-to-one to explicit parser/runtime settings."
requirements-completed: [EXP-02, EXP-03, EXP-04]
duration: 15min
completed: 2026-06-11
---

# Phase 03 Plan 03: Policy Fairness Summary

**Required baselines now map through auditable adapters that prevent hidden paired-replay drift**

## Performance

- **Duration:** 15 min
- **Started:** 2026-06-11T06:08:00Z
- **Completed:** 2026-06-11T06:28:54Z
- **Tasks:** 4
- **Files modified:** 5

## Accomplishments

- Added `policy_adapters.py` for full display, home only, nearest heuristic, top-k cheapest, min-lateness, hard filter, no-filter diagnostic, robust risk-adjusted, robust service-guarded, and random top-k.
- Connected adapter overrides to manifest policy resolution while rejecting policy-level drift in shared fairness fields.
- Added low and medium uptake regime declarations to pilot/formal contracts, with smoke carrying a medium live regime.
- Added policy fairness tests for adapter coverage, parser compatibility, diagnostic labeling, robust policy separation, disallowed drift, and uptake metadata.

## Task Commits

1. **Tasks 1-4: Policy adapters and fairness contracts** - `1acd867` (feat)

**Plan metadata:** pending in docs commit

## Files Created/Modified

- `work2_coding/Src/policy_adapters.py` - Baseline adapter table and policy-only drift guard.
- `work2_coding/scripts/test_policy_fairness_contract.py` - Adapter and uptake-regime tests.
- `work2_coding/Experiments/studies/*.yaml` - Baseline policy tags and split-level uptake regimes.
- `work2_coding/Src/experiment_contracts.py` - Adapter-backed policy resolution and validation.

## Decisions Made

- `robust_risk_adjusted` uses `risk_adjusted_expected_profit` with `chance_constraint`.
- `robust_service_guarded` uses `service_guarded_expected_profit` with `interval_overlap`.
- Pilot/formal require both low and medium uptake regimes; Phase 3 does not tune these to chase outcomes.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Verification

- `cd work2_coding; python scripts/test_experiment_contracts.py` -> `PASS: 12 experiment contract tests`
- `cd work2_coding; python scripts/test_paired_replay_contract.py` -> `PASS: 10 paired replay contract tests`
- `cd work2_coding; python scripts/test_policy_fairness_contract.py` -> `PASS: 10 policy fairness contract tests`
- `python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"` -> `IMPORT_OK`

## Next Phase Readiness

Ready for the public smoke runner and end-to-end row emission in Plan 04.

---
*Phase: 03-experiment-contracts-and-fair-replay*
*Completed: 2026-06-11*

