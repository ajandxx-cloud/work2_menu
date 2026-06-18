# Phase 07: TR-E Manuscript Revision And Submission Package - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md; this log preserves the alternatives considered.

**Date:** 2026-06-18T11:26:51.0219815+08:00
**Phase:** 07-TR-E Manuscript Revision And Submission Package
**Areas discussed:** Manuscript revision scope, Model and method rigor, Evidence narrative, Phase deliverables

---

## Manuscript Revision Scope

| Option | Description | Selected |
|--------|-------------|----------|
| Main-body rewrite | Rewrite Abstract, Introduction, Literature Review, Model, Results, and Discussion so the draft reads as a TR-E manuscript rather than an audit memo. | Yes |
| Targeted patch | Keep the existing structure and patch Phase 6 weak spots only. | |
| Submission-package cleanup | Prioritize source maps, appendix labels, claim audit, and checklist over main prose. | |

**User's choice:** Main-body rewrite.
**Notes:** The revised manuscript should be a full paper-quality draft, not only a checklist response.

| Option | Description | Selected |
|--------|-------------|----------|
| New revised draft | Preserve the Phase 5 draft and create `manuscript/TR_E_WORK2_MANUSCRIPT_REVISED.md`. | Yes |
| Overwrite original draft | Edit `TR_E_WORK2_MANUSCRIPT_DRAFT.md` directly. | |
| Revision plan first | Produce a revision blueprint before changing the manuscript. | |

**User's choice:** New revised draft.
**Notes:** This keeps Phase 5 provenance clear.

| Option | Description | Selected |
|--------|-------------|----------|
| Narrative first | Fix Abstract, Introduction, and Literature Review before technical sections. | Yes |
| Model rigor first | Expand notation and technical content before paper narrative. | |
| Paper order | Revise from Abstract through Appendix sequentially. | |

**User's choice:** Narrative first.
**Notes:** This directly addresses Phase 6's concern that the paper still reads partly like an evidence-boundary memo.

| Option | Description | Selected |
|--------|-------------|----------|
| Complete revised manuscript | Produce a coherent full manuscript from Abstract through Appendix. | Yes |
| Key sections only | Deeply revise only major sections and lightly patch the rest. | |
| Revised manuscript plus change log | Produce the full draft plus detailed change log. | |

**User's choice:** Complete revised manuscript.
**Notes:** A brief revision summary is still planned, but the main completion standard is the revised manuscript itself.

---

## Model And Method Rigor

| Option | Description | Selected |
|--------|-------------|----------|
| Reviewer-readable model | Define sets, state, bundles, menu, MNL probabilities, objective, constraints, outside option, home pickup, meeting-point pickup, and opt-out. | Yes |
| Conceptual model | Use formulas and prose but avoid full constraint detail. | |
| Appendix-heavy model | Keep main text light and push complete notation to appendix. | |

**User's choice:** Reviewer-readable model.
**Notes:** Model rigor was a Phase 6 major risk, so the revised draft should stand without planning files.

| Option | Description | Selected |
|--------|-------------|----------|
| MNL as service-menu response model | Present MNL over displayed bundles and outside option while denying real-passenger validation. | Yes |
| MNL as simulation mechanism only | Keep behavior model discussion minimal. | |
| Emphasize optimization contract | De-emphasize probabilities and focus on replay/menu construction. | |

**User's choice:** MNL as service-menu response model.
**Notes:** The paper should connect choice probabilities to the displayed service menu but avoid external validation claims.

| Option | Description | Selected |
|--------|-------------|----------|
| Core pseudocode | Include concise diagnostic service-menu evaluation pseudocode. | Yes |
| Text process only | Explain method in prose without an algorithm box. | |
| Appendix pseudocode | Keep main text light and put pseudocode in appendix. | |

**User's choice:** Core pseudocode.
**Notes:** Pseudocode should not be framed as an optimality algorithm.

| Option | Description | Selected |
|--------|-------------|----------|
| Diagnostic appendix plus main-text boundary | Put exact/greedy details in appendix and state limits in main text. | Yes |
| Main-text subsection | Discuss exact/greedy directly in Results or Solution Method. | |
| Minimal limitations mention | Mention only in limitations or future work. | |

