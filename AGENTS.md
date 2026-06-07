<!-- GSD:project-start source:PROJECT.md -->
## Project

**Work 2: Choice-Aware DRT Service Menu Optimization**

This project rebuilds Work 2 from insertion-cost representation learning into choice-aware, profit-aware dynamic service menu optimization for demand-responsive transit. The immediate purpose is to complete an experiment program that can support a defensible TR Part E conclusion: DRT menu design should explicitly account for passenger choice, opt-out risk, pricing, and route-cost feedback rather than only ranking meeting points by predicted insertion cost.

CNN-SetMenuNet is no longer treated as the main positive contribution. It remains valuable as a learned baseline and diagnostic result showing where insertion-cost-based menu design can become misaligned with realized system profit.

**Core Value:** Produce complete, reproducible experimental evidence that either supports or falsifies the new conclusion: choice-aware expected-profit menu optimization provides a more robust profit-service tradeoff than insertion-cost-only menu selection.

### Constraints

- **Existing worktree**: The repository currently contains many uncommitted code and artifact changes. Do not revert unrelated user work.
- **Scientific traceability**: Do not manually edit generated result rows toward a desired conclusion. Experiments must flow from manifests to outputs to artifacts.
- **Stable behavioral model**: MNL choice and outside-option behavior remain unchanged during the first refactor.
- **Stable routing backend**: HGS/Hygese route-cost evaluation remains unchanged during the first refactor.
- **Stable pricing backend**: Lambert-W pricing remains unchanged during the first refactor.
- **Pilot first**: New objective methods must pass smoke and 3-seed pilot diagnostics before formal evidence is claimed.
- **Conclusion honesty**: If Expected-Profit / Service-Constrained methods do not beat Cost-L or CNN-Menu on adjusted/service-constrained metrics, the output must diagnose simulation objective, MNL parameters, price range, candidate generation, or scenario design rather than inventing a positive result.
<!-- GSD:project-end -->

<!-- GSD:stack-start source:codebase/STACK.md -->
## Technology Stack

