---
phase: 13
status: claim_ready_false_causes_catalogued
claim_ready: false
generated_at: 2026-06-16T17:41:12+08:00
timezone: Asia/Shanghai
source_claim_guard: work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json
source_package_status: work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json
---

# Claim-Ready False Causes

## Current Claim Guard Snapshot

The strict Phase 10 claim guard is the controlling source for manuscript claim
authority. It reports schema `phase10-strict-claim-guard-v1`, eight claims,
overall `claim_ready=false`, and
`manuscript_positive_claims_allowed=false`.

| claim_id | support_status | manuscript_allowed | claim_ready | source_count | blocker_count | phase13_classification |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `C1_central_adaptive_menu_superiority` | `unsupported_blocked` | false | false | 36 | 38 | `rerun_candidate` |
| `C2_product_ablation_value` | `conditional_diagnostic_blocked` | false | false | 50 | 52 | `repair_candidate` |
| `C3_adaptive_window_increment` | `unsupported` | false | false | 44 | 46 | `diagnostic_lock_candidate` |
| `C4_menu_construction_value` | `conditional_diagnostic_blocked` | false | false | 56 | 58 | `rerun_candidate` |
| `C5_eta_robustness_boundary` | `diagnostic_only` | true | false | 20 | 21 | `diagnostic_lock_candidate` |
| `C6_exact_greedy_computational_credibility` | `blocked_diagnostic` | false | false | 18 | 20 | `rerun_candidate` |
| `C7_provenance_status_transparency` | `status_supported` | true | true | 74 | 74 | `already_safe_or_status_only` |
| `C8_semi_real_case_validation` | `scaffold_only_blocked` | false | false | 18 | 20 | `diagnostic_lock_candidate` |

Blocked claim ids in `PACKAGE_STATUS.json`: C1, C2, C3, C4, C6, and C8.
C5 is manuscript-allowed only as diagnostic boundary language, not
claim-ready robustness. C7 is claim-ready only as provenance/status
transparency.

## Source-Family Status Snapshot

| source_family | artifacts | existing | status | claim_ready | boundary |
| --- | ---: | ---: | --- | ---: | --- |
| `blocker_status` | 6 | 6 | `blocked` | false | Status documents are evidence about blockers, not performance evidence. |
| `main_rc` | 30 | 28 | `blocked` | false | Current package main RC artifacts are blocked by package-level formal/checkpoint causes. |
| `phase8_sensitivity` | 14 | 14 | `diagnostic_provisional_blocked` | false | Diagnostic sensitivity boundary only. |
| `phase9_tractability` | 12 | 12 | `diagnostic_provisional_blocked` | false | Diagnostic tractability boundary only. |
| `case_scaffold` | 12 | 10 | `scaffold_only_no_result_evidence` | false | Scaffold only; no validation evidence. |

## Canonical Causes

