import copy
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.experiment_contracts import load_manifest, load_suite, manifest_hash, suite_members  # noqa: E402
from Src.paired_replay import build_normalized_row, resolve_paired_settings  # noqa: E402
from Src.sensitivity_analysis import (  # noqa: E402
    ALLOWED_AXES,
    SensitivityValidationError,
    annotate_rows,
    build_sensitivity_artifacts,
    load_sensitivity_run,
    validate_sensitivity_rows,
    write_sensitivity_summary,
)


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


def write_baseline_report(path, status="passed"):
    report = {
        "schema_version": "phase8-baseline-validation-v1",
        "baseline_validation_status": status,
        "phase9_release_gate": "open" if status == "passed" else "blocked",
        "claim_ready": False,
        "claim_ready_status": "blocked",
        "run_id": "synthetic-baseline",
        "failures": [] if status == "passed" else [{"code": "synthetic_blocked", "reason": "blocked baseline"}],
    }
    write_json(path, report)
    return path


def _split_for_setting(manifest, setting):
    return [split for split in manifest["splits"] if split["split_id"] == setting["split_id"]][0]


def _numeric_value(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        mapping = {
            "hard": 0.0,
            "interval_overlap": 1.0,
            "chance_constraint": 2.0,
            "low": 0.0,
            "medium": 1.0,
        }
        return mapping.get(str(value), 0.0)


def synthetic_rows_for_manifest(manifest, run_id):
    mh = manifest_hash(manifest)
    rows = []
    for idx, setting in enumerate(resolve_paired_settings(manifest, manifest_hash_value=mh)):
        split = _split_for_setting(manifest, setting)
        score = _numeric_value(split.get("sensitivity_value")) + (idx % 5) * 0.01
        rows.append(
            build_normalized_row(
                setting,
                run_id=run_id,
                checkpoint_metadata={
                    "checkpoint_load_status": "loaded",
                    "checkpoint_path": setting["args"].get("checkpoint_path", ""),
                    "checkpoint_hash": "phase8-synthetic-checkpoint",
                    "checkpoint_required": True,
                    "checkpoint_intentional_mismatch": False,
                },
                stats_metadata={
                    "count_opted_out": 1 + int(score) % 2,
                    "count_accepted_home": 4,
                    "count_accepted_meeting_point": 5,
                    "net_price_revenue": 100.0 + score,
                    "operational_cost": 40.0 + score / 2.0,
                    "service_time_total": 35.0 + score / 3.0,
                },
                menu_metadata={
                    "eta_filter_mode": setting["args"].get("menu_eta_filter_mode"),
                    "effective_menu_policy": setting["args"].get("menu_policy"),
                    "menu_selection_solver_effective": "greedy",
                    "menu_build_time": 0.02 + idx * 0.001,
                    "menu_utilization": 0.75,
                    "relative_optimality_gap": 0.0,
                },
                provenance_metadata={
                    "git_commit": "synthetic",
                    "git_dirty": False,
                    "git_status_summary": "",
                },
                status="completed",
                execution_status="completed",
                placeholder_only=False,
            )
        )
    return rows


def write_sensitivity_run(studies_root, study_name, manifest=None):
    manifest = copy.deepcopy(manifest or load_manifest(study_name))
    run_id = "synthetic-" + study_name
    rows = synthetic_rows_for_manifest(manifest, run_id)
    run_dir = Path(studies_root) / study_name / run_id
    summary = {
        "study_name": study_name,
        "tier": manifest["tier"],
        "run_mode": manifest["run_mode"],
        "run_id": run_id,
        "manifest_hash": manifest_hash(manifest),
        "execution_status": "completed",
        "placeholder_only": False,
        "row_count": len(rows),
        "git_provenance": {
            "git_commit": "synthetic",
            "git_dirty": False,
            "git_status_summary": "",
        },
    }
    write_json(run_dir / "normalized_rows.json", rows)
    write_json(run_dir / "study_summary.json", summary)
    manifest_for_yaml = copy.deepcopy(manifest)
    manifest_for_yaml.pop("_path", None)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "manifest_snapshot.yaml").write_text(
        yaml.safe_dump(manifest_for_yaml, sort_keys=False),
        encoding="utf-8",
    )
    return run_dir


def write_all_sensitivity_runs(studies_root):
    suite = load_suite("phase8_sensitivity_must_have")
    for study_name in suite_members(suite):
        write_sensitivity_run(studies_root, study_name)


def _assert_raises_validation(rows, manifests, code):
    try:
        validate_sensitivity_rows(rows, manifests, strict=True, require_full_suite=False)
    except SensitivityValidationError as exc:
        assert code in {failure["code"] for failure in exc.failures}
        return
    raise AssertionError("expected sensitivity validation failure: " + code)


def test_missing_baseline_report_creates_blocked_summary():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        result = write_sensitivity_summary(
            studies_root=root / "studies",
            baseline_report=root / "missing" / "PHASE8_BASELINE_VALIDATION.json",
            artifact_root=root / "artifacts",
            planning_output=root / "SENSITIVITY_SUMMARY.md",
        )
        artifact_result = result["artifact_result"]
        assert artifact_result["builder_status"] == "blocked"
        assert artifact_result["baseline_validation_status"] == "missing"
        text = (root / "SENSITIVITY_SUMMARY.md").read_text(encoding="utf-8")
        assert "diagnostic_provisional_blocked" in text
        assert "claim_ready: false" in text
        assert "Sensitivity replay interpretation is blocked" in text


