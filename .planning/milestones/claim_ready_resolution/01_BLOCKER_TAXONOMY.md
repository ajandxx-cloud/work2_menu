---
phase: 13
status: blocker_taxonomy_complete
claim_ready: false
generated_at: 2026-06-16T17:41:12+08:00
timezone: Asia/Shanghai
---

# Blocker Taxonomy

Phase 13 classifies blockers only. It does not repair metadata, modify
builders, run new experiments, regenerate artifacts, write manuscript claims,
or select a downstream path.

## Taxonomy Table

| taxonomy_id | top_level_class | canonical_cause_refs | evidence_boundary_refs | affected_claim_ids | source_artifacts | current_status | repairability | phase13_treatment | downstream_owner | not_allowed_in_phase13 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BT-001 | provenance/readiness | CF-001, CF-011, CF-012 | EB-002, EB-007, EB-008, EB-018, EB-020 | C1, C2, C4, C5, C6, C7, C8 | `FORMAL_READINESS.json`; `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md`; `CLAIM_GUARD.json` | readiness blocked; C7 status-only supported | potentially repairable by metadata/provenance cleanup for gates; C7 boundary is status-only and must not be treated as empirical repair | Record boundary and defer action | Phase 14 for repair planning; Phase 16 for claim ceiling | No git cleanup, no readiness rerun, no claim upgrade |
| BT-002 | artifact-generation | CF-002, CF-003, CF-004 | EB-003, EB-016, EB-018, EB-CONF-002, EB-CONF-003 | C1, C2, C3, C4, C6, C8 | `PACKAGE_STATUS.json`; `PACKAGE_INDEX.json`; `work2_coding/artifacts/work2_robust_menu/ARTIFACT_STATUS.json`; `work2_coding/outputs/phase3_formal_artifacts/ARTIFACT_STATUS.json` | package `claim_ready=false`; 108 blockers; 4 missing artifacts | potentially repairable by metadata/schema repair or code/builder repair; source evidence does not prove which yet | Catalogue blocker families and preserve runtime/package scope conflict | Phase 14 | No artifact regeneration, no hand-editing package files, no row repair |
| BT-003 | empirical-performance | CF-005 | EB-004, EB-006 | C1, C4 | `.planning/results/RC_FORMAL_DIAGNOSIS.md`; `.planning/results/RC_FORMAL_POLICY_SUMMARY.csv`; `.planning/results/RC_FORMAL_PAIRED_DIFFS.csv` | random menu has better mean net profit; adaptive loses 3/5 profit splits to random | requires source-row/code-path diagnosis; may require legitimate pre-registered rerun or may be a true scientific limitation | Preserve as current empirical boundary | Phase 15, then Phase 16 | No parameter tuning, no baseline removal, no performance wording upgrade |
| BT-004 | adaptive-window | CF-006 | EB-005, EB-006 | C3 | `.planning/results/RC_FORMAL_DIAGNOSIS.md`; policy summary artifacts | adaptive and fixed-window rows are identical across tracked metrics | requires code/path diagnosis; if true equivalence, it is a scientific limitation; if implementation/config issue, later repair/rerun may be needed | Preserve equality as current blocker | Phase 15, then Phase 16 | No directional adaptive-window language |
| BT-005 | random-baseline | CF-005 | EB-004, EB-006 | C1, C4 | `.planning/results/RC_FORMAL_DIAGNOSIS.md`; paired diffs CSV | random-menu baseline currently outperforms adaptive on mean profit | requires diagnosis; cannot be fixed by metadata; may require legitimate pre-registered rerun or diagnostic lock | Keep random baseline visible as serious comparator | Phase 15, then Phase 16 | No deleting or downgrading random baseline |
| BT-006 | sensitivity | CF-007 | EB-009, EB-010, EB-011, EB-018 | C2, C4, C5 | `.planning/results/SENSITIVITY_SUMMARY.md`; Phase 8 sensitivity artifacts | `diagnostic_provisional_blocked`; `claim_ready=false`; deferred dimensions unavailable | current use is diagnostic lock; stronger robustness requires later legitimate pre-registered evidence | Preserve diagnostic/provisional label | Phase 16 | No robustness proof, no managerial upgrade, no new sensitivity run |
| BT-007 | tractability | CF-008 | EB-012, EB-013, EB-014, EB-018 | C4, C6 | `.planning/results/COMPUTATIONAL_TRACTABILITY_SUMMARY.md`; Phase 9 tractability artifacts | `diagnostic_provisional_blocked`; large rows did not use greedy; gap/overlap unavailable | stronger claim requires legitimate pre-registered rerun; builder/threshold repair possible only if later diagnosis supports it | Preserve blocked computational-credibility boundary | Phase 16 | No near-optimal greedy, online tractability, or exact-vs-greedy quality claim |
| BT-008 | semi-real-case | CF-009 | EB-015, EB-019 | C8 | `.planning/data/case_studies/*`; Phase 7 verification; Phase 10 case-scaffold entries | scaffold-only; no runtime case manifest or result evidence | true evidence absence for validation claims; requires later authorized case execution, not wording repair | Preserve scaffold-only boundary | Phase 16 and later selected execution phase | No case execution, no real passenger behavior language, no validation claim |
| BT-009 | manuscript-language | CF-010, CF-012 | EB-017, EB-020 | C1, C2, C3, C4, C5, C6, C7, C8 | `CLAIM_GUARD.json`; `.planning/paper/CLAIM_SAFE_LANGUAGE.md`; `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md` | strict guard blocks positive claims; C5 diagnostic only; C7 status only | not repairable by wording; only regenerated strict guard after authorized evidence can upgrade claims | Keep strict guard binding | Phase 16 and later manuscript-lock phases | No claim upgrade, no prohibited phrasing, no manuscript body writing |

