---
phase: 12
status: final_readiness_review
generated_at: 2026-06-16T14:22:51+08:00
timezone: Asia/Shanghai
runtime_root: work2_coding/
recommendation: draftable_only_as_conditional_diagnostic_paper
claim_guard_schema: phase10-strict-claim-guard-v1
phase10_claim_count: 8
claim_ready: false
manuscript_positive_claims_allowed: false
---

# TR-E Readiness Review

## Scope Lock

This is a final readiness audit for the Work2 TR-E service-menu optimization
paper. It does not run experiments, tune parameters, regenerate empirical rows,
or upgrade any claim beyond the Phase 10 strict `CLAIM_GUARD.json` result.

The controlling evidence boundary is:

- Phase 10 `CLAIM_GUARD.json` has 8 claims.
- Overall `claim_ready=false`.
- `manuscript_positive_claims_allowed=false`.
- Only C7 provenance/status transparency is supported, and only for that
  narrow status claim.
- Phase 8 and Phase 9 remain diagnostic/provisional.
- Phase 10 is paper-artifact packaging and strict claim guarding, not empirical
  claim approval.

## Inputs Audited

- `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`,
  `.planning/ROADMAP.md`, `.planning/STATE.md`
- `.planning/research/SUMMARY.md` and `.planning/codebase/` context maps,
  with stale `ooh_code/` references interpreted through the verified
  `work2_coding/` runtime root.
- `.planning/paper/TR_E_RESEARCH_DESIGN.md`,
  `.planning/paper/TR_E_MANUSCRIPT_STRUCTURE.md`,
  `.planning/paper/CLAIM_SAFE_LANGUAGE.md`, and
  `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md`
- `.planning/results/RC_FORMAL_DIAGNOSIS.md`,
  `.planning/results/SENSITIVITY_SUMMARY.md`,
  `.planning/results/COMPUTATIONAL_TRACTABILITY_SUMMARY.md`,
  `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md`,
  `.planning/results/FORMAL_FAILURE_DIAGNOSIS.md`, and
  `.planning/results/FROZEN_FINAL_SETTINGS.md`
- `.planning/phases/10-paper-artifact-generation/10-REVIEW.md`,
  `.planning/phases/10-paper-artifact-generation/10-VERIFICATION.md`, and
  `.planning/phases/11-manuscript-structure-and-writing-plan/11-RESULT_MANIFEST.md`
- Mirrored Phase 10 paper packages under
  `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/` and
  `artifacts/work2_robust_menu/phase10_paper_artifacts/`

## 1. Novelty And TR-E Positioning

The paper remains thematically plausible for Transportation Research Part E if
it is positioned as service operations and transportation optimization, not as
an attention model paper and not as a pricing-only extension. The strongest
novelty is the operational framing of the displayed service menu as a
front-end decision object in many-to-one DRT:

```text
(meeting point, pickup time window, price)
```

This framing is TR-E relevant because it links service design, passenger choice,
route/capacity feasibility, time-window risk, and platform profit in a single
sequential decision layer. The artifact-gated claim discipline is also a useful
research-process contribution because it prevents simulated or diagnostic rows
from being promoted into stronger claims.

The current limitation is that novelty is mostly structural and methodological.
The empirical package does not yet support a positive TR-E performance story.
The central superiority claim is blocked and the formal diagnosis shows mixed
profit-service trade-offs, including better service metrics in some comparisons
but no universal profit dominance. Therefore, the paper should not be pitched as
"a new menu algorithm that outperforms baselines." The viable pitch is narrower:
a formulation, implementation, and diagnostic evidence package for understanding
when optimized service-menu design helps or fails.

## 2. Modeling Rigor

The modeling skeleton is strong enough for manuscript drafting. It defines
requests, vehicles, candidate meeting points, feasible bundles, menu variables,
MNL choice probabilities, outside-option probability, expected profit, service
guardrails, ETA/window feasibility, and exact/greedy menu construction
contracts. It also correctly separates accepted home pickup from opt-out, which
is essential for credible service-quality accounting.

Modeling risks remain substantial:

- The passenger choice model is simulated, not calibrated to observed passenger
  behavior.
- The same or closely aligned behavioral structure can influence optimization
  and evaluation, so reviewers may challenge behavioral misspecification.
- The model does not establish full dynamic stochastic optimality; it evaluates
  online menu construction under paired replay.
- No-filter variants must remain diagnostic stress tests, not operational
  recommendations.
- The semi-real case work is scaffold-only and cannot validate behavior,
  demand, or performance.

The model section is draftable if it uses neutral verbs such as "formulate,"
"define," and "evaluate diagnostically." It is not ready for language implying
real-world behavioral validation or proven operational superiority.

## 3. Algorithmic Contribution And Limitations

