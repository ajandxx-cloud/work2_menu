import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.artifact_builder import build_artifacts  # noqa: E402
from Src.artifact_status import classify_artifact, collect_environment_provenance  # noqa: E402
from Src.experiment_contracts import load_manifest, manifest_hash  # noqa: E402
from Src.paired_replay import build_normalized_row, resolve_paired_settings  # noqa: E402
from Src.study_execution import collect_git_provenance  # noqa: E402


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


def synthetic_run(root, study="pilot_robust_menu", rows=None, summary_updates=None):
    manifest = load_manifest(study)
    mh = manifest_hash(manifest)
    run_dir = Path(root) / manifest["name"] / "synthetic-run"
    if rows is None:
        rows = synthetic_rows(manifest, mh)
    summary = {
        "study_name": manifest["name"],
        "tier": manifest["tier"],
        "run_mode": manifest["run_mode"],
        "run_id": "synthetic-run",
        "run_dir": str(run_dir),
        "manifest_hash": mh,
        "execution_status": "completed",
        "placeholder_only": False,
        "row_count": len(rows),
        "policy_tags": sorted({row["policy_tag"] for row in rows}),
        "split_ids": sorted({row["split_id"] for row in rows}),
        "uptake_regimes": sorted({row["uptake_regime"] for row in rows}),
        "checkpoint_statuses": sorted({row["checkpoint_load_status"] for row in rows}),
        "git_provenance": collect_git_provenance(),
        "blockers": [],
    }
    if summary_updates:
        summary.update(summary_updates)
    write_json(run_dir / "normalized_rows.json", rows)
    write_json(run_dir / "study_summary.json", summary)
    (run_dir / "manifest_snapshot.yaml").write_text("name: " + manifest["name"] + "\n", encoding="utf-8")
    return run_dir, rows, summary


def synthetic_rows(manifest, mh, placeholder=False, bad_checkpoint=False):
    rows = []
    provenance = collect_git_provenance()
    for setting in resolve_paired_settings(manifest, manifest_hash_value=mh)[:4]:
        checkpoint_status = "failed" if bad_checkpoint else ("loaded" if setting["args"].get("require_checkpoint") else "not_requested")
        rows.append(
            build_normalized_row(
                setting,
                run_id="synthetic-run",
                checkpoint_metadata={
                    "checkpoint_load_status": checkpoint_status,
                    "checkpoint_path": setting["args"].get("checkpoint_path", ""),
                    "checkpoint_hash": "abc123" if checkpoint_status == "loaded" else None,
                    "checkpoint_required": bool(setting["args"].get("require_checkpoint")),
                    "checkpoint_intentional_mismatch": False,
                },
                stats_metadata={
                    "acceptance_rate": 0.8,
                    "optout_rate": 0.2,
                    "count_opted_out": 2,
                    "count_accepted_home": 3,
                    "count_accepted_meeting_point": 5,
                },
                menu_metadata={
                    "eta_filter_mode": setting["args"].get("menu_eta_filter_mode"),
                    "effective_menu_policy": setting["args"].get("menu_policy"),
                    "menu_selection_solver_effective": "greedy",
                    "menu_build_time": 0.02,
                    "relative_optimality_gap": 0.0,
                },
                provenance_metadata=provenance,
                status="contract_only" if placeholder else "completed",
                execution_status="contract_only" if placeholder else "completed",
                placeholder_only=placeholder,
            )
        )
    return rows


def test_claim_ready_synthetic_pilot_rows():
    manifest = load_manifest("pilot_robust_menu")
    rows = synthetic_rows(manifest, manifest_hash(manifest))
    status = classify_artifact(rows, {"tier": "pilot", "execution_status": "completed"})
    assert status["status"] == "claim_ready"
    assert status["claim_ready"] is True


