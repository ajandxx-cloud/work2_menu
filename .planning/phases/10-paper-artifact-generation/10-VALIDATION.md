---
phase: 10
slug: paper-artifact-generation
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-06-16T12:20:00+08:00
---

# Phase 10 - Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | script-style Python assertions |
| **Config file** | none |
| **Quick run command** | `python scripts/test_phase10_paper_artifacts.py` |
| **Full suite command** | `python scripts/test_phase10_paper_artifacts.py; python scripts/test_manuscript_claim_guard.py; python scripts/test_artifact_builder.py; python scripts/test_artifact_gates.py; python scripts/test_phase8_sensitivity_summary.py; python scripts/test_phase9_tractability_summary.py` |
| **Estimated runtime** | ~60 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python scripts/test_phase10_paper_artifacts.py`
- **After every plan wave:** Run the full suite command above.
- **Before `$gsd-verify-work`:** Full suite must be green.
- **Max feedback latency:** 120 seconds.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 10-01-01 | 01 | 1 | ART-01 | T-10-01 | Package index preserves source tiers and claim_ready=false | unit | `python scripts/test_phase10_paper_artifacts.py` | W0 | pending |
| 10-01-02 | 01 | 1 | ART-01 | T-10-02 | Case scaffold cannot become result evidence | unit | `python scripts/test_phase10_paper_artifacts.py` | W0 | pending |
| 10-01-03 | 01 | 1 | ART-01 | T-10-03 | Artifact-to-section map uses only generated/source-indexed artifacts | unit | `python scripts/test_phase10_paper_artifacts.py` | W0 | pending |
| 10-02-01 | 02 | 2 | ART-02 | T-10-04 | Strict claim guard has all required per-claim fields | unit | `python scripts/test_phase10_paper_artifacts.py` | W0 | pending |
| 10-02-02 | 02 | 2 | ART-02 | T-10-05 | Forbidden language blocks overclaims and case validation | unit | `python scripts/test_manuscript_claim_guard.py` | exists | pending |
| 10-02-03 | 02 | 2 | ART-02 | T-10-06 | Artifact-facing frame avoids manuscript body upgrades | unit | `python scripts/test_phase10_paper_artifacts.py` | W0 | pending |

*Status: pending / green / red / flaky*

---

## Wave 0 Requirements

- [x] Existing script-style tests are present under `work2_coding/scripts/`.
- [x] Existing artifact and claim guard modules are importable.
- [ ] `work2_coding/scripts/test_phase10_paper_artifacts.py` stubs for ART-01 and ART-02.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Visual figure quality | ART-01 | Phase 10 tests can validate source/status metadata but not publication aesthetics. | Inspect copied/generated figures and status JSON; confirm diagnostic figures are not presented as claim-ready main figures. |

---

## Validation Sign-Off

- [x] All tasks have automated verify or Wave 0 dependencies.
- [x] Sampling continuity: no 3 consecutive tasks without automated verify.
- [x] Wave 0 covers all missing references.
- [x] No watch-mode flags.
- [x] Feedback latency < 120s.
- [x] `nyquist_compliant: true` set in frontmatter.

**Approval:** pending