The algorithmic contribution is the service-menu construction mechanism around
candidate bundles, menu size, ETA/window feasibility, service guardrails, and
Lambert-W pricing in the `mainline_optimized_adaptive` policy family. The
seven-tag comparison design gives the paper a clean decomposition of no-menu,
fixed-menu, random-menu, meeting-point-only, meeting-plus-window,
fixed-window full product, and adaptive full product variants.

The current algorithmic evidence ceiling is low:

- Phase 4 found `mainline_optimized_adaptive` does not dominate all baselines.
  `mainline_random_menu` has better mean net profit, and adaptive loses to
  random on net profit in 3 of 5 paired splits.
- `mainline_optimized_adaptive` and `mainline_optimized_fixed_window` are
  identical across tracked formal metrics, blocking any adaptive-window
  increment claim.
- Phase 9 did not establish the intended exact-vs-greedy comparison. The
  configured large scales still used the effective exact solver because
  realized candidate counts stayed below the greedy threshold.
- Relative optimality gap and menu overlap are unavailable, so greedy quality,
  near-optimality, and online scalability claims remain blocked.

The solution method can be described as auditable mechanism design plus
diagnostic computation. It cannot be described as a validated scalable heuristic
or as an empirically superior policy.

## 4. Experimental Credibility And Limitations

The experimental design has credible foundations: paired replay, shared
policy-family definitions, explicit checkpoint load status, separate opt-out
accounting, row status fields, and artifact gates. The selected formal RC run
has 35 completed comparable rows across 5 paired splits and 7 policy tags, and
the Phase 4 diagnosis uses split-level paired directions rather than headline
rankings alone.

The empirical limitations are decisive for claim readiness:

- Formal readiness and artifact status remain blocked.
- The central result is mixed: service metrics are often better for adaptive
  menus, but profit dominance is not supported.
- Five paired splits are too few for strong statistical language.
- Phase 8 sensitivity is diagnostic/provisional with `claim_ready=false`; it
  identifies boundary patterns, not formal robustness.
- Phase 9 tractability is diagnostic/provisional with `claim_ready=false`; it
  reports build-time and exact-solver diagnostics, not exact-vs-greedy quality.
- The semi-real case is scaffold-only. It is not a case study result and not an
  external validation.
- No generated result rows or paper artifacts may be hand-edited to repair these
  limitations.

The evidence can support a cautious diagnostic results section. It cannot
support an abstract-level claim that optimized adaptive `m+w+p` menus improve
overall performance.

## 5. Artifact Reproducibility And Traceability

Artifact traceability is the strongest readiness dimension. Phase 10 generated
mirrored paper packages under both runtime and root artifact paths. The audited
hashes match for `CLAIM_GUARD.json`, `PACKAGE_INDEX.json`, and
`PACKAGE_STATUS.json`. `PACKAGE_INDEX.json` has 74 entries and zero duplicate
`source_path` values. `PACKAGE_STATUS.json` reports 74 artifacts, 70 existing
artifacts, 4 missing artifacts, and 108 blockers. Source families are explicit:
6 blocker/status artifacts, 30 main RC artifacts, 14 Phase 8 sensitivity
artifacts, 12 Phase 9 tractability artifacts, and 12 case-scaffold artifacts.

The traceability limitation is that traceability does not equal claim
readiness. Main RC artifacts are blocked, Phase 8 and Phase 9 are diagnostic
appendices, and case artifacts are scaffold-only. The package is suitable for
claim-boundary-aware drafting and reviewer transparency, but it does not rescue
the empirical claims.

## 6. Claim Safety Under `claim_ready=false`

The manuscript must follow the Phase 10 strict guard exactly:

| Claim | Current status | Manuscript use |
| --- | --- | --- |
| C1 central adaptive-menu superiority | unsupported/blocked | no positive claim |
| C2 product ablation value | conditional diagnostic blocked | diagnostic structure only |
| C3 adaptive-window increment | unsupported | no directional adaptive-window claim |
| C4 menu construction value | conditional diagnostic blocked | mechanism/diagnostic structure only |
| C5 ETA robustness boundary | diagnostic only | diagnostic/no-filter stress-test wording only |
| C6 exact-greedy computational credibility | blocked diagnostic | report diagnostics only; no credibility upgrade |
| C7 provenance/status transparency | status supported | allowed for provenance/status only |
| C8 semi-real case validation | scaffold-only blocked | no validation claim |

Safe central thesis:

> We formulate and audit a dynamic service-menu optimization framework for
> many-to-one DRT, where displayed alternatives combine meeting point, pickup
> time window, and price. Under paired replay and strict artifact gates, the
> current evidence supports diagnostic analysis of profit-service trade-offs
> and claim-boundary transparency, but does not authorize empirical superiority
> claims.

