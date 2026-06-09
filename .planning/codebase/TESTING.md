# Testing Patterns

**Analysis Date:** 2026-06-09
**last_mapped_commit:** `37b20aa`

## Test Framework

**Runner:**
- Framework: executable Python scripts with direct `assert` statements and hand-written `main()` functions.
- Version: Not applicable.
- Config: Not detected. No `pytest.ini`, `tox.ini`, `noxfile.py`, `pyproject.toml`, `setup.cfg`, or dedicated test runner config exists.
- Dependency: Not detected. `ooh_code/requirements.txt` declares `pyyaml`, `numpy`, `torch`, `hygese`, and `matplotlib`, but no `pytest`, `coverage`, `hypothesis`, or mocking framework.

**Assertion Library:**
- Python built-in `assert` and explicit `AssertionError`.
- Some manifest and gate tests use local assertion helpers such as `_assert(...)` in `ooh_code/scripts/test_work2_main_manifest.py` and `assert_true(...)` in `ooh_code/scripts/test_phase6_redesign_policies.py`.

**Run Commands:**
```bash
cd ooh_code
python scripts/test_option_features.py              # Run one utility smoke test
python scripts/test_setmenunet.py                   # Run one neural model smoke test
python scripts/test_menu_objective_mode.py          # Run one menu objective test script
python scripts/test_work2_main_manifest.py          # Run one manifest contract test
python scripts/test_phase08_artifact_gate.py        # Run one artifact gate test script
python scripts/run_study.py --study smoke_rc        # Run workflow-level smoke verification
python scripts/build_artifacts.py --study rc_paper_v1 # Regenerate artifact snapshots after study output exists
```

- There is no repository-level "run all tests" command in `ooh_code/README.md`.
- Watch mode: Not detected.
- Coverage: Not detected.

## Test File Organization

**Location:**
- Tests are colocated with executable workflow scripts under `ooh_code/scripts/`, not under a separate `tests/` package.
- Model and utility tests live next to workflow scripts: `ooh_code/scripts/test_option_features.py`, `ooh_code/scripts/test_setmenunet.py`, `ooh_code/scripts/test_cnnsetmenunet.py`, `ooh_code/scripts/test_cnn_setmenu.py`, `ooh_code/scripts/test_mlp_setmenu.py`.
- Manifest and artifact-gate tests live in the same directory: `ooh_code/scripts/test_work2_main_manifest.py`, `ooh_code/scripts/test_work2_formal_manifest.py`, `ooh_code/scripts/test_phase08_manifest.py`, `ooh_code/scripts/test_phase08_artifact_gate.py`, `ooh_code/scripts/test_work2_robustness_artifacts.py`.

**Naming:**
- Use `test_<subject>.py` for executable test scripts.
- Use `test_<behavior>` or `test_<contract>` for test functions: `test_home_only_candidate_slots` in `ooh_code/scripts/test_option_features.py`, `test_expected_profit_enumeration_counts_k10_l3` in `ooh_code/scripts/test_menu_objective_mode.py`, `test_duplicate_policy_seed_fails` in `ooh_code/scripts/test_phase08_artifact_gate.py`.
- Use helper names with leading underscores for private test helpers: `_load_manifest` and `_assert` in `ooh_code/scripts/test_work2_main_manifest.py`; `_make_config` in `ooh_code/scripts/test_cnn_setmenu.py`.

**Structure:**
```text
ooh_code/
├── scripts/
│   ├── test_option_features.py
│   ├── test_setmenunet.py
│   ├── test_cnnsetmenunet.py
│   ├── test_cnn_setmenu.py
│   ├── test_mlp_setmenu.py
│   ├── test_menu_objective_mode.py
│   ├── test_work2_main_manifest.py
│   ├── test_work2_formal_manifest.py
│   ├── test_work2_robustness_manifests.py
│   ├── test_phase08_artifact_gate.py
│   └── test_work2_no_paper_changes.py
├── experiments/
│   ├── studies/*.yaml
│   └── suites/*.yaml
└── artifacts/
    ├── results_snapshot/
    ├── tables/
    └── figures/
```

- Treat study manifests under `ooh_code/experiments/studies/` as test fixtures for manifest-contract tests.
- Treat generated or committed artifact snapshots under `ooh_code/artifacts/` and root `artifacts/work2_cnn_setmenunet/` as inputs for artifact-summary and robustness tests when those tests validate output contracts.

