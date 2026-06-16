---
phase: 13
status: evidence_boundary_reconstructed
claim_ready: false
generated_at: 2026-06-16T17:41:12+08:00
timezone: Asia/Shanghai
sources:
  - .planning/PROJECT.md
  - .planning/REQUIREMENTS.md
  - .planning/ROADMAP.md
  - .planning/STATE.md
  - .planning/results/PHASE3_FORMAL_EVIDENCE_HANDOFF.md
  - .planning/results/RC_FORMAL_DIAGNOSIS.md
  - .planning/results/FORMAL_BLOCKER_DIAGNOSIS.md
  - .planning/results/FORMAL_FAILURE_DIAGNOSIS.md
  - .planning/results/CALIBRATION_PROTOCOL.md
  - .planning/results/FROZEN_FINAL_SETTINGS.md
  - .planning/results/SENSITIVITY_SUMMARY.md
  - .planning/results/COMPUTATIONAL_TRACTABILITY_SUMMARY.md
  - work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/
  - artifacts/work2_robust_menu/phase10_paper_artifacts/
---

# Evidence Boundary Reconstruction

## Executive Boundary

Phase 13 reconstructs the current evidence boundary only. It does not repair
readiness gates, regenerate artifacts, rerun experiments, tune parameters,
edit generated rows, write manuscript claims, or select a downstream path.

The current repository has completed diagnostic source evidence, but it does
not have paper-facing positive empirical claim authority. The selected Phase
3/4 formal RC run is complete and comparable for diagnosis: 35 completed rows,
5 paired splits, 7 mainline policy tags, loaded checkpoint status, no failed
rows, and no placeholder-only rows. That evidence can support diagnostic
interpretation of profit-service trade-offs.

The Phase 10 paper artifact package remains the binding manuscript claim
boundary. Runtime package file:
`work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`.
It uses schema `phase10-strict-claim-guard-v1`, contains 8 claims, and keeps
overall `claim_ready=false`. Phase 10 `CLAIM_GUARD.json` remains binding
unless later phases regenerate the package through the pipeline and pass a
strict claim guard. No Phase 13 wording can override that guard.

## Evidence Classes

| class | current evidence | claim use now | refs |
| --- | --- | --- | --- |
| Claim-ready evidence | C7 provenance/status transparency only. The strict guard marks C7 `status_supported`, `manuscript_allowed=true`, and `claim_ready=true`. | Status/provenance transparency only; not effectiveness evidence. | EB-020, CF-012, BT-009 |
| Diagnostic/provisional evidence | Phase 3/4 formal rows, Phase 8 sensitivity, Phase 9 tractability, and blocked main RC artifacts. | Diagnostic boundary analysis, blocker transparency, limitations, and future-work framing. | EB-001..EB-018 |
| Scaffold-only evidence | Phase 7 semi-real case contracts and Phase 10 case-scaffold package entries. | Future-study scaffold only; no validation or real passenger behavior claims. | EB-015, EB-019, CF-009, BT-008 |
| Unsupported claims | Central adaptive-menu superiority, adaptive-window increment, near-optimal greedy or online tractability, semi-real validation, and any operational no-filter recommendation. | Must not appear as positive manuscript claims. | EB-012, EB-016, EB-020, CF-005..CF-010 |

## Timeline

### Phase 3/4

- EB-001: Phase 3 selected
  `work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a`
  as the source run for Phase 4 diagnosis. It has `35` completed rows,
  `5` paired splits, `7` policies per split, uptake regimes `low` and
  `medium`, checkpoint status `loaded`, `0` failed rows, and
  placeholder-only `false`. This is diagnostic source evidence, not
  claim-ready evidence. See CF-001 and BT-001.
- EB-002: Formal readiness for the source evidence is blocked by
  `dirty_git`; readiness reports `claim_ready_allowed=false`. Dirty worktree
  cleanup was explicitly not automated. See CF-001 and BT-001.
- EB-003: Phase 3 artifact status is blocked because pilot/formal rows require
  `outside_option_util` metadata and valid `method_family` metadata. These
  are artifact/metadata blockers, not permission to edit rows by hand. See
  CF-003 and BT-002.
- EB-004: Phase 4 diagnosis found that `mainline_optimized_adaptive` improves
  several service metrics relative to most baselines, but does not dominate
  profit-side metrics. `mainline_random_menu` has better mean net profit
  (`-176651.519334`) than `mainline_optimized_adaptive` (`-180581.747301`),
  and adaptive loses to random on net profit in 3 of 5 paired splits. See
  CF-005, BT-003, and BT-005.
