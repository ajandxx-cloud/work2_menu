---
phase: 10
phase_name: Paper Artifact Generation
status: complete
generated: 2026-06-16T12:20:00+08:00
timezone: Asia/Shanghai
research_mode: inline
requirements:
  - ART-01
  - ART-02
runtime_root: work2_coding/
claim_ready_assumption: false
---

# Phase 10 Research: Paper Artifact Generation

## Research Complete

Phase 10 should assemble and guard the paper-facing artifact bundle. It should
not run new experiments, rerun final/formal evidence, fetch case-study data,
edit generated rows, write manuscript body text, or upgrade abstract/conclusion
claims.

The safest implementation path is a thin Phase 10 orchestration layer that
reuses the existing artifact builders and writes a machine-readable package
index over their outputs:

- main RC artifact bundle from `work2_coding/Src/artifact_builder.py`
- manuscript-frame and claim guard logic from
  `work2_coding/Src/manuscript_claims.py`
- Phase 8 diagnostic appendix artifacts from
  `work2_coding/Src/sensitivity_analysis.py`
- Phase 9 diagnostic appendix artifacts from
  `work2_coding/Src/computational_tractability.py`
- case-study scaffold indexes from `.planning/data/case_studies/`

The current artifact state is explicitly not claim-ready. The main RC artifact
status in `work2_coding/artifacts/work2_robust_menu/ARTIFACT_STATUS.json` is
`blocked` with `claim_ready: false`. Phase 8 and Phase 9 summaries both report
`diagnostic_provisional_blocked` and `claim_ready: false`. Phase 7 case-study
materials are `scaffolding_only_blocked_execution` and contain no result
evidence.

## Evidence Inventory

### Main RC Evidence

Core diagnostic source:

- `work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a/normalized_rows.json`
- `.planning/results/RC_FORMAL_DIAGNOSIS.md`
- `.planning/results/RC_FORMAL_POLICY_SUMMARY.csv`
- `.planning/results/RC_FORMAL_PAIRED_DIFFS.csv`
- `work2_coding/outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json`
- `work2_coding/outputs/phase3_formal_artifacts/ARTIFACT_STATUS.json`
- `work2_coding/outputs/phase3_formal_artifacts/manuscript/CLAIM_GUARD.json`

Status boundary:

- 35 completed rows across 5 paired splits and 7 mainline policies are usable
  for diagnosis.
- Checkpoint load status is `loaded` in the selected formal run.
- Readiness remains blocked by `dirty_git`.
- Current artifact/claim gates remain blocked or false.
- Strong universal dominance is unsupported.
- Adaptive equals optimized fixed-window across tracked metrics in the selected
  formal rows.

### Phase 8 Sensitivity Evidence

Core diagnostic sources:

- `.planning/results/SENSITIVITY_SUMMARY.md`
- `work2_coding/artifacts/work2_robust_menu/phase8_sensitivity/ARTIFACT_STATUS.json`
- `work2_coding/artifacts/work2_robust_menu/phase8_sensitivity/aggregates/sensitivity_axis_summary.json`
- `work2_coding/artifacts/work2_robust_menu/phase8_sensitivity/tables/sensitivity_axis_summary.tex`
- `work2_coding/artifacts/work2_robust_menu/phase8_sensitivity/tables/sensitivity_boundary_map.tex`
- `work2_coding/artifacts/work2_robust_menu/phase8_sensitivity/figures/optout_acceptance_by_axis.png`
- `work2_coding/artifacts/work2_robust_menu/phase8_sensitivity/figures/profit_service_tradeoff.png`

Status boundary:

- Baseline validation passed.
- Four must-have axes were executed: `menu_k`, `eta_filter_mode`,
  `uptake_regime`, and `guardrail`.
- The outputs are diagnostic/provisional and cannot upgrade manuscript claims.

### Phase 9 Tractability Evidence

Core diagnostic sources:

- `.planning/results/COMPUTATIONAL_TRACTABILITY_SUMMARY.md`
- `work2_coding/artifacts/work2_robust_menu/phase9_tractability/ARTIFACT_STATUS.json`
- `work2_coding/artifacts/work2_robust_menu/phase9_tractability/aggregates/exact_greedy_tractability_summary.json`
- `work2_coding/artifacts/work2_robust_menu/phase9_tractability/tables/exact_greedy_tractability.tex`
- `work2_coding/artifacts/work2_robust_menu/phase9_tractability/figures/menu_build_time_by_candidate_count.png`
- `work2_coding/artifacts/work2_robust_menu/phase9_tractability/figures/gap_overlap_by_candidate_count.png.status.json`

Status boundary:

- 15 rows completed and checkpoint load status is explicit.
- Large configured candidate scales did not trigger greedy fallback in the
  realized candidate sets.
- Gap/overlap evidence is unavailable.
- Near-optimal greedy and claim-ready online-tractability language remain
  blocked.

