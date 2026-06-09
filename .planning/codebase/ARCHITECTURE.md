<!-- refreshed: 2026-06-09 -->
<!-- last_mapped_commit: 37b20aa -->
# Architecture

**Analysis Date:** 2026-06-09

## System Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                 Research Workflow Entry Points              │
├──────────────────┬──────────────────┬───────────────────────┤
│ Direct runner    │ Study runner     │ Artifact/manuscript   │
│ `ooh_code/run_   │ `ooh_code/       │ `ooh_code/scripts/    │
│ menu_compare.py` │ scripts/run_     │ build_artifacts.py`,  │
│                  │ study.py`        │ `build_manuscript.py` │
└────────┬─────────┴────────┬─────────┴──────────┬────────────┘
         │                  │                     │
         ▼                  ▼                     ▼
┌─────────────────────────────────────────────────────────────┐
│             Manifest and Experiment Orchestration            │
│ `ooh_code/Src/research_pipeline.py`                          │
│ `ooh_code/experiments/studies/*.yaml`                        │
│ `ooh_code/experiments/suites/*.yaml`                         │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                 Runtime Configuration and Solver             │
│ `ooh_code/Src/parser.py`, `ooh_code/Src/config.py`,          │
│ `ooh_code/Src/work2_runtime.py`                              │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│             Algorithm, Simulator, Choice, and Routing         │
│ `ooh_code/Src/Algorithms/*.py`                               │
│ `ooh_code/Environments/OOH/*.py`                             │
│ `ooh_code/Src/Utils/*.py`                                    │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│        Raw Outputs, Committed Artifacts, and Manuscript       │
│ `ooh_code/outputs/`, `ooh_code/artifacts/`,                  │
│ `artifacts/work2_cnn_setmenunet/`, `ooh_code/manuscript/`    │
└─────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

| Component | Responsibility | File |
|-----------|----------------|------|
| Low-level comparison runner | Trains or loads a shared predictor, replays request traces, evaluates policies, aggregates paired metrics, and writes JSON comparison outputs. | `ooh_code/run_menu_compare.py` |
| Study pipeline | Resolves study/suite manifests, creates parser namespaces, trains/reuses checkpoints, freezes policy variants, writes normalized rows, and persists resumable summaries. | `ooh_code/Src/research_pipeline.py` |
| Study CLI | Parses `--study`, retrain, and resume flags, then delegates all execution to the study pipeline. | `ooh_code/scripts/run_study.py` |
| Artifact builder | Loads latest study or suite summaries and writes JSON/CSV snapshots, LaTeX tables, PNG figures, and root standard artifacts. | `ooh_code/scripts/build_artifacts.py` |
| Manuscript builder | Rebuilds artifacts, detects LaTeX tooling, runs `latexmk` or `pdflatex`, and writes build metadata. | `ooh_code/scripts/build_manuscript.py` |
| Argument schema | Defines experiment, menu, pricing, choice, routing, model, and output flags; finalizes legacy aliases. | `ooh_code/Src/parser.py` |
| Configuration factory | Builds output paths, loads demand data, creates train/test environments, selects algorithm class, and configures device/optimizer. | `ooh_code/Src/config.py` |
| Runtime solver | Owns training episodes, model reset/action/update calls, checkpoint cadence, and learned model instantiation. | `ooh_code/Src/work2_runtime.py` |
| Base DSPO algorithm | Provides legacy insertion-cost prediction, Lambert-W pricing, replay memory, HGS final re-optimization, and CNN/linear predictor training. | `ooh_code/Src/Algorithms/DSPO.py` |
| Set-menu model algorithm | Intended CNN-SetMenuNet algorithm subclass that predicts per-candidate costs from spatial state plus set features. | `ooh_code/Src/Algorithms/CNN_SetMenu.py` |
| MLP menu baseline | Intended MLP baseline subclass for option-feature-only cost prediction. | `ooh_code/Src/Algorithms/MLP_SetMenu.py` |
| Agent base | Handles neural module initialization, save/load, train/eval mode, and generic optimizer helpers. | `ooh_code/Src/Algorithms/Agent.py` |
| OOH simulator | Generates requests, applies passenger choice, mutates route/fleet/capacity state, logs menu decisions, and supports replay traces. | `ooh_code/Environments/OOH/Parcelpoint_py.py` |
| Choice model | Applies Gumbel-noise MNL utility over displayed `MenuOffer` options plus the outside option. | `ooh_code/Environments/OOH/customerchoice.py` |
| Routing utilities | Computes cheapest insertion, HGS re-optimization, fleet reset, parcel-point reset, and route travel cost. | `ooh_code/Environments/OOH/env_utils.py` |
| Domain containers | Defines dataclasses for locations, vehicles, customers, service bundles, and menu offers. | `ooh_code/Environments/OOH/containers.py` |
| Neural utilities | Provides CNN/MLP/set-menu models, option feature tensors, math fallback, data loading, logging, and replay memory. | `ooh_code/Src/Utils/` |
| Study manifests | Declare study type, reference policy, base args, policy variants, splits, behavior gates, and suite membership. | `ooh_code/experiments/studies/*.yaml`, `ooh_code/experiments/suites/*.yaml` |
| Manuscript and paper assets | Store generated artifact inputs and LaTeX source for the TR Part E paper draft. | `ooh_code/artifacts/`, `artifacts/work2_cnn_setmenunet/`, `ooh_code/manuscript/` |

