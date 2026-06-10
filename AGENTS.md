# Project Instructions

This repository is a GSD-managed research project for Work2 robust time-window service menu optimization in many-to-one DRT.

## Planning Context

Read these files before phase work:

- `.planning/PROJECT.md`
- `.planning/REQUIREMENTS.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `.planning/research/SUMMARY.md`
- `.planning/codebase/` documents, but treat `ooh_code/` references as stale until Phase 1 verifies them against the current filesystem.

## Active Runtime Assumption

Prefer `work2_coding/` as the active runtime root. A smoke import passed during initialization:

```powershell
python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"
```

Do not create a parallel `ooh_code/` root unless the Stage 0 audit proves it is required.

## Research Guardrails

- Start with Phase 1 repository audit before algorithm behavior changes.
- Preserve paired replay fairness across policy comparisons.
- Keep opt-out accounting separate from accepted home pickup.
- Make checkpoint load status explicit in result metadata.
- Treat no-filter as diagnostic unless formal evidence justifies stronger claims.
- Keep attention-based choice/scoring out of v1 scope.
- Do not hand-edit generated result rows or paper artifacts.

## Verification Baseline

Adapt commands to the confirmed runtime root. Minimum expected checks after implementation phases:

```powershell
cd work2_coding
python -c "import sys; sys.path.insert(0, '.'); import Src.config"
```

Add or identify script-style tests for opt-out accounting, robust ETA filters, menu objective behavior, manifest contracts, and artifact gates as the phases implement them.
