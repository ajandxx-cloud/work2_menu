# Roadmap: Akkerman RC No-Failure-Cost Reproduction

## Phase 1: Runtime Repair And Reproduction Runner

**Goal:** Implement the no-home-failure-cost RC reproduction flow in `work2_coding/`.

**Success Criteria**:
1. Parser/config/choice layers support disabled outside option and exact service modes.
2. Failure cost is zero in training, PPO terminal reward, evaluation, and summaries.
3. `scripts/run_akkerman_rc_no_failure.py` supports dry run, smoke run, analysis, and seed lists.
4. `tests/test_akkerman_rc_no_failure.py` verifies the core accounting and output contracts.
5. Smoke execution produces raw CSV, summary CSV, and summary JSON without touching paper artifacts.

**Requirements:** RUN-01, RUN-02, RUN-03, ACC-01, ACC-02, ACC-03, ACC-04, EXP-01, EXP-02, EXP-03, EXP-04, EXP-05

---
*Roadmap created: 2026-06-12 after initialization*
