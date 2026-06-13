import csv
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Environments.OOH.containers import Customer, Location, MenuOffer, ServiceBundle
from Environments.OOH.customerchoice import customerchoicemodel
from Src.parser import Parser
from Src.Utils.Utils import total_costs
from scripts.run_akkerman_rc_no_failure import (
    RAW_FIELDS,
    STRATEGIES,
    acceptance_gates,
    akkerman_base_args,
    analyze,
    summarize_rows,
    strategy_overrides,
)


def make_offer(is_home):
    loc = Location(0.0, 0.0, 1 if is_home else 2, 0)
    bundle = ServiceBundle(
        bundle_id="home" if is_home else "pp_2",
        location=loc,
        is_home=is_home,
        parcelpoint_id=-1 if is_home else 2,
        window_start=0.0,
        window_end=600.0,
        window_center=300.0,
        window_width=600.0,
        remaining_capacity=1000000.0 if is_home else 5.0,
    )
    return MenuOffer(bundle=bundle, predicted_cost=1.0, price=0.0, predicted_utility=10.0)


def make_choice(service_mode="mixed", outside_option_util=None):
    return customerchoicemodel(
        base_util=-2.0,
        dist_scaler=100.0,
        euclidean=lambda a, b: 1.0,
        dist_mat=[],
        n_cust=1,
        outside_option_util=outside_option_util,
        service_mode=service_mode,
    )


def test_parser_optional_float_and_aliases():
    parser = Parser().get_parser()
    args = parser.parse_args([
        "--outside_option_util", "None",
        "--quit_threshold", "None",
        "--algo_name", "Hindsight",
    ])
    assert args.outside_option_util is None
    assert args.quit_threshold is None
    assert args.algo_name == "Hindsight"
    assert parser.parse_args(["--algo_name", "Foresight"]).algo_name == "Foresight"


def test_menu_choice_can_disable_outside_option():
    customer = Customer(Location(0.0, 0.0, 1, 0), -0.25, 3.2, 30.0, 1)
    choice = make_choice(outside_option_util=None)
    result = choice.customerchoice_menu(customer, [make_offer(is_home=True)])
    assert result.outcome == "accepted_home"


def test_legacy_choice_uses_passenger_exit_utility():
    customer = Customer(Location(0.0, 0.0, 1, 0), -0.25, 3.2, 30.0, 1)
    choice = make_choice(service_mode="home_only", outside_option_util=1e9)
    result = choice.customerchoice_offer(customer, [], [])
    assert result.outcome == "opted_out"


def test_exact_service_modes_filter_menu_choices():
    customer = Customer(Location(0.0, 0.0, 1, 0), -0.25, 3.2, 30.0, 1)
    home = make_offer(is_home=True)
    ooh = make_offer(is_home=False)
    assert make_choice("home_only", None).customerchoice_menu(customer, [home, ooh]).outcome == "accepted_home"
    assert make_choice("ooh_only", None).customerchoice_menu(customer, [home, ooh]).outcome == "accepted_meeting_point"


def test_zero_failure_cost_objective():
    config = SimpleNamespace(driver_wage=30.0, fuel_cost=0.6, home_failure=0.0, failure_cost=20.0)
    base = total_costs(
        count_home=10,
        service_times=100.0,
        travel_time=200.0,
        discount_costs=[-5.0],
        charge_revenue=[2.0],
        config=config,
    )
    config.failure_cost = 0.0
    assert base == total_costs(10, 100.0, 200.0, [-5.0], [2.0], config)


def test_runner_includes_dspo_menu_with_menu_mode():
    assert "DSPO_Menu" in STRATEGIES
    overrides = strategy_overrides("DSPO_Menu")
    assert overrides["algo_name"] == "DSPO_Menu"
    assert overrides["menu_mode"] is True
    assert overrides["menu_eta_filter_mode"] == "none"
    args = akkerman_base_args(0, "test", outside_option_util=0.0)
    assert args["outside_option_util"] == 0.0


def write_raw(path):
    rows = [
        {
            "strategy": "NoOOH",
            "seed": 0,
            "home_delivery": 1.0,
            "travel_costs": 10.0,
            "service_costs": 5.0,
            "failure_costs": 0.0,
            "discount_costs": 0.0,
            "charge_revenue": 0.0,
            "avg_discount": 0.0,
            "avg_charge": 0.0,
            "total_costs": 15.0,
            "log_path": "noooh.log",
        },
        {
            "strategy": "OnlyOOH",
            "seed": 0,
            "home_delivery": 0.0,
            "travel_costs": 8.0,
            "service_costs": 0.0,
            "failure_costs": 0.0,
            "discount_costs": 0.0,
            "charge_revenue": 0.0,
            "avg_discount": 0.0,
            "avg_charge": 0.0,
            "total_costs": 8.0,
            "log_path": "onlyooh.log",
        },
        {
            "strategy": "DSPO_Menu",
            "seed": 0,
            "home_delivery": 0.4,
            "travel_costs": 7.0,
            "service_costs": 2.0,
            "failure_costs": 0.0,
            "discount_costs": 1.0,
            "charge_revenue": 3.0,
            "avg_discount": 1.0,
            "avg_charge": 2.0,
            "total_costs": 7.0,
            "log_path": "dspo_menu.log",
        },
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=RAW_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def test_summary_analyzer_contract():
    with TemporaryDirectory() as tmp:
        raw = Path(tmp) / "raw.csv"
        write_raw(raw)
        summary_json = analyze(raw)
        text = summary_json.read_text(encoding="utf-8")
        assert '"failure_cost": 0' in text
        assert '"outside_option_util": null' in text
        assert '"strategy": "DSPO_Menu"' in text
        assert '"passed": true' in text


def test_numeric_outside_option_disables_exact_baseline_gates_only():
    rows = [
        {
            "strategy": "NoOOH",
            "seed": 0,
            "home_delivery": 0.2,
            "travel_costs": 10.0,
            "service_costs": 5.0,
            "failure_costs": 0.0,
            "discount_costs": 0.0,
            "charge_revenue": 0.0,
            "avg_discount": 0.0,
            "avg_charge": 0.0,
            "total_costs": 15.0,
            "log_path": "noooh.log",
        },
        {
            "strategy": "OnlyOOH",
            "seed": 0,
            "home_delivery": 0.2,
            "travel_costs": 8.0,
            "service_costs": 0.0,
            "failure_costs": 0.0,
            "discount_costs": 0.0,
            "charge_revenue": 0.0,
            "avg_discount": 0.0,
            "avg_charge": 0.0,
            "total_costs": 8.0,
            "log_path": "onlyooh.log",
        },
    ]
    gates = acceptance_gates(rows, summarize_rows(rows), outside_option_util=0.0)
    assert gates["exact_baseline_gates_enabled"] is False
    assert gates["passed"] is True


def main():
    tests = [
        test_parser_optional_float_and_aliases,
        test_menu_choice_can_disable_outside_option,
        test_legacy_choice_uses_passenger_exit_utility,
        test_exact_service_modes_filter_menu_choices,
        test_zero_failure_cost_objective,
        test_runner_includes_dspo_menu_with_menu_mode,
        test_summary_analyzer_contract,
        test_numeric_outside_option_disables_exact_baseline_gates_only,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} Akkerman RC no-failure tests")


if __name__ == "__main__":
    main()
