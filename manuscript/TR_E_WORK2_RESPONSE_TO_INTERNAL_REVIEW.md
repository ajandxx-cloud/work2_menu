# Work2 TR-E Response To Internal Review

**Phase:** 05 - TR-E Manuscript Draft Construction
**Manuscript path:** conditional diagnostic
**Claim authority:** strict `CLAIM_GUARD.json`

## Migrated Legacy Material

The legacy `manuscript/main.tex` may contribute the following material only after rewrite:

- Notation for service bundles, displayed menus, and MNL choice.
- Mathematical model skeleton for bundle utility, outside option, and expected menu objective.
- Method concepts for candidate bundles, menu construction, time-window handling, and Lambert-W price generation.
- Literature references and bibliography entries from `manuscript/references.bib`.
- Elsevier metadata such as author, affiliation, and bibliography wiring.

Plan 02 migrated the notation and model skeleton into `TR_E_WORK2_MANUSCRIPT_DRAFT.md` after rewriting the venue, contribution, and results framing around the conditional diagnostic TR-E path. The draft uses service-menu optimization, paired replay, checkpoint provenance, artifact status, and strict claim guard language as the organizing frame.

## Removed Unsafe Framing

The Phase 5 manuscript must not carry forward these legacy elements:

Status label: removed unsafe framing.

- TR-C venue framing.
- Behavior-Aware foregrounding in title, abstract, or contribution list.
- DSPO_PLUS foregrounding as the central paper identity.
- Ranking validation promises.
- Dominance, superiority, improvement, proof, real-passenger validation, or near-optimality claims not authorized by the strict claim guard.

Plan 02 removed the legacy title, TR-C abstract framing, DSPO_PLUS-centered contribution frame, and policy-ranking promise from the new Markdown draft. Legacy method material was rewritten as service-menu formulation and diagnostic evaluation structure rather than as an empirical ranking claim.

## Reviewer-Risk Response

| Reviewer risk | Phase 5 response |
| --- | --- |
| Why not claim adaptive-menu superiority? | C1 is unsupported_blocked. The manuscript reports the comparison structure and blockers only. |
| Why was final replay not run? | The one authorized pre-replay gate remained blocked by dirty git provenance and missing formal checkpoint evidence; final replay was not authorized. |
| Is no-filter operationally recommended? | No. C5 is diagnostic boundary only. |
| Does case material validate passengers? | No. C8 is scaffold_only_blocked and future-study only. |
| Does tractability prove solver credibility? | No. C6 is blocked_diagnostic and appendix-only. |
| Does provenance transparency solve empirical blockers? | No. C7 supports status/provenance transparency only. |
| Are opt-out and accepted home pickup mixed? | No. The draft keeps opt-out, accepted home, and accepted meeting-point service separate. |
| Why trust the claim guard? | It is generated from package status and source-family evidence and is treated as the manuscript claim ceiling. |

## Unresolved Risks For Phase 6

- Academic prose quality and journal fit require final editorial review.
- Novelty framing must remain service-menu optimization centered without overstating current evidence.
- Any future positive claim requires regenerated evidence and strict guard authorization.
- Final LaTeX migration remains out of Phase 5 scope.
- Phase 6 should review whether the conditional diagnostic positioning is strong enough for TR-E or should be routed to revise-before-submission.

## Final Verification

Plan 03 verification completed on 2026-06-17.

| Check | Result |
| --- | --- |
| `python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` from `work2_coding/` | PASS: `IMPORT_OK` |
| `python scripts/test_manuscript_claim_guard.py` from `work2_coding/` | PASS: `PASS: 5 manuscript claim guard tests` |
| Five manuscript deliverables exist | PASS |
| Required TR-E manuscript sections exist | PASS |
| Source-map traceability columns exist | PASS |
| Claim audit covers C1 through C8 | PASS |
| Prohibited-language body scan | PASS: two hits, both classified as blocked/status discussion |

Remaining Phase 6 work is editorial and readiness-oriented: assess novelty, model rigor, empirical credibility, claim safety, traceability, reproducibility, English quality, and reviewer attack points before any submission recommendation.
