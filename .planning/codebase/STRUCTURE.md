# Codebase Structure

**Analysis Date:** 2026-05-27

## Directory Layout

```text
[project-root]/
├── .git/                         # Git metadata
├── .planning/                    # GSD planning metadata and generated codebase maps
├── 2025.9.11-pom_big price/      # Literature/reference PDFs and notes for publication context
├── ooh_code/                     # Executable many-to-one DRT menu optimization research project
│   ├── Src/                      # Scientific runtime, config, algorithms, utilities, study pipeline
│   ├── Environments/             # OOH simulator, domain containers, benchmark data
│   ├── experiments/              # YAML study and suite manifests
│   ├── scripts/                  # CLI wrappers for studies, artifacts, manuscript, extraction
│   ├── artifacts/                # Committed generated tables, figures, snapshots, summaries
│   ├── manuscript/               # LaTeX paper source and compiled/build outputs
│   ├── docs/                     # Research workflow and experiment protocol docs
│   ├── outputs/                  # Raw generated study/comparison/checkpoint outputs
│   ├── run_menu_compare.py       # Low-level direct experiment runner
│   ├── requirements.txt          # Python dependencies
│   └── README.md                 # Project overview and public workflows
├── qi_wei/                       # Reference PDF directory
├── learning meeting point.docx   # Research note document
└── 实验讨论5.26.md                # Research discussion notes
```

## Directory Purposes

**`.planning/`:**
- Purpose: Stores GSD workflow configuration and generated codebase intelligence.
- Contains: `.planning/config.json`, `.planning/codebase/ARCHITECTURE.md`, `.planning/codebase/STRUCTURE.md`
- Key files: `.planning/config.json`, `.planning/codebase/ARCHITECTURE.md`, `.planning/codebase/STRUCTURE.md`

**`ooh_code/`:**
- Purpose: Main executable research project for service-menu optimization in many-to-one demand-responsive transit.
- Contains: Scientific code, data, manifests, scripts, outputs, artifacts, and manuscript.
- Key files: `ooh_code/README.md`, `ooh_code/run_menu_compare.py`, `ooh_code/requirements.txt`, `ooh_code/LICENSE.md`

**`ooh_code/Src/`:**
- Purpose: Core Python package for configuration, CLI argument schema, solver runtime, and project-level study orchestration.
- Contains: `config.py`, `parser.py`, `work2_runtime.py`, `research_pipeline.py`, `Algorithms/`, `Utils/`
- Key files: `ooh_code/Src/config.py`, `ooh_code/Src/parser.py`, `ooh_code/Src/work2_runtime.py`, `ooh_code/Src/research_pipeline.py`

**`ooh_code/Src/Algorithms/`:**
- Purpose: Algorithm implementations and checkpoint-capable agent abstraction.
- Contains: Base agent, base DSPO algorithm, and work2 menu optimization algorithm.
- Key files: `ooh_code/Src/Algorithms/Agent.py`, `ooh_code/Src/Algorithms/DSPO.py`, `ooh_code/Src/Algorithms/DSPO_Menu.py`

**`ooh_code/Src/Utils/`:**
- Purpose: Shared model, math, logging, data-loading, routing, feature, and memory-buffer utilities.
- Contains: Predictor classes, Lambert W fallback, data loading, HGS route helpers, training curves, replay memory.
- Key files: `ooh_code/Src/Utils/Predictors.py`, `ooh_code/Src/Utils/MathUtils.py`, `ooh_code/Src/Utils/Utils.py`

**`ooh_code/Environments/`:**
- Purpose: Environment package namespace.
- Contains: `OOH/` simulator implementation and data.
- Key files: `ooh_code/Environments/__init__.py`

**`ooh_code/Environments/OOH/`:**
- Purpose: Out-of-home meeting-point simulator, customer choice model, route utilities, and domain containers.
- Contains: Python simulator modules plus benchmark data directories.
- Key files: `ooh_code/Environments/OOH/Parcelpoint_py.py`, `ooh_code/Environments/OOH/customerchoice.py`, `ooh_code/Environments/OOH/env_utils.py`, `ooh_code/Environments/OOH/containers.py`

