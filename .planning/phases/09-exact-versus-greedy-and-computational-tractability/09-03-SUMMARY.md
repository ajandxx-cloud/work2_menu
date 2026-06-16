---
phase: 09-exact-versus-greedy-and-computational-tractability
plan: 03
subsystem: research-runtime-artifacts
tags: [replay, tractability, exact-greedy, generated-artifacts, closeout]
requires:
  - phase: 09-exact-versus-greedy-and-computational-tractability
    provides: Plans 09-01 and 09-02 exact-greedy contract plus artifact builder
provides:
  - Completed 15-row Phase 9 diagnostic replay output
  - Generated tractability aggregates, table, figure/status artifacts, and metadata sidecars
  - Planning-side computational tractability summary with blocked claim boundary
affects: [phase-09, phase-10-artifacts, computational-tractability]
key-files:
  created:
    - work2_coding/outputs/studies/phase9_exact_greedy_tractability/phase9_exact_greedy_tractability-20260616T032010Z-5bc184cd/
    - work2_coding/artifacts/work2_robust_menu/phase9_tractability/aggregates/
    - work2_coding/artifacts/work2_robust_menu/phase9_tractability/tables/
    - work2_coding/artifacts/work2_robust_menu/phase9_tractability/figures/
  modified:
    - work2_coding/Src/computational_tractability.py
    - work2_coding/scripts/test_phase9_tractability_summary.py
    - .planning/results/COMPUTATIONAL_TRACTABILITY_SUMMARY.md
key-decisions:
  - "Preserved completed but contract-invalid rows as blocked diagnostic artifacts instead of discarding aggregate evidence."
  - "Kept `phase9_dspo_family_validation` as prerequisite status context only; no full DSPO-family replay was run."
  - "Narrowed Phase 9 tractability interpretation because configured large scales did not trigger greedy fallback."
requirements-completed:
  - COMP-01
  - COMP-02
duration: 25 min
completed: 2026-06-16
---

# Phase 09 Plan 03: Gated Replay And Tractability Closeout

**Completed the Phase 9 exact-greedy diagnostic replay and generated blocked tractability artifacts**

## Performance

- **Duration:** 25 min
- **Started:** 2026-06-16T11:17:30+08:00
- **Completed:** 2026-06-16T11:26:42+08:00
- **Tasks:** 5
- **Files modified:** runtime/artifact outputs plus planning closeout docs

## Accomplishments

- Confirmed the existing DSPO-family validation report is readable and still `passed` with `claim-ready: false`; no full DSPO-family validation replay was launched.
- Ran `phase9_exact_greedy_tractability` and produced 15 completed rows under `outputs/studies/phase9_exact_greedy_tractability/phase9_exact_greedy_tractability-20260616T032010Z-5bc184cd/`.
- Generated Phase 9 tractability aggregate JSON/CSV, LaTeX table, menu-build-time figure, gap/overlap figure-status artifact, status JSON, and metadata sidecars.
- Updated the artifact builder so completed but contract-invalid rows still produce aggregate/table/figure artifacts while the builder status remains `blocked`.
- Regenerated `.planning/results/COMPUTATIONAL_TRACTABILITY_SUMMARY.md` with `claim_ready: false`, 15-row coverage, source artifact paths, and validation blockers.

## Task Commits

1. **Tasks 1-4: Replay, blocked aggregate preservation, generated artifacts, and verification** - `b9f83dd` (`feat(09-03): run tractability replay and blocked artifacts`)

**Plan metadata:** this summary commit.

## Scientific Outcome

Phase 9 completed diagnostically, but it did not establish the intended exact-vs-greedy comparison. The configured large scales 12 and 16 did not trigger `above_exact_threshold` fallback because realized solver candidate counts stayed below the exact threshold. All 15 rows completed with checkpoint status `loaded`, but the effective solver remained `exact` for every scale.

The correct claim boundary is therefore blocked diagnostic: candidate count, enumerated menu count, and build time are reported, while optimality gap and menu overlap remain unavailable. No claim-ready online tractability or near-optimal greedy statement is authorized.

## Verification

Run from `work2_coding/`:

- `python scripts/test_phase9_dspo_family_validation.py` - passed, 9 tests
- `python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` - passed
- `python scripts/test_phase9_exact_greedy_contracts.py` - passed, 6 tests
- `python scripts/test_phase9_tractability_summary.py` - passed, 8 tests
- `python scripts/test_robust_menu_logic.py` - passed, 7 tests
- `python scripts/test_paired_replay_contract.py` - passed, 12 tests
- `python scripts/test_policy_fairness_contract.py` - passed, 16 tests
- `python scripts/test_artifact_builder.py` - passed, 5 tests
- `python scripts/test_artifact_gates.py` - passed, 22 tests

Run from repository root:

- `Select-String -Path .planning/results/COMPUTATIONAL_TRACTABILITY_SUMMARY.md -Pattern "claim_ready: false","above_exact_threshold"` - passed
- `Select-String -Path .planning/results/COMPUTATIONAL_TRACTABILITY_SUMMARY.md -Pattern "Source Artifacts","Claim Boundary","claim_ready: false"` - passed

## Deviations from Plan

- The replay generated completed rows rather than execution blockers, but the scientific contract still blocked because large configured scales did not trigger greedy fallback. The builder was adjusted to preserve the generated aggregates while retaining blocked status.
- Gap/overlap artifacts are represented by a status JSON rather than a plotted figure because no greedy comparison rows were available.

## Issues Encountered

- The repository remains dirty from unrelated prior work. Phase 9 commits staged only Phase 9 runtime, artifact, and planning changes.
- Generated run provenance correctly records `git_dirty=true`; Phase 9 did not clean provenance or artifact gates.

## Next Phase Readiness

Phase 10 may proceed to paper artifact generation, but it must treat Phase 9 outputs as diagnostic/provisional and preserve `claim_ready=false` until claim gates and exact-vs-greedy evidence are resolved or the manuscript claim is narrowed accordingly.

---
*Phase: 09-exact-versus-greedy-and-computational-tractability*
*Completed: 2026-06-16*
