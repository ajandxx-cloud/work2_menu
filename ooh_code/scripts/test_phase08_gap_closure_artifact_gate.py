import json
import io
from copy import deepcopy
from contextlib import redirect_stderr
from pathlib import Path
from tempfile import TemporaryDirectory

import build_phase08_gap_closure_artifacts as gate


BASE_TAGS = gate.BASE_TAGS
GRID = gate.EXPECTED_GRID


def grid_id(penalty, guardrail):
    return f"p{int(penalty)}_g{int(guardrail * 10):02d}"


def make_row(seed, penalty, guardrail, base_tag, overrides=None):
    gid = grid_id(penalty, guardrail)
    row = {
        "study_name": gate.STUDY_NAME,
        "run_id": "test_run",
        "manifest_hash": "abc123",
        "split_id": f"seed{seed}",
        "seed": seed,
        "variant_tag": f"{gid}_{base_tag}",
        "variant_label": base_tag,
        "policy": base_tag,
        "menu_k": 3,
        "candidate_pool_size": 10,
        "displayed_meeting_points": 3,
        "home_always_shown": True,
        "is_reference": False,
        "net_profit": 100.0,
        "adjusted_profit": 100.0,
        "service_constrained_net_profit": 100.0,
        "opt_out_rate": 0.1,
        "service_quit_rate_guardrail": guardrail,
        "service_guardrail_pass": True,
        "service_guardrail_violation": False,
        "avg_exact_enumerated_menu_count": 120.0 if base_tag in gate.NEW_METHOD_TAGS else 0.0,
        "service_constrained_fallback_rate": 0.0,
    }
    if base_tag == "cost_L":
        row["service_constrained_net_profit"] = 110.0
    if base_tag == "cnn_menu":
        row["service_constrained_net_profit"] = 105.0
    if base_tag == "expected_profit_enumeration":
        row["service_constrained_net_profit"] = 130.0
    if base_tag == "service_constrained_expected_profit":
        row["service_constrained_net_profit"] = 125.0
    if base_tag == "profit_oracle":
        row["service_constrained_net_profit"] = 150.0
    row["adjusted_profit"] = row["service_constrained_net_profit"]
    row["net_profit"] = row["service_constrained_net_profit"]
    if overrides:
        row.update(overrides)
    return row


def make_rows(row_overrides=None, omit=None, duplicate=None, bad_tag=False):
    row_overrides = row_overrides or {}
    omit = set(omit or [])
    rows = []
    for penalty, guardrail in GRID:
        for seed in gate.EXPECTED_SEEDS:
            for base_tag in BASE_TAGS:
                key = (grid_id(penalty, guardrail), seed, base_tag)
                if key in omit:
                    continue
                row = make_row(
                    seed,
                    penalty,
                    guardrail,
                    base_tag,
                    row_overrides.get(key) or row_overrides.get(base_tag),
                )
                if bad_tag and key == ("p100_g03", 0, "cost_L"):
                    row["variant_tag"] = "bad_cost_L"
                rows.append(row)
                if duplicate == key:
                    rows.append(deepcopy(row))
    return rows


def write_study(tmp_path, rows, status="completed"):
    study_dir = tmp_path / "outputs" / "studies" / gate.STUDY_NAME / "test_run"
    study_dir.mkdir(parents=True)
    summary = {
        "study": {
            "name": gate.STUDY_NAME,
            "manifest_hash": "abc123",
        },
        "run_metadata": {
            "run_id": "test_run",
            "status": status,
            "completed_splits": 3,
            "expected_splits": 3,
            "study_root": str(study_dir.resolve()),
        },
        "splits": [{"split_id": f"seed{seed}"} for seed in gate.EXPECTED_SEEDS],
    }
    (study_dir / "study_summary.json").write_text(json.dumps(summary), encoding="utf-8")
    (study_dir / "normalized_rows.json").write_text(json.dumps(rows), encoding="utf-8")
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


def test_complete_pass_writes_phase_local_artifacts():
    with TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        study_dir = write_study(tmp_path, make_rows())
        out_dir = tmp_path / "gap_closure_artifacts"
        result = gate.run(["--study-dir", str(study_dir), "--output-dir", str(out_dir)])
        assert result["decision_state"] == "proceed_to_formal", result
        assert result["human_confirmation_required"] is True, result
        expected = {
            "gap_closure_rows.csv",
            "gap_closure_summary.md",
            "gate_decision.md",
            "objective_validity.md",
            "gap_closure_summary.json",
        }
        assert expected == {path.name for path in out_dir.iterdir()}
        decision = (out_dir / "gate_decision.md").read_text(encoding="utf-8")
        assert decision.count("decision_state:") == 1
        assert "human_confirmation_required: true" in decision


