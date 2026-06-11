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


def test_required_baselines_present_in_smoke_manifest():
    manifest = load_manifest("smoke_robust_menu")
    tags = {policy["tag"] for policy in manifest["policies"]}
    assert set(required_policy_tags()).issubset(tags)
    assert "random_top_k" in tags


def test_no_filter_diagnostic_flag_and_runtime_knobs():
    manifest = load_manifest("smoke_robust_menu")
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
    manifest = load_manifest("smoke_robust_menu")
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
    manifest = load_manifest("smoke_robust_menu")
    split = manifest["splits"][0]
    hard = [p for p in manifest["policies"] if p["tag"] == "hard_filter"][0]
    robust = [p for p in manifest["policies"] if p["tag"] == "robust_risk_adjusted"][0]
    hard_args = resolve_policy_args(manifest, split, hard)
    robust_args = resolve_policy_args(manifest, split, robust)
    assert hard_args["menu_eta_filter_mode"] != robust_args["menu_eta_filter_mode"]
    assert hard_args["seed"] == robust_args["seed"]
    assert hard_args["hgs_final_time"] == robust_args["hgs_final_time"]
    assert hard_args["checkpoint_path"] == robust_args["checkpoint_path"]


def test_pilot_and_formal_uptake_regimes():
    for name in ["pilot_robust_menu", "formal_robust_menu"]:
        manifest = load_manifest(name)
        regimes = {split["uptake_regime"] for split in manifest["splits"]}
        assert {"low", "medium"}.issubset(regimes)


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
        test_required_baselines_present_in_smoke_manifest,
        test_no_filter_diagnostic_flag_and_runtime_knobs,
        test_home_only_is_cost_bound_not_ranked_policy,
        test_robust_policy_separation,
        test_policy_only_override_guard_rejects_hgs_drift,
        test_manifest_policy_drift_rejected,
        test_allowed_filter_and_objective_drift_passes,
        test_pilot_and_formal_uptake_regimes,
        test_uptake_regime_is_split_level_not_policy_level,
        test_row_ready_uptake_regime_metadata,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} policy fairness contract tests")


if __name__ == "__main__":
    main()
