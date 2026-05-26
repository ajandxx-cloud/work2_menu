"""Post-processing script for Phase 8 experiments.

Reads study summary JSONs from outputs/studies/ and writes aggregated result
files to outputs/phase7/. Run after both eta_robustness and rc_main_optout
studies complete.

Usage:
    python scripts/extract_phase8_results.py
"""

import json
import os
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Src.research_pipeline import OUTPUTS_DIR, load_study_summary

PHASE7_OUT = ROOT / "outputs" / "phase7"


def mean_std(values):
    """Return {mean, std} for a list of floats."""
    if not values:
        return {"mean": None, "std": None}
    arr = [float(v) for v in values]
    mean = float(np.mean(arr))
    std = float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0
    return {"mean": mean, "std": std}


def _row_by_tag(rows, tag):
    for row in rows:
        if row.get("variant_tag") == tag:
            return row
    return None


def _collect_per_split_metric(run_dir, variant_tag, metric_key):
    """Read per-split variant summary files and collect a metric for a given variant.

    Tries {variant_tag}_summary.json first (has all aggregate_episode_metrics keys),
    then falls back to split_summary.json aggregate_variant_summary rows.
    """
    splits_dir = run_dir / "splits"
    values = []
    if not splits_dir.exists():
        return values
    for split_dir in sorted(splits_dir.iterdir()):
        if not split_dir.is_dir():
            continue
        # Primary: read directly from per-variant summary file
        variant_summary_path = split_dir / f"{variant_tag}_summary.json"
        if variant_summary_path.exists():
            try:
                with open(variant_summary_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                val = data.get(metric_key)
                if val is not None:
                    values.append(float(val))
                    continue
            except Exception:
                pass
        # Fallback: split_summary.json aggregate_variant_summary
        split_summary_path = split_dir / "split_summary.json"
        if not split_summary_path.exists():
            continue
        try:
            with open(split_summary_path, "r", encoding="utf-8") as f:
                split_data = json.load(f)
            rows = split_data.get("aggregate_variant_summary", [])
            row = _row_by_tag(rows, variant_tag)
            if row is not None and row.get(metric_key) is not None:
                values.append(float(row[metric_key]))
        except Exception:
            continue
    return values


def extract_eta_robustness():
    """Extract ETA robustness results and write outputs/phase7/eta_robustness.json."""
    summary, run_dir = load_study_summary("eta_robustness")
    if summary is None:
        raise RuntimeError("eta_robustness study summary not found. Run the study first.")

    agg_rows = summary.get("aggregate_variant_summary", [])
    variants = {}
    for tag in ["v1_blended", "v1_heuristic", "v1_oracle", "v2"]:
        row = _row_by_tag(agg_rows, tag)
        if row is None:
            print(f"WARNING: variant {tag!r} not found in aggregate_variant_summary")
            variants[tag] = {
                "mean_net_profit_gap": None,
                "std_net_profit_gap": None,
                "win_rate": None,
                "avg_fn_pruning_rate": None,
            }
            continue

        # Collect per-split net_profit_gap for std computation
        per_split_gaps = _collect_per_split_metric(run_dir, tag, "mean_net_profit_gap_vs_reference")
        gap_stats = mean_std(per_split_gaps)

        mean_gap = row.get("mean_net_profit_gap_vs_reference")
        win_rate = row.get("net_profit_win_rate_vs_reference")
        # avg_fn_pruning_rate may not be in aggregate summary (not in SUMMARY_NUMERIC_KEYS);
        # read it from per-split variant summary files instead.
        if tag != "v2":
            per_split_fn = _collect_per_split_metric(run_dir, tag, "avg_fn_pruning_rate")
            fn_rate = float(np.mean(per_split_fn)) if per_split_fn else None
        else:
            fn_rate = None

        variants[tag] = {
            "mean_net_profit_gap": float(mean_gap) if mean_gap is not None else None,
            "std_net_profit_gap": gap_stats["std"],
            "win_rate": float(win_rate) if win_rate is not None else None,
            "avg_fn_pruning_rate": float(fn_rate) if fn_rate is not None else None,
        }

    result = {
        "study": "eta_robustness",
        "run_id": summary.get("run_metadata", {}).get("run_id"),
        "variants": variants,
        "split_count": 6,
    }

    os.makedirs(str(PHASE7_OUT), exist_ok=True)
    out_path = PHASE7_OUT / "eta_robustness.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")
    return result


def extract_rc_main_optout():
    """Extract opt-out validation results and write outputs/phase7/rc_main_optout.json."""
    summary, run_dir = load_study_summary("rc_main_optout")
    if summary is None:
        raise RuntimeError("rc_main_optout study summary not found. Run the study first.")

    agg_rows = summary.get("aggregate_variant_summary", [])
    v2_row = _row_by_tag(agg_rows, "menu_optimization_v2")
    if v2_row is None:
        raise RuntimeError("menu_optimization_v2 variant not found in rc_main_optout summary.")

    gap = v2_row.get("mean_net_profit_gap_vs_reference")
    win_rate = v2_row.get("net_profit_win_rate_vs_reference")

    gap_val = float(gap) if gap is not None else None
    win_rate_val = float(win_rate) if win_rate is not None else None

    gap_positive = bool(gap_val is not None and gap_val > 0)
    meets_threshold = bool(win_rate_val is not None and win_rate_val >= 0.8)

    if not meets_threshold:
        print(
            f"WARNING: v2 win rate {win_rate_val} is below the 0.8 threshold. "
            "This is a significant finding — flag for manuscript discussion."
        )

    result = {
        "study": "rc_main_optout",
        "run_id": summary.get("run_metadata", {}).get("run_id"),
        "v2_mean_net_profit_gap": gap_val,
        "v2_win_rate": win_rate_val,
        "v2_gap_positive": gap_positive,
        "v2_win_rate_meets_threshold": meets_threshold,
        "split_count": 6,
    }

    os.makedirs(str(PHASE7_OUT), exist_ok=True)
    out_path = PHASE7_OUT / "rc_main_optout.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")
    return result


if __name__ == "__main__":
    print("=== Phase 8 result extraction ===")
    try:
        r1 = extract_eta_robustness()
        print(f"  v2 gap: {r1['variants']['v2']['mean_net_profit_gap']}")
        print(f"  v1_blended fn_pruning_rate: {r1['variants']['v1_blended']['avg_fn_pruning_rate']}")
    except RuntimeError as e:
        print(f"[eta_robustness] {e}")

    try:
        r2 = extract_rc_main_optout()
        print(f"  v2 win_rate: {r2['v2_win_rate']}")
        print(f"  v2 gap_positive: {r2['v2_gap_positive']}")
        print(f"  v2 win_rate_meets_threshold: {r2['v2_win_rate_meets_threshold']}")
    except RuntimeError as e:
        print(f"[rc_main_optout] {e}")
