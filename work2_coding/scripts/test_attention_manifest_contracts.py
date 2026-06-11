import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.experiment_contracts import load_manifest, load_suite, resolve_policy_args, suite_members, validate_manifest
from Src.policy_adapters import adapter_metadata, adapter_overrides, attention_policy_tags


def expect_value_error(fn, contains):
    try:
        fn()
    except ValueError as exc:
        assert contains in str(exc), str(exc)
        return
    raise AssertionError("expected ValueError containing: " + contains)


def test_attention_policy_adapters_are_main_methods():
    for tag in attention_policy_tags():
        metadata = adapter_metadata(tag)
        overrides = adapter_overrides(tag)
        assert metadata["comparison_role"] == "method"
        assert metadata["diagnostic"] is False
        assert metadata["cost_bound"] is False
        assert overrides["algo_name"] == "DSPO_Menu"
        assert overrides["menu_mode"] is True
        assert overrides["menu_policy"] == "risk_adjusted_expected_profit"
        assert overrides["menu_eta_filter_mode"] == "chance_constraint"

    original = adapter_overrides("DSPO_original")
    attention = adapter_overrides("DSPO_attention")
    assert original["method_variant"] == "DSPO_original"
    assert original["attention_enabled"] is False
    assert attention["method_variant"] == "DSPO_attention"
    assert attention["attention_enabled"] is True


def test_attention_manifests_load_and_require_main_tags():
    for name in ["smoke_attention_dspo", "pilot_attention_dspo", "formal_attention_dspo"]:
        manifest = load_manifest(name)
        assert manifest["comparison_family"] == "attention_dspo"
        assert manifest["required_policy_tags"] == ["DSPO_original", "DSPO_attention"]
        assert [policy["tag"] for policy in manifest["policies"]] == ["DSPO_original", "DSPO_attention"]
        fields = set(manifest["output_schema"]["fields"])
        assert "method_variant" in fields
        assert "attention_pair_complete" in fields
        assert "net_objective_proxy" in fields


def test_attention_resolved_args_only_vary_attention_fields():
    manifest = load_manifest("smoke_attention_dspo")
    split = manifest["splits"][0]
    original = resolve_policy_args(manifest, split, manifest["policies"][0])
    attention = resolve_policy_args(manifest, split, manifest["policies"][1])

    varied = set(manifest["varied_fields"])
    differences = {key for key in original if original.get(key) != attention.get(key)}
    assert differences.issubset(varied), differences
    assert original["seed"] == attention["seed"]
    assert original["checkpoint_path"] == attention["checkpoint_path"]
    assert original["hgs_final_time"] == attention["hgs_final_time"]
    assert original["menu_policy"] == attention["menu_policy"]
    assert original["menu_eta_filter_mode"] == attention["menu_eta_filter_mode"]


def test_attention_pilot_and_formal_keep_checkpoint_and_uptake_gates():
    for name in ["pilot_attention_dspo", "formal_attention_dspo"]:
        manifest = load_manifest(name)
        assert manifest["shared_checkpoint"]["required"] is True
        assert manifest["base_args"]["require_checkpoint"] is True
        regimes = {split["uptake_regime"] for split in manifest["splits"]}
        assert {"low", "medium"}.issubset(regimes)


def test_attention_manifest_rejects_diagnostic_policy_in_main_family():
    manifest = load_manifest("smoke_attention_dspo")
    broken = copy.deepcopy(manifest)
    broken["policies"].append({"tag": "home_only"})
    expect_value_error(lambda: validate_manifest(broken), "attention_dspo main manifests")


def test_attention_manifest_requires_varied_attention_fields():
    manifest = load_manifest("smoke_attention_dspo")
    broken = copy.deepcopy(manifest)
    broken["varied_fields"] = ["method_variant"]
    expect_value_error(lambda: validate_manifest(broken), "varied attention")


def test_attention_suite_members_resolve():
    suite = load_suite("work2_attention_dspo")
    assert suite_members(suite) == ["smoke_attention_dspo", "pilot_attention_dspo", "formal_attention_dspo"]


def test_attention_ablation_manifests_are_preregistered_and_fair():
    names = [
        "pilot_attention_ablation_strength_high",
        "pilot_attention_ablation_eta_feature_focus",
        "pilot_attention_ablation_shared_eta_stronger",
    ]
    for name in names:
        manifest = load_manifest(name)
        assert manifest["tier"] == "pilot"
        assert manifest["shared_checkpoint"]["required"] is True
        assert manifest["base_args"]["require_checkpoint"] is True
        assert {split["uptake_regime"] for split in manifest["splits"]} == {"low", "medium"}
        assert [policy["tag"] for policy in manifest["policies"]] == ["DSPO_original", "DSPO_attention"]
        varied = set(manifest["varied_fields"])
        for split in manifest["splits"]:
            original = resolve_policy_args(manifest, split, manifest["policies"][0])
            attention = resolve_policy_args(manifest, split, manifest["policies"][1])
            differences = {key for key in original if original.get(key) != attention.get(key)}
            assert differences.issubset(varied), (name, differences - varied)
            assert original["checkpoint_path"] == attention["checkpoint_path"]
            assert original["menu_eta_filter_mode"] == attention["menu_eta_filter_mode"]


def test_attention_ablation_suite_members_resolve():
    suite = load_suite("work2_attention_ablation")
    assert suite_members(suite) == [
        "pilot_attention_ablation_strength_high",
        "pilot_attention_ablation_eta_feature_focus",
        "pilot_attention_ablation_shared_eta_stronger",
    ]


def main():
    tests = [
        test_attention_policy_adapters_are_main_methods,
        test_attention_manifests_load_and_require_main_tags,
        test_attention_resolved_args_only_vary_attention_fields,
        test_attention_pilot_and_formal_keep_checkpoint_and_uptake_gates,
        test_attention_manifest_rejects_diagnostic_policy_in_main_family,
        test_attention_manifest_requires_varied_attention_fields,
        test_attention_suite_members_resolve,
        test_attention_ablation_manifests_are_preregistered_and_fair,
        test_attention_ablation_suite_members_resolve,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} attention manifest contract tests")


if __name__ == "__main__":
    main()