**`ooh_code/Environments/OOH/HombergerGehring_data/`:**
- Purpose: Bundled C/R/RC benchmark coordinate data for mechanism experiments.
- Contains: `C/`, `R/`, `RC/` coordinate files and `README.md`.
- Key files: `ooh_code/Environments/OOH/HombergerGehring_data/RC/RC_90_0_coords.txt`, `ooh_code/Environments/OOH/HombergerGehring_data/RC/RC_90_1_coords.txt`, `ooh_code/Environments/OOH/HombergerGehring_data/README.md`

**`ooh_code/Environments/OOH/Amazon_data/`:**
- Purpose: Bundled Amazon Last Mile Austin/Seattle data for impact benchmarks.
- Contains: City subdirectories with coordinate, distance-matrix, and adjacency files.
- Key files: `ooh_code/Environments/OOH/Amazon_data/Austin/Austin_700_0_coords.txt`, `ooh_code/Environments/OOH/Amazon_data/Austin/Austin_700_0_dist_matrix.txt`, `ooh_code/Environments/OOH/Amazon_data/Seattle/Seattle_700_0_coords.txt`

**`ooh_code/experiments/`:**
- Purpose: Declarative experiment program for the paper.
- Contains: `studies/`, `suites/`, `README.md`
- Key files: `ooh_code/experiments/README.md`

**`ooh_code/experiments/studies/`:**
- Purpose: Single executable study manifests.
- Contains: Policy comparisons, robustness sweeps, ablations, sensitivity studies, smoke tests.
- Key files: `ooh_code/experiments/studies/rc_main.yaml`, `ooh_code/experiments/studies/rc_main_optout.yaml`, `ooh_code/experiments/studies/austin_main.yaml`, `ooh_code/experiments/studies/seattle_main.yaml`, `ooh_code/experiments/studies/smoke_rc.yaml`

**`ooh_code/experiments/suites/`:**
- Purpose: Named bundles of study manifests used by paper pipelines.
- Contains: Suite YAML files whose `members` list references `experiments/studies/`.
- Key files: `ooh_code/experiments/suites/rc_paper_v1.yaml`, `ooh_code/experiments/suites/phase31_uptake_menu_value.yaml`, `ooh_code/experiments/suites/phase34_outside_option_scan.yaml`

