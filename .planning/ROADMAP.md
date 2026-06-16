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
   Phases 6-8 may continue only as conditional diagnosis and boundary evidence,
   not as a strong-claim upgrade path.
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

**Goal:** Complete the existing RC formal benchmark pipeline diagnostically:
make readiness/checkpoint status explicit, produce comparable formal rows, and
build generated status artifacts while preserving claim-ready blockers.

**Success Criteria:**
1. `formal_robust_menu.yaml` and related manifests are inspected.
2. Required shared checkpoint is generated or verified.
3. Formal readiness status is explicit; claim-ready readiness remains blocked
   without bypasses.
4. Formal replay executes and writes comparable normalized rows.
5. Generated artifact and manuscript-frame status is explicit, with
   claim-ready gates blocked until residual blockers are resolved.

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

**Status:** Complete (2026-06-15)

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

**Status:** Complete (2026-06-15)

**Gate Result:** Completed as a process-integrity lock, not as empirical
evidence. Calibration/final manifests and frozen settings are documented, but
final rerun is `blocked_pending_gate_cleanup` until dirty-git provenance,
checkpoint hash/sidecar, readiness, artifact metadata, and claim guard gates
are resolved.

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

**Status:** Complete (2026-06-15)

**Gate Result:** Add a semi-real case in principle with decision
`approved_blocked_pending_gate_cleanup`. Phase 7 may prepare ingestion,
validation, manifest scaffolding, source-cache checks, and reproducibility
contracts, but may not run case experiments, generate case-study result
artifacts, or upgrade manuscript claims while provenance/readiness/artifact/
claim gates remain blocked.

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

**Status:** Complete (2026-06-15)

**Gate Result:** Completed as scaffold-only case-study contract preparation.
Phase 7 created planning-side contracts and validation checks under
`.planning/data/case_studies/`; it did not create runtime case-study YAML, run
smoke/pilot/formal case replay, generate normalized rows, build case artifacts,
or upgrade manuscript claims.

**Goal:** Implement the selected real/semi-real case reproducibly, if Phase 6
approves it.

**Gate:** If Phase 6 defers the case study, skip Phase 7 and proceed to Phase 8.
The manuscript plan must state that external case validation is deferred.
Phase 6 did not defer. It approved a semi-real route with
`approved_blocked_pending_gate_cleanup`: before gate cleanup, Phase 7 is limited
to scaffolding, validation contracts, source/matrix reproducibility checks, and
manifest preparation. Case-study experiment execution, generated result
artifacts, and manuscript claim upgrades remain blocked until upstream gates
pass.

**Success Criteria:**
1. Data ingestion and validation contracts are written.
2. Planning-side validation scripts and self-tests are added under
   `.planning/data/case_studies/`; no runtime validation script is added under
   `work2_coding/scripts/`.
3. Smoke, pilot, and formal/diagnostic execution remain as blocked contract
   fields only while upstream gates are unresolved; no case normalized rows are
   produced in Phase 7.
4. Formal case artifacts are not built in Phase 7; the case remains
   `scaffolding_only_blocked_execution`.
5. The case is not used to tune RC parameters.

**Requirements:** CASE-03, CASE-05

## Phase 8: Sensitivity And Robustness Experiments

**Status:** Complete (2026-06-15)

**Gate Result:** Baseline validation passed, then the four must-have diagnostic
sensitivity studies executed successfully. Generated artifacts and
`.planning/results/SENSITIVITY_SUMMARY.md` remain
`diagnostic_provisional_blocked` with `claim_ready=false`; no manuscript claim
upgrade is authorized.

**Goal:** Add sensitivity analyses needed for a credible TR Part E paper.

**Success Criteria:**
1. Sensitivity manifests and replay cover the must-have executable dimensions:
   `menu_k`, ETA uncertainty/filter mode, uptake regime, and opt-out/service
   guardrail.
2. Outputs include normalized rows, aggregate tables, figures, and
   `.planning/results/SENSITIVITY_SUMMARY.md`.
