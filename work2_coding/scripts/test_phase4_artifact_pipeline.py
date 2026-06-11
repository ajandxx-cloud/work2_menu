import json
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]


def test_pipeline_creates_mirrored_artifacts_and_status():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        result = subprocess.run(
            [
                sys.executable,
                "scripts/run_phase4_artifacts.py",
                "--study",
                "pilot_robust_menu",
                "--allow-incomplete",
                "--skip-formal",
                "--output-root",
                str(root / "outputs"),
                "--artifact-root",
                str(root / "artifacts"),
                "--mirror-root",
                str(root / "mirror" / "artifacts" / "work2_robust_menu"),
                "--max-policies",
                "2",
            ],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            check=True,
        )
        payload = json.loads(result.stdout)
        artifact_status = root / "artifacts" / "ARTIFACT_STATUS.json"
        mirror_status = root / "mirror" / "artifacts" / "work2_robust_menu" / "ARTIFACT_STATUS.json"
        assert artifact_status.exists()
        assert mirror_status.exists()
        status = json.loads(artifact_status.read_text(encoding="utf-8"))
        assert status["claim_ready"] is False
        assert status["formal_claim_ready"] is False
        assert status["phase4_pipeline"]["formal_blockers"][0]["code"] == "formal_skipped"
        assert status["phase4_pipeline"]["run_dir"]
        assert payload["mirror_root"].endswith("artifacts/work2_robust_menu") or "work2_robust_menu" in payload["mirror_root"]
        mirrored_files = {path.name for path in mirror_status.parent.rglob("*") if path.is_file()}
        assert "policy_summary.json" in mirrored_files
        assert "policy_summary.tex" in mirrored_files
        assert "normalized_rows.json" not in mirrored_files


def test_status_reports_checkpoint_blocker_and_uptake_coverage():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        subprocess.run(
            [
                sys.executable,
                "scripts/run_phase4_artifacts.py",
                "--study",
                "pilot_robust_menu",
                "--allow-incomplete",
                "--skip-formal",
                "--output-root",
                str(root / "outputs"),
                "--artifact-root",
                str(root / "artifacts"),
                "--mirror-root",
                str(root / "mirror"),
                "--max-policies",
                "1",
            ],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            check=True,
        )
        status = json.loads((root / "artifacts" / "ARTIFACT_STATUS.json").read_text(encoding="utf-8"))
        assert status["artifact_status"]["status"] == "blocked"
        assert "failed" in status["checkpoint_statuses"]
        assert status["uptake_regimes"]
        blockers = status.get("blockers", []) + status["artifact_status"].get("blockers", [])
        assert any(item.get("code") == "missing_checkpoint_file" for item in blockers)


def main():
    tests = [
        test_pipeline_creates_mirrored_artifacts_and_status,
        test_status_reports_checkpoint_blocker_and_uptake_coverage,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} Phase 4 artifact pipeline tests")


if __name__ == "__main__":
    main()

