import io
import json
from contextlib import redirect_stderr
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

import build_work2_phase6_redesign_formal_artifacts as gate


TAGS = [
    "nearest_L",
    "cost_L",
    "cnn_menu",
    "expected_profit_enumeration",
    "service_constrained_expected_profit",
    "risk_lambda_200",
    "risk_lambda_400",
    "min_quit_tol000",
    "min_quit_tol001",
    "min_quit_tol003",
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
        "episodes": 50,
        "net_profit": 100.0,
        "service_constrained_net_profit": 100.0,
        "opt_out_rate": 0.30,
        "acceptance_rate": 0.70,
        "checkpoint_path": "outputs/shared_training/test/supervised_ml.pt",
        "checkpoint_reused": True,
        "checkpoint_source": "existing_checkpoint",
        "redesign_fallback_rate": 0.0,
        "avg_redesign_predicted_outside_probability": 0.25,
        "avg_redesign_predicted_expected_system_profit": 10.0,
        "avg_redesign_score": 5.0,
    }
    if tag == "nearest_L":
        base.update({"service_constrained_net_profit": 90.0, "net_profit": 90.0, "opt_out_rate": 0.34})
    elif tag == "cost_L":
        base.update({"service_constrained_net_profit": 100.0, "net_profit": 100.0, "opt_out_rate": 0.30})
    elif tag == "cnn_menu":
        base.update({"service_constrained_net_profit": 95.0, "net_profit": 95.0, "opt_out_rate": 0.32})
    elif tag.startswith("risk_lambda_"):
        base.update({"service_constrained_net_profit": 120.0, "net_profit": 122.0, "opt_out_rate": 0.25})
    elif tag.startswith("min_quit_tol"):
        base.update({"service_constrained_net_profit": 112.0, "net_profit": 113.0, "opt_out_rate": 0.24})
    elif tag in {"cost_oracle", "profit_oracle"}:
        base.update({"service_constrained_net_profit": 130.0, "net_profit": 130.0, "opt_out_rate": 0.20})
    if tag not in gate.FORMAL_CANDIDATE_TAGS:
        base.update({
            "redesign_fallback_rate": 0.0,
            "avg_redesign_predicted_outside_probability": None,
            "avg_redesign_predicted_expected_system_profit": None,
            "avg_redesign_score": None,
        })
    if overrides:
        base.update(overrides)
    return base


def make_rows(overrides=None, omit=None, duplicate=None, extra=None):
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
    if extra:
        rows.extend(extra)
    return rows


