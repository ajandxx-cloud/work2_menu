<!-- refreshed: 2026-06-16 -->
<!-- last_mapped_commit: 97514c7 -->
# Architecture

**Analysis Date:** 2026-06-16

## System Overview

```text
+------------------------------------------------------------------+
|                    Planning and claim design                      |
| `.planning/PROJECT.md` `.planning/REQUIREMENTS.md`                |
| `.planning/ROADMAP.md` `.planning/paper/*` `.planning/results/*`  |
+-------------------------------+----------------------------------+
                                |
                                v
+------------------------------------------------------------------+
|                  Manifest-driven execution layer                  |
| `work2_coding/scripts/run_study.py`                               |
| `work2_coding/Experiments/studies/*.yaml`                         |
| `work2_coding/Experiments/suites/*.yaml`                          |
+-------------------+----------------------+-----------------------+
                    |                      |
                    v                      v
+--------------------------------+  +------------------------------+
| Contract and fairness layer    |  | Runtime configuration layer  |
| `work2_coding/Src/experiment_` |  | `work2_coding/Src/config.py` |
| `contracts.py`                 |  | `work2_coding/Src/parser.py` |
| `work2_coding/Src/policy_`     |  +---------------+--------------+
| `adapters.py`                  |                  |
| `work2_coding/Src/paired_`     |                  v
| `replay.py`                    |  +------------------------------+
+-------------------+------------+  | Algorithm and simulator      |
                    |               | `work2_coding/Src/Algorithms`|
                    v               | `work2_coding/Environments`  |
+--------------------------------+  +---------------+--------------+
| Study execution and row output |                  |
| `work2_coding/Src/study_`      |                  v
| `execution.py`                 |  +------------------------------+
| `work2_coding/outputs/studies` |  | Evidence and artifact gates  |
+-------------------+------------+  | `work2_coding/Src/artifact_` |
                    |               | `status.py`                  |
                    v               | `work2_coding/Src/artifact_` |
+--------------------------------+  | `builder.py`                 |
| Paper and package outputs      |  | `work2_coding/Src/manuscript`|
| `work2_coding/artifacts/*`     |  | `_claims.py`                 |
| `artifacts/*` mirror packages  |  | `work2_coding/Src/paper_`    |
| `.planning/results/*`          |  | `artifacts.py`               |
+--------------------------------+  +------------------------------+
```

## Component Responsibilities

| Component | Responsibility | File |
|-----------|----------------|------|
| Study CLI | Runs a single study or suite, writes manifest snapshots, normalized rows, summaries, and blockers. | `work2_coding/scripts/run_study.py` |
| Manifest contracts | Resolves study and suite YAML, validates schema, paired settings, checkpoint contracts, policy tags, tiers, and run modes. | `work2_coding/Src/experiment_contracts.py` |
| Policy adapters | Maps named policy tags to parser/runtime overrides while preserving paired replay fairness. | `work2_coding/Src/policy_adapters.py` |
| Paired replay rows | Defines normalized row schema, paired setting hashes, checkpoint row metadata, and row validation. | `work2_coding/Src/paired_replay.py` |
| Study execution | Executes actual replay rows, blocked rows, checkpoint metadata, git provenance, and row-level replay failure handling. | `work2_coding/Src/study_execution.py` |
| Runtime config | Builds `Config`, seeds runtime state, redirects logs, loads algorithm and environment modules, and creates run folders. | `work2_coding/Src/config.py` |
| CLI defaults | Owns runtime arguments for menu mode, product mode, ETA filters, pricing mode, method family, outside option, and attention diagnostics. | `work2_coding/Src/parser.py` |
| Service menu policy | Builds service-menu candidates, filters ETA robustness, prices alternatives, selects menus, and records solver diagnostics. | `work2_coding/Src/Algorithms/DSPO_Menu.py` |
| OOH simulator | Applies customer choices, route mutation, capacity updates, rewards, and separate opt-out/home/meeting-point counters. | `work2_coding/Environments/OOH/Parcelpoint_py.py` |
| Choice model | Implements MNL menu, offer, and pricing choices with outside option mapped to opt-out rather than home pickup. | `work2_coding/Environments/OOH/customerchoice.py` |
| Service contracts | Defines `ServiceBundle`, `ServiceProduct`, `MenuOffer`, and `ChoiceResult` domain objects. | `work2_coding/Environments/OOH/containers.py` |
| Checkpoint utilities | Loads and inspects model checkpoints, dependency snapshots, and checkpoint metadata. | `work2_coding/Src/Utils/Utils.py` |
| Formal readiness | Performs clean-git, dependency, checkpoint existence, hash, and smoke-load preflight for formal claims. | `work2_coding/Src/formal_readiness.py` |
| Artifact gate | Classifies artifacts as claim-ready, diagnostic, incomplete, or blocked from rows and readiness metadata. | `work2_coding/Src/artifact_status.py` |
| Main artifact builder | Aggregates run rows, writes status tables and figures, mirrors artifacts, and invokes manuscript frame output. | `work2_coding/Src/artifact_builder.py` |
| Manuscript claim guard | Produces strict claim guards and manuscript frame files with blocked empirical claims recorded explicitly. | `work2_coding/Src/manuscript_claims.py` |
| Phase 10 package builder | Indexes main RC, Phase 8, Phase 9, case scaffold, and blocker artifacts into the paper package. | `work2_coding/Src/paper_artifacts.py` |
| Phase 8 sensitivity | Builds diagnostic/provisional sensitivity artifacts and summary status for ETA, uptake, menu-k, and guardrail axes. | `work2_coding/Src/sensitivity_analysis.py` |
| Phase 9 tractability | Builds diagnostic/provisional exact-vs-greedy tractability artifacts and summary status. | `work2_coding/Src/computational_tractability.py` |
| Baseline validation | Checks Phase 8 baseline pairing, accounting, checkpoint, and claim-readiness prerequisites. | `work2_coding/Src/baseline_validation.py` |
| Model consistency | Checks Phase 7 method-family, outside-option, opt-out accounting, and artifact-gate consistency. | `work2_coding/Src/model_consistency_report.py` |
| Planning state | Defines current milestone scope, guardrails, phase status, and paper claim boundaries. | `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, `.planning/STATE.md` |

## Pattern Overview

**Overall:** Manifest-driven offline research pipeline with claim-gated evidence production around a stateful many-to-one DRT simulator.

**Key Characteristics:**
- Use `work2_coding/` as the active runtime root; no `ooh_code/` directory is present in the current repository.
- Treat `work2_coding/Experiments/studies/*.yaml` as executable contracts, not informal configuration.
- Keep policy comparisons paired by deriving every policy row from shared split, demand, pricing, HGS, checkpoint, candidate, and utility settings in `work2_coding/Src/paired_replay.py`.
- Keep opt-out accounting separate from accepted home pickup through `work2_coding/Environments/OOH/customerchoice.py`, `work2_coding/Environments/OOH/Parcelpoint_py.py`, and `work2_coding/Src/paired_replay.py`.
- Require explicit checkpoint load status and checkpoint hashes for pilot/formal evidence through `work2_coding/Src/study_execution.py` and `work2_coding/Src/formal_readiness.py`.
- Treat no-filter rows as diagnostic unless artifact gates in `work2_coding/Src/artifact_status.py` allow stronger use.
- Keep attention-based choice/scoring in diagnostic or V2 paths such as `work2_coding/Src/attention_artifacts.py`, not in v1 claim-ready manuscript evidence.

## Layers

**Planning and Research Control:**
- Purpose: Define project intent, phase order, research constraints, and claim boundaries.
- Location: `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, `.planning/STATE.md`, `.planning/research/SUMMARY.md`, `.planning/paper/`
- Contains: Roadmap state, requirements, manuscript structure, table/figure claim mapping, case-study scaffolds, and results summaries.
- Depends on: Generated evidence under `work2_coding/artifacts/` and root `artifacts/`.
- Used by: Phase planning, paper writing, codebase mapping, and artifact-package checks.

**Execution Entry Layer:**
- Purpose: Provide script-style entry points for studies, checkpoints, readiness, artifacts, and phase reports.
- Location: `work2_coding/scripts/`
- Contains: `work2_coding/scripts/run_study.py`, `work2_coding/scripts/train_shared_checkpoint.py`, `work2_coding/scripts/check_formal_readiness.py`, `work2_coding/scripts/build_artifacts.py`, `work2_coding/scripts/build_phase10_paper_artifacts.py`
- Depends on: `work2_coding/Src/` modules and YAML manifests under `work2_coding/Experiments/`.
- Used by: Manual verification, GSD phase execution, and artifact refresh workflows.

**Manifest Contract Layer:**
- Purpose: Convert YAML study and suite declarations into validated settings and policy overrides.
- Location: `work2_coding/Experiments/studies/`, `work2_coding/Experiments/suites/`, `work2_coding/Src/experiment_contracts.py`, `work2_coding/Src/policy_adapters.py`
- Contains: Formal, pilot, smoke, Phase 8, and Phase 9 manifests plus policy adapter catalog.
- Depends on: Parser argument schema in `work2_coding/Src/parser.py`.
- Used by: `work2_coding/scripts/run_study.py`, readiness checks, and phase artifact builders.

**Paired Replay and Row Layer:**
- Purpose: Preserve replay fairness and emit a stable normalized-row-v2 evidence schema.
- Location: `work2_coding/Src/paired_replay.py`, `work2_coding/Src/study_execution.py`
- Contains: Paired setting hashes, checkpoint row metadata, blocked row builders, actual replay row builders, row validators.
- Depends on: Study manifests, policy adapters, runtime config, environment counters, checkpoint metadata, and git provenance.
- Used by: Study run outputs under `work2_coding/outputs/studies/` and artifact gates under `work2_coding/Src/artifact_status.py`.

**Runtime Simulation Layer:**
- Purpose: Execute DRT service-menu decisions and route/environment updates.
- Location: `work2_coding/Src/config.py`, `work2_coding/Src/parser.py`, `work2_coding/Src/Algorithms/`, `work2_coding/Environments/OOH/`, `work2_coding/Src/Utils/`
- Contains: Runtime args, `Config`, DSPO menu logic, OOH simulator, choice model, route/data utilities, checkpoint loading.
- Depends on: Demand data under `work2_coding/Environments/OOH/`, model checkpoint paths under `work2_coding/outputs/shared_training/`, and runtime args from manifests.
- Used by: Actual replay in `work2_coding/Src/study_execution.py`.

**Evidence Gate and Artifact Layer:**
- Purpose: Convert rows into research artifacts only when provenance, accounting, readiness, and claim status permit it.
- Location: `work2_coding/Src/artifact_status.py`, `work2_coding/Src/artifact_builder.py`, `work2_coding/Src/manuscript_claims.py`, `work2_coding/Src/paper_artifacts.py`, `work2_coding/Src/sensitivity_analysis.py`, `work2_coding/Src/computational_tractability.py`
- Contains: Artifact classification, aggregate builders, strict claim guards, manuscript frames, Phase 8 and Phase 9 diagnostic summaries, Phase 10 package index.
- Depends on: Normalized rows, readiness JSON, generated run directories, and case-study scaffolds.
- Used by: `work2_coding/artifacts/work2_robust_menu/`, root `artifacts/work2_robust_menu/`, `.planning/results/`, and `.planning/paper/`.

**Generated Output Layer:**
- Purpose: Store run outputs and packaged evidence without manual row editing.
- Location: `work2_coding/outputs/`, `work2_coding/artifacts/`, root `artifacts/`
- Contains: `normalized_rows.json`, `normalized_rows.csv`, `study_summary.json`, `blockers.json`, `ARTIFACT_STATUS.json`, `CLAIM_GUARD.json`, `PACKAGE_STATUS.json`, package indexes, status tables, and mirrored artifact bundles.
- Depends on: Script entry points in `work2_coding/scripts/`.
- Used by: Planning summaries, paper artifact checks, and claim guards.

## Data Flow

### Primary Request Path

1. Run `work2_coding/scripts/run_study.py:259` from `work2_coding/` with a study name or suite name.
2. Resolve and validate the manifest with `work2_coding/Src/experiment_contracts.py:53` and `work2_coding/Src/experiment_contracts.py:91`.
3. Resolve policy overrides from `work2_coding/Src/policy_adapters.py:384` and paired settings from `work2_coding/Src/paired_replay.py:144`.
4. `work2_coding/scripts/run_study.py:109` chooses contract-only, blocked, or actual replay output based on manifest mode and prerequisite status.
5. `work2_coding/Src/study_execution.py:58` inspects prerequisites, including required checkpoints for pilot/formal manifests.
6. `work2_coding/Src/study_execution.py:377` loops over paired settings and calls `work2_coding/Src/study_execution.py:217` for actual replay rows.
7. `work2_coding/Src/config.py:8` builds runtime configuration and `work2_coding/Src/config.py:114` resolves the algorithm and environment.
8. `work2_coding/Src/Algorithms/DSPO_Menu.py:1718` builds a service menu action and `work2_coding/Environments/OOH/Parcelpoint_py.py:240` applies the choice to simulator state.
9. `work2_coding/Src/paired_replay.py:249` builds a normalized row and `work2_coding/Src/paired_replay.py:410` validates row contracts.
10. `work2_coding/scripts/run_study.py` writes `manifest_snapshot.yaml`, `normalized_rows.json`, `normalized_rows.csv`, `study_summary.json`, and `blockers.json` under `work2_coding/outputs/studies/<study>/<run_id>/`.

### Artifact and Claim Gate Path

1. Run `work2_coding/scripts/build_artifacts.py:32` against a run directory under `work2_coding/outputs/studies/`.
2. `work2_coding/Src/artifact_builder.py:287` loads rows, aggregates policy metrics, writes table/figure data, and invokes artifact classification.
3. `work2_coding/Src/artifact_status.py:53` classifies status from rows, readiness metadata, checkpoint metadata, accounting validity, and diagnostic boundaries.
4. `work2_coding/Src/manuscript_claims.py:281` and `work2_coding/Src/manuscript_claims.py:407` build ordinary and strict claim guards.
5. `work2_coding/Src/manuscript_claims.py:602` writes manuscript frame files when called by artifact builders.
6. Outputs land in `work2_coding/artifacts/work2_robust_menu/` and may mirror to root `artifacts/work2_robust_menu/`.

### Phase 10 Paper Package Path

1. Run `work2_coding/scripts/build_phase10_paper_artifacts.py:37`.
2. `work2_coding/Src/paper_artifacts.py:291` collects source artifacts from main RC, Phase 8, Phase 9, case scaffold, and blocker-status roots.
3. `work2_coding/Src/paper_artifacts.py:387` builds package indexes and source-family summaries.
4. `work2_coding/Src/paper_artifacts.py:586` writes `PACKAGE_INDEX.json`, `PACKAGE_STATUS.json`, `CLAIM_GUARD.json`, and Markdown indexes under `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/`.
5. The same package is mirrored under root `artifacts/work2_robust_menu/phase10_paper_artifacts/` for paper-facing consumption.

### Formal Readiness Path

1. Run `work2_coding/scripts/check_formal_readiness.py:21` with a formal manifest and checkpoint path.
2. `work2_coding/Src/formal_readiness.py:220` checks manifest validity, clean git policy, dependency snapshot, checkpoint existence, checkpoint hash, and checkpoint smoke-load status.
3. Readiness output is consumed by `work2_coding/Src/artifact_status.py` before any formal artifact can be classified as claim-ready.

### Phase-Specific Evidence Paths

1. Phase 8 sensitivity artifacts use `work2_coding/Src/sensitivity_analysis.py` and script wrappers under `work2_coding/scripts/build_phase8_sensitivity_*.py`.
2. Phase 9 tractability artifacts use `work2_coding/Src/computational_tractability.py` and script wrappers under `work2_coding/scripts/build_phase9_tractability_*.py`.
3. Baseline and model-consistency gates use `work2_coding/Src/baseline_validation.py` and `work2_coding/Src/model_consistency_report.py`.
4. Attention diagnostics use `work2_coding/Src/attention_artifacts.py` and `work2_coding/scripts/build_attention_artifacts.py`; these remain outside v1 claim-ready scope.

**State Management:**
- Runtime state is held in the simulator instance from `work2_coding/Environments/OOH/Parcelpoint_py.py` during each replay.
- Experiment state is file-based under `work2_coding/outputs/studies/` and `work2_coding/artifacts/`.
- Planning state is file-based under `.planning/` and should be updated only through phase workflows.
- Generated rows and paper artifact packages are evidence outputs; do not hand-edit files under `work2_coding/outputs/`, `work2_coding/artifacts/`, or root `artifacts/` to change conclusions.

## Key Abstractions

**Study Manifest:**
- Purpose: Declares tier, run mode, paired splits, policy tags, checkpoint requirements, and output schema.
- Examples: `work2_coding/Experiments/studies/formal_robust_menu.yaml`, `work2_coding/Experiments/studies/pilot_robust_menu.yaml`, `work2_coding/Experiments/studies/smoke_robust_menu.yaml`
- Pattern: Validate through `work2_coding/Src/experiment_contracts.py` before runtime execution.

**Suite Manifest:**
- Purpose: Groups study manifests for repeated diagnostic or phase execution.
- Examples: `work2_coding/Experiments/suites/phase8_sensitivity_must_have.yaml`, `work2_coding/Experiments/suites/phase9_exact_greedy_tractability.yaml`
- Pattern: `work2_coding/scripts/run_study.py` expands suites through `work2_coding/Src/experiment_contracts.py`.

**Policy Adapter:**
- Purpose: Maps stable policy tags to runtime args without changing non-policy paired settings.
- Examples: `mainline_optimized_adaptive` and `MAINLINE_POLICY_TAGS` in `work2_coding/Src/policy_adapters.py`
- Pattern: Add or change policies only through `work2_coding/Src/policy_adapters.py` plus parser support in `work2_coding/Src/parser.py`.

**Paired Setting:**
- Purpose: Captures all shared replay dimensions so policies remain comparable on identical splits and demand.
- Examples: `work2_coding/Src/paired_replay.py:144`, `work2_coding/Src/paired_replay.py:177`
- Pattern: Any new fairness dimension belongs in manifest paired fields and paired-setting validation before execution.

**Normalized Row:**
- Purpose: Stable evidence schema used by artifact builders, paper package indexes, and phase gates.
- Examples: `NORMALIZED_ROW_FIELDS` in `work2_coding/Src/paired_replay.py`, generated `work2_coding/outputs/studies/*/*/normalized_rows.json`
- Pattern: Add metrics through `work2_coding/Src/paired_replay.py` and `work2_coding/Src/study_execution.py`, then update artifact gates and script tests.

**Checkpoint Metadata:**
- Purpose: Records whether a checkpoint is `loaded`, `failed`, `missing`, or diagnostic-only, with path and hash when available.
- Examples: `work2_coding/Src/study_execution.py:106`, `work2_coding/Src/Utils/Utils.py:141`, `work2_coding/Src/formal_readiness.py`
- Pattern: Pilot/formal rows require explicit loaded checkpoint metadata for claim-bearing artifacts.

**Service Menu Domain Objects:**
- Purpose: Represent service bundles, products, offers, and customer outcomes.
- Examples: `work2_coding/Environments/OOH/containers.py`
- Pattern: Outside option maps to `ChoiceResult.opted_out`; do not encode outside option as accepted home pickup.

**Artifact Status:**
- Purpose: Encodes whether generated evidence supports claims or remains diagnostic, incomplete, or blocked.
- Examples: `work2_coding/Src/artifact_status.py`, `work2_coding/artifacts/work2_robust_menu/ARTIFACT_STATUS.json`
- Pattern: Artifact status is derived from source rows and readiness metadata; do not override generated status files manually.

**Strict Claim Guard:**
- Purpose: Records allowed and blocked paper claims using Phase 10 package evidence.
- Examples: `work2_coding/Src/manuscript_claims.py:407`, `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`
- Pattern: Universal dominance, real passenger validation, no-filter operational recommendation, exact optimality, and ungated attention claims remain blocked unless the guard source evidence changes.

## Entry Points

**Study Runner:**
- Location: `work2_coding/scripts/run_study.py`
- Triggers: Manual command or phase execution from `work2_coding/`.
- Responsibilities: Load manifests, validate contracts, produce normalized rows and run summaries.

**Shared Checkpoint Trainer:**
- Location: `work2_coding/scripts/train_shared_checkpoint.py`
- Triggers: Checkpoint preparation for pilot or formal manifests.
- Responsibilities: Train deterministic synthetic shared predictor checkpoints and write sidecar metadata.

**Formal Readiness Checker:**
- Location: `work2_coding/scripts/check_formal_readiness.py`
- Triggers: Preflight before formal claim-ready artifacts.
- Responsibilities: Validate clean git, dependency snapshot, checkpoint existence, hash, and load status.

**Main Artifact Builder:**
- Location: `work2_coding/scripts/build_artifacts.py`
- Triggers: After a study run directory exists under `work2_coding/outputs/studies/`.
- Responsibilities: Build aggregate metrics, tables, figure JSON, artifact status, and manuscript frame.

**Manuscript Frame Builder:**
- Location: `work2_coding/scripts/build_manuscript_frame.py`
- Triggers: Manual regeneration of manuscript frame files from artifact status.
- Responsibilities: Write claim-bounded paper scaffolding through `work2_coding/Src/manuscript_claims.py`.

**Phase 10 Package Builder:**
- Location: `work2_coding/scripts/build_phase10_paper_artifacts.py`
- Triggers: Paper package assembly.
- Responsibilities: Index source artifacts, write package status, and strict claim guard.

**Phase 8 Builders:**
- Location: `work2_coding/scripts/build_phase8_sensitivity_artifacts.py`, `work2_coding/scripts/build_phase8_sensitivity_summary.py`, `work2_coding/scripts/build_phase8_baseline_validation_report.py`
- Triggers: Sensitivity and baseline validation reporting.
- Responsibilities: Produce diagnostic/provisional sensitivity and baseline validation outputs.

**Phase 9 Builders:**
- Location: `work2_coding/scripts/build_phase9_tractability_artifacts.py`, `work2_coding/scripts/build_phase9_tractability_summary.py`, `work2_coding/scripts/build_phase9_dspo_family_validation_report.py`
- Triggers: Tractability and DSPO-family diagnostics.
- Responsibilities: Produce exact-vs-greedy and family validation diagnostics.

**Legacy Original Runtime:**
- Location: `work2_coding/run.py`, `work2_coding/run_ppo.py`
- Triggers: Original Akkerman-style runtime usage.
- Responsibilities: Legacy experiment execution; do not use as the primary TR-E service-menu evidence path unless a phase explicitly requires legacy comparison.

## Architectural Constraints

- **Runtime root:** Execute active research commands from `work2_coding/`; do not create or target `ooh_code/`.
- **Directory casing:** Current manifests live under `work2_coding/Experiments/`; `work2_coding/Src/experiment_contracts.py` contains a lowercase fallback only for compatibility.
- **Threading:** The active pipeline is synchronous and single-process; simulator state mutates in `work2_coding/Environments/OOH/Parcelpoint_py.py` during each replay.
- **Global state:** `work2_coding/Src/config.py` redirects `sys.stdout` through `work2_coding/Src/Utils/Utils.py` logging and seeds global numpy and torch RNGs.
- **Checkpoint contract:** Pilot and formal evidence requires explicit checkpoint load status through `work2_coding/Src/study_execution.py` and `work2_coding/Src/formal_readiness.py`.
- **Generated evidence boundary:** Files under `work2_coding/outputs/`, `work2_coding/artifacts/`, and root `artifacts/` are generated evidence; change builders or source rows instead of editing generated conclusions.
- **Claim boundary:** No-filter, Phase 8, Phase 9, and attention outputs are diagnostic/provisional unless `work2_coding/Src/artifact_status.py` and `work2_coding/Src/manuscript_claims.py` mark them otherwise.
- **Authentication:** Not applicable; this is a local research codebase without external auth integration.
- **Circular imports:** No known circular import chain is part of the active manifest pipeline; preserve script wrappers as thin importers into `work2_coding/Src/`.

## Anti-Patterns

### Targeting `ooh_code/`

**What happens:** New scripts, paths, or docs point to `ooh_code/`.
**Why it's wrong:** The current repository has active runtime files under `work2_coding/` and no detected `ooh_code/` directory.
**Do this instead:** Use `work2_coding/Src/`, `work2_coding/scripts/`, `work2_coding/Experiments/`, `work2_coding/outputs/`, and `work2_coding/artifacts/`.

### Bypassing Manifest Contracts

**What happens:** Code constructs runtime args directly for policy comparisons without updating `work2_coding/Experiments/studies/*.yaml` and `work2_coding/Src/policy_adapters.py`.
**Why it's wrong:** Paired replay fairness depends on shared fields, trace hashes, required policy tags, and validated policy-only overrides in `work2_coding/Src/experiment_contracts.py`.
**Do this instead:** Add study settings to `work2_coding/Experiments/studies/<name>.yaml`, add policy overrides to `work2_coding/Src/policy_adapters.py`, and validate through `work2_coding/scripts/test_experiment_contracts.py`.

### Collapsing Opt-Out Into Home Pickup

**What happens:** Outside-option choices are counted as accepted home service or included in accepted-home metrics.
**Why it's wrong:** Research guardrails and artifact gates require separate `count_opted_out`, `count_accepted_home`, and `count_accepted_meeting_point` accounting.
**Do this instead:** Preserve `ChoiceResult.opted_out` in `work2_coding/Environments/OOH/containers.py`, counter updates in `work2_coding/Environments/OOH/Parcelpoint_py.py`, and row validation in `work2_coding/Src/paired_replay.py`.

### Upgrading Diagnostic Evidence By Wording

**What happens:** Paper text treats no-filter, attention, Phase 8, or Phase 9 diagnostic outputs as operational recommendations or claim-ready evidence.
**Why it's wrong:** `work2_coding/Src/artifact_status.py`, `work2_coding/Src/manuscript_claims.py`, and `work2_coding/Src/paper_artifacts.py` encode blocked and diagnostic status.
**Do this instead:** Keep manuscript claims aligned with `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json` and `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md`.

### Hand-Editing Generated Rows Or Artifact Status

**What happens:** `normalized_rows.json`, `ARTIFACT_STATUS.json`, `CLAIM_GUARD.json`, or `PACKAGE_STATUS.json` is edited to change study results.
**Why it's wrong:** Artifact status and claim guards must be reproducible from manifests, runtime code, and generated source rows.
**Do this instead:** Update `work2_coding/Src/` builders, manifests in `work2_coding/Experiments/`, or source execution data, then rerun the appropriate script under `work2_coding/scripts/`.

## Error Handling

**Strategy:** Fail fast on invalid contracts, represent blocked prerequisites as explicit row/status metadata, and keep diagnostic outputs labeled as diagnostic.

**Patterns:**
- `work2_coding/Src/experiment_contracts.py` raises validation errors for invalid manifests, unsupported args, duplicate policy tags, unsupported tiers, and missing required fields.
- `work2_coding/Src/study_execution.py` emits blocked rows when prerequisite artifacts such as required checkpoints are missing.
- `work2_coding/Src/Utils/Utils.py` and `work2_coding/Src/Algorithms/Agent.py` record checkpoint load metadata and reject pilot/formal checkpoint mismatches.
- `work2_coding/Src/artifact_status.py` blocks claim-ready classification for placeholder rows, invalid accounting, missing readiness, failed checkpoint metadata, no-filter-only diagnostics, and all-diagnostic policies.
- Script tests under `work2_coding/scripts/test_*.py` return non-zero process status on contract failures.

## Cross-Cutting Concerns

**Logging:** Runtime logs are written through `work2_coding/Src/Utils/Utils.py` logger redirection from `work2_coding/Src/config.py`; orchestration scripts also use stdout for status output.

**Validation:** Manifest validation lives in `work2_coding/Src/experiment_contracts.py`; row validation lives in `work2_coding/Src/paired_replay.py`; artifact validation lives in `work2_coding/Src/artifact_status.py`; paper-claim validation lives in `work2_coding/Src/manuscript_claims.py`.

**Authentication:** Not applicable for active local execution; no external identity provider is part of the architecture.

**Provenance:** Git SHA, dirty flag, manifest snapshot, paired trace hash, dependency snapshot, checkpoint status, and checkpoint hash are recorded through `work2_coding/Src/study_execution.py`, `work2_coding/Src/formal_readiness.py`, and generated files under `work2_coding/outputs/`.

**Research Scope:** V1 service-menu claims use robust time-window menu evidence from `work2_coding/Src/Algorithms/DSPO_Menu.py`; attention features in `work2_coding/Src/attention_artifacts.py` and parser attention flags in `work2_coding/Src/parser.py` remain diagnostic or future-scope unless the claim guard changes.

---

*Architecture analysis: 2026-06-16*
