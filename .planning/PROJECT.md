# Work2_TR_E_Service_Menu_Optimization_Final

## What This Is

This is a GSD-managed brownfield research rebuild for Work2, focused on dynamic
service menu optimization for many-to-one demand-responsive transit and
last-mile mobility. The active runtime is `work2_coding/`, and the project
turns the existing Work2 robust-menu implementation into a claim-gated
Transportation Research Part E paper pipeline.

The central object is the displayed service menu: for each sequential passenger
request, the platform selects a limited set of service bundles combining a
meeting point, pickup-time window, and price, with home service and the outside
option handled explicitly.

## Core Value

Produce credible, reproducible TR Part E evidence on when and how optimized
adaptive `m+w+p` service menus improve, match, or fail to improve the
profit-service-quality trade-off under paired RC replay, without overclaiming
beyond artifact and readiness gates.

If formal evidence does not show strong dominance, reframe the paper as a
conditional service-menu design study that identifies when menu optimization
helps DRT operations and when it fails because of low uptake, excessive
opt-out, ETA uncertainty, or capacity constraints.

## Current Milestone: v1.1 Resolve Claim-Ready Gate or Lock Conditional Diagnostic TR-E Paper

**Goal:** Determine from current repository evidence and reproducible
experiment gates whether Work2 can honestly upgrade any manuscript claim from
`claim_ready=false` to `claim_ready=true`; if not, formally lock the paper as a
conditional diagnostic TR-E manuscript.

**Target features:**

- Reconstruct the exact Phase 10 evidence boundary and all causes of
  `claim_ready=false`.
- Plan only legitimate gate, metadata, provenance, and artifact repairs without
  changing empirical conclusions by hand.
- Diagnose whether the random-menu profit advantage and adaptive/fixed-window
  equality are real scientific results, configuration issues, modeling
  mismatches, or implementation bugs.
- Choose a gated path: gate-only repair, pre-registered final rerun, or
  conditional diagnostic lock.
- Execute only the selected path, with strict `CLAIM_GUARD.json` authority over
  any claim upgrade.
- Produce a final manuscript-path decision with explicit allowed and prohibited
  claims.

**Possible final outcomes:**

- **Outcome A:** `claim_ready=true` for one or more clearly defined manuscript
  claims, backed by passed readiness, completed paired rows, regenerated paper
  artifacts, and strict claim-guard approval.
- **Outcome B:** `claim_ready=false` remains, and the paper is locked as a
  conditional diagnostic service-menu optimization paper with no adaptive-menu
  superiority, adaptive-window value, near-optimal greedy, or case-validation
  claims.

## Requirements

### Validated

- [x] `work2_coding/` is the active importable runtime root.
- [x] `DSPO_Menu.py` exists in `work2_coding/Src/Algorithms/`.
- [x] Existing runtime imports pass with `python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"`.
- [x] Existing code contains robust-menu manifests, study execution scripts,
  artifact builders, formal readiness checks, and service-product tests.
- [x] Previous `.planning/codebase/` maps are available but stale where they
  reference `ooh_code/`.
- [x] Phase 1 locked the current repository state in `.planning/STATE_LOCK.md`
  before algorithm behavior changes.
- [x] Phase 2 locked the TR-E paper research design in
  `.planning/paper/TR_E_RESEARCH_DESIGN.md`.
- [x] Phase 3 completed the formal RC evidence pipeline diagnostically:
  readiness/checkpoint status is explicit, the selected formal run has 35
  comparable completed rows across the seven-tag family, and artifact/claim
  gates block claim-ready manuscript use until residual gates are resolved.
- [x] Phase 4 diagnosed the selected 35-row formal RC run: adaptive `m+w+p`
  improves several service metrics but does not support a strong universal
  dominance claim; all positive empirical classifications remain provisional
  while dirty-git readiness and artifact gates are blocked.
- [x] Phase 5 locked calibration integrity without p-hacking:
  `.planning/results/CALIBRATION_PROTOCOL.md` defines allowed/prohibited
  tuning, calibration/final manifests are separated, and
  `.planning/results/FROZEN_FINAL_SETTINGS.md` records pre-run final settings
  while final rerun remains blocked pending provenance/artifact gate cleanup.
- [x] Phase 6 approved a semi-real case study in principle with decision
  `approved_blocked_pending_gate_cleanup`: public OSM/open-network evidence is
  the default route, Yanjiao/Beijing material is narrative support unless it can
  be reproduced equally well, and Phase 7 may prepare scaffolding but may not
  run case experiments or upgrade claims while gates remain blocked.
- [x] Phase 7 delivered planning-side semi-real case scaffolding under
  `.planning/data/case_studies/`: source contracts, route-selection scoring,
  simulated-demand protocol placeholders, a non-executable manifest draft, a
  reduced-family gate, prohibitive claim placeholders, and a validator. This is
  contract coverage only; no case rows, result artifacts, runtime manifest, or
  claim upgrade were produced.
