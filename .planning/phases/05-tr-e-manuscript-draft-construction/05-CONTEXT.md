# Phase 5: TR-E Manuscript Draft Construction - Context

**Gathered:** 2026-06-17T18:40:41.0938801+08:00
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 5 builds a full claim-safe Transportation Research Part E manuscript
draft aligned with the Phase 4 conditional diagnostic path. The phase should
produce paper-facing manuscript deliverables under `manuscript/`, centered on a
new Markdown draft:

- `manuscript/TR_E_WORK2_MANUSCRIPT_DRAFT.md`
- `manuscript/TR_E_WORK2_RESPONSE_TO_INTERNAL_REVIEW.md`
- `manuscript/TR_E_WORK2_CLAIM_AUDIT.md`
- `manuscript/TR_E_WORK2_TABLE_FIGURE_SOURCE_MAP.md`
- `manuscript/TR_E_WORK2_PROHIBITED_LANGUAGE_CHECK.md`

This is a writing and claim-control phase. It must not run final replay,
calibration, checkpoint training, case-study execution, artifact builders for
claim upgrades, or any hand edits to generated rows, figures, tables,
package-status files, mirrors, or claim guards. The current strict claim guard
has `claim_ready=false`, and Phase 5 must treat that as the manuscript claim
ceiling.

</domain>

<decisions>
## Implementation Decisions

### Manuscript Carrier And Legacy Draft Handling
- **D-01:** The primary Phase 5 manuscript draft should be
  `manuscript/TR_E_WORK2_MANUSCRIPT_DRAFT.md`. Existing
  `manuscript/main.tex` is legacy/reference material, not the main writing
  surface for this phase.
- **D-02:** `manuscript/main.tex` may be used as a migration source, but
  migrated content must be rewritten. Do not carry forward old TR-C framing,
  `DSPO_PLUS` foregrounding, ranking-validation promises, or dominance
  language.
- **D-03:** Migrate only the safer reusable material first: notation,
  mathematical model skeleton, MNL and menu-objective content, literature
  references, bibliography material, and Elsevier metadata. Rewrite the
  abstract, introduction, results, discussion, and conclusion around the
  conditional diagnostic TR-E path.
- **D-04:** Write a separate
  `manuscript/TR_E_WORK2_RESPONSE_TO_INTERNAL_REVIEW.md` that records migrated
  items, removed items, prohibited-language risks, and how each risk was
  resolved.

### Introduction Narrative
- **D-05:** The abstract and introduction should lead with dynamic
  service-menu optimization for many-to-one DRT, where each displayed service
  option bundles meeting point, pickup time window, and price.
- **D-06:** The claim-gated pipeline should be presented as an evidence
  constraint and transparency mechanism, not as the only subject of the paper.
- **D-07:** The contribution list should have three parts:
  formulation, diagnostic evaluation, and claim-gated traceability.
- **D-08:** The abstract and introduction should explicitly identify the
  manuscript path as conditional diagnostic and state that positive empirical
  claims remain blocked by readiness and claim gates.
- **D-09:** Title and keywords should use TR-E-safe language such as
  service-menu optimization, many-to-one DRT, time windows, and claim-gated
  evidence. Do not foreground `Behavior-Aware`, `DSPO_PLUS`, or a DSPO/DSPO+
  ranking narrative.

### Results And Appendix Evidence Placement
- **D-10:** The Results section should open with a claim-gate/status table
  based on `PACKAGE_STATUS.json`, `CLAIM_GUARD.json`, blockers, claim IDs,
  claim statuses, and allowed manuscript use.
- **D-11:** Phase 8 ETA/no-filter material should appear as a short main-text
  diagnostic boundary subsection for `C5_eta_robustness_boundary`, with full
  Phase 8 tables and figures in the Appendix. No-filter must not be written as
  an operational recommendation.
- **D-12:** Phase 9 exact/greedy tractability material should be Appendix-first
  and only briefly referenced in Discussion as a future claim-ready
  computational-evidence need. Do not present it as computational credibility,
  greedy optimality, or near-optimality evidence.
- **D-13:** Case-study scaffold material should appear only in Appendix or
  future-work discussion. It must be labeled `C8` scaffold-only and must not be
  described as real passenger behavior, semi-real validation, or case-study
  validation.
- **D-14:** Every table or figure introduced in Phase 5 must have source
  artifact path, claim ID, claim status, allowed manuscript use, and evidence
  class: generated evidence, diagnostic evidence, blocked status,
  scaffold-only material, or conceptual illustration.

### Mathematical Model And Method Depth
- **D-15:** The main Mathematical Model section should include the complete
  core model: sets and indices, service bundle `b=(m,w,p)`, menu decision
  variable, menu-size limit, MNL choice with outside option, expected menu
  objective, feasibility constraints, and service guardrails. Longer
  derivations or detail tables may move to the Appendix.
