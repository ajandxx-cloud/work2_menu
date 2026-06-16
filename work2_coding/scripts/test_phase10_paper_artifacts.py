import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Src.paper_artifacts import collect_phase10_sources, write_phase10_package  # noqa: E402


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


def write_text(path, value="content\n"):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def status_payload(status, claim_ready=False, blockers=None):
    blockers = blockers or []
    return {
        "schema_version": "test-status-v1",
        "artifact_status": {
            "status": status,
            "claim_ready": claim_ready,
            "blockers": blockers,
            "checkpoint_statuses": ["loaded"],
        },
        "status": status,
        "claim_ready": claim_ready,
        "blockers": blockers,
    }


def build_source_roots(root):
    main_root = root / "work2_coding" / "artifacts" / "work2_robust_menu"
    phase8_root = main_root / "phase8_sensitivity"
    phase9_root = main_root / "phase9_tractability"
    case_root = root / ".planning" / "data" / "case_studies"
    results_root = root / ".planning" / "results"

    write_json(
        main_root / "ARTIFACT_STATUS.json",
        status_payload(
            "blocked",
            claim_ready=False,
            blockers=[{"code": "missing_checkpoint_file", "message": "checkpoint unavailable"}],
        ),
    )
    write_text(main_root / "README.md")
    write_json(main_root / "aggregates" / "policy_summary.json", [{"policy": "robust"}])
    write_text(main_root / "aggregates" / "policy_summary.csv", "policy,value\nrobust,1\n")
    write_text(main_root / "tables" / "policy_summary.tex", "\\begin{tabular}{l}x\\end{tabular}\n")
    write_json(main_root / "tables" / "policy_summary.tex.metadata.json", {"kind": "table"})
    write_json(main_root / "figures" / "profit_gap.png.status.json", {"status": "blocked"})
    write_json(main_root / "manuscript" / "CLAIM_GUARD.json", {"claim_ready": False})
    write_text(main_root / "manuscript" / "claim_checklist.md")

    write_json(phase8_root / "ARTIFACT_STATUS.json", status_payload("diagnostic", claim_ready=False))
    write_json(phase8_root / "ARTIFACT_STATUS.json.metadata.json", {"kind": "status"})
    write_json(phase8_root / "aggregates" / "sensitivity_axis_summary.json", [{"claim_ready": False}])
    write_text(phase8_root / "aggregates" / "sensitivity_axis_summary.csv", "axis,value\nmenu_k,3\n")
    write_json(phase8_root / "aggregates" / "sensitivity_axis_summary.json.metadata.json", {"kind": "aggregate"})
    write_text(phase8_root / "tables" / "sensitivity_axis_summary.tex")
    write_json(phase8_root / "tables" / "sensitivity_axis_summary.tex.metadata.json", {"kind": "table"})
    write_text(phase8_root / "figures" / "profit_service_tradeoff.png")
    write_json(phase8_root / "figures" / "profit_service_tradeoff.png.metadata.json", {"kind": "figure"})

    write_json(phase9_root / "ARTIFACT_STATUS.json", status_payload("diagnostic", claim_ready=False))
    write_json(phase9_root / "ARTIFACT_STATUS.json.metadata.json", {"kind": "status"})
    write_json(phase9_root / "aggregates" / "exact_greedy_tractability_summary.json", [{"claim_ready": False}])
    write_text(phase9_root / "aggregates" / "exact_greedy_tractability_summary.csv", "scale,value\n8,0.0\n")
    write_text(phase9_root / "tables" / "exact_greedy_tractability.tex")
    write_json(phase9_root / "tables" / "exact_greedy_tractability.tex.metadata.json", {"kind": "table"})
    write_json(phase9_root / "figures" / "menu_build_time_by_candidate_count.png.status.json", {"status": "blocked"})

    write_text(case_root / "README.md", "case scaffold\n")
    write_text(case_root / "case_manifest_draft.yaml", "status: scaffold\n")
    write_json(case_root / "source_contracts.json", {"status": "scaffold"})
    write_text(case_root / "validate_case_contracts.py", "print('validator scaffold')\n")

    for name in [
        "RC_FORMAL_DIAGNOSIS.md",
        "SENSITIVITY_SUMMARY.md",
        "COMPUTATIONAL_TRACTABILITY_SUMMARY.md",
        "FORMAL_BLOCKER_DIAGNOSIS.md",
        "FORMAL_FAILURE_DIAGNOSIS.md",
        "FROZEN_FINAL_SETTINGS.md",
    ]:
        write_text(results_root / name, f"# {name}\n")

    return {
        "main_rc": main_root,
        "phase8_sensitivity": phase8_root,
        "phase9_tractability": phase9_root,
        "case_scaffold": case_root,
        "blocker_status": results_root,
    }


