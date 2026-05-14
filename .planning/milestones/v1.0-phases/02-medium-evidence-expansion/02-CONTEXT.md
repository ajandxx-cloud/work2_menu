# Phase 2: Medium Evidence Expansion - Context

**Gathered:** 2026-05-14
**Status:** Ready for planning

<domain>
## Phase Boundary

Plan and execute medium-scope evidence additions: run existing MNL sensitivity manifests, expand filter validity diagnostics with bias, add 2-3 DRT operational baselines. Addresses reviewer Critical 2, Major 2, and Major 3. This phase creates new experiment data, implements new baseline policies, and adds manuscript placeholders for the new evidence.

</domain>

<decisions>
## Implementation Decisions

### MNL Sensitivity Scope
- Run existing Phase 27 MNL manifests as-is (low/medium/high) via `python scripts/run_study.py --study phase27_mnl_sensitivity`
- No separate outside-option strength sweep — implicitly covered by base_util and home_pickup_utility
- Add new results subsection "[Behavioral stress test] MNL Parameter Sensitivity" with summary table showing key metrics across 3 regimes
- Update existing `mnl_sensitivity_summary.tex` table in-place by re-running `build_artifacts.py` after Phase 27 completes

### Filter Validity Diagnostics Depth
- No P50/P90/P95 percentile errors — too much pipeline modification for medium scope
- Add bias (mean signed error) to existing filter_validity table — computed from existing episode-level data
- Keep FN pruning rate only — true confusion matrix requires ground-truth feasibility labels not logged
- No high-uptake filter validity — low-uptake diagnostic is the most relevant for this scope

### Operational Baseline Selection
- Add 3 new DRT baselines: (1) insertion-cost greedy using real-time cheapestInsertionCosts, (2) minimum-lateness ranking by pickup time deviation, (3) random-top-k as floor baseline
- Implement new strategies in `DSPO_Menu.py` `get_action_menu` method, following existing pattern of `nearest_heuristic` and `top_k_cheapest` (~20 lines each)
- Run new baselines in RC low-uptake regime only (6 split pairs), using existing manifest infrastructure

### Evidence-to-Manuscript Integration
- MNL sensitivity summary table goes to main results section (stress-test tier)
- Filter-validity expansion and operational baseline results go to supplementary appendix tables
- Phase 2 adds only structural placeholders and table references in results.tex — Phase 3 handles full narrative
- Critical 2 (MNL/outside-option calibration) gets a direct evidence response paragraph in results.tex

### Claude's Discretion
- Exact bias computation method and formatting
- New strategy implementation details (sorting keys, tie-breaking)
- Manifest naming and structure details
- Artifact table column formatting

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `ooh_code/experiments/suites/phase27_mnl_sensitivity.yaml` — bundles 3 MNL manifests (low/medium/high)
- `ooh_code/experiments/studies/phase27_mnl_sensitivity_{low,medium,high}.yaml` — individual study manifests
- `ooh_code/outputs/phase28/filter_validity.json` — 4-row filter validity data
- `ooh_code/artifacts/tables/filter_validity_summary.tex` — existing filter validity table
- `ooh_code/artifacts/tables/mnl_sensitivity_summary.tex` — existing MNL table (stale data)
- `ooh_code/artifacts/tables/main_policy_summary.tex` — all 7 strategy results

### Established Patterns
- Study manifests follow YAML schema: name, type, base_args, policies, splits
- Strategies are registered in `DSPO_Menu.py` `get_action_menu` with policy name string matching
- `build_artifacts.py` converts pipeline output to .tex/.csv tables
- `research_pipeline.py` tracks `SUMMARY_NUMERIC_KEYS` for standardized output
- CLI parameters controlled via `Src/parser.py` with `--` prefix flags

### Integration Points
- New strategies → `DSPO_Menu.py` line ~808 `get_action_menu` method
- Strategy registration → `Src/parser.py` line ~111 policy choice list
- New manifests → `ooh_code/experiments/studies/` directory
- New tables → `ooh_code/artifacts/tables/` directory, consumed by manuscript
- Manuscript placeholders → `ooh_code/manuscript/sections/results.tex`

</code_context>

<specifics>
## Specific Ideas

- The Phase 27 MNL manifests are complete and ready to run — no manifest creation needed
- Insertion-cost greedy can leverage the existing `cheapestInsertionCosts` method in `DSPO_Menu.py` (inherited via DSPO class)
- Minimum-lateness is a simpler variant of `nearest_heuristic` — just sort by time_deviation alone
- Random-top-k provides a floor baseline that makes other strategies' performance interpretable
- The existing `filter_validity_summary.tex` table needs a "Bias" column added — this is a table-formatting change in `build_artifacts.py`

</specifics>

<deferred>
## Deferred Ideas

- P50/P90/P95 percentile error tracking — requires pipeline modification, deferred to future work
- High-uptake regime filter validity — re-running with uptake parameters adds complexity
- Explicit outside-option utility parameter scan — requires code changes to customerchoice.py
- Full DRT-dispatch baselines (vehicle routing without menu optimization) — out of scope for this paper

</deferred>
