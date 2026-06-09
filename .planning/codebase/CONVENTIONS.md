# Coding Conventions

**Analysis Date:** 2026-06-09
**last_mapped_commit:** `37b20aa`

## Naming Patterns

**Files:**
- Use lowercase snake_case for project-level Python entry points and helper modules: `ooh_code/run_menu_compare.py`, `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, `ooh_code/scripts/build_manuscript.py`, `ooh_code/Src/research_pipeline.py`, `ooh_code/Src/work2_runtime.py`.
- Preserve existing mixed-case scientific modules under `ooh_code/Src/Algorithms/` and `ooh_code/Src/Utils/`: `ooh_code/Src/Algorithms/DSPO_Menu.py`, `ooh_code/Src/Algorithms/CNN_SetMenu.py`, `ooh_code/Src/Algorithms/MLP_SetMenu.py`, `ooh_code/Src/Utils/CNNSetMenuNet.py`, `ooh_code/Src/Utils/SetMenuNet.py`, `ooh_code/Src/Utils/MLPMenuNet.py`.
- Use `test_*.py` for executable script tests in `ooh_code/scripts/`: `ooh_code/scripts/test_option_features.py`, `ooh_code/scripts/test_menu_objective_mode.py`, `ooh_code/scripts/test_work2_main_manifest.py`, `ooh_code/scripts/test_phase08_artifact_gate.py`.
- Use lowercase descriptive names for YAML manifests under `ooh_code/experiments/studies/` and `ooh_code/experiments/suites/`: `ooh_code/experiments/studies/rc_main_optout.yaml`, `ooh_code/experiments/studies/work2_main.yaml`, `ooh_code/experiments/suites/rc_paper_v1.yaml`, `ooh_code/experiments/suites/work2_robustness.yaml`.
- Use descriptive artifact names that encode study and metric under `ooh_code/artifacts/` and root `artifacts/work2_cnn_setmenunet/`: `ooh_code/artifacts/results_snapshot/rc_main_optout_rows.csv`, `ooh_code/artifacts/figures/rc_main_optout_net_profit.png`, `artifacts/work2_cnn_setmenunet/tables/work2_main_operational.tex`.

**Functions:**
- Use snake_case for functions in orchestration and utility code: `utc_now_iso`, `run_id_from_hash`, `variant_specs_for_manifest`, `aggregate_rows`, and `execute_study_manifest` in `ooh_code/Src/research_pipeline.py`.
- Use snake_case for CLI workflow helpers: `build_artifacts`, `detect_compiler`, `compile_with_latexmk`, `sync_build_artifacts_to_root`, and `compile_with_pdflatex` in `ooh_code/scripts/build_manuscript.py`.
- Use verb-object names for workflow operations and artifact emitters: `write_csv`, `write_text`, `load_manifest`, `load_study_summary` in `ooh_code/Src/research_pipeline.py`; `write_tex_table`, `build_main_policy_artifacts`, `build_robustness_artifacts` in `ooh_code/scripts/build_artifacts.py`.
- Preserve existing class method names in the scientific core when extending behavior: `get_action_menu`, `_select_menu_exact`, `_select_menu_service_constrained`, `_choose_redesigned_menu`, and `enumerate_candidate_subsets` in `ooh_code/Src/Algorithms/DSPO_Menu.py`; `generate_request_traces` and `reopt_for_eval` in `ooh_code/Environments/OOH/Parcelpoint_py.py`.
- Test functions use `test_*` names even though pytest is not configured: `test_shape_k10` in `ooh_code/scripts/test_option_features.py`, `test_current_mode_preserves_menu_cost_pricing` in `ooh_code/scripts/test_menu_objective_mode.py`, `test_complete_pass_writes_phase_local_artifacts` in `ooh_code/scripts/test_phase08_artifact_gate.py`.

**Variables:**
- Use snake_case for local variables, manifest fields, run metadata, and normalized metrics: `study_name`, `run_id`, `manifest_hash`, `trace_seed`, `checkpoint_path`, `aggregate_variant_summary`, and `normalized_rows` in `ooh_code/Src/research_pipeline.py`.
- Use uppercase constants for roots, directory handles, schemas, field orders, and fixed contracts: `ROOT`, `EXPERIMENTS_DIR`, `STUDIES_DIR`, `SUITES_DIR`, `OUTPUTS_DIR`, `ARTIFACTS_DIR`, `SUMMARY_NUMERIC_KEYS`, `CSV_FIELD_ORDER`, and `STUDY_ONLY_ARG_KEYS` in `ooh_code/Src/research_pipeline.py`.
- Preserve simulator attribute names that are already camelCase or mixed-case on domain containers: `remainingCapacity`, `routePlan`, `incentiveSensitivity` in `ooh_code/Environments/OOH/containers.py`; `newCustomer` and `customerChoice` usage in `ooh_code/Environments/OOH/Parcelpoint_py.py`.
- Use explicit metric field names that match output rows and artifact columns: `net_profit`, `adjusted_profit`, `service_constrained_net_profit`, `opt_out_rate`, `acceptance_rate`, `avg_fn_pruning_rate`, `mean_net_profit_gap_vs_reference` in `ooh_code/Src/research_pipeline.py` and `ooh_code/run_menu_compare.py`.

**Types:**
- Use dataclasses for simple domain records that need attribute access: `Location`, `ParcelPoint`, `Vehicle`, `Fleet`, `Customer`, `ServiceBundle`, and `MenuOffer` in `ooh_code/Environments/OOH/containers.py`.
- Use classes for stateful runtime components: `Parser` in `ooh_code/Src/parser.py`, `Config` in `ooh_code/Src/config.py`, `Solver` in `ooh_code/Src/work2_runtime.py`, `DSPO_Menu` in `ooh_code/Src/Algorithms/DSPO_Menu.py`, `Parcelpoint_py` in `ooh_code/Environments/OOH/Parcelpoint_py.py`.
- Use light type hints where they clarify simple data contracts, matching `MenuOffer.bundle_id -> str`, `MenuOffer.window -> Tuple[float, float]`, and `build_option_tensor(...) -> tuple` in `ooh_code/Environments/OOH/containers.py` and `ooh_code/Src/Utils/option_features.py`.

## Code Style

**Formatting:**
- Tool used: Not detected. No `pyproject.toml`, `setup.cfg`, `.flake8`, `ruff.toml`, `.pre-commit-config.yaml`, `.prettierrc`, or formatter config is present at the repository root or under `ooh_code/`.
- Use 4-space indentation for Python, matching `ooh_code/Src/research_pipeline.py`, `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, and `ooh_code/scripts/test_phase08_artifact_gate.py`.
- Use pragmatic line wrapping. Long `argparse` help strings are wrapped with parentheses in `ooh_code/Src/parser.py`; long LaTeX table assembly lines are split into local variables and list fragments in `ooh_code/scripts/build_artifacts.py`.
- Prefer `pathlib.Path` in orchestration, artifact, manuscript, and tests that manipulate files: `ooh_code/Src/research_pipeline.py`, `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, `ooh_code/scripts/build_manuscript.py`, `ooh_code/scripts/test_phase08_artifact_gate.py`, `ooh_code/scripts/test_work2_main_manifest.py`.
- Preserve `os.path` style when editing adjacent legacy scientific code that already uses it: `ooh_code/run_menu_compare.py`, `ooh_code/Src/config.py`, `ooh_code/Src/Utils/Utils.py`, `ooh_code/scripts/test_option_features.py`, `ooh_code/scripts/test_setmenunet.py`.
- Put `matplotlib.use("Agg")` before importing `matplotlib.pyplot` in artifact-generating scripts, as in `ooh_code/scripts/build_artifacts.py`.
- Use `encoding="utf-8"` for explicit file reads and writes in durable workflow code: `read_yaml`, `write_yaml`, `write_csv`, and `write_text` in `ooh_code/Src/research_pipeline.py`; `write_tex_table` in `ooh_code/scripts/build_artifacts.py`.

**Linting:**
- Tool used: Not detected. No configured Python linter exists.
- Keep edits local and avoid project-wide style-only rewrites. The codebase mixes newer orchestration style in `ooh_code/Src/research_pipeline.py` with scientific-core style in `ooh_code/Src/Algorithms/DSPO.py` and `ooh_code/Environments/OOH/Parcelpoint_py.py`.
- Avoid unused imports and duplicated imports when adding code. `ooh_code/scripts/test_work2_artifact_summary.py` contains a duplicated `from copy import deepcopy`; do not copy that pattern.
- Do not rely on pytest fixtures, decorators, or markers in tests unless a test runner dependency and config are intentionally added to `ooh_code/requirements.txt`.

## Import Organization

**Order:**
1. Standard library imports first: `csv`, `hashlib`, `json`, `os`, `re`, `subprocess`, `datetime`, and `pathlib` in `ooh_code/Src/research_pipeline.py`.
2. Third-party imports next: `numpy`, `yaml`, `torch`, `matplotlib`, and `matplotlib.pyplot` in `ooh_code/Src/research_pipeline.py`, `ooh_code/scripts/build_artifacts.py`, and model tests under `ooh_code/scripts/`.
3. Local imports last, using package paths from the `ooh_code/` root: `Src.parser`, `Src.config`, `Src.work2_runtime`, `Src.research_pipeline`, `Environments.OOH.containers`.
- CLI scripts under `ooh_code/scripts/` insert `ooh_code/` into `sys.path` before local imports: `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, `ooh_code/scripts/build_manuscript.py`, `ooh_code/scripts/test_phase6_redesign_policies.py`.
- Keep `sys.path.insert(...)` local to executable scripts. Do not add path mutation in reusable modules under `ooh_code/Src/` or `ooh_code/Environments/OOH/`.

