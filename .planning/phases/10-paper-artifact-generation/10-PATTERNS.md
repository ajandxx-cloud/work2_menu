---
phase: 10
phase_name: Paper Artifact Generation
status: complete
generated: 2026-06-16T12:20:00+08:00
runtime_root: work2_coding/
---

# Phase 10 Pattern Map

## Pattern Mapping Complete

This pattern map is grounded in the active `work2_coding/` filesystem. Older
`.planning/codebase/` references to `ooh_code/` are historical only.

## Files To Create

### `work2_coding/Src/paper_artifacts.py`

Role:

- New Phase 10 orchestration helper for paper artifact package assembly.

Closest analogs:

- `work2_coding/Src/artifact_builder.py`
- `work2_coding/Src/sensitivity_analysis.py`
- `work2_coding/Src/computational_tractability.py`
- `work2_coding/Src/manuscript_claims.py`

Patterns to copy:

- Use `Path` roots and repository-relative path helpers.
- Use `write_json(path, value)` from `Src.artifact_status`.
- Use plain dictionaries/lists for artifact records and status payloads.
- Keep source metadata in sidecars or package indexes, not only prose.
- Do not use network calls or external services.

Expected responsibilities:

- Load existing status/source artifacts.
- Classify package entries by tier.
- Write `PACKAGE_INDEX.json`, `SOURCE_INDEX.json`,
  `ARTIFACT_TO_SECTION_MAP.json`, `CLAIM_GUARD.json`, `README.md`, and optional
  Markdown maps.
- Mirror lightweight outputs when requested.

### `work2_coding/scripts/build_phase10_paper_artifacts.py`

Role:

- Thin CLI wrapper for `Src.paper_artifacts`.

Closest analogs:

- `work2_coding/scripts/build_artifacts.py`
- `work2_coding/scripts/build_manuscript_frame.py`
- `work2_coding/scripts/build_phase8_sensitivity_artifacts.py`
- `work2_coding/scripts/build_phase9_tractability_artifacts.py`

Patterns to copy:

- Insert `work2_coding/` into `sys.path` at script start.
- Use `argparse`.
- Print a compact JSON result to stdout.
- Keep `main(argv=None)` thin.

### `work2_coding/scripts/test_phase10_paper_artifacts.py`

Role:

- Script-style tests for package indexing, strict guard, and no-overclaim
  constraints.

Closest analogs:

- `work2_coding/scripts/test_artifact_builder.py`
- `work2_coding/scripts/test_artifact_gates.py`
- `work2_coding/scripts/test_manuscript_claim_guard.py`
- `work2_coding/scripts/test_phase8_sensitivity_summary.py`
- `work2_coding/scripts/test_phase9_tractability_summary.py`

Patterns to copy:

- Use `TemporaryDirectory`.
- Build minimal JSON/YAML/Markdown fixtures where possible.
- Use direct `assert` statements.
- Implement `main()` with an explicit list of test functions.
- Print `PASS: N ... tests`.

## Files To Modify

### `work2_coding/Src/manuscript_claims.py`

Role:

- Existing manuscript frame and claim guard helper.

Relevant existing functions:

- `build_claim_guard(status)`
- `render_method_outline(guard)`
- `render_experiment_outline(guard)`
- `render_result_outline(guard)`
- `render_claim_checklist(guard)`
- `write_manuscript_frame(artifact_root, mirror_root=None)`

Recommended Phase 10 change:

- Add or expose strict per-claim guard support while preserving existing
  `build_claim_guard` behavior expected by current tests.
- If adding new functions, prefer names such as `build_strict_claim_guard` and
  `render_artifact_section_map`.

### `work2_coding/scripts/test_manuscript_claim_guard.py`

Role:

- Existing guard tests.

Recommended Phase 10 change:

- Add strict per-claim schema assertions without weakening existing blocked and
  claim-ready tests.

## Source Artifacts To Read Or Index

### Main RC

- `work2_coding/artifacts/work2_robust_menu/ARTIFACT_STATUS.json`
- `work2_coding/artifacts/work2_robust_menu/tables/*.tex`
- `work2_coding/artifacts/work2_robust_menu/figures/*.png`
- `work2_coding/artifacts/work2_robust_menu/figures/*.status.json`
- `work2_coding/artifacts/work2_robust_menu/aggregates/*.json`
- `work2_coding/artifacts/work2_robust_menu/manuscript/CLAIM_GUARD.json`
- `.planning/results/RC_FORMAL_DIAGNOSIS.md`

### Phase 8

- `work2_coding/artifacts/work2_robust_menu/phase8_sensitivity/ARTIFACT_STATUS.json`
- `work2_coding/artifacts/work2_robust_menu/phase8_sensitivity/aggregates/sensitivity_axis_summary.json`
- `work2_coding/artifacts/work2_robust_menu/phase8_sensitivity/tables/*.tex`
- `work2_coding/artifacts/work2_robust_menu/phase8_sensitivity/figures/*.png`
- `.planning/results/SENSITIVITY_SUMMARY.md`

### Phase 9

- `work2_coding/artifacts/work2_robust_menu/phase9_tractability/ARTIFACT_STATUS.json`
- `work2_coding/artifacts/work2_robust_menu/phase9_tractability/aggregates/exact_greedy_tractability_summary.json`
- `work2_coding/artifacts/work2_robust_menu/phase9_tractability/tables/*.tex`
- `work2_coding/artifacts/work2_robust_menu/phase9_tractability/figures/*.png`
- `work2_coding/artifacts/work2_robust_menu/phase9_tractability/figures/*.status.json`
- `.planning/results/COMPUTATIONAL_TRACTABILITY_SUMMARY.md`

### Case Scaffold

- `.planning/data/case_studies/*.md`
- `.planning/data/case_studies/*.yaml`
- `.planning/data/case_studies/VALIDATION_SUMMARY.md`

## Status And Tier Rules

| Source family | Required tier | Claim-ready handling |
| --- | --- | --- |
| Main RC generated artifacts | `main_paper_candidate` or `blocked_status` | Preserve upstream `claim_ready` value; current expected value is false. |
| Phase 8 sensitivity | `diagnostic_appendix` | Force or verify `claim_ready=false`. |
| Phase 9 tractability | `diagnostic_appendix` | Force or verify `claim_ready=false`; keep gap/overlap blocked. |
| Case scaffold | `scaffold_only` | Force `claim_ready=false`; exclude from result table/figure categories. |
| Formal blocker docs | `blocked_status` | Force `claim_ready=false`; link to provenance/gate sections. |

## Verification Pattern

Use focused script tests rather than a global test runner. Minimum commands:

```powershell
cd work2_coding
python scripts/test_phase10_paper_artifacts.py
python scripts/test_manuscript_claim_guard.py
python scripts/test_artifact_builder.py
python scripts/test_artifact_gates.py
python scripts/test_phase8_sensitivity_summary.py
python scripts/test_phase9_tractability_summary.py
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
```

## Anti-Patterns

- Do not hand-edit normalized rows, existing generated tables, existing
  generated figures, or prior claim guards to improve Phase 10 output.
- Do not run new replay, calibration, final formal evidence, or case-study
  execution in Phase 10.
- Do not write manuscript body paragraphs, abstract claims, or conclusion
  upgrades.
- Do not classify case scaffold files as result evidence.
- Do not treat no-filter or Phase 8/9 diagnostic outputs as operational or
  claim-ready recommendations.
