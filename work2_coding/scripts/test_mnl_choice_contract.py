import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Environments.OOH.containers import Customer, Location, MenuOffer, ServiceBundle  # noqa: E402
from Environments.OOH.customerchoice import customerchoicemodel  # noqa: E402
from Src.experiment_contracts import load_manifest, manifest_hash  # noqa: E402
from Src.paired_replay import build_normalized_row, resolve_paired_settings, validate_normalized_row  # noqa: E402
from Src.parser import Parser  # noqa: E402


def make_offer():
    loc = Location(2.0, 2.0, 1, 0)
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
    return MenuOffer(bundle=bundle, predicted_cost=1.0, price=0.0, predicted_utility=0.0)


def first_setting():
    manifest = load_manifest("smoke_robust_menu")
    return resolve_paired_settings(manifest, manifest_hash_value=manifest_hash(manifest))[0]


def test_parser_default_outside_utility_is_zero():
    args = Parser().get_parser().parse_args([])
    assert args.outside_option_util == 0.0


def test_parser_accepts_none_to_disable_outside_option():
    args = Parser().get_parser().parse_args(["--outside_option_util", "None"])
    assert args.outside_option_util is None


def test_high_outside_utility_forces_menu_optout():
    model = customerchoicemodel(
        base_util=-2.0,
        dist_scaler=10.0,
        euclidean=lambda a, b: 1.0,
        dist_mat=[],
        n_cust=1,
        outside_option_util=1e9,
    )
    customer = Customer(Location(0.0, 0.0, 10, 0), -0.25, 3.2, 30.0, 10)
    result = model.customerchoice_menu(customer, [make_offer()])
    assert result.outcome == "opted_out"
    assert result.route_mutates is False


def test_normalized_row_records_outside_utility():
    setting = first_setting()
    row = build_normalized_row(
        setting,
        run_id="synthetic-run",
        stats_metadata={
            "count_opted_out": 1,
            "count_accepted_home": 2,
            "count_accepted_meeting_point": 3,
        },
        placeholder_only=True,
    )
    assert "outside_option_util" in row
    assert row["outside_option_util"] == 0.0


def test_completed_rows_cannot_omit_outside_utility_field():
    setting = first_setting()
    row = build_normalized_row(
        setting,
        run_id="synthetic-run",
        stats_metadata={
            "count_opted_out": 1,
            "count_accepted_home": 2,
            "count_accepted_meeting_point": 3,
        },
        status="completed",
        execution_status="completed",
        placeholder_only=False,
    )
    row.pop("outside_option_util")
    try:
        validate_normalized_row(row)
    except ValueError as exc:
        assert "outside_option_util" in str(exc)
        return
    raise AssertionError("completed row without outside_option_util should fail validation")


def main():
    tests = [
        test_parser_default_outside_utility_is_zero,
        test_parser_accepts_none_to_disable_outside_option,
        test_high_outside_utility_forces_menu_optout,
        test_normalized_row_records_outside_utility,
        test_completed_rows_cannot_omit_outside_utility_field,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} MNL choice contract tests")


if __name__ == "__main__":
    main()
