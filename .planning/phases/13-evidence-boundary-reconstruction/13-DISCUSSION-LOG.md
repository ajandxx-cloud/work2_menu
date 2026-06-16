# Phase 13: Evidence Boundary Reconstruction - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md; this log preserves the alternatives considered.

**Date:** 2026-06-16T15:47:00+08:00
**Phase:** 13-Evidence Boundary Reconstruction
**Areas discussed:** Evidence source authority and conflicts, claim_ready=false classification granularity, Deliverable organization, Phase 13 recommendation boundary

---

## Evidence Source Authority And Conflicts

| Question | Options Considered | User's Choice |
| --- | --- | --- |
| When sources disagree, what authority order should Phase 13 use to reconstruct the evidence boundary? | Generated artifacts first; Planning summaries first; Dual-track audit; Other | Dual-track audit |
| How should disagreements between evidence sources be presented? | Conflict matrix; Narrative summary only; Only claim-impacting conflicts; Other | Conflict matrix |
| How deeply should Phase 13 read the evidence sources? | Layered reading; Read all 74 source artifacts; Read summary/status layer only; Other | Layered reading |
| How should Phase 13 handle the root mirror versus work2_coding artifact package? | Record mirror consistency check result; Audit both directories separately; Ignore root mirror; Other | Record mirror consistency check result |

**Notes:** Phase 13 records conflicts instead of forcing final authority. Runtime
source is `work2_coding/artifacts/...`; root `artifacts/...` is treated as a
mirror and compared for consistency.

---

## claim_ready=false Classification Granularity

| Question | Options Considered | User's Choice |
| --- | --- | --- |
| What level of detail should `01_CLAIM_READY_FALSE_CAUSES.md` use for causes? | Three-level traceability; Blocker-category summary only; Full raw blocker expansion; Other | Three-level traceability |
| How should repeated blockers be handled? | Merge duplicates and preserve instance counts; Keep every raw occurrence; Keep unique reason text only; Other | Merge duplicates and preserve instance counts |
| Should Phase 13 separate fixable gate/metadata causes from true empirical unsupported-result causes? | Yes, preliminary tags only; No; Yes, give explicit repair path; Other | Yes, give explicit repair path |
| How should each claim be classified at the end of Phase 13? | Four-state classification; Three-state classification; Use claim guard original state only; Other | Four-state classification |

**Notes:** The user revised the third decision from preliminary tags to explicit
repair-path recommendations. Phase 13 may recommend repair, rerun, or
diagnostic lock, but not execute or authorize those paths.

---

## Deliverable Organization

| Question | Options Considered | User's Choice |
| --- | --- | --- |
| What style should the three Phase 13 deliverables use? | Audit tables first; Narrative first; Mixed: first narrative, latter two tables; Other | Mixed: first narrative, latter two tables |
| What narrative spine should `01_EVIDENCE_BOUNDARY.md` use? | Timeline spine; Claim spine; Artifact-family spine; Other | Timeline spine |
| Should `01_BLOCKER_TAXONOMY.md` use the roadmap's nine categories exactly or allow subcategories? | Fixed nine top-level categories plus optional subcategories; Only nine categories; Free classification; Other | Fixed nine top-level categories plus optional subcategories |
| Should the three deliverables cross-index each other? | Strong cross-indexing; Lightweight references only; No cross-indexing; Other | Strong cross-indexing |

**Notes:** The deliverables should use stable ids such as `EB-001`, `CF-001`,
and `BT-001` so later phases can cite specific boundary items, false causes,
and taxonomy rows.

---

## Phase 13 Recommendation Boundary

| Question | Options Considered | User's Choice |
| --- | --- | --- |
| How strong should Phase 13's repair-path language be? | Recommended but not authorized; Quasi-authorizing; Hints only, no action; Other | Recommended but not authorized |
| May Phase 13 explicitly identify cases that should not be repaired by wording? | Allowed and mandatory; Only write what should be repaired; Only for severe cases; Other | Allowed and mandatory |
| How specific should rerun recommendations be? | Only mark rerun_candidate, no experiment design; Give minimum rerun conditions; Give concrete rerun draft; Other | Only mark rerun_candidate, no experiment design |
| Should Phase 13 write an overall Path A/B/C tendency? | No final path, claim-level candidates only; Write a non-binding tendency; Directly recommend a path; Other | No final path, claim-level candidates only |

**Notes:** Phase 13 should be action-oriented but not path-authorizing. Overall
Path A/B/C remains Phase 16 authority.

---

## The Agent's Discretion

- Choose exact table column names as long as cross-indexing and traceability are preserved.
- Choose representative artifact ids for canonical causes while preserving affected artifact counts.
- Use helper parsing scripts only for planning-side audit tables, not for editing generated evidence.

## Deferred Ideas

- Gate repair execution is deferred to Phase 14 and later.
- Source-row and code-path failure diagnosis is deferred to Phase 15.
- Overall Path A/B/C decision is deferred to Phase 16.