def test_blocked_baseline_prevents_sensitivity_interpretation():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_all_sensitivity_runs(root / "studies")
        baseline = write_baseline_report(root / "baseline" / "PHASE8_BASELINE_VALIDATION.json", status="blocked")
        result = build_sensitivity_artifacts(
            studies_root=root / "studies",
            baseline_report=baseline,
            output_root=root / "artifacts",
        )
        assert result["builder_status"] == "blocked"
        assert result["baseline_validation_status"] == "blocked"
        assert not (root / "artifacts" / "aggregates" / "sensitivity_axis_summary.json").exists()


def test_completed_synthetic_rows_generate_artifacts_and_summary():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_all_sensitivity_runs(root / "studies")
        baseline = write_baseline_report(root / "baseline" / "PHASE8_BASELINE_VALIDATION.json")
        result = build_sensitivity_artifacts(
            studies_root=root / "studies",
            baseline_report=baseline,
            output_root=root / "artifacts",
        )
        assert result["builder_status"] == "completed"
        aggregate_json = root / "artifacts" / "aggregates" / "sensitivity_axis_summary.json"
        aggregate_csv = root / "artifacts" / "aggregates" / "sensitivity_axis_summary.csv"
        assert aggregate_json.exists()
        assert aggregate_csv.exists()
        assert (root / "artifacts" / "tables" / "sensitivity_axis_summary.tex").exists()
        assert (root / "artifacts" / "tables" / "sensitivity_boundary_map.tex").exists()
        assert (root / "artifacts" / "figures" / "profit_service_tradeoff.png").exists()
        assert (root / "artifacts" / "figures" / "optout_acceptance_by_axis.png").exists()
        assert Path(str(aggregate_json) + ".metadata.json").exists()
        aggregates = json.loads(aggregate_json.read_text(encoding="utf-8"))
        assert {row["sensitivity_axis"] for row in aggregates} == set(ALLOWED_AXES)
        assert all(row["claim_ready"] is False for row in aggregates)

        summary = write_sensitivity_summary(
            studies_root=root / "studies",
            baseline_report=baseline,
            artifact_root=root / "artifacts",
            planning_output=root / "SENSITIVITY_SUMMARY.md",
        )
        text = Path(summary["summary_path"]).read_text(encoding="utf-8")
        assert "diagnostic_provisional_blocked" in text
        assert "claim_ready: false" in text
        for axis in ALLOWED_AXES:
            assert axis in text
        for deferred in ["max_candidates", "fleet_capacity_stress", "pricing_bounds", "price_sensitivity"]:
            assert deferred in text


def test_no_filter_row_is_flagged_not_promoted():
    manifest = load_manifest("phase8_sensitivity_eta_filter")
    rows = synthetic_rows_for_manifest(manifest, "synthetic-no-filter")
    run_data = {
        "run_dir": Path("synthetic"),
        "rows": rows,
        "summary": {"study_name": manifest["name"], "run_id": "synthetic-no-filter"},
        "manifest": manifest,
    }
    annotated = annotate_rows(run_data)
    annotated[0]["filter_mode"] = "none"
    _assert_raises_validation(annotated, {manifest["name"]: manifest}, "no_filter_main_row")


def test_bad_chance_constraint_threshold_fails():
    manifest = copy.deepcopy(load_manifest("phase8_sensitivity_eta_filter"))
    for split in manifest["splits"]:
        if split["sensitivity_value"] == "chance_constraint":
            split["args_overrides"]["menu_eta_chance_threshold"] = 0.30
    rows = synthetic_rows_for_manifest(manifest, "synthetic-bad-threshold")
    run_data = {
        "run_dir": Path("synthetic"),
        "rows": rows,
        "summary": {"study_name": manifest["name"], "run_id": "synthetic-bad-threshold"},
        "manifest": manifest,
    }
    annotated = annotate_rows(run_data)
    _assert_raises_validation(annotated, {manifest["name"]: manifest}, "bad_chance_constraint_threshold")


def test_guardrail_manifest_varying_one_field_fails():
    manifest = copy.deepcopy(load_manifest("phase8_sensitivity_guardrail"))
    manifest["guardrail_fields"] = ["service_quit_rate_guardrail"]
    manifest["sensitivity_contract"]["guardrail_fields"] = ["service_quit_rate_guardrail"]
    for split in manifest["splits"]:
        split["args_overrides"].pop("menu_optout_guardrail", None)
    rows = synthetic_rows_for_manifest(manifest, "synthetic-bad-guardrail")
    run_data = {
        "run_dir": Path("synthetic"),
        "rows": rows,
        "summary": {"study_name": manifest["name"], "run_id": "synthetic-bad-guardrail"},
        "manifest": manifest,
    }
    annotated = annotate_rows(run_data)
    _assert_raises_validation(annotated, {manifest["name"]: manifest}, "guardrail_fields_incomplete")


def main():
    tests = [
        test_missing_baseline_report_creates_blocked_summary,
        test_blocked_baseline_prevents_sensitivity_interpretation,
        test_completed_synthetic_rows_generate_artifacts_and_summary,
        test_no_filter_row_is_flagged_not_promoted,
        test_bad_chance_constraint_threshold_fails,
        test_guardrail_manifest_varying_one_field_fails,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} Phase 8 sensitivity summary tests")


if __name__ == "__main__":
    main()
