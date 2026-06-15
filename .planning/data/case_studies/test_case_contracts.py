"""Self-tests for the Phase 7 planning-side case contract validator."""

import importlib.util
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory


THIS_DIR = Path(__file__).resolve().parent


def _load_validator():
    path = THIS_DIR / "validate_case_contracts.py"
    spec = importlib.util.spec_from_file_location("phase7_case_validator", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = _load_validator()


def _copy_valid_fixture(repo_root):
    root = repo_root / ".planning" / "data" / "case_studies"
    root.mkdir(parents=True, exist_ok=True)
    for filename in validator.REQUIRED_FILES:
        shutil.copy2(THIS_DIR / filename, root / filename)
    return root


def _find(findings, code):
    return [item for item in findings if item["code"] == code]


def _blocking_codes(findings):
    return {item["code"] for item in findings if item["severity"] == "blocking"}


def test_missing_blocker_fields_are_blocking():
    with TemporaryDirectory() as tmp:
        repo_root = Path(tmp)
        root = _copy_valid_fixture(repo_root)
        readme = root / "README.md"
        readme.write_text(
            readme.read_text(encoding="utf-8").replace("case_execution_allowed: false\n", ""),
            encoding="utf-8",
        )
        findings = validator.validate(root, repo_root=repo_root)
        assert "missing_blocker_field" in _blocking_codes(findings)


def test_missing_simulated_labels_are_blocking():
    with TemporaryDirectory() as tmp:
        repo_root = Path(tmp)
        root = _copy_valid_fixture(repo_root)
        manifest = root / "case_manifest_draft.yaml"
        manifest.write_text(
            manifest.read_text(encoding="utf-8").replace("simulated choice", "synthetic selection"),
            encoding="utf-8",
        )
        findings = validator.validate(root, repo_root=repo_root)
        assert "missing_required_label" in _blocking_codes(findings)


def test_runtime_manifest_leak_is_blocking():
    with TemporaryDirectory() as tmp:
        repo_root = Path(tmp)
        root = _copy_valid_fixture(repo_root)
        studies = repo_root / "work2_coding" / "Experiments" / "studies"
        studies.mkdir(parents=True, exist_ok=True)
        (studies / "case_manifest_draft.yaml").write_text("name: forbidden\n", encoding="utf-8")
        findings = validator.validate(root, repo_root=repo_root)
        assert "runtime_manifest_leak" in _blocking_codes(findings)


def test_valid_scaffold_has_no_blocking_findings():
    with TemporaryDirectory() as tmp:
        repo_root = Path(tmp)
        root = _copy_valid_fixture(repo_root)
        findings = validator.validate(root, repo_root=repo_root)
        assert not [item for item in findings if item["severity"] == "blocking"], findings


def test_finding_severities_are_limited():
    with TemporaryDirectory() as tmp:
        repo_root = Path(tmp)
        root = _copy_valid_fixture(repo_root)
        findings = validator.validate(root, repo_root=repo_root)
        severities = {item["severity"] for item in findings}
        assert severities <= validator.SEVERITIES
        assert _find(findings, "source_contract_scope")
        assert _find(findings, "runtime_manifest_absent")


def main():
    tests = [
        test_missing_blocker_fields_are_blocking,
        test_missing_simulated_labels_are_blocking,
        test_runtime_manifest_leak_is_blocking,
        test_valid_scaffold_has_no_blocking_findings,
        test_finding_severities_are_limited,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} case contract validator tests")


if __name__ == "__main__":
    main()
