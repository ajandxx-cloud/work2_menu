---
phase: 07-audit-closure-and-traceability-repair
milestone: v2.1
status: planned
created: 2026-06-11
type: audit-closure
active_runtime_root: work2_coding
requirements:
  - TRACE-01
  - TRACE-02
  - TRACE-03
  - TRACE-04
  - TRACE-05
blocks_next_phase_until_verified: true
---

# Phase 07 Plan: Audit Closure And Traceability Repair

## Objective

Close the procedural GSD audit gaps before running more experiments. Phase 07 verifies already implemented Phase 2 semantics, creates missing verification/validation artifacts, reconciles traceability, and keeps any unsupported item explicitly marked as a remaining gap.

Phase 07 must not change algorithm behavior. Code edits are limited to script-style tests or documentation needed to verify existing behavior.

## Starting Evidence

- `.planning/v2.0-MILESTONE-AUDIT.md` reports `gaps_found`.
- Missing blocker: `.planning/phases/02-core-semantics-and-robust-menu-logic/02-VERIFICATION.md`.
- Missing Nyquist blocker: no `*-VALIDATION.md` files for phases 01..06 while `workflow.nyquist_validation=true`.
- ACCT-01..04, ETA-01..04, MENU-01..04 are mapped to Phase 2 but remain pending/orphaned in `REQUIREMENTS.md` audit logic.
- `MENU-02` needs special reconciliation because it was claimed in `02-04-PLAN.md` but absent from `02-04-SUMMARY.md` requirements-completed.

## Tasks

### Task 1: Reconstruct Phase 2 Evidence

Read Phase 2 plans and summaries, plus the current implementation/tests, then build a requirement-by-requirement evidence matrix for:

- ACCT-01..04
- ETA-01..04
- MENU-01..04

Evidence must distinguish implemented, verified, partially supported, and still-gap. Do not mark `MENU-02` complete without explicit pricing/system-aware cost evidence.

### Task 2: Create Phase 2 Verification Artifact

Create `.planning/phases/02-core-semantics-and-robust-menu-logic/02-VERIFICATION.md` with:

- phase result status,
- exact verification commands,
- observed outputs,
- per-requirement traceability rows,
- explicit `MENU-02` reconciliation,
- boundaries around no-filter, soft-penalty, checkpoint provenance, and solver diagnostics.

### Task 3: Create Phase 2 Validation Artifact

Create `.planning/phases/02-core-semantics-and-robust-menu-logic/02-VALIDATION.md` because Nyquist validation is enabled. It should audit:

- whether Phase 2 delivered its original intent,
- whether ACCT/ETA/MENU verification evidence is sufficient,
- whether downstream Phase 3-6 reliance on Phase 2 semantics is safe,
- any residual gaps that must remain blockers.

### Task 4: Reconcile Requirements Traceability

Update `.planning/REQUIREMENTS.md` only where evidence exists:

- ACCT-01..04 may become complete only if verification rows and tests prove the semantics.
- ETA-01..04 may become complete only if robust ETA modes and diagnostics are verified.
- MENU-01, MENU-03, MENU-04 may become complete only if objective and solver evidence is verified.
- MENU-02 must either become complete with explicit evidence or remain pending with an explicit Phase 07 gap note.

### Task 5: Run Required Verification Commands

From `work2_coding/`, run and record exact outputs:

```powershell
python scripts/test_menu_runtime_contract.py
python scripts/test_optout_accounting.py
python scripts/test_checkpoint_provenance.py
python scripts/test_robust_menu_logic.py
python scripts/test_experiment_contracts.py
python scripts/test_policy_fairness_contract.py
```

Also run the import baseline:

```powershell
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
```

### Task 6: Write Phase 07 Summary, Verification, And Validation

After implementation, create:

- `.planning/phases/07-audit-closure-and-traceability-repair/07-SUMMARY.md`
- `.planning/phases/07-audit-closure-and-traceability-repair/07-VERIFICATION.md`
- `.planning/phases/07-audit-closure-and-traceability-repair/07-VALIDATION.md`

The Phase 07 verification must state whether Phase 08 may proceed.

## Success Criteria

1. `02-VERIFICATION.md` exists and covers ACCT/ETA/MENU rows.
2. `02-VALIDATION.md` exists.
3. ACCT/ETA/MENU requirements are no longer orphaned in audit logic.
4. `MENU-02` has explicit evidence or an explicit remaining gap.
5. `REQUIREMENTS.md` no longer contradicts Phase 2 summaries/verifications.
6. Required script-style tests pass and outputs are recorded.
7. Phase 07 summary, verification, validation, and STATE update are complete.

## Stop Conditions

Stop before Phase 08 if any required command fails, if `MENU-02` cannot be reconciled honestly, or if Phase 2 verification reveals a real semantic gap rather than a documentation-only gap.
