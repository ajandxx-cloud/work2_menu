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

## Candidate, Menu, And Label Contract

Work 2 uses explicit public and internal naming so model comparisons do not
mix candidate availability with model quality:

- Public `K` / `--max_candidates` is the maximum number of meeting-point
  candidates retained for a request. It does not count the home option.
- Public `L` / `--menu_k` is the number of displayed meeting-point offers.
  The home option is always shown outside `L`, so the displayed choice set has
  `1 + L` options when enough meeting points are feasible.
- Internal neural tensors use `candidate_slots = K + 1`, with home at row 0
  and meeting-point candidates at rows 1..K.
- The centralized option feature schema is six columns in this order:
  `walk_distance`, `predicted_ivt`, `remaining_capacity`,
  `distance_to_destination`, `option_type`, `arrival_time`.
- `option_type = 1.0` only marks the home row. Meeting-point rows use
  `option_type = 0.0`.
- Requests with fewer than `K` feasible meeting points pad the remaining rows.
  Padding is excluded by `option_mask`; it must not be inferred from all-zero
  feature values.
- Requests with zero feasible meeting points remain valid home-only examples:
  row 0 is mask-true and all meeting-point rows are mask-false.
- Supervised learned menu models train on candidate-specific true insertion-cost
  labels aligned to the same rows. Padding labels are harmless fillers and are
  excluded from Huber/MSE losses by `option_mask`.

Guardrail: this contract does not rewrite Work 1 pricing, MNL passenger choice,
or HGS/Hygese route-cost core logic. Those components are only called through
their existing evaluation paths.

## Phase 4 Pilot Model-Comparison Contract

Phase 4 is a focused pilot for whether CNN-SetMenuNet has useful effect under
the locked Phase 3 menu semantics. It is not formal evidence, not a robustness
sweep, and not an exhaustive baseline census.

The core Phase 4 pilot methods are:

- `Nearest-L`
- `Cost-L heuristic`
- `CNN-Menu`
- `MLP-Menu`
- `CNN-SetMenuNet`
- `Oracle Menu`

Optional supplementary baselines are `Home only`, `Full-candidate CNN`, and
`SetMenuNet`. They may be added when already stable, but they must not block the
core six-method pilot.

The default pilot budget is exactly `seed0`, `seed1`, and `seed2`, with
`max_episodes = 80` for training and `eval_episodes = 20` for frozen
evaluation. Later formal evidence may use the project default
`150-300/50` episode budget and additional seeds; those formal settings are not
silently folded into this pilot.

All core methods must share the same split ids, `train_split`, `test_split`,
request traces, candidate pool, candidate order, option masks, and
candidate-specific insertion-cost labels. Public `K=10` remains the number of
meeting-point candidates. Public `L=3` remains the number of displayed
meeting-point offers, with home always shown outside `L`.

If one core method fails, Phase 4 may continue only as a documented partial
pilot when `CNN-SetMenuNet`, `Cost-L heuristic`, `Oracle Menu`, and at least one
of `CNN-Menu` or `MLP-Menu` run successfully. Missing core methods must be
listed as caveats in the study summary and verification report.

This pilot continues to treat Work 1 pricing, MNL passenger choice, and
HGS/Hygese route-cost evaluation as fixed dependencies. The comparison changes
menu policy/model inputs and selection logic only; it does not rewrite those
core dependent modules.

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
