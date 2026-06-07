from pathlib import Path
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.research_pipeline import load_manifest, variant_specs_for_manifest

STUDIES_DIR = ROOT / "experiments" / "studies"

EXPECTED_MEMBERS = [
    "work2_menu_size_robustness",
    "work2_candidate_pool_robustness",
    "work2_demand_robustness",
    "work2_outside_option_robustness",
    "work2_cross_instance_robustness",
]

EXPECTED_DIMENSIONS = {
    "work2_menu_size_robustness": ("menu_size", "menu_k", 3),
    "work2_candidate_pool_robustness": ("candidate_pool_size", "max_candidates", 10),
    "work2_demand_robustness": ("demand_intensity", "max_steps_r", 700),
    "work2_outside_option_robustness": ("outside_option_utility", "outside_option_util", 0.0),
    "work2_cross_instance_robustness": ("cross_instance_generalization", "instance", "RC"),
}

REQUIRED_LABEL_PREFIXES = [
    "Cost-L heuristic",
    "CNN-Menu",
    "CNN-SetMenuNet",
    "Oracle Menu",
]

EXPECTED_RUNTIME_PROFILE = "diagnostic_gap_closure"


def _assert(condition, message):
    if not condition:
        raise AssertionError(message)


def _load_raw_study(name):
    path = STUDIES_DIR / f"{name}.yaml"
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _effective_values(manifest, key):
    values = {manifest.get("base_args", {}).get(key)}
    for policy in manifest.get("policies", []):
        values.add(policy.get("args_overrides", {}).get(key, manifest.get("base_args", {}).get(key)))
    return {value for value in values if value is not None}


def test_suite_contract():
    suite = load_manifest("work2_robustness")
    _assert(suite["_kind"] == "suite", "work2_robustness must load as a suite")
    _assert(suite.get("members") == EXPECTED_MEMBERS, f"unexpected suite members: {suite.get('members')}")
    _assert(
        "mixed and inconclusive Phase 4 pilot evidence" in suite.get("description", ""),
        "suite must preserve the mixed Phase 4 evidence framing",
    )


def test_study_contracts():
    for name in EXPECTED_MEMBERS:
        manifest = load_manifest(name)
        raw = _load_raw_study(name)
        expected_dimension, expected_parameter, expected_default = EXPECTED_DIMENSIONS[name]

        _assert(manifest["_kind"] == "study", f"{name} must load as a study")
        _assert(raw.get("name") == name, f"{name} must use stable work2_* naming")
        _assert(raw.get("robustness_dimension") == expected_dimension, f"{name} dimension mismatch")
        _assert(raw.get("dimension_parameter") == expected_parameter, f"{name} parameter mismatch")
        _assert(raw.get("dimension_default") == expected_default, f"{name} default mismatch")
        dimension_values = set(raw.get("dimension_values", []))
        _assert(expected_default in dimension_values, f"{name} must include default value")
        if name == "work2_cross_instance_robustness":
            _assert(
                any(value != "RC" for value in dimension_values),
                f"{name} must include at least one non-RC value",
            )
        else:
            _assert(len(dimension_values) >= 3, f"{name} must include at least two non-default values")

        _assert(raw.get("runtime_profile") == EXPECTED_RUNTIME_PROFILE, f"{name} must declare diagnostic gap-closure profile")
        _assert("diagnostic" in raw.get("description", "").lower(), f"{name} must label closure evidence as diagnostic")
        _assert("positive" in raw.get("description", "").lower(), f"{name} must reject positive-claim evidence by itself")

        base_args = raw.get("base_args", {})
        _assert(0 < base_args.get("max_episodes", 0) <= 4, f"{name} must use a small nonzero training budget")
        _assert(0 < base_args.get("eval_episodes", 0) <= 2, f"{name} must use a small nonzero eval budget")
        _assert(base_args.get("menu_k") == 3, f"{name} must keep default L=3 in base args")
        _assert(base_args.get("max_candidates") == 10, f"{name} must keep default K=10 in base args")
        _assert(base_args.get("outside_option_util") == 0.0, f"{name} must keep outside option baseline 0.0")

        labels = [policy.get("label", "") for policy in raw.get("policies", [])]
        for prefix in REQUIRED_LABEL_PREFIXES:
            _assert(any(label.startswith(prefix) for label in labels), f"{name} missing {prefix}")

        specs = variant_specs_for_manifest(manifest)
        _assert(specs, f"{name} must produce variant specs")


def test_required_dimension_values():
    menu_manifest = _load_raw_study("work2_menu_size_robustness")
    _assert(3 in _effective_values(menu_manifest, "menu_k"), "L=3 disappeared from menu-size sweep")

    candidate_manifest = _load_raw_study("work2_candidate_pool_robustness")
    _assert(10 in _effective_values(candidate_manifest, "max_candidates"), "K=10 disappeared from candidate-pool sweep")

    outside_manifest = _load_raw_study("work2_outside_option_robustness")
    _assert(0.0 in _effective_values(outside_manifest, "outside_option_util"), "outside-option baseline 0.0 disappeared")

    cross_manifest = _load_raw_study("work2_cross_instance_robustness")
    _assert(cross_manifest.get("base_args", {}).get("instance") != "RC", "cross-instance study must run a non-RC instance")


def main():
    test_suite_contract()
    test_study_contracts()
    test_required_dimension_values()
    print(
        "PASS work2 robustness manifests: suite + five EXP-07 studies, "
        "K=10, L=3, outside-option 0.0, Austin cross-instance, diagnostic gap-closure budget."
    )


if __name__ == "__main__":
    main()
