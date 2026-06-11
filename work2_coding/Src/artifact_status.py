"""Artifact eligibility and provenance helpers for Phase 4 evidence."""

import importlib.metadata
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


CLAIM_READY = "claim_ready"
DIAGNOSTIC = "diagnostic"
INCOMPLETE = "incomplete"
BLOCKED = "blocked"
ARTIFACT_STATUSES = {CLAIM_READY, DIAGNOSTIC, INCOMPLETE, BLOCKED}
CLAIM_READY_CHECKPOINT_STATUSES = {"loaded", "not_requested"}


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
    checkpoint_bad = [
        row
        for row in rows
        if row.get("checkpoint_required") and row.get("checkpoint_load_status") not in CLAIM_READY_CHECKPOINT_STATUSES
    ]
    diagnostic_labels = sorted({row.get("policy_tag") for row in rows if row.get("diagnostic")})

    if placeholder:
        status = INCOMPLETE
        reasons.append("placeholder_only rows cannot support claim-ready artifacts")
    if "blocked" in row_statuses or "blocked" in execution_statuses or summary.get("execution_status") == "blocked":
        status = BLOCKED
        reasons.append("source study execution is blocked")
    elif row_statuses & {"incomplete", "contract_only"} or execution_statuses & {"incomplete", "contract_only"}:
        status = INCOMPLETE
        reasons.append("source rows are incomplete or contract-only")
    if checkpoint_bad and formal_or_pilot:
        status = BLOCKED
        reasons.append("pilot/formal rows require loaded checkpoint provenance")
    if diagnostic_labels and status == CLAIM_READY and len(diagnostic_labels) == len({row.get("policy_tag") for row in rows}):
        status = DIAGNOSTIC
        reasons.append("all source policies are diagnostic-only")
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

