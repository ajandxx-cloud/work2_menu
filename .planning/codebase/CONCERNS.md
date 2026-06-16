---
last_mapped_commit: 97514c74f4d103ba31191ff047dacde1bac47551
analysis_date: 2026-06-16
focus: concerns
active_runtime_root: work2_coding/
---

# Codebase Concerns

**Analysis Date:** 2026-06-16

**Active runtime root:** `work2_coding/`

**Mapped HEAD:** `97514c74f4d103ba31191ff047dacde1bac47551`

## Tech Debt

**Monolithic robust menu solver:**
- Issue: Robust menu construction, ETA filtering, pricing/product scoring, exact/greedy menu selection, attention diagnostics, and training update behavior are concentrated in `work2_coding/Src/Algorithms/DSPO_Menu.py`.
- Files: `work2_coding/Src/Algorithms/DSPO_Menu.py`, `work2_coding/Src/policy_adapters.py`, `work2_coding/Src/parser.py`
- Impact: Small scientific-policy changes have broad blast radius across service menu behavior, diagnostics, and generated row contracts.
- Fix approach: Keep Phase 11 writing-only. For implementation phases, split only behind existing public row/manifest contracts and preserve tests in `work2_coding/scripts/test_robust_menu_logic.py`, `work2_coding/scripts/test_policy_fairness_contract.py`, and `work2_coding/scripts/test_phase9_exact_greedy_contracts.py`.

**Duplicated claim and artifact gate logic:**
- Issue: Claim readiness and diagnostic/blocker states are enforced in several modules and generated JSON summaries.
- Files: `work2_coding/Src/artifact_status.py`, `work2_coding/Src/paper_artifacts.py`, `work2_coding/Src/manuscript_claims.py`, `work2_coding/Src/sensitivity_analysis.py`, `work2_coding/Src/computational_tractability.py`, `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`, `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`
- Impact: A status rule can drift between runtime validation, artifact packaging, and manuscript claim guarding.
- Fix approach: Treat `work2_coding/Src/manuscript_claims.py` as the manuscript boundary and `work2_coding/Src/artifact_status.py` as the row/artifact boundary. Update both with paired tests whenever a claim boundary changes.

**No configured project-wide test runner or CI gate:**
- Issue: The repo has many script-style tests but no detected `pytest.ini`, `tox.ini`, `noxfile.py`, `pyproject.toml`, `setup.cfg`, or CI workflow tying the checks together.
- Files: `work2_coding/scripts/test_artifact_gates.py`, `work2_coding/scripts/test_optout_accounting.py`, `work2_coding/scripts/test_formal_readiness.py`, `work2_coding/scripts/test_phase8_sensitivity_contracts.py`, `work2_coding/scripts/test_phase9_exact_greedy_contracts.py`, `work2_coding/tests/test_akkerman_rc_no_failure.py`
- Impact: Phase gates depend on manual command selection, so critical regressions can pass if the relevant script is not run.
- Fix approach: Add a canonical local check script or test runner configuration after the current writing-only phase. Include opt-out accounting, paired replay fairness, checkpoint metadata, artifact gates, Phase 8/9 contracts, and manuscript claim guard tests.

**Attention code exists inside the v1 runtime surface:**
- Issue: Attention-related flags, policy tags, and scoring knobs remain available while the research guardrail keeps attention-based choice/scoring outside v1 scope.
- Files: `work2_coding/Src/parser.py`, `work2_coding/Src/Algorithms/DSPO_Menu.py`, `work2_coding/Src/policy_adapters.py`, `work2_coding/Src/manuscript_claims.py`
- Impact: Attention rows can be mistaken for mainline evidence if a future manifest or manuscript section ignores the diagnostic-only boundary.
- Fix approach: Keep `DSPO_attention` and related settings diagnostic-only in `work2_coding/Src/policy_adapters.py` and blocked from manuscript upgrades in `work2_coding/Src/manuscript_claims.py`.

