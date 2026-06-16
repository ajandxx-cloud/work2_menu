---
phase: 11
status: claim_boundary_plan
generated_at: 2026-06-16T14:11:38+08:00
timezone: Asia/Shanghai
runtime_root: work2_coding/
source_package:
  - work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/
  - artifacts/work2_robust_menu/phase10_paper_artifacts/
claim_guard_schema: phase10-strict-claim-guard-v1
phase10_claim_count: 8
claim_ready: false
manuscript_positive_claims_allowed: false
---

# TR Part E Manuscript Structure And Claim Boundary Plan

## Phase 11 Scope Lock

Phase 11 is a writing and claim-boundary planning phase only. It does not run
new experiments, tune parameters, regenerate empirical rows, hand-edit evidence
tables, or upgrade any paper claim. The strict Phase 10 `CLAIM_GUARD.json`
remains the controlling evidence boundary: eight claims were evaluated,
overall `claim_ready=false`, and positive empirical manuscript claims are not
authorized.

Allowed manuscript work in this phase:

- define the TR Part E manuscript structure;
- identify where artifact-backed status, diagnostic, and scaffold material can
  be discussed;
- state what must not be claimed until future gates pass;
- map tables and figures to Phase 10 package entries only.

Disallowed manuscript work in this phase:

- state or imply that the optimized adaptive service menu is empirically
  superior to all baselines;
- state or imply that product, adaptive-window, menu-construction, or
  exact-greedy claims are claim-ready;
- treat diagnostic Phase 8 or Phase 9 outputs as formal evidence;
- describe the semi-real case scaffold as validation or as real passenger
  behavior;
- recommend no-filter operation as a deployable policy.

## Global Claim Ceiling

The manuscript may be structured as a TR Part E service-menu optimization paper,
but its empirical voice must stay claim-safe.

Current permitted claim ceiling:

- **Supported:** provenance, status, artifact indexing, and claim-gate
  transparency only.
- **Diagnostic/provisional:** ETA robustness boundaries, sensitivity patterns,
  and computational diagnostics may be described as diagnostic evidence only.
- **Unsupported or blocked:** central superiority, product ablation value,
  adaptive-window increment, menu-construction value, exact-greedy
  computational credibility, and semi-real case validation.

## Manuscript Outline

### 1. Introduction

Purpose:

- motivate dynamic service menu optimization for many-to-one DRT and last-mile
  service operations;
- frame the displayed service menu as bundles of meeting point, pickup time
  window, and price;
- explain that the paper studies an artifact-gated framework for comparing
  service-menu policies under paired replay;
- set up a conditional, claim-bounded contribution rather than a universal
  superiority story.

Can be claimed:

- the project targets dynamic service menu optimization rather than an
  attention-model or pricing-only paper;
- the manuscript studies service bundles `m+w+p`, accepted home service, and
  the outside option as separate modeling objects;
- the current artifact package makes claim boundaries explicit and traceable.

Cannot be claimed:

- that the adaptive robust menu dominates baselines;
- that the method is claim-ready for abstract or conclusion-level empirical
  superiority;
- that Phase 8 or Phase 9 diagnostics establish formal robustness or
  computational credibility;
- that the semi-real case validates findings.

Writing plan:

- Use a cautious contribution paragraph: "We formulate and evaluate a
  claim-gated service-menu optimization framework." Avoid positive performance
  verbs unless the sentence is explicitly about diagnostic or status artifacts.
- State early that generated evidence is currently blocked for positive
  empirical claims, so the paper is organized as a claim-bounded manuscript
  plan unless future readiness gates pass.

### 2. Literature Review

Purpose:

- position the work within DRT operations, service design, passenger choice,
  pickup time-window design, pricing, and online menu or assortment
  optimization;
- explain why menu design is a natural front-end decision layer for many-to-one
  DRT;
- separate this V1 contribution from attention-based choice or scoring.

Can be claimed:

- the manuscript connects DRT service design with menu/assortment-style
  service-product decisions;
- the V1 scope is service-menu optimization with explicit opt-out accounting;
- attention-based choice or scoring remains outside the V1 contribution.

Cannot be claimed:

- that the current empirical package closes all gaps in the literature;
- that real passenger behavior has been validated;
- that the framework has externally validated operational performance.

Writing plan:

- Use literature review language to motivate modeling choices, not to import
  empirical claims that the package does not support.
- Keep statements about novelty qualitative and structural, such as the joint
  treatment of meeting point, pickup window, and price in the displayed menu.

### 3. Problem Description

Purpose:

- define the many-to-one DRT setting, sequential request arrival, current fleet
  state, candidate meeting points, time windows, prices, and the outside option;
- define accepted home pickup and accepted meeting-point pickup as service
  outcomes;
- keep opt-out/lost demand separate from accepted home service.

