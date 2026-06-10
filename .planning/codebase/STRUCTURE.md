# Codebase Structure

**Analysis Date:** 2026-06-09

**last_mapped_commit:** `37b20aa`

## Directory Layout

```text
2.paper_2_menu optimization-7分_trE/
├── AGENTS.md                         # Project instructions and current GSD context
├── CLAUDE.md                         # Claude-facing project instructions
├── .planning/                        # GSD planning state and codebase maps
├── .claude/                          # Claude commands and worktree metadata
├── ooh_code/                         # Runnable Work2 research package
│   ├── README.md                     # Public workflow overview
│   ├── requirements.txt              # Python dependency manifest
│   ├── run_menu_compare.py           # Low-level direct comparison runner
│   ├── Src/                          # Runtime, orchestration, algorithms, utilities
│   │   ├── parser.py                 # CLI/runtime argument schema
│   │   ├── config.py                 # Config factory and environment construction
│   │   ├── work2_runtime.py          # Solver train/evaluate loop
│   │   ├── research_pipeline.py      # Manifest-driven study/suite orchestration
│   │   ├── Algorithms/               # Policy/model algorithm classes
│   │   └── Utils/                    # Neural models, math, data, logging helpers
│   ├── Environments/OOH/             # Simulator, choice model, routing utilities, data
│   ├── experiments/                  # Study and suite YAML manifests
│   ├── scripts/                      # CLI wrappers, artifact builders, checks, tests
│   ├── artifacts/                    # Generated paper snapshots/tables/figures
│   ├── manuscript/                   # LaTeX manuscript source and build directory
│   ├── docs/                         # Protocol and implementation-boundary docs
│   └── outputs/                      # Raw local generated runs and checkpoints
├── artifacts/work2_cnn_setmenunet/   # Root-level standard Work2 artifact bundle
├── qi_wei/                           # External notes/literature context
├── 2025.9.11-pom_big price/          # External notes/literature context
├── 实验讨论5.26.md                   # Research discussion notes
└── learning meeting point.docx       # Research notes document
```

## Directory Purposes

**`ooh_code/`:**
- Purpose: Runnable Python and LaTeX research package for Work2 service-menu optimization.
- Contains: `ooh_code/run_menu_compare.py`, `ooh_code/Src/`, `ooh_code/Environments/`, `ooh_code/experiments/`, `ooh_code/scripts/`, `ooh_code/artifacts/`, `ooh_code/manuscript/`.
- Key files: `ooh_code/README.md`, `ooh_code/requirements.txt`.

**`ooh_code/Src/`:**
- Purpose: Main Python package layer for runtime config, solver loops, research pipeline orchestration, algorithms, and utilities.
- Contains: `ooh_code/Src/parser.py`, `ooh_code/Src/config.py`, `ooh_code/Src/work2_runtime.py`, `ooh_code/Src/research_pipeline.py`, `ooh_code/Src/Algorithms/`, `ooh_code/Src/Utils/`.
- Key files: `ooh_code/Src/research_pipeline.py`, `ooh_code/Src/config.py`, `ooh_code/Src/parser.py`.

**`ooh_code/Src/Algorithms/`:**
- Purpose: Stateful model/policy classes used by `Config.algo`.
- Contains: `ooh_code/Src/Algorithms/Agent.py`, `ooh_code/Src/Algorithms/DSPO.py`, `ooh_code/Src/Algorithms/CNN_SetMenu.py`, `ooh_code/Src/Algorithms/MLP_SetMenu.py`.
- Key files: `ooh_code/Src/Algorithms/DSPO.py`, `ooh_code/Src/Algorithms/CNN_SetMenu.py`, `ooh_code/Src/Algorithms/MLP_SetMenu.py`.
- Constraint: `ooh_code/Src/Algorithms/DSPO_Menu.py` is imported by current code but is absent from this directory.

