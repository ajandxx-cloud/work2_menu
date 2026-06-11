# Claim Checklist

- Artifact status: `blocked`
- Claim ready: `false`
- Pilot claim ready: `false`
- Formal claim ready: `false`

## Allowed Now

- [robust_time_window_menu_framework] Robust time-window service-menu framework is implemented - Core menu logic, contracts, paired replay schema, and artifact gates exist in the repository.
- [robust_pruning_modes] Robust ETA pruning and soft-penalty modes are available - The method can describe hard, calibrated, interval-overlap, chance-constraint, soft-penalty, and none modes.
- [solver_auditability] Exact-small and greedy-large menu construction is auditable - Solver diagnostics record fallback, gap, overlap, candidate count, and build-time metadata.
- [paired_replay_contracts] Paired replay contracts are defined for fair policy comparisons - Study contracts require shared traces, seeds, checkpoints, pricing, and HGS settings.
- [artifact_status_transparency] Artifact status and blockers are reported transparently - Phase 4 status artifacts expose blocked, incomplete, placeholder, checkpoint, and provenance state.

## Conditional

- [pilot_formal_effect_sizes] Pilot/formal effect-size conclusions - blocked; requires claim_ready plus pilot or formal claim readiness.
- [formal_policy_ranking] Formal recommended-policy ranking - blocked; requires formal_claim_ready.
- [diagnostic_result_tables] Diagnostic/status tables and blocked-artifact explanations - allowed; requires artifact status available.

## Blocked

- [universal_dominance] Robust menu universally dominates all baselines - Universal dominance is stronger than any bounded simulation or diagnostic artifact can support.
- [real_passenger_validation] The choice model is validated on real passenger behavior - No external survey or revealed-preference validation is part of v1.
- [no_filter_operational_recommendation] No-filter is recommended as an operational policy - no_filter_diagnostic is a diagnostic upper bound or stress test, not an operational recommendation.
- [full_dynamic_exact_optimality] The full dynamic DRT system is solved exactly - Exact enumeration is limited to small menu candidate sets, with greedy fallback for larger sets.
- [empirical_superiority] Robust menu empirically improves profit, acceptance, or opt-out versus baselines - Current artifact status is not claim-ready.
- [pilot_formal_completed] Pilot/formal experiments are complete and support manuscript results - Current artifact status is blocked or incomplete.

## Blockers

- `missing_checkpoint_file`: Required checkpoint file is unavailable; refusing random-weight evidence. Path: `outputs/shared_training/work2_robust_menu/pilot/supervised_ml.pt`.
- `formal_skipped`: Formal evidence was skipped for this Phase 4 run; formal claim readiness is false.
