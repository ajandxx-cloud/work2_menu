from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Src.Algorithms.DSPO_Menu import DSPO_Menu


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def fake_agent(policy):
    agent = DSPO_Menu.__new__(DSPO_Menu)
    agent.menu_policy = policy
    agent.menu_outside_penalty_lambda = 200.0
    agent.menu_quit_tolerance = 0.01
    agent.menu_profit_tolerance_fraction = 0.05
    agent.menu_optout_guardrail = 0.40
    return agent


def evaluated(menu, profit, outside, score=None, cost=0.0):
    if score is None:
        score = profit - 200.0 * outside
    return {
        "menu": menu,
        "predicted_expected_system_profit": profit,
        "predicted_outside_probability": outside,
        "risk_adjusted_score": score,
        "system_eval_cost": cost,
    }


def test_evaluate_menu_exposes_outside_probability():
    source = (Path(__file__).resolve().parents[1] / "Src" / "Algorithms" / "DSPO_Menu.py").read_text(encoding="utf-8")
    assert_true("menu_outside_probability" in source, "evaluate_menu must expose menu_outside_probability")


def test_risk_penalty_changes_score():
    agent = fake_agent("risk_adjusted_expected_profit")
    menu, diag = DSPO_Menu._choose_redesigned_menu(agent, [
        evaluated(["high_out"], profit=100.0, outside=0.40),
        evaluated(["low_out"], profit=100.0, outside=0.10),
    ])
    assert_true(menu == ["low_out"], "risk-adjusted score should prefer lower outside probability at fixed profit")
    assert_true(diag["risk_adjusted_score"] == 80.0, "risk-adjusted score mismatch")


def test_min_quit_then_profit_prefers_lower_optout_then_profit():
    agent = fake_agent("min_quit_then_profit")
    menu, diag = DSPO_Menu._choose_redesigned_menu(agent, [
        evaluated(["profit_only"], profit=120.0, outside=0.20),
        evaluated(["low_out_lower_profit"], profit=110.0, outside=0.10),
        evaluated(["low_out_higher_profit"], profit=120.0, outside=0.105),
    ])
    assert_true(menu == ["low_out_higher_profit"], "min-quit should choose best profit inside low-outside band")
    assert_true(abs(diag["min_predicted_outside_probability"] - 0.10) < 1e-12, "min outside mismatch")


def test_service_guarded_feasible_and_fallback():
    agent = fake_agent("service_guarded_expected_profit")
    menu, diag = DSPO_Menu._choose_redesigned_menu(agent, [
        evaluated(["too_high"], profit=130.0, outside=0.50),
        evaluated(["feasible"], profit=100.0, outside=0.30),
    ])
    assert_true(menu == ["feasible"], "service-guarded should filter by guardrail")
    assert_true(diag["redesign_fallback_used"] is False, "feasible case should not fallback")

    menu, diag = DSPO_Menu._choose_redesigned_menu(agent, [
        evaluated(["bad"], profit=130.0, outside=0.60),
        evaluated(["least_bad"], profit=100.0, outside=0.50),
    ])
    assert_true(menu == ["least_bad"], "fallback should choose lowest outside probability")
    assert_true(diag["redesign_fallback_used"] is True, "infeasible case should mark fallback")


def test_exact_enumeration_count_is_not_hard_coded():
    agent = fake_agent("risk_adjusted_expected_profit")
    candidates = ["a", "b", "c", "d"]
    variable = list(DSPO_Menu.enumerate_candidate_subsets(agent, candidates, 3))
    fixed = list(DSPO_Menu.enumerate_fixed_candidate_subsets(agent, candidates, 3))
    assert_true(len(variable) == 14, "variable subset enumeration should sum C(n,i)")
    assert_true(len(fixed) == 4, "fixed subset enumeration should use exact subset size")


def main():
    tests = [
        test_evaluate_menu_exposes_outside_probability,
        test_risk_penalty_changes_score,
        test_min_quit_then_profit_prefers_lower_optout_then_profit,
        test_service_guarded_feasible_and_fallback,
        test_exact_enumeration_count_is_not_hard_coded,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} Phase 6 redesign policy tests")


if __name__ == "__main__":
    main()
