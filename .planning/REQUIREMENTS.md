# Requirements: Work2_ChoiceAware_DRT_Menu_Optimization

**Defined:** 2026-06-04
**Core Value:** Complete reproducible experiments that support or falsify the claim that choice-aware expected-profit menu optimization gives a stronger profit-service tradeoff than insertion-cost-only menu selection.

## v1 Requirements

### Project Framing

- [x] **FRAME-01**: Project documents state that CNN-SetMenuNet is now a baseline / diagnostic method, not the main positive contribution.
- [x] **FRAME-02**: Project documents define the new research question around passenger choice, finite menus, dynamic pricing, route-cost feedback, and opt-out risk.
- [x] **FRAME-03**: The rewritten 6.4 discussion file explains why insertion-cost ranking metrics can detach from realized net profit.
- [x] **FRAME-04**: The rewritten 6.4 discussion file defines the new paper contribution in terms of choice-aware dynamic service menu optimization.

### Objective And Metrics

- [x] **OBJ-01**: The experiment pipeline exposes `adjusted_profit` or an equivalent quit-penalized metric.
- [x] **OBJ-02**: The experiment pipeline exposes service-constrained evaluation for policies whose `quit_rate` exceeds a configured guardrail.
- [x] **OBJ-03**: Metric summaries separate raw `net_profit`, adjusted/service-constrained profit, `quit_rate`, `avg_walk`, route cost, and menu regret.
- [x] **OBJ-04**: Diagnostic reports explicitly flag high-quit policies that appear profitable only because they avoid service.

### Oracle Contract

- [x] **ORCL-01**: Cost Oracle is defined as selecting menus by true insertion cost.
- [x] **ORCL-02**: Profit Oracle is defined as selecting menus by expected profit under the choice/pricing/route-cost objective.
- [x] **ORCL-03**: Realized Oracle is either implemented as an ex-post diagnostic upper bound or explicitly marked infeasible for v1 with reason.
- [x] **ORCL-04**: Tables and prose avoid calling Cost Oracle a profit upper bound.

### Methods

- [x] **METH-01**: Expected-Profit Enumeration enumerates all `C(10,3)=120` meeting-point menus for `K=10`, `L=3`.
- [x] **METH-02**: Expected-Profit Enumeration includes the home option as always shown outside public `L`.
- [x] **METH-03**: Each enumerated menu computes MNL choice probability, expected revenue, expected route cost, and opt-out penalty or service cost.
- [x] **METH-04**: Service-Constrained Expected-Profit selects the best expected-profit menu satisfying a quit-rate guardrail, or falls back with an explicit diagnostic.
- [x] **METH-05**: Existing baselines remain comparable: Nearest-L, Cost-L heuristic, CNN-Menu, old CNN-SetMenuNet, and Cost Oracle.
- [x] **METH-06**: New policy names are wired through parser choices, manifests, normalized rows, and artifact summaries.

### Pilot Experiments

- [x] **PILOT-01**: A smoke study runs the new methods on a minimal RC setting without a formal budget.
- [x] **PILOT-02**: A 3-seed pilot runs `instance=RC`, `K=10`, `L=3`, home always shown, seeds `0,1,2`.
- [x] **PILOT-03**: Pilot outputs include `pilot_rows.csv`, `pilot_summary.md`, `oracle_diagnostics.md`, `profit_vs_quit_tradeoff.md`, and `phase08_decision.md`.
- [x] **PILOT-04**: Pilot decision classifies whether to proceed to formal evidence, recalibrate objective parameters, or diagnose simulation/scenario issues.

### Formal Evidence

- [ ] **FORM-01**: If pilot passes, formal evidence runs at least five seeds on RC with the approved train/test budget.
- [ ] **FORM-02**: Formal evidence compares old insertion-cost policies against Expected-Profit and Service-Constrained Expected-Profit methods.
- [ ] **FORM-03**: Formal artifact generation creates paper-ready tables/figures without manual row editing.
- [ ] **FORM-04**: Formal conclusion wording distinguishes RC evidence, robustness evidence, and diagnostic evidence.

### Learning Extension

- [ ] **LEARN-01**: If enumeration supports the new objective, define a ProfitAware option-level or menu-level learning target.
- [ ] **LEARN-02**: ProfitAware learning is compared against exact expected-profit enumeration as a teacher / upper reference.
- [ ] **LEARN-03**: Menu-level learning is deferred until the non-learning expected-profit objective produces a stable positive signal.

### Verification

- [x] **VER-01**: Each phase produces a verification note listing changed files, tests/commands run, generated outputs, and whether conclusions are supported.
- [x] **VER-02**: Verification confirms Work 1 pricing, choice, and routing cores were not changed unless explicitly approved.
- [x] **VER-03**: Verification checks that generated artifacts trace back to real study outputs.
- [x] **VER-04**: Verification reports failed or skipped commands with concrete reason.

## v2 Requirements

### Extended Evidence

- **V2-01**: Add MNL parameter sensitivity for price, walk, IVT, and outside-option utility.
- **V2-02**: Add cross-instance evidence beyond RC after RC formal evidence is stable.
- **V2-03**: Add ProfitAware-MLP / ProfitAware-SetMenu / ProfitAware-CNNSetMenu learning variants.
- **V2-04**: Add contextual bandit or offline policy learning only after objective alignment is established.
- **V2-05**: Add visualization of profit-quit Pareto fronts and menu diversity effects for manuscript explanation.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Forcing CNN-SetMenuNet as the main method | Existing formal evidence does not support that as the central claim |
| Rewriting pricing | Would confound whether menu objective alignment solves the problem |
| Rewriting MNL choice behavior | The first goal is to operate within the existing behavioral model |
| Rewriting HGS routing | Route-cost feedback should remain the stable evaluation backend |
| Immediate contextual bandit implementation | Too complex before expected-profit enumeration proves value |
| Manual artifact editing | Breaks reproducibility and scientific traceability |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| FRAME-01..FRAME-04 | Phase 1 | Complete |
| OBJ-01..OBJ-04 | Phase 2 | Complete |
| ORCL-01..ORCL-04 | Phase 2 | Complete |
| METH-01..METH-06 | Phase 3 | Complete |
| PILOT-01..PILOT-04 | Phase 4 | Pending |
| FORM-01..FORM-04 | Phase 5 | Pending |
| LEARN-01..LEARN-03 | Phase 6 | Pending |
| VER-01..VER-04 | Phase 1-2 | Complete |

**Coverage:**
- v1 requirements: 32 total
- Mapped to phases: 32
- Unmapped: 0

---
*Requirements defined: 2026-06-04*
*Last updated: 2026-06-04 after Phase 3 verification*
