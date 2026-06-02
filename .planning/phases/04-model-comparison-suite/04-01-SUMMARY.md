---
phase: 04-model-comparison-suite
plan: "01"
subsystem: experiments
tags: [manifest, model-comparison, pilot, yaml, pytest-free-check]

requires:
  - phase: 03-candidate-feature-and-label-contract
    provides: K/L/home semantics, home-first candidate tensors, masks, and labels
provides:
  - Six-method Phase 4 pilot manifest contract
  - Lightweight manifest drift check for work2_main
  - Protocol section documenting Phase 4 pilot comparability
affects: [04-model-comparison-suite, work2_main, experiment-reporting]

tech-stack:
  added: []
  patterns:
    - YAML manifest as method-roster source of truth
    - Fast manifest contract checks before expensive simulation

key-files:
  created:
    - ooh_code/scripts/test_work2_main_manifest.py
  modified:
    - ooh_code/experiments/studies/work2_main.yaml
    - ooh_code/docs/WORK2_EXPERIMENT_PROTOCOL.md

key-decisions:
  - "Phase 4 work2_main is a six-method, three-seed pilot, not formal 150-300/50 evidence."
  - "MLP-Menu is included as a core learned baseline; optional baselines remain non-blocking supplements."
  - "STATE/ROADMAP/REQUIREMENTS were not updated by this executor because they contained large pre-existing unrelated diffs."

patterns-established:
  - "Manifest checks assert method labels, tags, splits, budget, and K/L/home comments without running the simulator."

requirements-completed: [EXP-02, EXP-03, EXP-04, EXP-05, EXP-06, OUT-02]

duration: 5min
completed: 2026-06-02
---

# Phase 04 Plan 01: Manifest And Comparability Contract Summary

**Six-method Phase 4 pilot manifest with MLP-Menu, three shared seeds, K=10/L=3 guardrails, and a fast drift check.**

## Performance

- **Duration:** 5 min
- **Started:** 2026-06-02T04:04:28Z
- **Completed:** 2026-06-02T04:08:47Z
- **Tasks:** 3
- **Files modified:** 3

## Accomplishments

- Updated `work2_main.yaml` from a five-method description to the approved six-method Phase 4 pilot roster.
- Added `MLP-Menu` as a core learned baseline while preserving `seed0..seed2`, `instance=RC`, `80/20` pilot budget, `K=10`, `L=3`, and calibrated MNL/ETA settings already present in the working copy.
- Added a fast manifest contract script that checks core policies, split ids, shared train/test split values, pilot budget, and K/L/home comments.
- Added a Phase 4 pilot comparability section to the Work2 experiment protocol.

## Task Commits

1. **Task 1: Update the work2_main method roster** - `51989c8` (`feat`)
2. **Task 2: Add a lightweight manifest contract check** - `cba9119` (`test`)
3. **Task 3: Document Phase 4 pilot comparability** - `71cb590` (`docs`)

## Files Created/Modified

- `ooh_code/experiments/studies/work2_main.yaml` - Six-method Phase 4 pilot manifest with MLP-Menu and pilot/formal budget separation.
- `ooh_code/scripts/test_work2_main_manifest.py` - Fast PyYAML manifest contract check.
- `ooh_code/docs/WORK2_EXPERIMENT_PROTOCOL.md` - Phase 4 pilot comparability, optional baselines, shared-contract, and fallback-rule documentation.

## Decisions Made

- Kept the existing `cost_L` and `cnn_setmenu_net` machine tags to avoid unnecessary downstream tag churn in this plan; labels now match the approved display names.
- Treated `Home only`, `Full-candidate CNN`, and `SetMenuNet` as optional supplements, not blockers for Plan 04-01.
- Used `--resume_latest` for the smoke verification because current `run_study.py` reports `--resume` as an ambiguous shorthand.

## Deviations from Plan

None - plan executed within the requested file scope.

## Issues Encountered

- `python scripts/run_study.py --study smoke_work2_main --resume` failed because `--resume` is ambiguous in the current CLI. Verification was rerun successfully with `python scripts/run_study.py --study smoke_work2_main --resume_latest`.
- `.planning/STATE.md`, `.planning/ROADMAP.md`, and `.planning/REQUIREMENTS.md` had large pre-existing unrelated diffs before metadata close-out. This executor did not stage or commit those files to avoid mixing unrelated project-state migration changes into Plan 04-01.

## Verification

- `python scripts/test_work2_main_manifest.py` from `ooh_code/`: PASS.
- `python scripts/run_study.py --study smoke_work2_main --resume_latest` from `ooh_code/`: PASS; completed `smoke_work2_main` with 7 variants.
- Manifest inspection confirmed labels `Nearest-L`, `Cost-L heuristic`, `CNN-Menu`, `MLP-Menu`, `CNN-SetMenuNet`, and `Oracle Menu`.
- Manifest inspection confirmed split ids `seed0`, `seed1`, and `seed2`, all using `train_split: 0` and `test_split: 1`.
- Task commits touched only `work2_main.yaml`, `test_work2_main_manifest.py`, and `WORK2_EXPERIMENT_PROTOCOL.md`; no Work 1 pricing, MNL choice, or HGS/Hygese core files were modified by this plan.

## Known Stubs

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Plan 04-02 can rely on the six-method pilot roster and three-seed manifest contract. GSD state metadata still needs a safe single-writer update or manual reconciliation because the planning state files were already dirty before this executor ran.

## Self-Check: PASSED

- Found `ooh_code/experiments/studies/work2_main.yaml`.
- Found `ooh_code/scripts/test_work2_main_manifest.py`.
- Found `ooh_code/docs/WORK2_EXPERIMENT_PROTOCOL.md`.
- Found `.planning/phases/04-model-comparison-suite/04-01-SUMMARY.md`.
- Found task commits `51989c8`, `cba9119`, and `71cb590`.

---
*Phase: 04-model-comparison-suite*
*Completed: 2026-06-02*
