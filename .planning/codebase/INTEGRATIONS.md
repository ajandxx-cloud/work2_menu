# External Integrations

**Analysis Date:** 2026-05-27

## APIs & External Services

**Hosted APIs:**
- Not detected - No code imports or references to hosted SDKs such as OpenAI, Stripe, Supabase, Firebase, AWS, Redis, PostgreSQL, MySQL, or HTTP client libraries were found under `ooh_code/`.
  - SDK/Client: Not applicable
  - Auth: Not applicable

**Local Scientific Libraries:**
- Hygese HGS solver - Used for route optimization and final route recovery in `ooh_code/Src/Algorithms/DSPO.py` and `ooh_code/Environments/OOH/env_utils.py`.
  - SDK/Client: `hygese` package from `ooh_code/requirements.txt`
  - Auth: None
- PyTorch - Used for local model training, inference, and checkpoint files in `ooh_code/Src/Algorithms/DSPO.py`, `ooh_code/Src/Algorithms/DSPO_Menu.py`, and `ooh_code/Src/Utils/Predictors.py`.
  - SDK/Client: `torch` package from `ooh_code/requirements.txt`
  - Auth: None
- Matplotlib - Used for local publication figure generation in `ooh_code/scripts/build_artifacts.py` and training plots in `ooh_code/Src/Utils/Utils.py`.
  - SDK/Client: `matplotlib` package from `ooh_code/requirements.txt`
  - Auth: None

**Local Executables:**
- Git - Optional executable used by `ooh_code/Src/research_pipeline.py` to produce a short code-version marker.
  - SDK/Client: `subprocess.run(["git", "rev-parse", "--short", "HEAD"])`
  - Auth: None
- LaTeX toolchain - Optional manuscript compiler used by `ooh_code/scripts/build_manuscript.py`.
  - SDK/Client: `latexmk`, `pdflatex`, and optional `bibtex` executables
  - Auth: None

## Data Storage

**Databases:**
- Not detected.
  - Connection: Not applicable
  - Client: Not applicable

**File Storage:**
- Local filesystem only.
- Bundled benchmark inputs:
  - `ooh_code/Environments/OOH/HombergerGehring_data/` - Synthetic C/R/RC coordinate files; Euclidean travel times are derived by `ooh_code/Src/Utils/Utils.py`.
  - `ooh_code/Environments/OOH/Amazon_data/` - Austin and Seattle coordinate, distance-matrix, and adjacency files loaded by `ooh_code/Src/Utils/Utils.py`.
- Study manifests:
  - `ooh_code/experiments/studies/*.yaml` - Single executable studies loaded by `ooh_code/Src/research_pipeline.py`.
  - `ooh_code/experiments/suites/*.yaml` - Paper study suites loaded by `ooh_code/Src/research_pipeline.py`.
- Raw run outputs:
  - `ooh_code/outputs/studies/<study_name>/<run_id>/` - Study summaries, split outputs, manifest snapshots, and variant metrics.
  - `ooh_code/outputs/shared_training/<run_name>/<seed>/` - Shared training checkpoints, logs, and results created by `ooh_code/Src/config.py`.
  - `ooh_code/outputs/menu_compare/` and `ooh_code/outputs/phase*/` - Local analysis and extraction outputs used by support scripts such as `ooh_code/scripts/bootstrap_rc.py` and `ooh_code/scripts/bootstrap_amazon.py`.
- Committed lightweight artifacts:
  - `ooh_code/artifacts/results_snapshot/` - Compact JSON/CSV snapshots.
  - `ooh_code/artifacts/tables/` - CSV and LaTeX tables.
  - `ooh_code/artifacts/figures/` - PNG publication figures.
  - `ooh_code/artifacts/RESULTS_SUMMARY.md` - Prose summary.
- Manuscript assets:
  - `ooh_code/manuscript/main.tex`, `ooh_code/manuscript/sections/*.tex`, `ooh_code/manuscript/references.bib`, and `ooh_code/manuscript/main.pdf`.
  - `ooh_code/manuscript/build/` - Generated build metadata and compiled PDF output when present; ignored by `ooh_code/.gitignore`.

**Caching:**
- Local checkpoint reuse only.
- `ooh_code/Src/config.py` creates `ooh_code/outputs/shared_training/<run_name>/<seed>/checkpoints/` for model checkpoints.
- `ooh_code/Src/research_pipeline.py` supports shared checkpoint paths and resumable study runs under `ooh_code/outputs/studies/`.
- No Redis, Memcached, remote object cache, or HTTP cache was detected.

## Authentication & Identity

**Auth Provider:**
- None.
  - Implementation: The codebase is an offline research workflow with no user accounts, sessions, OAuth, API keys, or secret-managed credentials.

## Monitoring & Observability

**Error Tracking:**
- None. No Sentry, OpenTelemetry, hosted error tracking, or remote observability SDK was detected.

**Logs:**
- Local file/stdout logging.
- `ooh_code/Src/Utils/Utils.py` defines `Logger`, which mirrors stdout to `logfile.log` under `ooh_code/outputs/shared_training/<run_name>/<seed>/logs/`.
- CLI scripts print progress to stdout in `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, `ooh_code/scripts/build_manuscript.py`, `ooh_code/scripts/bootstrap_rc.py`, and `ooh_code/scripts/bootstrap_amazon.py`.
- Manuscript build metadata is written to `ooh_code/manuscript/build/build_status.json` by `ooh_code/scripts/build_manuscript.py`.

## CI/CD & Deployment

**Hosting:**
- Not applicable. No web app, service deployment target, container image, or hosting configuration was detected.

**CI Pipeline:**
- None detected. No GitHub Actions, GitLab CI, Azure Pipelines, CircleCI, Dockerfile, or Compose configuration was found in the workspace scan.

## Environment Configuration

**Required env vars:**
- None detected.

**Secrets location:**
- Not detected.
- No `.env`, `.env.*`, credential, certificate, package-manager token, or cloud service-account files were detected during the scan.
- Do not add secrets to study manifests or committed artifact files; configuration currently stays in CLI flags, YAML manifests, and local output snapshots.

## Webhooks & Callbacks

**Incoming:**
- None. No server, HTTP routes, webhook handlers, or callback endpoints were detected.

**Outgoing:**
- None. No outgoing webhook clients, HTTP POST calls, message queues, or cloud events were detected.

---

*Integration audit: 2026-05-27*
