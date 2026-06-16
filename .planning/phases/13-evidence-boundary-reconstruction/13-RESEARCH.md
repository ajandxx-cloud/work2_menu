---
phase: 13
phase_name: evidence-boundary-reconstruction
status: complete
research_type: local_repository_evidence
created: 2026-06-16T15:58:08+08:00
timezone: Asia/Shanghai
requirements:
  - EVID-01
  - EVID-02
  - EVID-03
  - EVID-04
---

# Phase 13 Research: Evidence Boundary Reconstruction

## RESEARCH COMPLETE

Phase 13 does not need external literature or ecosystem research. The
relevant research domain is the current repository's evidence chain:
planning state, result summaries, readiness/status outputs, frozen final
settings, generated Phase 10 package files, paper claim maps, and claim-safe
language docs.

## Sources Reviewed

Core planning and phase context:

- `AGENTS.md`
- `.planning/PROJECT.md`
- `.planning/REQUIREMENTS.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `.planning/research/SUMMARY.md`
- `.planning/phases/13-evidence-boundary-reconstruction/13-CONTEXT.md`

Prior evidence and package context:

- `.planning/results/PHASE3_FORMAL_EVIDENCE_HANDOFF.md`
- `.planning/results/RC_FORMAL_DIAGNOSIS.md`
- `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md`
- `.planning/results/FORMAL_FAILURE_DIAGNOSIS.md`
- `.planning/results/CALIBRATION_PROTOCOL.md`
- `.planning/results/FROZEN_FINAL_SETTINGS.md`
- `.planning/results/SENSITIVITY_SUMMARY.md`
- `.planning/results/COMPUTATIONAL_TRACTABILITY_SUMMARY.md`
- `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md`
- `.planning/paper/CLAIM_SAFE_LANGUAGE.md`
- `.planning/phases/08-sensitivity-and-robustness-experiments/08-CONTEXT.md`
- `.planning/phases/09-exact-versus-greedy-and-computational-tractability/09-CONTEXT.md`
- `.planning/phases/10-paper-artifact-generation/10-CONTEXT.md`
- `.planning/phases/10-paper-artifact-generation/10-VERIFICATION.md`

Phase 10 runtime-source and mirror package files:

- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_INDEX.json`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/SOURCE_INDEX.json`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/ARTIFACT_TO_SECTION_MAP.json`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`
- the matching files under `artifacts/work2_robust_menu/phase10_paper_artifacts/`

Runtime integration points and tests:

- `work2_coding/Src/paper_artifacts.py`
- `work2_coding/Src/manuscript_claims.py`
- `work2_coding/Src/artifact_status.py`
- `work2_coding/Src/artifact_builder.py`
- `work2_coding/scripts/test_phase10_paper_artifacts.py`
- `work2_coding/scripts/test_manuscript_claim_guard.py`

## Current Evidence Boundary

The current evidence package has two layers that Phase 13 must keep separate:

1. A completed comparable formal RC source run:
   `work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a`.
   It has 35 completed rows, 5 paired splits, 7 policies per split, and loaded
   checkpoint metadata. It is usable for diagnosis.
2. A Phase 10 paper artifact package under
   `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/` and a
   byte-matching root mirror under
   `artifacts/work2_robust_menu/phase10_paper_artifacts/`. It indexes 74
   source artifacts and writes strict claim boundaries, but keeps overall
   `claim_ready: false`.

Phase 13 should reconstruct this boundary without executing repairs,
regenerating artifacts, running final replay, or changing generated result
rows. The deliverables should make the distinction between "diagnostic source
evidence exists" and "claim-ready manuscript evidence is authorized" impossible
to miss.

## Phase 10 Package Facts

`PACKAGE_STATUS.json` reports:

- `schema_version: phase10-paper-artifact-package-v1`
- `artifact_count: 74`
- `existing_artifact_count: 70`
- `missing_artifact_count: 4`
- `blocker_count: 108`
- `claim_ready: false`
- `manuscript_positive_claims_allowed: false`
- blocked claim ids:
  - `C1_central_adaptive_menu_superiority`
  - `C2_product_ablation_value`
  - `C3_adaptive_window_increment`
  - `C4_menu_construction_value`
  - `C6_exact_greedy_computational_credibility`
  - `C8_semi_real_case_validation`

`PACKAGE_INDEX.json` uses an `entries` array rather than
`package_entries`; this is the actual current schema and should be treated as
package context, not as a conflict. The 74 entries group as:

| Source family | Entries | Status | Claim-ready |
| --- | ---: | --- | --- |
| `blocker_status` | 6 | `blocked` | false |
| `case_scaffold` | 12 | `scaffold_only_no_result_evidence` | false |
| `main_rc` | 30 | `blocked` | false |
| `phase8_sensitivity` | 14 | `diagnostic_provisional_blocked` | false |
| `phase9_tractability` | 12 | `diagnostic_provisional_blocked` | false |

Representative package blocker reasons are:

- `missing_checkpoint_file: Required checkpoint file is unavailable; refusing random-weight evidence.`
- `formal_skipped: Formal evidence was skipped for this Phase 4 run; formal claim readiness is false.`
- `diagnostic evidence only; not claim-ready`
- `case-study inputs are scaffold-only and cannot validate results`
- `blocker/status document only`
- `source file missing`
- `expected source pattern had no files`

Runtime-source package files and root-mirror package files currently have
matching SHA-256 hashes for every Phase 10 package file checked:
`ARTIFACT_TO_SECTION_MAP.json`, `artifact_to_section_map.md`,
`claim_checklist.md`, `CLAIM_GUARD.json`, `PACKAGE_INDEX.json`,
`PACKAGE_STATUS.json`, `README.md`, `safe_language_boundaries.md`, and
`SOURCE_INDEX.json`.

## Strict Claim Guard Facts

`CLAIM_GUARD.json` reports schema
`phase10-strict-claim-guard-v1`, eight claims, and overall
`claim_ready: false`.

| Claim id | Support status | Manuscript allowed | Claim-ready | Notes |
| --- | --- | ---: | ---: | --- |
| `C1_central_adaptive_menu_superiority` | `unsupported_blocked` | false | false | Blocks positive central superiority. |
| `C2_product_ablation_value` | `conditional_diagnostic_blocked` | false | false | Diagnostic ablation structure only. |
| `C3_adaptive_window_increment` | `unsupported` | false | false | No directional adaptive-window claim. |
| `C4_menu_construction_value` | `conditional_diagnostic_blocked` | false | false | Mechanism diagnostics only. |
| `C5_eta_robustness_boundary` | `diagnostic_only` | true | false | Diagnostic boundary language only. |
| `C6_exact_greedy_computational_credibility` | `blocked_diagnostic` | false | false | No near-optimal greedy or tractability upgrade. |
| `C7_provenance_status_transparency` | `status_supported` | true | true | Narrow status/provenance transparency only. |
| `C8_semi_real_case_validation` | `scaffold_only_blocked` | false | false | No case validation or real passenger behavior claim. |

The claim guard source code fixes these definitions in
`work2_coding/Src/manuscript_claims.py` and derives source artifacts and
source-level blockers from the Phase 10 package indexes.

## Scientific Boundary Facts

The selected formal RC rows support a diagnostic comparison but not a strong
central claim:

- `mainline_optimized_adaptive` improves several service metrics in the Phase 4
  diagnosis, but `mainline_random_menu` has better mean net profit and adaptive
  loses to random on net profit in 3 of 5 paired splits.
- `mainline_optimized_adaptive` and
  `mainline_optimized_fixed_window` are identical across tracked metrics in the
  selected formal run, blocking adaptive-window increment language.
- Phase 8 sensitivity is `diagnostic_provisional_blocked` and reports boundary
  behavior, not claim-ready robustness.
- Phase 9 tractability is `diagnostic_provisional_blocked`; the configured
  large candidate scales did not trigger greedy fallback, so exact-vs-greedy
  gap, overlap, near-optimality, and online tractability claims remain blocked.
- Phase 7 case material is scaffold-only and contains no executable case result
  evidence.

## Planning Implications

The most useful Phase 13 shape is one documentation plan with four execution
tasks:

1. Build `01_EVIDENCE_BOUNDARY.md` as a timeline narrative from Phase 3/4 to
   Phase 10, including a conflict matrix and source/mirror treatment.
2. Build `01_CLAIM_READY_FALSE_CAUSES.md` as an audit-table-first catalogue
   with `CF-*` ids, affected claims, package/source artifact ids, blocker
   reasons, canonical cause grouping, and recommended next action.
3. Build `01_BLOCKER_TAXONOMY.md` as an audit-table-first taxonomy using the
   nine exact roadmap categories and `BT-*` ids.
4. Cross-check all three deliverables for stable id links, forbidden actions,
   and claim-boundary language.

The phase should not create helper code unless an executor chooses a small
one-off parser for reading JSON. If helper parsing is used, it must read only
and should not edit generated package files.

## Validation Architecture

Phase 13 validation should be document and source-status validation:

- Verify all three required deliverables exist under
  `.planning/milestones/claim_ready_resolution/`.
- Verify stable id families `EB-*`, `CF-*`, and `BT-*` appear and cross-link
  across the three deliverables.
- Verify `01_BLOCKER_TAXONOMY.md` contains exactly the roadmap's nine top-level
  blocker classes:
  provenance/readiness, artifact-generation, empirical-performance,
  adaptive-window, random-baseline, sensitivity, tractability, semi-real-case,
  and manuscript-language.
- Verify `01_CLAIM_READY_FALSE_CAUSES.md` references all eight strict claim ids
  and all six currently blocked claim ids.
- Verify `01_EVIDENCE_BOUNDARY.md` includes the runtime/mirror hash-match
  finding or any conflict rows if a later executor finds drift.
- Verify no generated result rows, generated tables, generated figures, or
  generated Phase 10 package files are modified by the phase.
- Run the import smoke from the repository root:
  `python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"`

## Research Risks

- The package contains many duplicate blocker occurrences by artifact. The
  deliverables should merge repeated blocker reasons into canonical causes
  while preserving counts and representative artifact ids.
- Status artifacts are intentionally included as blockers/status documents.
  Phase 13 should not misread their presence as a failure to be removed.
- `C7_provenance_status_transparency` is `claim_ready: true`, but only for
  status/provenance transparency. It must not be rolled into empirical
  claim readiness.
- Phase 10 runtime-source and root mirror currently match; future drift should
  be recorded in the conflict matrix instead of silently resolved.

