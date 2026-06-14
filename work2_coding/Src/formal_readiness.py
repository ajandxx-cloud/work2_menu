"""Formal evidence readiness preflight for Work2 robust-menu studies."""

import json
import sys
from argparse import Namespace
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

from Src.artifact_status import collect_environment_provenance, write_json
from Src.experiment_contracts import load_manifest, manifest_hash, validate_manifest
from Src.paired_replay import build_normalized_row, resolve_paired_settings
from Src.study_execution import (
    checkpoint_path_for_manifest,
    collect_git_provenance,
    resolve_checkpoint_path,
    sha256_file,
)


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
READINESS_SCHEMA_VERSION = "formal-readiness-v1"
DEFAULT_OUTPUT_ROOT = ROOT / "outputs" / "formal_readiness"
FORMAL_CHECKPOINT_COMMAND = (
    "python scripts/train_shared_checkpoint.py --study formal_robust_menu "
    "--checkpoint-path outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt"
)


def utc_now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stable_hash(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    import hashlib

    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _report_dir(output_root, study_name):
    return Path(output_root or DEFAULT_OUTPUT_ROOT) / study_name


def _sidecar_path(checkpoint_path):
    return Path(str(checkpoint_path) + ".sidecar.json")


def _load_sidecar(checkpoint_path):
    sidecar_path = _sidecar_path(checkpoint_path)
    if not sidecar_path.exists():
        return {"path": str(sidecar_path), "exists": False, "hash": None, "data": None}
    return {
        "path": str(sidecar_path),
        "exists": True,
        "hash": sha256_file(sidecar_path),
        "data": json.loads(sidecar_path.read_text(encoding="utf-8")),
    }


def _settings_snapshot(manifest, manifest_hash_value):
    settings = resolve_paired_settings(manifest, manifest_hash_value=manifest_hash_value)
    key_fields = [
        "run_mode",
        "instance",
        "load_data",
        "pricing",
        "menu_k",
        "max_candidates",
        "hgs_reopt_time",
        "hgs_final_time",
        "reopt",
        "checkpoint_path",
        "require_checkpoint",
        "menu_eta_filter_mode",
        "menu_policy",
        "product_mode",
        "time_window_mode",
        "menu_contract_mode",
        "menu_pricing_mode",
    ]
    first_args = settings[0]["args"] if settings else {}
    payload = {
        "setting_count": len(settings),
        "settings_hashes": sorted({setting["settings_hash"] for setting in settings}),
        "paired_fields": manifest.get("paired_fields", []),
        "key_runtime_knobs": {key: first_args.get(key) for key in key_fields if key in first_args},
        "split_ids": [split.get("split_id") for split in manifest.get("splits", [])],
        "policy_tags": [policy.get("tag") for policy in manifest.get("policies", [])],
    }
    payload["settings_hash"] = _stable_hash(payload)
    return payload


def _write_dependency_snapshot(report_dir, manifest, manifest_hash_value, command):
    snapshot = collect_environment_provenance(include_freeze=True)
    snapshot.update(
        {
            "schema_version": "dependency-snapshot-v1",
            "created_at_utc": utc_now_iso(),
            "study": manifest["name"],
            "tier": manifest["tier"],
            "run_mode": manifest["run_mode"],
            "manifest_path": manifest.get("_path", ""),
            "manifest_hash": manifest_hash_value,
            "command": command,
            "resolved_settings": _settings_snapshot(manifest, manifest_hash_value),
        }
    )
    path = report_dir / "DEPENDENCY_SNAPSHOT.json"
    write_json(path, snapshot)
    return {"path": str(path), "hash": sha256_file(path), "data": snapshot}


def _load_checkpoint_smoke(manifest, checkpoint_path, run_id):
    """Use the same Config/model checkpoint path as actual replay, without replay."""

    from Src.config import Config

    mh = manifest_hash(manifest)
    setting = resolve_paired_settings(manifest, manifest_hash_value=mh)[0]
    args = deepcopy(setting["args"])
    args.update(
        {
            "checkpoint_path": str(checkpoint_path),
            "require_checkpoint": True,
            "allow_checkpoint_mismatch": False,
            "run_mode": manifest.get("run_mode", "formal"),
            "run_id": run_id,
            "save_model": False,
            "eval_only": True,
            "freeze_learning": True,
            "log_output": "file",
        }
    )

    original_stdout = sys.stdout
    try:
        config = Config(Namespace(**args))
        model = config.algo(config=config)
        return model.load_checkpoint(
            checkpoint_path=str(checkpoint_path),
            require_checkpoint=True,
            allow_checkpoint_mismatch=False,
            run_mode=manifest.get("run_mode", "formal"),
        )
    finally:
        sys.stdout = original_stdout


def _row_metadata_probe(manifest, run_id, checkpoint_path, checkpoint_hash):
    mh = manifest_hash(manifest)
    setting = resolve_paired_settings(manifest, manifest_hash_value=mh)[0]
    row = build_normalized_row(
        setting,
        run_id=run_id,
        checkpoint_metadata={
            "checkpoint_load_status": "loaded",
            "checkpoint_path": str(checkpoint_path),
            "checkpoint_hash": checkpoint_hash,
            "checkpoint_required": True,
            "checkpoint_intentional_mismatch": False,
        },
        stats_metadata={
            "acceptance_rate": 0.0,
            "optout_rate": 0.0,
            "count_opted_out": 0,
            "count_accepted_home": 0,
            "count_accepted_meeting_point": 0,
        },
        menu_metadata={
            "eta_filter_mode": setting["args"].get("menu_eta_filter_mode"),
            "effective_menu_policy": setting["args"].get("menu_policy"),
            "menu_selection_solver_effective": "readiness_probe",
        },
        provenance_metadata=collect_git_provenance(repo_root=REPO_ROOT),
        status="completed",
        execution_status="completed",
        placeholder_only=False,
    )
    return {
        "checkpoint_load_status": row["checkpoint_load_status"],
        "checkpoint_hash": row["checkpoint_hash"],
        "checkpoint_path": row["checkpoint_path"],
        "schema_version": row["schema_version"],
        "status": row["status"],
        "execution_status": row["execution_status"],
        "placeholder_only": row["placeholder_only"],
    }


def _blocker(code, message, **extra):
    item = {"code": code, "severity": "blocking", "message": message}
    item.update(extra)
    return item


def _markdown_report(report):
    blockers = report.get("blockers") or []
    lines = [
        "# Formal Readiness Report",
        "",
        f"- Study: `{report['study']}`",
        f"- Status: `{report['status']}`",
        f"- Claim-ready allowed: `{str(report['claim_ready_allowed']).lower()}`",
        f"- Manifest hash: `{report['manifest']['hash']}`",
        f"- Git dirty: `{str(report['git_provenance'].get('git_dirty')).lower()}`",
        f"- Dependency snapshot: `{report['dependency_snapshot']['path']}`",
        f"- Dependency snapshot hash: `{report['dependency_snapshot']['hash']}`",
        f"- Checkpoint status: `{report['checkpoint']['load_status']}`",
        f"- Checkpoint path: `{report['checkpoint']['resolved_path']}`",
        f"- Checkpoint hash: `{report['checkpoint'].get('hash') or ''}`",
        "",
        "## Blockers",
        "",
    ]
    if blockers:
        for blocker in blockers:
            lines.append(f"- `{blocker['code']}`: {blocker['message']}")
            if blocker.get("generation_command"):
                lines.append(f"  Remediation: `{blocker['generation_command']}`")
    else:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This readiness preflight does not execute formal replay and does not by itself support empirical claims.",
            "",
        ]
    )
    return "\n".join(lines)


