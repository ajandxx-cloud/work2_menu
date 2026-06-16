---
phase: 14
status: gate_repair_plan_created
claim_ready: false
generated_at: 2026-06-16T18:44:53+08:00
timezone: Asia/Shanghai
phase_scope: planning_and_audit_only
binding_inputs:
  - .planning/milestones/claim_ready_resolution/01_EVIDENCE_BOUNDARY.md
  - .planning/milestones/claim_ready_resolution/01_CLAIM_READY_FALSE_CAUSES.md
  - .planning/milestones/claim_ready_resolution/01_BLOCKER_TAXONOMY.md
  - .planning/phases/13-evidence-boundary-reconstruction/13-RESULT_MANIFEST.md
---

# Gate Repair Plan Without Result Manipulation

## Boundary

Phase 14 creates a repair plan only. It does not repair gates, run new
empirical experiments, tune parameters, regenerate empirical rows, modify
algorithms, regenerate artifacts, edit generated rows, edit generated tables
or figures, edit `CLAIM_GUARD.json`, upgrade manuscript claims, or choose
Path A, Path B, or Path C.

The Phase 10 strict claim guard remains binding:

- source:
  `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`
- schema: `phase10-strict-claim-guard-v1`
- claims: 8
- overall `claim_ready=false`
- `manuscript_positive_claims_allowed=false`

No repair below authorizes a claim upgrade. Any future claim upgrade requires
a later authorized path and a regenerated strict claim guard.

## Current Gate Snapshot

| gate area | current observation | blocker refs |
| --- | --- | --- |
| Current working tree | `git status --short` was clean before Phase 14 edits. | CF-001, BT-001 |
| Historical formal readiness | Existing `FORMAL_READINESS.json` is `status: blocked`, `claim_ready_allowed: false`, with blocker `dirty_git`. | CF-001, BT-001 |
| Selected formal source rows | 35 completed rows, 7 policies, 5 paired splits, all checkpoint status `loaded`; rows carry dirty provenance from their original run. | EB-001, EB-002, CF-001 |
| Row schema metadata | Selected formal rows are missing `method_family`, `outside_option_util`, and `solver_candidate_count` under the current row schema. | CF-003, CF-004, BT-002 |
| Formal checkpoint | Formal robust checkpoint file exists and hash is recorded; robust-menu checkpoint sidecar is missing. | CF-001, BT-001 |
| Main RC artifact package | Current main package indexes blocked pilot/placeholder artifacts, includes `formal_skipped` and `missing_checkpoint_file` blockers, and is not claim-ready. | CF-002, BT-002 |
| Phase 10 package | 74 indexed artifacts, 70 existing, 4 missing, 108 blockers, all source families `claim_ready=false`. | CF-004, CF-010, CF-011 |
| Empirical performance | Random menu beats optimized adaptive on mean net profit, and adaptive/fixed-window rows are identical across tracked metrics. | CF-005, CF-006, BT-003, BT-004, BT-005 |
| Diagnostic evidence families | Phase 8, Phase 9, and case scaffold remain diagnostic/provisional or scaffold-only. | CF-007, CF-008, CF-009 |

## Repair Classification Rules

Phase 14 uses these repair classes exactly:

| repair class | meaning |
| --- | --- |
| non-semantic metadata/schema repair | Fixes provenance, metadata, schema compatibility, paths, hashes, sidecars, or inventory labels without changing empirical values, policy behavior, or claims. |
| code/builder repair | Fixes a builder, classifier, package collector, or reporting script so future generated outputs reflect source evidence correctly. |
| true experiment-row issue | The source generated rows themselves lack required fields or carry historical provenance that cannot be fixed by editing package files. |
| evidence-quality issue | The required evidence is absent, diagnostic-only, scaffold-only, or insufficient for the target scientific claim. |
| new experiment path | A stronger claim would require an authorized future replay, rerun, case execution, or stress experiment. |

