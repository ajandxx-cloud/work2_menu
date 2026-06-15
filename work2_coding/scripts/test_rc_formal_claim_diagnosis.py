import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import diagnose_rc_formal_claims as diag  # noqa: E402


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


def make_row(split_id, regime, policy_tag, net_profit, optout_rate=0.2):
    return {
        "split_id": split_id,
        "uptake_regime": regime,
        "policy_tag": policy_tag,
        "status": "completed",
        "execution_status": "completed",
        "checkpoint_load_status": "loaded",
        "checkpoint_hash": "checkpoint-hash",
        "placeholder_only": False,
        "net_profit": net_profit,
        "operational_cost": 1000.0 - net_profit,
        "total_cost": 1000.0 - net_profit,
        "acceptance_rate": 0.7,
        "served_rate": 0.7,
        "optout_rate": optout_rate,
        "home_share": 0.5,
        "meeting_point_uptake_rate": 0.2,
        "service_time_total": 1000.0 - net_profit,
    }


def mini_bundle(root):
    run_dir = Path(root) / "formal-run"
    rows = []
    split_specs = [
        ("split-low-0", "low", 10.0),
        ("split-low-1", "low", 12.0),
        ("split-low-2", "low", 14.0),
        ("split-medium-0", "medium", 20.0),
        ("split-medium-1", "medium", 22.0),
    ]
    for split_id, regime, base_profit in split_specs:
        for index, policy in enumerate(diag.POLICY_TAGS):
            optout = 0.3 if regime == "low" else 0.1
            rows.append(make_row(split_id, regime, policy, base_profit + index, optout_rate=optout))
    summary = {
        "execution_status": "completed",
        "row_count": 35,
        "policy_tags": list(diag.POLICY_TAGS),
        "checkpoint_statuses": ["loaded"],
        "placeholder_only": False,
        "run_id": "unit-formal",
        "run_dir": str(run_dir),
    }
    readiness = {
        "status": "blocked",
        "claim_ready_allowed": False,
        "blockers": [{"code": "dirty_git", "message": "dirty tree", "severity": "blocking"}],
    }
    artifact = {
        "artifact_status": {"status": "blocked", "reasons": ["missing metadata"]},
        "claim_ready": False,
        "formal_claim_ready": False,
    }
    guard = {
        "claim_ready": False,
        "artifact_status": "blocked",
        "blocked_claims": [{"id": "empirical_superiority"}],
    }
    write_json(run_dir / "study_summary.json", summary)
    write_json(run_dir / "normalized_rows.json", rows)
    write_json(Path(root) / "readiness.json", readiness)
    write_json(Path(root) / "artifact.json", artifact)
    write_json(Path(root) / "guard.json", guard)
    return run_dir, Path(root) / "readiness.json", Path(root) / "artifact.json", Path(root) / "guard.json"


def test_paired_difference_direction_and_regime_grouping():
    rows = [
        make_row("s1", "low", "mainline_optimized_adaptive", 15.0, optout_rate=0.10),
        make_row("s1", "low", "mainline_random_menu", 10.0, optout_rate=0.20),
    ]
    for policy in diag.POLICY_TAGS:
        if policy not in {"mainline_optimized_adaptive", "mainline_random_menu"}:
            rows.append(make_row("s1", "low", policy, 9.0, optout_rate=0.25))
    paired = diag._paired_diffs(rows)
    profit = [row for row in paired if row["baseline_policy"] == "mainline_random_menu" and row["metric"] == "net_profit"][0]
    optout = [row for row in paired if row["baseline_policy"] == "mainline_random_menu" and row["metric"] == "optout_rate"][0]
    assert profit["diff_adaptive_minus_baseline"] == 5.0
    assert profit["direction"] == "adaptive_better"
    assert optout["diff_adaptive_minus_baseline"] == -0.1
    assert optout["direction"] == "adaptive_better"
    assert profit["uptake_regime"] == "low"


def test_blocker_propagation_and_no_confidence_interval_language():
    with TemporaryDirectory() as tmp:
        run_dir, readiness, artifact, guard = mini_bundle(tmp)
        out_dir = Path(tmp) / "out"
        result = diag.run(run_dir, readiness, artifact, guard, out_dir)
        markdown = Path(result["diagnostic_tables"]).read_text(encoding="utf-8")
        assert "dirty_git" in markdown
        assert "empirical_superiority" in markdown
        assert "Confidence intervals are intentionally omitted" in markdown
        assert "95%" not in markdown
        paired_csv = Path(result["paired_diffs"]).read_text(encoding="utf-8")
        assert "mainline_random_menu" in paired_csv
        assert "split-low" in paired_csv
        assert "split-medium" in paired_csv


def test_validation_rejects_bad_checkpoint_status():
    with TemporaryDirectory() as tmp:
        run_dir, readiness, artifact, guard = mini_bundle(tmp)
        rows = json.loads((run_dir / "normalized_rows.json").read_text(encoding="utf-8"))
        rows[0]["checkpoint_load_status"] = "failed"
        write_json(run_dir / "normalized_rows.json", rows)
        try:
            diag.run(run_dir, readiness, artifact, guard, Path(tmp) / "out")
        except ValueError as exc:
            assert "checkpoint_load_status" in str(exc)
            return
        raise AssertionError("bad checkpoint status should be rejected")


def main():
    tests = [
        test_paired_difference_direction_and_regime_grouping,
        test_blocker_propagation_and_no_confidence_interval_language,
        test_validation_rejects_bad_checkpoint_status,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} RC formal claim diagnosis tests")


if __name__ == "__main__":
    main()