**User's choice:** Diagnostic appendix plus main-text boundary.
**Notes:** No near-optimality or exact-greedy computational credibility claim is allowed.

---

## Evidence Narrative

| Option | Description | Selected |
|--------|-------------|----------|
| Claim-gate first | Results starts with `claim_ready=false` and strict claim boundary, then diagnostic insights. | Yes |
| Findings first | Present service-menu diagnostic findings before revealing claim gate status. | |
| Move gate to Methods/Appendix | Keep Results cleaner and move status details elsewhere. | |

**User's choice:** Claim-gate first.
**Notes:** The revised text should be transparent without becoming a raw status dump.

| Option | Description | Selected |
|--------|-------------|----------|
| Result boundaries and future conditions | Discuss blocked claims as current evidence boundaries and future upgrade requirements. | Yes |
| Claim audit table only | Centralize blocked claims in a table. | |
| Appendix mostly | Keep blocked claims mostly out of main text. | |

**User's choice:** Result boundaries and future conditions.
**Notes:** A compact table may assist, but main-text explanation must carry the boundary.

| Option | Description | Selected |
|--------|-------------|----------|
| Diagnostic boundary | Treat no-filter/C5 only as ETA robustness diagnostic boundary. | Yes |
| Robustness main result | Present no-filter as stronger robustness evidence. | |
| Limitations only | Mention no-filter only as a limitation. | |

**User's choice:** Diagnostic boundary.
**Notes:** No-filter must not become an operational recommendation.

| Option | Description | Selected |
|--------|-------------|----------|
| Firm but not inflated | Claim formulation, paired diagnostic replay, and transparency, but not empirical superiority. | Yes |
| Very conservative | Emphasize limitations and blocked claims heavily. | |
| More positive diagnostic packaging | Make transparency/evidence governance the main paper contribution. | |

**User's choice:** Firm but not inflated.
**Notes:** Confidence should come from formulation and evidence control, not unauthorized superiority claims.

---

## Phase Deliverables

| Option | Description | Selected |
|--------|-------------|----------|
| Lean supporting checks | Revised manuscript plus prohibited-language scan plus brief revision summary. | Yes |
| Full submission package | Also update source map, claim audit, response, checklist, and readiness materials. | |
| Revised manuscript only | Produce only the manuscript text. | |

**User's choice:** Lean supporting checks.
**Notes:** Phase 6 already performed the full readiness audit. Phase 7 should prioritize manuscript quality.

| Option | Description | Selected |
|--------|-------------|----------|
| Update source map only if objects change | Update only when tables, figures, captions, or appendix objects change. | Yes |
| Always update source map | Force a refreshed source map for the revised draft. | |
| Never update source map | Keep source map outside Phase 7. | |

**User's choice:** Update source map only if objects change.
**Notes:** If no evidence objects change, record that in the revision summary.

| Option | Description | Selected |
|--------|-------------|----------|
| Completely forbid generated-artifact edits | No generated row, package status, claim guard, table, figure, or mirror edits. | Yes |
| Rerun builders only | Allow regeneration but no manual edits. | |
| Small metadata edits | Allow minor metadata changes. | |

**User's choice:** Completely forbid generated-artifact edits.
**Notes:** Phase 7 is manuscript revision, not evidence regeneration.

| Option | Description | Selected |
|--------|-------------|----------|
| Manuscript-focused checks plus baseline tests | Import smoke, claim guard test, manuscript readiness test, prohibited-language scan, and source-map checks if needed. | Yes |
| Text scan only | Only scan prose for prohibited language. | |
| Full Phase 6 checks | Rerun the entire Phase 6 command set. | |

**User's choice:** Manuscript-focused checks plus baseline tests.
**Notes:** Verification should be strong enough for claim safety but lighter than a full readiness audit.

---

## the agent's Discretion

- Planner and executor may choose paragraph-level rewrite strategy.
- Planner and executor may choose exact pseudocode formatting.
- Planner and executor may decide whether source-map update is needed based on revised manuscript object changes.

## Deferred Ideas

None. Discussion stayed within Phase 7 scope.
