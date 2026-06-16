---
phase: 11
status: table_figure_claim_map
generated_at: 2026-06-16T14:11:38+08:00
timezone: Asia/Shanghai
source_package_index: work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_INDEX.json
source_section_map: work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/ARTIFACT_TO_SECTION_MAP.json
source_claim_guard: work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json
claim_ready: false
manuscript_positive_claims_allowed: false
---

# Table And Figure Claim Map

## Evidence Rules

Every proposed table or figure below traces to a source artifact indexed in the
Phase 10 package. These are manuscript planning entries only. No generated
result rows, evidence tables, figures, or paper artifacts may be hand-edited to
change evidence or claims.

Status key:

- **supported:** allowed only for C7 provenance/status transparency.
- **diagnostic/provisional:** can be discussed only with `claim_ready=false`.
- **unsupported:** can appear only as blocked status, limitation, or future-work
  context.

## Proposed Tables

| Manuscript item | Source artifact path | Phase 10 package entry | Supported claim | Section | Claim status | Use boundary |
| --- | --- | --- | --- | --- | --- | --- |
| T1. Evidence package and source-family status | `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json` | Phase 10 package status output | C7 provenance/status transparency | Experimental Design or Appendix | supported | Show artifact counts, source families, tiers, and `claim_ready=false`; do not infer effectiveness |
| T2. Strict claim guard summary | `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json` | Phase 10 strict guard output | C7 provenance/status transparency | Results or Appendix | supported | Summarize eight claims and status only; no claim upgrade |
| T3. Main RC policy summary status table | `work2_coding/artifacts/work2_robust_menu/tables/policy_summary.tex` | `main_rc:table:work2_coding_artifacts_work2_robust_menu_tables_policy_summary_tex` | C1 central adaptive menu superiority | Results | unsupported | Include only as blocked/status surface if used; cannot support central superiority |
| T4. Uptake-regime diagnostic/status table | `work2_coding/artifacts/work2_robust_menu/tables/uptake_regime.tex` | `main_rc:table:work2_coding_artifacts_work2_robust_menu_tables_uptake_regime_tex` | C2 product ablation value; C4 menu construction value | Results or Appendix | diagnostic/provisional | Current main RC artifact is blocked; use as diagnostic structure only |
| T5. Robust filtering status table | `work2_coding/artifacts/work2_robust_menu/tables/robust_filtering.tex` | `main_rc:table:work2_coding_artifacts_work2_robust_menu_tables_robust_filtering_tex` | C5 ETA robustness boundary | Results or Appendix | diagnostic/provisional | Use only with blocked main RC status and no-filter diagnostic wording |
| T6. Phase 8 sensitivity axis summary | `work2_coding/artifacts/work2_robust_menu/phase8_sensitivity/tables/sensitivity_axis_summary.tex` | `phase8_sensitivity:table:work2_coding_artifacts_work2_robust_menu_phase8_sensitivity_tables_sensitivity_axis_summary_tex` | C5 ETA robustness boundary; C2/C4 diagnostic boundaries | Results or Appendix | diagnostic/provisional | Report boundary patterns only; no robustness proof |
| T7. Phase 8 sensitivity boundary map | `work2_coding/artifacts/work2_robust_menu/phase8_sensitivity/tables/sensitivity_boundary_map.tex` | `phase8_sensitivity:table:work2_coding_artifacts_work2_robust_menu_phase8_sensitivity_tables_sensitivity_boundary_map_tex` | C5 ETA robustness boundary; C2/C4 diagnostic boundaries | Appendix | diagnostic/provisional | Label as diagnostic boundary map with `claim_ready=false` |
| T8. Phase 9 exact-greedy tractability table | `work2_coding/artifacts/work2_robust_menu/phase9_tractability/tables/exact_greedy_tractability.tex` | `phase9_tractability:table:work2_coding_artifacts_work2_robust_menu_phase9_tractability_tables_exact_greedy_tractability_tex` | C6 exact-greedy computational credibility | Results or Appendix | diagnostic/provisional | Report candidate counts, enumerated counts, build time, effective exact solver, and unavailable gap/overlap only |
| T9. Main RC exact-greedy status table | `work2_coding/artifacts/work2_robust_menu/tables/exact_greedy.tex` | `main_rc:table:work2_coding_artifacts_work2_robust_menu_tables_exact_greedy_tex` | C6 exact-greedy computational credibility | Appendix | diagnostic/provisional | Main RC table is blocked; no near-optimal or greedy-quality claim |
| T10. Provenance status table | `work2_coding/artifacts/work2_robust_menu/tables/provenance_status.tex` | `main_rc:table:work2_coding_artifacts_work2_robust_menu_tables_provenance_status_tex` | C7 provenance/status transparency | Experimental Design, Results, or Appendix | supported | Use for status transparency only; it does not resolve empirical blockers |
| T11. Case scaffold inventory | `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/ARTIFACT_TO_SECTION_MAP.json` | Phase 10 section map output, `case_scaffold_appendix` entries | C8 semi-real case validation | Appendix or Future Work | unsupported | Inventory scaffold-only files; no case result or validation language |

## Proposed Figures

