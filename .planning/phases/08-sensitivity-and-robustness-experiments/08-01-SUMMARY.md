---
phase: 08-sensitivity-and-robustness-experiments
plan: 01
subsystem: experiments
tags: [phase8, sensitivity, manifests, diagnostics, paired-replay]
requires:
  - phase: 07-case-study-implementation
    provides: scaffold-only case-study gate context and blocked-execution boundary
provides:
  - Phase 8 must-have sensitivity study manifests
  - Phase 8 must-have sensitivity suite manifest
  - Contract tests for diagnostic scope, axis values, and paired replay fairness
affects: [phase8-sensitivity, phase9-computational-tractability, artifact-generation]
tech-stack:
  added: []
  patterns: [manifest-driven diagnostic sensitivity, one-factor-at-a-time paired groups]
key-files:
  created:
    - work2_coding/Experiments/studies/phase8_sensitivity_menu_k.yaml
    - work2_coding/Experiments/studies/phase8_sensitivity_eta_filter.yaml
    - work2_coding/Experiments/studies/phase8_sensitivity_uptake_regime.yaml
    - work2_coding/Experiments/studies/phase8_sensitivity_guardrail.yaml
    - work2_coding/Experiments/suites/phase8_sensitivity_must_have.yaml
    - work2_coding/scripts/test_phase8_sensitivity_contracts.py
  modified:
    - work2_coding/scripts/test_experiment_contracts.py
    - work2_coding/scripts/test_policy_fairness_contract.py
key-decisions:
  - "Phase 8 executable sensitivity is limited to menu_k, ETA/filter mode, uptake regime, and guardrail axes."
  - "Sensitivity manifests remain pilot/diagnostic with claim_ready=false and diagnostic_provisional_blocked output intent."
  - "Axis metadata lives in manifest and split metadata so generated artifacts can map normalized rows without hand-edited row fields."
patterns-established:
  - "One-factor-at-a-time sensitivity splits use paired_group_id to preserve same seed/data/checkpoint/HGS settings across axis values."
  - "Nice-to-have axes are recorded as deferred dimensions rather than executable Phase 8 replay manifests."
requirements-completed: [SENS-01, SENS-03]
duration: 24 min
completed: 2026-06-15
---

# Phase 8 Plan 1: Must-Have Sensitivity Manifest Contracts Summary

**Diagnostic Phase 8 sensitivity manifests for the four must-have axes with paired replay contract tests**

## Performance

- **Duration:** 24 min
- **Started:** 2026-06-15T23:20:00+08:00
- **Completed:** 2026-06-15T23:44:43+08:00
- **Tasks:** 5 completed
- **Files modified:** 8

## Accomplishments

- Added four executable Phase 8 diagnostic sensitivity manifests for `menu_k`, ETA/filter mode, uptake regime, and guardrail axes only.
- Added `phase8_sensitivity_must_have` suite with exactly the four must-have studies and no baseline gate member.
- Added script-style tests that enforce pilot/diagnostic status, `claim_ready=false`, locked axis values, no `none` filter promotion, nice-to-have deferral, and paired replay invariants.

## Task Commits

1. **Tasks 1-4: Sensitivity manifests** - `7b5ed84` (config)
2. **Task 5: Suite and contract tests** - `54b574f` (test)

## Files Created/Modified

- `work2_coding/Experiments/studies/phase8_sensitivity_menu_k.yaml` - Diagnostic `menu_k` sensitivity with values 2, 3, and 4.
- `work2_coding/Experiments/studies/phase8_sensitivity_eta_filter.yaml` - Diagnostic ETA/filter sensitivity with `hard`, `interval_overlap`, and `chance_constraint` at threshold 0.25.
- `work2_coding/Experiments/studies/phase8_sensitivity_uptake_regime.yaml` - Diagnostic low/medium uptake-regime sensitivity.
- `work2_coding/Experiments/studies/phase8_sensitivity_guardrail.yaml` - Diagnostic guardrail sensitivity varying service and opt-out guardrails together at 0.35 and 0.40.
- `work2_coding/Experiments/suites/phase8_sensitivity_must_have.yaml` - Suite limited to the four must-have studies.
- `work2_coding/scripts/test_phase8_sensitivity_contracts.py` - Dedicated Phase 8 sensitivity contract tests.
- `work2_coding/scripts/test_experiment_contracts.py` - Existing manifest contract coverage extended to Phase 8 sensitivity.
- `work2_coding/scripts/test_policy_fairness_contract.py` - Existing fairness contract coverage extended to Phase 8 sensitivity.

## Decisions Made

- Kept `phase8_baseline_validation` separate from the sensitivity suite and referenced it only as `baseline_validation_required`.
- Used manifest/split metadata (`sensitivity_axis`, `sensitivity_value`, `center_value`, `paired_group_id`) as the source of truth for later artifact mapping.
- Paired uptake-regime splits across the same seed/data-seed surface to preserve one-factor comparability while using only the locked low and medium utility settings.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## Verification

- `python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` - passed.
- `python scripts/test_phase8_sensitivity_contracts.py` - passed.
- `python scripts/test_experiment_contracts.py` - passed.
- `python scripts/test_policy_fairness_contract.py` - passed.
- `python scripts/test_phase8_baseline_validation.py` - passed.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Wave 2 can build generated sensitivity artifact and summary tooling against the new manifest suite. Phase 8 remains diagnostic/provisional and not claim-ready.

---
*Phase: 08-sensitivity-and-robustness-experiments*
*Completed: 2026-06-15*
