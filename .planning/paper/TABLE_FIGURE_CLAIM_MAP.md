# Table, Figure, And Claim Map

**Current package:** `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/`
**Mirror package:** `artifacts/work2_robust_menu/phase10_paper_artifacts/`
**Current strict status:** `claim_ready=false`

## Current Allowed Use Summary

| Evidence family | Current status | Allowed manuscript use |
| --- | --- | --- |
| Main RC | blocked | Status/provenance discussion only until gates pass |
| Phase 8 sensitivity | diagnostic_provisional_blocked | Diagnostic appendix or boundary discussion only |
| Phase 9 tractability | diagnostic_provisional_blocked | Computational diagnostic appendix only |
| Case scaffold | scaffold_only_no_result_evidence | Future-work or scaffold description only |
| Blocker status | blocked | Provenance/status transparency only |

## Claim Map

| Claim ID | Current status | Allowed use |
| --- | --- | --- |
| C1_central_adaptive_menu_superiority | unsupported_blocked | Not allowed |
| C2_product_ablation_value | conditional_diagnostic_blocked | Diagnostic structure only |
| C3_adaptive_window_increment | unsupported | Not allowed |
| C4_menu_construction_value | conditional_diagnostic_blocked | Diagnostic mechanism only |
| C5_eta_robustness_boundary | diagnostic_only | Diagnostic boundary only |
| C6_exact_greedy_computational_credibility | blocked_diagnostic | Diagnostic computational boundary only |
| C7_provenance_status_transparency | status_supported | Allowed as provenance/status transparency |
| C8_semi_real_case_validation | scaffold_only_blocked | Not allowed |

## Current Artifact Sources

| Manuscript section | Source artifact path | Current use |
| --- | --- | --- |
| Experimental Design | `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/ARTIFACT_TO_SECTION_MAP.json` | Source map and evidence inventory |
| Results - claim gate status | `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json` | Claim ceiling |
| Results - package status | `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json` | Blocker and artifact family summary |
| Results - main RC artifacts | `work2_coding/artifacts/work2_robust_menu/aggregates/policy_summary.json` | Blocked/status only unless regenerated |
| Sensitivity appendix | `work2_coding/artifacts/work2_robust_menu/phase8_sensitivity/` | Diagnostic/provisional only |
| Computational appendix | `work2_coding/artifacts/work2_robust_menu/phase9_tractability/` | Diagnostic/provisional only |
| Case-study appendix | `.planning/data/case_studies/` | Scaffold/future work only |

## Required Rule For New Tables And Figures

Every manuscript table or figure must record:

1. Source artifact path.
2. Claim ID.
3. Claim status.
4. Allowed manuscript use.
5. Whether the object is generated evidence, diagnostic evidence, blocked
   status, scaffold-only material, or conceptual illustration.

Conceptual figures must be labeled as conceptual and must not support
empirical claims.
