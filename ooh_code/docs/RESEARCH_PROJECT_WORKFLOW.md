# Work2 Research Project Workflow

This document describes the project-level workflow added on top of the stable work2 experiment core.

## Layers

### Scientific core

- `run_menu_compare.py`
- `Src/Algorithms/DSPO_Menu.py`
- `Src/work2_runtime.py`
- `Environments/OOH/`

This layer owns shared training, frozen evaluation, and the simulator.

### Study orchestration

- `experiments/studies/*.yaml`
- `scripts/run_study.py`
- `Src/research_pipeline.py`

This layer owns study manifests, split programs, checkpoint reuse, and normalized study summaries.

### Artifact generation

- `scripts/build_artifacts.py`
- `artifacts/`

This layer turns normalized study summaries into:

- lightweight JSON/CSV snapshots
- LaTeX-ready tables
- publication figures
- a short prose results summary

### Manuscript

- `manuscript/`
- `scripts/build_manuscript.py`

This layer consumes generated artifact files directly. Tables and figures should not be edited manually inside the paper source.

## Default Commands

Run the first paper suite:

```powershell
python scripts/run_study.py --study rc_paper_v1
```

Rebuild the paper-facing artifacts:

```powershell
python scripts/build_artifacts.py --study rc_paper_v1
```

Refresh the LaTeX manuscript:

```powershell
python scripts/build_manuscript.py
```

If no LaTeX compiler is installed:

```powershell
python scripts/build_manuscript.py --skip_compile
```
