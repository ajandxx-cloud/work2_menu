# Technology Stack

**Analysis Date:** 2026-06-09
**last_mapped_commit:** `37b20aa`

## Languages

**Primary:**
- Python 3.10+ - Required runtime for the Work2 research pipeline under `ooh_code/`; the recommended version is documented in `ooh_code/README.md`.

**Secondary:**
- LaTeX - Manuscript source under `ooh_code/manuscript/main.tex`, `ooh_code/manuscript/sections/*.tex`, `ooh_code/manuscript/references.bib`, and the Elsevier template `ooh_code/elsarticle-template-harv.tex`.
- YAML - Study and suite manifests under `ooh_code/experiments/studies/*.yaml` and `ooh_code/experiments/suites/*.yaml`; loaded by `ooh_code/Src/research_pipeline.py`.
- Markdown - Project documentation in `ooh_code/README.md`, `ooh_code/docs/*.md`, `ooh_code/experiments/README.md`, `ooh_code/artifacts/README.md`, and `ooh_code/manuscript/README.md`.
- JSON/CSV/TEX/PNG - Generated research artifacts under `ooh_code/artifacts/results_snapshot/`, `ooh_code/artifacts/tables/`, `ooh_code/artifacts/figures/`, and raw outputs under `ooh_code/outputs/`.
- Plain text and NumPy data files - Bundled benchmark coordinates, distance matrices, and adjacency files under `ooh_code/Environments/OOH/HombergerGehring_data/` and `ooh_code/Environments/OOH/Amazon_data/`.

## Runtime

**Environment:**
- CPython 3.10+ - Create and run the environment from `ooh_code/` using the workflow in `ooh_code/README.md`.
- Optional CUDA through PyTorch - Enabled with `--gpu 1`; device selection is implemented in `ooh_code/Src/config.py`.
- Optional LaTeX toolchain - `latexmk`, `pdflatex`, and optionally `bibtex` are detected by `ooh_code/scripts/build_manuscript.py`.
- Optional Git executable - Used by `ooh_code/Src/research_pipeline.py` to stamp run metadata with `git rev-parse --short HEAD`.

**Package Manager:**
- pip - Dependencies are declared in `ooh_code/requirements.txt`.
- Lockfile: missing. No `requirements.lock`, `poetry.lock`, `Pipfile.lock`, `environment.yml`, or Conda lock file detected.

## Frameworks

**Core:**
- PyTorch `>=2.0.1` - Neural predictors, replay buffers, optimizers, checkpoints, and optional CUDA execution in `ooh_code/Src/Algorithms/DSPO.py`, `ooh_code/Src/Algorithms/DSPO_Menu.py`, `ooh_code/Src/Algorithms/CNN_SetMenu.py`, `ooh_code/Src/Algorithms/MLP_SetMenu.py`, `ooh_code/Src/Utils/Predictors.py`, `ooh_code/Src/Utils/CNNSetMenuNet.py`, and `ooh_code/Src/Utils/MLPMenuNet.py`.
- NumPy `~=1.25.1` - Numeric arrays, random sampling, route matrices, bootstrapping, aggregation, and artifact plotting throughout `ooh_code/Src/`, `ooh_code/Environments/OOH/`, and `ooh_code/scripts/`.
- Hygese `~=0.0.0.8` - Hybrid genetic search routing solver used in `ooh_code/Src/Algorithms/DSPO.py` and `ooh_code/Environments/OOH/env_utils.py`.
- PyYAML `>=6.0` - Reads study manifests and writes run snapshots in `ooh_code/Src/research_pipeline.py` and `ooh_code/Src/config.py`.
- Matplotlib `~=3.7.2` - Training curves and paper figures in `ooh_code/Src/Utils/Utils.py` and `ooh_code/scripts/build_artifacts.py`; `ooh_code/scripts/build_artifacts.py` uses the noninteractive `Agg` backend.

**Testing:**
- No dedicated test runner dependency is declared in `ooh_code/requirements.txt`.
- Script-style tests exist under `ooh_code/scripts/test_*.py`, including `ooh_code/scripts/test_menu_objective_mode.py`, `ooh_code/scripts/test_option_features.py`, `ooh_code/scripts/test_cnn_setmenu.py`, and `ooh_code/scripts/test_work2_robustness_manifests.py`.
- Smoke verification is workflow-based through manifests such as `ooh_code/experiments/studies/smoke_rc.yaml`, `ooh_code/experiments/studies/smoke_austin.yaml`, and `ooh_code/experiments/studies/smoke_baselines.yaml`.

