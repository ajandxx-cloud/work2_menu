import copy
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.baseline_validation import (  # noqa: E402
    MAIN_BASELINE_TAGS,
    synthetic_completed_rows,
    validate_phase8_baseline_rows,
    write_phase8_baseline_validation_report,
)


def _codes(report):
    return {failure["code"] for failure in report["failures"]}


def test_completed_paired_rows_pass_baseline_gate_but_not_claim_ready():
    rows, manifest = synthetic_completed_rows()
    report = validate_phase8_baseline_rows(rows, manifest=manifest, study_summary={"tier": "formal"})
    assert report["baseline_validation_status"] == "passed"
    assert report["phase9_release_gate"] == "open"
    assert report["claim_ready"] is False
    assert report["claim_ready_status"] == "blocked"
    assert report["main_baseline_tags"] == list(MAIN_BASELINE_TAGS)


def test_missing_static_split_blocks():
    rows, manifest = synthetic_completed_rows()
    rows = [row for row in rows if not (
        row["split_id"] == manifest["splits"][0]["split_id"]
        and row["policy_tag"] == "phase8_static_flat_markdown"
    )]
    report = validate_phase8_baseline_rows(rows, manifest=manifest)
    assert report["baseline_validation_status"] == "blocked"
    assert "missing_main_baseline_pair" in _codes(report)


def test_failed_or_placeholder_row_blocks():
    rows, manifest = synthetic_completed_rows()
    rows[0]["status"] = "failed"
    rows[0]["execution_status"] = "failed"
    rows[0]["error_type"] = "SyntheticFailure"
    rows[0]["error_message"] = "boom"
    rows[1]["placeholder_only"] = True
    report = validate_phase8_baseline_rows(rows, manifest=manifest)
    assert "row_not_completed" in _codes(report)
    assert "placeholder_row" in _codes(report)


def test_bad_checkpoint_blocks():
    rows, manifest = synthetic_completed_rows()
    rows[0]["checkpoint_load_status"] = "failed"
    rows[0]["checkpoint_hash"] = None
    report = validate_phase8_baseline_rows(rows, manifest=manifest)
    assert "checkpoint_not_loaded" in _codes(report)
    assert "missing_checkpoint_hash" in _codes(report)


def test_missing_provenance_blocks():
    rows, manifest = synthetic_completed_rows()
    rows[0]["settings_hash"] = ""
    rows[1]["trace_hash"] = ""
    report = validate_phase8_baseline_rows(rows, manifest=manifest)
    assert "missing_settings_hash" in _codes(report)
    assert "missing_trace_hash" in _codes(report)


def test_paired_drift_blocks():
    rows, manifest = synthetic_completed_rows()
    first_split = manifest["splits"][0]["split_id"]
    for row in rows:
        if row["split_id"] == first_split and row["policy_tag"] == "phase8_static_flat_markdown":
            row["trace_hash"] = "different"
            row["menu_k"] = 5
    report = validate_phase8_baseline_rows(rows, manifest=manifest)
    assert "paired_field_drift" in _codes(report)


def test_invalid_accounting_blocks():
    rows, manifest = synthetic_completed_rows()
    rows[0]["count_accepted_home"] += rows[0]["count_opted_out"]
    report = validate_phase8_baseline_rows(rows, manifest=manifest)
    assert "accepted_count_mismatch" in _codes(report)


def test_report_writes_json_and_markdown_from_run_dir():
    rows, manifest = synthetic_completed_rows()
    with TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "studies" / "phase8_baseline_validation" / "run"
        run_dir.mkdir(parents=True)
        (run_dir / "normalized_rows.json").write_text(json.dumps(rows), encoding="utf-8")
        (run_dir / "study_summary.json").write_text(
            json.dumps({"study_name": "phase8_baseline_validation", "tier": "formal", "run_id": "run"}),
            encoding="utf-8",
        )
        (run_dir / "manifest_snapshot.yaml").write_text("name: phase8_baseline_validation\n", encoding="utf-8")
        report = write_phase8_baseline_validation_report(output_root=Path(tmp) / "report", run_dir=run_dir)
        assert Path(report["reports"]["json"]).exists()
        assert Path(report["reports"]["markdown"]).exists()
        text = Path(report["reports"]["markdown"]).read_text(encoding="utf-8")
        assert "target ranking was not asserted" in text
        assert "Baseline validation" in text


def test_missing_run_writes_blocked_report():
    with TemporaryDirectory() as tmp:
        report = write_phase8_baseline_validation_report(
            output_root=Path(tmp) / "report",
            studies_root=Path(tmp) / "missing",
        )
        assert report["baseline_validation_status"] == "blocked"
        assert "no_rows" in _codes(report)


def test_every_failure_has_repair_fields():
    rows, manifest = synthetic_completed_rows()
    broken = copy.deepcopy(rows)
    broken[0]["checkpoint_load_status"] = "failed"
    report = validate_phase8_baseline_rows(broken, manifest=manifest)
    for failure in report["failures"]:
        assert failure["reason"]
        assert failure["minimal_fix"]
        assert failure["rerun_command"]
        assert failure["evidence_location"]


def main():
    tests = [
        test_completed_paired_rows_pass_baseline_gate_but_not_claim_ready,
        test_missing_static_split_blocks,
        test_failed_or_placeholder_row_blocks,
        test_bad_checkpoint_blocks,
        test_missing_provenance_blocks,
        test_paired_drift_blocks,
        test_invalid_accounting_blocks,
        test_report_writes_json_and_markdown_from_run_dir,
        test_missing_run_writes_blocked_report,
        test_every_failure_has_repair_fields,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} Phase 8 baseline validation tests")


if __name__ == "__main__":
    main()
