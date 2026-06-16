---
phase: 14
status: artifact_schema_repair_plan_created
claim_ready: false
generated_at: 2026-06-16T18:44:53+08:00
timezone: Asia/Shanghai
phase_scope: planning_and_audit_only
---

# Artifact Schema Repair Plan

## Boundary

This document diagnoses artifact-schema and reporting issues only. It does not
repair schemas, edit rows, regenerate artifacts, or change claim status.

Generated evidence files under `work2_coding/outputs/`, `work2_coding/artifacts/`,
and root `artifacts/` must not be edited by hand.

## Inputs Inspected

| input | observation |
| --- | --- |
| `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json` | `artifact_count=74`, `existing_artifact_count=70`, `missing_artifact_count=4`, `blocker_count=108`, `claim_ready=false`. |
| `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_INDEX.json` | Current package schema uses top-level `entries`; 74 entries across five source families. |
| `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json` | 8 claims, overall `claim_ready=false`; C7 only is status/provenance ready. |
| `work2_coding/artifacts/work2_robust_menu/ARTIFACT_STATUS.json` | Main RC package is blocked, `placeholder_only=true`, checkpoint status `failed`, blockers `missing_checkpoint_file` and `formal_skipped`. |
| `work2_coding/outputs/phase3_formal_artifacts/ARTIFACT_STATUS.json` | 35 completed formal rows, checkpoint status `loaded`, but artifact status is blocked because row metadata lacks `outside_option_util` and valid `method_family`. |
| selected formal `normalized_rows.json` | 35 completed rows are missing `method_family`, `outside_option_util`, and `solver_candidate_count` under the current schema. |
| `work2_coding/Src/paired_replay.py` | Current `NORMALIZED_ROW_FIELDS` includes `method_family`, `outside_option_util`, and `solver_candidate_count`. |
| `work2_coding/Src/artifact_status.py` | Formal/pilot artifact classification blocks missing `method_family` and missing `outside_option_util`. |
| `work2_coding/Src/paper_artifacts.py` | Package collection creates missing placeholder entries when a glob has no matches. |

## Schema Drift Finding

Read-only validation of the selected 35 formal rows against the current row
schema found:

| field | missing rows | classification | consequence |
| --- | ---: | --- | --- |
| `method_family` | 35/35 | true experiment-row issue; code/builder repair for future rows | Current rows cannot satisfy formal model-family artifact gates without authorized non-semantic migration or rerun. |
| `outside_option_util` | 35/35 | true experiment-row issue; code/builder repair for future rows | Current rows cannot satisfy outside-option utility artifact gates without authorized non-semantic migration or rerun. |
| `solver_candidate_count` | 35/35 | true experiment-row issue and evidence-quality issue | Current rows lack candidate-count evidence needed by solver/tractability diagnostics. |

The current row builder already defines these fields for new rows, so this is
also a historical row-schema drift issue: the selected formal rows predate the
current row schema.

## Artifact Issues