3. Conclusions identify where the method works best and where it fails.
4. Nice-to-have dimensions are candidate pool size, fleet/capacity stress, and
   pricing bounds or price sensitivity, and remain deferred rather than
   executed in Phase 8.
5. Summary and artifact metadata keep diagnostic/provisional status and do not
   upgrade abstract or conclusion-level claims.

**Requirements:** SENS-01, SENS-02, SENS-03

## Phase 9: Exact Versus Greedy And Computational Tractability

**Status:** Complete (2026-06-16)

**Gate Result:** Completed as diagnostic/provisional tractability evidence.
The `phase9_exact_greedy_tractability` replay produced 15 completed rows and
generated aggregate/table/figure-status artifacts, but the configured large
scales did not trigger greedy fallback because realized candidate counts stayed
below the exact threshold. Exact-vs-greedy quality, gap/overlap, and
claim-ready computational-credibility statements remain blocked/narrowed.

**Goal:** Show the online menu solver is computationally credible, or narrow
the claim if the exact-vs-greedy evidence is not established.

**Success Criteria:**
1. Small candidate sets report exact enumeration diagnostics.
2. Large configured candidate sets are attempted and explicitly report whether
   greedy fallback/exact infeasibility was exercised.
3. Tables/figures report available candidate count, enumerated menu count, and
   menu build time, plus explicit blocked status for unavailable gap/overlap.
4. Claims are narrowed because exact-vs-greedy quality was not established.

**Requirements:** COMP-01, COMP-02

## Phase 10: Paper Artifact Generation

**Status:** Complete (2026-06-16)

**Gate Result:** Phase 10 generated and verified the paper artifact package
under both
`work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/` and
`artifacts/work2_robust_menu/phase10_paper_artifacts/`. `CLAIM_GUARD.json`
uses schema `phase10-strict-claim-guard-v1`, contains 8 claims, and keeps
overall `claim_ready=false`. `PACKAGE_INDEX.json` contains 74 unique source
artifacts with no duplicate `source_path` values. The package is
paper-facing source and claim-boundary infrastructure; it does not authorize
manuscript claim upgrades.

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

**Status:** Deferred by v1.1 claim-ready resolution milestone (2026-06-16).

**Gate Result:** The old writing-only Phase 11 is intentionally deferred until
the v1.1 claim-ready resolution milestone determines whether the manuscript is
claim-ready empirical, conditional diagnostic, or not ready. Existing Phase 11
planning artifacts are preserved, but no manuscript claim should be upgraded
from them while Phase 10 `CLAIM_GUARD.json` remains overall
`claim_ready=false`.

**Requirements:** Deferred MS-01

## Phase 12: Final Quality Audit For TR Part E

**Status:** Deferred by v1.1 claim-ready resolution milestone (2026-06-16).

**Gate Result:** The old final audit is superseded by Phase 18 below, which
will review the selected claim path and produce the manuscript-path decision.

**Requirements:** Deferred until Phase 18

## v1.1 Milestone: Resolve Claim-Ready Gate Or Lock Diagnostic TR-E Paper

**Milestone Goal:** Determine whether Work2 can honestly become claim-ready for
one or more manuscript claims using current repository evidence and
reproducible experiment gates. If not, formally lock the paper as a conditional
diagnostic TR-E service-menu optimization manuscript.

**Research Decision:** External ecosystem research is skipped for this
milestone. The evidence source is the current repository, generated artifact
packages, readiness outputs, result summaries, source rows, and reproducible
study pipeline.

**Final Outcomes:**

1. `claim_ready=true` for specific authorized claims, backed by readiness,
   completed paired rows, regenerated artifacts, and strict claim guard.
2. `claim_ready=false` with a formal conditional diagnostic manuscript lock.
3. Not ready for manuscript because unresolved blockers remain.

## Phase 13: Evidence Boundary Reconstruction

**Status:** Not started

**Goal:** Reconstruct the exact current evidence boundary before any repair,
rerun, or manuscript writing.

**Success Criteria:**
1. Planning, paper, result, readiness, frozen-setting, and Phase 10 artifact
   files are read and summarized.
