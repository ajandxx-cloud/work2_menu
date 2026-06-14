# Phase 3 Research: Mainline Comparison Contract

**Date:** 2026-06-14
**Status:** Complete
**Mode:** Inline codebase research, no external web lookup

## Current Facts

- `work2_coding/` is the active runtime root. Phase 2 verified `python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` from that directory.
- Phase 2 added and verified normalized-row-v2, service product contracts, product/time-window/menu mode parser choices, contract adapters, failed-row behavior, artifact gates, and a smoke actual replay.
- `policy_adapters.py` currently has Phase 2 `contract_no_menu`, `contract_fixed_menu`, `contract_random_menu`, and `contract_optimized_menu`.
- `smoke_phase2_service_product_contract.yaml` covers `menu_k={1,2,3,5}` using the four Phase 2 `contract_*` tags.
- `smoke_robust_menu.yaml` has been partially upgraded to `normalized-row-v2`, but it still uses the older robust-policy family: full display, home-only, nearest, cheapest, lateness, hard/no-filter, risk-adjusted, service-guarded, random.
- `pilot_robust_menu.yaml` and `formal_robust_menu.yaml` still use `normalized-row-v1` and the older robust-policy family. `formal_robust_menu.yaml` currently has 4 splits, while the project audit says new V1 formal evidence requires at least 5 seeds unless explicitly smoke/pilot.
- `experiment_contracts.py` allows manifests to define `required_policy_tags`. This lets Phase 3 define a new required mainline family without breaking legacy robust adapter coverage.
- `artifact_status.py` already blocks claim-ready artifacts for placeholder rows, failed rows, blocked rows, bad required checkpoints, diagnostic run modes, diagnostic-only rows, and no-filter-only rows.

## Recommended Approach

Use a small adapter expansion and manifest migration instead of inventing a new execution path.

1. Add explicit mainline adapter tags in `policy_adapters.py`.
2. Mark those tags as optional/known, with `comparison_role` values that reflect `menu_mode`, `product_mode`, or `time_window_mode`.
3. Update robust-menu smoke/pilot/formal manifests to use the mainline family and `normalized-row-v2`.
4. Keep existing legacy robust tags available for diagnostics and backward-compatible tests.
5. Strengthen manifest tests so mainline family coverage, smoke/pilot `menu_k={1,2,3,5}` coverage, formal split count, row-v2 fields, and paired fairness are checked before any formal run.
6. Run the actual smoke study to prove the design is executable, not just syntactically valid.

## Proposed Mainline Family

| Tag | Product | Time Window | Menu | Pricing | Runtime Policy | Role |
| --- | --- | --- | --- | --- | --- | --- |
| `mainline_no_menu` | `m` | `no_time_window` | `no_menu` | `no_pricing` | `home_only` | menu baseline |
| `mainline_fixed_menu` | `m+w+p` | `fixed_window` | `fixed_menu` | `lambertw` | `nearest_heuristic` | menu baseline |
| `mainline_random_menu` | `m+w+p` | `fixed_window` | `random_menu` | `lambertw` | `random_top_k` | menu baseline |
| `mainline_optimized_m` | `m` | `no_time_window` | `optimized_menu` | `no_pricing` | `service_guarded_expected_profit` | product ablation |
| `mainline_optimized_mw` | `m+w` | `adaptive_window` | `optimized_menu` | `no_pricing` | `service_guarded_expected_profit` | product ablation |
| `mainline_optimized_fixed_window` | `m+w+p` | `fixed_window` | `optimized_menu` | `lambertw` | `service_guarded_expected_profit` | time-window ablation |
| `mainline_optimized_adaptive` | `m+w+p` | `adaptive_window` | `optimized_menu` | `lambertw` | `service_guarded_expected_profit` | primary method |

This design gives the paper a clean nested interpretation:

- `mainline_no_menu` -> default-service floor.
- `fixed/random/menu optimized` -> menu design value.
- `optimized_m / optimized_mw / optimized_mwp` -> product feature value.
- `fixed_window / adaptive_window` -> robust/adaptive time-window value.

## Risks And Mitigations

- **Risk:** Existing tests expect `required_policy_tags()` legacy robust coverage in `smoke_robust_menu`.
  **Mitigation:** Use manifest-level `required_policy_tags` for mainline manifests and update tests to distinguish legacy adapter availability from mainline manifest requirements.
- **Risk:** Formal checkpoint may not exist.
  **Mitigation:** Keep formal manifest checkpoint-required; tests validate contract and blocked-row behavior without forcing a formal run.
- **Risk:** `m` and `m+w` with optimized menu may expose runtime assumptions around price/window gating.
  **Mitigation:** Add focused tests that resolved rows use `no_pricing` when product mode is not `m+w+p`, and run smoke actual replay across all mainline tags.
- **Risk:** Reusing `work2_robust_menu` names can confuse old artifact claims.
  **Mitigation:** Keep Phase 3 output as contract/smoke only; Phase 4 must regenerate artifacts and status sidecars before manuscript claims.

## Verification Guidance

Minimum Phase 3 verification should run from `work2_coding/`:

```powershell
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_experiment_contracts.py
python scripts/test_policy_fairness_contract.py
python scripts/test_paired_replay_contract.py
python scripts/test_menu_mode_adapters.py
python scripts/test_smoke_study_rows.py
python scripts/test_study_execution_status.py
python scripts/test_artifact_gates.py
python scripts/run_study.py --study smoke_robust_menu --execute --output-root outputs/phase3_verification
```

Do not run or require formal evidence generation in Phase 3.

## Discussion Update

After formal Phase 3 discussion, the user locked these decisions:

- Keep the full 7-tag mainline family.
- Directly migrate existing `work2_robust_menu` manifests/suite to the V1 mainline contract.
- Phase 3 only declares formal 5+ seed/checkpoint contracts; it does not train or run formal.
- Phase 3 includes lightweight artifact eligibility tests only, not artifact builder/table/figure work.
- Smoke and pilot cover `menu_k={1,2,3,5}`; formal fixes `menu_k=3`.

## RESEARCH COMPLETE
