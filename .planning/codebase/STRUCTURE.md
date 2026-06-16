<!-- refreshed: 2026-06-16 -->
<!-- last_mapped_commit: 97514c7 -->
# Codebase Structure

**Analysis Date:** 2026-06-16

## Directory Layout

```text
[project-root]/
+-- AGENTS.md                         # Repository instructions and active runtime guardrails
+-- .planning/                        # GSD planning state, research context, phase artifacts
|   +-- PROJECT.md                     # Project state and current milestone context
|   +-- REQUIREMENTS.md                # Work2 v1 requirements and out-of-scope boundaries
|   +-- ROADMAP.md                     # Phase sequence and completion status
|   +-- STATE.md                       # Current workflow state and next phase
|   +-- codebase/                      # Codebase maps consumed by GSD planners/executors
|   +-- data/case_studies/             # Phase 10 case-study scaffold inputs
|   +-- paper/                         # Manuscript design, claim maps, table/figure maps
|   +-- research/                      # Research synthesis and framing notes
|   +-- results/                       # Generated or curated phase summaries
|   +-- phases/                        # Phase plans, UAT, review, and execution artifacts
|   +-- final/                         # Final GSD milestone material
|   +-- decisions/                     # Decision records when present
|   +-- learnings/                     # Extracted lessons when present
|   +-- threads/                       # Persistent GSD thread context when present
|   +-- validation/                    # Validation artifacts when present
|   +-- verification/                  # Verification artifacts when present
|   +-- graphs/                        # Knowledge graph artifacts when present
+-- work2_coding/                      # Active runtime root
|   +-- Src/                           # Python source for execution, contracts, gates, builders
|   |   +-- Algorithms/                # DSPO, DSPO_Menu, PPO, heuristic, agent code
|   |   +-- Utils/                     # Logger, checkpoint, predictor, math, feature utilities
|   +-- Environments/                  # DRT simulation environments and input data
|   |   +-- OOH/                       # Many-to-one OOH parcel-point environment
|   +-- Experiments/                   # Executable YAML studies, suites, and legacy run configs
|   |   +-- studies/                   # Study manifests
|   |   +-- suites/                    # Suite manifests
|   +-- scripts/                       # CLI wrappers and script-style contract tests
|   +-- tests/                         # Pytest-style tests retained from runtime
|   +-- outputs/                       # Generated study runs and checkpoint outputs
|   +-- artifacts/                     # Generated runtime artifact packages
|   +-- Environments/OOH/Amazon_data/  # OOH input data
|   +-- Environments/OOH/HombergerGehring_data/ # HGS/CVRP input data
|   +-- requirements.txt               # Python dependency list
|   +-- run.py                         # Legacy original runtime entry point
|   +-- run_ppo.py                     # Legacy PPO runtime entry point
+-- artifacts/                         # Root-level mirrored paper-facing artifact packages
+-- manuscript/                        # Paper/manuscript material
+-- paper/                             # Paper material outside .planning when present
```

## Directory Purposes