**`ooh_code/scripts/`:**
- Purpose: Public and support CLI scripts.
- Contains: Study runner, artifact builder, manuscript builder, manuscript checker, bootstrap scripts, historical extraction scripts.
- Key files: `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, `ooh_code/scripts/build_manuscript.py`, `ooh_code/scripts/check_manuscript.py`, `ooh_code/scripts/bootstrap_rc.py`, `ooh_code/scripts/bootstrap_amazon.py`

**`ooh_code/artifacts/`:**
- Purpose: Lightweight committed research outputs derived from normalized study summaries.
- Contains: `results_snapshot/`, `tables/`, `figures/`, `RESULTS_SUMMARY.md`, `README.md`
- Key files: `ooh_code/artifacts/README.md`, `ooh_code/artifacts/RESULTS_SUMMARY.md`

**`ooh_code/artifacts/results_snapshot/`:**
- Purpose: JSON/CSV snapshots for latest built study scopes.
- Contains: Per-study and per-suite summary JSON/CSV files.
- Key files: `ooh_code/artifacts/results_snapshot/rc_main_summary.json`, `ooh_code/artifacts/results_snapshot/rc_main_rows.csv`, `ooh_code/artifacts/results_snapshot/rc_paper_v1_summary.json`

**`ooh_code/artifacts/tables/`:**
- Purpose: Paper-ready CSV and LaTeX tables.
- Contains: Generated `.csv` and `.tex` tables for main studies, robustness checks, ablations, sensitivity studies, and diagnostics.
- Key files: `ooh_code/artifacts/tables/rc_main_summary.tex`, `ooh_code/artifacts/tables/rc_main_summary.csv`, `ooh_code/artifacts/tables/city_impact_summary.tex`, `ooh_code/artifacts/tables/profit_decomposition_summary.tex`

**`ooh_code/artifacts/figures/`:**
- Purpose: Generated publication figures.
- Contains: PNG plots for net profit, gaps, ablations, robustness, and city benchmarks.
- Key files: `ooh_code/artifacts/figures/rc_main_net_profit.png`, `ooh_code/artifacts/figures/rc_main_gap_vs_full.png`, `ooh_code/artifacts/figures/austin_main_net_profit.png`, `ooh_code/artifacts/figures/seattle_main_net_profit.png`

**`ooh_code/manuscript/`:**
- Purpose: English LaTeX paper source and compiled outputs.
- Contains: `main.tex`, section files, bibliography, build outputs, current PDF, manuscript notes.
- Key files: `ooh_code/manuscript/main.tex`, `ooh_code/manuscript/main.pdf`, `ooh_code/manuscript/references.bib`, `ooh_code/manuscript/README.md`

**`ooh_code/manuscript/sections/`:**
- Purpose: Section-level LaTeX source files included by `main.tex`.
- Contains: Abstract, introduction, related work, problem, method, experiments, results, managerial, limitations, conclusion, appendix.
- Key files: `ooh_code/manuscript/sections/abstract.tex`, `ooh_code/manuscript/sections/method.tex`, `ooh_code/manuscript/sections/experiments.tex`, `ooh_code/manuscript/sections/results.tex`, `ooh_code/manuscript/sections/appendix.tex`

**`ooh_code/manuscript/build/`:**
- Purpose: Generated LaTeX build output and manuscript build metadata.
- Contains: PDF/intermediate files and `build_status.json` when built through `scripts/build_manuscript.py`.
- Key files: `ooh_code/manuscript/build/main.pdf`, `ooh_code/manuscript/build/build_status.json`

**`ooh_code/docs/`:**
- Purpose: Project workflow, experiment protocol, and implementation-boundary documentation.
- Contains: Markdown reference docs for future implementation and paper work.
- Key files: `ooh_code/docs/RESEARCH_PROJECT_WORKFLOW.md`, `ooh_code/docs/WORK2_EXPERIMENT_PROTOCOL.md`, `ooh_code/docs/WORK2_IMPLEMENTATION_BOUNDARIES.md`

**`ooh_code/outputs/`:**
- Purpose: Raw generated outputs from direct comparisons, study runs, shared training, and phase extraction scripts.
- Contains: `menu_compare/`, `studies/`, `shared_training/`, `phase*/`, review text outputs.
- Key files: `ooh_code/outputs/menu_compare/*/paired_summary.json`, `ooh_code/outputs/studies/*/*/study_summary.json`, `ooh_code/outputs/shared_training/*/*/checkpoints/supervised_ml.pt`

**`2025.9.11-pom_big price/`:**
- Purpose: Publication reference material and paper notes related to pricing/capacity/control literature.
- Contains: PDF papers and `pom_品类优化三篇.txt`.
- Key files: `2025.9.11-pom_big price/pom_品类优化三篇.txt`

**`qi_wei/`:**
- Purpose: Additional literature reference directory.
- Contains: PDF reference article.
- Key files: `qi_wei/cao-qi-2022-stall-economy-the-value-of-mobility-in-retail-on-wheels.pdf`

## Key File Locations

**Entry Points:**
- `ooh_code/run_menu_compare.py`: Direct low-level train/evaluate comparison runner.
- `ooh_code/scripts/run_study.py`: Study/suite manifest runner.
- `ooh_code/scripts/build_artifacts.py`: Artifact generation entry point.
- `ooh_code/scripts/build_manuscript.py`: Artifact refresh plus LaTeX compile entry point.
- `ooh_code/scripts/check_manuscript.py`: LaTeX reference and artifact-path checker.
- `ooh_code/manuscript/main.tex`: Paper compilation entry point.

**Configuration:**
- `ooh_code/Src/parser.py`: CLI defaults, choices, and argument aliases.
- `ooh_code/Src/config.py`: Runtime config, output paths, data loading, environment construction, algorithm/device/optimizer selection.
- `ooh_code/requirements.txt`: Python dependency list.
- `.planning/config.json`: GSD planning configuration for the workspace.

**Core Logic:**
- `ooh_code/Src/work2_runtime.py`: Solver train loop and checkpoint-aware runtime.
- `ooh_code/Src/research_pipeline.py`: Manifest resolution, study/suite execution, normalized rows, CSV/JSON output.
- `ooh_code/Src/Algorithms/DSPO_Menu.py`: Work2 menu policy, pricing, exact/greedy selection, ETA filtering, predictor update.
- `ooh_code/Src/Algorithms/DSPO.py`: Base DSPO action, pricing, predictor, feature, and HGS route-cost logic.
- `ooh_code/Environments/OOH/Parcelpoint_py.py`: Simulator reset/step, request traces, menu logging, route updates.
- `ooh_code/Environments/OOH/customerchoice.py`: Customer menu choice and outside-option behavior.
- `ooh_code/Environments/OOH/env_utils.py`: Fleet/parcelpoint reset and HGS helper logic.
- `ooh_code/Environments/OOH/containers.py`: Domain dataclasses.

**Experiment Definitions:**
- `ooh_code/experiments/studies/rc_main.yaml`: RC main policy comparison.
- `ooh_code/experiments/studies/rc_main_optout.yaml`: Corrected outside-option RC benchmark.
- `ooh_code/experiments/studies/filtering_baselines.yaml`: ETA filtering baseline comparison.
- `ooh_code/experiments/studies/austin_main.yaml`: Austin impact benchmark.
- `ooh_code/experiments/studies/seattle_main.yaml`: Seattle impact benchmark.
- `ooh_code/experiments/studies/smoke_rc.yaml`: Minimal local verification study.
- `ooh_code/experiments/suites/rc_paper_v1.yaml`: Paper suite bundling RC studies.

**Data:**
- `ooh_code/Environments/OOH/HombergerGehring_data/RC/RC_90_0_coords.txt`: RC benchmark split.
- `ooh_code/Environments/OOH/HombergerGehring_data/C/C_90_0_coords.txt`: C benchmark split.
- `ooh_code/Environments/OOH/HombergerGehring_data/R/R_90_0_coords.txt`: R benchmark split.
- `ooh_code/Environments/OOH/Amazon_data/Austin/Austin_700_0_coords.txt`: Austin coordinates.
- `ooh_code/Environments/OOH/Amazon_data/Austin/Austin_700_0_dist_matrix.txt`: Austin distance matrix.
- `ooh_code/Environments/OOH/Amazon_data/Seattle/Seattle_700_0_coords.txt`: Seattle coordinates.
- `ooh_code/Environments/OOH/Amazon_data/Seattle/Seattle_700_0_dist_matrix.txt`: Seattle distance matrix.

**Outputs and Artifacts:**
- `ooh_code/outputs/studies/<study_name>/<run_id>/study_summary.json`: Normalized study summary output.
- `ooh_code/outputs/studies/<suite_name>/<run_id>/suite_summary.json`: Suite summary output.
- `ooh_code/outputs/menu_compare/<run_name>/<seed>/paired_summary.json`: Direct comparison paired summary.
- `ooh_code/outputs/shared_training/<run_name>/<seed>/checkpoints/supervised_ml.pt`: Shared predictor checkpoint.
- `ooh_code/artifacts/results_snapshot/*_summary.json`: Committed generated result snapshots.
- `ooh_code/artifacts/tables/*_summary.tex`: Generated LaTeX tables for the manuscript.
- `ooh_code/artifacts/figures/*.png`: Generated manuscript figures.
- `ooh_code/artifacts/RESULTS_SUMMARY.md`: Generated prose result summary.

**Manuscript:**
- `ooh_code/manuscript/main.tex`: LaTeX root and artifact macros.
- `ooh_code/manuscript/sections/results.tex`: Results narrative.
- `ooh_code/manuscript/sections/method.tex`: Method narrative.
- `ooh_code/manuscript/sections/experiments.tex`: Experiment design narrative.
- `ooh_code/manuscript/references.bib`: Bibliography.
- `ooh_code/manuscript/main.pdf`: Current compiled manuscript PDF.

**Documentation:**
- `ooh_code/README.md`: Project overview, public commands, study program, output locations.
- `ooh_code/docs/RESEARCH_PROJECT_WORKFLOW.md`: Layered workflow overview.
- `ooh_code/docs/WORK2_EXPERIMENT_PROTOCOL.md`: Fair-comparison design and saved output schema.
- `ooh_code/docs/WORK2_IMPLEMENTATION_BOUNDARIES.md`: Scientific implementation boundaries.
- `ooh_code/experiments/README.md`: Manifest layout and public experiment commands.
- `ooh_code/artifacts/README.md`: Artifact directory contract.
- `ooh_code/manuscript/README.md`: Manuscript build workflow.

## Naming Conventions

**Files:**
- Python modules use lowercase or legacy CamelCase/snake-mixed names: `ooh_code/Src/config.py`, `ooh_code/Src/research_pipeline.py`, `ooh_code/Src/Algorithms/DSPO_Menu.py`, `ooh_code/Environments/OOH/Parcelpoint_py.py`.
- Study manifests use snake_case names matching study names: `ooh_code/experiments/studies/rc_main.yaml`, `ooh_code/experiments/studies/phase32_operational_baselines.yaml`.
- Suite manifests use suite names and list member studies: `ooh_code/experiments/suites/rc_paper_v1.yaml`.
- Generated summary files use `<study_or_artifact>_summary.{json,csv,tex}`: `ooh_code/artifacts/results_snapshot/rc_main_summary.json`, `ooh_code/artifacts/tables/rc_main_summary.tex`.
- Generated row files use `<study>_rows.csv`: `ooh_code/artifacts/results_snapshot/austin_main_rows.csv`.
- Generated policy metric JSON files use `<variant>_episode_metrics.json`, `<variant>_summary.json`, and `<variant>_paired_vs_<reference>.json` under split outputs.
- Manuscript section files use lowercase topic names: `ooh_code/manuscript/sections/introduction.tex`, `ooh_code/manuscript/sections/limitations.tex`.

**Directories:**
- Study run directories follow `ooh_code/outputs/studies/<study_name>/<run_id>/`.
- Split outputs follow `ooh_code/outputs/studies/<study_name>/<run_id>/splits/<split_id>/`.
- Shared training outputs follow `ooh_code/outputs/shared_training/<run_name>/<seed>/`.
- Direct compare outputs follow `ooh_code/outputs/menu_compare/<run_name>/<seed>/`.
- Artifact subdirectories are fixed as `ooh_code/artifacts/results_snapshot/`, `ooh_code/artifacts/tables/`, and `ooh_code/artifacts/figures/`.
- Benchmark data is grouped by provider/instance: `ooh_code/Environments/OOH/HombergerGehring_data/RC/`, `ooh_code/Environments/OOH/Amazon_data/Austin/`.

## Where to Add New Code

**New Study Manifest:**
- Primary code: `ooh_code/experiments/studies/<study_name>.yaml`
- Suite membership: `ooh_code/experiments/suites/<suite_name>.yaml`
- Tests/verifications: Run through `ooh_code/scripts/run_study.py` with a small `eval_episodes` or add a smoke manifest under `ooh_code/experiments/studies/`.

**New Study Type or Manifest Field:**
- Primary code: `ooh_code/Src/research_pipeline.py`
- CLI argument mapping: `ooh_code/Src/parser.py`
- Artifact support: `ooh_code/scripts/build_artifacts.py`
- Tests/verifications: Use `ooh_code/experiments/studies/smoke_rc.yaml` or a new smoke study manifest.

**New Menu Policy:**
- Primary code: `ooh_code/Src/Algorithms/DSPO_Menu.py`
- CLI choice: `ooh_code/Src/parser.py`
- Manifest usage: `ooh_code/experiments/studies/*.yaml`
- Metrics/artifacts: `ooh_code/run_menu_compare.py` for low-level metric extraction, `ooh_code/scripts/build_artifacts.py` for paper-facing summaries.

**New Simulator Behavior:**
- Primary code: `ooh_code/Environments/OOH/Parcelpoint_py.py`
- Domain structures: `ooh_code/Environments/OOH/containers.py`
- Choice behavior: `ooh_code/Environments/OOH/customerchoice.py`
- Route/fleet utilities: `ooh_code/Environments/OOH/env_utils.py`

**New Predictor or Model Architecture:**
- Primary code: `ooh_code/Src/Utils/Predictors.py`
- Algorithm wiring: `ooh_code/Src/Algorithms/DSPO.py`, `ooh_code/Src/Algorithms/DSPO_Menu.py`
- Config/CLI flags: `ooh_code/Src/parser.py`, `ooh_code/Src/config.py`

**New Benchmark Dataset:**
- Data files: `ooh_code/Environments/OOH/<DatasetName>_data/`
- Loader changes: `ooh_code/Src/Utils/Utils.py`
- CLI choices: `ooh_code/Src/parser.py`
- Study manifests: `ooh_code/experiments/studies/<dataset>_main.yaml`

**New Artifact Table or Figure:**
- Primary code: `ooh_code/scripts/build_artifacts.py`
- Output locations: `ooh_code/artifacts/tables/`, `ooh_code/artifacts/figures/`, `ooh_code/artifacts/results_snapshot/`
- Manuscript reference: `ooh_code/manuscript/sections/*.tex`
- Verification: `python scripts/check_manuscript.py` from `ooh_code/`.

**New Manuscript Section or Paper Text:**
- Section file: `ooh_code/manuscript/sections/<section>.tex`
- Inclusion point: `ooh_code/manuscript/main.tex`
- Bibliography: `ooh_code/manuscript/references.bib`
- Build: `ooh_code/scripts/build_manuscript.py`

**Utilities:**
- Shared research/runtime helpers: `ooh_code/Src/Utils/`
- Pipeline file IO helpers: `ooh_code/Src/research_pipeline.py`
- One-off migration/extraction scripts: `ooh_code/scripts/`

## Special Directories

**`ooh_code/outputs/`:**
- Purpose: Raw generated outputs, checkpoints, and historical phase results.
- Generated: Yes
- Committed: Mixed/unclear from filesystem state; treat as generated working output and avoid making paper edits directly here.

**`ooh_code/artifacts/`:**
- Purpose: Lightweight committed outputs consumed by the manuscript.
- Generated: Yes, by `ooh_code/scripts/build_artifacts.py`
- Committed: Yes, intended as public paper artifacts.

**`ooh_code/manuscript/build/`:**
- Purpose: LaTeX build products and build metadata.
- Generated: Yes, by `ooh_code/scripts/build_manuscript.py` or LaTeX tools.
- Committed: Mixed/unclear from filesystem state; treat as build output unless project policy says otherwise.

**`ooh_code/**/__pycache__/`:**
- Purpose: Python bytecode cache directories.
- Generated: Yes
- Committed: No, should be treated as generated interpreter cache.

**`ooh_code/Environments/OOH/*_data/`:**
- Purpose: Bundled benchmark input data used by configured experiments.
- Generated: No for normal workflows
- Committed: Yes, required for reproducible local runs.

**`ooh_code/.planning/`:**
- Purpose: Existing planning/milestone metadata inside the research project subdirectory.
- Generated: Yes
- Committed: Project-dependent; keep separate from root `.planning/codebase/` maps unless orchestrator requests migration.

**`ooh_code/.claude/`:**
- Purpose: Tooling metadata for another agent/workflow system.
- Generated: Yes
- Committed: Project-dependent; do not use for runtime code placement.

**`2025.9.11-pom_big price/` and `qi_wei/`:**
- Purpose: Literature/reference materials outside executable code.
- Generated: No
- Committed: Project-dependent; do not place Python runtime files here.

---

*Structure analysis: 2026-05-27*
