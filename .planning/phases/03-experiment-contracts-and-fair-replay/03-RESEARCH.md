# Phase 03 Research: Experiment Contracts And Fair Replay

**Date:** 2026-06-11
**Runtime root:** `work2_coding/`
**Result:** Plan against current `work2_coding/` files only. There is no current `ooh_code/` root.

## Research Complete

Phase 3 should add a lightweight but real experiment-contract layer around the repaired Phase 2 menu runtime. The current runtime has `DSPO_Menu`, parser flags, opt-out accounting, checkpoint metadata, ETA diagnostics, and solver telemetry, but it does not yet have a manifest study runner, paired replay contract, normalized row schema, or study YAML files.

The safest implementation sequence is:

1. Add manifest schema, studies, suites, validation, and contract tests.
2. Add paired replay and normalized row helpers that consume Phase 2 metadata.
3. Add policy adapters and fairness validation for all required baselines.
4. Add a smoke study command that uses the public runner and emits normalized rows.

## Current Code Findings

### Existing Assets

- `work2_coding/Src/parser.py` contains parser choices for `DSPO_Menu`, `menu_policy`, `menu_eta_filter_mode`, checkpoint/run-mode fields, `menu_k`, `max_candidates`, pricing, and HGS controls.
- `work2_coding/Src/config.py` seeds NumPy/Torch, constructs train/test environments, and stores default checkpoint metadata.
- `work2_coding/Src/Algorithms/DSPO_Menu.py` supports required policy names: `offer_all_feasible_bundles`, `home_only`, `nearest_heuristic`, `top_k_cheapest`, `min_lateness`, `random_top_k`, `risk_adjusted_expected_profit`, and `service_guarded_expected_profit`. It records effective policy, ETA diagnostics, build time, and solver telemetry in offer metadata.
- `work2_coding/Environments/OOH/Parcelpoint_py.py` exposes `stats[8]` metadata, `choice_log`, `acceptance_rate()`, `optout_rate()`, and route mutation guardrails.
- `work2_coding/scripts/test_*.py` use direct script-style tests; Phase 3 should continue this pattern.

### Missing Phase 3 Surfaces

- No `work2_coding/experiments/studies/` or `work2_coding/experiments/suites/` contracts exist in the current file list.
- No `work2_coding/Src/research_pipeline.py`, `work2_coding/Src/experiment_contracts.py`, or equivalent normalized row writer exists.
- No `work2_coding/scripts/run_study.py` wrapper exists.
- No current command validates paired replay fairness across policy variants.
- No normalized row schema explicitly carries checkpoint, manifest, trace, filter, solver, opt-out, and acceptance metadata.

### Planning Implications

- Manifest validation should reuse parser choices where possible, so allowed policies/filter modes cannot drift from runtime.
- Pairing validation should compare resolved parser namespaces, not raw YAML, because parser defaults are part of the actual experimental contract.
- The smoke runner must keep formal-evidence status explicit. If the first smoke command uses synthetic or shortened execution, rows must carry `run_mode=smoke` and a non-formal/incomplete status.
- Pilot/formal manifests can be validated in Phase 3 without running expensive evidence. Phase 4 can run them and generate artifacts.
- Request trace fairness is the core scientific guardrail: seed, split, trace ID, checkpoint, pricing, HGS, and candidate settings must be shared unless intentionally varied.

## Recommended Plan Set

- `03-01-PLAN.md`: Study manifest contracts and schema validation.
- `03-02-PLAN.md`: Paired replay contract and normalized row writer.
- `03-03-PLAN.md`: Baseline policy adapters and fairness validators.
- `03-04-PLAN.md`: Smoke study runner, uptake regimes, and end-to-end row emission.

## RESEARCH COMPLETE