- EB-005: Phase 4 diagnosis found that
  `mainline_optimized_adaptive` and
  `mainline_optimized_fixed_window` are identical across tracked metrics and
  all five paired splits. This blocks the current adaptive-window increment
  claim. See CF-006 and BT-004.
- EB-006: Phase 4 classifies the central superiority story as unsupported as
  a strong claim and, at most, conditional diagnostic under current evidence.
  It allows diagnostic/status tables only while gates remain blocked. See
  CF-005, CF-010, and BT-009.

### Phase 5

- EB-007: `CALIBRATION_PROTOCOL.md` locks allowed and prohibited calibration
  behavior. The selected formal result is non-tuning input and cannot be used
  to select parameters, remove unfavorable cases, or upgrade manuscript
  claims. See BT-003 and BT-009.
- EB-008: `FROZEN_FINAL_SETTINGS.md` records `final_status:
  blocked_pending_gate_cleanup`. It preserves the seven policy tags and
  pre-run final settings, but final replay is not authorized while dirty-git,
  artifact metadata, checkpoint sidecar/hash, readiness, and claim-guard gates
  remain unresolved. See CF-001, CF-003, and BT-001.

### Phase 8

- EB-009: Phase 8 generated 50 completed sensitivity rows over the must-have
  axes `menu_k`, ETA filter mode, uptake regime, and guardrail. Baseline
  validation passed. See CF-007 and BT-006.
- EB-010: Phase 8 status remains `diagnostic_provisional_blocked` with
  `claim_ready=false`. Its generated artifacts are boundary diagnostics only;
  no abstract, conclusion, or managerial claim upgrade is authorized. See
  CF-007 and BT-006.
- EB-011: Deferred Phase 8 dimensions remain `max_candidates`,
  `fleet_capacity_stress`, `pricing_bounds`, and `price_sensitivity`. Current
  evidence therefore cannot be used as full robustness coverage. See CF-007
  and BT-006.

### Phase 9

- EB-012: Phase 9 generated 15 completed diagnostic tractability rows and
  tractability artifacts. Status remains `diagnostic_provisional_blocked` with
  `claim_ready=false`. See CF-008 and BT-007.
- EB-013: The intended exact-vs-greedy comparison was not established. The
  configured large rows at solver scale values 12 and 16 still used effective
  solver `exact`, and relative gap plus menu overlap fields are unavailable.
  See CF-008 and BT-007.
- EB-014: Phase 9 validation records repeated `large_row_not_greedy` and
  `large_fallback_reason_missing` failures for completed large-scale rows.
  Current evidence can report candidate counts, enumerated menu counts, and
  build times, but not near-optimal greedy, greedy quality, or online
  tractability. See CF-008 and BT-007.

### Phase 10

- EB-015: Phase 10 generated mirrored paper artifact packages under both
  `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/` and
  `artifacts/work2_robust_menu/phase10_paper_artifacts/`. The package indexes
  74 source artifacts: 6 blocker/status, 30 main RC, 14 Phase 8 sensitivity,
  12 Phase 9 tractability, and 12 case scaffold artifacts. See CF-010 and
  BT-009.
- EB-016: `PACKAGE_STATUS.json` reports `artifact_count=74`,
  `existing_artifact_count=70`, `missing_artifact_count=4`,
  `blocker_count=108`, `claim_ready=false`, and
  `manuscript_positive_claims_allowed=false`. See CF-002, CF-004, and BT-002.
- EB-017: `PACKAGE_STATUS.json` lists blocked claim ids:
  `C1_central_adaptive_menu_superiority`,
  `C2_product_ablation_value`,
  `C3_adaptive_window_increment`,
  `C4_menu_construction_value`,
  `C6_exact_greedy_computational_credibility`, and
  `C8_semi_real_case_validation`. See CF-010 and BT-009.
- EB-018: Phase 10 package source family status keeps every source family
  `claim_ready=false`: `main_rc` is blocked, Phase 8 and Phase 9 are
  `diagnostic_provisional_blocked`, case material is
  `scaffold_only_no_result_evidence`, and blocker/status documents are
  blocked status material. See CF-002, CF-007, CF-008, CF-009, and CF-011.