Path handling in this plan is conditional only:

- `Path A allowed if later selected`: potentially legitimate gate-only repair,
  no empirical row value changes, no algorithm changes, no claim upgrade by
  wording.
- `requires Path B if later selected`: cannot be made claim-ready from the
  current source rows without an authorized pre-registered rerun or equivalent
  source-row regeneration.
- `should lead to Path C unless later evidence changes`: current evidence
  should remain diagnostic/locked unless Phase 15/16 identify a legitimate
  recoverable cause.

## Candidate Repairs

| repair_id | possible repair | exact blocker addressed | repair class | Path A / B / C treatment |
| --- | --- | --- | --- | --- |
| GR-001 | Record the current clean working tree and require a clean tree before any future readiness or artifact regeneration. | CF-001, BT-001 dirty-git readiness blocker. | non-semantic metadata/schema repair | Path A allowed if later selected. It repairs current preconditions only, not historical dirty row provenance. |
| GR-002 | Rerun only the formal readiness preflight from a clean tree, using the existing formal manifest and existing checkpoint, if later authorized. | CF-001 readiness `status: blocked`, `claim_ready_allowed=false`, blocker `dirty_git`. | non-semantic metadata/schema repair | Path A allowed if later selected. It is a gate rerun, not an empirical replay. |
| GR-003 | Preserve the existing formal checkpoint file and record its path, SHA-256, load status, model type, and compatibility in readiness metadata. | CF-001, EB-008 checkpoint provenance readiness. | non-semantic metadata/schema repair | Path A allowed if later selected, only if based on the existing checkpoint and smoke-load metadata. |
| GR-004 | Create or regenerate a robust-menu formal checkpoint sidecar for the existing checkpoint, if sidecar content can be derived from existing checkpoint/provenance without retraining. | CF-001, EB-008 missing checkpoint sidecar/hash concern. | non-semantic metadata/schema repair | Path A allowed only for deterministic sidecar metadata. If sidecar provenance cannot be recovered, it becomes an evidence-quality issue and may require Path B or Path C. |
| GR-005 | Verify the dependency snapshot path and hash before any future readiness promotion. | CF-001, BT-001 dependency/provenance readiness. | non-semantic metadata/schema repair | Path A allowed if later selected. Current snapshot exists and hash matches the recorded value. |
| GR-006 | Fix artifact builder/source selection so the main RC package can be built from the selected completed formal run rather than the older blocked pilot/placeholder source. | CF-002, BT-002 `formal_skipped` and `missing_checkpoint_file` package blockers. | code/builder repair | Path A allowed if later selected and if it only changes artifact source selection/regeneration from existing rows. |
| GR-007 | Regenerate main RC artifacts from authorized existing source rows and readiness metadata after row/provenance schema issues are resolved. | CF-002, CF-003, CF-004, BT-002. | code/builder repair | Path A allowed only after Phase 16 authorizes it and only if no empirical values are edited. |
| GR-008 | Fix or narrow package glob rules that create synthetic missing entries for optional source patterns. | CF-004, EB-CONF-003; missing `.yml`, missing `.json`, missing figure PNG placeholder entries. | code/builder repair | Path A allowed if later selected, when the missing pattern is optional/reporting-only. If a required evidence artifact is genuinely absent, it becomes Path B or Path C. |
| GR-009 | Generate missing main RC figure PNGs from existing aggregate data through the artifact builder, not by hand. | CF-004 main RC missing `figures/*.png` source patterns. | code/builder repair | Path A allowed if later selected. It is reporting/artifact generation only. |
| GR-010 | Keep `PACKAGE_INDEX.json` schema compatibility explicit: current schema uses `entries`; consumers expecting `package_entries` should be updated or made backward compatible. | EB-CONF-003 package schema-consumer mismatch risk. | non-semantic metadata/schema repair | Path A allowed if later selected. Current `manuscript_claims.py` already handles both shapes, so this is not an active blocker by itself. |
| GR-011 | Ensure future normalized row builders emit `method_family` for every row and artifact gates validate it. | CF-003, BT-002 missing or invalid `method_family`. | code/builder repair plus true experiment-row issue for existing rows | Path A allowed for future builder code only. Existing selected rows missing this field cannot be hand-edited; using them for claim-ready artifacts requires an authorized non-semantic row-metadata migration or Path B. |
| GR-012 | Ensure future normalized row builders emit `outside_option_util` for every row and artifact gates validate it. | CF-003, BT-002 missing `outside_option_util`. | code/builder repair plus true experiment-row issue for existing rows | Path A allowed for future builder code only. Existing selected rows missing this field cannot be hand-edited; deterministic metadata migration would need Phase 16 authorization. |
| GR-013 | Ensure future normalized rows emit `solver_candidate_count` or explicitly record it as unavailable with a schema-supported status. | CF-004 missing result fields; current row-schema drift. | true experiment-row issue and evidence-quality issue | Requires Path B if candidate-count evidence is needed for claim-ready artifacts. If unavailable, computational or mechanism claims should stay Path C-limited. |
| GR-014 | Keep original selected formal rows immutable and, if metadata migration is later considered, write a separate audited derived-row package rather than overwriting source rows. | CF-003, CF-004; generated row integrity guardrail. | non-semantic metadata/schema repair if authorized; otherwise true experiment-row issue | Path A allowed only if Phase 16 explicitly permits a non-semantic derived package with unchanged empirical metrics. Otherwise requires Path B or Path C. |
| GR-015 | Make artifact status report row-schema failures separately from empirical performance blockers. | CF-003, CF-004, BT-002. | code/builder repair | Path A allowed if later selected. This improves diagnosis without changing evidence. |
| GR-016 | Rebuild `CLAIM_GUARD.json` only through the package builder after authorized repairs, never by hand. | CF-010, BT-009 strict claim guard authority. | code/builder repair | Path A allowed only as a generated consequence of authorized repairs. If empirical blockers remain, regenerated guard must remain `claim_ready=false` for those claims. |
| GR-017 | Preserve root/runtime Phase 10 package mirror consistency by regenerating or mirroring through the builder only. | EB-CONF-001, CF-004 mirror/package provenance risk. | non-semantic metadata/schema repair | Path A allowed if later selected. Phase 13 observed no hash conflict for checked files. |
| GR-018 | Treat random-menu profit advantage as a scientific or implementation-diagnosis issue, not a gate repair. | CF-005, BT-003, BT-005. | evidence-quality issue | Not allowed in Path A. Requires Phase 15 diagnosis, then Path B if recoverable by pre-registered rerun, or Path C if it is a true result. |
| GR-019 | Treat adaptive/fixed-window equality as a scientific or implementation-diagnosis issue, not a gate repair. | CF-006, BT-004. | evidence-quality issue | Not allowed in Path A. Requires Phase 15 diagnosis, then Path B if recoverable by pre-registered rerun, or Path C if equality is real. |
| GR-020 | Keep Phase 8 sensitivity as diagnostic/provisional unless a later path authorizes new formal robustness evidence. | CF-007, BT-006. | evidence-quality issue and new experiment path | Not allowed in Path A for claim upgrade. Requires Path B or future experiment path for stronger robustness; otherwise Path C diagnostic lock. |
| GR-021 | Keep Phase 9 tractability as diagnostic/provisional unless a later path authorizes a stress setup that actually exercises greedy fallback and records gap/overlap. | CF-008, BT-007. | evidence-quality issue and new experiment path | Not allowed in Path A for computational credibility. Requires Path B or future experiment path; otherwise Path C. |
| GR-022 | Keep semi-real case material scaffold-only unless a later path authorizes case execution and result artifacts. | CF-009, BT-008. | evidence-quality issue and new experiment path | Not allowed in Path A for validation claims. Requires future authorized case execution or Path C. |
| GR-023 | Keep C7 provenance/status transparency separate from empirical effectiveness. | CF-012, BT-001, BT-009. | evidence-quality issue for empirical claims; non-semantic metadata/schema repair for status wording | Path A can preserve status transparency, but it cannot upgrade empirical claims. |
| GR-024 | Keep safe-language and manuscript claim maps aligned with strict claim guard output. | CF-010, BT-009. | non-semantic metadata/schema repair | Path C lock work may be appropriate later; Phase 14 does not edit manuscript claims or upgrade wording. |

