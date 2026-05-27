# Coding Conventions

**Analysis Date:** 2026-05-27

## Naming Patterns

**Files:**
- Use lowercase snake_case for project-level Python scripts and modules: `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, `ooh_code/Src/research_pipeline.py`, `ooh_code/Src/work2_runtime.py`.
- Preserve legacy mixed-case scientific module names inside the imported core: `ooh_code/Src/Algorithms/DSPO_Menu.py`, `ooh_code/Src/Algorithms/DSPO.py`, `ooh_code/Src/Algorithms/Agent.py`, `ooh_code/Src/Utils/Utils.py`, `ooh_code/Src/Utils/Predictors.py`, `ooh_code/Src/Utils/MathUtils.py`.
- Preserve legacy package directory capitalization when adding to the current core: `ooh_code/Src/`, `ooh_code/Src/Algorithms/`, `ooh_code/Src/Utils/`, `ooh_code/Environments/OOH/`.
- Use lowercase descriptive names for experiment manifests: `ooh_code/experiments/studies/rc_main_optout.yaml`, `ooh_code/experiments/studies/phase32_operational_baselines.yaml`, `ooh_code/experiments/suites/rc_paper_v1.yaml`.
- Use lowercase descriptive names for manuscript sections and generated artifact files: `ooh_code/manuscript/sections/results.tex`, `ooh_code/artifacts/tables/rc_main_optout_summary.tex`, `ooh_code/artifacts/figures/rc_main_optout_net_profit.png`, `ooh_code/artifacts/results_snapshot/rc_main_optout_summary.json`.

**Functions:**
- Use snake_case for new functions: `load_manifest`, `execute_study_manifest`, `variant_specs_for_manifest`, `aggregate_rows` in `ooh_code/Src/research_pipeline.py`; `evaluate_policy`, `aggregate_episode_metrics`, `paired_summary` in `ooh_code/run_menu_compare.py`.
- Prefer verb-object names for workflow functions: `build_artifacts`, `detect_compiler`, `compile_with_latexmk`, `sync_build_artifacts_to_root` in `ooh_code/scripts/build_manuscript.py`.
- Keep legacy method names unchanged when extending environment/model classes: `get_new_customer_from_data`, `generate_request_traces`, `reopt_for_eval` in `ooh_code/Environments/OOH/Parcelpoint_py.py`; `get_action_menu`, `derive_preferred_pickup_time`, `_choose_display_window` in `ooh_code/Src/Algorithms/DSPO_Menu.py`.

**Variables:**
- Use snake_case for local variables and manifest fields in new code: `study_name`, `run_id`, `manifest_hash`, `trace_seed`, `checkpoint_path`, `aggregate_variant_summary` in `ooh_code/Src/research_pipeline.py`.
- Use uppercase module constants for repository roots, output directories, schemas, and field orders: `ROOT`, `EXPERIMENTS_DIR`, `STUDIES_DIR`, `SUITES_DIR`, `OUTPUTS_DIR`, `ARTIFACTS_DIR`, `MANUSCRIPT_DIR`, `SUMMARY_NUMERIC_KEYS`, `CSV_FIELD_ORDER` in `ooh_code/Src/research_pipeline.py`.
- Preserve legacy camelCase attributes on simulator dataclasses and environment objects: `remainingCapacity` in `ooh_code/Environments/OOH/containers.py`, `routePlan` in `ooh_code/Environments/OOH/containers.py`, `newCustomer` and `customerChoice` in `ooh_code/Environments/OOH/Parcelpoint_py.py`.
- Use explicit metric names matching artifact columns: `net_profit`, `acceptance_rate`, `opt_out_rate`, `avg_fn_pruning_rate`, `mean_net_profit_gap_vs_reference` in `ooh_code/Src/research_pipeline.py` and `ooh_code/run_menu_compare.py`.

**Types:**
- Use dataclasses for simple domain containers where the code expects attribute access and lightweight computed properties: `Location`, `ParcelPoint`, `Fleet`, `Customer`, `ServiceBundle`, `MenuOffer` in `ooh_code/Environments/OOH/containers.py`.
- Use classes for stateful simulation, solver, parser, and model components: `Config` in `ooh_code/Src/config.py`, `Parser` in `ooh_code/Src/parser.py`, `Solver` in `ooh_code/Src/work2_runtime.py`, `Parcelpoint_py` in `ooh_code/Environments/OOH/Parcelpoint_py.py`, `DSPO_Menu` in `ooh_code/Src/Algorithms/DSPO_Menu.py`.
- Type hints are sparse. Add them only when they clarify data contracts without forcing a broad typing refactor; follow the existing light hint pattern in `ooh_code/Environments/OOH/containers.py`.

## Code Style

**Formatting:**
- Formal formatter config is not detected. No `pyproject.toml`, `setup.cfg`, `.flake8`, `ruff.toml`, or `.pre-commit-config.yaml` exists in the repository root or `ooh_code/`.
- Use 4-space indentation for Python. Existing code uses conventional Python indentation in `ooh_code/Src/research_pipeline.py`, `ooh_code/scripts/run_study.py`, and `ooh_code/scripts/build_artifacts.py`.
- Keep line length pragmatic rather than mechanically enforced. Long argparse help strings appear in `ooh_code/Src/parser.py`; new command help should be readable and split with parentheses when needed.
- Prefer `pathlib.Path` in newer orchestration and artifact code: `ooh_code/Src/research_pipeline.py`, `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, `ooh_code/scripts/build_manuscript.py`.
- Preserve `os.path` style in legacy scientific runner code unless editing the surrounding block substantially: `ooh_code/run_menu_compare.py`, `ooh_code/Src/config.py`, `ooh_code/Src/Utils/Utils.py`.

