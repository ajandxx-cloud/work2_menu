# M4B Reviewer Risk Response Plan

**Manuscript path:** conditional diagnostic  
**Claim authority:** strict claim guard  

## Core Response Position

The paper should not pretend to be a claim-ready empirical superiority study. Its defensible position is a claim-gated diagnostic service-menu optimization manuscript: it formulates the menu decision, shows the paired replay and artifact-gate pipeline, and reports exactly which empirical claims remain blocked.

## Reviewer Risk Matrix

| Reviewer risk | Response strategy | Evidence source |
| --- | --- | --- |
| "Why do you not claim the adaptive menu is superior?" | State that the strict claim guard blocks central adaptive-menu superiority. The manuscript reports the comparison structure and blockers, not superiority. | `CLAIM_GUARD.json`, `PACKAGE_STATUS.json`, `M4B_SAFE_CLAIM_TABLE.md` |
| "Why was final replay not run?" | Explain that the one authorized pre-replay gate produced blocked readiness: `dirty_git` and `missing_formal_checkpoint`. Phase 4 explicitly prohibits running final replay on failed gates. | `M4A_PRE_REPLAY_GATE_REPORT.md`, `M4A_FINAL_REPLAY_REPORT.md` |
| "Is no-filter an operational recommendation?" | No. No-filter is diagnostic boundary evidence only. The manuscript must avoid deployment or recommendation language for no-filter variants. | `CLAIM_SAFE_LANGUAGE.md`, `M4B_SAFE_CLAIM_TABLE.md` |
| "Does the case material validate real passengers?" | No. Case material is scaffold-only and may be described only as future-study context. It must not be used as case validation or real passenger behavior evidence. | `.planning/data/case_studies/`, `CLAIM_GUARD.json` |
| "Does tractability evidence prove near-optimal greedy behavior?" | No. Tractability evidence is diagnostic/provisional and blocked for computational credibility claims. Avoid near-optimal wording. | Phase 9 package status, `CLAIM_GUARD.json` |
| "Does provenance transparency solve empirical blockers?" | No. C7 supports transparency about blockers and claim gates; it does not prove empirical effectiveness. | `PACKAGE_STATUS.json`, `CLAIM_GUARD.json` |
| "Are opt-out and home pickup mixed?" | State that the manuscript and artifact gates preserve opt-out/home/meeting-point separation, and any generated evidence must keep `count_opted_out`, `count_accepted_home`, and `count_accepted_meeting_point` separate. | paired replay schema, artifact gate tests, safe claim table |
| "Why trust the claim guard?" | The claim guard is generated from package status and source-family evidence, enumerates blocked claims and allowed claims by ID, and is treated as the manuscript claim ceiling. | `CLAIM_GUARD.json`, `PACKAGE_STATUS.json` |

## Required Language

Use:

- formulate
- evaluate
- diagnose
- audit
- identify boundary conditions
- claim-gated evidence
- diagnostic evidence
- conditional manuscript path

Avoid:

- dominates
- superior
- improves
- near-optimal
- validates real passengers
- real passenger behavior
- proves
- outperforms

## Section-Level Guidance

**Introduction:** Claim a transparent framework and diagnostic evidence boundary, not empirical dominance.

**Method:** Emphasize service-menu formulation, paired replay design, opt-out/home separation, and claim-gate contracts.

**Experimental Design:** Explain that final claim-ready replay was gated and blocked in this milestone. Present the gate as an integrity control, not a weakness to hide.

**Results:** Report package status, claim guard status, and diagnostic family statuses. Keep no-filter, case, and tractability material in boundary or appendix language.

**Discussion:** Convert blocked claims into reviewer-facing limitations and future work. State that stronger claims require clean provenance, loaded final checkpoint, completed final rows, package pass, and strict guard authorization.

**Conclusion:** The defensible conclusion is conditional diagnostic: the study provides a claim-gated service-menu optimization framework and transparent evidence audit, while positive empirical claims remain blocked.

## Evidence Boundary Summary

The evidence boundary is the protection mechanism. It prevents the manuscript from overstating blocked results, treating no-filter diagnostics as recommendations, treating scaffold-only case material as validation, or converting diagnostic tractability evidence into near-optimality claims.

The claim guard is the authority for manuscript wording. Phase 5 should quote or paraphrase claim-specific status, not infer broader empirical support from one allowed transparency claim.