- **D-16:** The Solution Method should describe exact enumeration and greedy
  fallback as an algorithmic menu-construction contract. It must also state
  that `C6_exact_greedy_computational_credibility` remains blocked diagnostic
  and does not support near-optimality or computational-credibility claims.
- **D-17:** The Method section should focus on service-menu algorithms:
  candidate bundle generation, menu construction, adaptive versus fixed window
  handling, Lambert-W price generation, and feasibility/guardrail filtering.
- **D-18:** Experimental Design should carry the reproducibility and claim-gate
  machinery: paired replay, checkpoint provenance, artifact status, strict
  claim guard, source-family status, and allowed-use interpretation.
- **D-19:** Lambert-W pricing should remain in the manuscript as a bundle price
  generation component. Do not frame the paper as a pricing-only paper or make
  pricing the sole contribution.

### The Agent's Discretion
None. The user selected explicit decisions for every discussed gray area. The
planner may choose exact paragraph wording, table captions, and section-level
ordering only within the locked claim and evidence boundaries above.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project And Roadmap
- `.planning/PROJECT.md` - project scope, runtime root, Phase 4 diagnostic
  path lock, claim ceiling, and manuscript-language constraints.
- `.planning/REQUIREMENTS.md` - Phase 5 requirements `MS-01` through `MS-05`
  and out-of-scope claim boundaries.
- `.planning/ROADMAP.md` - Phase 5 goal, deliverables, and success criteria.
- `.planning/STATE.md` - current workflow state and Phase 5 handoff.
- `.planning/research/SUMMARY.md` - regenerated research summary, current
  evidence facts, strict claim status, and safe framing.

### Prior Phase Handoff
- `.planning/phases/02-gate-cleanup-plan-without-destructive-changes/02-CONTEXT.md`
  - checkpoint provenance and non-destructive evidence boundary decisions.
- `.planning/phases/03-claim-ready-evidence-decision-gate/03-CONTEXT.md` -
  final replay legitimacy threshold, claim-by-claim classification, and
  failure rules.
- `.planning/phases/04-execute-selected-claim-path/04-CONTEXT.md` - Path B
  lock, diagnostic manuscript strength, prohibited/allowed language handoff,
  and Phase 5 claim traceability requirements.
- `.planning/milestones/tr_e_completion/M4A_PRE_REPLAY_GATE_REPORT.md` -
  controlling report for the blocked pre-replay gate pass.
- `.planning/milestones/tr_e_completion/M4A_FINAL_REPLAY_REPORT.md` -
  final replay status; final replay was not run.
- `.planning/milestones/tr_e_completion/M4B_DIAGNOSTIC_MANUSCRIPT_LOCK.md` -
  formal lock that Phase 5 must draft a conditional diagnostic TR-E manuscript.
- `.planning/milestones/tr_e_completion/M4B_SAFE_CLAIM_TABLE.md` - claim ID,
  source artifact, status, allowed-use, blocker, and prohibited-language table.
- `.planning/milestones/tr_e_completion/M4B_REVIEWER_RISK_RESPONSE_PLAN.md` -
  reviewer-risk framing and section-level guidance.

### Paper Design And Claim Controls
- `.planning/paper/CLAIM_SAFE_LANGUAGE.md` - allowed and forbidden language by
  strict claim ID.
- `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md` - table/figure source path,
  claim ID, claim status, and allowed-use requirements.
- `.planning/paper/TR_E_MANUSCRIPT_STRUCTURE.md` - required TR-E section
  structure and claim-safe section responsibilities.
- `.planning/paper/TR_E_RESEARCH_DESIGN.md` - research question, service
  product definition, primary policy family, and evidence-tier definitions.
- `manuscript/main.tex` - legacy draft and migration source. Use only after
  rewriting unsafe TR-C, `DSPO_PLUS`, ranking, and dominance language.
- `manuscript/references.bib` - bibliography source for migrated literature
  references.

### Generated Artifact Package And Claim Authority
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`
  - canonical strict claim guard; current `claim_ready=false`.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`
  - canonical package status and blocker summary.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_INDEX.json`
  - package artifact index and missing-entry source paths.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/ARTIFACT_TO_SECTION_MAP.json`
  - section-to-artifact mapping used for manuscript source traceability.
- `artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json` -
  paper-facing mirror; cite only with awareness that `work2_coding/` remains
  the canonical source.
- `artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json` -
  paper-facing mirror package status.

### Codebase Maps And Runtime Surfaces
- `.planning/codebase/CONVENTIONS.md` - manuscript, claim-guard, generated
  artifact, opt-out, no-filter, and attention-scope conventions.
