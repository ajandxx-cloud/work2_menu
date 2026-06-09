# Codebase Concerns

**Analysis Date:** 2026-06-09
**last_mapped_commit:** `37b20aa`

## Tech Debt

**Missing core menu algorithm module:**
- Issue: The default algorithm import target is absent from the current worktree. `ooh_code/Src/config.py` imports `Src.Algorithms.DSPO_Menu`, and the default parser value routes `--menu_model cnn_2d` to `DSPO_Menu`, but `ooh_code/Src/Algorithms/DSPO_Menu.py` is not present.
- Files: `ooh_code/Src/config.py`, `ooh_code/Src/parser.py`, `ooh_code/Src/Algorithms/CNN_SetMenu.py`, `ooh_code/Src/Algorithms/MLP_SetMenu.py`, `ooh_code/scripts/test_menu_objective_mode.py`, `ooh_code/scripts/test_phase6_redesign_policies.py`
- Impact: `import Src.config` fails with `ModuleNotFoundError: No module named 'Src.Algorithms.DSPO_Menu'`; study execution, smoke tests, artifact gates that import the pipeline, and all CNN/MLP menu variants are blocked.
- Fix approach: Restore or replace `ooh_code/Src/Algorithms/DSPO_Menu.py` before running any experiments. After restoration, run at minimum `python ooh_code/scripts/run_study.py --study smoke_rc --force_retrain` from `ooh_code/` plus the policy/unit smoke scripts that import `DSPO_Menu`.

**Monolithic artifact builder:**
- Issue: `ooh_code/scripts/build_artifacts.py` is a single large script that mixes data loading, classification, figure generation, LaTeX table rendering, Work2 formal summaries, robustness summaries, placeholder figures, and prose generation.
- Files: `ooh_code/scripts/build_artifacts.py`
- Impact: Changes to one artifact family can affect unrelated manuscript outputs. It is difficult to isolate tests, reason about fallback behavior, or review scientific claim wording independently from plotting/table code.
- Fix approach: Split by artifact family into small modules under `ooh_code/scripts/` or a package such as `ooh_code/Src/artifacts/`; keep `build_artifacts.py` as a thin CLI orchestrator.

**Silent checkpoint/model mismatch handling:**
- Issue: `Agent.load()` catches all exceptions from module loading and silently keeps random initialization when checkpoint files are missing or incompatible.
- Files: `ooh_code/Src/Algorithms/Agent.py`, `ooh_code/Src/work2_runtime.py`, `ooh_code/run_menu_compare.py`, `ooh_code/Src/research_pipeline.py`
- Impact: A run can report a checkpoint path while a variant evaluates with randomly initialized heads, especially across `cnn_2d`, `cnn_setmenu`, and `mlp_menu` model changes. This weakens scientific traceability of learned-baseline comparisons.
- Fix approach: Replace the blanket `except (RuntimeError, Exception): pass` with explicit compatibility checks and a structured `checkpoint_load_status` written into normalized rows. Fail closed for default/shared predictor loads unless the manifest marks a model-architecture mismatch as intentional.

**Legacy and new naming styles are tightly coupled:**
- Issue: New orchestration code uses snake_case helpers while the simulator and containers preserve legacy attribute names such as `remainingCapacity`, `routePlan`, `newCustomer`, and `customerChoice`.
- Files: `ooh_code/Environments/OOH/containers.py`, `ooh_code/Environments/OOH/Parcelpoint_py.py`, `ooh_code/Environments/OOH/env_utils.py`, `ooh_code/run_menu_compare.py`
- Impact: New code can accidentally mix dict access, object attributes, and legacy camelCase names. Bugs in route mutation or capacity accounting are hard to catch because the same objects are passed through environment, HGS, logging, and metric extraction layers.
- Fix approach: Add adapter helpers for route and capacity access in `ooh_code/Environments/OOH/env_utils.py` and use them from new code; do not introduce additional direct `routePlan` or `remainingCapacity` accesses outside the simulator layer.

