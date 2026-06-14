---
phase: 5
phase_name: Formal Evidence Readiness
status: complete
completed: 2026-06-14
requirements:
  - MLC-05
  - ART-02
  - ART-03
---

# Phase 5 Summary

Phase 5 implemented formal evidence readiness gates for Work2 V1.

## Implemented

- Dedicated formal readiness preflight in `work2_coding/Src/formal_readiness.py`.
- Thin CLI in `work2_coding/scripts/check_formal_readiness.py`.
- JSON, Markdown, and dependency snapshot outputs under the readiness output root.
- Checkpoint path resolution, SHA256 capture, load smoke, and normalized-row metadata probe.
- Dirty-git blocking for formal claim-ready readiness.
- `build_artifacts.py --claim-ready --readiness-json ...` enforcement for formal runs.
- Readiness and dependency snapshot metadata propagation into artifact status, sidecars, and claim guard outputs.
- Script-style tests for missing checkpoint, dirty git, loaded checkpoint probe, readiness JSON enforcement, mismatch blocking, and failed-row blocking.

## Current Formal Evidence State

The real formal readiness report is blocked, not claim-ready:

- `dirty_git`
- `missing_formal_checkpoint`

This is expected until the formal checkpoint exists and the repository is clean.

## Next Commands

Generate the formal checkpoint:

```powershell
cd work2_coding
python scripts/train_shared_checkpoint.py --study formal_robust_menu --checkpoint-path outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt
```

Rerun readiness after the checkpoint exists and git is clean:

```powershell
python scripts/check_formal_readiness.py --study formal_robust_menu --output-root outputs/phase5_readiness
```

Only after readiness passes, run formal replay:

```powershell
python scripts/run_study.py --study formal_robust_menu --execute --output-root outputs/formal_v1
```

Then build formal claim-ready artifacts with the passed readiness JSON:

```powershell
python scripts/build_artifacts.py --run-dir <formal-run-dir> --claim-ready --readiness-json outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json
```

## Not Done By Design

- Formal replay was not run.
- No empirical superiority claims were made.
- No generated rows, manuscript source, paper artifacts, or checkpoint binaries were hand-edited.
