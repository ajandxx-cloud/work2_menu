---
phase: 09-dspo-family-full-run
plan: 01
subsystem: experiment-contracts
tags: [dspo, paired-replay, manifest, policy-adapters, contract-tests]

requires:
  - phase: 08-baseline-validation
    provides: five formal-equivalent paired splits and checkpoint contract
provides:
  - DSPO-only dspo_clip and dspo_wide policy adapters
  - Phase 9 paired replay manifest reusing Phase 8 split/runtime settings
  - Contract tests for Phase 9 manifest, paired fairness, and method-family scope
affects: [phase9-dspo-family-full-run, phase9-reporting, phase11-manuscript-status]

tech-stack:
  added: []
  patterns:
    - adapter-driven policy identity
    - script-style contract tests
    - manifest-level paired replay gates

key-files:
  created:
    - work2_coding/Experiments/studies/phase9_dspo_family_validation.yaml
  modified:
    - work2_coding/Src/policy_adapters.py
    - work2_coding/scripts/test_experiment_contracts.py
    - work2_coding/scripts/test_policy_fairness_contract.py
    - work2_coding/scripts/test_method_family_contract.py

key-decisions:
  - "Phase 9 exposes dspo_clip and dspo_wide as DSPO-only policy tags, not DSPO_PLUS variants."
  - "Phase 9 manifest reuses the five Phase 8 split identities and lightweight runtime/checkpoint contract."
  - "Phase 9 primary manifest contains no Phase 8 baseline policies and no DSPO_PLUS policies."

patterns-established:
  - "DSPO clip/wide threshold identity: service_quit_rate_guardrail and menu_optout_guardrail distinguish clip=0.35 from wide=0.45."
  - "Phase 9 contract tests compare split fields directly against phase8_baseline_validation before execution."

requirements-completed: [EXP-04, GATE-01, GATE-02]

duration: 8min
completed: 2026-06-14
---

# Phase 09 Plan 01: DSPO Family Contract Summary

**DSPO-only clip/wide paired replay contract with Phase 8 split and checkpoint parity**

## Performance

- **Duration:** 8 min
- **Started:** 2026-06-14T12:41:00Z
- **Completed:** 2026-06-14T12:48:46Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments

- Added `dspo_clip` and `dspo_wide` optional policy adapters with `method_family=DSPO`, `comparison_role=dspo_family`, `method_variant=DSPO_original`, and no DSPO_PLUS penalties or contract metadata.
- Created `phase9_dspo_family_validation.yaml` with only the two DSPO policies, five Phase 8 split identities/settings, the Phase 8 lightweight runtime budget, and required loaded-checkpoint provenance.
- Added focused contract tests proving Phase 9 has no baseline rerun, no DSPO_PLUS validation scope, and paired replay drift limited to the declared DSPO threshold fields.

## Task Commits

1. **Task 1: Add Phase 9 manifest and adapter contract tests** - `bdeeee5` (test)
2. **Task 2: Implement DSPO clip/wide adapters and manifest** - `05e5c32` (feat)

## Files Created/Modified

- `work2_coding/Experiments/studies/phase9_dspo_family_validation.yaml` - Phase 9 formal-equivalent paired replay manifest for `dspo_clip` and `dspo_wide`.
- `work2_coding/Src/policy_adapters.py` - DSPO-only adapter tags and threshold metadata.
- `work2_coding/scripts/test_experiment_contracts.py` - Manifest loading, split parity, checkpoint, and tag-scope assertions.
- `work2_coding/scripts/test_policy_fairness_contract.py` - Paired-setting checks for DSPO clip/wide threshold-only drift.
- `work2_coding/scripts/test_method_family_contract.py` - DSPO-only method-family assertions and DSPO_PLUS exclusion from Phase 9 scope.

## Verification

RED gate:

```powershell
cd work2_coding
python scripts/test_experiment_contracts.py
```

Result: failed as expected before Task 2 with missing manifest `phase9_dspo_family_validation.yaml`.

Final plan verification passed from `work2_coding/`:

```powershell
python scripts/test_experiment_contracts.py
python scripts/test_policy_fairness_contract.py
python scripts/test_method_family_contract.py
```

Results:

- `PASS: 17 experiment contract tests`
- `PASS: 15 policy fairness contract tests`
- `PASS: 3 method-family contract tests`

## Decisions Made

Followed the locked Phase 9 decisions from `09-CONTEXT.md`: clip/wide are DSPO-internal service-risk threshold variants, the primary manifest excludes Phase 8 baselines and DSPO_PLUS, and checkpoint provenance remains required/loaded.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- The checkout already contained extensive unrelated local changes before this plan started. Only Phase 9 task files were staged and committed.
- The Task 1 test commit necessarily committed the untracked `test_method_family_contract.py` file because it is a required plan file and was part of the test surface.

## Known Stubs

None. The `placeholder_only` strings found during stub scanning are normalized-row schema/test fields, not placeholder implementation or generated evidence.

## Threat Flags

None. This plan added local manifest and adapter/test contract surface only; it did not add network endpoints, auth paths, file-upload surfaces, or new external trust boundaries beyond the planned YAML manifest to runtime parser boundary.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Ready for Plan 09-02/09-03 to execute Phase 9 DSPO rows and build the validation report from generated outputs. This plan did not run actual replay and does not unlock ranking claims.

## Self-Check: PASSED

- Found summary, manifest, adapter, and all three contract test files on disk.
- Found task commits `bdeeee5` and `05e5c32` in local git history.
- Re-ran the plan verification scripts successfully after writing the summary.

---
*Phase: 09-dspo-family-full-run*
*Completed: 2026-06-14*
