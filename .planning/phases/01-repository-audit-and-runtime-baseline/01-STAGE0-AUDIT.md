# Phase 1 Stage 0 Repository Audit

**Date:** 2026-06-11
**Scope:** Low-side-effect repository audit before algorithm behavior changes.
**Result:** `work2_coding/` is the active runtime root for this milestone.

## Audit Checklist

- Active runtime root identified: `work2_coding/`.
- Import smoke completed without constructing `Config(args)`.
- Runner scripts inspected statically only.
- Existing menu-oriented code asset identified.
- Parser/runner exposure gap identified as the top blocker.
- Opt-out accounting risk separated from accepted home delivery.
- Checkpoint status/provenance risk identified.
- Existing `.planning/codebase/` references to `ooh_code/` marked stale for this current filesystem.
- No `work2_coding/` files changed during Phase 1.

## Current Runtime Root

`rg --files work2_coding` confirms the current repository contains the inherited Work2 runtime package under `work2_coding/`, including:

- `work2_coding/Src/config.py`
- `work2_coding/Src/parser.py`
- `work2_coding/Src/Algorithms/DSPO_Menu.py`
- `work2_coding/run.py`
- `work2_coding/run_ppo.py`
- `work2_coding/Environments/OOH/`
- bundled `Amazon_data/` and `HombergerGehring_data/`

`Test-Path ooh_code` returned `False`. The existing `.planning/codebase/` maps are useful historical context, but their many `ooh_code/` paths are stale until each claim is rechecked against `work2_coding/`. No parallel `ooh_code/` root was created.

## Executed Commands

These commands were run from the repository root.

```powershell
rg --files work2_coding
```

Result: listed the current package files, including `Src/config.py`, `Src/parser.py`, `Src/Algorithms/DSPO_Menu.py`, `run.py`, `run_ppo.py`, and `Environments/OOH/`.

```powershell
python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"
```

Result:

```text
IMPORT_OK
```

```powershell
python -c "import sys; sys.path.insert(0, 'work2_coding'); from Src.parser import Parser; p=Parser().get_parser(); print('choices', p._option_string_actions['--algo_name'].choices); p.parse_args(['--algo_name','DSPO_Menu'])"
```

Result: printed parser choices `['DSPO', 'Heuristic', 'Baseline', 'PPO', 'SPO']`, then rejected `DSPO_Menu` as an invalid `--algo_name`.

Static inspection commands were also run with `rg` and `Get-Content` against `parser.py`, `config.py`, `run.py`, `run_ppo.py`, `DSPO_Menu.py`, `Agent.py`, `Predictors.py`, `customerchoice.py`, `Parcelpoint_py.py`, and selected `.planning/codebase/` documents.

## Recommended Commands Not Run

The following commands are intentionally **not run** in Phase 1 because they construct full runtime state, redirect stdout, create output directories, or execute training/evaluation episodes:

- `cd work2_coding; python run.py`
- `cd work2_coding; python run_ppo.py`
- `python -c "... Config(args) ..."`
- Any `--max_episodes 1` or episode-level smoke command
- Any formal replay, manifest, artifact, or manuscript build command

## Runner And Parser Contract

`work2_coding/run.py` and `work2_coding/run_ppo.py` both parse CLI args, construct `Config(args)`, instantiate `Solver`, and execute training/evaluation loops. They are not low-side-effect commands.

`work2_coding/Src/config.py` performs several side effects during `Config(args)` construction:

- creates experiment, log, checkpoint, and result directories;
- writes `args.yaml`;
- redirects `sys.stdout` through `Utils.Logger`;
- loads demand data;
- constructs training and test environments;
- dynamically loads the algorithm from `args.algo_name`.

`work2_coding/Src/parser.py` currently exposes `--algo_name` choices as `DSPO`, `Heuristic`, `Baseline`, `PPO`, and `SPO`. It does not expose `DSPO_Menu` and does not define the `menu_*` fields expected by `DSPO_Menu.__init__`, such as `menu_mode`, `menu_policy`, `menu_k`, `menu_selection_solver`, `menu_objective_mode`, ETA variant/filter controls, and service guardrail fields.

This means `DSPO_Menu.py` exists, but the parser/config/runner contract is inconsistent or incomplete for menu-mode experiments.

## Current Menu Assets

`work2_coding/Src/Algorithms/DSPO_Menu.py` is present and is a real current asset. Static inspection found:

