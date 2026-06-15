import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.experiment_contracts import load_manifest, load_suite, resolve_policy_args, suite_members  # noqa: E402


PHASE8_STUDIES = [
    "phase8_sensitivity_menu_k",
    "phase8_sensitivity_eta_filter",
    "phase8_sensitivity_uptake_regime",
    "phase8_sensitivity_guardrail",
]

EXPECTED_AXIS_VALUES = {
    "phase8_sensitivity_menu_k": {"2", "3", "4"},
    "phase8_sensitivity_eta_filter": {"hard", "interval_overlap", "chance_constraint"},
    "phase8_sensitivity_uptake_regime": {"low", "medium"},
    "phase8_sensitivity_guardrail": {"0.35", "0.40"},
}

INVARIANT_FIELDS = [
    "seed",
    "data_seed",
    "data_seed_test",
    "checkpoint_path",
    "require_checkpoint",
    "allow_checkpoint_mismatch",
    "hgs_reopt_time",
    "hgs_final_time",
    "reopt",
    "max_candidates",
    "max_steps_r",
    "max_steps_p",
    "n_vehicles",
    "veh_capacity",
]

NICE_TO_HAVE_KEYS = {
    "max_candidates",
    "n_vehicles",
    "veh_capacity",
    "max_price",
    "min_price",
    "menu_pricing_constant",
}


def _load_phase8_manifests():
    return {name: load_manifest(name) for name in PHASE8_STUDIES}


def _axis_values(manifest):
    return {str(split["sensitivity_value"]) for split in manifest["splits"]}


def test_all_phase8_sensitivity_manifests_load():
    manifests = _load_phase8_manifests()
    for name, manifest in manifests.items():
        assert manifest["name"] == name
        assert manifest["tier"] == "pilot"
        assert manifest["run_mode"] == "diagnostic"
        assert manifest["claim_ready"] is False
        assert manifest["output_intent"] == "diagnostic_provisional_blocked"
        assert manifest["baseline_validation_required"].endswith("PHASE8_BASELINE_VALIDATION.json")
        assert manifest["required_policy_tags"] == ["mainline_optimized_adaptive"]
        assert [policy["tag"] for policy in manifest["policies"]] == ["mainline_optimized_adaptive"]


def test_suite_members_are_exactly_must_have_studies():
    suite = load_suite("phase8_sensitivity_must_have")
    assert suite_members(suite) == PHASE8_STUDIES
    assert suite["claim_ready"] is False
    assert suite["output_intent"] == "diagnostic_provisional_blocked"


def test_axis_values_match_locked_phase8_context():
    manifests = _load_phase8_manifests()
    for name, expected in EXPECTED_AXIS_VALUES.items():
        assert _axis_values(manifests[name]) == expected

    menu_k = manifests["phase8_sensitivity_menu_k"]
    assert menu_k["sensitivity_axis"] == "menu_k"
    assert str(menu_k["center_value"]) == "3"
    assert {split["args_overrides"]["menu_k"] for split in menu_k["splits"]} == {2, 3, 4}

    eta = manifests["phase8_sensitivity_eta_filter"]
    values = {split["args_overrides"]["menu_eta_filter_mode"] for split in eta["splits"]}
    assert values == {"hard", "interval_overlap", "chance_constraint"}
    assert "none" not in values
    for split in eta["splits"]:
        overrides = split["args_overrides"]
        if overrides["menu_eta_filter_mode"] == "chance_constraint":
            assert overrides["menu_eta_chance_threshold"] == 0.25

    uptake = manifests["phase8_sensitivity_uptake_regime"]
    assert {split["uptake_regime"] for split in uptake["splits"]} == {"low", "medium"}
    assert "high" not in {split["uptake_regime"] for split in uptake["splits"]}

    guardrail = manifests["phase8_sensitivity_guardrail"]
    assert guardrail["guardrail_fields"] == ["service_quit_rate_guardrail", "menu_optout_guardrail"]
    assert {float(split["sensitivity_value"]) for split in guardrail["splits"]} == {0.35, 0.40}
    for split in guardrail["splits"]:
        overrides = split["args_overrides"]
        assert overrides["service_quit_rate_guardrail"] == overrides["menu_optout_guardrail"]


