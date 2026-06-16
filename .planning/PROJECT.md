# Work2 TR-E Claim-Ready Manuscript Completion

## What This Is

This is a regenerated GSD planning project for completing the Work2 paper as a
high-quality Transportation Research Part E manuscript. The repository studies
dynamic service-menu optimization for many-to-one demand-responsive transit and
last-mile mobility, where each displayed alternative is a bundle
`(meeting point, pickup time window, price)`.

The project must decide from current evidence whether the paper can honestly be
submitted as a claim-ready empirical optimization paper or whether it should be
written as a conditional diagnostic service-menu optimization paper. This
planning reset was created after the user chose not to restore deleted legacy
GSD planning files and instead regenerate new planning from the current
workspace, current artifacts, and the TR-E manuscript completion prompt.

## Core Value

Produce a credible TR-E manuscript package whose empirical claims are no
stronger than the generated evidence, readiness gates, and strict
`CLAIM_GUARD.json` allow.

## Requirements

### Validated

- `work2_coding/` is the active runtime root.
- The runtime import smoke passes from repository root:
  `python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"`.
- Phase 10 paper artifacts exist under both
  `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/` and
  `artifacts/work2_robust_menu/phase10_paper_artifacts/`.
- Current Phase 10 `CLAIM_GUARD.json` uses schema
  `phase10-strict-claim-guard-v1`, contains 8 claims, and has
  `claim_ready=false`.
- Current Phase 10 `PACKAGE_STATUS.json` reports 74 artifacts, 108 blockers,
  70 existing artifacts, and 4 missing artifacts.
- The only current strict claim marked ready is
  `C7_provenance_status_transparency`; positive empirical manuscript claims
  are not authorized.
- Existing case-study materials under `.planning/data/case_studies/` are
  scaffold-only and do not validate real passenger behavior.
- Phase 1 validated the current evidence boundary in
  `.planning/milestones/tr_e_completion/M1_EVIDENCE_BOUNDARY_AUDIT.md`,
  `.planning/milestones/tr_e_completion/M1_BLOCKER_LIST.md`, and
  `.planning/milestones/tr_e_completion/M1_DECISION.md`.
- Phase 2 validated non-destructive gate cleanup planning in
  `.planning/milestones/tr_e_completion/M2_GATE_CLEANUP_PLAN.md`,
  `.planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md`, and
  `.planning/milestones/tr_e_completion/M2_USER_ACTIONS_REQUIRED.md`.
- Phase 2 classified dirty git state without cleanup and locked the checkpoint
  provenance requirement set for path, hash, sidecar metadata, load status,
  dependency snapshot, manifest hash, git SHA, dirty state, readiness JSON
  hash, and source-row checkpoint metadata.

### Active

- [ ] Decide whether a final claim-ready rerun is scientifically legitimate
  under calibration/final-test separation.
- [ ] If claim-ready gates can be resolved legitimately, run only a
  pre-registered final replay and regenerate artifacts from source rows.
- [ ] If evidence remains mixed or `claim_ready=false`, lock the paper as a
  conditional diagnostic TR-E manuscript.
- [ ] Build a full manuscript draft with TR-E framing, paragraph prose,
  consistent notation, claim-safe results, and table/figure source mapping.
- [ ] Audit final submission readiness for novelty, model rigor, empirical
  credibility, claim safety, reproducibility, and reviewer risk.

### Out of Scope

- Attention-based choice or scoring as a v1 paper contribution.
- A pricing-only paper framing.
- A pure algorithm ranking paper framing.
- Positive claims such as "adaptive menu dominates", "adaptive windows
  improve", "near-optimal greedy", or "case-study validation" unless strict
  claim guard output explicitly authorizes them.
- Treating outside option as accepted home pickup.
- Treating no-filter variants as operational recommendations.
- Hand-editing generated rows, result tables, figures, package status, or
  claim guards.
- Fabricating real data, real passenger behavior, external validation, or
  claim-ready evidence.
- Tuning on final test results to force the desired ranking.
- Recreating a parallel `ooh_code/` runtime root.

