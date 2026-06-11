import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.attention_artifacts import attention_claim_guard, attention_pair_deltas, build_attention_artifacts
from Src.experiment_contracts import load_manifest, manifest_hash
from Src.paired_replay import annotate_attention_pair_completeness, build_normalized_row, resolve_paired_settings
from Src.study_execution import collect_git_provenance


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


def attention_settings(study="pilot_attention_dspo"):
    manifest = load_manifest(study)
    settings = resolve_paired_settings(manifest, manifest_hash_value=manifest_hash(manifest))
    first_split = settings[0]["split_id"]
    return manifest, [setting for setting in settings if setting["split_id"] == first_split]


def synthetic_attention_rows(
    study="pilot_attention_dspo",
    placeholder=False,
    bad_checkpoint=False,
    missing_attention=False,
    attention_delta=2.0,
    service_delta=1.0,
):
    manifest, settings = attention_settings(study)
    rows = []
    provenance = collect_git_provenance()
    for setting in settings:
        if missing_attention and setting["policy_tag"] == "DSPO_attention":
            continue
        is_attention = setting["policy_tag"] == "DSPO_attention"
        checkpoint_status = "failed" if bad_checkpoint else ("loaded" if setting["args"].get("require_checkpoint") else "not_requested")
        objective = 10.0 + (attention_delta if is_attention else 0.0)
        service_time = 100.0 + (service_delta if is_attention else 0.0)
        rows.append(
            build_normalized_row(
                setting,
                run_id="synthetic-attention-run",
                checkpoint_metadata={
                    "checkpoint_load_status": checkpoint_status,
                    "checkpoint_path": setting["args"].get("checkpoint_path", ""),
                    "checkpoint_hash": "abc123" if checkpoint_status == "loaded" else None,
                    "checkpoint_required": bool(setting["args"].get("require_checkpoint")),
                    "checkpoint_intentional_mismatch": False,
                },
                stats_metadata={
                    "acceptance_rate": 0.8 + (0.01 if is_attention else 0.0),
                    "optout_rate": 0.2 - (0.01 if is_attention else 0.0),
                    "meeting_point_uptake_rate": 0.4 + (0.02 if is_attention else 0.0),
                    "count_opted_out": 1,
                    "count_accepted_home": 2,
                    "count_accepted_meeting_point": 4,
                    "net_price_revenue": 50.0 + (attention_delta if is_attention else 0.0),
                    "service_time_total": service_time,
                    "net_objective_proxy": objective,
                },
                menu_metadata={
                    "eta_filter_mode": setting["args"].get("menu_eta_filter_mode"),
                    "effective_menu_policy": setting["args"].get("menu_policy"),
                    "menu_selection_solver_effective": "exact",
                    "attention_weight_summary": {"attention_weight_mean": 0.7 if is_attention else 0.5},
                },
                provenance_metadata=provenance,
                status="contract_only" if placeholder else "completed",
                execution_status="contract_only" if placeholder else "completed",
                placeholder_only=placeholder,
            )
        )
    annotate_attention_pair_completeness(rows)
    return manifest, rows


