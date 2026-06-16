# Phase 1: Repository And Evidence Boundary Audit - Research

**Researched:** 2026-06-16
**Status:** Complete
**Mode:** Inline research, because GSD subagent spawning is not available in this runtime.

## Research Question

What does the planner need to know to plan Phase 1 well?

Phase 1 is a read-only evidence-boundary audit. It must reconstruct the current
workspace, planning, manuscript, runtime, artifact, and claim-guard state before
any repair, replay, artifact regeneration, or manuscript claim upgrade.

## Current Boundary Facts

### Active Runtime And Planning Root

- Active runtime root: `work2_coding/`.
- Repository instructions explicitly prefer `work2_coding/` and treat `ooh_code/`
  references as stale until verified.
- The minimum runtime verification remains:
  `python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"`
  from repository root, or the equivalent import from `work2_coding/`.
- Phase 1 has existing context at
  `.planning/phases/01-repository-and-evidence-boundary-audit/01-CONTEXT.md`.
- No Phase 1 `PLAN.md` existed before this planning run.

### Git State Boundary

The worktree is dirty before Phase 1 planning. A read-only `git status` summary
showed:

- `M`: 9 modified files.
- `D`: 132 deleted files.

This dirty state is evidence-boundary material, not something Phase 1 should
repair. Phase 1 should record it without reverting, restoring, stashing, or
deleting unrelated user changes.

### Canonical Paper Artifact Package

Canonical package:

- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/`

Root mirror:

- `artifacts/work2_robust_menu/phase10_paper_artifacts/`

The four key JSON files exist in both locations and match by SHA-256:

| File | Mirror match |
| --- | --- |
| `CLAIM_GUARD.json` | yes |
| `PACKAGE_STATUS.json` | yes |
| `PACKAGE_INDEX.json` | yes |
| `ARTIFACT_TO_SECTION_MAP.json` | yes |

The canonical `PACKAGE_STATUS.json` reports:

| Field | Value |
| --- | --- |
| `schema_version` | `phase10-paper-artifact-package-v1` |
| `claim_ready` | `false` |
| `strict_claim_guard_claim_ready` | `false` |
| `artifact_count` | `74` |
| `existing_artifact_count` | `70` |
| `missing_artifact_count` | `4` |
| `blocker_count` | `108` |

The package reason states that Phase 10 is a provenance and paper-artifact
index and that positive claims remain blocked unless strict guards allow them.

### Artifact Family Status

`PACKAGE_STATUS.json` and `PACKAGE_INDEX.json` agree on the 74 artifact entries:

| Source family | Artifacts | Existing | Status |
| --- | ---: | ---: | --- |
| `main_rc` | 30 | 28 | `blocked` |
| `phase8_sensitivity` | 14 | 14 | `diagnostic_provisional_blocked` |
| `phase9_tractability` | 12 | 12 | `diagnostic_provisional_blocked` |
| `case_scaffold` | 12 | 10 | `scaffold_only_no_result_evidence` |
| `blocker_status` | 6 | 6 | `blocked` |

Package tier counts:

| Package tier | Count |
| --- | ---: |
| `main_paper_candidate` | 28 |
| `diagnostic_appendix` | 26 |
| `scaffold_only` | 12 |
| `blocked_status` | 8 |

The four missing entries are:

- `case_scaffold:case_scaffold_config:planning_data_case_studies_missing_yml`
- `case_scaffold:case_scaffold_contract:planning_data_case_studies_missing_json`
- `main_rc:figure:work2_coding_artifacts_work2_robust_menu_figures_missing_png`
- `main_rc:figure_metadata:work2_coding_artifacts_work2_robust_menu_figures_missing_metadata_json`

### Strict Claim Guard Status

`CLAIM_GUARD.json` uses schema `phase10-strict-claim-guard-v1` and reports
`claim_ready=false`.

| Claim ID | Support status | Claim ready | Manuscript allowed |
| --- | --- | --- | --- |
| `C1_central_adaptive_menu_superiority` | `unsupported_blocked` | false | false |
| `C2_product_ablation_value` | `conditional_diagnostic_blocked` | false | false |
| `C3_adaptive_window_increment` | `unsupported` | false | false |
| `C4_menu_construction_value` | `conditional_diagnostic_blocked` | false | false |
| `C5_eta_robustness_boundary` | `diagnostic_only` | false | true |
| `C6_exact_greedy_computational_credibility` | `blocked_diagnostic` | false | false |
| `C7_provenance_status_transparency` | `status_supported` | true | true |
| `C8_semi_real_case_validation` | `scaffold_only_blocked` | false | false |

Blocked claim IDs in `PACKAGE_STATUS.json`:

- `C1_central_adaptive_menu_superiority`
- `C2_product_ablation_value`
- `C3_adaptive_window_increment`
- `C4_menu_construction_value`
- `C6_exact_greedy_computational_credibility`
- `C8_semi_real_case_validation`

The only strict claim that is ready is provenance/status transparency. That is
not an empirical effectiveness claim.

### Artifact-To-Section Map

`ARTIFACT_TO_SECTION_MAP.json` has 8 manuscript sections and 260 section-artifact
links.

| Section | Artifact links |
| --- | ---: |
| `provenance_and_claim_gates` | 74 |
| `eta_time_window_robustness` | 44 |
| `product_time_window_ablation` | 44 |
| `experimental_design` | 30 |
| `main_rc_results` | 30 |
| `sensitivity_appendix` | 14 |
| `computational_performance_appendix` | 12 |
| `case_scaffold_appendix` | 12 |

This makes provenance/status the only fully cross-cutting safe section. Results,
sensitivity, tractability, and case-study sections need claim-boundary language.

## Blocker Taxonomy For Planning

The Phase 1 blocker list should keep the six classes from `01-CONTEXT.md`:

1. Provenance/readiness.
2. Empirical performance.
3. Artifact packaging.
4. Manuscript language.
5. Case-study.
6. Computational tractability.

The generated `PACKAGE_STATUS.json` blocker list is not already labeled with
those six classes. The executor should classify from source family, status,
artifact id, and blocker reason, then add short human explanations. The matrix
must remain traceable back to the 74 artifacts and 8 strict claims.

Important classification guidance:

- `main_rc` with `blocked` status contributes to provenance/readiness,
  empirical-performance, artifact-packaging, and manuscript-language risk.
- `phase8_sensitivity` contributes diagnostic ETA/robustness boundary material,
  but not operational no-filter recommendations.
- `phase9_tractability` contributes computational diagnostic material, but not
  exact/greedy credibility claims.
- `case_scaffold` contributes future-study/scaffold context only, not semi-real
  validation or real passenger behavior.
- `blocker_status` artifacts are provenance/status transparency evidence, not
  empirical-performance support.

## Manuscript Wording Risk

`manuscript/main.tex` is present. Read-only phrase search found terms that must
be inspected in context during execution:

- `dominates`
- `improve`
- `adaptive window`
- `adaptive menu`
- `claim-ready`

Some instances may already be framed as prohibited or conditional language, so
Phase 1 should not edit the manuscript. It should only record wording-risk
locations for later manuscript phases.

The active safe-language boundary is `.planning/paper/CLAIM_SAFE_LANGUAGE.md`.
It forbids unguarded positive wording such as "dominate", "outperform",
"superior", "near-optimal", "adaptive windows improve", "case-study
validation", and "real passenger behavior" unless the strict claim guard
authorizes the exact claim.

## Planning Implications

Phase 1 should produce one audit plan with three milestone deliverables:

- `.planning/milestones/tr_e_completion/M1_EVIDENCE_BOUNDARY_AUDIT.md`
- `.planning/milestones/tr_e_completion/M1_BLOCKER_LIST.md`
- `.planning/milestones/tr_e_completion/M1_DECISION.md`

The plan should:

- Stay read-only with respect to generated rows and artifact packages.
- Use small parsing helpers or shell/PowerShell/Node one-liners only for
  summarization, not regeneration.
- Record exact paths and key fields instead of copying entire JSON files.
- Preserve the conditional conclusion: current evidence is not claim-ready and
  leans diagnostic, while Phase 2 and Phase 3 still decide whether a legitimate
  final replay path exists.
- Verify with the import smoke command only. Do not run `run_study.py`,
  artifact builders, package builders, checkpoint training, calibration, final
  replay, or case-study execution.

## Validation Architecture

Phase 1 validation is audit-oriented, not experiment-oriented.

Recommended validation checks:

1. Runtime smoke import from repository root:
   `python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"`
2. File existence checks for the three milestone deliverables.
3. Source assertions in the deliverables:
   - `M1_EVIDENCE_BOUNDARY_AUDIT.md` records the four key JSON files and mirror
     match status.
   - `M1_BLOCKER_LIST.md` contains the six blocker classes and references all
     74 artifact entries plus all 8 claim IDs.
   - `M1_DECISION.md` states the conditional current decision and routes Phase
     2/3 without authorizing experiments.
4. Git diff check confirming no generated evidence files were modified by the
   phase.

Manual review remains useful for the scientific judgment in `M1_DECISION.md`,
but the core audit artifacts can be checked by source assertions and read-only
commands.

## Research Complete

Research found no reason to expand Phase 1 beyond a read-only audit. The plan
should be a single Wave 1 execution plan with explicit no-experiment and
no-generated-evidence constraints.
