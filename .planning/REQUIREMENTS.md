# Requirements: Work2 Attention-Enhanced DSPO Menu Optimization for Many-to-One DRT

**Defined:** 2026-06-10
**Core Value:** Produce defensible Work2 evidence that attention-enhanced DSPO improves the original DSPO method under reproducible paired replay.

## v1 Requirements

### Audit

- [x] **AUDIT-01**: Researcher can identify the active runtime root and distinguish current files from stale planning references.
- [x] **AUDIT-02**: Researcher can run an import smoke test for the active package and record the result.
- [x] **AUDIT-03**: Researcher can list available runner scripts, missing runner scripts, existing menu policies, and relevant simulator modules.
- [x] **AUDIT-04**: Researcher can produce a concise Stage 0 audit report before modifying algorithm behavior.

### Accounting

- [ ] **ACCT-01**: System can represent passenger outcomes as `accepted_home`, `accepted_meeting_point`, or `opted_out`.
- [ ] **ACCT-02**: System prevents `opted_out` events from mutating route plans as accepted home service.
- [ ] **ACCT-03**: System records opt-out count, acceptance rate, service cost, and route-state effects correctly.
- [ ] **ACCT-04**: System exposes checkpoint load success, failure, intentional mismatch, and checkpoint provenance in result metadata.

### Robust Filtering

- [ ] **ETA-01**: System supports ETA filter modes `hard`, `calibrated`, `interval_overlap`, `chance_constraint`, `soft_penalty`, and `none`.
- [ ] **ETA-02**: System records candidate-level ETA diagnostics including predicted ETA, sigma, interval bounds, window bounds, pass/fail, violation probability, and prune reason.
- [ ] **ETA-03**: System ensures no-filter disables ETA pruning only, not routing or capacity feasibility.
- [ ] **ETA-04**: System ensures soft-penalty preserves candidates while changing objective value through time-risk penalty.

### Menu Optimization

- [ ] **MENU-01**: System evaluates menus with expected profit, opt-out penalty, ETA risk penalty, and service guardrails.
- [ ] **MENU-02**: System applies pricing and system-aware cost definitions consistently across compared policies.
- [ ] **MENU-03**: System uses exact enumeration only for small candidate sets and greedy forward selection for larger sets.
- [ ] **MENU-04**: System logs exact-vs-greedy value, relative gap, overlap, build time, candidate count, and enumerated menu count.

### Experiments

- [x] **EXP-01**: Project defines smoke, pilot, and formal study contracts for robust time-window menu experiments.
- [x] **EXP-02**: Experiments compare full display, home only, nearest heuristic, top-k cheapest, min-lateness, hard filter, no-filter diagnostic, robust time-window menu, and optional random top-k.
- [x] **EXP-03**: Every formal comparison uses paired request traces, shared predictor checkpoints, fixed seeds, split IDs, pricing mode, and HGS/routing parameters.
- [x] **EXP-04**: Experiments include uptake-regime checks so results are not based only on degenerate opt-out behavior.

### Artifacts

- [x] **ART-01**: Pipeline writes normalized rows and aggregate summaries with policy tag, seed, split, trace ID, checkpoint status, menu settings, and filter mode.
- [x] **ART-02**: Pipeline builds robust filtering, exact-greedy, uptake-regime, ETA diagnostics, profit decomposition, and uncertainty/gap tables.
- [x] **ART-03**: Pipeline builds figures for net-profit gap, acceptance/opt-out, false-negative pruning, home-only menu share, ETA error quantiles, and exact/greedy build time.
- [x] **ART-04**: Artifact status records source run ID, manifest hash, git marker, checkpoint path/hash, completed/incomplete status, and placeholder flag.

### Manuscript

