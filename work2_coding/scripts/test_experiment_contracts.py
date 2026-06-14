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
    for name in ["smoke_robust_menu", "diagnostic_actual_menu", "pilot_robust_menu", "formal_robust_menu"]:
        manifest = load_manifest(name)
        assert manifest["name"] == name
        assert manifest["output_schema"].get("normalized-row-v1") is True or manifest["output_schema"].get("normalized-row-v2") is True
        tags = {policy["tag"] for policy in manifest["policies"]}
        if name == "diagnostic_actual_menu":
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
    for name in ["pilot_robust_menu", "formal_robust_menu"]:
        manifest = load_manifest(name)
        assert manifest["shared_checkpoint"]["required"] is True
        assert manifest["base_args"]["require_checkpoint"] is True
        assert manifest["base_args"]["checkpoint_path"]


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
