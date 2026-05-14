# Requirements: ServiceMenuDRT Paper Revision

**Defined:** 2026-05-14
**Core Value:** Produce a TR Part E-ready revision whose demand calibration, filter-validity evidence, operational-baseline integration, and manuscript polish are strong enough to withstand a critical transportation-operations review.

## v1.1 Requirements

Requirements for milestone v1.1. Each maps to exactly one roadmap phase.

### Operational Baseline Integration

- [ ] **BASE-01**: Operational baselines are described in the empirical-policy taxonomy and interpreted in the main evidence narrative.
- [x] **BASE-02**: The operational-baseline table is placed where reviewers will see it and is explicitly connected to transportation-operations relevance.

### Demand Calibration and MNL Sensitivity

- [ ] **CAL-01**: Outside-option utility sensitivity is implemented or otherwise produced as a concrete table/figure, not only discussed as a limitation.
- [ ] **CAL-02**: MNL parameter ranges are tied to cited DRT, stated-preference, or travel-behavior literature where possible.
- [ ] **CAL-03**: Demand-calibration claims clearly distinguish literature-bounded stress testing from external validation.

### Filter Validity Diagnostics

- [ ] **FILT-01**: Deployed ETA/IVT validation reports P50, P90, and P95 error diagnostics in addition to MAE and bias.
- [ ] **FILT-02**: Filtering-decision diagnostics quantify how many filtered bundles appear feasible under the realized or best-available feasibility proxy.
- [ ] **FILT-03**: False-negative pruning is broken down by meeting-point type, walking-distance band, or another logged operational dimension.

### Evidence Synthesis and Interpretation

- [ ] **SYN-01**: High-uptake, flat-markdown, Lambert-W, acceptance, and surplus results are interpreted as tradeoffs rather than policy dominance.

### Polish and Submission QA

- [ ] **TEXT-01**: Remaining mojibake, stale README/caption language, and internal project terminology are removed from manuscript-facing files.
- [ ] **QA-01**: Final manuscript compiles, references and artifacts resolve, and a Round 2 response matrix maps every blocker to evidence or a documented limitation.

## v1.0 Validated Requirements

- [x] **CLAIM-01**: Paper claims are reframed as diagnostic/exploratory unless evidence supports stronger language.
- [x] **THEORY-01**: Lambert-W pricing is rewritten as a bounded reference transform, not a core optimality contribution.
- [x] **STAT-01**: City and RC inference are presented with conservative split-level language.
- [x] **WELF-01**: Profit, acceptance, and passenger welfare tradeoffs are decomposed.

## Future Requirements

### External Validation

- **EXT-01**: Additional city splits or demand seeds provide stronger external validation beyond the targeted v1.1 evidence plan.
- **EXT-02**: Real survey or revealed-preference calibration data support the MNL parameterization.
- **EXT-03**: City-level inference is upgraded from descriptive checks to a larger external-validation design.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Full city-scale validation campaign | Deferred; v1.1 closes submission-risk blockers without a broad new city experiment campaign. |
| Real revealed-preference or survey-data estimation | Not available in the current workspace; v1.1 can only cite plausible ranges and run sensitivity. |
| Re-promoting Lambert-W as a core theorem | v1.0 intentionally demoted Lambert-W, and Round 2 agreed this reduced conceptual risk. |

## Traceability

Which phases cover which requirements.

| Requirement | Phase | Status |
|-------------|-------|--------|
| BASE-01 | Phase 1 | Pending |
| BASE-02 | Phase 1 | Complete |
| CAL-01 | Phase 2 | Pending |
| CAL-02 | Phase 2 | Pending |
| CAL-03 | Phase 2 | Pending |
| FILT-01 | Phase 3 | Pending |
| FILT-02 | Phase 3 | Pending |
| FILT-03 | Phase 3 | Pending |
| SYN-01 | Phase 4 | Pending |
| TEXT-01 | Phase 5 | Pending |
| QA-01 | Phase 5 | Pending |

**Coverage:**
- v1.1 requirements: 11 total
- Mapped to phases: 11
- Unmapped: 0

---
*Requirements defined: 2026-05-14*
*Last updated: 2026-05-14 after v1.1 roadmap creation*
