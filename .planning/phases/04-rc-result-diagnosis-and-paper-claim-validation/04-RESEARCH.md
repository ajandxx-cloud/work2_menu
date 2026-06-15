---
phase: 04-rc-result-diagnosis-and-paper-claim-validation
status: research-complete
created: 2026-06-15T12:45:00+08:00
timezone: Asia/Shanghai
mode: inline
---

# Phase 4 Research: RC Result Diagnosis And Paper-Claim Validation

## Research Question

Phase 4 must determine what the completed formal RC run can support as paper
evidence. The goal is not to improve the algorithm, tune parameters, rerun the
formal benchmark, or upgrade manuscript claims. The output is a blocker-first
diagnosis in `.planning/results/RC_FORMAL_DIAGNOSIS.md`.

## Source Evidence

Use the completed formal run selected by Phase 3:

```text
work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a
```

Key files:

- `study_summary.json`
- `normalized_rows.json`
- `normalized_rows.csv`

Gate and provenance inputs:

- `work2_coding/outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json`
- `work2_coding/outputs/phase3_formal_artifacts/ARTIFACT_STATUS.json`
- `work2_coding/outputs/phase3_formal_artifacts/manuscript/CLAIM_GUARD.json`
- `.planning/results/PHASE3_FORMAL_EVIDENCE_HANDOFF.md`
- `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md`
- `.planning/results/FORMAL_FAILURE_DIAGNOSIS.md`

The formal run has 35 completed rows, seven policy tags, five paired splits,
two uptake regimes (`low`, `medium`), checkpoint status `loaded`, and
`git_dirty: true`.

## Existing Code And Artifact Support

Existing Phase 4 code is artifact-pipeline oriented:

- `work2_coding/scripts/run_phase4_artifacts.py`
- `work2_coding/scripts/test_phase4_artifact_pipeline.py`

These scripts verify artifact generation and status propagation. They do not
perform the claim-ladder diagnosis required by this phase: paired split
differences, uptake-regime comparison, product/window ablation interpretation,
and provisional claim classification.

Existing reusable contracts:

- `work2_coding/Src/paired_replay.py` defines paired replay row fields.
- `work2_coding/Src/policy_adapters.py` defines the seven mainline policy tags.
- `work2_coding/Src/artifact_status.py` and
  `work2_coding/Src/manuscript_claims.py` define artifact and claim-gate
  boundaries.
- `work2_coding/scripts/test_paired_replay_contract.py`,
  `test_policy_fairness_contract.py`, `test_artifact_gates.py`, and
  `test_phase4_artifact_pipeline.py` are the relevant script-style checks.

## Diagnostic Approach

The diagnosis should be generated from formal rows and gate JSON, not from
hand-edited tables. A small read-only helper is acceptable if it:

- reads `normalized_rows.json` or `.csv`;
- validates `5 splits x 7 policies`;
- validates completed row status, loaded checkpoint status, and no placeholders;
- computes means and population standard deviations by policy;
- computes paired differences for
  `mainline_optimized_adaptive - baseline` within each split;
- groups paired differences by uptake regime;
- reports directions and average paired differences rather than significance;
- writes diagnostic tables under `.planning/results/`;
- never edits generated formal rows or paper artifacts.

Do not report confidence intervals in this phase because there are only five
formal splits and the Phase 4 context explicitly chose split-level paired
differences and direction counts instead.

## Early Read-Only Metric Signal

A read-only pass over the selected run showed:

- `mainline_optimized_adaptive` improves mean net profit versus
  `mainline_no_menu`, `mainline_optimized_m`, and `mainline_optimized_mw`.
- It loses mean net profit versus `mainline_random_menu`.
- It is identical to `mainline_optimized_fixed_window` on the inspected key
  metrics.
- It has better mean acceptance and lower mean opt-out than several baselines.

Therefore, the likely paper conclusion is not universal dominance. The plan
must force claim-by-claim diagnosis and keep all classifications provisional or
blocked while dirty-git and artifact gates remain unresolved.

## Recommended Plan Shape

Use two plans:

1. Formal row and provenance diagnostics.
2. Claim matrix, blocker-first diagnosis document, and Phase 5 routing.

This keeps data extraction separate from scientific interpretation while
remaining small enough for a documentary phase.

## Verification Strategy

Minimum checks:

```powershell
cd work2_coding
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_paired_replay_contract.py
python scripts/test_policy_fairness_contract.py
python scripts/test_artifact_gates.py
python scripts/test_phase4_artifact_pipeline.py
```

If a diagnosis helper is added, add or run a script-style test that uses a
temporary mini row set and asserts paired differences, blocker propagation, and
no confidence-interval language for five splits.

## Research Complete

Phase 4 can proceed to planning with no external literature search. The needed
research is repository-local: formal rows, Phase 3 handoff, artifact gates, and
the locked paper claim ladder.
