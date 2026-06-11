import sys
from pathlib import Path
from types import MethodType, SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Environments.OOH.containers import Customer, Location, MenuOffer, ServiceBundle
from Src.Algorithms.DSPO_Menu import DSPO_Menu
from Src.parser import Parser


def make_customer():
    home = Location(0.0, 0.0, 1, 0)
    customer = Customer(home, incentiveSensitivity=-0.1, home_util=0.0, service_time=30.0, id_num=1)
    customer.preferred_pickup_time = 1000.0
    customer.earliest_pickup_time = 900.0
    customer.latest_pickup_time = 1100.0
    return customer


def make_algo(mode="hard"):
    algo = object.__new__(DSPO_Menu)
    algo.menu_eta_filter_mode = mode
    algo._eta_sigma = 60.0
    algo._eta_sigma_source = "test"
    algo.menu_eta_chance_threshold = 0.25
    algo.menu_eta_soft_penalty_lambda = 2.0
    algo.menu_time_scale = 100.0
    algo.pref_window_half_width = 100.0
    algo.display_window_half_width = 50.0
    algo.menu_window_slots_each_side = 3
    algo.menu_target_arrival_time = 1200.0
    algo.menu_pref_buffer_seconds = 0.0
    algo.base_util = 0.0
    algo.menu_travel_time_weight = 0.0
    algo.menu_pickup_time_weight = 0.0
    algo.dist_scaler = 1000.0
    algo.config = SimpleNamespace(home_failure=0.0, failure_cost=0.0)
    algo.menu_objective_mode = "current"
    algo.menu_policy = "menu_optimization"
    algo.requested_menu_policy = "menu_optimization"
    algo.menu_keep_home = True
    algo.menu_k = 2
    algo.menu_selection_solver = "auto"
    algo.menu_use_exact_eval = True
    algo.menu_exact_threshold = 3
    algo.menu_exact_gap_threshold = 0
    algo.max_candidates = 5
    algo.menu_pricing_mode = "zero"
    algo.menu_pricing_constant = 0.0
    algo.min_p = -10.0
    algo.max_p = 10.0
    algo.revenue = 0.0
    algo.cost_multiplier = 1.0
    algo.menu_route_delay_lambda = 0.0
    algo.menu_capacity_risk_lambda = 0.0
    algo.menu_outside_penalty_lambda = 0.0
    algo.menu_quit_tolerance = 0.0
    algo.menu_profit_tolerance_fraction = 0.0
    algo.menu_optout_guardrail = 0.4
    algo.service_quit_penalty = 100.0
    algo.service_quit_rate_guardrail = 0.4
    algo.last_policy_diagnostic = {}
    algo.last_exact_gap_diagnostic = None
    algo.last_candidate_diagnostics = []
    return algo


def make_offer(bundle_id, value=1.0, eta_penalty=0.0, is_home=False):
    loc = Location(float(value), 0.0, int(value) + 10, 0)
    bundle = ServiceBundle(
        bundle_id=bundle_id,
        location=loc,
        is_home=is_home,
        parcelpoint_id=-1 if is_home else int(value),
        window_start=950.0,
        window_end=1050.0,
        window_center=1000.0,
        window_width=100.0,
        remaining_capacity=1000000.0 if is_home else 3.0,
    )
    return MenuOffer(
        bundle=bundle,
        predicted_cost=1.0,
        price=5.0,
        predicted_eta=1000.0,
        predicted_in_vehicle_time=0.0,
        walk_distance=0.0,
        time_deviation=0.0,
        metadata={"value": float(value), "eta_soft_penalty": float(eta_penalty)},
    )


def fake_objective(self, customer, menu, return_priced=False, already_priced=False):
    value = sum(float((offer.metadata or {}).get("value", 0.0)) for offer in menu)
    return (value, menu) if return_priced else value


def test_parser_exposes_robust_menu_flags():
    parser = Parser().get_parser()
    args = parser.parse_args([
        "--algo_name", "DSPO_Menu",
        "--menu_mode", "True",
        "--menu_eta_filter_mode", "interval_overlap",
        "--menu_pricing_mode", "flat_markdown",
        "--menu_eta_chance_threshold", "0.15",
    ])
    assert args.menu_eta_filter_mode == "interval_overlap"
    assert args.menu_pricing_mode == "flat_markdown"
    assert args.menu_eta_chance_threshold == 0.15