**Path Aliases:**
- Not detected. No configured Python package alias system exists.
- Run scripts from `ooh_code/` when using commands documented in `ooh_code/README.md`, so imports such as `from Src.research_pipeline import ...` and `from Environments.OOH.containers import ...` resolve.

## Error Handling

**Patterns:**
- Use `ValueError` for invalid configuration, unsupported modes, invalid parser overrides, and invalid numeric domains: `parser_namespace_with_overrides` and `execute_study_manifest` in `ooh_code/Src/research_pipeline.py`, optimizer validation in `ooh_code/Src/config.py`, Lambert W domain validation in `ooh_code/Src/Utils/MathUtils.py`, menu-update preconditions in `ooh_code/Src/Algorithms/CNN_SetMenu.py` and `ooh_code/Src/Algorithms/MLP_SetMenu.py`.
- Use `FileNotFoundError` for missing manifests, checkpoints, run directories, and benchmark data: `resolve_manifest` and `train_or_reuse_shared_model` in `ooh_code/Src/research_pipeline.py`, data loading in `ooh_code/Src/Utils/Utils.py`, bootstrap scripts `ooh_code/scripts/bootstrap_rc.py` and `ooh_code/scripts/bootstrap_amazon.py`.
- Use `RuntimeError` for failed external commands or missing derived state where the caller cannot continue: `_git_lines` in `ooh_code/scripts/test_work2_no_paper_changes.py`, extraction scripts such as `ooh_code/scripts/extract_phase8_results.py` and `ooh_code/scripts/extract_phase9_results.py`.
- Use custom `ValueError` subclasses for decision-gate scripts: `GateError` in `ooh_code/scripts/build_phase08_artifacts.py`, `ooh_code/scripts/build_phase08_gap_closure_artifacts.py`, `ooh_code/scripts/build_phase6_redesign_artifacts.py`, and `ooh_code/scripts/build_work2_phase6_redesign_formal_artifacts.py`.
- Use `SystemExit` for CLI stop conditions with direct user-facing messages: missing LaTeX compiler in `ooh_code/scripts/build_manuscript.py`, artifact gate CLI failures in `ooh_code/scripts/build_phase08_artifacts.py`, and manuscript-change guard failures in `ooh_code/scripts/test_work2_no_paper_changes.py`.
- Keep broad `except Exception` blocks only around optional fallback, tolerant cleanup, or partial smoke-test handling: stdout restoration in `ooh_code/run_menu_compare.py`, Git marker and resume scanning in `ooh_code/Src/research_pipeline.py`, and minimal synthetic-data handling in `ooh_code/scripts/test_cnn_setmenu.py`.