## Pattern Overview

**Overall:** Manifest-driven offline research pipeline around a stateful DRT simulator.

**Key Characteristics:**
- Use YAML manifests in `ooh_code/experiments/studies/*.yaml` and `ooh_code/experiments/suites/*.yaml` as the source of truth for reproducible studies.
- Use shared-predictor training followed by frozen replay evaluation through `ooh_code/Src/research_pipeline.py` and `ooh_code/run_menu_compare.py`.
- Keep menu policy/model changes inside `ooh_code/Src/Algorithms/` and simulator/choice semantics inside `ooh_code/Environments/OOH/`.
- Generate paper-facing artifacts from normalized outputs with `ooh_code/scripts/build_artifacts.py`; do not hand-edit generated result snapshots.
- Treat `ooh_code/outputs/` as raw local run state and `ooh_code/artifacts/` plus `artifacts/work2_cnn_setmenunet/` as lightweight committed deliverables.

## Layers

**Repository Shell:**
- Purpose: Holds GSD planning metadata, publication notes, legacy artifacts, and the runnable Work2 package.
- Location: `.`
- Contains: `AGENTS.md`, `CLAUDE.md`, `.planning/`, `ooh_code/`, `artifacts/`, `qi_wei/`, `2025.9.11-pom_big price/`, `实验讨论5.26.md`
- Depends on: Local filesystem and git metadata.
- Used by: Planning workflows and author-facing publication work.

**Research Package:**
- Purpose: Provides the runnable Python/LaTeX project.
- Location: `ooh_code/`
- Contains: `ooh_code/README.md`, `ooh_code/requirements.txt`, `ooh_code/run_menu_compare.py`, `ooh_code/Src/`, `ooh_code/Environments/`, `ooh_code/experiments/`, `ooh_code/scripts/`, `ooh_code/artifacts/`, `ooh_code/manuscript/`
- Depends on: Python, NumPy, PyTorch, Hygese, PyYAML, Matplotlib, optional LaTeX.
- Used by: All experiment, artifact, and manuscript workflows.