def test_eta_filter_modes_and_diagnostics():
    customer = make_customer()

    hard_algo = make_algo("hard")
    hard_window, hard_diag = hard_algo._eta_filter_result(customer, 1250.0)
    assert hard_window is None
    assert hard_diag["eta_filter_passed"] is False
    assert hard_diag["prune_reason"] == "outside_preferred_window"

    interval_algo = make_algo("interval_overlap")
    interval_window, interval_diag = interval_algo._eta_filter_result(customer, 1150.0)
    assert interval_window is not None
    assert interval_diag["eta_filter_passed"] is True
    assert interval_diag["eta_interval_lower"] == 1090.0

    chance_algo = make_algo("chance_constraint")
    chance_algo._eta_sigma = 20.0
    chance_window, chance_diag = chance_algo._eta_filter_result(customer, 1150.0)
    assert chance_window is None
    assert chance_diag["prune_reason"] == "violation_probability_above_threshold"
    assert chance_diag["violation_probability"] > chance_algo.menu_eta_chance_threshold

    soft_algo = make_algo("soft_penalty")
    soft_window, soft_diag = soft_algo._eta_filter_result(customer, 1250.0)
    assert soft_window is not None
    assert soft_diag["retained_in_objective"] is True
    assert soft_diag["eta_soft_penalty"] > 0.0

    none_algo = make_algo("none")
    none_window, none_diag = none_algo._eta_filter_result(customer, 1250.0)
    assert none_window is not None
    assert none_diag["eta_filter_passed"] is True
    assert none_diag["eta_soft_penalty"] == 0.0


def test_home_offer_carries_eta_diagnostics():
    algo = make_algo("soft_penalty")
    customer = make_customer()
    offer = algo._build_home_offer(
        customer,
        home_cost=1.0,
        home_eta=1250.0,
        home_ivt=0.0,
        eta_target=1250.0,
        ivt_target=0.0,
    )
    assert offer.metadata["eta_filter_mode"] == "soft_penalty"
    assert offer.metadata["eta_soft_penalty"] > 0.0
    assert offer.metadata["retained_in_objective"] is True


def test_eta_soft_penalty_enters_objective():
    algo = make_algo("soft_penalty")
    customer = make_customer()
    safe = make_offer("safe", eta_penalty=0.0)
    risky = make_offer("risky", eta_penalty=10.0)

    safe_value = algo.evaluate_menu(customer, [safe], already_priced=True)
    risky_value = algo.evaluate_menu(customer, [risky], already_priced=True)

    assert risky_value < safe_value
    assert risky.metadata["eta_risk_penalty"] == 10.0
    assert risky.metadata["eta_risk_penalty_weighted"] > 0.0


def test_service_guard_fallback_diagnostic():
    algo = make_algo("hard")
    algo.menu_policy = "service_guarded_expected_profit"
    algo.menu_optout_guardrail = 0.1
    evaluated = [
        {
            "menu": [make_offer("high_profit", value=1.0)],
            "predicted_expected_system_profit": 10.0,
            "predicted_outside_probability": 0.7,
            "risk_adjusted_score": 10.0,
            "system_eval_cost": 1.0,
        },
        {
            "menu": [make_offer("low_quit", value=2.0)],
            "predicted_expected_system_profit": 3.0,
            "predicted_outside_probability": 0.3,
            "risk_adjusted_score": 3.0,
            "system_eval_cost": 1.0,
        },
    ]

    selected, diag = algo._choose_redesigned_menu(evaluated)
    assert selected[0].bundle_id == "low_quit"
    assert diag["redesign_fallback_used"] is True
    assert diag["redesign_fallback_reason"] == "no_guardrail_feasible_menu"


def test_solver_exact_and_threshold_fallback_diagnostics():
    customer = make_customer()
    home = make_offer("home", value=0.0, is_home=True)
    offers = [home, make_offer("a", value=1.0), make_offer("b", value=2.0)]

    exact_algo = make_algo("hard")
    exact_algo.menu_selection_solver = "exact"
    exact_algo._evaluate_menu_for_objective = MethodType(fake_objective, exact_algo)
    exact_menu = exact_algo._select_menu_candidates(customer, offers)
    exact_diag = exact_algo.last_policy_diagnostic
    assert [offer.bundle_id for offer in exact_menu if not offer.is_home] == ["a", "b"]
    assert exact_diag["menu_selection_solver_effective"] == "exact"
    assert exact_diag["exact_enumerated_menu_count"] == 3

    greedy_algo = make_algo("hard")
    greedy_algo.menu_selection_solver = "exact"
    greedy_algo.menu_exact_threshold = 1
    greedy_algo._evaluate_menu_for_objective = MethodType(fake_objective, greedy_algo)
    greedy_menu = greedy_algo._select_menu_candidates(customer, offers)
    greedy_diag = greedy_algo.last_policy_diagnostic
    assert len(greedy_menu) == 3
    assert greedy_diag["menu_selection_solver_effective"] == "greedy"
    assert greedy_diag["solver_fallback_used"] is True
    assert greedy_diag["solver_fallback_reason"] == "above_exact_threshold"


def main():
    tests = [
        test_parser_exposes_robust_menu_flags,
        test_eta_filter_modes_and_diagnostics,
        test_home_offer_carries_eta_diagnostics,
        test_eta_soft_penalty_enters_objective,
        test_service_guard_fallback_diagnostic,
        test_solver_exact_and_threshold_fallback_diagnostics,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} robust menu logic tests")


if __name__ == "__main__":
    main()