## Logging

**Framework:** `print` and redirected stdout through `Utils.Logger`

**Patterns:**
- Use `print` for command-line status summaries: `ooh_code/scripts/run_study.py`, `ooh_code/run_menu_compare.py`, `ooh_code/scripts/build_artifacts.py`, `ooh_code/scripts/build_manuscript.py`, and executable tests under `ooh_code/scripts/test_*.py`.
- Use `Utils.Logger` to redirect runtime training logs when configured by `Config`: `ooh_code/Src/config.py` assigns `sys.stdout = Utils.Logger(...)`, implemented in `ooh_code/Src/Utils/Utils.py`.
- Call or preserve `restore_stdout()` around orchestration code that must return normal CLI output after model training redirects stdout, as implemented in `ooh_code/run_menu_compare.py` and imported by `ooh_code/Src/research_pipeline.py`.
- Store durable experiment state in files rather than relying on console logs: `study_summary.json`, `normalized_rows.json`, and `aggregate_variant_summary.csv` from `ooh_code/Src/research_pipeline.py`; `build_status.json` from `ooh_code/scripts/build_manuscript.py`; artifact snapshots under `ooh_code/artifacts/results_snapshot/`.

## Comments

**When to Comment:**
- Use comments for research assumptions, compatibility constraints, and non-obvious numerical or scientific semantics: `_INCENTIVE_SENS_BETA` in `ooh_code/run_menu_compare.py`, feature-vector layout comments in `ooh_code/Src/Utils/option_features.py`, and manifest contract comments in `ooh_code/experiments/studies/work2_main.yaml`.
- Use comments in tests to explain the requirement ID or scientific contract being guarded, as in `ooh_code/scripts/test_setmenunet.py`, `ooh_code/scripts/test_cnn_setmenu.py`, and `ooh_code/scripts/test_work2_main_manifest.py`.
- Avoid comments that restate simple assignments. Prefer helper names such as `behavior_non_degenerate`, `compute_acceptance_rate`, `resolve_behavior_gate`, and `variant_display_label` in `ooh_code/Src/research_pipeline.py` and `ooh_code/scripts/build_artifacts.py`.

