---
phase: 04-execute-selected-claim-path
plan: 01
subsystem: research-evidence-gates
tags: [work2, formal-readiness, claim-guard, diagnostic-lock, manuscript-handoff]
requires:
  - phase: 03-claim-ready-evidence-decision-gate
    provides: blocked_pending_gate_cleanup decision and pre-replay gate rules
provides:
  - Current non-tuning calibration protocol and frozen final settings records
  - One-pass final_robust_menu readiness gate report
  - Diagnostic Path B manuscript lock and C1-C8 claim-safe handoff
  - Verification evidence for Phase 4 PATH requirements
affects: [phase-05-manuscript-draft, claim-language, table-figure-source-map]
tech-stack:
  added: []
  patterns:
    - One-pass readiness gate before final replay
    - Diagnostic lock when claim-ready gates remain blocked
    - Strict claim guard as manuscript claim ceiling
key-files:
  created:
    - .planning/results/CALIBRATION_PROTOCOL.md
    - .planning/results/FROZEN_FINAL_SETTINGS.md
    - .planning/milestones/tr_e_completion/M4A_PRE_REPLAY_GATE_REPORT.md
    - .planning/milestones/tr_e_completion/M4A_FINAL_REPLAY_REPORT.md
    - .planning/milestones/tr_e_completion/M4B_DIAGNOSTIC_MANUSCRIPT_LOCK.md
    - .planning/milestones/tr_e_completion/M4B_SAFE_CLAIM_TABLE.md
    - .planning/milestones/tr_e_completion/M4B_REVIEWER_RISK_RESPONSE_PLAN.md
  modified: []
key-decisions:
  - "Final replay was not run because formal readiness remained blocked."
  - "Phase 5 must use a conditional diagnostic, claim-gated manuscript path."
  - "C7 may be used only for provenance/status transparency; C5 only as diagnostic boundary material."
patterns-established:
  - "Readiness JSON status controls replay authorization, not process exit alone."
  - "Ignored runtime readiness outputs are recorded through committed path/hash reports."
requirements-completed: [PATH-01, PATH-02, PATH-03, PATH-04]
duration: 5min
completed: 2026-06-17
---

# Phase 04 Plan 01: Execute Selected Claim Path Summary

**Claim-ready replay was gated, blocked by current provenance and checkpoint evidence, and routed into a diagnostic manuscript lock with C1-C8 claim traceability.**

## Performance

- **Duration:** 5 min task commit window, plus orchestration and verification
- **Started:** 2026-06-17T18:09:09+08:00
- **Completed:** 2026-06-17T18:13:51+08:00
- **Tasks:** 7 evaluated; tasks 1, 2, 3, and 7 executed; tasks 4, 5, and 6 skipped by the blocked-gate branch
- **Files modified:** 7 committed planning/evidence handoff files

## Accomplishments

- Created current-state `CALIBRATION_PROTOCOL.md` and `FROZEN_FINAL_SETTINGS.md` from the active calibration/final manifests and current filesystem evidence.
- Ran the one authorized `final_robust_menu` formal readiness pass; readiness was `blocked` with `dirty_git` and `missing_formal_checkpoint`.
- Recorded final replay as `not_run`, with no artifact build, no package regeneration, and no generated row or claim-guard hand edits.
- Locked Phase 5 to the conditional diagnostic manuscript path and produced a safe claim table covering C1 through C8.

## Task Commits

1. **Task 04-01-01: Create current non-tuning freeze and calibration protocol records** - `5079887`
2. **Task 04-01-02: Run the one-pass pre-replay gate and formal readiness check** - `ab2ab72`
3. **Task 04-01-03: Lock diagnostic Path B when pre-replay gates remain blocked** - `5a235b2`
4. **Tasks 04-01-04 through 04-01-06:** skipped because pre-replay readiness was blocked and final replay was not authorized.
5. **Task 04-01-07:** verification recorded in this summary.

## Files Created/Modified