**`.planning/`:**
- Purpose: GSD-managed planning, research state, phase status, and paper claim boundaries.
- Contains: `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, `.planning/STATE.md`, `.planning/research/SUMMARY.md`, `.planning/paper/*.md`, `.planning/results/*.md`
- Key files: `.planning/paper/TR_E_RESEARCH_DESIGN.md`, `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md`, `.planning/paper/TR_E_MANUSCRIPT_STRUCTURE.md`

**`.planning/codebase/`:**
- Purpose: Generated codebase maps consumed by GSD planning and execution commands.
- Contains: `.planning/codebase/ARCHITECTURE.md`, `.planning/codebase/STRUCTURE.md`, `.planning/codebase/STACK.md`, `.planning/codebase/INTEGRATIONS.md`, `.planning/codebase/CONVENTIONS.md`, `.planning/codebase/TESTING.md`, `.planning/codebase/CONCERNS.md`
- Key files: `.planning/codebase/ARCHITECTURE.md`, `.planning/codebase/STRUCTURE.md`

**`.planning/paper/`:**
- Purpose: Paper design, manuscript structure, claim mapping, and table/figure evidence rules.
- Contains: Research design docs and claim maps that must align with generated claim guards.
- Key files: `.planning/paper/TR_E_RESEARCH_DESIGN.md`, `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md`, `.planning/paper/TR_E_MANUSCRIPT_STRUCTURE.md`

**`.planning/results/`:**
- Purpose: Phase summary outputs and evidence-status summaries.
- Contains: `SENSITIVITY_SUMMARY.md`, `COMPUTATIONAL_TRACTABILITY_SUMMARY.md`, and related generated or reviewed result summaries.
- Key files: `.planning/results/SENSITIVITY_SUMMARY.md`, `.planning/results/COMPUTATIONAL_TRACTABILITY_SUMMARY.md`

**`.planning/data/case_studies/`:**
- Purpose: Case-study scaffold sources indexed by Phase 10 paper packages.
- Contains: Scaffold JSON/Markdown inputs for source-family evidence.
- Key files: `.planning/data/case_studies/` entries referenced by `work2_coding/Src/paper_artifacts.py`

**`work2_coding/`:**
- Purpose: Active runtime root for Work2 service-menu research code.
- Contains: `work2_coding/Src/`, `work2_coding/Environments/`, `work2_coding/Experiments/`, `work2_coding/scripts/`, `work2_coding/outputs/`, `work2_coding/artifacts/`
- Key files: `work2_coding/requirements.txt`, `work2_coding/run.py`, `work2_coding/run_ppo.py`

**`work2_coding/Src/`:**
- Purpose: Core orchestration, contracts, algorithm adapters, artifact builders, and phase gates.
- Contains: Python modules for manifest validation, paired replay, execution, artifact status, paper packages, and phase-specific diagnostics.
- Key files: `work2_coding/Src/experiment_contracts.py`, `work2_coding/Src/policy_adapters.py`, `work2_coding/Src/paired_replay.py`, `work2_coding/Src/study_execution.py`, `work2_coding/Src/artifact_status.py`

**`work2_coding/Src/Algorithms/`:**
- Purpose: Algorithm implementations and checkpoint-loading base agent logic.
- Contains: DSPO, DSPO menu, PPO, heuristic, and baseline implementations.
- Key files: `work2_coding/Src/Algorithms/DSPO_Menu.py`, `work2_coding/Src/Algorithms/Agent.py`, `work2_coding/Src/Algorithms/DSPO.py`, `work2_coding/Src/Algorithms/Baseline.py`

**`work2_coding/Src/Utils/`:**
- Purpose: Runtime utilities for logging, dynamic imports, checkpoint metadata, predictors, math helpers, and option features.
- Contains: Utility modules shared by config, algorithms, and execution.
- Key files: `work2_coding/Src/Utils/Utils.py`, `work2_coding/Src/Utils/option_features.py`, `work2_coding/Src/Utils/Predictors.py`

**`work2_coding/Environments/OOH/`:**
- Purpose: Out-of-home parcel-point DRT simulator, domain containers, customer choice, and environment data utilities.
- Contains: Environment class, MNL choice functions, service-menu domain objects, and input data folders.
- Key files: `work2_coding/Environments/OOH/Parcelpoint_py.py`, `work2_coding/Environments/OOH/customerchoice.py`, `work2_coding/Environments/OOH/containers.py`, `work2_coding/Environments/OOH/env_utils.py`

**`work2_coding/Experiments/`:**
- Purpose: Executable experiment contracts and legacy experiment outputs/configs.
- Contains: Study manifests, suite manifests, and original run folders under `work2_coding/Experiments/Parcelpoint_py/`.
- Key files: `work2_coding/Experiments/studies/formal_robust_menu.yaml`, `work2_coding/Experiments/studies/pilot_robust_menu.yaml`, `work2_coding/Experiments/studies/smoke_robust_menu.yaml`

**`work2_coding/Experiments/studies/`:**
- Purpose: Single-study YAML contracts for smoke, pilot, formal, sensitivity, tractability, and validation runs.
- Contains: Manifest files consumed by `work2_coding/Src/experiment_contracts.py`.
- Key files: `work2_coding/Experiments/studies/formal_robust_menu.yaml`, `work2_coding/Experiments/studies/phase8_sensitivity_eta_filter.yaml`, `work2_coding/Experiments/studies/phase9_exact_greedy_tractability.yaml`

**`work2_coding/Experiments/suites/`:**
- Purpose: Multi-study YAML contracts for grouped phase execution.
- Contains: Suite files consumed by `work2_coding/scripts/run_study.py`.
- Key files: `work2_coding/Experiments/suites/phase8_sensitivity_must_have.yaml`, `work2_coding/Experiments/suites/phase9_exact_greedy_tractability.yaml`

**`work2_coding/scripts/`:**
- Purpose: Script-style CLIs and test harnesses.
- Contains: Study runners, artifact builders, readiness checks, checkpoint trainers, diagnostics, and `test_*.py` scripts.
- Key files: `work2_coding/scripts/run_study.py`, `work2_coding/scripts/build_artifacts.py`, `work2_coding/scripts/check_formal_readiness.py`, `work2_coding/scripts/build_phase10_paper_artifacts.py`

**`work2_coding/outputs/`:**
- Purpose: Generated study run outputs and shared training outputs.
- Contains: `work2_coding/outputs/studies/` run directories and checkpoint outputs under `work2_coding/outputs/shared_training/`.
- Key files: `work2_coding/outputs/studies/*/*/normalized_rows.json`, `work2_coding/outputs/studies/*/*/study_summary.json`, `work2_coding/outputs/studies/*/*/blockers.json`

**`work2_coding/artifacts/`:**
- Purpose: Generated runtime artifact packages.
- Contains: Work2 robust menu packages, attention diagnostics, actual smoke outputs, phase outputs, and paper package outputs.
- Key files: `work2_coding/artifacts/work2_robust_menu/ARTIFACT_STATUS.json`, `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`, `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`

**`artifacts/`:**
- Purpose: Root-level mirror of paper-facing artifact packages.
- Contains: Mirrored `artifacts/work2_robust_menu/` package files generated from `work2_coding/Src/artifact_builder.py` and `work2_coding/Src/paper_artifacts.py`.
- Key files: `artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`, `artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`

**`manuscript/` and `paper/`:**
- Purpose: Paper-facing material outside `.planning/`.
- Contains: Manuscript artifacts or paper assets when present.
- Key files: `manuscript/`, `paper/`

## Key File Locations

**Entry Points:**
- `work2_coding/scripts/run_study.py`: Primary study and suite runner.
- `work2_coding/scripts/train_shared_checkpoint.py`: Shared checkpoint training for pilot/formal manifests.
- `work2_coding/scripts/check_formal_readiness.py`: Formal readiness preflight.
- `work2_coding/scripts/build_artifacts.py`: Main robust-menu artifact builder.
- `work2_coding/scripts/build_phase10_paper_artifacts.py`: Phase 10 paper package builder.
- `work2_coding/scripts/build_manuscript_frame.py`: Manuscript frame builder.
- `work2_coding/scripts/build_phase8_sensitivity_artifacts.py`: Phase 8 sensitivity artifact builder.
- `work2_coding/scripts/build_phase9_tractability_artifacts.py`: Phase 9 tractability artifact builder.
- `work2_coding/run.py`: Legacy original runtime entry point.
- `work2_coding/run_ppo.py`: Legacy PPO runtime entry point.

**Configuration:**
- `AGENTS.md`: Repository instructions and guardrails.
- `work2_coding/requirements.txt`: Runtime dependency list.
- `work2_coding/Src/parser.py`: Runtime argument defaults and valid choices.
- `work2_coding/Src/config.py`: Runtime config construction, logging, seeds, algorithm/environment loading.
- `work2_coding/Experiments/studies/*.yaml`: Study contracts.
- `work2_coding/Experiments/suites/*.yaml`: Suite contracts.

**Contract and Fairness Logic:**
- `work2_coding/Src/experiment_contracts.py`: Manifest path resolution and validation.
- `work2_coding/Src/policy_adapters.py`: Policy-tag adapter catalog.
- `work2_coding/Src/paired_replay.py`: Paired replay settings and normalized row schema.
- `work2_coding/Src/study_execution.py`: Actual, blocked, and failed row construction.

**Core Runtime Logic:**
- `work2_coding/Src/Algorithms/DSPO_Menu.py`: V1 robust service-menu behavior.
- `work2_coding/Environments/OOH/Parcelpoint_py.py`: OOH simulator step/reset/stats logic.
- `work2_coding/Environments/OOH/customerchoice.py`: MNL choice with outside option.
- `work2_coding/Environments/OOH/containers.py`: Service product, bundle, offer, and choice result dataclasses.
- `work2_coding/Src/Utils/Utils.py`: Logging, dynamic import, data loading, checkpoint metadata, checkpoint loading.

**Artifact and Claim Logic:**
- `work2_coding/Src/artifact_status.py`: Artifact claim-readiness classifier.
- `work2_coding/Src/artifact_builder.py`: Main robust-menu artifact builder.
- `work2_coding/Src/manuscript_claims.py`: Claim guards and manuscript frame rendering.
- `work2_coding/Src/paper_artifacts.py`: Phase 10 package index and status builder.
- `work2_coding/Src/formal_readiness.py`: Formal preflight checker.
- `work2_coding/Src/sensitivity_analysis.py`: Phase 8 sensitivity builder.
- `work2_coding/Src/computational_tractability.py`: Phase 9 tractability builder.
- `work2_coding/Src/baseline_validation.py`: Baseline validation gate.
- `work2_coding/Src/model_consistency_report.py`: Model consistency gate.
- `work2_coding/Src/attention_artifacts.py`: Attention diagnostics outside v1 claim-ready scope.

**Planning and Paper Context:**
- `.planning/PROJECT.md`: Current project state.
- `.planning/REQUIREMENTS.md`: Requirements and out-of-scope constraints.
- `.planning/ROADMAP.md`: Phase map and status.
- `.planning/STATE.md`: Active next-step state.
- `.planning/research/SUMMARY.md`: Research framing.
- `.planning/paper/TR_E_RESEARCH_DESIGN.md`: TR-E research design.
- `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md`: Table/figure claim-source mapping.
- `.planning/paper/TR_E_MANUSCRIPT_STRUCTURE.md`: Manuscript structure.

**Generated Evidence:**
- `work2_coding/outputs/studies/*/*/manifest_snapshot.yaml`: Frozen manifest copy for a run.
- `work2_coding/outputs/studies/*/*/normalized_rows.json`: Generated normalized rows.
- `work2_coding/outputs/studies/*/*/normalized_rows.csv`: Generated normalized rows in CSV form.
- `work2_coding/outputs/studies/*/*/study_summary.json`: Run summary.
- `work2_coding/outputs/studies/*/*/blockers.json`: Blocker metadata.
- `work2_coding/artifacts/work2_robust_menu/ARTIFACT_STATUS.json`: Main artifact gate output.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`: Phase 10 package gate.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`: Strict claim guard.
- `artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`: Mirrored Phase 10 package gate.

**Testing:**
- `work2_coding/scripts/test_experiment_contracts.py`: Manifest contract tests.
- `work2_coding/scripts/test_policy_fairness_contract.py`: Paired policy fairness tests.
- `work2_coding/scripts/test_paired_replay_contract.py`: Paired replay row contract tests.
- `work2_coding/scripts/test_optout_accounting.py`: Opt-out and home pickup accounting tests.
- `work2_coding/scripts/test_checkpoint_provenance.py`: Checkpoint provenance tests.
- `work2_coding/scripts/test_artifact_gates.py`: Artifact gate tests.
- `work2_coding/scripts/test_formal_readiness.py`: Formal readiness tests.
- `work2_coding/scripts/test_phase10_paper_artifacts.py`: Phase 10 package tests.
- `work2_coding/tests/test_akkerman_rc_no_failure.py`: Pytest-style legacy RC test.

## Naming Conventions

**Files:**
- Use lowercase snake_case for new Python orchestration and builder modules, as in `work2_coding/Src/study_execution.py` and `work2_coding/Src/artifact_status.py`.
- Preserve legacy mixed-case runtime filenames when extending existing modules, as in `work2_coding/Src/Algorithms/DSPO_Menu.py` and `work2_coding/Environments/OOH/Parcelpoint_py.py`.
- Use `test_<contract>.py` for script-style tests under `work2_coding/scripts/`, as in `work2_coding/scripts/test_optout_accounting.py`.
- Use descriptive lowercase YAML names for study manifests under `work2_coding/Experiments/studies/`, as in `work2_coding/Experiments/studies/formal_robust_menu.yaml`.
- Use uppercase status artifact filenames for generated gates, as in `work2_coding/artifacts/work2_robust_menu/ARTIFACT_STATUS.json`, `PACKAGE_STATUS.json`, and `CLAIM_GUARD.json`.

**Directories:**
- Use existing project casing for active runtime directories: `work2_coding/Src/`, `work2_coding/Experiments/`, `work2_coding/Environments/`.
- Place study manifests in `work2_coding/Experiments/studies/`.
- Place suite manifests in `work2_coding/Experiments/suites/`.
- Place executable wrappers and script tests in `work2_coding/scripts/`.
- Place generated runtime outputs in `work2_coding/outputs/`.
- Place generated runtime artifact packages in `work2_coding/artifacts/`.
- Place paper-facing mirrors in root `artifacts/`.

**Functions:**
- Use snake_case for new functions, matching `load_manifest`, `validate_manifest`, `build_normalized_row`, `classify_artifact`, and `write_phase10_package`.
- Keep class methods in snake_case in legacy classes, as in `work2_coding/Src/Algorithms/DSPO_Menu.py`.

**Classes and Types:**
- Use PascalCase for domain dataclasses and runtime classes, as in `ServiceBundle`, `ServiceProduct`, `MenuOffer`, `ChoiceResult`, `Config`, and `DSPO_Menu`.
- Keep generated row schema fields in lowercase snake_case, as in `count_opted_out`, `count_accepted_home`, `checkpoint_status`, and `paired_trace_hash`.

## Runtime, Planning, and Artifact Boundaries

**Runtime Boundary:**
- Active runtime code lives under `work2_coding/`.
- New executable behavior belongs in `work2_coding/Src/` and should be exposed through thin wrappers in `work2_coding/scripts/`.
- Do not add a parallel `ooh_code/` runtime root.

**Planning Boundary:**
- Planning context lives under `.planning/`.
- Update `.planning/paper/` for research design, claim mapping, and manuscript structure.
- Update `.planning/results/` only through the phase/report builder that owns the result summary.
- Do not make `.planning/` the source of executable runtime behavior.

**Generated Artifact Boundary:**
- Raw generated run evidence lives under `work2_coding/outputs/`.
- Runtime artifact packages live under `work2_coding/artifacts/`.
- Root `artifacts/` is a mirror or paper-facing package location.
- Do not hand-edit generated rows, package status, or claim guard files to change conclusions.

**Paper Boundary:**
- `.planning/paper/` contains planning and claim-map documents.
- `manuscript/` and `paper/` contain paper-facing material.
- Paper claims must align with `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json` and `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md`.

## Where to Add New Code

**New Study Contract:**
- Primary code: `work2_coding/Experiments/studies/<study_name>.yaml`
- Suite membership: `work2_coding/Experiments/suites/<suite_name>.yaml`
- Validation support: `work2_coding/Src/experiment_contracts.py`
- Tests: `work2_coding/scripts/test_experiment_contracts.py`

**New Policy Comparison:**
- Policy tag and overrides: `work2_coding/Src/policy_adapters.py`
- Runtime parser support: `work2_coding/Src/parser.py`
- Study manifest fields: `work2_coding/Experiments/studies/<study_name>.yaml`
- Fairness tests: `work2_coding/scripts/test_policy_fairness_contract.py`, `work2_coding/scripts/test_paired_replay_contract.py`

**New Service-Menu Algorithm Behavior:**
- Implementation: `work2_coding/Src/Algorithms/DSPO_Menu.py`
- Parser flags: `work2_coding/Src/parser.py`
- Policy adapter wiring: `work2_coding/Src/policy_adapters.py`
- Runtime tests: `work2_coding/scripts/test_robust_menu_logic.py`, `work2_coding/scripts/test_menu_runtime_contract.py`

**New Choice or Accounting Behavior:**
- Domain objects: `work2_coding/Environments/OOH/containers.py`
- Choice logic: `work2_coding/Environments/OOH/customerchoice.py`
- Environment counters: `work2_coding/Environments/OOH/Parcelpoint_py.py`
- Row schema and rates: `work2_coding/Src/paired_replay.py`, `work2_coding/Src/study_execution.py`
- Tests: `work2_coding/scripts/test_optout_accounting.py`, `work2_coding/scripts/test_mnl_choice_contract.py`

**New Normalized Row Field:**
- Schema: `work2_coding/Src/paired_replay.py`
- Actual row population: `work2_coding/Src/study_execution.py`
- Artifact validation: `work2_coding/Src/artifact_status.py`
- Artifact aggregation: `work2_coding/Src/artifact_builder.py`
- Tests: `work2_coding/scripts/test_paired_replay_contract.py`, `work2_coding/scripts/test_artifact_gates.py`

**New Checkpoint or Readiness Rule:**
- Checkpoint metadata: `work2_coding/Src/study_execution.py`, `work2_coding/Src/Utils/Utils.py`
- Formal preflight: `work2_coding/Src/formal_readiness.py`
- Artifact gate: `work2_coding/Src/artifact_status.py`
- Tests: `work2_coding/scripts/test_checkpoint_provenance.py`, `work2_coding/scripts/test_formal_readiness.py`

**New Artifact or Table/Figure Builder:**
- Main robust-menu artifacts: `work2_coding/Src/artifact_builder.py`
- Artifact status rules: `work2_coding/Src/artifact_status.py`
- Script wrapper: `work2_coding/scripts/build_<artifact_name>.py`
- Paper claim map: `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md`
- Tests: `work2_coding/scripts/test_artifact_builder.py`, `work2_coding/scripts/test_artifact_gates.py`

**New Phase 8 Sensitivity Output:**
- Implementation: `work2_coding/Src/sensitivity_analysis.py`
- Study manifest: `work2_coding/Experiments/studies/phase8_sensitivity_<axis>.yaml`
- Suite manifest: `work2_coding/Experiments/suites/phase8_sensitivity_must_have.yaml`
- Script wrapper: `work2_coding/scripts/build_phase8_sensitivity_artifacts.py`
- Tests: `work2_coding/scripts/test_phase8_sensitivity_contracts.py`, `work2_coding/scripts/test_phase8_sensitivity_summary.py`

**New Phase 9 Tractability Output:**
- Implementation: `work2_coding/Src/computational_tractability.py`
- Study manifest: `work2_coding/Experiments/studies/phase9_exact_greedy_tractability.yaml`
- Script wrapper: `work2_coding/scripts/build_phase9_tractability_artifacts.py`
- Tests: `work2_coding/scripts/test_phase9_exact_greedy_contracts.py`, `work2_coding/scripts/test_phase9_tractability_summary.py`

**New Phase 10 Paper Package Source:**
- Source collection and indexing: `work2_coding/Src/paper_artifacts.py`
- Claim guard rules: `work2_coding/Src/manuscript_claims.py`
- Builder script: `work2_coding/scripts/build_phase10_paper_artifacts.py`
- Paper source map: `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md`
- Tests: `work2_coding/scripts/test_phase10_paper_artifacts.py`, `work2_coding/scripts/test_manuscript_claim_guard.py`

**New Manuscript Claim Language:**
- Claim guard implementation: `work2_coding/Src/manuscript_claims.py`
- Manuscript design docs: `.planning/paper/TR_E_RESEARCH_DESIGN.md`, `.planning/paper/TR_E_MANUSCRIPT_STRUCTURE.md`
- Evidence map: `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md`
- Do not edit generated `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json` directly.

**New Attention Diagnostic:**
- Implementation: `work2_coding/Src/attention_artifacts.py`
- Script wrapper: `work2_coding/scripts/build_attention_artifacts.py`
- Parser flags: `work2_coding/Src/parser.py`
- Tests: `work2_coding/scripts/test_attention_*.py`
- Scope: Keep outputs diagnostic or future-scope for v1 unless claim guards are changed through evidence-backed gates.

**Shared Utilities:**
- Runtime helpers: `work2_coding/Src/Utils/Utils.py`
- Option-feature helpers: `work2_coding/Src/Utils/option_features.py`
- Predictor helpers: `work2_coding/Src/Utils/Predictors.py`

## Special Directories

**`work2_coding/outputs/`:**
- Purpose: Raw generated run outputs, shared checkpoint outputs, and study evidence.
- Generated: Yes
- Committed: Selectively, only when project workflow expects evidence artifacts.
- Rule: Do not hand-edit `work2_coding/outputs/studies/*/*/normalized_rows.json` or `work2_coding/outputs/studies/*/*/normalized_rows.csv`.

**`work2_coding/artifacts/`:**
- Purpose: Generated artifact packages produced by runtime builders.
- Generated: Yes
- Committed: Selectively, for evidence packages and paper artifacts.
- Rule: Regenerate through `work2_coding/scripts/build_artifacts.py`, `work2_coding/scripts/build_phase10_paper_artifacts.py`, or phase-specific builders.

**`artifacts/`:**
- Purpose: Root-level mirror or paper-facing package copy.
- Generated: Yes
- Committed: Selectively, for final or paper-facing packages.
- Rule: Treat root `artifacts/work2_robust_menu/` as a mirror of generated evidence, not a separate source of truth.

**`.planning/`:**
- Purpose: GSD workflow, planning, research, phase, and paper-claim state.
- Generated: Mixed; some files are human-authored planning docs and some are generated by GSD commands.
- Committed: Yes
- Rule: Keep codebase maps and paper maps aligned with current `work2_coding/` files.

**`.planning/data/case_studies/`:**
- Purpose: Case-study scaffold evidence indexed by Phase 10.
- Generated: Mixed
- Committed: Yes
- Rule: Treat as scaffold sources unless a phase upgrades them with formal evidence.

**`work2_coding/Experiments/Parcelpoint_py/`:**
- Purpose: Legacy/original experiment folders retained from the base runtime.
- Generated: Mixed
- Committed: Existing project state
- Rule: Do not place new TR-E service-menu study contracts here; use `work2_coding/Experiments/studies/` and `work2_coding/Experiments/suites/`.

**`work2_coding/venv/`:**
- Purpose: Local Python virtual environment.
- Generated: Yes
- Committed: No
- Rule: Do not use as a source for architecture or dependency documentation.

**`work2_coding/.idea/`:**
- Purpose: Local IDE metadata.
- Generated: Yes
- Committed: No
- Rule: Ignore for runtime, planning, and artifact architecture.

**`manuscript/`:**
- Purpose: Paper manuscript material outside `.planning/`.
- Generated: Mixed
- Committed: Project-dependent
- Rule: Keep claim language aligned with `.planning/paper/` and generated claim guards.

**`paper/`:**
- Purpose: Paper assets outside `.planning/`.
- Generated: Mixed
- Committed: Project-dependent
- Rule: Do not use as executable runtime input unless a phase explicitly wires it through `work2_coding/Src/`.

---

*Structure analysis: 2026-06-16*
