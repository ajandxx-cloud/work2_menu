# Phase 2 Verification: Service Product Contract

**Date:** 2026-06-14  
**Status:** Passed  
**Runtime root:** `work2_coding/`

## Verification Commands

All commands were run from `work2_coding/`.

```powershell
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_service_product_contract.py
python scripts/test_paired_replay_contract.py
python scripts/test_menu_mode_adapters.py
python scripts/test_product_time_window_modes.py
python scripts/test_artifact_gates.py
python scripts/test_experiment_contracts.py
python scripts/test_menu_runtime_contract.py
python scripts/test_smoke_study_rows.py
python scripts/test_study_execution_status.py
python scripts/run_study.py --study smoke_phase2_service_product_contract --execute --output-root outputs/phase2_verification
```

## Results

Script verification passed:

- `IMPORT_OK`
- `PASS: 4 service product contract tests`
- `PASS: 11 paired replay contract tests`
- `PASS: 4 menu mode adapter tests`
- `PASS: 4 product time-window mode tests`
- `PASS: 9 artifact gate tests`
- `PASS: 13 experiment contract tests`
- `PASS: 5 menu runtime contract tests`
- `PASS: 9 smoke study row tests`
- `PASS: 9 study execution status tests`

Actual Phase 2 smoke replay passed:

- Run directory: `work2_coding/outputs/phase2_verification/smoke_phase2_service_product_contract/smoke_phase2_service_product_contract-20260614T004638Z-f9ea8529`
- `execution_status`: `completed`
- `contract_only`: `false`
- `placeholder_only`: `false`
- `blocker_count`: `0`
- `row_count`: `16`
- `checkpoint_statuses`: `["not_requested"]`

Normalized-row acceptance passed:

- All rows use `schema_version="normalized-row-v2"`.
- All rows have `status="completed"` and `execution_status="completed"`.
- Required v2 fields are present and non-empty, except `error_type` and `error_message`, which are intentionally empty for completed rows.
- `contract_no_menu` maps to `m / no_time_window / no_menu / no_pricing`.
- `contract_fixed_menu` maps to `m+w+p / fixed_window / fixed_menu / lambertw`.
- `contract_random_menu` maps to `m+w+p / fixed_window / random_menu / lambertw`.
- `contract_optimized_menu` maps to `m+w+p / adaptive_window / optimized_menu / lambertw`.

## Phase 2 Closeout

Phase 2 is verified as a contract and smoke-replay foundation for Phase 3. The implementation exposes service product, product-mode, time-window-mode, menu-mode, pricing-mode, failed-row, and artifact-gate contracts required for downstream experiment design.

Deferred to Phase 3 or later:

- Formal 5-seed evidence.
- Paper artifact regeneration.
- Mainline product/time-window/menu comparison design.
- Claim-ready conclusions about `m`, `m+w`, `m+w+p`, `no_menu`, `fixed_menu`, `random_menu`, and `optimized_menu`.
