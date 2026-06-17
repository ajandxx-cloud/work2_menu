---
phase: 05
slug: tr-e-manuscript-draft-construction
status: complete
created: 2026-06-17
research_mode: inline
sources: local-planning-and-artifact-state
---

# Phase 05 Research - TR-E Manuscript Draft Construction

## Research Question

What does Phase 5 need to know to plan a full TR-E manuscript draft without
overstating the current Work2 evidence?

## Research Basis

This research used local project and artifact state only. No internet research,
final replay, artifact regeneration, generated-row editing, claim-guard editing,
or manuscript claim upgrade was performed.

Primary inputs:

- `.planning/PROJECT.md`
- `.planning/REQUIREMENTS.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `.planning/research/SUMMARY.md`
- `.planning/phases/05-tr-e-manuscript-draft-construction/05-CONTEXT.md`
- `.planning/milestones/tr_e_completion/M4A_PRE_REPLAY_GATE_REPORT.md`
- `.planning/milestones/tr_e_completion/M4A_FINAL_REPLAY_REPORT.md`
- `.planning/milestones/tr_e_completion/M4B_DIAGNOSTIC_MANUSCRIPT_LOCK.md`
- `.planning/milestones/tr_e_completion/M4B_SAFE_CLAIM_TABLE.md`
- `.planning/milestones/tr_e_completion/M4B_REVIEWER_RISK_RESPONSE_PLAN.md`
- `.planning/paper/CLAIM_SAFE_LANGUAGE.md`
- `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md`
- `.planning/paper/TR_E_MANUSCRIPT_STRUCTURE.md`
- `.planning/paper/TR_E_RESEARCH_DESIGN.md`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/ARTIFACT_TO_SECTION_MAP.json`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/claim_checklist.md`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/safe_language_boundaries.md`
- `manuscript/main.tex`
- `manuscript/references.bib`
- `work2_coding/scripts/build_manuscript_frame.py`
- `work2_coding/scripts/test_manuscript_claim_guard.py`
- `work2_coding/Src/manuscript_claims.py`

## Evidence State To Preserve

Phase 4 locked the paper to a conditional diagnostic manuscript path. The one
authorized pre-replay gate for `final_robust_menu` remained blocked by dirty
git provenance and missing formal checkpoint evidence, so final replay was not
run.

The current Phase 10 package reports:

| Field | Value |
| --- | --- |
| Package schema | `phase10-paper-artifact-package-v1` |
| Strict claim schema | `phase10-strict-claim-guard-v1` |
| Package `claim_ready` | `false` |
| Strict claim guard `claim_ready` | `false` |
| Manuscript positive claims allowed | `false` |
| Artifact count | 74 |
| Existing artifact count | 70 |
| Missing artifact count | 4 |
| Blocker count | 108 |

Source-family status:

| Source family | Status | Artifacts | Claim ready |
| --- | --- | ---: | --- |
| `main_rc` | `blocked` | 30 | false |
| `phase8_sensitivity` | `diagnostic_provisional_blocked` | 14 | false |
| `phase9_tractability` | `diagnostic_provisional_blocked` | 12 | false |
| `case_scaffold` | `scaffold_only_no_result_evidence` | 12 | false |
| `blocker_status` | `blocked` | 6 | false |

Strict claim status:

| Claim ID | Support status | Claim ready | Manuscript allowed |
| --- | --- | --- | --- |
| `C1_central_adaptive_menu_superiority` | `unsupported_blocked` | false | false |
| `C2_product_ablation_value` | `conditional_diagnostic_blocked` | false | false |
| `C3_adaptive_window_increment` | `unsupported` | false | false |
| `C4_menu_construction_value` | `conditional_diagnostic_blocked` | false | false |
| `C5_eta_robustness_boundary` | `diagnostic_only` | false | true |
| `C6_exact_greedy_computational_credibility` | `blocked_diagnostic` | false | false |
| `C7_provenance_status_transparency` | `status_supported` | true | true |
| `C8_semi_real_case_validation` | `scaffold_only_blocked` | false | false |

Planning implication: Phase 5 may use C7 as status/provenance transparency and
C5 as diagnostic boundary material. Every other positive empirical claim is
blocked unless a future regenerated strict guard authorizes that exact claim.

## Manuscript Strategy

The primary Phase 5 draft should be Markdown:

- `manuscript/TR_E_WORK2_MANUSCRIPT_DRAFT.md`

Markdown is the safer phase target because it allows claim labels, source-path
footnotes, and audit checklists to be built directly around the current
evidence boundary. The legacy `manuscript/main.tex` remains useful as source
material, but not as the main writing surface.

Required companion deliverables:

- `manuscript/TR_E_WORK2_RESPONSE_TO_INTERNAL_REVIEW.md`
- `manuscript/TR_E_WORK2_CLAIM_AUDIT.md`
- `manuscript/TR_E_WORK2_TABLE_FIGURE_SOURCE_MAP.md`
- `manuscript/TR_E_WORK2_PROHIBITED_LANGUAGE_CHECK.md`

The draft should read first as a TR-E transportation operations paper about
dynamic service-menu optimization for many-to-one DRT. It should not read as an
attention model paper, pricing-only paper, pure algorithm ranking paper, or a
post-hoc apology for blocked evidence.

## Legacy Draft Migration Findings

`manuscript/main.tex` contains reusable material:

- Elsevier manuscript metadata and bibliography wiring.
- MNL service-menu model skeleton.
- Basic service bundle notation.
- Literature references and bibliography source.
- Method material for menu construction, time windows, and pricing.

It also contains unsafe or outdated material that must be rewritten:

- Title and short title foreground "Behavior-Aware".
- The abstract identifies the paper as a TR-C draft.
- The text uses `DSPO_PLUS`/DSPO family ranking language that is outside the
  locked Phase 5 framing.
- The results section still describes planned ranking validation rather than
  the Phase 4 diagnostic lock.
- Several phrases contain improvement, dominance, validation, or ranking
  language that would exceed the current strict claim guard.

Migration rule: use `main.tex` only as a raw source. Reuse notation and
literature references after rewriting; do not copy unsafe framing into the new
Markdown draft.

## Required Manuscript Structure

The draft must include academic paragraph prose for:

1. Introduction
2. Literature Review
3. Problem Description
4. Mathematical Model
5. Solution Method
6. Experimental Design
7. Results
8. Discussion
9. Conclusion
10. Appendix

Suggested section duties:

- Introduction: motivate many-to-one DRT, displayed service menus, service
  bundles `(meeting point, pickup time window, price)`, and claim-gated
  diagnostic contribution.
- Literature Review: cover DRT, meeting points, time windows, passenger choice,
  assortment/service menus, pricing, and reproducible computational evidence.
- Problem Description: define sequential requests, fleet state, candidate
  meeting points, pickup windows, prices, home service, outside option, and
  separate opt-out accounting.
- Mathematical Model: include sets, bundle `b=(m,w,p)`, menu variables,
  menu-size limit, MNL with outside option, expected objective, feasibility and
  service guardrails.
- Solution Method: describe candidate generation, menu construction, adaptive
  versus fixed windows, Lambert-W pricing, exact enumeration, greedy fallback,
  and blocked computational-credibility status.
- Experimental Design: explain paired replay, seven mainline policies,
  checkpoint provenance, evidence tiers, artifact status, and strict claim
  guard interpretation.
- Results: lead with claim-gate/package status, then use only diagnostic or
  status-supported material.
- Discussion: convert blocked claims into limitations, reviewer-risk responses,
  and future evidence requirements.
- Conclusion: summarize formulation, diagnostic evidence, and reproducibility
  boundary without empirical superiority language.
- Appendix: include source maps, diagnostic sensitivity, tractability
  diagnostics, scaffold-only case material, and prohibited-language check.

## Table And Figure Source Requirements

Every table or figure introduced in Phase 5 must have:

1. Source artifact path.
2. Claim ID.
3. Claim status.
4. Allowed manuscript use.
5. Evidence class: generated evidence, diagnostic evidence, blocked status,
   scaffold-only material, or conceptual illustration.

Conceptual figures may be included only if they are labeled conceptual and do
not support empirical claims.

Recommended manuscript objects:

| Object | Evidence class | Claim ID | Required source |
| --- | --- | --- | --- |
| Claim gate status table | blocked/status | C1-C8 | `CLAIM_GUARD.json`, `PACKAGE_STATUS.json` |
| Source-family status table | blocked/status | C7 | `PACKAGE_STATUS.json` |
| Service-menu notation figure/table | conceptual | none or C7 | manuscript-created conceptual material |
| ETA/no-filter diagnostic boundary table | diagnostic | C5 | Phase 8 package sources and claim map |
| Exact/greedy appendix table | diagnostic | C6 | Phase 9 package sources and claim map |
| Case scaffold appendix table | scaffold-only | C8 | `.planning/data/case_studies/` |

## Prohibited Language Boundary

The final prohibited-language check must scan at least these terms and phrases:

- `dominate`, `dominates`, `dominance`
- `superior`, `superiority`
- `outperform`, `outperforms`, `outperformed`
- `improve`, `improves`, `improvement`, `advantage`
- `prove`, `proves`, `validated`, `validation`
- `near-optimal`, `optimal greedy`, `greedy optimality`
- `real passenger`, `real passenger behavior`
- `case-study validation`, `semi-real validation`
- `no-filter recommendation`, `operationally recommended`
- `DSPO_PLUS`, `Behavior-Aware`, `TR-C`, `ranking validation`

Not every occurrence is automatically invalid because some companion audit
files must list forbidden phrases. The manuscript body should avoid prohibited
positive wording or quote it only inside an explicitly marked prohibited
language table.

## Verification Architecture

Phase 5 is writing-focused, but it still needs automated and source-level
validation:

- Smoke import from `work2_coding/`:
  `python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"`
- Manuscript claim guard contract:
  `python scripts/test_manuscript_claim_guard.py`
- File-existence checks for all five manuscript deliverables.
- Source assertions that the manuscript draft contains every required TR-E
  section.
- Source assertions that `TR_E_WORK2_TABLE_FIGURE_SOURCE_MAP.md` contains
  source path, claim ID, claim status, allowed use, and evidence class columns.
- Source assertions that `TR_E_WORK2_CLAIM_AUDIT.md` covers strict claim IDs
  C1 through C8.
- Source assertions that `TR_E_WORK2_PROHIBITED_LANGUAGE_CHECK.md` records
  each prohibited term class and marks body occurrences as pass/fail.
- A final body scan that flags prohibited positive language in
  `TR_E_WORK2_MANUSCRIPT_DRAFT.md`.

Manual review is still needed for academic prose quality, novelty framing, and
TR-E reviewer risk, but the plan should not allow the phase to pass without the
source-map and claim-language artifacts.

## Planning Implications

The safest execution split is:

1. Build evidence controls first: source map, claim audit, prohibited-language
   checklist, and internal-review response shell.
2. Draft the manuscript body from those controls and the legacy/source inputs.
3. Run final claim-language, section-coverage, and source-traceability checks.

This split prevents the writer from composing prose first and discovering only
afterward that tables, figures, or results paragraphs exceed the strict claim
guard.

## RESEARCH COMPLETE