**`ooh_code/Src/Utils/`:**
- Purpose: Shared neural networks, option feature construction, replay memory, data loading, HGS helpers, logging, and numerical fallbacks.
- Contains: `ooh_code/Src/Utils/Predictors.py`, `ooh_code/Src/Utils/CNNSetMenuNet.py`, `ooh_code/Src/Utils/SetMenuNet.py`, `ooh_code/Src/Utils/MLPMenuNet.py`, `ooh_code/Src/Utils/option_features.py`, `ooh_code/Src/Utils/MathUtils.py`, `ooh_code/Src/Utils/Utils.py`.
- Key files: `ooh_code/Src/Utils/option_features.py`, `ooh_code/Src/Utils/CNNSetMenuNet.py`, `ooh_code/Src/Utils/Utils.py`.

**`ooh_code/Environments/OOH/`:**
- Purpose: Demand-responsive transit simulator, customer choice, routing utilities, domain containers, and bundled benchmark data.
- Contains: `ooh_code/Environments/OOH/Parcelpoint_py.py`, `ooh_code/Environments/OOH/customerchoice.py`, `ooh_code/Environments/OOH/env_utils.py`, `ooh_code/Environments/OOH/containers.py`, `ooh_code/Environments/OOH/Amazon_data/`, `ooh_code/Environments/OOH/HombergerGehring_data/`.
- Key files: `ooh_code/Environments/OOH/Parcelpoint_py.py`, `ooh_code/Environments/OOH/customerchoice.py`, `ooh_code/Environments/OOH/containers.py`.

**`ooh_code/experiments/`:**
- Purpose: Declarative experiment program.
- Contains: single studies under `ooh_code/experiments/studies/` and bundles under `ooh_code/experiments/suites/`.
- Key files: `ooh_code/experiments/studies/work2_main.yaml`, `ooh_code/experiments/studies/smoke_work2_main.yaml`, `ooh_code/experiments/studies/rc_main_optout.yaml`, `ooh_code/experiments/suites/work2_robustness.yaml`, `ooh_code/experiments/suites/rc_paper_v1.yaml`.

**`ooh_code/scripts/`:**
- Purpose: User-facing command wrappers, artifact generators, manuscript checks, extraction scripts, smoke scripts, and direct test scripts.
- Contains: `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, `ooh_code/scripts/build_manuscript.py`, `ooh_code/scripts/check_manuscript.py`, `ooh_code/scripts/test_*.py`, `ooh_code/scripts/extract_phase*_results.py`.
- Key files: `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, `ooh_code/scripts/build_manuscript.py`.

**`ooh_code/artifacts/`:**
- Purpose: Generated lightweight paper artifacts inside the runnable project.
- Contains: `ooh_code/artifacts/results_snapshot/`, `ooh_code/artifacts/tables/`, `ooh_code/artifacts/figures/`, `ooh_code/artifacts/README.md`.
- Key files: `ooh_code/artifacts/RESULTS_SUMMARY.md` when generated, plus generated files under the three artifact subdirectories.

**`artifacts/work2_cnn_setmenunet/`:**
- Purpose: Root-level standard artifact bundle mirrored by `ooh_code/scripts/build_artifacts.py`.
- Contains: `artifacts/work2_cnn_setmenunet/results_snapshot/`, `artifacts/work2_cnn_setmenunet/tables/`, `artifacts/work2_cnn_setmenunet/figures/`, `artifacts/work2_cnn_setmenunet/diagnostics/`.
- Key files: Generated from `ooh_code/scripts/build_artifacts.py`.

**`ooh_code/manuscript/`:**
- Purpose: LaTeX paper source and build output.
- Contains: `ooh_code/manuscript/main.tex`, `ooh_code/manuscript/references.bib`, `ooh_code/manuscript/sections/`, `ooh_code/manuscript/build/`.
- Key files: `ooh_code/manuscript/main.tex`, `ooh_code/manuscript/sections/*.tex`, `ooh_code/manuscript/README.md`.

**`ooh_code/outputs/`:**
- Purpose: Raw local experiment outputs and checkpoints.
- Contains: `ooh_code/outputs/studies/`, `ooh_code/outputs/shared_training/`, `ooh_code/outputs/menu_compare/`, and phase-specific local run directories.
- Key files: `study_summary.json`, `normalized_rows.json`, `aggregate_variant_summary.csv`, `request_traces.npy`, checkpoint files generated under nested run directories.