2. Exact causes of `claim_ready=false` are identified from source artifacts.
3. Blockers are classified into provenance/readiness, artifact-generation,
   empirical-performance, adaptive-window, random-baseline, sensitivity,
   tractability, semi-real-case, and manuscript-language categories.
4. Deliverables are written under
   `.planning/milestones/claim_ready_resolution/`.

**Deliverables:**
- `.planning/milestones/claim_ready_resolution/01_EVIDENCE_BOUNDARY.md`
- `.planning/milestones/claim_ready_resolution/01_CLAIM_READY_FALSE_CAUSES.md`
- `.planning/milestones/claim_ready_resolution/01_BLOCKER_TAXONOMY.md`

**Requirements:** EVID-01, EVID-02, EVID-03, EVID-04

**Verification:**
```powershell
python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"
```

## Phase 14: Gate Repair Plan Without Result Manipulation

**Status:** Not started

**Goal:** Create a safe plan to repair readiness and artifact gates without
changing empirical results or forcing positive conclusions.

**Success Criteria:**
1. Git status and dirty-git blockers are inspected without destructive cleanup.
2. Readiness blockers are mapped to dirty files, metadata, checkpoint
   sidecar/hash, missing result fields, or artifact schema issues.
3. Artifact failures such as missing `outside_option_util` and invalid or
   missing `method_family` are classified by root cause.
4. Every proposed repair is tied to a gate and labeled as legitimate
   metadata/schema repair, builder repair, true experiment-row issue, evidence
   quality issue, or new experiment path.

**Deliverables:**
- `.planning/milestones/claim_ready_resolution/02_GATE_REPAIR_PLAN.md`
- `.planning/milestones/claim_ready_resolution/02_DIRTY_GIT_ACTIONS_REQUIRED.md`
- `.planning/milestones/claim_ready_resolution/02_ARTIFACT_SCHEMA_REPAIR_PLAN.md`
- `.planning/milestones/claim_ready_resolution/02_CHECKPOINT_PROVENANCE_PLAN.md`

**Requirements:** GATE-01, GATE-02, GATE-03, GATE-04

## Phase 15: Main Result Failure Diagnosis

**Status:** Not started

**Goal:** Diagnose whether the weak central claim is a real scientific result,
a configuration issue, a modeling mismatch, or an implementation bug.

**Success Criteria:**
1. The random-menu profit advantage is explained using source rows and code
   paths.
2. Profit is decomposed into revenue, operating cost, discount/price effect,
   opt-out/lost demand, accepted home service, accepted meeting-point service,
   and service-cost effects where available.
3. Adaptive-window and optimized fixed-window equality is explained by code
   path, generated window values, feasibility filtering, metric availability,
   manifest configuration, or true equivalence.
4. The phase states whether a strong central claim remains scientifically
   plausible.

**Deliverables:**
- `.planning/milestones/claim_ready_resolution/03_RANDOM_BASELINE_DIAGNOSIS.md`
- `.planning/milestones/claim_ready_resolution/03_ADAPTIVE_WINDOW_DIAGNOSIS.md`
- `.planning/milestones/claim_ready_resolution/03_OBJECTIVE_EVALUATION_ALIGNMENT.md`
- `.planning/milestones/claim_ready_resolution/03_RECOVERABILITY_DECISION.md`

**Requirements:** DIAG-01, DIAG-02, DIAG-03, DIAG-04

## Phase 16: Claim-Ready Path Decision

**Status:** Not started

**Goal:** Choose Path A, Path B, or Path C based on Phase 13-15 evidence.

**Success Criteria:**
1. `.planning/results/CALIBRATION_PROTOCOL.md` and
   `.planning/results/FROZEN_FINAL_SETTINGS.md` are read.
2. The phase determines whether frozen settings support a legitimate final
   rerun under calibration/final-test separation.
3. Additional experiments are classified as legitimate robustness evidence or
   prohibited result-chasing.
4. The decision uses the required fields: selected path, reason, allowed
   actions, prohibited actions, claim ceiling, positive central claim status,
   conditional claim status, and diagnostic status.

