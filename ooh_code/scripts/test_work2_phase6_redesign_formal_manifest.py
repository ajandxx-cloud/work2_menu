from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "experiments" / "studies" / "work2_phase6_redesign_formal.yaml"

EXPECTED_SPLITS = ["seed0", "seed1", "seed2", "seed3", "seed4"]
REQUIRED_TAGS = [
    "nearest_L",
    "cost_L",
    "cnn_menu",
    "expected_profit_enumeration",
    "service_constrained_expected_profit",
    "risk_lambda_200",
    "risk_lambda_400",
    "min_quit_tol000",
    "min_quit_tol001",
    "min_quit_tol003",
    "cost_oracle",
    "profit_oracle",
]
FORMAL_CANDIDATE_TAGS = {
    "risk_lambda_200",
    "risk_lambda_400",
    "min_quit_tol000",
    "min_quit_tol001",
    "min_quit_tol003",
}
NON_ORACLE_BASELINE_TAGS = {"nearest_L", "cost_L", "cnn_menu"}
LEGACY_DIAGNOSTIC_TAGS = {
    "expected_profit_enumeration",
    "service_constrained_expected_profit",
}
ORACLE_TAGS = {"cost_oracle", "profit_oracle"}


def _assert(condition, message):
    if not condition:
        raise AssertionError(message)


def _load_manifest():
    with MANIFEST_PATH.open("r", encoding="utf-8") as handle:
        manifest = yaml.safe_load(handle)
    _assert(isinstance(manifest, dict), "manifest must be a mapping")
    return manifest


def test_identity_and_budget(manifest):
    _assert(
        manifest.get("name") == "work2_phase6_redesign_formal",
        "manifest name must be work2_phase6_redesign_formal",
    )
    base_args = manifest.get("base_args", {})
    expected_args = {
        "experiment_name": "work2_phase6_redesign_formal",
        "instance": "RC",
        "max_episodes": 150,
        "eval_episodes": 50,
        "candidate_meeting_points": 10,
        "max_candidates": 10,
        "menu_k": 3,
        "menu_objective_mode": "system_profit",
        "menu_selection_solver": "exact",
    }
    for key, expected in expected_args.items():
        observed = base_args.get(key)
        _assert(observed == expected, f"base_args.{key} expected {expected}, got {observed}")

    gate = manifest.get("behavior_gate", {})
    _assert(gate.get("min_acceptance_rate") == 0.05, "min acceptance gate mismatch")
    _assert(gate.get("max_acceptance_rate") == 1.00, "max acceptance gate mismatch")
    _assert(gate.get("max_opt_out_rate") == 0.90, "opt-out gate mismatch")

    checkpoint = base_args.get("cnn_aux_checkpoint")
    _assert(isinstance(checkpoint, str) and checkpoint.strip(), "cnn_aux_checkpoint must be a non-empty string")
    checkpoint_path = ROOT / checkpoint
    print(f"INFO cnn_aux_checkpoint={checkpoint} exists={checkpoint_path.exists()}")


def test_policy_contract(manifest):
    policies = manifest.get("policies", [])
    observed_tags = [policy.get("tag") for policy in policies]
    _assert(observed_tags == REQUIRED_TAGS, f"unexpected policy order/tags: {observed_tags}")
    observed_set = set(observed_tags)

    _assert(
        "service_guarded_diagnostic" not in observed_set,
        "service_guarded_diagnostic must remain absent from the formal policy tags",
    )
    _assert(
        observed_set & FORMAL_CANDIDATE_TAGS == FORMAL_CANDIDATE_TAGS,
        f"formal candidates missing: {FORMAL_CANDIDATE_TAGS - observed_set}",
    )
    _assert(
        {tag for tag in observed_tags if tag in FORMAL_CANDIDATE_TAGS} == FORMAL_CANDIDATE_TAGS,
        "formal candidate tags must be exactly the accepted Phase 6B winners",
    )
    _assert(
        {tag for tag in observed_tags if tag in NON_ORACLE_BASELINE_TAGS} == NON_ORACLE_BASELINE_TAGS,
        "non-oracle baselines must be nearest_L, cost_L, and cnn_menu",
    )
    _assert(
        {tag for tag in observed_tags if tag in LEGACY_DIAGNOSTIC_TAGS} == LEGACY_DIAGNOSTIC_TAGS,
        "legacy expected-profit diagnostics must remain present",
    )
    _assert(
        not (FORMAL_CANDIDATE_TAGS & LEGACY_DIAGNOSTIC_TAGS),
        "legacy diagnostics must not be formal candidates",
    )
    _assert(
        {tag for tag in observed_tags if tag in ORACLE_TAGS} == ORACLE_TAGS,
        "cost_oracle and profit_oracle must remain diagnostic references",
    )
    _assert(
        not (FORMAL_CANDIDATE_TAGS & ORACLE_TAGS),
        "oracle references must not be formal candidates",
    )

    by_tag = {policy["tag"]: policy for policy in policies}
    _assert(
        by_tag["risk_lambda_200"].get("args_overrides", {}).get("menu_outside_penalty_lambda") == 200.0,
        "risk_lambda_200 must keep lambda=200",
    )
    _assert(
        by_tag["risk_lambda_400"].get("args_overrides", {}).get("menu_outside_penalty_lambda") == 400.0,
        "risk_lambda_400 must keep lambda=400",
    )
    _assert(
        by_tag["min_quit_tol000"].get("args_overrides", {}).get("menu_quit_tolerance") == 0.0,
        "min_quit_tol000 must keep tolerance 0.00",
    )
    _assert(
        by_tag["min_quit_tol001"].get("args_overrides", {}).get("menu_quit_tolerance") == 0.01,
        "min_quit_tol001 must keep tolerance 0.01",
    )
    _assert(
        by_tag["min_quit_tol003"].get("args_overrides", {}).get("menu_quit_tolerance") == 0.03,
        "min_quit_tol003 must keep tolerance 0.03",
    )
    _assert(
        by_tag["profit_oracle"].get("args_overrides", {}).get("menu_use_oracle_eta") is True,
        "profit_oracle must keep oracle ETA enabled",
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


def test_description_contract():
    text = MANIFEST_PATH.read_text(encoding="utf-8")
    _assert("winning redesign families" in text, "description should document redesign winner reuse")
    _assert("human confirmation was given" in text, "description should document the gate prerequisite")


def main():
    manifest = _load_manifest()
    test_identity_and_budget(manifest)
    test_policy_contract(manifest)
    test_split_contract(manifest)
    test_description_contract()
    print(
        "PASS work2_phase6_redesign_formal manifest: redesign-aligned five-seed RC formal "
        "budget and policy contract."
    )


if __name__ == "__main__":
    main()
