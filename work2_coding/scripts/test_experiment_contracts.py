import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.experiment_contracts import (  # noqa: E402
    load_manifest,
    load_suite,
    manifest_hash,
    parser_choices,
    resolve_policy_args,
    suite_members,
    validate_manifest,
)
from Src.policy_adapters import mainline_policy_tags, required_policy_tags  # noqa: E402


def expect_value_error(fn, contains):
    try:
        fn()
    except ValueError as exc:
        assert contains in str(exc), str(exc)
        return
    raise AssertionError("expected ValueError containing: " + contains)


def test_parser_choices_are_available():
    choices = parser_choices()
    assert "menu_policy" in choices
    assert "risk_adjusted_expected_profit" in choices["menu_policy"]
    assert "menu_eta_filter_mode" in choices
    assert "chance_constraint" in choices["menu_eta_filter_mode"]
    assert "product_mode" in choices
    assert "m+w+p" in choices["product_mode"]
    assert "time_window_mode" in choices
    assert "adaptive_window" in choices["time_window_mode"]
    assert "menu_contract_mode" in choices
    assert "optimized_menu" in choices["menu_contract_mode"]


def test_valid_manifests_load():
    for name in [
        "smoke_robust_menu",
        "diagnostic_actual_menu",
        "pilot_robust_menu",
        "formal_robust_menu",
        "phase8_baseline_validation",
        "phase8_sensitivity_menu_k",
        "phase8_sensitivity_eta_filter",
        "phase8_sensitivity_uptake_regime",
        "phase8_sensitivity_guardrail",
        "phase9_dspo_family_validation",
    ]:
        manifest = load_manifest(name)
        assert manifest["name"] == name
        assert manifest["output_schema"].get("normalized-row-v1") is True or manifest["output_schema"].get("normalized-row-v2") is True
        tags = {policy["tag"] for policy in manifest["policies"]}
        if name == "phase8_baseline_validation":
            assert tags == {"mainline_optimized_mw", "phase8_static_flat_markdown"}
        elif name.startswith("phase8_sensitivity_"):
            assert tags == {"mainline_optimized_adaptive"}
        elif name == "phase9_dspo_family_validation":
            assert tags == {"dspo_clip", "dspo_wide"}
        elif name == "diagnostic_actual_menu":
            assert set(required_policy_tags()).issubset(tags)
        else:
            assert set(mainline_policy_tags()).issubset(tags)


def test_phase2_contract_manifest_covers_menu_k_set():
    manifest = load_manifest("smoke_phase2_service_product_contract")
    assert manifest["output_schema"]["normalized-row-v2"] is True
    assert {split["args_overrides"]["menu_k"] for split in manifest["splits"]} == {1, 2, 3, 5}
    tags = {policy["tag"] for policy in manifest["policies"]}
    assert tags == {
        "contract_no_menu",
        "contract_fixed_menu",
        "contract_random_menu",
        "contract_optimized_menu",
    }


def test_manifest_hash_stability():
    manifest = load_manifest("smoke_robust_menu")
    first = manifest_hash(manifest)
    second = manifest_hash(manifest)
    assert first == second
    changed = copy.deepcopy(manifest)
    changed["description"] = changed["description"] + " changed"
    assert manifest_hash(changed) != first


def test_policy_resolution_is_parser_compatible():
    manifest = load_manifest("smoke_robust_menu")
    split = manifest["splits"][0]
    for policy in manifest["policies"]:
        args = resolve_policy_args(manifest, split, policy)
        assert args["algo_name"] == "DSPO_Menu"
        assert args["menu_mode"] is True
        assert args["menu_policy"] in parser_choices()["menu_policy"]
        assert args["menu_eta_filter_mode"] in parser_choices()["menu_eta_filter_mode"]


def test_no_filter_is_diagnostic():
    manifest = load_manifest("diagnostic_actual_menu")
    no_filter = [p for p in manifest["policies"] if p["tag"] == "no_filter_diagnostic"][0]
    assert no_filter["diagnostic"] is True
    args = resolve_policy_args(manifest, manifest["splits"][0], no_filter)
    assert args["menu_eta_filter_mode"] == "none"
    assert args["menu_time_filtering"] is False


