import json
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Src.manuscript_claims import build_claim_guard, build_strict_claim_guard, write_manuscript_frame  # noqa: E402


def blocked_status():
    return {
        "artifact_status": {
            "status": "blocked",
            "claim_ready": False,
            "placeholder_only": True,
            "diagnostic_policy_labels": ["no_filter_diagnostic"],
            "blockers": [
                {
                    "code": "missing_checkpoint_file",
                    "message": "Required checkpoint file is unavailable; refusing random-weight evidence.",
                    "checkpoint_path": "outputs/shared_training/work2_robust_menu/pilot/supervised_ml.pt",
                }
            ],
            "uptake_regimes": ["low", "medium"],
        },
        "blockers": [
            {
                "code": "formal_skipped",
                "message": "Formal evidence was skipped for this Phase 4 run.",
            }
        ],
        "claim_ready": False,
        "pilot_claim_ready": False,
        "formal_claim_ready": False,
        "placeholder_only": True,
        "policies": ["robust_risk_adjusted", "no_filter_diagnostic"],
        "run_id": "pilot-test",
        "study": "pilot_robust_menu",
    }


def claim_ready_status():
    return {
        "artifact_status": {
            "status": "claim_ready",
            "claim_ready": True,
            "placeholder_only": False,
            "diagnostic_policy_labels": ["no_filter_diagnostic"],
            "blockers": [],
            "uptake_regimes": ["low", "medium"],
        },
        "blockers": [],
        "claim_ready": True,
        "pilot_claim_ready": True,
        "formal_claim_ready": True,
        "placeholder_only": False,
        "policies": ["robust_risk_adjusted", "hard_filter", "no_filter_diagnostic"],
        "run_id": "formal-test",
        "study": "formal_robust_menu",
        "formal_readiness": {
            "status": "passed",
            "path": "outputs/formal_readiness/formal_robust_menu/FORMAL_READINESS.json",
            "hash": "readiness-hash",
            "dependency_snapshot_hash": "dependency-hash",
            "checkpoint_hash": "abc123",
        },
    }


def write_status(root, status):
    artifact_root = root / "artifacts" / "work2_robust_menu"
    artifact_root.mkdir(parents=True)
    (artifact_root / "ARTIFACT_STATUS.json").write_text(json.dumps(status), encoding="utf-8")
    return artifact_root


def strict_package_indexes():
    entries = [
        {
            "artifact_id": "main_rc:status:artifact_status",
            "source_family": "main_rc",
            "source_path": "work2_coding/artifacts/work2_robust_menu/ARTIFACT_STATUS.json",
            "package_tier": "main_paper_candidate",
            "package_role": "status",
            "status": "blocked",
            "claim_ready": False,
        },
        {
            "artifact_id": "phase8_sensitivity:aggregate:sensitivity",
            "source_family": "phase8_sensitivity",
            "source_path": "work2_coding/artifacts/work2_robust_menu/phase8_sensitivity/aggregates/sensitivity_axis_summary.json",
            "package_tier": "diagnostic_appendix",
            "package_role": "aggregate",
            "status": "diagnostic_provisional_blocked",
            "claim_ready": False,
        },
        {
            "artifact_id": "phase9_tractability:aggregate:tractability",
            "source_family": "phase9_tractability",
            "source_path": "work2_coding/artifacts/work2_robust_menu/phase9_tractability/aggregates/exact_greedy_tractability_summary.json",
            "package_tier": "diagnostic_appendix",
            "package_role": "aggregate",
            "status": "diagnostic_provisional_blocked",
            "claim_ready": False,
        },
        {
            "artifact_id": "case_scaffold:case_scaffold_doc:readme",
            "source_family": "case_scaffold",
            "source_path": ".planning/data/case_studies/README.md",
            "package_tier": "scaffold_only",
            "package_role": "case_scaffold_doc",
            "status": "scaffold_only_no_result_evidence",
            "claim_ready": False,
        },
        {
            "artifact_id": "blocker_status:blocker_status:formal_blocker",
            "source_family": "blocker_status",
            "source_path": ".planning/results/FORMAL_BLOCKER_DIAGNOSIS.md",
            "package_tier": "blocked_status",
            "package_role": "blocker_status",
            "status": "blocked",
            "claim_ready": False,
        },
    ]
    return {
        "package_index": {
            "schema_version": "phase10-paper-artifact-package-v1",
            "claim_ready": False,
            "entries": entries,
        },
        "package_status": {
            "claim_ready": False,
            "blockers": [
                {
                    "artifact_id": "main_rc:status:artifact_status",
                    "source_family": "main_rc",
                    "reason": "missing_checkpoint_file: checkpoint unavailable",
                }
            ],
        },
    }