**CLI and Workflow Layer:**
- Purpose: Gives users executable entry points for direct comparisons, manifest studies, artifact builds, and manuscript builds.
- Location: `ooh_code/run_menu_compare.py`, `ooh_code/scripts/`
- Contains: `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, `ooh_code/scripts/build_manuscript.py`, `ooh_code/scripts/check_manuscript.py`, `ooh_code/scripts/run_work2_robustness_closure.py`
- Depends on: `ooh_code/Src/research_pipeline.py`, `ooh_code/Src/parser.py`, `ooh_code/Src/config.py`
- Used by: README workflows in `ooh_code/README.md` and protocol docs in `ooh_code/docs/WORK2_EXPERIMENT_PROTOCOL.md`.

**Orchestration Layer:**
- Purpose: Converts manifest definitions into train/evaluate/output phases with normalized schemas.
- Location: `ooh_code/Src/research_pipeline.py`
- Contains: Manifest resolution, parser override validation, checkpoint reuse, request trace generation, variant loops, aggregate rows, suite runs, and resumable summaries.
- Depends on: `ooh_code/Src/parser.py`, `ooh_code/Src/config.py`, `ooh_code/Src/work2_runtime.py`, `ooh_code/run_menu_compare.py`
- Used by: `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, `ooh_code/scripts/build_manuscript.py`, and extraction scripts under `ooh_code/scripts/`.

**Runtime Layer:**
- Purpose: Builds configured environments and algorithms, then executes train/eval episode loops.
- Location: `ooh_code/Src/config.py`, `ooh_code/Src/parser.py`, `ooh_code/Src/work2_runtime.py`
- Contains: Argument defaults, derived aliases, output path construction, train/test environment construction, device and optimizer selection, solver loop.
- Depends on: `ooh_code/Environments/OOH/Parcelpoint_py.py`, `ooh_code/Src/Algorithms/*.py`, `ooh_code/Src/Utils/Utils.py`
- Used by: `ooh_code/run_menu_compare.py` and `ooh_code/Src/research_pipeline.py`.

**Algorithm Layer:**
- Purpose: Builds service menus, predicts operational signals, trains predictors, computes prices, and selects displayed alternatives.
- Location: `ooh_code/Src/Algorithms/`
- Contains: `ooh_code/Src/Algorithms/DSPO.py`, `ooh_code/Src/Algorithms/CNN_SetMenu.py`, `ooh_code/Src/Algorithms/MLP_SetMenu.py`, `ooh_code/Src/Algorithms/Agent.py`
- Depends on: `ooh_code/Src/Utils/`, `ooh_code/Environments/OOH/containers.py`, PyTorch, NumPy, Hygese.
- Used by: `ooh_code/Src/config.py` through `Config.algo`.

**Simulator and Routing Layer:**
- Purpose: Encodes request generation, state transitions, MNL choice, capacity mutation, route insertion, and HGS route-cost realization.
- Location: `ooh_code/Environments/OOH/`
- Contains: `ooh_code/Environments/OOH/Parcelpoint_py.py`, `ooh_code/Environments/OOH/customerchoice.py`, `ooh_code/Environments/OOH/env_utils.py`, `ooh_code/Environments/OOH/containers.py`
- Depends on: `ooh_code/Src/Utils/Utils.py`, Hygese, NumPy, bundled demand data.
- Used by: `ooh_code/Src/config.py` and algorithm update/evaluation paths.

**Utility and Model Layer:**
- Purpose: Supplies reusable neural modules, option feature schema, numerical fallback, data loading, HGS helpers, logging, and replay buffers.
- Location: `ooh_code/Src/Utils/`
- Contains: `ooh_code/Src/Utils/Predictors.py`, `ooh_code/Src/Utils/CNNSetMenuNet.py`, `ooh_code/Src/Utils/SetMenuNet.py`, `ooh_code/Src/Utils/MLPMenuNet.py`, `ooh_code/Src/Utils/option_features.py`, `ooh_code/Src/Utils/MathUtils.py`, `ooh_code/Src/Utils/Utils.py`
- Depends on: PyTorch, NumPy, Matplotlib, optional SciPy behavior in `ooh_code/Src/Utils/MathUtils.py`.
- Used by: `ooh_code/Src/Algorithms/*.py`, `ooh_code/Src/config.py`, and environment utilities.