## Blocker-To-Repair Map

| blocker | mapped repairs | repair boundary |
| --- | --- | --- |
| CF-001 provenance/readiness | GR-001, GR-002, GR-003, GR-004, GR-005 | Current clean-tree readiness may be repairable in Path A; historical dirty row provenance is not erased. |
| CF-002 artifact-generation | GR-006, GR-007, GR-016, GR-017 | Builder/source selection can be repaired later, but generated package files cannot be hand-edited. |
| CF-003 metadata | GR-011, GR-012, GR-014, GR-015 | Current selected rows are missing required metadata; repairability depends on Phase 16 authorization for non-semantic derived metadata versus Path B. |
| CF-004 artifact-schema | GR-008, GR-009, GR-010, GR-013, GR-015 | Optional package/schema issues are Path A candidates; missing result fields are not automatic Path A repairs. |
| CF-005 empirical-performance | GR-018 | Not a gate repair. Phase 15 owns diagnosis. |
| CF-006 adaptive-window | GR-019 | Not a gate repair. Phase 15 owns diagnosis. |
| CF-007 sensitivity-robustness | GR-020 | Diagnostic boundary unless later authorized evidence exists. |
| CF-008 computational-tractability | GR-021 | Diagnostic boundary unless later authorized evidence exists. |
| CF-009 semi-real-case | GR-022 | Scaffold-only boundary unless later authorized case evidence exists. |
| CF-010 manuscript-language | GR-016, GR-024 | Language cannot upgrade evidence; strict generated guard remains authority. |
| CF-011 blocker/status documents | GR-023, GR-024 | Status transparency only; not empirical evidence. |
| CF-012 C7 status-only support | GR-023 | Preserve provenance/status claim only. |

