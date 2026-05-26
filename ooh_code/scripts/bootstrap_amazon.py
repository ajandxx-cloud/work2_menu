#!/usr/bin/env python3
"""
Paired bootstrap CI for v2 vs full-display net-profit gap on Amazon Last Mile instances.
B=1000 resamples of 2 split-level mean_net_profit_gap values per city.
Note: n=2 splits per city — CI is unreliable due to small sample; reported for completeness.
"""
import json
import os
import warnings
import numpy as np

CITIES = {
    "austin": {
        "study_dir": "outputs/studies/austin_main",
        "split_ids": ["austin_0_to_1", "austin_1_to_0"],
    },
    "seattle": {
        "study_dir": "outputs/studies/seattle_main",
        "split_ids": ["seattle_0_to_1", "seattle_1_to_0"],
    },
}
PAIRED_FILES = [
    "menu_optimization_v2_paired_vs_full_display.json",
    "menu_optimization_paired_vs_full_display.json",  # fallback
]
OUTPUT_PATH = "outputs/phase11/bootstrap_amazon.json"
B = 1000
SEED = 42


def find_latest_run(study_dir):
    runs = sorted(
        d for d in os.listdir(study_dir)
        if os.path.isdir(os.path.join(study_dir, d))
    )
    if not runs:
        raise FileNotFoundError(f"No run directories found in {study_dir}")
    return os.path.join(study_dir, runs[-1])


def read_gap(run_dir, split_id):
    for fname in PAIRED_FILES:
        path = os.path.join(run_dir, "splits", split_id, fname)
        if os.path.exists(path):
            if fname != PAIRED_FILES[0]:
                warnings.warn(f"Using fallback file {fname} for {split_id}")
            with open(path) as f:
                data = json.load(f)
            return data["mean_net_profit_gap"]
    raise FileNotFoundError(
        f"No paired file found for {split_id} in {run_dir}"
    )


def bootstrap_city(gaps, rng):
    gaps = np.array(gaps)
    observed_mean = float(np.mean(gaps))
    boot_means = np.array([
        float(np.mean(rng.choice(gaps, size=len(gaps), replace=True)))
        for _ in range(B)
    ])
    return {
        "n_splits": len(gaps),
        "split_gaps": gaps.tolist(),
        "observed_mean": observed_mean,
        "bootstrap_std": float(np.std(boot_means)),
        "ci_lower": float(np.percentile(boot_means, 2.5)),
        "ci_upper": float(np.percentile(boot_means, 97.5)),
    }


def main():
    rng = np.random.default_rng(SEED)
    result = {
        "B": B,
        "seed": SEED,
        "ci_level": 0.95,
        "note": (
            "Paired bootstrap CI. n=2 splits per city — "
            "CI is unreliable due to small sample; reported for completeness."
        ),
    }

    for city, cfg in CITIES.items():
        run_dir = find_latest_run(cfg["study_dir"])
        print(f"\n{city.capitalize()}: using run {run_dir}")
        gaps = []
        for split_id in cfg["split_ids"]:
            gap = read_gap(run_dir, split_id)
            gaps.append(gap)
            print(f"  {split_id}: gap = {gap:.4f}")

        city_result = bootstrap_city(gaps, rng)
        city_result["study"] = f"{city}_main"
        city_result["policy"] = "menu_optimization_v2"
        city_result["reference"] = "full_display"
        result[city] = city_result
        print(f"  95% CI: [{city_result['ci_lower']:.4f}, {city_result['ci_upper']:.4f}]")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nSaved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
