---
phase: 03-experiment-contracts-and-fair-replay
plan: 01
subsystem: experiment-contracts
tags: [manifest, yaml, parser-validation, baselines, script-tests]
requires:
  - phase: 02-core-semantics-and-robust-menu-logic
    provides: parser menu policies, ETA modes, checkpoint metadata, robust solver telemetry
provides:
  - smoke, pilot, and formal robust-menu study contracts
  - suite manifest for Phase 3 robust-menu studies
  - parser-derived manifest validation helpers
  - deterministic manifest contract tests
affects: [phase-03, phase-04, evidence-and-artifacts]
tech-stack:
  added: []
  patterns: [manifest-first study contracts, parser-derived validation, script-style contract tests]
key-files:
  created:
    - work2_coding/Src/experiment_contracts.py
    - work2_coding/Experiments/studies/smoke_robust_menu.yaml
    - work2_coding/Experiments/studies/pilot_robust_menu.yaml
    - work2_coding/Experiments/studies/formal_robust_menu.yaml
    - work2_coding/Experiments/suites/work2_robust_menu.yaml
    - work2_coding/scripts/test_experiment_contracts.py
  modified:
    - work2_coding/.gitignore
key-decisions:
  - "Manifest validation derives parser choices from Parser().get_parser() so study contracts cannot drift from runtime policy/filter flags."
  - "Pilot/formal manifests require explicit shared checkpoint provenance but are not executed in Phase 3."
  - "No-filter appears only as no_filter_diagnostic with diagnostic metadata."
patterns-established:
  - "Study manifests declare schema_version, tier, run_mode, base_args, splits, policies, paired_fields, varied_fields, and output_schema."
  - "Contract metadata such as uptake_regime is allowed as row/study metadata without becoming a legacy parser flag."
requirements-completed: [EXP-01, EXP-02, EXP-03]
duration: 20min
completed: 2026-06-11
---

# Phase 03 Plan 01: Study Contract Summary

**Smoke, pilot, formal, and suite contracts now validate robust-menu policy intent before expensive evidence runs**

## Performance

- **Duration:** 20 min
- **Started:** 2026-06-11T06:08:00Z
- **Completed:** 2026-06-11T06:28:54Z
- **Tasks:** 3
- **Files modified:** 7

## Accomplishments

- Added `experiment_contracts.py` with manifest loading, deterministic hashes, parser choices, parser-compatible policy resolution, suite resolution, checkpoint gates, and uptake-regime validation.
- Added smoke, pilot, formal, and suite YAML contracts with required baselines and no-filter diagnostic labeling.
- Added `test_experiment_contracts.py` covering valid manifests, parser compatibility, duplicate detection, invalid filters, checkpoint requirements, and suite membership.

## Task Commits

1. **Tasks 1-3: Manifest contracts and validation tests** - `1acd867` (feat)

**Plan metadata:** pending in docs commit

## Files Created/Modified

- `work2_coding/Src/experiment_contracts.py` - Manifest schema, parser validation, hash, and resolver helpers.
- `work2_coding/Experiments/studies/*.yaml` - Smoke, pilot, and formal robust-menu study contracts.
- `work2_coding/Experiments/suites/work2_robust_menu.yaml` - Phase 3 suite contract.
- `work2_coding/scripts/test_experiment_contracts.py` - Script-style manifest contract tests.
- `work2_coding/.gitignore` - Ignores local `outputs/` runs.

## Decisions Made

- The committed manifest directory is `work2_coding/Experiments/...` because the existing Windows ignore pattern treats `Experiments/` and `experiments/` as the same path; the helper resolves both lowercase and uppercase directories.
- Formal rows remain blocked from placeholder-only evidence; formal execution is deferred to Phase 4.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Added case-insensitive manifest directory fallback**
- **Found during:** Task 2 manifest staging
- **Issue:** Windows/Git resolved lower `experiments/` paths as `Experiments/`, which would break lowercase-only lookup on a case-sensitive checkout.
- **Fix:** `experiment_contracts.py` now prefers lowercase `experiments/` and falls back to uppercase `Experiments/`.
- **Files modified:** `work2_coding/Src/experiment_contracts.py`
- **Verification:** All Phase 3 tests passed after the change.
- **Committed in:** `1acd867`

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** The fallback preserves the planned manifest structure while keeping cross-platform lookup robust.

## Issues Encountered

None beyond the path-case handling above.

## User Setup Required

None - no external service configuration required.

## Verification

- `cd work2_coding; python scripts/test_experiment_contracts.py` -> `PASS: 12 experiment contract tests`
- `cd work2_coding; python -c "import sys; sys.path.insert(0,'.'); from Src.experiment_contracts import load_manifest, validate_manifest; m=load_manifest('smoke_robust_menu'); validate_manifest(m); print('SMOKE_MANIFEST_OK')"` -> covered by test suite and helper import.
- `python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"` -> `IMPORT_OK`
- `Test-Path ooh_code` -> `False`

## Next Phase Readiness

Ready for paired replay and normalized row helpers in Plan 02.

---
*Phase: 03-experiment-contracts-and-fair-replay*
*Completed: 2026-06-11*

