import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np

from Environments.OOH.Parcelpoint_py import Parcelpoint_py
from Environments.OOH.containers import ChoiceResult, Customer, Location, MenuOffer, ServiceBundle
from Src.Utils.Utils import generate_demand_data


def make_env():
    coords = generate_demand_data(100)
    service_times = np.ones(len(coords), dtype=float) * 30.0
    env = Parcelpoint_py(
        model="DSPO_Menu",
        max_steps_r=1,
        max_steps_p=0.5,
        pricing=False,
        n_vehicles=2,
        veh_capacity=10,
        parcelpoint_capacity=3,
        fraction_capacitated=0.0,
        incentive_sens=-0.25,
        base_util=-2.0,
        home_util=3.2,
        reopt=10000000,
        load_data=False,
        coords=coords,
        dist_matrix=[],
        n_parcelpoints=6,
        adjacency=[],
        service_times=service_times,
        hgs_time=0.1,
    )
    force_customer(env)
    return env


def force_customer(env, home_id=10, service_time=45.0):
    home = Location(10.0, 10.0, home_id, env.steps)
    env.newCustomer = Customer(home, env.incentive_sens, env.home_util, service_time, home_id)
    env.curr_state = [env.newCustomer, env.fleet, env.parcelPoints, env.steps]


def route_len(env):
    return sum(len(vehicle.routePlan) for vehicle in env.fleet["fleet"])


def data_id_count(env):
    return len(np.atleast_1d(env.data["id"]))


def make_offer(is_home=False):
    loc = Location(10.0, 10.0, 10, 0) if is_home else Location(25.0, 25.0, 0, 0)
    bundle = ServiceBundle(
        bundle_id="home" if is_home else "pp_0",
        location=loc,
        is_home=is_home,
        parcelpoint_id=-1 if is_home else 0,
        window_start=0.0,
        window_end=600.0,
        window_center=300.0,
        window_width=600.0,
        remaining_capacity=1000000.0 if is_home else 3.0,
    )
    return MenuOffer(bundle=bundle, predicted_cost=1.0, price=1.5)


def test_choice_result_contract():
    result = ChoiceResult.opted_out({"reason": "test"})
    assert result.outcome == "opted_out"
    assert result.location is None
    assert result.route_mutates is False


def test_optout_does_not_mutate_routes_or_service():
    env = make_env()
    before_route = route_len(env)
    before_ids = data_id_count(env)
    before_home = env.count_home_delivery
    before_service = env.service_time
    before_capacity = env.parcelPoints["parcelpoints"][0].remainingCapacity

    env.get_delivery_loc = lambda action: ChoiceResult.opted_out({"forced": True})
    _, _, stats, _ = env.step([])

    assert route_len(env) == before_route
    assert data_id_count(env) == before_ids
    assert env.parcelPoints["parcelpoints"][0].remainingCapacity == before_capacity
    assert env.service_time == before_service
    assert env.count_home_delivery == before_home
    assert env.count_opted_out == 1
    assert env.count_accepted_home == 0
    assert env.count_accepted_meeting_point == 0
    assert env.last_selected_offer is None
    assert stats[8]["last_outcome"] == "opted_out"
    assert stats[8]["acceptance_rate"] == 0.0


def test_accepted_home_mutates_service_accounting():
    env = make_env()
    offer = make_offer(is_home=True)
    before_route = route_len(env)
    before_ids = data_id_count(env)
    service_time = env.newCustomer.service_time

    env.get_delivery_loc = lambda action: ChoiceResult.accepted_home(
        env.newCustomer.home,
        offer=offer,
        price=2.0,
    )
    _, _, stats, _ = env.step([offer])

    assert route_len(env) > before_route
    assert data_id_count(env) == before_ids + 1
    assert env.count_home_delivery == 1
    assert env.count_accepted_home == 1
    assert env.count_opted_out == 0
    assert env.service_time == service_time
    assert env.last_selected_offer is offer
    assert stats[1] == 1
    assert stats[8]["acceptance_rate"] == 1.0


def test_accepted_meeting_point_decrements_capacity():
    env = make_env()
    pp = env.parcelPoints["parcelpoints"][0]
    offer = make_offer(is_home=False)
    before_route = route_len(env)
    before_ids = data_id_count(env)
    before_capacity = pp.remainingCapacity

    env.get_delivery_loc = lambda action: ChoiceResult.accepted_meeting_point(
        pp.location,
        pp.id_num,
        offer=offer,
        price=-1.0,
    )
    _, _, stats, _ = env.step([offer])

    assert route_len(env) > before_route
    assert data_id_count(env) == before_ids + 1
    assert pp.remainingCapacity == before_capacity - 1
    assert env.count_accepted_meeting_point == 1
    assert env.count_home_delivery == 0
    assert env.service_time == 0
    assert env.last_selected_offer is offer
    assert stats[8]["last_outcome"] == "accepted_meeting_point"
    assert stats[8]["optout_rate"] == 0.0


def test_mixed_acceptance_and_optout_rates():
    env = make_env()
    pp = env.parcelPoints["parcelpoints"][0]
    outcomes = [
        ChoiceResult.opted_out({"forced": True}),
        ChoiceResult.accepted_home(env.newCustomer.home, price=1.0),
        ChoiceResult.accepted_meeting_point(pp.location, pp.id_num, price=-1.0),
    ]

    def next_choice(action):
        return outcomes.pop(0)

    env.get_delivery_loc = next_choice
    env.step([])
    force_customer(env, home_id=11, service_time=40.0)
    env.step([])
    force_customer(env, home_id=12, service_time=35.0)
    _, _, stats, _ = env.step([])

    assert env.count_opted_out == 1
    assert env.count_accepted_home == 1
    assert env.count_accepted_meeting_point == 1
    assert abs(env.acceptance_rate() - (2.0 / 3.0)) < 1e-12
    assert abs(env.optout_rate() - (1.0 / 3.0)) < 1e-12
    assert abs(stats[8]["acceptance_rate"] - (2.0 / 3.0)) < 1e-12


def main():
    tests = [
        test_choice_result_contract,
        test_optout_does_not_mutate_routes_or_service,
        test_accepted_home_mutates_service_accounting,
        test_accepted_meeting_point_decrements_capacity,
        test_mixed_acceptance_and_optout_rates,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} opt-out accounting tests")


if __name__ == "__main__":
    main()