**Output and Publication Layer:**
- Purpose: Separates raw generated experiment state from committed summaries, figures, tables, and manuscript source.
- Location: `ooh_code/outputs/`, `ooh_code/artifacts/`, `artifacts/work2_cnn_setmenunet/`, `ooh_code/manuscript/`
- Contains: `ooh_code/outputs/studies/`, `ooh_code/outputs/shared_training/`, `ooh_code/artifacts/results_snapshot/`, `ooh_code/artifacts/tables/`, `ooh_code/artifacts/figures/`, `ooh_code/manuscript/main.tex`, `ooh_code/manuscript/sections/*.tex`
- Depends on: `ooh_code/scripts/build_artifacts.py` and `ooh_code/scripts/build_manuscript.py`.
- Used by: Paper writing, verification, and archival workflows.

## Data Flow

### Manifest-Driven Study Path

1. User runs `python scripts/run_study.py --study <name>` from `ooh_code/` (`ooh_code/scripts/run_study.py:13`).
2. `load_manifest()` resolves a study or suite from `ooh_code/experiments/studies/` or `ooh_code/experiments/suites/` (`ooh_code/Src/research_pipeline.py:321`).
3. `execute_study_manifest()` creates or resumes `ooh_code/outputs/studies/<study>/<run_id>/` and writes `manifest_snapshot.yaml` (`ooh_code/Src/research_pipeline.py:684`).
4. `build_study_args()` merges manifest `base_args`, split overrides, and variant overrides into parser args (`ooh_code/Src/research_pipeline.py:362`).
5. `train_or_reuse_shared_model()` builds `Config`, runs `Solver.train()` if needed, and requires `supervised_ml.pt` under `ooh_code/outputs/shared_training/` (`ooh_code/Src/research_pipeline.py:390`).
6. `generate_request_traces()` builds an eval solver and obtains replayable test-environment traces (`ooh_code/Src/research_pipeline.py:421`).
7. Each variant builds a frozen solver and calls `evaluate_policy()` with a policy tag and `menu_k` (`ooh_code/Src/research_pipeline.py:819`).
8. `aggregate_episode_metrics()` and `paired_summary()` produce per-variant and paired rows (`ooh_code/run_menu_compare.py:514`, `ooh_code/run_menu_compare.py:640`).
9. The pipeline writes `normalized_rows.json`, `normalized_rows.csv`, `aggregate_variant_summary.json`, `aggregate_variant_summary.csv`, and `study_summary.json` (`ooh_code/Src/research_pipeline.py:719`).

### Direct Low-Level Comparison

1. User runs `python run_menu_compare.py` with CLI flags from `ooh_code/` (`ooh_code/run_menu_compare.py:717`).
2. `Parser.finalize_args()` derives legacy aliases and selects `algo_name` from `menu_model` (`ooh_code/Src/parser.py:559`).
3. `Config` loads train/test data, constructs train/test `Parcelpoint_py` environments, and selects `Config.algo` (`ooh_code/Src/config.py:14`).
4. `Solver.train()` loops over environment episodes, calls `model.get_action()`, `env.step()`, and `model.update()` (`ooh_code/Src/work2_runtime.py:20`).
5. `evaluate_policy()` replays the same request traces on `solver.test_env`, invokes `model.get_action()`, and evaluates final travel cost with `reopt_for_eval()` (`ooh_code/run_menu_compare.py:662`).
6. JSON files are saved under `ooh_code/outputs/menu_compare/<run_name>/<seed>/` (`ooh_code/run_menu_compare.py:713`).

### Simulator Step Path