**Path Options:**
- **Path A:** Gate-only repair and artifact regeneration, only when empirical
  evidence is already sufficient and blockers are repairable provenance or
  artifact metadata issues.
- **Path B:** Pre-registered final rerun, only when evidence is scientifically
  recoverable and frozen final settings are valid without tuning on final
  results.
- **Path C:** Conditional diagnostic lock, when central superiority is not
  recoverable, adaptive-window value is unsupported, a rerun would be
  p-hacking, or claim readiness cannot be honestly upgraded.

**Deliverable:**
- `.planning/milestones/claim_ready_resolution/04_PATH_DECISION.md`

**Requirements:** PATH-01, PATH-02, PATH-03, PATH-04

## Phase 17: Execute Selected Claim Path

**Status:** Not started; conditional on Phase 16

**Goal:** Execute only the selected path and let strict `CLAIM_GUARD.json`
determine whether any manuscript claim can be upgraded.

**Success Criteria:**
1. If Path A is selected, only non-semantic metadata/provenance/artifact
   repairs approved by Phase 16 are applied and artifacts are regenerated.
2. If Path B is selected, only pre-registered frozen final settings are used,
   and completed, failed, timeout, infeasible, blocked, and missing rows are
   all preserved.
3. If Path C is selected, or Path A/B still produce `claim_ready=false`, the
   paper is formally locked as conditional diagnostic.
4. Every claim upgrade is authorized only by strict claim guard output.
5. If the paper remains diagnostic, unsupported central superiority,
   adaptive-window, greedy optimality, online tractability, and case-validation
   claims are explicitly prohibited.

**Conditional Deliverables:**
- Path A:
  - `.planning/milestones/claim_ready_resolution/05A_GATE_REPAIR_REPORT.md`
  - new regenerated artifact package
  - `.planning/milestones/claim_ready_resolution/05A_CLAIM_GUARD_COMPARISON.md`
- Path B:
  - `.planning/milestones/claim_ready_resolution/05B_FINAL_RERUN_PROTOCOL.md`
  - `.planning/milestones/claim_ready_resolution/05B_FINAL_RERUN_REPORT.md`
  - `.planning/milestones/claim_ready_resolution/05B_FINAL_CLAIM_CLASSIFICATION.md`
  - final regenerated artifact package
- Path C:
  - `.planning/milestones/claim_ready_resolution/05C_DIAGNOSTIC_LOCK.md`
  - `.planning/milestones/claim_ready_resolution/05C_SAFE_CLAIM_TABLE.md`
  - `.planning/milestones/claim_ready_resolution/05C_PROHIBITED_LANGUAGE.md`
  - `.planning/milestones/claim_ready_resolution/05C_MANUSCRIPT_POSITIONING.md`

**Requirements:** EXEC-01, EXEC-02, EXEC-03, EXEC-04, EXEC-05, LOCK-01,
LOCK-02, LOCK-03, LOCK-04

## Phase 18: Final Milestone Readiness Review

**Status:** Not started

**Goal:** Produce the final evidence-based answer on whether the paper can move
to manuscript writing.

**Success Criteria:**
1. All v1.1 deliverables are reviewed.
2. Final `CLAIM_GUARD.json` status is reviewed.
3. Allowed and prohibited claims are listed by abstract, introduction, results,
   and conclusion sections.
4. The manuscript path is classified as claim-ready empirical TR-E paper,
   conditional diagnostic TR-E paper, or not ready for manuscript.
5. Required verification commands are run or explicitly documented as
   unavailable/failed.

**Deliverable:**
- `.planning/milestones/claim_ready_resolution/06_FINAL_DECISION.md`

**Verification:**
```powershell
cd work2_coding
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_artifact_gates.py
python scripts/test_paired_replay_contract.py
python scripts/test_policy_fairness_contract.py
python scripts/test_manuscript_claim_guard.py
```

**Requirements:** FINAL-01, FINAL-02, FINAL-03, FINAL-04

---
*Roadmap initialized: 2026-06-14; updated 2026-06-16 after v1.1 claim-ready resolution milestone initialization*
