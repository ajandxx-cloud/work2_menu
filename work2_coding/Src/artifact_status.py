"""Artifact eligibility and provenance helpers for Phase 4 evidence."""

import importlib.metadata
import json
import platform
import subprocess
import sys
import hashlib
from datetime import datetime, timezone
from pathlib import Path


CLAIM_READY = "claim_ready"
DIAGNOSTIC = "diagnostic"
INCOMPLETE = "incomplete"
BLOCKED = "blocked"
ARTIFACT_STATUSES = {CLAIM_READY, DIAGNOSTIC, INCOMPLETE, BLOCKED}
CLAIM_READY_CHECKPOINT_STATUSES = {"loaded"}


def utc_now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _unique(rows, field):
    return sorted({row.get(field) for row in rows if row.get(field) not in (None, "")})


def classify_artifact(rows, summary=None, claim_ready_requested=False, dependency_snapshot=None):
    summary = summary or {}
    rows = rows or []
    reasons = []
    status = CLAIM_READY

    if not rows:
        status = BLOCKED
        reasons.append("no normalized rows are available")

    tiers = set(_unique(rows, "tier") or [summary.get("tier")])
    formal_or_pilot = bool(tiers & {"pilot", "formal"})
    placeholder = any(bool(row.get("placeholder_only")) for row in rows)
    row_statuses = set(_unique(rows, "status"))
    execution_statuses = set(_unique(rows, "execution_status"))
    run_modes = set(_unique(rows, "run_mode") or [summary.get("run_mode")])
    checkpoint_bad = [
        row
        for row in rows
        if row.get("checkpoint_required") and row.get("checkpoint_load_status") not in CLAIM_READY_CHECKPOINT_STATUSES
    ]
    diagnostic_labels = sorted({row.get("policy_tag") for row in rows if row.get("diagnostic")})
    no_filter_only = bool(rows) and all(str(row.get("policy_tag", "")).find("no_filter") >= 0 for row in rows)

    if placeholder:
        status = INCOMPLETE
        reasons.append("placeholder_only rows cannot support claim-ready artifacts")
    if "blocked" in row_statuses or "blocked" in execution_statuses or summary.get("execution_status") == "blocked":
        status = BLOCKED
        reasons.append("source study execution is blocked")
    elif "failed" in row_statuses or "failed" in execution_statuses or summary.get("execution_status") == "failed":
        status = BLOCKED
        reasons.append("source study execution has failed rows")
    elif row_statuses & {"incomplete", "contract_only"} or execution_statuses & {"incomplete", "contract_only"}:
        status = INCOMPLETE
        reasons.append("source rows are incomplete or contract-only")
    if checkpoint_bad and formal_or_pilot:
        status = BLOCKED
        reasons.append("pilot/formal rows require loaded checkpoint provenance")
    if "formal" in tiers and status == CLAIM_READY and not dependency_snapshot:
        status = BLOCKED
        reasons.append("formal claim-ready artifacts require a dependency snapshot")
    if "smoke" in tiers and status == CLAIM_READY:
        status = DIAGNOSTIC
        reasons.append("smoke artifacts are diagnostic/status evidence only")
    if "diagnostic" in run_modes and status in {CLAIM_READY, DIAGNOSTIC}:
        status = DIAGNOSTIC
        reasons.append("diagnostic run mode is not claim-ready evidence")
    if diagnostic_labels and status == CLAIM_READY and len(diagnostic_labels) == len({row.get("policy_tag") for row in rows}):
        status = DIAGNOSTIC
        reasons.append("all source policies are diagnostic-only")
    if no_filter_only and status == CLAIM_READY:
        status = DIAGNOSTIC
        reasons.append("no-filter-only rows are diagnostic and cannot support formal claims")
    if claim_ready_requested and "formal" in tiers and not dependency_snapshot:
        status = BLOCKED
        reasons.append("formal claim-ready artifacts require a dependency snapshot")

    blockers = list(summary.get("blockers") or [])
    if blockers and status != BLOCKED:
        status = BLOCKED
        reasons.append("study summary contains blocker reports")

    return {
        "status": status,
        "claim_ready": status == CLAIM_READY,
        "reasons": sorted(set(reasons)),
        "placeholder_only": placeholder,
        "row_statuses": sorted(row_statuses),
        "execution_statuses": sorted(execution_statuses),
        "checkpoint_statuses": _unique(rows, "checkpoint_load_status"),
        "uptake_regimes": _unique(rows, "uptake_regime"),
        "diagnostic_policy_labels": diagnostic_labels,
        "blockers": blockers,
    }


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_formal_readiness(path):
    path = Path(path)
    with path.open("r", encoding="utf-8") as handle:
        readiness = json.load(handle)
    readiness["_path"] = str(path)
    readiness["_hash"] = sha256_file(path)
    return readiness