**JSDoc/TSDoc:**
- Not applicable.
- Python docstrings are used for public utility modules and executable smoke tests: `ooh_code/Src/Utils/option_features.py`, `ooh_code/scripts/test_option_features.py`, `ooh_code/scripts/test_setmenunet.py`, and `ooh_code/scripts/test_cnn_setmenu.py`.
- Add docstrings for public helpers with non-obvious input contracts, especially tensor shapes, manifest schema assumptions, or gate outputs. Keep private one-purpose helpers self-documenting through names.

## Function Design

**Size:** Use small pure helpers for orchestration, artifact formatting, validation, and aggregation. `ooh_code/Src/research_pipeline.py` exposes focused helpers such as `slugify`, `behavior_gate`, `read_yaml`, `write_csv`, `manifest_hash`, and `aggregate_rows`; `ooh_code/scripts/build_artifacts.py` uses helpers such as `latex_escape`, `format_metric`, `numeric_key`, and `compute_behavior_non_degenerate`.

**Parameters:** Use explicit keyword-style calls for high-arity workflows. `ooh_code/scripts/run_study.py` calls `execute_study_manifest(manifest, reuse_existing=..., resume_run_id=...)`; gate tests call `phase08.run(["--study-dir", str(study_dir), "--output-dir", str(out_dir)])` in `ooh_code/scripts/test_phase08_artifact_gate.py`.

