import copy
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.dspo_validation import (  # noqa: E402
    DSPO_POLICY_TAGS,
    DEFAULT_STUDY_NAME,
    markdown_report,
    validate_phase9_dspo_rows,
    write_phase9_dspo_family_validation_report,
)
from Src.experiment_contracts import load_manifest, manifest_hash  # noqa: E402
from Src.paired_replay import build_normalized_row, resolve_paired_settings  # noqa: E402


def _codes(report):
    return {failure["code"] for failure in report["failures"]}


def _synthetic_completed_rows():
    manifest = load_manifest(DEFAULT_STUDY_NAME)
    mh = manifest_hash(manifest)
    rows = []
    for index, setting in enumerate(resolve_paired_settings(manifest, manifest_hash_value=mh)):
        rows.append(
            build_normalized_row(
                setting,
                run_id="phase9-synthetic",
                checkpoint_metadata={
                    "checkpoint_load_status": "loaded",
                    "checkpoint_path": "outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt",
                    "checkpoint_hash": "phase9-checkpoint-hash",
                    "checkpoint_required": True,
                    "checkpoint_intentional_mismatch": False,
                },
                stats_metadata={
                    "count_opted_out": 1,
                    "count_accepted_home": 2,
                    "count_accepted_meeting_point": 3,
                    "net_price_revenue": 20.0 + index,
                    "operational_cost": 6.0,
                },
                status="completed",
                execution_status="completed",
                placeholder_only=False,
            )
        )
    return rows, manifest


def _phase8_reference(status="passed", supports_advantage=False):
    return {
        "baseline_validation_status": status,
        "run_id": "phase8-reference-run",
        "phase9_release_gate": "open" if status == "passed" else "blocked",
        "main_baseline_tags": ["mainline_optimized_mw", "phase8_static_flat_markdown"],
        "sanity_reference": {
            "supports_dspo_advantage": supports_advantage,
            "metrics": ["net_profit", "served_rate", "optout_rate"],
        },
    }


def test_completed_paired_dspo_rows_pass_gate_but_keep_claim_ready_separate():
    rows, manifest = _synthetic_completed_rows()
    report = validate_phase9_dspo_rows(
        rows,
        manifest=manifest,
        study_summary={"tier": "formal", "run_id": "phase9-synthetic"},
        phase8_report=_phase8_reference(),
    )
    assert report["dspo_validation_status"] == "passed"
    assert report["phase9_gate"] == "open"
    assert report["claim_ready"] is False
    assert report["claim_ready_status"] == "blocked"
    assert report["dspo_policy_tags"] == list(DSPO_POLICY_TAGS)
    assert report["main_row_count"] == 10


def test_missing_clip_or_wide_row_in_any_split_blocks():
    rows, manifest = _synthetic_completed_rows()
    rows = [
        row
        for row in rows
        if not (
            row["split_id"] == manifest["splits"][0]["split_id"]
            and row["policy_tag"] == "dspo_wide"
        )
    ]
    report = validate_phase9_dspo_rows(rows, manifest=manifest)
    assert report["dspo_validation_status"] == "blocked"
    assert "missing_dspo_pair" in _codes(report)


def test_bad_row_statuses_and_placeholder_rows_block():
    status_values = ["failed", "blocked", "incomplete", "contract_only"]
    for value in status_values:
        rows, manifest = _synthetic_completed_rows()
        rows[0]["status"] = value
        rows[0]["execution_status"] = value
        report = validate_phase9_dspo_rows(rows, manifest=manifest)
        assert "row_not_completed" in _codes(report)

    rows, manifest = _synthetic_completed_rows()
    rows[0]["placeholder_only"] = True
    report = validate_phase9_dspo_rows(rows, manifest=manifest)
    assert "placeholder_row" in _codes(report)


def test_checkpoint_provenance_row_v2_pairing_and_accounting_errors_block():
    rows, manifest = _synthetic_completed_rows()
    broken = copy.deepcopy(rows)
    broken[0]["checkpoint_load_status"] = "failed"
    broken[1]["checkpoint_path"] = ""
    broken[2]["checkpoint_hash"] = None
    broken[3]["settings_hash"] = ""
    broken[4]["trace_hash"] = ""
    broken[5]["manifest_hash"] = ""
    first_split = manifest["splits"][0]["split_id"]
    for row in broken:
        if row["split_id"] == first_split and row["policy_tag"] == "dspo_wide":
            row["trace_id"] = "drifted-trace"
    broken[6]["count_accepted_home"] += broken[6]["count_opted_out"]
    broken[7]["home_share"] = 0.99
    report = validate_phase9_dspo_rows(broken, manifest=manifest)
    codes = _codes(report)
    assert "checkpoint_not_loaded" in codes
    assert "missing_checkpoint_path" in codes
    assert "missing_checkpoint_hash" in codes
    assert "missing_settings_hash" in codes
    assert "missing_trace_hash" in codes
    assert "missing_manifest_hash" in codes
    assert "paired_field_drift" in codes
    assert "accepted_count_mismatch" in codes
    assert "invalid_home_share" in codes


