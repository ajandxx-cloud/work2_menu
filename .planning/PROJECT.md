# ServiceMenuDRT Paper Revision

## What This Is

This project manages the revision of the manuscript `ooh_code/manuscript/main.tex` for a Transportation Research Part E submission. The current milestone converts the latest 6.5/10 review in `review_ServiceMenuDRT_round2b_202605151030.md` into a focused final-tightening roadmap.

## Core Value

Produce a TR Part E-ready revision that is honest about remaining empirical limits while removing avoidable wording, filter-validity, baseline-scope, and PDF-polish risks before submission.

## Current Milestone: v1.2 Final Tightening for TR-E Submission

**Goal:** Move the paper from "borderline major-revision-ready" toward submission-preparable by tightening claims, clarifying large filter errors, optionally strengthening operational baselines in behaviorally live regimes, and completing compiled-PDF polish.

**Target features:**
- Soften outside-option sensitivity claims so they read as RC stress-test robustness, not external demand stability.
- Add an explicit explanation or limitation for large ETA/IVT errors and their implications for filtering credibility.
- Decide whether to run medium/high-uptake operational baselines; if feasible, add them as stronger review-facing evidence.
- Verify final typography and encoding in the compiled PDF, especially dash characters and manuscript-facing polish.
- Prepare a final response matrix that maps the 6.5/10 review comments to the final tightening changes.

## Requirements

### Validated

- [v1.0] CLAIM-01: Paper claims are reframed as diagnostic/exploratory unless evidence supports stronger language.
- [v1.0] THEORY-01: Lambert-W pricing is rewritten as a bounded reference transform, not a core optimality contribution.
- [v1.1] BASE-01: Operational baselines are integrated into method/results narrative.
- [v1.1] CAL-01: Outside-option utility scan exists as a concrete artifact.
- [v1.1] FILT-01: Filter validity reports quantile diagnostics and false-negative breakdowns.
- [v1.1] SYN-01: Pricing, uptake, acceptance, and surplus are interpreted as tradeoffs.

### Active

- [ ] CLAIM-02: Outside-option scan language is softened to "not obviously brittle within this RC stress test" rather than "stable across demand assumptions."
- [ ] FILT-04: Manuscript explains why large ETA/IVT errors do not fully invalidate the filtering diagnostic, or explicitly names them as a key limitation.
- [ ] BASE-03: A feasibility decision is made for medium/high-uptake operational-baseline reruns, with either new evidence or a documented deferral.
- [ ] BASE-04: If rerun evidence is feasible, operational-baseline results are extended beyond RC low uptake and integrated into the manuscript.
- [ ] PDF-01: Compiled PDF is checked for dash/encoding/polish issues, not only raw LaTeX source.
- [ ] QA-02: A final response matrix maps the 6.5/10 review to completed changes, remaining limits, and submission readiness.

### Out of Scope

- Full external demand validation with new survey or revealed-preference estimation. The latest review accepts that this remains unresolved but asks for careful framing.
- Large city-scale external validation expansion. Austin/Seattle remain descriptive unless a separate future milestone expands them.
- Reworking the whole paper narrative again. v1.2 is a final tightening pass, not another broad revision.

## Context

Primary manuscript entrypoint: `ooh_code/manuscript/main.tex`, with sections included from `ooh_code/manuscript/sections/`.

Authoritative latest review source: `review_ServiceMenuDRT_round2b_202605151030.md`.

Previous review source: `review_ServiceMenuDRT_round2_202605142050.md`.

The latest review scored the manuscript 6.5/10. It acknowledged that v1.1 materially improved operational-baseline integration, outside-option scanning, filter diagnostics, and tradeoff framing. The remaining requested work is narrower: soften outside-option claims, handle large ETA/IVT errors explicitly, verify PDF polish, and optionally rerun operational baselines in medium/high uptake to make them more persuasive.

## Constraints

- Keep the diagnostic/exploratory framing from v1.0 and v1.1.
- Do not claim true external demand validation.
- Treat medium/high operational-baseline reruns as optional and decision-gated because they may require nontrivial experiment time.
- Preserve existing user and generated changes; do not reset the broad dirty worktree.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Use `review_ServiceMenuDRT_round2b_202605151030.md` as the v1.2 source review | It is the newest structured reassessment and scored the latest manuscript 6.5/10 | Active |
| Keep v1.2 to a final-tightening milestone | Latest review asks for targeted wording, limitation, optional evidence, and PDF checks rather than another broad rewrite | Active |
| Make operational-baseline reruns decision-gated | The review says "if time permits"; the plan should first assess feasibility before committing to long runs | Active |

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
*Last updated: 2026-05-15 after v1.2 milestone initialization*