## Test Structure

**Suite Organization:**
```python
def test_behavior_name():
    # arrange
    # act
    # assert
    assert condition, "actionable failure message"


def main():
    tests = [
        test_behavior_name,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} tests")


if __name__ == "__main__":
    main()
```

**Patterns:**
- Use direct script execution with `if __name__ == "__main__": main()` in `ooh_code/scripts/test_menu_objective_mode.py`, `ooh_code/scripts/test_work2_main_manifest.py`, `ooh_code/scripts/test_phase08_artifact_gate.py`, and `ooh_code/scripts/test_work2_no_paper_changes.py`.
- Use named test lists with PASS/FAIL accounting when individual test continuation is useful: `ooh_code/scripts/test_option_features.py` and `ooh_code/scripts/test_setmenunet.py`.
- Use fail-fast `main()` loops when tests are deterministic and failures should stop the script: `ooh_code/scripts/test_menu_objective_mode.py`, `ooh_code/scripts/test_work2_artifact_summary.py`, and `ooh_code/scripts/test_phase08_artifact_gate.py`.
- Keep tests deterministic where invariants depend on neural outputs: `torch.manual_seed(42)` appears in `ooh_code/scripts/test_setmenunet.py` and `ooh_code/scripts/test_cnnsetmenunet.py`.
- Put `ooh_code/` on `sys.path` at the top of scripts that import `Src` or `Environments`: `ooh_code/scripts/test_option_features.py`, `ooh_code/scripts/test_menu_objective_mode.py`, `ooh_code/scripts/test_phase6_redesign_policies.py`, `ooh_code/scripts/test_work2_robustness_manifests.py`.

## Mocking

**Framework:** Not detected. No `unittest.mock`, pytest `monkeypatch`, or third-party mocking library is used.

**Patterns:**
```python
from types import SimpleNamespace

algo = object.__new__(DSPO_Menu)
algo.menu_policy = "menu_optimization"
algo.config = SimpleNamespace(home_failure=0.0, failure_cost=0.0)
```

- Use hand-built lightweight objects for isolated algorithm tests. `ooh_code/scripts/test_menu_objective_mode.py` constructs a `DSPO_Menu` instance with `object.__new__` and assigns only fields required by `_evaluate_menu_for_objective`.
- Use synthetic domain containers as test fixtures: `Customer`, `Location`, `ServiceBundle`, and `MenuOffer` in `ooh_code/scripts/test_menu_objective_mode.py`; evaluated menu dictionaries in `ooh_code/scripts/test_phase6_redesign_policies.py`.
- Use minimal real `Config` instances when integration with parser/config/algorithm wiring matters: `_make_config(...)` in `ooh_code/scripts/test_cnn_setmenu.py` and corresponding patterns in `ooh_code/scripts/test_mlp_setmenu.py`.
- Use temporary filesystem fixtures through `TemporaryDirectory` for artifact and gate tests: `ooh_code/scripts/test_phase08_artifact_gate.py`, `ooh_code/scripts/test_phase08_gap_closure_artifact_gate.py`, `ooh_code/scripts/test_work2_artifact_summary.py`, `ooh_code/scripts/test_work2_robustness_artifacts.py`.
- Use temporary files for model save/load round trips: `tempfile.NamedTemporaryFile` in `ooh_code/scripts/test_setmenunet.py` and `ooh_code/scripts/test_cnnsetmenunet.py`.

**What to Mock:**
- Mock or synthesize heavy environment state when unit-testing pure menu scoring and selection helpers: follow `ooh_code/scripts/test_menu_objective_mode.py` and `ooh_code/scripts/test_phase6_redesign_policies.py`.
- Mock study output directories with minimal `study_summary.json` and `normalized_rows.json` when testing artifact gates: follow `write_study(...)` in `ooh_code/scripts/test_phase08_artifact_gate.py`.
- Use simple dictionaries for normalized artifact rows when testing result classification: `make_rows(...)` in `ooh_code/scripts/test_work2_artifact_summary.py` and `ooh_code/scripts/test_work2_robustness_artifacts.py`.

