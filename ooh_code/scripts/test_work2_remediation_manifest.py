from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
STUDIES = ROOT / "experiments" / "studies"


def load(name):
    with open(STUDIES / f"{name}.yaml", "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def test_smoke_manifest():
    manifest = load("work2_remediation_smoke")
    assert_true(manifest["base_args"]["menu_objective_mode"] == "system_profit", "smoke must exercise system_profit")
    assert_true(len(manifest["splits"]) == 1, "smoke must be one seed")
    tags = {policy["tag"] for policy in manifest["policies"]}
    assert_true("cnn_setmenu_net_current" in tags, "smoke must keep current objective comparator")
    assert_true("cnn_setmenu_net_system_profit" in tags, "smoke must include system_profit headline")


def test_phase3_expected_profit_smoke_manifest():
    manifest = load("work2_phase3_expected_profit_smoke")
    assert_true(manifest["base_args"]["max_candidates"] == 10, "Phase 3 smoke must use K=10")
    assert_true(manifest["base_args"]["candidate_meeting_points"] == 10, "Phase 3 smoke must request 10 candidates")
    assert_true(manifest["base_args"]["menu_k"] == 3, "Phase 3 smoke must use L=3")
    tags = {policy["tag"] for policy in manifest["policies"]}
    required = {
        "cost_oracle",
        "expected_profit_enumeration",
        "service_constrained_expected_profit",
        "profit_oracle",
    }
    assert_true(required.issubset(tags), "Phase 3 smoke must include new expected-profit contracts")


def test_pilot_manifest():
    manifest = load("work2_remediation_pilot")
    seeds = [split["args_overrides"]["seed"] for split in manifest["splits"]]
    assert_true(seeds == [0, 1, 2], "pilot must use seeds 0..2")
    assert_true(manifest["base_args"]["max_episodes"] == 80, "pilot train budget must be 80")
    assert_true(manifest["base_args"]["eval_episodes"] == 20, "pilot eval budget must be 20")
    tags = {policy["tag"] for policy in manifest["policies"]}
    assert_true("cnn_setmenu_net_system_profit_route025" in tags, "pilot must include a route-delay sweep candidate")
    assert_true("cnn_setmenu_net_system_profit" in tags, "pilot must include a system_profit headline candidate")


def test_formal_manifest():
    manifest = load("work2_remediation_formal")
    seeds = [split["args_overrides"]["seed"] for split in manifest["splits"]]
    assert_true(seeds == [0, 1, 2, 3, 4], "formal must use seeds 0..4")
    assert_true(manifest["base_args"]["max_episodes"] == 150, "formal train budget must be 150")
    assert_true(manifest["base_args"]["eval_episodes"] == 50, "formal eval budget must be 50")
    assert_true(manifest["base_args"]["menu_objective_mode"] == "system_profit", "formal must use remediated objective")
    tags = {policy["tag"] for policy in manifest["policies"]}
    required = {"nearest_L", "cost_L", "cnn_menu", "mlp_menu", "setmenu_net", "cnn_setmenu_net", "oracle_menu"}
    assert_true(required.issubset(tags), "formal must retain all required Phase 6 methods")


def main():
    tests = [
        test_smoke_manifest,
        test_phase3_expected_profit_smoke_manifest,
        test_pilot_manifest,
        test_formal_manifest,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} Work2 remediation manifest tests")


if __name__ == "__main__":
    main()
