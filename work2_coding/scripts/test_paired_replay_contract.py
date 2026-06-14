import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.experiment_contracts import load_manifest, manifest_hash  # noqa: E402
from Src.paired_replay import (  # noqa: E402
    NORMALIZED_ROW_FIELDS,
    build_normalized_row,
    checkpoint_row_metadata,
    resolve_paired_settings,
    settings_hash,
    trace_identity,
    validate_normalized_row,
    validate_paired_settings,
)
from Src.policy_adapters import mainline_policy_tags  # noqa: E402


MAINLINE_METHODS = {
    "mainline_no_menu": ("m", "no_time_window", "no_menu", "no_pricing"),
    "mainline_fixed_menu": ("m+w+p", "fixed_window", "fixed_menu", "lambertw"),
    "mainline_random_menu": ("m+w+p", "fixed_window", "random_menu", "lambertw"),
    "mainline_optimized_m": ("m", "no_time_window", "optimized_menu", "no_pricing"),
    "mainline_optimized_mw": ("m+w", "adaptive_window", "optimized_menu", "no_pricing"),
    "mainline_optimized_fixed_window": ("m+w+p", "fixed_window", "optimized_menu", "lambertw"),
    "mainline_optimized_adaptive": ("m+w+p", "adaptive_window", "optimized_menu", "lambertw"),
}


def expect_value_error(fn, contains):
    try:
        fn()
    except ValueError as exc:
        assert contains in str(exc), str(exc)
        return
    raise AssertionError("expected ValueError containing: " + contains)


def smoke_settings():
    manifest = load_manifest("smoke_robust_menu")
    return manifest, resolve_paired_settings(manifest)


def test_resolve_paired_settings_count_and_fields():
    manifest, settings = smoke_settings()
    assert len(settings) == len(manifest["splits"]) * len(manifest["policies"])
    first = settings[0]
    assert first["study_name"] == manifest["name"]
    assert first["split_id"] == manifest["splits"][0]["split_id"]
    assert first["trace_id"].startswith("trace-")
    assert first["manifest_hash"] == manifest_hash(manifest)
    assert first["args"]["seed"] == manifest["splits"][0]["seed"]


def test_trace_id_is_policy_independent_within_split():
    _, settings = smoke_settings()
    split_to_traces = {}
    split_to_tags = {}
    for setting in settings:
        split_to_traces.setdefault(setting["split_id"], set()).add(setting["trace_id"])
        split_to_tags.setdefault(setting["split_id"], set()).add(setting["policy_tag"])
    for traces in split_to_traces.values():
        assert len(traces) == 1
    for policy_tags in split_to_tags.values():
        assert policy_tags == set(mainline_policy_tags())


def test_trace_id_changes_when_seed_or_split_changes():
    args = {
        "seed": 1,
        "data_seed": 0,
        "data_seed_test": 1,
        "instance": "RC",
        "max_episodes": 1,
        "max_steps_r": 2,
        "max_steps_p": 0.9,
        "uptake_regime": "medium",
    }
    first, _ = trace_identity("study", "split-a", args)
    changed_seed = dict(args)
    changed_seed["seed"] = 2
    second, _ = trace_identity("study", "split-a", changed_seed)
    third, _ = trace_identity("study", "split-b", args)
    assert first != second
    assert first != third


def test_settings_hash_stability():
    args = {"seed": 1, "menu_policy": "home_only", "menu_k": 3}
    assert settings_hash(args) == settings_hash(copy.deepcopy(args))
    changed = dict(args)
    changed["menu_k"] = 4
    assert settings_hash(args) != settings_hash(changed)


def test_paired_drift_rejected_for_hgs_time():
    _, settings = smoke_settings()
    broken = copy.deepcopy(settings)
    for setting in broken:
        if setting["policy_tag"] == "mainline_no_menu":
            setting["args"]["hgs_final_time"] = 99.0
            break
    expect_value_error(
        lambda: validate_paired_settings(broken, ["hgs_final_time"], []),
        "hgs_final_time",
    )


def test_allowed_varied_fields_do_not_break_pairing():
    _, settings = smoke_settings()
    validate_paired_settings(settings, ["menu_policy", "menu_eta_filter_mode"], ["menu_policy", "menu_eta_filter_mode"])


