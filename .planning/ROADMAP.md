# Roadmap: ServiceMenuDRT Paper Revision

## Roadmap v1.1: TR-E Submission Risk Closure

**Milestone Goal:** Close the Round 2 blockers that keep the revised manuscript at 6/10: external demand calibration, filter validity, operational-baseline integration, behavioral interpretation, and final polish.

## Overview

This roadmap converts the Round 2 review in `review_ServiceMenuDRT_round2_202605142050.md` into a five-phase revision milestone. The work starts by making already-generated operational baselines visible in the manuscript, then adds the two hardest evidence upgrades: outside-option/MNL calibration and filter-validity diagnostics. The final phases synthesize the evidence into a cautious TR-E narrative and complete submission QA plus response traceability.

## Phases

**Phase Numbering:**
- Phase numbering resets for this milestone after v1.0 phase directories were archived.
- Integer phases 1-5 are planned milestone work.
- Decimal phases are reserved for urgent insertions if later needed.

- [ ] **Phase 1: Operational Baseline Integration** - Make the existing insertion-cost, minimum-lateness, and random-top-k baselines visible and interpretable in the manuscript.
- [ ] **Phase 2: Demand Calibration and Outside-Option Sensitivity** - Add concrete outside-option sensitivity and literature-bounded MNL calibration framing.
- [ ] **Phase 3: Filter Validity Diagnostics** - Add quantile errors, filtering-decision diagnostics, and false-negative breakdowns for ETA/IVT filtering.
- [ ] **Phase 4: Evidence Synthesis and Behavioral Interpretation** - Reconcile pricing, uptake, acceptance, surplus, and operational-value claims into one cautious results narrative.
- [ ] **Phase 5: Polish, QA, and Round 2 Traceability** - Remove remaining polish issues, compile, verify references/artifacts, and prepare the Round 2 response matrix.

## Phase Details

### Phase 1: Operational Baseline Integration

**Goal:** Make the existing insertion-cost, minimum-lateness, and random-top-k operational baselines visible and interpretable in the manuscript.
**Depends on:** Nothing (first phase)
**Requirements:** [BASE-01, BASE-02]
**Canonical refs:**
- `review_ServiceMenuDRT_round2_202605142050.md` - Round 2 operational-baseline weakness and actionable fix.
- `ooh_code/manuscript/sections/method.tex` - Empirical policy and baseline taxonomy.
- `ooh_code/manuscript/sections/experiments.tex` - Study design and evaluation protocol.
- `ooh_code/manuscript/sections/results.tex` - Main evidence narrative.
- `ooh_code/artifacts/tables/operational_baselines_summary.tex` - Existing operational-baseline table.
- `ooh_code/artifacts/tables/phase32_operational_baselines_summary.tex` - Existing generated comparison table.

**Success Criteria** (what must be TRUE):
1. Method/experiments text names the operational baselines and explains their DRT-facing role.
2. Results or appendix includes the operational-baseline table with a reader-facing caption and interpretation.
3. The manuscript states what the operational baselines do and do not prove relative to menu optimization.
4. Round 2's "artifact exists but is not integrated" criticism is directly addressed.

**Plans:** 2 plans

Plans:
- [x] 01-01-PLAN.md — Baseline taxonomy and method/experiment integration (Wave 1)
- [x] 01-02-PLAN.md — Operational-baseline results placement and interpretation (Wave 2, depends on 01-01)

### Phase 2: Demand Calibration and Outside-Option Sensitivity

**Goal:** Add concrete outside-option sensitivity and literature-bounded MNL calibration framing.
**Depends on:** Phase 1
**Requirements:** [CAL-01, CAL-02, CAL-03]
**Canonical refs:**
- `review_ServiceMenuDRT_round2_202605142050.md` - Round 2 demand-calibration blocker.
- `ooh_code/Environments/OOH/customerchoice.py` - MNL/outside-option implementation.
- `ooh_code/experiments/studies/phase27_mnl_sensitivity_*.yaml` - Existing MNL sensitivity studies.
- `ooh_code/experiments/studies/phase31_uptake_menu_value_*.yaml` - Existing uptake-regime studies.
- `ooh_code/manuscript/sections/method.tex` - MNL parameter table and calibration language.
- `ooh_code/manuscript/sections/results.tex` - MNL sensitivity narrative.
- `ooh_code/manuscript/references.bib` - Literature anchors for parameter ranges.

**Success Criteria** (what must be TRUE):
1. Outside-option strength is varied in a concrete sensitivity artifact rather than only deferred.
2. MNL parameter ranges are justified by cited literature where the literature supports them.
3. The manuscript distinguishes literature-bounded sensitivity from true external demand validation.
4. Demand-calibration limitations are narrowed and honestly documented.

**Plans:** 3 plans

Plans:
- [ ] 02-01-PLAN.md — Parameterize outside-option utility + create 5 YAML study manifests + suite (Wave 1)
- [ ] 02-02-PLAN.md — Run outside-option scan suite + build artifact table (Wave 2, depends on 02-01)
- [ ] 02-03-PLAN.md — Literature-bounded calibration text, Table 2 update, results.tex outside-option subsection (Wave 3, depends on 02-02)

