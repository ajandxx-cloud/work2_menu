<!-- refreshed: 2026-05-27 -->
# Architecture

**Analysis Date:** 2026-05-27

## System Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                 Publication / Research Workspace             │
├──────────────────┬──────────────────┬───────────────────────┤
│  Research Code   │ Experiment Specs │   Manuscript/Artifacts │
│  `ooh_code/`     │ `ooh_code/experiments/` │ `ooh_code/manuscript/` │
└────────┬─────────┴────────┬─────────┴──────────┬────────────┘
         │                  │                     │
         ▼                  ▼                     ▼
┌─────────────────────────────────────────────────────────────┐
│             Study Orchestration and Artifact Pipeline        │
│ `ooh_code/scripts/`, `ooh_code/Src/research_pipeline.py`     │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│          Scientific Core: Solver, Menu Policy, Simulator     │
│ `ooh_code/run_menu_compare.py`, `ooh_code/Src/`,             │
│ `ooh_code/Environments/OOH/`                                │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│       Data, Raw Outputs, Committed Artifacts, Paper PDF       │
│ `ooh_code/Environments/OOH/*_data/`, `ooh_code/outputs/`,    │
│ `ooh_code/artifacts/`, `ooh_code/manuscript/main.pdf`        │
└─────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

| Component | Responsibility | File |
|-----------|----------------|------|
| Low-level menu comparison runner | Trains or loads one shared predictor, replays request traces, evaluates full display and menu policies, and writes JSON comparison outputs. | `ooh_code/run_menu_compare.py` |
| Study pipeline | Resolves YAML study/suite manifests, trains/reuses checkpoints per split, runs frozen policy variants, normalizes rows, and writes study summaries. | `ooh_code/Src/research_pipeline.py` |
| CLI study runner | Public command wrapper around the study pipeline, including resume and force-retrain flags. | `ooh_code/scripts/run_study.py` |
| Artifact builder | Converts normalized study summaries into committed JSON/CSV snapshots, LaTeX tables, PNG figures, and prose summaries. | `ooh_code/scripts/build_artifacts.py` |
| Manuscript builder | Rebuilds artifacts, detects LaTeX tooling, compiles `main.tex`, and writes build metadata. | `ooh_code/scripts/build_manuscript.py` |
| Runtime solver | Owns train/evaluate loops over environment episodes and delegates actions/updates to the configured algorithm. | `ooh_code/Src/work2_runtime.py` |
| Configuration factory | Parses args into paths, data, environments, algorithm class, optimizer, and device configuration. | `ooh_code/Src/config.py` |
| CLI argument schema | Defines experiment, data, menu-policy, pricing, simulator, and model hyperparameters. | `ooh_code/Src/parser.py` |
| Menu optimization algorithm | Builds service bundles, predicts cost/ETA/IVT, prices menus, selects exact/greedy/heuristic menus, and updates predictor training buffers. | `ooh_code/Src/Algorithms/DSPO_Menu.py` |
| Base DSPO algorithm | Provides legacy offer/pricing policies, neural predictor training, HGS final re-optimization, and feature extraction. | `ooh_code/Src/Algorithms/DSPO.py` |
| Agent base class | Handles module initialization, save/load, train/eval mode, and generic gradient helpers. | `ooh_code/Src/Algorithms/Agent.py` |
| OOH simulator | Generates customers, applies menu choices, updates fleet/routes/capacity, logs menu decisions, and supports frozen request traces. | `ooh_code/Environments/OOH/Parcelpoint_py.py` |
| Domain containers | Defines dataclasses for locations, vehicles, customers, service bundles, and displayed menu offers. | `ooh_code/Environments/OOH/containers.py` |
| Customer choice model | Implements Gumbel-noise multinomial menu choice with an outside option. | `ooh_code/Environments/OOH/customerchoice.py` |
| Environment utilities | Handles fleet reset, parcel-point capacity reset, cheapest insertion, and HGS route re-optimization. | `ooh_code/Environments/OOH/env_utils.py` |
| Research data | Stores bundled RC/C/R and Amazon Austin/Seattle benchmark coordinates, adjacency, and distance matrices. | `ooh_code/Environments/OOH/HombergerGehring_data/`, `ooh_code/Environments/OOH/Amazon_data/` |
| Experiment manifests | Declarative study and suite definitions for reproducible policy comparisons, sweeps, and ablations. | `ooh_code/experiments/studies/*.yaml`, `ooh_code/experiments/suites/*.yaml` |
| Paper artifacts | Stores committed snapshots, tables, figures, and `RESULTS_SUMMARY.md` generated from normalized outputs. | `ooh_code/artifacts/` |
| Manuscript | LaTeX paper source with generated artifact inclusion macros and section files. | `ooh_code/manuscript/main.tex`, `ooh_code/manuscript/sections/*.tex` |
| Notes/literature | Non-executable publication context and reference material outside the research code package. | `2025.9.11-pom_big price/`, `qi_wei/`, `实验讨论5.26.md`, `learning meeting point.docx` |