Safe abstract-level wording:

> This paper studies a claim-gated service-menu optimization framework for
> many-to-one demand-responsive transit. The framework treats the displayed menu
> as bundles of meeting point, pickup time window, and price, and evaluates
> policy variants under paired replay with explicit opt-out, checkpoint, and
> artifact-status accounting. Current generated artifacts identify diagnostic
> boundary patterns and reproducibility blockers; positive performance claims
> remain conditional on future claim-ready evidence.

Do not use wording such as "adaptive menu dominates," "adaptive windows
improve," "near-optimal greedy," "case-study validation," "real passenger
behavior," or "provenance resolves empirical blockers."

## 7. Reviewer Risks And Likely Attack Points

High-risk reviewer questions:

- Why should TR-E accept a paper whose main empirical claim is not claim-ready?
- Why does random menu outperform adaptive on mean net profit in the selected
  formal diagnosis?
- Why are adaptive and fixed-window variants identical across tracked metrics?
- Why did the exact-vs-greedy experiment not trigger greedy fallback at the
  intended large settings?
- Are simulated MNL choices too close to the optimization assumptions?
- Does opt-out accounting affect routing/cost outcomes cleanly, or can opt-out
  be confused with home pickup?
- Where is the real or semi-real validation evidence?
- Are artifacts reproducible if formal readiness was blocked by dirty git and
  artifact metadata blockers?
- Are Phase 8 no-filter and ETA-filter diagnostics being quietly interpreted as
  operational recommendations?

These risks are not fatal to a diagnostic paper if they are placed in the
paper's premise, results, and limitations. They are fatal to a conventional
performance-superiority submission in the current form.

## 8. Minimum Revisions Before Manuscript Drafting

Minimum revisions for a conditional/diagnostic manuscript draft:

1. Rewrite the contribution statement around formulation, paired-replay
   evaluation design, diagnostic boundary analysis, and claim-gated
   reproducibility.
2. Put the claim gate before empirical tables in the experimental design or
   results section.
3. Move unsupported main RC artifacts to status or limitation context unless a
   future claim-ready package replaces them.
4. Label every Phase 8 sensitivity table/figure as diagnostic/provisional with
   `claim_ready=false`.
5. Label every Phase 9 computational table/figure as diagnostic/provisional and
   explicitly state that exact-vs-greedy quality was not established.
6. Keep case-study scaffold material in appendix or future-work language only.
7. Define accepted home, accepted meeting-point service, and opt-out before any
   metric table.
8. Exclude all prohibited language from the abstract, introduction,
   conclusion, and managerial implications.
9. Add a reviewer-risk paragraph that openly states central claim, greedy
   fallback, case validation, and provenance gaps.

Minimum revisions for a claim-ready TR-E empirical submission:

1. Resolve provenance/readiness blockers, including dirty-git readiness for the
   exact evidence run.
2. Regenerate rows and artifacts through the pipeline with required metadata,
   including `method_family`, `outside_option_util`, checkpoint hash/sidecar,
   opt-out/home/meeting-point accounting, and status/error fields.
3. Produce a strict claim guard whose relevant empirical claims are approved.
4. Establish either a defensible conditional central claim or explicitly abandon
   superiority framing.
5. If computational credibility is claimed, run an exact-vs-greedy design that
   actually exercises greedy fallback and reports gap/overlap where applicable.
6. If case validation is claimed, execute a reproducible case study and keep
   simulated demand/choice labels explicit.

## 9. Final Recommendation

Recommendation: **draftable only as a conditional/diagnostic paper**.

The paper is still viable if it is drafted as a claim-bounded TR-E service-menu
optimization study: a rigorous formulation, an auditable policy comparison
pipeline, a diagnostic account of profit-service trade-offs, and a transparent
artifact/claim-gate package. That version should be honest that the current
evidence does not support superiority, adaptive-window increment,
near-optimal-greedy, computational-credibility, or semi-real validation claims.

It is not ready as a claim-ready empirical TR-E submission. If the target is a
standard TR-E performance paper with a positive abstract-level claim, additional
evidence is required before drafting.

## Verification Ledger

| Check | Result |
| --- | --- |
| Import smoke from `work2_coding` | passed: `IMPORT_OK` |
| `python scripts/test_phase10_paper_artifacts.py` | passed: 3 Phase 10 paper artifact package tests |
| `python scripts/test_manuscript_claim_guard.py` | passed: 5 manuscript claim guard tests |
| `python scripts/test_phase8_sensitivity_summary.py` | passed: 7 Phase 8 sensitivity summary tests |
| `python scripts/test_phase9_tractability_summary.py` | passed: 8 Phase 9 tractability summary tests |
| `git diff --cached --check -- .planning/final/TR_E_READINESS_REVIEW.md` | passed |
