---
phase: 03-experiment-contracts-and-fair-replay
plan: 04
subsystem: smoke-study-runner
tags: [study-runner, normalized-rows, smoke, csv, json, artifact-gates]
requires:
  - phase: 03-experiment-contracts-and-fair-replay
    provides: 03-01 manifests, 03-02 rows, 03-03 adapters
provides:
  - public contract-only study runner
  - normalized JSON and CSV smoke row outputs
  - study summary and manifest snapshot outputs
  - end-to-end smoke row tests
affects: [phase-04, evidence-and-artifacts, reproducibility]
tech-stack:
  added: []
  patterns: [thin CLI wrapper, temp-output tests, explicit placeholder status]
key-files:
  created:
    - work2_coding/scripts/run_study.py
    - work2_coding/scripts/test_smoke_study_rows.py
  modified:
    - work2_coding/Src/paired_replay.py
    - work2_coding/Src/experiment_contracts.py
    - work2_coding/.gitignore
key-decisions:
  - "Phase 3 runner emits contract_only rows by default and refuses formal placeholder rows."
  - "Smoke output writes manifest_snapshot.yaml, study_summary.json, normalized_rows.json, and normalized_rows.csv under outputs/studies."
  - "Actual pilot/formal evidence execution remains Phase 4 scope."
patterns-established:
  - "Public runner tests exercise the CLI path rather than private helpers only."
requirements-completed: [EXP-01, EXP-02, EXP-03, EXP-04]
duration: 20min
completed: 2026-06-11
---

# Phase 03 Plan 04: Smoke Runner Summary

**Public smoke study command now emits provenance-backed normalized rows without generating paper artifacts**

## Performance

- **Duration:** 20 min
- **Started:** 2026-06-11T06:08:00Z
- **Completed:** 2026-06-11T06:28:54Z
- **Tasks:** 4
- **Files modified:** 5

## Accomplishments

- Added `scripts/run_study.py` with `--study`, `--suite`, `--output-root`, `--contract-only`, and `--max-policies`.
- Runner writes manifest snapshots, study summaries, normalized JSON rows, and normalized CSV rows.
- Added end-to-end smoke row tests using temporary output directories.
- Verified public smoke command writes rows under ignored `work2_coding/outputs/studies/...`.

## Task Commits

1. **Tasks 1-4: Public smoke runner and end-to-end tests** - `1acd867` (feat)

**Plan metadata:** pending in docs commit

## Files Created/Modified

- `work2_coding/scripts/run_study.py` - Public study/suite CLI for contract-only row emission.
- `work2_coding/scripts/test_smoke_study_rows.py` - End-to-end public runner tests.
- `work2_coding/Src/paired_replay.py` - Row builder used by the runner.
- `work2_coding/.gitignore` - Ignores local `outputs/`.

## Decisions Made

- The runner blocks formal `--contract-only` row emission because formal placeholder rows would be misleading.
- The default Phase 3 smoke path is honest contract-only output; actual simulator execution is deferred rather than faked.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Replaced deprecated UTC timestamp call**
- **Found during:** Public smoke command verification
- **Issue:** `datetime.utcnow()` emitted a deprecation warning on the local Python runtime.
- **Fix:** Switched to timezone-aware `datetime.now(timezone.utc)`.
- **Files modified:** `work2_coding/scripts/run_study.py`
- **Verification:** `cd work2_coding; python scripts/run_study.py --study smoke_robust_menu --contract-only`
- **Committed in:** `1acd867`

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** CLI output remains clean and warning-free.

## Issues Encountered

None beyond the UTC timestamp warning above.

## User Setup Required

None - no external service configuration required.

## Verification

- `cd work2_coding; python scripts/test_experiment_contracts.py` -> `PASS: 12 experiment contract tests`
- `cd work2_coding; python scripts/test_paired_replay_contract.py` -> `PASS: 10 paired replay contract tests`
- `cd work2_coding; python scripts/test_policy_fairness_contract.py` -> `PASS: 10 policy fairness contract tests`
- `cd work2_coding; python scripts/test_smoke_study_rows.py` -> `PASS: 9 smoke study row tests`
- `cd work2_coding; python scripts/run_study.py --study smoke_robust_menu --contract-only` -> wrote `normalized_rows.json`, `normalized_rows.csv`, and `study_summary.json`
- `cd work2_coding; python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` -> `IMPORT_OK`
- `cd work2_coding; rg -n "placeholder_only|formal|no_filter_diagnostic|manifest_hash|trace_id|checkpoint_load_status|uptake_regime" Src scripts experiments` -> implementation/test coverage found.

## Next Phase Readiness

Phase 3 is ready for verification and Phase 4 evidence/artifact generation. Pilot/formal execution should use the same manifest, adapter, paired replay, and row schema surfaces.

---
*Phase: 03-experiment-contracts-and-fair-replay*
*Completed: 2026-06-11*