**`ooh_code/docs/`:**
- Purpose: Human-readable workflow, protocol, and boundary documentation.
- Contains: `ooh_code/docs/WORK2_EXPERIMENT_PROTOCOL.md`, `ooh_code/docs/WORK2_IMPLEMENTATION_BOUNDARIES.md`, `ooh_code/docs/RESEARCH_PROJECT_WORKFLOW.md`.
- Key files: `ooh_code/docs/WORK2_EXPERIMENT_PROTOCOL.md`, `ooh_code/docs/WORK2_IMPLEMENTATION_BOUNDARIES.md`.

**`.planning/codebase/`:**
- Purpose: GSD codebase intelligence documents consumed by planning and execution workflows.
- Contains: `.planning/codebase/ARCHITECTURE.md`, `.planning/codebase/STRUCTURE.md`, and other focus maps when generated.
- Key files: `.planning/codebase/ARCHITECTURE.md`, `.planning/codebase/STRUCTURE.md`.

## Key File Locations

**Entry Points:**
- `ooh_code/run_menu_compare.py`: Low-level direct train/evaluate comparison and menu-size robustness runner.
- `ooh_code/scripts/run_study.py`: Study/suite manifest CLI.
- `ooh_code/scripts/build_artifacts.py`: Artifact snapshot, table, figure, and summary generator.
- `ooh_code/scripts/build_manuscript.py`: Artifact refresh plus LaTeX compile wrapper.
- `ooh_code/scripts/run_baseline_smoke.py`: Smoke runner for baseline verification.

**Configuration:**
- `ooh_code/Src/parser.py`: CLI defaults, choices, and derived aliases.
- `ooh_code/Src/config.py`: Output paths, data loading, environment construction, algorithm selection, device, optimizer.
- `ooh_code/requirements.txt`: Python dependency manifest.
- `ooh_code/experiments/studies/*.yaml`: Single executable study definitions.
- `ooh_code/experiments/suites/*.yaml`: Study bundle definitions.

**Core Logic:**
- `ooh_code/Src/research_pipeline.py`: Manifest execution, checkpoint reuse, request trace generation, normalized rows, suite summaries.
- `ooh_code/Src/work2_runtime.py`: Solver train loop and model/environment episode interaction.
- `ooh_code/Src/Algorithms/DSPO.py`: Legacy predictor, insertion-cost learning, pricing, and HGS final re-optimization.
- `ooh_code/Src/Algorithms/CNN_SetMenu.py`: CNN-SetMenuNet intended algorithm subclass.
- `ooh_code/Src/Algorithms/MLP_SetMenu.py`: MLP-Menu intended baseline subclass.
- `ooh_code/Environments/OOH/Parcelpoint_py.py`: Simulator reset, request trace replay, step transition, menu logging.
- `ooh_code/Environments/OOH/customerchoice.py`: MNL choice with outside option.
- `ooh_code/Environments/OOH/env_utils.py`: Cheapest insertion and HGS utilities.
- `ooh_code/Environments/OOH/containers.py`: Domain dataclasses and the `MenuOffer` contract.
- `ooh_code/Src/Utils/option_features.py`: Six-column option feature schema.
- `ooh_code/Src/Utils/CNNSetMenuNet.py`: CNN plus set-attention model.

**Testing and Checks:**
- `ooh_code/scripts/test_option_features.py`: Option tensor checks.
- `ooh_code/scripts/test_cnnsetmenunet.py`: CNN-SetMenuNet checks.
- `ooh_code/scripts/test_mlp_setmenu.py`: MLP-Menu checks.
- `ooh_code/scripts/test_work2_main_manifest.py`: Work2 manifest checks.
- `ooh_code/scripts/test_work2_formal_artifacts.py`: Artifact builder checks.
- `ooh_code/scripts/check_manuscript.py`: Manuscript validation helper.

