from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "experiments" / "studies" / "work2_formal_main.yaml"

REQUIRED_POLICIES = [
    ("nearest_L", "Nearest-L", "nearest_heuristic"),
    ("cost_L", "Cost-L heuristic", "cost_l_heuristic"),
    ("cnn_menu", "CNN-Menu", "top_k_cheapest"),
    ("mlp_menu", "MLP-Menu", "menu_optimization"),
    ("setmenu_net", "SetMenuNet", "menu_optimization"),
    ("cnn_setmenu_net", "CNN-SetMenuNet", "menu_optimization"),
    ("oracle_menu", "Oracle Menu", "menu_optimization"),
]

EXPECTED_SPLITS = ["seed0", "seed1", "seed2", "seed3", "seed4"]


def _assert(condition, message):
    if not condition:
        raise AssertionError(message)


def _load_manifest():
    with MANIFEST_PATH.open("r", encoding="utf-8") as handle:
        manifest = yaml.safe_load(handle)
    _assert(isinstance(manifest, dict), "manifest must be a mapping")
    return manifest


def test_identity_and_budget(manifest):
    _assert(manifest.get("name") == "work2_formal_main", "manifest name must be work2_formal_main")
    base_args = manifest.get("base_args", {})
    expected_args = {
        "experiment_name": "work2_formal_main",
        "instance": "RC",
        "max_episodes": 150,
        "eval_episodes": 50,
        "max_candidates": 10,
        "menu_k": 3,
    }
    for key, expected in expected_args.items():
        observed = base_args.get(key)
        _assert(observed == expected, f"base_args.{key} expected {expected}, got {observed}")
    _assert(base_args.get("max_episodes") != 300, "300/50 must not be the default formal budget")


def test_policy_contract(manifest):
    policies = manifest.get("policies", [])
    observed = [
        (policy.get("tag"), policy.get("label"), policy.get("policy"))
        for policy in policies
    ]
    _assert(observed == REQUIRED_POLICIES, f"expected policies {REQUIRED_POLICIES}, got {observed}")

    by_tag = {policy["tag"]: policy for policy in policies}
    _assert(
        by_tag["mlp_menu"].get("args_overrides", {}).get("menu_model") == "mlp_menu",
        "MLP-Menu must evaluate the mlp_menu model path",
    )
    _assert(
        by_tag["setmenu_net"].get("args_overrides", {}).get("menu_model") == "mlp_menu",
        "SetMenuNet must route through the stable set-menu-capable learned path",
    )
    _assert(
        by_tag["cnn_setmenu_net"].get("args_overrides", {}).get("menu_model") == "cnn_setmenu",
        "CNN-SetMenuNet must evaluate the cnn_setmenu model path",
    )
    _assert(
        by_tag["oracle_menu"].get("args_overrides", {}).get("menu_use_oracle_eta") is True,
        "Oracle Menu must keep oracle ETA enabled",
    )


def test_split_contract(manifest):
    splits = manifest.get("splits", [])
    observed_ids = [split.get("id") for split in splits]
    _assert(observed_ids == EXPECTED_SPLITS, f"expected splits {EXPECTED_SPLITS}, got {observed_ids}")

    for index, split in enumerate(splits):
        _assert(split.get("train_split") == 0, f"{split.get('id')} must use train_split=0")
        _assert(split.get("test_split") == 1, f"{split.get('id')} must use test_split=1")
        seed = split.get("args_overrides", {}).get("seed")
        _assert(seed == index, f"{split.get('id')} must use seed={index}, got {seed}")


def test_semantic_comments():
    text = MANIFEST_PATH.read_text(encoding="utf-8")
    _assert("home is always shown outside L" in text, "manifest must document home outside public L")
    _assert("candidate_slots = K + 1" in text, "manifest must document home-first K+1 tensors")
    _assert("300/50 is" in text, "manifest must document that 300/50 is diagnostic escalation only")
    _assert("Home only" not in text, "Home only is optional and must not be a required formal method")
    _assert("Full-candidate CNN" not in text, "Full-candidate CNN is optional and must not be a required formal method")


def main():
    manifest = _load_manifest()
    test_identity_and_budget(manifest)
    test_policy_contract(manifest)
    test_split_contract(manifest)
    test_semantic_comments()
    print(
        "PASS work2_formal_main manifest: seven required methods, "
        "seed0..seed4, train/test split 0/1, K=10, L=3, 150/50 formal pass."
    )


if __name__ == "__main__":
    main()
