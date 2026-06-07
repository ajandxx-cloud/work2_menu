import csv
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

import build_artifacts


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ROBUSTNESS_DIR = PROJECT_ROOT / "artifacts" / "work2_cnn_setmenunet"

BASE_METRICS = {
    "Nearest-L": {
        "net_profit": 92.0,
        "total_cost": 55.0,
        "quit_rate": 0.11,
        "meeting_point_share": 0.42,
        "avg_walk": 990.0,
        "menu_regret": 6.0,
        "top_L_overlap": 0.40,
    },
    "Cost-L heuristic": {
        "net_profit": 100.0,
        "total_cost": 50.0,
        "quit_rate": 0.10,
        "meeting_point_share": 0.45,
        "avg_walk": 1000.0,
        "menu_regret": 5.0,
        "top_L_overlap": 0.50,
    },
    "CNN-Menu": {
        "net_profit": 99.0,
        "total_cost": 51.0,
        "quit_rate": 0.10,
        "meeting_point_share": 0.46,
        "avg_walk": 1000.0,
        "menu_regret": 5.5,
        "top_L_overlap": 0.45,
    },
    "MLP-Menu": {
        "net_profit": 97.0,
        "total_cost": 52.0,
        "quit_rate": 0.10,
        "meeting_point_share": 0.44,
        "avg_walk": 1000.0,
        "menu_regret": 5.2,
        "top_L_overlap": 0.47,
    },
    "SetMenuNet": {
        "net_profit": 101.0,
        "total_cost": 49.0,
        "quit_rate": 0.10,
        "meeting_point_share": 0.46,
        "avg_walk": 990.0,
        "menu_regret": 4.8,
        "top_L_overlap": 0.52,
    },
    "CNN-SetMenuNet": {
        "net_profit": 112.0,
        "total_cost": 45.0,
        "quit_rate": 0.10,
        "meeting_point_share": 0.48,
        "avg_walk": 970.0,
        "menu_regret": 4.0,
        "top_L_overlap": 0.70,
    },
    "Oracle Menu": {
        "net_profit": 125.0,
        "total_cost": 40.0,
        "quit_rate": 0.08,
        "meeting_point_share": 0.50,
        "avg_walk": 900.0,
        "menu_regret": 1.0,
        "top_L_overlap": 1.00,
    },
}


def make_rows(overrides=None, omit_methods=None):
    overrides = overrides or {}
    omit_methods = set(omit_methods or [])
    rows = []
    for seed in range(5):
        for method, metrics in BASE_METRICS.items():
            if method in omit_methods:
                continue
            row = {
                "study": "work2_formal_main",
                "method": method,
                "seed": seed,
                "instance": "RC",
                "K": 10,
                "L": 3,
                "spearman_cost_ranking": 0.5,
                "runtime_per_decision": 0.1,
                "train_episodes": 150,
                "test_episodes": 50,
                "home_always_shown": True,
                "status": "ok",
                "notes": "synthetic formal test row",
            }
            row.update(deepcopy(metrics))
            for key, value in overrides.get(method, {}).items():
                row[key] = value[seed] if isinstance(value, list) else value
            rows.append(row)
    return rows


def test_formal_classification_cases():
    result = build_artifacts.classify_work2_formal_evidence(make_rows())
    assert result["status"] == "stronger_support", result

    mixed_rows = make_rows(
        {
            "CNN-SetMenuNet": {"net_profit": [130.0, 80.0, 130.0, 80.0, 130.0]},
            "Cost-L heuristic": {"net_profit": [100.0, 100.0, 100.0, 100.0, 100.0]},
        }
    )
    mixed = build_artifacts.classify_work2_formal_evidence(mixed_rows)
    assert mixed["status"] == "mixed_inconclusive", mixed
    assert mixed["diagnostic_required"] is True

    degraded_rows = make_rows({"CNN-SetMenuNet": {"quit_rate": 0.22}})
    degraded = build_artifacts.classify_work2_formal_evidence(degraded_rows)
    assert degraded["status"] == "tradeoff_mixed", degraded
    assert degraded["diagnostic_required"] is True

    incomplete = build_artifacts.classify_work2_formal_evidence(make_rows(omit_methods={"SetMenuNet"}))
    assert incomplete["status"] == "incomplete", incomplete
    assert "SetMenuNet" in incomplete["caveats"][0]


