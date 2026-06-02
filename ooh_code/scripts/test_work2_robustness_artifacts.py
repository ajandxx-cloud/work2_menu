from pathlib import Path
from tempfile import TemporaryDirectory

import build_artifacts


def make_dimension_rows(dimension="menu_size", overrides=None, omit_methods=None):
    overrides = overrides or {}
    omit_methods = set(omit_methods or [])
    base = {
        "Cost-L heuristic": {
            "net_profit": 100.0,
            "quit_rate": 0.10,
            "avg_walk": 1000.0,
            "menu_regret": 5.0,
            "top_L_overlap": 0.50,
        },
        "CNN-Menu": {
            "net_profit": 98.0,
            "quit_rate": 0.10,
            "avg_walk": 1000.0,
            "menu_regret": 5.5,
            "top_L_overlap": 0.45,
        },
        "CNN-SetMenuNet": {
            "net_profit": 110.0,
            "quit_rate": 0.10,
            "avg_walk": 950.0,
            "menu_regret": 4.0,
            "top_L_overlap": 0.70,
        },
        "Oracle Menu": {
            "net_profit": 125.0,
            "quit_rate": 0.08,
            "avg_walk": 900.0,
            "menu_regret": 1.0,
            "top_L_overlap": 1.00,
        },
    }
    rows = []
    for seed in range(2):
        for method, metrics in base.items():
            if method in omit_methods:
                continue
            row = {
                "study": f"work2_{dimension}_robustness",
                "robustness_dimension": dimension,
                "robustness_setting": 3,
                "method": method,
                "seed": seed,
                "instance": "RC",
                "K": 10,
                "L": 3,
                "demand_setting": 700,
                "outside_option_util": 0.0,
                "total_cost": 0.0,
                "spearman_cost_ranking": 0.5,
                "runtime_per_decision": 0.1,
            }
            row.update(metrics)
            row.update(overrides.get(method, {}))
            rows.append(row)
    return rows


def assert_dimension_status(name, rows, expected):
    result = build_artifacts.classify_work2_robustness_dimension(name, rows)
    assert result["status"] == expected, f"expected {expected}, got {result}"


def test_stable_support_dimension():
    assert_dimension_status("menu_size", make_dimension_rows("menu_size"), "stable_support")


def test_mixed_dimension_does_not_become_supportive():
    rows = make_dimension_rows(
        "outside_option",
        overrides={"CNN-SetMenuNet": {"menu_regret": 8.0, "top_L_overlap": 0.20}},
    )
    assert_dimension_status("outside_option", rows, "conditional_mixed")


def test_degraded_dimension_requires_diagnostic():
    rows = make_dimension_rows(
        "demand",
        overrides={"CNN-SetMenuNet": {"net_profit": 70.0, "quit_rate": 0.30}},
    )
    result = build_artifacts.classify_work2_robustness_dimension("demand", rows)
    assert result["status"] == "degraded", result
    assert result["diagnostic_required"] is True


def test_incomplete_dimension_missing_oracle():
    rows = make_dimension_rows("candidate_pool", omit_methods={"Oracle Menu"})
    assert_dimension_status("candidate_pool", rows, "incomplete")


def test_not_run_dimension_is_distinct_from_failed():
    result = build_artifacts.classify_work2_robustness_dimension("cross_instance", [], missing_source=True)
    assert result["status"] == "not_run", result
    assert "no member study summary" in result["summary"]


def test_summary_and_diagnostic_language():
    dimension_results = [
        {
            "study_name": "work2_menu_size_robustness",
            "dimension": "menu_size",
            "classification": build_artifacts.classify_work2_robustness_dimension(
                "menu_size", make_dimension_rows("menu_size")
            ),
            "likely_cause": "menu selection error",
        },
        {
            "study_name": "work2_demand_robustness",
            "dimension": "demand",
            "classification": build_artifacts.classify_work2_robustness_dimension(
                "demand",
                make_dimension_rows("demand", overrides={"CNN-SetMenuNet": {"net_profit": 70.0}}),
            ),
            "likely_cause": "demand sensitivity",
        },
    ]
    rows = make_dimension_rows("menu_size") + make_dimension_rows(
        "demand", overrides={"CNN-SetMenuNet": {"net_profit": 70.0}}
    )
    with TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        csv_path = tmp_path / "work2_robustness_rows.csv"
        csv_path.write_text("placeholder\n", encoding="utf-8")
        summary_path = tmp_path / "work2_robustness_summary.md"
        diagnostic_path = tmp_path / "work2_robustness_diagnostic.md"
        build_artifacts._write_work2_robustness_diagnostic(diagnostic_path, dimension_results)
        build_artifacts._write_work2_robustness_summary(summary_path, rows, csv_path, dimension_results, diagnostic_path)
        summary_text = summary_path.read_text(encoding="utf-8")
        diagnostic_text = diagnostic_path.read_text(encoding="utf-8")
    assert "diagnostic-only claim" in summary_text
    assert "Missing or negative dimensions remain diagnostic evidence" in summary_text
    for heading in [
        "## Incomplete/Degraded/Mixed Dimensions",
        "## Prediction Error",
        "## Ranking/Menu Selection Error",
        "## Demand Sensitivity",
        "## Outside-Option/MNL Sensitivity",
        "## Instance Instability",
        "## Training Budget",
        "## Candidate-Pool Scaling",
    ]:
        assert heading in diagnostic_text, heading


def test_missing_member_outputs_generate_incomplete_artifacts():
    bundle = {
        "manifest": build_artifacts.load_manifest("work2_robustness"),
        "member_summaries": [],
    }
    snapshot = build_artifacts.build_work2_robustness_artifacts(bundle)
    statuses = {item["classification"]["status"] for item in snapshot["dimension_results"]}
    assert statuses == {"not_run"}, statuses
    summary_path = build_artifacts.WORK2_STANDARD_ARTIFACTS_DIR / "work2_robustness_summary.md"
    diagnostic_path = (
        build_artifacts.WORK2_STANDARD_ARTIFACTS_DIR
        / "diagnostics"
        / "work2_robustness_diagnostic.md"
    )
    assert summary_path.exists()
    assert diagnostic_path.exists()
    assert "not run" in summary_path.read_text(encoding="utf-8").lower()


def main():
    tests = [
        test_stable_support_dimension,
        test_mixed_dimension_does_not_become_supportive,
        test_degraded_dimension_requires_diagnostic,
        test_incomplete_dimension_missing_oracle,
        test_not_run_dimension_is_distinct_from_failed,
        test_summary_and_diagnostic_language,
        test_missing_member_outputs_generate_incomplete_artifacts,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} Work2 robustness artifact tests")


if __name__ == "__main__":
    main()
