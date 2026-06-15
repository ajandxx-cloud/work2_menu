# Requirements: Work2_TR_E_Service_Menu_Optimization_Final

**Defined:** 2026-06-14
**Core Value:** Produce credible, reproducible TR Part E evidence that optimized
adaptive `m+w+p` service menus improve the profit-service-quality trade-off
under paired RC replay, without overclaiming beyond artifact and readiness
gates.

## v1 Requirements

### State And Runtime

- [x] **STATE-01**: Phase 1 verifies `work2_coding/` as the active runtime root
  and records the result in `.planning/STATE_LOCK.md`.
- [x] **STATE-02**: Phase 1 inventories current manifests, tests, scripts,
  artifacts, formal checkpoint status, and current blockers.
- [x] **STATE-03**: Phase 1 maps stale `ooh_code/` planning references to
  current `work2_coding/` paths or marks them obsolete.

### Paper Design

- [x] **PAPER-01**: The project defines a TR Part E research design centered on
  dynamic service menu optimization, not attention and not pricing-only.
- [x] **PAPER-02**: The paper design defines service bundles as
  `(meeting point, pickup time window, price)` and includes home service plus
  outside option semantics.
- [x] **PAPER-03**: Every planned paper claim maps to policy comparisons,
  metrics, and artifact evidence.
- [x] **PAPER-04**: The paper design distinguishes V1 main evidence, V2
  diagnostic attention evidence, appendix evidence, and non-claims.
- [x] **PAPER-05**: The paper design includes a mathematical model skeleton
  with sets and indices, service-bundle definition, menu decision variable,
  utility model, choice probability, expected-profit objective,
  opt-out/service-quality guardrail, ETA/time-window feasibility, and
  exact/greedy solver definitions.

### Formal RC Evidence

- [x] **RC-01**: `formal_robust_menu.yaml` and related manifests are inspected
  before formal execution.
- [x] **RC-02**: The required shared checkpoint path is generated or verified:
  `outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt`.
- [x] **RC-03**: Formal readiness passes without bypassing blockers.
- [x] **RC-04**: Formal RC replay produces completed or explicitly failed
  normalized rows for comparable policy variants.
- [x] **RC-05**: Formal artifact generation produces readiness, row, summary,
  artifact-status, claim-guard, table, figure, and manuscript-frame outputs.

### Claim Diagnosis

- [x] **CLAIM-01**: Formal results are diagnosed by effect size, paired split,
  uptake regime, and metric trade-off rather than ranking alone.
- [x] **CLAIM-02**: The project classifies each planned claim as strong,
  conditional, weak/diagnostic, or unsupported.
- [x] **CLAIM-03**: Unsupported or mixed results trigger diagnosis rather than
  manual result editing or forced claims.
- [x] **CLAIM-04**: Formal result diagnosis reports mean, standard deviation,
  paired differences, and confidence intervals where feasible; if seed count is
  small, it reports split-level paired differences and avoids strong
  significance language.
- [x] **CLAIM-05**: If optimized adaptive `m+w+p` does not strongly dominate,
  the paper is reframed as a conditional service-menu optimization study rather
  than a universal superiority claim.

### Calibration Integrity

- [x] **CAL-01**: If results are weak or unstable, calibration parameters are
  declared before final testing.
- [x] **CAL-02**: Calibration and formal testing are separated into distinct
  manifests, outputs, and documents.
- [x] **CAL-03**: Frozen final settings are documented before rerunning final
  evidence.
- [x] **CAL-04**: Phase 5 may be marked skipped-by-gate if Phase 4 supports at
  least one central claim with stable paired differences; otherwise Phase 5 is
  mandatory.

### Case Study

- [x] **CASE-01**: The project audits whether a real or semi-real case study is
  feasible from existing materials, public data, or real geography plus
  simulated demand.
- [x] **CASE-02**: No fabricated real data is used or implied.
- [x] **CASE-03**: If feasible, the case study has a reproducible ingestion,
  validation, smoke, pilot, and formal/diagnostic execution contract. Phase 7
  covers this as planning-side contract scaffolding only: source contracts,
  validation checks, manifest draft, and execution gates exist, but no case
  rows or runtime manifest were produced.
- [x] **CASE-04**: A minimum acceptable semi-real case is defined as real or
  manually documented geography, realistic depot/destination and candidate
  meeting points, real road distance or reproducible distance matrix, simulated
  sequential DRT demand clearly labeled as simulated, same seven-tag or reduced
  six-tag comparison, and no use for tuning RC parameters.
