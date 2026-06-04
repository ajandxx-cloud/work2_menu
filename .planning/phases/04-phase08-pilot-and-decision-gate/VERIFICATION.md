# Phase 4 Verification: Phase08 Pilot And Decision Gate

## Status

status: passed

Phase08 smoke and 3-seed pilot both completed through the study pipeline. The dedicated artifact gate generated the five required phase-local artifacts from the explicit pilot run id. The decision is `recalibrate_objective`, not `proceed_to_formal`.

## Changed Files

- `ooh_code/experiments/studies/work2_phase08_smoke.yaml`
- `ooh_code/experiments/studies/work2_phase08_pilot.yaml`
- `ooh_code/scripts/test_phase08_manifest.py`
- `ooh_code/scripts/build_phase08_artifacts.py`
- `ooh_code/scripts/test_phase08_artifact_gate.py`
- `ooh_code/run_menu_compare.py`
- `.planning/phases/04-phase08-pilot-and-decision-gate/artifacts/pilot_rows.csv`
- `.planning/phases/04-phase08-pilot-and-decision-gate/artifacts/pilot_summary.md`
- `.planning/phases/04-phase08-pilot-and-decision-gate/artifacts/oracle_diagnostics.md`
- `.planning/phases/04-phase08-pilot-and-decision-gate/artifacts/profit_vs_quit_tradeoff.md`
- `.planning/phases/04-phase08-pilot-and-decision-gate/artifacts/phase08_decision.md`
- `.planning/phases/04-phase08-pilot-and-decision-gate/VERIFICATION.md`

## Commands Run

| Command | Result |
| --- | --- |
| `cd ooh_code && python scripts/test_phase08_manifest.py` | passed |
| `cd ooh_code && python scripts/test_phase08_artifact_gate.py` | passed |
| `cd ooh_code && python -m py_compile scripts/build_phase08_artifacts.py scripts/test_phase08_manifest.py scripts/test_phase08_artifact_gate.py Src/research_pipeline.py run_menu_compare.py scripts/run_study.py` | passed |
| `cd ooh_code && python scripts/run_study.py --study work2_phase08_smoke` | passed |
| `cd ooh_code && python scripts/run_study.py --study work2_phase08_pilot` | initially failed on nullable `service_constrained_net_profit` aggregation; fixed and resumed |
| `cd ooh_code && python scripts/run_study.py --study work2_phase08_pilot --resume_run_id 20260604T124624Z_bf03b88d` | completed after resume |
| `cd ooh_code && python scripts/build_phase08_artifacts.py --run-id 20260604T124624Z_bf03b88d` | passed |
| `git diff -- ooh_code/Environments/OOH/customerchoice.py ooh_code/Src/Utils/MathUtils.py ooh_code/Environments/OOH/env_utils.py ooh_code/Src/Algorithms/DSPO_Menu.py` | showed a pre-existing `DSPO_Menu.py` diff; no Phase08 edits were made to MNL, Lambert-W, or HGS/Hygese files |
| `git status --short -- ooh_code/artifacts` | non-empty from pre-existing artifact changes; explicit search found no `phase08` files under `ooh_code/artifacts` |

## Runs

- Smoke run id: `20260604T124314Z_847e54ae`
- Smoke path: `ooh_code/outputs/studies/work2_phase08_smoke/20260604T124314Z_847e54ae`
- Pilot run id: `20260604T124624Z_bf03b88d`
- Pilot path: `ooh_code/outputs/studies/work2_phase08_pilot/20260604T124624Z_bf03b88d`
- Pilot status: `completed`
- Pilot splits: `3/3`

## Artifact Outputs

- `.planning/phases/04-phase08-pilot-and-decision-gate/artifacts/pilot_rows.csv`
- `.planning/phases/04-phase08-pilot-and-decision-gate/artifacts/pilot_summary.md`
- `.planning/phases/04-phase08-pilot-and-decision-gate/artifacts/oracle_diagnostics.md`
- `.planning/phases/04-phase08-pilot-and-decision-gate/artifacts/profit_vs_quit_tradeoff.md`
- `.planning/phases/04-phase08-pilot-and-decision-gate/artifacts/phase08_decision.md`

## Decision

- decision_state: `recalibrate_objective`
- pilot_complete: `true`
- human_confirmation_required: `false`

Primary reasons recorded by `phase08_decision.md`:

- Service-Constrained Expected-Profit used fallback on at least one seed.
- Expected-Profit Enumeration violated the quit-rate guardrail and had ineligible service-constrained profit rows.
- Service-Constrained Expected-Profit violated the quit-rate guardrail and had ineligible service-constrained profit rows.
- Cost-L or CNN-Menu had unavailable service-constrained profit, so the hard comparison gate could not proceed.
- Profit Oracle did not provide a clear service-constrained reference above Cost-L and CNN-Menu.

## Deviations And Fixes

- `aggregate_episode_metrics` crashed when episode-level `service_constrained_net_profit` mixed floats and `None`. The fix preserves `None` for unavailable service-constrained aggregates instead of averaging through unavailable guardrail-failing rows.
- The artifact gate initially treated `service_guardrail_pass` and `service_guardrail_violation` as booleans. Real normalized rows store them as averaged rates across eval episodes, so the gate now validates rates and marks any nonzero violation rate as ineligible.
- The artifact gate initially assumed Cost-L and CNN-Menu service-constrained profit were always numeric. Real pilot rows can make comparator service-constrained profit unavailable; this now blocks `proceed_to_formal` and routes to scenario/recalibration evidence rather than crashing.
- The pilot process exited twice without a Python traceback after seed2 setup. Resuming with `PYTHONFAULTHANDLER=1` completed seed2 evaluation and final aggregation.

## Stable-Core Statement

This phase did not edit:

- `ooh_code/Environments/OOH/customerchoice.py`
- `ooh_code/Src/Utils/MathUtils.py`
- `ooh_code/Environments/OOH/env_utils.py`

`ooh_code/Src/Algorithms/DSPO_Menu.py` already has a worktree diff from prior policy-semantics work. Phase08 execution did not add edits to that file.

## No Formal Claim

The pilot does not support proceeding to formal evidence as-is. The next human-reviewed step should recalibrate objective/service parameters or diagnose why the service-constrained and oracle references fail the Phase08 guardrails.