**Linting:**
- Not detected. There is no configured linter.
- Do not introduce project-wide lint-only rewrites. Keep edits local to the function or script being changed.
- When adding new code, avoid unused imports and broad `except Exception` blocks except where the code already uses tolerant detection or cleanup patterns, such as `detect_code_version_marker` and `latest_resumable_run_id` in `ooh_code/Src/research_pipeline.py`.

## Import Organization

**Order:**
1. Standard library imports first: `csv`, `hashlib`, `json`, `os`, `re`, `subprocess`, `datetime`, `pathlib` in `ooh_code/Src/research_pipeline.py`; `argparse`, `json`, `sys`, `Path` in `ooh_code/scripts/run_study.py`.
2. Third-party imports next: `numpy`, `yaml`, `torch`, `matplotlib` in `ooh_code/Src/research_pipeline.py`, `ooh_code/Src/Algorithms/DSPO_Menu.py`, and `ooh_code/scripts/build_artifacts.py`.
3. Local imports last: `from Src.parser import Parser`, `from Src.config import Config`, `from Src.work2_runtime import Solver`, and imports from `run_menu_compare.py` in `ooh_code/Src/research_pipeline.py`.

**Path Aliases:**
- No configured Python path aliases exist.
- CLI scripts under `ooh_code/scripts/` insert the repository root into `sys.path` before importing `Src`: `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, `ooh_code/scripts/build_manuscript.py`.
- Local imports use package paths from the `ooh_code/` root: `Src.research_pipeline`, `Src.parser`, `Src.work2_runtime`, `Environments.OOH.containers`.
- Run Python commands from `ooh_code/` so imports like `from Src.config import Config` and `from Environments.OOH.Parcelpoint_py import Parcelpoint_py` resolve consistently.

## Error Handling

**Patterns:**
- Use `ValueError` for invalid user/configuration state: unknown parser overrides in `ooh_code/Src/research_pipeline.py`, unsupported study types in `ooh_code/Src/research_pipeline.py`, invalid optimizer names in `ooh_code/Src/config.py`, invalid boolean strings in `ooh_code/Src/parser.py`, invalid Lambert W domain in `ooh_code/Src/Utils/MathUtils.py`.
- Use `FileNotFoundError` when required manifests, checkpoints, run directories, or data files are missing: `resolve_manifest` and `train_or_reuse_shared_model` in `ooh_code/Src/research_pipeline.py`, data loading in `ooh_code/Src/Utils/Utils.py`, bootstrap scripts in `ooh_code/scripts/bootstrap_rc.py` and `ooh_code/scripts/bootstrap_amazon.py`.
- Use `RuntimeError` in extraction scripts when prerequisite study summaries or variants are missing: `ooh_code/scripts/extract_phase8_results.py`, `ooh_code/scripts/extract_phase9_results.py`, `ooh_code/scripts/extract_phase22_results.py`, `ooh_code/scripts/extract_phase23_results.py`, `ooh_code/scripts/extract_phase24_results.py`.
- Use `SystemExit` for CLI-stop conditions where the user needs an actionable command, as in missing LaTeX compiler handling in `ooh_code/scripts/build_manuscript.py`.
- Keep tolerant `try/except Exception` only around non-critical cleanup, fallback detection, or optional parsing: stdout restoration in `ooh_code/run_menu_compare.py`, git marker detection and resume scanning in `ooh_code/Src/research_pipeline.py`, old extraction consolidation fallbacks in `ooh_code/scripts/extract_phase9_results.py`.

## Logging

**Framework:** `print` and custom stdout mirroring.

**Patterns:**
- Use `print` for CLI summaries and human-readable workflow status: `ooh_code/scripts/run_study.py`, `ooh_code/run_menu_compare.py`, `ooh_code/scripts/build_artifacts.py`, `ooh_code/scripts/build_manuscript.py`.
- Runtime training logs are redirected by `Utils.Logger` through `sys.stdout` in `ooh_code/Src/config.py` and `ooh_code/Src/Utils/Utils.py`; call `restore_stdout()` from `ooh_code/run_menu_compare.py` around orchestration code that needs to return normal CLI output.
- Keep artifact and study metadata in machine-readable JSON/YAML/CSV files rather than relying on logs: `study_summary.json`, `normalized_rows.json`, `aggregate_variant_summary.csv` written by `ooh_code/Src/research_pipeline.py`; `build_status.json` written by `ooh_code/scripts/build_manuscript.py`.

## Comments

**When to Comment:**
- Use comments to document research assumptions, legacy compatibility, and non-obvious numerical constants. Examples include `_INCENTIVE_SENS_BETA` in `ooh_code/run_menu_compare.py`, `_eta_sigma` and ETA filter compatibility notes in `ooh_code/Src/Algorithms/DSPO_Menu.py`, and public workflow notes in `ooh_code/docs/WORK2_EXPERIMENT_PROTOCOL.md`.
- Avoid comments that restate simple assignments. Most helper functions in `ooh_code/Src/research_pipeline.py` are named directly enough to avoid extra comments.
- Keep manuscript-source comments in LaTeX only when they assist paper assembly; generated tables and figures are consumed through artifact macros in `ooh_code/manuscript/main.tex` and section files under `ooh_code/manuscript/sections/`.

**JSDoc/TSDoc:**
- Not applicable.
- Python docstrings are minimal. Add docstrings only for public helpers or stateful methods where call contracts are not obvious, matching `reset()` in `ooh_code/Environments/OOH/Parcelpoint_py.py`.

## Function Design

**Size:** 
- Prefer small pure helpers for orchestration and artifact code: `utc_now_iso`, `slugify`, `read_yaml`, `write_csv`, `manifest_hash`, `behavior_gate` in `ooh_code/Src/research_pipeline.py`; `latex_escape`, `format_metric`, `ensure_artifact_dirs` in `ooh_code/scripts/build_artifacts.py`.
- Large legacy model/environment methods exist in `ooh_code/Src/Algorithms/DSPO_Menu.py`, `ooh_code/Environments/OOH/Parcelpoint_py.py`, and `ooh_code/run_menu_compare.py`. When modifying them, extract only clearly reusable helper logic and preserve behavior.
- Keep CLI `main()` functions thin: parse args, call core workflow helpers, print summary. Examples: `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, `ooh_code/scripts/build_manuscript.py`.

