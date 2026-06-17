# M4B Safe Claim Table

**Source guard:** `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`  
**Source package:** `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`  
**Current package claim_ready:** `false`  

## Global Manuscript Rules

Preserve these evidence boundaries in Phase 5:

- Opt-out remains separate from accepted home pickup and accepted meeting-point pickup.
- No-filter evidence remains diagnostic only and is not an operational recommendation.
- Case-study material remains scaffold-only and cannot validate real passenger behavior.
- Exact/greedy evidence remains blocked diagnostic material and cannot support near-optimality or computational credibility claims.
- Strict claim guard output is the claim ceiling.

Prohibited wording unless a future strict guard authorizes the exact claim:

- dominates
- superior
- improves
- validates real passengers
- near-optimal
- outperforms
- proves
- case-study validation
- real passenger behavior

## Claim Table

| Claim ID | Current support status | claim_ready | manuscript_allowed | Source artifact path | Allowed manuscript use | Blocker reason | Prohibited language |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `C1_central_adaptive_menu_superiority` | unsupported_blocked | false | false | `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`; `work2_coding/artifacts/work2_robust_menu/ARTIFACT_STATUS.json` | Not allowed as a positive claim. May report the comparison as generated artifact/status structure only. | Main RC artifacts are blocked by checkpoint/formal readiness status; positive superiority requires claim-ready generated rows. | adaptive menu dominates; universal dominance; claim-ready superiority; robust menu is better than all baselines; superior |
| `C2_product_ablation_value` | conditional_diagnostic_blocked | false | false | `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`; `work2_coding/artifacts/work2_robust_menu/phase8_sensitivity/` | Diagnostic structure or boundary discussion only. | Phase 8 sensitivity artifacts are appendix diagnostics, not claim-ready evidence. | product ablation proves; adaptive window increment is validated; claim-ready ablation value; improves |
| `C3_adaptive_window_increment` | unsupported | false | false | `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`; `work2_coding/artifacts/work2_robust_menu/ARTIFACT_STATUS.json` | Not allowed. Fixed-window and adaptive-window slots may be listed without directional effect language. | Adaptive-window increment must not be inferred from diagnostic appendices or blocked main RC artifacts. | adaptive windows improve; adaptive window increment; adaptive window advantage; improves |
| `C4_menu_construction_value` | conditional_diagnostic_blocked | false | false | `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`; `work2_coding/artifacts/work2_robust_menu/phase9_tractability/` | Discuss menu construction as an auditable diagnostic mechanism only. | Exact/greedy and menu-construction material is computational-boundary evidence only. | menu construction proves value; near-optimal greedy; greedy is optimal; dominates |
| `C5_eta_robustness_boundary` | diagnostic_only | false | true | `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`; `work2_coding/artifacts/work2_robust_menu/phase8_sensitivity/` | Diagnostic ETA robustness boundary discussion only. | ETA/no-filter evidence is diagnostic and cannot support operational recommendation language. | no-filter recommendation; no-filter is operationally recommended; no-filter policy should be deployed |
| `C6_exact_greedy_computational_credibility` | blocked_diagnostic | false | false | `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`; `work2_coding/artifacts/work2_robust_menu/phase9_tractability/` | Computational diagnostic appendix only. | Phase 9 exact/greedy outputs are diagnostic computational boundary artifacts and do not establish credibility. | near-optimal greedy; full dynamic exact optimality; greedy optimality; near-optimal |
| `C7_provenance_status_transparency` | status_supported | true | true | `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`; `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`; `.planning/milestones/tr_e_completion/M4A_PRE_REPLAY_GATE_REPORT.md` | Allowed as provenance/status transparency only. | This claim reports transparent blocker, diagnostic, scaffold, and claim-gate status; it does not prove empirical effectiveness. | status transparency proves effectiveness; provenance resolves empirical blockers |
| `C8_semi_real_case_validation` | scaffold_only_blocked | false | false | `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`; `.planning/data/case_studies/` | Future-study scaffold only. Do not use as validation evidence. | Case-study files are scaffold-only and contain no runtime validation evidence. | case-study validation; semi-real validation; real passenger behavior; validates real passengers; validated on real data |

## Phase 5 Handoff

Phase 5 can use C7 for transparent status/provenance reporting and C5 for diagnostic boundary discussion. All other claims are blocked from positive manuscript language.

Every table or figure must carry source artifact path, claim ID, claim status, allowed use, and whether the object is generated evidence, diagnostic evidence, blocked status, scaffold-only material, or conceptual illustration.
