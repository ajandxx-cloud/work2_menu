"""Post-processing script for Phase 9 experiments.

Reads study summary JSONs from outputs/studies/ and writes aggregated result
files to outputs/phase9/. Run after all three Phase 9 studies complete.

Usage:
    python scripts/extract_phase9_results.py
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Src.research_pipeline import load_study_summary

PHASE9_OUT = ROOT / "outputs" / "phase9"


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
    """Read per-split variant summary files and collect a metric for a given variant."""
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


def extract_fleet_size_sweep():
    """Extract fleet size sweep results and write outputs/phase9/fleet_size_sweep.json."""
    summary, run_dir = load_study_summary("fleet_size_sweep")
    if summary is None:
        raise RuntimeError("fleet_size_sweep study summary not found. Run the study first.")

    agg_rows = summary.get("aggregate_variant_summary", [])
    fleet_sizes = {
        10: "v2_fleet10",
        15: "v2_fleet15",
        20: "v2_fleet20",
    }
    results = {}
    for fleet_size, tag in fleet_sizes.items():
        row = _row_by_tag(agg_rows, tag)
        if row is None:
            print(f"WARNING: variant {tag!r} not found in fleet_size_sweep summary")
            results[fleet_size] = {"gap": None, "std": None, "win_rate": None}
            continue
        per_split_gaps = _collect_per_split_metric(run_dir, tag, "mean_net_profit_gap_vs_reference")
        gap_stats = mean_std(per_split_gaps)
        gap = row.get("mean_net_profit_gap_vs_reference")
        win_rate = row.get("net_profit_win_rate_vs_reference")
        results[fleet_size] = {
            "gap": float(gap) if gap is not None else None,
            "std": gap_stats["std"],
            "win_rate": float(win_rate) if win_rate is not None else None,
        }

    result = {
        "study": "fleet_size_sweep",
        "run_id": summary.get("run_metadata", {}).get("run_id"),
        "fleet_sizes": results,
        "split_count": 6,
    }
    os.makedirs(str(PHASE9_OUT), exist_ok=True)
    out_path = PHASE9_OUT / "fleet_size_sweep.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")
    return result


def extract_demand_sweep():
    """Extract demand sweep results and write outputs/phase9/demand_sweep.json."""
    summary, run_dir = load_study_summary("demand_sweep")
    if summary is None:
        raise RuntimeError("demand_sweep study summary not found. Run the study first.")

    agg_rows = summary.get("aggregate_variant_summary", [])
    demand_levels = {
        "0.7x": "v2_demand07",
        "1.0x": "v2_demand10",
        "1.3x": "v2_demand13",
    }
    results = {}
    for label, tag in demand_levels.items():
        row = _row_by_tag(agg_rows, tag)
        if row is None:
            print(f"WARNING: variant {tag!r} not found in demand_sweep summary")
            results[label] = {"gap": None, "std": None, "win_rate": None}
            continue
        per_split_gaps = _collect_per_split_metric(run_dir, tag, "mean_net_profit_gap_vs_reference")
        gap_stats = mean_std(per_split_gaps)
        gap = row.get("mean_net_profit_gap_vs_reference")
        win_rate = row.get("net_profit_win_rate_vs_reference")
        results[label] = {
            "gap": float(gap) if gap is not None else None,
            "std": gap_stats["std"],
            "win_rate": float(win_rate) if win_rate is not None else None,
        }

    result = {
        "study": "demand_sweep",
        "run_id": summary.get("run_metadata", {}).get("run_id"),
        "demand_levels": results,
        "split_count": 6,
    }
    os.makedirs(str(PHASE9_OUT), exist_ok=True)
    out_path = PHASE9_OUT / "demand_sweep.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")
    return result


def extract_pricing_sensitivity():
    """Extract pricing sensitivity results and write outputs/phase9/pricing_sensitivity.json."""
    summary, run_dir = load_study_summary("pricing_sensitivity")
    if summary is None:
        raise RuntimeError("pricing_sensitivity study summary not found. Run the study first.")

    agg_rows = summary.get("aggregate_variant_summary", [])
    grid_entries = []
    for R in [25, 50, 75]:
        for p_min in [-3, -6, -9]:
            tag = f"R{R}_pmin{p_min}"
            row = _row_by_tag(agg_rows, tag)
            if row is None:
                print(f"WARNING: variant {tag!r} not found in pricing_sensitivity summary")
                grid_entries.append({
                    "R": R, "p_min": p_min, "tag": tag,
                    "gap": None, "std": None, "win_rate": None,
                    "price_at_floor_fraction": None,
                })
                continue
            per_split_gaps = _collect_per_split_metric(run_dir, tag, "mean_net_profit_gap_vs_reference")
            gap_stats = mean_std(per_split_gaps)
            gap = row.get("mean_net_profit_gap_vs_reference")
            win_rate = row.get("net_profit_win_rate_vs_reference")
            floor_frac = row.get("price_at_floor_fraction")
            grid_entries.append({
                "R": R,
                "p_min": p_min,
                "tag": tag,
                "gap": float(gap) if gap is not None else None,
                "std": gap_stats["std"],
                "win_rate": float(win_rate) if win_rate is not None else None,
                "price_at_floor_fraction": float(floor_frac) if floor_frac is not None else None,
            })

    result = {
        "study": "pricing_sensitivity",
        "run_id": summary.get("run_metadata", {}).get("run_id"),
        "grid": grid_entries,
        "split_count": 6,
    }
    os.makedirs(str(PHASE9_OUT), exist_ok=True)
    out_path = PHASE9_OUT / "pricing_sensitivity.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")
    return result


def consolidate():
    """Merge all three result files into outputs/phase9/expanded_experiments.json."""
    parts = {}
    for name in ["fleet_size_sweep", "demand_sweep", "pricing_sensitivity"]:
        path = PHASE9_OUT / f"{name}.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                parts[name] = json.load(f)
        else:
            print(f"WARNING: {path} not found — skipping from consolidated output")
            parts[name] = None

    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "fleet_size_sweep": parts.get("fleet_size_sweep"),
        "demand_sweep": parts.get("demand_sweep"),
        "pricing_sensitivity": parts.get("pricing_sensitivity"),
    }
    out_path = PHASE9_OUT / "expanded_experiments.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_path}")
    return result


if __name__ == "__main__":
    print("=== Phase 9 result extraction ===")
    try:
        r1 = extract_fleet_size_sweep()
        print(f"  fleet10 gap: {r1['fleet_sizes'][10]['gap']}")
        print(f"  fleet15 gap: {r1['fleet_sizes'][15]['gap']}")
        print(f"  fleet20 gap: {r1['fleet_sizes'][20]['gap']}")
    except RuntimeError as e:
        print(f"[fleet_size_sweep] {e}")

    try:
        r2 = extract_demand_sweep()
        print(f"  demand 0.7x gap: {r2['demand_levels']['0.7x']['gap']}")
        print(f"  demand 1.0x gap: {r2['demand_levels']['1.0x']['gap']}")
        print(f"  demand 1.3x gap: {r2['demand_levels']['1.3x']['gap']}")
    except RuntimeError as e:
        print(f"[demand_sweep] {e}")

    try:
        r3 = extract_pricing_sensitivity()
        baseline = next((e for e in r3["grid"] if e["R"] == 50 and e["p_min"] == -6), None)
        if baseline:
            print(f"  baseline (R=50, p_min=-6) gap: {baseline['gap']}, floor_frac: {baseline['price_at_floor_fraction']}")
    except RuntimeError as e:
        print(f"[pricing_sensitivity] {e}")

    try:
        consolidate()
    except Exception as e:
        print(f"[consolidate] {e}")
