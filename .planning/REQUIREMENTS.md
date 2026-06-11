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

- [x] **ACCT-01**: System can represent passenger outcomes as `accepted_home`, `accepted_meeting_point`, or `opted_out`.
- [x] **ACCT-02**: System prevents `opted_out` events from mutating route plans as accepted home service.
- [x] **ACCT-03**: System records opt-out count, acceptance rate, service cost, and route-state effects correctly.
- [x] **ACCT-04**: System exposes checkpoint load success, failure, intentional mismatch, and checkpoint provenance in result metadata.

### Robust Filtering

- [x] **ETA-01**: System supports ETA filter modes `hard`, `calibrated`, `interval_overlap`, `chance_constraint`, `soft_penalty`, and `none`.
- [x] **ETA-02**: System records candidate-level ETA diagnostics including predicted ETA, sigma, interval bounds, window bounds, pass/fail, violation probability, and prune reason.
- [x] **ETA-03**: System ensures no-filter disables ETA pruning only, not routing or capacity feasibility.
- [x] **ETA-04**: System ensures soft-penalty preserves candidates while changing objective value through time-risk penalty.

### Menu Optimization

- [x] **MENU-01**: System evaluates menus with expected profit, opt-out penalty, ETA risk penalty, and service guardrails.
- [x] **MENU-02**: System applies pricing and system-aware cost definitions consistently across compared policies.
- [x] **MENU-03**: System uses exact enumeration only for small candidate sets and greedy forward selection for larger sets.
- [x] **MENU-04**: System logs exact-vs-greedy value, relative gap, overlap, build time, candidate count, and enumerated menu count.

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

## v2.1 Requirements

### Audit Closure And Traceability

- [x] **TRACE-01**: Project has a Phase 2 verification artifact that records ACCT-01..04, ETA-01..04, and MENU-01..04 with command-backed evidence or explicit gaps.
- [x] **TRACE-02**: Project has Phase 2 validation evidence because `workflow.nyquist_validation` is enabled.
- [x] **TRACE-03**: Requirements traceability no longer contradicts Phase 2 summaries, verification, or validation artifacts.
- [x] **TRACE-04**: MENU-02 is reconciled with explicit pricing/system-aware cost evidence or a documented remaining gap.
- [x] **TRACE-05**: Phase 07 records a pass/fail gate before Phase 08 begins.

### Repository Hygiene And Provenance

- [x] **PROV-01**: Dirty and untracked files are classified into planning docs, generated artifacts, local outputs, dependency files, deleted user documents, and other local state.
- [x] **PROV-02**: `.gitignore` prevents future venv, cache, temporary output, and large local artifact tracking risks.
- [x] **PROV-03**: Generated artifacts to track versus keep local are documented.
- [x] **PROV-04**: Evidence runs can report `git_dirty=false`, or `git_dirty=true` with a narrow documented reason.

### Shared Checkpoints

- [x] **CKPT-01**: A stable shared checkpoint training entry point exists for the attention evidence family.
- [x] **CKPT-02**: Pilot and formal checkpoints are real trained weights, not placeholders.
- [x] **CKPT-03**: Checkpoint sidecars record sha256, training command, seed, split, dataset, run_id, git commit, dirty status, training args, and timestamp.
- [x] **CKPT-04**: Checkpoints load through the same code path used by `run_study.py`.
- [x] **CKPT-05**: Missing, mismatched, or random-weight checkpoints are refused for pilot/formal evidence.

### Pilot Evidence

- [x] **PILOT-01**: `pilot_attention_dspo` completes with non-placeholder rows and loaded checkpoint provenance.
- [x] **PILOT-02**: Every attention pair contains both `DSPO_original` and `DSPO_attention`.
- [x] **PILOT-03**: Low and medium uptake regimes are present and behaviorally live.
- [x] **PILOT-04**: Pilot artifacts and claim guard are rebuilt from the completed run.
- [x] **PILOT-05**: Pilot summary reports primary and secondary paired deltas, attention weights, checkpoint provenance, and regime-level results.
- [x] **PILOT-06**: A written go/no-go decision controls whether formal evidence or ablation follows.

### Attention Ablation

