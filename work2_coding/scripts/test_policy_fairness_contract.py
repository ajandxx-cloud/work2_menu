import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.experiment_contracts import (  # noqa: E402
    load_manifest,
    parser_choices,
    resolve_policy_args,
    validate_manifest,
)
from Src.paired_replay import build_normalized_row, resolve_paired_settings  # noqa: E402
from Src.policy_adapters import (  # noqa: E402
    POLICY_ONLY_FIELDS,
    adapter_metadata,
    adapter_overrides,
    mainline_policy_tags,
    required_policy_tags,
    validate_policy_only_overrides,
    validate_required_adapter_coverage,
)


def expect_value_error(fn, contains):
    try:
        fn()
    except ValueError as exc:
        assert contains in str(exc), str(exc)
        return
    raise AssertionError("expected ValueError containing: " + contains)


def test_required_adapter_coverage_and_parser_compatibility():
    assert validate_required_adapter_coverage(parser_choices()) is True
    for tag in required_policy_tags():
        overrides = adapter_overrides(tag)
        assert overrides["algo_name"] == "DSPO_Menu"
        assert overrides["menu_mode"] is True
        assert overrides["menu_policy"] in parser_choices()["menu_policy"]
        assert overrides["menu_eta_filter_mode"] in parser_choices()["menu_eta_filter_mode"]


def test_mainline_family_present_in_smoke_manifest():
    manifest = load_manifest("smoke_robust_menu")
    tags = {policy["tag"] for policy in manifest["policies"]}
    assert set(mainline_policy_tags()).issubset(tags)
    assert tags == set(mainline_policy_tags())


def test_no_filter_diagnostic_flag_and_runtime_knobs():
    manifest = load_manifest("diagnostic_actual_menu")
    policy = [p for p in manifest["policies"] if p["tag"] == "no_filter_diagnostic"][0]
    args = resolve_policy_args(manifest, manifest["splits"][0], policy)
    metadata = adapter_metadata("no_filter_diagnostic")
    assert metadata["diagnostic"] is True
    assert args["menu_eta_filter_mode"] == "none"
    assert args["menu_time_filtering"] is False


def test_home_only_is_cost_bound_not_ranked_policy():
    metadata = adapter_metadata("home_only")
    assert metadata["comparison_role"] == "cost_bound"
    assert metadata["cost_bound"] is True
    assert metadata["diagnostic"] is False


def test_robust_policy_separation():
    manifest = load_manifest("diagnostic_actual_menu")
    split = manifest["splits"][0]
    risk = [p for p in manifest["policies"] if p["tag"] == "robust_risk_adjusted"][0]
    guarded = [p for p in manifest["policies"] if p["tag"] == "robust_service_guarded"][0]
    risk_args = resolve_policy_args(manifest, split, risk)
    guarded_args = resolve_policy_args(manifest, split, guarded)
    assert risk_args["menu_policy"] == "risk_adjusted_expected_profit"
    assert guarded_args["menu_policy"] == "service_guarded_expected_profit"
    assert risk_args["menu_eta_filter_mode"] == "chance_constraint"
    assert guarded_args["menu_eta_filter_mode"] == "interval_overlap"


def test_policy_only_override_guard_rejects_hgs_drift():
    expect_value_error(
        lambda: validate_policy_only_overrides("bad_policy", {"hgs_final_time": 99.0}, POLICY_ONLY_FIELDS),
        "non-policy fields",
    )


def test_manifest_policy_drift_rejected():
    manifest = load_manifest("smoke_robust_menu")
    broken = copy.deepcopy(manifest)
    broken["policies"][0]["args_overrides"] = {"checkpoint_path": "other.pt"}
    expect_value_error(lambda: validate_manifest(broken), "non-policy fields")


def test_allowed_filter_and_objective_drift_passes():
    manifest = load_manifest("diagnostic_actual_menu")
    split = manifest["splits"][0]
    hard = [p for p in manifest["policies"] if p["tag"] == "hard_filter"][0]
    robust = [p for p in manifest["policies"] if p["tag"] == "robust_risk_adjusted"][0]
    hard_args = resolve_policy_args(manifest, split, hard)
    robust_args = resolve_policy_args(manifest, split, robust)
    assert hard_args["menu_eta_filter_mode"] != robust_args["menu_eta_filter_mode"]
    assert hard_args["seed"] == robust_args["seed"]
    assert hard_args["hgs_final_time"] == robust_args["hgs_final_time"]
    assert hard_args["checkpoint_path"] == robust_args["checkpoint_path"]