**Many phase-specific scripts duplicate artifact gates:**
- Issue: Multiple phase scripts implement similar row loading, gate errors, metric coercion, manifest snapshot handling, and Markdown output logic.
- Files: `ooh_code/scripts/build_phase08_artifacts.py`, `ooh_code/scripts/build_phase08_gap_closure_artifacts.py`, `ooh_code/scripts/build_phase6_redesign_artifacts.py`, `ooh_code/scripts/build_work2_phase6_redesign_formal_artifacts.py`, `ooh_code/scripts/build_work2_phase6b_repaired_contract.py`, `ooh_code/scripts/diagnose_work2_phase6_primary_metric.py`
- Impact: Gate semantics can drift across phases. A metric accepted by one artifact script can be rejected, reclassified, or described differently by another.
- Fix approach: Move shared row validation, metric coercion, gate-state classification, and output-directory safety checks into reusable helpers, then keep phase scripts as thin configurations.

## Known Bugs

**Project import is currently broken:**
- Symptoms: Running `python -c "import sys; sys.path.insert(0, 'ooh_code'); import Src.config"` fails with `ModuleNotFoundError`.
- Files: `ooh_code/Src/config.py`, `ooh_code/Src/Algorithms/DSPO_Menu.py`
- Trigger: Any command that imports `Src.config`, including `ooh_code/scripts/run_study.py`, `ooh_code/scripts/build_artifacts.py`, and direct use of `ooh_code/run_menu_compare.py`.
- Workaround: None in the current tree. Restore `ooh_code/Src/Algorithms/DSPO_Menu.py` or update every importer and manifest that assumes `DSPO_Menu`.

**Outside-option choice is logged through a home-offer fallback:**
- Symptoms: When the outside option is chosen, `customerchoice_menu()` returns the home location and a home offer tagged with `metadata["opted_out"] = True`; `Parcelpoint_py.step()` then appends that home location to routing data and home-delivery service accounting.
- Files: `ooh_code/Environments/OOH/customerchoice.py`, `ooh_code/Environments/OOH/Parcelpoint_py.py`, `ooh_code/run_menu_compare.py`
- Trigger: Any menu episode where the MNL draw selects the outside option.
- Workaround: Metric extraction reads `menu_log["opted_out"]`, but routing and service-time side effects still include the fallback location. Separate outside-option state transitions from accepted home-delivery state transitions before using opt-out runs as formal route-cost evidence.

**Mojibake appears in source comments:**
- Symptoms: Comments contain corrupted characters in source text.
- Files: `ooh_code/Src/Algorithms/Agent.py`, `ooh_code/Environments/OOH/customerchoice.py`
- Trigger: Opening or editing affected files with the wrong encoding, or regenerating comments from already-corrupted text.
- Workaround: Use UTF-8 consistently and repair comments in-place when touching the affected files. Do not use corrupted comments as manuscript text.

## Security Considerations

**Unsafe checkpoint deserialization path:**
- Risk: Several predictor `load()` methods call `torch.load(..., map_location='cpu')` without `weights_only=True`.
- Files: `ooh_code/Src/Utils/Predictors.py`, `ooh_code/Src/Algorithms/Agent.py`, `ooh_code/Src/work2_runtime.py`
- Current mitigation: Some newer set-menu utilities use `weights_only=True`, but the default `CNN_2d` and `LinReg` loaders do not.
- Recommendations: Use `torch.load(filename, map_location='cpu', weights_only=True)` where supported, and load checkpoints only from trusted local experiment output directories. Record checkpoint file hashes in normalized study metadata for formal runs.

**No secret-management surface detected:**
- Risk: Not applicable for external API credentials. No `.env` files were detected at the repository root or under `ooh_code/`, and keyword search did not find credential variables.
- Files: `ooh_code/.gitignore`, `ooh_code/Src/research_pipeline.py`, `ooh_code/scripts/build_manuscript.py`
- Current mitigation: Runtime configuration is CLI/YAML based and output paths are local.
- Recommendations: Keep generated credentials, if any are added later, out of manifests and out of committed artifacts. Extend `ooh_code/.gitignore` before adding any service integration.

