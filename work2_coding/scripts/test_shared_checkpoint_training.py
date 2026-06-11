import json
import subprocess
import sys
from argparse import Namespace
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.config import Config  # noqa: E402
from Src.experiment_contracts import load_manifest, resolve_policy_args  # noqa: E402
from Src.study_execution import sha256_file  # noqa: E402


def run_command(args):
    return subprocess.run(args, cwd=str(ROOT), text=True, capture_output=True)


def _load_via_model(checkpoint_path):
    manifest = load_manifest("pilot_attention_dspo")
    args = resolve_policy_args(manifest, manifest["splits"][0], manifest["policies"][0])
    args.update({
        "checkpoint_path": str(checkpoint_path),
        "require_checkpoint": True,
        "allow_checkpoint_mismatch": False,
        "run_mode": "pilot",
        "run_id": "shared-checkpoint-test",
        "save_model": False,
        "eval_only": True,
        "freeze_learning": True,
        "log_output": "file",
    })
    original_stdout = sys.stdout
    try:
        config = Config(Namespace(**args))
        model = config.algo(config=config)
        status = model.load_checkpoint(
            checkpoint_path=str(checkpoint_path),
            require_checkpoint=True,
            allow_checkpoint_mismatch=False,
            run_mode="pilot",
        )
    finally:
        sys.stdout = original_stdout
    return status


def test_train_shared_checkpoint_writes_sidecar_and_loads():
    with TemporaryDirectory() as tmp:
        checkpoint_path = Path(tmp) / "supervised_ml.pt"
        result = run_command([
            sys.executable,
            "scripts/train_shared_checkpoint.py",
            "--study",
            "pilot_attention_dspo",
            "--checkpoint-path",
            str(checkpoint_path),
            "--epochs",
            "3",
            "--samples",
            "32",
            "--seed",
            "777",
            "--allow-dirty",
        ])
        assert result.returncode == 0, result.stderr
        sidecar_path = checkpoint_path.with_suffix(checkpoint_path.suffix + ".sidecar.json")
        assert checkpoint_path.exists()
        assert sidecar_path.exists()
        sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))
        assert sidecar["status"] == "completed"
        assert sidecar["placeholder"] is False
        assert sidecar["weights_changed"] is True
        assert sidecar["checkpoint_sha256"] == sha256_file(checkpoint_path)
        assert sidecar["training_args"]["seed"] == 777
        assert sidecar["training_data_source"] == "deterministic_synthetic_proxy"
        status = _load_via_model(checkpoint_path)
        assert status["checkpoint_load_status"] == "loaded"
        assert status["checkpoint_hash"] == sidecar["checkpoint_sha256"]
        assert status["checkpoint_required"] is True


def main():
    tests = [
        test_train_shared_checkpoint_writes_sidecar_and_loads,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} shared checkpoint training tests")


if __name__ == "__main__":
    main()

