import math
import sys
from pathlib import Path

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


def make_algo(attention_enabled=False, attention_strength=1.0):
    algo = object.__new__(DSPO_Menu)
    algo.menu_policy = "menu_optimization"
    algo.requested_menu_policy = "menu_optimization"
    algo.menu_objective_mode = "current"
    algo.menu_keep_home = False
    algo.menu_k = 1
    algo.menu_selection_solver = "exact"
    algo.menu_use_exact_eval = True
    algo.menu_exact_threshold = 3
    algo.menu_exact_gap_threshold = 0
    algo.max_candidates = 3
    algo.menu_pricing_mode = "zero"
    algo.menu_pricing_constant = 0.0
    algo.min_p = -10.0
    algo.max_p = 10.0
    algo.revenue = 10.0
    algo.base_util = 0.0
    algo.menu_travel_time_weight = 0.0
    algo.menu_pickup_time_weight = 0.0
    algo.dist_scaler = 1000.0
    algo.menu_time_scale = 100.0
    algo.cost_multiplier = 1.0
    algo.menu_route_delay_lambda = 0.0
    algo.menu_capacity_risk_lambda = 0.0
    algo.menu_outside_penalty_lambda = 0.0
    algo.menu_quit_tolerance = 0.0
    algo.menu_profit_tolerance_fraction = 0.0
    algo.menu_optout_guardrail = 0.4
    algo.service_quit_penalty = 100.0
    algo.service_quit_rate_guardrail = 0.4
    algo.method_variant = "DSPO_attention" if attention_enabled else "DSPO_original"
    algo.attention_enabled = bool(attention_enabled)
    algo.attention_mode = "deterministic"
    algo.attention_strength = float(attention_strength)
    algo.attention_feature_weights = {
        "eta_risk": -1.0,
        "walk": -0.25,
        "time": -0.25,
        "cost": -0.05,
        "route_delay": -0.5,
        "capacity_risk": -0.5,
        "price": 0.05,
    }
    algo.last_policy_diagnostic = {}
    algo.last_exact_gap_diagnostic = None
    algo.last_candidate_diagnostics = []
    return algo


def make_offer(bundle_id, cost, eta_risk=0.0, walk=0.0, capacity=10.0):
    loc = Location(float(cost), 0.0, int(cost * 10) + len(bundle_id), 0)
    bundle = ServiceBundle(
        bundle_id=bundle_id,
        location=loc,
        is_home=False,
        parcelpoint_id=int(cost * 10),
        window_start=950.0,
        window_end=1050.0,
        window_center=1000.0,
        window_width=100.0,
        remaining_capacity=capacity,
    )
    return MenuOffer(
        bundle=bundle,
        predicted_cost=float(cost),
        price=0.0,
        predicted_eta=1000.0,
        predicted_in_vehicle_time=0.0,
        walk_distance=float(walk),
        time_deviation=0.0,
        metadata={"eta_risk_score": float(eta_risk), "route_delay": 0.0},
    )


def test_parser_attention_defaults_and_choices():
    args = Parser().get_parser().parse_args([])
    assert args.method_variant == "DSPO_original"
    assert args.attention_enabled is False
    assert args.attention_mode == "deterministic"

    enabled = Parser().get_parser().parse_args([
        "--method_variant", "DSPO_attention",
        "--attention_enabled", "True",
        "--attention_strength", "2.5",
        "--attention_mode", "neural",
    ])
    assert enabled.method_variant == "DSPO_attention"
    assert enabled.attention_enabled is True
    assert enabled.attention_mode == "neural"
    assert enabled.attention_strength == 2.5


def test_disabled_attention_preserves_objective_value():
    customer = make_customer()
    offer = make_offer("risky", cost=1.0, eta_risk=3.0)
    original = make_algo(attention_enabled=False)
    explicit_disabled = make_algo(attention_enabled=False, attention_strength=100.0)

    value_original = original._evaluate_menu_for_objective(customer, [offer])
    value_disabled = explicit_disabled._evaluate_menu_for_objective(customer, [offer])

    assert math.isclose(value_original, value_disabled, rel_tol=0.0, abs_tol=1e-12)
    assert original.last_policy_diagnostic["attention_enabled"] is False


def test_deterministic_attention_writes_diagnostics():
    customer = make_customer()
    offer = make_offer("safe", cost=2.0, eta_risk=0.0, walk=10.0)
    algo = make_algo(attention_enabled=True, attention_strength=3.0)

    value, priced = algo.evaluate_menu(customer, [offer], return_priced=True)
    metadata = priced[0].metadata

    assert value < 0.0
    assert metadata["method_variant"] == "DSPO_attention"
    assert metadata["attention_enabled"] is True
    assert metadata["attention_mode"] == "deterministic"
    assert "eta_risk" in metadata["attention_features"]
    assert math.isfinite(metadata["attention_weight"])
    assert math.isfinite(metadata["attention_score_delta"])
    assert "attention_weight_summary" in algo.last_policy_diagnostic


def test_attention_changes_exact_selection():
    customer = make_customer()
    risky_cheap = make_offer("risky_cheap", cost=1.0, eta_risk=4.0)
    safe_costly = make_offer("safe_costly", cost=2.0, eta_risk=0.0)

    original = make_algo(attention_enabled=False)
    original_menu = original._select_menu_candidates(customer, [risky_cheap, safe_costly])
    assert [offer.bundle_id for offer in original_menu] == ["risky_cheap"]

    attention = make_algo(attention_enabled=True, attention_strength=10.0)
    attention_menu = attention._select_menu_candidates(customer, [risky_cheap, safe_costly])
    assert [offer.bundle_id for offer in attention_menu] == ["safe_costly"]
    summary = attention.last_policy_diagnostic["attention_weight_summary"]
    assert summary["attention_weight_min"] is not None
    assert summary["attention_score_delta_total"] <= 0.0


def main():
    tests = [
        test_parser_attention_defaults_and_choices,
        test_disabled_attention_preserves_objective_value,
        test_deterministic_attention_writes_diagnostics,
        test_attention_changes_exact_selection,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} attention menu logic tests")


if __name__ == "__main__":
    main()
