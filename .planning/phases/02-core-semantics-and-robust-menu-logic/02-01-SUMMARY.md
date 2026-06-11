---
phase: 02-core-semantics-and-robust-menu-logic
plan: 01
subsystem: runtime
tags: [parser, menu-runtime, dataclasses, predictors, script-tests]
requires:
  - phase: 01-repository-audit-and-runtime-baseline
    provides: active runtime root and menu contract gap audit
provides:
  - DSPO_Menu parser registration and conservative menu flags
  - ServiceBundle and MenuOffer domain contracts
  - option feature normalization and padded tensor helper
  - aux_dim/output_dim predictor and MemoryBuffer compatibility
  - script-style menu runtime contract regression test
affects: [phase-02, menu-algorithm, simulator, checkpoint-provenance]
tech-stack:
  added: []
  patterns: [script-style tests, narrow compatibility dataclasses, parser-driven menu controls]
key-files:
  created:
    - work2_coding/Src/Utils/MathUtils.py
    - work2_coding/Src/Utils/option_features.py
    - work2_coding/scripts/test_menu_runtime_contract.py
  modified:
    - work2_coding/Src/parser.py
    - work2_coding/Environments/OOH/containers.py
    - work2_coding/Src/Utils/Predictors.py
    - work2_coding/Src/Utils/Utils.py
key-decisions:
  - "Kept menu activation low-side-effect: parser/import/script tests only, no Config(args) construction."
  - "Preserved legacy predictor defaults while adding explicit aux_dim/output_dim support for DSPO_Menu."
  - "Fixed dynamic_load to infer package paths from Src/Environments instead of the stale ooh_code root name."
patterns-established:
  - "Menu runtime compatibility is guarded by executable scripts under work2_coding/scripts/."
  - "Menu diagnostics should flow through MenuOffer.metadata rather than parallel arrays."
requirements-completed: [ACCT-01, ETA-01, MENU-03]
duration: 35min
completed: 2026-06-11
---

# Phase 02 Plan 01: Menu Runtime Contract Summary

**DSPO_Menu is now importable and parser-configurable through work2_coding with narrow menu dataclasses, option feature tensors, and multi-output predictor support**

## Performance

- **Duration:** 35 min
- **Started:** 2026-06-11T04:04:18Z
- **Completed:** 2026-06-11T04:39:00Z
- **Tasks:** 4
- **Files modified:** 7

## Accomplishments

- Registered `DSPO_Menu` in the CLI parser and added conservative `menu_*` defaults, including ETA modes and exact/greedy controls.
- Added `ServiceBundle`, `MenuOffer`, `MathUtils.lambertw`, and `option_features` contracts required by the existing menu algorithm.
- Extended predictors and `MemoryBuffer` so legacy scalar DSPO and menu cost/ETA/IVT outputs both work.
- Added `scripts/test_menu_runtime_contract.py` covering import, parser, dataclass, option tensor, predictor, and replay-buffer contracts.

## Task Commits

1. **Tasks 1-4: Menu runtime contract** - `2b99803` (feat)

**Plan metadata:** pending in docs commit

## Files Created/Modified

- `work2_coding/Src/parser.py` - Added `DSPO_Menu` algorithm choice and Phase 2 menu controls.
- `work2_coding/Environments/OOH/containers.py` - Added menu bundle/offer dataclasses.
- `work2_coding/Src/Utils/option_features.py` - Added six-column option normalization and padding helper.
- `work2_coding/Src/Utils/MathUtils.py` - Added local Lambert W helper with SciPy fallback behavior.
- `work2_coding/Src/Utils/Predictors.py` - Added `aux_dim` and `output_dim` constructor compatibility.
- `work2_coding/Src/Utils/Utils.py` - Added `MemoryBuffer(aux_dim=...)` and dynamic package path inference.
- `work2_coding/scripts/test_menu_runtime_contract.py` - Added deterministic low-side-effect regression script.

## Decisions Made

- Kept defaults conservative: menu mode stays off unless explicitly enabled.
- Included legacy `interval` as a parser alias for later canonicalization in Plan 04.
- Added `MathUtils.py` because `DSPO_Menu` already imported it and importability is part of the runtime contract.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Added missing MathUtils module**
- **Found during:** Plan-level `DSPO_Menu` import check
- **Issue:** `DSPO_Menu.py` imported `Src.Utils.MathUtils.lambertw`, but the module did not exist.
- **Fix:** Added `MathUtils.py` with SciPy delegation and a small principal-branch fallback.
- **Files modified:** `work2_coding/Src/Utils/MathUtils.py`
- **Verification:** `python -c "import sys; sys.path.insert(0, 'work2_coding'); from Src.Algorithms.DSPO_Menu import DSPO_Menu; print('DSPO_MENU_IMPORT_OK')"`
- **Committed in:** `2b99803`

**2. [Rule 3 - Blocking] Repaired dynamic_load root inference for work2_coding**
- **Found during:** Runtime contract inspection
- **Issue:** `dynamic_load()` inferred module paths by searching for stale root segment `ooh_code`.
- **Fix:** Infer package path from `Src` or `Environments` path segments, which matches the active `work2_coding/` root.
- **Files modified:** `work2_coding/Src/Utils/Utils.py`
- **Verification:** Covered by import/parser checks; later `Config(args)` work can reuse the corrected loader.
- **Committed in:** `2b99803`

---

**Total deviations:** 2 auto-fixed (2 blocking)
**Impact on plan:** Both fixes are required to make the existing DSPO_Menu asset importable and compatible with the confirmed active runtime root. No parallel runtime root or experiment artifact was created.

## Issues Encountered

None beyond the auto-fixed import/runtime-contract gaps above.

## User Setup Required

None - no external service configuration required.

## Verification

- `python -c "import sys; sys.path.insert(0, 'work2_coding'); from Src.parser import Parser; p=Parser().get_parser(); args=p.parse_args(['--algo_name','DSPO_Menu','--menu_mode','True','--menu_eta_filter_mode','chance_constraint']); print(args.algo_name, args.menu_mode, args.menu_eta_filter_mode)"` -> `DSPO_Menu True chance_constraint`
- `python -c "import sys; sys.path.insert(0, 'work2_coding'); from Environments.OOH.containers import ServiceBundle, MenuOffer; from Src.Utils.option_features import normalize_features, build_option_tensor; print('MENU_CONTRACT_OK')"` -> `MENU_CONTRACT_OK`
- `python -c "import sys; sys.path.insert(0, 'work2_coding'); from Src.Utils.Predictors import CNN_2d, LinReg; CNN_2d(11,2,16,0.05,aux_dim=4,output_dim=3); LinReg(242,aux_dim=4,output_dim=3); print('PREDICTOR_CONTRACT_OK')"` -> `PREDICTOR_CONTRACT_OK`
- `cd work2_coding; python scripts/test_menu_runtime_contract.py` -> `PASS: 5 menu runtime contract tests`
- `python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"` -> `IMPORT_OK`
- `Test-Path ooh_code` -> false

## Next Phase Readiness

Ready for Plan 02 opt-out accounting and Plan 03 checkpoint provenance. The menu domain surfaces and runtime flags needed by those plans now exist.

---
*Phase: 02-core-semantics-and-robust-menu-logic*
*Completed: 2026-06-11*