**Legacy numeric approximation remains in utilities:**
- Issue: A route-cost helper records an approximation TODO for an exact calculation.
- Files: `work2_coding/Src/Utils/Utils.py`
- Impact: Distance/cost-derived behavior may carry approximation error into optimization comparisons when that helper is used.
- Fix approach: Localize the exact calculation behind tests before using it for claim-supporting evidence.

## Known Bugs

**Formal claim readiness is blocked by dirty provenance:**
- Symptoms: The readiness command completes but reports blocked status because `git_dirty=true`.
- Files: `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md`, `.planning/STATE.md`, `.planning/STATE_LOCK.md`, `work2_coding/Src/formal_readiness.py`, `work2_coding/Src/study_execution.py`, `work2_coding/outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json`
- Trigger: Formal readiness evaluation against the current dirty working tree.
- Workaround: Keep results diagnostic/status-only until a clean, archived run has matching git metadata, dependency snapshot, manifest hash, and checkpoint hash.

**Main artifact status includes blocked pilot provenance:**
- Symptoms: The active artifact status at `work2_coding/artifacts/work2_robust_menu/ARTIFACT_STATUS.json` is blocked by pilot checkpoint failure, placeholder-only status, and skipped formal evidence.
- Files: `work2_coding/artifacts/work2_robust_menu/ARTIFACT_STATUS.json`, `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md`, `work2_coding/Src/artifact_status.py`
- Trigger: Artifact packaging that indexes the blocked pilot source instead of a fully claim-ready formal source.
- Workaround: Use Phase 10 package status as a blocker index only. Do not upgrade manuscript claims from this artifact set.

**Phase 9 exact-vs-greedy run does not exercise greedy fallback:**
- Symptoms: The tractability summary has completed rows but `relative_optimality_gap` and overlap are unavailable because realized candidate counts do not exceed the exact threshold.
- Files: `.planning/results/COMPUTATIONAL_TRACTABILITY_SUMMARY.md`, `work2_coding/artifacts/work2_robust_menu/phase9_tractability/ARTIFACT_STATUS.json`, `work2_coding/Experiments/studies/phase9_exact_greedy_tractability.yaml`, `work2_coding/Src/computational_tractability.py`, `work2_coding/Src/Algorithms/DSPO_Menu.py`
- Trigger: Configured large scales do not guarantee realized candidate counts above `menu_exact_threshold`.
- Workaround: Treat Phase 9 as diagnostic and blocked for computational credibility claims.

**Adaptive-window increment is unsupported by current formal diagnostics:**
- Symptoms: The adaptive policy matches optimized fixed-window on tracked metrics in the formal diagnostic summary.
- Files: `.planning/results/RC_FORMAL_DIAGNOSIS.md`, `work2_coding/Experiments/studies/formal_robust_menu.yaml`, `work2_coding/Src/policy_adapters.py`
- Trigger: Formal diagnostic comparisons across paired replay splits.
- Workaround: Manuscript language must not claim an adaptive-window increment.

**Central superiority claim is unsupported by current formal diagnostics:**
- Symptoms: Random menu has higher mean net profit than adaptive in the formal diagnostic summary, and adaptive loses to random on net profit in most paired splits.
- Files: `.planning/results/RC_FORMAL_DIAGNOSIS.md`, `work2_coding/Experiments/studies/formal_robust_menu.yaml`, `work2_coding/Src/manuscript_claims.py`
- Trigger: Phase 5 formal diagnostic source run summarized in `.planning/results/RC_FORMAL_DIAGNOSIS.md`.
- Workaround: Keep central claims blocked or rewrite them as limited diagnostic observations with the current claim guard.

## Security Considerations