**Documentation:**
- `ooh_code/README.md`: Public workflows and repository layers.
- `ooh_code/experiments/README.md`: Study and suite manifest conventions.
- `ooh_code/docs/WORK2_EXPERIMENT_PROTOCOL.md`: Experiment protocol and fair-comparison contract.
- `ooh_code/docs/WORK2_IMPLEMENTATION_BOUNDARIES.md`: Scope, route-cost realization, and non-goals.
- `ooh_code/manuscript/README.md`: Manuscript workflow.
- `ooh_code/artifacts/README.md`: Artifact workflow.

## Naming Conventions

**Files:**
- Use lowercase snake_case for new Python workflow modules: `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, `ooh_code/Src/research_pipeline.py`.
- Preserve legacy mixed-case algorithm/model files under `ooh_code/Src/Algorithms/` and `ooh_code/Src/Utils/`: `ooh_code/Src/Algorithms/CNN_SetMenu.py`, `ooh_code/Src/Utils/CNNSetMenuNet.py`, `ooh_code/Src/Utils/MLPMenuNet.py`.
- Use lowercase descriptive YAML names under `ooh_code/experiments/studies/` and `ooh_code/experiments/suites/`: `work2_main.yaml`, `work2_robustness.yaml`, `smoke_work2_main.yaml`.
- Use lowercase manuscript section files under `ooh_code/manuscript/sections/`: `ooh_code/manuscript/sections/*.tex`.
- Use generated artifact names that include the study or metric under `ooh_code/artifacts/results_snapshot/`, `ooh_code/artifacts/tables/`, and `ooh_code/artifacts/figures/`.

**Directories:**
- Preserve legacy capitalization for Python package directories: `ooh_code/Src/`, `ooh_code/Src/Algorithms/`, `ooh_code/Src/Utils/`, `ooh_code/Environments/OOH/`.
- Use lowercase plural workflow directories for declarative inputs and outputs: `ooh_code/experiments/`, `ooh_code/scripts/`, `ooh_code/artifacts/`, `ooh_code/manuscript/`, `ooh_code/outputs/`.
- Keep bundled benchmark data under provider/instance subdirectories: `ooh_code/Environments/OOH/Amazon_data/Austin/`, `ooh_code/Environments/OOH/HombergerGehring_data/RC/`.

**Manifest Fields:**
- Use `name`, `title`, `type`, `description`, `reference_tag`, `reference_policy`, `base_args`, `policies`, and `splits` for policy studies in `ooh_code/experiments/studies/*.yaml`.
- Use `args_overrides` inside policy or split entries when changing parser-controlled behavior in `ooh_code/experiments/studies/*.yaml`.
- Use `members` for suite composition in `ooh_code/experiments/suites/*.yaml`.

## Where to Add New Code

**New Study:**
- Primary code: `ooh_code/experiments/studies/<study_name>.yaml`
- Suite membership: `ooh_code/experiments/suites/<suite_name>.yaml`
- Validation checks: `ooh_code/scripts/test_<study_name>_manifest.py` when adding nontrivial manifest rules.
- Artifact support: `ooh_code/scripts/build_artifacts.py` when the study needs new table, figure, or prose outputs.

**New Policy Variant:**
- Manifest entry: `ooh_code/experiments/studies/<study_name>.yaml` under `policies`.
- Parser option: `ooh_code/Src/parser.py` when a new runtime knob is needed.
- Policy implementation: the menu algorithm base in `ooh_code/Src/Algorithms/` once `ooh_code/Src/Algorithms/DSPO_Menu.py` is restored or replaced.
- Metrics: `ooh_code/run_menu_compare.py` for episode metrics and `ooh_code/Src/research_pipeline.py` for normalized row columns.

**New Algorithm or Model:**
- Algorithm implementation: `ooh_code/Src/Algorithms/<ModelName>.py`
- Neural module: `ooh_code/Src/Utils/<ModelName>.py`
- Algorithm selection: `ooh_code/Src/config.py`
- CLI/model switch: `ooh_code/Src/parser.py`
- Smoke tests: `ooh_code/scripts/test_<model_name>.py`

**New Simulator Behavior:**
- Core transition logic: `ooh_code/Environments/OOH/Parcelpoint_py.py`
- Choice semantics: `ooh_code/Environments/OOH/customerchoice.py`
- Route or capacity helper: `ooh_code/Environments/OOH/env_utils.py`
- Domain object shape: `ooh_code/Environments/OOH/containers.py`
- Add behavior carefully because `ooh_code/run_menu_compare.py` metric extraction consumes simulator logs.

**New Metric:**
- Collection: `ooh_code/run_menu_compare.py` in `extract_menu_metrics()`, `summarize_episode()`, or `aggregate_episode_metrics()`.
- Normalized schema: `ooh_code/Src/research_pipeline.py` in `SUMMARY_NUMERIC_KEYS` and `CSV_FIELD_ORDER`.
- Artifact rendering: `ooh_code/scripts/build_artifacts.py`.
- Tests/checks: relevant `ooh_code/scripts/test_*artifact*.py` file.

**New Artifact:**
- Build logic: `ooh_code/scripts/build_artifacts.py`.
- Project artifact output: `ooh_code/artifacts/results_snapshot/`, `ooh_code/artifacts/tables/`, or `ooh_code/artifacts/figures/`.
- Standard mirrored output: `artifacts/work2_cnn_setmenunet/results_snapshot/`, `artifacts/work2_cnn_setmenunet/tables/`, `artifacts/work2_cnn_setmenunet/figures/`, or `artifacts/work2_cnn_setmenunet/diagnostics/`.
- Manuscript inclusion: `ooh_code/manuscript/main.tex` or `ooh_code/manuscript/sections/*.tex`.

**New Documentation:**
- Workflow/protocol docs: `ooh_code/docs/`.
- Experiment-manifest docs: `ooh_code/experiments/README.md`.
- Artifact docs: `ooh_code/artifacts/README.md`.
- Manuscript docs: `ooh_code/manuscript/README.md`.
- Planning/codebase maps: `.planning/codebase/`.

**Utilities:**
- Shared research orchestration helpers: `ooh_code/Src/research_pipeline.py`.
- Shared neural/data/math helpers: `ooh_code/Src/Utils/`.
- Script-local helpers: keep inside the relevant file under `ooh_code/scripts/` unless reused by multiple scripts.

## Special Directories

**`ooh_code/outputs/`:**
- Purpose: Raw experiment state, checkpoints, request traces, and run summaries.
- Generated: Yes.
- Committed: No for heavy/local run state; treat as local experiment output.

**`ooh_code/artifacts/`:**
- Purpose: Lightweight generated paper artifacts consumed by manuscript and review workflows.
- Generated: Yes, through `ooh_code/scripts/build_artifacts.py`.
- Committed: Yes when artifacts are part of the publication evidence bundle.

**`artifacts/work2_cnn_setmenunet/`:**
- Purpose: Root-level standard artifact bundle mirrored from the project artifact builder.
- Generated: Yes, through `ooh_code/scripts/build_artifacts.py`.
- Committed: Yes when current result snapshots are intended for review.

**`ooh_code/manuscript/build/`:**
- Purpose: LaTeX build products and `build_status.json`.
- Generated: Yes, through `ooh_code/scripts/build_manuscript.py`.
- Committed: No for transient compiler outputs unless explicitly required.

**`ooh_code/Environments/OOH/Amazon_data/` and `ooh_code/Environments/OOH/HombergerGehring_data/`:**
- Purpose: Bundled benchmark coordinate, adjacency, service-time, and distance data.
- Generated: No.
- Committed: Yes.

**`.planning/`:**
- Purpose: GSD workflow state, codebase maps, phase plans, and orchestration metadata.
- Generated: Yes.
- Committed: Project-dependent; do not remove or rewrite unrelated planning files.

**`.claude/`:**
- Purpose: Claude command and worktree metadata.
- Generated: Yes.
- Committed: Project-dependent; avoid editing unless the task targets Claude workflow files.

---

*Structure analysis: 2026-06-09*
