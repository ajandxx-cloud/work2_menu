import io
import json
from contextlib import redirect_stderr
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

import build_phase6_redesign_artifacts as gate


TAGS = [
    "nearest_L",
    "cost_L",
    "cnn_menu",
    "expected_profit_enumeration",
    "service_constrained_expected_profit",
    "risk_lambda_50",
    "risk_lambda_100",
    "risk_lambda_200",
    "risk_lambda_400",
    "min_quit_tol000",
    "min_quit_tol001",
    "min_quit_tol003",
    "service_guarded_diagnostic",
    "cost_oracle",
    "profit_oracle",
]


def make_row(seed, tag, overrides=None):
    base = {
        "study_name": gate.STUDY_NAME,
        "run_id": "test_run",
        "manifest_hash": "abc123",
        "split_id": f"seed{seed}",
        "seed": seed,
        "variant_tag": tag,
        "variant_label": tag,
        "policy": tag,
        "menu_k": 3,
        "candidate_pool_size": 10,
        "displayed_meeting_points": 3,
        "is_reference": False,
        "episodes": 20,
        "net_profit": 100.0,
        "opt_out_rate": 0.30,
        "acceptance_rate": 0.70,
        "is_behavior_non_degenerate": True,
        "menu_optout_guardrail": 0.40,
        "redesign_fallback_rate": 0.0,
        "avg_redesign_predicted_outside_probability": 0.25,
        "avg_redesign_predicted_expected_system_profit": 10.0,
        "avg_redesign_score": 5.0,
    }
    if tag == "cost_L":
        base.update({"net_profit": 100.0, "opt_out_rate": 0.30})
    elif tag == "cnn_menu":
        base.update({"net_profit": 95.0, "opt_out_rate": 0.32})
    elif str(tag).startswith("risk_lambda_"):
        base.update({"net_profit": 120.0, "opt_out_rate": 0.25})
    elif str(tag).startswith("min_quit_tol"):
        base.update({"net_profit": 112.0, "opt_out_rate": 0.24})
    elif tag == "service_guarded_diagnostic":
        base.update({"net_profit": 111.0, "opt_out_rate": 0.22})
    if tag not in gate.REDESIGNED_TAGS:
        base.update({
            "redesign_fallback_rate": 0.0,
            "avg_redesign_predicted_outside_probability": 0.0,
            "avg_redesign_predicted_expected_system_profit": 0.0,
            "avg_redesign_score": 0.0,
        })
    if overrides:
        base.update(overrides)
    return base


def make_rows(overrides=None, omit=None, duplicate=None):
    overrides = overrides or {}
    omit = set(omit or [])
    rows = []
    for seed in gate.EXPECTED_SEEDS:
        for tag in TAGS:
            key = (seed, tag)
            if key in omit:
                continue
            row = make_row(seed, tag, overrides.get(key) or overrides.get(tag))
            rows.append(row)
            if duplicate == key:
                rows.append(deepcopy(row))
    return rows


def write_study(tmp_path, rows, completed=3):
    study_dir = tmp_path / "outputs" / "studies" / gate.STUDY_NAME / "test_run"
    study_dir.mkdir(parents=True)
    summary = {
        "study": {"name": gate.STUDY_NAME, "manifest_hash": "abc123"},
        "run_metadata": {
            "run_id": "test_run",
            "status": "completed",
            "completed_splits": completed,
            "expected_splits": 3,
            "study_root": str(study_dir.resolve()),
        },
        "splits": [{"split_id": f"seed{seed}"} for seed in range(completed)],
    }
    (study_dir / "study_summary.json").write_text(json.dumps(summary), encoding="utf-8")
    (study_dir / "normalized_rows.json").write_text(json.dumps(rows), encoding="utf-8")
    (study_dir / "manifest_snapshot.yaml").write_text("name: test\n", encoding="utf-8")
    return study_dir


def expect_gate_error(args):
    try:
        gate.run(args)
    except gate.GateError:
        return
    raise AssertionError("expected GateError")


def test_missing_explicit_input_fails():
    try:
        with redirect_stderr(io.StringIO()):
            gate.parse_args([])
    except SystemExit:
        return
    raise AssertionError("missing explicit input must fail")