Can be claimed:

- a displayed service bundle is `(meeting point, pickup time window, price)`;
- accepted home pickup is an accepted service bundle, while the outside option
  is refusal or lost demand;
- acceptance, home-service share, meeting-point uptake, and opt-out must be
  reported as separate accounting categories.

Cannot be claimed:

- that simulated choice outcomes are observed passenger behavior;
- that opt-out is equivalent to accepted home pickup;
- that scaffold-only case materials provide real-world validation.

Writing plan:

- Include a precise service-outcome taxonomy before any metric discussion.
- Use notation and definitions from `.planning/paper/TR_E_RESEARCH_DESIGN.md`,
  but do not add new behavioral assumptions beyond the Phase 10 package.

### 4. Model

Purpose:

- present the mathematical service-menu model: requests, vehicles, candidate
  points, feasible bundles, menu decision variables, passenger choice
  probabilities, expected profit, service guardrails, and ETA/window
  feasibility;
- define exact and greedy menu construction contracts at the model level.

Can be claimed:

- the model provides a paper-level formulation of sequential menu selection
  with service bundles and outside option;
- expected profit can be written with acceptance probabilities, revenue/cost
  terms, opt-out penalties, ETA risk, and service guardrails;
- exact enumeration is a small-candidate benchmark and greedy construction is
  a planned scalable heuristic.

Cannot be claimed:

- that the solved policy is globally optimal for the full dynamic stochastic
  system;
- that greedy selection is near-optimal or optimal;
- that the passenger-choice model is calibrated to real passenger observations.

Writing plan:

- Keep the model section claim-neutral and implementation-aligned.
- Use "formulate", "define", and "evaluate under diagnostic gates" rather
  than "prove effectiveness" or "validate superiority".

### 5. Solution Method

Purpose:

- describe how candidate service bundles are scored and selected;
- describe exact small-candidate enumeration, greedy fallback contract,
  adaptive/fixed window variants, pricing mode, and ETA filter modes;
- identify required diagnostics: candidate count, enumerated menu count,
  build time, fallback reason, gap and overlap when available.

Can be claimed:

- the solution method is auditable through generated artifact/status fields;
- Phase 9 generated diagnostic rows for candidate count, enumerated menu count,
  and menu build time;
- Phase 9 did not establish greedy fallback quality because configured large
  scales still used the effective exact solver.

Cannot be claimed:

- near-optimal greedy behavior;
- full dynamic exact optimality;
- online tractability as a claim-ready result;
- adaptive-window or menu-construction value as validated.

Writing plan:

- Present solver logic as method design plus diagnostics.
- In computational paragraphs, state that current evidence is diagnostic and
  that gap/overlap evidence is unavailable or blocked where Phase 9 says so.

### 6. Experimental Design

Purpose:

- define the RC replay benchmark, seven-tag policy family, paired fairness
  requirements, metrics, and artifact gates;
- define Phase 8 sensitivity axes and Phase 9 computational diagnostics;
- explain that Phase 7 semi-real case work is scaffold-only.

Can be claimed:

- the comparison design includes seven mainline policy tags:
  `mainline_no_menu`, `mainline_fixed_menu`, `mainline_random_menu`,
  `mainline_optimized_m`, `mainline_optimized_mw`,
  `mainline_optimized_fixed_window`, and `mainline_optimized_adaptive`;
- paired replay fairness requires shared split, seed/request trace,
  checkpoint provenance, pricing settings, routing settings, and artifact
  status;
- Phase 8 covers diagnostic sensitivity axes for `menu_k`, ETA filter mode,
  uptake regime, and guardrail;
- Phase 9 covers diagnostic tractability rows but not successful greedy
  fallback evidence.

Cannot be claimed:

- that formal empirical claims are ready;
- that diagnostic sensitivity is a formal robustness proof;
- that the case scaffold is an external validation study;
- that any generated row or table may be manually edited for manuscript use.

Writing plan:

- Make the claim gate part of the experimental design, not a footnote.
- Use a dedicated subsection for "Evidence tiers and claim gates" with Phase
  10 package status.

### 7. Results

Purpose:

- report only what the Phase 10 package authorizes: status/provenance,
  blocked main RC claim surfaces, diagnostic Phase 8 sensitivity boundaries,
  diagnostic Phase 9 tractability boundaries, and scaffold-only case status.

Can be claimed:

- Phase 10 indexes 74 unique source artifacts and mirrors the package under
  both runtime and root artifact paths;
- `CLAIM_GUARD.json` evaluates eight claims and keeps overall
  `claim_ready=false`;
- Phase 8 diagnostic results identify boundary patterns, such as lower profit
  at `menu_k=2` and `menu_k=4` relative to center `3`, no observed ETA filter
  changes across listed modes, lower profit under low uptake, and no observed
  change from guardrail `0.40` relative to `0.35`;