| issue_id | issue | evidence | diagnosis | allowed future treatment |
| --- | --- | --- | --- | --- |
| AS-001 | Missing `method_family` in selected formal rows. | 35/35 selected formal rows lack the field; Phase 3 artifact status lists `method_families=[]`. | true experiment-row issue; possible code/builder repair for future rows | Path A only if Phase 16 authorizes a non-semantic derived metadata package without overwriting source rows. Otherwise requires Path B or remains diagnostic. |
| AS-002 | Missing `outside_option_util` in selected formal rows. | 35/35 selected formal rows lack the field; Phase 3 artifact status lists `outside_option_utils=[]`. | true experiment-row issue; possible code/builder repair for future rows | Same as AS-001. Do not hand-edit rows to insert `0.0`. |
| AS-003 | Missing `solver_candidate_count` in selected formal rows. | Current schema requires it; selected formal rows lack it. | true experiment-row issue and evidence-quality issue | Requires Path B if candidate counts are needed for claim-ready mechanism or computational evidence. If unavailable, keep relevant claims blocked. |
| AS-004 | Main RC artifact package indexes older blocked pilot/placeholder source instead of the selected completed formal run. | Main `ARTIFACT_STATUS.json` source run is `pilot_robust_menu-20260611T082839Z-e1646ba1`, with `placeholder_only=true`, `checkpoint_statuses=['failed']`, `formal_skipped`. | code/builder repair | Path A candidate if later selected: rebuild/package from the authorized completed source and readiness metadata. |
| AS-005 | `formal_skipped` package blockers. | Phase 10 package records 28 `formal_skipped` blockers for main RC artifacts. | artifact-builder/source-selection issue | Path A candidate only after source-selection and readiness/row schema blockers are resolved. |
| AS-006 | `missing_checkpoint_file` package blockers for pilot checkpoint path. | Main artifact package records missing pilot checkpoint `outputs/shared_training/work2_robust_menu/pilot/supervised_ml.pt`. | artifact-builder/source-selection issue for main RC package; checkpoint evidence issue for that old pilot package | Path A candidate if the package stops using the blocked pilot source. Do not fabricate a pilot checkpoint for old blocked rows. |
| AS-007 | Missing main RC figure PNGs. | `work2_coding/artifacts/work2_robust_menu/figures/` contains only `*.status.json`; package records missing `figures/missing.png` and `figures/missing.metadata.json`. | reporting/artifact-builder issue | Path A candidate if figures are regenerated from existing authorized aggregate data. |
| AS-008 | Package collector creates synthetic missing entries for optional absent patterns. | `PACKAGE_INDEX.json` has missing `.planning/data/case_studies/missing.yml`, missing `.planning/data/case_studies/missing.json`, and missing main figure placeholders. | package metadata/builder issue when the patterns are optional | Path A candidate if the builder distinguishes required from optional source patterns. If a source is truly required evidence, it remains evidence-quality blocked. |
| AS-009 | Case scaffold package has missing `.yml` and `.json` placeholders. | Case scaffold directory has `.yaml`, `.md`, and `.py` files but no `.yml` or `.json`; package counts 10 existing out of 12. | package metadata/builder issue plus scaffold-only evidence boundary | Path A can clean optional inventory noise; case validation claims still require Path B/future execution or Path C. |
| AS-010 | `PACKAGE_INDEX.json` uses `entries`, not `package_entries`. | Phase 13 EB-CONF-003 found no `package_entries` key; current `manuscript_claims.py` supports both. | non-semantic metadata/schema compatibility issue, not an active blocker | Path A candidate only if a downstream consumer fails; otherwise no repair needed. |
| AS-011 | Phase 8 status remains diagnostic/provisional. | Phase 8 `ARTIFACT_STATUS.json` status `diagnostic_provisional_blocked`, `claim_ready=false`. | evidence-quality issue, not schema repair | Not Path A for claim upgrade. Requires later authorized evidence or diagnostic lock. |
| AS-012 | Phase 9 status remains diagnostic/provisional and greedy fallback was not exercised. | Phase 9 `ARTIFACT_STATUS.json` has `large_row_not_greedy` and `large_fallback_reason_missing` failures. | evidence-quality issue and possible new experiment path | Not Path A for computational credibility. Requires Path B/future stress evidence or diagnostic lock. |
| AS-013 | `CLAIM_GUARD.json` and package status are generated blocked outputs. | Strict guard keeps six positive claim ids blocked; C5 diagnostic-only; C7 status-only. | claim-boundary artifact, not schema error | Regenerate only through builders after authorized repairs. Do not edit by hand. |

## Source-Row Versus Reporting Split

| category | issues | repair boundary |
| --- | --- | --- |
| Reporting/schema issue | AS-007, AS-008, AS-009, AS-010 | Can be Path A candidates if later selected and if regenerated from existing source evidence. |
| Artifact-builder issue | AS-004, AS-005, AS-006, AS-007, AS-008 | Can be Path A candidates if later selected, but only through builder changes and regeneration. |
| True source-row issue | AS-001, AS-002, AS-003 | Cannot be fixed by hand-editing rows. Requires Phase 16 authorization for a derived metadata package, Path B, or diagnostic lock. |
| Evidence-quality issue | AS-003, AS-011, AS-012, AS-013 | Cannot be made claim-ready by schema repair alone. |

## Required Future Guardrails

If a later phase authorizes repairs:

1. Preserve original generated rows unchanged.
2. If non-semantic row metadata migration is permitted, write a separate
   derived package with explicit source hashes and unchanged empirical metrics.
3. Regenerate artifacts only through `work2_coding/scripts/*` builders.
4. Keep artifact status and claim guard generated, not manually edited.
5. Keep Phase 8, Phase 9, and case scaffold status labels unless new
   authorized evidence changes them.
6. Keep random-menu profit advantage and adaptive/fixed-window equality out of
   gate repair scope.

## Non-Authorization Statement

This plan does not repair artifact schema issues. It only records what would
need to be repaired if a later path authorizes it.
