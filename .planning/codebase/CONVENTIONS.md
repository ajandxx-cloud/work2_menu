---
last_mapped_commit: 97514c7
---

# Coding Conventions

**Analysis Date:** 2026-06-16

## Naming Patterns

**Files:**
- Use snake_case for Python modules and script entry points: `work2_coding/scripts/run_study.py`, `work2_coding/Src/paired_replay.py`, `work2_coding/Src/artifact_status.py`, `work2_coding/Src/formal_readiness.py`.
- Keep script-style tests under `work2_coding/scripts/` with `test_*.py` names: `work2_coding/scripts/test_paired_replay_contract.py`, `work2_coding/scripts/test_artifact_gates.py`, `work2_coding/scripts/test_optout_accounting.py`.
- Keep standalone package tests under `work2_coding/tests/` only when they exercise legacy package behavior: `work2_coding/tests/test_akkerman_rc_no_failure.py`.
- Keep study manifests in `work2_coding/Experiments/studies/*.yaml`: `work2_coding/Experiments/studies/smoke_robust_menu.yaml`, `work2_coding/Experiments/studies/formal_robust_menu.yaml`.
- Keep planning-only validators with the planning artifacts they validate: `.planning/data/case_studies/validate_case_contracts.py`, `.planning/data/case_studies/test_case_contracts.py`.

**Functions:**
- Use snake_case for functions and methods: `build_normalized_row()` in `work2_coding/Src/paired_replay.py`, `classify_artifact()` in `work2_coding/Src/artifact_status.py`, `check_formal_readiness()` in `work2_coding/Src/formal_readiness.py`.
- Use `main(argv=None)` for CLI scripts so commands can be tested without spawning a new process: `work2_coding/scripts/check_formal_readiness.py`, `work2_coding/scripts/build_artifacts.py`, `work2_coding/scripts/run_study.py`.
- Use `test_*` function names in script-style tests, then list them explicitly inside `main()`: `work2_coding/scripts/test_robust_menu_logic.py`, `work2_coding/scripts/test_service_product_contract.py`.

**Variables:**
- Use snake_case for local variables, parsed arguments, and metadata fields: `manifest_path`, `output_root`, `readiness_json`, `claim_ready`, `checkpoint_load_status`.
- Use uppercase constants for schema fields, policy tag sets, and fixed contract values: `NORMALIZED_ROW_FIELDS` in `work2_coding/Src/paired_replay.py`, `MAINLINE_POLICY_TAGS` and `ATTENTION_POLICY_TAGS` in `work2_coding/Src/policy_adapters.py`, `SCHEMA_VERSION` in `work2_coding/Src/paper_artifacts.py`.
- Use explicit row keys matching the normalized output schema instead of shorthand names. Examples include `optout_count`, `accepted_home_count`, `meeting_point_uptake_rate`, `checkpoint_load_status`, `manifest_hash`, and `settings_hash` in `work2_coding/Src/paired_replay.py`.

**Types:**
- Use dataclasses for domain containers and route-choice payloads: `Location`, `ParcelPoint`, `ServiceProduct`, `MenuOffer`, and `ChoiceResult` in `work2_coding/Environments/OOH/containers.py`.
- Use dictionaries for normalized experiment rows, study summaries, metadata sidecars, and paper artifact manifests: `work2_coding/Src/paired_replay.py`, `work2_coding/Src/artifact_builder.py`, `work2_coding/Src/paper_artifacts.py`.
- Use `pathlib.Path` in new orchestration, artifact, and gate code: `work2_coding/Src/study_execution.py`, `work2_coding/Src/formal_readiness.py`, `work2_coding/Src/artifact_builder.py`.

## Code Style

**Formatting:**
- No formatter configuration is present. `pyproject.toml`, `.prettierrc`, `ruff.toml`, `setup.cfg`, and `.flake8` are not detected at the repository root.
- Use standard Python formatting with 4-space indentation and readable helper functions. Match local style in the file being edited.
- Prefer `pathlib.Path` for new filesystem code, especially in `work2_coding/Src/*` and `work2_coding/scripts/*`.
- Preserve legacy style inside legacy simulation modules unless changing the local behavior requires cleanup: `work2_coding/Src/config.py`, `work2_coding/run.py`, `work2_coding/Environments/OOH/Parcelpoint_py.py`.
- Use non-interactive plotting backends in artifact-producing scripts and tests. `matplotlib.use("Agg")` is used in `work2_coding/scripts/test_artifact_gates.py`.