def check_formal_readiness(
    study="formal_robust_menu",
    output_root=None,
    allow_dirty=False,
    command=None,
    root=None,
):
    """Run the formal preflight and persist JSON/Markdown readiness reports."""

    runtime_root = Path(root or ROOT)
    manifest = deepcopy(study) if isinstance(study, dict) else load_manifest(study)
    validate_manifest(manifest)
    if manifest.get("tier") != "formal":
        raise ValueError("formal readiness requires a formal-tier manifest")

    manifest_hash_value = manifest_hash(manifest)
    report_dir = _report_dir(output_root or DEFAULT_OUTPUT_ROOT, manifest["name"])
    report_dir.mkdir(parents=True, exist_ok=True)
    run_id = manifest["name"] + "-readiness-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    command = command or (
        "python scripts/check_formal_readiness.py --study "
        + manifest["name"]
        + " --output-root "
        + str(output_root or DEFAULT_OUTPUT_ROOT)
    )

    dependency_snapshot = _write_dependency_snapshot(report_dir, manifest, manifest_hash_value, command)
    git_provenance = collect_git_provenance(repo_root=runtime_root.parent)
    blockers = []
    if git_provenance.get("git_dirty") and not allow_dirty:
        blockers.append(
            _blocker(
                "dirty_git",
                "Repository has uncommitted changes; formal claim-ready readiness requires git_dirty=false.",
                git_status_summary=git_provenance.get("git_status_summary", ""),
            )
        )

    manifest_checkpoint_path = checkpoint_path_for_manifest(manifest)
    resolved_checkpoint_path = resolve_checkpoint_path(manifest, root=runtime_root)
    checkpoint = {
        "manifest_path": manifest_checkpoint_path,
        "resolved_path": str(resolved_checkpoint_path),
        "expected_status": (manifest.get("shared_checkpoint") or {}).get("expected_status", "loaded"),
        "required": bool((manifest.get("shared_checkpoint") or {}).get("required")),
        "exists": bool(resolved_checkpoint_path.exists()),
        "hash": None,
        "sidecar_path": str(_sidecar_path(resolved_checkpoint_path)),
        "sidecar_hash": None,
        "load_status": "missing",
        "load_smoke": None,
        "row_metadata_probe": None,
    }

    if not resolved_checkpoint_path.exists():
        blockers.append(
            _blocker(
                "missing_formal_checkpoint",
                "Required formal checkpoint is missing; refusing random-weight formal evidence.",
                checkpoint_path=manifest_checkpoint_path,
                resolved_checkpoint_path=str(resolved_checkpoint_path),
                expected_status=checkpoint["expected_status"],
                generation_command=FORMAL_CHECKPOINT_COMMAND,
            )
        )
    else:
        checkpoint_hash = sha256_file(resolved_checkpoint_path)
        checkpoint["hash"] = checkpoint_hash
        sidecar = _load_sidecar(resolved_checkpoint_path)
        checkpoint["sidecar_path"] = sidecar["path"]
        checkpoint["sidecar_hash"] = sidecar["hash"]
        try:
            smoke = _load_checkpoint_smoke(manifest, resolved_checkpoint_path, run_id)
            checkpoint["load_smoke"] = smoke
            checkpoint["load_status"] = smoke.get("checkpoint_load_status", "failed")
            if checkpoint["load_status"] != "loaded":
                blockers.append(
                    _blocker(
                        "formal_checkpoint_not_loaded",
                        "Formal checkpoint load smoke did not report loaded status.",
                        checkpoint_load_status=checkpoint["load_status"],
                        checkpoint_path=str(resolved_checkpoint_path),
                    )
                )
            elif smoke.get("checkpoint_hash") != checkpoint_hash:
                blockers.append(
                    _blocker(
                        "formal_checkpoint_hash_mismatch",
                        "Formal checkpoint load smoke hash does not match the resolved file hash.",
                        checkpoint_hash=checkpoint_hash,
                        load_smoke_hash=smoke.get("checkpoint_hash"),
                    )
                )
            else:
                checkpoint["row_metadata_probe"] = _row_metadata_probe(
                    manifest,
                    run_id,
                    resolved_checkpoint_path,
                    checkpoint_hash,
                )
        except Exception as exc:
            checkpoint["load_status"] = "failed"
            checkpoint["load_smoke"] = {"error_type": exc.__class__.__name__, "error_message": str(exc)}
            blockers.append(
                _blocker(
                    "formal_checkpoint_load_failed",
                    "Formal checkpoint load smoke failed.",
                    checkpoint_path=str(resolved_checkpoint_path),
                    error_type=exc.__class__.__name__,
                    error_message=str(exc),
                )
            )

    status = "blocked" if blockers else "passed"
    report = {
        "schema_version": READINESS_SCHEMA_VERSION,
        "created_at_utc": utc_now_iso(),
        "status": status,
        "claim_ready_allowed": status == "passed",
        "blockers": blockers,
        "study": manifest["name"],
        "tier": manifest["tier"],
        "run_mode": manifest["run_mode"],
        "run_id": run_id,
        "raw_run_dir": "",
        "formal_command": "python scripts/run_study.py --study formal_robust_menu --execute --output-root outputs/formal_v1",
        "readiness_command": command,
        "manifest": {
            "path": manifest.get("_path", ""),
            "hash": manifest_hash_value,
        },
        "settings": _settings_snapshot(manifest, manifest_hash_value),
        "checkpoint": checkpoint,
        "git_provenance": git_provenance,
        "dependency_snapshot": {
            "path": dependency_snapshot["path"],
            "hash": dependency_snapshot["hash"],
        },
        "notes": [
            "Readiness preflight does not execute formal replay.",
            "Formal empirical claims also require completed formal rows and claim-ready artifact gates.",
        ],
    }

    json_path = report_dir / "FORMAL_READINESS.json"
    md_path = report_dir / "FORMAL_READINESS.md"
    write_json(json_path, report)
    md_path.write_text(_markdown_report(report), encoding="utf-8")
    report["reports"] = {"json": str(json_path), "markdown": str(md_path)}
    write_json(json_path, report)
    return report