**Subprocess calls are local tooling only:**
- Risk: LaTeX and Git subprocesses execute local binaries. They do not use `shell=True`, but they still depend on the local toolchain and local manuscript inputs.
- Files: `ooh_code/Src/research_pipeline.py`, `ooh_code/scripts/build_manuscript.py`, `ooh_code/scripts/run_work2_robustness_closure.py`, `ooh_code/scripts/test_work2_no_paper_changes.py`
- Current mitigation: Commands are passed as argument lists, not shell strings.
- Recommendations: Keep subprocess inputs as fixed command arrays. Do not pass manifest-controlled values into shell commands.

## Performance Bottlenecks

**HGS route optimization dominates runtime:**
- Problem: HGS is invoked during final evaluation and optionally during environment re-optimization; each solver has a time limit from parser settings.
- Files: `ooh_code/Src/Algorithms/DSPO.py`, `ooh_code/Environments/OOH/env_utils.py`, `ooh_code/Environments/OOH/Parcelpoint_py.py`, `ooh_code/Src/parser.py`
- Cause: `solve_cvrp()` is called for route-cost feedback and final costs, and the solver is configured with `hgs_reopt_time` / `hgs_final_time`.
- Improvement path: Keep smoke and pilot manifests with short HGS limits. For formal runs, report HGS timing and fixed solver parameters in run metadata, and cache deterministic route evaluations only when the full route input and solver parameters match.

**Exact menu enumeration can grow combinatorially:**
- Problem: Exact subset enumeration is configured for small candidate sets, with greedy fallback controlled by parser settings.
- Files: `ooh_code/Src/parser.py`, `ooh_code/scripts/test_phase6_redesign_policies.py`, `ooh_code/run_menu_compare.py`
- Cause: Menu policies compare subsets of feasible meeting-point offers; exact enumeration is only tractable for limited candidate counts.
- Improvement path: Keep `menu_exact_threshold` and `menu_exact_gap_threshold` low for pilots. Log candidate count, enumerated menu count, exact build time, greedy build time, and fallback status for every formal variant.

**Large scripts slow review and increase accidental rebuild cost:**
- Problem: Artifact generation and formal diagnostics run through scripts with hundreds to thousands of lines.
- Files: `ooh_code/scripts/build_artifacts.py`, `ooh_code/Src/research_pipeline.py`, `ooh_code/run_menu_compare.py`
- Cause: Data normalization, plotting, table generation, and text generation are not separated into smaller testable units.
- Improvement path: Extract pure aggregation and formatting helpers first; leave CLI behavior stable and add small tests for each extracted helper.

## Fragile Areas

**Experiment fairness depends on shared checkpoint reuse:**
- Files: `ooh_code/Src/research_pipeline.py`, `ooh_code/run_menu_compare.py`, `ooh_code/Src/work2_runtime.py`, `ooh_code/Src/Algorithms/Agent.py`
- Why fragile: The scientific comparison assumes one shared predictor and frozen policy variants, but checkpoint loading can silently fail and reuse decisions are path-based.
- Safe modification: Any change to training, checkpoint paths, `menu_model`, or `freeze_learning` must update normalized metadata and include a smoke run proving each variant loaded the intended weights.
- Test coverage: Existing scripts include manifest and gate tests under `ooh_code/scripts/test_*.py`, but no configured test runner or CI file is detected.

**Choice-model opt-out accounting affects both service and routing metrics:**
- Files: `ooh_code/Environments/OOH/customerchoice.py`, `ooh_code/Environments/OOH/Parcelpoint_py.py`, `ooh_code/run_menu_compare.py`
- Why fragile: Outside-option draws are represented as an opted-out home offer for update/logging compatibility. This is convenient for metrics but can contaminate route-cost feedback if treated as an accepted home pickup.
- Safe modification: Add explicit outcome states such as accepted-home, accepted-meeting-point, and opted-out. Keep `last_selected_offer` only for model update compatibility, and prevent opted-out requests from entering route data unless the scientific model intentionally penalizes them as service failures.
- Test coverage: Add a deterministic customer-choice test that forces outside option selection and asserts route data, service time, opt-out count, and `acceptance_rate`.

