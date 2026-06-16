---
last_mapped_commit: 97514c7
---

# External Integrations

**Analysis Date:** 2026-06-16

**Active runtime root:** `work2_coding/`

## APIs & External Services

**Cloud/HTTP APIs:**
- Not detected. Current source under `work2_coding/Src/`, `work2_coding/Environments/`, and `work2_coding/scripts/` does not use `requests`, `httpx`, cloud SDKs, payment SDKs, hosted databases, or external web APIs.

**Routing Solver:**
- Hygese HGS solver - Local package integration for route reoptimization and final route cost evaluation.
  - SDK/Client: `hygese~=0.0.0.8` from `work2_coding/requirements.txt`.
  - Implementation: `work2_coding/Environments/OOH/env_utils.py`, with algorithm calls from `work2_coding/Src/Algorithms/DSPO.py`, `work2_coding/Src/Algorithms/DSPO_Menu.py`, `work2_coding/Src/Algorithms/Baseline.py`, and `work2_coding/Src/Algorithms/Heuristic.py`.
  - Config: `--hgs_reopt_time` and `--hgs_final_time` in `work2_coding/Src/parser.py`.
  - Auth: not applicable.

**Scientific Runtime Libraries:**
- PyTorch - Local model training and checkpoint interface.
  - SDK/Client: `torch>=2.0.1`.
  - Implementation: `work2_coding/Src/Utils/Predictors.py`, `work2_coding/Src/Algorithms/Agent.py`, `work2_coding/scripts/train_shared_checkpoint.py`, and `work2_coding/Src/formal_readiness.py`.
  - Auth: not applicable.
- SciPy Lambert W - Pricing support for DSPO.
  - SDK/Client: `scipy~=1.11.1`.
  - Implementation: `work2_coding/Src/Algorithms/DSPO.py`; menu code uses `work2_coding/Src/Utils/MathUtils.py`, which includes an internal fallback for the real principal branch.
  - Auth: not applicable.
- Matplotlib - Noninteractive figure generation.
  - SDK/Client: `matplotlib~=3.7.2`.
  - Implementation: `work2_coding/Src/artifact_builder.py`, `work2_coding/Src/computational_tractability.py`, `work2_coding/Src/sensitivity_analysis.py`, and `work2_coding/Src/Utils/Utils.py`.
  - Auth: not applicable.

## Data Storage

**Databases:**
- Not detected. There is no SQL database, ORM, migration system, document database, or remote persistence layer.
  - Connection: not applicable.
  - Client: not applicable.

**File Storage:**
- Local filesystem only. All datasets, manifests, normalized rows, checkpoints, readiness outputs, and paper artifacts are read from or written to repository-local paths.

**Caching:**
- No dedicated cache service is detected.
- Checkpoints and generated outputs function as durable local artifacts, not cache entries.

## File and Artifact Interfaces

**Bundled datasets:**
- Homberger-Gehring style instances: `work2_coding/Environments/OOH/HombergerGehring_data/`.
- Amazon-style instances: `work2_coding/Environments/OOH/Amazon_data/`.
- Dataset loading entry point: `work2_coding/Src/Utils/Utils.py`.
- Environment selection flags: `--instance` and `--load_data` in `work2_coding/Src/parser.py`.

**Study and suite manifests:**
- Studies: `work2_coding/Experiments/studies/*.yaml`.
- Suites: `work2_coding/Experiments/suites/*.yaml`.
- Contract loader/validator: `work2_coding/Src/experiment_contracts.py`.
- Use manifests to define run mode, policy tags, checkpoint requirements, paired fields, varied fields, acceptance guardrails, and diagnostic status.

**Study outputs:**
- Default study output root: `work2_coding/outputs/studies/<study>/<run_id>/`.
- Key files: `manifest_snapshot.yaml`, `normalized_rows.json`, `normalized_rows.csv`, `study_summary.json`, and optional `blockers.json`.
- Writer: `work2_coding/scripts/run_study.py` through `work2_coding/Src/study_execution.py`.
- Normalized schema and paired replay checks: `work2_coding/Src/paired_replay.py`.