## Context

The paper target is Transportation Research Part E: Logistics and
Transportation Review. The paper should therefore be framed in transportation
logistics, service operations, online decision-making, passenger choice, and
optimization.

The current service product is a displayed menu of feasible bundles combining
meeting point, pickup time window, and price. Accepted home pickup and accepted
meeting-point pickup are both accepted service outcomes. The outside option is
refusal or lost demand and must remain separate from accepted home service.

The primary v1 policy family is:

1. `mainline_no_menu`
2. `mainline_fixed_menu`
3. `mainline_random_menu`
4. `mainline_optimized_m`
5. `mainline_optimized_mw`
6. `mainline_optimized_fixed_window`
7. `mainline_optimized_adaptive`

The primary method is `mainline_optimized_adaptive`: optimized menu, adaptive
pickup-time window, Lambert-W pricing, product mode `m+w+p`, time-window mode
`adaptive_window`, menu-contract mode `optimized_menu`, and pricing mode
`lambertw`.

Current artifact evidence does not authorize positive manuscript claims. The
strict claim guard blocks central adaptive-menu superiority, product ablation
value, adaptive-window increment, menu-construction value, exact-greedy
computational credibility, and semi-real case validation. Phase 8 sensitivity
and Phase 9 tractability material are diagnostic/provisional. Case-study
materials are scaffold-only.

## Constraints

- **Runtime root:** Use `work2_coding/` for active Python commands.
- **Evidence integrity:** Preserve paired replay fairness across policy
  comparisons.
- **Accounting:** Keep opt-out separate from accepted home pickup.
- **Checkpoint provenance:** Make checkpoint path, hash, sidecar metadata, and
  load status explicit in result metadata.
- **Generated evidence:** Do not hand-edit generated rows or paper artifacts.
- **Claim ceiling:** `CLAIM_GUARD.json` is the authority for manuscript claim
  upgrades.
- **No-filter status:** Treat no-filter as diagnostic unless formal evidence
  justifies stronger claims.
- **Case-study boundary:** Semi-real case materials are scaffold-only unless
  reproducible runtime rows and artifact gates are generated later.
- **Manuscript language:** Use claim-safe verbs such as "formulate",
  "evaluate", "diagnose", "audit", "identify boundary conditions", and
  "claim-gated evidence".
- **Planning reset:** This new project plan does not restore deleted legacy GSD
  planning files. It regenerates planning from the prompt, current artifacts,
  current codebase maps, and current workspace state.

## Key Decisions

| Decision | Rationale | Outcome |
| --- | --- | --- |
| Regenerate planning instead of restoring deleted legacy planning files | The user selected option 2 after deletion of prior GSD core docs was detected. | Active |
| Use `work2_coding/` as runtime root | Current import smoke passed and codebase maps identify it as active. | Validated |
| Keep seven mainline policy tags as the primary family | They preserve the intended service-menu comparison surface. | Active |
| Keep `mainline_optimized_adaptive` as the primary method | It matches the intended optimized `m+w+p` adaptive-window Lambert-W service-menu method. | Active |
| Use strict claim guard as claim authority | Current artifacts show `claim_ready=false`; evidence must control wording. | Active |
| Plan a branch between claim-ready rerun and diagnostic lock | The manuscript path depends on evidence, not desired conclusions. | Active |
| Defer manuscript prose until evidence path is selected | Prevents writing positive claims before gates authorize them. | Active |

## Evolution

This document evolves at phase transitions and milestone boundaries.

After each phase transition:

1. Requirements invalidated? Move to Out of Scope with reason.
2. Requirements validated? Move to Validated with phase reference.
3. New requirements emerged? Add to Active.
4. Decisions to log? Add to Key Decisions.
5. "What This Is" still accurate? Update if drifted.

After each milestone:

1. Full review of all sections.
2. Core Value check: still the right priority?
3. Audit Out of Scope: reasons still valid?
4. Update Context with current state.

---
*Last updated: 2026-06-16 after Phase 1 evidence-boundary audit*
