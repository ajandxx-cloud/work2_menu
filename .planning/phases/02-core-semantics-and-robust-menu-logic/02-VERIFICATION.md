---
phase: 02-core-semantics-and-robust-menu-logic
status: passed
verified: 2026-06-11T21:43:53+08:00
verified_by_phase: 07-audit-closure-and-traceability-repair
active_runtime_root: work2_coding
requirements:
  - ACCT-01
  - ACCT-02
  - ACCT-03
  - ACCT-04
  - ETA-01
  - ETA-02
  - ETA-03
  - ETA-04
  - MENU-01
  - MENU-02
  - MENU-03
  - MENU-04
---

# Phase 02 Verification: Core Semantics And Robust Menu Logic

## Result

**Status:** passed

Phase 2 is no longer an orphaned implementation phase. ACCT-01..04, ETA-01..04, and MENU-01..04 all have command-backed evidence from the current `work2_coding/` runtime.

`MENU-02` was reconciled under the strict Phase 07 discussion rule: it is marked complete only because focused deterministic tests now prove both parts of the contract:

- compared study settings pair `pricing` and prevent `menu_pricing_mode` / `menu_pricing_constant` from drifting as policy overrides,
- menu expected-profit evaluation records pricing and system-aware cost definitions in offer metadata.

## Verification Commands

All commands were run from `work2_coding/` on 2026-06-11.

| Command | Observed Output | Result |
|---|---|---|
| `python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` | `IMPORT_OK` | PASS |
| `python scripts/test_menu_runtime_contract.py` | `PASS: 5 menu runtime contract tests` | PASS |
| `python scripts/test_optout_accounting.py` | `PASS: 5 opt-out accounting tests` | PASS |
| `python scripts/test_checkpoint_provenance.py` | `PASS: 6 checkpoint provenance tests` | PASS |
| `python scripts/test_robust_menu_logic.py` | `PASS: 7 robust menu logic tests` | PASS |
| `python scripts/test_experiment_contracts.py` | `PASS: 12 experiment contract tests` | PASS |
| `python scripts/test_policy_fairness_contract.py` | `PASS: 12 policy fairness contract tests` | PASS |

## Requirement Traceability

| Requirement | Status | Evidence |
|---|---|---|
| ACCT-01 | complete | `ChoiceResult` exposes `accepted_home`, `accepted_meeting_point`, and `opted_out`; `test_optout_accounting.py` passes. |
| ACCT-02 | complete | `Parcelpoint_py.step()` gates mutation on `ChoiceResult.route_mutates`; forced opt-out test verifies no accepted-home route/service mutation. |
| ACCT-03 | complete | `test_optout_accounting.py` verifies `count_opted_out`, accepted-home/meeting-point counts, acceptance rate, and stats metadata. |
| ACCT-04 | complete | `test_checkpoint_provenance.py` verifies loaded, failed, intentional mismatch, hash, required flag, and config/agent metadata propagation. |
| ETA-01 | complete | Parser and `_eta_filter_result()` support `hard`, `calibrated`, `interval_overlap`, `chance_constraint`, `soft_penalty`, and `none`; `test_robust_menu_logic.py` passes. |
| ETA-02 | complete | ETA diagnostics include predicted/filter ETA, sigma, interval bounds, window bounds, pass/fail, violation probability, prune reason, source/variant, and retention metadata. |
| ETA-03 | complete | `none` mode disables ETA pruning and keeps diagnostics explicit; routing/capacity feasibility remain outside the ETA filter and are not disabled by no-filter. |
| ETA-04 | complete | `soft_penalty` retains candidates and applies `eta_soft_penalty` through objective metadata; `test_eta_soft_penalty_enters_objective` passes. |
| MENU-01 | complete | Menu evaluation combines expected profit, outside-option probability, ETA risk penalty, service guardrails, and policy diagnostics; robust menu tests pass. |
| MENU-02 | complete | `test_pricing_contract_is_paired_and_row_recorded` verifies paired `pricing` and row recording; `test_pricing_and_system_cost_kind_metadata_for_expected_profit_policy` verifies pricing/evaluation cost-kind metadata uses `system_eval_cost`. |
| MENU-03 | complete | Exact-small and greedy-large behavior is tested through exact solver and threshold fallback diagnostics. |
| MENU-04 | complete | Solver telemetry includes effective solver, fallback reason, enumerated menu count, relative gap/overlap where computed, and build diagnostics. |

## Boundary Notes

- `no_filter` remains diagnostic: it disables ETA pruning only and does not imply routing or capacity feasibility is disabled.
- `soft_penalty` is not a pruning mode. It preserves ETA-risky candidates and moves risk into objective value.
- Checkpoint load status is explicit in metadata. Required pilot/formal checkpoints still fail closed when absent.
- Exact enumeration remains limited to configured small candidate sets; larger sets use greedy fallback with diagnostics.
- `MENU-02` is complete for the current contract evidence, but later formal evidence must still preserve paired pricing/cost settings in manifests and rows.

## Audit Closure

The v2.0 audit orphan reason for Phase 2 is closed: `02-VERIFICATION.md` now exists and records all ACCT/ETA/MENU rows with command-backed evidence.
