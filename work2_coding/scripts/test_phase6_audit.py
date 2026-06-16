import sys
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.phase6_audit import PHASE6_REQUIREMENTS, build_phase6_audit, write_phase6_audit  # noqa: E402
from Src.policy_adapters import attention_policy_tags, mainline_policy_tags  # noqa: E402


def _all_gap_like(audit):
    items = []
    items.extend(audit["pricing"].get("gaps") or [])
    items.extend(audit["rc_dataset"].get("gaps") or [])
    items.extend(audit["readiness"].get("blockers") or [])
    items.extend(audit["artifact_gates"].get("exclusions") or [])
    items.extend(audit["claim_status"].get("blocked_by") or [])
    items.extend(audit.get("downstream_gaps") or [])
    return items


def test_import_smoke_result_is_captured():
    audit = build_phase6_audit()
    assert audit["runtime"]["root"] == "work2_coding/"
    assert audit["runtime"]["import_status"] == "IMPORT_OK"
    assert "Src.config" in audit["runtime"]["command"]


def test_manifest_family_has_exact_mainline_tags():
    audit = build_phase6_audit()
    expected = mainline_policy_tags()
    assert audit["policies"]["mainline_tags"] == expected
    for name in ["smoke_robust_menu", "pilot_robust_menu", "formal_robust_menu"]:
        assert audit["manifests"][name]["required_policy_tags"] == expected
        assert audit["manifests"][name]["policy_tags"] == expected
        assert audit["manifests"][name]["normalized_row_v2"] is True


def test_formal_manifest_is_rc_with_five_splits():
    audit = build_phase6_audit()
    formal = audit["manifests"]["formal_robust_menu"]
    assert formal["instance"] == "RC"
    assert formal["split_count"] == 5
    assert audit["rc_dataset"]["instance"] == "RC"
    assert audit["rc_dataset"]["data_root_exists"] is True
    assert audit["rc_dataset"]["formal_split_count"] == 5
    assert {item["data_seed"] for item in audit["rc_dataset"]["split_seed_surface"]} == {0, 1}
    assert {item["data_seed_test"] for item in audit["rc_dataset"]["split_seed_surface"]} == {0, 1}


def test_current_readiness_dirty_git_and_loaded_checkpoint_are_preserved():
    audit = build_phase6_audit()
    assert audit["readiness"]["status"] == "blocked"
    assert audit["readiness"]["claim_ready_allowed"] is False
    assert "dirty_git" in audit["readiness"]["blocker_codes"]
    assert audit["readiness"]["checkpoint_load_status"] == "loaded"
    assert audit["readiness"]["checkpoint_hash"]
    assert audit["readiness"]["dependency_snapshot_hash"]


def test_gap_and_blocker_rows_have_required_handoff_fields():
    audit = build_phase6_audit()
    required = {"reason", "minimal_fix", "rerun_command", "evidence_location"}
    for item in _all_gap_like(audit):
        missing = [key for key in required if not item.get(key)]
        assert not missing, (item, missing)


def test_attention_tags_are_excluded_from_v1_claim_ladder():
    audit = build_phase6_audit()
    excluded = {row["tag"] for row in audit["policies"]["excluded_attention_diagnostic_tags"]}
    assert excluded == set(attention_policy_tags())
    mainline = set(audit["policies"]["mainline_tags"])
    assert not (mainline & excluded)
    assert all(row["v1_claim_ladder_member"] is False for row in audit["policies"]["excluded_attention_diagnostic_tags"])


def test_phase6_requirement_coverage_and_rerun_commands():
    audit = build_phase6_audit()
    assert audit["requirements"] == PHASE6_REQUIREMENTS
    for req in ["EXP-01", "EXP-02", "GATE-01", "GATE-02", "GATE-04"]:
        assert req in audit["requirements"]
    for key in ["import_smoke", "readiness_preflight", "formal_replay", "claim_ready_artifacts"]:
        assert audit["commands"][key]
        assert "work2_coding" in audit["commands"][key] or key.startswith("formal")


def test_pricing_modes_are_audited_by_resolved_pricing_mode():
    audit = build_phase6_audit()
    modes = audit["pricing"]["pricing_modes_by_tag"]
    assert set(modes) == {"no_pricing", "lambertw"}
    assert "mainline_no_menu" in modes["no_pricing"]
    assert "mainline_optimized_mw" in modes["no_pricing"]
    assert "mainline_fixed_menu" in modes["lambertw"]
    assert "mainline_optimized_adaptive" in modes["lambertw"]
    assert audit["pricing"]["static_pricing_modes_detected"] == []
    assert any(item["code"] == "static_pricing_contract_missing" for item in audit["pricing"]["gaps"])


def test_artifact_gate_exclusions_are_present():
    audit = build_phase6_audit()
    codes = {item["code"] for item in audit["artifact_gates"]["exclusions"]}
    assert {
        "placeholder_only_excluded",
        "bad_row_status_excluded",
        "checkpoint_provenance_required",
        "diagnostic_rows_excluded",
    }.issubset(codes)
    assert audit["artifact_gates"]["status"] == "blocked"


def test_report_writer_outputs_json_and_markdown():
    with TemporaryDirectory() as tmp:
        audit = write_phase6_audit(output_root=Path(tmp) / "phase6_audit")
        json_path = Path(audit["reports"]["json"])
        md_path = Path(audit["reports"]["markdown"])
        assert json_path.exists()
        assert md_path.exists()
        markdown = md_path.read_text(encoding="utf-8")
        assert "checkpoint_load_status" in markdown
        assert "claim_ready=false" in markdown
        assert "Formal replay was not run" in markdown


def main():
    tests = [
        test_import_smoke_result_is_captured,
        test_manifest_family_has_exact_mainline_tags,
        test_formal_manifest_is_rc_with_five_splits,
        test_current_readiness_dirty_git_and_loaded_checkpoint_are_preserved,
        test_gap_and_blocker_rows_have_required_handoff_fields,
        test_attention_tags_are_excluded_from_v1_claim_ladder,
        test_phase6_requirement_coverage_and_rerun_commands,
        test_pricing_modes_are_audited_by_resolved_pricing_mode,
        test_artifact_gate_exclusions_are_present,
        test_report_writer_outputs_json_and_markdown,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} phase6 audit tests")


if __name__ == "__main__":
    main()
