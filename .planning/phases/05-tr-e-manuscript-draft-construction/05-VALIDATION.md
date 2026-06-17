---
phase: 05
slug: tr-e-manuscript-draft-construction
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-06-17
---

# Phase 05 - Validation Strategy

## Test Infrastructure

| Property | Value |
| --- | --- |
| Framework | Script-style Python tests plus PowerShell source assertions |
| Config file | none |
| Quick run command | `cd work2_coding; python scripts/test_manuscript_claim_guard.py` |
| Full suite command | `cd work2_coding; python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"; python scripts/test_manuscript_claim_guard.py` |
| Estimated runtime | under 60 seconds for script checks |

## Sampling Rate

- After every task commit: run the quick claim-guard script when the task
  changes claim/audit/manuscript wording.
- After every plan wave: run full suite plus source assertions for files
  produced in that wave.
- Before verify-work: full suite and all source assertions must pass.
- Max feedback latency: 60 seconds for automated checks.

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 05-01-01 | 01 | 1 | MS-04, MS-05 | T-05-01 | Source map and claim audit are derived from generated claim/package status, not hand-edited generated evidence | source/script | `cd work2_coding; python scripts/test_manuscript_claim_guard.py` | yes | pending |
| 05-01-02 | 01 | 1 | MS-04, MS-05 | T-05-02 | Prohibited-language checklist records forbidden phrases and scan rules before prose is finalized | source | `rg -n "domin|superior|outperform|near-optimal|real passenger|case-study validation|no-filter recommendation|DSPO_PLUS|Behavior-Aware|TR-C" manuscript/TR_E_WORK2_PROHIBITED_LANGUAGE_CHECK.md` | yes | pending |
| 05-02-01 | 02 | 2 | MS-01, MS-02, MS-03, MS-05 | T-05-03 | Draft contains all TR-E sections and uses paragraph prose with claim-safe framing | source | `rg -n "^## (Introduction|Literature Review|Problem Description|Mathematical Model|Solution Method|Experimental Design|Results|Discussion|Conclusion|Appendix)" manuscript/TR_E_WORK2_MANUSCRIPT_DRAFT.md` | yes | pending |
| 05-02-02 | 02 | 2 | MS-04, MS-05 | T-05-04 | Every manuscript table/figure reference is traceable to source path, claim ID, status, allowed use, and evidence class | source | `rg -n "source artifact path|claim ID|claim status|allowed use|evidence class" manuscript/TR_E_WORK2_TABLE_FIGURE_SOURCE_MAP.md` | yes | pending |
| 05-03-01 | 03 | 3 | MS-01..MS-05 | T-05-05 | Final audit flags or clears unsafe positive language in the body and records migration risk decisions | source/script | `cd work2_coding; python scripts/test_manuscript_claim_guard.py` | yes | pending |

## Wave 0 Requirements

Existing infrastructure covers all phase requirements. No new test framework is
needed before manuscript writing.

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
| --- | --- | --- | --- |
| Academic paragraph prose quality | MS-02 | Script checks cannot judge coherence, journal tone, or argument flow | Read `TR_E_WORK2_MANUSCRIPT_DRAFT.md` and confirm the body is not outline fragments |
| TR-E novelty and reviewer positioning | MS-01, MS-03 | Requires domain judgment | Compare Introduction, Literature Review, Discussion, and reviewer-risk response against `M4B_REVIEWER_RISK_RESPONSE_PLAN.md` |
| Claim-safe nuance | MS-05 | Some forbidden terms may appear legitimately in audit tables | Confirm any forbidden phrase in the manuscript body is negated, quoted as prohibited language, or removed |

## Validation Sign-Off

- [x] All tasks have automated verify or source assertion coverage.
- [x] Sampling continuity: no 3 consecutive tasks without automated verify.
- [x] Wave 0 covers all missing references.
- [x] No watch-mode flags.
- [x] Feedback latency target is under 60 seconds.
- [x] `nyquist_compliant: true` set in frontmatter.

**Approval:** pending execution