def test_build_normalized_row_from_synthetic_metadata():
    _, settings = smoke_settings()
    setting = [s for s in settings if s["policy_tag"] == "mainline_optimized_adaptive"][0]
    checkpoint = checkpoint_row_metadata(setting["args"], {"checkpoint_load_status": "not_requested"})
    row = build_normalized_row(
        setting,
        run_id="unit-run",
        checkpoint_metadata=checkpoint,
        stats_metadata={
            "acceptance_rate": 0.75,
            "optout_rate": 0.25,
            "count_opted_out": 1,
            "count_accepted_home": 1,
            "count_accepted_meeting_point": 2,
        },
        menu_metadata={
            "eta_filter_mode": "chance_constraint",
            "effective_menu_policy": "risk_adjusted_expected_profit",
            "menu_selection_solver_effective": "greedy",
            "solver_fallback_reason": "above_exact_threshold",
            "exact_enumerated_menu_count": 0,
            "relative_optimality_gap": None,
            "menu_overlap_rate": None,
            "menu_build_time": 0.01,
        },
        status="completed",
        execution_status="completed",
        placeholder_only=False,
    )
    assert set(NORMALIZED_ROW_FIELDS).issubset(set(row.keys()))
    assert row["trace_id"] == setting["trace_id"]
    assert row["schema_version"] == "normalized-row-v2"
    assert row["study_id"] == setting["study_name"]
    assert row["manifest_path"].endswith("smoke_robust_menu.yaml")
    assert row["candidate_id"] == "aggregate"
    assert row["product_mode"] == "m+w+p"
    assert row["time_window_mode"] == "adaptive_window"
    assert row["menu_mode"] == "optimized_menu"
    assert row["pricing_mode"] == "lambertw"
    assert row["method"] == "m+w+p__adaptive_window__optimized_menu__lambertw"
    assert row["checkpoint_load_status"] == "not_requested"
    assert row["acceptance_rate"] == 0.75
    assert row["accepted_count"] == 3
    assert row["served_count"] == 3
    assert row["served_rate"] == 0.75
    assert row["filter_mode"] == "chance_constraint"
    assert row["uptake_regime"] == "medium"


def test_mainline_rows_cover_exact_method_family():
    _, settings = smoke_settings()
    by_tag = {setting["policy_tag"]: setting for setting in settings if setting["split_id"] == "smoke_mainline_k3"}
    assert set(by_tag) == set(MAINLINE_METHODS)
    for tag, expected in MAINLINE_METHODS.items():
        row = build_normalized_row(by_tag[tag], run_id="mainline-family")
        product_mode, time_window_mode, menu_mode, pricing_mode = expected
        assert row["product_mode"] == product_mode
        assert row["time_window_mode"] == time_window_mode
        assert row["menu_mode"] == menu_mode
        assert row["pricing_mode"] == pricing_mode
        assert row["method"] == "__".join(expected)
        if product_mode != "m+w+p":
            assert row["pricing_mode"] == "no_pricing"
        assert row["candidate_id"] == "aggregate"


def test_missing_required_row_field_rejected():
    _, settings = smoke_settings()
    row = build_normalized_row(settings[0], run_id="unit-run")
    del row["trace_id"]
    expect_value_error(lambda: validate_normalized_row(row), "trace_id")


def test_product_mode_without_price_forces_no_pricing_method():
    _, settings = smoke_settings()
    setting = copy.deepcopy(settings[0])
    setting["args"]["product_mode"] = "m"
    setting["args"]["time_window_mode"] = "no_time_window"
    setting["args"]["menu_contract_mode"] = "no_menu"
    setting["args"]["menu_pricing_mode"] = "lambertw"
    row = build_normalized_row(setting, run_id="unit-run")
    assert row["pricing_mode"] == "no_pricing"
    assert row["method"] == "m__no_time_window__no_menu__no_pricing"


def test_formal_placeholder_row_rejected():
    manifest = load_manifest("formal_robust_menu")
    settings = resolve_paired_settings(manifest)
    expect_value_error(
        lambda: build_normalized_row(settings[0], run_id="formal-placeholder"),
        "formal normalized rows",
    )


def test_checkpoint_contract_status_propagates():
    manifest = load_manifest("pilot_robust_menu")
    setting = resolve_paired_settings(manifest)[0]
    checkpoint = checkpoint_row_metadata(setting["args"])
    assert checkpoint["checkpoint_load_status"] == "contract_required"
    assert checkpoint["checkpoint_required"] is True
    assert checkpoint["checkpoint_path"].endswith("supervised_ml.pt")


def main():
    tests = [
        test_resolve_paired_settings_count_and_fields,
        test_trace_id_is_policy_independent_within_split,
        test_trace_id_changes_when_seed_or_split_changes,
        test_settings_hash_stability,
        test_paired_drift_rejected_for_hgs_time,
        test_allowed_varied_fields_do_not_break_pairing,
        test_build_normalized_row_from_synthetic_metadata,
        test_mainline_rows_cover_exact_method_family,
        test_missing_required_row_field_rejected,
        test_product_mode_without_price_forces_no_pricing_method,
        test_formal_placeholder_row_rejected,
        test_checkpoint_contract_status_propagates,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} paired replay contract tests")


if __name__ == "__main__":
    main()