def test_nice_to_have_dimensions_are_deferred():
    manifests = _load_phase8_manifests()
    for manifest in manifests.values():
        assert "max_candidates" in manifest["sensitivity_contract"]["deferred_dimensions"]
        for split in manifest["splits"]:
            overrides = split.get("args_overrides") or {}
            varied_nice_to_have = NICE_TO_HAVE_KEYS.intersection(overrides)
            if manifest["sensitivity_axis"] != "guardrail":
                assert not varied_nice_to_have, (manifest["name"], split["split_id"], varied_nice_to_have)
            else:
                assert varied_nice_to_have <= {"service_quit_rate_guardrail", "menu_optout_guardrail"}
        for policy in manifest["policies"]:
            assert not NICE_TO_HAVE_KEYS.intersection(policy.get("args_overrides") or {})


def test_no_filter_absent_from_executable_suite():
    manifests = _load_phase8_manifests()
    for manifest in manifests.values():
        assert "no_filter_diagnostic" not in [policy["tag"] for policy in manifest["policies"]]
        assert manifest["base_args"]["menu_eta_filter_mode"] != "none"
        for split in manifest["splits"]:
            assert (split.get("args_overrides") or {}).get("menu_eta_filter_mode") != "none"


def test_paired_groups_preserve_replay_fairness_fields():
    manifests = _load_phase8_manifests()
    for manifest in manifests.values():
        policy = manifest["policies"][0]
        groups = defaultdict(list)
        for split in manifest["splits"]:
            groups[split["paired_group_id"]].append(split)

        expected_values = EXPECTED_AXIS_VALUES[manifest["name"]]
        for group_id, splits in groups.items():
            assert {str(split["sensitivity_value"]) for split in splits} == expected_values, group_id
            resolved = [resolve_policy_args(manifest, split, policy) for split in splits]
            baseline = resolved[0]
            for args in resolved[1:]:
                for field in INVARIANT_FIELDS:
                    assert args[field] == baseline[field], (manifest["name"], group_id, field)

            if manifest["sensitivity_axis"] == "menu_k":
                assert {args["menu_k"] for args in resolved} == {2, 3, 4}
            else:
                assert {args["menu_k"] for args in resolved} == {3}
            if manifest["sensitivity_axis"] != "eta_filter_mode":
                assert {args["menu_eta_filter_mode"] for args in resolved} == {"interval_overlap"}


def test_policy_resolution_keeps_single_adaptive_method():
    manifests = _load_phase8_manifests()
    for manifest in manifests.values():
        policy = manifest["policies"][0]
        for split in manifest["splits"]:
            args = resolve_policy_args(manifest, split, policy)
            assert args["algo_name"] == "DSPO_Menu"
            assert args["menu_mode"] is True
            assert args["product_mode"] == "m+w+p"
            assert args["time_window_mode"] == "adaptive_window"
            assert args["menu_contract_mode"] == "optimized_menu"
            assert args["menu_pricing_mode"] == "lambertw"
            assert args["checkpoint_path"] == manifest["shared_checkpoint"]["path"]


def main():
    tests = [
        test_all_phase8_sensitivity_manifests_load,
        test_suite_members_are_exactly_must_have_studies,
        test_axis_values_match_locked_phase8_context,
        test_nice_to_have_dimensions_are_deferred,
        test_no_filter_absent_from_executable_suite,
        test_paired_groups_preserve_replay_fairness_fields,
        test_policy_resolution_keeps_single_adaptive_method,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} Phase 8 sensitivity contract tests")


if __name__ == "__main__":
    main()
