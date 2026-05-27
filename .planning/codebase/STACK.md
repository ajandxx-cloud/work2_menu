# Technology Stack

**Analysis Date:** 2026-05-27

## Languages

**Primary:**
- Python 3.10+ - Required runtime for the Work2 research pipeline under `ooh_code/`; recommended in `ooh_code/README.md`.
- LaTeX - Manuscript source under `ooh_code/manuscript/main.tex`, `ooh_code/manuscript/sections/*.tex`, and `ooh_code/manuscript/references.bib`.
- YAML - Study and suite manifests under `ooh_code/experiments/studies/*.yaml` and `ooh_code/experiments/suites/*.yaml`.

**Secondary:**
- Markdown - Project documentation and research notes in `ooh_code/README.md`, `ooh_code/docs/*.md`, `ooh_code/experiments/README.md`, `ooh_code/artifacts/README.md`, `ooh_code/manuscript/README.md`, and root notes such as `实验讨论5.26.md`.
- JSON/CSV/TEX/PNG artifacts - Generated or committed research outputs under `ooh_code/artifacts/results_snapshot/`, `ooh_code/artifacts/tables/`, and `ooh_code/artifacts/figures/`.
- Plain text benchmark data - Bundled coordinate and distance files under `ooh_code/Environments/OOH/HombergerGehring_data/` and `ooh_code/Environments/OOH/Amazon_data/`.

## Runtime

**Environment:**
- CPython 3.10+ - Install and run from `ooh_code/` with `python -m pip install -r requirements.txt`.
- Optional CUDA through PyTorch - Enabled by `--gpu 1`; device selection is implemented in `ooh_code/Src/config.py`.
- Optional LaTeX toolchain - `latexmk`, `pdflatex`, and optionally `bibtex` are detected by `ooh_code/scripts/build_manuscript.py`.
- Optional Git executable - Used only for code-version marker detection in `ooh_code/Src/research_pipeline.py`.

**Package Manager:**
- pip - Dependencies are declared in `ooh_code/requirements.txt`.
- Lockfile: missing. No `requirements.lock`, `poetry.lock`, `Pipfile.lock`, or Conda environment file detected.

## Frameworks

**Core:**
- PyTorch `>=2.0.1` - Neural predictors, replay buffers, optimizers, model checkpointing, and optional CUDA execution in `ooh_code/Src/Algorithms/DSPO.py`, `ooh_code/Src/Algorithms/DSPO_Menu.py`, `ooh_code/Src/Utils/Predictors.py`, and `ooh_code/Src/Utils/Utils.py`.
- NumPy `~=1.25.1` - Numeric arrays, random sampling, distance matrices, bootstrap routines, and experiment aggregation throughout `ooh_code/Src/`, `ooh_code/Environments/OOH/`, and `ooh_code/scripts/`.
- Hygese `~=0.0.0.8` - Hybrid genetic search routing solver used in `ooh_code/Src/Algorithms/DSPO.py` and `ooh_code/Environments/OOH/env_utils.py`.
- PyYAML `>=6.0` - Reads study manifests and writes run snapshots in `ooh_code/Src/research_pipeline.py` and `ooh_code/Src/config.py`.
- Matplotlib `~=3.7.2` - Training curves and paper figures in `ooh_code/Src/Utils/Utils.py` and `ooh_code/scripts/build_artifacts.py`; `build_artifacts.py` forces the noninteractive `Agg` backend.

**Testing:**
- Not detected. No `pytest`, `unittest` test suite, or test runner configuration was found in the repository.
- Smoke verification is workflow-based through `ooh_code/experiments/studies/smoke_rc.yaml`, `ooh_code/experiments/studies/smoke_austin.yaml`, and `python ooh_code/scripts/run_study.py --study smoke_rc`.

