import json
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Src.manuscript_claims import build_claim_guard, write_manuscript_frame  # noqa: E402


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
    }


def write_status(root, status):
    artifact_root = root / "artifacts" / "work2_robust_menu"
    artifact_root.mkdir(parents=True)
    (artifact_root / "ARTIFACT_STATUS.json").write_text(json.dumps(status), encoding="utf-8")
    return artifact_root


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
    assert "universal_dominance" in blocked_ids
    assert "real_passenger_validation" in blocked_ids


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
        test_generator_writes_markdown_json_and_mirror,
        test_public_script_uses_artifact_root_argument,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} manuscript claim guard tests")


if __name__ == "__main__":
    main()