**Runtime experiment logs:**
- Default runtime experiment tree: `work2_coding/Experiments/Parcelpoint_py/`.
- Runtime config snapshot: `args.yaml` written by `work2_coding/Src/config.py`.
- Log file redirection: `work2_coding/Src/Utils/Utils.py` via `Logger`.

**Checkpoints:**
- Formal shared checkpoint path: `work2_coding/outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt`.
- Sidecar metadata path: `work2_coding/outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt.sidecar.json`.
- Trainer: `work2_coding/scripts/train_shared_checkpoint.py`.
- Loader and checkpoint status metadata: `work2_coding/Src/Algorithms/Agent.py`, `work2_coding/Src/study_execution.py`, and `work2_coding/Src/formal_readiness.py`.
- Formal and pilot rows must preserve explicit `checkpoint_load_status`, `checkpoint_path`, `checkpoint_hash`, `checkpoint_required`, and mismatch metadata.

**Formal readiness outputs:**
- Default root: `work2_coding/outputs/formal_readiness/<study>/`.
- Files: `FORMAL_READINESS.json`, `FORMAL_READINESS.md`, and `DEPENDENCY_SNAPSHOT.json`.
- Writer: `work2_coding/scripts/check_formal_readiness.py` and `work2_coding/Src/formal_readiness.py`.
- Dependency snapshots use Git provenance and `python -m pip freeze`.

**Artifact packages:**
- Main artifact root: `work2_coding/artifacts/work2_robust_menu/`.
- Root mirror: `artifacts/work2_robust_menu/`.
- Phase 10 package root: `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/`.
- Phase 10 mirror: `artifacts/work2_robust_menu/phase10_paper_artifacts/`.
- Builders: `work2_coding/scripts/build_artifacts.py`, `work2_coding/scripts/build_manuscript_frame.py`, and `work2_coding/scripts/build_phase10_paper_artifacts.py`.
- Package indexes/status files: `PACKAGE_INDEX.json`, `SOURCE_INDEX.json`, `ARTIFACT_TO_SECTION_MAP.json`, `PACKAGE_STATUS.json`, and `CLAIM_GUARD.json`.
- Claim guard logic: `work2_coding/Src/manuscript_claims.py`.

