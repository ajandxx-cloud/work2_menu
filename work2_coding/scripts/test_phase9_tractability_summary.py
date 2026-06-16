import copy
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.computational_tractability import (  # noqa: E402
    EXPECTED_SCALE_VALUES,
    TractabilityValidationError,
    aggregate_tractability_rows,
    build_tractability_artifacts,
    claim_boundary_for_aggregates,
    load_tractability_run,
    render_tractability_summary,
    validate_tractability_rows,
    write_tractability_summary,
)
from Src.experiment_contracts import load_manifest, manifest_hash  # noqa: E402


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


def write_status_gate(path, status="open"):
    payload = {
        "schema_version": "phase9-dspo-family-validation-v1",
        "phase": "09",
        "phase9_gate": status,
        "dspo_validation_status": "passed" if status == "open" else "blocked",
        "claim_ready": False,
        "claim_ready_status": "blocked",
        "run_id": "synthetic-phase9-gate",
        "failures": [] if status == "open" else [{"code": "synthetic_blocked", "reason": "blocked gate"}],
    }
    write_json(path, payload)
    return path


def _combination_count(n, k):
    total = 0
    for size in range(1, min(n, k) + 1):
        numerator = 1
        denominator = 1
        for idx in range(size):
            numerator *= n - idx
            denominator *= idx + 1
        total += numerator // denominator
    return total


def synthetic_rows(manifest=None, high_gap=False):
    manifest = copy.deepcopy(manifest or load_manifest("phase9_exact_greedy_tractability"))
    mh = manifest_hash(manifest)
    rows = []
    for idx, split in enumerate(manifest["splits"]):
        scale = str(split["solver_scale_value"])
        candidates = int(scale)
        exact = scale == "8"
        rows.append(
            {
                "schema_version": "normalized-row-v2",
                "study_name": manifest["name"],
                "run_id": "synthetic-tractability-run",
                "tier": "formal",
                "run_mode": "diagnostic",
                "policy_tag": "mainline_optimized_adaptive",
                "split_id": split["split_id"],
                "solver_scale_variant": split["solver_scale_variant"],
                "solver_scale_value": scale,
                "paired_group_id": split["paired_group_id"],
                "seed": split["seed"],
                "data_seed": split["data_seed"],
                "data_seed_test": split["data_seed_test"],
                "manifest_hash": mh,
                "settings_hash": "settings-" + split["split_id"],
                "checkpoint_load_status": "loaded",
                "checkpoint_path": manifest["shared_checkpoint"]["path"],
                "checkpoint_hash": "phase9-synthetic-checkpoint",
                "checkpoint_required": True,
                "menu_k": 3,
                "max_candidates": candidates,
                "solver_candidate_count": candidates,
                "menu_selection_solver_effective": "exact" if exact else "greedy",
                "solver_fallback_reason": "" if exact else "above_exact_threshold",
                "exact_enumerated_menu_count": _combination_count(candidates, 3) if exact else None,
                "relative_optimality_gap": 0.0 if exact else (0.2 if high_gap else 0.02 + idx * 0.0001),
                "menu_overlap_rate": 1.0 if exact else (0.3 if high_gap else 0.8),
                "menu_build_time": 0.01 * candidates + idx * 0.0001,
                "uptake_regime": split["uptake_regime"],
                "status": "completed",
                "execution_status": "completed",
                "error_type": "",
                "error_message": "",
            }
        )
    return rows


def write_tractability_run(studies_root, rows=None, manifest=None):
    manifest = copy.deepcopy(manifest or load_manifest("phase9_exact_greedy_tractability"))
    rows = rows or synthetic_rows(manifest)
    run_dir = Path(studies_root) / manifest["name"] / "synthetic-tractability-run"
    summary = {
        "study_name": manifest["name"],
        "tier": manifest["tier"],
        "run_mode": manifest["run_mode"],
        "run_id": "synthetic-tractability-run",
        "run_dir": str(run_dir),
        "manifest_hash": manifest_hash(manifest),
        "execution_status": "completed",
        "placeholder_only": False,
        "row_count": len(rows),
        "git_provenance": {
            "git_commit": "synthetic",
            "git_dirty": False,
            "git_status_summary": "",
        },
        "blockers": [],
    }
    write_json(run_dir / "normalized_rows.json", rows)
    write_json(run_dir / "study_summary.json", summary)
    manifest_for_yaml = copy.deepcopy(manifest)
    manifest_for_yaml.pop("_path", None)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "manifest_snapshot.yaml").write_text(yaml.safe_dump(manifest_for_yaml, sort_keys=False), encoding="utf-8")
    return run_dir


def _annotated_rows_from_run(run_dir):
    from Src.computational_tractability import annotate_rows

    return annotate_rows(load_tractability_run(run_dir=run_dir))


def _assert_validation_failure(rows, code):
    try:
        validate_tractability_rows(rows, strict=True)
    except TractabilityValidationError as exc:
        assert code in {failure["code"] for failure in exc.failures}
        return
    raise AssertionError("expected tractability validation failure: " + code)


def test_missing_run_produces_blocked_summary_object():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        status_gate = write_status_gate(root / "gate" / "PHASE9_DSPO_FAMILY_VALIDATION.json")
        result = write_tractability_summary(
            studies_root=root / "missing-studies",
            status_gate=status_gate,
            artifact_root=root / "artifacts",
            planning_output=root / "COMPUTATIONAL_TRACTABILITY_SUMMARY.md",
        )
        artifact_result = result["artifact_result"]
        assert artifact_result["builder_status"] == "blocked"
        assert artifact_result["claim_ready"] is False
        text = (root / "COMPUTATIONAL_TRACTABILITY_SUMMARY.md").read_text(encoding="utf-8")
        assert "claim_ready: false" in text
        assert "blocked" in text


