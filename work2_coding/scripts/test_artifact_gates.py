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
from Src.study_execution import collect_git_provenance, sha256_file  # noqa: E402


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


def synthetic_readiness(root, manifest, checkpoint_hash="abc123", status="passed", git_dirty=False, manifest_hash_override=None):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    dependency_path = root / "DEPENDENCY_SNAPSHOT.json"
    write_json(dependency_path, {"schema_version": "dependency-snapshot-v1", "study": manifest["name"]})
    readiness = {
        "schema_version": "formal-readiness-v1",
        "status": status,
        "claim_ready_allowed": status == "passed",
        "blockers": [] if status == "passed" else [{"code": "blocked_test", "message": "blocked"}],
        "study": manifest["name"],
        "tier": manifest["tier"],
        "run_mode": manifest["run_mode"],
        "run_id": "synthetic-readiness",
        "manifest": {
            "path": manifest.get("_path", ""),
            "hash": manifest_hash_override or manifest_hash(manifest),
        },
        "checkpoint": {
            "load_status": "loaded" if checkpoint_hash else "failed",
            "hash": checkpoint_hash,
            "resolved_path": "synthetic/supervised_ml.pt",
        },
        "dependency_snapshot": {
            "path": str(dependency_path),
            "hash": sha256_file(dependency_path),
        },
        "git_provenance": {
            "git_commit": "synthetic",
            "git_dirty": git_dirty,
            "git_status_summary": "",
        },
    }
    readiness_path = root / "FORMAL_READINESS.json"
    write_json(readiness_path, readiness)
    return readiness_path


