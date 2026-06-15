# Work2_TR_E_Service_Menu_Optimization_Final

## What This Is

This is a GSD-managed brownfield research rebuild for Work2, focused on dynamic
service menu optimization for many-to-one demand-responsive transit and
last-mile mobility. The active runtime is `work2_coding/`, and the project
turns the existing Work2 robust-menu implementation into a claim-ready
Transportation Research Part E paper pipeline.

The central object is the displayed service menu: for each sequential passenger
request, the platform selects a limited set of service bundles combining a
meeting point, pickup-time window, and price, with home service and the outside
option handled explicitly.

## Core Value

Produce credible, reproducible TR Part E evidence that optimized adaptive
`m+w+p` service menus improve the profit-service-quality trade-off under paired
RC replay, without overclaiming beyond artifact and readiness gates.

If formal evidence does not show strong dominance, reframe the paper as a
conditional service-menu design study that identifies when menu optimization
helps DRT operations and when it fails because of low uptake, excessive
opt-out, ETA uncertainty, or capacity constraints.

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

### Active

- [ ] Complete formal RC evidence for the seven-tag mainline family.
- [ ] Diagnose whether formal RC results support strong, conditional, weak, or
  unsupported paper claims.
- [ ] If needed, calibrate through a documented pilot/final split rather than
  test-set tuning.
- [ ] Decide whether a real or semi-real case study is feasible and valuable.
- [ ] Add sensitivity, exact-vs-greedy, artifact, manuscript, and final
  readiness phases only after upstream evidence gates pass.

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
*Last updated: 2026-06-15 after Phase 2 paper research design lock*
