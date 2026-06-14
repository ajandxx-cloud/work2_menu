# Roadmap: Work2 TR-C Paper Rewriting and Experiment Rebuild

## Execution Policy: Local-Only

This project is executed offline/local-only. Do not require git commit, git
push, remote branch creation, or PR publication as part of project progress,
verification, formal readiness, artifact generation, or manuscript preparation.

Git may be inspected only as a local provenance signal when useful, but project
completion must not depend on updating a remote git repository. For formal
evidence, prefer local reproducibility artifacts such as readiness JSON,
dependency snapshots, manifest hashes, checkpoint hashes, command logs, and
output-directory archives.

## Previous Milestone Summary

Phases 1-5 completed the V1 robust time-window service-menu pipeline, including
runtime-root audit, service-product contracts, mainline comparison contracts,
artifact pipeline and claim guards, and formal evidence readiness. The new
milestone continues numbering from Phase 6 because existing phase directories
are still present and no safe reset archive target is configured.

## Phase 6: Code And Experiment Audit

**Goal:** Audit DSPO, DSPO_PLUS, menu, time-window, pricing, RC data, and
artifact-state assumptions before changing behavior or making paper claims.

**Status:** Complete (2026-06-14)

**Success Criteria**:
1. `work2_coding/` import smoke passes.
2. Current DSPO/DSPO_PLUS/static/no-pricing code paths and manifests are
   located and classified.
3. RC dataset loading and split/seeding contracts are documented.
4. Current artifact claim blockers are summarized for the manuscript.
5. Failure states include reason, minimal fix, and rerun command.

**Requirements:** EXP-01, EXP-02, GATE-01, GATE-02, GATE-04

**Phase 6 completion note:** Audit matrix, verification report, and downstream
handoff are available in `.planning/phases/06-code-and-experiment-audit/` and
`work2_coding/outputs/phase6_audit/`. Formal claim readiness remains blocked by
`dirty_git`; Phase 6 did not run formal replay or advance manuscript ranking
claims.

## Phase 7: Model Consistency Repair

**Goal:** Align the paper and implementation around a single MNL-with-outside
option model and consistent DSPO/DSPO_PLUS definitions.

**Status:** Complete (2026-06-14)

**Success Criteria**:
1. Utility terms for price, IVT, walking distance, pickup/time-window
   feasibility, and outside option are consistent across manuscript, code, and
   experiments.
2. DSPO and DSPO_PLUS are distinguished without adding an out-of-scope
   algorithm family.
3. Opt-out is not counted as accepted home pickup.
4. Focused tests or script checks cover the repaired contracts.

**Requirements:** MODEL-01, MODEL-02, MODEL-03, MODEL-04, GATE-04

**Phase 7 completion note:** Runtime rows, artifact gates, and manuscript text
now record the MNL outside-option utility, explicit DSPO/DSPO_PLUS
`method_family`, and opt-out/home/meeting-point separation. Focused contract
tests and the Phase 7 model-consistency report passed. Empirical baseline and
DSPO/DSPO_PLUS ranking validation remains downstream in Phases 8-10.

## Phase 8: Baseline Validation

**Goal:** Validate no-pricing and static-pricing baselines under stable paired
replay before running the DSPO family ladder.

**Status:** Complete (2026-06-14)

**Success Criteria**:
1. No-pricing baseline runs without schema or checkpoint ambiguity.
2. Static-pricing baseline runs without schema or checkpoint ambiguity.
3. Baseline rows include source run IDs, manifest hashes, checkpoint status, and
   opt-out/home-pickup separation.
4. Baseline failure blocks Phase 9 and reports minimal repair steps.

**Requirements:** EXP-03, GATE-01, GATE-02, GATE-04

**Phase 8 completion note:** Paired actual replay completed for
`mainline_optimized_mw` and `phase8_static_flat_markdown` across five
formal-equivalent splits. The Phase 8 report passed baseline validation and
opened the Phase 9 release gate, while keeping `claim_ready=false` because
formal ranking artifacts still require dependency snapshot and clean git
provenance.

## Phase 9: DSPO Family Full Run

**Goal:** Run and gate DSPO clip/wide configurations under the same paired
replay contract as the baselines.

**Status:** Pending

**Success Criteria**:
1. DSPO clip and DSPO wide variants are executable.
2. DSPO runs share comparable request traces, seeds, pricing mode, and routing
   settings with baselines.
3. Ranking sanity checks are generated without manuscript overclaiming.
4. Any failure enters a debug loop before Phase 10.

**Requirements:** EXP-04, GATE-01, GATE-02, GATE-04

## Phase 10: DSPO_PLUS Full Run

**Goal:** Run and gate DSPO_PLUS clip/wide configurations, then verify whether
the target ranking is actually reproduced.

**Status:** Pending

**Success Criteria**:
1. DSPO_PLUS clip and DSPO_PLUS wide variants are executable.
2. DSPO_PLUS comparisons share paired replay state with DSPO and baselines.
3. The target ranking `DSPO_PLUS > DSPO > Static Pricing > No Pricing` is
   verified or explicitly blocked.
4. If DSPO_PLUS does not exceed DSPO, a debug report states failure reason,
   minimal fix, and rerun instruction.

**Requirements:** EXP-04, EXP-05, GATE-01, GATE-02, GATE-04

## Phase 11: Paper Writing Generation And Reviewer Risk

**Goal:** Generate the TR-C manuscript draft, tables, method comparison summary,
GSD execution report, ablation plan/results, and reviewer-style risk analysis
only after the experiment gates allow the corresponding claims.

**Status:** Pending

**Success Criteria**:
1. The main manuscript uses Elsevier CAS double-column formatting.
2. The paper follows the requested TR-C section structure.
3. Results sections distinguish implemented framework, diagnostic evidence,
   blocked evidence, and claim-ready evidence.
4. Ablation sections cover time windows, menu expansion, and DSPO_PLUS gap
   decomposition.
5. Reviewer-style risk analysis covers novelty, modeling weakness, experiment
   weakness, and acceptance probability.

**Requirements:** PAPER-01, PAPER-02, PAPER-03, PAPER-04, ABL-01, ABL-02, ABL-03, REV-01, GATE-03, GATE-04

---
*Roadmap updated: 2026-06-14 for milestone v1.1 paper rewriting and experiment rebuild*