- [x] Phase 8 ran `phase8_baseline_validation`, executed the four must-have
  diagnostic sensitivity studies, generated sensitivity artifacts under
  `work2_coding/artifacts/work2_robust_menu/phase8_sensitivity/`, and wrote
  `.planning/results/SENSITIVITY_SUMMARY.md` with
  `status: diagnostic_provisional_blocked` and `claim_ready: false`.
  Phases 6-8 continued after weak Phase 4 central-claim evidence to add
  conditional diagnosis and boundary evidence, not to upgrade strong manuscript
  claims.
- [x] Phase 9 ran `phase9_exact_greedy_tractability`, generated 15 completed
  diagnostic rows and tractability artifacts under
  `work2_coding/artifacts/work2_robust_menu/phase9_tractability/`, and wrote
  `.planning/results/COMPUTATIONAL_TRACTABILITY_SUMMARY.md` with
  `status: diagnostic_provisional_blocked` and `claim_ready: false`.
  The intended exact-vs-greedy comparison was not established: realized
  candidate counts stayed below the greedy threshold, so even large configured
  scales still used the effective exact solver. Phase 9 remains
  diagnostic/provisional, and exact-vs-greedy quality plus
  computational-credibility claims remain narrowed/blocked.
- [x] Phase 10 generated and verified the paper artifact package under both
  `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/` and
  `artifacts/work2_robust_menu/phase10_paper_artifacts/`. The package includes
  `CLAIM_GUARD.json` with schema `phase10-strict-claim-guard-v1`, 8 claims,
  and overall `claim_ready=false`; `PACKAGE_INDEX.json` contains 74 unique
  source artifacts with no duplicate `source_path` values. Phase 10 generated
  paper-facing artifacts, but did not authorize manuscript claim upgrades.

### Active

- [ ] Reconstruct the current Phase 10 evidence boundary before any repair,
  rerun, or manuscript writing.
- [ ] Classify every `claim_ready=false` cause into provenance/readiness,
  artifact-generation, empirical-performance, adaptive-window,
  random-baseline, sensitivity, tractability, semi-real-case, or
  manuscript-language blockers.
- [ ] Produce a safe gate repair plan that separates metadata/schema fixes from
  experiment semantics and never changes empirical values by hand.
- [ ] Diagnose why `mainline_random_menu` currently beats
  `mainline_optimized_adaptive` on mean net profit and why adaptive and fixed
  windows are identical across tracked metrics.
- [ ] Choose and document exactly one path: gate-only repair, pre-registered
  final rerun, or conditional diagnostic lock.
- [ ] Regenerate readiness/artifacts or run final replay only when the selected
  path authorizes it, preserving paired replay fairness, outside-option
  accounting, checkpoint provenance, and the seven-tag mainline family unless
  a reduction is formally justified.
- [ ] Lock all manuscript claims to strict `CLAIM_GUARD.json` output and produce
  a final decision on whether the manuscript path is claim-ready empirical,
  conditional diagnostic, or not ready.

### Out of Scope

- Making attention-based choice or scoring the V1 paper contribution.
- Claiming universal dominance across every metric or setting.
- Treating no-filter diagnostics as formal evidence without additional proof.
- Hand-editing generated result rows, tables, figures, or claim outputs.
- Creating or reviving a parallel `ooh_code/` runtime root.
- Fabricating real data or describing simulated demand as real behavior.
- Tuning directly on formal test results to force the target ranking.

## Context

The 6.14 Work2 discussion note argues that Work2 should be positioned as a
service-menu optimization paper rather than an attention paper or a
pricing-only extension. Its strongest framing is:

> Dynamic service menu optimization for many-to-one DRT with meeting-point,
> pickup-time-window, and pricing choices.

The current repository is not empty. It already contains a Work2 implementation,
service-product contracts, robust-menu manifests, smoke/pilot/formal study
definitions, artifact builders, formal readiness checks, and manuscript-frame
builders. The current Work2 V1 mainline family is:

1. `mainline_no_menu`
2. `mainline_fixed_menu`
3. `mainline_random_menu`
4. `mainline_optimized_m`
5. `mainline_optimized_mw`
6. `mainline_optimized_fixed_window`
7. `mainline_optimized_adaptive`

The primary V1 method is `mainline_optimized_adaptive`: optimized menu,
adaptive pickup-time window, and Lambert-W pricing, with product mode `m+w+p`,
time-window mode `adaptive_window`, menu-contract mode `optimized_menu`, and
pricing mode `lambertw`.

The 6.14 discussion also states a scientific status boundary: current smoke and
pipeline evidence can show that the experiment framework works, but formal
checkpoint training, formal replay, and claim-ready artifact gates must pass
before any empirical superiority claim is made.

## Constraints

- **Runtime root:** Use `work2_coding/` for all Python commands.
- **Path hygiene:** Treat `.planning/codebase/` `ooh_code/` references as stale
  until Phase 1 verifies equivalent `work2_coding/` paths.
- **Evidence integrity:** Preserve paired replay fairness across policy
  comparisons.
