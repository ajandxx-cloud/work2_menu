# Concerns

**Analysis Date:** 2026-05-27

## Executive Summary

This is a publication-oriented research codebase, so the highest risks are not typical web-app failures. The important failure mode is scientific drift: experiments, generated artifacts, and manuscript claims can fall out of sync while still producing plausible-looking tables and prose.

The code already contains useful safeguards: versioned YAML manifests, shared-predictor evaluation, replayed request traces, manifest hashes, checkpoint metadata, and explicit implementation-boundary documents. Future work should preserve those contracts and add lightweight verification around them rather than treating the repository like a generic Python package.

## High-Priority Concerns

### Experiment Contract Drift

**Files:**
- `ooh_code/Src/research_pipeline.py`
- `ooh_code/run_menu_compare.py`
- `ooh_code/experiments/studies/*.yaml`
- `ooh_code/experiments/suites/*.yaml`

The central fairness contract is: train or reuse one shared predictor, freeze learning, replay identical request traces, then vary only the display policy. This is documented in `ooh_code/docs/WORK2_EXPERIMENT_PROTOCOL.md` and implemented through `train_or_reuse_shared_model`, `generate_request_traces`, and `evaluate_policy` in `ooh_code/Src/research_pipeline.py`.

Risk points:
- A new study manifest can accidentally change base args between variants.
- `reuse_existing=True` can reuse an old checkpoint if the expected file exists.
- Request traces are generated from `trace_seed`, but downstream policy changes depend on all solver/environment state staying comparable.
- Low-level `ooh_code/run_menu_compare.py` and project-level `ooh_code/Src/research_pipeline.py` are parallel entry paths, so changes to one path can leave the other semantically behind.

Mitigation:
- Add a manifest validation check that diffs variant args and explicitly allows only known policy/treatment keys.
- Record the checkpoint code marker, manifest hash, and relevant config snapshot in every generated comparison row.
- Run a smoke study after changes to `ooh_code/Src/config.py`, `ooh_code/Src/parser.py`, `ooh_code/Src/research_pipeline.py`, `ooh_code/run_menu_compare.py`, or `ooh_code/Src/Algorithms/DSPO_Menu.py`.

### Artifact and Manuscript Synchronization

**Files:**
- `ooh_code/scripts/build_artifacts.py`
- `ooh_code/scripts/build_manuscript.py`
- `ooh_code/artifacts/`
- `ooh_code/manuscript/main.tex`
- `ooh_code/manuscript/sections/*.tex`

The repository commits generated tables, figures, result snapshots, and a manuscript PDF. That is useful for publication work, but it creates a synchronization hazard: text in `ooh_code/manuscript/sections/*.tex` can cite results that no longer match the latest normalized outputs or generated tables.

Risk points:
- `ooh_code/artifacts/RESULTS_SUMMARY.md` currently reflects a requested scope, not necessarily the whole manuscript evidence base.
- `ooh_code/scripts/build_manuscript.py --skip_compile` refreshes inputs without proving that LaTeX still compiles.
- Missing LaTeX tooling is handled explicitly, but compilation success is not a substitute for scientific consistency.

Mitigation:
- Before manuscript edits, rebuild artifacts with the intended study or suite, then build the manuscript.
- Add a small claim-audit checklist for tables referenced by `\ArtifactTable{...}` in `ooh_code/manuscript/sections/*.tex`.
- Treat `ooh_code/artifacts/` as generated output unless a script or README says otherwise.

### Calibration and Interpretation Boundaries

**Files:**
- `ooh_code/docs/WORK2_IMPLEMENTATION_BOUNDARIES.md`
- `ooh_code/manuscript/sections/limitations.tex`
- `ooh_code/manuscript/sections/experiments.tex`
- `ooh_code/Src/Algorithms/DSPO_Menu.py`

The paper's interpretation depends on fixed simulator parameters, MNL choice behavior, uptake regimes, and ETA approximation choices. These are valid research assumptions, but they are easy to overstate as empirical validation.

Risk points:
- `DSPO_Menu` uses fixed or configured values for price sensitivity, ETA filtering, time prediction blend, route-delay penalties, and exact/greedy thresholds.
- `DSPO_Menu._eta_sigma` is hardcoded as an empirical ETA MAE constant.
- The manuscript already notes that MNL parameters are design choices rather than passenger-estimated values; future edits must preserve this nuance.

Mitigation:
- Keep calibration language in `ooh_code/manuscript/sections/limitations.tex` synchronized with the actual flags in `ooh_code/Src/parser.py`.
- When changing ETA, pricing, or utility parameters, update both experiment manifests and boundary documentation.
- Prefer wording such as "mechanism evidence", "behavioral stress test", and "descriptive external check" where the current evidence hierarchy requires it.

## Medium-Priority Concerns

### Broad Exception Handling Can Hide Data Issues

**Files:**
- `ooh_code/run_menu_compare.py`
- `ooh_code/Src/research_pipeline.py`
- `ooh_code/scripts/extract_phase8_results.py`
- `ooh_code/scripts/extract_phase9_results.py`

Several scripts intentionally continue when optional artifacts are missing. That is reasonable for exploratory paper workflows, but it can hide malformed summaries, missing variants, or stale outputs.

Examples:
- `ooh_code/run_menu_compare.py` ignores errors while restoring stdout/log handles.
- `ooh_code/Src/research_pipeline.py` continues when reading candidate resume metadata fails.
- Phase extraction scripts often print warnings and continue with partial payloads.

