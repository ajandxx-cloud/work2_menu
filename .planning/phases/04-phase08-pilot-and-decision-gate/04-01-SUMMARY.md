---
phase: 04-phase08-pilot-and-decision-gate
plan: 04-01
subsystem: experiments
tags: [work2, phase08, pilot, decision-gate, service-constrained-profit]
requires:
  - phase: 03-expected-profit-enumeration-policies
    provides: Expected-Profit Enumeration, Service-Constrained Expected-Profit, Cost Oracle, and Profit Oracle policy wiring
provides:
  - Phase08 smoke and 3-seed pilot study manifests
  - Phase08 fail-closed artifact and decision gate
  - Phase-local pilot rows, summaries, oracle diagnostics, tradeoff report, and decision memo
  - Pilot decision that routes to objective recalibration
affects: [phase05-formal-evidence, work2-choice-aware-menu-optimization]
tech-stack:
  added: []
  patterns:
    - Explicit run-id artifact generation from normalized study rows
    - Service-constrained profit unavailable values are preserved as null
key-files:
  created:
    - ooh_code/experiments/studies/work2_phase08_smoke.yaml
    - ooh_code/experiments/studies/work2_phase08_pilot.yaml
    - ooh_code/scripts/test_phase08_manifest.py
    - ooh_code/scripts/build_phase08_artifacts.py
    - ooh_code/scripts/test_phase08_artifact_gate.py
    - .planning/phases/04-phase08-pilot-and-decision-gate/artifacts/pilot_rows.csv
    - .planning/phases/04-phase08-pilot-and-decision-gate/artifacts/pilot_summary.md
    - .planning/phases/04-phase08-pilot-and-decision-gate/artifacts/oracle_diagnostics.md
    - .planning/phases/04-phase08-pilot-and-decision-gate/artifacts/profit_vs_quit_tradeoff.md
    - .planning/phases/04-phase08-pilot-and-decision-gate/artifacts/phase08_decision.md
    - .planning/phases/04-phase08-pilot-and-decision-gate/VERIFICATION.md
  modified:
    - ooh_code/run_menu_compare.py
key-decisions:
  - "Phase08 decision artifacts remain phase-local and are not synced to ooh_code/artifacts."
  - "Unavailable service-constrained profit is preserved as None instead of averaged through guardrail-failing rows."
  - "The completed pilot routes to recalibrate_objective rather than proceed_to_formal."
patterns-established:
  - "Pilot artifacts require explicit --run-id or --study-dir and refuse latest-run inference."
  - "Any nonzero service guardrail violation rate makes a policy ineligible for proceed."
requirements-completed: [PILOT-01, PILOT-02, PILOT-03, PILOT-04, VER-01, VER-02, VER-03, VER-04]
duration: about 4h 30m
completed: 2026-06-05
---

# Phase 4 Plan 04-01: Phase08 Pilot And Decision Gate Summary

**Phase08 smoke and 3-seed pilot decision gate with phase-local recalibration memo from normalized rows**

## Performance

- **Duration:** about 4h 30m
- **Started:** 2026-06-04T20:30+08:00
- **Completed:** 2026-06-05T01:15+08:00
- **Tasks:** 3
- **Files modified:** 12

## Accomplishments

- Added Phase08-specific smoke and pilot manifests with the locked eight-policy comparison set.
- Added a dedicated fail-closed Phase08 artifact builder and fixture tests.
- Ran Phase08 smoke and the full 3-seed pilot through the study runner.
- Generated the five required phase-local artifacts from explicit pilot run `20260604T124624Z_bf03b88d`.
- Recorded the honest pilot decision: `recalibrate_objective`.

## Task Commits

1. **Task 1: Create Phase08 study manifests and manifest contract tests** - `e4b122b`
2. **Task 2: Create fail-closed Phase08 artifact gate and tests** - `62fe15e`
3. **Task 3: Execute smoke, pilot, artifact generation, and verification note** - `b2399a2`, `17b8863`, `92dc811`