| Manuscript item | Source artifact path | Phase 10 package entry | Supported claim | Section | Claim status | Use boundary |
| --- | --- | --- | --- | --- | --- | --- |
| F1. Phase 8 profit-service diagnostic tradeoff | `work2_coding/artifacts/work2_robust_menu/phase8_sensitivity/figures/profit_service_tradeoff.png` | `phase8_sensitivity:figure:work2_coding_artifacts_work2_robust_menu_phase8_sensitivity_figures_profit_service_tradeoff_png` | C5 ETA robustness boundary; C2/C4 diagnostic boundaries | Results or Appendix | diagnostic/provisional | Diagnostic sensitivity figure only; no claim-ready tradeoff improvement |
| F2. Phase 8 opt-out and acceptance by axis | `work2_coding/artifacts/work2_robust_menu/phase8_sensitivity/figures/optout_acceptance_by_axis.png` | `phase8_sensitivity:figure:work2_coding_artifacts_work2_robust_menu_phase8_sensitivity_figures_optout_acceptance_by_axis_png` | C5 ETA robustness boundary; C2/C4 diagnostic boundaries | Results or Appendix | diagnostic/provisional | Diagnostic service metric boundary only |
| F3. Phase 9 menu build time by candidate count | `work2_coding/artifacts/work2_robust_menu/phase9_tractability/figures/menu_build_time_by_candidate_count.png` | `phase9_tractability:figure:work2_coding_artifacts_work2_robust_menu_phase9_tractability_figures_menu_build_time_by_candidate_count_png` | C6 exact-greedy computational credibility | Results or Appendix | diagnostic/provisional | Build-time diagnostic only; no tractability or greedy-quality upgrade |
| F4. Phase 9 gap/overlap status panel | `work2_coding/artifacts/work2_robust_menu/phase9_tractability/figures/gap_overlap_by_candidate_count.png.status.json` | `phase9_tractability:figure_status:work2_coding_artifacts_work2_robust_menu_phase9_tractability_figures_gap_overlap_by_candidate_count_png_status_json` | C6 exact-greedy computational credibility | Appendix | diagnostic/provisional | Status panel only; gap/overlap evidence is unavailable or blocked |
| F5. Main RC profit-gap figure status | `work2_coding/artifacts/work2_robust_menu/figures/profit_gap.png.status.json` | `main_rc:figure_status:work2_coding_artifacts_work2_robust_menu_figures_profit_gap_png_status_json` | C1 central adaptive menu superiority | Appendix | unsupported | Include only as blocked status if needed; no positive performance figure |
| F6. Main RC acceptance/opt-out figure status | `work2_coding/artifacts/work2_robust_menu/figures/acceptance_optout.png.status.json` | `main_rc:figure_status:work2_coding_artifacts_work2_robust_menu_figures_acceptance_optout_png_status_json` | C1 central adaptive menu superiority; C5 ETA robustness boundary | Appendix | unsupported | Status artifact only; cannot be shown as empirical figure |
| F7. Main RC ETA pruning figure status | `work2_coding/artifacts/work2_robust_menu/figures/eta_pruning.png.status.json` | `main_rc:figure_status:work2_coding_artifacts_work2_robust_menu_figures_eta_pruning_png_status_json` | C5 ETA robustness boundary | Appendix | diagnostic/provisional | Status artifact only; no operational no-filter recommendation |
| F8. Main RC exact-greedy time figure status | `work2_coding/artifacts/work2_robust_menu/figures/exact_greedy_time.png.status.json` | `main_rc:figure_status:work2_coding_artifacts_work2_robust_menu_figures_exact_greedy_time_png_status_json` | C6 exact-greedy computational credibility | Appendix | diagnostic/provisional | Status artifact only; no greedy optimality language |
| F9. Main RC home-only share figure status | `work2_coding/artifacts/work2_robust_menu/figures/home_only_share.png.status.json` | `main_rc:figure_status:work2_coding_artifacts_work2_robust_menu_figures_home_only_share_png_status_json` | C1 central adaptive menu superiority | Appendix | unsupported | Status artifact only; do not infer service quality improvement |

## Deferred Or Rejected Visuals

| Item | Reason |
| --- | --- |
| Service-menu conceptual schematic as a new figure | Not present as a generated Phase 10 figure; may be drafted later only as non-evidence conceptual artwork with separate approval |
| Case-study map or network figure | No executed case-study result artifact exists in the Phase 10 package |
| Claim-ready main RC profit or acceptance figure | Main RC figure entries are status JSON or blocked/missing artifacts, not claim-ready PNG evidence |
| Exact-vs-greedy gap/overlap plot | Phase 9 status reports gap/overlap unavailable or blocked |

## Manuscript Placement Summary

| Manuscript section | Tables/Figures allowed now | Claim boundary |
| --- | --- | --- |
| Experimental Design | T1, T10 | Status/provenance only |
| Results | T2, T5, T6, T8, F1, F2, F3 | Diagnostic/provisional unless T2/T10 are used for C7 status |
| Discussion | T2, T10, T11 | Claim gates, blockers, and future-work framing |
| Appendix | Any listed item with its source path and claim status | Must preserve `claim_ready=false` labels except C7 status transparency |

## Non-Editing Rule

Tables and figures listed here must be consumed as generated or indexed Phase
10 artifacts. If a future manuscript needs a cleaner table, it must be
regenerated by the artifact pipeline from source rows and status metadata, not
hand-edited in the manuscript.
