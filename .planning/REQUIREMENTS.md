# Requirements: Work2 Robust Time-Window Service Menu Optimization

**Defined:** 2026-06-14
**Core Value:** Paired-replay V1 evidence for robust time-window service menu
optimization in many-to-one DRT.

## v1 Requirements

### Runtime And Scope

- [x] **RUN-01**: The active runtime root is `work2_coding/`.
- [x] **RUN-02**: Stale `ooh_code/` codebase-map references are audited and mapped.
- [x] **RUN-03**: `Src.config` imports successfully from `work2_coding/`.
- [x] **RUN-04**: Phase 4 artifact commands operate only on regenerated
  `work2_coding/` outputs and do not hand-edit paper artifacts.

### Service Product Contract

- [x] **SPC-01**: Service products expose `product_mode` values `m`, `m+w`,
  and `m+w+p`.
- [x] **SPC-02**: Time-window modes expose `no_time_window`, `fixed_window`,
  and `adaptive_window`.
- [x] **SPC-03**: Menu modes expose `no_menu`, `fixed_menu`, `random_menu`,
  and `optimized_menu`.
- [x] **SPC-04**: Passenger-facing price/incentive is separate from system
  profit, operational cost, and total cost.
- [x] **SPC-05**: Opt-out remains separate from accepted home pickup and does
  not mutate routes as accepted service.

### Mainline Comparison Contract

- [x] **MLC-01**: `work2_robust_menu` uses exactly seven V1 mainline policy tags.
- [x] **MLC-02**: Smoke and pilot manifests cover `menu_k={1,2,3,5}`.
- [x] **MLC-03**: Formal manifest fixes `menu_k=3`.
- [x] **MLC-04**: Formal manifest declares at least five paired splits/seeds and
  covers low and medium uptake regimes.
- [x] **MLC-05**: Formal manifest requires checkpoint provenance.
- [x] **MLC-06**: Paired replay fairness prevents policy-level drift in
  non-comparison fields.

### Row And Execution Contract

- [x] **ROW-01**: Normalized rows use `normalized-row-v2`.
- [x] **ROW-02**: Rows include product, time-window, menu, pricing, method,
  candidate, status, checkpoint, profit, and service fields.
- [x] **ROW-03**: Aggregate rows use `candidate_id="aggregate"`.
- [x] **ROW-04**: Failed rows include `status`, `execution_status`,
  `error_type`, and `error_message`, and batch execution continues.
- [x] **ROW-05**: Smoke actual replay completes all seven mainline policies.

### Artifacts And Claims

- [x] **ART-01**: Artifact builder consumes normalized-row-v2 mainline outputs.
- [x] **ART-02**: Mainline claim guard excludes diagnostic, failed, blocked,
  placeholder-only, no-filter-only, contract-only, and bad-checkpoint rows.
- [x] **ART-03**: Mainline artifacts include source run IDs, manifest hashes,
  checkpoint statuses, and provenance metadata.
- [x] **ART-04**: Mirrored artifact bundles and manuscript-facing tables/figures
  are generated from outputs, not edited by hand.

## v2 Requirements

- Attention-based choice/scoring and attention artifacts are deferred to V2 or
  diagnostic work.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Hand-edited paper artifacts | Evidence must be reproducible from generated outputs. |
| No-filter formal ranking claims | No-filter remains diagnostic unless separately justified. |
| Attention-based V1 ranking | Attention is diagnostic/V2 only. |
| Parallel `ooh_code/` runtime | `work2_coding/` is active and verified. |

## Traceability

| Requirement | Phase | Status |
| --- | --- | --- |
| RUN-01, RUN-02, RUN-03 | Phase 1 | Validated |
| SPC-01..SPC-05 | Phase 2 | Validated |
| MLC-01..MLC-06, ROW-01..ROW-05 | Phase 3 | Validated |
| ART-01..ART-04, RUN-04 | Phase 4 | Validated |
| MLC-05, ART-02, ART-03 formal readiness gates | Phase 5 | Validated |

---
*Last updated: 2026-06-14 after Phase 5 readiness gate verification*