- Phase 9 diagnostic results report 15 completed rows, effective exact solver
  use at configured scales 8, 12, and 16, and unavailable gap/overlap evidence.

Cannot be claimed:

- adaptive menu superiority;
- product ablation proof;
- adaptive-window advantage;
- menu-construction value;
- claim-ready computational credibility;
- case-study validation.

Writing plan:

- Lead with a claim-gate table before numerical or diagnostic material.
- Use "diagnostic boundary", "observed in this diagnostic package", and
  "not claim-ready" wherever Phase 8 or Phase 9 evidence is discussed.
- Put blocked main RC result artifacts in a status subsection, not a positive
  result subsection.

### 8. Discussion

Purpose:

- interpret why the claim guard blocks positive empirical claims;
- explain reviewer risks, such as readiness blockers, checkpoint provenance,
  diagnostic-only sensitivity, and unavailable exact-vs-greedy quality;
- describe the conditional paper path if future gates pass.

Can be claimed:

- the current package supports transparent claim gating;
- the manuscript should be framed as conditional and diagnostic unless future
  formal gates pass;
- the semi-real case material is useful as reproducibility scaffold for future
  execution, not as validation.

Cannot be claimed:

- that provenance transparency resolves empirical blockers;
- that diagnostic boundary findings imply deployment recommendations;
- that a no-filter policy should be deployed;
- that case-study scaffold materials validate operational claims.

Writing plan:

- Include a reviewer-risk subsection with explicit mitigation: future formal
  readiness, checkpoint hash/sidecar resolution, claim-ready regenerated
  artifacts, and real or clearly semi-real case execution before validation
  language.

### 9. Conclusion

Purpose:

- conclude the claim-safe manuscript plan;
- restate the structural contribution and the current evidence boundary;
- identify next steps for claim-ready manuscript conversion.

Can be claimed:

- the paper structure and package support transparent, artifact-backed writing;
- claim-ready empirical conclusions remain blocked until strict gates pass;
- the current contribution is a service-menu optimization formulation and
  claim-gated evidence package, not an empirical dominance result.

Cannot be claimed:

- that optimized adaptive `m+w+p` service menus improve, dominate, or validate
  performance in a claim-ready way;
- that diagnostics authorize operational policy prescriptions;
- that the manuscript is final submission-ready.

Writing plan:

- Avoid directional performance language in the final paragraph.
- End with the evidence gate: future work must resolve formal readiness,
  provenance, artifact status, and strict claim guard blockers before stronger
  claims can enter the abstract or conclusion.

### 10. Appendix

Purpose:

- hold the Phase 10 package index, claim guard, source map, diagnostic
  sensitivity outputs, diagnostic tractability outputs, case-study scaffold
  inventory, and prohibited-language checklist.

Can be claimed:

- appendix materials document source paths, artifact tiers, claim status, and
  blocker reasons;
- diagnostic appendices can preserve Phase 8 and Phase 9 findings without
  upgrading them;
- scaffold appendices can document future case-study preparation.

Cannot be claimed:

- appendix placement upgrades claim readiness;
- missing, blocked, scaffold-only, or diagnostic artifacts support positive
  empirical claims;
- manually edited evidence tables are acceptable.

Writing plan:

- Include only generated or indexed artifact paths from the Phase 10 package.
- Label each appendix table or figure with `claim_ready=false` unless it is
  strictly about C7 provenance/status transparency.

## Reviewer-Risk Register

| Risk | Why it matters | Safe manuscript handling |
| --- | --- | --- |
| Main RC artifacts are blocked | Positive central results cannot enter abstract or conclusion | Treat main RC tables as status or blocked evidence only |
| Phase 8 is diagnostic | Sensitivity patterns are useful but not claim-ready | Put sensitivity in diagnostic results or appendix |
| Phase 9 did not trigger greedy fallback | Exact-vs-greedy quality is unavailable | Report build-time diagnostics and blocked gap/overlap only |
| Case study is scaffold-only | No external validation claim is authorized | Move case material to appendix/future study scaffold |
| Opt-out accounting can be confused with home service | Service metrics depend on clean outcome taxonomy | Define outside option separately before results |
| No-filter can be misread as recommendation | Diagnostic stress tests can sound operational | Call no-filter diagnostic only in every reference |

## Phase 12 Handoff Criteria

Before any final TR Part E readiness review upgrades claims, the project must
have evidence that:

- formal readiness and checkpoint provenance are resolved;
- generated rows and artifact status are claim-ready;
- strict claim guard permits the specific manuscript claims;
- Phase 8 and Phase 9 diagnostic boundaries are either upgraded by new gated
  evidence or left as diagnostic appendices;
- any case-study language is backed by executed, reproducible case evidence and
  clearly labels simulated demand and choice behavior.
