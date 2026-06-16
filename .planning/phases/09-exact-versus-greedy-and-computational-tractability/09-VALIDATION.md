---
phase: 09
slug: exact-versus-greedy-and-computational-tractability
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-06-16T10:09:40+08:00
---

# Phase 09 Validation Strategy

## Test Infrastructure

| Property | Value |
|----------|-------|
| Framework | executable Python scripts with direct `assert` |
| Config file | none |
| Quick run command | `python scripts/test_phase9_exact_greedy_contracts.py` |
| Full suite command | `python scripts/test_phase9_exact_greedy_contracts.py; python scripts/test_phase9_tractability_summary.py; python scripts/test_robust_menu_logic.py; python scripts/test_paired_replay_contract.py; python scripts/test_policy_fairness_contract.py; python scripts/test_artifact_builder.py` |
| Estimated runtime | 60-180 seconds for tests, excluding actual replay |

## Sampling Rate

- After every task commit: run the quick Phase 9 contract test when the touched
  files affect manifests, solver diagnostics, rows, or reports.
- After every plan wave: run the full suite listed above.
- Before `$gsd-verify-work`: full suite must be green or failures must be
  recorded as explicit blockers.
- Max feedback latency: under 3 minutes for tests excluding actual replay.

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 09-01-01 | 01 | 1 | COMP-01 | T-09-01 | Manifest encodes 5 paired groups x 3 solver-scale variants. | contract | `python scripts/test_phase9_exact_greedy_contracts.py` | yes | pending |
| 09-01-02 | 01 | 1 | COMP-01 | T-09-02 | Large candidate variants request exact above threshold and expect greedy fallback metadata. | unit/contract | `python scripts/test_phase9_exact_greedy_contracts.py; python scripts/test_robust_menu_logic.py` | yes | pending |
| 09-02-01 | 02 | 2 | COMP-01 | T-09-03 | Artifact builder reports candidate count, enumerated count, build time, gap, overlap, fallback/status, and source metadata. | artifact | `python scripts/test_phase9_tractability_summary.py` | yes | pending |
| 09-02-02 | 02 | 2 | COMP-02 | T-09-04 | Summary preserves `claim_ready=false` and narrows claims when gaps are large. | artifact/docs | `python scripts/test_phase9_tractability_summary.py` | yes | pending |
| 09-03-01 | 03 | 3 | COMP-01 | T-09-05 | Actual replay writes 15 completed or explicitly blocked rows. | run | `python scripts/run_study.py --study phase9_exact_greedy_tractability --execute --output-root outputs/studies` | yes | pending |
| 09-03-02 | 03 | 3 | COMP-02 | T-09-06 | Closeout cites generated artifacts and keeps claim-ready blockers visible. | docs | `Select-String -Path ..\.planning\results\COMPUTATIONAL_TRACTABILITY_SUMMARY.md -Pattern "claim_ready: false","above_exact_threshold"` | yes | pending |

## Wave 0 Requirements

Existing infrastructure covers all phase requirements:

- `work2_coding/scripts/test_robust_menu_logic.py`
- `work2_coding/scripts/test_paired_replay_contract.py`
- `work2_coding/scripts/test_policy_fairness_contract.py`
- `work2_coding/scripts/test_artifact_builder.py`
- `work2_coding/Src/experiment_contracts.py`

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Manuscript-safe interpretation of large greedy gaps | COMP-02 | Requires research judgment after generated gap/overlap values are known. | Read `.planning/results/COMPUTATIONAL_TRACTABILITY_SUMMARY.md` and confirm any positive tractability language is narrowed if relative gaps or overlap are poor. |

## Validation Sign-Off

- [x] All tasks have automated verify commands or existing Wave 0 coverage.
- [x] Sampling continuity: no 3 consecutive tasks without automated verify.
- [x] Wave 0 covers all MISSING references.
- [x] No watch-mode flags.
- [x] Feedback latency target is documented.
- [x] `nyquist_compliant: true` set in frontmatter.

Approval: pending execution
