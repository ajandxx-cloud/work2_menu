import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.experiment_contracts import load_manifest, manifest_hash, resolve_policy_args  # noqa: E402
from Src.paired_replay import resolve_paired_settings  # noqa: E402
from Src.policy_adapters import mainline_policy_tags  # noqa: E402


CALIBRATION = "calibration_robust_menu"
FINAL = "final_robust_menu"


def _manifests():
    return load_manifest(CALIBRATION), load_manifest(FINAL)


def _split_keys(manifest):
    return {
        (split["split_id"], split["seed"], split["data_seed"], split["data_seed_test"])
        for split in manifest["splits"]
    }


def test_policy_family_and_checkpoint_contracts():
    expected = mainline_policy_tags()
    for manifest in _manifests():
        tags = [policy["tag"] for policy in manifest["policies"]]
        assert tags == expected
        assert manifest["required_policy_tags"] == expected
        assert manifest["shared_checkpoint"]["required"] is True
        assert manifest["shared_checkpoint"]["expected_status"] == "loaded"
        assert manifest["shared_checkpoint"]["path"]
        assert manifest["base_args"]["checkpoint_path"] == manifest["shared_checkpoint"]["path"]
        assert manifest["base_args"]["require_checkpoint"] is True
        assert manifest_hash(manifest)


def test_calibration_and_final_splits_are_disjoint():
    calibration, final = _manifests()
    assert _split_keys(calibration).isdisjoint(_split_keys(final))
    assert {split["uptake_regime"] for split in calibration["splits"]} >= {"low", "medium"}
    assert {split["uptake_regime"] for split in final["splits"]} >= {"low", "medium"}


def test_paired_and_varied_fields_cover_contract():
    calibration, final = _manifests()
    required_paired = {
        "seed",
        "data_seed",
        "data_seed_test",
        "instance",
        "pricing",
        "hgs_reopt_time",
        "hgs_final_time",
        "checkpoint_path",
        "require_checkpoint",
        "menu_k",
        "max_candidates",
        "home_util",
        "base_util",
        "incentive_sens",
    }
    required_varied = {
        "menu_policy",
        "product_mode",
        "time_window_mode",
        "menu_contract_mode",
        "menu_pricing_mode",
        "menu_eta_filter_mode",
        "menu_objective_mode",
        "service_quit_rate_guardrail",
        "menu_optout_guardrail",
    }
    for manifest in [calibration, final]:
        assert required_paired.issubset(set(manifest["paired_fields"]))
        assert required_varied.issubset(set(manifest["varied_fields"]))
        resolve_paired_settings(manifest)


def test_output_schema_preserves_provenance_and_accounting():
    required = {
        "checkpoint_load_status",
        "checkpoint_hash",
        "method_family",
        "outside_option_util",
        "count_opted_out",
        "count_accepted_home",
        "count_accepted_meeting_point",
        "home_share",
        "meeting_point_uptake_rate",
        "status",
        "execution_status",
        "error_type",
        "error_message",
    }
    for manifest in _manifests():
        fields = set(manifest["output_schema"]["fields"])
        assert required.issubset(fields)


def test_policy_drift_does_not_remove_required_cases_or_metrics():
    calibration, final = _manifests()
    assert calibration["output_intent"] == "calibration_only"
    assert final["output_intent"] == "final_claim_candidate_after_gates"
    for manifest in [calibration, final]:
        settings = resolve_paired_settings(manifest)
        assert len(settings) == len(manifest["splits"]) * len(mainline_policy_tags())
        for policy in manifest["policies"]:
            args = resolve_policy_args(manifest, manifest["splits"][0], policy)
            assert args["seed"] == manifest["splits"][0]["seed"]
            assert args["checkpoint_path"] == manifest["shared_checkpoint"]["path"]


def main():
    tests = [
        test_policy_family_and_checkpoint_contracts,
        test_calibration_and_final_splits_are_disjoint,
        test_paired_and_varied_fields_cover_contract,
        test_output_schema_preserves_provenance_and_accounting,
        test_policy_drift_does_not_remove_required_cases_or_metrics,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} calibration manifest tests")


if __name__ == "__main__":
    main()