**No runtime secrets are detected in the active project surface:**
- Risk: Adding API keys or private data files would create a publication and repository leak risk.
- Files: `.gitignore`, `AGENTS.md`, `work2_coding/README.md`
- Current mitigation: No `.env` files are detected in the repo scan, and current integrations are local filesystem, git, Python packages, HGS routing, and LaTeX/artifact generation.
- Recommendations: Keep credentials out of the repo and do not read or quote secret-like files in future mapping or phase work.

**Checkpoint loading is intentionally fail-closed for formal evidence:**
- Risk: Loading arbitrary PyTorch checkpoints can be unsafe or scientifically invalid if source, hash, or architecture compatibility is unclear.
- Files: `work2_coding/Src/Algorithms/Agent.py`, `work2_coding/Src/Utils/Utils.py`, `work2_coding/Src/formal_readiness.py`, `work2_coding/Src/study_execution.py`
- Current mitigation: Checkpoint metadata includes load status and hashes, and formal/pilot paths reject missing or incompatible required checkpoints.
- Recommendations: Use only local, expected checkpoints with recorded SHA-256 hashes and sidecar metadata for claim-supporting runs.

**Case-study data boundaries remain unresolved:**
- Risk: Semi-real case study materials can be over-claimed as real passenger behavior, real acceptance, or real opt-out evidence.
- Files: `.planning/data/CASE_STUDY_FEASIBILITY.md`, `.planning/data/case_studies/VALIDATION_SUMMARY.md`, `work2_coding/Src/case_study_validation.py`
- Current mitigation: Case study status is scaffold-only and execution is blocked.
- Recommendations: Keep all Yanjiao/OSM/GTFS case material as scaffold or context until source licensing, cache contracts, generated matrices, and runtime manifests are approved.

## Performance Bottlenecks

**Exact menu enumeration is combinatorial:**
- Problem: Exact menu selection scales poorly with candidate count and menu size.
- Files: `work2_coding/Src/Algorithms/DSPO_Menu.py`, `work2_coding/Src/computational_tractability.py`, `work2_coding/Experiments/studies/phase9_exact_greedy_tractability.yaml`
- Cause: Exact search enumerates candidate menu combinations, while the Phase 9 evidence run does not currently force candidate counts high enough to validate greedy fallback.
- Improvement path: Add a tractability scenario that guarantees realized candidate counts above `menu_exact_threshold`, records fallback reason, and validates exact-vs-greedy metrics before any computational claim.

**HGS routing and paired replay multiply runtime cost:**
- Problem: Formal studies run multiple policies across paired splits and route evaluations.
- Files: `work2_coding/Environments/OOH/Parcelpoint_py.py`, `work2_coding/Src/paired_replay.py`, `work2_coding/Src/study_execution.py`, `work2_coding/Experiments/studies/formal_robust_menu.yaml`
- Cause: Fair policy comparison requires shared seeds, paired replay groups, checkpoint metadata, and per-policy execution over the same scenario structure.
- Improvement path: Keep paired replay fairness intact and optimize only with measured profiling around route-cost calls and candidate generation.

**Artifact packaging carries a large blocker surface:**
- Problem: Phase 10 package status indexes 74 artifacts and 108 blockers.
- Files: `work2_coding/Src/paper_artifacts.py`, `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`, `artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`
- Cause: Diagnostic, scaffold, main RC, sensitivity, and tractability outputs are all packaged with explicit blocker metadata.
- Improvement path: Keep package status as a generated index and avoid manual edits; regenerate after gate cleanup rather than patching rows.

## Reproducibility Risks

**Current working tree is dirty:**
- Issue: The planning state and blocker diagnosis record dirty runtime, planning, and manuscript changes.
- Files: `.planning/STATE.md`, `.planning/STATE_LOCK.md`, `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md`, `work2_coding/Src/study_execution.py`
- Impact: Formal evidence cannot be treated as claim-ready because rows and reports cannot be tied to a clean source revision.
- Fix approach: Finish or isolate the current phase, then regenerate readiness and artifact packages from a clean tree before changing claim status.