def test_pricing_contract_is_paired_and_row_recorded():
    manifest = load_manifest("smoke_robust_menu")
    assert "pricing" in manifest["paired_fields"]
    assert "pricing" not in manifest["varied_fields"]
    assert "menu_pricing_mode" in manifest["varied_fields"]
    assert "menu_pricing_constant" not in manifest["varied_fields"]

    settings = resolve_paired_settings(manifest)
    pricing_values = {setting["args"]["pricing"] for setting in settings}
    pricing_modes = {setting["args"].get("menu_pricing_mode") for setting in settings}
    pricing_constants = {setting["args"].get("menu_pricing_constant") for setting in settings}

    assert pricing_values == {True}
    assert pricing_modes == {"lambertw", "no_pricing"}
    assert len(pricing_constants) == 1

    row = build_normalized_row(settings[0], run_id="pricing-contract")
    assert row["pricing"] is True


def test_mainline_policy_drift_is_limited_to_comparison_fields():
    manifest = load_manifest("smoke_robust_menu")
    split = manifest["splits"][0]
    resolved = {
        policy["tag"]: resolve_policy_args(manifest, split, policy)
        for policy in manifest["policies"]
    }
    for tag, args in resolved.items():
        assert args["seed"] == split["seed"]
        assert args["data_seed"] == split["data_seed"]
        assert args["hgs_final_time"] == manifest["base_args"]["hgs_final_time"]
        assert args["checkpoint_path"] == manifest["base_args"]["checkpoint_path"]
        assert args["menu_policy"] in {"home_only", "nearest_heuristic", "random_top_k", "service_guarded_expected_profit"}
    assert resolved["mainline_no_menu"]["product_mode"] == "m"
    assert resolved["mainline_optimized_mw"]["product_mode"] == "m+w"
    assert resolved["mainline_optimized_adaptive"]["product_mode"] == "m+w+p"
    assert resolved["mainline_optimized_adaptive"]["menu_policy"] == "service_guarded_expected_profit"


def test_pilot_and_formal_uptake_regimes():
    for name in ["pilot_robust_menu", "formal_robust_menu", "phase8_baseline_validation"]:
        manifest = load_manifest(name)
        regimes = {split["uptake_regime"] for split in manifest["splits"]}
        assert {"low", "medium"}.issubset(regimes)


def test_phase8_baseline_pairing_and_pricing_contract():
    manifest = load_manifest("phase8_baseline_validation")
    settings = resolve_paired_settings(manifest)
    assert len(settings) == 10

    by_split = {}
    for setting in settings:
        by_split.setdefault(setting["split_id"], {})[setting["policy_tag"]] = setting
    assert len(by_split) == 5

    shared_fields = [
        "seed",
        "data_seed",
        "data_seed_test",
        "instance",
        "load_data",
        "pricing",
        "checkpoint_path",
        "require_checkpoint",
        "allow_checkpoint_mismatch",
        "hgs_reopt_time",
        "hgs_final_time",
        "reopt",
        "menu_k",
        "max_candidates",
        "n_vehicles",
        "veh_capacity",
        "menu_pricing_constant",
        "home_util",
        "base_util",
        "incentive_sens",
    ]
    for split_id, group in by_split.items():
        assert set(group) == {"mainline_optimized_mw", "phase8_static_flat_markdown"}, split_id
        no_pricing = group["mainline_optimized_mw"]["args"]
        static = group["phase8_static_flat_markdown"]["args"]
        for field in shared_fields:
            assert no_pricing.get(field) == static.get(field), field
        assert no_pricing["product_mode"] == "m+w"
        assert no_pricing["menu_pricing_mode"] == "no_pricing"
        assert static["product_mode"] == "m+w+p"
        assert static["menu_pricing_mode"] == "flat_markdown"

    static_row = build_normalized_row(
        by_split[next(iter(by_split))]["phase8_static_flat_markdown"],
        run_id="phase8",
        checkpoint_metadata={
            "checkpoint_load_status": "loaded",
            "checkpoint_path": "synthetic.pt",
            "checkpoint_hash": "hash",
            "checkpoint_required": True,
            "checkpoint_intentional_mismatch": False,
        },
        stats_metadata={
            "count_opted_out": 1,
            "count_accepted_home": 2,
            "count_accepted_meeting_point": 3,
        },
        status="completed",
        execution_status="completed",
        placeholder_only=False,
    )
    assert static_row["pricing_mode"] == "flat_markdown"
    assert static_row["comparison_role"] == "static_pricing_baseline"


def test_phase8_sensitivity_manifests_keep_single_policy_and_shared_checkpoint():
    for name in [
        "phase8_sensitivity_menu_k",
        "phase8_sensitivity_eta_filter",
        "phase8_sensitivity_uptake_regime",
        "phase8_sensitivity_guardrail",
    ]:
        manifest = load_manifest(name)
        settings = resolve_paired_settings(manifest)
        assert {setting["policy_tag"] for setting in settings} == {"mainline_optimized_adaptive"}
        checkpoint_paths = {setting["args"]["checkpoint_path"] for setting in settings}
        assert checkpoint_paths == {"outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt"}
        for setting in settings:
            args = setting["args"]
            assert args["pricing"] is True
            assert args["max_candidates"] == 10
            assert args["hgs_reopt_time"] == 0.1
            assert args["hgs_final_time"] == 0.1
            assert args["product_mode"] == "m+w+p"
            assert args["time_window_mode"] == "adaptive_window"
            assert args["menu_pricing_mode"] == "lambertw"


