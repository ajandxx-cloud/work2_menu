import csv
import json
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.paired_replay import NORMALIZED_ROW_FIELDS, validate_normalized_row  # noqa: E402
from Src.policy_adapters import required_policy_tags  # noqa: E402


def run_smoke(output_root):
    command = [
        sys.executable,
        "scripts/run_study.py",
        "--study",
        "smoke_robust_menu",
        "--contract-only",
        "--output-root",
        str(output_root),
    ]
    result = subprocess.run(command, cwd=str(ROOT), text=True, capture_output=True, check=True)
    run_dir = Path(result.stdout.strip().splitlines()[-1])
    assert run_dir.exists(), result.stdout + result.stderr
    return run_dir


def load_rows(run_dir):
    json_path = run_dir / "normalized_rows.json"
    csv_path = run_dir / "normalized_rows.csv"
    summary_path = run_dir / "study_summary.json"
    assert json_path.exists()
    assert csv_path.exists()
    assert summary_path.exists()
    rows = json.loads(json_path.read_text(encoding="utf-8"))
    with csv_path.open("r", newline="", encoding="utf-8") as handle:
        csv_rows = list(csv.DictReader(handle))
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    return rows, csv_rows, summary


def test_public_runner_writes_expected_files():
    with TemporaryDirectory() as tmp:
        run_dir = run_smoke(Path(tmp))
        names = {path.name for path in run_dir.iterdir()}
        assert {
            "manifest_snapshot.yaml",
            "study_summary.json",
            "normalized_rows.json",
            "normalized_rows.csv",
        }.issubset(names)


def test_json_and_csv_rows_agree():
    with TemporaryDirectory() as tmp:
        run_dir = run_smoke(Path(tmp))
        rows, csv_rows, summary = load_rows(run_dir)
        assert len(rows) == len(csv_rows)
        assert summary["row_count"] == len(rows)
        assert summary["execution_status"] == "contract_only"
        assert summary["placeholder_only"] is True


def test_required_policy_tags_are_emitted():
    with TemporaryDirectory() as tmp:
        run_dir = run_smoke(Path(tmp))
        rows, _, _ = load_rows(run_dir)
        tags = {row["policy_tag"] for row in rows}
        assert set(required_policy_tags()).issubset(tags)
        assert "random_top_k" in tags


def test_trace_id_shared_within_split():
    with TemporaryDirectory() as tmp:
        run_dir = run_smoke(Path(tmp))
        rows, _, _ = load_rows(run_dir)
        split_to_traces = {}
        for row in rows:
            split_to_traces.setdefault(row["split_id"], set()).add(row["trace_id"])
        assert split_to_traces
        for traces in split_to_traces.values():
            assert len(traces) == 1


def test_manifest_hash_and_required_fields_present():
    with TemporaryDirectory() as tmp:
        run_dir = run_smoke(Path(tmp))
        rows, _, _ = load_rows(run_dir)
        for row in rows:
            assert set(NORMALIZED_ROW_FIELDS).issubset(row.keys())
            assert row["manifest_hash"]
            assert row["settings_hash"]
            assert row["schema_version"] == "normalized-row-v1"
            validate_normalized_row(row)


def test_no_filter_diagnostic_status():
    with TemporaryDirectory() as tmp:
        run_dir = run_smoke(Path(tmp))
        rows, _, _ = load_rows(run_dir)
        row = [r for r in rows if r["policy_tag"] == "no_filter_diagnostic"][0]
        assert row["diagnostic"] is True
        assert row["filter_mode"] == "none"
        assert row["effective_policy"] == "risk_adjusted_expected_profit"


def test_checkpoint_and_uptake_metadata_present():
    with TemporaryDirectory() as tmp:
        run_dir = run_smoke(Path(tmp))
        rows, _, _ = load_rows(run_dir)
        for row in rows:
            assert row["checkpoint_load_status"] == "not_requested"
            assert row["checkpoint_required"] is False
            assert row["uptake_regime"] == "medium"
            assert row["status"] == "contract_only"
            assert row["placeholder_only"] is True


def test_no_paper_artifacts_are_written():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        run_smoke(root)
        written = {path.name for path in root.rglob("*") if path.is_file()}
        assert not any(name.endswith(".tex") for name in written)
        assert "RESULTS_SUMMARY.md" not in written
        assert "study_summary.json" in written


def test_formal_placeholder_rows_are_rejected_by_runner():
    with TemporaryDirectory() as tmp:
        command = [
            sys.executable,
            "scripts/run_study.py",
            "--study",
            "formal_robust_menu",
            "--contract-only",
            "--output-root",
            str(Path(tmp)),
        ]
        result = subprocess.run(command, cwd=str(ROOT), text=True, capture_output=True)
        assert result.returncode != 0
        assert "formal studies cannot emit placeholder" in (result.stderr + result.stdout)


def main():
    tests = [
        test_public_runner_writes_expected_files,
        test_json_and_csv_rows_agree,
        test_required_policy_tags_are_emitted,
        test_trace_id_shared_within_split,
        test_manifest_hash_and_required_fields_present,
        test_no_filter_diagnostic_status,
        test_checkpoint_and_uptake_metadata_present,
        test_no_paper_artifacts_are_written,
        test_formal_placeholder_rows_are_rejected_by_runner,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} smoke study row tests")


if __name__ == "__main__":
    main()

