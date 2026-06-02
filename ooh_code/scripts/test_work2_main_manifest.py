from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "experiments" / "studies" / "work2_main.yaml"

CORE_POLICIES = [
    ("nearest_L", "Nearest-L", "nearest_heuristic"),
    ("cost_L", "Cost-L heuristic", "cost_l_heuristic"),
    ("cnn_menu", "CNN-Menu", "top_k_cheapest"),
    ("mlp_menu", "MLP-Menu", "menu_optimization"),
    ("cnn_setmenu_net", "CNN-SetMenuNet", "menu_optimization"),
    ("oracle_menu", "Oracle Menu", "menu_optimization"),
]

EXPECTED_SPLITS = ["seed0", "seed1", "seed2"]


def _assert(condition, message):
    if not condition:
        raise AssertionError(message)


def _load_manifest():
    with MANIFEST_PATH.open("r", encoding="utf-8") as handle:
        manifest = yaml.safe_load(handle)
    _assert(isinstance(manifest, dict), "manifest must be a mapping")
    return manifest


def test_policy_contract(manifest):
    policies = manifest.get("policies", [])
    observed = [
        (policy.get("tag"), policy.get("label"), policy.get("policy"))
        for policy in policies
    ]
    _assert(
        observed == CORE_POLICIES,
        f"expected core policies {CORE_POLICIES}, got {observed}",
    )

    by_tag = {policy["tag"]: policy for policy in policies}
    _assert(
        by_tag["mlp_menu"].get("args_overrides", {}).get("menu_model") == "mlp_menu",
        "MLP-Menu must evaluate the mlp_menu model path",
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


def test_budget_and_candidate_contract(manifest):
    base_args = manifest.get("base_args", {})
    expected_args = {
        "instance": "RC",
        "max_episodes": 80,
        "eval_episodes": 20,
        "max_candidates": 10,
        "menu_k": 3,
    }
    for key, expected in expected_args.items():
        observed = base_args.get(key)
        _assert(observed == expected, f"base_args.{key} expected {expected}, got {observed}")

    text = MANIFEST_PATH.read_text(encoding="utf-8")
    _assert("home is always shown outside L" in text, "manifest must document home outside public L")
    _assert("candidate_slots = K + 1" in text, "manifest must document home-first K+1 tensors")
    _assert("formal 150-300/50 episode evidence remains" in text, "manifest must separate pilot and formal budgets")


def main():
    manifest = _load_manifest()
    test_policy_contract(manifest)
    test_split_contract(manifest)
    test_budget_and_candidate_contract(manifest)
    print(
        "PASS work2_main manifest: "
        "6 core methods, seed0..seed2, train/test split 0/1, K=10, L=3, 80/20 pilot."
    )


if __name__ == "__main__":
    main()
