---
phase: 05-robustness-experiments
plan: "01"
subsystem: experiments
tags: [work2, robustness, manifests, exp-07, testing]

requires:
  - phase: 04-model-comparison-suite
    provides: mixed Phase 4 Work2 pilot evidence and diagnostic framing
provides:
  - Work2 robustness suite manifest covering five EXP-07 dimensions
  - Compact dimension-specific study manifests for menu size, candidate pool, demand, outside option, and cross-instance stress tests
  - Fast manifest contract test guarding K/L/home semantics and default robustness settings
affects: [phase-05, phase-06, work2-artifacts, robustness-analysis]

tech-stack:
  added: []
  patterns:
    - Work2 robustness dimensions are encoded as loadable YAML study manifests with explicit dimension metadata
    - Manifest contract tests validate experimental design before simulator execution

key-files:
  created:
    - ooh_code/experiments/suites/work2_robustness.yaml
    - ooh_code/experiments/studies/work2_menu_size_robustness.yaml
    - ooh_code/experiments/studies/work2_candidate_pool_robustness.yaml
    - ooh_code/experiments/studies/work2_demand_robustness.yaml
    - ooh_code/experiments/studies/work2_outside_option_robustness.yaml
    - ooh_code/experiments/studies/work2_cross_instance_robustness.yaml
    - ooh_code/scripts/test_work2_robustness_manifests.py
  modified: []

key-decisions:
  - "Use compact 80/20 pilot-sized robustness manifests for Phase 5 instead of formal-budget runs."
  - "Use four interpretable methods per robustness setting: Cost-L heuristic, CNN-Menu, CNN-SetMenuNet, and Oracle Menu."
  - "Treat Phase 5 as stress-test evidence after mixed Phase 4 results, not as a positive-claim confirmation."

patterns-established:
  - "Robustness manifests carry robustness_dimension, dimension_parameter, dimension_default, and dimension_values metadata for downstream artifact grouping."
  - "Cross-instance robustness is satisfied by a non-RC Austin stress test with caveats documented in the manifest."

requirements-completed: [EXP-07]

duration: 34 min
completed: 2026-06-02
---

# Phase 05 Plan 01: Robustness Manifest Suite Summary

**Work2 EXP-07 robustness manifests with fast contract checks for K/L/home semantics and Phase 4 mixed-evidence framing**

## Performance

- **Duration:** 34 min
- **Started:** 2026-06-02T20:10:00Z
- **Completed:** 2026-06-02T20:44:28Z
- **Tasks:** 3
- **Files modified:** 7

## Accomplishments

- Created `work2_robustness` as the Phase 5 suite entry point with exactly five EXP-07 member studies.
- Added compact study manifests for menu size, candidate pool size, demand intensity, outside option utility, and Austin cross-instance robustness.
- Added a fast Python contract test that loads the suite and studies, checks defaults (`K=10`, `L=3`, `outside_option_util=0.0`), confirms Austin non-RC coverage, and verifies variant specs are generated.

## Task Commits

1. **Tasks 1-3: Work2 robustness manifests and contract test** - `f1f9065` (feat)

**Plan metadata:** pending in docs commit

## Files Created/Modified

- `ooh_code/experiments/suites/work2_robustness.yaml` - Suite manifest listing the five robustness dimensions.
- `ooh_code/experiments/studies/work2_menu_size_robustness.yaml` - L sweep including default `L=3`.
- `ooh_code/experiments/studies/work2_candidate_pool_robustness.yaml` - K sweep including default `K=10`.
- `ooh_code/experiments/studies/work2_demand_robustness.yaml` - Low/default/high demand sweep via `max_steps_r`.
- `ooh_code/experiments/studies/work2_outside_option_robustness.yaml` - Outside-option utility sweep including `0.0`.
- `ooh_code/experiments/studies/work2_cross_instance_robustness.yaml` - Austin non-RC robustness stress test.
- `ooh_code/scripts/test_work2_robustness_manifests.py` - Fast manifest contract test.

## Decisions Made

- Used four required interpretable methods per robustness setting to control runtime while preserving the main comparison structure: Cost-L heuristic, CNN-Menu, CNN-SetMenuNet, and Oracle Menu.
- Encoded dimension metadata directly in each manifest so Plan 02 can group robustness rows without relying on filename-only inference.
- Kept Phase 4’s mixed/inconclusive framing in the suite and study descriptions.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- Initial `test_work2_robustness_manifests.py` import failed when run as a script because `ooh_code/` was not on `sys.path`; fixed by inserting the project root before importing `Src.research_pipeline`.
- The first cross-instance assertion was stricter than the plan, requiring two non-default instances. Adjusted it to match EXP-07 and the plan: default RC metadata plus at least one non-RC executable member.
- `gsd-sdk query state.advance-plan` could not parse the current `STATE.md` plan counter format; execution continued with ROADMAP/REQUIREMENTS updates and this SUMMARY as the durable plan close-out.

## Verification

- `python scripts/test_work2_main_manifest.py` - passed.
- `python scripts/test_work2_robustness_manifests.py` - passed.
- `load_manifest('work2_robustness')` - returned `_kind == 'suite'` with all five members.
- No Work 1 pricing, MNL choice, or HGS/Hygese route-cost core files were edited by this plan.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Plan 02 can consume stable `work2_*_robustness` names and the manifest-level dimension metadata to build robustness artifacts and conservative evidence classifications.

---
*Phase: 05-robustness-experiments*
*Completed: 2026-06-02*