**Global RNG mutation in capacity selection:**
- Files: `ooh_code/Environments/OOH/env_utils.py`, `ooh_code/Src/config.py`, `ooh_code/Environments/OOH/Parcelpoint_py.py`
- Why fragile: `generate_fixed_list()` calls `np.random.seed(seed)` and `np.random.shuffle(array)`, mutating NumPy global RNG during environment construction.
- Safe modification: Use a local `np.random.RandomState(seed)` or `np.random.default_rng(seed)` inside `generate_fixed_list()` so constructing capacity masks does not affect training replay-buffer sampling or request generation.
- Test coverage: Add a repeatability test that constructs two environments and verifies subsequent global NumPy draws are unchanged by capacity-mask generation.

**Artifact placeholders can look like outputs:**
- Files: `ooh_code/scripts/build_artifacts.py`, `ooh_code/scripts/test_work2_robustness_artifacts.py`, `ooh_code/artifacts/figures/`, `ooh_code/artifacts/tables/`
- Why fragile: The artifact builder can render placeholder figures and rows such as no-data states. These are useful for manuscript assembly but risky if mistaken for completed evidence.
- Safe modification: Preserve explicit incomplete/status fields in every generated artifact and include source study run IDs. Formal manuscript inclusion should require completed study summaries and non-placeholder row counts.
- Test coverage: Robustness artifact tests cover incomplete dimensions, but add a top-level check that formal tables/figures cannot be generated from placeholder-only inputs.

**Generated outputs and committed artifacts have different trust levels:**
- Files: `ooh_code/outputs/`, `ooh_code/artifacts/results_snapshot/`, `ooh_code/artifacts/tables/`, `ooh_code/artifacts/figures/`, `ooh_code/.gitignore`
- Why fragile: Raw outputs are ignored, while lightweight snapshots are committed. Reviewers see committed artifacts but not the raw run directories unless they are preserved separately.
- Safe modification: Keep `manifest_hash`, `code_version_marker`, checkpoint provenance, run ID, and source output path in every committed snapshot. For formal evidence, archive the exact `ooh_code/outputs/studies/...` run directory outside git or provide a reproducible rerun manifest.
- Test coverage: Existing artifact tests inspect summaries, but formal reproducibility still depends on retaining raw outputs and checkpoint files.

## Scaling Limits

**Formal studies multiply by seeds, policies, traces, and HGS calls:**
- Current capacity: Study manifests include one-seed smokes, three-seed pilots, and five-seed formal designs under `ooh_code/experiments/studies/`.
- Limit: Runtime grows roughly with `splits * policies * eval_episodes * episode_length * route-solver cost`, and route-solver cost depends on HGS time limits.
- Scaling path: Keep suite manifests under `ooh_code/experiments/suites/` for batching, use resumable run IDs in `ooh_code/scripts/run_study.py`, and make checkpoint provenance mandatory when reusing shared training.

**Menu candidate tensor size is bounded by manifest/parser settings:**
- Current capacity: `max_candidates`, `menu_k`, `menu_exact_threshold`, and `menu_exact_gap_threshold` are parser-level controls in `ooh_code/Src/parser.py`.
- Limit: Learned set-menu models and exact policies become expensive as candidate count grows.
- Scaling path: Increase candidate pools only with explicit profiling rows for build time, enumerated menu count, memory use, and exact/greedy fallback rate.

## Dependencies at Risk

**`hygese~=0.0.0.8`:**
- Risk: The simulator warns that this package can assert on negative coordinates.
- Impact: Route optimization can fail for coordinate data that violates Hygese assumptions.
- Migration plan: Keep coordinate shifting in `ooh_code/Src/Utils/Utils.py` for Amazon instances, add a preflight data validation check, and document exact Hygese version and coordinate transform in formal run metadata.