1. `Solver` obtains a state from `Parcelpoint_py.reset()` as `[Customer, Fleet, ParcelPoints, steps]` (`ooh_code/Src/work2_runtime.py:10`, `ooh_code/Environments/OOH/Parcelpoint_py.py:124`).
2. The algorithm returns a menu action, intended as a list of `MenuOffer` instances from `ooh_code/Environments/OOH/containers.py`.
3. `Parcelpoint_py.step()` passes the action to `customerchoice_menu()`, logs displayed offers and the chosen offer, mutates price/discount arrays, route data, parcel-point capacity, and fleet route plans (`ooh_code/Environments/OOH/Parcelpoint_py.py:386`).
4. `customerchoice_menu()` computes utilities for each displayed offer plus an outside option, samples Gumbel noise, and returns either home, a meeting point, or opt-out metadata (`ooh_code/Environments/OOH/customerchoice.py:24`).
5. `utils_env.cheapestInsertionRoute()` inserts accepted locations into the current fleet and `utils_env.reopt_HGS()` periodically or finally re-optimizes routes with Hygese (`ooh_code/Environments/OOH/env_utils.py:61`, `ooh_code/Environments/OOH/env_utils.py:94`).

### Artifact and Manuscript Path

1. User runs `python scripts/build_artifacts.py --study <name>` from `ooh_code/` (`ooh_code/scripts/build_artifacts.py`).
2. `pick_summary_bundle()` loads the latest study or suite summary through `load_study_summary()` (`ooh_code/scripts/build_artifacts.py:105`).
3. Artifact code writes to `ooh_code/artifacts/results_snapshot/`, `ooh_code/artifacts/tables/`, `ooh_code/artifacts/figures/`, and mirrored standard artifacts under `artifacts/work2_cnn_setmenunet/` (`ooh_code/scripts/build_artifacts.py:35`).
4. `python scripts/build_manuscript.py` runs artifact generation first, then compiles `ooh_code/manuscript/main.tex` when a LaTeX compiler is present (`ooh_code/scripts/build_manuscript.py:10`, `ooh_code/scripts/build_manuscript.py:85`).

**State Management:**
- Simulator state is mutable and object-based in `ooh_code/Environments/OOH/Parcelpoint_py.py`.
- Algorithm training state, replay buffers, and neural modules are mutable inside `ooh_code/Src/Algorithms/*.py`.
- Study-level durable state is file-based under `ooh_code/outputs/studies/` and `ooh_code/outputs/shared_training/`.
- Paper-facing state is generated into `ooh_code/artifacts/` and `artifacts/work2_cnn_setmenunet/`.

## Key Abstractions

**Manifest:**
- Purpose: Declarative experiment contract for studies and suites.
- Examples: `ooh_code/experiments/studies/work2_main.yaml`, `ooh_code/experiments/studies/smoke_work2_main.yaml`, `ooh_code/experiments/suites/work2_robustness.yaml`
- Pattern: Keep new study definitions in YAML and let `ooh_code/Src/research_pipeline.py` validate parser overrides.

**Parser Namespace:**
- Purpose: Runtime configuration object shared by `Config`, `Solver`, and artifact metadata.
- Examples: `ooh_code/Src/parser.py`, `ooh_code/Src/research_pipeline.py:334`
- Pattern: Add CLI/runtime options to `Parser`, then use manifest `base_args` or `args_overrides` to set them.

**Config:**
- Purpose: Converts args into paths, data arrays, environments, algorithm class, device, and optimizer.
- Examples: `ooh_code/Src/config.py`
- Pattern: Keep environment construction in `Config.build_environment()` and avoid duplicating data loading in scripts.

**Solver:**
- Purpose: Owns episode loops while delegating policy behavior to algorithms and transitions to environments.
- Examples: `ooh_code/Src/work2_runtime.py`
- Pattern: Add algorithm behavior to `ooh_code/Src/Algorithms/`; keep `Solver` as orchestration glue.

**MenuOffer and ServiceBundle:**
- Purpose: Typed contract between menu algorithms, MNL choice, simulator logging, and metric extraction.
- Examples: `ooh_code/Environments/OOH/containers.py`
- Pattern: Put new displayed-offer metadata into `MenuOffer.metadata` when it is diagnostic rather than core state.

