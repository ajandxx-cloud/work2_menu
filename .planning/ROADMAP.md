# Roadmap: ServiceMenuDRT Paper Revision

## Roadmap v1.2: Final Tightening for TR-E Submission

**Milestone Goal:** Move the paper from "borderline major-revision-ready" toward submission-preparable by tightening claims, clarifying large filter errors, optionally strengthening operational baselines in behaviorally live regimes, and completing compiled-PDF polish.

## Overview

This roadmap converts the latest 6.5/10 review in `review_ServiceMenuDRT_round2b_202605151030.md` into a compact final-tightening milestone. The work first removes avoidable claim and filter-reliability risk, then decides whether operational baselines can be extended to medium/high uptake, and finishes with compiled-PDF QA plus a final response matrix.

## Phases

**Phase Numbering:**
- Phase numbering resets for this milestone after v1.1 phase directories were archived.
- Integer phases 1-3 are planned milestone work.
- Decimal phases are reserved for urgent insertions if later needed.

- [ ] **Phase 1: Claim and Filter-Reliability Tightening** - Soften outside-option claims and directly address large ETA/IVT errors.
- [ ] **Phase 2: Operational-Baseline Uptake Decision** - Decide whether to rerun operational baselines in medium/high uptake and integrate or document the outcome.
- [ ] **Phase 3: PDF Polish and Final Response** - Verify compiled PDF polish and prepare final traceability/readiness artifacts.

## Phase Details

### Phase 1: Claim and Filter-Reliability Tightening

**Goal:** Soften outside-option claims and directly address large ETA/IVT errors.
**Depends on:** Nothing (first phase)
**Requirements:** [CLAIM-02, FILT-04]
**Canonical refs:**
- `review_ServiceMenuDRT_round2b_202605151030.md` - Latest 6.5/10 review and actionable fixes.
- `ooh_code/manuscript/sections/results.tex` - Outside-option scan and filter-validity discussion.
- `ooh_code/manuscript/sections/limitations.tex` - Demand and filter reliability limitations.
- `ooh_code/artifacts/tables/outside_option_scan_summary.tex` - Outside-option scan artifact.
- `ooh_code/artifacts/tables/filter_validity_summary.tex` - Quantile and false-negative diagnostics.

**Success Criteria** (what must be TRUE):
1. Outside-option scan language avoids broad "stable across demand assumptions" claims.
2. Results or limitations explains that the scan shows "not obvious brittleness within the RC stress test."
3. The manuscript explicitly states how large ETA/IVT errors affect the filter diagnostic interpretation.
4. The final filter claim remains useful but bounded.

**Plans:** 2 plans

Plans:
- [ ] 01-01: Outside-option claim softening.
- [ ] 01-02: Large ETA/IVT error interpretation and limitation.

### Phase 2: Operational-Baseline Uptake Decision

**Goal:** Decide whether to rerun operational baselines in medium/high uptake and integrate or document the outcome.
**Depends on:** Phase 1
**Requirements:** [BASE-03, BASE-04]
**Canonical refs:**
- `review_ServiceMenuDRT_round2b_202605151030.md` - Optional "if time permits" operational-baseline rerun suggestion.
- `ooh_code/experiments/studies/phase32_operational_baselines.yaml` - Existing RC low-uptake operational-baseline study.
- `ooh_code/experiments/studies/phase31_uptake_menu_value_medium.yaml` - Existing medium-uptake configuration reference.
- `ooh_code/experiments/studies/phase31_uptake_menu_value_high.yaml` - Existing high-uptake configuration reference.
- `ooh_code/scripts/run_study.py` and `ooh_code/scripts/build_artifacts.py` - Study execution and artifact generation.
- `ooh_code/manuscript/sections/results.tex` - Integration point if new evidence is generated.

**Success Criteria** (what must be TRUE):
1. Feasibility is assessed from existing manifests and expected runtime before launching reruns.
2. If reruns are feasible, medium/high operational-baseline artifacts are generated and integrated.
3. If reruns are not feasible, the manuscript or response matrix documents why low-uptake baseline evidence is the available scope.
4. The operational-baseline claim does not overgeneralize beyond the tested uptake regimes.

**Plans:** 2 plans

Plans:
- [ ] 02-01: Medium/high operational-baseline feasibility and manifest plan.
- [ ] 02-02: Execute feasible reruns or document deferral, then integrate evidence/limitation.

### Phase 3: PDF Polish and Final Response

**Goal:** Verify compiled PDF polish and prepare final traceability/readiness artifacts.
**Depends on:** Phase 2
**Requirements:** [PDF-01, QA-02]
**Canonical refs:**
- `review_ServiceMenuDRT_round2b_202605151030.md` - Latest review source.
- `ooh_code/manuscript/main.tex` - Final compile target.
- `ooh_code/manuscript/main.pdf` - Rendered PDF output.
- `ooh_code/manuscript/sections/` - Manuscript-facing source files.
- `ooh_code/artifacts/tables/` - Artifact table directory.
- `.planning/ROADMAP.md` and `.planning/REQUIREMENTS.md` - v1.2 traceability sources.

**Success Criteria** (what must be TRUE):
1. Compiled PDF is checked for dash characters, mojibake, missing tables, and obvious rendering polish issues.
2. LaTeX compile status is documented with exact warnings/errors if any remain.
3. All referenced artifacts, labels, and citations resolve or remaining issues are explicitly listed.
4. A v1.2 response matrix maps every 6.5/10 review action item to changes, deferrals, and final readiness.

**Plans:** 2 plans

Plans:
- [ ] 03-01: Compiled PDF and LaTeX polish QA.
- [ ] 03-02: Final response matrix and submission-readiness reassessment.

## Progress

**Execution Order:** Phase 1 -> Phase 2 -> Phase 3

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Claim and Filter-Reliability Tightening | v1.2 | 0/2 | Not started | - |
| 2. Operational-Baseline Uptake Decision | v1.2 | 0/2 | Not started | - |
| 3. PDF Polish and Final Response | v1.2 | 0/2 | Not started | - |