### Phase 3: Filter Validity Diagnostics

**Goal:** Add quantile errors, filtering-decision diagnostics, and false-negative breakdowns for ETA/IVT filtering.
**Depends on:** Phase 2
**Requirements:** [FILT-01, FILT-02, FILT-03]
**Canonical refs:**
- `review_ServiceMenuDRT_round2_202605142050.md` - Round 2 filter-validity blocker.
- `ooh_code/run_menu_compare.py` - Existing metric logging and episode outputs.
- `ooh_code/Src/research_pipeline.py` - Aggregation pipeline.
- `ooh_code/scripts/extract_phase22_results.py` and `ooh_code/scripts/extract_phase28_results.py` - Existing filter-validity extractors.
- `ooh_code/scripts/build_artifacts.py` - Artifact table generation.
- `ooh_code/artifacts/tables/filter_validity_summary.tex` - Existing MAE/bias table.

**Success Criteria** (what must be TRUE):
1. Filter-validity artifacts report P50, P90, and P95 ETA/IVT errors.
2. Filtering diagnostics quantify a realized-feasibility or best-available proxy for filtered bundles.
3. False-negative pruning is broken down by at least one operationally meaningful logged dimension.
4. The manuscript explains why the remaining filtering evidence is sufficient or clearly limits the claim.

**Plans:** 3 plans

Plans:
- [ ] 03-01: Quantile error logging and artifact extraction.
- [ ] 03-02: Filtering-decision feasibility proxy and false-negative breakdown.
- [ ] 03-03: Filter-validity manuscript integration.

### Phase 4: Evidence Synthesis and Behavioral Interpretation

**Goal:** Reconcile pricing, uptake, acceptance, surplus, and operational-value claims into one cautious results narrative.
**Depends on:** Phase 3
**Requirements:** [SYN-01]
**Canonical refs:**
- `review_ServiceMenuDRT_round2_202605142050.md` - Round 2 behavioral-fragility and pricing-tradeoff comments.
- `ooh_code/manuscript/sections/results.tex` - Main quantitative synthesis.
- `ooh_code/manuscript/sections/managerial.tex` - Managerial interpretation.
- `ooh_code/manuscript/sections/limitations.tex` - Evidence-boundary language.
- `ooh_code/artifacts/tables/phase31_uptake_menu_value_summary.tex` - Uptake/pricing comparison.
- `ooh_code/artifacts/tables/profit_decomposition_summary.tex` - Profit-channel decomposition.
- `ooh_code/artifacts/tables/rc_main_optout_welfare_table.tex` - Welfare table.

**Success Criteria** (what must be TRUE):
1. Flat-markdown versus Lambert-W results are framed as regime-specific tradeoffs.
2. Acceptance, non-home uptake, all-request surplus, and accepted-user surplus are interpreted together.
3. Near-zero acceptance regimes are treated as mechanism diagnostics, not operational-value proof.
4. The final narrative makes the paper's strongest defensible TR-E claim clear.

**Plans:** 2 plans

Plans:
- [ ] 04-01: Pricing, uptake, and welfare synthesis rewrite.
- [ ] 04-02: Managerial and limitations alignment.

### Phase 5: Polish, QA, and Round 2 Traceability

**Goal:** Remove remaining polish issues, compile, verify references/artifacts, and prepare the Round 2 response matrix.
**Depends on:** Phase 4
**Requirements:** [TEXT-01, QA-01]
**Canonical refs:**
- `review_ServiceMenuDRT_round2_202605142050.md` - Round 2 polish and verdict.
- `ooh_code/manuscript/main.tex` - Final compile target.
- `ooh_code/manuscript/sections/` - Manuscript-facing source files.
- `ooh_code/manuscript/references.bib` - Citation target.
- `ooh_code/artifacts/tables/` - Artifact table directory.
- `.planning/ROADMAP.md` and `.planning/REQUIREMENTS.md` - v1.1 traceability sources.

**Success Criteria** (what must be TRUE):
1. Manuscript-facing files decode cleanly and contain no mojibake or stale internal project language.
2. `main.tex` compiles or all remaining build issues are documented with exact causes.
3. All referenced tables, figures, labels, and citations resolve.
4. A Round 2 response matrix maps every blocker to manuscript/evidence changes or explicit limitations.
5. Final readiness is reassessed against the Round 2 6/10 verdict.

**Plans:** 2 plans

Plans:
- [ ] 05-01: Encoding, labels, captions, references, and compile QA.
- [ ] 05-02: Round 2 response matrix and final readiness reassessment.

## Progress

**Execution Order:** Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 -> Phase 5

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Operational Baseline Integration | v1.1 | 0/2 | Complete | 2026-05-14 |
| 2. Demand Calibration and Outside-Option Sensitivity | v1.1 | 0/3 | Planning complete | - |
| 3. Filter Validity Diagnostics | v1.1 | 0/3 | Not started | - |
| 4. Evidence Synthesis and Behavioral Interpretation | v1.1 | 0/2 | Not started | - |
| 5. Polish, QA, and Round 2 Traceability | v1.1 | 0/2 | Not started | - |