**Generated artifacts exist in mirrored locations:**
- Issue: Work2 artifacts appear under both `work2_coding/artifacts/` and root `artifacts/`.
- Files: `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`, `artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`, `work2_coding/Src/paper_artifacts.py`
- Impact: A manuscript or planner can cite a stale mirror if the package index and root mirror drift.
- Fix approach: Treat `PACKAGE_STATUS.json` as the source index and cite exact source artifact paths from it.

**Dependency state is not locked for replay:**
- Issue: Runtime requirements are listed, but no lockfile or CI-pinned environment is detected.
- Files: `work2_coding/requirements.txt`, `work2_coding/outputs/phase5_readiness/formal_robust_menu/dependency_snapshot.json`, `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md`
- Impact: Python, NumPy, PyTorch, HGS, or YAML version drift can change checkpoint compatibility, solver behavior, or artifact generation.
- Fix approach: Keep dependency snapshots with every formal run and add a reproducible environment lock before final claim-ready reruns.

**Output rows are generated evidence and must remain immutable:**
- Issue: Research guardrails prohibit hand-editing generated result rows or paper artifacts.
- Files: `work2_coding/outputs/`, `work2_coding/artifacts/`, `artifacts/`, `work2_coding/Src/artifact_builder.py`, `work2_coding/Src/paper_artifacts.py`
- Impact: Manual row edits invalidate provenance and can bypass artifact gates.
- Fix approach: Fix code or manifests, rerun generation scripts, and let `work2_coding/Src/artifact_status.py` classify the outputs.

## Fragile Areas

**Paired replay fairness contract:**
- Files: `work2_coding/Src/paired_replay.py`, `work2_coding/Src/study_execution.py`, `work2_coding/Src/policy_adapters.py`, `work2_coding/Experiments/studies/formal_robust_menu.yaml`, `work2_coding/scripts/test_paired_replay_contract.py`, `work2_coding/scripts/test_policy_fairness_contract.py`
- Why fragile: Policy comparisons rely on shared replay groups, seeds, trace IDs, manifest hashes, and comparable policy tags.
- Safe modification: Any change to policy tags, manifest paired fields, or row identity fields needs paired replay and policy fairness tests.
- Test coverage: Script-style coverage exists, but there is no central runner enforcing it.

**Opt-out accounting must stay separate from accepted home pickup:**
- Files: `work2_coding/Environments/OOH/customerchoice.py`, `work2_coding/Environments/OOH/Parcelpoint_py.py`, `work2_coding/Environments/OOH/containers.py`, `work2_coding/Src/paired_replay.py`, `work2_coding/Src/artifact_status.py`, `work2_coding/scripts/test_optout_accounting.py`
- Why fragile: Opt-out, accepted home, and accepted meeting-point outcomes all feed service metrics and artifact validation.
- Safe modification: Preserve `count_opted_out`, `count_accepted_home`, and `count_accepted_meeting_point` as separate row fields and validation inputs.
- Test coverage: Dedicated opt-out accounting tests exist; include them in any gate that touches choice behavior or row normalization.

**Checkpoint load status is a formal evidence boundary:**
- Files: `work2_coding/Src/Algorithms/Agent.py`, `work2_coding/Src/Utils/Utils.py`, `work2_coding/Src/formal_readiness.py`, `work2_coding/Src/study_execution.py`, `work2_coding/scripts/test_checkpoint_provenance.py`, `work2_coding/scripts/test_formal_readiness.py`
- Why fragile: Claim readiness depends on explicit `loaded` status, checkpoint hash, sidecar metadata, and dependency snapshot matching.
- Safe modification: Preserve fail-closed behavior for formal/pilot checkpoints and keep load status in generated rows and readiness reports.
- Test coverage: Checkpoint provenance tests exist, but final claim-ready reruns need end-to-end readiness and artifact validation.

