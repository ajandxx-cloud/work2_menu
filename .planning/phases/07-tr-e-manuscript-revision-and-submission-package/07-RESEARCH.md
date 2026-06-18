# Phase 07 Research - TR-E Manuscript Revision And Submission Package

**Phase:** 07 - TR-E Manuscript Revision And Submission Package  
**Research date:** 2026-06-18  
**Mode:** inline plan-phase research  
**Status:** ready for planning

## Research Question

How should Phase 7 revise the current conditional diagnostic manuscript into a
TR-E-ready draft while preserving `claim_ready=false`, the current strict claim
guard, and the generated-evidence boundary?

## Source Basis

This research is based on local project context only. No internet research,
final replay, calibration, artifact regeneration, claim upgrade, case-study
execution, or generated-row editing was performed.

Primary inputs:

- `.planning/PROJECT.md`
- `.planning/REQUIREMENTS.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `.planning/research/SUMMARY.md`
- `.planning/phases/07-tr-e-manuscript-revision-and-submission-package/07-CONTEXT.md`
- `.planning/milestones/tr_e_completion/M6_FINAL_TR_E_READINESS_AUDIT.md`
- `manuscript/TR_E_WORK2_FINAL_REVISION_TASKS.md`
- `.planning/milestones/tr_e_completion/M4B_DIAGNOSTIC_MANUSCRIPT_LOCK.md`
- `.planning/milestones/tr_e_completion/M4B_SAFE_CLAIM_TABLE.md`
- `.planning/paper/TR_E_RESEARCH_DESIGN.md`
- `.planning/paper/TR_E_MANUSCRIPT_STRUCTURE.md`
- `.planning/paper/CLAIM_SAFE_LANGUAGE.md`
- `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md`
- `manuscript/TR_E_WORK2_MANUSCRIPT_DRAFT.md`
- `manuscript/TR_E_WORK2_CLAIM_AUDIT.md`
- `manuscript/TR_E_WORK2_TABLE_FIGURE_SOURCE_MAP.md`
- `manuscript/TR_E_WORK2_PROHIBITED_LANGUAGE_CHECK.md`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`

## Current Manuscript And Evidence State

The Phase 5 draft exists at `manuscript/TR_E_WORK2_MANUSCRIPT_DRAFT.md` and
already has the required section spine from Abstract through Appendix. Phase 7
should preserve that file as historical input and create a new manuscript at
`manuscript/TR_E_WORK2_MANUSCRIPT_REVISED.md`.

The current package is not claim-ready:

- `claim_ready=false`
- `strict_claim_guard_claim_ready=false`
- `manuscript_positive_claims_allowed=false`
- 74 package artifacts
- 70 existing artifacts
- 4 missing artifacts
- 108 blockers

Blocked strict claims:

- `C1_central_adaptive_menu_superiority`
- `C2_product_ablation_value`
- `C3_adaptive_window_increment`
- `C4_menu_construction_value`
- `C6_exact_greedy_computational_credibility`
- `C8_semi_real_case_validation`

Allowed or usable boundaries:

- `C5_eta_robustness_boundary` is diagnostic-only.
- `C7_provenance_status_transparency` is status/provenance transparency only.

Final replay was not run. The diagnostic manuscript path is locked by Phase 4
because pre-replay readiness was blocked by `dirty_git` and
`missing_formal_checkpoint`.

## Planning Implications

Phase 7 should be an execution phase with three sequential work streams:

1. **Core manuscript rewrite:** Create the revised manuscript and deeply rewrite
   the front matter, Introduction, Literature Review, Problem Description,
   Mathematical Model, and Solution Method around the service-menu contribution.
2. **Claim-gated evidence integration:** Rework Experimental Design, Results,
   Discussion, Conclusion, and Appendix so claim-gate status leads the evidence
   narrative without turning the paper into a package-status dump.
3. **Submission package verification:** Create the lean revision summary and
   revised prohibited-language check, then run manuscript-focused verification.

The Mathematical Model must be reviewer-readable without planning artifacts and
must define candidate bundles, displayed menus, MNL response probabilities,
objective components, feasibility constraints, outside option, accepted home
pickup, accepted meeting-point pickup, and opt-out accounting.

The Solution Method should include concise pseudocode for the diagnostic
service-menu evaluation pipeline: state input, candidate bundle generation,
ETA/window feasibility, pricing, menu selection, replay logging, and claim-gate
reporting.

## Scope Guardrails

Phase 7 must not:

- Run final replay, calibration, checkpoint training, case-study execution, or
  artifact regeneration.
- Upgrade `CLAIM_GUARD.json` or any manuscript claim by wording.
- Hand-edit generated rows, package status, package indexes, claim guards,
  generated tables, generated figures, artifact mirrors, or source rows.
- Present no-filter material as an operational recommendation.
- Present exact/greedy material as computational credibility or near-optimality.
- Present scaffold-only case material as real passenger behavior or validation.
- Revive stale `ooh_code/` paths.

## Recommended Plan Split

Use three sequential plans:

- `07-01-PLAN.md`: Revised manuscript core narrative, model, and method.
- `07-02-PLAN.md`: Claim-gated evidence sections, appendix, and source-map
  synchronization.
- `07-03-PLAN.md`: Revision summary, revised prohibited-language scan, and
  verification closeout.

This split keeps writing work manageable while preserving traceability and
claim-safety verification as first-class deliverables.

## Verification Strategy

Minimum Phase 7 checks:

```powershell
cd work2_coding
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_manuscript_claim_guard.py
python scripts/test_manuscript_readiness_package.py
```

Repository-root checks:

```powershell
Test-Path manuscript/TR_E_WORK2_MANUSCRIPT_REVISED.md
Test-Path manuscript/TR_E_WORK2_REVISION_SUMMARY.md
Test-Path manuscript/TR_E_WORK2_REVISED_PROHIBITED_LANGUAGE_CHECK.md
rg -n -i "dominat|superior|outperform|near[- ]optimal|real passenger|case-study validation|semi-real validation|no-filter recommendation|operationally recommended|DSPO_PLUS|Behavior-Aware|TR-C|ranking validation|adaptive windows improve|greedy optimal" manuscript/TR_E_WORK2_MANUSCRIPT_REVISED.md
```

If `manuscript/TR_E_WORK2_TABLE_FIGURE_SOURCE_MAP.md` is updated, verify that
it still contains `Source artifact path`, `Claim ID`, `Claim status`,
`Allowed manuscript use`, and `Evidence class`, and that any concrete source
paths are real local paths or clearly labeled conceptual/scaffold sources.

## RESEARCH COMPLETE