## Pattern Overview

**Overall:** Layered research pipeline with declarative experiment manifests over an imperative scientific simulator.

**Key Characteristics:**
- Use `ooh_code/experiments/studies/*.yaml` and `ooh_code/experiments/suites/*.yaml` as the source of truth for study design; avoid encoding paper study variants only in scripts.
- Keep policy-evaluation fairness centralized: train one shared predictor with `offer_all_feasible_bundles`, then evaluate variants with `eval_only=True`, `freeze_learning=True`, and replayed traces via `ooh_code/Src/research_pipeline.py`.
- Generate paper-facing tables and figures from normalized summaries under `ooh_code/outputs/studies/`; do not manually edit generated files under `ooh_code/artifacts/`.
- Treat `ooh_code/Src/Algorithms/DSPO_Menu.py` and `ooh_code/Environments/OOH/Parcelpoint_py.py` as the coupled scientific core. Menu offers produced by the algorithm must remain compatible with simulator choice and logging.

## Layers

**Workspace Layer:**
- Purpose: Holds the executable research project plus publication notes, literature, planning metadata, and discussion files.
- Location: `.`
- Contains: `ooh_code/`, `2025.9.11-pom_big price/`, `qi_wei/`, `.planning/`, `实验讨论5.26.md`, `learning meeting point.docx`
- Depends on: Local filesystem only.
- Used by: Planning agents and the author workflow.

**Research Project Layer:**
- Purpose: Provides the runnable many-to-one DRT menu optimization project.
- Location: `ooh_code/`
- Contains: `README.md`, `requirements.txt`, `run_menu_compare.py`, `Src/`, `Environments/`, `experiments/`, `scripts/`, `artifacts/`, `manuscript/`, `outputs/`, `docs/`
- Depends on: Python runtime, PyTorch, NumPy, pandas/matplotlib/YAML stack, `hygese`, optional LaTeX tooling.
- Used by: All experiment, artifact, and manuscript workflows.

**Entry-Point Layer:**
- Purpose: Exposes command-line workflows for direct comparison, manifest execution, artifact generation, manuscript compilation, and legacy extraction tasks.
- Location: `ooh_code/run_menu_compare.py`, `ooh_code/scripts/`
- Contains: `scripts/run_study.py`, `scripts/build_artifacts.py`, `scripts/build_manuscript.py`, `scripts/check_manuscript.py`, `scripts/bootstrap_*.py`, `scripts/extract_phase*_results.py`
- Depends on: `ooh_code/Src/research_pipeline.py`, `ooh_code/Src/parser.py`, `ooh_code/Src/config.py`, `ooh_code/run_menu_compare.py`
- Used by: Public workflows documented in `ooh_code/README.md` and `ooh_code/docs/RESEARCH_PROJECT_WORKFLOW.md`.

**Experiment Specification Layer:**
- Purpose: Describes studies, suites, split pairs, policy variants, behavior gates, and headline variants.
- Location: `ooh_code/experiments/`
- Contains: `experiments/studies/rc_main.yaml`, `experiments/studies/austin_main.yaml`, `experiments/studies/seattle_main.yaml`, `experiments/studies/rc_main_optout.yaml`, `experiments/suites/rc_paper_v1.yaml`, `experiments/suites/phase31_uptake_menu_value.yaml`
- Depends on: Field names consumed by `ooh_code/Src/research_pipeline.py`.
- Used by: `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`.

