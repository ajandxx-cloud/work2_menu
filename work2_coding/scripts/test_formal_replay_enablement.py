import copy
import json
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.experiment_contracts import load_manifest, manifest_hash  # noqa: E402
from Src.paired_replay import build_normalized_row, resolve_paired_settings  # noqa: E402


def run_command(args):
    return subprocess.run(args, cwd=str(ROOT), text=True, capture_output=True)


def _last_stdout_path(result):
    return Path(result.stdout.strip().splitlines()[-1])


def _tiny_formal_manifest(tmp, checkpoint_path):
    manifest = copy.deepcopy(load_manifest("formal_attention_dspo"))
    manifest["name"] = "formal_attention_enablement_fixture"
    manifest["description"] = "Tiny formal fixture for strict actual replay enablement tests."
    manifest["shared_checkpoint"]["path"] = str(checkpoint_path)
    manifest["base_args"].update({
        "max_episodes": 1,
        "max_steps_r": 2,
        "max_steps_p": 0.95,
        "hgs_reopt_time": 0.05,
        "hgs_final_time": 0.05,
        "checkpoint_path": str(checkpoint_path),
    })
    manifest["splits"] = [
        {
            "split_id": "formal_enablement_low_seed0",
            "seed": 511,
            "data_seed": 0,
            "data_seed_test": 1,
            "uptake_regime": "low",
            "args_overrides": {
                "home_util": 3.8,
                "base_util": -2.8,
                "incentive_sens": -0.18,
            },
        },
        {
            "split_id": "formal_enablement_medium_seed1",
            "seed": 512,
            "data_seed": 1,
            "data_seed_test": 0,
            "uptake_regime": "medium",
            "args_overrides": {
                "home_util": 3.2,
                "base_util": -2.0,
                "incentive_sens": -0.25,
            },
        },
    ]
    manifest.pop("_path", None)
    path = Path(tmp) / "formal_attention_enablement_fixture.yaml"
    path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    return path


def _train_temp_checkpoint(tmp, manifest_path):
    checkpoint_path = Path(tmp) / "shared" / "formal" / "supervised_ml.pt"
    train = run_command([
        sys.executable,
        "scripts/train_shared_checkpoint.py",
        "--study",
        str(manifest_path),
        "--checkpoint-path",
        str(checkpoint_path),
        "--epochs",
        "3",
        "--samples",
        "32",
        "--seed",
        "999",
        "--allow-dirty",
    ])
    assert train.returncode == 0, train.stderr
    return checkpoint_path


def test_formal_contract_only_rejects_placeholder_rows():
    result = run_command([
        sys.executable,
        "scripts/run_study.py",
        "--study",
        "formal_attention_dspo",
        "--contract-only",
    ])
    assert result.returncode != 0
    assert "formal studies cannot emit placeholder" in (result.stderr + result.stdout)


def test_formal_missing_checkpoint_writes_blocker_metadata():
    with TemporaryDirectory() as tmp:
        missing_checkpoint = Path(tmp) / "missing" / "supervised_ml.pt"
        manifest_path = _tiny_formal_manifest(tmp, missing_checkpoint)
        result = run_command([
            sys.executable,
            "scripts/run_study.py",
            "--study",
            str(manifest_path),
            "--execute",
            "--output-root",
            str(Path(tmp) / "runs"),
        ])
        assert result.returncode == 0, result.stderr
        run_dir = _last_stdout_path(result)
        summary = json.loads((run_dir / "study_summary.json").read_text(encoding="utf-8"))
        blockers = json.loads((run_dir / "blockers.json").read_text(encoding="utf-8"))["blockers"]
        assert summary["execution_status"] == "blocked"
        assert summary["row_count"] == 0
        assert summary["placeholder_only"] is True
        assert blockers[0]["code"] == "missing_checkpoint_file"
        assert blockers[0]["checkpoint_path"] == str(missing_checkpoint)


def test_formal_loaded_checkpoint_actual_replay_completes_without_placeholders():
    with TemporaryDirectory() as tmp:
        initial_manifest = _tiny_formal_manifest(tmp, Path(tmp) / "unused" / "supervised_ml.pt")
        checkpoint_path = _train_temp_checkpoint(tmp, initial_manifest)
        manifest_path = _tiny_formal_manifest(tmp, checkpoint_path)
        result = run_command([
            sys.executable,
            "scripts/run_study.py",
            "--study",
            str(manifest_path),
            "--execute",
            "--output-root",
            str(Path(tmp) / "runs"),
        ])
        assert result.returncode == 0, result.stderr
        run_dir = _last_stdout_path(result)
        rows = json.loads((run_dir / "normalized_rows.json").read_text(encoding="utf-8"))
        summary = json.loads((run_dir / "study_summary.json").read_text(encoding="utf-8"))
        assert summary["execution_status"] == "completed"
        assert summary["placeholder_only"] is False
        assert summary["row_count"] == 4
        assert summary["checkpoint_statuses"] == ["loaded"]
        assert {row["tier"] for row in rows} == {"formal"}
        assert {row["checkpoint_load_status"] for row in rows} == {"loaded"}
        assert not any(row["placeholder_only"] for row in rows)


def test_formal_placeholder_row_validation_still_fails():
    manifest = load_manifest("formal_attention_dspo")
    settings = resolve_paired_settings(manifest, manifest_hash_value=manifest_hash(manifest))
    try:
        build_normalized_row(settings[0], run_id="formal-placeholder")
    except ValueError as exc:
        assert "formal normalized rows" in str(exc)
        return
    raise AssertionError("formal placeholder rows must remain impossible")


def main():
    tests = [
        test_formal_contract_only_rejects_placeholder_rows,
        test_formal_missing_checkpoint_writes_blocker_metadata,
        test_formal_loaded_checkpoint_actual_replay_completes_without_placeholders,
        test_formal_placeholder_row_validation_still_fails,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} formal replay enablement tests")


if __name__ == "__main__":
    main()