| cause_id | top_level_category | affected_claim_ids | source_family | representative_artifact_ids | raw_blocker_reason_examples | affected_artifact_count | evidence_boundary_refs | taxonomy_refs | recommended_next_action | requires_confirmation_from | do_not_repair_by_wording |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CF-001 | provenance/readiness | C1, C2, C4, C6, C7 | formal readiness; blocker_status | `FORMAL_READINESS.json`; `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md` | `dirty_git`; `claim_ready_allowed: false`; readiness `status: blocked` | 1 readiness gate plus 6 blocker/status docs | EB-002, EB-007, EB-008 | BT-001 | repair | Phase 14 | true |
| CF-002 | artifact-generation | C1, C2, C3, C4, C6 | main_rc | `main_rc:status:work2_coding_artifacts_work2_robust_menu_artifact_status_json`; `main_rc:claim_guard:work2_coding_artifacts_work2_robust_menu_manuscript_claim_guard_json` | `formal_skipped: Formal evidence was skipped for this Phase 4 run`; `missing_checkpoint_file: Required checkpoint file is unavailable` | 28 `formal_skipped` blockers and 28 `missing_checkpoint_file` blockers | EB-016, EB-018, EB-CONF-002 | BT-002 | repair | Phase 14 | true |
| CF-003 | metadata | C1, C2, C4, C7 | Phase 3/4 artifact status | `work2_coding/outputs/phase3_formal_artifacts/ARTIFACT_STATUS.json` | `pilot/formal rows require outside_option_util metadata`; `pilot/formal rows require valid method_family metadata` | exact row-level affected count unavailable from Phase 13 sources | EB-003, EB-008 | BT-001, BT-002 | repair | Phase 14 | true |
| CF-004 | artifact-schema | C1, C2, C3, C4, C6, C8 | package index/status | `PACKAGE_STATUS.json`; `PACKAGE_INDEX.json` | `source file missing`; `expected source pattern had no files`; `missing_artifact_count=4` | 4 missing artifacts; 4 source-missing blockers; 4 expected-pattern blockers | EB-016, EB-CONF-003 | BT-002 | repair | Phase 14 | true |
| CF-005 | empirical-performance | C1, C4 | Phase 4 formal diagnosis | `.planning/results/RC_FORMAL_DIAGNOSIS.md`; `.planning/results/RC_FORMAL_PAIRED_DIFFS.csv` | random menu has better mean net profit; adaptive loses to random on net profit in 3 of 5 paired splits | 5 paired formal splits; 1 central comparison family | EB-004, EB-006 | BT-003, BT-005 | rerun | Phase 15 then Phase 16 | true |
| CF-006 | adaptive-window | C3 | Phase 4 formal diagnosis; main_rc | `.planning/results/RC_FORMAL_DIAGNOSIS.md`; policy summary artifacts | adaptive and optimized fixed-window are identical across tracked metrics and all five splits | 5 paired formal splits; all tracked metrics in diagnosis | EB-005, EB-006 | BT-004 | diagnostic_lock | Phase 15 then Phase 16 | true |
| CF-007 | sensitivity-robustness | C2, C4, C5 | phase8_sensitivity | `phase8_sensitivity:status:work2_coding_artifacts_work2_robust_menu_phase8_sensitivity_artifact_status_json`; `SENSITIVITY_SUMMARY.md` | `diagnostic evidence only; not claim-ready`; `diagnostic_provisional_blocked`; `claim_ready=false` | 14 Phase 8 package artifacts; 50 completed sensitivity rows | EB-009, EB-010, EB-011 | BT-006 | diagnostic_lock | Phase 16 | true |
| CF-008 | computational-tractability | C4, C6 | phase9_tractability | `phase9_tractability:status:work2_coding_artifacts_work2_robust_menu_phase9_tractability_artifact_status_json`; `COMPUTATIONAL_TRACTABILITY_SUMMARY.md` | `diagnostic evidence only; not claim-ready`; `large_row_not_greedy`; `large_fallback_reason_missing`; gap/overlap unavailable | 12 Phase 9 package artifacts; 15 rows; 20 validation failures in artifact status | EB-012, EB-013, EB-014 | BT-007 | rerun | Phase 16 | true |
| CF-009 | semi-real-case | C8 | case_scaffold | `case_scaffold:case_scaffold_doc:planning_data_case_studies_readme_md`; `case_scaffold:case_scaffold_doc:planning_data_case_studies_validation_summary_md` | `case-study inputs are scaffold-only and cannot validate results`; no runtime case manifest; no case rows | 12 case-scaffold package artifacts; 2 missing scaffold patterns | EB-015, EB-019 | BT-008 | diagnostic_lock | Phase 16 | true |
| CF-010 | manuscript-language | C1, C2, C3, C4, C5, C6, C8 | strict claim guard; paper claim maps | `CLAIM_GUARD.json`; `.planning/paper/CLAIM_SAFE_LANGUAGE.md`; `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md` | forbidden language includes adaptive dominance, adaptive-window advantage, near-optimal greedy, no-filter recommendation, case-study validation, real passenger behavior | 8 claims; 6 blocked claim ids; C5 diagnostic only | EB-017, EB-020 | BT-009 | diagnostic_lock | Phase 16 and later manuscript-lock phases | true |
| CF-011 | provenance/readiness | C1, C2, C4, C5, C6, C7, C8 | blocker_status | `blocker_status:blocker_status:planning_results_rc_formal_diagnosis_md`; `blocker_status:blocker_status:planning_results_sensitivity_summary_md` | `blocker/status document only`; blocked-status artifact is not claim-ready | 6 blocker/status package artifacts | EB-018 | BT-001, BT-009 | diagnostic_lock | Phase 16 | true |
| CF-012 | manuscript-language | C7 | strict claim guard | `C7_provenance_status_transparency` in `CLAIM_GUARD.json` | C7 is `status_supported`, but safe language says it does not establish empirical effectiveness | 74 source artifacts are indexed for status transparency; no empirical upgrade follows | EB-020 | BT-001, BT-009 | diagnostic_lock | Phase 16 and later manuscript-lock phases | true |

## Separated Cause Groups

### Empirical-Performance Causes

- CF-005: The random-menu baseline currently outperforms adaptive on mean net
  profit and in 3 of 5 paired profit splits.