- EB-019: Semi-real case material remains scaffold-only. Phase 7 verification
  records no runtime case YAML, no external data download, no road graph, no
  matrix, no demand rows, no replay output, no result artifacts, and no
  manuscript claim upgrade. See CF-009 and BT-008.
- EB-020: Strict `CLAIM_GUARD.json` contains eight claims. C1, C2, C3, C4,
  C6, and C8 block positive manuscript use; C5 is diagnostic-only; C7 is
  status/provenance supported only. See CF-010, CF-012, and BT-009.

## Runtime Source And Mirror Check

Runtime source is
`work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/`.
The root mirror is
`artifacts/work2_robust_menu/phase10_paper_artifacts/`.

| file | sha256 runtime | sha256 mirror | match |
| --- | --- | --- | --- |
| `CLAIM_GUARD.json` | `4030dddfcf967d420d83bf6870cd78e00d93d47e22a8705f12f24cf5a385113c` | `4030dddfcf967d420d83bf6870cd78e00d93d47e22a8705f12f24cf5a385113c` | yes |
| `PACKAGE_STATUS.json` | `002f3a98ab23bad4f27b4abeefa9f01d262e261098a9b1782f4d957b9b7625be` | `002f3a98ab23bad4f27b4abeefa9f01d262e261098a9b1782f4d957b9b7625be` | yes |
| `PACKAGE_INDEX.json` | `9bf3561617a287ee75d08da2addc6c88c5eaf3855e8bcc7e362163379165ffae` | `9bf3561617a287ee75d08da2addc6c88c5eaf3855e8bcc7e362163379165ffae` | yes |
| `SOURCE_INDEX.json` | `30472202ce569e823bbfd133de368158d72e175a6d57f0a9ec5464da6f6e1084` | `30472202ce569e823bbfd133de368158d72e175a6d57f0a9ec5464da6f6e1084` | yes |
| `ARTIFACT_TO_SECTION_MAP.json` | `f9092a4994728122596d5d14b5e470b8904e6927ca016728cc7ba00350d56d7b` | `f9092a4994728122596d5d14b5e470b8904e6927ca016728cc7ba00350d56d7b` | yes |
| `claim_checklist.md` | `a2c71849224eb8720e00b5724d9d20f41fd377313b9eaca6aa7b98b6bba01112` | `a2c71849224eb8720e00b5724d9d20f41fd377313b9eaca6aa7b98b6bba01112` | yes |
| `safe_language_boundaries.md` | `28b5fbc963f03bf2863514b34ca542fd9138a96208152317d5e114e3a341abbd` | `28b5fbc963f03bf2863514b34ca542fd9138a96208152317d5e114e3a341abbd` | yes |
| `README.md` | `e4b2a0c6d037ad402f5db5c48c392a5c1198910e3a71fb80d2b5004efebddb95` | `e4b2a0c6d037ad402f5db5c48c392a5c1198910e3a71fb80d2b5004efebddb95` | yes |
| `artifact_to_section_map.md` | `bbdf9aec20a1f3d8d96e6548e397914b91a4964b714ad2148bda8f89a1e647fe` | `bbdf9aec20a1f3d8d96e6548e397914b91a4964b714ad2148bda8f89a1e647fe` | yes |

Boundary result: no runtime/mirror hash conflict was observed for checked
Phase 10 package files. This lets Phase 13 cite the runtime source and root
mirror as byte-consistent copies. It does not upgrade any claim.

## Conflict Matrix

| conflict_id | source_a | source_b | field_or_wording | affected_claim_or_blocker | phase13_treatment | downstream_owner |
| --- | --- | --- | --- | --- | --- | --- |
| EB-CONF-001 | Runtime Phase 10 package | Root Phase 10 mirror | Package file hashes | Phase 10 package authority | `no_runtime_mirror_hash_conflict_observed`; merge the evidence record for checked files while preserving source/mirror paths | Phase 13 record only |
| EB-CONF-002 | Phase 3/4 selected formal run and diagnosis | Current Phase 10 `main_rc` package source family | Completed formal source rows versus current package blockers `formal_skipped` and `missing_checkpoint_file` | C1, C2, C3, C4, C6; CF-002, CF-003 | Keep both facts: completed rows are diagnostic source evidence; strict Phase 10 package remains binding for manuscript claims | Phase 14 for gate/artifact repair plan; Phase 15 for source-row/code-path diagnosis |
| EB-CONF-003 | Phase 13 planning expectation | Runtime `PACKAGE_INDEX.json` | Package index uses `entries`; no `package_entries` key is present | Artifact-schema consumers, not empirical claims | Treat `entries` as the actual current schema; no claim-ready cause is inferred from this alone | Phase 14 if schema consumers need repair |
| EB-CONF-004 | `.planning/final/TR_E_READINESS_REVIEW.md` | Phase 13 scope | Final review recommends conditional/diagnostic drafting, but Phase 13 is not a path-decision phase | Manuscript path decision | Treat as source context only; Phase 13 records evidence boundary and does not select any path | Phase 16 |