**Parameters:** 
- Use explicit keyword-style function calls for multi-parameter workflows and solvers: `execute_study_manifest(manifest, reuse_existing=..., resume_run_id=...)` in `ooh_code/scripts/run_study.py`, `Parcelpoint_py(...)` construction in `ooh_code/Src/config.py`.
- Use argparse for CLI user input. Add new runtime settings in `ooh_code/Src/parser.py`, then map legacy aliases in `Parser.finalize_args`.
- Add manifest-level options under `base_args`, per-split `args_overrides`, or per-policy `args_overrides` in `ooh_code/experiments/studies/*.yaml`; `parser_namespace_with_overrides` in `ooh_code/Src/research_pipeline.py` validates unknown parser keys.

**Return Values:** 
- Return plain dictionaries/lists for normalized study summaries and artifact rows: `aggregate_episode_metrics` and `paired_summary` in `ooh_code/run_menu_compare.py`, `aggregate_rows` and `execute_study_manifest` in `ooh_code/Src/research_pipeline.py`.
- Write durable outputs through helper functions (`save_json`, `write_csv`, `write_yaml`, `write_text`) rather than ad hoc file writes in new orchestration code. These helpers live in `ooh_code/Src/research_pipeline.py` and `ooh_code/run_menu_compare.py`.
- Use `None` to represent unavailable optional metrics in normalized rows, and downstream formatters convert missing values to display placeholders such as `"--"` in `ooh_code/scripts/build_artifacts.py`.