**Linting:**
- No linting configuration is detected. Use local script tests as the effective quality gate.
- Where scripts modify `sys.path` before importing `Src`, keep the import below the path mutation and use `# noqa: E402` if the file already follows that pattern: `work2_coding/scripts/run_study.py`, `work2_coding/scripts/check_formal_readiness.py`.

## Import Organization

**Order:**
1. Standard library imports: `argparse`, `json`, `sys`, `pathlib.Path`, `tempfile`, `subprocess`.
2. Third-party imports: `yaml`, `numpy`, `matplotlib`, `torch`.
3. Runtime-root path setup for script entry points:

```python
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
```

4. Local imports from `Src` and `Environments`: `from Src.experiment_contracts import load_manifest`, `from Src.paired_replay import build_normalized_row`.

**Path Aliases:**
- No Python package alias system is configured. Scripts insert `work2_coding/` into `sys.path` and import modules with `Src.*`.
- Study manifest resolution supports `work2_coding/Experiments/` as the current manifest root, with lowercase fallback in `work2_coding/Src/experiment_contracts.py`.
- Do not introduce a parallel runtime root. Use `work2_coding/` for imports, scripts, manifests, and generated runtime artifacts.

## Error Handling

**Patterns:**
- Raise `ValueError` for invalid manifests, invalid normalized rows, invalid readiness inputs, and invalid research contracts: `work2_coding/Src/experiment_contracts.py`, `work2_coding/Src/paired_replay.py`, `work2_coding/Src/formal_readiness.py`.
- Raise `FileNotFoundError` for missing required manifests, checkpoints, readiness files, or run artifacts: `work2_coding/Src/study_execution.py`, `work2_coding/Src/artifact_builder.py`.
- Use `RuntimeError` for runtime execution failures that should stop study execution: `work2_coding/Src/study_execution.py`.
- Use `SystemExit(main())` or `raise SystemExit(...)` in CLI scripts so shell callers receive a meaningful exit code: `work2_coding/scripts/check_formal_readiness.py`, `work2_coding/scripts/build_artifacts.py`.
- Catch broad exceptions only at boundaries where an error must be converted into structured status metadata. `actual_rows_for_manifest()` records failed rows in `work2_coding/Src/study_execution.py`; readiness and artifact builders record blocked status in JSON/Markdown outputs.
- Formal and pilot gates fail closed. Missing checkpoints, placeholder formal rows, dirty git without an explicit override, and missing dependency snapshots block claim-ready outputs in `work2_coding/Src/formal_readiness.py` and `work2_coding/Src/artifact_status.py`.

## Logging

**Framework:** console output plus durable JSON/CSV/Markdown status artifacts.

**Patterns:**
- CLIs print concise status to stdout and write machine-readable outputs under the requested artifact directory: `work2_coding/scripts/run_study.py`, `work2_coding/scripts/build_artifacts.py`, `work2_coding/scripts/check_formal_readiness.py`.
- Tests print a single `PASS: ...` line after all assertions pass: `work2_coding/scripts/test_paired_replay_contract.py`, `work2_coding/scripts/test_policy_fairness_contract.py`.
- Artifact and readiness status belongs in files, not only logs. Examples include `FORMAL_READINESS.json`, `artifact_status.json`, `claim_guard.json`, and sidecar `*.metadata.json` files produced by `work2_coding/Src/formal_readiness.py`, `work2_coding/Src/artifact_builder.py`, and `work2_coding/Src/paper_artifacts.py`.
- Legacy experiment logging remains in the legacy runtime utilities. Keep new research-contract logging in structured artifacts rather than expanding legacy logger usage.

## Comments