- CF-006: Adaptive and fixed-window variants are identical across tracked
  metrics in the selected formal diagnosis.

### Provenance And Readiness Causes

- CF-001: Formal readiness is blocked by `dirty_git`.
- CF-011: Blocker/status documents are transparent evidence about gate status,
  not claim-ready empirical evidence.
- CF-012: C7 status support does not upgrade empirical claims.

### Artifact-Generation, Artifact-Schema, And Metadata Causes

- CF-002: Current Phase 10 main RC package artifacts include package-level
  `formal_skipped` and `missing_checkpoint_file` blockers.
- CF-003: Prior formal artifact status reports missing `outside_option_util`
  and valid `method_family` metadata.
- CF-004: Phase 10 package inventory reports 4 missing artifacts and source
  pattern misses. No runtime/mirror hash conflict was observed.

### Sensitivity-Robustness Causes

- CF-007: Phase 8 remains diagnostic/provisional with `claim_ready=false`.
  Deferred sensitivity dimensions remain unavailable in current evidence.

### Computational-Tractability Causes

- CF-008: Phase 9 remains diagnostic/provisional because intended greedy
  fallback and exact-vs-greedy quality evidence were not established.

### Semi-Real-Case Causes

- CF-009: Semi-real case materials are scaffold-only. No external data,
  runtime case manifest, matrix, demand rows, replay rows, or case result
  artifacts exist as claim evidence.

### Manuscript-Language Causes

- CF-010: Strict claim guard and paper claim maps prohibit positive claims
  that current evidence does not support.
- CF-012: The only claim-ready item, C7, is status/provenance transparency
  only.

## Claim-Level Recommendations

| claim_id | phase13_classification | reason | recommended_next_action | requires_confirmation_from |
| --- | --- | --- | --- | --- |
| C1_central_adaptive_menu_superiority | `rerun_candidate` | Existing formal diagnosis is mixed and package gates are blocked; random menu outperforms adaptive on mean profit. | rerun | Phase 15 diagnosis and Phase 16 decision |
| C2_product_ablation_value | `repair_candidate` | Existing diagnosis has conditional ablation signals, but artifact/readiness/package causes block manuscript use. Source evidence is insufficient to say repair alone will make it claim-ready. | repair | Phase 14, with Phase 15/16 confirmation if performance interpretation changes |
| C3_adaptive_window_increment | `diagnostic_lock_candidate` | Existing tracked metrics show adaptive and fixed-window equality. This cannot be repaired by wording. | diagnostic_lock | Phase 15 and Phase 16 |
| C4_menu_construction_value | `rerun_candidate` | Mechanism diagnostics exist, but random-menu profit and package blockers prevent a strong value claim. | rerun | Phase 15 and Phase 16 |
| C5_eta_robustness_boundary | `diagnostic_lock_candidate` | Manuscript use is allowed only as diagnostic/no-filter boundary language; `claim_ready` is false. | diagnostic_lock | Phase 16 |
| C6_exact_greedy_computational_credibility | `rerun_candidate` | Phase 9 did not exercise greedy fallback or produce gap/overlap evidence. | rerun | Phase 16 |
| C7_provenance_status_transparency | `already_safe_or_status_only` | Supported only as provenance/status transparency. It is not effectiveness evidence. | diagnostic_lock | Phase 16 and later manuscript-lock phases |
| C8_semi_real_case_validation | `diagnostic_lock_candidate` | Case material is scaffold-only with no execution or validation evidence. | diagnostic_lock | Phase 16 |

## Unavailable Evidence Explicitly Marked

- Root cause of random-menu profit advantage is unavailable from Phase 13
  source reading alone. Phase 15 owns row and code-path diagnosis.
- Root cause of adaptive/fixed-window equality is unavailable from Phase 13
  source reading alone. Phase 15 owns row and code-path diagnosis.
- Whether missing `method_family` and `outside_option_util` are purely
  metadata/schema repair, builder repair, or evidence-row issues is
  unavailable from Phase 13 source reading alone. Phase 14 owns that
  classification.
- Whether a final rerun is legitimate is unavailable from Phase 13 source
  reading alone. Phase 16 owns the decision after Phase 14 and Phase 15.
- No Phase 13 source provides real passenger behavior, real acceptance,
  real opt-out, real profit, or executed semi-real case result evidence.

## Non-Authorization Note

The `recommended_next_action` values above are audit labels only. They do not
authorize repair, rerun, artifact regeneration, manuscript writing, generated
row edits, generated table or figure edits, or claim upgrades. Later phases
must confirm any action and regenerate strict claim-guard outputs before any
claim can be upgraded.