**Orchestration Layer:**
- Purpose: Resolves manifests, expands variants, trains/reuses shared checkpoints, generates request traces, executes variants, aggregates rows, and saves summary schemas.
- Location: `ooh_code/Src/research_pipeline.py`
- Contains: Manifest IO, study execution, suite execution, CSV/JSON writers, run-id generation, normalized row aggregation.
- Depends on: `ooh_code/Src/parser.py`, `ooh_code/Src/config.py`, `ooh_code/Src/work2_runtime.py`, `ooh_code/run_menu_compare.py`.
- Used by: `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, `ooh_code/scripts/build_manuscript.py`.

**Scientific Runtime Layer:**
- Purpose: Executes training/evaluation episodes and computes low-level comparison metrics.
- Location: `ooh_code/run_menu_compare.py`, `ooh_code/Src/work2_runtime.py`
- Contains: `Solver`, `evaluate_policy`, `summarize_episode`, `aggregate_episode_metrics`, `paired_summary`, checkpoint handling.
- Depends on: `ooh_code/Src/config.py`, `ooh_code/Src/Algorithms/DSPO_Menu.py`, `ooh_code/Environments/OOH/Parcelpoint_py.py`.
- Used by: Orchestration layer and direct low-level runner.

**Algorithm Layer:**
- Purpose: Implements policy construction, model prediction, pricing, menu selection, and learning updates.
- Location: `ooh_code/Src/Algorithms/`
- Contains: `Agent.py`, `DSPO.py`, `DSPO_Menu.py`
- Depends on: `ooh_code/Src/Utils/`, `ooh_code/Environments/OOH/containers.py`, PyTorch, NumPy, `hygese`.
- Used by: `Config.algo` in `ooh_code/Src/config.py` and `Solver.model` in `ooh_code/Src/work2_runtime.py`.

**Simulator Layer:**
- Purpose: Provides the environment state transition model, request traces, menu choice realization, fleet mutation, and route re-optimization hooks.
- Location: `ooh_code/Environments/OOH/`
- Contains: `Parcelpoint_py.py`, `customerchoice.py`, `env_utils.py`, `containers.py`, benchmark data directories.
- Depends on: `ooh_code/Src/Utils/Utils.py`, `hygese`, NumPy.
- Used by: `Config.build_environment()` in `ooh_code/Src/config.py`.

**Utility / Model Layer:**
- Purpose: Supplies predictors, math fallback, logging, data loading, HGS helpers, grid feature encoding, and replay memory.
- Location: `ooh_code/Src/Utils/`
- Contains: `Predictors.py`, `MathUtils.py`, `Utils.py`
- Depends on: PyTorch, NumPy, matplotlib, bundled data paths.
- Used by: `DSPO.py`, `DSPO_Menu.py`, `config.py`, and environment utilities.

**Output and Publication Layer:**
- Purpose: Separates heavy raw outputs from lightweight committed paper artifacts and manuscript source.
- Location: `ooh_code/outputs/`, `ooh_code/artifacts/`, `ooh_code/manuscript/`
- Contains: Raw run directories under `outputs/studies/` and `outputs/menu_compare/`; committed `artifacts/results_snapshot/`, `artifacts/tables/`, `artifacts/figures/`; LaTeX source under `manuscript/`.
- Depends on: `ooh_code/scripts/build_artifacts.py`, `ooh_code/scripts/build_manuscript.py`.
- Used by: Paper writing and review workflows.

## Data Flow

### Primary Request Path

1. A study or suite name enters through `python scripts/run_study.py --study <name>` (`ooh_code/scripts/run_study.py:12`).
2. The manifest is resolved from `ooh_code/experiments/studies/` or `ooh_code/experiments/suites/` (`ooh_code/Src/research_pipeline.py:265`).
3. `execute_study_manifest()` creates a run directory under `ooh_code/outputs/studies/<study>/<run_id>/`, snapshots the manifest, and expands reference plus variant specs (`ooh_code/Src/research_pipeline.py:643`).
4. `build_study_args()` maps manifest fields into parser/config arguments and split-specific train/test seeds (`ooh_code/Src/research_pipeline.py:322`).
5. `train_or_reuse_shared_model()` instantiates `Config`, `Solver`, and `DSPO_Menu`, then trains or reuses `supervised_ml.pt` under `ooh_code/outputs/shared_training/` (`ooh_code/Src/research_pipeline.py:350`).
6. `generate_request_traces()` freezes request traces from `Parcelpoint_py.generate_request_traces()` (`ooh_code/Src/research_pipeline.py:381`, `ooh_code/Environments/OOH/Parcelpoint_py.py:207`).
7. Each variant builds an evaluation solver with `build_eval_solver()` and calls `evaluate_policy()` using the same checkpoint and traces (`ooh_code/run_menu_compare.py:72`, `ooh_code/run_menu_compare.py:417`).
8. `DSPO_Menu.get_action_menu()` builds, selects, prices, and returns displayed `MenuOffer` objects for each request (`ooh_code/Src/Algorithms/DSPO_Menu.py:837`).
9. `Parcelpoint_py.step()` realizes customer choice, updates fleet/capacity, logs the menu decision, and returns `stats` plus `route_data` (`ooh_code/Environments/OOH/Parcelpoint_py.py:320`).
10. Episode and paired metrics are written as JSON/CSV under split directories and aggregated to `study_summary.json` (`ooh_code/Src/research_pipeline.py:690`).

### Direct Low-Level Comparison

1. `python run_menu_compare.py` parses CLI args and normalizes any shared checkpoint path (`ooh_code/run_menu_compare.py:472`).
2. If no checkpoint is supplied, it trains with `menu_policy="offer_all_feasible_bundles"` (`ooh_code/run_menu_compare.py:500`).
3. It generates frozen request traces and writes them to `ooh_code/outputs/menu_compare/<run_name>/<seed>/request_traces.npy` (`ooh_code/run_menu_compare.py:533`).
4. It evaluates `offer_all_feasible_bundles`, `menu_optimization`, and optional `menu_k` robustness values through `evaluate_policy()` (`ooh_code/run_menu_compare.py:536`).
5. It writes summary JSON files such as `full_display_summary.json`, `menu_optimization_summary.json`, `paired_summary.json`, and `robustness_menu_k_summary.json` (`ooh_code/run_menu_compare.py:554`).

### Artifact and Manuscript Flow

1. `python scripts/build_artifacts.py --study <name>` loads the latest study or suite summary (`ooh_code/scripts/build_artifacts.py:1789`).
2. It enriches rows with display labels, behavior flags, and headline variant filtering (`ooh_code/scripts/build_artifacts.py:214`).
3. It writes lightweight snapshots under `ooh_code/artifacts/results_snapshot/`, tables under `ooh_code/artifacts/tables/`, figures under `ooh_code/artifacts/figures/`, and a prose summary at `ooh_code/artifacts/RESULTS_SUMMARY.md` (`ooh_code/scripts/build_artifacts.py:20`, `ooh_code/scripts/build_artifacts.py:1800`).
4. `python scripts/build_manuscript.py` calls artifact generation first, then compiles `ooh_code/manuscript/main.tex` when `latexmk` or `pdflatex` is available (`ooh_code/scripts/build_manuscript.py:12`, `ooh_code/scripts/build_manuscript.py:86`).
5. `ooh_code/manuscript/main.tex` includes section files from `ooh_code/manuscript/sections/` and generated artifacts through `\ArtifactTable` and `\ArtifactFigure` macros (`ooh_code/manuscript/main.tex:16`, `ooh_code/manuscript/main.tex:31`, `ooh_code/manuscript/main.tex:56`).

**State Management:**
- Runtime state is episode-local in `Solver`, `DSPO_Menu`, and `Parcelpoint_py`; reset between episodes through `Solver.train()`, `evaluate_policy()`, and `Parcelpoint_py.reset()`.
- Reproducibility state is controlled by parser/config seeds, `Config.__init__()` NumPy/Torch seed setting, and simulator request/choice RNGs in `Parcelpoint_py.seed()`.
- Persistent state is filesystem-based: shared checkpoints under `ooh_code/outputs/shared_training/`, normalized study runs under `ooh_code/outputs/studies/`, direct compare outputs under `ooh_code/outputs/menu_compare/`, and committed paper artifacts under `ooh_code/artifacts/`.

## Key Abstractions

**Manifest:**
- Purpose: Declarative specification of a study or suite.
- Examples: `ooh_code/experiments/studies/rc_main.yaml`, `ooh_code/experiments/studies/austin_main.yaml`, `ooh_code/experiments/suites/rc_paper_v1.yaml`
- Pattern: YAML mapping consumed by `load_manifest()`, `variant_specs_for_manifest()`, and `execute_study_manifest()` in `ooh_code/Src/research_pipeline.py`.

**Config:**
- Purpose: Converts parser arguments into data, environment instances, algorithm class, device, optimizer, and output paths.
- Examples: `ooh_code/Src/config.py`, `ooh_code/Src/parser.py`
- Pattern: Attribute bag initialized from argparse namespace, with compatibility aliases assigned by `Parser.finalize_args()`.

**Solver:**
- Purpose: Owns high-level train/evaluation loops and delegates policy choice/update behavior to `config.algo`.
- Examples: `ooh_code/Src/work2_runtime.py`
- Pattern: Thin runtime shell around `env`, `test_env`, and `model`.

**Algorithm / Agent:**
- Purpose: Encapsulates policy action generation, predictor training, checkpoint IO, and route-cost learning.
- Examples: `ooh_code/Src/Algorithms/Agent.py`, `ooh_code/Src/Algorithms/DSPO.py`, `ooh_code/Src/Algorithms/DSPO_Menu.py`
- Pattern: Inheritance stack where `DSPO_Menu` extends base DSPO behavior and overrides menu-mode action/update flow.

**MenuOffer and ServiceBundle:**
- Purpose: Represent displayable alternatives composed of meeting point, pickup window, price, predicted ETA/IVT, utility, score, and metadata.
- Examples: `ooh_code/Environments/OOH/containers.py`, `ooh_code/Src/Algorithms/DSPO_Menu.py`
- Pattern: Dataclasses passed from algorithm to simulator; simulator logs serialized menu decisions from these objects.

**Parcelpoint_py Environment:**
- Purpose: Simulates customer arrivals, menu choice, route insertion, route re-optimization, and metric logging.
- Examples: `ooh_code/Environments/OOH/Parcelpoint_py.py`
- Pattern: OpenAI-Gym-like `reset()` and `step(action)` API using project-specific state arrays.

**Normalized Row:**
- Purpose: Common schema for split-level and aggregate policy comparison metrics.
- Examples: `ooh_code/Src/research_pipeline.py`, `ooh_code/artifacts/results_snapshot/*_rows.csv`
- Pattern: Dict rows whose field order starts with `CSV_FIELD_ORDER` and numeric metric list `SUMMARY_NUMERIC_KEYS`.

**Artifact Snapshot:**
- Purpose: Lightweight committed representation of latest study results for paper tables/figures.
- Examples: `ooh_code/artifacts/results_snapshot/rc_main_summary.json`, `ooh_code/artifacts/tables/rc_main_summary.tex`, `ooh_code/artifacts/figures/rc_main_net_profit.png`
- Pattern: Generated outputs managed by `ooh_code/scripts/build_artifacts.py`.

## Entry Points

**Low-Level Runner:**
- Location: `ooh_code/run_menu_compare.py`
- Triggers: `python run_menu_compare.py ...`
- Responsibilities: Parse full scientific CLI, train/load shared model, evaluate direct paired comparison, write `ooh_code/outputs/menu_compare/`.

**Study Runner:**
- Location: `ooh_code/scripts/run_study.py`
- Triggers: `python scripts/run_study.py --study <name>`
- Responsibilities: Resolve study/suite manifest, execute or resume runs, print summary paths.

**Artifact Builder:**
- Location: `ooh_code/scripts/build_artifacts.py`
- Triggers: `python scripts/build_artifacts.py --study <name>`
- Responsibilities: Build `ooh_code/artifacts/results_snapshot/`, `ooh_code/artifacts/tables/`, `ooh_code/artifacts/figures/`, and `ooh_code/artifacts/RESULTS_SUMMARY.md`.

**Manuscript Builder:**
- Location: `ooh_code/scripts/build_manuscript.py`
- Triggers: `python scripts/build_manuscript.py [--study <name>] [--skip_compile]`
- Responsibilities: Refresh artifacts, detect LaTeX compiler, compile `ooh_code/manuscript/main.tex`, write `ooh_code/manuscript/build/build_status.json`.

**Manuscript Checker:**
- Location: `ooh_code/scripts/check_manuscript.py`
- Triggers: `python scripts/check_manuscript.py` from `ooh_code/`
- Responsibilities: Check LaTeX internal references and generated artifact paths.

**Bootstrap and Legacy Extractors:**
- Location: `ooh_code/scripts/bootstrap_rc.py`, `ooh_code/scripts/bootstrap_amazon.py`, `ooh_code/scripts/extract_phase*_results.py`
- Triggers: Manual phase/debug commands.
- Responsibilities: Create support outputs and extract historical phase summaries into artifact-compatible files.

**LaTeX Entrypoint:**
- Location: `ooh_code/manuscript/main.tex`
- Triggers: `latexmk`, `pdflatex`, or `scripts/build_manuscript.py`
- Responsibilities: Compose paper sections from `ooh_code/manuscript/sections/`, bibliography from `ooh_code/manuscript/references.bib`, and generated tables/figures from `ooh_code/artifacts/`.

## Architectural Constraints

- **Threading:** The code uses a single Python process per command. No worker pool is present in `ooh_code/Src/research_pipeline.py` or `ooh_code/run_menu_compare.py`; parallelism comes from external shell/process orchestration if needed.
- **Global state:** `Config.__init__()` sets global NumPy and Torch seeds and redirects `sys.stdout` through `Src.Utils.Utils.Logger` (`ooh_code/Src/config.py`). Use `restore_stdout()` from `ooh_code/run_menu_compare.py` around nested Config/Solver construction in orchestration code.
- **Current working directory:** Scripts assume `ooh_code/` is on `sys.path` or is the working directory. Script wrappers insert `ROOT` into `sys.path` (`ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, `ooh_code/scripts/build_manuscript.py`).
- **Filesystem outputs:** Config construction creates directories and writes `args.yaml` under `ooh_code/outputs/shared_training/`. Study execution writes into `ooh_code/outputs/studies/`; artifact generation writes into committed `ooh_code/artifacts/`.
- **Checkpoint semantics:** Checkpoints store module weights, not all runtime flags. Evaluation checkpoint loading explicitly sets `initial_phase=False` for learned predictor use (`ooh_code/Src/work2_runtime.py`).
- **Manifest schema coupling:** New manifest keys must either map to parser args or be listed as study-only keys in `STUDY_ONLY_ARG_KEYS` (`ooh_code/Src/research_pipeline.py`).
- **HGS dependency:** Route re-optimization relies on `hygese.Solver` in `ooh_code/Src/Algorithms/DSPO.py` and `ooh_code/Environments/OOH/env_utils.py`.
- **Circular imports:** No circular dependency chain is detected in the primary architecture, but `ooh_code/Src/research_pipeline.py` imports helper functions from top-level `ooh_code/run_menu_compare.py`; keep shared metric helpers stable there or move them deliberately.

## Anti-Patterns

### Manual Artifact Editing

**What happens:** Editing generated `.tex`, `.csv`, `.json`, or `.png` files under `ooh_code/artifacts/` directly bypasses the normalized study summaries.
**Why it's wrong:** The manuscript consumes generated artifact paths, and direct edits break traceability to `ooh_code/outputs/studies/`.
**Do this instead:** Re-run `python scripts/build_artifacts.py --study <name>` from `ooh_code/` after updating manifests or study outputs; use `ooh_code/scripts/build_artifacts.py` for new table/figure logic.

### Policy Variants Hidden Only in Python

**What happens:** Adding a paper comparison only inside `ooh_code/scripts/build_artifacts.py` or `ooh_code/run_menu_compare.py`.
**Why it's wrong:** The study runner and suite system cannot reproduce it from manifest state.
**Do this instead:** Add the variant to a manifest such as `ooh_code/experiments/studies/rc_main.yaml` or create a new manifest under `ooh_code/experiments/studies/`, then consume it through `ooh_code/Src/research_pipeline.py`.

### Mutating Simulator Menu State Without Metadata

**What happens:** Returning menu actions that are not `MenuOffer` objects or omitting metadata expected by `Parcelpoint_py._log_menu_decision()` and metric extraction.
**Why it's wrong:** `run_menu_compare.extract_menu_metrics()` depends on `displayed_offers`, `chosen_offer`, `metadata`, ETA/IVT fields, and menu counts.
**Do this instead:** Build alternatives through `ServiceBundle` and `MenuOffer` in `ooh_code/Environments/OOH/containers.py` and populate metadata in `ooh_code/Src/Algorithms/DSPO_Menu.py` before returning from `get_action_menu()`.

### Creating Config in Nested Code Without Restoring Stdout

**What happens:** Instantiating `Config` during study orchestration without resetting redirected stdout.
**Why it's wrong:** `Config.__init__()` installs `Utils.Logger`, so nested solver creation can leak logging handles or hide terminal output.
**Do this instead:** Follow `restore_stdout()` usage in `ooh_code/run_menu_compare.py` and `ooh_code/Src/research_pipeline.py` around Config/Solver creation.

## Error Handling

**Strategy:** Fail fast for invalid manifest paths, unknown parser overrides, missing checkpoints, unsupported study types, and missing LaTeX compilers; write partial/in-progress study summaries during long runs.

**Patterns:**
- Raise `FileNotFoundError` when a study/suite manifest cannot be resolved (`ooh_code/Src/research_pipeline.py`).
- Raise `ValueError` for unknown parser overrides and unsupported study types (`ooh_code/Src/research_pipeline.py`).
- Raise `FileNotFoundError` if a shared training checkpoint is expected but absent (`ooh_code/Src/research_pipeline.py`).
- Raise `SystemExit` when manuscript compilation is requested without `latexmk` or `pdflatex` (`ooh_code/scripts/build_manuscript.py`).
- Use `subprocess.run(..., check=True)` for artifact and manuscript subprocesses (`ooh_code/scripts/build_manuscript.py`).
- Persist `study_summary.json` with `status="in_progress"` after each split so interrupted runs can resume (`ooh_code/Src/research_pipeline.py`).

## Cross-Cutting Concerns

**Logging:** Runtime logs are redirected by `Src.Utils.Utils.Logger` from `Config.__init__()` into `ooh_code/outputs/shared_training/<run>/logs/`; orchestration uses `restore_stdout()` to avoid nested redirection leaks.

**Validation:** CLI-level validation lives in argparse choices in `ooh_code/Src/parser.py`; manifest validation lives in `resolve_manifest()`, `load_manifest()`, `parser_namespace_with_overrides()`, and `variant_specs_for_manifest()` in `ooh_code/Src/research_pipeline.py`; manuscript artifact/reference validation lives in `ooh_code/scripts/check_manuscript.py`.

**Authentication:** Not applicable. The repository uses local files and public/packaged research dependencies; no auth provider or secret-based integration is detected.

**Reproducibility:** Use YAML manifests, split IDs, manifest hashes, code-version markers, random seeds, frozen request traces, shared checkpoints, and normalized output schemas in `ooh_code/Src/research_pipeline.py`.

**Scientific Traceability:** Keep the chain `experiments/` -> `outputs/studies/` -> `artifacts/` -> `manuscript/` intact. Tables and figures referenced by `ooh_code/manuscript/main.tex` should be generated from `ooh_code/scripts/build_artifacts.py`.

---

*Architecture analysis: 2026-05-27*
