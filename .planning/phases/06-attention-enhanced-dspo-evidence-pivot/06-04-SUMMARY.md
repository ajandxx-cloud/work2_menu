---
phase: 06-attention-enhanced-dspo-evidence-pivot
plan: 04
subsystem: verification
tags: [attention, smoke, evidence-ladder, blocker, artifacts]
requires:
  - phase: 06-attention-enhanced-dspo-evidence-pivot
    provides: attention scoring, study contracts, and artifact builder
provides:
  - completed actual smoke attention run
  - pilot missing-checkpoint blocker run
  - refreshed attention artifact mirror
  - public runner smoke regression coverage
affects: [phase-verification, attention-evidence, manuscript-claims]
tech-stack:
  added: []
  patterns: [temporary-output runner tests, fail-closed pilot checkpoint blocker]
key-files:
  created:
    - work2_coding/scripts/test_attention_smoke_execution.py
    - work2_coding/outputs/studies/smoke_attention_dspo/smoke_attention_dspo-20260611T105742Z-80ab59ee/
    - work2_coding/outputs/studies/pilot_attention_dspo/pilot_attention_dspo-20260611T105742Z-07415c4f/
  modified:
    - work2_coding/artifacts/work2_attention_dspo/
    - artifacts/work2_attention_dspo/
key-decisions:
  - "Actual smoke is committed as execution/schema evidence only."
  - "Pilot evidence remains blocked until the shared attention checkpoint exists."
  - "Final attention artifacts are built from completed actual smoke rows but still block superiority claims."
patterns-established:
  - "Public runner tests accept actual smoke completion or explicit blocker rows, never silent random evidence."
requirements-completed: [ATTN-02, ATTN-03, ATTN-04]
duration: 24min
completed: 2026-06-11
---

# Phase 06 Plan 04: Smoke Evidence Summary

**Completed attention smoke replay with paired rows, blocked pilot checkpoint metadata, and refreshed fail-closed artifacts**

## Performance

- **Duration:** 24 min
- **Started:** 2026-06-11T19:35:00+08:00
- **Completed:** 2026-06-11T19:59:00+08:00
- **Tasks:** 4
- **Files modified:** 24

## Accomplishments

- Added `test_attention_smoke_execution.py` covering contract smoke rows, actual smoke attempt behavior, pilot missing-checkpoint blockers, and artifact guard blocking.
- Ran actual smoke attention replay for `DSPO_original` and `DSPO_attention` on the same trace.
- Generated and committed completed smoke normalized rows under `work2_coding/outputs/studies/smoke_attention_dspo/smoke_attention_dspo-20260611T105742Z-80ab59ee/`.
- Exercised the pilot evidence gate and committed blocker metadata for missing `outputs/shared_training/work2_attention_dspo/pilot/supervised_ml.pt`.
- Refreshed `work2_attention_dspo` artifacts and root mirror from the completed smoke run.

## Task Commits

1. **Tasks 1-3: Smoke runner coverage, actual smoke output, pilot blocker, and refreshed artifacts** - `c9d44ae` (test)

**Plan metadata:** pending in this summary commit.

## Files Created/Modified

- `work2_coding/scripts/test_attention_smoke_execution.py` - Public runner boundary tests.
- `work2_coding/outputs/studies/smoke_attention_dspo/smoke_attention_dspo-20260611T105742Z-80ab59ee/` - Completed actual smoke rows.
- `work2_coding/outputs/studies/pilot_attention_dspo/pilot_attention_dspo-20260611T105742Z-07415c4f/` - Blocked pilot rows and checkpoint blocker metadata.
- `work2_coding/artifacts/work2_attention_dspo/` - Source attention artifacts from completed smoke.
- `artifacts/work2_attention_dspo/` - Mirrored review artifacts.

## Decisions Made

- The actual smoke run is useful for executability and schema evidence, but it remains smoke-tier evidence and cannot support directional improvement claims.
- The committed artifact guard blocks `attention_improves_dspo` because evidence is smoke-only and the primary metric delta is not positive.
- Pilot/formal evidence should be rerun only after checkpoint provenance exists.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- `python scripts/build_attention_artifacts.py --study smoke_attention_dspo ...` follows latest run ordering, so an extra contract-only run could become the latest. The final committed artifacts were rebuilt with explicit `--run-dir` pointing to the completed actual smoke run.

## Verification

- `cd work2_coding; python scripts/test_attention_menu_logic.py` - PASS
- `cd work2_coding; python scripts/test_attention_manifest_contracts.py` - PASS
- `cd work2_coding; python scripts/test_attention_paired_rows.py` - PASS
- `cd work2_coding; python scripts/test_attention_artifact_gate.py` - PASS
- `cd work2_coding; python scripts/test_attention_smoke_execution.py` - PASS
- `cd work2_coding; python scripts/run_study.py --study smoke_attention_dspo --contract-only` - PASS
- `cd work2_coding; python scripts/build_attention_artifacts.py --run-dir outputs/studies/smoke_attention_dspo/smoke_attention_dspo-20260611T105742Z-80ab59ee --allow-incomplete --mirror-root ../artifacts/work2_attention_dspo` - PASS
- `cd work2_coding; python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` - PASS

## Evidence Status

- **Smoke:** completed actual replay; paired rows exist for both method variants on one trace.
- **Artifact guard:** not claim-ready; `attention_improves_dspo_allowed=false`.
- **Pilot:** blocked because `outputs/shared_training/work2_attention_dspo/pilot/supervised_ml.pt` is missing.
- **Formal:** not executed; should remain held out and run once after valid checkpoint provenance exists.

## Later Pilot/Formal Commands

- Pilot after checkpoint is available: `cd work2_coding; python scripts/run_study.py --study pilot_attention_dspo --execute`
- Formal after pilot validation and checkpoint is available: `cd work2_coding; python scripts/run_study.py --study formal_attention_dspo --execute`
- Artifact rebuild from chosen completed run: `cd work2_coding; python scripts/build_attention_artifacts.py --run-dir <completed-run-dir> --allow-incomplete --mirror-root ../artifacts/work2_attention_dspo`

## User Setup Required

None for smoke. Pilot/formal require a shared checkpoint at the manifest paths before empirical claims can be considered.

## Next Phase Readiness

All Phase 6 plans are complete and ready for phase-level verification. The paper claim must remain restrained until pilot/formal completed non-placeholder paired evidence supports a positive primary metric delta.

---
*Phase: 06-attention-enhanced-dspo-evidence-pivot*
*Completed: 2026-06-11*
