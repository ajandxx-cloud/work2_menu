# Requirements: Akkerman RC No-Failure-Cost Reproduction

**Defined:** 2026-06-12
**Core Value:** Produce a defensible Table-2-style RC reproduction where failure cost is truly absent.

## v1 Requirements

### Runtime

- [ ] **RUN-01**: The active runtime root is `work2_coding/`, with no new `ooh_code/` root created.
- [ ] **RUN-02**: `Hindsight`, `Foresight`, and `PPO` can pass CLI/parser/runtime compatibility checks.
- [ ] **RUN-03**: `outside_option_util=None` disables customer exit in menu choice.

### Accounting

- [ ] **ACC-01**: Training reward excludes home-delivery failure cost.
- [ ] **ACC-02**: PPO terminal reward excludes home-delivery failure cost.
- [ ] **ACC-03**: Evaluation reports `failure_costs=0` and total cost excludes failure cost.
- [ ] **ACC-04**: Summary CSV/JSON records zero failure cost and does not subtract it after aggregation.

### Experiment

- [ ] **EXP-01**: The runner supports `--dry_run`, `--smoke`, `--analyze`, and `--seeds`.
- [ ] **EXP-02**: The default experiment runs `NoOOH`, `OnlyOOH`, `NoPricing`, `StaticPricing`, and `DSPO`.
- [ ] **EXP-03**: NoOOH yields home delivery share at least 0.999.
- [ ] **EXP-04**: OnlyOOH yields home delivery share at most 0.001.
- [ ] **EXP-05**: Raw CSV, summary CSV, and summary JSON follow the requested Table-2-style schema.

## v2 Requirements

(None)

## Out of Scope

| Feature | Reason |
|---------|--------|
| Manuscript edits | The task is code and reproducible experiment setup only. |
| DRPO/SPO/attention methods | The target is Akkerman DSPO reproduction, not new method development. |
| Historical artifact edits | Results must be regenerated, not hand-edited. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| RUN-01 | Phase 1 | Pending |
| RUN-02 | Phase 1 | Pending |
| RUN-03 | Phase 1 | Pending |
| ACC-01 | Phase 1 | Pending |
| ACC-02 | Phase 1 | Pending |
| ACC-03 | Phase 1 | Pending |
| ACC-04 | Phase 1 | Pending |
| EXP-01 | Phase 1 | Pending |
| EXP-02 | Phase 1 | Pending |
| EXP-03 | Phase 1 | Pending |
| EXP-04 | Phase 1 | Pending |
| EXP-05 | Phase 1 | Pending |

---
*Requirements defined: 2026-06-12*
*Last updated: 2026-06-12 after initialization*