- `.planning/results/CALIBRATION_PROTOCOL.md` - current non-tuning calibration protocol with allowed knobs and prohibited tuning actions.
- `.planning/results/FROZEN_FINAL_SETTINGS.md` - frozen final setting status with manifest hashes, policy tags, split IDs, checkpoint status, and gate commands.
- `.planning/milestones/tr_e_completion/M4A_PRE_REPLAY_GATE_REPORT.md` - one-pass readiness report with command outputs, readiness/dependency hashes, git state, checkpoint state, blocker codes, and routing decision.
- `.planning/milestones/tr_e_completion/M4A_FINAL_REPLAY_REPORT.md` - durable `not_run` replay accounting.
- `.planning/milestones/tr_e_completion/M4B_DIAGNOSTIC_MANUSCRIPT_LOCK.md` - conditional diagnostic manuscript lock.
- `.planning/milestones/tr_e_completion/M4B_SAFE_CLAIM_TABLE.md` - C1-C8 claim-safe handoff with allowed and prohibited language.
- `.planning/milestones/tr_e_completion/M4B_REVIEWER_RISK_RESPONSE_PLAN.md` - reviewer-risk responses for no-filter, case, tractability, claim guard, and evidence boundary attacks.

## Verification Results

Run from `work2_coding/`:

```powershell
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_calibration_manifests.py
python scripts/test_calibration_protocol.py
python scripts/test_frozen_final_settings.py
python scripts/test_formal_readiness.py
python scripts/test_checkpoint_provenance.py
python scripts/test_artifact_gates.py
python scripts/test_phase10_paper_artifacts.py
python scripts/test_manuscript_claim_guard.py
```

Results:

- `IMPORT_OK`
- `PASS: 5 calibration manifest tests`
- `PASS: 4 calibration protocol tests`
- `PASS: 4 frozen final settings tests`
- `PASS: 4 formal readiness tests`
- `PASS: 6 checkpoint provenance tests`
- `PASS: 22 artifact gate tests`
- `PASS: 3 Phase 10 paper artifact package tests`
- `PASS: 5 manuscript claim guard tests`

Path checks:

- `M4A_PRE_REPLAY_GATE_REPORT.md` exists.
- `M4A_FINAL_REPLAY_REPORT.md` exists and records `not_run`.
- All three M4B diagnostic lock files exist.
- `M4A_CLAIM_CLASSIFICATION.md` was not created because final artifact/package generation did not run.

## Generated-Evidence Diff Review

The readiness command generated ignored runtime files under:

- `work2_coding/outputs/formal_readiness/final_robust_menu/FORMAL_READINESS.json`
- `work2_coding/outputs/formal_readiness/final_robust_menu/FORMAL_READINESS.md`
- `work2_coding/outputs/formal_readiness/final_robust_menu/DEPENDENCY_SNAPSHOT.json`

These are ignored by `work2_coding/.gitignore`; their paths and SHA-256 hashes are recorded in `M4A_PRE_REPLAY_GATE_REPORT.md`.

No generated rows, package status files, package indexes, figures, tables, mirrors, or claim guards were hand-edited. Existing unrelated deleted legacy `.planning/results/*` files remain outside this task scope.

## Decisions Made

- Treat `FORMAL_READINESS.json` status as authoritative even though the readiness command returned zero under `--diagnostic-ok`.
- Route to Path B immediately after blocked readiness, preserving Phase 4's no-remediation-loop rule.
- Use the current strict Phase 10 claim guard as Phase 5's claim ceiling because no regenerated final package exists.

## Deviations from Plan

None - plan executed exactly as written along the blocked readiness branch. Tasks 4, 5, and 6 were skipped by the plan's own gate condition.

## Issues Encountered

- Formal readiness reported `dirty_git` and `missing_formal_checkpoint`; these were recorded as blockers and routed to diagnostic lock.
- Runtime readiness outputs are gitignored; durable evidence was committed through the gate report's paths and hashes.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Phase 5 can proceed with a clear claim ceiling:

- manuscript path: conditional diagnostic
- allowed positive empirical claims: none
- allowed status/provenance claim: C7 only
- allowed diagnostic boundary material: C5 only, with no-filter kept diagnostic
- prohibited unless future guard authorization exists: dominance, superiority, improvement, real-passenger validation, and near-optimality language

## Self-Check: PASSED

- PATH-01 protected: final replay did not run on blocked gates.
- PATH-02 covered: skipped replay is durably recorded as `not_run` with blocker accounting.
- PATH-03 covered: diagnostic manuscript lock package exists.
- PATH-04 covered: strict `CLAIM_GUARD.json` remains the claim ceiling.

---
*Phase: 04-execute-selected-claim-path*
*Completed: 2026-06-17*
