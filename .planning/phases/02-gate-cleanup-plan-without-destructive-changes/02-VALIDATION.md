---
phase: 02
slug: gate-cleanup-plan-without-destructive-changes
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-06-16
---

# Phase 02 - Validation Strategy

Per-phase validation contract for the non-destructive gate cleanup planning
phase.

## Test Infrastructure

| Property | Value |
| --- | --- |
| Framework | Script-style command checks and source assertions |
| Config file | none |
| Quick run command | `cd work2_coding; python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` |
| Full suite command | Quick command plus source assertions in the three M2 milestone documents |
| Estimated runtime | Less than 30 seconds |

## Sampling Rate

- After every task commit: run source assertions for the document touched by
  the task.
- After the plan wave: run the full validation checklist below.
- Before `$gsd-verify-work`: all document assertions and the import smoke must
  pass.
- Max feedback latency: 30 seconds.

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 02-01-01 | 01 | 1 | GATE-01 | T-02-01 | Dirty worktree is inspected and categorized without restore/stash/revert/delete | source assertion | `git status --short --branch` | N/A | pending |
| 02-01-02 | 01 | 1 | GATE-02 | T-02-02 | Checkpoint provenance contract is documented without smoke-loading checkpoints | source assertion | `Test-Path .planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md` | yes | pending |
| 02-01-03 | 01 | 1 | GATE-01, GATE-02 | T-02-03 | Cleanup matrix maps blockers to later actions and approval gates | source assertion | `Test-Path .planning/milestones/tr_e_completion/M2_GATE_CLEANUP_PLAN.md` | yes | pending |
| 02-01-04 | 01 | 1 | GATE-01 | T-02-04 | Destructive and evidence-generating actions are routed to user approval | source assertion | `Test-Path .planning/milestones/tr_e_completion/M2_USER_ACTIONS_REQUIRED.md` | yes | pending |
| 02-01-05 | 01 | 1 | GATE-01, GATE-02 | T-02-05 | Generated evidence remains untouched | source assertion | `git diff --name-only -- work2_coding/outputs work2_coding/artifacts artifacts` | N/A | pending |
| 02-01-06 | 01 | 1 | GATE-02 | T-02-02 | Runtime root remains importable | smoke | `cd work2_coding; python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` | N/A | pending |

## Wave 0 Requirements

Existing infrastructure covers all phase requirements. Phase 2 does not need
new test files or dependencies.

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
| --- | --- | --- | --- |
| Cleanup recommendation sufficiency | GATE-01, GATE-02 | The action matrix is a scientific and provenance judgment rather than runtime behavior | Confirm every recommended action maps to a readiness or claim-guard blocker and that no forbidden command is represented as executed in Phase 2 |

## Validation Sign-Off

- [x] All tasks have automated or source-assertion verification.
- [x] Sampling continuity: no 3 consecutive tasks without verification.
- [x] Wave 0 covers all missing infrastructure references.
- [x] No watch-mode flags.
- [x] Feedback latency under 30 seconds.
- [x] `nyquist_compliant: true` set in frontmatter.

**Approval:** pending