- `.planning/codebase/STRUCTURE.md` - active `work2_coding/` layout,
  manuscript directory, `.planning/paper/` docs, and generated artifact
  boundaries.
- `.planning/codebase/ARCHITECTURE.md` - manifest-driven execution, artifact
  gate, strict claim guard, and generated output architecture.
- `.planning/codebase/CONCERNS.md` - claim boundary risks, manuscript
  language risks, formal readiness blockers, and artifact mirror drift.
- `.planning/codebase/INTEGRATIONS.md` - file/artifact interfaces, LaTeX
  source, package outputs, and manuscript-frame builder interface.
- `.planning/codebase/STACK.md` - active runtime root, manuscript tooling,
  and common script commands.
- `.planning/codebase/TESTING.md` - script-style checks, including
  `test_manuscript_claim_guard.py`.
- `work2_coding/scripts/build_manuscript_frame.py` - existing script wrapper
  for generated manuscript frames and claim guard material.
- `work2_coding/scripts/test_manuscript_claim_guard.py` - claim-guard
  validation test relevant to prohibited-language and manuscript boundaries.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `manuscript/main.tex`: legacy Elsevier CAS LaTeX manuscript with reusable
  notation, MNL/menu-objective material, references, and metadata. It also
  contains unsafe old framing that must be rewritten.
- `manuscript/references.bib`: bibliography source for the new Markdown draft.
- `.planning/paper/TR_E_MANUSCRIPT_STRUCTURE.md`: section scaffold for
  Introduction, Literature Review, Problem Description, Mathematical Model,
  Solution Method, Experimental Design, Results, Discussion, Conclusion, and
  Appendix.
- `.planning/paper/CLAIM_SAFE_LANGUAGE.md` and
  `.planning/milestones/tr_e_completion/M4B_SAFE_CLAIM_TABLE.md`: direct
  source material for `TR_E_WORK2_CLAIM_AUDIT.md` and
  `TR_E_WORK2_PROHIBITED_LANGUAGE_CHECK.md`.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/`: source
  package for claim status, package status, and section-source mapping.
- `work2_coding/scripts/build_manuscript_frame.py`: existing generated
  manuscript-frame script, useful as context but not a substitute for the new
  full TR-E draft.

### Established Patterns
- Active runtime root is `work2_coding/`; manuscript work should not revive or
  cite stale `ooh_code/` paths.
- Generated rows, package status, package indexes, figures, tables, mirrors,
  and claim guards are evidence outputs. Do not hand-edit them to improve
  manuscript claims.
- Strict `CLAIM_GUARD.json` controls all manuscript claim upgrades. Current
  positive empirical claims remain blocked.
- Opt-out must stay separate from accepted home pickup and accepted
  meeting-point pickup in model text, metrics, tables, and claim audit.
- No-filter evidence is diagnostic only. Attention-based choice/scoring is out
  of v1 scope and should not become manuscript framing.
- Root `artifacts/` is a mirror or paper-facing copy; `work2_coding/artifacts/`
  is the canonical generated source unless a phase explicitly records mirror
  drift checks.

### Integration Points
- Create the new manuscript draft and companion audit files in `manuscript/`.
- Use `.planning/paper/` docs and Phase 4 M4B deliverables as planning inputs,
  not as generated evidence to modify.
- Use `CLAIM_GUARD.json`, `PACKAGE_STATUS.json`, `PACKAGE_INDEX.json`, and
  `ARTIFACT_TO_SECTION_MAP.json` to build the table/figure source map and
  prohibited-language check.
- Verification should at minimum run the import smoke from `work2_coding/`.
  If Phase 5 changes claim-check scripts or generated manuscript-frame logic,
  include `python scripts/test_manuscript_claim_guard.py` from
  `work2_coding/`.

</code_context>

<specifics>
## Specific Ideas

- The user selected all four Phase 5 gray areas for discussion.
- The user consistently selected the recommended, claim-safer option in every
  Phase 5 decision.
- The new draft should read first as a TR-E transportation operations and
  service-menu optimization manuscript, not as a post-hoc apology for blocked
  evidence.
- The diagnostic status should be explicit early, especially in abstract and
  introduction, so the manuscript does not create a positive empirical promise
  and then retract it in Results.
- The old LaTeX manuscript is useful, but only as raw material. Its old TR-C,
  `Behavior-Aware`, `DSPO_PLUS`, dominance, and ranking-validation language is
  not a safe Phase 5 frame.

</specifics>

<deferred>
## Deferred Ideas

None. Discussion stayed within Phase 5 scope.

</deferred>

---

*Phase: 5-TR-E Manuscript Draft Construction*
*Context gathered: 2026-06-17T18:40:41.0938801+08:00*
