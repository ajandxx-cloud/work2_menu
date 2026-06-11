---
phase: 03-experiment-contracts-and-fair-replay
plan: 02
subsystem: paired-replay
tags: [paired-replay, trace-id, normalized-rows, provenance, schema-tests]
requires:
  - phase: 03-experiment-contracts-and-fair-replay
    provides: 03-01 manifest contracts
  - phase: 02-core-semantics-and-robust-menu-logic
    provides: stats metadata and checkpoint provenance fields
provides:
  - paired setting expansion across split/policy combinations
  - deterministic trace IDs and settings hashes
  - normalized row schema and row builder
  - paired replay fairness tests
affects: [phase-03, phase-04, artifact-generation]
tech-stack:
  added: []
  patterns: [deterministic JSON hashing, split-level paired fairness validation, nullable contract diagnostics]
key-files:
  created:
    - work2_coding/Src/paired_replay.py
    - work2_coding/scripts/test_paired_replay_contract.py
  modified:
    - work2_coding/Src/experiment_contracts.py
key-decisions:
  - "Trace identity excludes policy tag so compared policies within a split share trace provenance."
  - "Contract-only rows may leave runtime metrics null, but formal rows cannot be placeholder-only."
  - "Checkpoint row metadata uses not_requested for smoke and contract_required for pilot/formal contracts."
patterns-established:
  - "Normalized rows carry manifest_hash, settings_hash, trace_id, checkpoint fields, policy/filter fields, solver diagnostics, opt-out metrics, and placeholder status."
requirements-completed: [EXP-01, EXP-03]
duration: 15min
completed: 2026-06-11
---

# Phase 03 Plan 02: Paired Replay Summary

**Paired setting expansion now produces stable trace provenance and schema-validated normalized rows**

## Performance

- **Duration:** 15 min
- **Started:** 2026-06-11T06:08:00Z
- **Completed:** 2026-06-11T06:28:54Z
- **Tasks:** 4
- **Files modified:** 3

## Accomplishments

- Added `paired_replay.py` with paired settings, trace identity, settings hash, checkpoint metadata, normalized row fields, row construction, and schema validation.
- Added tests proving trace IDs are policy-independent within a split and change with split/seed changes.
- Added row schema tests for synthetic stats/checkpoint/menu metadata, missing required fields, and formal placeholder rejection.

## Task Commits

1. **Tasks 1-4: Paired replay and normalized row contract** - `1acd867` (feat)

**Plan metadata:** pending in docs commit

## Files Created/Modified

- `work2_coding/Src/paired_replay.py` - Paired replay expansion, trace/settings hashes, and row schema helpers.
- `work2_coding/scripts/test_paired_replay_contract.py` - Paired fairness and row schema tests.
- `work2_coding/Src/experiment_contracts.py` - Exposes resolved policy args consumed by paired replay.

## Decisions Made

- `trace_id` is derived from study, split, seeds, data seeds, episode/request settings, instance, and uptake regime, not policy tag.
- Runtime-only diagnostics such as solver gap and acceptance/opt-out metrics are allowed to be `None` in contract-only rows.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Made solver telemetry nullable for contract-only rows**
- **Found during:** Task 4 paired replay tests
- **Issue:** Initial schema required `menu_selection_solver_effective` even when no actual runtime execution had occurred.
- **Fix:** Treated solver telemetry as nullable diagnostics for contract-only rows while keeping the fields present.
- **Files modified:** `work2_coding/Src/paired_replay.py`
- **Verification:** `cd work2_coding; python scripts/test_paired_replay_contract.py`
- **Committed in:** `1acd867`

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** Contract-only rows remain honest and schema-stable without inventing runtime metrics.

## Issues Encountered

None beyond the nullable telemetry adjustment above.

## User Setup Required

None - no external service configuration required.

## Verification

- `cd work2_coding; python scripts/test_experiment_contracts.py` -> `PASS: 12 experiment contract tests`
- `cd work2_coding; python scripts/test_paired_replay_contract.py` -> `PASS: 10 paired replay contract tests`
- `python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"` -> `IMPORT_OK`

## Next Phase Readiness

Ready for policy adapters and fairness guards in Plan 03.

---
*Phase: 03-experiment-contracts-and-fair-replay*
*Completed: 2026-06-11*

