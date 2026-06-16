---
phase: 09-exact-versus-greedy-and-computational-tractability
plan: 01
subsystem: research-runtime
tags: [manifest, paired-replay, solver-diagnostics, tractability, testing]
requires:
  - phase: 08-sensitivity-and-robustness-experiments
    provides: diagnostic paired split surfaces and claim-boundary context
provides:
  - Phase 9 exact-greedy tractability manifest with 5 paired groups x 3 solver-scale variants
  - Normalized-row support for observed solver candidate counts
  - Script-style contract tests for paired fairness, exact threshold, greedy fallback, checkpoint, and claim boundary
affects: [phase-09, phase-10-artifacts, computational-tractability]
tech-stack:
  added: []
  patterns: [manifest-driven solver-scale treatment, row-level solver diagnostics, script-style contract tests]
key-files:
  created:
    - work2_coding/Experiments/studies/phase9_exact_greedy_tractability.yaml
    - work2_coding/scripts/test_phase9_exact_greedy_contracts.py
  modified:
    - work2_coding/Src/paired_replay.py
    - work2_coding/Src/study_execution.py
    - work2_coding/scripts/test_paired_replay_contract.py
    - work2_coding/scripts/test_robust_menu_logic.py
key-decisions:
  - "Encoded solver scale as split metadata and args_overrides while keeping policy_tag=mainline_optimized_adaptive."
  - "Represented large exact infeasibility through existing above_exact_threshold fallback metadata."
  - "Persisted observed solver_candidate_count separately from configured max_candidates."
patterns-established:
  - "Phase 9 paired groups compare solver scale within shared seed/data/checkpoint/utility settings."
  - "Diagnostic tractability outputs keep claim_ready=false until upstream gates are resolved."
requirements-completed:
  - COMP-01
  - COMP-02
duration: 45 min
completed: 2026-06-16
---

# Phase 09 Plan 01: Exact-Greedy Study Contract Summary

**Exact-greedy tractability contract with solver-scale manifest, candidate-count row metadata, and fallback/fairness tests**

## Performance

- **Duration:** 45 min
- **Started:** 2026-06-16T10:17:00+08:00
- **Completed:** 2026-06-16T11:02:23+08:00
- **Tasks:** 4
- **Files modified:** 6

## Accomplishments

- Added `phase9_exact_greedy_tractability.yaml` with 15 diagnostic solver-scale rows: five paired split surfaces times exact-8, fallback-12, and fallback-16.
- Propagated `solver_candidate_count` from runtime diagnostics into normalized rows while keeping it optional for blocked/failed rows.
- Added Phase 9 contract tests for manifest shape, paired fairness, threshold fallback semantics, checkpoint requirements, and `claim_ready=false`.
- Strengthened existing paired replay and robust-menu tests to assert solver candidate count survives row building and fallback diagnostics.

## Task Commits

1. **Tasks 1-4: Exact-greedy manifest, candidate-count row support, contract tests, fallback assertions** - `006fb2e` (`feat(09-01): add exact greedy tractability contract`)

**Plan metadata:** this summary commit.

## Files Created/Modified

- `work2_coding/Experiments/studies/phase9_exact_greedy_tractability.yaml` - Phase 9 manifest for exact-small versus threshold-fallback greedy diagnostic replay.
- `work2_coding/scripts/test_phase9_exact_greedy_contracts.py` - Direct script tests for the Phase 9 solver-scale contract.
- `work2_coding/Src/paired_replay.py` - Adds `solver_candidate_count` to normalized rows.
- `work2_coding/Src/study_execution.py` - Reads observed solver candidate count from `last_policy_diagnostic`.
- `work2_coding/scripts/test_paired_replay_contract.py` - Verifies candidate count survives normalized row construction.
- `work2_coding/scripts/test_robust_menu_logic.py` - Verifies exact and fallback solver diagnostics include candidate count.

## Decisions Made

- Kept `mainline_optimized_adaptive` as the only policy tag and used split-level solver-scale metadata instead of adding invalid policy adapters.
- Kept large variants as `menu_selection_solver=exact` with `max_candidates > menu_exact_threshold`, so the existing runtime fallback path records `above_exact_threshold`.
- Preserved diagnostic/provisional status and `claim_ready: false`; this plan does not clean provenance or artifact gates.

## Deviations from Plan

None - plan behavior and scientific scope were executed as written.

## Issues Encountered

- The repository already had a large dirty worktree. Runtime hunks were staged selectively so the production commit did not include unrelated pre-existing edits in the same files.
- The manifest-load snippet in the plan used bash heredoc syntax; this PowerShell shell rejected it, so the equivalent PowerShell here-string form was used.

## Verification

Run from `work2_coding/`:

- `python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')` - passed
- manifest load smoke for `phase9_exact_greedy_tractability` - passed, 15 splits
- `python scripts/test_phase9_exact_greedy_contracts.py` - passed, 6 tests
- `python scripts/test_paired_replay_contract.py` - passed, 12 tests
- `python scripts/test_policy_fairness_contract.py` - passed, 16 tests
- `python scripts/test_robust_menu_logic.py` - passed, 7 tests

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Plan 09-02 can build artifact and summary tooling on top of the new manifest and row-level `solver_candidate_count` support. Claim-ready status remains blocked/provisional as planned.

---
*Phase: 09-exact-versus-greedy-and-computational-tractability*
*Completed: 2026-06-16*
