# Work2 Research Project for Many-to-One DRT Menu Optimization

This repository is now organized as a public-friendly research project for work2: service-menu optimization in many-to-one demand-responsive transit (DRT).

Each displayed service option is a bundle of:

- `meeting point`
- `pickup time window`

The project supports the full research loop:

1. run reproducible study manifests
2. reuse shared checkpoints for frozen policy comparison
3. aggregate normalized study summaries
4. generate paper tables and figures
5. compile an English LaTeX manuscript draft

## Research Question

The current work2 pipeline studies a management-oriented question: how strongly does
candidate-set filtering shape menu outcomes in many-to-one DRT, and when does relaxing
an overly strict filter improve operator performance relative to exhaustive full display?

The key comparisons still share:

- the same trained bundle predictor
- the same replayed request traces
- the same simulator initialization

The main paired-comparison metric remains:

`net_profit = charge_revenue - discount_cost - travel_cost - service_cost - failure_cost`

The experimental program now separates:

- `RC` as a mechanism benchmark for diagnosing candidate-set distortion
- `Austin` and `Seattle` as impact benchmarks for testing whether no-filter menus improve
  profit and user-facing outcomes in non-degenerate demand settings

## Repository Layers

- `run_menu_compare.py`: low-level scientific runner for shared training, paired comparison, and `menu_k` robustness
- `experiments/`: versioned study manifests and paper study suites
- `scripts/`: project-level batch execution, artifact generation, and manuscript orchestration
- `artifacts/`: committed lightweight snapshots, tables, figures, and prose result summaries
- `manuscript/`: English LaTeX paper draft wired to generated artifacts
- `Src/`: stable scientific core and project helper modules
- `docs/`: experiment protocol and implementation boundaries

## Public Workflows

### 1. Low-level scientific runner

Use the original work2 runner when you want to inspect a single configuration directly:

```powershell
python run_menu_compare.py `
  --instance RC `
  --data_seed 0 `
  --data_seed_test 1 `
  --menu_k 3 `
  --eval_episodes 20
```

### 2. Project-level study execution

Run the RC-focused suite:

```powershell
python scripts/run_study.py --study rc_paper_v1
```

Run only the local smoke verification study:

```powershell
python scripts/run_study.py --study smoke_rc
```

### 3. Build tables and figures

```powershell
python scripts/build_artifacts.py --study rc_paper_v1
```

This updates:

- `artifacts/results_snapshot/`
- `artifacts/tables/`
- `artifacts/figures/`
- `artifacts/RESULTS_SUMMARY.md`

### 4. Build the manuscript

```powershell
python scripts/build_manuscript.py
```

If the local machine does not have `latexmk` or `pdflatex`, you can still refresh the manuscript inputs:

```powershell
python scripts/build_manuscript.py --skip_compile
```

## Study Program

The project now uses a two-layer study design.

### Mechanism layer

- `rc_main_optout`
  - corrected outside-option RC benchmark
  - headline comparison focuses on `full_display`, `menu_optimization` (v1), and
    `menu_optimization_v2` (v2)
  - used to diagnose whether removing ETA filtering changes menu structure
- `filtering_baselines`
  - compares hard, calibrated, interval-overlap, and no-filter ETA screens
  - used to quantify false-negative pruning and candidate-set distortion

### Impact layer

- `austin_main`
- `seattle_main`

These studies are the headline management-effect benchmarks. Their artifact summaries focus on:

- `full_display`
- `menu_optimization` (v1)
- `menu_optimization_v2` (v2)

Additional heuristics are retained as supplementary robustness checks rather than headline policies.

### Legacy/support studies

- `rc_menu_k_robustness`
- `rc_menu_ablation`
- `rc_menu_ablation_v2`

These remain useful for development diagnostics, but they are not the primary source of the
management-oriented main conclusion.

## Normalized Outputs

Raw study runs are saved under:

- `outputs/studies/<study_name>/<run_id>/`

Each study run produces:

- split-level request traces
- per-variant episode metrics
- per-variant summaries
- normalized split rows
- aggregate study summaries

Policy-comparison summaries now also expose lightweight experiment-role metadata such as:

- `study_role`
- `acceptance_rate`
- `is_behavior_non_degenerate`

Committed lightweight research artifacts are saved under:

- `artifacts/results_snapshot/`
- `artifacts/tables/`
- `artifacts/figures/`

The public JSON outputs use work2 terminology, including:

- `home_pickup_count`
- `avg_meeting_point_count_per_menu`
- `feasible_meeting_point_count_sequence`

## Installation

Python 3.10+ is recommended.

```powershell
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
```

`scipy` is optional. If it is not installed, the Lambert W pricing transform falls back to the repository's internal principal-branch implementation.

The manuscript build additionally requires either:

- `latexmk`, or
- `pdflatex`

## Current Boundaries

The repository remains intentionally narrow and keeps the current work2 assumptions explicit:

- Pickup windows are front-end approximate service windows, not strict back-end VRPTW guarantees.
- Feasibility filtering uses predicted ETA logic and passenger-side acceptable intervals.
- Final route cost is recovered through HGS-based re-optimization at episode end.
- The goal is to identify high-leverage menu-design rules, especially candidate filtering, rather than to claim a universally dominant heuristic.
- The RC benchmark is now interpreted primarily as mechanism evidence; city studies carry the main impact comparison.
- The project does not claim a new exact routing solver.

## Key Documents

- `docs/WORK2_EXPERIMENT_PROTOCOL.md`
- `docs/WORK2_IMPLEMENTATION_BOUNDARIES.md`
- `experiments/README.md`
- `artifacts/README.md`
- `manuscript/README.md`

## License

`LICENSE.md` is preserved from the original codebase.
