---
gsd_state_version: 1.0
milestone: v1.1
milestone_name: Resolve Claim-Ready Gate or Lock Conditional Diagnostic TR-E Paper
status: executing
last_updated: "2026-06-16T08:03:00.802Z"
last_activity: 2026-06-16 -- Phase 13 planning complete
progress:
  total_phases: 6
  completed_phases: 0
  total_plans: 1
  completed_plans: 0
  percent: 0
---

# State

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-06-16)

**Core value:** Produce credible, reproducible TR Part E evidence on when and
how optimized adaptive `m+w+p` service menus improve, match, or fail to improve
the profit-service-quality trade-off under paired RC replay, without
overclaiming beyond artifact and readiness gates.

**Current focus:** Phase 13 - evidence boundary reconstruction before any
repair, rerun, or manuscript writing.

## Current Position

Phase: 13 - Evidence Boundary Reconstruction
Plan: Not started
Status: Ready to execute
Last activity: 2026-06-16 -- Phase 13 planning complete

## Initialization Evidence

Runtime root checked from repository root on 2026-06-14:

```powershell
python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"
```

Result: `IMPORT_OK`

Existing runtime files observed:

- `work2_coding/Src/Algorithms/DSPO_Menu.py`
- `work2_coding/scripts/run_study.py`
- `work2_coding/scripts/train_shared_checkpoint.py`
- `work2_coding/scripts/check_formal_readiness.py`
- `work2_coding/scripts/build_artifacts.py`
- `work2_coding/scripts/build_manuscript_frame.py`
- `work2_coding/Experiments/studies/formal_robust_menu.yaml`
- `work2_coding/Experiments/studies/final_robust_menu.yaml`
- `work2_coding/Experiments/studies/pilot_robust_menu.yaml`
- `work2_coding/Experiments/studies/smoke_robust_menu.yaml`

## Current Notes

- `.planning/codebase/` exists and has been refreshed for `work2_coding/`, but
  any remaining `ooh_code/` references must still be treated as stale until
  verified against the current filesystem.

- Do not revert, delete, stash, or overwrite unrelated user or prior workflow
  changes while resolving claim-ready gates.

- The v1.1 milestone supersedes the old writing-first next step. Manuscript
  writing remains deferred until this milestone decides whether the paper is
  claim-ready empirical, conditional diagnostic, or not ready.

- Phase 10 `CLAIM_GUARD.json` uses schema
  `phase10-strict-claim-guard-v1`, contains 8 claims, and keeps overall
  `claim_ready=false`. The paper-facing artifacts do not authorize manuscript
  claim upgrades.

- The current selected formal run has 35 completed comparable rows, 5 paired
  splits, and 7 policy tags. It is diagnostic/provisional, not claim-ready.

- `mainline_random_menu` currently has better mean net profit than
  `mainline_optimized_adaptive`, and adaptive loses to random on net profit in
  3 of 5 paired splits.

- `mainline_optimized_adaptive` and
  `mainline_optimized_fixed_window` are identical across tracked metrics, so
  adaptive-window increment claims are blocked until evidence changes.

- Phase 8 sensitivity evidence remains diagnostic/provisional with
  `claim_ready=false`.

- Phase 9 tractability evidence remains diagnostic/provisional because the
  configured large scales did not exercise greedy fallback; near-optimal greedy
  and online-tractability claims remain blocked.

- Phase 7 semi-real case material remains scaffold-only. Do not claim case
  validation or real passenger behavior from simulated demand or simulated
  choice.

- Phase 13 reconstructs the exact evidence boundary and current
  `claim_ready=false` causes before any repair, rerun, or manuscript writing.

- Phase 14 produces a gate repair plan without result manipulation.

- Phase 15 diagnoses the random-menu baseline issue and adaptive/fixed-window
  equality using source rows and code paths.

- Phase 16 selects Path A gate-only repair, Path B pre-registered final rerun,
  or Path C conditional diagnostic lock.

- Phase 17 executes only the selected path, with strict `CLAIM_GUARD.json` as
  the only authority for claim upgrades.

- Phase 18 produces the final manuscript-path decision.

- Timestamps should use ISO-8601 with timezone. Planning timestamps default to
  Beijing time; generated run artifacts may use UTC if their own metadata says
  so.

## Verification Baseline

Minimum check after implementation phases:

```powershell
cd work2_coding
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
```

Expected additional checks as phases implement them:

- `python scripts/test_optout_accounting.py`
- `python scripts/test_robust_menu_logic.py`
- `python scripts/test_menu_runtime_contract.py`
- `python scripts/test_menu_mode_adapters.py`
- `python scripts/test_policy_fairness_contract.py`
- `python scripts/test_paired_replay_contract.py`
- `python scripts/test_artifact_gates.py`
- `python scripts/test_formal_readiness.py`
- `python scripts/test_formal_replay_enablement.py`
- `python scripts/test_study_execution_status.py`
- `python scripts/test_manuscript_claim_guard.py`

## Next Step

The v1.1 claim-ready resolution milestone is initialized. Start by planning
Phase 13 evidence boundary reconstruction.

```text
$gsd-discuss-phase 13
```

Do not run calibration pilot, final replay, semi-real case execution, or
manuscript claim upgrades until Phase 13-16 evidence and path decisions
explicitly authorize them.

---
*Updated: 2026-06-16 after v1.1 claim-ready resolution milestone initialization*
