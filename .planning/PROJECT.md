# Work2 Robust Time-Window Service Menu Optimization for Many-to-One DRT

## What This Is

This project turns Work2 into a runnable, reproducible experimental pipeline for many-to-one demand-responsive transit service-menu optimization. The platform chooses a limited displayed menu of service bundles, where each bundle combines a meeting point, pickup time window, and price, while accounting for passenger choice, ETA uncertainty, routing cost, capacity risk, and service quality.

The contribution is not "turning off ETA filtering." The contribution is an uncertainty-aware service-menu optimization framework with auditable exact-small and greedy-large menu construction, paired replay experiments, diagnostic artifacts, and paper-ready evidence for when robust time-window menu construction improves profit, acceptance, non-home uptake, opt-out, and service-quality metrics.

## Core Value

The project must produce defensible Work2 evidence: a reproducible pipeline where robust time-window menu policies can be fairly compared against hard filtering, no-filter diagnostics, and practical baselines on the same request traces and shared predictor checkpoints.

## Requirements

### Validated

- Existing Work2 runtime package is present under `work2_coding/`.
- `work2_coding/Src/config.py` imports successfully when `work2_coding/` is on `sys.path`.
- `work2_coding/Src/Algorithms/DSPO_Menu.py` exists and already contains menu-mode logic, ETA filter variants, menu policies, exact/greedy selection paths, and exact-vs-greedy diagnostics.
- `work2_coding/Environments/OOH/` contains the OOH simulator, MNL choice model, routing utilities, domain containers, and bundled Homberger/Gehring and Amazon data.
- Existing README documents the inherited DSPO/OOH codebase, Python 3.10 runtime, PyTorch dependency, and Hygese routing dependency.
- Phase 1 Stage 0 audit is complete and recorded in `.planning/phases/01-repository-audit-and-runtime-baseline/01-STAGE0-AUDIT.md`.
- `ooh_code/` is absent from the current filesystem; existing `.planning/codebase/` references to `ooh_code/` are stale historical context until revalidated.

### Active

- [ ] Repair or isolate opt-out accounting so outside-option choices do not mutate routes as accepted home pickups.
- [ ] Make shared predictor checkpoint loading explicit and row-level visible.
- [ ] Implement robust ETA/time-window filtering modes with diagnostics and metadata.
- [ ] Integrate robust ETA/time-window risk into menu evaluation and selection.
- [ ] Compare exact-small and greedy-large menu selection with approximation diagnostics.
- [ ] Create reproducible smoke, pilot, and formal experiment manifests or their nearest runnable equivalent in the current package.
- [ ] Generate normalized result rows, aggregate summaries, artifact tables/figures, and provenance records.
- [ ] Produce a manuscript-ready method/result outline and claim checklist that prevents overclaiming.

### Out of Scope

- Attention-based choice/scoring module - defer until the robust time-window service-menu pipeline is runnable and evidenced.
- Work3 many-to-many DRT and Work4 planning - separate dissertation workstreams.
- Rewriting the whole simulator - reuse the inherited Work1/Work2 infrastructure unless an audit proves a targeted replacement is necessary.
- Treating `no_filter` as the recommended policy by default - it is a diagnostic upper bound unless formal evidence justifies a stronger claim.
- Real passenger behavioral validation - current evidence is simulation-based unless external survey or revealed-preference data is added later.
- Exact optimality for the full dynamic DRT system - exact enumeration is only an auditable surrogate for small candidate sets.

## Context

Work1 studies dynamic meeting-point recommendation and pricing with cost prediction and decision-focused learning. Work2 extends that pricing/recommendation layer into the menu layer: instead of asking how to price already-given boarding options, Work2 asks which limited set of feasible spatiotemporal service bundles should be displayed to each passenger.

The user discussion on 2026-06-10 selects "scheme 1": robust time-window service menu optimization. Attention is explicitly deferred; it may become a later behavioral-model enhancement, not the main contribution.

The repository is a brownfield research codebase. Current filesystem inspection shows `work2_coding/` as the actual runnable package, while the existing `.planning/codebase/` map refers heavily to `ooh_code/`. This mismatch must be resolved during Stage 0 so future phases do not duplicate work into the wrong root.

Known engineering risks to address early:
- Active runtime root and import paths must be verified before patches.
- Opt-out must be separated from accepted home service in routing and accounting.
- Checkpoint loading must fail visibly or emit explicit `checkpoint_load_status`; random fallback cannot silently enter formal comparisons.
- All policy comparisons must use paired request traces, shared trained predictors, fixed seeds, and shared routing/HGS parameters.
- Exact enumeration must be limited to small candidate sets; large candidate sets need greedy/approximate selection with logged diagnostics.

## Constraints

- **Runtime root**: Prefer `work2_coding/` because it is present and imports `Src.config`; do not create a parallel `ooh_code/` implementation unless the audit proves it is required.
- **Language and dependencies**: Python 3.10 style code with PyTorch, NumPy, Hygese, and local script-style tests; avoid adding heavyweight framework dependencies without need.
- **Experiment fairness**: Formal comparisons must share request traces, checkpoints, seeds, split IDs, routing parameters, and pricing mode unless a manifest explicitly varies one factor.
- **Scientific scope**: Robust filtering and service-constrained menu optimization are the main Work2 contribution; attention, decision-focused regret learning, and many-to-many DRT are deferred.
- **Artifacts**: Do not hand-edit generated results. Formal artifacts need manifest hash, run ID, git commit/hash, checkpoint provenance, and placeholder status.
- **Implementation style**: Keep functions small, testable, and modular. Prefer config flags, metadata fields, tests, and manifest contracts over hard-coded experiment choices.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Use `work2_coding/` as the active runtime root unless Stage 0 finds otherwise | It exists in the current tree, passed an import smoke check, and Phase 1 confirmed no current `ooh_code/` root | Validated in Phase 1 |
| Focus Work2 on robust time-window service-menu optimization | This is feasible in the existing DSPO_Menu code and gives a clearer contribution than attention-first framing | Pending |
| Treat `no_filter` as diagnostic, not the final method | It can expose candidate-availability upper bounds but is not automatically operationally credible | Pending |
| Defer attention mechanisms | The user selected scheme 1 and explicitly excluded attention for this project | Pending |
| Start with Stage 0 audit before algorithm edits | Existing path/accounting/checkpoint risks can invalidate downstream evidence if skipped | Validated in Phase 1 |
| Use exact-small and greedy-large solver diagnostics | Provides auditability for small sets and scalability for realistic candidate sets | Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `$gsd-transition`):
1. Requirements invalidated? Move to Out of Scope with reason.
2. Requirements validated? Move to Validated with phase reference.
3. New requirements emerged? Add to Active.
4. Decisions to log? Add to Key Decisions.
5. "What This Is" still accurate? Update if drifted.

**After each milestone** (via `$gsd-complete-milestone`):
1. Full review of all sections.
2. Core Value check - still the right priority?
3. Audit Out of Scope - reasons still valid?
4. Update Context with current state.

---
*Last updated: 2026-06-11 after Phase 1 completion*
