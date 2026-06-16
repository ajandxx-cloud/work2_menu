# M1 Evidence Boundary Audit

**Phase:** 01 - Repository And Evidence Boundary Audit
**Created:** 2026-06-16
**Scope:** Read-only reconstruction of the current Work2 TR-E repository,
planning, manuscript, runtime, generated package, and strict claim-guard state.

## Scope

This audit records the current evidence boundary before any repair, final
replay, artifact regeneration, manuscript rewrite, or claim upgrade. It covers
the current planning files, codebase maps, runtime root, generated Phase 10
paper package, root mirror package, manuscript source, and dirty git state.

No experiments were run. No generated evidence was modified. No package
builder, artifact builder, checkpoint training, final replay, calibration, or
case-study execution command was run during this audit.

## Current Workspace Boundary

- Project root: `C:\Users\39583\Desktop\4_Publication\2.paper_2_menu optimization-7分_trE`.
- Active runtime root: `work2_coding/`.
- Legacy `ooh_code/` root: absent in the current filesystem. Existing
  `ooh_code/` references in older codebase maps are treated as stale until a
  future audit proves otherwise.
- Current project is a regenerated GSD planning project for Work2 robust
  time-window service menu optimization in many-to-one DRT.
- The current milestone is `v1.0` / TR-E Claim-Ready Manuscript Completion.

## Planning Boundary

The current planning boundary is defined by:

- `.planning/PROJECT.md`
- `.planning/REQUIREMENTS.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `.planning/research/SUMMARY.md`
- `.planning/codebase/ARCHITECTURE.md`
- `.planning/codebase/STRUCTURE.md`
- `.planning/codebase/CONCERNS.md`
- `.planning/codebase/CONVENTIONS.md`
- `.planning/codebase/INTEGRATIONS.md`
- `.planning/codebase/STACK.md`
- `.planning/codebase/TESTING.md`
- `.planning/phases/01-repository-and-evidence-boundary-audit/01-CONTEXT.md`
- `.planning/phases/01-repository-and-evidence-boundary-audit/01-RESEARCH.md`
- `.planning/phases/01-repository-and-evidence-boundary-audit/01-VALIDATION.md`

Current planning states that Phase 1 is a read-only audit. Phase 2 is reserved
for provenance/readiness cleanup planning without destructive changes. Phase 3
is reserved for deciding whether frozen final settings and calibration/final
test separation can justify a legitimate final replay.

## Runtime Boundary

The active runtime package lives under `work2_coding/`. The import smoke check
defined by the project is:

```powershell
python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"
```

Allowed Phase 1 runtime inspection is limited to import health and read-only
source/path inspection. Phase 1 does not run `run_study.py --execute`, suite
execution, checkpoint training, formal readiness repair, artifact generation,
package regeneration, calibration, final replay, or case-study execution.

Runtime guardrails confirmed for later phases:

- Preserve paired replay fairness across policy comparisons.
- Keep opt-out accounting separate from accepted home pickup.
- Keep checkpoint load status explicit in generated rows and metadata.
- Treat no-filter variants as diagnostic unless formal evidence supports a
  stronger use.
- Keep attention-based choice/scoring outside v1 manuscript scope.
- Do not hand-edit generated result rows or paper artifacts.

## Generated Evidence Boundary

The canonical generated paper artifact package is:

```text
work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/
```

The root package is a paper-facing mirror only:

```text
artifacts/work2_robust_menu/phase10_paper_artifacts/
```

Phase 1 checked only these four key JSON files for mirror drift:

- `CLAIM_GUARD.json`
- `PACKAGE_STATUS.json`
- `PACKAGE_INDEX.json`
- `ARTIFACT_TO_SECTION_MAP.json`

All four key mirror JSON files match the canonical files by SHA-256.

| JSON file | Mirror match | Use in Phase 1 |
| --- | --- | --- |
| `CLAIM_GUARD.json` | yes | Strict claim ceiling |
| `PACKAGE_STATUS.json` | yes | Package status and blocker counts |
| `PACKAGE_INDEX.json` | yes | 74-entry package traceability |
| `ARTIFACT_TO_SECTION_MAP.json` | yes | Manuscript section linkage |

No full generated JSON document is copied into this audit. The following
snapshot records only top-level fields, status summaries, and strict claim
status values.

## Phase 10 Package Snapshot

Canonical `PACKAGE_STATUS.json`:

| Field | Value |
| --- | --- |
| `schema_version` | `phase10-paper-artifact-package-v1` |
| `generated_at_utc` | `2026-06-16T05:48:47+00:00` |
| `claim_ready` | `false` |
| `strict_claim_guard_claim_ready` | `false` |
| `manuscript_positive_claims_allowed` | `false` |
| `artifact_count` | `74` |
| `existing_artifact_count` | `70` |
| `missing_artifact_count` | `4` |
| `blocker_count` | `108` |
| `claim_ready_reason` | Phase 10 package is a provenance and paper-artifact index; positive claims remain blocked unless strict guards allow them. |

Source-family status from `PACKAGE_STATUS.json`:

| Source family | Artifacts | Existing | Claim ready | Status |
| --- | ---: | ---: | --- | --- |
| `main_rc` | 30 | 28 | false | `blocked` |
| `phase8_sensitivity` | 14 | 14 | false | `diagnostic_provisional_blocked` |
| `phase9_tractability` | 12 | 12 | false | `diagnostic_provisional_blocked` |
| `case_scaffold` | 12 | 10 | false | `scaffold_only_no_result_evidence` |
| `blocker_status` | 6 | 6 | false | `blocked` |

Package-tier counts:

| Package tier | Count |
| --- | ---: |
| `main_paper_candidate` | 28 |
| `diagnostic_appendix` | 26 |
| `scaffold_only` | 12 |
| `blocked_status` | 8 |

Missing artifact IDs:

- `case_scaffold:case_scaffold_config:planning_data_case_studies_missing_yml`
- `case_scaffold:case_scaffold_contract:planning_data_case_studies_missing_json`
- `main_rc:figure:work2_coding_artifacts_work2_robust_menu_figures_missing_png`
- `main_rc:figure_metadata:work2_coding_artifacts_work2_robust_menu_figures_missing_metadata_json`

Canonical `CLAIM_GUARD.json`:

| Field | Value |
| --- | --- |
| `schema_version` | `phase10-strict-claim-guard-v1` |
| `generated_at_utc` | `2026-06-16T05:48:47+00:00` |
| `claim_ready` | `false` |
| `manuscript_positive_claims_allowed` | `false` |
| `source_package_index.artifact_count` | `74` |
| `source_package_index.package_claim_ready` | `false` |

Strict claim guard table:

| Claim ID | Support status | Claim ready | Manuscript allowed | Current use |
| --- | --- | --- | --- | --- |
| `C1_central_adaptive_menu_superiority` | `unsupported_blocked` | false | false | Not allowed |
| `C2_product_ablation_value` | `conditional_diagnostic_blocked` | false | false | Diagnostic structure only, no positive claim |
| `C3_adaptive_window_increment` | `unsupported` | false | false | Not allowed |
| `C4_menu_construction_value` | `conditional_diagnostic_blocked` | false | false | Diagnostic mechanism only |
| `C5_eta_robustness_boundary` | `diagnostic_only` | false | true | Diagnostic boundary only |
| `C6_exact_greedy_computational_credibility` | `blocked_diagnostic` | false | false | Diagnostic computational boundary only |
| `C7_provenance_status_transparency` | `status_supported` | true | true | Provenance/status transparency only |
| `C8_semi_real_case_validation` | `scaffold_only_blocked` | false | false | Not allowed |

Blocked claim IDs in package status:

- `C1_central_adaptive_menu_superiority`
- `C2_product_ablation_value`
- `C3_adaptive_window_increment`
- `C4_menu_construction_value`
- `C6_exact_greedy_computational_credibility`
- `C8_semi_real_case_validation`

`ARTIFACT_TO_SECTION_MAP.json` uses schema
`phase10-paper-artifact-package-v1` and contains 8 manuscript sections with
260 section-artifact links:

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

## Manuscript Boundary

Manuscript files inspected read-only:

- `manuscript/main.tex`
- `manuscript/references.bib`
- `.planning/paper/CLAIM_SAFE_LANGUAGE.md`
- `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md`
- `.planning/paper/TR_E_MANUSCRIPT_STRUCTURE.md`
- `.planning/paper/TR_E_RESEARCH_DESIGN.md`

`manuscript/main.tex` is present. Phase 1 did not edit the manuscript or
bibliography. Manuscript rewriting is deferred to later phases after the
evidence path is selected.

## Manuscript Claim-Language Boundary

The current safe-language authority is `.planning/paper/CLAIM_SAFE_LANGUAGE.md`.
It permits terms such as formulate, evaluate, diagnose, audit, identify
boundary conditions, claim-gated evidence, and diagnostic evidence. It forbids
unguarded wording such as dominate, outperform, superior, near-optimal,
adaptive windows improve, case-study validation, and real passenger behavior
unless the strict claim guard authorizes the exact claim.

Read-only phrase scan of `manuscript/main.tex` found these line references:

| Line | Phrase | Short context | Boundary interpretation |
| ---: | --- | --- | --- |
| 54 | dominance | Empirical dominance claims remain blocked until gates pass. | Currently framed as blocked, acceptable as a warning. |
| 69 | improve | Meeting points can reduce routing cost and improve vehicle productivity. | Literature/background wording; later manuscript phase should keep this distinct from Work2 empirical claims. |
| 101 | dominates | Draft says it does not claim `DSPO_PLUS` already dominates baselines. | Currently framed as prohibited/blocked. |
| 112 | improve | Literature claim that meeting points can improve pooling efficiency. | Literature/background wording; needs source-bounded phrasing. |
| 253 | claim-ready | Current artifacts are not claim-ready. | Correct claim-gate statement. |
| 256 | dominance | Results describe planned families rather than empirical dominance claims. | Currently framed as blocked. |
| 285 | dominance | Policy dominance remains to be verified. | Correct conditional wording. |
| 313 | improve | Acceptance probability can improve only after the evidence ladder passes. | Editorial risk language, not evidence claim. |

No `superior`, `outperform`, `near-optimal`, `adaptive window`, `adaptive menu`,
`case-study validation`, or `real passenger behavior` matches were found in the
current manuscript source during this scan.

## Dirty Git Boundary

Read-only `git status --short --branch` during execution reported:

```text
## main...origin/main [ahead 13]
142 changed paths total
10 modified paths
132 deleted paths
0 untracked paths
```

The dirty boundary includes regenerated planning files and deleted legacy
planning/results files. The deleted legacy planning/results files are recorded
as a provenance risk, not as an automatic blocker for Phase 1, because current
evidence is based on present generated packages and current workspace files.
Phase 1 did not restore, revert, stash, delete, or normalize unrelated user
changes.

Representative dirty categories:

- Modified regenerated planning core: `.planning/PROJECT.md`,
  `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, `.planning/STATE.md`,
  `.planning/config.json`, `.planning/research/SUMMARY.md`.
- Modified paper boundary docs: `.planning/paper/CLAIM_SAFE_LANGUAGE.md`,
  `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md`,
  `.planning/paper/TR_E_MANUSCRIPT_STRUCTURE.md`,
  `.planning/paper/TR_E_RESEARCH_DESIGN.md`.
- Deleted legacy planning and results material under older milestone and phase
  directories, including `.planning/STATE_LOCK.md`, older
  `.planning/phases/*`, and older `.planning/results/*`.

## No-Modification Statement

No experiments were run. No generated evidence was modified. No generated rows,
package status, claim guard, figure, table, artifact package, manuscript source,
or bibliography file was hand-edited by Phase 1 execution.

Phase 1 only creates planning audit deliverables under:

```text
.planning/milestones/tr_e_completion/
```

The current generated package is not claim-ready. The evidence boundary leans
diagnostic-only from current files, while Phase 2 and Phase 3 must still decide
whether clean provenance and frozen final settings can support a legitimate
final replay without tuning on final outputs.