## Class Notes

### provenance/readiness

This class covers dirty-git readiness, checkpoint/provenance status, blocked
status documents, and the C7 status-only ceiling. Some readiness blockers may
be repairable by legitimate metadata/provenance cleanup, but Phase 13 cannot
perform cleanup or rerun gates.

### artifact-generation

This class covers package and artifact-builder outputs that currently report
blocked main RC artifacts, missing source patterns, missing files, and missing
row metadata. Phase 13 cannot determine whether each item is a schema repair,
builder repair, or true row issue; Phase 14 owns that separation.

### empirical-performance

This class covers observed performance facts from the selected formal
diagnosis. Random-menu profit advantage is not a metadata blocker. It is
either an empirical limitation, a configuration/modeling issue, or a code-path
issue to be diagnosed in Phase 15.

### adaptive-window

This class covers the equality of adaptive and optimized fixed-window rows.
The current evidence blocks directional adaptive-window wording. Phase 15 must
diagnose whether equality is expected, configured, or erroneous.

### random-baseline

This class corresponds to the user's random-menu-baseline boundary and keeps
the random menu as a real comparator. Phase 13 may not remove or reframe it
away because it is unfavorable to the central claim.

### sensitivity

This class corresponds to the user's sensitivity-robustness boundary. Phase 8
is useful diagnostic boundary evidence, but it is not claim-ready robustness
evidence.

### tractability

This class corresponds to the user's computational-tractability boundary.
Phase 9 currently reports exact-solver diagnostics, not an established
exact-vs-greedy comparison.

### semi-real-case

This class covers scaffold-only case material. It is not repairable by
language because the missing object is executed, reproducible case evidence.

### manuscript-language

This class enforces strict claim-guard authority. Language can make current
claims safer, but it cannot make unsupported evidence claim-ready.

## Cross-Reference Completeness

- Every CF-* cause from `01_CLAIM_READY_FALSE_CAUSES.md` appears in at least
  one BT-* row.
- Every BT-* row references at least one EB-* boundary fact.
- All top-level classes required by the roadmap appear exactly once as primary
  rows: provenance/readiness, artifact-generation, empirical-performance,
  adaptive-window, random-baseline, sensitivity, tractability,
  semi-real-case, and manuscript-language.