**What NOT to Mock:**
- Do not mock parser/config wiring when testing algorithm registration or model-selection contracts; use `Parser` and `Config` as in `ooh_code/scripts/test_cnn_setmenu.py` and `ooh_code/scripts/test_mlp_setmenu.py`.
- Do not mock manifest files when testing manifest contracts; read actual YAML manifests such as `ooh_code/experiments/studies/work2_main.yaml`, `ooh_code/experiments/studies/work2_formal_main.yaml`, and `ooh_code/experiments/studies/work2_phase08_pilot.yaml`.
- Do not mock Git state in manuscript-change guard tests; `ooh_code/scripts/test_work2_no_paper_changes.py` intentionally shells out to `git diff --name-only` and `git ls-files --others --exclude-standard`.

## Fixtures and Factories

**Test Data:**
```python
def make_rows(row_overrides=None, omit=None, duplicate=None):
    rows = []
    for seed in phase08.EXPECTED_SEEDS:
        for tag in REQUIRED_TAGS:
            rows.append(make_row(seed, tag, row_overrides.get(tag)))
    return rows
```

**Location:**
- Fixture factories are local to each test script rather than shared across modules.
- Row factories: `make_rows` in `ooh_code/scripts/test_work2_artifact_summary.py`, `ooh_code/scripts/test_work2_formal_artifacts.py`, `ooh_code/scripts/test_phase08_artifact_gate.py`, and `ooh_code/scripts/test_work2_robustness_artifacts.py`.
- Domain factories: `make_algo`, `make_customer`, and `make_offer` in `ooh_code/scripts/test_menu_objective_mode.py`; `fake_agent` and `evaluated` in `ooh_code/scripts/test_phase6_redesign_policies.py`.
- Filesystem factories: `write_study` in `ooh_code/scripts/test_phase08_artifact_gate.py`; temporary diagnostic report writes in `ooh_code/scripts/test_work2_artifact_summary.py`.
- Use actual YAML manifests as fixtures in manifest tests: `ooh_code/experiments/studies/work2_main.yaml`, `ooh_code/experiments/studies/work2_formal_main.yaml`, `ooh_code/experiments/studies/work2_phase08_smoke.yaml`, `ooh_code/experiments/suites/work2_robustness.yaml`.

## Coverage

**Requirements:** None enforced. No coverage target, coverage command, or coverage configuration is detected.

**View Coverage:**
```bash
# Not configured
```

- Coverage is behavioral and contract-oriented rather than measured.
- Current tests cover tensor feature construction (`ooh_code/scripts/test_option_features.py`), SetMenuNet/CNNSetMenuNet model invariants (`ooh_code/scripts/test_setmenunet.py`, `ooh_code/scripts/test_cnnsetmenunet.py`), algorithm integration (`ooh_code/scripts/test_cnn_setmenu.py`, `ooh_code/scripts/test_mlp_setmenu.py`), menu objective semantics (`ooh_code/scripts/test_menu_objective_mode.py`), manifest contracts (`ooh_code/scripts/test_work2_main_manifest.py`, `ooh_code/scripts/test_work2_formal_manifest.py`), artifact gates (`ooh_code/scripts/test_phase08_artifact_gate.py`, `ooh_code/scripts/test_work2_phase6_redesign_formal_gate.py`), and manuscript-change constraints (`ooh_code/scripts/test_work2_no_paper_changes.py`).

## Test Types

**Unit Tests:**
- Pure utility tests validate tensor normalization, padding, masks, NaN handling, and shape contracts in `ooh_code/scripts/test_option_features.py` against `ooh_code/Src/Utils/option_features.py`.
- Menu scoring and selection tests validate isolated `DSPO_Menu` helper behavior with synthetic offers in `ooh_code/scripts/test_menu_objective_mode.py` and `ooh_code/scripts/test_phase6_redesign_policies.py`.
- Artifact classifier tests validate row-level classification and generated diagnostic headings in `ooh_code/scripts/test_work2_artifact_summary.py`, `ooh_code/scripts/test_work2_formal_artifacts.py`, and `ooh_code/scripts/test_work2_robustness_artifacts.py`.

