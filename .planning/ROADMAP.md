# Roadmap: Work2_TR_E_Service_Menu_Optimization_Final

## Execution Policy

This roadmap follows the attached GSD new-project prompt, translated to the
current repository convention that repository audit starts as Phase 1. The
attached prompt's Phase 0 is therefore Phase 1 here; attached Phases 1-11 map
to Phases 2-12.

Execute locally from `work2_coding/` unless a phase explicitly works on
planning, manuscript, or root-level artifact files. Do not modify algorithm
behavior before Phase 1 locks current state. Do not make manuscript claims from
smoke-only, diagnostic-only, placeholder-only, blocked, or failed rows.

## Additional Gate Rules

1. Phase 5 is conditional. If Phase 4 shows that formal RC evidence supports at
   least one central paper claim with stable paired differences, Phase 5 may be
   marked `skipped-by-gate`. If Phase 4 evidence is weak, unstable, or
   unsupported, Phase 5 becomes mandatory.
2. Phase 7 is conditional. If Phase 6 decides that a real or semi-real case
   study is infeasible or not valuable, Phase 7 is skipped and Phase 8 starts.
   The manuscript must then state explicitly that external case validation is
   deferred.
3. If Phase 4 finds that RC formal evidence does not support any defensible
   central claim, do not continue mechanically into case study and sensitivity.
   First produce failure diagnosis and paper reframing guidance.
4. Phase 2 must produce a paper-level mathematical model skeleton, not only a
   prose research plan.
5. Phase 4 must report paired differences by split and uptake regime. If seed
   count is too small for formal statistical testing, report effect sizes and
   confidence intervals where feasible and avoid strong significance language.
6. Phase 8 sensitivity experiments are divided into must-have and nice-to-have
   groups. Must-have: `menu_k`, ETA uncertainty/filter mode, uptake regime, and
   opt-out guardrail. Nice-to-have: candidate pool size, fleet/capacity stress,
   and pricing sensitivity.
7. If optimized adaptive `m+w+p` does not strongly dominate, reframe the paper
   as a conditional service-menu optimization study instead of forcing a
   universal superiority claim.
8. If formal readiness is blocked by `dirty_git`, do not revert files automatically. Produce `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md` listing relevant modified/deleted files, blockers, and recommended cleanup/commit/stash actions. Request user confirmation before any destructive cleanup.

9. If formal replay fails, save failed rows with `status`, `error_type`, and `error_message` metadata. Produce `.planning/results/FORMAL_FAILURE_DIAGNOSIS.md` before Phase 4 claim validation.

10. If no suitable public real dataset is available, build a clearly labeled semi-real case using documented geography, a reproducible distance matrix, and simulated sequential demand. Do not describe simulated demand or simulated choice behavior as real observations.

11. Every paper-facing table or figure must record its source artifact path and the exact manuscript claim it supports.

## Phase 1: Repository Audit And State Locking

**Status:** Complete (2026-06-14)

**Goal:** Confirm current repository state, active runtime root, relevant
manifests, tests, artifact paths, and blockers before behavior changes.

**Success Criteria:**
1. Import smoke passes from `work2_coding/`.
2. `work2_coding/` is confirmed as active runtime root.
3. Current Work2 objective is service menu optimization, not old Akkerman
   reproduction and not old TR-C DSPO_PLUS ladder planning.
4. Seven-tag mainline family is confirmed from manifests/adapters.
5. Formal replay/checkpoint status is verified from actual files.
6. Available tests for service-product contracts, menu adapters, paired replay,
   artifact gates, formal readiness, and study execution are inventoried.
7. `.planning/STATE_LOCK.md` is written.

**Requirements:** STATE-01, STATE-02, STATE-03

**Verification:**
```powershell
cd work2_coding
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
```

## Phase 2: Paper-Level Research Design Lock

**Status:** Complete (2026-06-15)

**Goal:** Turn the project into a TR Part E paper plan rather than an experiment
script collection.

**Success Criteria:**
1. `.planning/paper/TR_E_RESEARCH_DESIGN.md` defines problem, service product,
   decisions, passenger choice, objective, guardrails, solver, benchmarks,
   metrics, claims, and non-claims.
2. V1 evidence, V2 attention diagnostics, appendix evidence, and non-claims are
   separated.