- [x] **CASE-05**: If Phase 6 defers the case study, Phase 7 is skipped and the
  manuscript explicitly states that external case validation is deferred. Phase
  6 did not defer; Phase 7 was not skipped, and case execution plus manuscript
  external-validation claims remain blocked until upstream gates pass.

### Sensitivity And Computation

- [x] **SENS-01**: Phase 8 diagnostic sensitivity experiments cover the
  executable must-have dimensions: menu size, ETA uncertainty/filter mode,
  uptake regime, and opt-out/service guardrail. Candidate pool size,
  fleet/capacity stress, pricing bounds, and price sensitivity remain deferred
  nice-to-have dimensions.
- [x] **SENS-02**: `.planning/results/SENSITIVITY_SUMMARY.md` supports
  conditional diagnostic conclusions and identifies where the method works,
  fails, or exposes profit-service-quality trade-offs, without upgrading
  manuscript claims.
- [x] **SENS-03**: Phase 8 separates must-have sensitivity dimensions
  (`menu_k`, ETA uncertainty/filter mode, uptake regime, opt-out guardrail)
  from nice-to-have dimensions (candidate pool size, fleet/capacity stress,
  pricing bounds or price sensitivity).
- [ ] **COMP-01**: Exact-small versus greedy-large experiments report optimality
  gap, menu overlap, build time, candidate count, and enumerated menu count.
- [ ] **COMP-02**: The solver is shown to be computationally credible for
  online DRT, or the claim is narrowed.

### Artifacts And Manuscript

- [ ] **ART-01**: Paper-facing tables and figures are generated from run rows
  and artifact builders only.
- [ ] **ART-02**: `CLAIM_GUARD.json` states whether each claim is supported
  before manuscript language is upgraded.
- [ ] **MS-01**: The manuscript plan follows the TR Part E structure:
  Introduction, Literature Review, Problem Description, Model, Solution Method,
  Experimental Design, Results, Discussion, Conclusion, and Appendix.
- [ ] **MS-02**: Manuscript claims are traceable to source artifacts and avoid
  overstating simulated passenger behavior.
- [ ] **FINAL-01**: A final TR Part E readiness review audits novelty, modeling
  rigor, algorithmic contribution, experimental credibility, reproducibility,
  and claim clarity.

## Deferred Requirements

- **ATT-01**: Attention-based choice or scoring may be revisited only as V2 or
  appendix diagnostic evidence after V1 RC claims are stable.
- **REAL-01**: A real passenger choice validation study is future work unless
  actual choice data are obtained and documented.
- **RL-01**: New RL methods or unrelated model families are outside this
  refactoring plan unless a later milestone explicitly expands scope.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Hand-edited generated evidence | Violates reproducibility and claim traceability. |
| Attention as V1 main contribution | The current paper contribution is service menu optimization. |
| Universal dominance claims | TR-E claims must reflect measured trade-offs and caveats. |
| Formal claims from smoke-only runs | Smoke runs validate the pipeline, not empirical superiority. |
| Fabricated real case study | Case data must be real, semi-real, or clearly synthetic. |
| Parallel `ooh_code/` root | Active runtime is `work2_coding/`; stale maps are historical only. |

## Traceability

| Requirement | Phase | Status |
| --- | --- | --- |
| STATE-01..STATE-03 | Phase 1 | Complete |
| PAPER-01..PAPER-05 | Phase 2 | Complete |
| RC-01..RC-05 | Phase 3 | Pending |
| CLAIM-01..CLAIM-05 | Phase 4 | Complete |
| CAL-01..CAL-04 | Phase 5 | Complete |
| CASE-01, CASE-02, CASE-04 | Phase 6 | Complete |
| CASE-03, CASE-05 | Phase 7 | Complete - scaffold contracts only; no case evidence rows |
| SENS-01..SENS-03 | Phase 8 | Complete - diagnostic/provisional; nice-to-have axes deferred |
| COMP-01..COMP-02 | Phase 9 | Pending |
| ART-01..ART-02 | Phase 10 | Pending |
| MS-01..MS-02 | Phase 11 | Pending |
| FINAL-01 | Phase 12 | Pending |

**Coverage:**
- v1 requirements: 39 total
- Mapped to phases: 39
- Unmapped: 0

---
*Requirements defined: 2026-06-14*
*Last updated: 2026-06-15 after Phase 8 diagnostic sensitivity closeout*
