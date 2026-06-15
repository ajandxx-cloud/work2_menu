---
phase: 08-sensitivity-and-robustness-experiments
status: verified
verified_at: 2026-06-15T16:02:28Z
requirements: [SENS-01, SENS-02, SENS-03]
claim_ready: false
artifact_status: diagnostic_provisional_blocked
---

# Phase 8 Verification

## Verdict

Phase 8 is verified as complete for diagnostic/provisional sensitivity coverage. It is not claim-ready evidence and does not authorize manuscript abstract, conclusion, or managerial claim upgrades.

## Goal Checks

- Baseline validation ran before sensitivity replay and returned `PHASE8_BASELINE_VALIDATION_STATUS=passed`.
- Sensitivity replay ran only for the four must-have executable dimensions: `menu_k`, `eta_filter_mode`, `uptake_regime`, and `guardrail`.
- Nice-to-have dimensions remained deferred: candidate pool size, fleet/capacity stress, pricing bounds, and price sensitivity.
- Generated artifacts were produced under `work2_coding/artifacts/work2_robust_menu/phase8_sensitivity/` from normalized rows and manifest snapshots.
- `.planning/results/SENSITIVITY_SUMMARY.md` includes guarded frontmatter, all four axes, deferred dimensions, source artifact paths, and a claim boundary.
- Boundary labels distinguish exact ties as `no_observed_change`, preventing tied outcomes from being overstated as help.

## Source Evidence

- Baseline report: `work2_coding/outputs/phase8_baseline_validation/PHASE8_BASELINE_VALIDATION.json` (ignored local output).
- Sensitivity artifact status: `work2_coding/artifacts/work2_robust_menu/phase8_sensitivity/ARTIFACT_STATUS.json`.
- Sensitivity aggregate: `work2_coding/artifacts/work2_robust_menu/phase8_sensitivity/aggregates/sensitivity_axis_summary.json`.
- Planning summary: `.planning/results/SENSITIVITY_SUMMARY.md`.
- Code review: `.planning/phases/08-sensitivity-and-robustness-experiments/08-REVIEW.md`.

## Verification Commands

- `python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` - passed.
- `python scripts/test_phase8_sensitivity_contracts.py` - passed.
- `python scripts/test_phase8_sensitivity_summary.py` - passed.
- `python scripts/test_phase8_baseline_validation.py` - passed.
- `python scripts/test_artifact_gates.py` - passed.
- `python scripts/test_paired_replay_contract.py` - passed.
- `python scripts/test_policy_fairness_contract.py` - passed.
- `Select-String -Path .planning/results/SENSITIVITY_SUMMARY.md -Pattern "diagnostic_provisional_blocked","claim_ready: false"` - passed.

## Residual Risks

- Raw replay rows are ignored local outputs by repository policy; generated artifacts and metadata record their source run directories.
- Dirty-git provenance from broader pre-existing workspace changes remains visible in generated metadata, so Phase 8 appropriately remains diagnostic/provisional and not claim-ready.
- The suite runner printed a top-level `execution_status: contract_only`, while each member study summary and generated artifact validation reported completed rows. Phase 8 closeout relies on member-level summaries and artifact validation.