def test_mainline_manifests_use_required_family_and_row_v2():
    for name in ["smoke_robust_menu", "pilot_robust_menu", "formal_robust_menu"]:
        manifest = load_manifest(name)
        assert manifest["required_policy_tags"] == mainline_policy_tags()
        assert manifest["output_schema"]["normalized-row-v2"] is True
        tags = [policy["tag"] for policy in manifest["policies"]]
        assert tags == mainline_policy_tags()
        assert "no_filter_diagnostic" not in tags
        for field in [
            "method_family",
            "outside_option_util",
            "product_mode",
            "time_window_mode",
            "menu_mode",
            "pricing_mode",
            "method",
            "candidate_id",
            "status",
            "execution_status",
            "net_profit",
            "served_rate",
        ]:
            assert field in manifest["output_schema"]["fields"]


def test_mainline_menu_k_contracts():
    smoke = load_manifest("smoke_robust_menu")
    pilot = load_manifest("pilot_robust_menu")
    formal = load_manifest("formal_robust_menu")
    assert {split["args_overrides"]["menu_k"] for split in smoke["splits"]} == {1, 2, 3, 5}
    assert {split["args_overrides"]["menu_k"] for split in pilot["splits"]} == {1, 2, 3, 5}
    assert formal["base_args"]["menu_k"] == 3
    assert all("menu_k" not in (split.get("args_overrides") or {}) for split in formal["splits"])
    assert len(formal["splits"]) >= 5


def test_pilot_and_formal_require_checkpoint_contract():
    for name in ["pilot_robust_menu", "formal_robust_menu", "phase8_baseline_validation"]:
        manifest = load_manifest(name)
        assert manifest["shared_checkpoint"]["required"] is True
        assert manifest["base_args"]["require_checkpoint"] is True
        assert manifest["base_args"]["checkpoint_path"]


def test_phase8_baseline_manifest_contract():
    manifest = load_manifest("phase8_baseline_validation")
    assert manifest["tier"] == "formal"
    assert manifest["run_mode"] == "formal"
    assert manifest["required_policy_tags"] == ["mainline_optimized_mw", "phase8_static_flat_markdown"]
    assert len(manifest["splits"]) == 5
    assert {split["uptake_regime"] for split in manifest["splits"]} == {"low", "medium"}
    assert manifest["base_args"]["menu_pricing_constant"] == -3.0
    assert manifest["base_args"]["checkpoint_path"] == manifest["shared_checkpoint"]["path"]

    no_pricing = resolve_policy_args(manifest, manifest["splits"][0], {"tag": "mainline_optimized_mw"})
    static = resolve_policy_args(manifest, manifest["splits"][0], {"tag": "phase8_static_flat_markdown"})
    assert no_pricing["product_mode"] == "m+w"
    assert no_pricing["menu_pricing_mode"] == "no_pricing"
    assert static["product_mode"] == "m+w+p"
    assert static["menu_pricing_mode"] == "flat_markdown"
    assert static["menu_pricing_constant"] == -3.0


def test_phase8_sensitivity_suite_contract():
    suite = load_suite("phase8_sensitivity_must_have")
    assert suite_members(suite) == [
        "phase8_sensitivity_menu_k",
        "phase8_sensitivity_eta_filter",
        "phase8_sensitivity_uptake_regime",
        "phase8_sensitivity_guardrail",
    ]
    assert suite["claim_ready"] is False
    for name in suite_members(suite):
        manifest = load_manifest(name)
        assert manifest["tier"] == "pilot"
        assert manifest["run_mode"] == "diagnostic"
        assert manifest["claim_ready"] is False
        assert manifest["baseline_validation_required"].endswith("PHASE8_BASELINE_VALIDATION.json")
        assert manifest["shared_checkpoint"]["required"] is True
        assert manifest["base_args"]["require_checkpoint"] is True
        assert manifest["base_args"]["checkpoint_path"] == manifest["shared_checkpoint"]["path"]