**Option Feature Tensor:**
- Purpose: Central six-column candidate feature schema for SetMenuNet, CNN-SetMenuNet, and MLP-Menu style models.
- Examples: `ooh_code/Src/Utils/option_features.py`, `ooh_code/Src/Utils/CNNSetMenuNet.py`
- Pattern: Preserve row 0 as home and use `option_mask` for padding.

**Normalized Row:**
- Purpose: Stable machine-readable schema for studies, artifacts, and manuscript tables.
- Examples: `ooh_code/Src/research_pipeline.py`, `ooh_code/scripts/build_artifacts.py`
- Pattern: Add new metrics to `SUMMARY_NUMERIC_KEYS` and `CSV_FIELD_ORDER` in `ooh_code/Src/research_pipeline.py` before consuming them in artifacts.

## Entry Points

**Low-Level Comparison:**
- Location: `ooh_code/run_menu_compare.py`
- Triggers: `python run_menu_compare.py`
- Responsibilities: Train or load one checkpoint, evaluate full display and optimized menus, run menu-size robustness, and write JSON outputs.

**Manifest Study Runner:**
- Location: `ooh_code/scripts/run_study.py`
- Triggers: `python scripts/run_study.py --study <study-or-suite>`
- Responsibilities: Load manifests, resume or start runs, execute studies/suites, and print output roots.

**Artifact Builder:**
- Location: `ooh_code/scripts/build_artifacts.py`
- Triggers: `python scripts/build_artifacts.py --study <study-or-suite>`
- Responsibilities: Convert latest normalized outputs into committed snapshots, tables, figures, and summary prose.

**Manuscript Builder:**
- Location: `ooh_code/scripts/build_manuscript.py`
- Triggers: `python scripts/build_manuscript.py`
- Responsibilities: Refresh artifacts, compile `ooh_code/manuscript/main.tex`, and write `ooh_code/manuscript/build/build_status.json`.

**Smoke and Regression Scripts:**
- Location: `ooh_code/scripts/test_*.py`, `ooh_code/scripts/run_baseline_smoke.py`
- Triggers: Direct `python scripts/test_*.py` invocations.
- Responsibilities: Validate manifests, artifact gates, model tensor behavior, and no-paper-change constraints.

## Architectural Constraints

- **Threading:** Execution is single-process Python loops in `ooh_code/Src/work2_runtime.py`; Hygese calls in `ooh_code/Environments/OOH/env_utils.py` and `ooh_code/Src/Algorithms/DSPO.py` are synchronous.
- **Global state:** `Config` redirects `sys.stdout` to `Utils.Logger` in `ooh_code/Src/config.py`; orchestration must call `restore_stdout()` from `ooh_code/run_menu_compare.py` after constructing configs.
- **Mutable simulation state:** `Parcelpoint_py` mutates `fleet`, `parcelPoints`, `data`, `menu_history`, and RNGs in `ooh_code/Environments/OOH/Parcelpoint_py.py`; replay fairness depends on `set_request_trace()` and deterministic seeding.
- **Import path:** Scripts under `ooh_code/scripts/` insert `ooh_code/` into `sys.path`; run Python commands from `ooh_code/` so imports like `Src.research_pipeline` and `run_menu_compare` resolve.
- **Missing base menu module:** `ooh_code/Src/config.py`, `ooh_code/Src/Algorithms/CNN_SetMenu.py`, and `ooh_code/Src/Algorithms/MLP_SetMenu.py` import `Src.Algorithms.DSPO_Menu`, but `ooh_code/Src/Algorithms/DSPO_Menu.py` is not present in the current worktree. Any path importing `Config`, `CNN_SetMenu`, or `MLP_SetMenu` requires this module to exist or the imports to be repaired.
- **Routing backend:** Route realization is HGS/Hygese-based in `ooh_code/Environments/OOH/env_utils.py` and `ooh_code/Src/Algorithms/DSPO.py`; do not replace routing semantics while changing menu policy logic.
- **Choice backend:** Outside-option MNL behavior lives in `ooh_code/Environments/OOH/customerchoice.py`; keep choice semantics stable unless a phase explicitly changes them.

