# Phase 07: TR-E Manuscript Revision And Submission Package - Context

**Gathered:** 2026-06-18T11:26:51.0219815+08:00
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 7 rewrites the current conditional diagnostic TR-E manuscript into a
complete, coherent revised draft while preserving the evidence boundary locked
by Phases 4-6. The phase is a manuscript revision phase, not an evidence
regeneration phase.

The phase must create a new revised manuscript file rather than overwriting
the Phase 5 draft. It must strengthen the TR-E service-menu contribution,
mathematical model, solution method, diagnostic results framing, discussion,
conclusion, and appendix consistency.

Phase 7 must not run final replay, calibration, case-study execution,
checkpoint training, claim upgrades, artifact regeneration, or any hand edits
to generated rows, generated tables, generated figures, package status files,
claim guards, or artifact mirrors. Current `claim_ready=false` and
conditional diagnostic status remain the claim ceiling.

</domain>

<decisions>
## Implementation Decisions

### Manuscript Revision Scope
- **D-01:** Phase 7 performs a main-body rewrite rather than a narrow patch.
  The revised manuscript should read as a TR-E paper, not as an extension of
  the Phase 6 audit.
- **D-02:** Preserve `manuscript/TR_E_WORK2_MANUSCRIPT_DRAFT.md` as the
  Phase 5 source draft and create a new revised draft, expected at
  `manuscript/TR_E_WORK2_MANUSCRIPT_REVISED.md`.
- **D-03:** Revision order should prioritize paper narrative first:
  Abstract, Introduction, and Literature Review establish the TR-E
  service-menu contribution before Model, Method, Results, and Discussion are
  expanded.
- **D-04:** The completion standard is a complete revised manuscript from
  Abstract through Appendix. Key sections should be deeply rewritten; other
  sections should still be synchronized for terminology, claim status, and
  source-traceability consistency.

### Model And Method Rigor
- **D-05:** The Mathematical Model must be readable without planning
  artifacts. It should define sets, state, candidate bundles, displayed menu,
  MNL response probabilities, objective components, constraints, outside
  option, accepted home pickup, accepted meeting-point pickup, and opt-out
  accounting.
- **D-06:** Present MNL as a service-menu response model over the displayed
  bundle set plus the outside option. The text must state that this is an
  experimental response component and not real-passenger behavioral
  validation.
- **D-07:** The Solution Method should include concise core pseudocode for the
  diagnostic service-menu evaluation pipeline: state input, candidate bundle
  generation, ETA/window feasibility, pricing, menu selection, replay logging,
  and claim-gate reporting.
- **D-08:** Exact/greedy computational material belongs in a diagnostic
  appendix plus a short main-text boundary statement. Do not claim near-optimality,
  exact-greedy computational credibility, or algorithmic superiority.

### Evidence Narrative
- **D-09:** Results should open with strict claim-gate status and current
  `claim_ready=false`, then explain diagnostic insights within that boundary.
  Avoid turning Results into a raw package-status dump.
- **D-10:** Blocked claims C1, C2, C3, C4, C6, and C8 should appear as result
  boundaries and future evidence-upgrade conditions, not as buried appendix
  items or positive claims.
- **D-11:** C5/no-filter material should be framed only as an ETA robustness
  diagnostic boundary. It must not be presented as an operational
  recommendation or robustness superiority result.
- **D-12:** Discussion tone should be firm but not inflated: the paper can
  confidently claim formulation, paired diagnostic replay, and claim-boundary
  transparency, but not adaptive-menu empirical superiority.

### Deliverables And Verification
- **D-13:** Phase 7 deliverables are intentionally lean: complete revised
  manuscript, revised prohibited-language scan, and brief revision summary.
  Do not expand this phase into another full readiness audit package.
- **D-14:** Update `manuscript/TR_E_WORK2_TABLE_FIGURE_SOURCE_MAP.md` only if
  the revised manuscript adds, removes, renames, renumbers, or materially
  changes tables, figures, captions, or appendix evidence objects.
- **D-15:** Phase 7 must not modify generated artifacts, generated rows,
  package status files, claim guards, or artifact mirrors.
- **D-16:** Verification should use manuscript-focused checks plus baseline
  contract tests: import smoke, manuscript claim guard test, manuscript
  readiness package test, and prohibited-language scan. If the source map is
  updated, also verify source-map columns and concrete source paths.

### the agent's Discretion
The planner and executor may choose the exact manuscript section ordering,
paragraph-level rewrite strategy, pseudocode formatting, and revision-summary
layout, as long as the decisions above and the claim ceiling are honored.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project And Phase State
- `.planning/PROJECT.md` - project scope, active runtime root, current claim
  ceiling, and regenerated planning decisions.
- `.planning/REQUIREMENTS.md` - manuscript requirements, submission-readiness
  requirements, and out-of-scope boundaries.
- `.planning/ROADMAP.md` - Phase 7 goal, deliverables, success criteria, and
  verification commands.
- `.planning/STATE.md` - current workflow state and evidence-boundary notes.
- `.planning/research/SUMMARY.md` - evidence facts, strict claim status, and
  conditional diagnostic framing.

### Prior Phase Handoff
- `.planning/phases/06-final-tr-e-submission-readiness-audit/06-CONTEXT.md`
  - Phase 6 audit stance, reviewer-risk taxonomy, verification threshold, and
  author-facing revision-list requirements.
- `.planning/milestones/tr_e_completion/M6_FINAL_TR_E_READINESS_AUDIT.md`
  - final readiness verdict, TR-E risk matrix, reviewer attack points, and
  required revision path.
- `manuscript/TR_E_WORK2_FINAL_REVISION_TASKS.md` - concrete major/minor
  revision tasks and section-by-section implementation map.