- [x] **PAPER-01**: Project produces a method outline covering service bundles, displayed menu decision, outside option, ETA uncertainty, MNL choice, pricing, robust filter, and exact/greedy solver.
- [x] **PAPER-02**: Project produces an experiment outline covering datasets/scenarios, baselines, metrics, paired replay, seeds, and splits.
- [x] **PAPER-03**: Project produces a result outline for exact-vs-greedy quality, robust filtering comparison, uptake-regime behavior, external/semi-real check, and limitations.
- [x] **PAPER-04**: Project maintains a claim checklist that prevents universal dominance, real passenger validation, no-filter operational recommendation, or full dynamic-system exact-optimality claims without evidence.

## v2 Requirements

### Behavioral Enhancements

- **BEHAV-01**: System can test attention-based menu-aware choice/scoring as an ablation or extension.
- **BEHAV-02**: System can test decision-focused menu regret or oracle-label ranking after robust pipeline evidence is stable.

### Attention Evidence Pivot

- **ATTN-01**: System exposes explicit `DSPO_original` and `DSPO_attention` variants without conflating robust-menu diagnostics with the main method comparison.
- **ATTN-02**: Attention-enhanced DSPO integrates attention into candidate/menu scoring or cost prediction while preserving opt-out accounting, checkpoint metadata, and routing feasibility.
- **ATTN-03**: Attention-vs-original experiments use paired replay with identical request traces, seeds, split IDs, pricing mode, routing/HGS settings, and checkpoint policy.
- **ATTN-04**: Artifacts and claim guards report attention-vs-original DSPO deltas and only allow superiority claims from completed, non-placeholder paired evidence.

### Calibration Enhancements

- **CAL-01**: System can estimate distance-band or candidate-type ETA sigma after global-sigma robust policies are complete.
- **CAL-02**: System can incorporate survey or revealed-preference data if available.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Work3 many-to-many DRT | Separate dissertation workstream |
| Work4 planning | Separate dissertation workstream |
| Full simulator rewrite | Current code has reusable DSPO, simulator, and routing infrastructure |
| Manual edits to generated result rows | Breaks reproducibility and provenance |
| Universal real-world behavioral claims | Current evidence is simulation-based unless new external behavior data is added |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| AUDIT-01 | Phase 1 | Complete |
| AUDIT-02 | Phase 1 | Complete |
| AUDIT-03 | Phase 1 | Complete |
| AUDIT-04 | Phase 1 | Complete |
| ACCT-01 | Phase 2 | Pending |
| ACCT-02 | Phase 2 | Pending |
| ACCT-03 | Phase 2 | Pending |
| ACCT-04 | Phase 2 | Pending |
| ETA-01 | Phase 2 | Pending |
| ETA-02 | Phase 2 | Pending |
| ETA-03 | Phase 2 | Pending |
| ETA-04 | Phase 2 | Pending |
| MENU-01 | Phase 2 | Pending |
| MENU-02 | Phase 2 | Pending |
| MENU-03 | Phase 2 | Pending |
| MENU-04 | Phase 2 | Pending |
| EXP-01 | Phase 3 | Complete |
| EXP-02 | Phase 3 | Complete |
| EXP-03 | Phase 3 | Complete |
| EXP-04 | Phase 3 | Complete |
| ART-01 | Phase 4 | Complete |
| ART-02 | Phase 4 | Complete |
| ART-03 | Phase 4 | Complete |
| ART-04 | Phase 4 | Complete |
| PAPER-01 | Phase 5 | Complete |
| PAPER-02 | Phase 5 | Complete |
| PAPER-03 | Phase 5 | Complete |
| PAPER-04 | Phase 5 | Complete |
| BEHAV-01 | Phase 6 | Complete |
| ATTN-01 | Phase 6 | Complete |
| ATTN-02 | Phase 6 | Complete |
| ATTN-03 | Phase 6 | Complete |
| ATTN-04 | Phase 6 | Complete |

**Coverage:**
- v1 requirements: 28 total
- Mapped to phases: 28
- Unmapped: 0
- v2 attention-pivot requirements: 5 mapped to Phase 6

---
*Requirements defined: 2026-06-10*
*Last updated: 2026-06-11 after Phase 6 execution*