**No-filter policy is diagnostic-only:**
- Files: `work2_coding/Src/policy_adapters.py`, `work2_coding/Src/sensitivity_analysis.py`, `work2_coding/Src/manuscript_claims.py`, `.planning/results/SENSITIVITY_SUMMARY.md`
- Why fragile: `no_filter_diagnostic` is useful for diagnosis but cannot support operational ETA-filter claims.
- Safe modification: Keep `menu_eta_filter_mode: none` out of mainline policy evidence and manuscript upgrades.
- Test coverage: Phase 8 sensitivity contract tests exist in `work2_coding/scripts/test_phase8_sensitivity_contracts.py`.

**Case study remains scaffold-only:**
- Files: `.planning/data/CASE_STUDY_FEASIBILITY.md`, `.planning/data/case_studies/VALIDATION_SUMMARY.md`, `work2_coding/Src/case_study_validation.py`
- Why fragile: The case study has documentation scaffolding without approved execution, runtime manifest, matrices, or replay outputs.
- Safe modification: Do not generate or cite case result artifacts until the case gates explicitly allow execution.
- Test coverage: Validation is document/scaffold oriented; runtime case execution tests are not active evidence.

**Manuscript edits are claim-boundary sensitive:**
- Files: `manuscript/main.tex`, `manuscript/references.bib`, `paper/`, `work2_coding/Src/manuscript_claims.py`, `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`
- Why fragile: The current state marks Phase 11 as writing-only with `claim_ready=false`; manuscript language must not imply claim-ready empirical support.
- Safe modification: Use `CLAIM_GUARD.json`, `.planning/results/RC_FORMAL_DIAGNOSIS.md`, `.planning/results/SENSITIVITY_SUMMARY.md`, and `.planning/results/COMPUTATIONAL_TRACTABILITY_SUMMARY.md` as boundaries.
- Test coverage: Claim guard tests exist in `work2_coding/scripts/test_manuscript_claim_guard.py`.

## Scaling Limits

**Formal replay scale is bounded by paired split and policy count:**
- Current capacity: The formal diagnostic summary uses 5 paired splits and 7 policy tags.
- Files: `.planning/results/RC_FORMAL_DIAGNOSIS.md`, `work2_coding/Experiments/studies/formal_robust_menu.yaml`, `work2_coding/Src/study_execution.py`
- Limit: Increasing splits, episodes, policies, or candidate count multiplies route and menu-selection work.
- Scaling path: Profile first, preserve paired replay fields, and scale one axis at a time with artifact status validation.

**Exact-vs-greedy evidence depends on realized candidate counts:**
- Current capacity: Phase 9 rows complete but do not cross the effective greedy fallback condition.
- Files: `.planning/results/COMPUTATIONAL_TRACTABILITY_SUMMARY.md`, `work2_coding/Experiments/studies/phase9_exact_greedy_tractability.yaml`, `work2_coding/Src/Algorithms/DSPO_Menu.py`
- Limit: Configured `max_candidates` alone does not prove the candidate pool exceeds `menu_exact_threshold`.
- Scaling path: Add a deterministic stress setup or fixture that guarantees enough feasible candidates for greedy fallback.

## Dependencies at Risk

**HGS routing dependency:**
- Risk: Route-cost behavior and installation compatibility depend on the local HGS/Hygese stack.
- Impact: Replay results, menu feasibility, and service metrics can shift if route evaluation changes.
- Files: `work2_coding/requirements.txt`, `work2_coding/Environments/OOH/Parcelpoint_py.py`, `work2_coding/Src/Utils/Utils.py`
- Migration plan: Capture route dependency versions in dependency snapshots and add a route-cost smoke test to the canonical gate.

**PyTorch checkpoint compatibility:**
- Risk: Model checkpoints can fail to load or silently mismatch if PyTorch defaults, architecture keys, or checkpoint schema changes.
- Impact: Pilot/formal rows become blocked or invalid for claims.
- Files: `work2_coding/requirements.txt`, `work2_coding/Src/Algorithms/Agent.py`, `work2_coding/Src/Utils/Utils.py`, `work2_coding/Src/formal_readiness.py`
- Migration plan: Keep sidecar metadata and hashes mandatory for formal evidence and rerun readiness after dependency changes.

