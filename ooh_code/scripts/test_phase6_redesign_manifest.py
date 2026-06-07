from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Src.parser import Parser


STUDIES = ROOT / "experiments" / "studies"

NEW_POLICIES = [
    "risk_adjusted_expected_profit",
    "min_quit_then_profit",
    "service_guarded_expected_profit",
]
EXISTING_POLICIES = [
    "cost_l_heuristic",
    "top_k_cheapest",
    "expected_profit_enumeration",
    "service_constrained_expected_profit",
    "cost_oracle",
    "profit_oracle",
]
REQUIRED_TAGS = {
    "nearest_L",
    "cost_L",
    "cnn_menu",
    "expected_profit_enumeration",
    "service_constrained_expected_profit",
    "risk_lambda_50",
    "risk_lambda_100",
    "risk_lambda_200",
    "risk_lambda_400",
    "min_quit_tol000",
    "min_quit_tol001",
    "min_quit_tol003",
    "service_guarded_diagnostic",
    "cost_oracle",
    "profit_oracle",
}
MAIN_CANDIDATE_TAGS = [
    "risk_lambda_50",
    "risk_lambda_100",
    "risk_lambda_200",
    "risk_lambda_400",
    "min_quit_tol000",
    "min_quit_tol001",
    "min_quit_tol003",
]


def load_manifest(name):
    with open(STUDIES / f"{name}.yaml", "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def test_parser_accepts_redesign_policies_and_args():
    parser = Parser()
    for policy in NEW_POLICIES + EXISTING_POLICIES:
        args = parser.parse_args(["--menu_policy", policy])
        assert_true(args.menu_policy == policy, f"parser rejected {policy}")

    defaults = parser.parse_args([])
    assert_true(defaults.menu_outside_penalty_lambda == 0.0, "outside penalty default mismatch")
    assert_true(defaults.menu_quit_tolerance == 0.01, "quit tolerance default mismatch")
    assert_true(defaults.menu_profit_tolerance_fraction == 0.05, "profit tolerance default mismatch")
    assert_true(defaults.menu_optout_guardrail == 0.40, "optout guardrail default mismatch")


def assert_manifest(name, max_episodes, eval_episodes, seeds):
    manifest = load_manifest(name)
    base_args = manifest["base_args"]
    assert_true(manifest["name"] == name, f"{name} name mismatch")
    assert_true(manifest["type"] == "policy_compare", f"{name} must be policy_compare")
    assert_true(manifest["reference_policy"] == "offer_all_feasible_bundles", f"{name} reference mismatch")
    assert_true(base_args["experiment_name"] == name, f"{name} experiment mismatch")
    assert_true(base_args["instance"] == "RC", f"{name} instance mismatch")
    assert_true(base_args["max_episodes"] == max_episodes, f"{name} max_episodes mismatch")
    assert_true(base_args["eval_episodes"] == eval_episodes, f"{name} eval_episodes mismatch")
    assert_true(base_args["menu_k"] == 3, f"{name} menu_k mismatch")
    assert_true(base_args["max_candidates"] == 10, f"{name} max_candidates mismatch")
    assert_true(base_args["menu_objective_mode"] == "system_profit", f"{name} objective mismatch")
    assert_true(base_args["menu_outside_penalty_lambda"] == 200.0, f"{name} lambda mismatch")
    assert_true(base_args["menu_quit_tolerance"] == 0.01, f"{name} quit tolerance mismatch")
    assert_true(base_args["menu_profit_tolerance_fraction"] == 0.05, f"{name} profit tolerance mismatch")
    assert_true(base_args["menu_optout_guardrail"] == 0.40, f"{name} guardrail mismatch")
    gate = manifest["behavior_gate"]
    assert_true(gate["min_acceptance_rate"] == 0.05, f"{name} min acceptance gate mismatch")
    assert_true(gate["max_acceptance_rate"] == 1.00, f"{name} max acceptance gate mismatch")
    assert_true(gate["max_opt_out_rate"] == 0.90, f"{name} opt-out gate mismatch")
    phase_gate = manifest["phase6_redesign_gate"]
    assert_true(phase_gate["main_candidate_tags"] == MAIN_CANDIDATE_TAGS, f"{name} candidate tags mismatch")
    assert_true(
        phase_gate["diagnostic_only_tags"] == ["service_guarded_diagnostic"],
        f"{name} diagnostic-only tags mismatch",
    )

    actual_seeds = [split["args_overrides"]["seed"] for split in manifest["splits"]]
    assert_true(actual_seeds == seeds, f"{name} seed mismatch")
    tags = {policy["tag"] for policy in manifest["policies"]}
    assert_true(tags == REQUIRED_TAGS, f"{name} policy tags mismatch: {tags}")
    policy_by_tag = {policy["tag"]: policy for policy in manifest["policies"]}
    assert_true(policy_by_tag["risk_lambda_50"]["args_overrides"]["menu_outside_penalty_lambda"] == 50.0, "lambda 50 missing")
    assert_true(policy_by_tag["risk_lambda_100"]["args_overrides"]["menu_outside_penalty_lambda"] == 100.0, "lambda 100 missing")
    assert_true(policy_by_tag["risk_lambda_200"]["args_overrides"]["menu_outside_penalty_lambda"] == 200.0, "lambda 200 missing")
    assert_true(policy_by_tag["risk_lambda_400"]["args_overrides"]["menu_outside_penalty_lambda"] == 400.0, "lambda 400 missing")
    assert_true(policy_by_tag["min_quit_tol000"]["args_overrides"]["menu_quit_tolerance"] == 0.0, "tol 0.00 missing")
    assert_true(policy_by_tag["min_quit_tol001"]["args_overrides"]["menu_quit_tolerance"] == 0.01, "tol 0.01 missing")
    assert_true(policy_by_tag["min_quit_tol003"]["args_overrides"]["menu_quit_tolerance"] == 0.03, "tol 0.03 missing")
    assert_true(
        policy_by_tag["service_guarded_diagnostic"]["policy"] == "service_guarded_expected_profit",
        "service-guarded diagnostic policy mismatch",
    )


def test_manifests():
    assert_manifest("work2_phase6_redesign_smoke", 1, 1, [0])
    assert_manifest("work2_phase6_redesign_diagnostic", 80, 20, [0, 1, 2])


def main():
    tests = [test_parser_accepts_redesign_policies_and_args, test_manifests]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} Phase 6 redesign manifest tests")


if __name__ == "__main__":
    main()
