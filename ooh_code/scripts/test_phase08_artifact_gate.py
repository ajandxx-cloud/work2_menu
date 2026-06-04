import json
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

import build_phase08_artifacts as phase08


REQUIRED_TAGS = phase08.REQUIRED_TAGS


def make_row(seed, tag, overrides=None):
    row = {
        "study_name": phase08.PILOT_STUDY_NAME,
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
        "home_always_shown": True,
        "is_reference": False,
        "net_profit": 100.0,
        "adjusted_profit": 100.0,
        "service_constrained_net_profit": 100.0,
        "opt_out_rate": 0.1,
        "service_quit_rate_guardrail": 0.4,
        "service_guardrail_pass": True,
        "service_guardrail_violation": False,
        "avg_exact_enumerated_menu_count": 120.0 if tag in phase08.NEW_METHOD_TAGS else 0.0,
        "service_constrained_fallback_rate": 0.0,
    }
    if tag == "cost_L":
        row["service_constrained_net_profit"] = 110.0
    if tag == "cnn_menu":
        row["service_constrained_net_profit"] = 105.0
    if tag == "expected_profit_enumeration":
        row["service_constrained_net_profit"] = 130.0
    if tag == "service_constrained_expected_profit":
        row["service_constrained_net_profit"] = 125.0
    if tag == "profit_oracle":
        row["service_constrained_net_profit"] = 150.0
    row["adjusted_profit"] = row["service_constrained_net_profit"]
    row["net_profit"] = row["service_constrained_net_profit"]
    if overrides:
        row.update(overrides)
    return row


def make_rows(row_overrides=None, omit=None, duplicate=None):
    row_overrides = row_overrides or {}
    omit = set(omit or [])
    rows = []
    for seed in phase08.EXPECTED_SEEDS:
        for tag in REQUIRED_TAGS:
            if (seed, tag) in omit:
                continue
            row = make_row(seed, tag, row_overrides.get((seed, tag)) or row_overrides.get(tag))
            rows.append(row)
            if duplicate == (seed, tag):
                rows.append(deepcopy(row))
    return rows


def write_study(tmp_path, rows, status="completed"):
    study_dir = tmp_path / "outputs" / "studies" / phase08.PILOT_STUDY_NAME / "test_run"
    study_dir.mkdir(parents=True)
    summary = {
        "study": {
            "name": phase08.PILOT_STUDY_NAME,
            "manifest_hash": "abc123",
        },
        "run_metadata": {
            "run_id": "test_run",
            "status": status,
            "completed_splits": 3,
            "expected_splits": 3,
            "study_root": str(study_dir.resolve()),
        },
    }
    (study_dir / "study_summary.json").write_text(json.dumps(summary), encoding="utf-8")
    (study_dir / "normalized_rows.json").write_text(json.dumps(rows), encoding="utf-8")
    return study_dir


def expect_gate_error(args):
    try:
        phase08.run(args)
    except phase08.GateError:
        return
    raise AssertionError("expected GateError")


def test_missing_explicit_input_fails():
    try:
        phase08.parse_args([])
    except SystemExit:
        return
    raise AssertionError("missing explicit input must fail")


def test_complete_pass_writes_phase_local_artifacts():
    with TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        study_dir = write_study(tmp_path, make_rows())
        out_dir = tmp_path / "phase08_artifacts"
        result = phase08.run(["--study-dir", str(study_dir), "--output-dir", str(out_dir)])
        assert result["decision_state"] == "proceed_to_formal", result
        assert result["human_confirmation_required"] is True, result
        expected = {
            "pilot_rows.csv",
            "pilot_summary.md",
            "oracle_diagnostics.md",
            "profit_vs_quit_tradeoff.md",
            "phase08_decision.md",
        }
        assert expected == {path.name for path in out_dir.iterdir()}
        decision = (out_dir / "phase08_decision.md").read_text(encoding="utf-8")
        assert decision.count("decision_state:") == 1
        assert "human_confirmation_required: true" in decision


def test_refuses_formal_artifact_output():
    with TemporaryDirectory() as tmp:
        study_dir = write_study(Path(tmp), make_rows())
        expect_gate_error(["--study-dir", str(study_dir), "--output-dir", str(phase08.FORMAL_ARTIFACTS_DIR)])


def test_missing_seed_fails():
    with TemporaryDirectory() as tmp:
        study_dir = write_study(Path(tmp), make_rows(omit={(2, "cost_L")}))
        expect_gate_error(["--study-dir", str(study_dir), "--output-dir", str(Path(tmp) / "out")])


def test_missing_policy_fails():
    with TemporaryDirectory() as tmp:
        rows = [row for row in make_rows() if row["variant_tag"] != "profit_oracle"]
        study_dir = write_study(Path(tmp), rows)
        expect_gate_error(["--study-dir", str(study_dir), "--output-dir", str(Path(tmp) / "out")])


def test_missing_metric_fails():
    with TemporaryDirectory() as tmp:
        rows = make_rows({"expected_profit_enumeration": {"adjusted_profit": None}})
        study_dir = write_study(Path(tmp), rows)
        expect_gate_error(["--study-dir", str(study_dir), "--output-dir", str(Path(tmp) / "out")])


def test_null_service_profit_with_pass_fails():
    with TemporaryDirectory() as tmp:
        rows = make_rows({"expected_profit_enumeration": {"service_constrained_net_profit": None}})
        study_dir = write_study(Path(tmp), rows)
        expect_gate_error(["--study-dir", str(study_dir), "--output-dir", str(Path(tmp) / "out")])


def test_guardrail_violation_blocks_proceed():
    with TemporaryDirectory() as tmp:
        rows = make_rows(
            {
                "expected_profit_enumeration": {
                    "opt_out_rate": 0.5,
                    "service_guardrail_pass": False,
                    "service_guardrail_violation": True,
                    "service_constrained_net_profit": None,
                }
            }
        )
        study_dir = write_study(Path(tmp), rows)
        out_dir = Path(tmp) / "out"
        result = phase08.run(["--study-dir", str(study_dir), "--output-dir", str(out_dir)])
        assert result["decision_state"] == "recalibrate_objective", result
        assert result["human_confirmation_required"] is False, result


def test_duplicate_policy_seed_fails():
    with TemporaryDirectory() as tmp:
        study_dir = write_study(Path(tmp), make_rows(duplicate=(1, "cnn_menu")))
        expect_gate_error(["--study-dir", str(study_dir), "--output-dir", str(Path(tmp) / "out")])


def main():
    tests = [
        test_missing_explicit_input_fails,
        test_complete_pass_writes_phase_local_artifacts,
        test_refuses_formal_artifact_output,
        test_missing_seed_fails,
        test_missing_policy_fails,
        test_missing_metric_fails,
        test_null_service_profit_with_pass_fails,
        test_guardrail_violation_blocks_proceed,
        test_duplicate_policy_seed_fails,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} Phase08 artifact gate tests")


if __name__ == "__main__":
    main()
