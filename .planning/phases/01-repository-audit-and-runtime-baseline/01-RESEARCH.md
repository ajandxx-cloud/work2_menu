# Phase 1 Research: Repository Audit And Runtime Baseline

**Researched:** 2026-06-11
**Mode:** inline research; no subagent tool available
**Status:** Ready for planning

## Research Questions

1. Which runtime root is authoritative for Phase 1?
2. What low-side-effect checks already prove or challenge the runtime baseline?
3. Which current files expose menu assets, runner gaps, opt-out risks, checkpoint risks, and stale planning references?
4. What should Phase 1 execute without drifting into Phase 2 behavior changes?

## Findings

### Active Runtime Root

- `work2_coding/` is the current active runtime root.
- `rg --files` found `work2_coding/Src/config.py`, `work2_coding/Src/parser.py`, `work2_coding/Src/Algorithms/DSPO_Menu.py`, `work2_coding/run.py`, `work2_coding/run_ppo.py`, and `work2_coding/Environments/OOH/`.
- No current `ooh_code/` root was found in the repository file listing.
- Existing `.planning/codebase/` maps still heavily reference `ooh_code/`; treat them as historical/stale until each claim is verified against `work2_coding/`.

### Executed Low-Side-Effect Checks

- Command run from repository root:
  `python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"`
  Result: `IMPORT_OK`.
- Command run from repository root:
  `python -c "import sys; sys.path.insert(0, 'work2_coding'); from Src.parser import Parser; p=Parser().get_parser(); print('choices', p._option_string_actions['--algo_name'].choices); p.parse_args(['--algo_name','DSPO_Menu'])"`
  Result: parser printed choices `['DSPO', 'Heuristic', 'Baseline', 'PPO', 'SPO']` and rejected `DSPO_Menu` as an invalid `--algo_name`.

### Menu Asset And Entrypoint Gap

- `work2_coding/Src/Algorithms/DSPO_Menu.py` exists and contains menu-oriented logic:
  - constructor guard requiring `config.menu_mode`;
  - menu policy fields such as `menu_policy`, `menu_k`, `menu_selection_solver`, `menu_objective_mode`;
  - ETA/filter fields such as `menu_eta_filter_mode`, `eta_scale`, `menu_time_filtering`;
  - policy branches including `home_only`, `nearest_heuristic`, `top_k_cheapest`, `min_lateness`, `random_top_k`, expected-profit variants, service-constrained variants, exact and greedy selection paths;
  - metadata hooks for exact/greedy diagnostics and selected offer metadata.
- `work2_coding/Src/parser.py` does not expose `DSPO_Menu` in `--algo_name` choices and does not define the many `menu_*` fields required by `DSPO_Menu.__init__`.
- `work2_coding/Src/config.py` dynamically loads the algorithm using `args.algo_name`; therefore the current parser/config/runner contract cannot reliably instantiate `DSPO_Menu` through the inherited CLI.
- Phase 1 should document this as the top blocker and defer parser/runner repair to Phase 2.

### Runner And Config Side Effects

- `work2_coding/run.py` and `work2_coding/run_ppo.py` both construct `Config(args)` and execute training/evaluation loops.
- `work2_coding/Src/config.py` creates experiment/log/checkpoint/result directories, writes `args.yaml`, redirects `sys.stdout`, loads data, constructs train/test environments, and dynamically loads the algorithm.
- Because Phase 1 is a low-side-effect audit, it should inspect these files and record risks, not run episode-level smoke commands.

### Opt-Out And Accounting Risk

- Current `work2_coding/Environments/OOH/customerchoice.py` exposes only home delivery or accepted parcelpoint outcomes in the legacy `customerchoice_offer` and `customerchoice_pricing` paths.
- `work2_coding/Environments/OOH/Parcelpoint_py.py` treats `accepted_pp == False` as home delivery, increments `count_home_delivery`, appends the selected location into route data, and inserts that location into the fleet route.
- `DSPO_Menu.py` models outside-option probability internally for menu scoring, but the audited simulator path does not yet prove a separate `opted_out` transition that avoids route mutation.
- Phase 1 should report this as a Phase 2 accounting blocker, not repair it.

### Checkpoint Visibility Risk

- `work2_coding/Src/Algorithms/Agent.py` saves models through module `save(...)`.
- `work2_coding/Src/Utils/Predictors.py` and `work2_coding/Src/Utils/Utils.py` expose `load(...)` methods that call `torch.load(...)` directly.
- The current low-side-effect scan did not find row-level `checkpoint_load_status` or checkpoint provenance metadata.
- Phase 1 should flag explicit checkpoint status/provenance as a Phase 2 and experiment-pipeline requirement.

## Planning Recommendation

Create one autonomous execution plan:

- Read planning context, current runtime files, and stale codebase maps.
- Run only the already-approved low-side-effect checks plus static inspections.
- Write `.planning/phases/01-repository-audit-and-runtime-baseline/01-STAGE0-AUDIT.md`.
- Keep the audit concise: current facts, executed commands, not-run commands, runner gaps, menu asset/gap, opt-out risk, checkpoint risk, fairness risk, and minimal patch plan.
- Do not edit algorithm/runtime behavior in Phase 1.

## RESEARCH COMPLETE

