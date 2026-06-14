import json
import sys
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.experiment_contracts import load_manifest, manifest_hash  # noqa: E402
from Src.formal_readiness import FORMAL_CHECKPOINT_COMMAND, check_formal_readiness  # noqa: E402
from Src.study_execution import sha256_file  # noqa: E402
from scripts.train_shared_checkpoint import train_checkpoint, write_sidecar  # noqa: E402


def _temp_formal_manifest(checkpoint_path):
    manifest = deepcopy(load_manifest("formal_robust_menu"))
    manifest["shared_checkpoint"]["path"] = str(checkpoint_path)
    manifest["base_args"]["checkpoint_path"] = str(checkpoint_path)
    return manifest


def test_missing_checkpoint_writes_blocked_reports_and_command():
    with TemporaryDirectory() as tmp:
        checkpoint_path = Path(tmp) / "missing" / "supervised_ml.pt"
        report = check_formal_readiness(
            study=_temp_formal_manifest(checkpoint_path),
            output_root=Path(tmp) / "readiness",
            allow_dirty=True,
            command="test readiness",
        )
        assert report["status"] == "blocked"
        assert report["claim_ready_allowed"] is False
        assert any(item["code"] == "missing_formal_checkpoint" for item in report["blockers"])
        assert FORMAL_CHECKPOINT_COMMAND in json.dumps(report)
        assert Path(report["reports"]["json"]).exists()
        assert Path(report["reports"]["markdown"]).exists()
        assert Path(report["dependency_snapshot"]["path"]).exists()
        assert report["dependency_snapshot"]["hash"] == sha256_file(report["dependency_snapshot"]["path"])


def test_existing_checkpoint_records_loaded_probe_and_hash():
    with TemporaryDirectory() as tmp:
        checkpoint_path = Path(tmp) / "shared" / "supervised_ml.pt"
        manifest = _temp_formal_manifest(checkpoint_path)
        result = train_checkpoint(manifest, checkpoint_path, epochs=2, samples=16, seed=99)
        write_sidecar(
            checkpoint_path.with_suffix(checkpoint_path.suffix + ".sidecar.json"),
            manifest,
            checkpoint_path,
            result,
            command="test training",
            allow_dirty=True,
        )

        report = check_formal_readiness(
            study=manifest,
            output_root=Path(tmp) / "readiness",
            allow_dirty=True,
            command="test readiness",
        )
        assert report["status"] == "passed"
        assert report["checkpoint"]["load_status"] == "loaded"
        assert report["checkpoint"]["hash"] == sha256_file(checkpoint_path)
        assert report["checkpoint"]["sidecar_hash"]
        probe = report["checkpoint"]["row_metadata_probe"]
        assert probe["checkpoint_load_status"] == "loaded"
        assert probe["checkpoint_hash"] == report["checkpoint"]["hash"]
        assert probe["placeholder_only"] is False


def test_dirty_git_blocks_without_allow_dirty():
    with TemporaryDirectory() as tmp:
        dirty_marker = ROOT / ".tmp_dirty_readiness_test"
        dirty_marker.write_text("temporary dirty marker for readiness test\n", encoding="utf-8")
        checkpoint_path = Path(tmp) / "missing" / "supervised_ml.pt"
        try:
            report = check_formal_readiness(
                study=_temp_formal_manifest(checkpoint_path),
                output_root=Path(tmp) / "readiness",
                allow_dirty=False,
                command="test readiness",
            )
            codes = {item["code"] for item in report["blockers"]}
            assert "dirty_git" in codes
        finally:
            dirty_marker.unlink(missing_ok=True)


def test_manifest_hash_is_recorded():
    with TemporaryDirectory() as tmp:
        checkpoint_path = Path(tmp) / "missing" / "supervised_ml.pt"
        manifest = _temp_formal_manifest(checkpoint_path)
        report = check_formal_readiness(
            study=manifest,
            output_root=Path(tmp) / "readiness",
            allow_dirty=True,
            command="test readiness",
        )
        assert report["manifest"]["hash"] == manifest_hash(manifest)
        assert report["settings"]["settings_hash"]


def main():
    tests = [
        test_missing_checkpoint_writes_blocked_reports_and_command,
        test_existing_checkpoint_records_loaded_probe_and_hash,
        test_dirty_git_blocks_without_allow_dirty,
        test_manifest_hash_is_recorded,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} formal readiness tests")


if __name__ == "__main__":
    main()
