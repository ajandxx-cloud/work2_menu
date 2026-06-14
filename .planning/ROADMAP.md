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

## Phase 1: Repository Audit And State Locking

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

**Requirements:** PAPER-01, PAPER-02, PAPER-03, PAPER-04

## Phase 3: Formal RC Evidence Pipeline Repair And Completion

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

**Requirements:** CLAIM-01, CLAIM-02, CLAIM-03

## Phase 5: Calibration And Robustness Without P-Hacking

**Goal:** If formal RC results are weak or unstable, improve experimental
validity through pre-registered calibration rather than test-set tuning.

**Success Criteria:**
1. `.planning/results/CALIBRATION_PROTOCOL.md` defines allowed and prohibited
   tuning.
2. Calibration manifests are created if needed.
3. `.planning/results/FROZEN_FINAL_SETTINGS.md` records final settings before
   rerun.
4. Changes are justified by realism and robustness, not ranking improvement
   alone.

**Requirements:** CAL-01, CAL-02, CAL-03

## Phase 6: Real Or Semi-Real Case Study Feasibility Audit

**Goal:** Decide whether to add a real or semi-real dataset case for TR Part E.

**Success Criteria:**
1. `.planning/data/CASE_STUDY_FEASIBILITY.md` audits Yanjiao/commuting
   materials, public mobility/network options, and synthetic-over-real-network
   options.
2. Decision is one of: add real case, add semi-real case, or defer case study.
3. The decision includes data source, preprocessing plan, required code changes,
   and paper value.

**Requirements:** CASE-01, CASE-02

## Phase 7: Case Study Implementation

**Goal:** Implement the selected real/semi-real case reproducibly, if Phase 6
approves it.

**Success Criteria:**
1. Data ingestion and validation contracts are written.
2. Case dataset build/validate/run scripts or manifest integration are added.
3. Smoke and pilot case studies produce normalized rows.
4. Formal case artifacts are built, or the case remains explicitly diagnostic.

**Requirements:** CASE-03

## Phase 8: Sensitivity And Robustness Experiments

**Goal:** Add sensitivity analyses needed for a credible TR Part E paper.

**Success Criteria:**
1. Sensitivity manifests cover menu size, candidate pool size, ETA uncertainty,
   preference/uptake regime, opt-out guardrail, and fleet/capacity stress where
   feasible.
2. Outputs include normalized rows, aggregate tables, figures, and
   `.planning/results/SENSITIVITY_SUMMARY.md`.
3. Conclusions identify where the method works best and where it fails.

**Requirements:** SENS-01, SENS-02

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
