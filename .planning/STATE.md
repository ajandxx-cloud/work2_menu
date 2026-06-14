---
gsd_state_version: 1.0
milestone: v1.1
milestone_name: Work2_TR_PartC_Paper_Rewriting_and_Experiment_Rebuild_RC
status: verifying
last_updated: "2026-06-14T13:07:31.188Z"
last_activity: 2026-06-14
progress:
  total_phases: 6
  completed_phases: 4
  total_plans: 12
  completed_plans: 15
  percent: 67
---

# State

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-06-14)

**Core value:** A defensible TR-C manuscript whose DSPO, DSPO_PLUS,
static-pricing, and no-pricing comparisons are reproducible, behaviorally
coherent, and gated before empirical superiority claims are made.

**Current focus:** Phase 09 — dspo-family-full-run

## Current Position

Phase: 09 (dspo-family-full-run) — EXECUTING
Plan: 3 of 3
Status: Phase complete — ready for verification
Last activity: 2026-06-14

## Recent Verification

Runtime root: `work2_coding/`

Verified from `work2_coding/` on 2026-06-14:

```powershell
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_artifact_gates.py
python scripts/test_smoke_study_rows.py
python scripts/test_experiment_contracts.py
python scripts/run_study.py --study smoke_robust_menu --execute --output-root outputs/phase4_verification
python scripts/build_artifacts.py --run-dir outputs/phase4_verification/smoke_robust_menu/smoke_robust_menu-20260614T021107Z-759dc2ce --output-root outputs/phase4_artifacts --allow-incomplete
python scripts/build_manuscript_frame.py --artifact-root outputs/phase4_artifacts
```

Phase 4 smoke actual replay completed 28 rows with all seven mainline policy
tags and no blockers. Phase 4 artifact generation produced diagnostic/status
artifacts, ranking/baseline outputs, and `CLAIM_GUARD.json`.

Phase 5 implemented formal readiness preflight, dependency snapshot reporting,
checkpoint load-smoke gates, and formal `--claim-ready` artifact enforcement.
Focused tests passed. Current formal readiness JSON reports the formal
checkpoint as loaded with a dependency snapshot present, but still blocks formal
claim-ready status on `dirty_git`, as intended.

Phase 6 implemented the runtime/code/experiment audit matrix and closeout
handoff. Required lightweight checks passed:

```powershell
python scripts/test_phase6_audit.py
python scripts/test_experiment_contracts.py
python scripts/test_artifact_gates.py
python scripts/test_smoke_study_rows.py
python scripts/test_policy_fairness_contract.py
python scripts/test_optout_accounting.py
python scripts/test_checkpoint_provenance.py
```

Phase 6 outputs:

- `.planning/phases/06-code-and-experiment-audit/06-VERIFICATION.md`
- `.planning/phases/06-code-and-experiment-audit/06-SUMMARY.md`
- `work2_coding/outputs/phase6_audit/PHASE6_AUDIT.json`
- `work2_coding/outputs/phase6_audit/PHASE6_AUDIT.md`

Phase 7 implemented the model-consistency repair. Required focused checks
passed:

```powershell
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_mnl_choice_contract.py
python scripts/test_method_family_contract.py
python scripts/test_optout_accounting.py
python scripts/test_experiment_contracts.py
python scripts/test_artifact_gates.py
python scripts/test_checkpoint_provenance.py
python scripts/test_phase7_model_consistency_report.py
python scripts/build_phase7_model_consistency_report.py --output-root outputs/phase7_model_consistency
```

Phase 7 outputs:

- `.planning/phases/07-model-consistency-repair/07-VERIFICATION.md`
- `.planning/phases/07-model-consistency-repair/07-SUMMARY.md`
- `work2_coding/outputs/phase7_model_consistency/PHASE7_MODEL_CONSISTENCY.json`
- `work2_coding/outputs/phase7_model_consistency/PHASE7_MODEL_CONSISTENCY.md`

Phase 8 implemented and ran paired baseline validation for
`mainline_optimized_mw` and `phase8_static_flat_markdown`. Required focused
checks passed:

```powershell
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_phase8_baseline_validation.py
python scripts/test_experiment_contracts.py
python scripts/test_policy_fairness_contract.py
python scripts/test_artifact_gates.py
python scripts/test_checkpoint_provenance.py
python scripts/test_optout_accounting.py
python scripts/build_phase8_baseline_validation_report.py --output-root outputs/phase8_baseline_validation
```

Phase 8 outputs:

- `.planning/phases/08-baseline-validation/08-VERIFICATION.md`
- `.planning/phases/08-baseline-validation/08-SUMMARY.md`
- `work2_coding/outputs/studies/phase8_baseline_validation/phase8_baseline_validation-20260614T111317Z-1e1ee9fb`
- `work2_coding/outputs/phase8_baseline_validation/PHASE8_BASELINE_VALIDATION.json`
- `work2_coding/outputs/phase8_baseline_validation/PHASE8_BASELINE_VALIDATION.md`

Phase 9 executed actual paired replay for `dspo_clip` and `dspo_wide` across
the five Phase 8-equivalent splits. The Phase 9 report opened the DSPO
validation gate while keeping `claim_ready=false` and ranking claims locked.

Phase 9 outputs:

- `work2_coding/outputs/studies/phase9_dspo_family_validation/phase9_dspo_family_validation-20260614T130443Z-0cf5543f`
- `work2_coding/outputs/phase9_dspo_family_validation/PHASE9_DSPO_FAMILY_VALIDATION.json`
- `work2_coding/outputs/phase9_dspo_family_validation/PHASE9_DSPO_FAMILY_VALIDATION.md`

## Current Notes

- Active runtime root is `work2_coding/`.
- `.planning/codebase/` still contains stale `ooh_code/` references; use
  `.planning/repository_audit.md` for current path mapping.

- Existing Work2 source and test changes are already present in the worktree and
  should be preserved.

- Manuscript source may be edited for TR-C structure and Elsevier formatting,
  but generated result rows, generated tables, generated figures, and
  claim-ready artifacts must not be hand-edited.

- Attention artifacts remain V2/diagnostic and are not V1 ranking evidence.
- Phase 9 DSPO clip/wide replay has been executed, but final ranking claims
  and claim-ready artifacts remain gated.

- Real formal readiness report:
  `work2_coding/outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json`

## Next Step

Verify Phase 9 DSPO family full run, then proceed only to manuscript status
and reviewer-risk language unless a later gate explicitly unlocks ranking
claims.

---
*Updated: 2026-06-14 after completing Phase 9 DSPO family validation*