3. Main tables and figures are defined before formal experiments.
4. Every paper claim maps to a policy comparison and metric.
5. The design includes a mathematical model skeleton with sets and indices,
   service-bundle definition, menu decision variable, utility model, choice
   probability, expected-profit objective, service guardrail, ETA/time-window
   feasibility, and exact/greedy solver definitions.

**Requirements:** PAPER-01, PAPER-02, PAPER-03, PAPER-04, PAPER-05

## Phase 3: Formal RC Evidence Pipeline Repair And Completion

**Status:** Complete (2026-06-15)

**Gate Result:** Completed comparable formal rows and diagnostic artifacts are
available. Claim-ready manuscript use remains blocked by dirty-git readiness
and generated artifact/claim-guard gates.

**Goal:** Complete the existing RC formal benchmark pipeline and produce
claim-ready formal artifacts if gates pass.

**Success Criteria:**
1. `formal_robust_menu.yaml` and related manifests are inspected.
2. Required shared checkpoint is generated or verified.
3. Formal readiness passes without bypasses.
4. Formal replay executes and writes comparable normalized rows.
5. Claim-ready artifacts and manuscript frame are built from generated rows.

**Requirements:** RC-01, RC-02, RC-03, RC-04, RC-05

**Baseline Commands:**
```powershell
cd work2_coding
python scripts/train_shared_checkpoint.py --study formal_robust_menu --checkpoint-path outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt
python scripts/check_formal_readiness.py --study formal_robust_menu --output-root outputs/phase5_readiness
python scripts/run_study.py --study formal_robust_menu --execute --output-root outputs/formal_v1
python scripts/build_artifacts.py --run-dir <formal-run-dir> --claim-ready --readiness-json outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json
python scripts/build_manuscript_frame.py --artifact-root <formal-artifact-root>
```

## Phase 4: RC Result Diagnosis And Paper-Claim Validation

**Goal:** Determine what formal RC results actually support.

**Success Criteria:**
1. `.planning/results/RC_FORMAL_DIAGNOSIS.md` is written.
2. Diagnosis covers profit, cost, acceptance, served rate, opt-out, home share,
   meeting-point uptake, product ablations, fixed/adaptive windows, seeds, and
   uptake regimes.
3. Effect sizes and paired comparisons are reported.
4. Claim matrix classifies each claim as strong, conditional, weak/diagnostic,
   or unsupported.
5. Mean, standard deviation, paired differences, and confidence intervals are
   reported where feasible.
6. If seed count is small, split-level paired differences are reported and the
   diagnosis avoids strong statistical-significance language.
7. If no central claim is supported, the output includes failure diagnosis and
   reframing guidance before downstream expansion.

**Requirements:** CLAIM-01, CLAIM-02, CLAIM-03, CLAIM-04, CLAIM-05

## Phase 5: Calibration And Robustness Without P-Hacking

**Goal:** If formal RC results are weak or unstable, improve experimental
validity through pre-registered calibration rather than test-set tuning.

**Gate:** Skip this phase only if Phase 4 supports at least one central claim
with stable paired differences. Record the skip as `skipped-by-gate`; otherwise
execute this phase before any final rerun or stronger manuscript claim.

**Phase 4 Gate Result:** Not eligible for `skipped-by-gate` yet. The selected
formal RC run is useful diagnostically, but strong central dominance is not
supported: random menu has better mean net profit, adaptive loses to random on
3/5 paired profit splits, and adaptive ties optimized fixed-window across
tracked metrics. Dirty-git readiness and artifact gates also block final claim
classification. Resolve provenance first; if a strong empirical claim is still
desired, Phase 5 calibration is mandatory before any final rerun or stronger
manuscript claim. Otherwise preserve the conditional service-menu design
framing.

**Success Criteria:**
1. `.planning/results/CALIBRATION_PROTOCOL.md` defines allowed and prohibited
   tuning.
2. Calibration manifests are created if needed.
3. `.planning/results/FROZEN_FINAL_SETTINGS.md` records final settings before
   rerun.
4. Changes are justified by realism and robustness, not ranking improvement
   alone.
5. If skipped, a short gate note records why calibration was not needed.

**Requirements:** CAL-01, CAL-02, CAL-03, CAL-04

## Phase 6: Real Or Semi-Real Case Study Feasibility Audit

**Goal:** Decide whether to add a real or semi-real dataset case for TR Part E.