**Planning and blocker inputs:**
- Project state and requirements: `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, `.planning/STATE.md`, and `.planning/research/SUMMARY.md`.
- Case-study scaffolds consumed by Phase 10 packaging: `.planning/data/case_studies/`.
- Planning blockers consumed by Phase 10 packaging: `.planning/results/`.

**Manuscript and references:**
- Manuscript source: `manuscript/main.tex`.
- Bibliography: `manuscript/references.bib`.
- Elsevier CAS class/template files: `manuscript/els-cas-dc.cls` and `manuscript/b-els-cas-templates-模版/`.
- Literature/reference PDFs and notes: `paper/`.
- Current Python builders emit paper-facing `.tex`, Markdown, JSON, CSV, and PNG artifacts; they do not invoke an external LaTeX compiler.

## Authentication & Identity

**Auth Provider:**
- Not detected.
  - Implementation: not applicable.

**Secrets:**
- No `.env` files are present at the repository root or under `work2_coding/`.
- No required API keys, tokens, database URLs, or webhook secrets are detected in the active runtime source.

## Monitoring & Observability

**Error Tracking:**
- None. No Sentry, OpenTelemetry, cloud logging, metrics service, or hosted observability integration is detected.

**Logs:**
- Local stdout/file logging through `Logger` in `work2_coding/Src/Utils/Utils.py`.
- Runtime logs are written under `work2_coding/Experiments/Parcelpoint_py/.../logs/logfile.log` by `work2_coding/Src/config.py`.
- Study summaries and blockers are written as JSON under `work2_coding/outputs/studies/<study>/<run_id>/`.
- Artifact/readiness status is written as JSON and Markdown under `work2_coding/artifacts/`, `artifacts/`, and `work2_coding/outputs/formal_readiness/`.

## CI/CD & Deployment

**Hosting:**
- None. This is an offline research repository, not a deployed application.

**CI Pipeline:**
- Not detected. There is no `.github/workflows/`, CI config, or deployment manifest in the current repository root.

**Release/Delivery Artifact:**
- Paper-facing delivery is the generated artifact package under `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/` and the mirror under `artifacts/work2_robust_menu/phase10_paper_artifacts/`.

## Environment Configuration

**Required env vars:**
- None detected.

**Secrets location:**
- Not applicable. Do not introduce secret-backed integrations unless the project requirements explicitly change.

**Runtime configuration files:**
- Dependency list: `work2_coding/requirements.txt`.
- Study manifests: `work2_coding/Experiments/studies/*.yaml`.
- Suite manifests: `work2_coding/Experiments/suites/*.yaml`.
- Per-run runtime snapshot: `work2_coding/Experiments/Parcelpoint_py/.../args.yaml`.
- Formal readiness snapshot: `work2_coding/outputs/formal_readiness/<study>/FORMAL_READINESS.json`.

## Webhooks & Callbacks

**Incoming:**
- None detected.

**Outgoing:**
- None detected.

## External Command-Line and Runtime Dependencies

**Python:**
- Required for all runtime, study, readiness, and artifact scripts.
- Active working directory should be `work2_coding/` for command execution unless a script explicitly accepts repository-root paths.

**Git:**
- Used by `work2_coding/Src/study_execution.py` and `work2_coding/Src/formal_readiness.py` to collect commit SHA and dirty-state metadata.
- Formal readiness treats dirty Git state as a blocker unless the relevant diagnostic/override flag is used.

**pip:**
- Used through `python -m pip freeze` by `work2_coding/Src/artifact_status.py` and `work2_coding/Src/formal_readiness.py` for dependency snapshots.

**LaTeX compiler:**
- Optional external dependency for manual manuscript compilation of `manuscript/main.tex`.
- Not invoked by current Python artifact scripts.

## Integration Contracts and Guardrails

**Paired replay fairness:**
- Preserve stable paired fields in study manifests under `work2_coding/Experiments/studies/*.yaml`.
- Validation lives in `work2_coding/Src/paired_replay.py` and `work2_coding/Src/experiment_contracts.py`.

**Opt-out accounting:**
- Keep outside-option opt-out separate from accepted home pickup and accepted meeting-point service.
- Accounting lives in `work2_coding/Environments/OOH/customerchoice.py`, `work2_coding/Environments/OOH/Parcelpoint_py.py`, and normalized row fields in `work2_coding/Src/paired_replay.py`.

**Checkpoint metadata:**
- Preserve explicit checkpoint load status and hash fields in all study rows and artifact metadata.
- Contract fields are generated by `work2_coding/Src/study_execution.py` and checked by `work2_coding/Src/artifact_status.py`.

**No-filter status:**
- Treat no-filter runs as diagnostic unless a formal readiness and artifact-status gate explicitly supports claim-ready use.
- `work2_coding/Src/artifact_status.py` classifies no-filter-only artifacts as diagnostic.

**Attention scope:**
- Attention-based choice/scoring is outside v1 claim scope.
- Attention CLI options exist in `work2_coding/Src/parser.py`, but `work2_coding/Src/manuscript_claims.py` blocks ungated DSPO_PLUS/attention ranking claims.

**Generated artifacts:**
- Do not hand-edit generated result rows or paper artifacts.
- Regenerate `normalized_rows.json`, `normalized_rows.csv`, `PACKAGE_INDEX.json`, `PACKAGE_STATUS.json`, `CLAIM_GUARD.json`, tables, figures, and manuscript frames through scripts in `work2_coding/scripts/`.

---

*Integration audit: 2026-06-16*