def test_unexpected_phase9_policy_including_dspo_plus_blocks():
    rows, manifest = _synthetic_completed_rows()
    extra = copy.deepcopy(rows[0])
    extra["policy_tag"] = "dspo_plus_clip"
    extra["method_family"] = "DSPO_PLUS"
    rows.append(extra)
    report = validate_phase9_dspo_rows(rows, manifest=manifest)
    assert "unexpected_phase9_policy" in _codes(report)


def test_every_failure_has_repair_fields():
    rows, manifest = _synthetic_completed_rows()
    rows[0]["checkpoint_load_status"] = "failed"
    report = validate_phase9_dspo_rows(rows, manifest=manifest)
    for failure in report["failures"]:
        assert failure["reason"]
        assert failure["minimal_fix"]
        assert failure["rerun_command"]
        assert failure["evidence_location"]


def test_report_fields_sanity_status_next_step_and_dspo_plus_exclusion():
    rows, manifest = _synthetic_completed_rows()
    report = validate_phase9_dspo_rows(
        rows,
        manifest=manifest,
        study_summary={"tier": "formal", "run_id": "phase9-synthetic"},
        phase8_report=_phase8_reference(supports_advantage=False),
    )
    for field in [
        "dspo_validation_status",
        "phase9_gate",
        "claim_ready",
        "phase8_reference_run_id",
        "phase8_reference_status",
        "sanity_status",
        "next_step",
        "dspo_plus_exclusion",
    ]:
        assert field in report
    assert report["dspo_validation_status"] == "passed"
    assert report["phase8_reference_run_id"] == "phase8-reference-run"
    assert report["phase8_reference_status"] == "passed"
    assert report["sanity_status"]["supports_advantage_conclusion"] is False
    assert "status/risk" in report["next_step"]
    assert "DSPO_PLUS is unrelated/stale" in report["dspo_plus_exclusion"]


def test_markdown_report_states_sanity_is_status_only_not_ranking_conclusion():
    rows, manifest = _synthetic_completed_rows()
    report = validate_phase9_dspo_rows(rows, manifest=manifest, phase8_report=_phase8_reference())
    text = markdown_report(report)
    assert "status-only" in text
    assert "not a manuscript ranking conclusion" in text
    assert "DSPO_PLUS is unrelated/stale" in text


def test_report_writer_writes_only_json_and_markdown_from_run_dir():
    rows, _manifest = _synthetic_completed_rows()
    with TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "studies" / DEFAULT_STUDY_NAME / "run"
        run_dir.mkdir(parents=True)
        (run_dir / "normalized_rows.json").write_text(json.dumps(rows), encoding="utf-8")
        (run_dir / "study_summary.json").write_text(
            json.dumps({"study_name": DEFAULT_STUDY_NAME, "tier": "formal", "run_id": "run"}),
            encoding="utf-8",
        )
        (run_dir / "manifest_snapshot.yaml").write_text(
            Path(ROOT / "Experiments" / "studies" / "phase9_dspo_family_validation.yaml").read_text(
                encoding="utf-8"
            ),
            encoding="utf-8",
        )
        phase8_path = Path(tmp) / "phase8.json"
        phase8_path.write_text(json.dumps(_phase8_reference()), encoding="utf-8")
        report = write_phase9_dspo_family_validation_report(
            output_root=Path(tmp) / "report",
            run_dir=run_dir,
            phase8_report=phase8_path,
        )
        report_dir = Path(tmp) / "report"
        assert Path(report["reports"]["json"]).exists()
        assert Path(report["reports"]["markdown"]).exists()
        assert sorted(path.name for path in report_dir.iterdir()) == [
            "PHASE9_DSPO_FAMILY_VALIDATION.json",
            "PHASE9_DSPO_FAMILY_VALIDATION.md",
        ]


def main():
    tests = [
        test_completed_paired_dspo_rows_pass_gate_but_keep_claim_ready_separate,
        test_missing_clip_or_wide_row_in_any_split_blocks,
        test_bad_row_statuses_and_placeholder_rows_block,
        test_checkpoint_provenance_row_v2_pairing_and_accounting_errors_block,
        test_unexpected_phase9_policy_including_dspo_plus_blocks,
        test_every_failure_has_repair_fields,
        test_report_fields_sanity_status_next_step_and_dspo_plus_exclusion,
        test_markdown_report_states_sanity_is_status_only_not_ranking_conclusion,
        test_report_writer_writes_only_json_and_markdown_from_run_dir,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} Phase 9 DSPO family validation tests")


if __name__ == "__main__":
    main()
