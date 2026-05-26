#!/usr/bin/env python3
"""
Paired bootstrap CI for v2 vs full-display net-profit gap on RC benchmark.
B=1000 resamples of 6 split-level mean_net_profit_gap values.
"""
import json
import os
import numpy as np

SPLIT_IDS = [
    "rc_0_to_1",
    "rc_1_to_0",
    "rc_0_to_1_seed2025",
    "rc_2_to_3",
    "rc_3_to_2",
    "rc_4_to_2",
]
STUDY_DIR = "outputs/studies/rc_main_optout"
PAIRED_FILE = "menu_optimization_v2_paired_vs_full_display.json"
OUTPUT_PATH = "outputs/phase11/bootstrap_rc.json"
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


def main():
    run_dir = find_latest_run(STUDY_DIR)
    print(f"Using run: {run_dir}")

    gaps = []
    for split_id in SPLIT_IDS:
        path = os.path.join(run_dir, "splits", split_id, PAIRED_FILE)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing: {path}")
        with open(path) as f:
            data = json.load(f)
        gap = data["mean_net_profit_gap"]
        gaps.append(gap)
        print(f"  {split_id}: gap = {gap:.4f}")

    gaps = np.array(gaps)
    observed_mean = float(np.mean(gaps))

    rng = np.random.default_rng(SEED)
    boot_means = [
        float(np.mean(rng.choice(gaps, size=len(gaps), replace=True)))
        for _ in range(B)
    ]
    boot_means = np.array(boot_means)

    ci_lower = float(np.percentile(boot_means, 2.5))
    ci_upper = float(np.percentile(boot_means, 97.5))
    bootstrap_std = float(np.std(boot_means))

    result = {
        "study": "rc_main_optout",
        "policy": "menu_optimization_v2",
        "reference": "full_display",
        "metric": "mean_net_profit_gap",
        "n_splits": len(gaps),
        "B": B,
        "seed": SEED,
        "split_gaps": gaps.tolist(),
        "observed_mean": observed_mean,
        "bootstrap_std": bootstrap_std,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "ci_level": 0.95,
        "note": (
            "Paired bootstrap CI. "
            "Unit of resampling: split-level mean net-profit gap (v2 minus full display)."
        ),
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nSaved to {OUTPUT_PATH}")
    print(f"Observed mean: {observed_mean:.4f}")
    print(f"95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")


if __name__ == "__main__":
    main()