**Plan metadata:** this summary commit.

## Files Created/Modified

- `ooh_code/experiments/studies/work2_phase08_smoke.yaml` - Minimal Phase08 smoke study.
- `ooh_code/experiments/studies/work2_phase08_pilot.yaml` - 3-seed RC Phase08 pilot study.
- `ooh_code/scripts/test_phase08_manifest.py` - Manifest contract checks.
- `ooh_code/scripts/build_phase08_artifacts.py` - Explicit-run artifact and decision generator.
- `ooh_code/scripts/test_phase08_artifact_gate.py` - Artifact-gate fixture checks.
- `ooh_code/run_menu_compare.py` - Preserves unavailable service-constrained aggregate profit as `None`.
- `.planning/phases/04-phase08-pilot-and-decision-gate/artifacts/*` - Five generated decision artifacts.
- `.planning/phases/04-phase08-pilot-and-decision-gate/VERIFICATION.md` - Command and evidence record.

## Decisions Made

- Phase08 artifacts are decision-gate outputs only; they stay under `.planning/phases/04-phase08-pilot-and-decision-gate/artifacts/`.
- The pilot cannot proceed to formal evidence because expected-profit methods violate guardrails and Service-Constrained Expected-Profit uses fallback.
- Comparator unavailable service-constrained profit blocks the hard gate instead of being coerced to zero.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Nullable service-constrained profit crashed pilot aggregation**
- **Found during:** Task 3 pilot execution.
- **Issue:** `aggregate_episode_metrics` attempted to average floats with `None`.
- **Fix:** Added `mean_or_none_if_unavailable` and used it for `service_constrained_net_profit`.
- **Files modified:** `ooh_code/run_menu_compare.py`
- **Verification:** `python -m py_compile run_menu_compare.py`; pilot resumed and completed.
- **Committed in:** `b2399a2`

**2. [Rule 3 - Blocking] Artifact gate assumed guardrail fields were booleans**
- **Found during:** Task 3 artifact generation.
- **Issue:** Real normalized rows store `service_guardrail_pass` and `service_guardrail_violation` as rates across evaluation episodes.
- **Fix:** Validated guardrail fields as rates and marked any nonzero violation rate ineligible.
- **Files modified:** `ooh_code/scripts/build_phase08_artifacts.py`
- **Verification:** `python scripts/test_phase08_artifact_gate.py`; real artifact build passed.
- **Committed in:** `17b8863`

**3. [Rule 3 - Blocking] Comparator service-constrained profit can be unavailable**
- **Found during:** Task 3 artifact generation.
- **Issue:** The classifier tried to compare `None` with numeric comparator values.
- **Fix:** Comparator-unavailable rows now fail closed and route away from `proceed_to_formal`.
- **Files modified:** `ooh_code/scripts/build_phase08_artifacts.py`
- **Verification:** `python scripts/test_phase08_artifact_gate.py`; real artifact build passed.
- **Committed in:** `17b8863`

---

**Total deviations:** 3 auto-fixed blocking issues.
**Impact on plan:** All fixes were required to complete the real pilot and preserve conclusion honesty. No MNL, pricing, or routing semantics were changed.

## Issues Encountered

- The pilot exited twice during seed2 without console traceback after writing seed2 training artifacts. Resume with `PYTHONFAULTHANDLER=1` completed the final seed and study aggregation.
- `git diff` still shows a pre-existing `DSPO_Menu.py` diff from earlier policy-semantics work; this plan did not edit that file.
- `git status --short -- ooh_code/artifacts` remains non-empty because of pre-existing artifact changes; no `phase08` files were created under `ooh_code/artifacts`.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Phase08 is complete, but it does not authorize formal evidence. The next step should review the recalibration memo and decide whether to adjust objective/service parameters, inspect fallback behavior, or diagnose scenario design before spending formal runtime.

---
*Phase: 04-phase08-pilot-and-decision-gate*
*Completed: 2026-06-05*