## Phase 17 Path A Candidate Set

If Phase 16 later selects Path A, the safe candidate repairs are limited to:

- clean-tree readiness preflight and provenance re-evaluation;
- deterministic checkpoint sidecar/hash/load-status metadata for the existing
  checkpoint;
- dependency snapshot verification;
- artifact-builder source selection and package schema fixes;
- missing reporting artifacts regenerated from existing authorized source
  evidence;
- strict claim guard regeneration through builders only.

Path A must not:

- change empirical row values by hand;
- overwrite original source rows;
- remove unfavorable baselines;
- tune parameters;
- modify algorithms;
- claim random-menu profit or adaptive-window problems were solved without
  Phase 15/16 authorization;
- upgrade any claim not authorized by a regenerated strict claim guard.

## Path B Or Path C Boundaries

The following are not legitimate gate-only repairs:

- changing the random-menu profit ranking;
- changing adaptive/fixed-window equality;
- producing candidate-count, greedy-gap, or case-validation evidence that is
  absent from current rows;
- converting Phase 8, Phase 9, or case scaffold evidence from diagnostic to
  claim-ready by wording;
- treating C7 status support as empirical effectiveness support.

These issues require Phase 15/16 diagnosis and either a pre-registered Path B
rerun/future experiment path or a Path C diagnostic lock. Phase 14 does not
choose between them.

## Non-Authorization Statement

This plan is an audit artifact. It does not authorize any gate repair, artifact
regeneration, row migration, empirical rerun, parameter change, manuscript
language upgrade, or claim upgrade.
