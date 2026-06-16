---
phase: 13
slug: evidence-boundary-reconstruction
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-06-16T15:58:08+08:00
---

# Phase 13 Validation Strategy

## Test Infrastructure

| Property | Value |
|----------|-------|
| Framework | PowerShell source assertions plus Python import smoke |
| Config file | none |
| Quick run command | `Test-Path ..\.planning\milestones\claim_ready_resolution\01_EVIDENCE_BOUNDARY.md` from `work2_coding/` after execution |
| Full suite command | `python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` from `work2_coding/`, plus the source assertions listed below |
| Estimated runtime | under 30 seconds |

## Sampling Rate

- After every task commit: run the task-specific source assertions listed in
  the plan.
- After the plan wave: run the full assertion set.
- Before `$gsd-verify-work`: full assertion set must pass or failures must be
  recorded as explicit blockers.
- Max feedback latency: under 30 seconds.

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 13-01-01 | 01 | 1 | EVID-01 | T-13-01 | Evidence boundary is reconstructed from named source files before repair/rerun/writing. | docs/source | `Select-String -Path ..\.planning\milestones\claim_ready_resolution\01_EVIDENCE_BOUNDARY.md -Pattern "EB-001","CLAIM_GUARD.json","PACKAGE_STATUS.json","claim_ready"` | W0 | pending |
| 13-01-02 | 01 | 1 | EVID-02 | T-13-02 | `claim_ready=false` causes are traced to claims and source artifact/blocker reasons. | docs/source | `Select-String -Path ..\.planning\milestones\claim_ready_resolution\01_CLAIM_READY_FALSE_CAUSES.md -Pattern "CF-001","C1_central_adaptive_menu_superiority","C8_semi_real_case_validation","recommended_next_action"` | W0 | pending |
| 13-01-03 | 01 | 1 | EVID-03 | T-13-03 | Blockers use the roadmap's nine categories exactly. | docs/source | `Select-String -Path ..\.planning\milestones\claim_ready_resolution\01_BLOCKER_TAXONOMY.md -Pattern "provenance/readiness","artifact-generation","empirical-performance","adaptive-window","random-baseline","sensitivity","tractability","semi-real-case","manuscript-language"` | W0 | pending |
| 13-01-04 | 01 | 1 | EVID-04 | T-13-04 | Deliverables are planning docs only and generated artifacts remain untouched. | git/source | `git status --short -- .planning/milestones/claim_ready_resolution .planning/phases/13-evidence-boundary-reconstruction work2_coding/artifacts artifacts work2_coding/outputs` | yes | pending |

## Wave 0 Requirements

Existing infrastructure covers all phase requirements:

- `work2_coding/scripts/test_phase10_paper_artifacts.py`
- `work2_coding/scripts/test_manuscript_claim_guard.py`
- generated Phase 10 package JSON files
- project-level import smoke

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Recommendation boundary stays non-authorizing | EVID-01..EVID-04 | Requires research judgment and wording review. | Confirm Phase 13 uses `recommended_next_action` and downstream owner fields, but does not choose Path A/B/C or authorize repair/rerun. |
| Conflict matrix treatment is fair | EVID-01 | Requires comparison of source semantics. | Confirm disagreements are recorded rather than silently resolved; if no runtime/mirror conflict exists, confirm the hash-match finding is stated. |

## Validation Sign-Off

- [x] All tasks have automated source assertions or existing Wave 0 coverage.
- [x] Sampling continuity: no 3 consecutive tasks without automated verify.
- [x] Wave 0 covers all missing references.
- [x] No watch-mode flags.
- [x] Feedback latency target is documented.
- [x] `nyquist_compliant: true` set in frontmatter.

Approval: pending execution
