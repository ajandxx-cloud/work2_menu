"""Post-processing script for Phase 24 welfare-distribution outputs.

Builds compact quantile and heterogeneity summaries from completed study outputs.

Usage:
    python scripts/extract_phase24_results.py
"""

import json
import os
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Src.research_pipeline import load_study_summary

PHASE24_OUT = ROOT / "outputs" / "phase24"
QUANTILE_POINTS = [10, 25, 50, 75, 90]
METRIC_KEYS = [
    "net_profit",
    "acceptance_rate",
    "non_home_acceptance_rate",
    "avg_walk_distance",
    "avg_pickup_time_deviation",
    "avg_in_vehicle_time",
    "consumer_surplus",
]


def _required_summary(study_name):
    summary, run_dir = load_study_summary(study_name)
    if summary is None or run_dir is None:
        raise RuntimeError(f"{study_name} study summary not found. Run the study first.")
    return summary, Path(run_dir)


def _load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _quantiles(values):
    arr = np.asarray(values, dtype=float)
    if arr.size == 0:
        return {"mean": 0.0, **{f"p{q}": 0.0 for q in QUANTILE_POINTS}}
    return {
        "mean": float(np.mean(arr)),
        **{f"p{q}": float(np.percentile(arr, q)) for q in QUANTILE_POINTS},
    }


def _episode_quantiles(episodes):
    return {metric: _quantiles([episode.get(metric, 0.0) for episode in episodes]) for metric in METRIC_KEYS}


def _heterogeneity_summary(episodes):
    acceptance = np.asarray([episode.get("acceptance_rate", 0.0) for episode in episodes], dtype=float)
    non_home = np.asarray([episode.get("non_home_acceptance_rate", 0.0) for episode in episodes], dtype=float)
    home = np.clip(acceptance - non_home, 0.0, 1.0)
    opt_out = np.asarray([episode.get("opt_out_rate", 0.0) for episode in episodes], dtype=float)
    displayed = np.asarray([episode.get("average_menu_size", 0.0) for episode in episodes], dtype=float)
    walk = np.asarray([episode.get("avg_walk_distance", 0.0) for episode in episodes], dtype=float)
    pickup_dev = np.asarray([episode.get("avg_pickup_time_deviation", 0.0) for episode in episodes], dtype=float)
    surplus = np.asarray([episode.get("consumer_surplus", 0.0) for episode in episodes], dtype=float)

    exposure_threshold = float(np.median(displayed)) if displayed.size > 0 else 0.0
    low_mask = displayed <= exposure_threshold
    high_mask = displayed > exposure_threshold

    def exposure_slice(mask):
        if not np.any(mask):
            return {
                "episode_count": 0,
                "mean_acceptance_rate": 0.0,
                "mean_non_home_acceptance_rate": 0.0,
                "mean_consumer_surplus": 0.0,
            }
        return {
            "episode_count": int(np.sum(mask)),
            "mean_acceptance_rate": float(np.mean(acceptance[mask])),
            "mean_non_home_acceptance_rate": float(np.mean(non_home[mask])),
            "mean_consumer_surplus": float(np.mean(surplus[mask])),
        }

    return {
        "outcome_mass": {
            "mean_opt_out_rate": float(np.mean(opt_out)) if opt_out.size > 0 else 0.0,
            "mean_home_acceptance_rate": float(np.mean(home)) if home.size > 0 else 0.0,
            "mean_non_home_acceptance_rate": float(np.mean(non_home)) if non_home.size > 0 else 0.0,
        },
        "service_quality": {
            "mean_walk_distance": float(np.mean(walk)) if walk.size > 0 else 0.0,
            "mean_pickup_time_deviation": float(np.mean(pickup_dev)) if pickup_dev.size > 0 else 0.0,
        },
        "menu_exposure_cut": {
            "threshold_average_menu_size": exposure_threshold,
            "lower_exposure": exposure_slice(low_mask),
            "higher_exposure": exposure_slice(high_mask),
        },
    }


def extract_phase24_outputs():
    studies = [
        ("phase22_eta_compare", ["deployed", "stronger"]),
        ("phase23_pricing_baselines", ["lambertw", "cost_plus", "flat_markdown"]),
    ]

    quantiles_payload = {"studies": {}, "variants": {}}
    heterogeneity_payload = {"studies": {}, "variants": {}}

    for study_name, variant_tags in studies:
        summary, run_dir = _required_summary(study_name)
        quantiles_payload["studies"][study_name] = {
            "run_id": summary.get("run_metadata", {}).get("run_id"),
            "status": summary.get("run_metadata", {}).get("status"),
        }
        heterogeneity_payload["studies"][study_name] = {
            "run_id": summary.get("run_metadata", {}).get("run_id"),
            "status": summary.get("run_metadata", {}).get("status"),
        }

        split_dirs = sorted((run_dir / "splits").glob("*"))
        episodes_by_variant = {tag: [] for tag in variant_tags}
        for split_dir in split_dirs:
            if not split_dir.is_dir():
                continue
            for tag in variant_tags:
                episode_path = split_dir / f"{tag}_episode_metrics.json"
                if episode_path.exists():
                    episodes_by_variant[tag].extend(_load_json(episode_path))

        for tag, episodes in episodes_by_variant.items():
            if not episodes:
                raise RuntimeError(f"No episode metrics found for {study_name}:{tag}")
            key = f"{study_name}:{tag}"
            quantiles_payload["variants"][key] = _episode_quantiles(episodes)
            heterogeneity_payload["variants"][key] = _heterogeneity_summary(episodes)

    os.makedirs(PHASE24_OUT, exist_ok=True)
    quantiles_path = PHASE24_OUT / "welfare_quantiles.json"
    heterogeneity_path = PHASE24_OUT / "welfare_heterogeneity.json"

    with open(quantiles_path, "w", encoding="utf-8") as f:
        json.dump(quantiles_payload, f, indent=2)
    with open(heterogeneity_path, "w", encoding="utf-8") as f:
        json.dump(heterogeneity_payload, f, indent=2)

    print(f"Saved: {quantiles_path}")
    print(f"Saved: {heterogeneity_path}")


if __name__ == "__main__":
    print("=== Phase 24 result extraction ===")
    extract_phase24_outputs()