**When to Comment:**
- Use comments where they mark a research contract, guardrail, or boundary condition that is easy to violate. Good locations are manifest validation in `work2_coding/Src/experiment_contracts.py`, artifact classification in `work2_coding/Src/artifact_status.py`, and opt-out route mutation rules in `work2_coding/Environments/OOH/containers.py`.
- Avoid comments that restate assignments or simple control flow. The script-style test names should describe the expected contract.

**JSDoc/TSDoc:**
- Not applicable. This is a Python codebase.

**Python Docstrings:**
- Use module or function docstrings for contract-heavy modules and validation scripts. Examples are `work2_coding/Src/paired_replay.py`, `work2_coding/Src/artifact_status.py`, `.planning/data/case_studies/validate_case_contracts.py`.

## Function Design

**Size:** Prefer small, named helpers for validation, row derivation, status classification, and CLI argument parsing. Examples include `validate_normalized_row()` in `work2_coding/Src/paired_replay.py`, `validate_manifest()` in `work2_coding/Src/experiment_contracts.py`, and `classify_artifact()` in `work2_coding/Src/artifact_status.py`.

**Parameters:** Use explicit parameters and `argv=None` for testable CLIs. Pass paths as `Path` or path-like values and convert at the boundary.

**Return Values:** Return structured dictionaries, lists, or dataclasses instead of relying on ambient state. Examples include normalized row dictionaries in `work2_coding/Src/paired_replay.py`, artifact status dictionaries in `work2_coding/Src/artifact_status.py`, and readiness result dictionaries in `work2_coding/Src/formal_readiness.py`.

**Side Effects:** Keep side effects at script or orchestration boundaries. Core validators should be pure where possible. Environment mutation is intentionally localized to simulation/runtime modules such as `work2_coding/Environments/OOH/Parcelpoint_py.py`.

## Module Design

**Exports:** No package-level `__all__` convention is used. Import concrete functions/classes directly from their modules.

**Barrel Files:** Barrel files are not used. Do not add re-export modules unless a package boundary emerges.

**Contract Modules:**
- Put normalized row schema, derived metrics, trace hashes, manifest hashes, and paired settings checks in `work2_coding/Src/paired_replay.py`.
- Put manifest parsing and manifest-level contract validation in `work2_coding/Src/experiment_contracts.py`.
- Put policy tag semantics, policy adapter overrides, policy-only drift rules, and attention-policy scope in `work2_coding/Src/policy_adapters.py`.
- Put artifact readiness classification in `work2_coding/Src/artifact_status.py`.
- Put formal checkpoint and dependency readiness gates in `work2_coding/Src/formal_readiness.py`.
- Put paper artifact package and claim-guard materialization in `work2_coding/Src/paper_artifacts.py` and `work2_coding/Src/manuscript_claims.py`.

## Manifest And Artifact Conventions

**Manifests:**
- Study manifests live in `work2_coding/Experiments/studies/*.yaml`. Use existing smoke, pilot, diagnostic, and formal manifests as templates: `work2_coding/Experiments/studies/smoke_robust_menu.yaml`, `work2_coding/Experiments/studies/pilot_robust_menu.yaml`, `work2_coding/Experiments/studies/formal_robust_menu.yaml`.
- Manifest tiers are `smoke`, `pilot`, and `formal`; run modes include `smoke`, `diagnostic`, `pilot`, and `formal` in `work2_coding/Src/experiment_contracts.py`.
- Every comparison policy in a paired study must preserve paired replay fairness. Fields listed in `paired_fields` cannot drift unless explicitly listed in `varied_fields`, enforced by `validate_paired_settings()` in `work2_coding/Src/paired_replay.py`.
- Policy differences belong in policy adapter fields and policy-only overrides, enforced by `validate_policy_only_overrides()` in `work2_coding/Src/policy_adapters.py`.

**Normalized Rows:**
- Use the row schema in `NORMALIZED_ROW_FIELDS` in `work2_coding/Src/paired_replay.py`. Do not hand-create ad hoc CSV columns.
- Use `build_normalized_row()` to derive `accepted_count`, `served_count`, `acceptance_rate`, `optout_rate`, `home_share`, `meeting_point_uptake_rate`, `served_rate`, `total_cost`, and `net_profit`.
- Use `validate_normalized_row()` before promoting generated rows into artifact pipelines. Formal placeholder rows are invalid.
- Keep `optout_count` separate from `accepted_home_count`. Opt-out is an outside option and must not mutate routes, service time, or parcel-point capacity.

