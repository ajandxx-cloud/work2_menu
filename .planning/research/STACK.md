# Stack Research

## Current Stack

The active project should be treated as a local/offline research pipeline, not a hosted application.

| Layer | Current Evidence | Planning Implication |
|-------|------------------|----------------------|
| Runtime root | `work2_coding/` exists and `import Src.config` succeeds when inserted on `sys.path` | Stage 0 should verify this root and update stale planning references that mention `ooh_code/` |
| Language | Python 3.10 style code | Keep changes compatible with the existing scripts and imports |
| Core numerical stack | NumPy, PyTorch, Hygese | Reuse existing predictor and routing code; do not introduce new optimization frameworks before the audit |
| Entry points | `work2_coding/run.py`, `work2_coding/run_ppo.py`; no `work2_coding/scripts/` directory currently detected | A manifest runner may need to be added or adapted from existing entry points |
| Algorithm layer | `work2_coding/Src/Algorithms/DSPO_Menu.py`, `DSPO.py`, `Heuristic.py`, `Baseline.py` | Robust menu behavior should live near `DSPO_Menu.py` unless audit suggests extracting a helper module |
| Simulator layer | `work2_coding/Environments/OOH/Parcelpoint_py.py`, `customerchoice.py`, `env_utils.py`, `containers.py` | Opt-out/accounting repairs must be made in simulator and choice-model boundaries |
| Testing style | Script-style tests are implied by prior maps but not currently visible under `work2_coding/scripts/` | Stage 0 should create or identify a minimal smoke/unit test path before algorithm edits |

## Recommended Stack Decisions

- Keep `work2_coding/` as the active package until disproven.
- Add experiment orchestration in a small script/package only after confirming existing runner behavior.
- Keep dependency footprint stable: Python, NumPy, PyTorch, Hygese, PyYAML if manifests are introduced, Matplotlib for artifacts.
- Store robust experiment settings in YAML manifests or JSON-equivalent contract files rather than ad hoc constants.
- Add provenance fields to normalized outputs before building paper artifacts.

## Open Questions For Phase 1

- Is `work2_coding/DSPO_Menu.py` the authoritative latest version, or is there another root hidden outside the current workspace?
- Which current command can run a one-episode menu-mode smoke test with acceptable runtime?
- Are there already result/artifact scripts outside `work2_coding/` that should be reused rather than recreated?
- Which checkpoint path is currently expected by Work2, and what happens on load failure?

---
*Research note generated: 2026-06-10*