**Success Criteria:**
1. `.planning/data/CASE_STUDY_FEASIBILITY.md` audits Yanjiao/commuting
   materials, public mobility/network options, and synthetic-over-real-network
   options.
2. Decision is one of: add real case, add semi-real case, or defer case study.
3. The decision includes data source, preprocessing plan, required code changes,
   and paper value.
4. The feasibility report defines the minimum acceptable semi-real case:
   documented real geography, realistic depot/destination and candidate meeting
   points, real road distance or reproducible distance matrix, simulated demand
   labeled as simulated, same seven-tag or reduced six-tag comparison, and no
   use for tuning RC parameters.

**Requirements:** CASE-01, CASE-02, CASE-04

## Phase 7: Case Study Implementation

**Goal:** Implement the selected real/semi-real case reproducibly, if Phase 6
approves it.

**Gate:** If Phase 6 defers the case study, skip Phase 7 and proceed to Phase 8.
The manuscript plan must state that external case validation is deferred.

**Success Criteria:**
1. Data ingestion and validation contracts are written.
2. Case dataset build/validate/run scripts or manifest integration are added.
3. Smoke and pilot case studies produce normalized rows.
4. Formal case artifacts are built, or the case remains explicitly diagnostic.
5. The case is not used to tune RC parameters.

**Requirements:** CASE-03, CASE-05

## Phase 8: Sensitivity And Robustness Experiments

**Goal:** Add sensitivity analyses needed for a credible TR Part E paper.

**Success Criteria:**
1. Sensitivity manifests cover menu size, candidate pool size, ETA uncertainty,
   preference/uptake regime, opt-out guardrail, and fleet/capacity stress where
   feasible.
2. Outputs include normalized rows, aggregate tables, figures, and
   `.planning/results/SENSITIVITY_SUMMARY.md`.
3. Conclusions identify where the method works best and where it fails.
4. Must-have dimensions are `menu_k`, ETA uncertainty/filter mode, uptake
   regime, and opt-out guardrail.
5. Nice-to-have dimensions are candidate pool size, fleet/capacity stress, and
   pricing bounds or price sensitivity.

**Requirements:** SENS-01, SENS-02, SENS-03

## Phase 9: Exact Versus Greedy And Computational Tractability

**Goal:** Show the online menu solver is computationally credible.

**Success Criteria:**
1. Small candidate sets compare exact enumeration and greedy selection.
2. Large candidate sets report greedy runtime and exact infeasibility.
3. Tables/figures report optimality gap, menu overlap, menu build time,
   candidate count, and enumerated menu count.
4. Claims are narrowed if greedy gaps are large.

**Requirements:** COMP-01, COMP-02

## Phase 10: Paper Artifact Generation

**Goal:** Generate paper-facing tables, figures, and manuscript frame.

**Success Criteria:**
1. Tables cover experimental design, main RC results, product ablation,
   time-window/ETA robustness, case study if implemented, sensitivity, and
   computational performance.
2. Figures cover framework, product definition, main results, sensitivity, and
   case-study map/network if implemented.
3. All outputs are generated from rows and artifact builders.
4. `CLAIM_GUARD.json` states claim support.

**Requirements:** ART-01, ART-02

## Phase 11: Manuscript Structure And Writing Plan

**Goal:** Prepare the final TR Part E manuscript structure.

**Success Criteria:**
1. Manuscript plan covers Introduction, Literature Review, Problem Description,
   Model, Solution Method, Experimental Design, Results, Discussion,
   Conclusion, and Appendix.
2. Every claim maps to artifact evidence.
3. Every figure/table has a source artifact.
4. Reviewer-risk section is included.

**Requirements:** MS-01, MS-02

## Phase 12: Final Quality Audit For TR Part E

**Goal:** Audit whether the project is ready to become a high-quality TR Part E
submission.

**Success Criteria:**
1. `.planning/final/TR_E_READINESS_REVIEW.md` audits novelty, modeling rigor,
   algorithmic contribution, experimental credibility, case-study value,
   reproducibility, and claim clarity.
2. Fatal weaknesses are identified before submission.
3. Final deliverables and next-step writing instructions are recorded.

**Requirements:** FINAL-01

---
*Roadmap initialized: 2026-06-14 for TR-E service menu optimization experimental refactoring*