## Evidence Boundary Conclusions

Allowed current use:

- Use the selected 35-row formal run for diagnostic analysis of profit,
  service quality, opt-out, home service, meeting-point uptake, and split-level
  paired directions.
- Use Phase 8 as diagnostic/provisional sensitivity boundary evidence with
  `claim_ready=false`.
- Use Phase 9 as diagnostic/provisional computational evidence with
  `claim_ready=false`, explicitly noting that greedy fallback quality was not
  established.
- Use Phase 10 package artifacts to disclose source paths, artifact tiers,
  blocker counts, claim ids, and strict claim-safe language.
- Use C7 only for provenance/status transparency, not effectiveness.

Prohibited current use:

- Do not claim adaptive menu superiority, universal dominance, or claim-ready
  central performance.
- Do not claim adaptive-window increment while adaptive and fixed-window rows
  remain identical across tracked metrics.
- Do not claim product ablation value, menu-construction value, near-optimal
  greedy behavior, online tractability, case validation, or real passenger
  behavior.
- Do not treat no-filter or ETA diagnostics as operational recommendations.
- Do not hand-edit generated rows, tables, figures, package status, or claim
  guards to change evidence.
- Do not run repair, rerun, artifact regeneration, manuscript writing, or path
  selection in Phase 13.

Downstream ownership:

- Phase 14 owns gate, provenance, metadata, and artifact-schema repair
  planning without result manipulation.
- Phase 15 owns diagnosis of random-menu profit advantage and adaptive/fixed
  equality using source rows and code paths.
- Phase 16 owns the path decision.
- Later execution phases may regenerate claim artifacts only if explicitly
  authorized, and only regenerated strict claim-guard output can upgrade
  claims.

## Verification Notes

Commands run from the repository root unless noted:

| command | result |
| --- | --- |
| `Test-Path .planning\milestones\claim_ready_resolution\01_EVIDENCE_BOUNDARY.md` | passed |
| `Test-Path .planning\milestones\claim_ready_resolution\01_CLAIM_READY_FALSE_CAUSES.md` | passed |
| `Test-Path .planning\milestones\claim_ready_resolution\01_BLOCKER_TAXONOMY.md` | passed |
| `Test-Path .planning\phases\13-evidence-boundary-reconstruction\13-RESULT_MANIFEST.md` | passed |
| `Select-String` checks for EB/CF/BT ids, all eight strict claim ids, the nine taxonomy classes, `CLAIM_GUARD.json`, and `PACKAGE_STATUS.json` | passed |
| `cd work2_coding; python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` | passed: `IMPORT_OK` |
| `cd work2_coding; python scripts/test_phase10_paper_artifacts.py` | passed: `PASS: 3 Phase 10 paper artifact package tests` |
| `cd work2_coding; python scripts/test_manuscript_claim_guard.py` | passed: `PASS: 5 manuscript claim guard tests` |
| `git status --short -- .planning/milestones/claim_ready_resolution .planning/phases/13-evidence-boundary-reconstruction work2_coding/artifacts artifacts work2_coding/outputs` | only the new Phase 13 documentation files were untracked; generated artifact roots were not modified |
| `rg -n "Path A|Path B|Path C" .planning\milestones\claim_ready_resolution .planning\phases\13-evidence-boundary-reconstruction\13-RESULT_MANIFEST.md` | passed: no matches |
| `git diff --cached --check -- .planning/milestones/claim_ready_resolution/01_EVIDENCE_BOUNDARY.md .planning/milestones/claim_ready_resolution/01_CLAIM_READY_FALSE_CAUSES.md .planning/milestones/claim_ready_resolution/01_BLOCKER_TAXONOMY.md .planning/phases/13-evidence-boundary-reconstruction/13-RESULT_MANIFEST.md` | passed: no whitespace findings |
