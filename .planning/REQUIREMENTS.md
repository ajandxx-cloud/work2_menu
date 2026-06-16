# Requirements: Work2_TR_E_Service_Menu_Optimization_Final

**Defined:** 2026-06-16
**Milestone:** v1.1 Resolve Claim-Ready Gate or Lock Conditional Diagnostic TR-E Paper
**Core Value:** Produce credible, reproducible TR Part E evidence on when and
how optimized adaptive `m+w+p` service menus improve, match, or fail to improve
the profit-service-quality trade-off under paired RC replay, without
overclaiming beyond artifact and readiness gates.

Previous v1.0 requirements and completed evidence remain recorded in
`.planning/PROJECT.md` and the completed Phase 1-10 history in
`.planning/ROADMAP.md`. This file now scopes the active v1.1 milestone.

## v1.1 Requirements

### Evidence Boundary

- [ ] **EVID-01**: The project reconstructs the exact current evidence boundary
  from planning docs, result summaries, final readiness review, frozen final
  settings, and the Phase 10 paper artifact package before any repair, rerun,
  or manuscript writing.
- [ ] **EVID-02**: The project identifies every concrete reason the current
  Phase 10 `CLAIM_GUARD.json` keeps overall `claim_ready=false`.
- [ ] **EVID-03**: The project classifies all blockers into provenance/readiness,
  artifact-generation, empirical-performance, adaptive-window,
  random-menu-baseline, sensitivity-robustness, computational-tractability,
  semi-real-case, and manuscript-language categories.
- [ ] **EVID-04**: The evidence boundary deliverables are written under
  `.planning/milestones/claim_ready_resolution/` without editing generated
  result rows or paper artifacts.

### Gate Repair Planning

- [ ] **GATE-01**: The project inspects git status and identifies dirty-git
  blockers without deleting, reverting, stashing, or overwriting unrelated
  files.
- [ ] **GATE-02**: The project determines whether readiness blockers come from
  unrelated dirty files, missing metadata, missing checkpoint sidecar/hash,
  missing result fields, or artifact schema issues.
- [ ] **GATE-03**: The project diagnoses whether missing
  `outside_option_util`, invalid or missing `method_family`, and related
  artifact-status failures are metadata/reporting issues, artifact-builder
  issues, true experiment-row issues, or evidence-quality issues.
- [ ] **GATE-04**: The project produces a safe repair plan where every proposed
  repair maps to a specific gate and is labeled as non-semantic metadata/schema
  repair, code/builder repair, or new experiment path.

### Empirical Failure Diagnosis

- [ ] **DIAG-01**: The project diagnoses why `mainline_random_menu` has better
  mean net profit than `mainline_optimized_adaptive` using source rows and code
  paths rather than speculation.
- [ ] **DIAG-02**: The project decomposes profit differences into revenue,
  operating cost, discount or price effect, opt-out/lost-demand effect,
  accepted home service, accepted meeting-point service, and service-cost
  effect where data support it.
- [ ] **DIAG-03**: The project diagnoses why `mainline_optimized_adaptive` and
  `mainline_optimized_fixed_window` are identical across tracked metrics.
- [ ] **DIAG-04**: The project states whether the central positive claim is
  scientifically recoverable, conditionally recoverable, or unsupported.

### Path Decision

- [ ] **PATH-01**: The project reads the calibration protocol and frozen final
  settings before deciding whether a final rerun is legitimate.
- [ ] **PATH-02**: The project chooses exactly one path: Path A gate-only repair,
  Path B pre-registered final rerun, or Path C conditional diagnostic lock.
- [ ] **PATH-03**: The selected path decision records reason, allowed actions,
  prohibited actions, claim ceiling, whether a positive central claim is
  allowed, whether a conditional claim is allowed, and whether the manuscript
  must remain diagnostic.
- [ ] **PATH-04**: The path decision forbids result-chasing, tuning on final
  results, deleting inconvenient baselines, or upgrading diagnostic evidence by
  wording.

### Selected Path Execution

- [ ] **EXEC-01**: If Path A is selected, the project repairs only legitimate
  metadata/provenance/artifact blockers and regenerates readiness, artifacts,
  and strict claim guard without changing empirical rows or experiment
  semantics.
- [ ] **EXEC-02**: If Path B is selected, the project runs only the
  pre-registered final experiment allowed by frozen settings, saving completed,
  failed, timeout, infeasible, blocked, and missing rows as durable evidence.
