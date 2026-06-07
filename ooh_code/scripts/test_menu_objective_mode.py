from types import SimpleNamespace
import os
import sys


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Environments.OOH.containers import Customer, Location, MenuOffer, ServiceBundle
from Src.Algorithms.DSPO_Menu import DSPO_Menu


def make_algo(objective_mode, menu_policy="menu_optimization"):
    algo = object.__new__(DSPO_Menu)
    algo.requested_menu_policy = menu_policy
    algo.menu_policy = menu_policy
    algo.menu_k = 3
    algo.max_candidates = 10
    algo.menu_keep_home = True
    algo.menu_exact_threshold = 8
    algo.menu_objective_mode = objective_mode
    algo.menu_pricing_mode = "cost_plus"
    algo.menu_pricing_constant = -3.0
    algo.menu_route_delay_lambda = 1.0
    algo.menu_capacity_risk_lambda = 0.0
    algo.service_quit_penalty = 100.0
    algo.service_quit_rate_guardrail = 0.0
    algo.last_policy_diagnostic = {}
    algo.cost_multiplier = 1.0
    algo.revenue = 0.0
    algo.min_p = -1_000.0
    algo.max_p = 1_000.0
    algo.base_util = 1.0
    algo.menu_travel_time_weight = 0.0
    algo.menu_pickup_time_weight = 0.0
    algo.dist_scaler = 1_000.0
    algo.config = SimpleNamespace(home_failure=0.0, failure_cost=0.0)
    return algo


def make_customer():
    return Customer(
        home=Location(0.0, 0.0, 1, 0),
        incentiveSensitivity=-0.08,
        home_util=1.0,
        service_time=0.0,
        id_num=1,
    )


def make_offer(idx=1, is_home=False):
    bundle = ServiceBundle(
        bundle_id="home" if is_home else f"pp_{idx}",
        location=Location(float(idx), float(idx), idx + 1, 0),
        is_home=is_home,
        parcelpoint_id=-1 if is_home else idx + 1,
        window_start=0.0,
        window_end=1.0,
        window_center=0.5,
        window_width=1.0,
        remaining_capacity=10.0,
    )
    return MenuOffer(
        bundle=bundle,
        predicted_cost=10.0,
        price=0.0,
        predicted_eta=0.0,
        predicted_in_vehicle_time=0.0,
        walk_distance=0.0,
        time_deviation=0.0,
        metadata={"route_delay": 100.0, "insertion_cost": float(idx)},
    )


def test_current_mode_preserves_menu_cost_pricing():
    algo = make_algo("current")
    _, priced = algo._evaluate_menu_for_objective(make_customer(), [make_offer()], return_priced=True)
    offer = priced[0]
    assert offer.price == 10.0
    assert offer.metadata["pricing_eval_cost_kind"] == "menu_eval_cost"
    assert offer.metadata["evaluation_cost_kind"] == "system_eval_cost"
    assert offer.metadata["system_eval_cost"] == 110.0


def test_system_profit_aligns_pricing_and_evaluation_cost():
    algo = make_algo("system_profit")
    _, priced = algo._evaluate_menu_for_objective(make_customer(), [make_offer()], return_priced=True)
    offer = priced[0]
    assert offer.price == 110.0
    assert offer.metadata["pricing_eval_cost_kind"] == "system_eval_cost"
    assert offer.metadata["evaluation_cost_kind"] == "system_eval_cost"
    assert offer.metadata["choice_probability"] >= 0.0
    assert "expected_profit" in offer.metadata


def test_expected_profit_enumeration_counts_k10_l3():
    algo = make_algo("current", menu_policy="expected_profit_enumeration")
    home = make_offer(0, is_home=True)
    candidates = [make_offer(idx) for idx in range(10)]
    selected = algo._select_menu_exact(make_customer(), home, candidates)
    assert len([offer for offer in selected if not offer.is_home]) == 3
    assert algo.last_policy_diagnostic["exact_enumerated_menu_count"] == 120
    assert algo.last_policy_diagnostic["effective_menu_policy"] == "expected_profit_enumeration"


def test_service_constrained_fallback_diagnostic():
    algo = make_algo("current", menu_policy="service_constrained_expected_profit")
    home = make_offer(0, is_home=True)
    candidates = [make_offer(idx) for idx in range(3)]
    selected = algo._select_menu_service_constrained(make_customer(), home, candidates)
    assert len([offer for offer in selected if not offer.is_home]) == 3
    assert algo.last_policy_diagnostic["service_constrained_fallback_used"] is True
    assert algo.last_policy_diagnostic["service_constrained_fallback_reason"] == "no_guardrail_feasible_menu"


def main():
    tests = [
        test_current_mode_preserves_menu_cost_pricing,
        test_system_profit_aligns_pricing_and_evaluation_cost,
        test_expected_profit_enumeration_counts_k10_l3,
        test_service_constrained_fallback_diagnostic,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} menu objective mode tests")


if __name__ == "__main__":
    main()
