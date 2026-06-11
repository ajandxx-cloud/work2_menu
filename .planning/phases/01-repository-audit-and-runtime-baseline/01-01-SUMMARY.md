---
phase: 01-repository-audit-and-runtime-baseline
plan: 01
subsystem: audit
tags: [work2, runtime, parser, menu, checkpoint, opt-out]
requires: []
provides:
  - Stage 0 repository audit for current Work2 runtime root
  - Minimal patch plan for robust time-window menu experiments
affects: [phase-2-core-semantics-and-robust-menu-logic, experiments, artifacts]
tech-stack:
  added: []
  patterns: [low-side-effect audit before behavior changes]
key-files:
  created:
    - .planning/phases/01-repository-audit-and-runtime-baseline/01-STAGE0-AUDIT.md
    - .planning/phases/01-repository-audit-and-runtime-baseline/01-01-SUMMARY.md
  modified:
    - .planning/config.json
key-decisions:
  - "Use work2_coding/ as the active runtime root for this milestone."
  - "Treat ooh_code/ references in .planning/codebase/ as stale until revalidated."
  - "Keep Phase 1 to audit and minimal patch planning only."
patterns-established:
  - "Separate executed low-side-effect commands from recommended not-run commands."
  - "Document parser/runner exposure before modifying algorithm behavior."
requirements-completed:
  - AUDIT-01
  - AUDIT-02
  - AUDIT-03
  - AUDIT-04
duration: 21min
completed: 2026-06-11
---

# Phase 01 Plan 01: Repository Audit And Runtime Baseline Summary

**Stage 0 audit identifying `work2_coding/` as the active runtime root and parser/runner menu exposure as the top blocker.**

## Performance

- **Duration:** 21 min
- **Started:** 2026-06-11T09:19:00+08:00
- **Completed:** 2026-06-11T09:40:00+08:00
- **Tasks:** 3/3 complete
- **Files modified:** 3 planning files

## Accomplishments

- Created the Stage 0 audit at `.planning/phases/01-repository-audit-and-runtime-baseline/01-STAGE0-AUDIT.md`.
- Confirmed `work2_coding/` contains the active runtime files and `ooh_code/` is absent from the current filesystem.
- Re-ran the import smoke and parser-only check; `Src.config` imports successfully, while parser rejects `--algo_name DSPO_Menu`.
- Documented current menu assets in `DSPO_Menu.py`, runner/config side effects, opt-out accounting risk, checkpoint provenance risk, and paired replay fairness risks.
- Produced a ranked minimal patch plan for Phase 2+ without modifying runtime behavior.

## Task Commits

Each task was executed in the current session. No production-code commits were created because Phase 1 is documentation-only.

1. **Task 1: Confirm active runtime and low-side-effect baseline** - completed in working tree
2. **Task 2: Audit current menu, runner, accounting, and checkpoint risks** - completed in working tree
3. **Task 3: Produce minimal patch plan and execution summary** - completed in working tree

**Plan metadata:** pending commit by execute-phase close-out.

## Files Created/Modified

- `.planning/phases/01-repository-audit-and-runtime-baseline/01-STAGE0-AUDIT.md` - concise Stage 0 repository audit and minimal patch plan.
- `.planning/phases/01-repository-audit-and-runtime-baseline/01-01-SUMMARY.md` - execution summary and self-check.
- `.planning/config.json` - workflow `_auto_chain_active` cleared by execute-phase initialization to avoid stale auto-chain behavior.

No files under `work2_coding/` were modified.

## Commands Executed

```powershell
gsd-sdk query config-set workflow._auto_chain_active false
gsd-sdk query init.execute-phase 1
gsd-sdk query phase-plan-index 1
rg --files work2_coding
python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"
python -c "import sys; sys.path.insert(0, 'work2_coding'); from Src.parser import Parser; p=Parser().get_parser(); print('choices', p._option_string_actions['--algo_name'].choices); p.parse_args(['--algo_name','DSPO_Menu'])"
rg -n "algo_name|choices|menu_|DSPO_Menu|Config\(|dynamic_load" work2_coding\Src\parser.py work2_coding\Src\config.py work2_coding\run.py work2_coding\run_ppo.py
rg -n "menu_policy|menu_k|menu_selection_solver|menu_objective_mode|eta|filter|exact|greedy|home_only|nearest_heuristic|top_k_cheapest|min_lateness|random_top_k|metadata|opt" work2_coding\Src\Algorithms\DSPO_Menu.py
rg -n "opted_out|outside|home|accepted_pp|count_home_delivery|route|append|insert|customerchoice|customerChoice" work2_coding\Environments\OOH\customerchoice.py work2_coding\Environments\OOH\Parcelpoint_py.py
rg -n "checkpoint|torch\.load|load\(|save\(|except|pass|checkpoint_load_status|provenance" work2_coding\Src\Algorithms\Agent.py work2_coding\Src\Utils\Predictors.py work2_coding\Src\Utils\Utils.py work2_coding\Src\config.py
Test-Path ooh_code
```

Key results:

- Import smoke printed `IMPORT_OK`.
- Parser choices were `['DSPO', 'Heuristic', 'Baseline', 'PPO', 'SPO']`.
- Parser rejected `DSPO_Menu` as an invalid `--algo_name`.
- `Test-Path ooh_code` returned `False`.

## Commands Intentionally Not Run

- `cd work2_coding; python run.py`
- `cd work2_coding; python run_ppo.py`
- Any command constructing `Config(args)` directly
- Any episode-level smoke, training, replay, artifact, or manuscript command

Reason: Phase 1 is restricted to low-side-effect checks. Those commands can create runtime directories, redirect stdout, write outputs, or execute episodes.

## Decisions Made

- `work2_coding/` is the active runtime root for this milestone.
- Existing `.planning/codebase/` references to `ooh_code/` are stale historical context until revalidated.
- Parser/runner menu exposure is the first minimal patch-plan item because `DSPO_Menu.py` exists but is not reachable through the inherited CLI contract.
- Opt-out accounting, checkpoint metadata, robust ETA/objective behavior, experiments, and artifacts are future Phase 2+ work.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- Historical git log contains older `01-01` commits from previous phase directories. They were inspected and found unrelated to the current `.planning/phases/01-repository-audit-and-runtime-baseline/` plan, so safe resume continued.
- The parser-only command exits nonzero by design because it validates that `DSPO_Menu` is currently rejected.

## User Setup Required

None - no external service configuration required.

## Verification

- `python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"`: PASSED, printed `IMPORT_OK`.
- `01-STAGE0-AUDIT.md` exists and contains `## Minimal Patch Plan`: PASSED.
- `01-STAGE0-AUDIT.md` separates executed commands from recommended commands not run: PASSED.
- `01-STAGE0-AUDIT.md` mentions `work2_coding/`, `DSPO_Menu`, `parser.py`, `opt-out`, `checkpoint`, and stale `ooh_code/` references: PASSED.
- No files under `work2_coding/` modified by this plan: PASSED.
- `01-01-SUMMARY.md` exists and contains `Self-Check: PASSED`: PASSED.

## Self-Check: PASSED

All Phase 1 Plan 01 acceptance criteria are satisfied.

## Next Phase Readiness

Phase 2 can start from a verified runtime baseline. The top follow-up is to add safe parser/config/runner exposure for menu mode before changing opt-out, checkpoint, ETA, objective, solver, experiment, or artifact behavior.

---
*Phase: 01-repository-audit-and-runtime-baseline*
*Completed: 2026-06-11*