- `.planning/milestones/tr_e_completion/M4A_FINAL_REPLAY_REPORT.md` - final
  replay was not run and no regenerated final package exists.
- `.planning/milestones/tr_e_completion/M4B_DIAGNOSTIC_MANUSCRIPT_LOCK.md`
  - diagnostic manuscript lock and claim-path boundary.
- `.planning/milestones/tr_e_completion/M4B_SAFE_CLAIM_TABLE.md` - claim IDs,
  source status, allowed use, blockers, and prohibited language.
- `.planning/milestones/tr_e_completion/M4B_REVIEWER_RISK_RESPONSE_PLAN.md`
  - reviewer-facing risk framing to integrate into manuscript prose.

### Manuscript Inputs
- `manuscript/TR_E_WORK2_MANUSCRIPT_DRAFT.md` - Phase 5 source draft to revise
  from, not overwrite.
- `manuscript/TR_E_WORK2_CLAIM_AUDIT.md` - claim-by-claim support boundary.
- `manuscript/TR_E_WORK2_TABLE_FIGURE_SOURCE_MAP.md` - table/figure source
  path, claim status, allowed use, and evidence class.
- `manuscript/TR_E_WORK2_PROHIBITED_LANGUAGE_CHECK.md` - Phase 5 prohibited
  language scan and allowed hits.
- `manuscript/TR_E_WORK2_RESPONSE_TO_INTERNAL_REVIEW.md` - Phase 5 internal
  review response and risk notes.

### Paper Design And Claim Controls
- `.planning/paper/TR_E_RESEARCH_DESIGN.md` - research question, service
  product definition, policy family, and evidence-tier definitions.
- `.planning/paper/TR_E_MANUSCRIPT_STRUCTURE.md` - required section structure
  and section-level claim responsibilities.
- `.planning/paper/CLAIM_SAFE_LANGUAGE.md` - allowed and forbidden claim-safe
  language by strict claim ID.
- `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md` - source-map rules for tables,
  figures, evidence class, and allowed manuscript use.

### Generated Claim Authority
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`
  - canonical strict claim guard; current `claim_ready=false`.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`
  - canonical package status and blocker counts.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_INDEX.json`
  - package index and missing entries.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/ARTIFACT_TO_SECTION_MAP.json`
  - artifact-to-section mapping for paper integration.

### Codebase And Test Context
- `.planning/codebase/STRUCTURE.md` - active runtime root, manuscript
  directory, planning-paper docs, and generated artifact boundaries.
- `.planning/codebase/ARCHITECTURE.md` - manifest, replay, artifact, and
  claim-guard architecture.
- `.planning/codebase/TESTING.md` - script-style test commands and manuscript
  claim/readiness checks.
- `work2_coding/scripts/test_manuscript_claim_guard.py` - existing claim guard
  validation test.
- `work2_coding/scripts/test_manuscript_readiness_package.py` - manuscript
  package readiness test from Phase 6.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `manuscript/TR_E_WORK2_MANUSCRIPT_DRAFT.md`: source draft for the revised
  manuscript.
- `manuscript/TR_E_WORK2_FINAL_REVISION_TASKS.md`: Phase 6 revision backlog
  that should drive the rewrite.
- `manuscript/TR_E_WORK2_CLAIM_AUDIT.md`: claim boundary reference for C1-C8.
- `manuscript/TR_E_WORK2_TABLE_FIGURE_SOURCE_MAP.md`: evidence object map to
  preserve or update only when object identities change.
- `work2_coding/scripts/test_manuscript_claim_guard.py` and
  `work2_coding/scripts/test_manuscript_readiness_package.py`: manuscript
  verification scripts to run after revision.

### Established Patterns
- Active runtime commands run from `work2_coding/`; do not target stale
  `ooh_code/` paths.
- Script-style tests are invoked directly with `python scripts/test_*.py`.
- Manuscript claims must align with strict claim guard output and the
  table/figure source map.
- Generated rows, artifacts, package status files, and claim guards are
  evidence outputs, not editable manuscript inputs.
- No-filter, Phase 8, Phase 9, exact/greedy, and case-study materials remain
  diagnostic/provisional unless a future evidence-regeneration milestone
  changes the guard.

### Integration Points
- Create `manuscript/TR_E_WORK2_MANUSCRIPT_REVISED.md`.
- Create `manuscript/TR_E_WORK2_REVISION_SUMMARY.md`.
- Create `manuscript/TR_E_WORK2_REVISED_PROHIBITED_LANGUAGE_CHECK.md`.
- Update `manuscript/TR_E_WORK2_TABLE_FIGURE_SOURCE_MAP.md` only if revised
  manuscript evidence objects change.
- Record verification outcomes in the Phase 7 summary or verification
  artifact during execution.

</code_context>

<specifics>
## Specific Ideas

- The user selected all four Phase 7 gray areas for discussion: revision
  scope, model rigor, evidence narrative, and deliverables.
- The user selected main-body rewrite, new revised draft, narrative-first
  revision order, and complete revised-manuscript completion standard.
- The user selected reviewer-readable model rigor, MNL as service-menu
  response model, core pseudocode, and diagnostic appendix handling for
  exact/greedy material.
- The user selected claim-gate-first Results framing, blocked claims as
  result boundaries/future conditions, C5 as ETA robustness diagnostic only,
  and firm but not inflated Discussion tone.
- The user selected lean deliverables, source-map update only when evidence
  objects change, no generated-artifact edits, and manuscript-focused
  verification plus baseline checks.

</specifics>

<deferred>
## Deferred Ideas

None. Discussion stayed within Phase 7 scope.

</deferred>

---

*Phase: 07-TR-E Manuscript Revision And Submission Package*
*Context gathered: 2026-06-18T11:26:51.0219815+08:00*
