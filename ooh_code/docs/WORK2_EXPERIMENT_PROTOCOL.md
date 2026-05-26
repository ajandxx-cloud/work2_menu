# Work2 Experiment Protocol

## Objective

Evaluate two linked questions under a common paired design:

1. whether ETA-based candidate filtering distorts the displayed feasible set
2. whether relaxing that filtering improves profit and user-facing outcomes relative to exhaustive full display

The paired comparison is made under:

- the same trained bundle predictor
- the same replayed request traces
- the same random seed and simulator setup

The main experiment metric is:

`net_profit = charge_revenue - discount_cost - travel_cost - service_cost - failure_cost`

The protocol now separates:

- `RC` as a mechanism benchmark
- `Austin` and `Seattle` as impact benchmarks

## Fair-Comparison Design

### Phase A: shared predictor training

Train one shared bundle predictor with:

- `menu_policy = offer_all_feasible_bundles`

This phase is not used to compare display policies. It exists only to produce a common predictor for work2 evaluation.

### Phase B: frozen evaluation

Load the same shared predictor and replay the same request traces while changing only the display policy:

- `offer_all_feasible_bundles`
- `menu_optimization`
- internal heuristic menu baselines, when required by a study manifest
- ablated menu-optimization variants, when required by a study manifest

Frozen evaluation runs with:

- `eval_only = True`
- `freeze_learning = True`

This avoids mixing policy effects with model-training differences.

## Public Entry Points

Use:

- `python run_menu_compare.py`
- `python scripts/run_study.py --study <name>`

The low-level runner can:

1. train and compare in one command
2. skip training and compare from an existing checkpoint
3. run a `menu_k` robustness sweep for `menu_optimization`

The project-level study runner can:

1. load a versioned YAML manifest
2. train one shared predictor per split pair
3. reuse frozen evaluation across all compared variants
4. save normalized split and aggregate summaries under `outputs/studies/`

## Saved Outputs

The comparison directory stores:

- `request_traces.npy`
- `full_display_episode_metrics.json`
- `menu_optimization_episode_metrics.json`
- `full_display_summary.json`
- `menu_optimization_summary.json`
- `paired_summary.json`
- `robustness_menu_k_summary.json`

`paired_summary.json` reports the main paired comparison, including:

- mean net-profit gap: `menu - full`
- mean total-cost gap
- net-profit win rate
- 95% confidence-interval half width
- whether optimized menus remain no larger than full display on average

Project-level study runs additionally store:

- `manifest_snapshot.yaml`
- split-level `request_traces.npy`
- per-variant summary JSON files
- `normalized_rows.json`
- `aggregate_variant_summary.json`
- `study_summary.json`

Policy-comparison rows also expose lightweight interpretation fields:

- `study_role`
- `acceptance_rate`
- `is_behavior_non_degenerate`