**LaTeX/manuscript toolchain:**
- Risk: Manuscript artifacts and references can fail independently of Python evidence generation.
- Impact: Phase 11 writing output can diverge from claim guard and artifact status.
- Files: `manuscript/main.tex`, `manuscript/references.bib`, `paper/`, `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/MANUSCRIPT_INSERTS.md`
- Migration plan: Add a manuscript build/check command only after claim-safe wording is settled.

## Missing Critical Features

**Clean formal provenance gate:**
- Problem: Claim-ready formal evidence requires a clean git state and matching readiness/artifact metadata.
- Blocks: Empirical effectiveness claims, final RC claims, and final manuscript upgrades.
- Files: `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md`, `.planning/STATE.md`, `.planning/STATE_LOCK.md`, `work2_coding/Src/formal_readiness.py`, `work2_coding/Src/artifact_status.py`

**Claim-ready final run execution:**
- Problem: `final_robust_menu.yaml` defines a final candidate path, but current planning state keeps Phase 11 writing-only and final claims blocked.
- Blocks: Final claim-ready replay and paper claims based on final settings.
- Files: `work2_coding/Experiments/studies/final_robust_menu.yaml`, `.planning/results/FROZEN_FINAL_SETTINGS.md`, `.planning/results/CALIBRATION_PROTOCOL.md`, `.planning/STATE.md`

**Semi-real case execution artifacts:**
- Problem: Case study validation permits scaffold only and records no runtime manifest, matrices, demand rows, replay outputs, or case results.
- Blocks: Semi-real case validation claims and any real passenger behavior claims.
- Files: `.planning/data/CASE_STUDY_FEASIBILITY.md`, `.planning/data/case_studies/VALIDATION_SUMMARY.md`, `work2_coding/Src/case_study_validation.py`

**Canonical run-all verification command:**
- Problem: Tests are present but not unified under a configured runner or CI workflow.
- Blocks: Reliable regression gates across opt-out accounting, paired replay, artifact status, readiness, sensitivity, tractability, and manuscript claims.
- Files: `work2_coding/scripts/`, `work2_coding/tests/test_akkerman_rc_no_failure.py`

## Stale Docs and Path Risks

**Previous codebase maps reference stale `ooh_code/` paths:**
- Issue: Existing map documents in `.planning/codebase/` predate the active runtime lock and include stale `ooh_code/` references.
- Files: `.planning/codebase/ARCHITECTURE.md`, `.planning/codebase/STRUCTURE.md`, `.planning/codebase/STACK.md`, `.planning/codebase/INTEGRATIONS.md`, `.planning/codebase/TESTING.md`, `.planning/codebase/CONVENTIONS.md`, `.planning/STATE_LOCK.md`, `AGENTS.md`
- Impact: Future planning agents can navigate to obsolete paths or revive incorrect missing-file concerns.
- Fix approach: Prefer `work2_coding/` paths and verify any `ooh_code/` reference against the current filesystem before use.

**Current concern map supersedes obsolete missing-menu concern:**
- Issue: The active runtime root contains `work2_coding/Src/Algorithms/DSPO_Menu.py`, so any concern that the menu algorithm file is missing under `ooh_code/` is stale for the active root.
- Files: `work2_coding/Src/Algorithms/DSPO_Menu.py`, `.planning/STATE_LOCK.md`, `AGENTS.md`
- Impact: Treating the stale concern as current can misdirect Phase 11 or follow-up work.
- Fix approach: Use the active import smoke and `work2_coding/` file paths for runtime analysis.

## Claim Boundary Risks

