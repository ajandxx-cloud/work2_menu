---
phase: 3
phase_name: Mainline Comparison Contract
status: passed
verified: 2026-06-14
runtime_root: work2_coding
smoke_output: work2_coding/outputs/phase3_verification/smoke_robust_menu/smoke_robust_menu-20260614T012930Z-759dc2ce
---

# Phase 3 Verification

## Result

Phase 3 passed. The `work2_robust_menu` smoke, pilot, and formal manifests now define the V1 seven-tag mainline comparison family:

- `mainline_no_menu`
- `mainline_fixed_menu`
- `mainline_random_menu`
- `mainline_optimized_m`
- `mainline_optimized_mw`
- `mainline_optimized_fixed_window`
- `mainline_optimized_adaptive`

The legacy robust-policy adapter tags remain available for diagnostic/compatibility manifests, but they are no longer the required family for the V1 `work2_robust_menu` mainline manifests.

## Commands Run

All commands were run from `work2_coding/`.

```powershell
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_menu_mode_adapters.py
python scripts/test_experiment_contracts.py
python scripts/test_policy_fairness_contract.py
python scripts/test_paired_replay_contract.py
python scripts/test_smoke_study_rows.py
python scripts/test_study_execution_status.py
python scripts/test_artifact_gates.py
python scripts/test_menu_runtime_contract.py
python scripts/test_product_time_window_modes.py
python scripts/test_service_product_contract.py
python scripts/run_study.py --study smoke_robust_menu --execute --output-root outputs/phase3_verification
```

## Automated Results

- Import smoke: passed (`IMPORT_OK`)
- Adapter tests: passed, 6 tests
- Experiment manifest tests: passed, 15 tests
- Policy fairness tests: passed, 13 tests
- Paired replay row tests: passed, 12 tests
- Smoke study row tests: passed, 9 tests
- Study execution status tests: passed, 9 tests
- Artifact gate tests: passed, 9 tests
- Optional menu runtime contract tests: passed, 5 tests
- Optional product/time-window tests: passed, 4 tests
- Optional service product tests: passed, 4 tests
- Actual smoke replay: completed

## Smoke Replay Output

Output directory:

```text
work2_coding/outputs/phase3_verification/smoke_robust_menu/smoke_robust_menu-20260614T012930Z-759dc2ce
```

Observed `study_summary.json` and `normalized_rows.json`:

- `execution_status`: `completed`
- `row_count`: 28
- `schema_version`: `normalized-row-v2`
- `status` values: `completed`
- `execution_status` row values: `completed`
- `checkpoint_load_status` values: `not_requested`
- `menu_k` coverage: `{1, 2, 3, 5}`
- `policy_tag` coverage: all seven mainline tags

Mainline method coverage:

| Policy tag | Method |
| --- | --- |
| `mainline_no_menu` | `m__no_time_window__no_menu__no_pricing` |
| `mainline_fixed_menu` | `m+w+p__fixed_window__fixed_menu__lambertw` |
| `mainline_random_menu` | `m+w+p__fixed_window__random_menu__lambertw` |
| `mainline_optimized_m` | `m__no_time_window__optimized_menu__no_pricing` |
| `mainline_optimized_mw` | `m+w__adaptive_window__optimized_menu__no_pricing` |
| `mainline_optimized_fixed_window` | `m+w+p__fixed_window__optimized_menu__lambertw` |
| `mainline_optimized_adaptive` | `m+w+p__adaptive_window__optimized_menu__lambertw` |

## Scope Guardrails

- No manuscript source was edited.
- No generated paper-facing tables or figures were created or hand-edited.
- Formal replay was not executed.
- Formal checkpoint training was not executed.
- Deleted root planning files `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, and `.planning/STATE.md` were not recreated.
- `no_filter_diagnostic` remains diagnostic/legacy only and is not present in the V1 mainline manifests.

## Phase 4 Handoff

- Make artifact building mainline-aware and consume `normalized-row-v2` outputs from the seven-tag family.
- Keep claim guards excluding diagnostic, failed, blocked, placeholder, no-filter-only, and bad-checkpoint rows.
- Require formal checkpoint provenance and a dependency snapshot before formal rows become claim-ready.
- Build mirrored artifact bundles and manuscript-facing tables/figures from regenerated outputs, not by editing result rows by hand.