### Case-Study Scaffold

Core scaffold-only sources:

- `.planning/data/case_studies/README.md`
- `.planning/data/case_studies/source_contracts.yaml`
- `.planning/data/case_studies/route_selection_scorecard.yaml`
- `.planning/data/case_studies/simulated_demand_protocol.md`
- `.planning/data/case_studies/case_manifest_draft.yaml`
- `.planning/data/case_studies/reduced_family_gate.md`
- `.planning/data/case_studies/claim_boundary_placeholders.md`
- `.planning/data/case_studies/VALIDATION_SUMMARY.md`

Status boundary:

- These are contracts and placeholders only.
- No external case data, matrices, simulated demand rows, replay rows, result
  tables, result figures, or case validation claims exist.
- Phase 10 may index these as scaffold-only appendix material, but must not
  present them as empirical evidence.

## Existing Builder Surfaces

### `work2_coding/Src/artifact_builder.py`

Useful functions:

- `load_run(run_dir)`
- `latest_run_dir(study, study_output_root=None)`
- `aggregate_by_policy(rows)`
- `write_latex_table(path, caption, rows, columns)`
- `artifact_metadata(artifact_path, run_data, status_info, source_rows, artifact_kind)`
- `write_sidecar(artifact_path, run_data, status_info, artifact_kind)`
- `generate_figures(figures_dir, aggregates, run_data, status_info)`
- `build_artifacts(run_dir, output_root=None, mirror_root=None, allow_incomplete=False, claim_ready=False, readiness_json=None)`

Important behavior:

- `build_artifacts` already writes aggregate JSON/CSV, LaTeX tables,
  incomplete figure-status JSON files, `ARTIFACT_STATUS.json`, README, and a
  manuscript frame.
- Claim-ready build mode fails closed unless readiness and artifact gates pass.
- Diagnostic/incomplete builds require `allow_incomplete=True`.
- Metadata sidecars carry source run, row count, status, checkpoint summary,
  method-family, outside-option utility, uptake regime, and provenance fields.

### `work2_coding/Src/artifact_status.py`

Useful functions:

- `classify_artifact(rows, summary=None, claim_ready_requested=False, dependency_snapshot=None)`
- `validate_formal_readiness_for_run(readiness_json, rows, summary)`
- `collect_environment_provenance(include_freeze=False)`
- `write_json(path, value)`

Important behavior:

- Formal/pilot rows require loaded checkpoint provenance, valid
  `method_family`, `outside_option_util`, and accepted-home/meeting-point/
  opt-out accounting.
- Smoke and diagnostic modes cannot become claim-ready.
- Formal claim-ready artifacts require a dependency snapshot and passed
  readiness.
- Blockers in source summaries force blocked artifact status.

### `work2_coding/Src/manuscript_claims.py`

Useful functions:

- `build_claim_guard(status)`
- `write_manuscript_frame(artifact_root, mirror_root=None)`

Current limitation:

- The existing guard has allowed, conditional, and blocked claim families, but
  Phase 10 needs stricter per-claim entries with `claim_id`, `claim_text`,
  `support_status`, `source_artifacts`, `blocker_reasons`, `safe_language`,
  `forbidden_language`, `manuscript_allowed`, and `claim_ready`.

Recommended extension:

- Add a new strict Phase 10 guard builder or extend `build_claim_guard` while
  preserving existing tests and JSON compatibility.
- Ensure universal dominance, claim-ready superiority, real passenger
  behavior, case-study validation, no-filter operational recommendation, and
  near-optimal greedy statements are explicitly forbidden under current
  evidence.

### Phase 8 and Phase 9 Helpers

Useful functions in `work2_coding/Src/sensitivity_analysis.py`:

- `build_sensitivity_artifacts(...)`
- `render_sensitivity_summary(result)`
- `write_sensitivity_summary(...)`
- `validate_sensitivity_rows(...)`
- `aggregate_sensitivity_rows(rows)`

Useful functions in `work2_coding/Src/computational_tractability.py`:

- `build_tractability_artifacts(...)`
- `render_tractability_summary(result)`
- `write_tractability_summary(...)`
- `validate_tractability_rows(...)`
- `aggregate_tractability_rows(rows)`

Important behavior:

- Both helper modules force `claim_ready: false`.
- Both write metadata sidecars.
- Phase 9 writes a status JSON when gap/overlap figures are unavailable.

## Recommended Phase 10 Architecture

Add a small module:

```text
work2_coding/Src/paper_artifacts.py
```

Add a CLI wrapper:

```text
work2_coding/scripts/build_phase10_paper_artifacts.py
```

This module should not re-implement the artifact builders. It should:

1. Accept source roots for main RC, Phase 8 sensitivity, Phase 9 tractability,
   and case scaffold contracts.
2. Validate each source root has an artifact/status file or documented
   scaffold-only status.
