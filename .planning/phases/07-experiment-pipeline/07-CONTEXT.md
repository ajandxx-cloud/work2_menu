# Phase 7: Experiment Pipeline - Context

**Gathered:** 2026-05-30
**Status:** Ready for planning

<domain>
## Phase Boundary

Verify and validate the complete 6-method experiment pipeline end-to-end. The infrastructure is already ~90% built (manifests, metric keys, artifact builder, parser/config routing). This phase runs the pipeline, fixes any runtime gaps, and confirms paper-ready output.

Specifically this phase delivers:
- Verified `smoke_work2_main` run completing all 6 methods without error
- Verified `build_artifacts.py` generating 3 LaTeX tables + 1 figure for Work 2
- Confirmed metric population (prediction/ranking/operational/passenger) for all methods
- Any code fixes needed to close runtime gaps

Not in scope: Running the full-scale experiment (Phase 8), new model architectures, new metrics beyond what's already declared.

</domain>

<decisions>
## Implementation Decisions

### Smoke Test Strategy
- **D-01:** Run-then-fix approach — run `smoke_work2_main` immediately, fix errors as they appear
- **D-02:** Full 6-method run in one pass via `run_study.py` (not split by method category)

### Oracle Menu Variant
- **D-03:** Oracle menu in `work2_main.yaml` uses `menu_model: cnn_setmenu` with `init_theta_cnn: 0.0` and `cool_theta_cnn: 0.0` + `menu_use_oracle_eta: true`. This aligns with Phase 1 decision D-03 (oracle merged into cost_l_heuristic with theta=0). Verify at runtime.

### Table/Figure Output
- **D-04:** Use the existing `build_work2_results_artifacts` output as-is (3 tables + 1 figure). Fix only if runtime issues are found.

### Claude's Discretion
- Specific error fixes during smoke test run
- Whether to adjust artifact output format
- Whether to split smoke test if full run fails catastrophically
- Exact metric gap resolution strategy

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Experiment Manifests
- `ooh_code/experiments/studies/work2_main.yaml` — 6-method comparison manifest (K=10, L=3, 3 seeds, 80 train/20 test)
- `ooh_code/experiments/studies/smoke_work2_main.yaml` — Reduced-scale smoke test manifest

### Metrics Pipeline
- `ooh_code/Src/research_pipeline.py` — SUMMARY_NUMERIC_KEYS (lines 35-104), CSV_FIELD_ORDER (lines 106-135), aggregate_rows (lines 511-547), execute_study_manifest
- `ooh_code/run_menu_compare.py` — extract_menu_metrics (lines 136-375), aggregate_episode_metrics (lines 407-472), prediction helpers: _spearman_rank_correlation, _ndcg_at_k

### Artifact Generation
- `ooh_code/scripts/build_artifacts.py` — build_work2_results_artifacts (lines 1467-1577), _WORK2_METHOD_ORDER, _WORK2_LEARNING_METHODS

### Config/Parser Routing
- `ooh_code/Src/parser.py` — --menu_model (lines 129-133), finalize_args routing (lines 494-515)
- `ooh_code/Src/config.py` — algo routing (lines 100-108)

### Algorithm Classes
- `ooh_code/Src/Algorithms/CNN_SetMenu.py` — CNN_SetMenu(DSPO_Menu) subclass
- `ooh_code/Src/Algorithms/MLP_SetMenu.py` — MLP_SetMenu(DSPO_Menu) subclass
- `ooh_code/Src/Algorithms/DSPO_Menu.py` — Base menu algorithm with all policy dispatch

### Prior Phase Context
- `.planning/phases/01-baseline-consolidation/01-CONTEXT.md` — 4 baselines, oracle/cost_l merge
- `.planning/phases/05-algorithm-integration/05-CONTEXT.md` — CNN_SetMenu integration decisions
- `.planning/REQUIREMENTS.md` — EXPR-01 through EXPR-07 requirements
- `.planning/ROADMAP.md` — Phase 7 goal and success criteria

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets (Already Built)
- **SUMMARY_NUMERIC_KEYS**: 68 numeric keys declared including 7 Work 2 prediction/ranking keys (cost_pred_mae, cost_pred_rmse, spearman_cost_ranking, top_L_overlap, ndcg_at_L, menu_regret, cost_pred_n_samples)
- **extract_menu_metrics**: Computes all prediction/ranking metrics per step (MAE, RMSE, Spearman, Top-L overlap, NDCG@L, menu regret)
- **build_work2_results_artifacts**: Generates 3 LaTeX tables (prediction accuracy, operational, menu regret) + net profit bar chart
- **variant_display_label**: Maps cnn_menu, setmenu_net, cnn_setmenu_net, oracle_menu tags to display names
- **_WORK2_METHOD_ORDER**: oracle_menu, cnn_setmenu_net, setmenu_net, cnn_menu, cost_L, nearest_L

### Established Patterns
- Study pipeline: manifest → train shared model → generate traces → run variants → aggregate rows → write summary
- Policy_compare study type: trains reference model, replays traces across policy variants
- Artifact routing: study name matching (work2_main, smoke_work2_main) → Work 2 artifact builder
- Metric flow: per-step → per-episode → per-split → cross-split aggregate

### Integration Points
- `research_pipeline.py` executes `run_study.py` flow: reads manifest, calls `run_menu_compare` per variant
- `build_artifacts.py` reads study_summary.json from outputs/studies/{study_name}/
- Manifest variant tags must match _WORK2_METHOD_ORDER for correct table ordering

</code_context>

<specifics>
## Specific Ideas

- The smoke test uses heavily reduced parameters (1 train ep, 1 test ep, 2 vehicles, capacity 2). Some metrics may be degenerate (e.g., Spearman with < 3 data points). This is expected and acceptable — the smoke test verifies pipeline connectivity, not metric quality.
- The oracle_menu variant may not emit `predicted_cost` metadata in the same way as CNN-SetMenuNet. If prediction table shows `--` for oracle, this is acceptable since oracle uses true costs (theta=0).
- Potential gap: `menu_use_oracle_eta` flag must be registered in parser.py for the manifest override to work.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 07-experiment-pipeline*
*Context gathered: 2026-05-30*