def synthetic_run(root, study="pilot_attention_dspo", rows=None, summary_updates=None):
    manifest = load_manifest(study)
    run_dir = Path(root) / manifest["name"] / "synthetic-attention-run"
    rows = rows if rows is not None else synthetic_attention_rows(study)[1]
    summary = {
        "study_name": manifest["name"],
        "tier": manifest["tier"],
        "run_mode": manifest["run_mode"],
        "run_id": "synthetic-attention-run",
        "run_dir": str(run_dir),
        "manifest_hash": manifest_hash(manifest),
        "execution_status": "completed",
        "placeholder_only": any(bool(row.get("placeholder_only")) for row in rows),
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


def guard_for(rows, summary=None):
    deltas = attention_pair_deltas(rows)
    return attention_claim_guard(rows, deltas, summary=summary or {"run_id": "synthetic"})


def test_claim_ready_pilot_positive_delta():
    _, rows = synthetic_attention_rows()
    guard = guard_for(rows)
    assert guard["attention_improves_dspo_allowed"] is True
    assert guard["primary_metric"]["delta_mean"] > 0.0
    assert guard["pair_completeness"]["all_pairs_complete"] is True


def test_smoke_only_blocks_improvement_claim():
    _, rows = synthetic_attention_rows(study="smoke_attention_dspo")
    guard = guard_for(rows)
    assert guard["attention_improves_dspo_allowed"] is False
    assert any(blocker["code"] == "smoke_only" for blocker in guard["blockers"])


def test_missing_pair_blocks_claim():
    _, rows = synthetic_attention_rows(missing_attention=True)
    guard = guard_for(rows)
    assert guard["attention_improves_dspo_allowed"] is False
    assert any(blocker["code"] == "incomplete_pairs" for blocker in guard["blockers"])


def test_bad_checkpoint_blocks_pilot_claim():
    _, rows = synthetic_attention_rows(bad_checkpoint=True)
    guard = guard_for(rows)
    assert guard["attention_improves_dspo_allowed"] is False
    assert any(blocker["code"] == "checkpoint_invalid" for blocker in guard["blockers"])


def test_placeholder_rows_block_claim():
    _, rows = synthetic_attention_rows(study="smoke_attention_dspo", placeholder=True)
    guard = guard_for(rows)
    assert guard["attention_improves_dspo_allowed"] is False
    assert any(blocker["code"] == "placeholder_rows" for blocker in guard["blockers"])


def test_negative_primary_delta_blocks_claim():
    _, rows = synthetic_attention_rows(attention_delta=-1.0)
    guard = guard_for(rows)
    assert guard["attention_improves_dspo_allowed"] is False
    assert any(blocker["code"] == "primary_metric_not_positive" for blocker in guard["blockers"])


def test_material_service_degradation_blocks_claim():
    _, rows = synthetic_attention_rows(service_delta=20.0)
    guard = guard_for(rows)
    assert guard["attention_improves_dspo_allowed"] is False
    assert any(
        blocker["code"] == "service_constraint_failed" and blocker.get("metric") == "service_time_total"
        for blocker in guard["blockers"]
    )


def test_builder_writes_outputs_and_mirror_for_incomplete_smoke():
    with TemporaryDirectory() as tmp:
        _, rows = synthetic_attention_rows(study="smoke_attention_dspo", placeholder=True)
        run_dir, _, _ = synthetic_run(Path(tmp) / "runs", study="smoke_attention_dspo", rows=rows)
        result = build_attention_artifacts(
            run_dir,
            output_root=Path(tmp) / "artifacts",
            mirror_root=Path(tmp) / "mirror",
            allow_incomplete=True,
        )
        guard_path = Path(result["claim_guard_path"])
        assert guard_path.exists()
        assert (Path(tmp) / "artifacts" / "paired_deltas" / "attention_pair_deltas.json").exists()
        assert (Path(tmp) / "artifacts" / "tables" / "attention_pair_deltas.tex").exists()
        assert (Path(tmp) / "mirror" / "ATTENTION_CLAIM_GUARD.json").exists()
        guard = json.loads(guard_path.read_text(encoding="utf-8"))
        assert guard["attention_improves_dspo_allowed"] is False


def main():
    tests = [
        test_claim_ready_pilot_positive_delta,
        test_smoke_only_blocks_improvement_claim,
        test_missing_pair_blocks_claim,
        test_bad_checkpoint_blocks_pilot_claim,
        test_placeholder_rows_block_claim,
        test_negative_primary_delta_blocks_claim,
        test_material_service_degradation_blocks_claim,
        test_builder_writes_outputs_and_mirror_for_incomplete_smoke,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} attention artifact gate tests")


if __name__ == "__main__":
    main()
