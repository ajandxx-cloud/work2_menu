---
phase: 03-formal-rc-evidence-pipeline-repair-and-completion
plan: 03-02
status: completed_candidate_rows_with_diagnostic_failure_history
created: 2026-06-15T12:05:00+08:00
timezone: Asia/Shanghai
---

# Formal Failure Diagnosis

## Selected Formal Source Run

Phase 3 selects the latest completed formal run as the source run for Phase 4
diagnosis:

```text
work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a
```

This run is complete and comparable as candidate formal evidence, but remains
diagnostic rather than claim-ready because readiness is blocked by dirty git and
the current manifest hash differs from the run snapshot.

| Field | Value |
| --- | --- |
| Execution status | `completed` |
| Row count | `35` |
| Split count | `5` |
| Policies per split | `7` |
| Checkpoint statuses | `loaded` |
| Placeholder-only rows | `0` |
| Failed rows | `0` |
| Non-empty error metadata | `0` |
| Uptake regimes | `low`, `medium` |
| Run manifest hash | `c672286a45342771a92d28d14f8f7e85fd20dea9a5f89ab50a8aca375e54296c` |
| Current manifest hash observed during Plan 03-02 | `5028ef16cb808d423a957664451e1013e2a81408c9d173a999684a1682774ae8` |

The selected run covers the seven mainline policies for each formal split:

1. `mainline_no_menu`
2. `mainline_fixed_menu`
3. `mainline_random_menu`
4. `mainline_optimized_m`
5. `mainline_optimized_mw`
6. `mainline_optimized_fixed_window`
7. `mainline_optimized_adaptive`

The five split IDs are:

1. `formal_mainline_low_seed0`
2. `formal_mainline_low_seed1`
3. `formal_mainline_medium_seed0`
4. `formal_mainline_medium_seed1`
5. `formal_mainline_medium_seed2`

## Row Comparability Audit

`normalized_rows.json` contains exactly `5 x 7 = 35` rows.

| Check | Result |
| --- | --- |
| `status` | `completed` for all 35 rows |
| `execution_status` | `completed` for all 35 rows |
| `placeholder_only` | `false` for all 35 rows |
| `checkpoint_load_status` | `loaded` for all 35 rows |
| `error_type` / `error_message` | empty for all 35 rows |
| Seven unique policies per split | passed |
| Paired fields consistent within each split | passed |
| Opt-out separate from home/meeting-point acceptance | verified by focused tests and row fields `count_opted_out`, `count_accepted_home`, `count_accepted_meeting_point` |

Because the row comparability audit passed, Phase 3 did not rerun formal replay.
Rerunning while dirty git persists would create another diagnostic run, not a
claim-ready source.

## Preserved Failed Run

The prior failed run remains part of the evidence trail:

```text
work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T031927Z-fca35a73
```

| Field | Value |
| --- | --- |
| Execution status | `failed` |
| Row count | `35` |
| Completed rows | `28` |
| Failed rows | `7` |
| Blocker code | `actual_replay_failed_rows` |
| Error type | `UnboundLocalError` |
| Example error | `cannot access local variable 'coords' where it is not associated with a value` |
| Checkpoint statuses | `loaded` |

The failed run includes structured failed rows with `status`,
`execution_status`, `error_type`, and `error_message`. No rows were edited or
hidden.

## Verification

Run from `work2_coding/`:

| Command | Result |
| --- | --- |
| `python scripts/test_optout_accounting.py` | PASS: 7 opt-out accounting tests |
| `python scripts/test_paired_replay_contract.py` | PASS: 12 paired replay contract tests |
| `python scripts/test_policy_fairness_contract.py` | PASS: 15 policy fairness contract tests |
| `python scripts/test_study_execution_status.py` | PASS: 9 study execution status tests |
| `python scripts/test_formal_replay_enablement.py` | PASS: 4 formal replay enablement tests |

## Claim Boundary

The selected completed run is scientifically usable for Phase 4 diagnosis of
formal rows. It is not claim-ready while readiness remains blocked and artifact
gates have not promoted it. Phase 4 should diagnose effect sizes and paired
differences from the selected run without treating dirty-git diagnostic status
as empirical superiority support.
