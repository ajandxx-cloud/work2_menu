"""Execution-status helpers for Work2 robust-menu studies."""

import hashlib
import subprocess
from pathlib import Path

from Src.paired_replay import build_normalized_row, checkpoint_row_metadata, resolve_paired_settings, validate_rows


BLOCKING_TIERS = {"pilot", "formal"}


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _repo_root():
    return Path(__file__).resolve().parents[2]


def collect_git_provenance(repo_root=None):
    repo_root = Path(repo_root or _repo_root())
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(repo_root),
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--short"],
            cwd=str(repo_root),
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip().splitlines()
    except Exception as exc:  # pragma: no cover - defensive for non-git archives
        return {
            "git_commit": "unknown",
            "git_dirty": True,
            "git_status_summary": "git unavailable: " + str(exc),
        }

    return {
        "git_commit": commit,
        "git_dirty": bool(status),
        "git_status_summary": "; ".join(status[:20]),
    }


def checkpoint_path_for_manifest(manifest):
    checkpoint = manifest.get("shared_checkpoint") or {}
    path = checkpoint.get("path") or (manifest.get("base_args") or {}).get("checkpoint_path", "")
    return path or ""


def resolve_checkpoint_path(manifest, root=None):
    checkpoint_path = checkpoint_path_for_manifest(manifest)
    if not checkpoint_path:
        return Path("")
    path = Path(checkpoint_path)
    if path.is_absolute():
        return path
    return Path(root or Path(__file__).resolve().parents[1]) / path


def inspect_manifest_prerequisites(manifest, root=None, actual_execution=False, contract_only=False):
    blockers = []
    tier = manifest.get("tier", "")
    shared = manifest.get("shared_checkpoint") or {}
    checkpoint_required = bool(shared.get("required") or (manifest.get("base_args") or {}).get("require_checkpoint"))
    expected_status = shared.get("expected_status", "loaded")
    checkpoint_path = checkpoint_path_for_manifest(manifest)
    resolved_path = resolve_checkpoint_path(manifest, root=root)

    if contract_only and tier == "formal":
        blockers.append(
            {
                "code": "formal_placeholder_not_allowed",
                "severity": "blocking",
                "tier": tier,
                "message": "Formal studies cannot emit placeholder contract-only rows.",
            }
        )

    if tier in BLOCKING_TIERS and checkpoint_required:
        if not checkpoint_path:
            blockers.append(
                {
                    "code": "missing_checkpoint_path",
                    "severity": "blocking",
                    "tier": tier,
                    "expected_status": expected_status,
                    "checkpoint_path": "",
                    "message": "Required checkpoint path is missing from manifest.",
                }
            )
        elif not resolved_path.exists():
            blockers.append(
                {
                    "code": "missing_checkpoint_file",
                    "severity": "blocking",
                    "tier": tier,
                    "expected_status": expected_status,
                    "checkpoint_path": checkpoint_path,
                    "resolved_checkpoint_path": str(resolved_path),
                    "message": "Required checkpoint file is unavailable; refusing random-weight evidence.",
                }
            )

    if actual_execution and not blockers:
        blockers.append(
            {
                "code": "actual_runtime_not_enabled",
                "severity": "blocking",
                "tier": tier,
                "message": "Actual simulator replay is not wired into the public Phase 4 runner yet.",
            }
        )

    return blockers


def checkpoint_metadata_for_setting(setting, manifest, root=None):
    args = setting["args"]
    metadata = checkpoint_row_metadata(args)
    if not metadata["checkpoint_required"]:
        return metadata

    checkpoint_path = metadata.get("checkpoint_path") or checkpoint_path_for_manifest(manifest)
    resolved_path = Path(checkpoint_path)
    if checkpoint_path and not resolved_path.is_absolute():
        resolved_path = Path(root or Path(__file__).resolve().parents[1]) / checkpoint_path
    metadata["checkpoint_path"] = checkpoint_path
    if resolved_path.exists():
        metadata["checkpoint_load_status"] = "loaded"
        metadata["checkpoint_hash"] = sha256_file(resolved_path)
    else:
        metadata["checkpoint_load_status"] = "failed"
        metadata["checkpoint_hash"] = None
    return metadata


def blocked_rows_for_manifest(manifest, run_id, manifest_hash_value, blockers, max_policies=None, root=None):
    if manifest.get("tier") == "formal":
        return []
    settings = resolve_paired_settings(manifest, manifest_hash_value=manifest_hash_value)
    if max_policies is not None:
        allowed_tags = []
        for setting in settings:
            tag = setting["policy_tag"]
            if tag not in allowed_tags:
                allowed_tags.append(tag)
            if len(allowed_tags) >= max_policies:
                break
        settings = [setting for setting in settings if setting["policy_tag"] in set(allowed_tags)]

    provenance = collect_git_provenance()
    rows = []
    status = "blocked" if any(item.get("severity") == "blocking" for item in blockers) else "incomplete"
    for setting in settings:
        checkpoint = checkpoint_metadata_for_setting(setting, manifest, root=root)
        rows.append(
            build_normalized_row(
                setting,
                run_id=run_id,
                checkpoint_metadata=checkpoint,
                stats_metadata={
                    "acceptance_rate": None,
                    "optout_rate": None,
                    "count_opted_out": None,
                    "count_accepted_home": None,
                    "count_accepted_meeting_point": None,
                },
                menu_metadata={
                    "eta_filter_mode": setting["args"].get("menu_eta_filter_mode"),
                    "effective_menu_policy": setting["args"].get("menu_policy"),
                    "menu_selection_solver_effective": "not_executed",
                    "solver_fallback_reason": blockers[0]["code"] if blockers else "incomplete",
                },
                provenance_metadata=provenance,
                status=status,
                execution_status=status,
                placeholder_only=True,
            )
        )
    validate_rows(rows)
    return rows
