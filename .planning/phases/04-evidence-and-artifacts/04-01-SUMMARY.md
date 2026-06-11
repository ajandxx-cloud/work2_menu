---
phase: 04-evidence-and-artifacts
plan: 01
subsystem: study-execution-status
tags: [study-runner, normalized-rows, blockers, provenance]
requires:
  - phase: 03-experiment-contracts-and-fair-replay
    provides: public contract-only study runner and normalized row schema
provides:
  - explicit study execution status vocabulary
  - blocker-aware pilot/formal prerequisite checks
  - git provenance fields on normalized rows
  - deterministic execution status regression tests
affects: [phase-04, artifacts, claim-gates, phase-05]
tech-stack:
  added: []
  patterns: [honest blocker rows, public runner tests, row provenance fields]
key-files:
  created:
    - work2_coding/Src/study_execution.py
    - work2_coding/scripts/test_study_execution_status.py
  modified:
    - work2_coding/Src/paired_replay.py
    - work2_coding/scripts/run_study.py
    - work2_coding/scripts/test_paired_replay_contract.py
key-decisions:
  - "Actual pilot/formal execution fails closed into blockers when required checkpoints are unavailable."
  - "Formal contract-only placeholder rows remain rejected instead of downgraded into formal-looking output."
patterns-established:
  - "Rows carry status/execution_status plus git provenance for downstream artifact gates."
  - "Missing pilot checkpoints produce blockers.json and blocked rows, not synthetic runtime metrics."
requirements-completed: [ART-01, ART-04]
duration: 25min
completed: 2026-06-11
---

# Phase 04 Plan 01: Study Execution Status Summary

**Study runner now emits provenance-labeled contract rows or explicit blocker metadata instead of ambiguous evidence**

## Performance

- **Duration:** 25 min
- **Started:** 2026-06-11T07:10:00Z
- **Completed:** 2026-06-11T07:18:00Z
- **Tasks:** 4
- **Files modified:** 5

## Accomplishments

- Added centralized study execution statuses: `completed`, `contract_only`, `diagnostic`, `incomplete`, and `blocked`.
- Added checkpoint prerequisite inspection for pilot/formal manifests and blocker output beside study summaries.
- Added row-level git provenance fields so dirty state is visible to downstream artifact status.
- Added deterministic tests for contract-only smoke, formal placeholder rejection, pilot missing-checkpoint blockers, and no-filter diagnostic labels.

## Task Commits

1. **Tasks 1-4: Execution status, blockers, actual-or-blocked runner path, and tests** - `abf07ed` (feat)

**Plan metadata:** included in docs completion commit.

## Files Created/Modified

- `work2_coding/Src/study_execution.py` - Checkpoint prerequisite, blocker row, and git provenance helpers.
- `work2_coding/Src/paired_replay.py` - Status vocabulary, row validation, and provenance fields.
- `work2_coding/scripts/run_study.py` - `--execute`/actual-or-blocked mode, blockers.json, and richer summaries.
- `work2_coding/scripts/test_study_execution_status.py` - Regression coverage for status and blocker behavior.
- `work2_coding/scripts/test_paired_replay_contract.py` - Fixture updated to use the new legal completed status.

## Decisions Made

- Actual simulator replay is not faked: if runtime prerequisites are missing, the public runner writes blocked/incomplete metadata.
- Formal placeholder rows remain a hard error so formal-looking placeholder evidence cannot enter the pipeline.
- Dirty git state is allowed but explicitly recorded in rows and study summaries.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- Existing paired replay test used `execution_status="synthetic"` as a fixture label. The status vocabulary now rejects that value, so the fixture was updated to `completed`.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Artifact builders can now consume rows and summaries with explicit `contract_only`, `blocked`, placeholder, checkpoint, and git provenance fields.

---
*Phase: 04-evidence-and-artifacts*
*Completed: 2026-06-11*

