import numpy as np
import torch


FEATURE_ORDER = (
    "walk_distance",
    "predicted_ivt",
    "remaining_capacity",
    "distance_to_destination",
    "option_type",
    "arrival_time",
)


def _as_float_array(raw, key, length):
    values = raw.get(key)
    if values is None:
        return np.zeros(length, dtype=np.float32)
    return np.asarray(values, dtype=np.float32).reshape(-1)


def normalize_features(raw, menu_time_scale, menu_target_arrival_time):
    """Normalize the six-column menu option feature schema deterministically."""
    if not raw:
        return {key: np.zeros(0, dtype=np.float32) for key in FEATURE_ORDER}

    first_key = next(iter(raw))
    length = len(np.asarray(raw[first_key]).reshape(-1))
    scale = max(float(menu_time_scale), 1.0)
    target = float(menu_target_arrival_time)

    normed = {}
    normed["walk_distance"] = _as_float_array(raw, "walk_distance", length) / scale
    normed["predicted_ivt"] = _as_float_array(raw, "predicted_ivt", length) / scale
    normed["remaining_capacity"] = _as_float_array(raw, "remaining_capacity", length)
    normed["distance_to_destination"] = _as_float_array(raw, "distance_to_destination", length) / scale
    normed["option_type"] = _as_float_array(raw, "option_type", length)
    normed["arrival_time"] = (_as_float_array(raw, "arrival_time", length) - target) / scale
    return normed


def build_option_tensor(normed, max_k, device=None):
    """Return a fixed max_k x 6 feature tensor plus a boolean valid-row mask."""
    max_k = int(max_k)
    features = torch.zeros((max_k, len(FEATURE_ORDER)), dtype=torch.float32, device=device)
    mask = torch.zeros(max_k, dtype=torch.bool, device=device)
    if not normed:
        return features, mask

    arrays = [np.asarray(normed.get(key, []), dtype=np.float32).reshape(-1) for key in FEATURE_ORDER]
    row_count = min(max((len(arr) for arr in arrays), default=0), max_k)
    if row_count == 0:
        return features, mask

    matrix = np.zeros((row_count, len(FEATURE_ORDER)), dtype=np.float32)
    for col, arr in enumerate(arrays):
        if len(arr) > 0:
            matrix[:, col] = arr[:row_count]
    features[:row_count] = torch.tensor(matrix, dtype=torch.float32, device=device)
    mask[:row_count] = True
    return features, mask
