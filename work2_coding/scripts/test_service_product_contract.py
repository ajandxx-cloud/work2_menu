import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Environments.OOH.containers import Location, MenuOffer, ServiceBundle, ServiceProduct  # noqa: E402


def make_bundle(is_home=False):
    loc = Location(1.0, 2.0, 7, 0)
    return ServiceBundle(
        bundle_id="home" if is_home else "pp_7",
        location=loc,
        is_home=is_home,
        parcelpoint_id=-1 if is_home else 7,
        window_start=100.0,
        window_end=700.0,
        window_center=400.0,
        window_width=600.0,
        remaining_capacity=9.0,
    )


def test_service_product_from_bundle_and_back():
    bundle = make_bundle()
    product = ServiceProduct.from_bundle(
        bundle,
        product_mode="m+w",
        time_window_mode="fixed_window",
        menu_mode="fixed_menu",
        price=-2.5,
        metadata={"source": "unit"},
    )
    assert product.product_id == bundle.bundle_id
    assert product.window == (100.0, 700.0)
    assert product.price == -2.5
    assert product.is_home is False
    restored = product.to_bundle(remaining_capacity=3.0)
    assert restored.bundle_id == bundle.bundle_id
    assert restored.parcelpoint_id == 7
    assert restored.remaining_capacity == 3.0


def test_service_product_from_offer_preserves_contract_metadata():
    offer = MenuOffer(
        bundle=make_bundle(is_home=True),
        predicted_cost=4.0,
        price=0.0,
        metadata={
            "product_mode": "m",
            "time_window_mode": "no_time_window",
            "menu_mode": "no_menu",
        },
    )
    product = ServiceProduct.from_offer(offer)
    assert product.product_mode == "m"
    assert product.time_window_mode == "no_time_window"
    assert product.menu_mode == "no_menu"
    assert product.is_home is True
    assert product.parcelpoint_id == -1


def test_opt_out_is_not_route_service_product():
    product = ServiceProduct.opt_out({"reason": "outside_option"})
    assert product.is_opt_out is True
    assert product.location is None
    assert product.price == 0.0
    try:
        product.to_bundle()
    except ValueError as exc:
        assert "opt-out" in str(exc)
        return
    raise AssertionError("opt-out must not convert to a route-mutating bundle")


def test_to_offer_writes_contract_metadata():
    product = ServiceProduct.from_bundle(
        make_bundle(),
        product_mode="m+w+p",
        time_window_mode="adaptive_window",
        menu_mode="optimized_menu",
        price=-1.0,
    )
    offer = product.to_offer(
        predicted_cost=3.0,
        predicted_eta=500.0,
        predicted_in_vehicle_time=200.0,
        walk_distance=30.0,
        time_deviation=20.0,
        remaining_capacity=5.0,
    )
    assert offer.price == -1.0
    assert offer.metadata["product_mode"] == "m+w+p"
    assert offer.metadata["time_window_mode"] == "adaptive_window"
    assert offer.metadata["menu_mode"] == "optimized_menu"


def main():
    tests = [
        test_service_product_from_bundle_and_back,
        test_service_product_from_offer_preserves_contract_metadata,
        test_opt_out_is_not_route_service_product,
        test_to_offer_writes_contract_metadata,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} service product contract tests")


if __name__ == "__main__":
    main()
