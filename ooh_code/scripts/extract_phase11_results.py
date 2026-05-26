"""Post-processing script for Phase 11 experiments.

Reads study summaries from outputs/studies/ and writes compact result files to
outputs/phase11/ for manuscript consumption.

Usage:
    python scripts/extract_phase11_results.py
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Src.research_pipeline import load_study_summary

PHASE11_OUT = ROOT / "outputs" / "phase11"


def _row_by_tag(rows, tag):
    for row in rows:
        if row.get("variant_tag") == tag:
            return row
    return None


def _required_summary(study_name):
    summary, _ = load_study_summary(study_name)
    if summary is None:
        raise RuntimeError(f"{study_name} study summary not found. Run the study first.")
    return summary


def extract_filtering_baselines():
    summary = _required_summary("filtering_baselines")
    agg_rows = summary.get("aggregate_variant_summary", [])
    run_metadata = summary.get("run_metadata", {})

    variants = {}
    for tag in ["v1_hard", "v1_calibrated", "v1_interval", "v2"]:
        row = _row_by_tag(agg_rows, tag)
        if row is None:
            raise RuntimeError(f"Variant {tag!r} missing from filtering_baselines summary.")
        variants[tag] = {
            "label": row.get("variant_label", tag),
            "mean_net_profit_gap": float(row.get("mean_net_profit_gap_vs_reference")),
            "ci95_half_width": float(row.get("net_profit_gap_ci95_half_width_vs_reference")),
            "win_rate": float(row.get("net_profit_win_rate_vs_reference")),
            "avg_fn_pruning_rate": float(row.get("avg_fn_pruning_rate", 0.0)),
            "avg_displayed_eta_mae": float(row.get("avg_displayed_eta_mae", 0.0)),
            "avg_displayed_ivt_mae": float(row.get("avg_displayed_ivt_mae", 0.0)),
            "avg_selected_eta_mae": float(row.get("avg_eta_mae", 0.0)),
            "avg_selected_ivt_mae": float(row.get("avg_ivt_mae", 0.0)),
        }

    result = {
        "study": "filtering_baselines",
        "run_id": run_metadata.get("run_id"),
        "split_count": int(run_metadata.get("completed_splits", 0)),
        "expected_split_count": int(run_metadata.get("expected_splits", 0)),
        "status": run_metadata.get("status"),
        "metric_note": (
            "Displayed-offer ETA/IVT MAE is the primary predictor-error diagnostic. "
            "Selected-offer MAE can collapse toward zero under the outside-option model "
            "because few non-home offers are ultimately chosen."
        ),
        "variants": variants,
    }

    os.makedirs(PHASE11_OUT, exist_ok=True)
    out_path = PHASE11_OUT / "filtering_baselines.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")
    return result


def extract_predictor_by_policy():
    summary = _required_summary("rc_main_optout")
    agg_rows = summary.get("aggregate_variant_summary", [])
    run_metadata = summary.get("run_metadata", {})

    tags = ["full_display", "menu_optimization", "menu_optimization_v2"]
    policies = {}
    for tag in tags:
        row = _row_by_tag(agg_rows, tag)
        if row is None:
            raise RuntimeError(f"Variant {tag!r} missing from rc_main_optout summary.")
        policies[tag] = {
            "label": row.get("variant_label", tag),
            "avg_displayed_eta_mae": float(row.get("avg_displayed_eta_mae", 0.0)),
            "avg_displayed_ivt_mae": float(row.get("avg_displayed_ivt_mae", 0.0)),
            "avg_selected_eta_mae": float(row.get("avg_eta_mae", 0.0)),
            "avg_selected_ivt_mae": float(row.get("avg_ivt_mae", 0.0)),
            "opt_out_rate": float(row.get("opt_out_rate", 0.0)),
            "home_pickup_share": float(row.get("home_pickup_share", 0.0)),
            "average_menu_size": float(row.get("average_menu_size", 0.0)),
            "mean_net_profit_gap": (
                None if row.get("mean_net_profit_gap_vs_reference") is None
                else float(row.get("mean_net_profit_gap_vs_reference"))
            ),
        }

    result = {
        "study": "rc_main_optout",
        "run_id": run_metadata.get("run_id"),
        "split_count": int(run_metadata.get("completed_splits", 0)),
        "expected_split_count": int(run_metadata.get("expected_splits", 0)),
        "status": run_metadata.get("status"),
        "metric_note": (
            "Displayed-offer ETA/IVT MAE averages across all displayed non-home offers. "
            "Selected-offer MAE is retained for completeness but is often weakly identified "
            "when passengers almost always opt out or revert to home pickup."
        ),
        "policies": policies,
    }

    os.makedirs(PHASE11_OUT, exist_ok=True)
    out_path = PHASE11_OUT / "predictor_by_policy.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")
    return result


if __name__ == "__main__":
    print("=== Phase 11 result extraction ===")
    try:
        filtering = extract_filtering_baselines()
        print(
            "  filtering split coverage:",
            f"{filtering['split_count']}/{filtering['expected_split_count']}",
        )
    except RuntimeError as e:
        print(f"[filtering_baselines] {e}")

    try:
        predictor = extract_predictor_by_policy()
        print(
            "  predictor split coverage:",
            f"{predictor['split_count']}/{predictor['expected_split_count']}",
        )
    except RuntimeError as e:
        print(f"[predictor_by_policy] {e}")