- [ ] **ABLT-01**: Pilot-only attention strength, feature, and ETA-variant ablation manifests exist when pilot evidence is weak.
- [ ] **ABLT-02**: Ablations pre-register varied fields and selection criteria before execution.
- [ ] **ABLT-03**: Paired replay fairness is preserved; only declared attention fields vary.
- [ ] **ABLT-04**: Exactly one formal candidate configuration is selected before formal, or the superiority claim is stopped.

### Formal Enablement

- [ ] **FORM-01**: Formal actual replay is no longer blocked by the old unconditional guard when strict evidence gates are satisfied.
- [ ] **FORM-02**: Formal execution requires `tier=formal`, `actual_execution=true`, `require_checkpoint=true`, existing checkpoint, loaded status, non-empty hash, non-placeholder rows, and git provenance.
- [ ] **FORM-03**: Formal execution fails closed with blocker metadata for missing checkpoints or invalid provenance.
- [ ] **FORM-04**: Formal placeholder rows are impossible.
- [ ] **FORM-05**: Formal contract-only, missing-checkpoint, loaded-checkpoint, and placeholder-impossibility tests exist.

### Formal Evidence And Claim Decision

- [ ] **CLAIM-01**: `formal_attention_dspo` completes with non-placeholder, checkpoint-loaded, paired formal rows.
- [ ] **CLAIM-02**: Formal artifacts report primary and secondary paired deltas, regime deltas, and variance/confidence summaries.
- [ ] **CLAIM-03**: Diagnostic and cost-bound policies are not ranked as method baselines.
- [ ] **CLAIM-04**: `ATTENTION_CLAIM_GUARD.json` alone decides whether attention-improves-DSPO language is allowed.
- [ ] **CLAIM-05**: Manuscript support and milestone archive status match artifact status and final validation/audit results.

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
| ACCT-01 | Phase 2 | Complete |
| ACCT-02 | Phase 2 | Complete |
| ACCT-03 | Phase 2 | Complete |
| ACCT-04 | Phase 2 | Complete |
| ETA-01 | Phase 2 | Complete |
| ETA-02 | Phase 2 | Complete |
| ETA-03 | Phase 2 | Complete |
| ETA-04 | Phase 2 | Complete |
| MENU-01 | Phase 2 | Complete |
| MENU-02 | Phase 2 | Complete |
| MENU-03 | Phase 2 | Complete |
| MENU-04 | Phase 2 | Complete |
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
| TRACE-01 | Phase 7 | Complete |
| TRACE-02 | Phase 7 | Complete |
| TRACE-03 | Phase 7 | Complete |
| TRACE-04 | Phase 7 | Complete |
| TRACE-05 | Phase 7 | Complete |
| PROV-01 | Phase 8 | Complete |
| PROV-02 | Phase 8 | Complete |
| PROV-03 | Phase 8 | Complete |
| PROV-04 | Phase 8 | Complete |
| CKPT-01 | Phase 9 | Complete |
| CKPT-02 | Phase 9 | Complete |
| CKPT-03 | Phase 9 | Complete |
| CKPT-04 | Phase 9 | Complete |
| CKPT-05 | Phase 9 | Complete |
| PILOT-01 | Phase 10 | Complete |
| PILOT-02 | Phase 10 | Complete |
| PILOT-03 | Phase 10 | Complete |
| PILOT-04 | Phase 10 | Complete |
| PILOT-05 | Phase 10 | Complete |
| PILOT-06 | Phase 10 | Complete |
| ABLT-01 | Phase 11 | Planned |
| ABLT-02 | Phase 11 | Planned |
| ABLT-03 | Phase 11 | Planned |
| ABLT-04 | Phase 11 | Planned |
| FORM-01 | Phase 12 | Planned |
| FORM-02 | Phase 12 | Planned |
| FORM-03 | Phase 12 | Planned |
| FORM-04 | Phase 12 | Planned |
| FORM-05 | Phase 12 | Planned |
| CLAIM-01 | Phase 13 | Planned |
| CLAIM-02 | Phase 13 | Planned |
| CLAIM-03 | Phase 13 | Planned |
| CLAIM-04 | Phase 13 | Planned |
| CLAIM-05 | Phase 13 | Planned |

**Coverage:**
- v1 requirements: 28 total
- Mapped to phases: 28
- Unmapped: 0
- v2 attention-pivot requirements: 5 mapped to Phase 6
- v2.1 evidence-ladder requirements: 34 mapped to Phases 7-13

---
*Requirements defined: 2026-06-10*
*Last updated: 2026-06-11 starting milestone v2.1*
