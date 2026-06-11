import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import torch

import Src.config  # noqa: F401
from Environments.OOH.containers import Location, MenuOffer, ServiceBundle
from Src.parser import Parser
from Src.Utils.option_features import build_option_tensor, normalize_features
from Src.Utils.Predictors import CNN_2d, LinReg
from Src.Utils.Utils import MemoryBuffer


def test_parser_menu_contract():
    parser = Parser().get_parser()
    args = parser.parse_args([
        "--algo_name", "DSPO_Menu",
        "--menu_mode", "True",
        "--menu_eta_filter_mode", "chance_constraint",
    ])
    assert args.algo_name == "DSPO_Menu"
    assert args.menu_mode is True
    assert args.menu_eta_filter_mode == "chance_constraint"
    assert args.menu_selection_solver == "auto"
    assert args.menu_exact_threshold > 0


def test_menu_containers():
    home = Location(0.0, 0.0, 1, 0)
    bundle = ServiceBundle(
        bundle_id="home",
        location=home,
        is_home=True,
        parcelpoint_id=-1,
        window_start=0.0,
        window_end=600.0,
        window_center=300.0,
        window_width=600.0,
        remaining_capacity=1000000.0,
    )
    offer = MenuOffer(bundle=bundle, predicted_cost=1.5)
    assert offer.bundle_id == "home"
    assert offer.is_home is True
    assert offer.location is home
    assert offer.parcelpoint_id == -1
    assert offer.window == (0.0, 600.0)


def test_option_features():
    raw = {
        "walk_distance": [0.0, 300.0],
        "predicted_ivt": [600.0, 900.0],
        "remaining_capacity": [1000000.0, 4.0],
        "distance_to_destination": [600.0, 900.0],
        "option_type": [1.0, 0.0],
        "arrival_time": [3300.0, 3600.0],
    }
    normed = normalize_features(raw, menu_time_scale=3600.0, menu_target_arrival_time=3600.0)
    features, mask = build_option_tensor(normed, max_k=4, device=torch.device("cpu"))
    assert tuple(features.shape) == (4, 6)
    assert tuple(mask.shape) == (4,)
    assert mask.tolist() == [True, True, False, False]


def test_predictor_contracts():
    legacy_cnn = CNN_2d(11, 2, 16, 0.05)
    legacy_lin = LinReg(242)
    menu_cnn = CNN_2d(11, 2, 16, 0.05, aux_dim=4, output_dim=3)
    menu_lin = LinReg(242, aux_dim=4, output_dim=3)

    x = torch.zeros((2, 2, 11, 11), dtype=torch.float32)
    cap = torch.ones(2, dtype=torch.float32)
    aux = torch.ones((2, 4), dtype=torch.float32)
    assert tuple(legacy_cnn(x, cap).shape) == (2, 1)
    assert tuple(legacy_lin(x, cap).shape) == (2, 1)
    assert tuple(menu_cnn(x, aux).shape) == (2, 3)
    assert tuple(menu_lin(x, aux).shape) == (2, 3)


def test_memory_buffer_contract():
    config = SimpleNamespace(device=torch.device("cpu"))
    buffer = MemoryBuffer(
        max_len=4,
        time_intervals=2,
        matrix_dim=3,
        target_dim=3,
        atype=torch.float32,
        config=config,
        aux_dim=4,
    )
    features = torch.zeros((2, 18), dtype=torch.float32).numpy()
    aux = [[1.0, 2.0, 3.0, 4.0], [5.0, 6.0, 7.0, 8.0]]
    target = [[9.0, 10.0, 11.0], [12.0, 13.0, 14.0]]
    buffer.add(features, aux, target)
    feat, cap_feat, sampled = buffer.sample(2)
    assert feat.shape[1:] == (2, 3, 3)
    assert cap_feat.shape[1] == 4
    assert sampled.shape[1] == 3


def main():
    tests = [
        test_parser_menu_contract,
        test_menu_containers,
        test_option_features,
        test_predictor_contracts,
        test_memory_buffer_contract,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} menu runtime contract tests")


if __name__ == "__main__":
    main()
