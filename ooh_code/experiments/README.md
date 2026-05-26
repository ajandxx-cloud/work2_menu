# Experiment Manifests

This directory defines the project-level experiment program for the work2 paper.

## Layout

- `studies/`: single executable studies
- `suites/`: named bundles of studies used by the paper pipeline

## Main Manifests

- `rc_main.yaml`: primary RC policy comparison
- `rc_menu_k_robustness.yaml`: RC robustness sweep over `menu_k`
- `rc_menu_ablation.yaml`: RC menu-component ablations
- `smoke_rc.yaml`: minimal verification study for local testing
- `suites/rc_paper_v1.yaml`: the first paper bundle that ties the three RC studies together

For the bundled `RC` data, only split files `0` and `1` are present. The first-paper manifests therefore use:

- `0->1`
- `1->0`
- one additional `0->1` replication with a different random seed and trace seed

## Public Workflow

Run the full first-paper study bundle:

```powershell
python scripts/run_study.py --study rc_paper_v1
```

Run only the smoke verification study:

```powershell
python scripts/run_study.py --study smoke_rc
```
