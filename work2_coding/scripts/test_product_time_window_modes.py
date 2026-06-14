import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Environments.OOH.containers import Location, MenuOffer, ServiceBundle  # noqa: E402
from Src.Algorithms.DSPO_Menu import DSPO_Menu  # noqa: E402


def make_algo(product_mode, time_window_mode="adaptive_window", pricing_mode="lambertw"):
    algo = object.__new__(DSPO_Menu)
    algo.product_mode = product_mode
    algo.time_window_mode = time_window_mode
    algo.menu_contract_mode = "optimized_menu"
    algo.menu_pricing_mode = pricing_mode
    algo.base_util = -2.0
    algo.menu_travel_time_weight = 0.0
    algo.menu_pickup_time_weight = -1.0
    algo.dist_scaler = 1000.0
    algo.menu_time_scale = 1000.0
    algo.config = SimpleNamespace(outside_option_util=0.0)
    return algo


def make_offer(price=-4.0, time_deviation=10.0):
    loc = Location(0.0, 0.0, 1, 0)
    bundle = ServiceBundle(
        bundle_id="pp_1",
        location=loc,
        is_home=False,
        parcelpoint_id=1,
        window_start=0.0,
        window_end=600.0,
        window_center=300.0,
        window_width=600.0,
        remaining_capacity=10.0,
    )
    return MenuOffer(
        bundle=bundle,
        predicted_cost=2.0,
        price=price,
        predicted_eta=300.0,
        predicted_in_vehicle_time=0.0,
        walk_distance=0.0,
        time_deviation=time_deviation,
    )


def test_m_mode_disables_window_and_price_utility():
    customer = SimpleNamespace(home_util=0.0, incentiveSensitivity=-0.25)
    algo = make_algo("m", "no_time_window")
    base = algo._menu_utility(customer, make_offer(price=-4.0, time_deviation=0.0), include_price=True)
    changed = algo._menu_utility(customer, make_offer(price=-99.0, time_deviation=99.0), include_price=True)
    assert base == changed
    assert algo._effective_pricing_mode() == "no_pricing"


def test_m_plus_w_uses_window_but_not_price():
    customer = SimpleNamespace(home_util=0.0, incentiveSensitivity=-0.25)
    algo = make_algo("m+w", "fixed_window")
    near = algo._menu_utility(customer, make_offer(price=-4.0, time_deviation=0.0), include_price=True)
    late_same_price = algo._menu_utility(customer, make_offer(price=-4.0, time_deviation=10.0), include_price=True)
    late_other_price = algo._menu_utility(customer, make_offer(price=-99.0, time_deviation=10.0), include_price=True)
    assert late_same_price < near
    assert late_other_price == late_same_price
    assert algo._effective_pricing_mode() == "no_pricing"


def test_m_plus_w_plus_p_uses_window_and_price():
    customer = SimpleNamespace(home_util=0.0, incentiveSensitivity=-0.25)
    algo = make_algo("m+w+p", "adaptive_window")
    no_discount = algo._menu_utility(customer, make_offer(price=0.0, time_deviation=10.0), include_price=True)
    discount = algo._menu_utility(customer, make_offer(price=-4.0, time_deviation=10.0), include_price=True)
    assert discount > no_discount
    assert algo._effective_pricing_mode() == "lambertw"


def test_no_filter_is_not_no_time_window():
    algo = make_algo("m+w", "adaptive_window")
    algo.menu_eta_filter_mode = "none"
    assert algo.time_window_mode == "adaptive_window"
    assert algo._product_uses_window() is True


def main():
    tests = [
        test_m_mode_disables_window_and_price_utility,
        test_m_plus_w_uses_window_but_not_price,
        test_m_plus_w_plus_p_uses_window_and_price,
        test_no_filter_is_not_no_time_window,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} product time-window mode tests")


if __name__ == "__main__":
    main()
