---
last_mapped_commit: 97514c7
---

# Testing Patterns

**Analysis Date:** 2026-06-16

## Test Framework

**Runner:**
- Script-style Python tests using direct `assert` statements.
- No `pytest`, `unittest`, `coverage.py`, `tox`, `nox`, or CI configuration is detected.
- Test scripts are invoked directly with `python path/to/test_file.py`.

**Assertion Library:**
- Built-in Python `assert` is the standard assertion mechanism.
- Helper functions such as `expect_value_error()` are used for negative-path tests in `work2_coding/scripts/test_paired_replay_contract.py` and `work2_coding/scripts/test_robust_menu_logic.py`.

**Run Commands:**
```powershell
cd work2_coding
python -c "import sys; sys.path.insert(0, '.'); import Src.config"
python scripts/test_paired_replay_contract.py
python scripts/test_policy_fairness_contract.py
python scripts/test_optout_accounting.py
python scripts/test_artifact_gates.py
python scripts/test_robust_menu_logic.py
python scripts/test_service_product_contract.py
python scripts/test_formal_readiness.py
python scripts/test_checkpoint_provenance.py
python scripts/test_study_execution_status.py
```

```powershell
python scripts/test_phase8_sensitivity_contracts.py
python scripts/test_phase8_sensitivity_summary.py
python scripts/test_phase8_baseline_validation.py
python scripts/test_phase9_dspo_family_validation.py
python scripts/test_phase9_exact_greedy_contracts.py
python scripts/test_phase9_tractability_summary.py
python scripts/test_phase10_paper_artifacts.py
python scripts/test_manuscript_claim_guard.py
```

```powershell
cd ..
python .planning/data/case_studies/test_case_contracts.py
```

## Test File Organization

**Location:**
- Contract and workflow tests live in `work2_coding/scripts/test_*.py`.
- Legacy package tests live in `work2_coding/tests/`.
- Planning-only validation tests live beside planning validators, such as `.planning/data/case_studies/test_case_contracts.py`.
- Study manifests used as fixtures live in `work2_coding/Experiments/studies/*.yaml`.
- Generated artifacts are used as contract evidence through metadata and status files, not edited directly.

**Naming:**
- Use `test_*.py` for executable test scripts.
- Use `test_*` function names inside test scripts.
- Use descriptive test names tied to contracts, for example `test_formal_placeholder_rejected`, `test_no_filter_only_is_diagnostic`, and `test_optout_does_not_mutate_route`.

**Structure:**
```text
work2_coding/
├── scripts/
│   ├── test_paired_replay_contract.py
│   ├── test_policy_fairness_contract.py
│   ├── test_artifact_gates.py
│   ├── test_optout_accounting.py
│   ├── test_formal_readiness.py
│   ├── test_phase8_sensitivity_contracts.py
│   ├── test_phase9_exact_greedy_contracts.py
│   └── test_phase10_paper_artifacts.py
├── tests/
│   └── test_akkerman_rc_no_failure.py
└── Experiments/
    └── studies/
        ├── smoke_robust_menu.yaml
        └── formal_robust_menu.yaml
.planning/
└── data/
    └── case_studies/
        ├── validate_case_contracts.py
        └── test_case_contracts.py
```

## Test Structure

**Suite Organization:**
```python
def test_contract_behavior():
    # Arrange
    row = build_normalized_row(...)

    # Act
    result = classify_artifact([row], ...)

    # Assert
    assert result["status"] == "diagnostic"


def main():
    tests = [
        test_contract_behavior,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} contract tests")


if __name__ == "__main__":
    main()
```

**Patterns:**
- Build synthetic rows through contract helpers instead of manually filling all schema fields. Use `build_normalized_row()` in `work2_coding/Src/paired_replay.py`.
- Load real manifest fixtures with `load_manifest()` from `work2_coding/Src/experiment_contracts.py`.
- Use `TemporaryDirectory()` for artifact and readiness outputs in tests such as `work2_coding/scripts/test_artifact_gates.py`, `work2_coding/scripts/test_formal_readiness.py`, and `work2_coding/scripts/test_phase10_paper_artifacts.py`.
- Assert explicit status strings, schema versions, blocker codes, and provenance fields instead of checking only file existence.
- Print one `PASS` line at the end of each script.

## Mocking

**Framework:** No mocking framework is used.

**Patterns:**
```python
from types import SimpleNamespace
from tempfile import TemporaryDirectory

cfg = SimpleNamespace(menu_time_filtering=True, eta_filter_mode="soft_penalty")
with TemporaryDirectory() as tmp:
    output_root = Path(tmp)
    result = build_artifacts(run_root, output_root=output_root)
    assert result["artifact_status"]["status"] in {"diagnostic", "incomplete"}
```

```python
model = object.__new__(DSPO_Menu)
model.config = cfg
model.solver_diagnostics = {}
```