**PyTorch checkpoint API:**
- Risk: Old-style `torch.load()` calls may become warning-prone or unsafe compared with `weights_only=True`.
- Impact: Checkpoint loading behavior can vary by PyTorch version and can carry deserialization risk for untrusted files.
- Migration plan: Update loaders in `ooh_code/Src/Utils/Predictors.py` and legacy model utilities to `weights_only=True`, with version-guarded fallback if required.

**No dependency lockfile:**
- Risk: `ooh_code/requirements.txt` pins broad versions but no lockfile is present.
- Impact: Reproduced formal runs can vary across dependency resolver dates, especially for PyTorch, NumPy, Matplotlib, and Hygese behavior.
- Migration plan: Generate and archive a lockfile or `pip freeze` snapshot for each formal evidence run, and write it under the run directory alongside `manifest_snapshot.yaml`.

## Missing Critical Features

**Configured automated test runner:**
- Problem: Test-like scripts exist under `ooh_code/scripts/test_*.py`, but no `pytest`, `unittest`, CI workflow, or test runner config is detected.
- Blocks: Fast regression checks for imports, parser/manifests, artifact gates, and opt-out accounting.

**Formal run provenance hard gate:**
- Problem: Normalized rows include provenance fields, but checkpoint load success, raw output retention, dependency snapshot, and source commit cleanliness are not enforced as a single formal gate.
- Blocks: Defensible TR Part E reproducibility when results are regenerated from manifests.

**Explicit outside-option transition model:**
- Problem: Opt-out is represented through metadata on a home offer.
- Blocks: Clean separation between passenger refusal, accepted home pickup, route cost, service penalty, and learning update semantics.

## Test Coverage Gaps

**Core import and smoke execution:**
- What's not tested: A single automated command that imports `Src.config`, constructs `Config`, and runs `smoke_rc`.
- Files: `ooh_code/Src/config.py`, `ooh_code/scripts/run_study.py`, `ooh_code/experiments/studies/smoke_rc.yaml`
- Risk: Missing modules or dependency regressions block all experiments before artifact tests run.
- Priority: High

**Checkpoint compatibility and load status:**
- What's not tested: Whether each variant actually loads intended checkpoint weights or intentionally starts with random/incompatible heads.
- Files: `ooh_code/Src/Algorithms/Agent.py`, `ooh_code/Src/work2_runtime.py`, `ooh_code/run_menu_compare.py`, `ooh_code/Src/research_pipeline.py`
- Risk: Learned baselines can be compared under different initialization conditions without visible row-level diagnostics.
- Priority: High

**Opt-out route-state semantics:**
- What's not tested: Deterministic outside-option choice behavior at the simulator transition level.
- Files: `ooh_code/Environments/OOH/customerchoice.py`, `ooh_code/Environments/OOH/Parcelpoint_py.py`, `ooh_code/run_menu_compare.py`
- Risk: Opt-out rates, route costs, adjusted profit, and service-constrained claims can diverge from the intended behavioral model.
- Priority: High

**Artifact placeholder blocking for formal evidence:**
- What's not tested: A hard gate that prevents placeholder/no-data figures or rows from entering formal manuscript artifacts.
- Files: `ooh_code/scripts/build_artifacts.py`, `ooh_code/scripts/test_work2_robustness_artifacts.py`, `ooh_code/artifacts/`
- Risk: Incomplete outputs can look publication-ready.
- Priority: Medium

**RNG isolation:**
- What's not tested: Environment construction and capacity-mask generation do not perturb unrelated NumPy random streams.
- Files: `ooh_code/Environments/OOH/env_utils.py`, `ooh_code/Environments/OOH/Parcelpoint_py.py`, `ooh_code/Src/config.py`
- Risk: Study reruns with the same manifest can differ if construction order changes.
- Priority: Medium

---

*Concerns audit: 2026-06-09*