def test_completed_synthetic_rows_generate_artifacts_and_summary():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        run_dir = write_tractability_run(root / "studies")
        status_gate = write_status_gate(root / "gate" / "PHASE9_DSPO_FAMILY_VALIDATION.json")
        result = build_tractability_artifacts(
            studies_root=root / "studies",
            status_gate=status_gate,
            output_root=root / "artifacts",
            run_dir=run_dir,
        )
        assert result["builder_status"] == "completed"
        assert result["claim_ready"] is False
        aggregate_json = root / "artifacts" / "aggregates" / "exact_greedy_tractability_summary.json"
        aggregate_csv = root / "artifacts" / "aggregates" / "exact_greedy_tractability_summary.csv"
        table = root / "artifacts" / "tables" / "exact_greedy_tractability.tex"
        assert aggregate_json.exists()
        assert aggregate_csv.exists()
        assert table.exists()
        assert Path(str(aggregate_json) + ".metadata.json").exists()
        assert (
            (root / "artifacts" / "figures" / "menu_build_time_by_candidate_count.png").exists()
            or (root / "artifacts" / "figures" / "menu_build_time_by_candidate_count.png.status.json").exists()
        )
        aggregates = json.loads(aggregate_json.read_text(encoding="utf-8"))
        assert [row["solver_scale_value"] for row in aggregates] == list(EXPECTED_SCALE_VALUES)
        assert all(row["claim_ready"] is False for row in aggregates)

        summary = render_tractability_summary(result)
        for text in [
            "claim_ready: false",
            "candidate count",
            "exact_enumerated_menu_count",
            "menu_build_time",
            "relative_optimality_gap",
            "menu_overlap_rate",
            "above_exact_threshold",
        ]:
            assert text in summary


def test_missing_scale_variant_fails_validation():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        rows = [row for row in synthetic_rows() if row["max_candidates"] != 16]
        run_dir = write_tractability_run(root / "studies", rows=rows)
        annotated = _annotated_rows_from_run(run_dir)
        _assert_validation_failure(annotated, "missing_scale_variant")


def test_completed_large_row_without_fallback_fails_validation():
    rows = synthetic_rows()
    for row in rows:
        if row["max_candidates"] == 12:
            row["solver_fallback_reason"] = ""
            break
    _assert_validation_failure(rows, "large_fallback_reason_missing")


def test_builder_preserves_aggregates_for_contract_invalid_rows():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        rows = synthetic_rows()
        for row in rows:
            if row["max_candidates"] in {12, 16}:
                row["menu_selection_solver_effective"] = "exact"
                row["solver_fallback_reason"] = ""
        run_dir = write_tractability_run(root / "studies", rows=rows)
        status_gate = write_status_gate(root / "gate" / "PHASE9_DSPO_FAMILY_VALIDATION.json")
        result = build_tractability_artifacts(
            studies_root=root / "studies",
            status_gate=status_gate,
            output_root=root / "artifacts",
            run_dir=run_dir,
        )
        assert result["builder_status"] == "blocked"
        assert result["claim_boundary"] == "blocked_diagnostic"
        aggregate_json = root / "artifacts" / "aggregates" / "exact_greedy_tractability_summary.json"
        table = root / "artifacts" / "tables" / "exact_greedy_tractability.tex"
        assert aggregate_json.exists()
        assert table.exists()
        aggregates = json.loads(aggregate_json.read_text(encoding="utf-8"))
        assert [row["solver_scale_value"] for row in aggregates] == list(EXPECTED_SCALE_VALUES)
        assert all(row["claim_boundary"] == "blocked_diagnostic" for row in aggregates)
        assert aggregates[1]["candidate_count_mean"] == 12.0


def test_completed_row_without_loaded_checkpoint_fails_validation():
    rows = synthetic_rows()
    rows[0]["checkpoint_load_status"] = "failed"
    _assert_validation_failure(rows, "completed_checkpoint_not_loaded")


def test_large_gap_or_low_overlap_narrows_claim_boundary():
    rows = synthetic_rows(high_gap=True)
    validation = validate_tractability_rows(rows, strict=True)
    assert validation["valid"] is True
    aggregates = aggregate_tractability_rows(rows)
    assert claim_boundary_for_aggregates(aggregates) == "fast_but_approximate_regime_dependent"


def test_summary_cli_writes_required_sections():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        run_dir = write_tractability_run(root / "studies")
        status_gate = write_status_gate(root / "gate" / "PHASE9_DSPO_FAMILY_VALIDATION.json")
        summary = write_tractability_summary(
            studies_root=root / "studies",
            status_gate=status_gate,
            artifact_root=root / "artifacts",
            planning_output=root / "COMPUTATIONAL_TRACTABILITY_SUMMARY.md",
            run_dir=run_dir,
        )
        text = Path(summary["summary_path"]).read_text(encoding="utf-8")
        assert "## Status Gate" in text
        assert "## 15-Row Coverage" in text
        assert "## Exact-Greedy Table" in text
        assert "## Claim Boundary" in text
        assert "## Source Artifacts" in text
        assert "No claim-ready manuscript upgrade is authorized" in text


def main():
    tests = [
        test_missing_run_produces_blocked_summary_object,
        test_completed_synthetic_rows_generate_artifacts_and_summary,
        test_missing_scale_variant_fails_validation,
        test_completed_large_row_without_fallback_fails_validation,
        test_builder_preserves_aggregates_for_contract_invalid_rows,
        test_completed_row_without_loaded_checkpoint_fails_validation,
        test_large_gap_or_low_overlap_narrows_claim_boundary,
        test_summary_cli_writes_required_sections,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} Phase 9 tractability summary tests")


if __name__ == "__main__":
    main()