def test_proceed_to_formal_fixture():
    with TemporaryDirectory() as tmp:
        study_dir = write_study(Path(tmp), make_rows())
        out_dir = Path(tmp) / "out"
        result = gate.run(["--study-dir", str(study_dir), "--output-dir", str(out_dir)])
        assert result["decision_state"] == "proceed_to_formal", result
        assert result["human_confirmation_required"] is True, result
        assert set(gate.REQUIRED_OUTPUTS) == {path.name for path in out_dir.iterdir()}


def test_continue_redesign_fixture():
    overrides = {
        "risk_lambda_50": {"net_profit": 90.0, "opt_out_rate": 0.20},
        "risk_lambda_100": {"net_profit": 90.0, "opt_out_rate": 0.20},
        "risk_lambda_200": {"net_profit": 90.0, "opt_out_rate": 0.20},
        "risk_lambda_400": {"net_profit": 90.0, "opt_out_rate": 0.20},
        "min_quit_tol000": {"net_profit": 92.0, "opt_out_rate": 0.22},
        "min_quit_tol001": {"net_profit": 92.0, "opt_out_rate": 0.22},
        "min_quit_tol003": {"net_profit": 92.0, "opt_out_rate": 0.22},
        "service_guarded_diagnostic": {"net_profit": 130.0, "opt_out_rate": 0.21, "redesign_fallback_rate": 0.8},
    }
    with TemporaryDirectory() as tmp:
        study_dir = write_study(Path(tmp), make_rows(overrides))
        out_dir = Path(tmp) / "out"
        result = gate.run(["--study-dir", str(study_dir), "--output-dir", str(out_dir)])
        assert result["decision_state"] == "continue_redesign", result


def test_conclude_method_unsuitable_fixture():
    overrides = {
        "risk_lambda_50": {"net_profit": 80.0, "opt_out_rate": 0.50},
        "risk_lambda_100": {"net_profit": 80.0, "opt_out_rate": 0.50},
        "risk_lambda_200": {"net_profit": 80.0, "opt_out_rate": 0.50},
        "risk_lambda_400": {"net_profit": 80.0, "opt_out_rate": 0.50},
        "min_quit_tol000": {"net_profit": 82.0, "opt_out_rate": 0.48},
        "min_quit_tol001": {"net_profit": 82.0, "opt_out_rate": 0.48},
        "min_quit_tol003": {"net_profit": 82.0, "opt_out_rate": 0.48},
        "service_guarded_diagnostic": {"net_profit": 150.0, "opt_out_rate": 0.20, "redesign_fallback_rate": 1.0},
    }
    with TemporaryDirectory() as tmp:
        study_dir = write_study(Path(tmp), make_rows(overrides))
        out_dir = Path(tmp) / "out"
        result = gate.run(["--study-dir", str(study_dir), "--output-dir", str(out_dir)])
        assert result["decision_state"] == "conclude_method_unsuitable", result


def test_missing_rows_fail_closed():
    with TemporaryDirectory() as tmp:
        study_dir = write_study(Path(tmp), make_rows(omit={(2, "risk_lambda_200")}))
        expect_gate_error(["--study-dir", str(study_dir), "--output-dir", str(Path(tmp) / "out")])


def test_duplicate_rows_fail_closed():
    with TemporaryDirectory() as tmp:
        study_dir = write_study(Path(tmp), make_rows(duplicate=(1, "cnn_menu")))
        expect_gate_error(["--study-dir", str(study_dir), "--output-dir", str(Path(tmp) / "out")])


def test_incomplete_seeds_fail_closed():
    with TemporaryDirectory() as tmp:
        study_dir = write_study(Path(tmp), make_rows(), completed=2)
        expect_gate_error(["--study-dir", str(study_dir), "--output-dir", str(Path(tmp) / "out")])


def test_refuses_formal_and_manuscript_outputs():
    with TemporaryDirectory() as tmp:
        study_dir = write_study(Path(tmp), make_rows())
        expect_gate_error(["--study-dir", str(study_dir), "--output-dir", str(gate.FORMAL_ARTIFACTS_DIR)])
        expect_gate_error(["--study-dir", str(study_dir), "--output-dir", str(gate.MANUSCRIPT_DIR)])


def main():
    tests = [
        test_missing_explicit_input_fails,
        test_proceed_to_formal_fixture,
        test_continue_redesign_fixture,
        test_conclude_method_unsuitable_fixture,
        test_missing_rows_fail_closed,
        test_duplicate_rows_fail_closed,
        test_incomplete_seeds_fail_closed,
        test_refuses_formal_and_manuscript_outputs,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} Phase 6 redesign artifact gate tests")


if __name__ == "__main__":
    main()
