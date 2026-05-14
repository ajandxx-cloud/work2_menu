"""Post-processing script for Phase 22 experiments.

Reads Phase 22 study summaries from outputs/studies/ and writes compact result
files to outputs/phase22/ for downstream manuscript phases.

Usage:
    python scripts/extract_phase22_results.py
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Src.research_pipeline import load_study_summary

PHASE22_OUT = ROOT / "outputs" / "phase22"


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


def extract_eta_compare():
    summary = _required_summary("phase22_eta_compare")
    agg_rows = summary.get("aggregate_variant_summary", [])
    run_metadata = summary.get("run_metadata", {})

    variants = {}
    for tag in ["deployed", "heuristic", "stronger", "oracle"]:
        row = _row_by_tag(agg_rows, tag)
        if row is None:
            raise RuntimeError(f"Variant {tag!r} missing from phase22_eta_compare summary.")
        variants[tag] = {
            "label": row.get("variant_label", tag),
            "mean_net_profit_gap": float(row.get("mean_net_profit_gap_vs_reference")),
            "ci95_half_width": float(row.get("net_profit_gap_ci95_half_width_vs_reference")),
            "win_rate": float(row.get("net_profit_win_rate_vs_reference")),
            "average_menu_size": float(row.get("average_menu_size", 0.0)),
            "avg_meeting_point_count_per_menu": float(row.get("avg_meeting_point_count_per_menu", 0.0)),
            "opt_out_rate": float(row.get("opt_out_rate", 0.0)),
            "acceptance_rate": float(row.get("acceptance_rate", 0.0)),
            "non_home_acceptance_rate": float(row.get("non_home_acceptance_rate", 0.0)),
            "consumer_surplus": float(row.get("consumer_surplus", 0.0)),
            "avg_fn_pruning_rate": float(row.get("avg_fn_pruning_rate", 0.0)),
            "avg_displayed_eta_mae": float(row.get("avg_displayed_eta_mae", 0.0)),
            "avg_displayed_ivt_mae": float(row.get("avg_displayed_ivt_mae", 0.0)),
            "avg_displayed_eta_bias": float(row.get("avg_displayed_eta_bias", 0.0)),
            "avg_displayed_ivt_bias": float(row.get("avg_displayed_ivt_bias", 0.0)),
            "avg_selected_eta_mae": float(row.get("avg_eta_mae", 0.0)),
            "avg_selected_ivt_mae": float(row.get("avg_ivt_mae", 0.0)),
            "displayed_eta_p50": float(row.get("displayed_eta_p50", 0.0)),
            "displayed_eta_p90": float(row.get("displayed_eta_p90", 0.0)),
            "displayed_eta_p95": float(row.get("displayed_eta_p95", 0.0)),
            "displayed_ivt_p50": float(row.get("displayed_ivt_p50", 0.0)),
            "displayed_ivt_p90": float(row.get("displayed_ivt_p90", 0.0)),
            "displayed_ivt_p95": float(row.get("displayed_ivt_p95", 0.0)),
            "avg_fn_pruned_near": float(row.get("avg_fn_pruned_near", 0.0)),
            "avg_fn_pruned_mid": float(row.get("avg_fn_pruned_mid", 0.0)),
            "avg_fn_pruned_far": float(row.get("avg_fn_pruned_far", 0.0)),
        }

    stronger = variants["stronger"]
    stronger_distinct = any(
        abs(stronger[key] - variants[other][key]) > 1e-9
        for other in ["deployed", "heuristic"]
        for key in ["avg_displayed_eta_mae", "avg_selected_eta_mae", "avg_fn_pruning_rate", "average_menu_size", "opt_out_rate"]
    )

    result = {
        "study": "phase22_eta_compare",
        "run_id": run_metadata.get("run_id"),
        "split_count": int(run_metadata.get("completed_splits", 0)),
        "expected_split_count": int(run_metadata.get("expected_splits", 0)),
        "status": run_metadata.get("status"),
        "stronger_distinct": bool(stronger_distinct),
        "variants": variants,
    }

    os.makedirs(PHASE22_OUT, exist_ok=True)
    out_path = PHASE22_OUT / "eta_compare.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")
    return result


def extract_uptake_calibration():
    summary = _required_summary("phase22_uptake_calibration")
    agg_rows = summary.get("aggregate_variant_summary", [])
    run_metadata = summary.get("run_metadata", {})

    full_row = _row_by_tag(agg_rows, "full_display")
    menu_row = _row_by_tag(agg_rows, "menu_optimization")
    if full_row is None or menu_row is None:
        raise RuntimeError("phase22_uptake_calibration summary missing full_display or menu_optimization rows.")

    full_display = {
        "label": full_row.get("variant_label", "full_display"),
        "opt_out_rate": float(full_row.get("opt_out_rate", 0.0)),
        "acceptance_rate": float(full_row.get("acceptance_rate", 0.0)),
        "non_home_acceptance_rate": float(full_row.get("non_home_acceptance_rate", 0.0)),
        "average_menu_size": float(full_row.get("average_menu_size", 0.0)),
        "avg_meeting_point_count_per_menu": float(full_row.get("avg_meeting_point_count_per_menu", 0.0)),
        "consumer_surplus": float(full_row.get("consumer_surplus", 0.0)),
        "net_profit": float(full_row.get("net_profit", 0.0)),
    }
    menu_optimization = {
        "label": menu_row.get("variant_label", "menu_optimization"),
        "opt_out_rate": float(menu_row.get("opt_out_rate", 0.0)),
        "acceptance_rate": float(menu_row.get("acceptance_rate", 0.0)),
        "non_home_acceptance_rate": float(menu_row.get("non_home_acceptance_rate", 0.0)),
        "average_menu_size": float(menu_row.get("average_menu_size", 0.0)),
        "avg_meeting_point_count_per_menu": float(menu_row.get("avg_meeting_point_count_per_menu", 0.0)),
        "consumer_surplus": float(menu_row.get("consumer_surplus", 0.0)),
        "net_profit": float(menu_row.get("net_profit", 0.0)),
        "mean_net_profit_gap_vs_reference": float(menu_row.get("mean_net_profit_gap_vs_reference", 0.0)),
        "net_profit_win_rate_vs_reference": float(menu_row.get("net_profit_win_rate_vs_reference", 0.0)),
        "net_profit_gap_ci95_half_width_vs_reference": float(menu_row.get("net_profit_gap_ci95_half_width_vs_reference", 0.0)),
    }

    calibration_success = bool(
        menu_optimization["acceptance_rate"] >= 0.10
        and menu_optimization["opt_out_rate"] < 0.95
        and menu_optimization["non_home_acceptance_rate"] > 0.0
    )

    result = {
        "study": "phase22_uptake_calibration",
        "run_id": run_metadata.get("run_id"),
        "split_count": int(run_metadata.get("completed_splits", 0)),
        "expected_split_count": int(run_metadata.get("expected_splits", 0)),
        "status": run_metadata.get("status"),
        "calibration_success": calibration_success,
        "full_display": full_display,
        "menu_optimization": menu_optimization,
    }

    os.makedirs(PHASE22_OUT, exist_ok=True)
    out_path = PHASE22_OUT / "uptake_calibration.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")
    return result


def write_phase22_summary(eta_compare, uptake):
    result = {
        "eta_compare": eta_compare,
        "uptake_calibration": uptake,
    }
    out_path = PHASE22_OUT / "phase22_summary.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    print("=== Phase 22 result extraction ===")
    eta_compare = extract_eta_compare()
    uptake = extract_uptake_calibration()
    write_phase22_summary(eta_compare, uptake)