def test_refuses_formal_artifact_output():
    with TemporaryDirectory() as tmp:
        study_dir = write_study(Path(tmp), make_rows())
        expect_gate_error(["--study-dir", str(study_dir), "--output-dir", str(gate.FORMAL_ARTIFACTS_DIR)])


def test_one_passing_grid_is_enough():
    overrides = {}
    for penalty, guardrail in GRID:
        if (penalty, guardrail) != (500.0, 0.4):
            for seed in gate.EXPECTED_SEEDS:
                for base_tag in gate.NEW_METHOD_TAGS:
                    overrides[(grid_id(penalty, guardrail), seed, base_tag)] = {
                        "opt_out_rate": 0.5,
                        "service_guardrail_pass": False,
                        "service_guardrail_violation": True,
                        "service_constrained_net_profit": None,
                    }
    with TemporaryDirectory() as tmp:
        study_dir = write_study(Path(tmp), make_rows(overrides))
        out_dir = Path(tmp) / "out"
        result = gate.run(["--study-dir", str(study_dir), "--output-dir", str(out_dir)])
        assert result["decision_state"] == "proceed_to_formal", result
        assert result["selected_grid"] == "p500_g04", result


def test_all_grids_fail_closed():
    overrides = {
        "expected_profit_enumeration": {
            "opt_out_rate": 0.5,
            "service_guardrail_pass": False,
            "service_guardrail_violation": True,
            "service_constrained_net_profit": None,
        },
        "service_constrained_expected_profit": {
            "opt_out_rate": 0.5,
            "service_guardrail_pass": False,
            "service_guardrail_violation": True,
            "service_constrained_net_profit": None,
        },
    }
    with TemporaryDirectory() as tmp:
        study_dir = write_study(Path(tmp), make_rows(overrides))
        out_dir = Path(tmp) / "out"
        result = gate.run(["--study-dir", str(study_dir), "--output-dir", str(out_dir)])
        assert result["decision_state"] == "recalibrate_objective", result
        assert result["human_confirmation_required"] is False, result


def test_missing_grid_fails():
    with TemporaryDirectory() as tmp:
        omit = {(grid_id(500.0, 0.4), seed, tag) for seed in gate.EXPECTED_SEEDS for tag in BASE_TAGS}
        study_dir = write_study(Path(tmp), make_rows(omit=omit))
        expect_gate_error(["--study-dir", str(study_dir), "--output-dir", str(Path(tmp) / "out")])


def test_missing_seed_fails():
    with TemporaryDirectory() as tmp:
        omit = {(grid_id(p, g), 2, tag) for p, g in GRID for tag in BASE_TAGS}
        study_dir = write_study(Path(tmp), make_rows(omit=omit))
        expect_gate_error(["--study-dir", str(study_dir), "--output-dir", str(Path(tmp) / "out")])


def test_missing_policy_fails():
    with TemporaryDirectory() as tmp:
        omit = {(grid_id(p, g), seed, "profit_oracle") for p, g in GRID for seed in gate.EXPECTED_SEEDS}
        study_dir = write_study(Path(tmp), make_rows(omit=omit))
        expect_gate_error(["--study-dir", str(study_dir), "--output-dir", str(Path(tmp) / "out")])


def test_duplicate_row_fails():
    with TemporaryDirectory() as tmp:
        study_dir = write_study(Path(tmp), make_rows(duplicate=("p100_g03", 1, "cnn_menu")))
        expect_gate_error(["--study-dir", str(study_dir), "--output-dir", str(Path(tmp) / "out")])


def test_bad_tag_fails():
    with TemporaryDirectory() as tmp:
        study_dir = write_study(Path(tmp), make_rows(bad_tag=True))
        expect_gate_error(["--study-dir", str(study_dir), "--output-dir", str(Path(tmp) / "out")])


def test_missing_metric_fails():
    with TemporaryDirectory() as tmp:
        rows = make_rows({"expected_profit_enumeration": {"adjusted_profit": None}})
        study_dir = write_study(Path(tmp), rows)
        expect_gate_error(["--study-dir", str(study_dir), "--output-dir", str(Path(tmp) / "out")])


def main():
    tests = [
        test_missing_explicit_input_fails,
        test_complete_pass_writes_phase_local_artifacts,
        test_refuses_formal_artifact_output,
        test_one_passing_grid_is_enough,
        test_all_grids_fail_closed,
        test_missing_grid_fails,
        test_missing_seed_fails,
        test_missing_policy_fails,
        test_duplicate_row_fails,
        test_bad_tag_fails,
        test_missing_metric_fails,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} Phase08 gap-closure artifact gate tests")


if __name__ == "__main__":
    main()