- **Behavior accounting:** Keep opt-out separate from accepted home pickup.
- **Checkpoint provenance:** Record checkpoint load status and checkpoint
  provenance in result metadata.
- **Claim gates:** Formal paper claims require readiness JSON, normalized rows,
  artifact status, and claim guard approval.
- **Research scope:** RC benchmark is primary. Real/semi-real case study is
  optional and only after RC formal evidence is stable.
- **Paper positioning:** Write for logistics, transportation optimization, and
  service operations; do not frame V1 as an attention model paper.
- **Phase gates:** Phase 5 and Phase 7 are conditional. Skip them by documented
  gate decision when evidence or feasibility makes them unnecessary.
- **Fallback contribution:** If `mainline_optimized_adaptive` does not strongly
  dominate, do not force a superiority story; write a conditional diagnostic
  contribution.
- **Timestamp discipline:** Use ISO timestamps with timezone and record whether
  timestamps are local machine time, Beijing time, or UTC.

## Key Decisions

| Decision | Rationale | Outcome |
| --- | --- | --- |
| Use `work2_coding/` as runtime root | Current import smoke passes there and `DSPO_Menu.py` exists. | Validated |
| Rebuild planning around TR Part E | The 6.14 discussion identifies service-product menu optimization as the stronger contribution. | Active |
| Keep seven mainline tags as V1 comparison family | They decompose menu optimization, product composition, pricing, and time-window value. | Active |
| Keep `mainline_optimized_adaptive` as the primary method | It represents optimized `m+w+p` service menus with adaptive windows and Lambert-W pricing. | Active |
| Keep attention diagnostic only | Existing discussion and prompt both exclude attention as the V1 contribution. | Active |
| Require formal evidence before claims | Current pipeline status is not yet sufficient for TR-E empirical claims. | Active |
| Separate calibration from final formal testing | Prevents p-hacking and protects paper credibility. | Active |
| Allow skipped-by-gate phases | Avoids mechanically executing optional heavy phases when evidence or feasibility says to stop or reframe. | Active |
| Preserve a fallback claim path | Mixed results can still support a conditional service-menu design contribution. | Active |
| Use `.planning/STATE_LOCK.md` as the Phase 1 baseline | Phase 1 verified `work2_coding/`, current evidence blockers, and stale `ooh_code/` mappings before behavior changes. | Validated |
| Use `.planning/paper/TR_E_RESEARCH_DESIGN.md` as the Phase 2 paper contract | Phase 2 defined service-bundle semantics, model skeleton, claim ladder, evidence gates, and table/figure plans. | Validated |
| Use the 35-row formal RC run as Phase 4 diagnostic input | Phase 3 validated `formal_robust_menu-20260614T032323Z-c672286a` as comparable candidate evidence while preserving readiness/artifact blockers. | Validated |
| Do not claim strong adaptive-menu dominance from the selected formal RC run | Phase 4 found random menu has better mean net profit, adaptive loses to random on 3/5 paired profit splits, and adaptive equals optimized fixed-window across tracked metrics. | Validated |
| Do not skip Phase 5 while provenance and central-claim evidence remain weak | Phase 4 recommends provenance cleanup first, then Phase 5 calibration if the project still wants a strong central empirical claim; otherwise reframe as conditional service-menu design. | Active |
| Lock calibration before any rerun | Phase 5 created pre-registered calibration and final manifests plus frozen settings, but marked final execution blocked until gate cleanup passes. | Validated |
| Add a semi-real case only behind gates | Phase 6 found public OSM/open-network data is reproducible enough for a supplemental semi-real external scenario, but no real passenger behavior, acceptance, opt-out, or profit may be claimed from simulated demand/choice. | Validated |
| Close Phase 7 as scaffold-only | Phase 7 created reproducible planning contracts and validation checks, but upstream gates still block case execution, result artifacts, and manuscript claim upgrades. | Validated |
| Treat Phase 8 sensitivity as diagnostic boundary evidence | Phase 8 generated 50 completed rows across the four must-have axes, but artifacts and summary remain `diagnostic_provisional_blocked` with `claim_ready=false`; candidate pool, fleet/capacity stress, and pricing sensitivity stay deferred. | Validated |
| Treat Phase 9 exact-vs-greedy as blocked diagnostic evidence | The 15-row run completed, but realized candidate counts stayed below the greedy threshold on the configured large scales, so the effective exact solver was still used and gap/overlap evidence is unavailable. | Validated |
| Treat Phase 10 paper artifacts as claim-boundary packaging | Phase 10 generated mirrored paper-facing artifact packages with a strict 8-claim guard and 74 unique indexed source artifacts, but overall `claim_ready=false` blocks manuscript claim upgrades. | Validated |
| Start v1.1 claim-ready resolution before manuscript writing | Phase 10 leaves the paper artifact package draftable only under strict claim boundaries; the next milestone must either resolve the gate honestly or lock the diagnostic manuscript path. | Active |

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
*Last updated: 2026-06-16 after v1.1 claim-ready resolution milestone initialization*
