import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.experiment_contracts import load_manifest, manifest_hash  # noqa: E402
from Src.paired_replay import build_normalized_row, resolve_paired_settings  # noqa: E402
from Src.policy_adapters import (  # noqa: E402
    adapter_metadata,
    adapter_overrides,
    attention_policy_tags,
    known_policy_tags,
    mainline_policy_tags,
)


def test_mainline_rows_are_dspo_not_dspo_plus():
    manifest = load_manifest("smoke_robust_menu")
    rows = [
        build_normalized_row(setting, run_id="synthetic-run")
        for setting in resolve_paired_settings(manifest, manifest_hash_value=manifest_hash(manifest))
    ]
    assert {row["policy_tag"] for row in rows} == set(mainline_policy_tags())
    assert {row["method_family"] for row in rows} == {"DSPO"}
    assert all(row["method_family"] != "DSPO_PLUS" for row in rows)


def test_phase9_dspo_tags_are_dspo_only_and_exclude_dspo_plus_scope():
    tags = set(known_policy_tags(include_optional=True))
    assert {"dspo_clip", "dspo_wide"}.issubset(tags)
    thresholds = {
        "dspo_clip": 0.35,
        "dspo_wide": 0.45,
    }
    for tag, threshold in thresholds.items():
        metadata = adapter_metadata(tag)
        overrides = adapter_overrides(tag)
        assert metadata["method_family"] == "DSPO"
        assert metadata["comparison_role"] == "dspo_family"
        assert metadata["dspo_plus_contract"] == {}
        assert overrides["method_family"] == "DSPO"
        assert overrides["method_variant"] == "DSPO_original"
        assert overrides["menu_policy"] == "service_guarded_expected_profit"
        assert overrides["menu_eta_filter_mode"] == "interval_overlap"
        assert overrides["attention_enabled"] is False
        assert overrides["service_quit_rate_guardrail"] == threshold
        assert overrides["menu_optout_guardrail"] == threshold
        assert "service_quit_penalty" not in overrides
        assert "menu_outside_penalty_lambda" not in overrides


def test_attention_tags_remain_diagnostic_not_dspo_plus():
    for tag in attention_policy_tags():
        metadata = adapter_metadata(tag)
        overrides = adapter_overrides(tag)
        assert metadata["diagnostic"] is True
        assert metadata["method_family"] == "diagnostic"
        assert overrides["method_family"] == "diagnostic"
        assert overrides["attention_enabled"] == (tag == "DSPO_attention")


def main():
    tests = [
        test_mainline_rows_are_dspo_not_dspo_plus,
        test_phase9_dspo_tags_are_dspo_only_and_exclude_dspo_plus_scope,
        test_attention_tags_remain_diagnostic_not_dspo_plus,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} method-family contract tests")


if __name__ == "__main__":
    main()
