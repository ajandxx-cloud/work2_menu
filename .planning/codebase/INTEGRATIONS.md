# External Integrations

**Analysis Date:** 2026-06-09
**last_mapped_commit:** `37b20aa`

## APIs & External Services

**HTTP/Cloud APIs:**
- Not detected. No `requests`, `httpx`, `urllib`, `boto`, `stripe`, `supabase`, `openai`, or equivalent external API client usage is present in `ooh_code/**/*.py`.

**Routing Solver Backend:**
- Hygese HGS solver - Used for CVRP route-cost evaluation and route recovery.
  - SDK/Client: `hygese~=0.0.0.8` from `ooh_code/requirements.txt`.
  - Auth: Not applicable.
  - Implementation: `ooh_code/Environments/OOH/env_utils.py` imports `AlgorithmParameters` and `Solver`, initializes `Solver(parameters=ap, verbose=False)`, and calls `solve_cvrp`.
  - Implementation: `ooh_code/Src/Algorithms/DSPO.py` imports `AlgorithmParameters` and `Solver` for algorithm-level route evaluation.
  - Runtime knobs: `--hgs_reopt_time`, `--hgs_final_time`, and `--reopt` are defined in `ooh_code/Src/parser.py`.

**Scientific Math Backend:**
- Optional SciPy Lambert W - Used only when installed for the pricing transform.
  - SDK/Client: `scipy.special.lambertw`.
  - Auth: Not applicable.
  - Implementation: `ooh_code/Src/Utils/MathUtils.py` imports SciPy inside `lambertw()` and falls back to `_lambertw_principal_real()` when SciPy is unavailable.
  - Pricing consumers: `ooh_code/Src/Algorithms/DSPO.py` and menu pricing options in `ooh_code/Src/parser.py`.

**Local Toolchain Integrations:**
- Git CLI - Used to stamp experiment metadata with the current short commit.
  - SDK/Client: external `git` executable through `subprocess.run`.
  - Auth: Not applicable for the local `git rev-parse --short HEAD` call.
  - Implementation: `ooh_code/Src/research_pipeline.py` implements `detect_code_version_marker()`.
- LaTeX CLI - Used to compile the manuscript.
  - SDK/Client: external `latexmk`, `pdflatex`, and optional `bibtex` executables.
  - Auth: Not applicable.
  - Implementation: `ooh_code/scripts/build_manuscript.py` implements `detect_compiler()`, `compile_with_latexmk()`, and `compile_with_pdflatex()`.

## Data Storage

**Databases:**
- Not detected. No relational database, NoSQL database, ORM, SQL client, or database connection string usage was found in `ooh_code/**/*.py`.
  - Connection: Not applicable.
  - Client: Not applicable.

**File Storage:**
- Local filesystem only.
  - Bundled benchmark data: `ooh_code/Environments/OOH/HombergerGehring_data/` and `ooh_code/Environments/OOH/Amazon_data/`.
  - Raw run outputs: `ooh_code/outputs/studies/`, `ooh_code/outputs/shared_training/`, and `ooh_code/outputs/menu_compare/`.
  - Committed artifacts: `ooh_code/artifacts/results_snapshot/`, `ooh_code/artifacts/tables/`, `ooh_code/artifacts/figures/`, and root `artifacts/work2_cnn_setmenunet/`.
  - Manuscript build outputs: `ooh_code/manuscript/build/`.

**Caching:**
- Local checkpoint reuse only.
  - Shared predictor checkpoints are stored under `ooh_code/outputs/shared_training/`.
  - `ooh_code/Src/research_pipeline.py` reuses `supervised_ml.pt` through `train_or_reuse_shared_model()`.
  - `ooh_code/run_menu_compare.py` accepts `--shared_checkpoint_path` and `--skip_train` for checkpoint-backed evaluation.

## Authentication & Identity

**Auth Provider:**
- Not detected.
  - Implementation: No login, session, API key, OAuth, token validation, user model, or identity provider integration exists in the runnable research code under `ooh_code/`.

## Monitoring & Observability

**Error Tracking:**
- None.

**Logs:**
- Local file and terminal logging through `Utils.Logger` in `ooh_code/Src/Utils/Utils.py`.
- `ooh_code/Src/config.py` redirects `sys.stdout` to `Utils.Logger` and writes logs under each run's `logs/logfile.log`.
- Workflow status is printed by CLIs such as `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, and `ooh_code/scripts/build_manuscript.py`.
- Machine-readable observability comes from JSON/CSV outputs written by `ooh_code/Src/research_pipeline.py` and `ooh_code/run_menu_compare.py`.

## CI/CD & Deployment

**Hosting:**
- Not applicable. The project is a local/offline research codebase, not a deployed service.

**CI Pipeline:**
- Not detected. No GitHub Actions workflow, GitLab CI, Azure Pipelines, or equivalent CI configuration was found in the explored repository.
- Local validation uses script-style tests under `ooh_code/scripts/test_*.py` and smoke studies such as `ooh_code/experiments/studies/smoke_rc.yaml`.

## Environment Configuration

**Required env vars:**
- Not detected.

**Secrets location:**
- Not applicable. No `.env` files were detected in the repository root or `ooh_code/`, and no secret/config credential files were read or required.

**Runtime configuration files:**
- Dependency manifest: `ooh_code/requirements.txt`.
- CLI argument schema: `ooh_code/Src/parser.py`.
- Study manifests: `ooh_code/experiments/studies/*.yaml`.
- Suite manifests: `ooh_code/experiments/suites/*.yaml`.
- Manuscript and artifact workflow docs: `ooh_code/README.md`, `ooh_code/experiments/README.md`, and `ooh_code/manuscript/README.md`.

## Webhooks & Callbacks

**Incoming:**
- None.

**Outgoing:**
- None.

## Integration Boundaries

**Do not introduce cloud dependencies for core experiments:**
- Keep experiment execution reproducible from local manifests in `ooh_code/experiments/studies/*.yaml` and `ooh_code/experiments/suites/*.yaml`.
- Keep route-cost feedback on the existing Hygese backend in `ooh_code/Environments/OOH/env_utils.py` and `ooh_code/Src/Algorithms/DSPO.py`.
- Keep pricing on the implemented Lambert-W/cost-plus/flat-markdown modes exposed by `ooh_code/Src/parser.py` unless a phase explicitly changes the pricing backend.

**Do not store generated evidence by hand:**
- Write raw outputs through `ooh_code/Src/research_pipeline.py` into `ooh_code/outputs/`.
- Regenerate committed snapshots, LaTeX tables, and figures with `ooh_code/scripts/build_artifacts.py`.
- Compile or prepare manuscript artifacts through `ooh_code/scripts/build_manuscript.py`.

---

*Integration audit: 2026-06-09*