def test_phase9_dspo_family_pairing_and_threshold_contract():
    manifest = load_manifest("phase9_dspo_family_validation")
    settings = resolve_paired_settings(manifest)
    assert len(settings) == 10

    by_split = {}
    for setting in settings:
        by_split.setdefault(setting["split_id"], {})[setting["policy_tag"]] = setting
    assert len(by_split) == 5

    shared_fields = [
        "seed",
        "data_seed",
        "data_seed_test",
        "instance",
        "load_data",
        "pricing",
        "checkpoint_path",
        "require_checkpoint",
        "allow_checkpoint_mismatch",
        "hgs_reopt_time",
        "hgs_final_time",
        "reopt",
        "menu_k",
        "max_candidates",
        "max_steps_r",
        "max_steps_p",
        "n_vehicles",
        "veh_capacity",
        "home_util",
        "base_util",
        "incentive_sens",
    ]
    for split_id, group in by_split.items():
        assert set(group) == {"dspo_clip", "dspo_wide"}, split_id
        clip = group["dspo_clip"]["args"]
        wide = group["dspo_wide"]["args"]
        for field in shared_fields:
            assert clip.get(field) == wide.get(field), field
        assert clip["menu_policy"] == "service_guarded_expected_profit"
        assert wide["menu_policy"] == "service_guarded_expected_profit"
        assert clip["service_quit_rate_guardrail"] == 0.35
        assert clip["menu_optout_guardrail"] == 0.35
        assert wide["service_quit_rate_guardrail"] == 0.45
        assert wide["menu_optout_guardrail"] == 0.45
        assert clip["method_family"] == "DSPO"
        assert wide["method_family"] == "DSPO"
        assert clip["attention_enabled"] is False
        assert wide["attention_enabled"] is False

    row = build_normalized_row(
        by_split[next(iter(by_split))]["dspo_clip"],
        run_id="phase9",
        checkpoint_metadata={
            "checkpoint_load_status": "loaded",
            "checkpoint_path": "synthetic.pt",
            "checkpoint_hash": "hash",
            "checkpoint_required": True,
            "checkpoint_intentional_mismatch": False,
        },
        stats_metadata={
            "count_opted_out": 1,
            "count_accepted_home": 2,
            "count_accepted_meeting_point": 3,
        },
        status="completed",
        execution_status="completed",
        placeholder_only=False,
    )
    assert row["method_family"] == "DSPO"
    assert row["comparison_role"] == "dspo_family"
    assert row["policy_tag"] == "dspo_clip"


def test_uptake_regime_is_split_level_not_policy_level():
    manifest = load_manifest("pilot_robust_menu")
    for policy in manifest["policies"]:
        assert "uptake_regime" not in (policy.get("args_overrides") or {})
    low_split = [split for split in manifest["splits"] if split["uptake_regime"] == "low"][0]
    medium_split = [split for split in manifest["splits"] if split["uptake_regime"] == "medium"][0]
    policy = manifest["policies"][0]
    low_args = resolve_policy_args(manifest, low_split, policy)
    medium_args = resolve_policy_args(manifest, medium_split, policy)
    assert low_args["uptake_regime"] == "low"
    assert medium_args["uptake_regime"] == "medium"
    assert low_args["home_util"] != medium_args["home_util"]


def test_row_ready_uptake_regime_metadata():
    manifest = load_manifest("smoke_robust_menu")
    setting = resolve_paired_settings(manifest)[0]
    row = build_normalized_row(setting, run_id="uptake-row")
    assert row["uptake_regime"] == "medium"
    assert row["policy_tag"] == setting["policy_tag"]
    assert row["placeholder_only"] is True


def main():
    tests = [
        test_required_adapter_coverage_and_parser_compatibility,
        test_mainline_family_present_in_smoke_manifest,
        test_no_filter_diagnostic_flag_and_runtime_knobs,
        test_home_only_is_cost_bound_not_ranked_policy,
        test_robust_policy_separation,
        test_policy_only_override_guard_rejects_hgs_drift,
        test_manifest_policy_drift_rejected,
        test_allowed_filter_and_objective_drift_passes,
        test_pricing_contract_is_paired_and_row_recorded,
        test_mainline_policy_drift_is_limited_to_comparison_fields,
        test_pilot_and_formal_uptake_regimes,
        test_phase8_baseline_pairing_and_pricing_contract,
        test_phase8_sensitivity_manifests_keep_single_policy_and_shared_checkpoint,
        test_phase9_dspo_family_pairing_and_threshold_contract,
        test_uptake_regime_is_split_level_not_policy_level,
        test_row_ready_uptake_regime_metadata,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} policy fairness contract tests")


if __name__ == "__main__":
    main()
