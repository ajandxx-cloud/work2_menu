---
phase: 01
slug: repository-and-evidence-boundary-audit
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-06-16
---

# Phase 01 - Validation Strategy

Per-phase validation contract for the read-only repository and evidence
boundary audit.

## Test Infrastructure

| Property | Value |
| --- | --- |
| Framework | Script-style command checks and source assertions |
| Config file | none |
| Quick run command | `python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"` |
| Full suite command | Same as quick command plus source assertions in the three milestone documents |
| Estimated runtime | Less than 30 seconds |

## Sampling Rate

- After every task commit: run the import smoke if runtime paths were inspected.
- After the plan wave: run the full validation checklist below.
- Before `$gsd-verify-work`: all source assertions must pass.
- Max feedback latency: 30 seconds.

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01-01-01 | 01 | 1 | EVID-01 | T-01-01 | Read-only audit does not alter generated evidence | source assertion | `git diff --name-only -- work2_coding/outputs work2_coding/artifacts artifacts` | yes | pending |
| 01-01-02 | 01 | 1 | EVID-02 | T-01-02 | Key JSON status is recorded without copying whole generated files | source assertion | `Test-Path .planning/milestones/tr_e_completion/M1_EVIDENCE_BOUNDARY_AUDIT.md` | yes | pending |
| 01-01-03 | 01 | 1 | EVID-03 | T-01-03 | Blockers are classified into the six required classes | source assertion | `Test-Path .planning/milestones/tr_e_completion/M1_BLOCKER_LIST.md` | yes | pending |
| 01-01-04 | 01 | 1 | EVID-04 | T-01-04 | Decision preserves Phase 2/3 gate and does not authorize rerun | source assertion | `Test-Path .planning/milestones/tr_e_completion/M1_DECISION.md` | yes | pending |
| 01-01-05 | 01 | 1 | EVID-01 | T-01-01 | Runtime root remains importable | smoke | `python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"` | N/A | pending |

## Wave 0 Requirements

Existing infrastructure covers all phase requirements. Phase 1 does not need
new test files or dependencies.

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
| --- | --- | --- | --- |
| Scientific feasibility wording in `M1_DECISION.md` | EVID-04 | The final phrasing is a judgment about evidence sufficiency and claim ceiling | Confirm it says current package is not claim-ready, leans diagnostic, and leaves legitimate final replay to Phase 2/3 gates |

## Validation Sign-Off

- [x] All tasks have automated or source-assertion verification.
- [x] Sampling continuity: no 3 consecutive tasks without verification.
- [x] Wave 0 covers all missing infrastructure references.
- [x] No watch-mode flags.
- [x] Feedback latency under 30 seconds.
- [x] `nyquist_compliant: true` set in frontmatter.

**Approval:** pending
