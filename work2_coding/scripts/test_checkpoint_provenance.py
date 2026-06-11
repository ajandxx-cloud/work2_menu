import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import torch

from Src.Algorithms.Agent import Agent
from Src.parser import Parser
from Src.Utils.Predictors import LinReg
from Src.Utils.Utils import default_checkpoint_metadata


def test_parser_checkpoint_flags():
    args = Parser().get_parser().parse_args([
        "--run_mode", "formal",
        "--require_checkpoint", "True",
        "--checkpoint_path", "dummy.pt",
        "--run_id", "run-123",
    ])
    assert args.run_mode == "formal"
    assert args.require_checkpoint is True
    assert args.checkpoint_path == "dummy.pt"
    assert args.run_id == "run-123"


def test_successful_predictor_load_records_hash():
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / "linreg.pt"
        source = LinReg(4)
        source.save(str(path))

        target = LinReg(4)
        status = target.load(str(path), required=True, run_mode="pilot")
        assert status["checkpoint_load_status"] == "loaded"
        assert status["checkpoint_path"] == str(path)
        assert status["checkpoint_hash"]
        assert status["checkpoint_model_type"] == "LinReg"
        assert status["checkpoint_required"] is True


def test_missing_checkpoint_is_explicit_diagnostic_failure():
    model = LinReg(4)
    status = model.load("missing-does-not-exist.pt", required=False, run_mode="diagnostic")
    assert status["checkpoint_load_status"] == "failed"
    assert "not found" in status["checkpoint_load_error"]
    assert status["checkpoint_required"] is False


def test_missing_formal_required_checkpoint_raises():
    model = LinReg(4)
    try:
        model.load("missing-does-not-exist.pt", required=True, run_mode="formal")
    except FileNotFoundError:
        return
    raise AssertionError("formal required missing checkpoint should raise")


def test_intentional_mismatch_is_diagnostic_only():
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / "linreg.pt"
        LinReg(4, output_dim=1).save(str(path))

        mismatched = LinReg(4, output_dim=2)
        status = mismatched.load(
            str(path),
            required=False,
            allow_mismatch=True,
            run_mode="diagnostic",
        )
        assert status["checkpoint_load_status"] == "intentional_mismatch"
        assert status["checkpoint_intentional_mismatch"] is True
        assert status["checkpoint_hash"]

        formal = LinReg(4, output_dim=2)
        try:
            formal.load(
                str(path),
                required=False,
                allow_mismatch=True,
                run_mode="formal",
            )
        except ValueError:
            return
    raise AssertionError("formal intentional mismatch should be blocked")


def test_agent_load_checkpoint_updates_config_metadata():
    with TemporaryDirectory() as tmp:
        checkpoint_dir = Path(tmp)
        source = LinReg(4)
        source.save(str(checkpoint_dir / "supervised_ml.pt"))

        config = SimpleNamespace(
            checkpoint_path=str(checkpoint_dir),
            require_checkpoint=True,
            allow_checkpoint_mismatch=False,
            run_mode="pilot",
            run_id="agent-test",
            algo_name="DSPO_Menu",
            checkpoint_metadata=default_checkpoint_metadata(),
        )
        agent = Agent(config)
        agent.modules = [("supervised_ml", LinReg(4))]
        status = agent.load_checkpoint()

        assert status["checkpoint_load_status"] == "loaded"
        assert status["modules"]["supervised_ml"]["checkpoint_load_status"] == "loaded"
        assert config.checkpoint_metadata["checkpoint_load_status"] == "loaded"
        assert config.checkpoint_metadata["run_id"] == "agent-test"


def main():
    tests = [
        test_parser_checkpoint_flags,
        test_successful_predictor_load_records_hash,
        test_missing_checkpoint_is_explicit_diagnostic_failure,
        test_missing_formal_required_checkpoint_raises,
        test_intentional_mismatch_is_diagnostic_only,
        test_agent_load_checkpoint_updates_config_metadata,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} checkpoint provenance tests")


if __name__ == "__main__":
    main()
