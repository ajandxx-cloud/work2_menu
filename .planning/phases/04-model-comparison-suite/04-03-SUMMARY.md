---
phase: 04-model-comparison-suite
plan: "03"
subsystem: experiments
tags: [work2, model-comparison, pilot-run, artifacts, verification]

requires:
  - phase: 04-model-comparison-suite
    provides: Six-method Phase 4 pilot manifest and comparability contract
  - phase: 04-model-comparison-suite
    provides: Phase 4 summary and diagnostic reporting gate
provides:
  - Completed three-seed work2_main pilot run
  - Work2-standard Phase 4 artifacts from full pilot output
  - Phase 4 verification and readiness decision
affects: [04-model-comparison-suite, work2_main, phase5-readiness]

tech-stack:
  added: []
  patterns:
    - Resume long pilot runs with explicit run id instead of ambiguous --resume shorthand
    - Keep raw simulator outputs ignored and commit paper-facing standard artifacts
    - Treat mixed pilot evidence as diagnostic input, not a manually editable result

key-files:
  created:
    - artifacts/work2_cnn_setmenunet/results_snapshot/work2_main_rows.csv
    - artifacts/work2_cnn_setmenunet/work2_main_summary.md
    - artifacts/work2_cnn_setmenunet/tables/work2_main_prediction_accuracy.tex
    - artifacts/work2_cnn_setmenunet/tables/work2_main_operational.tex
    - artifacts/work2_cnn_setmenunet/tables/work2_main_menu_regret.tex
    - artifacts/work2_cnn_setmenunet/figures/work2_main_net_profit.png
    - artifacts/work2_cnn_setmenunet/diagnostics/work2_main_diagnostic.md
    - .planning/phases/04-model-comparison-suite/VERIFICATION.md
  modified:
    - ooh_code/scripts/build_artifacts.py

key-decisions:
  - "The completed Phase 4 pilot is interpretable but mixed/inconclusive, not supportive of a CNN-SetMenuNet net-profit claim."
  - "Phase 5 can proceed only with risks/remediation, using the diagnostic report as the next decision input."
  - "Formal 150-300/50 evidence remains later-phase scope; Phase 4 used the planned 80/20 pilot budget."

requirements-completed: [EXP-02, EXP-03, EXP-04, EXP-05, EXP-06, OUT-02, OUT-03, OUT-04, OUT-05]

duration: 110min
completed: 2026-06-02
---

# Phase 04 Plan 03: Pilot Run And Verification Summary

**Ran the full three-seed `work2_main` pilot, generated standard artifacts, and closed Phase 4 with a mixed/inconclusive evidence decision.**

## Performance

- **Duration:** about 110 min, dominated by resumed seed1/seed2 training and evaluation.
- **Completed:** 2026-06-02
- **Tasks:** 3
- **Files modified:** 9 tracked Phase 4 outputs plus raw ignored study-output directories.

## Accomplishments

- Resumed and completed `work2_main` run `20260602T042600Z_41f91b9d`.
- Verified `study_summary.json` reached `status=completed`, `completed_splits=3`, and `expected_splits=3`.
- Built Work2-standard artifacts under `artifacts/work2_cnn_setmenunet/`.
- Added root-standard `.tex` tables and `work2_main_net_profit.png` alongside the existing legacy `ooh_code/artifacts` outputs.
- Wrote `.planning/phases/04-model-comparison-suite/VERIFICATION.md` with a PASS WITH RISKS decision.

## Task Commits

1. **Task 1: Run or resume the work2_main pilot** - raw outputs only; not committed by design.
2. **Task 2: Build standard artifacts and inspect evidence** - `6d47355` (`feat`)
3. **Task 3: Write Phase 4 verification and readiness decision** - closeout metadata commit.

## Files Created/Modified

- `ooh_code/scripts/build_artifacts.py` - writes Work2 tables and net-profit figure to both legacy and root-standard artifact directories.
- `artifacts/work2_cnn_setmenunet/results_snapshot/work2_main_rows.csv` - 18 rows = 3 seeds x 6 core methods.
- `artifacts/work2_cnn_setmenunet/work2_main_summary.md` - Phase 4 pilot summary with mixed/inconclusive conclusion.
- `artifacts/work2_cnn_setmenunet/diagnostics/work2_main_diagnostic.md` - diagnostic report for mixed evidence.
- `artifacts/work2_cnn_setmenunet/tables/work2_main_prediction_accuracy.tex`
- `artifacts/work2_cnn_setmenunet/tables/work2_main_operational.tex`
- `artifacts/work2_cnn_setmenunet/tables/work2_main_menu_regret.tex`
- `artifacts/work2_cnn_setmenunet/figures/work2_main_net_profit.png`
- `.planning/phases/04-model-comparison-suite/VERIFICATION.md`

## Decisions Made

- Used `--resume_run_id 20260602T042600Z_41f91b9d` instead of ambiguous `--resume`.
- Treated the completed pilot as mixed/inconclusive because CNN-SetMenuNet did not improve mean net profit versus Cost-L, CNN-Menu, MLP-Menu, or Nearest-L.
- Marked Phase 5 as ready only with risks/remediation, not as ready for a positive robustness claim.

## Deviations from Plan

- The initial executor was interrupted while the long pilot run was still incomplete, so the main orchestrator resumed the same run id and completed the plan inline.
- `build_artifacts.py --study work2_main` also rewrote legacy `ooh_code/artifacts` files. The closeout commit includes only Phase 4 standard root artifacts and the targeted builder change; unrelated pre-existing legacy artifact churn was not staged.

## Verification

- `python scripts/test_work2_main_manifest.py`: PASS.
- `python scripts/test_work2_artifact_summary.py`: PASS, 7 tests.
- `python -u scripts/run_study.py --study work2_main --resume_run_id 20260602T042600Z_41f91b9d`: PASS, completed study with 7 variants.
- `python scripts/build_artifacts.py --study work2_main`: PASS.
- CSV check: 18 rows, seeds `0`, `1`, `2`, methods `CNN-Menu`, `CNN-SetMenuNet`, `Cost-L heuristic`, `MLP-Menu`, `Nearest-L`, `Oracle Menu`.

## Evidence Classification

- **Conclusion gate:** Mixed/inconclusive pilot evidence.
- **CNN-SetMenuNet net profit mean:** `-5093.849`.
- **Primary issue:** CNN-SetMenuNet did not beat Cost-L heuristic, CNN-Menu, MLP-Menu, or Nearest-L on mean net profit.
- **Diagnostic path:** `artifacts/work2_cnn_setmenunet/diagnostics/work2_main_diagnostic.md`.

## User Setup Required

None.

## Next Phase Readiness

Phase 5 may proceed with risks. It should treat Phase 4 as a completed, interpretable pilot whose evidence is mixed/inconclusive and should use diagnostics/remediation before any stronger paper claim.

## Self-Check: PASSED

- Found `.planning/phases/04-model-comparison-suite/04-03-SUMMARY.md`.
- Found `.planning/phases/04-model-comparison-suite/VERIFICATION.md`.
- Found `artifacts/work2_cnn_setmenunet/results_snapshot/work2_main_rows.csv`.
- Found `artifacts/work2_cnn_setmenunet/work2_main_summary.md`.
- Found `artifacts/work2_cnn_setmenunet/diagnostics/work2_main_diagnostic.md`.
- Found all three root-standard table files and the net-profit figure.

---
*Phase: 04-model-comparison-suite*
*Completed: 2026-06-02*
