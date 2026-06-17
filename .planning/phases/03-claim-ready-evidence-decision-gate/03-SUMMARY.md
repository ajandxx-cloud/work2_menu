---
phase: 03-claim-ready-evidence-decision-gate
plan: 01
subsystem: research-decision
tags: [claim-guard, provenance, final-replay, manuscript-boundary]

requires:
  - phase: 01-repository-and-evidence-boundary-audit
    provides: current generated evidence boundary and strict claim ceiling
  - phase: 02-gate-cleanup-plan-without-destructive-changes
    provides: provenance, checkpoint, dependency, and cleanup boundary requirements
provides:
  - Phase 3 go/no-go decision for final replay authorization
  - Pre-replay gate checklist for Phase 4
  - Claim-by-claim manuscript handoff rule
affects: [phase-04-claim-path, phase-05-manuscript, claim-guard]

tech-stack:
  added: []
  patterns: [claim-by-claim guard authority, conditional go-after-gates routing]

key-files:
  created:
    - .planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md
  modified:
    - .planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md

key-decisions:
  - "Current final replay status is blocked_pending_gate_cleanup; immediate final replay is not authorized."
  - "Missing freeze/protocol evidence blocks replay authorization but does not permanently force diagnostic lock by itself."
  - "Phase 4 cleanup may repair provenance/evidence-chain records only, not result-affecting runtime settings."
  - "Strict CLAIM_GUARD.json remains claim-by-claim authority for Phase 5 manuscript use."
  - "At most one same-settings technical rerun is allowed after an authorized final replay technical failure."

patterns-established:
  - "Gate cleanup must distinguish provenance repair from final-result tuning."
  - "A passing local claim cannot upgrade unrelated blocked claims or the whole paper."

requirements-completed:
  - GATE-03
  - GATE-04

duration: 12 min
completed: 2026-06-17
---

# Phase 03 Plan 01: Claim-Ready Evidence Decision Gate Summary

**Formal M3 decision classifying final replay as blocked pending gate cleanup, with strict pre-replay gates and claim-by-claim manuscript routing**

## Performance

- **Duration:** 12 min
- **Started:** 2026-06-17T08:17:00Z
- **Completed:** 2026-06-17T08:29:18Z
- **Tasks:** 6
- **Files modified:** 1

## Accomplishments

- Created `.planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md`.
- Classified the current final replay path as `blocked_pending_gate_cleanup`, not immediately authorized.
- Recorded calibration/final manifest contract status without running calibration or replay.
- Defined required pre-replay gates, approved cleanup boundaries, and forbidden result-affecting cleanup.
- Added claim-by-claim classification for C1 through C8 and a Phase 5 manuscript handoff rule.
- Defined Phase 4 routing for gate failure, one same-settings technical rerun, second failure, and completed replay with `claim_ready=false`.

## Task Commits

1. **Task 03-01-01: Establish current freeze/protocol and manifest authorization status** - `b8b127a`
2. **Task 03-01-02: Validate candidate manifest separation without replay** - `b41df71`
3. **Task 03-01-03: Define required pre-replay gates and approved cleanup boundary** - `9235674`
4. **Task 03-01-04: Define claim-by-claim manuscript classification rule** - `83f9db8`
5. **Task 03-01-05: Define failure, rerun, and diagnostic-lock routing** - `4239f18`, `936e7b9`
6. **Task 03-01-06: Run Phase 3 verification and no-evidence-generation checks** - verification-only task, no file changes

## Files Created/Modified

- `.planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md` - Formal Phase 3 decision, pre-replay gate list, cleanup boundary, claim classification, and Phase 4 routing.

## Verification

Commands run:

```powershell
cd work2_coding
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_calibration_manifests.py
cd ..
Test-Path .planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md
Test-Path .planning/results/FROZEN_FINAL_SETTINGS.md
Test-Path .planning/results/CALIBRATION_PROTOCOL.md
git diff --name-only -- work2_coding/outputs work2_coding/artifacts artifacts
```

Results:

- Runtime import smoke printed `IMPORT_OK`.
- Manifest contract test printed `PASS: 5 calibration manifest tests`.
- `M3_CLAIM_READY_DECISION.md` exists.
- `.planning/results/FROZEN_FINAL_SETTINGS.md` remains absent.
- `.planning/results/CALIBRATION_PROTOCOL.md` remains absent.
- Generated-evidence diff check printed no paths.

## Decisions Made

- Final replay is conditionally possible only after all gates pass; it is not currently authorized.
- Missing freeze/protocol files are blockers, not a permanent no-go by themselves.
- Phase 4 may repair only provenance and evidence-chain records before replay.
- Phase 4 must lock diagnostic if pre-replay gates fail, the second technical replay attempt fails, or regenerated guard output remains `claim_ready=false`.
- Phase 5 may use only claim-specific `manuscript_allowed=true` content with explicit claim ID, status, source artifact, and allowed-use labeling.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None. The manifest contract and runtime import checks passed, and no generated evidence paths changed.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Phase 4 can now choose the evidence-authorized path: approved gate cleanup before any final replay, or diagnostic lock if pre-replay gates fail. Phase 4 must not run final replay until M3 pre-replay gates pass.

---
*Phase: 03-claim-ready-evidence-decision-gate*
*Completed: 2026-06-17*
