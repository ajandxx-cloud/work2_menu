"""Per-candidate option feature extraction for DRT service menu models.

Provides pure tensor construction utilities used by DSPO_Menu and
downstream models (SetMenuNet, CNN-SetMenuNet, MLP-Menu).

Feature vector (6-dim per candidate):
    [0] walk_distance     — customer-to-pickup travel distance/time
    [1] predicted_ivt     — in-vehicle time from pickup to depot
    [2] remaining_capacity — remaining slots at the pickup point
    [3] distance_to_destination — travel time from pickup to depot
    [4] option_type       — 1.0 for home delivery, 0.0 for parcel point
    [5] arrival_time      — centered ETA (eta - target) / time_scale
"""

import math
import numpy as np
import torch

_FEATURE_KEYS = [
    "walk_distance",
    "predicted_ivt",
    "remaining_capacity",
    "distance_to_destination",
    "option_type",
    "arrival_time",
]


def normalize_features(raw: dict, time_scale: float, target_time: float) -> dict:
    """Normalize raw feature arrays for neural network consumption.

    Args:
        raw: Dict mapping feature key -> 1-D numpy array of length K.
        time_scale: Divisor for time-based features (seconds).
        target_time: Center value for ETA normalization (seconds).

    Returns:
        Dict with same keys, values as float32 numpy arrays.
    """
    out = {}
    for key in _FEATURE_KEYS:
        arr = np.asarray(raw[key], dtype=np.float64)

        if key == "predicted_ivt":
            arr = arr / time_scale
        elif key == "distance_to_destination":
            arr = arr / time_scale
        elif key == "arrival_time":
            arr = (arr - target_time) / time_scale

        out[key] = arr.astype(np.float32)
    return out


def build_option_tensor(normalized: dict, max_k: int, device) -> tuple:
    """Convert normalized feature arrays to padded (K, 6) tensor + mask.

    Args:
        normalized: Dict from normalize_features with keys matching
                    _FEATURE_KEYS.  Each value is a 1-D array of length
                    actual_k (may be < max_k).
        max_k:      Padded sequence length.  If actual_k < max_k the
                    remaining rows are zero-filled and masked False.
        device:     torch device for the returned tensors.

    Returns:
        features: Tensor[max_k, 6]  float32
        mask:     Tensor[max_k]     bool — True for real candidates
    """
    actual_k = len(normalized[_FEATURE_KEYS[0]])
    k = min(actual_k, max_k)

    features = np.zeros((max_k, len(_FEATURE_KEYS)), dtype=np.float32)
    for col, key in enumerate(_FEATURE_KEYS):
        features[:k, col] = normalized[key][:k]

    # Numerical safety: replace NaN/inf with 0
    bad = ~np.isfinite(features)
    features[bad] = 0.0

    mask = np.zeros(max_k, dtype=bool)
    mask[:k] = True
    # Also mask out rows where ALL features are zero beyond actual_k
    # (already handled by the slice above)

    features_t = torch.tensor(features, dtype=torch.float32, device=device)
    mask_t = torch.tensor(mask, dtype=torch.bool, device=device)

    return features_t, mask_t
