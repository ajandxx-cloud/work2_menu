from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
STUDIES = ROOT / "experiments" / "studies"

REQUIRED_TAGS = [
    "nearest_L",
    "cost_L",
    "cnn_menu",
    "cnn_setmenu_net_current",
    "expected_profit_enumeration",
    "service_constrained_expected_profit",
    "cost_oracle",
    "profit_oracle",
]
FORBIDDEN_TAGS = {
    "mlp_menu",
    "cnn_setmenu_net_system_profit_route025",
    "cnn_setmenu_net_system_profit",
    "oracle_menu",
}


def load(name):
    with open(STUDIES / f"{name}.yaml", "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def policy_by_tag(manifest):
    return {policy["tag"]: policy for policy in manifest["policies"]}


def assert_common_contract(manifest, expected_name):
    base_args = manifest["base_args"]
    tags = list(policy_by_tag(manifest))

    assert_true(manifest["name"] == expected_name, f"{expected_name} name mismatch")
    assert_true(manifest["type"] == "policy_compare", f"{expected_name} must be policy_compare")
    assert_true(manifest["reference_tag"] == "full_display", f"{expected_name} reference tag mismatch")
    assert_true(manifest["reference_policy"] == "offer_all_feasible_bundles", f"{expected_name} reference policy mismatch")
    assert_true(base_args["instance"] == "RC", f"{expected_name} must use RC")
    assert_true(base_args["menu_k"] == 3, f"{expected_name} must use L=3")
    assert_true(base_args["candidate_meeting_points"] == 10, f"{expected_name} must request K=10")
    assert_true(base_args["max_candidates"] == 10, f"{expected_name} must cap K=10")
    assert_true(base_args["menu_selection_solver"] == "exact", f"{expected_name} must use exact solver")
    assert_true(base_args["menu_use_exact_eval"] is True, f"{expected_name} must enable exact eval")
    assert_true(base_args["menu_exact_threshold"] == 8, f"{expected_name} exact threshold mismatch")
    assert_true(base_args["menu_objective_mode"] == "system_profit", f"{expected_name} must use system_profit base objective")
    assert_true(base_args["service_quit_penalty"] == 100.0, f"{expected_name} quit penalty mismatch")
    assert_true(base_args["service_quit_rate_guardrail"] == 0.4, f"{expected_name} guardrail mismatch")
    assert_true(tags == REQUIRED_TAGS, f"{expected_name} policy tags must match locked set")
    assert_true(not (set(tags) & FORBIDDEN_TAGS), f"{expected_name} contains remediation-only tags")

    policies = policy_by_tag(manifest)
    current = policies["cnn_setmenu_net_current"]
    assert_true(current["policy"] == "menu_optimization", "current CNN-SetMenuNet must use menu_optimization")
    assert_true(current["args_overrides"]["menu_objective_mode"] == "current", "current CNN-SetMenuNet must keep old objective")
    assert_true(current["args_overrides"]["menu_route_delay_lambda"] == 0.0, "current CNN-SetMenuNet route lambda mismatch")
    assert_true(current["args_overrides"]["menu_capacity_risk_lambda"] == 0.0, "current CNN-SetMenuNet capacity lambda mismatch")

    profit_oracle = policies["profit_oracle"]
    assert_true(profit_oracle["policy"] == "profit_oracle", "profit oracle policy mismatch")
    assert_true(profit_oracle["args_overrides"]["menu_objective_mode"] == "system_profit", "profit oracle objective mismatch")
    assert_true(profit_oracle["args_overrides"]["init_theta_cnn"] == 0.0, "profit oracle init theta mismatch")
    assert_true(profit_oracle["args_overrides"]["cool_theta_cnn"] == 0.0, "profit oracle cool theta mismatch")
    assert_true(profit_oracle["args_overrides"]["menu_use_oracle_eta"] is True, "profit oracle ETA override mismatch")


def assert_split(split, split_id, seed):
    assert_true(split["id"] == split_id, f"{split_id} id mismatch")
    assert_true(split["train_split"] == 0, f"{split_id} train split must be 0")
    assert_true(split["test_split"] == 1, f"{split_id} test split must be 1")
    assert_true(split["args_overrides"]["seed"] == seed, f"{split_id} seed mismatch")


def test_smoke_manifest():
    manifest = load("work2_phase08_smoke")
    assert_common_contract(manifest, "work2_phase08_smoke")
    assert_true(manifest["base_args"]["experiment_name"] == "work2_phase08_smoke", "smoke experiment name mismatch")
    assert_true(manifest["base_args"]["max_episodes"] == 1, "smoke train budget must be 1")
    assert_true(manifest["base_args"]["eval_episodes"] == 1, "smoke eval budget must be 1")
    assert_true(len(manifest["splits"]) == 1, "smoke must have one split")
    assert_split(manifest["splits"][0], "seed0", 0)


def test_pilot_manifest():
    manifest = load("work2_phase08_pilot")
    assert_common_contract(manifest, "work2_phase08_pilot")
    assert_true(manifest["base_args"]["experiment_name"] == "work2_phase08_pilot", "pilot experiment name mismatch")
    assert_true(manifest["base_args"]["max_episodes"] == 80, "pilot train budget must be 80")
    assert_true(manifest["base_args"]["eval_episodes"] == 20, "pilot eval budget must be 20")
    assert_true(len(manifest["splits"]) == 3, "pilot must have three splits")
    for index, split in enumerate(manifest["splits"]):
        assert_split(split, f"seed{index}", index)


def main():
    tests = [
        test_smoke_manifest,
        test_pilot_manifest,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} Phase08 manifest tests")


if __name__ == "__main__":
    main()