Mitigation:
- Keep "partial evidence" outputs explicit, as in `ooh_code/scripts/extract_phase27_results.py`.
- For headline studies, fail closed when required variants or metrics are absent.
- Distinguish optional development diagnostics from manuscript-critical evidence in script output.

### No Conventional Automated Test Suite

**Files:**
- `ooh_code/experiments/studies/smoke_rc.yaml`
- `ooh_code/experiments/studies/smoke_austin.yaml`
- `ooh_code/scripts/run_study.py`
- `ooh_code/scripts/build_artifacts.py`
- `ooh_code/scripts/check_manuscript.py`

No `pytest`, `unittest`, CI workflow, or dedicated test directory was detected. Verification is currently study-driven and artifact-driven.

Mitigation:
- Use smoke studies as the minimum regression check after code changes.
- Add small unit tests only around high-leverage pure functions first: manifest loading, row normalization, paired summary math, pricing transforms, and fallback Lambert W.
- Add a manuscript smoke check that verifies referenced generated artifact files exist.

### Dependency and Runtime Reproducibility

**Files:**
- `ooh_code/requirements.txt`
- `ooh_code/Environments/OOH/env_utils.py`
- `ooh_code/Environments/OOH/Parcelpoint_py.py`
- `ooh_code/Src/Utils/MathUtils.py`

Dependencies are version-constrained but not locked. `hygese` is a critical solver dependency, PyTorch behavior can vary across CPU/GPU/runtime versions, and SciPy is optional for Lambert W.

Mitigation:
- Record Python, torch, numpy, hygese, and optional scipy versions in run metadata.
- Be cautious comparing results across machines without a version snapshot.
- Preserve the internal Lambert W fallback behavior if SciPy remains optional.

### Encoding and Filename Portability

**Files:**
- Root-level Chinese notes such as `实验讨论5.26.md`
- Literature folders such as `2025.9.11-pom_big price/`
- Generated `.planning/codebase/*.md`

This workspace uses Chinese filenames and mixed publication notes outside `ooh_code/`. Some terminal output displayed mojibake during mapping, which means tools may disagree about encoding even when the files are valid.

Mitigation:
- Keep executable paths inside `ooh_code/` ASCII-oriented where possible.
- Use UTF-8 explicitly when reading/writing research notes or manuscript text.
- Avoid relying on rendered terminal output for Chinese filenames; use filesystem paths directly.

## Scientific-Core Hotspots

### Menu Construction and Pricing

**File:** `ooh_code/Src/Algorithms/DSPO_Menu.py`

This file is the densest scientific hotspot. It owns candidate generation, ETA filtering, price assignment, exact/greedy selection, heuristic baselines, metadata logging, and training-target updates.

Change risk:
- Small edits can change both mechanism diagnostics and headline results.
- Some methods use metadata fields set by earlier methods; missing metadata may silently change downstream summaries.
- Random baseline behavior in `random_top_k` uses Python's `random` module, so reproducibility should be checked if that baseline becomes manuscript-critical.

Recommended guard:
- For every change here, run at least `python scripts/run_study.py --study smoke_rc` from `ooh_code/`.
- For ETA or pricing changes, rerun the specific mechanism study that the manuscript uses for that claim.

### Simulator Coupling

**Files:**
- `ooh_code/Environments/OOH/Parcelpoint_py.py`
- `ooh_code/Environments/OOH/customerchoice.py`
- `ooh_code/Environments/OOH/containers.py`

The algorithm and simulator communicate through menu offers, selected offers, and metadata. `DSPO_Menu.update()` expects `env.last_selected_offer` to be populated, so environment changes can break model updates even if the runner still executes.

Recommended guard:
- Check that selected-offer metadata survives from menu construction through choice logging and normalized row aggregation.
- Preserve outside-option semantics when changing choice logic.

### Study Pipeline and Resume Logic

**File:** `ooh_code/Src/research_pipeline.py`

The pipeline supports resumable runs, checkpoint reuse, suite execution, manifest snapshots, and normalized row output. This makes it powerful but raises stale-output risk.

Recommended guard:
- Use force/retrain flags when a change affects model behavior.
- Treat resumed runs as suspect after changes to parser defaults, data loading, menu policies, or metric computation.

## Security and Privacy

No obvious credential-handling code, external write API, authentication provider, or secret-bearing config was identified in the research project. The main privacy/security concern is accidental publication of local paths, intermediate outputs, or non-public notes.

Potential exposure points:
- Generated artifacts can include absolute or local checkpoint paths if not sanitized.
- Publication notes and PDF literature outside `ooh_code/` may not be intended for repository publication.
- `outputs/studies/` can be large and may include raw traces or metadata not meant for a paper artifact package.

Mitigation:
- Before sharing, inspect `ooh_code/outputs/`, `.planning/`, and root-level notes separately from the public `ooh_code/` package.
- Prefer committed snapshots under `ooh_code/artifacts/` over raw run directories when packaging.

## Maintenance Recommendations

1. Preserve the documented research contract before optimizing code structure.
2. Add validation around manifests and required headline variants.
3. Add small automated checks for artifact/manuscript references.
4. Keep `ooh_code/docs/WORK2_IMPLEMENTATION_BOUNDARIES.md` current whenever simulator or menu semantics change.
5. Use smoke studies as the default regression test for scientific changes.

---
*Last mapped: 2026-05-27*
