# Requirements: Work2 TR-C Paper Rewriting and Experiment Rebuild

**Defined:** 2026-06-14
**Core Value:** A defensible TR-C manuscript whose DSPO, DSPO_PLUS,
static-pricing, and no-pricing comparisons are reproducible, behaviorally
coherent, and gated before empirical superiority claims are made.

## v1.1 Requirements

### Manuscript Structure

- [ ] **PAPER-01**: The main LaTeX manuscript uses Elsevier CAS double-column
  formatting through `cas-dc`.
- [ ] **PAPER-02**: The manuscript follows the TR-C structure: Introduction,
  Literature Review, Problem Formulation, Methodology, Experimental Design,
  Results, Ablation Study, and Conclusion.
- [ ] **PAPER-03**: The manuscript states current artifact and claim-gate status
  explicitly before any empirical ranking language.
- [ ] **PAPER-04**: The manuscript includes or reserves reviewer-facing risk
  analysis covering novelty, modeling weakness, experiment weakness, and
  acceptance probability.

### Model And Choice Consistency

- [x] **MODEL-01**: The paper and code use a consistent MNL choice model with an
  outside option.
- [x] **MODEL-02**: Utility terms are aligned around price sensitivity,
  in-vehicle time, walking distance, and pickup/time-window feasibility.
- [x] **MODEL-03**: DSPO and DSPO_PLUS are defined as distinct model families
  without introducing a new out-of-scope RL method.
- [x] **MODEL-04**: Opt-out, accepted home pickup, and accepted meeting-point
  pickup remain separate in metrics and manuscript language.

### Experiment Rebuild

- [ ] **EXP-01**: Phase work audits the DSPO, DSPO_PLUS, menu, pricing, and
  time-window pipeline before behavior changes.
- [ ] **EXP-02**: The RC dataset pipeline is verified as the primary formal
  experiment source.
- [x] **EXP-03**: No-pricing and static-pricing baselines run stably before DSPO
  or DSPO_PLUS claims are advanced.
- [x] **EXP-04**: DSPO clip/wide and DSPO_PLUS clip/wide configurations are
  executable under paired replay.
- [ ] **EXP-05**: The target ranking
  `DSPO_PLUS > DSPO > Static Pricing > No Pricing` is treated as a validation
  gate and is not asserted until reproduced.

### Evidence And Artifact Gates

- [x] **GATE-01**: Checkpoint load status is explicit in normalized rows and
  manuscript-facing metadata.
- [x] **GATE-02**: Placeholder-only, blocked, diagnostic, and no-filter-only
  rows are excluded from formal ranking claims.
- [ ] **GATE-03**: Generated tables and figures are consumed from artifact
  builders rather than edited by hand.
- [ ] **GATE-04**: Every failed phase reports failure reason, minimal fix, and
  rerun instruction before the roadmap advances.

### Ablation And Reviewer Readiness

- [ ] **ABL-01**: The paper includes a gated ablation plan for removing time
  windows.
- [ ] **ABL-02**: The paper includes a gated ablation plan for removing menu
  expansion.
- [ ] **ABL-03**: The paper includes a DSPO vs DSPO_PLUS gap-decomposition plan.
- [ ] **REV-01**: The final milestone output includes a reviewer-style risk
  analysis with novelty, modeling, experiment, and acceptance-probability notes.

## Deferred Requirements

- **EXT-01**: Yanjiao or additional external data extensions are future work
  unless formal RC gates pass and the user explicitly expands scope.
- **ATT-01**: Attention-based choice/scoring remains diagnostic or V2 work.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Hand-edited generated evidence | Evidence must remain reproducible from code and artifact builders. |
| No-filter formal recommendation | No-filter is diagnostic unless separately justified. |
| Unverified DSPO_PLUS dominance claim | The ranking is a gate, not a premise. |
| New RL algorithm family | The milestone scope is DSPO/DSPO_PLUS consistency and paper rebuild. |
| Parallel `ooh_code/` runtime | `work2_coding/` is active and verified. |

## Traceability

| Requirement | Phase | Status |
| --- | --- | --- |
| PAPER-01..PAPER-04 | Phase 11 | Pending |
| MODEL-01..MODEL-04 | Phase 7 | Complete |
| EXP-01, EXP-02 | Phase 6 | Phase 6 audit complete; downstream experiment validation still pending |
| EXP-03 | Phase 8 | Complete |
| EXP-04 | Phase 9, Phase 10 | Complete |
| EXP-05 | Phase 10 | Pending |
| GATE-01..GATE-04 | Phase 6..Phase 11 | Phase 6 audit complete; formal claim gates still active |
| ABL-01..ABL-03, REV-01 | Phase 11 | Pending |

**Coverage:**
- v1.1 requirements: 20 total
- Mapped to phases: 20
- Unmapped: 0

---
*Requirements defined: 2026-06-14*
*Last updated: 2026-06-14 after Phase 6 audit completion*
