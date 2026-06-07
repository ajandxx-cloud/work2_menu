from copy import deepcopy
from copy import deepcopy
from tempfile import TemporaryDirectory
from pathlib import Path

import build_artifacts


BASE_METRICS = {
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
    "MLP-Menu": {
        "net_profit": 97.0,
        "quit_rate": 0.10,
        "avg_walk": 1000.0,
        "menu_regret": 5.2,
        "top_L_overlap": 0.47,
    },
    "CNN-SetMenuNet": {
        "net_profit": 110.0,
        "quit_rate": 0.10,
        "avg_walk": 1000.0,
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


def make_rows(overrides=None):
    overrides = overrides or {}
    rows = []
    for seed in range(3):
        for method, metrics in BASE_METRICS.items():
            row = {
                "study": "work2_main",
                "method": method,
                "seed": seed,
                "instance": "RC",
                "K": 10,
                "L": 3,
                "total_cost": 0.0,
                "spearman_cost_ranking": 0.5,
                "runtime_per_decision": 0.1,
            }
            row.update(deepcopy(metrics))
            for key, value in overrides.get(method, {}).items():
                row[key] = value[seed] if isinstance(value, list) else value
            rows.append(row)
    return rows


def assert_status(name, rows, expected):
    result = build_artifacts.classify_work2_pilot_evidence(rows)
    assert result["status"] == expected, f"{name}: expected {expected}, got {result}"


def test_stronger_support():
    assert_status("stronger", make_rows(), "stronger_support")


def test_preliminary_support():
    rows = make_rows({"CNN-SetMenuNet": {"menu_regret": 6.0, "top_L_overlap": 0.40}})
    assert_status("preliminary", rows, "preliminary_support")


def test_tradeoff_mixed_guardrail():
    rows = make_rows({"CNN-SetMenuNet": {"quit_rate": 0.20}})
    assert_status("tradeoff", rows, "tradeoff_mixed")


def test_high_opt_out_cannot_be_supportive():
    rows = make_rows(
        {
            "CNN-SetMenuNet": {
                "net_profit": 200.0,
                "quit_rate": 0.99,
                "avg_walk": 10.0,
            }
        }
    )
    result = build_artifacts.classify_work2_pilot_evidence(rows)
    assert result["status"] == "mixed_inconclusive"
    assert result["diagnostic_required"] is True
    assert "opt-out" in result["summary"]


def test_mixed_inconclusive_seed_trend():
    rows = make_rows(
        {
            "CNN-SetMenuNet": {"net_profit": [130.0, 80.0, 130.0]},
            "Cost-L heuristic": {"net_profit": [100.0, 100.0, 100.0]},
            "CNN-Menu": {"net_profit": [100.0, 100.0, 100.0]},
            "MLP-Menu": {"net_profit": [100.0, 100.0, 100.0]},
        }
    )
    assert_status("mixed", rows, "mixed_inconclusive")


def test_incomplete_minimum_methods():
    rows = [row for row in make_rows() if row["method"] != "Oracle Menu"]
    assert_status("incomplete", rows, "incomplete")


def test_supportive_evidence_does_not_require_diagnostic():
    result = build_artifacts.classify_work2_pilot_evidence(make_rows())
    assert result["diagnostic_required"] is False


def test_diagnostic_report_contains_required_headings():
    rows = make_rows({"CNN-SetMenuNet": {"quit_rate": 0.20}})
    classification = build_artifacts.classify_work2_pilot_evidence(rows)
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / "work2_main_diagnostic.md"
        build_artifacts._write_work2_diagnostic_report(
            path,
            "work2_main",
            rows,
            rows,
            {"base_args": {"max_episodes": 80, "eval_episodes": 20}},
            classification,
        )
        text = path.read_text(encoding="utf-8")
    for heading in [
        "## Cost Prediction Error",
        "## Ranking/Menu Selection Error",
        "## Offer-Level Objective Trace",
        "## Training Budget",
        "## Seed Instability",
    ]:
        assert heading in text, heading
    assert "unavailable" in text


def main():
    tests = [
        test_stronger_support,
        test_preliminary_support,
        test_tradeoff_mixed_guardrail,
        test_high_opt_out_cannot_be_supportive,
        test_mixed_inconclusive_seed_trend,
        test_incomplete_minimum_methods,
        test_supportive_evidence_does_not_require_diagnostic,
        test_diagnostic_report_contains_required_headings,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} Work2 artifact summary gate tests")


if __name__ == "__main__":
    main()