## Languages
- Python 3.10+ - Required runtime for the Work2 research pipeline under `ooh_code/`; recommended in `ooh_code/README.md`.
- LaTeX - Manuscript source under `ooh_code/manuscript/main.tex`, `ooh_code/manuscript/sections/*.tex`, and `ooh_code/manuscript/references.bib`.
- YAML - Study and suite manifests under `ooh_code/experiments/studies/*.yaml` and `ooh_code/experiments/suites/*.yaml`.
- Markdown - Project documentation and research notes in `ooh_code/README.md`, `ooh_code/docs/*.md`, `ooh_code/experiments/README.md`, `ooh_code/artifacts/README.md`, `ooh_code/manuscript/README.md`, and root notes such as `实验讨论5.26.md`.
- JSON/CSV/TEX/PNG artifacts - Generated or committed research outputs under `ooh_code/artifacts/results_snapshot/`, `ooh_code/artifacts/tables/`, and `ooh_code/artifacts/figures/`.
- Plain text benchmark data - Bundled coordinate and distance files under `ooh_code/Environments/OOH/HombergerGehring_data/` and `ooh_code/Environments/OOH/Amazon_data/`.
## Runtime
- CPython 3.10+ - Install and run from `ooh_code/` with `python -m pip install -r requirements.txt`.
- Optional CUDA through PyTorch - Enabled by `--gpu 1`; device selection is implemented in `ooh_code/Src/config.py`.
- Optional LaTeX toolchain - `latexmk`, `pdflatex`, and optionally `bibtex` are detected by `ooh_code/scripts/build_manuscript.py`.
- Optional Git executable - Used only for code-version marker detection in `ooh_code/Src/research_pipeline.py`.
- pip - Dependencies are declared in `ooh_code/requirements.txt`.
- Lockfile: missing. No `requirements.lock`, `poetry.lock`, `Pipfile.lock`, or Conda environment file detected.
## Frameworks
- PyTorch `>=2.0.1` - Neural predictors, replay buffers, optimizers, model checkpointing, and optional CUDA execution in `ooh_code/Src/Algorithms/DSPO.py`, `ooh_code/Src/Algorithms/DSPO_Menu.py`, `ooh_code/Src/Utils/Predictors.py`, and `ooh_code/Src/Utils/Utils.py`.
- NumPy `~=1.25.1` - Numeric arrays, random sampling, distance matrices, bootstrap routines, and experiment aggregation throughout `ooh_code/Src/`, `ooh_code/Environments/OOH/`, and `ooh_code/scripts/`.
- Hygese `~=0.0.0.8` - Hybrid genetic search routing solver used in `ooh_code/Src/Algorithms/DSPO.py` and `ooh_code/Environments/OOH/env_utils.py`.
- PyYAML `>=6.0` - Reads study manifests and writes run snapshots in `ooh_code/Src/research_pipeline.py` and `ooh_code/Src/config.py`.
- Matplotlib `~=3.7.2` - Training curves and paper figures in `ooh_code/Src/Utils/Utils.py` and `ooh_code/scripts/build_artifacts.py`; `build_artifacts.py` forces the noninteractive `Agg` backend.
- Not detected. No `pytest`, `unittest` test suite, or test runner configuration was found in the repository.
- Smoke verification is workflow-based through `ooh_code/experiments/studies/smoke_rc.yaml`, `ooh_code/experiments/studies/smoke_austin.yaml`, and `python ooh_code/scripts/run_study.py --study smoke_rc`.
- `argparse` command-line interfaces - Main entry points are `ooh_code/run_menu_compare.py`, `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, and `ooh_code/scripts/build_manuscript.py`.
- LaTeX build tools - `ooh_code/scripts/build_manuscript.py` runs `latexmk` when available, otherwise `pdflatex` with optional `bibtex`.
- Git metadata - `ooh_code/Src/research_pipeline.py` calls `git rev-parse --short HEAD`; if unavailable it hashes selected source files.
- Matplotlib artifact generation - `ooh_code/scripts/build_artifacts.py` writes publication figures to `ooh_code/artifacts/figures/`.
## Key Dependencies
- `torch>=2.0.1` - Required for CNN/linear predictors, supervised learning, checkpoint save/load, and tensor-backed memory buffers.
- `numpy~=1.25.1` - Required for simulator state, routing matrices, benchmark data loading, MNL computations, bootstrap confidence intervals, and result aggregation.
- `hygese~=0.0.0.8` - Required for final and intermediate HGS route optimization. `ooh_code/Environments/OOH/Parcelpoint_py.py` notes a known Hygese coordinate assertion behavior.
- `pyyaml>=6.0` - Required for the manifest-driven study system and saved `args.yaml` / `manifest_snapshot.yaml` files.
- `matplotlib~=3.7.2` - Required for generated training curves and paper-ready figures.
- Standard library `subprocess` - Used by `ooh_code/Src/research_pipeline.py` for Git marker detection and by `ooh_code/scripts/build_manuscript.py` for artifact and LaTeX subprocesses.
- Standard library `csv`, `json`, `hashlib`, `pathlib`, `datetime` - Used for normalized summaries, run IDs, manifest hashing, and reproducible artifact metadata in `ooh_code/Src/research_pipeline.py`.
- Optional SciPy - Not declared in `ooh_code/requirements.txt`. `ooh_code/Src/Utils/MathUtils.py` uses `scipy.special.lambertw` when installed and falls back to an internal principal-branch Lambert W implementation.
## Configuration
- No `.env` file or environment-variable based configuration was detected.
- Runtime configuration is CLI-driven in `ooh_code/Src/parser.py`; common options include study instance (`--instance`), split IDs (`--data_seed`, `--data_seed_test`), training length (`--max_episodes`), GPU use (`--gpu`), menu policy (`--menu_policy`), solver timing (`--hgs_reopt_time`, `--hgs_final_time`), and pricing mode (`--menu_pricing_mode`).
- Study configuration is YAML-driven through `ooh_code/experiments/studies/*.yaml` and suite configuration through `ooh_code/experiments/suites/*.yaml`.
- Run-time snapshots are written under `ooh_code/outputs/` by `ooh_code/Src/config.py` and `ooh_code/Src/research_pipeline.py`.
- Dependency manifest: `ooh_code/requirements.txt`.
- Main research runner: `ooh_code/run_menu_compare.py`.
- Study orchestration: `ooh_code/scripts/run_study.py`.
- Artifact build: `ooh_code/scripts/build_artifacts.py`.
- Manuscript build: `ooh_code/scripts/build_manuscript.py`.
- Manuscript source: `ooh_code/manuscript/main.tex`, `ooh_code/manuscript/sections/*.tex`, and `ooh_code/manuscript/references.bib`.
- Artifact outputs: `ooh_code/artifacts/results_snapshot/`, `ooh_code/artifacts/tables/`, and `ooh_code/artifacts/figures/`.
- Raw run outputs: `ooh_code/outputs/` and nested `ooh_code/outputs/studies/`, `ooh_code/outputs/shared_training/`, `ooh_code/outputs/menu_compare/`; ignored by `ooh_code/.gitignore`.
## Platform Requirements
- Windows PowerShell examples are documented in `ooh_code/README.md`, but the Python code uses portable `pathlib`/`os.path` patterns in most scripts.
- Create a virtual environment from `ooh_code/` and install `ooh_code/requirements.txt`.
- Run research workflows from `ooh_code/` so imports like `Src.research_pipeline` and bundled data paths resolve correctly.
- Keep benchmark data available under `ooh_code/Environments/OOH/HombergerGehring_data/` and `ooh_code/Environments/OOH/Amazon_data/`.
- Install `latexmk` or `pdflatex` only when compiling the manuscript PDF; `--skip_compile` still refreshes artifacts and metadata.
- Not applicable as a hosted application. The repository is a local/offline research codebase.
- Public-facing deliverables are committed research artifacts under `ooh_code/artifacts/` and manuscript files under `ooh_code/manuscript/`.
- Raw generated outputs under `ooh_code/outputs/` are local experiment state and are excluded by `ooh_code/.gitignore`.
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

## Naming Patterns
- Use lowercase snake_case for project-level Python scripts and modules: `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, `ooh_code/Src/research_pipeline.py`, `ooh_code/Src/work2_runtime.py`.
- Preserve legacy mixed-case scientific module names inside the imported core: `ooh_code/Src/Algorithms/DSPO_Menu.py`, `ooh_code/Src/Algorithms/DSPO.py`, `ooh_code/Src/Algorithms/Agent.py`, `ooh_code/Src/Utils/Utils.py`, `ooh_code/Src/Utils/Predictors.py`, `ooh_code/Src/Utils/MathUtils.py`.
- Preserve legacy package directory capitalization when adding to the current core: `ooh_code/Src/`, `ooh_code/Src/Algorithms/`, `ooh_code/Src/Utils/`, `ooh_code/Environments/OOH/`.
- Use lowercase descriptive names for experiment manifests: `ooh_code/experiments/studies/rc_main_optout.yaml`, `ooh_code/experiments/studies/phase32_operational_baselines.yaml`, `ooh_code/experiments/suites/rc_paper_v1.yaml`.
- Use lowercase descriptive names for manuscript sections and generated artifact files: `ooh_code/manuscript/sections/results.tex`, `ooh_code/artifacts/tables/rc_main_optout_summary.tex`, `ooh_code/artifacts/figures/rc_main_optout_net_profit.png`, `ooh_code/artifacts/results_snapshot/rc_main_optout_summary.json`.
- Use snake_case for new functions: `load_manifest`, `execute_study_manifest`, `variant_specs_for_manifest`, `aggregate_rows` in `ooh_code/Src/research_pipeline.py`; `evaluate_policy`, `aggregate_episode_metrics`, `paired_summary` in `ooh_code/run_menu_compare.py`.
- Prefer verb-object names for workflow functions: `build_artifacts`, `detect_compiler`, `compile_with_latexmk`, `sync_build_artifacts_to_root` in `ooh_code/scripts/build_manuscript.py`.
- Keep legacy method names unchanged when extending environment/model classes: `get_new_customer_from_data`, `generate_request_traces`, `reopt_for_eval` in `ooh_code/Environments/OOH/Parcelpoint_py.py`; `get_action_menu`, `derive_preferred_pickup_time`, `_choose_display_window` in `ooh_code/Src/Algorithms/DSPO_Menu.py`.
- Use snake_case for local variables and manifest fields in new code: `study_name`, `run_id`, `manifest_hash`, `trace_seed`, `checkpoint_path`, `aggregate_variant_summary` in `ooh_code/Src/research_pipeline.py`.
- Use uppercase module constants for repository roots, output directories, schemas, and field orders: `ROOT`, `EXPERIMENTS_DIR`, `STUDIES_DIR`, `SUITES_DIR`, `OUTPUTS_DIR`, `ARTIFACTS_DIR`, `MANUSCRIPT_DIR`, `SUMMARY_NUMERIC_KEYS`, `CSV_FIELD_ORDER` in `ooh_code/Src/research_pipeline.py`.
- Preserve legacy camelCase attributes on simulator dataclasses and environment objects: `remainingCapacity` in `ooh_code/Environments/OOH/containers.py`, `routePlan` in `ooh_code/Environments/OOH/containers.py`, `newCustomer` and `customerChoice` in `ooh_code/Environments/OOH/Parcelpoint_py.py`.
- Use explicit metric names matching artifact columns: `net_profit`, `acceptance_rate`, `opt_out_rate`, `avg_fn_pruning_rate`, `mean_net_profit_gap_vs_reference` in `ooh_code/Src/research_pipeline.py` and `ooh_code/run_menu_compare.py`.
- Use dataclasses for simple domain containers where the code expects attribute access and lightweight computed properties: `Location`, `ParcelPoint`, `Fleet`, `Customer`, `ServiceBundle`, `MenuOffer` in `ooh_code/Environments/OOH/containers.py`.
- Use classes for stateful simulation, solver, parser, and model components: `Config` in `ooh_code/Src/config.py`, `Parser` in `ooh_code/Src/parser.py`, `Solver` in `ooh_code/Src/work2_runtime.py`, `Parcelpoint_py` in `ooh_code/Environments/OOH/Parcelpoint_py.py`, `DSPO_Menu` in `ooh_code/Src/Algorithms/DSPO_Menu.py`.
- Type hints are sparse. Add them only when they clarify data contracts without forcing a broad typing refactor; follow the existing light hint pattern in `ooh_code/Environments/OOH/containers.py`.
## Code Style
- Formal formatter config is not detected. No `pyproject.toml`, `setup.cfg`, `.flake8`, `ruff.toml`, or `.pre-commit-config.yaml` exists in the repository root or `ooh_code/`.
- Use 4-space indentation for Python. Existing code uses conventional Python indentation in `ooh_code/Src/research_pipeline.py`, `ooh_code/scripts/run_study.py`, and `ooh_code/scripts/build_artifacts.py`.
- Keep line length pragmatic rather than mechanically enforced. Long argparse help strings appear in `ooh_code/Src/parser.py`; new command help should be readable and split with parentheses when needed.
- Prefer `pathlib.Path` in newer orchestration and artifact code: `ooh_code/Src/research_pipeline.py`, `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, `ooh_code/scripts/build_manuscript.py`.
- Preserve `os.path` style in legacy scientific runner code unless editing the surrounding block substantially: `ooh_code/run_menu_compare.py`, `ooh_code/Src/config.py`, `ooh_code/Src/Utils/Utils.py`.
- Not detected. There is no configured linter.
- Do not introduce project-wide lint-only rewrites. Keep edits local to the function or script being changed.
- When adding new code, avoid unused imports and broad `except Exception` blocks except where the code already uses tolerant detection or cleanup patterns, such as `detect_code_version_marker` and `latest_resumable_run_id` in `ooh_code/Src/research_pipeline.py`.
## Import Organization
- No configured Python path aliases exist.
- CLI scripts under `ooh_code/scripts/` insert the repository root into `sys.path` before importing `Src`: `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, `ooh_code/scripts/build_manuscript.py`.
- Local imports use package paths from the `ooh_code/` root: `Src.research_pipeline`, `Src.parser`, `Src.work2_runtime`, `Environments.OOH.containers`.
- Run Python commands from `ooh_code/` so imports like `from Src.config import Config` and `from Environments.OOH.Parcelpoint_py import Parcelpoint_py` resolve consistently.
## Error Handling
- Use `ValueError` for invalid user/configuration state: unknown parser overrides in `ooh_code/Src/research_pipeline.py`, unsupported study types in `ooh_code/Src/research_pipeline.py`, invalid optimizer names in `ooh_code/Src/config.py`, invalid boolean strings in `ooh_code/Src/parser.py`, invalid Lambert W domain in `ooh_code/Src/Utils/MathUtils.py`.
- Use `FileNotFoundError` when required manifests, checkpoints, run directories, or data files are missing: `resolve_manifest` and `train_or_reuse_shared_model` in `ooh_code/Src/research_pipeline.py`, data loading in `ooh_code/Src/Utils/Utils.py`, bootstrap scripts in `ooh_code/scripts/bootstrap_rc.py` and `ooh_code/scripts/bootstrap_amazon.py`.
- Use `RuntimeError` in extraction scripts when prerequisite study summaries or variants are missing: `ooh_code/scripts/extract_phase8_results.py`, `ooh_code/scripts/extract_phase9_results.py`, `ooh_code/scripts/extract_phase22_results.py`, `ooh_code/scripts/extract_phase23_results.py`, `ooh_code/scripts/extract_phase24_results.py`.
- Use `SystemExit` for CLI-stop conditions where the user needs an actionable command, as in missing LaTeX compiler handling in `ooh_code/scripts/build_manuscript.py`.
- Keep tolerant `try/except Exception` only around non-critical cleanup, fallback detection, or optional parsing: stdout restoration in `ooh_code/run_menu_compare.py`, git marker detection and resume scanning in `ooh_code/Src/research_pipeline.py`, old extraction consolidation fallbacks in `ooh_code/scripts/extract_phase9_results.py`.
## Logging
- Use `print` for CLI summaries and human-readable workflow status: `ooh_code/scripts/run_study.py`, `ooh_code/run_menu_compare.py`, `ooh_code/scripts/build_artifacts.py`, `ooh_code/scripts/build_manuscript.py`.
- Runtime training logs are redirected by `Utils.Logger` through `sys.stdout` in `ooh_code/Src/config.py` and `ooh_code/Src/Utils/Utils.py`; call `restore_stdout()` from `ooh_code/run_menu_compare.py` around orchestration code that needs to return normal CLI output.
- Keep artifact and study metadata in machine-readable JSON/YAML/CSV files rather than relying on logs: `study_summary.json`, `normalized_rows.json`, `aggregate_variant_summary.csv` written by `ooh_code/Src/research_pipeline.py`; `build_status.json` written by `ooh_code/scripts/build_manuscript.py`.
## Comments
- Use comments to document research assumptions, legacy compatibility, and non-obvious numerical constants. Examples include `_INCENTIVE_SENS_BETA` in `ooh_code/run_menu_compare.py`, `_eta_sigma` and ETA filter compatibility notes in `ooh_code/Src/Algorithms/DSPO_Menu.py`, and public workflow notes in `ooh_code/docs/WORK2_EXPERIMENT_PROTOCOL.md`.
- Avoid comments that restate simple assignments. Most helper functions in `ooh_code/Src/research_pipeline.py` are named directly enough to avoid extra comments.
- Keep manuscript-source comments in LaTeX only when they assist paper assembly; generated tables and figures are consumed through artifact macros in `ooh_code/manuscript/main.tex` and section files under `ooh_code/manuscript/sections/`.
- Not applicable.
- Python docstrings are minimal. Add docstrings only for public helpers or stateful methods where call contracts are not obvious, matching `reset()` in `ooh_code/Environments/OOH/Parcelpoint_py.py`.
## Function Design
- Prefer small pure helpers for orchestration and artifact code: `utc_now_iso`, `slugify`, `read_yaml`, `write_csv`, `manifest_hash`, `behavior_gate` in `ooh_code/Src/research_pipeline.py`; `latex_escape`, `format_metric`, `ensure_artifact_dirs` in `ooh_code/scripts/build_artifacts.py`.
- Large legacy model/environment methods exist in `ooh_code/Src/Algorithms/DSPO_Menu.py`, `ooh_code/Environments/OOH/Parcelpoint_py.py`, and `ooh_code/run_menu_compare.py`. When modifying them, extract only clearly reusable helper logic and preserve behavior.
- Keep CLI `main()` functions thin: parse args, call core workflow helpers, print summary. Examples: `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, `ooh_code/scripts/build_manuscript.py`.
- Use explicit keyword-style function calls for multi-parameter workflows and solvers: `execute_study_manifest(manifest, reuse_existing=..., resume_run_id=...)` in `ooh_code/scripts/run_study.py`, `Parcelpoint_py(...)` construction in `ooh_code/Src/config.py`.
- Use argparse for CLI user input. Add new runtime settings in `ooh_code/Src/parser.py`, then map legacy aliases in `Parser.finalize_args`.
- Add manifest-level options under `base_args`, per-split `args_overrides`, or per-policy `args_overrides` in `ooh_code/experiments/studies/*.yaml`; `parser_namespace_with_overrides` in `ooh_code/Src/research_pipeline.py` validates unknown parser keys.
- Return plain dictionaries/lists for normalized study summaries and artifact rows: `aggregate_episode_metrics` and `paired_summary` in `ooh_code/run_menu_compare.py`, `aggregate_rows` and `execute_study_manifest` in `ooh_code/Src/research_pipeline.py`.
- Write durable outputs through helper functions (`save_json`, `write_csv`, `write_yaml`, `write_text`) rather than ad hoc file writes in new orchestration code. These helpers live in `ooh_code/Src/research_pipeline.py` and `ooh_code/run_menu_compare.py`.
- Use `None` to represent unavailable optional metrics in normalized rows, and downstream formatters convert missing values to display placeholders such as `"--"` in `ooh_code/scripts/build_artifacts.py`.
## Module Design
- There are no explicit `__all__` exports.
- Utility and orchestration modules expose top-level functions by direct import: `ooh_code/Src/research_pipeline.py` is imported by `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, and `ooh_code/scripts/build_manuscript.py`.
- Scientific core classes are imported directly from their modules: `Config` from `ooh_code/Src/config.py`, `Parser` from `ooh_code/Src/parser.py`, `Solver` from `ooh_code/Src/work2_runtime.py`, `DSPO_Menu` from `ooh_code/Src/Algorithms/DSPO_Menu.py`.
- Package marker files exist but do not act as public barrels: `ooh_code/Environments/__init__.py`, `ooh_code/Environments/OOH/__init__.py`.
- Do not add barrel imports unless a package-level API is intentionally introduced; direct module imports are the current convention.
## Manuscript, Experiments, and Artifacts
- Use YAML manifests under `ooh_code/experiments/studies/` for single executable studies and `ooh_code/experiments/suites/` for bundles.
- Required study fields include `name`, `title`, `type`, `reference_*` fields for policy comparisons, `base_args`, `policies`, and `splits`, as shown in `ooh_code/experiments/studies/smoke_rc.yaml` and `ooh_code/experiments/studies/rc_main_optout.yaml`.
- Suite manifests use `type: suite` and `members`, as in `ooh_code/experiments/suites/rc_paper_v1.yaml`.
- Keep the paper source in `ooh_code/manuscript/main.tex`, `ooh_code/manuscript/references.bib`, and section files under `ooh_code/manuscript/sections/`.
- Generated artifacts should be referenced from manuscript sources, not hand-edited into section files. The workflow is documented in `ooh_code/docs/RESEARCH_PROJECT_WORKFLOW.md` and `ooh_code/manuscript/README.md`.
- Lightweight committed outputs live under `ooh_code/artifacts/results_snapshot/`, `ooh_code/artifacts/tables/`, `ooh_code/artifacts/figures/`, and `ooh_code/artifacts/RESULTS_SUMMARY.md`.
- Raw or heavier run outputs live under `ooh_code/outputs/` and are produced by `ooh_code/Src/research_pipeline.py` and `ooh_code/run_menu_compare.py`.
- Use `ooh_code/scripts/build_artifacts.py` to regenerate artifact snapshots, LaTeX tables, PNG figures, and prose summaries from normalized study output.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

## System Overview
```text
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
- Use `ooh_code/experiments/studies/*.yaml` and `ooh_code/experiments/suites/*.yaml` as the source of truth for study design; avoid encoding paper study variants only in scripts.
- Keep policy-evaluation fairness centralized: train one shared predictor with `offer_all_feasible_bundles`, then evaluate variants with `eval_only=True`, `freeze_learning=True`, and replayed traces via `ooh_code/Src/research_pipeline.py`.
- Generate paper-facing tables and figures from normalized summaries under `ooh_code/outputs/studies/`; do not manually edit generated files under `ooh_code/artifacts/`.
- Treat `ooh_code/Src/Algorithms/DSPO_Menu.py` and `ooh_code/Environments/OOH/Parcelpoint_py.py` as the coupled scientific core. Menu offers produced by the algorithm must remain compatible with simulator choice and logging.
## Layers
- Purpose: Holds the executable research project plus publication notes, literature, planning metadata, and discussion files.
- Location: `.`
- Contains: `ooh_code/`, `2025.9.11-pom_big price/`, `qi_wei/`, `.planning/`, `实验讨论5.26.md`, `learning meeting point.docx`
- Depends on: Local filesystem only.
- Used by: Planning agents and the author workflow.
- Purpose: Provides the runnable many-to-one DRT menu optimization project.
- Location: `ooh_code/`
- Contains: `README.md`, `requirements.txt`, `run_menu_compare.py`, `Src/`, `Environments/`, `experiments/`, `scripts/`, `artifacts/`, `manuscript/`, `outputs/`, `docs/`
- Depends on: Python runtime, PyTorch, NumPy, pandas/matplotlib/YAML stack, `hygese`, optional LaTeX tooling.
- Used by: All experiment, artifact, and manuscript workflows.
- Purpose: Exposes command-line workflows for direct comparison, manifest execution, artifact generation, manuscript compilation, and legacy extraction tasks.
- Location: `ooh_code/run_menu_compare.py`, `ooh_code/scripts/`
- Contains: `scripts/run_study.py`, `scripts/build_artifacts.py`, `scripts/build_manuscript.py`, `scripts/check_manuscript.py`, `scripts/bootstrap_*.py`, `scripts/extract_phase*_results.py`
- Depends on: `ooh_code/Src/research_pipeline.py`, `ooh_code/Src/parser.py`, `ooh_code/Src/config.py`, `ooh_code/run_menu_compare.py`
- Used by: Public workflows documented in `ooh_code/README.md` and `ooh_code/docs/RESEARCH_PROJECT_WORKFLOW.md`.
- Purpose: Describes studies, suites, split pairs, policy variants, behavior gates, and headline variants.
- Location: `ooh_code/experiments/`
- Contains: `experiments/studies/rc_main.yaml`, `experiments/studies/austin_main.yaml`, `experiments/studies/seattle_main.yaml`, `experiments/studies/rc_main_optout.yaml`, `experiments/suites/rc_paper_v1.yaml`, `experiments/suites/phase31_uptake_menu_value.yaml`
- Depends on: Field names consumed by `ooh_code/Src/research_pipeline.py`.
- Used by: `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`.
- Purpose: Resolves manifests, expands variants, trains/reuses shared checkpoints, generates request traces, executes variants, aggregates rows, and saves summary schemas.
- Location: `ooh_code/Src/research_pipeline.py`
- Contains: Manifest IO, study execution, suite execution, CSV/JSON writers, run-id generation, normalized row aggregation.
- Depends on: `ooh_code/Src/parser.py`, `ooh_code/Src/config.py`, `ooh_code/Src/work2_runtime.py`, `ooh_code/run_menu_compare.py`.
- Used by: `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, `ooh_code/scripts/build_manuscript.py`.
- Purpose: Executes training/evaluation episodes and computes low-level comparison metrics.
- Location: `ooh_code/run_menu_compare.py`, `ooh_code/Src/work2_runtime.py`
- Contains: `Solver`, `evaluate_policy`, `summarize_episode`, `aggregate_episode_metrics`, `paired_summary`, checkpoint handling.
- Depends on: `ooh_code/Src/config.py`, `ooh_code/Src/Algorithms/DSPO_Menu.py`, `ooh_code/Environments/OOH/Parcelpoint_py.py`.
- Used by: Orchestration layer and direct low-level runner.
- Purpose: Implements policy construction, model prediction, pricing, menu selection, and learning updates.
- Location: `ooh_code/Src/Algorithms/`
- Contains: `Agent.py`, `DSPO.py`, `DSPO_Menu.py`
- Depends on: `ooh_code/Src/Utils/`, `ooh_code/Environments/OOH/containers.py`, PyTorch, NumPy, `hygese`.
- Used by: `Config.algo` in `ooh_code/Src/config.py` and `Solver.model` in `ooh_code/Src/work2_runtime.py`.
- Purpose: Provides the environment state transition model, request traces, menu choice realization, fleet mutation, and route re-optimization hooks.
- Location: `ooh_code/Environments/OOH/`
- Contains: `Parcelpoint_py.py`, `customerchoice.py`, `env_utils.py`, `containers.py`, benchmark data directories.
- Depends on: `ooh_code/Src/Utils/Utils.py`, `hygese`, NumPy.
- Used by: `Config.build_environment()` in `ooh_code/Src/config.py`.
- Purpose: Supplies predictors, math fallback, logging, data loading, HGS helpers, grid feature encoding, and replay memory.
- Location: `ooh_code/Src/Utils/`
- Contains: `Predictors.py`, `MathUtils.py`, `Utils.py`
- Depends on: PyTorch, NumPy, matplotlib, bundled data paths.
- Used by: `DSPO.py`, `DSPO_Menu.py`, `config.py`, and environment utilities.
- Purpose: Separates heavy raw outputs from lightweight committed paper artifacts and manuscript source.
- Location: `ooh_code/outputs/`, `ooh_code/artifacts/`, `ooh_code/manuscript/`
- Contains: Raw run directories under `outputs/studies/` and `outputs/menu_compare/`; committed `artifacts/results_snapshot/`, `artifacts/tables/`, `artifacts/figures/`; LaTeX source under `manuscript/`.
- Depends on: `ooh_code/scripts/build_artifacts.py`, `ooh_code/scripts/build_manuscript.py`.
- Used by: Paper writing and review workflows.
## Data Flow
### Primary Request Path
### Direct Low-Level Comparison
### Artifact and Manuscript Flow
- Runtime state is episode-local in `Solver`, `DSPO_Menu`, and `Parcelpoint_py`; reset between episodes through `Solver.train()`, `evaluate_policy()`, and `Parcelpoint_py.reset()`.
- Reproducibility state is controlled by parser/config seeds, `Config.__init__()` NumPy/Torch seed setting, and simulator request/choice RNGs in `Parcelpoint_py.seed()`.
- Persistent state is filesystem-based: shared checkpoints under `ooh_code/outputs/shared_training/`, normalized study runs under `ooh_code/outputs/studies/`, direct compare outputs under `ooh_code/outputs/menu_compare/`, and committed paper artifacts under `ooh_code/artifacts/`.
## Key Abstractions
- Purpose: Declarative specification of a study or suite.
- Examples: `ooh_code/experiments/studies/rc_main.yaml`, `ooh_code/experiments/studies/austin_main.yaml`, `ooh_code/experiments/suites/rc_paper_v1.yaml`
- Pattern: YAML mapping consumed by `load_manifest()`, `variant_specs_for_manifest()`, and `execute_study_manifest()` in `ooh_code/Src/research_pipeline.py`.
- Purpose: Converts parser arguments into data, environment instances, algorithm class, device, optimizer, and output paths.
- Examples: `ooh_code/Src/config.py`, `ooh_code/Src/parser.py`
- Pattern: Attribute bag initialized from argparse namespace, with compatibility aliases assigned by `Parser.finalize_args()`.
- Purpose: Owns high-level train/evaluation loops and delegates policy choice/update behavior to `config.algo`.
- Examples: `ooh_code/Src/work2_runtime.py`
- Pattern: Thin runtime shell around `env`, `test_env`, and `model`.
- Purpose: Encapsulates policy action generation, predictor training, checkpoint IO, and route-cost learning.
- Examples: `ooh_code/Src/Algorithms/Agent.py`, `ooh_code/Src/Algorithms/DSPO.py`, `ooh_code/Src/Algorithms/DSPO_Menu.py`
- Pattern: Inheritance stack where `DSPO_Menu` extends base DSPO behavior and overrides menu-mode action/update flow.
- Purpose: Represent displayable alternatives composed of meeting point, pickup window, price, predicted ETA/IVT, utility, score, and metadata.
- Examples: `ooh_code/Environments/OOH/containers.py`, `ooh_code/Src/Algorithms/DSPO_Menu.py`
- Pattern: Dataclasses passed from algorithm to simulator; simulator logs serialized menu decisions from these objects.
- Purpose: Simulates customer arrivals, menu choice, route insertion, route re-optimization, and metric logging.
- Examples: `ooh_code/Environments/OOH/Parcelpoint_py.py`
- Pattern: OpenAI-Gym-like `reset()` and `step(action)` API using project-specific state arrays.
- Purpose: Common schema for split-level and aggregate policy comparison metrics.
- Examples: `ooh_code/Src/research_pipeline.py`, `ooh_code/artifacts/results_snapshot/*_rows.csv`
- Pattern: Dict rows whose field order starts with `CSV_FIELD_ORDER` and numeric metric list `SUMMARY_NUMERIC_KEYS`.
- Purpose: Lightweight committed representation of latest study results for paper tables/figures.
- Examples: `ooh_code/artifacts/results_snapshot/rc_main_summary.json`, `ooh_code/artifacts/tables/rc_main_summary.tex`, `ooh_code/artifacts/figures/rc_main_net_profit.png`
- Pattern: Generated outputs managed by `ooh_code/scripts/build_artifacts.py`.
## Entry Points
- Location: `ooh_code/run_menu_compare.py`
- Triggers: `python run_menu_compare.py ...`
- Responsibilities: Parse full scientific CLI, train/load shared model, evaluate direct paired comparison, write `ooh_code/outputs/menu_compare/`.
- Location: `ooh_code/scripts/run_study.py`
- Triggers: `python scripts/run_study.py --study <name>`
- Responsibilities: Resolve study/suite manifest, execute or resume runs, print summary paths.
- Location: `ooh_code/scripts/build_artifacts.py`
- Triggers: `python scripts/build_artifacts.py --study <name>`
- Responsibilities: Build `ooh_code/artifacts/results_snapshot/`, `ooh_code/artifacts/tables/`, `ooh_code/artifacts/figures/`, and `ooh_code/artifacts/RESULTS_SUMMARY.md`.
- Location: `ooh_code/scripts/build_manuscript.py`
- Triggers: `python scripts/build_manuscript.py [--study <name>] [--skip_compile]`
- Responsibilities: Refresh artifacts, detect LaTeX compiler, compile `ooh_code/manuscript/main.tex`, write `ooh_code/manuscript/build/build_status.json`.
- Location: `ooh_code/scripts/check_manuscript.py`
- Triggers: `python scripts/check_manuscript.py` from `ooh_code/`
- Responsibilities: Check LaTeX internal references and generated artifact paths.
- Location: `ooh_code/scripts/bootstrap_rc.py`, `ooh_code/scripts/bootstrap_amazon.py`, `ooh_code/scripts/extract_phase*_results.py`
- Triggers: Manual phase/debug commands.
- Responsibilities: Create support outputs and extract historical phase summaries into artifact-compatible files.
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
### Policy Variants Hidden Only in Python
### Mutating Simulator Menu State Without Metadata
### Creating Config in Nested Code Without Restoring Stdout
## Error Handling
- Raise `FileNotFoundError` when a study/suite manifest cannot be resolved (`ooh_code/Src/research_pipeline.py`).
- Raise `ValueError` for unknown parser overrides and unsupported study types (`ooh_code/Src/research_pipeline.py`).
- Raise `FileNotFoundError` if a shared training checkpoint is expected but absent (`ooh_code/Src/research_pipeline.py`).
- Raise `SystemExit` when manuscript compilation is requested without `latexmk` or `pdflatex` (`ooh_code/scripts/build_manuscript.py`).
- Use `subprocess.run(..., check=True)` for artifact and manuscript subprocesses (`ooh_code/scripts/build_manuscript.py`).
- Persist `study_summary.json` with `status="in_progress"` after each split so interrupted runs can resume (`ooh_code/Src/research_pipeline.py`).
## Cross-Cutting Concerns
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`, or `.codex/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