**Integration Tests:**
- Model integration tests build `Config` and algorithm instances to verify registration, buffers, forward passes, and finite loss behavior: `ooh_code/scripts/test_cnn_setmenu.py` and `ooh_code/scripts/test_mlp_setmenu.py`.
- Manifest contract tests read real study manifests and validate method sets, split IDs, budget settings, candidate counts, and documented assumptions: `ooh_code/scripts/test_work2_main_manifest.py`, `ooh_code/scripts/test_work2_formal_manifest.py`, `ooh_code/scripts/test_phase08_manifest.py`, `ooh_code/scripts/test_phase08_gap_closure_manifest.py`, `ooh_code/scripts/test_work2_robustness_manifests.py`.
- Artifact gate tests exercise CLI-like gate `run(...)` functions against temporary study directories: `ooh_code/scripts/test_phase08_artifact_gate.py`, `ooh_code/scripts/test_phase08_gap_closure_artifact_gate.py`, `ooh_code/scripts/test_phase6_redesign_artifact_gate.py`, `ooh_code/scripts/test_work2_phase6_redesign_formal_gate.py`.

**E2E Tests:**
- No browser or hosted-app E2E framework is used.
- Workflow-level smoke verification is performed by running manifest studies such as `python scripts/run_study.py --study smoke_rc`, documented in `ooh_code/README.md`.
- Artifact-generation smoke verification is performed with commands such as `python scripts/build_artifacts.py --study rc_paper_v1` and `python scripts/build_manuscript.py --skip_compile`, documented in `ooh_code/README.md`.

## Common Patterns

**Async Testing:**
```python
# Not used. Tests are synchronous executable scripts.
```

**Error Testing:**
```python
def expect_gate_error(args):
    try:
        phase08.run(args)
    except phase08.GateError:
        return
    raise AssertionError("expected GateError")
```

- Use helper functions that expect custom gate exceptions: `expect_gate_error(...)` in `ooh_code/scripts/test_phase08_artifact_gate.py`, `ooh_code/scripts/test_phase08_gap_closure_artifact_gate.py`, and `ooh_code/scripts/test_phase6_redesign_artifact_gate.py`.
- Use `try/except SystemExit` to verify CLI argument validation when missing explicit inputs must fail: `test_missing_explicit_input_fails` in `ooh_code/scripts/test_phase08_artifact_gate.py`.
- Use negative tests for missing seeds, missing policies, duplicate rows, missing metrics, null service profits, and forbidden output directories in artifact-gate tests: `ooh_code/scripts/test_phase08_artifact_gate.py` and `ooh_code/scripts/test_phase08_gap_closure_artifact_gate.py`.

**Numerical Testing:**
```python
assert torch.allclose(out_orig, out_restored, atol=1e-5)
assert abs(normed["predicted_ivt"][1] - 300.0 / 3600.0) < 1e-5
```

- Use `torch.no_grad()` and `model.eval()` for neural invariant checks in `ooh_code/scripts/test_setmenunet.py` and `ooh_code/scripts/test_cnnsetmenunet.py`.
- Use tolerance-based assertions for floating-point normalization and neural outputs: `ooh_code/scripts/test_option_features.py`, `ooh_code/scripts/test_setmenunet.py`, `ooh_code/scripts/test_cnnsetmenunet.py`.
- Use `np.isfinite(...)` checks for generated costs and losses in algorithm integration tests: `ooh_code/scripts/test_cnn_setmenu.py` and `ooh_code/scripts/test_mlp_setmenu.py`.

**Filesystem Testing:**
```python
with TemporaryDirectory() as tmp:
    out_dir = Path(tmp) / "phase08_artifacts"
    result = phase08.run(["--study-dir", str(study_dir), "--output-dir", str(out_dir)])
    assert {path.name for path in out_dir.iterdir()} == expected
```

- Use `TemporaryDirectory` for tests that write artifacts or study summaries.
- Assert exact output filenames for gate outputs in `ooh_code/scripts/test_phase08_artifact_gate.py`.
- Read generated Markdown or JSON back from disk and assert required headings or status fields in `ooh_code/scripts/test_work2_artifact_summary.py`, `ooh_code/scripts/test_work2_formal_artifacts.py`, and `ooh_code/scripts/test_work2_robustness_artifacts.py`.

**Scientific Workflow Testing:**
- Keep scientific tests tied to explicit contracts: candidate slot shape `K + 1`, home-first option tensors, exact enumeration counts, opt-out guardrails, manifest seed sets, and manuscript unlock decisions.
- For new menu methods, add at least one isolated objective test under `ooh_code/scripts/test_menu_objective_mode.py` or a focused companion script, one manifest contract test if a YAML study changes, and one artifact/gate test if generated paper evidence changes.
- For new study manifests, add assertions against actual files under `ooh_code/experiments/studies/` rather than duplicating the manifest as an in-test dictionary.

---

*Testing analysis: 2026-06-09*