**Build/Dev:**
- `argparse` command-line interfaces - Main entry points are `ooh_code/run_menu_compare.py`, `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, `ooh_code/scripts/build_manuscript.py`, and `ooh_code/scripts/run_baseline_smoke.py`.
- LaTeX build tools - `ooh_code/scripts/build_manuscript.py` runs `latexmk` when available, falls back to `pdflatex`, and runs `bibtex` when present.
- Git metadata detection - `ooh_code/Src/research_pipeline.py` calls `git rev-parse --short HEAD`; when Git metadata is unavailable it hashes selected source files under `ooh_code/Src/`, `ooh_code/Environments/OOH/`, `ooh_code/run_menu_compare.py`, and `ooh_code/requirements.txt`.
- Matplotlib artifact generation - `ooh_code/scripts/build_artifacts.py` writes committed figures under `ooh_code/artifacts/figures/` and mirrored Work2 standard artifacts under root `artifacts/work2_cnn_setmenunet/`.

## Key Dependencies

**Critical:**
- `torch>=2.0.1` - Required for CNN, SetMenuNet, MLP, and linear predictor implementations plus checkpoint save/load.
- `numpy~=1.25.1` - Required for simulator state, bundled demand data loading, MNL metrics, rank diagnostics, and aggregation.
- `hygese~=0.0.0.8` - Required for intermediate and final HGS route optimization in `ooh_code/Environments/OOH/env_utils.py` and `ooh_code/Src/Algorithms/DSPO.py`.
- `pyyaml>=6.0` - Required for manifest execution and saved `args.yaml` / `manifest_snapshot.yaml` files.
- `matplotlib~=3.7.2` - Required for generated training curves and publication figures.

**Infrastructure:**
- Standard library `subprocess` - Used for Git marker detection in `ooh_code/Src/research_pipeline.py`, manuscript compilation in `ooh_code/scripts/build_manuscript.py`, robustness orchestration in `ooh_code/scripts/run_work2_robustness_closure.py`, and paper-change checks in `ooh_code/scripts/test_work2_no_paper_changes.py`.
- Standard library `csv`, `json`, `hashlib`, `pathlib`, `datetime`, and `argparse` - Used for manifest hashes, run IDs, normalized summaries, command-line workflows, and reproducible artifact metadata in `ooh_code/Src/research_pipeline.py`, `ooh_code/run_menu_compare.py`, and `ooh_code/scripts/*.py`.
- Optional SciPy - Not declared in `ooh_code/requirements.txt`; `ooh_code/Src/Utils/MathUtils.py` imports `scipy.special.lambertw` when installed and otherwise uses an internal principal-branch Lambert W implementation.
- Optional LaTeX binaries - `latexmk`, `pdflatex`, and `bibtex` are external executables invoked from `ooh_code/scripts/build_manuscript.py`.

## Configuration

**Environment:**
- Environment-variable configuration: Not detected.
- `.env` files: Not detected in the repository root or `ooh_code/`.
- Runtime configuration is CLI-driven in `ooh_code/Src/parser.py`; important options include `--instance`, `--data_seed`, `--data_seed_test`, `--max_episodes`, `--eval_episodes`, `--gpu`, `--menu_policy`, `--menu_k`, `--menu_model`, `--menu_pricing_mode`, `--hgs_reopt_time`, and `--hgs_final_time`.
- Study configuration is YAML-driven through `ooh_code/experiments/studies/*.yaml`; suite configuration is YAML-driven through `ooh_code/experiments/suites/*.yaml`.
- Run configuration snapshots are written under `ooh_code/outputs/` as `args.yaml`, `manifest_snapshot.yaml`, `study_summary.json`, `normalized_rows.json`, and related CSV/JSON outputs by `ooh_code/Src/config.py` and `ooh_code/Src/research_pipeline.py`.

**Build:**
- Dependency manifest: `ooh_code/requirements.txt`.
- Main research runner: `ooh_code/run_menu_compare.py`.
- Study orchestration: `ooh_code/scripts/run_study.py`.
- Baseline smoke runner: `ooh_code/scripts/run_baseline_smoke.py`.
- Artifact build: `ooh_code/scripts/build_artifacts.py`.
- Manuscript build: `ooh_code/scripts/build_manuscript.py`.
- Manuscript entry point: `ooh_code/manuscript/main.tex`.
- Artifact outputs: `ooh_code/artifacts/results_snapshot/`, `ooh_code/artifacts/tables/`, `ooh_code/artifacts/figures/`, and root `artifacts/work2_cnn_setmenunet/`.
- Raw run outputs: `ooh_code/outputs/studies/`, `ooh_code/outputs/shared_training/`, and `ooh_code/outputs/menu_compare/`; `ooh_code/.gitignore` excludes `outputs/`.

## Platform Requirements

**Development:**
- Work from `ooh_code/` for documented commands so imports like `Src.research_pipeline`, `Src.config`, and `Environments.OOH.Parcelpoint_py` resolve consistently.
- Create a virtual environment and install `ooh_code/requirements.txt` with `python -m pip install -r requirements.txt`.
- Keep bundled benchmark data available under `ooh_code/Environments/OOH/HombergerGehring_data/` for `C`, `R`, and `RC` instances and under `ooh_code/Environments/OOH/Amazon_data/` for `Austin` and `Seattle` instances.
- Install a LaTeX compiler only when compiling the manuscript PDF; `python scripts/build_manuscript.py --skip_compile` still refreshes linked artifacts and build metadata.

**Production:**
- Not applicable as a hosted application. The repository is a local/offline research codebase.
- Public-facing deliverables are committed research artifacts under `ooh_code/artifacts/`, mirrored Work2 artifacts under root `artifacts/work2_cnn_setmenunet/`, and manuscript files under `ooh_code/manuscript/`.
- Raw generated outputs under `ooh_code/outputs/` are local experiment state and are excluded by `ooh_code/.gitignore`.

---

*Stack analysis: 2026-06-09*