**Return Values:** Return plain dictionaries and lists for normalized study rows, summaries, gate decisions, and artifact metadata. Examples include `aggregate_episode_metrics` and `paired_summary` in `ooh_code/run_menu_compare.py`, `aggregate_rows` and `execute_study_manifest` in `ooh_code/Src/research_pipeline.py`, and gate `run(...)` functions in `ooh_code/scripts/build_phase08_artifacts.py`.

- Keep CLI `main()` functions thin: parse arguments, call workflow helpers, print concise output. Follow `ooh_code/scripts/run_study.py` and `ooh_code/scripts/build_manuscript.py`.
- Add new CLI runtime settings in `ooh_code/Src/parser.py`; map derived algorithm choices in parser finalization or configuration code rather than hard-coding one-off script behavior.
- Add manifest-driven experiment settings under `base_args`, per-split `args_overrides`, or per-policy `args_overrides` in `ooh_code/experiments/studies/*.yaml`; `parser_namespace_with_overrides` in `ooh_code/Src/research_pipeline.py` validates unknown parser keys.
- Use `None` for unavailable optional metrics in normalized rows. Downstream formatters convert missing values to display placeholders such as `"--"` in `ooh_code/scripts/build_artifacts.py`.

## Module Design

**Exports:** No `__all__` declarations are detected. Modules expose functions and classes by direct import.

**Barrel Files:** Package marker files exist but are not public barrels: `ooh_code/Environments/__init__.py` and `ooh_code/Environments/OOH/__init__.py`.

- Use direct module imports for scientific core classes: `Config` from `ooh_code/Src/config.py`, `Parser` from `ooh_code/Src/parser.py`, `Solver` from `ooh_code/Src/work2_runtime.py`, `DSPO_Menu` from `ooh_code/Src/Algorithms/DSPO_Menu.py`, `CNN_SetMenu` from `ooh_code/Src/Algorithms/CNN_SetMenu.py`, and `MLP_SetMenu` from `ooh_code/Src/Algorithms/MLP_SetMenu.py`.
- Keep reusable study orchestration in `ooh_code/Src/research_pipeline.py`; keep public command wrappers in `ooh_code/scripts/`.
- Keep domain data records in `ooh_code/Environments/OOH/containers.py`; keep simulator behavior in `ooh_code/Environments/OOH/Parcelpoint_py.py`; keep choice logic in `ooh_code/Environments/OOH/customerchoice.py`.
- Keep paper artifact generation in `ooh_code/scripts/build_artifacts.py` and phase-specific artifact gates in dedicated scripts such as `ooh_code/scripts/build_phase08_artifacts.py`, `ooh_code/scripts/build_phase08_gap_closure_artifacts.py`, and `ooh_code/scripts/build_phase6_redesign_artifacts.py`.
- Do not add barrel imports unless a package-level API is intentionally introduced and all script imports are migrated consistently.

## Manuscript, Experiments, and Artifacts

- Use YAML manifests under `ooh_code/experiments/studies/` for executable studies and under `ooh_code/experiments/suites/` for bundles.
- Keep generated artifacts under `ooh_code/artifacts/` and root `artifacts/work2_cnn_setmenunet/`; do not hand-edit generated result rows or generated tables to change conclusions.
- Use `ooh_code/scripts/run_study.py` for manifest execution, `ooh_code/scripts/build_artifacts.py` for result snapshots/tables/figures, and `ooh_code/scripts/build_manuscript.py` for manuscript build preparation.
- Use `ooh_code/scripts/test_work2_no_paper_changes.py` as the manuscript-change guard when a phase must avoid direct edits to `ooh_code/manuscript/`, root `manuscript/`, `.bib`, or non-artifact `.tex` files.

---

*Convention analysis: 2026-06-09*
