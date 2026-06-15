---
phase: 04-rc-result-diagnosis-and-paper-claim-validation
plan: 01
subsystem: research-diagnostics
tags: [formal-rc, paired-differences, claim-gates, diagnostics]
requires:
  - phase: 03-formal-rc-evidence-pipeline-repair-and-completion
    provides: completed 35-row formal RC run and blocked readiness/artifact gate handoff
provides:
  - formal RC policy-level metric summary
  - adaptive-versus-baseline paired split differences
  - blocker-first diagnostic tables for Phase 4 claim classification
affects: [phase-04-claim-diagnosis, phase-05-calibration-routing, manuscript-claim-guard]
tech-stack:
  added: []
  patterns: [stdlib-json-csv-diagnostics, script-style-contract-tests]
key-files:
  created:
    - work2_coding/scripts/diagnose_rc_formal_claims.py
    - work2_coding/scripts/test_rc_formal_claim_diagnosis.py
    - .planning/results/RC_FORMAL_POLICY_SUMMARY.csv
    - .planning/results/RC_FORMAL_PAIRED_DIFFS.csv
    - .planning/results/RC_FORMAL_DIAGNOSTIC_TABLES.md
  modified: []
key-decisions:
  - "Treat the selected 35-row formal run as diagnostic evidence only while dirty-git readiness and artifact gates remain blocked."
  - "Report paired split differences and direction counts, not confidence intervals or significance language, because the formal diagnosis has five splits."
  - "Separate raw adaptive-minus-baseline differences from direction labels so lower-is-better metrics such as cost and opt-out are interpreted correctly."
patterns-established:
  - "Formal claim diagnosis should be generated from structured rows through a read-only helper rather than hand-built tables."
  - "Blocker/provenance status appears before any result interpretation."
requirements-completed: [CLAIM-01, CLAIM-04]
duration: 36 min
completed: 2026-06-15
---

# Phase 4 Plan 1: Formal Row And Provenance Diagnostics Summary

**Read-only formal RC diagnostics with policy means, paired split differences, uptake-regime summaries, and blocker-first gate status**

## Performance

- **Duration:** 36 min
- **Started:** 2026-06-15T13:24:00+08:00
- **Completed:** 2026-06-15T14:00:40+08:00
- **Tasks:** 4
- **Files modified:** 5

## Accomplishments

- Validated the selected formal run as 35 completed rows across seven policy tags and five paired splits.
- Added a read-only diagnostic helper and script-style test for paired differences, blocker propagation, and no-CI language.
- Generated policy summary, paired-difference CSV, and Markdown diagnostic tables under `.planning/results/`.
- Confirmed readiness remains blocked by `dirty_git`, artifact status remains blocked, and claim guard keeps empirical claims unavailable.

## Task Commits

1. **Task 2: Add read-only diagnosis helper** - `4879a6b` (`feat(04-01)`)
2. **Task 3: Generate diagnostic tables** - `cd834b6` (`docs(04-01)`)

## Files Created/Modified

- `work2_coding/scripts/diagnose_rc_formal_claims.py` - validates formal run inputs and emits policy summary, paired diffs, and Markdown diagnostics.
- `work2_coding/scripts/test_rc_formal_claim_diagnosis.py` - covers paired difference direction, uptake grouping, blocker propagation, and checkpoint validation.
- `.planning/results/RC_FORMAL_POLICY_SUMMARY.csv` - policy-level means and population standard deviations.
- `.planning/results/RC_FORMAL_PAIRED_DIFFS.csv` - split-level adaptive-minus-baseline comparisons by metric.
- `.planning/results/RC_FORMAL_DIAGNOSTIC_TABLES.md` - blocker-first human-readable diagnostic tables.

## Decisions Made

- Confidence intervals are intentionally omitted because there are only five formal paired splits.
- The diagnostic source remains `formal_robust_menu-20260614T032323Z-c672286a`; older smoke artifacts and claim guards are excluded from Phase 4 claim evidence.
- Adaptive versus optimized fixed-window equality is preserved as a major diagnostic signal.
- Random-menu mean net profit outperforming adaptive is preserved as a blocker for universal or strong dominance language.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- The first unit-test fixture had only two splits; it was corrected to the formal 5 split x 7 policy structure so the test exercises the same validation gate as the real run.

## Verification

Run from `work2_coding/`:

- `python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` - PASS
- `python scripts/test_rc_formal_claim_diagnosis.py` - PASS: 3 tests
- `python scripts/test_paired_replay_contract.py` - PASS: 12 tests
- `python scripts/test_policy_fairness_contract.py` - PASS: 15 tests
- `python scripts/test_artifact_gates.py` - PASS: 22 tests
- `python scripts/test_phase4_artifact_pipeline.py` - PASS: 2 tests

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Plan 2 can classify claims from `.planning/results/RC_FORMAL_DIAGNOSTIC_TABLES.md`, `.planning/results/RC_FORMAL_POLICY_SUMMARY.csv`, and `.planning/results/RC_FORMAL_PAIRED_DIFFS.csv`.

---
*Phase: 04-rc-result-diagnosis-and-paper-claim-validation*
*Completed: 2026-06-15*
