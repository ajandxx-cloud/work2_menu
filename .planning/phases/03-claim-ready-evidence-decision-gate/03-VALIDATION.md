---
phase: 03
slug: claim-ready-evidence-decision-gate
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-06-17
---

# Phase 03 - Validation Strategy

Per-phase validation contract for the claim-ready evidence decision gate.

## Test Infrastructure

| Property | Value |
| --- | --- |
| Framework | Script-style command checks and source assertions |
| Config file | none |
| Quick run command | `cd work2_coding; python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` |
| Full suite command | Quick command plus `python scripts/test_calibration_manifests.py` and source assertions in `M3_CLAIM_READY_DECISION.md` |
| Estimated runtime | Less than 60 seconds |

## Sampling Rate

- After every task commit: run source assertions for the decision section
  touched by the task.
- After the plan wave: run the full validation checklist below.
- Before `$gsd-verify-work`: all document assertions, the import smoke, and
  the manifest contract test must pass.
- Max feedback latency: 60 seconds.

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 03-01-01 | 01 | 1 | GATE-03 | T-03-01 | Current freeze/protocol gap is classified as blocked without creating missing files | source assertion | `Test-Path .planning/results/FROZEN_FINAL_SETTINGS.md; Test-Path .planning/results/CALIBRATION_PROTOCOL.md` | no | pending |
| 03-01-02 | 01 | 1 | GATE-03 | T-03-02 | Calibration/final manifest separation and policy family are inspected without replay | script test | `cd work2_coding; python scripts/test_calibration_manifests.py` | N/A | pending |
| 03-01-03 | 01 | 1 | GATE-03, GATE-04 | T-03-03 | Pre-replay gate checklist preserves provenance, manifest, paired replay, checkpoint, dependency, and readiness boundaries | source assertion | `Select-String -Path .planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md -Pattern "Required Pre-Replay Gates"` | yes | pending |
| 03-01-04 | 01 | 1 | GATE-04 | T-03-04 | Claim classification remains claim-by-claim and guard-controlled | source assertion | `Select-String -Path .planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md -Pattern "Claim-By-Claim Classification"` | yes | pending |
| 03-01-05 | 01 | 1 | GATE-04 | T-03-05 | Failure and rerun rules prevent final-result tuning and repeated reruns | source assertion | `Select-String -Path .planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md -Pattern "Second Final Replay Failure"` | yes | pending |
| 03-01-06 | 01 | 1 | GATE-03, GATE-04 | T-03-06 | Generated evidence remains untouched | source assertion | `git diff --name-only -- work2_coding/outputs work2_coding/artifacts artifacts` | N/A | pending |
| 03-01-07 | 01 | 1 | GATE-03 | T-03-02 | Runtime root remains importable | smoke | `cd work2_coding; python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` | N/A | pending |

## Wave 0 Requirements

Existing infrastructure covers all phase requirements. Phase 3 does not need
new test files or dependencies.

Do not run `work2_coding/scripts/test_frozen_final_settings.py` or
`work2_coding/scripts/test_calibration_protocol.py` as expected-green Phase 3
tests. Their target documents are intentionally absent and must not be created
by this phase.

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
| --- | --- | --- | --- |
| Scientific legitimacy of conditional go-after-gates decision | GATE-03, GATE-04 | This is a research-integrity judgment assembled from manifests, missing freeze/protocol evidence, prior milestone docs, and strict claim guard status | Confirm `M3_CLAIM_READY_DECISION.md` says current replay is `blocked_pending_gate_cleanup`, Phase 4 may proceed only after gates pass, and blocked or failed gates route to diagnostic lock. |

## Validation Sign-Off

- [x] All tasks have automated or source-assertion verification.
- [x] Sampling continuity: no 3 consecutive tasks without verification.
- [x] Wave 0 covers all missing infrastructure references.
- [x] No watch-mode flags.
- [x] Feedback latency under 60 seconds.
- [x] `nyquist_compliant: true` set in frontmatter.

**Approval:** pending
