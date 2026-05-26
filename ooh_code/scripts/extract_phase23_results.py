"""Post-processing script for Phase 23 pricing-baseline experiments.

Reads Phase 23 study summaries from outputs/studies/ and writes compact result
files to outputs/phase23/ for downstream manuscript phases.

Usage:
    python scripts/extract_phase23_results.py
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Src.research_pipeline import load_study_summary

PHASE23_OUT = ROOT / "outputs" / "phase23"


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


def _variant_payload(row, baseline_tag="lambertw"):
    payload = {
        "label": row.get("variant_label", row.get("variant_tag")),
        "policy": row.get("policy"),
        "mean_net_profit_gap_vs_reference": float(row.get("mean_net_profit_gap_vs_reference", 0.0)),
        "net_profit_win_rate_vs_reference": float(row.get("net_profit_win_rate_vs_reference", 0.0)),
        "net_profit_gap_ci95_half_width_vs_reference": float(row.get("net_profit_gap_ci95_half_width_vs_reference", 0.0)),
        "acceptance_rate": float(row.get("acceptance_rate", 0.0)),
        "opt_out_rate": float(row.get("opt_out_rate", 0.0)),
        "non_home_acceptance_rate": float(row.get("non_home_acceptance_rate", 0.0)),
        "average_menu_size": float(row.get("average_menu_size", 0.0)),
        "avg_meeting_point_count_per_menu": float(row.get("avg_meeting_point_count_per_menu", 0.0)),
        "consumer_surplus": float(row.get("consumer_surplus", 0.0)),
        "price_at_floor_fraction": float(row.get("price_at_floor_fraction", 0.0)),
        "price_at_ceil_fraction": float(row.get("price_at_ceil_fraction", 0.0)),
        "avg_chosen_price": float(row.get("avg_chosen_price", 0.0)),
        "avg_fn_pruning_rate": float(row.get("avg_fn_pruning_rate", 0.0)),
        "is_behavior_non_degenerate": bool(row.get("is_behavior_non_degenerate")),
    }
    if row.get("variant_tag") != baseline_tag:
        payload["mean_net_profit_gap_vs_baseline"] = float(row.get("mean_net_profit_gap_vs_baseline", 0.0))
        payload["net_profit_win_rate_vs_baseline"] = float(row.get("net_profit_win_rate_vs_baseline", 0.0))
        payload["net_profit_gap_ci95_half_width_vs_baseline"] = float(row.get("net_profit_gap_ci95_half_width_vs_baseline", 0.0))
    return payload


def extract_phase23_pricing_baselines():
    summary = _required_summary("phase23_pricing_baselines")
    agg_rows = summary.get("aggregate_variant_summary", [])
    run_metadata = summary.get("run_metadata", {})

    reference_row = _row_by_tag(agg_rows, "full_display")
    lambertw_row = _row_by_tag(agg_rows, "lambertw")
    cost_plus_row = _row_by_tag(agg_rows, "cost_plus")
    flat_markdown_row = _row_by_tag(agg_rows, "flat_markdown")
    required = {
        "full_display": reference_row,
        "lambertw": lambertw_row,
        "cost_plus": cost_plus_row,
        "flat_markdown": flat_markdown_row,
    }
    missing = [tag for tag, row in required.items() if row is None]
    if missing:
        raise RuntimeError(f"Missing Phase 23 aggregate rows: {missing}")

    variants = {
        "lambertw": _variant_payload(lambertw_row),
        "cost_plus": _variant_payload(cost_plus_row),
        "flat_markdown": _variant_payload(flat_markdown_row),
    }

    result = {
        "study": "phase23_pricing_baselines",
        "run_id": run_metadata.get("run_id"),
        "split_count": int(run_metadata.get("completed_splits", 0)),
        "expected_split_count": int(run_metadata.get("expected_splits", 0)),
        "status": run_metadata.get("status"),
        "reference": {
            "label": reference_row.get("variant_label", "full display"),
            "acceptance_rate": float(reference_row.get("acceptance_rate", 0.0)),
            "opt_out_rate": float(reference_row.get("opt_out_rate", 0.0)),
            "non_home_acceptance_rate": float(reference_row.get("non_home_acceptance_rate", 0.0)),
            "net_profit": float(reference_row.get("net_profit", 0.0)),
            "consumer_surplus": float(reference_row.get("consumer_surplus", 0.0)),
        },
        "baseline_variant": "lambertw",
        "variants": variants,
        "pricing_matter_signal": {
            "cost_plus_vs_lambertw_gap": float(cost_plus_row.get("mean_net_profit_gap_vs_baseline", 0.0)),
            "flat_markdown_vs_lambertw_gap": float(flat_markdown_row.get("mean_net_profit_gap_vs_baseline", 0.0)),
            "lambertw_floor_hit_rate": float(lambertw_row.get("price_at_floor_fraction", 0.0)),
            "lambertw_ceil_hit_rate": float(lambertw_row.get("price_at_ceil_fraction", 0.0)),
        },
    }

    os.makedirs(PHASE23_OUT, exist_ok=True)
    out_path = PHASE23_OUT / "pricing_baselines.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")
    return result


if __name__ == "__main__":
    print("=== Phase 23 result extraction ===")
    extract_phase23_pricing_baselines()