def test_collects_required_source_families_and_tiers():
    with TemporaryDirectory() as tmp:
        roots = build_source_roots(Path(tmp))
        entries = collect_phase10_sources(source_roots=roots)
        families = {entry["source_family"] for entry in entries}
        assert families == {"main_rc", "phase8_sensitivity", "phase9_tractability", "case_scaffold", "blocker_status"}
        assert any(entry["package_tier"] == "main_paper_candidate" for entry in entries)
        assert all(entry["claim_ready"] is False for entry in entries if entry["source_family"] in {"phase8_sensitivity", "phase9_tractability"})
        assert all(entry["package_tier"] == "diagnostic_appendix" for entry in entries if entry["source_family"] in {"phase8_sensitivity", "phase9_tractability"})
        case_entries = [entry for entry in entries if entry["source_family"] == "case_scaffold"]
        assert case_entries
        assert all(entry["package_tier"] == "scaffold_only" for entry in case_entries)
        assert not any(entry["package_role"] in {"result_table", "result_figure", "table", "figure"} for entry in case_entries)


def test_writer_outputs_indexes_markdown_and_mirror():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        roots = build_source_roots(root)
        output_root = root / "package"
        mirror_root = root / "mirror" / "phase10_paper_artifacts"
        result = write_phase10_package(output_root=output_root, mirror_root=mirror_root, source_roots=roots)
        for name in [
            "CLAIM_GUARD.json",
            "PACKAGE_INDEX.json",
            "SOURCE_INDEX.json",
            "ARTIFACT_TO_SECTION_MAP.json",
            "PACKAGE_STATUS.json",
            "README.md",
            "artifact_to_section_map.md",
            "claim_checklist.md",
            "safe_language_boundaries.md",
        ]:
            assert (output_root / name).exists()
            assert (mirror_root / name).exists()
        package_index = json.loads((output_root / "PACKAGE_INDEX.json").read_text(encoding="utf-8"))
        section_map = json.loads((output_root / "ARTIFACT_TO_SECTION_MAP.json").read_text(encoding="utf-8"))
        status = json.loads((output_root / "PACKAGE_STATUS.json").read_text(encoding="utf-8"))
        guard = json.loads((output_root / "CLAIM_GUARD.json").read_text(encoding="utf-8"))
        path_counts = Counter(entry["source_path"] for entry in package_index["entries"])
        assert result["claim_ready"] is False
        assert package_index["claim_ready"] is False
        assert not [path for path, count in path_counts.items() if count > 1]
        assert status["claim_ready"] is False
        assert status["strict_claim_guard_claim_ready"] is False
        assert status["manuscript_positive_claims_allowed"] is False
        assert status["strict_claim_guard_path"].endswith("CLAIM_GUARD.json")
        assert status["source_family_counts"]["case_scaffold"] >= 1
        assert "main_rc_results" in section_map["sections"]
        assert "case_scaffold_appendix" in section_map["sections"]
        assert guard["schema_version"] == "phase10-strict-claim-guard-v1"
        assert guard["claim_ready"] is False
        assert len(guard["claims"]) == 8
        claims = {claim["claim_id"]: claim for claim in guard["claims"]}
        assert claims["C1_central_adaptive_menu_superiority"]["support_status"] == "unsupported_blocked"
        assert claims["C8_semi_real_case_validation"]["support_status"] == "scaffold_only_blocked"
        assert "C1_central_adaptive_menu_superiority" in status["blocked_claim_ids"]
        assert "C8_semi_real_case_validation" in status["blocked_claim_ids"]
        assert not (mirror_root / "normalized_rows.json").exists()
        checklist = (output_root / "claim_checklist.md").read_text(encoding="utf-8")
        boundaries = (output_root / "safe_language_boundaries.md").read_text(encoding="utf-8")
        assert "overall_claim_ready: false" in checklist
        assert "C1_central_adaptive_menu_superiority" in checklist
        assert "semi-real case scaffold" in checklist
        assert "case-study validation" in boundaries
        assert "near-optimal greedy" in boundaries


def test_public_script_builds_package_with_arguments():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        roots = build_source_roots(root)
        output_root = root / "cli-package"
        mirror_root = root / "cli-mirror"
        completed = subprocess.run(
            [
                sys.executable,
                "scripts/build_phase10_paper_artifacts.py",
                "--output-root",
                str(output_root),
                "--mirror-root",
                str(mirror_root),
                "--main-artifact-root",
                str(roots["main_rc"]),
                "--phase8-root",
                str(roots["phase8_sensitivity"]),
                "--phase9-root",
                str(roots["phase9_tractability"]),
                "--case-scaffold-root",
                str(roots["case_scaffold"]),
                "--results-root",
                str(roots["blocker_status"]),
            ],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            check=True,
        )
        payload = json.loads(completed.stdout)
        assert payload["claim_ready"] is False
        assert payload["artifact_count"] > 0
        assert (output_root / "PACKAGE_STATUS.json").exists()
        assert (output_root / "CLAIM_GUARD.json").exists()
        assert (mirror_root / "PACKAGE_STATUS.json").exists()
        assert (mirror_root / "CLAIM_GUARD.json").exists()


def main():
    tests = [
        test_collects_required_source_families_and_tiers,
        test_writer_outputs_indexes_markdown_and_mirror,
        test_public_script_builds_package_with_arguments,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} Phase 10 paper artifact package tests")


if __name__ == "__main__":
    main()
