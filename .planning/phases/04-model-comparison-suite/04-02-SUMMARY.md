---
phase: 04-model-comparison-suite
plan: "02"
subsystem: experiments
tags: [work2, model-comparison, artifacts, diagnostics, pilot-summary]

requires:
  - phase: 04-model-comparison-suite
    provides: Six-method Phase 4 pilot manifest and comparability contract
provides:
  - Phase 4 pilot summary wording for work2_main
  - Graded CNN-SetMenuNet evidence gate
  - Conditional diagnostic report for weak, mixed, trade-off, or incomplete pilot evidence
affects: [04-model-comparison-suite, work2_main, experiment-reporting, phase5-readiness]

tech-stack:
  added: []
  patterns:
    - Work2 standard artifacts under root artifacts/work2_cnn_setmenunet
    - Conservative graded evidence classification before Phase 5 readiness
    - Diagnostic markdown generated only when pilot evidence is not supportive

key-files:
  created:
    - ooh_code/scripts/test_work2_artifact_summary.py
    - artifacts/work2_cnn_setmenunet/results_snapshot/work2_main_rows.csv
    - artifacts/work2_cnn_setmenunet/work2_main_summary.md
    - artifacts/work2_cnn_setmenunet/diagnostics/work2_main_diagnostic.md
  modified:
    - ooh_code/scripts/build_artifacts.py

key-decisions:
  - "Phase 4 work2_main summary now uses graded evidence language instead of smoke wording."
  - "Obvious guardrail worsening is defined conservatively as quit_rate increase > 0.05 or avg_walk increase > 300, with a 10% relative worsening floor."
  - "Current existing work2_main rows classify as mixed/inconclusive pilot evidence and generate a diagnostic report."
  - "STATE/ROADMAP/REQUIREMENTS were not updated by this executor because they contained large pre-existing unrelated diffs."

patterns-established:
  - "Synthetic artifact-summary tests exercise conclusion-gate states without running the simulator."
  - "Supportive evidence suppresses diagnostics; mixed, trade-off, or incomplete evidence writes diagnostics and links them from the summary."

requirements-completed: [OUT-02, OUT-03, OUT-04, OUT-05, EXP-02]

duration: 22min
completed: 2026-06-02
---

# Phase 04 Plan 02: Summary And Diagnostic Reporting Summary

**Phase 4 Work2 pilot reporting with conservative graded conclusions and conditional diagnostics.**

## Performance

- **Duration:** 22 min
- **Started:** 2026-06-02T04:00:58Z
- **Completed:** 2026-06-02T04:21:41Z
- **Tasks:** 3
- **Files modified:** 5

## Accomplishments

- Split Work2 standard reporting so `smoke_work2_main` keeps one-seed smoke language while `work2_main` receives a Phase 4 pilot summary.
- Added a graded conclusion gate for `stronger_support`, `preliminary_support`, `tradeoff_mixed`, `mixed_inconclusive`, and `incomplete` evidence states.
- Added focused synthetic tests for support, trade-off, mixed, incomplete, and diagnostic behavior without running the expensive simulator.
- Generated `work2_main_summary.md`, standard per-seed CSV rows, and a conditional diagnostic report for the current mixed/inconclusive pilot evidence.

## Task Commits

1. **Task 1: Separate smoke summaries from Phase 4 pilot summaries** - `13318e3` (`feat`)
2. **Task 2: Implement the graded conclusion gate** - `24af233` (`feat`)
3. **Task 3: Add conditional diagnostic report generation** - `ff193f5` (`feat`)

## Files Created/Modified

- `ooh_code/scripts/build_artifacts.py` - Work2 standard artifact generation, graded evidence gate, Phase 4 summary writer, and conditional diagnostics.
- `ooh_code/scripts/test_work2_artifact_summary.py` - Synthetic tests for summary/gate behavior.
- `artifacts/work2_cnn_setmenunet/results_snapshot/work2_main_rows.csv` - Standard per-seed method-level rows for existing `work2_main` outputs.
- `artifacts/work2_cnn_setmenunet/work2_main_summary.md` - Phase 4 pilot summary with aggregate means, seed variation, method explanations, conclusion gate, caveats, and Phase 5 readiness.
- `artifacts/work2_cnn_setmenunet/diagnostics/work2_main_diagnostic.md` - Conditional diagnostic report for current mixed/inconclusive evidence.

## Decisions Made

- Kept smoke wording for `smoke_work2_main` and added separate Phase 4 pilot wording only for `work2_main`.
- Treated `net_profit` as primary, `menu_regret` and `top_L_overlap` as support metrics, and `quit_rate`/`avg_walk` as guardrails.
- Classified the existing `work2_main` artifact rows as mixed/inconclusive because CNN-SetMenuNet did not improve mean `net_profit` versus Cost-L or a core learned baseline.
- Did not update `.planning/STATE.md`, `.planning/ROADMAP.md`, or `.planning/REQUIREMENTS.md` because those files had large unrelated dirty diffs before this plan ran.

## Deviations from Plan

None - plan executed within the requested implementation scope.

## Issues Encountered

- A quick inspection command initially used Bash heredoc syntax in PowerShell and failed without modifying files. It was rerun with `python -c`.
- `python scripts/build_artifacts.py --study work2_main` rewrites legacy `ooh_code/artifacts/work2_main_*` files as a side effect. Those verification-only rewrites were restored after each run so this plan did not commit unrelated legacy artifact churn.
- Root `artifacts/work2_cnn_setmenunet/smoke_work2_main_*` files remain untracked from the broader pre-existing `artifacts/` working-tree state and were not committed by this plan.

## Verification

- `python scripts/test_work2_artifact_summary.py` from `ooh_code/`: PASS; 7 synthetic gate/diagnostic tests.
- `python scripts/build_artifacts.py --study smoke_work2_main` from `ooh_code/`: PASS; smoke artifacts still build and keep smoke wording.
- `python scripts/build_artifacts.py --study work2_main` from `ooh_code/`: PASS; existing `work2_main` outputs generate the Phase 4 summary and diagnostic.
- Inspected `artifacts/work2_cnn_setmenunet/work2_main_summary.md`: includes method-level explanations, mixed/inconclusive conclusion, diagnostic link, caveats, and Phase 5 readiness text.
- Inspected `artifacts/work2_cnn_setmenunet/diagnostics/work2_main_diagnostic.md`: includes cost prediction error, ranking/menu selection error, training budget, and seed instability sections.

## Known Stubs

None. Existing placeholder-figure helper code in `build_artifacts.py` predates this plan and is a generated-artifact fallback, not an unwired Phase 4 reporting stub.

## Threat Flags

None - this plan added no network endpoints, auth paths, file-upload paths, or new trust-boundary schema.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Plan 04-03 can consume the reporting gate and current artifact outputs. The current pilot evidence is mixed/inconclusive, so Phase 5 readiness is conditional on diagnostics identifying a fixable issue or a clear remedial experiment. Planning metadata files still need safe single-writer reconciliation because they were dirty before this executor ran.

## Self-Check: PASSED

- Found `ooh_code/scripts/build_artifacts.py`.
- Found `ooh_code/scripts/test_work2_artifact_summary.py`.
- Found `artifacts/work2_cnn_setmenunet/results_snapshot/work2_main_rows.csv`.
- Found `artifacts/work2_cnn_setmenunet/work2_main_summary.md`.
- Found `artifacts/work2_cnn_setmenunet/diagnostics/work2_main_diagnostic.md`.
- Found task commits `13318e3`, `24af233`, and `ff193f5`.

---
*Phase: 04-model-comparison-suite*
*Completed: 2026-06-02*
