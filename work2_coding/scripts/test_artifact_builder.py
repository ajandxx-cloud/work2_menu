import json
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.artifact_builder import aggregate_by_policy, build_artifacts  # noqa: E402


def run_smoke(output_root):
    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_study.py",
            "--study",
            "smoke_robust_menu",
            "--contract-only",
            "--output-root",
            str(output_root),
        ],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=True,
    )
    return Path(result.stdout.strip().splitlines()[-1])


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_aggregate_preserves_counts_and_diagnostic_label():
    with TemporaryDirectory() as tmp:
        run_dir = run_smoke(Path(tmp) / "outputs")
        rows = load_json(run_dir / "normalized_rows.json")
        aggregates = aggregate_by_policy(rows)
        assert sum(row["row_count"] for row in aggregates) == len(rows)
        no_filter = [row for row in aggregates if row["policy_tag"] == "no_filter_diagnostic"][0]
        assert no_filter["diagnostic"] is True
        assert no_filter["rank_eligible"] is False


def test_build_writes_json_csv_tables_and_status_files():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        run_dir = run_smoke(root / "outputs")
        result = build_artifacts(run_dir, output_root=root / "artifacts", allow_incomplete=True)
        output_root = Path(result["output_root"])
        assert (output_root / "aggregates" / "policy_summary.json").exists()
        assert (output_root / "aggregates" / "policy_summary.csv").exists()
        assert (output_root / "tables" / "policy_summary.tex").exists()
        assert (output_root / "tables" / "robust_filtering.tex").exists()
        assert (output_root / "tables" / "exact_greedy.tex").exists()
        assert (output_root / "tables" / "uptake_regime.tex").exists()
        assert (output_root / "tables" / "provenance_status.tex").exists()
        assert (output_root / "ARTIFACT_STATUS.json").exists()
        assert (output_root / "aggregates" / "policy_summary.json.metadata.json").exists()
        table = (output_root / "tables" / "robust_filtering.tex").read_text(encoding="utf-8")
        assert "no\\_filter\\_diagnostic" in table


def test_metric_poor_rows_write_incomplete_figure_status():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        run_dir = run_smoke(root / "outputs")
        build_artifacts(run_dir, output_root=root / "artifacts", allow_incomplete=True)
        status_path = root / "artifacts" / "figures" / "acceptance_optout.png.status.json"
        assert status_path.exists()
        status = load_json(status_path)
        assert status["figure_status"] == "incomplete"
        assert "acceptance_rate" in status["missing_reason"]


def test_cli_builds_from_explicit_run_dir_and_mirrors_lightweight_files():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        run_dir = run_smoke(root / "outputs")
        result = subprocess.run(
            [
                sys.executable,
                "scripts/build_artifacts.py",
                "--run-dir",
                str(run_dir),
                "--output-root",
                str(root / "artifacts"),
                "--mirror-root",
                str(root / "mirror"),
                "--allow-incomplete",
            ],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            check=True,
        )
        payload = json.loads(result.stdout)
        assert Path(payload["status_path"]).exists()
        assert (root / "mirror" / "ARTIFACT_STATUS.json").exists()
        mirrored = {path.name for path in (root / "mirror").rglob("*") if path.is_file()}
        assert "normalized_rows.json" not in mirrored
        assert "policy_summary.tex" in mirrored


def test_cli_builds_from_latest_study():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        run_smoke(root / "outputs")
        result = subprocess.run(
            [
                sys.executable,
                "scripts/build_artifacts.py",
                "--study",
                "smoke_robust_menu",
                "--study-output-root",
                str(root / "outputs"),
                "--output-root",
                str(root / "artifacts"),
                "--allow-incomplete",
            ],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            check=True,
        )
        payload = json.loads(result.stdout)
        assert payload["artifact_status"]["status"] == "incomplete"


def main():
    tests = [
        test_aggregate_preserves_counts_and_diagnostic_label,
        test_build_writes_json_csv_tables_and_status_files,
        test_metric_poor_rows_write_incomplete_figure_status,
        test_cli_builds_from_explicit_run_dir_and_mirrors_lightweight_files,
        test_cli_builds_from_latest_study,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} artifact builder tests")


if __name__ == "__main__":
    main()

