import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.experiment_contracts import load_manifest, resolve_policy_args  # noqa: E402
from Src.paired_replay import build_normalized_row, resolve_paired_settings  # noqa: E402


STUDY = "phase9_exact_greedy_tractability"
EXPECTED_SCALE_VALUES = {"8", "12", "16"}
SHARED_FIELDS = [
    "seed",
    "data_seed",
    "data_seed_test",
    "instance",
    "load_data",
    "pricing",
    "checkpoint_path",
    "require_checkpoint",
    "allow_checkpoint_mismatch",
    "hgs_reopt_time",
    "hgs_final_time",
    "reopt",
    "menu_k",
    "max_steps_r",
    "max_steps_p",
    "n_vehicles",
    "veh_capacity",
    "home_util",
    "base_util",
    "incentive_sens",
]


def _manifest():
    return load_manifest(STUDY)


def _groups(manifest):
    groups = defaultdict(list)
    for split in manifest["splits"]:
        groups[split["paired_group_id"]].append(split)
    return groups


def test_manifest_loads_single_adaptive_policy_and_claim_boundary():
    manifest = _manifest()
    assert manifest["name"] == STUDY
    assert manifest["tier"] == "formal"
    assert manifest["run_mode"] == "diagnostic"
    assert manifest["output_intent"] == "diagnostic_provisional_blocked"
    assert manifest["claim_ready"] is False
    assert manifest["required_policy_tags"] == ["mainline_optimized_adaptive"]
    assert [policy["tag"] for policy in manifest["policies"]] == ["mainline_optimized_adaptive"]


def test_fifteen_splits_and_five_paired_groups():
    manifest = _manifest()
    groups = _groups(manifest)
    assert len(manifest["splits"]) == 15
    assert len(groups) == 5
    for group_id, splits in groups.items():
        assert {str(split["solver_scale_value"]) for split in splits} == EXPECTED_SCALE_VALUES, group_id
        assert {split["solver_scale_variant"] for split in splits} == {
            "small_exact_8",
            "large_fallback_12",
            "large_fallback_16",
        }


def test_scale_settings_and_threshold_fallback_contract():
    manifest = _manifest()
    policy = manifest["policies"][0]
    for split in manifest["splits"]:
        args = resolve_policy_args(manifest, split, policy)
        assert args["menu_k"] == 3
        assert args["menu_exact_threshold"] == 8
        assert args["menu_exact_gap_threshold"] == 8
        assert args["menu_selection_solver"] == "exact"
        if split["solver_scale_variant"] == "small_exact_8":
            assert args["max_candidates"] == 8
            assert args["max_candidates"] == args["menu_exact_threshold"]
        else:
            assert args["max_candidates"] in {12, 16}
            assert args["max_candidates"] > args["menu_exact_threshold"]


def test_paired_groups_preserve_replay_fairness_except_solver_scale():
    manifest = _manifest()
    policy = manifest["policies"][0]
    for group_id, splits in _groups(manifest).items():
        resolved = [resolve_policy_args(manifest, split, policy) for split in splits]
        baseline = resolved[0]
        for args in resolved[1:]:
            for field in SHARED_FIELDS:
                assert args.get(field) == baseline.get(field), (group_id, field)
        assert {args["max_candidates"] for args in resolved} == {8, 12, 16}
        assert {args["menu_selection_solver"] for args in resolved} == {"exact"}


def test_checkpoint_contract_and_output_schema_candidate_count():
    manifest = _manifest()
    assert manifest["shared_checkpoint"]["required"] is True
    assert manifest["shared_checkpoint"]["expected_status"] == "loaded"
    assert manifest["base_args"]["checkpoint_path"] == manifest["shared_checkpoint"]["path"]
    assert manifest["base_args"]["require_checkpoint"] is True
    assert manifest["base_args"]["allow_checkpoint_mismatch"] is False
    assert "solver_candidate_count" in manifest["output_schema"]["fields"]


def test_resolved_rows_preserve_solver_candidate_count():
    manifest = _manifest()
    setting = resolve_paired_settings(manifest)[0]
    row = build_normalized_row(
        setting,
        run_id="phase9-contract",
        checkpoint_metadata={
            "checkpoint_load_status": "loaded",
            "checkpoint_path": "outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt",
            "checkpoint_hash": "synthetic-hash",
            "checkpoint_required": True,
            "checkpoint_intentional_mismatch": False,
        },
        stats_metadata={
            "count_opted_out": 1,
            "count_accepted_home": 2,
            "count_accepted_meeting_point": 3,
        },
        menu_metadata={
            "menu_selection_solver_effective": "exact",
            "solver_candidate_count": 8,
            "exact_enumerated_menu_count": 56,
            "relative_optimality_gap": 0.0,
            "menu_overlap_rate": 1.0,
            "menu_build_time": 0.01,
            "solver_fallback_reason": "",
        },
        status="completed",
        execution_status="completed",
        placeholder_only=False,
    )
    assert row["solver_candidate_count"] == 8
    assert row["checkpoint_load_status"] == "loaded"


def main():
    tests = [
        test_manifest_loads_single_adaptive_policy_and_claim_boundary,
        test_fifteen_splits_and_five_paired_groups,
        test_scale_settings_and_threshold_fallback_contract,
        test_paired_groups_preserve_replay_fairness_except_solver_scale,
        test_checkpoint_contract_and_output_schema_candidate_count,
        test_resolved_rows_preserve_solver_candidate_count,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} Phase 9 exact-greedy contract tests")


if __name__ == "__main__":
    main()