def _resolve_recorded_path(path_value, base_path):
    if not path_value:
        return Path("")
    path = Path(path_value)
    if path.is_absolute() or path.exists():
        return path
    return Path(base_path).parent / path.name


def readiness_metadata(readiness):
    checkpoint = readiness.get("checkpoint") or {}
    dependency = readiness.get("dependency_snapshot") or {}
    git = readiness.get("git_provenance") or {}
    return {
        "path": readiness.get("_path", ""),
        "hash": readiness.get("_hash", ""),
        "schema_version": readiness.get("schema_version"),
        "status": readiness.get("status"),
        "claim_ready_allowed": bool(readiness.get("claim_ready_allowed")),
        "study": readiness.get("study"),
        "run_id": readiness.get("run_id"),
        "manifest_hash": (readiness.get("manifest") or {}).get("hash"),
        "checkpoint_hash": checkpoint.get("hash"),
        "checkpoint_status": checkpoint.get("load_status"),
        "dependency_snapshot_path": dependency.get("path"),
        "dependency_snapshot_hash": dependency.get("hash"),
        "git_commit": git.get("git_commit"),
        "git_dirty": bool(git.get("git_dirty")),
        "blockers": readiness.get("blockers") or [],
    }


def validate_formal_readiness_for_run(readiness_json, rows, summary):
    readiness = load_formal_readiness(readiness_json)
    metadata = readiness_metadata(readiness)
    reasons = []

    if readiness.get("status") != "passed":
        reasons.append("formal readiness JSON status is not passed")
    if readiness.get("claim_ready_allowed") is not True:
        reasons.append("formal readiness JSON does not allow claim-ready artifacts")
    if (readiness.get("git_provenance") or {}).get("git_dirty"):
        reasons.append("formal readiness git_dirty must be false")

    dependency = readiness.get("dependency_snapshot") or {}
    dependency_path = dependency.get("path")
    dependency_hash = dependency.get("hash")
    if not dependency_path or not dependency_hash:
        reasons.append("formal readiness JSON must reference a dependency snapshot path and hash")
    else:
        resolved_dependency = _resolve_recorded_path(dependency_path, readiness.get("_path", ""))
        if not resolved_dependency.exists():
            reasons.append("formal readiness dependency snapshot does not exist")
        elif sha256_file(resolved_dependency) != dependency_hash:
            reasons.append("formal readiness dependency snapshot hash mismatch")

    checkpoint = readiness.get("checkpoint") or {}
    if checkpoint.get("load_status") != "loaded" or not checkpoint.get("hash"):
        reasons.append("formal readiness checkpoint must be loaded and hashed")

    expected_manifest_hash = summary.get("manifest_hash") or next((row.get("manifest_hash") for row in rows if row.get("manifest_hash")), "")
    readiness_manifest_hash = (readiness.get("manifest") or {}).get("hash")
    if expected_manifest_hash and readiness_manifest_hash != expected_manifest_hash:
        reasons.append("formal readiness manifest hash does not match source run")

    row_checkpoint_hashes = sorted({row.get("checkpoint_hash") for row in rows if row.get("checkpoint_hash")})
    row_checkpoint_statuses = sorted({row.get("checkpoint_load_status") for row in rows if row.get("checkpoint_load_status")})
    if "loaded" not in row_checkpoint_statuses or any(status != "loaded" for status in row_checkpoint_statuses):
        reasons.append("formal source rows must all report loaded checkpoint status")
    if row_checkpoint_hashes and checkpoint.get("hash") not in row_checkpoint_hashes:
        reasons.append("formal readiness checkpoint hash does not match source rows")
    if not row_checkpoint_hashes:
        reasons.append("formal source rows must include checkpoint hashes")

    return {
        "valid": not reasons,
        "reasons": reasons,
        "readiness": readiness,
        "metadata": metadata,
        "dependency_snapshot": {
            "path": dependency_path,
            "hash": dependency_hash,
        }
        if dependency_path and dependency_hash
        else None,
    }


def collect_environment_provenance(include_freeze=False):
    packages = {}
    for name in ("numpy", "matplotlib", "yaml", "torch"):
        try:
            package_name = "PyYAML" if name == "yaml" else name
            packages[name] = importlib.metadata.version(package_name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = None

    snapshot = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "packages": packages,
        "pip_freeze": None,
    }
    if include_freeze:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "freeze"],
                text=True,
                capture_output=True,
                check=True,
            )
            snapshot["pip_freeze"] = result.stdout.strip().splitlines()
        except Exception as exc:  # pragma: no cover - environment dependent
            snapshot["pip_freeze_error"] = str(exc)
    return snapshot


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
