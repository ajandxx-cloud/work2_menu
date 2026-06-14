---
phase: 4
plan: 04-02-mainline-artifact-bundle-and-ranking
status: complete
completed: 2026-06-14
key_files:
  - work2_coding/Src/artifact_builder.py
  - work2_coding/scripts/test_artifact_gates.py
---

# 04-02 Summary: Mainline Artifact Bundle And Ranking

## Result

Artifact bundle generation is now mainline-aware.

- `mainline_no_menu` is excluded from `recommended_policy_ranking.json`.
- `mainline_no_menu` is emitted through baseline/boundary reporting.
- The ranking-eligible mainline tags are:
  - `mainline_fixed_menu`
  - `mainline_random_menu`
  - `mainline_optimized_m`
  - `mainline_optimized_mw`
  - `mainline_optimized_fixed_window`
  - `mainline_optimized_adaptive`
- Existing diagnostic and cost-bound exclusions remain in place.
- The artifact bundle still emits aggregates, LaTeX tables, figures/status
  sidecars, `ARTIFACT_STATUS.json`, README, and metadata sidecars.

## Verification

Run from `work2_coding/`:

```powershell
python scripts/test_artifact_gates.py
python scripts/build_artifacts.py --run-dir outputs/phase3_verification/smoke_robust_menu/smoke_robust_menu-20260614T012930Z-759dc2ce --output-root outputs/phase4_artifact_probe --allow-incomplete
```

Results:

```text
PASS: 12 artifact gate tests
```

The artifact build probe completed with:

- `artifact_status.status`: `diagnostic`
- `claim_ready`: `false`
- reason: `smoke artifacts are diagnostic/status evidence only`
- ranking tags: six operational mainline tags
- baseline tags: `mainline_no_menu`

## Deviations

None.

## Self-Check

PASSED. The implementation covers D-01, D-03, and D-09 through D-13 without
editing manuscript source or generated result rows by hand.
