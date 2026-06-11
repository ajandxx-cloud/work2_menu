---
phase: 02-core-semantics-and-robust-menu-logic
plan: 03
subsystem: checkpoint-provenance
tags: [checkpoint, provenance, fail-closed, parser, agent]
requires:
  - phase: 02-core-semantics-and-robust-menu-logic
    provides: 02-01 runtime predictor compatibility
provides:
  - run-mode and checkpoint parser controls
  - Config checkpoint metadata defaults
  - structured checkpoint hash/load status helpers
  - Agent.load_checkpoint metadata propagation
  - checkpoint provenance regression tests
affects: [phase-03, experiment-contracts, formal-provenance]
tech-stack:
  added: []
  patterns: [structured metadata dicts, SHA-256 checkpoint provenance, diagnostic-only mismatch handling]
key-files:
  created:
    - work2_coding/scripts/test_checkpoint_provenance.py
  modified:
    - work2_coding/Src/parser.py
    - work2_coding/Src/config.py
    - work2_coding/Src/Algorithms/Agent.py
    - work2_coding/Src/Utils/Predictors.py
    - work2_coding/Src/Utils/Utils.py
key-decisions:
  - "Pilot/formal required checkpoint failures raise instead of silently falling back."
  - "Intentional mismatch is blocked in pilot/formal mode and marked diagnostic-only otherwise."
  - "Checkpoint metadata is copied onto both algorithm instances and Config for later row writers."
patterns-established:
  - "Module loaders return checkpoint metadata dictionaries."
  - "Agent.load_checkpoint aggregates per-module status into a row-ready metadata surface."
requirements-completed: [ACCT-04]
duration: 25min
completed: 2026-06-11
---

# Phase 02 Plan 03: Checkpoint Provenance Summary

**Checkpoint loads now produce explicit status, hash, mismatch, and fail-closed metadata for shared predictor comparisons**

## Performance

- **Duration:** 25 min
- **Started:** 2026-06-11T05:09:00Z
- **Completed:** 2026-06-11T05:34:00Z
- **Tasks:** 4
- **Files modified:** 6

## Accomplishments

- Added parser flags for `run_mode`, `checkpoint_path`, `require_checkpoint`, `allow_checkpoint_mismatch`, and `run_id`.
- Initialized `Config.checkpoint_metadata` with explicit `not_requested` provenance.
- Added SHA-256 hashing and safe structured checkpoint load helpers.
- Updated predictor and neural net loaders to return metadata instead of silently hiding load outcomes.
- Added `Agent.load_checkpoint()` to aggregate module statuses and synchronize metadata to `config`.
- Added deterministic tests for success, missing-path diagnostics, formal required blocking, mismatch rules, and agent metadata propagation.

## Task Commits

1. **Tasks 1-4: Checkpoint provenance metadata** - `d6cf185` (feat)

**Plan metadata:** pending in docs commit

## Files Created/Modified

- `work2_coding/Src/parser.py` - Added run-mode and checkpoint controls.
- `work2_coding/Src/config.py` - Added default checkpoint metadata.
- `work2_coding/Src/Utils/Utils.py` - Added metadata, hash, and load helpers.
- `work2_coding/Src/Utils/Predictors.py` - Routed predictor loads through structured metadata helpers.
- `work2_coding/Src/Algorithms/Agent.py` - Added aggregate checkpoint load method.
- `work2_coding/scripts/test_checkpoint_provenance.py` - Added regression coverage.

## Decisions Made

- `allow_checkpoint_mismatch=True` is treated as a diagnostic-only mode and raises in pilot/formal runs.
- Missing checkpoint in smoke/diagnostic mode records explicit `failed` metadata rather than pretending to load.
- Required formal/pilot failures raise clear exceptions so later comparisons can fail closed.

## Deviations from Plan

None - plan executed as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Verification

- `cd work2_coding; python scripts/test_menu_runtime_contract.py` -> `PASS: 5 menu runtime contract tests`
- `cd work2_coding; python scripts/test_optout_accounting.py` -> `PASS: 5 opt-out accounting tests`
- `cd work2_coding; python scripts/test_checkpoint_provenance.py` -> `PASS: 6 checkpoint provenance tests`
- `python -c "import sys; sys.path.insert(0, 'work2_coding'); from Src.parser import Parser; args=Parser().get_parser().parse_args(['--run_mode','formal','--require_checkpoint','True','--checkpoint_path','dummy.pt']); print(args.run_mode, args.require_checkpoint, args.checkpoint_path)"` -> `formal True dummy.pt`
- `python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"` -> `IMPORT_OK`
- `rg -n "checkpoint_load_status|checkpoint_hash|intentional_mismatch|require_checkpoint" work2_coding/Src work2_coding/scripts` -> provenance fields found.

## Next Phase Readiness

Ready for robust ETA/objective/solver work in Plan 04. Later study rows can consume `config.checkpoint_metadata` without guessing whether checkpoint loading succeeded.

---
*Phase: 02-core-semantics-and-robust-menu-logic*
*Completed: 2026-06-11*