def write_study(tmp_path, rows, completed=5):
    study_dir = tmp_path / "outputs" / "studies" / gate.STUDY_NAME / "test_run"
    study_dir.mkdir(parents=True)
    summary = {
        "study": {"name": gate.STUDY_NAME, "manifest_hash": "abc123"},
        "run_metadata": {
            "run_id": "test_run",
            "status": "completed",
            "completed_splits": completed,
            "expected_splits": 5,
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


def read_gate_text(out_dir):
    return (out_dir / "formal_gate.md").read_text(encoding="utf-8")


def test_missing_explicit_input_fails():
    try:
        with redirect_stderr(io.StringIO()):
            gate.parse_args([])
    except SystemExit:
        return
    raise AssertionError("missing explicit input must fail")


def test_formal_support_fixture():
    with TemporaryDirectory() as tmp:
        study_dir = write_study(Path(tmp), make_rows())
        out_dir = Path(tmp) / "out"
        result = gate.run(["--study-dir", str(study_dir), "--output-dir", str(out_dir)])
        assert result["decision_state"] == "formal_support", result
        assert result["manuscript_artifacts_unlocked"] is True, result
        assert set(gate.REQUIRED_OUTPUTS) == {path.name for path in out_dir.iterdir()}
        text = read_gate_text(out_dir)
        assert text.count("decision_state:") == 1
        assert "manuscript_artifacts_unlocked: true" in text


def test_mixed_support_fixture():
    overrides = {
        "risk_lambda_200": {"service_constrained_net_profit": 90.0, "net_profit": 90.0, "opt_out_rate": 0.20},
        "risk_lambda_400": {"service_constrained_net_profit": 92.0, "net_profit": 92.0, "opt_out_rate": 0.20},
        "min_quit_tol000": {"service_constrained_net_profit": 91.0, "net_profit": 91.0, "opt_out_rate": 0.21},
        "min_quit_tol001": {"service_constrained_net_profit": 91.0, "net_profit": 91.0, "opt_out_rate": 0.21},
        "min_quit_tol003": {"service_constrained_net_profit": 91.0, "net_profit": 91.0, "opt_out_rate": 0.21},
    }
    with TemporaryDirectory() as tmp:
        study_dir = write_study(Path(tmp), make_rows(overrides))
        out_dir = Path(tmp) / "out"
        result = gate.run(["--study-dir", str(study_dir), "--output-dir", str(out_dir)])
        assert result["decision_state"] == "mixed_support", result
        assert result["manuscript_artifacts_unlocked"] is False, result
        assert "manuscript_artifacts_unlocked: false" in read_gate_text(out_dir)


def test_no_support_fixture():
    overrides = {
        "risk_lambda_200": {"service_constrained_net_profit": 80.0, "net_profit": 80.0, "opt_out_rate": 0.50},
        "risk_lambda_400": {"service_constrained_net_profit": 80.0, "net_profit": 80.0, "opt_out_rate": 0.50},
        "min_quit_tol000": {"service_constrained_net_profit": 82.0, "net_profit": 82.0, "opt_out_rate": 0.48},
        "min_quit_tol001": {"service_constrained_net_profit": 82.0, "net_profit": 82.0, "opt_out_rate": 0.48},
        "min_quit_tol003": {"service_constrained_net_profit": 82.0, "net_profit": 82.0, "opt_out_rate": 0.48},
    }
    with TemporaryDirectory() as tmp:
        study_dir = write_study(Path(tmp), make_rows(overrides))
        out_dir = Path(tmp) / "out"
        result = gate.run(["--study-dir", str(study_dir), "--output-dir", str(out_dir)])
        assert result["decision_state"] == "no_support", result
        assert result["manuscript_artifacts_unlocked"] is False, result


def test_missing_row_fails_closed():
    with TemporaryDirectory() as tmp:
        study_dir = write_study(Path(tmp), make_rows(omit={(2, "risk_lambda_200")}))
        expect_gate_error(["--study-dir", str(study_dir), "--output-dir", str(Path(tmp) / "out")])


def test_duplicate_row_fails_closed():
    with TemporaryDirectory() as tmp:
        study_dir = write_study(Path(tmp), make_rows(duplicate=(1, "cnn_menu")))
        expect_gate_error(["--study-dir", str(study_dir), "--output-dir", str(Path(tmp) / "out")])


def test_incomplete_seed_count_fails_closed():
    with TemporaryDirectory() as tmp:
        study_dir = write_study(Path(tmp), make_rows(), completed=4)
        expect_gate_error(["--study-dir", str(study_dir), "--output-dir", str(Path(tmp) / "out")])


def test_bad_numeric_metric_fails_closed():
    with TemporaryDirectory() as tmp:
        study_dir = write_study(Path(tmp), make_rows(overrides={(0, "cost_L"): {"net_profit": "nan"}}))
        expect_gate_error(["--study-dir", str(study_dir), "--output-dir", str(Path(tmp) / "out")])


def test_all_baseline_primary_metrics_unavailable_fails_closed_to_no_support():
    overrides = {
        "nearest_L": {"service_constrained_net_profit": None},
        "cost_L": {"service_constrained_net_profit": None},
        "cnn_menu": {"service_constrained_net_profit": None},
    }
    with TemporaryDirectory() as tmp:
        study_dir = write_study(Path(tmp), make_rows(overrides))
        out_dir = Path(tmp) / "out"
        result = gate.run(["--study-dir", str(study_dir), "--output-dir", str(out_dir)])
        assert result["decision_state"] == "no_support", result
        assert "manuscript_artifacts_unlocked: false" in read_gate_text(out_dir)


def test_service_guarded_row_present_fails_closed():
    with TemporaryDirectory() as tmp:
        extra = [make_row(0, "service_guarded_diagnostic")]
        study_dir = write_study(Path(tmp), make_rows(extra=extra))
        expect_gate_error(["--study-dir", str(study_dir), "--output-dir", str(Path(tmp) / "out")])


def test_refuses_artifact_and_manuscript_outputs():
    with TemporaryDirectory() as tmp:
        study_dir = write_study(Path(tmp), make_rows())
        expect_gate_error(["--study-dir", str(study_dir), "--output-dir", str(gate.FORMAL_ARTIFACTS_DIR)])
        expect_gate_error(["--study-dir", str(study_dir), "--output-dir", str(gate.MANUSCRIPT_DIR)])


def main():
    tests = [
        test_missing_explicit_input_fails,
        test_formal_support_fixture,
        test_mixed_support_fixture,
        test_no_support_fixture,
        test_missing_row_fails_closed,
        test_duplicate_row_fails_closed,
        test_incomplete_seed_count_fails_closed,
        test_bad_numeric_metric_fails_closed,
        test_all_baseline_primary_metrics_unavailable_fails_closed_to_no_support,
        test_service_guarded_row_present_fails_closed,
        test_refuses_artifact_and_manuscript_outputs,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} Phase 6 redesign formal gate tests")


if __name__ == "__main__":
    main()