## Module Design

**Exports:** 
- There are no explicit `__all__` exports.
- Utility and orchestration modules expose top-level functions by direct import: `ooh_code/Src/research_pipeline.py` is imported by `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, and `ooh_code/scripts/build_manuscript.py`.
- Scientific core classes are imported directly from their modules: `Config` from `ooh_code/Src/config.py`, `Parser` from `ooh_code/Src/parser.py`, `Solver` from `ooh_code/Src/work2_runtime.py`, `DSPO_Menu` from `ooh_code/Src/Algorithms/DSPO_Menu.py`.

**Barrel Files:** 
- Package marker files exist but do not act as public barrels: `ooh_code/Environments/__init__.py`, `ooh_code/Environments/OOH/__init__.py`.
- Do not add barrel imports unless a package-level API is intentionally introduced; direct module imports are the current convention.

## Manuscript, Experiments, and Artifacts

**Experiment Manifests:**
- Use YAML manifests under `ooh_code/experiments/studies/` for single executable studies and `ooh_code/experiments/suites/` for bundles.
- Required study fields include `name`, `title`, `type`, `reference_*` fields for policy comparisons, `base_args`, `policies`, and `splits`, as shown in `ooh_code/experiments/studies/smoke_rc.yaml` and `ooh_code/experiments/studies/rc_main_optout.yaml`.
- Suite manifests use `type: suite` and `members`, as in `ooh_code/experiments/suites/rc_paper_v1.yaml`.

**Manuscript:**
- Keep the paper source in `ooh_code/manuscript/main.tex`, `ooh_code/manuscript/references.bib`, and section files under `ooh_code/manuscript/sections/`.
- Generated artifacts should be referenced from manuscript sources, not hand-edited into section files. The workflow is documented in `ooh_code/docs/RESEARCH_PROJECT_WORKFLOW.md` and `ooh_code/manuscript/README.md`.

**Artifacts:**
- Lightweight committed outputs live under `ooh_code/artifacts/results_snapshot/`, `ooh_code/artifacts/tables/`, `ooh_code/artifacts/figures/`, and `ooh_code/artifacts/RESULTS_SUMMARY.md`.
- Raw or heavier run outputs live under `ooh_code/outputs/` and are produced by `ooh_code/Src/research_pipeline.py` and `ooh_code/run_menu_compare.py`.
- Use `ooh_code/scripts/build_artifacts.py` to regenerate artifact snapshots, LaTeX tables, PNG figures, and prose summaries from normalized study output.

---

*Convention analysis: 2026-05-27*