- [ ] **EXEC-03**: If Path C is selected, or if Path A/B still produce
  `claim_ready=false`, the project formally locks the paper as a conditional
  diagnostic TR-E service-menu optimization manuscript.
- [ ] **EXEC-04**: Any regenerated artifact package records readiness JSON,
  source rows, artifact status, table/figure/claim maps, and strict
  `CLAIM_GUARD.json` as the only authority for claim upgrades.
- [ ] **EXEC-05**: The seven mainline policy tags remain the primary policy
  family unless a reduced family is formally justified and documented.

### Manuscript Claim Lock

- [ ] **LOCK-01**: The project converts every planned manuscript claim into a
  supported status/provenance claim, conditional diagnostic claim, unsupported
  claim, or future-work claim.
- [ ] **LOCK-02**: The manuscript claim table prohibits adaptive-menu
  dominance, adaptive-menu superiority, adaptive-window increment,
  near-optimal greedy, online tractability, case-study validation, real
  passenger behavior, and no-filter recommendations unless strict claim guard
  evidence explicitly authorizes them.
- [ ] **LOCK-03**: If the diagnostic path is selected, the paper thesis is
  reframed around service-menu formulation, paired-replay evaluation, and
  transparent claim-boundary analysis.
- [ ] **LOCK-04**: Sensitivity, tractability, and semi-real case materials
  retain diagnostic/provisional or scaffold-only labels unless regenerated
  evidence and claim guard status change.

### Final Decision

- [ ] **FINAL-01**: The milestone produces a final decision file stating
  `final_claim_ready_status`, manuscript path, allowed claims by manuscript
  section, prohibited claims, required next milestone, reviewer risks, and
  final recommendation.
- [ ] **FINAL-02**: The final decision runs the minimum import smoke from
  `work2_coding/` and records any unavailable or failed verification commands.
- [ ] **FINAL-03**: Relevant existing tests touched by this milestone are run
  or explicitly documented if unavailable, including artifact gates, paired
  replay, policy fairness, and manuscript claim guard tests.
- [ ] **FINAL-04**: The milestone ends only with an explicit outcome:
  claim-ready with authorized claims, claim-ready false with diagnostic lock,
  or not ready for manuscript because unresolved blockers remain.

## Deferred Requirements

- **MS-01**: Full manuscript drafting resumes only after v1.1 decides whether
  the paper is claim-ready empirical, conditional diagnostic, or not ready.
- **CASE-EXEC-01**: Semi-real case execution remains deferred unless upstream
  gates and the selected path explicitly authorize runtime evidence.
- **GREEDY-01**: New exact-vs-greedy stress evidence remains deferred unless
  Path B or a future milestone pre-registers a legitimate tractability run.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Hand-edited generated rows, tables, figures, or claim guards | Violates reproducibility and claim traceability. |
| Tuning on final results to force the desired ranking | Would make any positive claim scientifically invalid. |
| Removing `mainline_random_menu` because it outperforms adaptive on profit | The random baseline is a serious comparator and must stay visible. |
| Claiming adaptive-window value while adaptive and fixed-window outputs remain identical | Current evidence blocks the increment claim. |
| Treating no-filter variants as operational recommendations | No-filter is diagnostic unless formal evidence justifies stronger use. |
| Describing simulated demand or simulated choice as real passenger behavior | The current case material is scaffold-only and simulated where applicable. |
| Manuscript polishing before the claim path is decided | The milestone is about evidence gates and claim authority, not prose polish. |

## Traceability

| Requirement | Phase | Status |
| --- | --- | --- |
| EVID-01..EVID-04 | Phase 13 | Pending |
| GATE-01..GATE-04 | Phase 14 | Pending |
| DIAG-01..DIAG-04 | Phase 15 | Pending |
| PATH-01..PATH-04 | Phase 16 | Pending |
| EXEC-01..EXEC-05 | Phase 17 | Pending |
| LOCK-01..LOCK-04 | Phase 17 | Pending |
| FINAL-01..FINAL-04 | Phase 18 | Pending |

**Coverage:**
- v1.1 requirements: 29 total
- Mapped to phases: 29
- Unmapped: 0

---
*Requirements defined: 2026-06-16*
*Last updated: 2026-06-16 after v1.1 claim-ready resolution milestone initialization*
