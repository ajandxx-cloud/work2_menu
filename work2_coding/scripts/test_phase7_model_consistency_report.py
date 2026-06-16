import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.model_consistency_report import write_phase7_model_consistency_report  # noqa: E402


REQUIRED_SECTIONS = {
    "mnl_contract",
    "method_family_contract",
    "optout_accounting",
    "row_schema",
    "artifact_gates",
    "manuscript_alignment",
    "verification",
    "downstream_handoff",
}


def test_report_writes_json_and_markdown():
    with TemporaryDirectory() as tmp:
        report = write_phase7_model_consistency_report(tmp)
        json_path = Path(report["reports"]["json"])
        md_path = Path(report["reports"]["markdown"])
        assert json_path.exists()
        assert md_path.exists()
        loaded = json.loads(json_path.read_text(encoding="utf-8"))
        assert loaded["schema_version"] == "phase7-model-consistency-v1"
        assert REQUIRED_SECTIONS.issubset(set(loaded["sections"]))


def test_report_contracts_are_passed_or_explicit():
    with TemporaryDirectory() as tmp:
        report = write_phase7_model_consistency_report(tmp)
        assert report["sections"]["mnl_contract"]["status"] == "passed"
        assert report["sections"]["method_family_contract"]["status"] == "passed"
        assert report["sections"]["optout_accounting"]["status"] == "passed"
        assert report["sections"]["row_schema"]["status"] == "passed"
        assert report["sections"]["artifact_gates"]["status"] == "passed"
        assert report["sections"]["manuscript_alignment"]["status"] == "passed"
        for section in report["sections"].values():
            for item in section.get("blockers", []):
                assert item["reason"]
                assert item["minimal_fix"]
                assert item["rerun_command"]
                assert item["evidence_location"]


def test_downstream_handoff_does_not_assert_target_ranking():
    with TemporaryDirectory() as tmp:
        report = write_phase7_model_consistency_report(tmp)
        handoff = report["sections"]["downstream_handoff"]
        assert handoff["status"] == "handoff"
        text = json.dumps(report, sort_keys=True)
        assert "target ranking was not asserted" in text
        assert "phase10_dspo_plus_full_run_pending" in text


def main():
    tests = [
        test_report_writes_json_and_markdown,
        test_report_contracts_are_passed_or_explicit,
        test_downstream_handoff_does_not_assert_target_ranking,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} Phase 7 model consistency report tests")


if __name__ == "__main__":
    main()