def synthetic_rows(manifest, mh, placeholder=False, bad_checkpoint=False, checkpoint_status=None, limit=4):
    rows = []
    provenance = collect_git_provenance()
    settings = resolve_paired_settings(manifest, manifest_hash_value=mh)
    if limit is not None:
        settings = settings[:limit]
    for setting in settings:
        row_checkpoint_status = checkpoint_status or (
            "failed" if bad_checkpoint else ("loaded" if setting["args"].get("require_checkpoint") else "not_requested")
        )
        rows.append(
            build_normalized_row(
                setting,
                run_id="synthetic-run",
                checkpoint_metadata={
                    "checkpoint_load_status": row_checkpoint_status,
                    "checkpoint_path": setting["args"].get("checkpoint_path", ""),
                    "checkpoint_hash": "abc123" if row_checkpoint_status == "loaded" else None,
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


def test_clean_smoke_rows_are_diagnostic_only():
    manifest = load_manifest("smoke_robust_menu")
    rows = synthetic_rows(manifest, manifest_hash(manifest))
    status = classify_artifact(rows, {"tier": "smoke", "execution_status": "completed"})
    assert status["status"] == "diagnostic"
    assert status["claim_ready"] is False
    assert any("smoke" in reason for reason in status["reasons"])


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


def test_failed_rows_block_claim_ready():
    manifest = load_manifest("smoke_robust_menu")
    rows = synthetic_rows(manifest, manifest_hash(manifest))
    for row in rows:
        row["status"] = "failed"
        row["execution_status"] = "failed"
        row["error_type"] = "RuntimeError"
        row["error_message"] = "boom"
    status = classify_artifact(rows, {"tier": "smoke", "execution_status": "failed"})
    assert status["status"] == "blocked"
    assert status["claim_ready"] is False
    assert any("failed rows" in reason for reason in status["reasons"])


def test_no_filter_only_rows_are_diagnostic():
    manifest = load_manifest("diagnostic_actual_menu")
    mh = manifest_hash(manifest)
    provenance = collect_git_provenance()
    setting = [
        setting
        for setting in resolve_paired_settings(manifest, manifest_hash_value=mh)
        if setting["policy_tag"] == "no_filter_diagnostic"
    ][0]
    rows = [
        build_normalized_row(
            setting,
            run_id="synthetic-run",
            checkpoint_metadata={
                "checkpoint_load_status": "not_requested",
                "checkpoint_path": "",
                "checkpoint_hash": None,
                "checkpoint_required": False,
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
                "eta_filter_mode": "none",
                "effective_menu_policy": "risk_adjusted_expected_profit",
            },
            provenance_metadata=provenance,
            status="completed",
            execution_status="completed",
            placeholder_only=False,
        )
    ]
    status = classify_artifact(rows, {"tier": "smoke", "execution_status": "completed"})
    assert status["status"] == "diagnostic"
    assert status["claim_ready"] is False


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


def test_formal_claim_ready_requires_loaded_checkpoint():
    manifest = load_manifest("formal_robust_menu")
    rows = synthetic_rows(manifest, manifest_hash(manifest), checkpoint_status="not_requested")
    status = classify_artifact(
        rows,
        {"tier": "formal", "execution_status": "completed"},
        claim_ready_requested=True,
        dependency_snapshot=collect_environment_provenance(include_freeze=False),
    )
    assert status["status"] == "blocked"
    assert any("checkpoint" in reason for reason in status["reasons"])


def test_formal_claim_ready_build_requires_readiness_json():
    with TemporaryDirectory() as tmp:
        manifest = load_manifest("formal_robust_menu")
        rows = synthetic_rows(manifest, manifest_hash(manifest))
        run_dir, _, _ = synthetic_run(Path(tmp) / "runs", study="formal_robust_menu", rows=rows)
        try:
            build_artifacts(run_dir, output_root=Path(tmp) / "artifacts", claim_ready=True)
        except ValueError as exc:
            assert "readiness JSON" in str(exc)
            return
        raise AssertionError("formal claim-ready artifacts should require readiness JSON")


def test_formal_claim_ready_blocks_bad_readiness_json():
    with TemporaryDirectory() as tmp:
        manifest = load_manifest("formal_robust_menu")
        rows = synthetic_rows(manifest, manifest_hash(manifest))
        run_dir, _, _ = synthetic_run(Path(tmp) / "runs", study="formal_robust_menu", rows=rows)
        readiness = synthetic_readiness(Path(tmp) / "readiness", manifest, status="blocked")
        try:
            build_artifacts(run_dir, output_root=Path(tmp) / "artifacts", claim_ready=True, readiness_json=readiness)
        except ValueError as exc:
            assert "status is not passed" in str(exc)
            return
        raise AssertionError("blocked formal readiness should block claim-ready artifacts")


def test_formal_claim_ready_blocks_dirty_readiness_json():
    with TemporaryDirectory() as tmp:
        manifest = load_manifest("formal_robust_menu")
        rows = synthetic_rows(manifest, manifest_hash(manifest))
        run_dir, _, _ = synthetic_run(Path(tmp) / "runs", study="formal_robust_menu", rows=rows)
        readiness = synthetic_readiness(Path(tmp) / "readiness", manifest, git_dirty=True)
        try:
            build_artifacts(run_dir, output_root=Path(tmp) / "artifacts", claim_ready=True, readiness_json=readiness)
        except ValueError as exc:
            assert "git_dirty" in str(exc)
            return
        raise AssertionError("dirty readiness should block claim-ready artifacts")


def test_formal_claim_ready_blocks_manifest_and_checkpoint_mismatches():
    with TemporaryDirectory() as tmp:
        manifest = load_manifest("formal_robust_menu")
        rows = synthetic_rows(manifest, manifest_hash(manifest))
        run_dir, _, _ = synthetic_run(Path(tmp) / "runs", study="formal_robust_menu", rows=rows)
        stale = synthetic_readiness(Path(tmp) / "stale-readiness", manifest, manifest_hash_override="stale")
        try:
            build_artifacts(run_dir, output_root=Path(tmp) / "artifacts1", claim_ready=True, readiness_json=stale)
        except ValueError as exc:
            assert "manifest hash" in str(exc)
        else:
            raise AssertionError("stale readiness manifest hash should block")

        mismatch = synthetic_readiness(Path(tmp) / "mismatch-readiness", manifest, checkpoint_hash="different")
        try:
            build_artifacts(run_dir, output_root=Path(tmp) / "artifacts2", claim_ready=True, readiness_json=mismatch)
        except ValueError as exc:
            assert "checkpoint hash" in str(exc)
            return
        raise AssertionError("checkpoint hash mismatch should block")


def test_passed_formal_readiness_allows_existing_gates_to_proceed():
    with TemporaryDirectory() as tmp:
        manifest = load_manifest("formal_robust_menu")
        rows = synthetic_rows(manifest, manifest_hash(manifest))
        run_dir, _, _ = synthetic_run(Path(tmp) / "runs", study="formal_robust_menu", rows=rows)
        readiness = synthetic_readiness(Path(tmp) / "readiness", manifest)
        result = build_artifacts(run_dir, output_root=Path(tmp) / "artifacts", claim_ready=True, readiness_json=readiness)
        assert result["artifact_status"]["claim_ready"] is True
        status = json.loads((Path(tmp) / "artifacts" / "ARTIFACT_STATUS.json").read_text(encoding="utf-8"))
        assert status["formal_readiness"]["status"] == "passed"
        assert status["formal_readiness"]["dependency_snapshot_hash"]
        sidecar = json.loads((Path(tmp) / "artifacts" / "tables" / "policy_summary.tex.metadata.json").read_text(encoding="utf-8"))
        assert sidecar["formal_readiness"]["status"] == "passed"


def test_failed_formal_row_blocks_even_when_readiness_passes():
    with TemporaryDirectory() as tmp:
        manifest = load_manifest("formal_robust_menu")
        rows = synthetic_rows(manifest, manifest_hash(manifest))
        rows[0]["status"] = "failed"
        rows[0]["execution_status"] = "failed"
        rows[0]["error_type"] = "RuntimeError"
        rows[0]["error_message"] = "boom"
        run_dir, _, _ = synthetic_run(Path(tmp) / "runs", study="formal_robust_menu", rows=rows)
        readiness = synthetic_readiness(Path(tmp) / "readiness", manifest)
        try:
            build_artifacts(run_dir, output_root=Path(tmp) / "artifacts", claim_ready=True, readiness_json=readiness)
        except ValueError as exc:
            assert "failed rows" in str(exc)
            return
        raise AssertionError("failed formal rows should block even with passed readiness")


def test_no_filter_excluded_from_recommended_ranking():
    with TemporaryDirectory() as tmp:
        run_dir, _, _ = synthetic_run(Path(tmp) / "runs", study="diagnostic_actual_menu")
        build_artifacts(run_dir, output_root=Path(tmp) / "artifacts", allow_incomplete=True)
        ranking = json.loads(((Path(tmp) / "artifacts" / "aggregates" / "recommended_policy_ranking.json").read_text(encoding="utf-8")))
        assert ranking
        assert all(row["policy_tag"] != "no_filter_diagnostic" for row in ranking)
        assert all(row["policy_tag"] != "home_only" for row in ranking)
        policy_summary = json.loads(((Path(tmp) / "artifacts" / "aggregates" / "policy_summary.json").read_text(encoding="utf-8")))
        home_only = [row for row in policy_summary if row["policy_tag"] == "home_only"][0]
        assert home_only["cost_bound"] is True
        assert home_only["rank_eligible"] is False


def test_mainline_no_menu_is_baseline_not_recommended_ranking():
    with TemporaryDirectory() as tmp:
        manifest = load_manifest("smoke_robust_menu")
        rows = synthetic_rows(manifest, manifest_hash(manifest), limit=None)
        run_dir, _, _ = synthetic_run(Path(tmp) / "runs", study="smoke_robust_menu", rows=rows)
        build_artifacts(run_dir, output_root=Path(tmp) / "artifacts", allow_incomplete=True)
        ranking = json.loads(((Path(tmp) / "artifacts" / "aggregates" / "recommended_policy_ranking.json").read_text(encoding="utf-8")))
        ranked_tags = {row["policy_tag"] for row in ranking}
        assert "mainline_no_menu" not in ranked_tags
        assert {
            "mainline_fixed_menu",
            "mainline_random_menu",
            "mainline_optimized_m",
            "mainline_optimized_mw",
            "mainline_optimized_fixed_window",
            "mainline_optimized_adaptive",
        }.issubset(ranked_tags)

        baseline = json.loads(((Path(tmp) / "artifacts" / "aggregates" / "baseline_boundary_policies.json").read_text(encoding="utf-8")))
        baseline_tags = {row["policy_tag"] for row in baseline}
        assert "mainline_no_menu" in baseline_tags
        no_menu = [row for row in baseline if row["policy_tag"] == "mainline_no_menu"][0]
        assert no_menu["baseline_boundary"] is True
        assert no_menu["rank_eligible"] is False


def test_artifact_build_writes_manuscript_frame_and_claim_guard():
    with TemporaryDirectory() as tmp:
        manifest = load_manifest("smoke_robust_menu")
        rows = synthetic_rows(manifest, manifest_hash(manifest), limit=None)
        run_dir, _, _ = synthetic_run(Path(tmp) / "runs", study="smoke_robust_menu", rows=rows)
        build_artifacts(run_dir, output_root=Path(tmp) / "artifacts", allow_incomplete=True)

        manuscript_dir = Path(tmp) / "artifacts" / "manuscript"
        expected = {
            "method_outline.md",
            "experiment_outline.md",
            "result_outline.md",
            "claim_checklist.md",
            "CLAIM_GUARD.json",
        }
        assert expected.issubset({path.name for path in manuscript_dir.iterdir()})

        guard = json.loads((manuscript_dir / "CLAIM_GUARD.json").read_text(encoding="utf-8"))
        assert guard["artifact_status"] == "diagnostic"
        assert guard["claim_ready"] is False
        assert "mainline_no_menu" not in guard.get("diagnostic_policies", [])
        checklist = (manuscript_dir / "claim_checklist.md").read_text(encoding="utf-8")
        assert "empirical_superiority" in checklist
        assert "Current artifact status is not claim-ready" in checklist


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
        test_clean_smoke_rows_are_diagnostic_only,
        test_placeholder_rows_are_not_claim_ready,
        test_bad_checkpoint_blocks_pilot_claim_ready,
        test_failed_rows_block_claim_ready,
        test_no_filter_only_rows_are_diagnostic,
        test_diagnostic_run_mode_is_not_claim_ready,
        test_formal_claim_ready_requires_dependency_snapshot,
        test_formal_claim_ready_requires_loaded_checkpoint,
        test_formal_claim_ready_build_requires_readiness_json,
        test_formal_claim_ready_blocks_bad_readiness_json,
        test_formal_claim_ready_blocks_dirty_readiness_json,
        test_formal_claim_ready_blocks_manifest_and_checkpoint_mismatches,
        test_passed_formal_readiness_allows_existing_gates_to_proceed,
        test_failed_formal_row_blocks_even_when_readiness_passes,
        test_no_filter_excluded_from_recommended_ranking,
        test_mainline_no_menu_is_baseline_not_recommended_ranking,
        test_artifact_build_writes_manuscript_frame_and_claim_guard,
        test_sidecar_and_dirty_git_provenance_are_recorded,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} artifact gate tests")


if __name__ == "__main__":
    main()