## Anti-Patterns

### Bypassing Manifests For Paper Experiments

**What happens:** New comparisons are encoded directly in ad hoc scripts under `ooh_code/scripts/`.
**Why it's wrong:** `ooh_code/Src/research_pipeline.py` is the source for shared-checkpoint, replay-trace, and normalized-row fairness.
**Do this instead:** Add a study YAML in `ooh_code/experiments/studies/` or a suite YAML in `ooh_code/experiments/suites/`, then run `ooh_code/scripts/run_study.py`.

### Editing Generated Results By Hand

**What happens:** Rows or tables under `ooh_code/artifacts/` or `artifacts/work2_cnn_setmenunet/` are changed directly.
**Why it's wrong:** The manuscript pipeline expects artifacts to flow from `ooh_code/outputs/studies/` through `ooh_code/scripts/build_artifacts.py`.
**Do this instead:** Change manifests, code, or artifact builders, rerun the study or builder, and let outputs regenerate.

### Adding Menu Fields Outside `MenuOffer`

**What happens:** Algorithms pass raw dicts or parallel arrays to the simulator.
**Why it's wrong:** `customerchoice_menu()` and `_log_menu_decision()` expect `MenuOffer` attributes from `ooh_code/Environments/OOH/containers.py`.
**Do this instead:** Extend `MenuOffer.metadata` for diagnostics or the dataclasses in `ooh_code/Environments/OOH/containers.py` for core contract changes.

### Relying On Missing `DSPO_Menu`

**What happens:** New work assumes `menu_model: cnn_2d`, `cnn_setmenu`, or `mlp_menu` can instantiate while `ooh_code/Src/Algorithms/DSPO_Menu.py` is absent.
**Why it's wrong:** `ooh_code/Src/config.py` imports `DSPO_Menu` at module import time, so the runtime can fail before a study starts.
**Do this instead:** Restore or replace `ooh_code/Src/Algorithms/DSPO_Menu.py`, or change `ooh_code/Src/config.py`, `ooh_code/Src/Algorithms/CNN_SetMenu.py`, and `ooh_code/Src/Algorithms/MLP_SetMenu.py` to subclass an existing implemented base with equivalent menu methods.

## Error Handling

**Strategy:** Fail fast for invalid configuration, tolerate optional tooling and resumable workflow state.

**Patterns:**
- Use `ValueError` for unknown manifest parser overrides in `ooh_code/Src/research_pipeline.py` and invalid optimizer names in `ooh_code/Src/config.py`.
- Use `FileNotFoundError` when required manifests or checkpoints are absent in `ooh_code/Src/research_pipeline.py`.
- Use `SystemExit` for missing LaTeX compiler conditions in `ooh_code/scripts/build_manuscript.py`.
- Use tolerant `try/except Exception` only around optional stdout cleanup, git marker detection, resume scanning, and optional checkpoint warm-start behavior in `ooh_code/run_menu_compare.py`, `ooh_code/Src/research_pipeline.py`, and `ooh_code/Src/Algorithms/CNN_SetMenu.py`.

## Cross-Cutting Concerns

**Logging:** Use `print` for CLI status in `ooh_code/scripts/*.py`; runtime training logs are redirected by `Utils.Logger` from `ooh_code/Src/Utils/Utils.py` through `ooh_code/Src/config.py`.

**Validation:** Use parser choices in `ooh_code/Src/parser.py` and manifest override validation in `ooh_code/Src/research_pipeline.py`; artifact gates live in `ooh_code/scripts/test_*artifact*py`.

**Authentication:** Not applicable. The codebase is a local/offline research pipeline with no detected auth layer.

**Reproducibility:** Preserve shared checkpoint reuse, request trace replay, manifest snapshots, manifest hashes, and code version markers in `ooh_code/Src/research_pipeline.py`.

---

*Architecture analysis: 2026-06-09*