**What to Mock:**
- Mock heavy solver state and environment objects with lightweight namespaces when testing parser flags, ETA filter diagnostics, solver fallback metadata, and artifact gates.
- Use synthetic normalized rows for artifact classification, readiness, and claim-guard tests.
- Use temporary output directories for file-producing tests.

**What NOT to Mock:**
- Do not mock normalized row validation, manifest validation, artifact status classification, checkpoint readiness gates, or opt-out route mutation contracts.
- Do not mock paired replay fairness checks when testing policy comparisons.
- Do not mock generated artifact sidecar validation when testing claim readiness.

## Fixtures and Factories

**Test Data:**
```python
row = build_normalized_row(
    study_id="smoke_robust_menu",
    run_id="run_001",
    policy_tag="mainline_optimized_mw",
    split_id="split_001",
    seed=123,
    status="completed",
    execution_status="completed",
    checkpoint_load_status="loaded",
    optout_count=2,
    accepted_home_count=3,
    accepted_meeting_point_count=5,
)
validate_normalized_row(row)
```

**Location:**
- Manifest fixtures: `work2_coding/Experiments/studies/*.yaml`.
- Synthetic row factories and schema validation: `work2_coding/Src/paired_replay.py`.
- Policy tag and override fixtures: `work2_coding/Src/policy_adapters.py`.
- Planning case-study fixtures: `.planning/data/case_studies/test_case_contracts.py`.

## Coverage

**Requirements:** No numeric coverage target is enforced.

**View Coverage:**
```powershell
# Not configured
```

**Effective Coverage Gates:**
- Import smoke test for runtime package health: `python -c "import sys; sys.path.insert(0, '.'); import Src.config"` from `work2_coding/`.
- Contract tests for normalized rows, paired replay, manifest fields, policy-only drift, checkpoint metadata, opt-out accounting, artifact eligibility, and paper claim guards.
- Phase verification documents record the command sets used for phase-specific acceptance: `.planning/phases/08-sensitivity-and-robustness-experiments/08-VERIFICATION.md`, `.planning/phases/09-exact-versus-greedy-and-computational-tractability/09-VERIFICATION.md`, `.planning/phases/10-paper-artifact-generation/10-VERIFICATION.md`.

## Test Types

**Unit Tests:**
- Contract helpers and validators: `work2_coding/scripts/test_paired_replay_contract.py`, `work2_coding/scripts/test_formal_readiness.py`, `work2_coding/scripts/test_checkpoint_provenance.py`.
- Policy semantics and drift constraints: `work2_coding/scripts/test_policy_fairness_contract.py`.
- Service product and opt-out semantics: `work2_coding/scripts/test_service_product_contract.py`, `work2_coding/scripts/test_optout_accounting.py`.
- Parser and robust menu objective behavior: `work2_coding/scripts/test_robust_menu_logic.py`.

**Integration Tests:**
- Study execution status and blocked-row behavior: `work2_coding/scripts/test_study_execution_status.py`.
- Artifact builder and artifact status gates: `work2_coding/scripts/test_artifact_builder.py`, `work2_coding/scripts/test_artifact_gates.py`.
- Phase 8 sensitivity summaries and contracts: `work2_coding/scripts/test_phase8_sensitivity_contracts.py`, `work2_coding/scripts/test_phase8_sensitivity_summary.py`, `work2_coding/scripts/test_phase8_baseline_validation.py`.
- Phase 9 DSPO family and exact-vs-greedy diagnostics: `work2_coding/scripts/test_phase9_dspo_family_validation.py`, `work2_coding/scripts/test_phase9_exact_greedy_contracts.py`, `work2_coding/scripts/test_phase9_tractability_summary.py`.
- Phase 10 paper artifact package and claim guard: `work2_coding/scripts/test_phase10_paper_artifacts.py`, `work2_coding/scripts/test_manuscript_claim_guard.py`.

**E2E Tests:**
- No automated full end-to-end formal replay suite is configured.
- CLI workflow checks exist for readiness, study execution, artifact building, and paper artifact package generation.
- Formal empirical readiness depends on running the real commands against real checkpoints and generated rows, not only script-style unit tests.

## Smoke, Pilot, And Formal Readiness Checks

**Smoke Checks:**
```powershell
cd work2_coding
python -c "import sys; sys.path.insert(0, '.'); import Src.config"
python scripts/run_study.py --manifest Experiments/studies/smoke_robust_menu.yaml --output-root artifacts/work2_robust_menu/smoke --contract-only
```

**Pilot/Formal Prerequisites:**
- Required checkpoint contracts are validated by `work2_coding/Src/experiment_contracts.py` and `work2_coding/Src/study_execution.py`.
- Checkpoint load status must be explicit in rows and readiness metadata, using fields from `work2_coding/Src/paired_replay.py`.
- Dependency snapshots and git state are checked by `work2_coding/Src/formal_readiness.py`.