def test_formal_summary_and_diagnostic_text():
    rows = make_rows({"CNN-SetMenuNet": {"quit_rate": 0.22}})
    classification = build_artifacts.classify_work2_formal_evidence(rows)
    manifest = {"name": "work2_formal_main", "base_args": {"max_episodes": 150, "eval_episodes": 50, "outside_option_util": 0.0}}
    with TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        csv_path = tmp_path / "work2_formal_main_rows.csv"
        diagnostic_path = tmp_path / "work2_formal_main_diagnostic.md"
        summary_path = tmp_path / "work2_formal_main_summary.md"
        build_artifacts._write_standard_csv(csv_path, rows)
        build_artifacts._write_work2_diagnostic_report(
            diagnostic_path,
            "work2_formal_main",
            rows,
            rows,
            manifest,
            classification,
        )
        build_artifacts._write_work2_formal_summary(summary_path, "work2_formal_main", rows, csv_path, manifest, diagnostic_path)
        diagnostic_text = diagnostic_path.read_text(encoding="utf-8")
        summary_text = summary_path.read_text(encoding="utf-8")

    for heading in [
        "## Cost Prediction Error",
        "## Ranking/Menu Selection Error",
        "## Offer-Level Objective Trace",
        "## Candidate Feature Insufficiency",
        "## Training Budget",
        "## MNL/Outside-Option Sensitivity",
        "## Route-Cost Realization Gap",
        "## Seed Instability",
        "## Instance/Robustness Instability",
    ]:
        assert heading in diagnostic_text, heading
    assert "Main Formal Table" in summary_text
    assert "MP share" in summary_text
    assert "Robustness Claim Separation" in summary_text
    assert "300/50" in summary_text


def test_remediation_study_names_are_supported():
    assert build_artifacts._is_work2_standard_study("work2_remediation_smoke")
    assert build_artifacts._is_work2_standard_study("work2_remediation_pilot")
    assert build_artifacts._is_work2_standard_study("work2_remediation_formal")
    assert build_artifacts._is_work2_pilot_study("work2_remediation_pilot")
    assert build_artifacts._is_work2_formal_study("work2_remediation_formal")


def test_standard_csv_columns_include_phase6_fields():
    rows = make_rows()
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / "rows.csv"
        build_artifacts._write_standard_csv(path, rows)
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            fields = set(reader.fieldnames or [])
    for column in [
        "study",
        "method",
        "seed",
        "instance",
        "K",
        "L",
        "net_profit",
        "total_cost",
        "quit_rate",
        "meeting_point_share",
        "avg_walk",
        "menu_regret",
        "top_L_overlap",
        "runtime_per_decision",
        "train_episodes",
        "test_episodes",
    ]:
        assert column in fields, column


def test_robustness_freshness_artifacts_exist():
    manifest = build_artifacts.load_manifest("work2_robustness")
    bundle = {
        "manifest": manifest,
        "member_summaries": build_artifacts.suite_member_summaries(manifest, suite_summary=None),
    }
    build_artifacts.build_work2_robustness_artifacts(bundle)

    required = [
        ROBUSTNESS_DIR / "results_snapshot" / "work2_robustness_rows.csv",
        ROBUSTNESS_DIR / "work2_robustness_summary.md",
        ROBUSTNESS_DIR / "diagnostics" / "work2_robustness_diagnostic.md",
        ROBUSTNESS_DIR / "tables" / "work2_robustness_by_dimension.tex",
        ROBUSTNESS_DIR / "figures" / "work2_robustness_net_profit.png",
    ]
    missing = [str(path) for path in required if not path.exists()]
    assert not missing, f"missing robustness artifacts: {missing}"

    rows_path = ROBUSTNESS_DIR / "results_snapshot" / "work2_robustness_rows.csv"
    with rows_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows, "robustness CSV must contain real rows"
    dimensions = {row.get("robustness_dimension") for row in rows}
    expected = {"menu_size", "candidate_pool", "demand", "outside_option", "cross_instance"}
    assert expected <= dimensions, f"missing robustness dimensions: {expected - dimensions}"
    summary = (ROBUSTNESS_DIR / "work2_robustness_summary.md").read_text(encoding="utf-8").lower()
    assert "diagnostic-only" in summary or "conditional" in summary or "mixed" in summary


def main():
    tests = [
        test_formal_classification_cases,
        test_formal_summary_and_diagnostic_text,
        test_remediation_study_names_are_supported,
        test_standard_csv_columns_include_phase6_fields,
        test_robustness_freshness_artifacts_exist,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} Work2 formal artifact tests")


if __name__ == "__main__":
    main()
