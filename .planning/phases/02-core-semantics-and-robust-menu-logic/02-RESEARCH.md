# Phase 02 Research: Core Semantics And Robust Menu Logic

**Date:** 2026-06-11
**Runtime root:** `work2_coding/`
**Result:** Plan against current `work2_coding/` files only. Existing `.planning/codebase/` `ooh_code/` references are stale risk memory unless revalidated.

## Research Complete

Phase 2 should treat `work2_coding/Src/Algorithms/DSPO_Menu.py` as the existing menu algorithm asset, but the surrounding runtime contracts are behind it. The file already imports `MenuOffer`, `ServiceBundle`, and `Src.Utils.option_features`, expects many `menu_*` parser fields, uses predictor constructors with multi-output and auxiliary-feature arguments, and writes menu diagnostics into offer metadata. In the current filesystem, those support surfaces are missing or incomplete.

The safest implementation sequence is:

1. Restore the low-side-effect menu runtime contract.
2. Separate choice outcomes and simulator mutation semantics.
3. Make checkpoint load status and provenance explicit.
4. Tighten robust ETA filter/objective/solver behavior with script-style tests.

## Current Code Findings

### Runtime Contract

- `work2_coding/Src/parser.py` rejects `--algo_name DSPO_Menu`; choices are `DSPO`, `Heuristic`, `Baseline`, `PPO`, and `SPO`.
- `parser.py` does not define the `menu_*`, `max_candidates`, `freeze_learning`, `eval_only`, or checkpoint/run-mode controls expected by `DSPO_Menu.py` and the Phase 2 context.
- `work2_coding/Environments/OOH/containers.py` currently defines only `Location`, `ParcelPoint`, `ParcelPoints`, `Vehicle`, `Fleet`, and `Customer`; it does not define `ServiceBundle`, `MenuOffer`, or a structured choice result.
- `work2_coding/Src/Utils/option_features.py` is absent even though `DSPO_Menu.py` imports `normalize_features` and `build_option_tensor`.
- `work2_coding/Src/Utils/Predictors.py` constructors currently return single-output models with scalar capacity features. `DSPO_Menu.py` expects `aux_dim` and `output_dim` support.

### Opt-Out Accounting

- `customerchoice_offer()` and `customerchoice_pricing()` return legacy tuples `(loc, accepted_pp, idx, price)`.
- Home delivery and any future opt-out both currently look like `accepted_pp == False` to `Parcelpoint_py.step()`.
- `Parcelpoint_py.step()` appends `loc` to route data before distinguishing outcomes, increments home-delivery service accounting when `accepted_pp` is false, then inserts `loc` into the fleet route.
- Therefore an outside option must not be represented by the home location unless a dual adapter marks it as non-mutating and `step()` honors that marker.

### Checkpoint Status

- `Agent.save()` delegates module saves, but there is no corresponding structured load status on the agent.
- `Predictors.py` and `Utils.NeuralNet.load()` use direct `torch.load(...)` and return no status metadata.
- Formal/pilot fail-closed behavior needs a small status object or dictionary that can be attached to `config` or algorithm instances and later emitted by result rows.

### Robust ETA And Solver Semantics

- `DSPO_Menu.py` already has substantial ETA and menu-selection code, including `hard`, `calibrated`, legacy `interval`, and `none` handling, objective families, service guardrails, exact/greedy paths, and metadata hooks.
- Required Phase 2 modes are `hard`, `calibrated`, `interval_overlap`, `chance_constraint`, `soft_penalty`, and `none`. Current `interval` naming and diagnostics need normalization.
- `soft_penalty` must retain candidates and apply risk in objective value, not prune.
- `none` must disable ETA pruning only; it must not become "display every candidate regardless of routing/capacity".
- Exact/greedy diagnostics exist in pieces, but they should be consistently logged for exact-small and greedy-large decisions, including threshold and time-budget fallback reasons.

## Planning Implications

- Start with import/parser and dataclass/helper compatibility before any behavior tests.
- Keep script-style tests under `work2_coding/scripts/` because the active runtime currently has no test directory.
- Avoid full episode or `Config(args)` smoke as the first acceptance target; Phase 2 minimum is import plus parser contract unless constructor/menu-action smoke naturally becomes cheap after runtime repair.
- Use synthetic lightweight objects for objective, filter, and solver tests so HGS/data loading does not become a planning dependency.
- Keep no-filter diagnostic framing explicit in plan text and metadata checks.

## Research Risks

- `DSPO_Menu.py` may require small compatibility edits beyond parser/dataclasses because current predictors and memory buffer targets are single-output by default.
- `Parcelpoint_py.step()` returns a positional stats tuple consumed by `run.py` and `run_ppo.py`; opt-out fields should be appended or exposed through metadata/log attributes without breaking legacy indexes.
- Checkpoint metadata can be made explicit before a full manifest pipeline exists, but Phase 2 should not pretend to complete formal normalized rows. That belongs to Phase 3/4.

## Recommended Plan Set

- `02-01-PLAN.md`: Runtime menu contract and script-style test harness.
- `02-02-PLAN.md`: Structured choice result and opt-out non-mutation.
- `02-03-PLAN.md`: Checkpoint load status and provenance metadata.
- `02-04-PLAN.md`: Robust ETA filters, objective semantics, and solver diagnostics.

## RESEARCH COMPLETE
