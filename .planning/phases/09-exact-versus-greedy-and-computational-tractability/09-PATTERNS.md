---
phase: 09
phase_name: Exact Versus Greedy And Computational Tractability
status: complete
generated: 2026-06-16T10:09:40+08:00
---

# Phase 9 Pattern Map

## Manifest Pattern

Closest analogs:

- `work2_coding/Experiments/studies/phase8_sensitivity_menu_k.yaml`
- `work2_coding/Experiments/studies/phase8_sensitivity_eta_filter.yaml`
- `work2_coding/Experiments/studies/phase9_dspo_family_validation.yaml`

Reusable patterns:

- Keep active runtime under `work2_coding/Experiments/studies/`.
- Use `schema_version`, `name`, `tier`, `run_mode`, `description`,
  `shared_checkpoint`, `base_args`, `splits`, `policies`, `paired_fields`,
  `varied_fields`, and `output_schema`.
- Use extra top-level split metadata such as `sensitivity_axis`,
  `sensitivity_value`, and `paired_group_id` without putting those keys in
  parser args. Phase 9 can mirror this pattern with `solver_scale_variant`,
  `solver_scale_value`, and `paired_group_id`.
- Use known policy tags from `Src.policy_adapters.py`; avoid new policy tags
  unless the adapter registry is intentionally extended.

## Test Pattern

Closest analogs:

- `work2_coding/scripts/test_phase8_sensitivity_contracts.py`
- `work2_coding/scripts/test_phase9_dspo_family_validation.py`
- `work2_coding/scripts/test_policy_fairness_contract.py`
- `work2_coding/scripts/test_robust_menu_logic.py`

Reusable patterns:

- Tests are executable Python scripts with direct assertions and a `main()`.
- Manifest contract tests should load real YAML through
  `Src.experiment_contracts.load_manifest`.
- Paired-group tests can group split metadata and assert shared replay fields.
- Runtime logic tests can instantiate lightweight `DSPO_Menu` objects and call
  menu-selection helpers directly.

## Artifact And Summary Pattern

Closest analogs:

- `work2_coding/Src/sensitivity_analysis.py`
- `work2_coding/scripts/build_phase8_sensitivity_artifacts.py`
- `work2_coding/scripts/build_phase8_sensitivity_summary.py`
- `work2_coding/Src/artifact_builder.py`
- `.planning/results/SENSITIVITY_SUMMARY.md`

Reusable patterns:

- Keep generated row/artifact paths as source of truth.
- Use sidecar metadata JSON for generated tables and figures.
- Preserve `claim_ready=false` and diagnostic/provisional status in artifact
  metadata and planning summaries.
- Use synthetic temporary fixtures in tests for artifact builders.

## Runtime Diagnostic Pattern

Closest analogs:

- `work2_coding/Src/Algorithms/DSPO_Menu.py`
- `work2_coding/Src/study_execution.py`
- `work2_coding/Src/paired_replay.py`

Reusable patterns:

- Solver diagnostics originate in `DSPO_Menu.last_policy_diagnostic`.
- `study_execution.py` aggregates diagnostics across replay steps.
- `paired_replay.py` owns normalized-row schema and field ordering.
- Add row fields only when the value is needed by paper-facing or
  planning-facing artifacts and can be generated, blocked, or failed without
  hand editing rows.
