import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.policy_adapters import adapter_metadata, adapter_overrides, known_policy_tags, mainline_policy_tags  # noqa: E402


MAINLINE_EXPECTED = {
    "mainline_no_menu": {
        "menu_policy": "home_only",
        "product_mode": "m",
        "time_window_mode": "no_time_window",
        "menu_contract_mode": "no_menu",
        "menu_pricing_mode": "no_pricing",
        "comparison_role": "menu_baseline",
    },
    "mainline_fixed_menu": {
        "menu_policy": "nearest_heuristic",
        "product_mode": "m+w+p",
        "time_window_mode": "fixed_window",
        "menu_contract_mode": "fixed_menu",
        "menu_pricing_mode": "lambertw",
        "comparison_role": "menu_baseline",
    },
    "mainline_random_menu": {
        "menu_policy": "random_top_k",
        "product_mode": "m+w+p",
        "time_window_mode": "fixed_window",
        "menu_contract_mode": "random_menu",
        "menu_pricing_mode": "lambertw",
        "comparison_role": "menu_baseline",
    },
    "mainline_optimized_m": {
        "menu_policy": "service_guarded_expected_profit",
        "product_mode": "m",
        "time_window_mode": "no_time_window",
        "menu_contract_mode": "optimized_menu",
        "menu_pricing_mode": "no_pricing",
        "comparison_role": "product_ablation",
    },
    "mainline_optimized_mw": {
        "menu_policy": "service_guarded_expected_profit",
        "product_mode": "m+w",
        "time_window_mode": "adaptive_window",
        "menu_contract_mode": "optimized_menu",
        "menu_pricing_mode": "no_pricing",
        "comparison_role": "product_ablation",
    },
    "mainline_optimized_fixed_window": {
        "menu_policy": "service_guarded_expected_profit",
        "product_mode": "m+w+p",
        "time_window_mode": "fixed_window",
        "menu_contract_mode": "optimized_menu",
        "menu_pricing_mode": "lambertw",
        "comparison_role": "time_window_ablation",
    },
    "mainline_optimized_adaptive": {
        "menu_policy": "service_guarded_expected_profit",
        "product_mode": "m+w+p",
        "time_window_mode": "adaptive_window",
        "menu_contract_mode": "optimized_menu",
        "menu_pricing_mode": "lambertw",
        "comparison_role": "primary_method",
    },
}


def test_phase2_menu_mode_tags_are_known():
    tags = set(known_policy_tags(include_optional=True))
    for tag in {
        "contract_no_menu",
        "contract_fixed_menu",
        "contract_random_menu",
        "contract_optimized_menu",
    }:
        assert tag in tags


def test_no_menu_maps_to_single_home_contract():
    overrides = adapter_overrides("contract_no_menu")
    metadata = adapter_metadata("contract_no_menu")
    assert overrides["menu_policy"] == "home_only"
    assert overrides["menu_contract_mode"] == "no_menu"
    assert overrides["product_mode"] == "m"
    assert overrides["time_window_mode"] == "no_time_window"
    assert overrides["menu_pricing_mode"] == "no_pricing"
    assert metadata["menu_mode"] == "no_menu"


def test_fixed_random_and_optimized_menu_mappings():
    fixed = adapter_overrides("contract_fixed_menu")
    random = adapter_overrides("contract_random_menu")
    optimized = adapter_overrides("contract_optimized_menu")
    assert fixed["menu_policy"] == "nearest_heuristic"
    assert fixed["menu_contract_mode"] == "fixed_menu"
    assert random["menu_policy"] == "random_top_k"
    assert random["menu_contract_mode"] == "random_menu"
    assert optimized["menu_policy"] == "service_guarded_expected_profit"
    assert optimized["menu_contract_mode"] == "optimized_menu"
    assert optimized["time_window_mode"] == "adaptive_window"


def test_no_filter_diagnostic_does_not_claim_no_time_window():
    overrides = adapter_overrides("no_filter_diagnostic")
    metadata = adapter_metadata("no_filter_diagnostic")
    assert overrides["menu_eta_filter_mode"] == "none"
    assert overrides["menu_time_filtering"] is False
    assert "time_window_mode" not in overrides
    assert metadata["diagnostic"] is True


def test_mainline_tags_are_known_and_exact():
    assert mainline_policy_tags() == list(MAINLINE_EXPECTED.keys())
    tags = set(known_policy_tags(include_optional=True))
    assert set(MAINLINE_EXPECTED).issubset(tags)
    for tag, expected in MAINLINE_EXPECTED.items():
        overrides = adapter_overrides(tag)
        metadata = adapter_metadata(tag)
        for key, value in expected.items():
            if key == "comparison_role":
                assert metadata[key] == value
            else:
                assert overrides[key] == value


def test_mainline_optimized_tags_use_service_guard():
    for tag in {
        "mainline_optimized_m",
        "mainline_optimized_mw",
        "mainline_optimized_fixed_window",
        "mainline_optimized_adaptive",
    }:
        overrides = adapter_overrides(tag)
        assert overrides["menu_policy"] == "service_guarded_expected_profit"
        assert overrides["menu_eta_filter_mode"] == "interval_overlap"
        assert overrides["service_quit_rate_guardrail"] == 0.35


def main():
    tests = [
        test_phase2_menu_mode_tags_are_known,
        test_no_menu_maps_to_single_home_contract,
        test_fixed_random_and_optimized_menu_mappings,
        test_no_filter_diagnostic_does_not_claim_no_time_window,
        test_mainline_tags_are_known_and_exact,
        test_mainline_optimized_tags_use_service_guard,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} menu mode adapter tests")


if __name__ == "__main__":
    main()
