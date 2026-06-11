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
    trace_ids = {setting["trace_id"] for setting in settings}
    assert len(trace_ids) == 1
    policy_tags = {setting["policy_tag"] for setting in settings}
    assert "hard_filter" in policy_tags
    assert "robust_service_guarded" in policy_tags


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
        if setting["policy_tag"] == "home_only":
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
    setting = [s for s in settings if s["policy_tag"] == "robust_risk_adjusted"][0]
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
        execution_status="synthetic",
        placeholder_only=False,
    )
    assert set(NORMALIZED_ROW_FIELDS).issubset(set(row.keys()))
    assert row["trace_id"] == setting["trace_id"]
    assert row["checkpoint_load_status"] == "not_requested"
    assert row["acceptance_rate"] == 0.75
    assert row["filter_mode"] == "chance_constraint"
    assert row["uptake_regime"] == "medium"


def test_missing_required_row_field_rejected():
    _, settings = smoke_settings()
    row = build_normalized_row(settings[0], run_id="unit-run")
    del row["trace_id"]
    expect_value_error(lambda: validate_normalized_row(row), "trace_id")


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
        test_missing_required_row_field_rejected,
        test_formal_placeholder_row_rejected,
        test_checkpoint_contract_status_propagates,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} paired replay contract tests")


if __name__ == "__main__":
    main()

