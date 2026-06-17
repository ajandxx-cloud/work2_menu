# Phase 5: TR-E Manuscript Draft Construction - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution
> agents. Decisions are captured in CONTEXT.md; this log preserves the
> alternatives considered.

**Date:** 2026-06-17T18:40:41.0938801+08:00
**Phase:** 5-TR-E Manuscript Draft Construction
**Areas discussed:** Manuscript carrier and legacy draft handling,
Introduction narrative, Results and appendix evidence placement, Mathematical
model and method depth

---

## Manuscript Carrier And Legacy Draft Handling

| Question | Options considered | Selected |
| --- | --- | --- |
| How should Phase 5 handle the existing `manuscript/main.tex`? | Create new Markdown draft; rewrite LaTeX; maintain parallel Markdown and LaTeX drafts | Create `manuscript/TR_E_WORK2_MANUSCRIPT_DRAFT.md` as the primary draft |
| How should the old `manuscript/main.tex` be used during Phase 5? | Keep but do not edit body; minimal cleanup; use as migration source | Use as migration source after rewriting unsafe framing |
| Which content should be migrated first? | Model/notation/literature first; migrate broadly then audit; only migrate references | Model, notation, MNL/menu objective, literature references, and Elsevier metadata first |
| How should legacy migration risk be represented? | Separate internal review; claim audit only; manuscript footnotes | Separate `TR_E_WORK2_RESPONSE_TO_INTERNAL_REVIEW.md` |

**User's choices:** 1, 3, 1, 1.
**Notes:** The old LaTeX source is useful but must not carry forward old TR-C,
`DSPO_PLUS`, ranking-validation, or dominance language.

---

## Introduction Narrative

| Question | Options considered | Selected |
| --- | --- | --- |
| What should be the primary narrative in abstract and introduction? | Service-menu optimization framework first; evidence audit first; equal emphasis | Service-menu optimization framework first |
| How should the contribution list be organized? | Three contributions; two contributions; four contributions | Three contributions: formulation, diagnostic evaluation, claim-gated traceability |
| How should the current empirical state be described? | Explicit conditional diagnostic wording; light evidence-boundary wording; move blocked state to Results/Discussion | Explicit conditional diagnostic wording |
| Should title and keywords retain old `Behavior-Aware` and `DSPO_PLUS` language? | Switch to service-menu / claim-gated diagnostic language; keep Behavior-Aware only; keep DSPO/DSPO_PLUS | Switch to service-menu / claim-gated diagnostic language |

**User's choices:** 1, 1, 1, 1.
**Notes:** The paper should look first like a TR-E transportation operations
and service-menu optimization manuscript, while being transparent early about
the conditional diagnostic evidence state.

---

## Results And Appendix Evidence Placement

| Question | Options considered | Selected |
| --- | --- | --- |
| How should the main Results section begin? | Claim-gate status table first; policy comparison status first; diagnostic narrative first | Claim-gate status table first |
| Where should Phase 8 ETA/no-filter diagnostic material appear? | Short main-text subsection plus full appendix; appendix only; main-text emphasis | Short main-text subsection plus full appendix |
| Where should Phase 9 exact/greedy tractability material appear? | Appendix first with brief Discussion reference; Results subsection; claim audit only | Appendix first with brief Discussion reference |
| How should case-study scaffold material be handled? | Appendix/future-work scaffold; exclude from manuscript; method section future case design | Appendix/future-work scaffold |

**User's choices:** 1, 1, 1, 1.
**Notes:** C5 can appear as diagnostic boundary material. C6 and C8 must remain
blocked diagnostic or scaffold-only and cannot support positive manuscript
claims.

---

## Mathematical Model And Method Depth

| Question | Options considered | Selected |
| --- | --- | --- |
| How deep should Mathematical Model be? | Complete core model in main text; light main text with full appendix; conceptual model only | Complete core model in main text |
| How should exact enumeration and greedy fallback be described? | Algorithm contract plus blocked diagnostic status; conceptual only; detailed performance | Algorithm contract plus blocked diagnostic status |
| Where should provenance and claim-gate mechanisms be described? | Experimental Design; both Method and Experimental Design; Results/Appendix only | Experimental Design |
| Should Lambert-W pricing remain in main method description? | Keep as price-generation component; reduce to implementation detail; emphasize as core contribution | Keep as price-generation component |

**User's choices:** 1, 1, 1, 1.
**Notes:** Method should be technically credible without turning blocked
computational or pricing evidence into positive claims.

---

## The Agent's Discretion

None. The user made explicit selections for all discussed gray areas.

## Deferred Ideas

None.