**Most empirical claim IDs remain blocked:**
- Issue: Phase 10 claim guard blocks central adaptive superiority, product ablation, adaptive window increment, menu construction value, exact-greedy computational credibility, and semi-real case validation.
- Files: `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`, `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`, `work2_coding/Src/manuscript_claims.py`
- Impact: Manuscript text can only state diagnostic/status-limited findings unless a future clean run changes the guard.
- Fix approach: Keep `claim_ready=false` language and cite blockers explicitly.

**Provenance/status transparency is the only supported strict claim class:**
- Issue: The claim guard allows status transparency but not empirical effectiveness upgrades.
- Files: `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`, `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md`, `work2_coding/Src/manuscript_claims.py`
- Impact: The paper can describe auditability, checkpoint metadata, and blocker states, but not superiority claims.
- Fix approach: Phrase Phase 11 output around transparent diagnostic evidence and blocked claim boundaries.

**No-filter can only support diagnostic interpretation:**
- Issue: No-filter rows are explicitly diagnostic and cannot support operational recommendations.
- Files: `work2_coding/Src/policy_adapters.py`, `work2_coding/Src/sensitivity_analysis.py`, `work2_coding/Src/manuscript_claims.py`, `.planning/results/SENSITIVITY_SUMMARY.md`
- Impact: Any no-filter claim beyond diagnostic sensitivity violates the research guardrail.
- Fix approach: Keep no-filter in appendix/status language only.

**Attention-based choice/scoring is outside v1 scope:**
- Issue: Attention implementation hooks exist, but v1 guardrails exclude attention-based choice/scoring from claim scope.
- Files: `work2_coding/Src/parser.py`, `work2_coding/Src/Algorithms/DSPO_Menu.py`, `work2_coding/Src/policy_adapters.py`, `work2_coding/Src/manuscript_claims.py`
- Impact: Including attention results in v1 would create a scope and evidence mismatch.
- Fix approach: Keep attention policy tags diagnostic-only and outside v1 manuscript claims.

## Test Coverage Gaps

**End-to-end greedy fallback coverage is missing for actual generated evidence:**
- What's not tested: A full Phase 9 run that guarantees realized candidate counts above the exact threshold and validates greedy fallback metrics.
- Files: `work2_coding/scripts/test_phase9_exact_greedy_contracts.py`, `.planning/results/COMPUTATIONAL_TRACTABILITY_SUMMARY.md`, `work2_coding/Experiments/studies/phase9_exact_greedy_tractability.yaml`
- Risk: Synthetic or contract tests can pass while generated evidence remains invalid for computational claims.
- Priority: High

**Formal artifact rebuild coverage is incomplete:**
- What's not tested: Full path from clean readiness pass to regenerated artifact package with loaded checkpoint, dependency snapshot, method metadata, outside option utility, and valid claim guard.
- Files: `work2_coding/scripts/test_formal_readiness.py`, `work2_coding/scripts/test_artifact_gates.py`, `work2_coding/Src/formal_readiness.py`, `work2_coding/Src/artifact_status.py`, `work2_coding/Src/paper_artifacts.py`
- Risk: Individual contracts pass but the final paper package remains blocked.
- Priority: High

**Case-study execution tests are not active evidence:**
- What's not tested: Runtime generation of case matrices, demand rows, paired replay outputs, and case artifact status.
- Files: `.planning/data/case_studies/VALIDATION_SUMMARY.md`, `work2_coding/Src/case_study_validation.py`
- Risk: Case-study manuscript language can exceed scaffold evidence.
- Priority: Medium

**Root/work2 artifact mirror drift is not centrally enforced:**
- What's not tested: Consistency between root `artifacts/` mirrors and `work2_coding/artifacts/` source packages.
- Files: `artifacts/`, `work2_coding/artifacts/`, `work2_coding/Src/paper_artifacts.py`
- Risk: A stale mirrored artifact can be cited after regeneration under the runtime root.
- Priority: Medium

---

*Concerns audit: 2026-06-16*
