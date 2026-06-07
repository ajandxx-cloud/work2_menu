"""Smoke test for option_features utility.

Usage:  python scripts/test_option_features.py
Run from ooh_code/ directory.
"""

import sys
import os
import math
import numpy as np
import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from Src.Utils.option_features import normalize_features, build_option_tensor


def test_shape_k10():
    """Public K=10 meeting points plus home produce tensor [11, 6]."""
    raw = {
        "walk_distance": np.random.rand(11) * 1000,
        "predicted_ivt": np.random.rand(11) * 600,
        "remaining_capacity": np.random.randint(1, 25, size=11).astype(float),
        "distance_to_destination": np.random.rand(11) * 600,
        "option_type": np.array([1.0] + [0.0] * 10),
        "arrival_time": np.random.rand(11) * 3600 + 27000,
    }
    normed = normalize_features(raw, time_scale=3600.0, target_time=30600.0)
    features, mask = build_option_tensor(normed, max_k=11, device=torch.device("cpu"))

    assert features.shape == (11, 6), f"Expected (11, 6), got {features.shape}"
    assert mask.shape == (11,), f"Expected (11,), got {mask.shape}"
    assert mask.all(), "Home plus all 10 meeting points should be masked True"
    assert features[0, 4].item() == 1.0, "Home row should be index 0"
    assert torch.all(features[1:, 4] == 0.0), "Meeting-point rows should have option_type 0"
    assert features.dtype == torch.float32
    assert mask.dtype == torch.bool
    return True


def test_padding():
    """Home plus four meeting points padded to candidate_slots=11 has correct mask."""
    raw = {
        "walk_distance": np.random.rand(5) * 1000,
        "predicted_ivt": np.random.rand(5) * 600,
        "remaining_capacity": np.random.randint(1, 25, size=5).astype(float),
        "distance_to_destination": np.random.rand(5) * 600,
        "option_type": np.array([1.0, 0.0, 0.0, 0.0, 0.0]),
        "arrival_time": np.random.rand(5) * 3600 + 27000,
    }
    normed = normalize_features(raw, time_scale=3600.0, target_time=30600.0)
    features, mask = build_option_tensor(normed, max_k=11, device=torch.device("cpu"))

    assert features.shape == (11, 6), f"Expected (11, 6), got {features.shape}"
    assert mask[:5].all(), "First 5 should be True"
    assert not mask[5:].any(), "Last 5 should be False (padding)"
    assert (features[5:] == 0).all(), "Padding rows should be zero"
    return True


def test_normalization():
    """Normalized features have reasonable ranges."""
    time_scale = 3600.0
    target_time = 30600.0
    raw = {
        "walk_distance": np.array([0.0, 500.0, 1200.0]),
        "predicted_ivt": np.array([0.0, 300.0, 900.0]),
        "remaining_capacity": np.array([1000000.0, 25.0, 3.0]),
        "distance_to_destination": np.array([600.0, 300.0, 900.0]),
        "option_type": np.array([1.0, 0.0, 0.0]),
        "arrival_time": np.array([30300.0, 30000.0, 29700.0]),
    }
    normed = normalize_features(raw, time_scale, target_time)

    # IVT should be divided by time_scale
    assert abs(normed["predicted_ivt"][1] - 300.0 / 3600.0) < 1e-5
    # distance_to_destination normalized
    assert abs(normed["distance_to_destination"][0] - 600.0 / 3600.0) < 1e-5
    # arrival_time centered and scaled: (30300 - 30600) / 3600 = -0.0833
    assert abs(normed["arrival_time"][0] - (-300.0 / 3600.0)) < 1e-5
    # walk_distance and capacity NOT normalized
    assert abs(normed["walk_distance"][1] - 500.0) < 1e-5
    assert abs(normed["remaining_capacity"][1] - 25.0) < 1e-5
    return True


def test_nan_handling():
    """NaN and inf in features are replaced with 0 and masked False."""
    raw = {
        "walk_distance": np.array([100.0, float("nan"), 300.0]),
        "predicted_ivt": np.array([0.0, 100.0, float("inf")]),
        "remaining_capacity": np.array([10.0, 5.0, 3.0]),
        "distance_to_destination": np.array([200.0, 100.0, 50.0]),
        "option_type": np.array([1.0, 0.0, 0.0]),
        "arrival_time": np.array([30000.0, 30100.0, 30200.0]),
    }
    normed = normalize_features(raw, time_scale=3600.0, target_time=30600.0)
    features, mask = build_option_tensor(normed, max_k=3, device=torch.device("cpu"))

    assert features.shape == (3, 6)
    assert torch.isfinite(features).all(), "No NaN or inf should remain"
    return True


def test_home_first():
    """Home candidate (option_type=1) is at index 0."""
    raw = {
        "walk_distance": np.array([0.0, 500.0, 800.0]),
        "predicted_ivt": np.array([0.0, 300.0, 600.0]),
        "remaining_capacity": np.array([1000000.0, 20.0, 15.0]),
        "distance_to_destination": np.array([400.0, 300.0, 600.0]),
        "option_type": np.array([1.0, 0.0, 0.0]),
        "arrival_time": np.array([30300.0, 30000.0, 29700.0]),
    }
    normed = normalize_features(raw, time_scale=3600.0, target_time=30600.0)
    features, mask = build_option_tensor(normed, max_k=3, device=torch.device("cpu"))

    # option_type is column 4
    assert features[0, 4].item() == 1.0, "Home should be first (type=1)"
    assert features[1, 4].item() == 0.0, "PP should be type=0"
    # walk_distance is column 0
    assert features[0, 0].item() == 0.0, "Home walk_distance should be 0"
    # remaining_capacity is column 2
    assert features[0, 2].item() == 1000000.0, "Home capacity should be large"
    return True


def test_home_only_candidate_slots():
    """No feasible meeting points still yields valid home-only [K+1, 6] tensor."""
    raw = {
        "walk_distance": np.array([0.0]),
        "predicted_ivt": np.array([0.0]),
        "remaining_capacity": np.array([1000000.0]),
        "distance_to_destination": np.array([400.0]),
        "option_type": np.array([1.0]),
        "arrival_time": np.array([30300.0]),
    }
    normed = normalize_features(raw, time_scale=3600.0, target_time=30600.0)
    features, mask = build_option_tensor(normed, max_k=11, device=torch.device("cpu"))

    assert features.shape == (11, 6), f"Expected (11, 6), got {features.shape}"
    assert mask[0].item() is True, "Home row should be valid"
    assert not mask[1:].any(), "Meeting-point/padding rows should be masked False"
    assert features[0, 4].item() == 1.0, "Home row should have option_type 1"
    assert torch.all(features[1:] == 0), "Padding rows should remain zero"
    return True


if __name__ == "__main__":
    tests = [
        ("Shape K=10 plus home", test_shape_k10),
        ("Padding K=5→10", test_padding),
        ("Normalization", test_normalization),
        ("NaN handling", test_nan_handling),
        ("Home first", test_home_first),
        ("Home-only K=10", test_home_only_candidate_slots),
    ]

    passed = 0
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"  PASS  {name}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  {name}: {e}")
            failed += 1

    print(f"\n{passed}/{passed + failed} tests passed")
    if failed > 0:
        sys.exit(1)