**Generated Artifacts:**
- Runtime study outputs are generated under `work2_coding/artifacts/` and `work2_coding/outputs/`. Treat them as evidence of contracts, not as source code.
- Do not hand-edit generated result rows or paper artifacts. Regenerate through `work2_coding/scripts/run_study.py`, `work2_coding/scripts/build_artifacts.py`, `work2_coding/scripts/check_formal_readiness.py`, and `work2_coding/scripts/build_phase10_paper_artifacts.py`.
- Artifact sidecars must carry provenance. Sidecar metadata is generated by `work2_coding/Src/artifact_builder.py` and `work2_coding/Src/paper_artifacts.py`.
- Claim-ready artifact generation requires readiness JSON, non-placeholder rows, clean or explicitly allowed git state, dependency snapshot, and formal checkpoint metadata.

## Research Integrity Conventions

**Paired Replay Fairness:**
- Preserve identical paired fields across policies unless the manifest explicitly declares them varied. Enforcement lives in `work2_coding/Src/paired_replay.py` and is tested by `work2_coding/scripts/test_paired_replay_contract.py` and `work2_coding/scripts/test_policy_fairness_contract.py`.
- Use manifest hashes, settings hashes, trace hashes, split identifiers, and seed fields in normalized rows so policy comparisons can be replayed and audited.

**Opt-Out Accounting:**
- Keep opt-out accounting separate from accepted home pickup and accepted meeting-point pickup. `ServiceProduct.opt_out()` and `ChoiceResult.opted_out()` in `work2_coding/Environments/OOH/containers.py` represent non-route choices.
- Route mutation for accepted home or meeting-point services happens in `work2_coding/Environments/OOH/Parcelpoint_py.py`; opt-out increments `count_opted_out` without route mutation.
- Artifact gates must block rows that mix opt-out into accepted home accounting. This is tested in `work2_coding/scripts/test_optout_accounting.py` and `work2_coding/scripts/test_artifact_gates.py`.

**Checkpoint Metadata:**
- Pilot and formal studies must make checkpoint load status explicit. Required fields include `checkpoint_policy`, `checkpoint_path`, `checkpoint_required`, `checkpoint_load_status`, and related status metadata in `work2_coding/Src/paired_replay.py`.
- Missing or unloaded required checkpoints block pilot/formal readiness in `work2_coding/Src/study_execution.py`, `work2_coding/Src/formal_readiness.py`, and `work2_coding/Src/artifact_status.py`.

**No-Filter Diagnostic Status:**
- Treat no-filter and all-diagnostic policy sets as diagnostic, not empirical claim evidence. Classification lives in `work2_coding/Src/artifact_status.py`.
- `no_filter` aliases to ETA filter mode `none` in `work2_coding/Src/Algorithms/DSPO_Menu.py`; artifacts that depend only on no-filter rows must remain diagnostic unless stronger evidence is added through the formal gates.

**Attention Scope:**
- Keep attention-based choice and scoring out of v1 claim scope. Attention tags are centralized as diagnostic/V2 policy tags in `work2_coding/Src/policy_adapters.py`.
- Attention smoke and pilot manifests may exist as exploratory contracts, but v1 paper artifacts and claim guards must not promote them as claim-ready v1 evidence.

**Smoke, Pilot, And Formal Boundaries:**
- Smoke manifests are for contract checks and diagnostics.
- Pilot manifests require explicit checkpoint status and are not automatically claim-ready.
- Formal manifests cannot emit placeholder contract-only rows. `execute_study()` in `work2_coding/scripts/run_study.py` and `work2_coding/Src/study_execution.py` reject formal placeholder behavior.

**Planning-Only Case Studies:**
- Planning case-study scaffolds are validated separately from runtime experiments. `.planning/data/case_studies/validate_case_contracts.py` enforces scaffold labels, blockers, and absence of runtime case manifests under `work2_coding/Experiments/studies/`.
- Do not treat planning-only case scaffolds as executed case-study evidence.

---

*Convention analysis: 2026-06-16*
