# Phase 2 Code Review: Service Product Contract

**Date:** 2026-06-14  
**Status:** Passed after one closeout fix  
**Runtime root:** `work2_coding/`

## Scope

Reviewed Phase 2 contract surfaces and execution gates:

- `ServiceProduct` adapters around `ServiceBundle` and `MenuOffer`.
- Parser contract args: `product_mode`, `time_window_mode`, and `menu_contract_mode`.
- Policy adapters for `contract_no_menu`, `contract_fixed_menu`, `contract_random_menu`, and `contract_optimized_menu`.
- `normalized-row-v2` schema construction and validation.
- `DSPO_Menu` metadata propagation and product utility gating.
- Failed-row handling and artifact claim gates.

## Findings

### Fixed: actual replay summaries could hide row-level failures

Severity: Warning  
Files: `work2_coding/scripts/run_study.py`, `work2_coding/scripts/test_study_execution_status.py`

During review, `actual_rows_for_manifest()` was found to continue after per-setting failures by writing `status="failed"` rows, but `execute_study()` still marked the study summary as `execution_status="completed"` whenever the outer replay call returned normally. That could make a run summary look completed while normalized rows contained failed executions.

Resolution:

- Added `_failed_row_blockers()` to convert row-level actual replay failures into explicit summary blockers.
- Updated `execute_study()` so actual replay summaries become `execution_status="failed"` when any normalized row is failed.
- Added `test_actual_replay_failed_rows_mark_summary_failed()` to lock the behavior.

## Review Result

No remaining blocker was found for Phase 2 closeout.

The reviewed implementation now preserves these Phase 2 contracts:

- `m` disables window utility and passenger price utility.
- `m+w` enables window utility and disables passenger price utility.
- `m+w+p` enables both window and passenger price utility.
- Failed policy/split executions produce normalized failed rows with error metadata.
- Claim/artifact gates exclude failed, blocked, contract-only, placeholder, diagnostic-only, and no-filter-only evidence from formal claims.
- Actual smoke replay rows carry the required `normalized-row-v2` contract fields.

## Residual Risk

This review validates Phase 2 contract readiness only. It does not claim formal experimental evidence, regenerate paper artifacts, or establish 5-seed formal comparisons.
