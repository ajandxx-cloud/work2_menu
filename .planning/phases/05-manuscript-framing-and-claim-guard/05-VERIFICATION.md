---
phase: 05-manuscript-framing-and-claim-guard
status: passed
verified: 2026-06-11
requirements:
  - PAPER-01
  - PAPER-02
  - PAPER-03
  - PAPER-04
---

# Phase 05 Verification: Manuscript Framing And Claim Guard

## Result

Status: passed

Phase 5 achieved its goal: the project now has paper-ready method, experiment, and result outlines plus an explicit claim checklist and machine-readable claim guard. These artifacts are generated from the Phase 4 artifact status and correctly preserve the current blocked/non-claim-ready evidence boundary.

## Requirement Traceability

| Requirement | Status | Evidence |
|-------------|--------|----------|
| PAPER-01 | passed | `work2_coding/artifacts/work2_robust_menu/manuscript/method_outline.md` covers service bundles, displayed menu decision, outside option, robust ETA handling, MNL choice, pricing, and exact/greedy solver behavior. |
| PAPER-02 | passed | `work2_coding/artifacts/work2_robust_menu/manuscript/experiment_outline.md` covers smoke/pilot/formal tiers, baselines, metrics, paired replay, seeds/splits, checkpoint handling, and uptake regimes. |
| PAPER-03 | passed | `work2_coding/artifacts/work2_robust_menu/manuscript/result_outline.md` covers exact-vs-greedy quality, robust filtering, uptake regimes, profit/status outputs, external/semi-real checks, and limitations while blocking unsupported empirical conclusions. |
| PAPER-04 | passed | `work2_coding/artifacts/work2_robust_menu/manuscript/claim_checklist.md` and `CLAIM_GUARD.json` allow robust-pruning, solver-auditability, paired-replay, artifact-transparency claims while blocking universal dominance, unsupported behavioral validation, no-filter operational recommendation, full-system exact optimality, and pilot/formal empirical conclusions under current status. |

## Automated Checks

- `cd work2_coding; python scripts/test_manuscript_claim_guard.py` -> `PASS: 4 manuscript claim guard tests`
- `cd work2_coding; python scripts/build_manuscript_frame.py --artifact-root artifacts/work2_robust_menu --mirror-root ../artifacts/work2_robust_menu` -> generated all five manuscript support files and reported `claim_ready: false`
- `cd work2_coding; python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` -> `IMPORT_OK`
- `cd work2_coding; python -m py_compile Src/manuscript_claims.py scripts/build_manuscript_frame.py scripts/test_manuscript_claim_guard.py` -> passed

## Must-Have Review

- The generated claim guard reads `ARTIFACT_STATUS.json`; it does not infer claim readiness from prose.
- Current status remains `blocked`, with `claim_ready=false`, `pilot_claim_ready=false`, and `formal_claim_ready=false`.
- Missing checkpoint and formal skipped blockers are preserved in `CLAIM_GUARD.json` and checklist output.
- `no_filter_diagnostic` remains diagnostic-only.
- Synthetic claim-ready tests allow pilot/formal result-family claims but still block universal dominance and real passenger validation.
- Generated files are mirrored under root `artifacts/work2_robust_menu/manuscript/`.

## Current Artifact Status

- `work2_coding/artifacts/work2_robust_menu/manuscript/CLAIM_GUARD.json` -> `artifact_status = blocked`
- `claim_ready = false`
- `pilot_claim_ready = false`
- `formal_claim_ready = false`
- blocked empirical claim IDs include `empirical_superiority` and `pilot_formal_completed`

## Boundaries

Phase 5 does not make the manuscript empirically complete. It makes the current manuscript framing safe and reproducible. Any stronger empirical claim still requires a claim-ready Phase 4 artifact bundle with loaded checkpoint provenance and non-placeholder pilot/formal rows.

## Residual Risks

- The repository still has unrelated pre-existing dirty state (`learning meeting point.docx` deletion and one untracked Chinese-named text file). Phase 5 ignored these files.
- The generated outlines are Markdown support artifacts, not final LaTeX paper text.

