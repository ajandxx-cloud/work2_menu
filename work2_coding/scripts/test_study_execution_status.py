import json
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.experiment_contracts import load_manifest  # noqa: E402
from Src.paired_replay import build_normalized_row, resolve_paired_settings, validate_normalized_row  # noqa: E402
from Src.study_execution import inspect_manifest_prerequisites  # noqa: E402


def run_command(args):
    return subprocess.run(args, cwd=str(ROOT), text=True, capture_output=True)


def last_stdout_path(result):
    return Path(result.stdout.strip().splitlines()[-1])


def test_contract_only_smoke_status_and_git_fields():
    with TemporaryDirectory() as tmp:
        result = run_command([
            sys.executable,
            "scripts/run_study.py",
            "--study",
            "smoke_robust_menu",
            "--contract-only",
            "--output-root",
            str(Path(tmp)),
        ])
        assert result.returncode == 0, result.stderr
        run_dir = last_stdout_path(result)
        rows = json.loads((run_dir / "normalized_rows.json").read_text(encoding="utf-8"))
        summary = json.loads((run_dir / "study_summary.json").read_text(encoding="utf-8"))
        assert summary["execution_status"] == "contract_only"
        assert summary["placeholder_only"] is True
        assert rows
        for row in rows:
            assert row["status"] == "contract_only"
            assert row["execution_status"] == "contract_only"
            assert row["placeholder_only"] is True
            assert row["git_commit"]
            assert "git_dirty" in row


def test_formal_placeholder_rejection_preserved():
    with TemporaryDirectory() as tmp:
        result = run_command([
            sys.executable,
            "scripts/run_study.py",
            "--study",
            "formal_robust_menu",
            "--contract-only",
            "--output-root",
            str(Path(tmp)),
        ])
        assert result.returncode != 0
        assert "formal studies cannot emit placeholder" in (result.stderr + result.stdout)


def test_pilot_missing_checkpoint_writes_blockers():
    with TemporaryDirectory() as tmp:
        result = run_command([
            sys.executable,
            "scripts/run_study.py",
            "--study",
            "pilot_robust_menu",
            "--execute",
            "--output-root",
            str(Path(tmp)),
            "--max-policies",
            "2",
        ])
        assert result.returncode == 0, result.stderr
        run_dir = last_stdout_path(result)
        blockers = json.loads((run_dir / "blockers.json").read_text(encoding="utf-8"))["blockers"]
        summary = json.loads((run_dir / "study_summary.json").read_text(encoding="utf-8"))
        rows = json.loads((run_dir / "normalized_rows.json").read_text(encoding="utf-8"))
        assert summary["execution_status"] == "blocked"
        assert summary["blocker_count"] >= 1
        assert blockers[0]["code"] == "missing_checkpoint_file"
        assert "supervised_ml.pt" in blockers[0]["checkpoint_path"]
        assert rows
        assert {row["status"] for row in rows} == {"blocked"}
        assert {row["checkpoint_load_status"] for row in rows} == {"failed"}
        assert all(row["placeholder_only"] for row in rows)


def test_actual_smoke_writes_completed_rows():
    with TemporaryDirectory() as tmp:
        result = run_command([
            sys.executable,
            "scripts/run_study.py",
            "--study",
            "smoke_robust_menu",
            "--execute",
            "--output-root",
            str(Path(tmp)),
            "--max-policies",
            "2",
        ])
        assert result.returncode == 0, result.stderr
        run_dir = last_stdout_path(result)
        summary = json.loads((run_dir / "study_summary.json").read_text(encoding="utf-8"))
        rows = json.loads((run_dir / "normalized_rows.json").read_text(encoding="utf-8"))
        assert summary["execution_status"] == "completed"
        assert summary["placeholder_only"] is False
        assert rows
        assert {row["status"] for row in rows} == {"completed"}
        assert {row["execution_status"] for row in rows} == {"completed"}
        assert not any(row["placeholder_only"] for row in rows)
        assert all(row["acceptance_rate"] is not None for row in rows)
        assert all(row["optout_rate"] is not None for row in rows)
        assert all(row["home_share"] is not None for row in rows)
        assert all(row["meeting_point_uptake_rate"] is not None for row in rows)
        assert all(row["net_price_revenue"] is not None for row in rows)
        assert {row["checkpoint_load_status"] for row in rows} == {"not_requested"}


def test_incomplete_or_blocked_row_cannot_look_completed():
    manifest = load_manifest("smoke_robust_menu")
    setting = resolve_paired_settings(manifest)[0]
    row = build_normalized_row(
        setting,
        run_id="unit",
        status="blocked",
        execution_status="blocked",
        placeholder_only=True,
    )
    validate_normalized_row(row)
    row["status"] = "completed"
    try:
        validate_normalized_row(row)
    except ValueError as exc:
        assert "completed normalized rows cannot be placeholder" in str(exc)
        return
    raise AssertionError("completed placeholder row should fail validation")


def test_no_filter_label_survives_public_runner():
    with TemporaryDirectory() as tmp:
        result = run_command([
            sys.executable,
            "scripts/run_study.py",
            "--study",
            "smoke_robust_menu",
            "--contract-only",
            "--output-root",
            str(Path(tmp)),
        ])
        assert result.returncode == 0, result.stderr
        rows = json.loads((last_stdout_path(result) / "normalized_rows.json").read_text(encoding="utf-8"))
        no_filter = [row for row in rows if row["policy_tag"] == "no_filter_diagnostic"][0]
        assert no_filter["diagnostic"] is True
        assert no_filter["filter_mode"] == "none"
        assert no_filter["status"] == "contract_only"


def test_prerequisite_helper_reports_expected_checkpoint_status():
    manifest = load_manifest("pilot_robust_menu")
    blockers = inspect_manifest_prerequisites(manifest, root=ROOT, actual_execution=True)
    assert blockers
    assert blockers[0]["expected_status"] == "loaded"
    assert blockers[0]["code"] == "missing_checkpoint_file"


def main():
    tests = [
        test_contract_only_smoke_status_and_git_fields,
        test_formal_placeholder_rejection_preserved,
        test_pilot_missing_checkpoint_writes_blockers,
        test_actual_smoke_writes_completed_rows,
        test_incomplete_or_blocked_row_cannot_look_completed,
        test_no_filter_label_survives_public_runner,
        test_prerequisite_helper_reports_expected_checkpoint_status,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} study execution status tests")


if __name__ == "__main__":
    main()
