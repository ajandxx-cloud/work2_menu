---
phase: 3
plan: 2
subsystem: formal-replay-validation
tags:
  - formal-replay
  - normalized-rows
  - failure-diagnosis
requires:
  - RC-04
provides:
  - selected-formal-source-run
  - formal-failure-diagnosis
affects:
  - .planning/results/FORMAL_FAILURE_DIAGNOSIS.md
tech-stack:
  added: []
  patterns:
    - row comparability audit
key-files:
  created:
    - .planning/results/FORMAL_FAILURE_DIAGNOSIS.md
  modified: []
key-decisions:
  - Use the completed 35-row formal run as diagnostic source evidence for Phase 4.
  - Do not rerun formal replay while the candidate rows pass comparability and dirty git keeps new runs diagnostic.
requirements-completed:
  - RC-04
duration: 10 min
completed: 2026-06-15T11:53:41+08:00
---

# Phase 3 Plan 2: Formal Replay Row Validation And Completion Summary

Plan 03-02 validated the latest completed formal run as comparable candidate
evidence and documented the earlier failed run without editing generated rows.

## Results

| Task | Result |
| --- | --- |
| Validate candidate completed formal run | Selected `formal_robust_menu-20260614T032323Z-c672286a`; it has 35 completed rows, five formal splits, seven policies per split, loaded checkpoint status, and no row errors. |
| Preserve and summarize prior formal failure | Documented `formal_robust_menu-20260614T031927Z-fca35a73`, which has 7 failed rows with `UnboundLocalError` metadata and blocker code `actual_replay_failed_rows`. |
| Rerun formal replay only if needed | Not needed; the selected completed run passed row comparability. |
| Run row and accounting verification | Opt-out accounting, paired replay, fairness, study status, and formal replay enablement scripts passed. |

## Selected Run

```text
work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a
```

The run is suitable for Phase 4 diagnosis, but remains diagnostic rather than
claim-ready because Plan 03-01 readiness is blocked by dirty git and artifact
claim gates have not promoted the run.

## Verification

Run from `work2_coding/`:

| Command | Result |
| --- | --- |
| `python scripts/test_optout_accounting.py` | PASS: 7 opt-out accounting tests |
| `python scripts/test_paired_replay_contract.py` | PASS: 12 paired replay contract tests |
| `python scripts/test_policy_fairness_contract.py` | PASS: 15 policy fairness contract tests |
| `python scripts/test_study_execution_status.py` | PASS: 9 study execution status tests |
| `python scripts/test_formal_replay_enablement.py` | PASS: 4 formal replay enablement tests |

## Commits

| Commit | Description |
| --- | --- |
| `f7782d5` | `docs(03-02): validate formal replay rows` |

## Deviations from Plan

None - plan executed exactly as written. The optional formal replay rerun was
skipped because the candidate completed run satisfied row comparability and
rerunning under dirty git would not produce claim-ready evidence.

**Total deviations:** 0 auto-fixed.
**Impact:** Phase 4 can diagnose the completed formal rows, with gate status
clearly separated from empirical row completion.

## Self-Check: PASSED

The selected run has 35 completed comparable rows, the prior failed rows remain
visible with structured error metadata, and no generated formal rows were
hand-edited.

## Next

Ready for Plan 03-03 artifact gates and formal evidence handoff.