- a constructor guard requiring `config.menu_mode`;
- menu fields including `menu_policy`, `menu_k`, `menu_selection_solver`, and `menu_objective_mode`;
- ETA/time-window fields including `menu_time_filtering`, `menu_eta_filter_mode`, `eta_scale`, `menu_eta_variant`, and oracle/stronger ETA options;
- policies including `home_only`, `nearest_heuristic`, `top_k_cheapest`, `min_lateness`, `random_top_k`, expected-profit variants, service-constrained variants, and diagnostic all-feasible behavior;
- exact and greedy selection paths, including `exact_enumerated_menu_count`, `exact_menu_value`, `greedy_menu_value`, `relative_optimality_gap`, `menu_overlap_rate`, build times, and candidate counts;
- metadata hooks on selected offers for policy, ETA, exact/greedy, and menu-build diagnostics.

Phase 1 did not review or change the behavioral correctness of this file. That belongs to Phase 2+.

## Simulator And Choice Modules

Relevant current simulator modules are:

- `work2_coding/Environments/OOH/customerchoice.py`
- `work2_coding/Environments/OOH/Parcelpoint_py.py`
- `work2_coding/Environments/OOH/env_utils.py`
- `work2_coding/Environments/OOH/containers.py`

The legacy `customerchoice_offer` and `customerchoice_pricing` paths return either an accepted parcel point or `customer.home, False, -1` for home delivery. The current audited path does not prove a separate `opted_out` transition.

`Parcelpoint_py.step()` appends the returned `loc` into route data, increments home-delivery service accounting when `accepted_pp` is false, and inserts `loc` into the fleet route through `cheapestInsertionRoute(...)`. Therefore future opt-out work must keep `opted_out` separate from accepted home pickup so outside-option choices do not mutate routes or service accounting as delivered requests.

## Checkpoint And Provenance Risk

`Agent.save()` delegates module checkpoints to `module.save(...)`. Predictor modules in `work2_coding/Src/Utils/Predictors.py` call `torch.save(...)` and load with direct `torch.load(...)`.

The current low-side-effect scan did not find row-level fields such as `checkpoint_load_status`, checkpoint hash, checkpoint compatibility status, or explicit provenance metadata. Before formal comparisons, shared predictor loading must be visible in result metadata and must fail closed or mark intentional mismatch explicitly.

## Experiment Fairness Risks

Later robust menu comparisons must preserve paired replay fairness:

- same request traces;
- same trained predictor checkpoint;
- same random seeds and split IDs;
- same routing/HGS parameters;
- same pricing mode unless the manifest explicitly varies it;
- no-filter treated as diagnostic unless formal evidence justifies stronger claims.

Current Phase 1 did not run episode-level comparisons, so it does not validate these fairness conditions yet.

## Blocking Gaps

1. Parser/runner menu exposure is incomplete: `DSPO_Menu.py` exists, but `parser.py` rejects `--algo_name DSPO_Menu` and does not expose required `menu_*` configuration fields.
2. `Config(args)` is not a safe Phase 1 smoke target because it creates directories, writes config snapshots, redirects stdout, loads data, and constructs environments.
3. Opt-out accounting is not yet isolated from accepted home delivery in the audited simulator path.
4. Checkpoint load status and provenance are not explicit enough for formal scientific comparisons.
5. `.planning/codebase/` currently describes `ooh_code/`; this is stale relative to the current filesystem, where `work2_coding/` is the active root.

## Minimal Patch Plan

Future phases should address the gaps in this order:

1. **Parser and runner menu exposure:** Add a safe, explicit CLI/config contract for menu mode. Expose `DSPO_Menu` or a canonical menu algorithm name, add required `menu_*` fields, and create a low-cost smoke path that can instantiate the menu algorithm without running full studies.
2. **Opt-out accounting:** Introduce explicit passenger outcomes such as `accepted_home`, `accepted_meeting_point`, and `opted_out`. Add deterministic tests proving opted-out requests do not enter route data, service time, or home-delivery counts as accepted pickups.
3. **Checkpoint metadata:** Add explicit `checkpoint_load_status`, checkpoint path/hash, compatibility status, and intentional-mismatch markers to runtime metadata and normalized result rows.
4. **Robust ETA and objective behavior:** Implement and test robust ETA filter modes, candidate-level diagnostics, opt-out/ETA risk penalties, service guardrails, and exact-small versus greedy-large diagnostics.
5. **Experiment contracts:** Define smoke, pilot, and formal manifests with paired request traces, shared checkpoint reuse, fixed seeds/splits, policy tags, and no-filter diagnostic handling.
6. **Artifact gates:** Require provenance-backed normalized rows, aggregate summaries, tables/figures, manifest hashes, and placeholder-status gates before manuscript claims are strengthened.

Phase 1 made no algorithm behavior changes, no simulator accounting changes, no checkpoint behavior changes, no ETA/objective/solver changes, no experiment manifest changes, and no generated-result or paper-artifact edits.