def test_blocked_status_blocks_empirical_claims():
    guard = build_claim_guard(blocked_status())
    blocked_ids = {claim["id"] for claim in guard["blocked_claims"]}
    assert guard["claim_ready"] is False
    assert "empirical_superiority" in blocked_ids
    assert "pilot_formal_completed" in blocked_ids
    assert "universal_dominance" in blocked_ids
    assert "real_passenger_validation" in blocked_ids
    assert "no_filter_operational_recommendation" in blocked_ids
    assert "full_dynamic_exact_optimality" in blocked_ids
    assert "no_filter_diagnostic" in guard["diagnostic_policies"]
    assert any(item.get("code") == "missing_checkpoint_file" for item in guard["blockers"])


def test_claim_ready_status_allows_effect_size_family_not_universal_claims():
    guard = build_claim_guard(claim_ready_status())
    conditional = {claim["id"]: claim for claim in guard["conditional_claims"]}
    blocked_ids = {claim["id"] for claim in guard["blocked_claims"]}
    assert guard["claim_ready"] is True
    assert conditional["pilot_formal_effect_sizes"]["allowed"] is True
    assert conditional["formal_policy_ranking"]["allowed"] is True
    assert guard["formal_readiness_status"] == "passed"
    assert "universal_dominance" in blocked_ids
    assert "real_passenger_validation" in blocked_ids


def test_strict_claim_guard_blocks_positive_claims_and_preserves_status_claim():
    guard = build_strict_claim_guard(strict_package_indexes(), artifact_statuses={"main_rc": blocked_status()})
    claims = {claim["claim_id"]: claim for claim in guard["claims"]}
    assert guard["schema_version"] == "phase10-strict-claim-guard-v1"
    assert guard["claim_ready"] is False
    assert guard["manuscript_positive_claims_allowed"] is False
    assert claims["C1_central_adaptive_menu_superiority"]["support_status"] == "unsupported_blocked"
    assert claims["C1_central_adaptive_menu_superiority"]["manuscript_allowed"] is False
    assert claims["C3_adaptive_window_increment"]["support_status"] == "unsupported"
    assert claims["C6_exact_greedy_computational_credibility"]["support_status"] == "blocked_diagnostic"
    assert claims["C7_provenance_status_transparency"]["support_status"] == "status_supported"
    assert claims["C7_provenance_status_transparency"]["manuscript_allowed"] is True
    assert claims["C7_provenance_status_transparency"]["claim_ready"] is True
    assert claims["C8_semi_real_case_validation"]["support_status"] == "scaffold_only_blocked"
    forbidden = " ".join(
        phrase
        for claim in claims.values()
        for phrase in claim["forbidden_language"]
    )
    for phrase in [
        "universal dominance",
        "claim-ready superiority",
        "real passenger behavior",
        "case-study validation",
        "no-filter recommendation",
        "near-optimal greedy",
    ]:
        assert phrase in forbidden


def test_generator_writes_markdown_json_and_mirror():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        artifact_root = write_status(root, blocked_status())
        mirror_root = root / "mirror" / "work2_robust_menu"
        result = write_manuscript_frame(artifact_root, mirror_root=mirror_root)
        output_dir = Path(result["output_dir"])
        for name in ("method_outline.md", "experiment_outline.md", "result_outline.md", "claim_checklist.md", "CLAIM_GUARD.json"):
            assert (output_dir / name).exists()
            assert (mirror_root / "manuscript" / name).exists()
        guard = json.loads((output_dir / "CLAIM_GUARD.json").read_text(encoding="utf-8"))
        checklist = (output_dir / "claim_checklist.md").read_text(encoding="utf-8")
        result_outline = (output_dir / "result_outline.md").read_text(encoding="utf-8")
        assert guard["claim_ready"] is False
        assert "empirical_superiority" in {claim["id"] for claim in guard["blocked_claims"]}
        assert "no_filter_diagnostic" in checklist
        assert "not claim-ready" in result_outline


def test_public_script_uses_artifact_root_argument():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        artifact_root = write_status(root, blocked_status())
        completed = subprocess.run(
            [
                sys.executable,
                "scripts/build_manuscript_frame.py",
                "--artifact-root",
                str(artifact_root),
                "--mirror-root",
                str(root / "mirror"),
            ],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            check=True,
        )
        payload = json.loads(completed.stdout)
        assert payload["claim_ready"] is False
        assert "empirical_superiority" in payload["blocked_claims"]
        assert (artifact_root / "manuscript" / "CLAIM_GUARD.json").exists()


def main():
    tests = [
        test_blocked_status_blocks_empirical_claims,
        test_claim_ready_status_allows_effect_size_family_not_universal_claims,
        test_strict_claim_guard_blocks_positive_claims_and_preserves_status_claim,
        test_generator_writes_markdown_json_and_mirror,
        test_public_script_uses_artifact_root_argument,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} manuscript claim guard tests")


if __name__ == "__main__":
    main()
