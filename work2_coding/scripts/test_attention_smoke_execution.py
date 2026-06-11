import json
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.attention_artifacts import attention_claim_guard, attention_pair_deltas


def run_command(args):
    return subprocess.run(args, cwd=str(ROOT), text=True, capture_output=True)


def last_stdout_path(result):
    return Path(result.stdout.strip().splitlines()[-1])


def load_run(run_dir):
    rows = json.loads((run_dir / "normalized_rows.json").read_text(encoding="utf-8"))
    summary = json.loads((run_dir / "study_summary.json").read_text(encoding="utf-8"))
    return rows, summary


def assert_attention_pair_contract(rows):
    assert {row["policy_tag"] for row in rows} == {"DSPO_original", "DSPO_attention"}
    assert {row["method_variant"] for row in rows} == {"DSPO_original", "DSPO_attention"}
    assert len({row["trace_id"] for row in rows}) == 1
    assert len({row["attention_pair_id"] for row in rows}) == 1
    assert all(row["attention_pair_complete"] is True for row in rows)
    for row in rows:
        assert "attention_enabled" in row
        assert "attention_mode" in row
        assert "attention_weight_summary" in row
        assert "net_objective_proxy" in row


def assert_guard_blocks_improvement(rows, summary):
    guard = attention_claim_guard(rows, attention_pair_deltas(rows), summary=summary)
    assert guard["attention_improves_dspo_allowed"] is False
    assert guard["blocked_claims"]


def test_contract_attention_smoke_rows_are_paired_and_block_claims():
    with TemporaryDirectory() as tmp:
        result = run_command([
            sys.executable,
            "scripts/run_study.py",
            "--study",
            "smoke_attention_dspo",
            "--contract-only",
            "--output-root",
            str(Path(tmp)),
        ])
        assert result.returncode == 0, result.stderr
        rows, summary = load_run(last_stdout_path(result))
        assert summary["execution_status"] == "contract_only"
        assert summary["placeholder_only"] is True
        assert_attention_pair_contract(rows)
        assert_guard_blocks_improvement(rows, summary)


def test_attention_actual_smoke_attempt_is_completed_or_blocked_explicitly():
    with TemporaryDirectory() as tmp:
        result = run_command([
            sys.executable,
            "scripts/run_study.py",
            "--study",
            "smoke_attention_dspo",
            "--execute",
            "--output-root",
            str(Path(tmp)),
            "--max-policies",
            "2",
        ])
        assert result.returncode == 0, result.stderr
        run_dir = last_stdout_path(result)
        rows, summary = load_run(run_dir)
        assert_attention_pair_contract(rows)
        assert summary["execution_status"] in {"completed", "blocked"}
        if summary["execution_status"] == "completed":
            assert summary["placeholder_only"] is False
            assert {row["status"] for row in rows} == {"completed"}
            assert not any(row["placeholder_only"] for row in rows)
            assert all(row["acceptance_rate"] is not None for row in rows)
        else:
            assert summary["blocker_count"] >= 1
            assert (run_dir / "blockers.json").exists()
            assert {row["status"] for row in rows} == {"blocked"}
        assert_guard_blocks_improvement(rows, summary)


def test_attention_pilot_missing_checkpoint_writes_blockers():
    with TemporaryDirectory() as tmp:
        manifest = yaml.safe_load((ROOT / "Experiments" / "studies" / "pilot_attention_dspo.yaml").read_text(encoding="utf-8"))
        missing_checkpoint = Path(tmp) / "missing" / "supervised_ml.pt"
        manifest["shared_checkpoint"]["path"] = str(missing_checkpoint)
        manifest["base_args"]["checkpoint_path"] = str(missing_checkpoint)
        manifest_path = Path(tmp) / "pilot_attention_missing_checkpoint.yaml"
        manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
        result = run_command([
            sys.executable,
            "scripts/run_study.py",
            "--study",
            str(manifest_path),
            "--execute",
            "--output-root",
            str(Path(tmp)),
            "--max-policies",
            "2",
        ])
        assert result.returncode == 0, result.stderr
        run_dir = last_stdout_path(result)
        rows, summary = load_run(run_dir)
        blockers = json.loads((run_dir / "blockers.json").read_text(encoding="utf-8"))["blockers"]
        assert summary["execution_status"] == "blocked"
        assert blockers[0]["code"] == "missing_checkpoint_file"
        assert blockers[0]["checkpoint_path"] == str(missing_checkpoint)
        assert {row["checkpoint_load_status"] for row in rows} == {"failed"}
        assert all(row["placeholder_only"] for row in rows)
        assert_guard_blocks_improvement(rows, summary)


def test_attention_artifact_builder_blocks_contract_smoke_claims():
    with TemporaryDirectory() as tmp:
        output_root = Path(tmp) / "runs"
        result = run_command([
            sys.executable,
            "scripts/run_study.py",
            "--study",
            "smoke_attention_dspo",
            "--contract-only",
            "--output-root",
            str(output_root),
        ])
        assert result.returncode == 0, result.stderr
        build = run_command([
            sys.executable,
            "scripts/build_attention_artifacts.py",
            "--study",
            "smoke_attention_dspo",
            "--study-output-root",
            str(output_root),
            "--output-root",
            str(Path(tmp) / "artifacts"),
            "--mirror-root",
            str(Path(tmp) / "mirror"),
            "--allow-incomplete",
        ])
        assert build.returncode == 0, build.stderr
        guard = json.loads((Path(tmp) / "artifacts" / "ATTENTION_CLAIM_GUARD.json").read_text(encoding="utf-8"))
        assert guard["attention_improves_dspo_allowed"] is False
        assert (Path(tmp) / "mirror" / "ATTENTION_CLAIM_GUARD.json").exists()


def main():
    tests = [
        test_contract_attention_smoke_rows_are_paired_and_block_claims,
        test_attention_actual_smoke_attempt_is_completed_or_blocked_explicitly,
        test_attention_pilot_missing_checkpoint_writes_blockers,
        test_attention_artifact_builder_blocks_contract_smoke_claims,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} attention smoke execution tests")


if __name__ == "__main__":
    main()