def test_phase9_dspo_family_manifest_contract():
    phase8 = load_manifest("phase8_baseline_validation")
    phase9 = load_manifest("phase9_dspo_family_validation")
    assert phase9["tier"] == "formal"
    assert phase9["run_mode"] == "formal"
    assert phase9["required_policy_tags"] == ["dspo_clip", "dspo_wide"]
    assert [policy["tag"] for policy in phase9["policies"]] == ["dspo_clip", "dspo_wide"]
    assert "mainline_optimized_mw" not in phase9["required_policy_tags"]
    assert "phase8_static_flat_markdown" not in phase9["required_policy_tags"]
    assert all(not policy["tag"].startswith("dspo_plus_") for policy in phase9["policies"])
    assert len(phase9["splits"]) == 5
    assert phase9["shared_checkpoint"]["required"] is True
    assert phase9["shared_checkpoint"]["expected_status"] == "loaded"
    assert phase9["shared_checkpoint"]["path"] == "outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt"
    assert phase9["base_args"]["checkpoint_path"] == phase9["shared_checkpoint"]["path"]
    assert phase9["base_args"]["require_checkpoint"] is True
    assert phase9["base_args"]["allow_checkpoint_mismatch"] is False

    for field, expected in {
        "menu_k": 3,
        "max_candidates": 8,
        "menu_exact_threshold": 8,
        "menu_exact_gap_threshold": 8,
        "hgs_reopt_time": 0.1,
        "hgs_final_time": 0.1,
        "max_episodes": 1,
        "max_steps_r": 20,
        "max_steps_p": 0.7,
        "n_vehicles": 2,
        "veh_capacity": 3,
    }.items():
        assert phase9["base_args"][field] == expected
        assert phase9["base_args"][field] == phase8["base_args"][field]

    split_fields = ["split_id", "seed", "data_seed", "data_seed_test", "uptake_regime"]
    override_fields = ["home_util", "base_util", "incentive_sens"]
    for split8, split9 in zip(phase8["splits"], phase9["splits"]):
        for field in split_fields:
            assert split9[field] == split8[field]
        for field in override_fields:
            assert split9["args_overrides"][field] == split8["args_overrides"][field]

    clip = resolve_policy_args(phase9, phase9["splits"][0], {"tag": "dspo_clip"})
    wide = resolve_policy_args(phase9, phase9["splits"][0], {"tag": "dspo_wide"})
    assert clip["service_quit_rate_guardrail"] == 0.35
    assert clip["menu_optout_guardrail"] == 0.35
    assert wide["service_quit_rate_guardrail"] == 0.45
    assert wide["menu_optout_guardrail"] == 0.45


def test_duplicate_policy_rejected():
    manifest = load_manifest("smoke_robust_menu")
    broken = copy.deepcopy(manifest)
    broken["policies"].append(copy.deepcopy(broken["policies"][0]))
    expect_value_error(lambda: validate_manifest(broken), "duplicate policy tags")


def test_invalid_filter_rejected():
    manifest = load_manifest("smoke_robust_menu")
    broken = copy.deepcopy(manifest)
    broken["policies"][0]["args_overrides"] = {"menu_eta_filter_mode": "bogus"}
    expect_value_error(lambda: validate_manifest(broken), "menu_eta_filter_mode")


def test_duplicate_split_rejected():
    manifest = load_manifest("smoke_robust_menu")
    broken = copy.deepcopy(manifest)
    broken["splits"].append(copy.deepcopy(broken["splits"][0]))
    expect_value_error(lambda: validate_manifest(broken), "duplicate split")


def test_unknown_parser_override_rejected():
    manifest = load_manifest("smoke_robust_menu")
    broken = copy.deepcopy(manifest)
    broken["base_args"]["not_a_parser_key"] = 123
    expect_value_error(lambda: validate_manifest(broken), "unknown parser key")


def test_missing_required_baseline_rejected():
    manifest = load_manifest("smoke_robust_menu")
    broken = copy.deepcopy(manifest)
    broken["policies"] = [p for p in broken["policies"] if p["tag"] != "mainline_no_menu"]
    expect_value_error(lambda: validate_manifest(broken), "missing required policy")


def test_suite_members_resolve():
    suite = load_suite("work2_robust_menu")
    assert suite_members(suite) == ["smoke_robust_menu", "pilot_robust_menu", "formal_robust_menu"]


def main():
    tests = [
        test_parser_choices_are_available,
        test_valid_manifests_load,
        test_phase2_contract_manifest_covers_menu_k_set,
        test_manifest_hash_stability,
        test_policy_resolution_is_parser_compatible,
        test_no_filter_is_diagnostic,
        test_mainline_manifests_use_required_family_and_row_v2,
        test_mainline_menu_k_contracts,
        test_pilot_and_formal_require_checkpoint_contract,
        test_phase8_baseline_manifest_contract,
        test_phase8_sensitivity_suite_contract,
        test_phase9_dspo_family_manifest_contract,
        test_duplicate_policy_rejected,
        test_invalid_filter_rejected,
        test_duplicate_split_rejected,
        test_unknown_parser_override_rejected,
        test_missing_required_baseline_rejected,
        test_suite_members_resolve,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} experiment contract tests")


if __name__ == "__main__":
    main()