3. Copy or reference existing generated tables/figures into a Phase 10 package
   root, defaulting to:

```text
work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/
```

4. Write machine-readable package files:

```text
PACKAGE_INDEX.json
SOURCE_INDEX.json
ARTIFACT_TO_SECTION_MAP.json
CLAIM_GUARD.json
README.md
```

5. Write optional lightweight Markdown checklists:

```text
claim_checklist.md
artifact_to_section_map.md
```

6. Mirror lightweight outputs to:

```text
artifacts/work2_robust_menu/phase10_paper_artifacts/
```

7. Keep `claim_ready=false` unless all upstream gates are explicitly passed.

Suggested package tiers:

- `main_paper_candidate`
- `diagnostic_appendix`
- `scaffold_only`
- `blocked_status`

Suggested section map:

- experimental design
- main RC results
- product/time-window ablation
- ETA/time-window robustness
- sensitivity appendix
- computational performance appendix
- case-study scaffold appendix
- provenance and claim gates

## Strict Claim Guard Design

Phase 10 should define a strict claim list based on
`.planning/paper/TR_E_RESEARCH_DESIGN.md` and Phase 4/8/9 closeouts:

- `C1`: central adaptive menu superiority
- `C2`: product ablation value
- `C3`: adaptive window value
- `C4`: menu construction value
- `C5`: ETA robustness/no-filter boundary
- `C6`: exact-vs-greedy computational credibility
- `C7`: provenance/status transparency
- `C8`: semi-real case-study validation

Minimum per-claim schema:

```json
{
  "claim_id": "C1",
  "claim_text": "...",
  "support_status": "unsupported|conditional_diagnostic|blocked|status_supported",
  "source_artifacts": ["..."],
  "blocker_reasons": ["..."],
  "safe_language": ["..."],
  "forbidden_language": ["..."],
  "manuscript_allowed": false,
  "claim_ready": false
}
```

Overall `claim_ready` must be the conjunction of all relevant upstream gates,
not a manually selected value.

## Validation Architecture

Phase 10 is primarily an artifact-contract phase. Verification should be
script-style and fast.

Recommended tests:

- `python scripts/test_phase10_paper_artifacts.py`
- `python scripts/test_manuscript_claim_guard.py`
- `python scripts/test_artifact_builder.py`
- `python scripts/test_artifact_gates.py`
- `python scripts/test_phase8_sensitivity_summary.py`
- `python scripts/test_phase9_tractability_summary.py`
- `python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"`

Recommended new test coverage:

1. `PACKAGE_INDEX.json` includes main RC, Phase 8, Phase 9, and case scaffold
   source families.
2. Every package item has `source_path`, `tier`, `status`, `claim_linkage`,
   and `claim_ready`.
3. Case scaffold entries are `scaffold_only` and cannot appear in result-table
   or result-figure tiers.
4. Phase 8 and Phase 9 entries preserve `diagnostic_provisional_blocked` and
   `claim_ready=false`.
5. Strict `CLAIM_GUARD.json` has all required per-claim fields.
6. Forbidden language blocks universal dominance, claim-ready superiority,
   real passenger behavior, case-study validation, no-filter recommendation,
   and near-optimal greedy statements.
7. Artifact-facing frame outputs do not write manuscript body sections,
   abstract upgrades, or conclusion upgrades.

## Implementation Risks

| Risk | Mitigation |
| --- | --- |
| Phase 10 accidentally rebuilds or mutates prior outputs | Implement package assembly by copying/referencing existing builder outputs; do not edit rows or source artifacts. |
| Diagnostic appendices are mistaken for main evidence | Require tier/status fields on every package item and test them. |
| Case scaffolding becomes a case-study result | Force `scaffold_only_no_result_evidence` and block result-table/figure classification. |
| Strict guard diverges from existing manuscript guard tests | Preserve existing `build_claim_guard` behavior or add a compatible strict wrapper. |
| `claim_ready` is accidentally upgraded | Default false and compute true only from upstream status gates. |
| Missing source artifacts cause silent gaps | Emit blocked/status entries with missing source paths and test package completeness. |

## Suggested Execution Order

1. Add Phase 10 package/index module and CLI.
2. Add tests for source indexing, package tiers, metadata, and case scaffold
   restrictions.
3. Extend strict claim guard and artifact-facing frame generation.
4. Add tests for per-claim schema and forbidden/safe language.
5. Run focused artifact, guard, Phase 8, Phase 9, and import checks.

## Research Summary

The existing codebase already has the right foundation for Phase 10. The gap is
not another experiment or another standalone plotting system. The gap is a
claim-aware package assembler that indexes generated outputs, separates main
paper candidates from diagnostic appendices and scaffold-only material, and
emits a strict per-claim `CLAIM_GUARD.json` that keeps current manuscript
language conservative.

## RESEARCH COMPLETE
