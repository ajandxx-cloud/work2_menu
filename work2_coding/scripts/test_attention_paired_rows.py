import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.experiment_contracts import load_manifest
from Src.paired_replay import (
    NORMALIZED_ROW_FIELDS,
    annotate_attention_pair_completeness,
    build_normalized_row,
    resolve_paired_settings,
    validate_rows,
)


def test_attention_settings_share_trace_and_pair_id():
    manifest = load_manifest("smoke_attention_dspo")
    settings = resolve_paired_settings(manifest)
    assert len(settings) == 2
    assert {setting["policy_tag"] for setting in settings} == {"DSPO_original", "DSPO_attention"}
    assert len({setting["trace_id"] for setting in settings}) == 1

    rows = [build_normalized_row(setting, run_id="attention-contract") for setting in settings]
    annotate_attention_pair_completeness(rows)
    assert len({row["attention_pair_id"] for row in rows}) == 1
    assert all(row["attention_pair_complete"] is True for row in rows)


def test_attention_row_fields_from_adapter_defaults():
    manifest = load_manifest("smoke_attention_dspo")
    settings = resolve_paired_settings(manifest)
    rows = [build_normalized_row(setting, run_id="attention-contract") for setting in settings]
    rows = annotate_attention_pair_completeness(rows)
    by_method = {row["method_variant"]: row for row in rows}

    original = by_method["DSPO_original"]
    attention = by_method["DSPO_attention"]
    assert set(NORMALIZED_ROW_FIELDS).issubset(set(original.keys()))
    assert original["attention_enabled"] is False
    assert attention["attention_enabled"] is True
    assert original["attention_mode"] == "deterministic"
    assert attention["attention_mode"] == "deterministic"
    assert original["net_objective_proxy"] == 0.0
    assert isinstance(attention["attention_weight_summary"], dict)


def test_attention_row_fields_from_actual_diagnostics_override_defaults():
    manifest = load_manifest("smoke_attention_dspo")
    setting = [s for s in resolve_paired_settings(manifest) if s["policy_tag"] == "DSPO_attention"][0]
    row = build_normalized_row(
        setting,
        run_id="attention-actual",
        stats_metadata={
            "acceptance_rate": 0.8,
            "optout_rate": 0.2,
            "count_opted_out": 1,
            "count_accepted_home": 1,
            "count_accepted_meeting_point": 3,
            "net_objective_proxy": 12.5,
        },
        menu_metadata={
            "eta_filter_mode": "chance_constraint",
            "effective_menu_policy": "risk_adjusted_expected_profit",
            "menu_selection_solver_effective": "exact",
            "method_variant": "DSPO_attention",
            "attention_enabled": True,
            "attention_mode": "deterministic",
            "attention_strength": 2.0,
            "attention_weight_summary": {"attention_weight_mean": 0.6},
        },
        status="completed",
        execution_status="completed",
        placeholder_only=False,
    )
    assert row["net_objective_proxy"] == 12.5
    assert row["attention_strength"] == 2.0
    assert row["attention_weight_summary"]["attention_weight_mean"] == 0.6


def test_robust_rows_get_safe_attention_defaults():
    manifest = load_manifest("smoke_robust_menu")
    setting = resolve_paired_settings(manifest)[0]
    row = build_normalized_row(setting, run_id="robust-default")
    assert row["method_variant"] == "DSPO_original"
    assert row["attention_enabled"] is False
    assert row["attention_mode"] == "deterministic"
    assert row["attention_pair_complete"] is False


def test_validate_rows_accepts_attention_contract_rows():
    manifest = load_manifest("smoke_attention_dspo")
    rows = [build_normalized_row(setting, run_id="attention-contract") for setting in resolve_paired_settings(manifest)]
    annotate_attention_pair_completeness(rows)
    assert validate_rows(rows) is True


def main():
    tests = [
        test_attention_settings_share_trace_and_pair_id,
        test_attention_row_fields_from_adapter_defaults,
        test_attention_row_fields_from_actual_diagnostics_override_defaults,
        test_robust_rows_get_safe_attention_defaults,
        test_validate_rows_accepts_attention_contract_rows,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} attention paired row tests")


if __name__ == "__main__":
    main()
