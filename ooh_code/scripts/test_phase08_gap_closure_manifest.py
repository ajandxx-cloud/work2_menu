from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
STUDIES = ROOT / "experiments" / "studies"

EXPECTED_GRID = {
    (100.0, 0.3),
    (100.0, 0.4),
    (200.0, 0.3),
    (200.0, 0.4),
    (500.0, 0.3),
    (500.0, 0.4),
}
BASE_TAGS = [
    "nearest_L",
    "cost_L",
    "cnn_menu",
    "cnn_setmenu_net_current",
    "expected_profit_enumeration",
    "service_constrained_expected_profit",
    "cost_oracle",
    "profit_oracle",
]


def load(name):
    with open(STUDIES / f"{name}.yaml", "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def parse_grid_tag(tag):
    prefix, base = tag.split("_", 2)[0:2], tag.split("_", 2)[2]
    penalty = float(prefix[0][1:])
    guardrail = float(prefix[1][1:]) / 10.0
    return penalty, guardrail, base


def assert_common(manifest, expected_name, max_episodes, eval_episodes, expected_seeds):
    base_args = manifest["base_args"]
    assert_true(manifest["name"] == expected_name, f"{expected_name} name mismatch")
    assert_true(manifest["type"] == "policy_compare", f"{expected_name} must be policy_compare")
    assert_true(manifest["reference_tag"] == "full_display", f"{expected_name} reference tag mismatch")
    assert_true(manifest["reference_policy"] == "offer_all_feasible_bundles", f"{expected_name} reference mismatch")
    assert_true(base_args["experiment_name"] == expected_name, f"{expected_name} experiment name mismatch")
    assert_true(base_args["instance"] == "RC", f"{expected_name} must use RC")
    assert_true(base_args["menu_k"] == 3, f"{expected_name} must use L=3")
    assert_true(base_args["candidate_meeting_points"] == 10, f"{expected_name} must request K=10")
    assert_true(base_args["max_candidates"] == 10, f"{expected_name} must cap K=10")
    assert_true(base_args["menu_selection_solver"] == "exact", f"{expected_name} must use exact solver")
    assert_true(base_args["menu_use_exact_eval"] is True, f"{expected_name} must enable exact eval")
    assert_true(base_args["menu_exact_threshold"] == 8, f"{expected_name} exact threshold mismatch")
    assert_true(base_args["menu_objective_mode"] == "system_profit", f"{expected_name} must use system_profit")
    assert_true(base_args["max_episodes"] == max_episodes, f"{expected_name} train budget mismatch")
    assert_true(base_args["eval_episodes"] == eval_episodes, f"{expected_name} eval budget mismatch")

    seeds = [split["args_overrides"]["seed"] for split in manifest["splits"]]
    assert_true(seeds == expected_seeds, f"{expected_name} seed mismatch")
    for split in manifest["splits"]:
        assert_true(split["train_split"] == 0, f"{split['id']} train split must be 0")
        assert_true(split["test_split"] == 1, f"{split['id']} test split must be 1")

    policies_by_grid = {}
    for policy in manifest["policies"]:
        penalty, guardrail, base_tag = parse_grid_tag(policy["tag"])
        overrides = policy.get("args_overrides", {})
        policies_by_grid.setdefault((penalty, guardrail), set()).add(base_tag)
        assert_true((penalty, guardrail) in EXPECTED_GRID, f"unexpected grid for {policy['tag']}")
        assert_true(overrides["service_quit_penalty"] == penalty, f"penalty override mismatch for {policy['tag']}")
        assert_true(overrides["service_quit_rate_guardrail"] == guardrail, f"guardrail override mismatch for {policy['tag']}")

        if base_tag == "cnn_setmenu_net_current":
            assert_true(policy["policy"] == "menu_optimization", "current CNN policy mismatch")
            assert_true(overrides["menu_model"] == "cnn_setmenu", "current CNN model mismatch")
            assert_true(overrides["menu_objective_mode"] == "current", "current CNN objective mismatch")
            assert_true(overrides["menu_route_delay_lambda"] == 0.0, "current CNN route lambda mismatch")
            assert_true(overrides["menu_capacity_risk_lambda"] == 0.0, "current CNN capacity lambda mismatch")
        if base_tag in {"expected_profit_enumeration", "service_constrained_expected_profit"}:
            assert_true(overrides["menu_objective_mode"] == "system_profit", f"{base_tag} objective mismatch")
        if base_tag == "profit_oracle":
            assert_true(policy["policy"] == "profit_oracle", "profit oracle policy mismatch")
            assert_true(overrides["menu_objective_mode"] == "system_profit", "profit oracle objective mismatch")
            assert_true(overrides["init_theta_cnn"] == 0.0, "profit oracle init theta mismatch")
            assert_true(overrides["cool_theta_cnn"] == 0.0, "profit oracle cool theta mismatch")
            assert_true(overrides["menu_use_oracle_eta"] is True, "profit oracle ETA mismatch")

    assert_true(set(policies_by_grid) == EXPECTED_GRID, f"{expected_name} grid mismatch")
    for grid, tags in policies_by_grid.items():
        assert_true(tags == set(BASE_TAGS), f"{expected_name} base policies mismatch for {grid}")
    assert_true(len(manifest["policies"]) == len(EXPECTED_GRID) * len(BASE_TAGS), f"{expected_name} policy count mismatch")


def test_smoke_manifest():
    assert_common(load("work2_phase08_gap_closure_smoke"), "work2_phase08_gap_closure_smoke", 1, 1, [0])


def test_gap_closure_manifest():
    assert_common(load("work2_phase08_gap_closure"), "work2_phase08_gap_closure", 80, 20, [0, 1, 2])
    assert_true((STUDIES / "work2_formal_main.yaml").exists(), "formal manifest should exist but not be modified here")


def main():
    tests = [test_smoke_manifest, test_gap_closure_manifest]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} Phase08 gap-closure manifest tests")


if __name__ == "__main__":
    main()