**Build/Dev:**
- `argparse` command-line interfaces - Main entry points are `ooh_code/run_menu_compare.py`, `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, and `ooh_code/scripts/build_manuscript.py`.
- LaTeX build tools - `ooh_code/scripts/build_manuscript.py` runs `latexmk` when available, otherwise `pdflatex` with optional `bibtex`.
- Git metadata - `ooh_code/Src/research_pipeline.py` calls `git rev-parse --short HEAD`; if unavailable it hashes selected source files.
- Matplotlib artifact generation - `ooh_code/scripts/build_artifacts.py` writes publication figures to `ooh_code/artifacts/figures/`.

## Key Dependencies

**Critical:**
- `torch>=2.0.1` - Required for CNN/linear predictors, supervised learning, checkpoint save/load, and tensor-backed memory buffers.
- `numpy~=1.25.1` - Required for simulator state, routing matrices, benchmark data loading, MNL computations, bootstrap confidence intervals, and result aggregation.
- `hygese~=0.0.0.8` - Required for final and intermediate HGS route optimization. `ooh_code/Environments/OOH/Parcelpoint_py.py` notes a known Hygese coordinate assertion behavior.
- `pyyaml>=6.0` - Required for the manifest-driven study system and saved `args.yaml` / `manifest_snapshot.yaml` files.
- `matplotlib~=3.7.2` - Required for generated training curves and paper-ready figures.

**Infrastructure:**
- Standard library `subprocess` - Used by `ooh_code/Src/research_pipeline.py` for Git marker detection and by `ooh_code/scripts/build_manuscript.py` for artifact and LaTeX subprocesses.
- Standard library `csv`, `json`, `hashlib`, `pathlib`, `datetime` - Used for normalized summaries, run IDs, manifest hashing, and reproducible artifact metadata in `ooh_code/Src/research_pipeline.py`.
- Optional SciPy - Not declared in `ooh_code/requirements.txt`. `ooh_code/Src/Utils/MathUtils.py` uses `scipy.special.lambertw` when installed and falls back to an internal principal-branch Lambert W implementation.

## Configuration

**Environment:**
- No `.env` file or environment-variable based configuration was detected.
- Runtime configuration is CLI-driven in `ooh_code/Src/parser.py`; common options include study instance (`--instance`), split IDs (`--data_seed`, `--data_seed_test`), training length (`--max_episodes`), GPU use (`--gpu`), menu policy (`--menu_policy`), solver timing (`--hgs_reopt_time`, `--hgs_final_time`), and pricing mode (`--menu_pricing_mode`).
- Study configuration is YAML-driven through `ooh_code/experiments/studies/*.yaml` and suite configuration through `ooh_code/experiments/suites/*.yaml`.
- Run-time snapshots are written under `ooh_code/outputs/` by `ooh_code/Src/config.py` and `ooh_code/Src/research_pipeline.py`.

**Build:**
- Dependency manifest: `ooh_code/requirements.txt`.
- Main research runner: `ooh_code/run_menu_compare.py`.
- Study orchestration: `ooh_code/scripts/run_study.py`.
- Artifact build: `ooh_code/scripts/build_artifacts.py`.
- Manuscript build: `ooh_code/scripts/build_manuscript.py`.
- Manuscript source: `ooh_code/manuscript/main.tex`, `ooh_code/manuscript/sections/*.tex`, and `ooh_code/manuscript/references.bib`.
- Artifact outputs: `ooh_code/artifacts/results_snapshot/`, `ooh_code/artifacts/tables/`, and `ooh_code/artifacts/figures/`.
- Raw run outputs: `ooh_code/outputs/` and nested `ooh_code/outputs/studies/`, `ooh_code/outputs/shared_training/`, `ooh_code/outputs/menu_compare/`; ignored by `ooh_code/.gitignore`.

## Platform Requirements

**Development:**
- Windows PowerShell examples are documented in `ooh_code/README.md`, but the Python code uses portable `pathlib`/`os.path` patterns in most scripts.
- Create a virtual environment from `ooh_code/` and install `ooh_code/requirements.txt`.
- Run research workflows from `ooh_code/` so imports like `Src.research_pipeline` and bundled data paths resolve correctly.
- Keep benchmark data available under `ooh_code/Environments/OOH/HombergerGehring_data/` and `ooh_code/Environments/OOH/Amazon_data/`.
- Install `latexmk` or `pdflatex` only when compiling the manuscript PDF; `--skip_compile` still refreshes artifacts and metadata.

**Production:**
- Not applicable as a hosted application. The repository is a local/offline research codebase.
- Public-facing deliverables are committed research artifacts under `ooh_code/artifacts/` and manuscript files under `ooh_code/manuscript/`.
- Raw generated outputs under `ooh_code/outputs/` are local experiment state and are excluded by `ooh_code/.gitignore`.

---

*Stack analysis: 2026-05-27*
