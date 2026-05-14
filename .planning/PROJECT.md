# ServiceMenuDRT Paper Revision

## What This Is

This project manages the revision of the manuscript `ooh_code/manuscript/main.tex` for a Transportation Research Part E submission. The current milestone converts the Round 2 review findings in `review_ServiceMenuDRT_round2_202605142050.md` into targeted evidence and manuscript revisions intended to move the paper from borderline 6/10 to submission-ready.

## Core Value

Produce a TR Part E-ready revision whose demand calibration, filter-validity evidence, operational-baseline integration, and manuscript polish are strong enough to withstand a critical transportation-operations review.

## Current Milestone: v1.1 TR-E Submission Risk Closure

**Goal:** Close the Round 2 blockers that keep the revised manuscript at 6/10: external demand calibration, filter validity, operational-baseline integration, behavioral interpretation, and final polish.

**Target features:**
- Integrate the existing DRT operational baselines into the Method, Results, and evidence hierarchy so they function as review-facing evidence.
- Add an explicit outside-option and MNL calibration/sensitivity layer anchored to plausible parameter ranges from DRT and travel-behavior literature.
- Strengthen filter validity with ETA/IVT error quantiles, filtering-decision diagnostics, and false-negative breakdowns where the logged data supports them.
- Reconcile high-uptake, pricing, welfare, and acceptance tradeoffs so profit improvements are not overread as service-quality improvements.
- Remove remaining encoding/polish issues and finish a fresh compile, traceability, and Round 3 readiness check.

## Requirements

### Validated

- [v1.0] CLAIM-01: Paper claims are reframed as diagnostic/exploratory unless evidence supports stronger language.
- [v1.0] THEORY-01: Lambert-W pricing is rewritten as a bounded reference transform, not a core optimality contribution.
- [v1.0] STAT-01: City and RC inference are presented with conservative split-level language.
- [v1.0] WELF-01: Profit, acceptance, and passenger welfare tradeoffs are decomposed.

### Active

- [ ] BASE-01: Operational baselines are described in the empirical-policy taxonomy and interpreted in the main evidence narrative.
- [ ] BASE-02: The operational-baseline table is placed where reviewers will see it and is explicitly connected to transportation-operations relevance.
- [ ] CAL-01: Outside-option utility sensitivity is implemented or otherwise produced as a concrete table/figure, not only discussed as a limitation.
- [ ] CAL-02: MNL parameter ranges are tied to cited DRT, stated-preference, or travel-behavior literature where possible.
- [ ] CAL-03: Demand-calibration claims clearly distinguish literature-bounded stress testing from external validation.
- [ ] FILT-01: Deployed ETA/IVT validation reports P50, P90, and P95 error diagnostics in addition to MAE and bias.
- [ ] FILT-02: Filtering-decision diagnostics quantify how many filtered bundles appear feasible under the realized or best-available feasibility proxy.
- [ ] FILT-03: False-negative pruning is broken down by meeting-point type, walking-distance band, or another logged operational dimension.
- [ ] SYN-01: High-uptake, flat-markdown, Lambert-W, acceptance, and surplus results are interpreted as tradeoffs rather than policy dominance.
- [ ] TEXT-01: Remaining mojibake, stale README/caption language, and internal project terminology are removed from manuscript-facing files.
- [ ] QA-01: Final manuscript compiles, references and artifacts resolve, and a Round 2 response matrix maps every blocker to evidence or a documented limitation.

### Out of Scope

- Full city-scale external validation campaign with many new Austin/Seattle splits. Round 2 says this remains desirable, but the v1.1 milestone focuses on submission-risk closure using feasible targeted evidence.
- Real revealed-preference or survey-data estimation. The milestone can cite plausible ranges and run sensitivity, but it cannot create new primary demand data.
- Re-promoting Lambert-W as a theoretical contribution. The v1.0 demotion remains a settled decision.

## Context

Primary manuscript entrypoint: `ooh_code/manuscript/main.tex`, with sections included from `ooh_code/manuscript/sections/`.

Authoritative Round 2 review source: `review_ServiceMenuDRT_round2_202605142050.md`.

Previous review source: `review_ServiceMenuDRT_202605141407.md`.

v1.0 moved the score from 5/10 to 6/10 by improving claim framing, Lambert-W positioning, conservative statistics, MNL stress tests, welfare interpretation, and QA. Round 2 still identifies three major blockers: external demand calibration, filter validity, and operational-baseline integration. It also flags behavioral fragility, limited city evidence, and possible remaining mojibake/polish issues.

## Constraints

- Do not undo v1.0's diagnostic/exploratory framing.
- Treat Austin/Seattle as descriptive unless a later milestone adds substantially more splits.
- Use existing code and logged artifacts where possible; add pipeline fields only where needed for Round 2 blockers.
- Keep manuscript-facing source clean UTF-8 and avoid adding new mojibake.
- Preserve user/unrelated workspace changes; do not reset or revert broad worktree state.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Use `review_ServiceMenuDRT_round2_202605142050.md` as the v1.1 source review | It is the latest structured reassessment and directly explains why the paper remains 6/10 | Active |
| Keep v1.1 targeted rather than full external validation | Round 2 blockers can be substantially reduced by outside-option sensitivity, filter diagnostics, and better integration | Active |
| Reset phase numbering to 1-5 after archiving v1.0 | The v1.0 phase directories were archived by `gsd milestone complete v1.0 --archive-phases` | Active |
| Operational baseline integration comes before new experiments | Existing baseline evidence is already available but underused in the manuscript | Active |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition**:
1. Requirements invalidated? Move to Out of Scope with reason.
2. Requirements validated? Move to Validated with phase reference.
3. New requirements emerged? Add to Active.
4. Decisions to log? Add to Key Decisions.
5. "What This Is" still accurate? Update if drifted.

**After each milestone**:
1. Full review of all sections.
2. Core Value check - still the right priority?
3. Audit Out of Scope - reasons still valid?
4. Update Context with current state.

---
*Last updated: 2026-05-14 after v1.1 milestone initialization*
