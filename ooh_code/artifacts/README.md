# Research Artifacts

This directory stores lightweight, committed outputs derived from normalized study summaries.

## Layout

- `results_snapshot/`: compact JSON and CSV snapshots for the latest built study scope
- `tables/`: paper-ready CSV and LaTeX tables
- `figures/`: publication figures generated from study summaries
- `RESULTS_SUMMARY.md`: short prose summary of the latest built artifacts

Regenerate with:

```powershell
python scripts/build_artifacts.py --study rc_paper_v1
```

Full raw run outputs are intentionally kept under `outputs/` and remain excluded from git.