**Formal Readiness:**
```powershell
cd work2_coding
python scripts/check_formal_readiness.py --manifest Experiments/studies/formal_robust_menu.yaml --output-root artifacts/work2_robust_menu/formal_readiness
python scripts/run_study.py --manifest Experiments/studies/formal_robust_menu.yaml --output-root artifacts/work2_robust_menu/formal --execute
python scripts/build_artifacts.py --run-root artifacts/work2_robust_menu/formal --output-root artifacts/work2_robust_menu/formal_artifacts --readiness-json artifacts/work2_robust_menu/formal_readiness/FORMAL_READINESS.json --claim-ready
```

**Formal Guardrails:**
- Formal studies cannot emit placeholder contract-only rows. This is enforced by `work2_coding/scripts/run_study.py` and `work2_coding/Src/study_execution.py`.
- Claim-ready artifacts require formal readiness JSON, dependency snapshot metadata, non-placeholder completed rows, checkpoint load status `loaded`, and artifact status `claim_ready`.
- No-filter-only outputs are diagnostic. This is enforced by `work2_coding/Src/artifact_status.py` and tested by `work2_coding/scripts/test_artifact_gates.py`.
- Attention-based policy outputs are out of v1 claim scope. Attention tags are centralized in `work2_coding/Src/policy_adapters.py`.

## Artifact Gate Checks

**Artifact Status:**
- `work2_coding/Src/artifact_status.py` classifies artifacts as blocked, incomplete, diagnostic, pilot, or claim-ready.
- `work2_coding/scripts/test_artifact_gates.py` checks no rows, placeholder rows, blocked/failed rows, incomplete rows, missing checkpoints, dependency snapshots, no-filter diagnostic status, no-menu ranking exclusion, sidecar provenance, and opt-out accounting blockers.

**Artifact Builder:**
- `work2_coding/Src/artifact_builder.py` builds aggregates, tables, figures, status files, sidecars, and claim-guard outputs.
- `work2_coding/scripts/test_artifact_builder.py` checks generated artifact contracts and status metadata.

**Paper Artifacts:**
- `work2_coding/Src/paper_artifacts.py` writes the Phase 10 paper artifact package.
- `work2_coding/Src/manuscript_claims.py` writes the strict manuscript claim guard.
- `work2_coding/scripts/test_phase10_paper_artifacts.py` and `work2_coding/scripts/test_manuscript_claim_guard.py` validate the package and claim guard.
- Phase 10 verification records `claim_ready=false` for current package status in `.planning/phases/10-paper-artifact-generation/10-VERIFICATION.md`.

**Planning Artifact Gates:**
- `.planning/data/case_studies/validate_case_contracts.py` verifies planning-only case scaffolds, blocker fields, labels, and absence of runtime case manifests.
- `.planning/data/case_studies/test_case_contracts.py` verifies that invalid planning scaffolds fail validation.

## Common Patterns

**Async Testing:**
```python
# Not used. Tests are synchronous script invocations.
```

**Error Testing:**
```python
def expect_value_error(func, message_fragment):
    try:
        func()
    except ValueError as exc:
        assert message_fragment in str(exc)
    else:
        raise AssertionError("expected ValueError")
```

**Numerical Testing:**
- Use exact checks for counts and status fields.
- Use tolerance checks for floating-point rates, utilities, and objective values when asserting derived metrics in `work2_coding/scripts/test_robust_menu_logic.py` and related policy tests.

**Filesystem Testing:**
- Use `TemporaryDirectory()` and `Path` for generated outputs.
- Assert both content and metadata sidecars when validating artifacts.
- Do not modify committed generated rows or paper artifacts directly.

**Subprocess Testing:**
- Use subprocess calls for CLI behavior only when the script boundary matters. Planning case-study tests exercise `.planning/data/case_studies/validate_case_contracts.py` as a command boundary.

## Known Coverage Gaps

**Repo-Wide Runner:**
- There is no single maintained command that discovers and runs every test under `work2_coding/scripts/`, `work2_coding/tests/`, and `.planning/data/`.
- There is no committed CI workflow file detected for these checks.

**Formal Replay:**
- Automated tests validate contracts, readiness gates, and artifact blockers, but do not run the full expensive formal replay with trained checkpoints.
- Formal empirical claims require external execution through `work2_coding/scripts/check_formal_readiness.py`, `work2_coding/scripts/run_study.py --execute`, and `work2_coding/scripts/build_artifacts.py --claim-ready`.

**Generated Artifact Review:**
- Tests validate artifact schemas, sidecars, statuses, and claim guards. Human review remains needed for figure/table presentation quality and manuscript integration.

**Real Case Studies:**
- Current case-study validation is scaffold-only. `.planning/data/case_studies/validate_case_contracts.py` explicitly does not execute runtime studies, fetch external data, validate road graphs, or import `Src.config`.

**Attention-Based Policies:**
- Attention policy tests and manifests are diagnostic/exploratory. They do not establish v1 claim readiness.

**Legacy Runtime:**
- Legacy Akkerman and OOH runtime behavior has limited automated coverage outside `work2_coding/tests/test_akkerman_rc_no_failure.py` and targeted Work2 contract tests.

---

*Testing analysis: 2026-06-16*