def test_placeholder_rows_are_not_claim_ready():
    manifest = load_manifest("smoke_robust_menu")
    rows = synthetic_rows(manifest, manifest_hash(manifest), placeholder=True)
    status = classify_artifact(rows, {"tier": "smoke", "execution_status": "contract_only"})
    assert status["status"] == "incomplete"
    assert status["claim_ready"] is False
    assert "placeholder_only" in " ".join(status["reasons"])


def test_bad_checkpoint_blocks_pilot_claim_ready():
    manifest = load_manifest("pilot_robust_menu")
    rows = synthetic_rows(manifest, manifest_hash(manifest), bad_checkpoint=True)
    status = classify_artifact(rows, {"tier": "pilot", "execution_status": "completed"})
    assert status["status"] == "blocked"
    assert any("checkpoint" in reason for reason in status["reasons"])


def test_diagnostic_run_mode_is_not_claim_ready():
    manifest = load_manifest("diagnostic_actual_menu")
    rows = synthetic_rows(manifest, manifest_hash(manifest))
    status = classify_artifact(rows, {"tier": "smoke", "run_mode": "diagnostic", "execution_status": "completed"})
    assert status["status"] == "diagnostic"
    assert status["claim_ready"] is False
    assert any("diagnostic run mode" in reason for reason in status["reasons"])


def test_formal_claim_ready_requires_dependency_snapshot():
    manifest = load_manifest("formal_robust_menu")
    rows = synthetic_rows(manifest, manifest_hash(manifest))
    status = classify_artifact(rows, {"tier": "formal", "execution_status": "completed"}, claim_ready_requested=True)
    assert status["status"] == "blocked"
    assert any("dependency snapshot" in reason for reason in status["reasons"])
    ok = classify_artifact(
        rows,
        {"tier": "formal", "execution_status": "completed"},
        claim_ready_requested=True,
        dependency_snapshot=collect_environment_provenance(include_freeze=False),
    )
    assert ok["status"] == "claim_ready"


def test_no_filter_excluded_from_recommended_ranking():
    with TemporaryDirectory() as tmp:
        run_dir, _, _ = synthetic_run(Path(tmp) / "runs")
        build_artifacts(run_dir, output_root=Path(tmp) / "artifacts", allow_incomplete=True)
        ranking = json.loads(((Path(tmp) / "artifacts" / "aggregates" / "recommended_policy_ranking.json").read_text(encoding="utf-8")))
        assert ranking
        assert all(row["policy_tag"] != "no_filter_diagnostic" for row in ranking)
        assert all(row["policy_tag"] != "home_only" for row in ranking)
        policy_summary = json.loads(((Path(tmp) / "artifacts" / "aggregates" / "policy_summary.json").read_text(encoding="utf-8")))
        home_only = [row for row in policy_summary if row["policy_tag"] == "home_only"][0]
        assert home_only["cost_bound"] is True
        assert home_only["rank_eligible"] is False


def test_sidecar_and_dirty_git_provenance_are_recorded():
    with TemporaryDirectory() as tmp:
        run_dir, _, _ = synthetic_run(Path(tmp) / "runs")
        build_artifacts(run_dir, output_root=Path(tmp) / "artifacts", allow_incomplete=True)
        sidecar = Path(tmp) / "artifacts" / "tables" / "policy_summary.tex.metadata.json"
        assert sidecar.exists()
        data = json.loads(sidecar.read_text(encoding="utf-8"))
        assert data["source_run_id"] == "synthetic-run"
        assert "git_dirty" in data["git_provenance"]
        assert data["uptake_regimes"]


def main():
    tests = [
        test_claim_ready_synthetic_pilot_rows,
        test_placeholder_rows_are_not_claim_ready,
        test_bad_checkpoint_blocks_pilot_claim_ready,
        test_diagnostic_run_mode_is_not_claim_ready,
        test_formal_claim_ready_requires_dependency_snapshot,
        test_no_filter_excluded_from_recommended_ranking,
        test_sidecar_and_dirty_git_provenance_are_recorded,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} artifact gate tests")


if __name__ == "__main__":
    main()
