"""Phase 6 audit matrix for Work2 robust-menu experiment state."""

import json
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

from Src.artifact_status import load_formal_readiness, readiness_metadata, sha256_file, write_json
from Src.experiment_contracts import load_manifest, manifest_hash, resolve_policy_args
from Src.paired_replay import NORMALIZED_ROW_FIELDS, contract_modes
from Src.policy_adapters import adapter_metadata, attention_policy_tags, mainline_policy_tags


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
DEFAULT_OUTPUT_ROOT = ROOT / "outputs" / "phase6_audit"
DEFAULT_READINESS_JSON = ROOT / "outputs" / "phase5_readiness" / "formal_robust_menu" / "FORMAL_READINESS.json"

IMPORT_SMOKE_COMMAND = 'python -c "import sys; sys.path.insert(0, \'.\'); import Src.config; print(\'IMPORT_OK\')"'
PHASE6_AUDIT_COMMAND = "python scripts/audit_phase6_experiment_state.py --output-root outputs/phase6_audit"
READINESS_COMMAND = (
    "python scripts/check_formal_readiness.py --study formal_robust_menu "
    "--output-root outputs/phase5_readiness --diagnostic-ok"
)
FORMAL_REPLAY_COMMAND = "python scripts/run_study.py --study formal_robust_menu --execute --output-root outputs/formal_v1"
CLAIM_READY_ARTIFACT_COMMAND = (
    "python scripts/build_artifacts.py --run-dir <formal-run-dir> --claim-ready "
    "--readiness-json outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json"
)

PHASE6_REQUIREMENTS = ["EXP-01", "EXP-02", "GATE-01", "GATE-02", "GATE-04"]
STUDY_NAMES = ["smoke_robust_menu", "pilot_robust_menu", "formal_robust_menu"]
CANONICAL_AUDIT_FILES = [
    "Src/config.py",
    "Src/Algorithms/DSPO_Menu.py",
    "Src/Algorithms/DSPO.py",
    "Src/policy_adapters.py",
    "Src/experiment_contracts.py",
    "Src/paired_replay.py",
    "Src/study_execution.py",
    "Src/formal_readiness.py",
    "Src/artifact_status.py",
    "Src/artifact_builder.py",
    "Src/manuscript_claims.py",
    "scripts/check_formal_readiness.py",
    "scripts/build_artifacts.py",
    "scripts/build_manuscript_frame.py",
    "Experiments/studies/smoke_robust_menu.yaml",
    "Experiments/studies/pilot_robust_menu.yaml",
    "Experiments/studies/formal_robust_menu.yaml",
    "Experiments/suites/work2_robust_menu.yaml",
    "outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json",
]


def utc_now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _rel(path):
    try:
        return str(Path(path).resolve().relative_to(ROOT.resolve())).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _repo_rel(path):
    try:
        return str(Path(path).resolve().relative_to(REPO_ROOT.resolve())).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _command(command):
    return "cd work2_coding && " + command


def _blocker(reason, minimal_fix, rerun_command, evidence_location, code=None, severity="blocking", **extra):
    item = {
        "reason": reason,
        "minimal_fix": minimal_fix,
        "rerun_command": rerun_command,
        "evidence_location": evidence_location,
        "severity": severity,
    }
    if code:
        item["code"] = code
    item.update(extra)
    return item


def _import_smoke():
    try:
        if str(ROOT) not in sys.path:
            sys.path.insert(0, str(ROOT))
        __import__("Src.config")
        return {
            "import_status": "IMPORT_OK",
            "command": _command(IMPORT_SMOKE_COMMAND),
            "error_type": "",
            "error_message": "",
        }
    except Exception as exc:
        return {
            "import_status": "IMPORT_FAILED",
            "command": _command(IMPORT_SMOKE_COMMAND),
            "error_type": exc.__class__.__name__,
            "error_message": str(exc),
        }


def _canonical_file_status():
    files = []
    for rel_path in CANONICAL_AUDIT_FILES:
        path = ROOT / rel_path
        files.append(
            {
                "path": rel_path,
                "exists": path.exists(),
                "hash": sha256_file(path) if path.exists() and path.is_file() else None,
            }
        )
    return files


def _manifest_summary(name):
    manifest = load_manifest(name)
    fields = manifest.get("output_schema", {}).get("fields", [])
    policy_tags = [policy.get("tag") for policy in manifest.get("policies", [])]
    split_ids = [split.get("split_id") for split in manifest.get("splits", [])]
    split_seed_surface = [
        {
            "split_id": split.get("split_id"),
            "seed": split.get("seed"),
            "data_seed": split.get("data_seed"),
            "data_seed_test": split.get("data_seed_test"),
            "uptake_regime": split.get("uptake_regime"),
            "menu_k": (split.get("args_overrides") or {}).get("menu_k", (manifest.get("base_args") or {}).get("menu_k")),
        }
        for split in manifest.get("splits", [])
    ]
    return {
        "name": manifest["name"],
        "path": _repo_rel(manifest.get("_path", "")),
        "hash": manifest_hash(manifest),
        "tier": manifest.get("tier"),
        "run_mode": manifest.get("run_mode"),
        "instance": (manifest.get("base_args") or {}).get("instance"),
        "split_count": len(manifest.get("splits", [])),
        "split_ids": split_ids,
        "split_seed_surface": split_seed_surface,
        "policy_tags": policy_tags,
        "required_policy_tags": manifest.get("required_policy_tags", []),
        "paired_fields": list(manifest.get("paired_fields", [])),
        "checkpoint_required": bool((manifest.get("shared_checkpoint") or {}).get("required")),
        "checkpoint_path": (manifest.get("shared_checkpoint") or {}).get("path")
        or (manifest.get("base_args") or {}).get("checkpoint_path", ""),
        "normalized_row_v2": bool((manifest.get("output_schema") or {}).get("normalized-row-v2")),
        "output_fields": fields,
        "row_v2_fields_present": sorted(set(fields) & set(NORMALIZED_ROW_FIELDS)),
    }


def _policy_summary(formal_manifest):
    mainline_tags = mainline_policy_tags()
    attention_tags = attention_policy_tags()
    first_split = formal_manifest["splits"][0]
    policies_by_tag = {policy["tag"]: policy for policy in formal_manifest["policies"]}
    mainline = []
    for tag in mainline_tags:
        policy = policies_by_tag[tag]
        args = resolve_policy_args(formal_manifest, first_split, policy)
        product_mode, time_window_mode, menu_mode, pricing_mode = contract_modes(args, policy_metadata=adapter_metadata(tag))
        mainline.append(
            {
                "tag": tag,
                "description": adapter_metadata(tag).get("description", ""),
                "comparison_role": adapter_metadata(tag).get("comparison_role"),
                "product_mode": product_mode,
                "time_window_mode": time_window_mode,
                "menu_mode": menu_mode,
                "pricing_mode": pricing_mode,
                "menu_policy": args.get("menu_policy"),
                "eta_filter_mode": args.get("menu_eta_filter_mode"),
                "v1_claim_ladder_member": True,
            }
        )
    excluded_attention = []
    for tag in attention_tags:
        metadata = adapter_metadata(tag)
        excluded_attention.append(
            {
                "tag": tag,
                "description": metadata.get("description", ""),
                "reason_excluded": "attention-based DSPO is V2/diagnostic and out of Phase 6 V1 claim scope",
                "v1_claim_ladder_member": False,
            }
        )
    return {
        "mainline_tags": mainline_tags,
        "mainline": mainline,
        "excluded_attention_diagnostic_tags": excluded_attention,
        "classification_note": (
            "The current code is the seven-tag mainline robust-menu family; "
            "Phase 6 does not relabel it as DSPO_PLUS or the TR-C target ladder."
        ),
    }


def _pricing_summary(policy_summary):
    modes = {}
    for row in policy_summary["mainline"]:
        modes.setdefault(row["pricing_mode"], []).append(row["tag"])
    static_modes = [mode for mode in modes if mode in {"constant", "flat_markdown", "cost_plus"}]
    gaps = []
    if not static_modes:
        gaps.append(
            _blocker(
                reason="No explicit static-pricing policy/tag is present in the seven-tag mainline family.",
                minimal_fix="Define a static-pricing baseline contract by pricing_mode in Phase 8 before ranking it.",
                rerun_command=_command(PHASE6_AUDIT_COMMAND),
                evidence_location="work2_coding/Src/policy_adapters.py",
                code="static_pricing_contract_missing",
                severity="gap",
            )
        )
    return {
        "pricing_modes_by_tag": modes,
        "source_of_truth": "pricing_mode from resolved policy args / normalized-row-v2 metadata",
        "static_pricing_modes_detected": static_modes,
        "gaps": gaps,
    }


def _rc_dataset_summary(manifest_summaries):
    formal = manifest_summaries["formal_robust_menu"]
    data_root = ROOT / "Environments" / "OOH" / "HombergerGehring_data" / "RC"
    return {
        "instance": formal["instance"],
        "data_root": _rel(data_root),
        "data_root_exists": data_root.exists(),
        "formal_split_count": formal["split_count"],
        "split_seed_surface": formal["split_seed_surface"],
        "trace_identity_fields": [
            "study_name",
            "split_id",
            "seed",
            "data_seed",
            "data_seed_test",
            "instance",
            "max_episodes",
            "max_steps_r",
            "max_steps_p",
            "uptake_regime",
        ],
        "status": "audited" if formal["instance"] == "RC" and data_root.exists() else "blocked",
        "gaps": []
        if formal["instance"] == "RC" and data_root.exists()
        else [
            _blocker(
                reason="Formal manifest does not resolve to an existing RC data root.",
                minimal_fix="Repair the manifest instance or restore HombergerGehring RC data before formal runs.",
                rerun_command=_command("python scripts/test_experiment_contracts.py"),
                evidence_location="work2_coding/Experiments/studies/formal_robust_menu.yaml",
                code="rc_dataset_unavailable",
            )
        ],
    }


def _paired_replay_summary(manifest_summaries):
    formal = manifest_summaries["formal_robust_menu"]
    return {
        "status": "contract_audited",
        "paired_fields": formal["paired_fields"],
        "formal_setting_count": formal["split_count"] * len(formal["policy_tags"]),
        "trace_hash_contract": "Src.paired_replay.trace_identity",
        "verification_command": _command("python scripts/test_policy_fairness_contract.py"),
    }


def _readiness_summary(readiness_json):
    readiness_path = Path(readiness_json or DEFAULT_READINESS_JSON)
    readiness = load_formal_readiness(readiness_path)
    metadata = readiness_metadata(readiness)
    checkpoint = readiness.get("checkpoint") or {}
    dependency = readiness.get("dependency_snapshot") or {}
    blockers = []
    for item in readiness.get("blockers") or []:
        code = item.get("code", "readiness_blocker")
        blockers.append(
            _blocker(
                reason=item.get("message") or code,
                minimal_fix="Clear or intentionally snapshot the blocker, then rerun formal readiness preflight.",
                rerun_command=_command(READINESS_COMMAND),
                evidence_location=_repo_rel(readiness_path),
                code=code,
                git_status_summary=item.get("git_status_summary", ""),
            )
        )
    return {
        "path": _repo_rel(readiness_path),
        "hash": readiness.get("_hash"),
        "status": readiness.get("status"),
        "claim_ready_allowed": bool(readiness.get("claim_ready_allowed")),
        "checkpoint_load_status": checkpoint.get("load_status"),
        "checkpoint_hash": checkpoint.get("hash"),
        "checkpoint_path": checkpoint.get("resolved_path") or checkpoint.get("manifest_path"),
        "dependency_snapshot_path": dependency.get("path"),
        "dependency_snapshot_hash": dependency.get("hash"),
        "blocker_codes": [item.get("code") for item in readiness.get("blockers") or []],
        "blockers": blockers,
        "readiness_command": readiness.get("readiness_command") or _command(READINESS_COMMAND),
        "formal_replay_command": readiness.get("formal_command") or _command(FORMAL_REPLAY_COMMAND),
        "metadata": metadata,
        "notes": readiness.get("notes") or [],
    }


def _artifact_gate_summary(readiness_summary):
    exclusions = [
        _blocker(
            reason="Placeholder-only rows cannot support claim-ready artifacts.",
            minimal_fix="Run the corresponding study to generate completed normalized-row-v2 outputs.",
            rerun_command=_command(FORMAL_REPLAY_COMMAND),
            evidence_location="work2_coding/Src/artifact_status.py",
            code="placeholder_only_excluded",
            severity="gate",
        ),
        _blocker(
            reason="Blocked, failed, incomplete, and contract-only rows are excluded from formal claims.",
            minimal_fix="Fix the failed run state and regenerate rows through the manifest runner.",
            rerun_command=_command(FORMAL_REPLAY_COMMAND),
            evidence_location="work2_coding/Src/artifact_status.py",
            code="bad_row_status_excluded",
            severity="gate",
        ),
        _blocker(
            reason="Pilot/formal rows require loaded checkpoint provenance.",
            minimal_fix="Train or restore the shared checkpoint and rerun readiness.",
            rerun_command=_command(READINESS_COMMAND),
            evidence_location="work2_coding/Src/artifact_status.py",
            code="checkpoint_provenance_required",
            severity="gate",
        ),
        _blocker(
            reason="Smoke, diagnostic, and no-filter-only rows are diagnostic/status evidence only.",
            minimal_fix="Use formal non-diagnostic rows with passed readiness for manuscript ranking claims.",
            rerun_command=_command(CLAIM_READY_ARTIFACT_COMMAND),
            evidence_location="work2_coding/Src/artifact_status.py",
            code="diagnostic_rows_excluded",
            severity="gate",
        ),
    ]
    return {
        "status": "blocked" if not readiness_summary["claim_ready_allowed"] else "ready_for_formal_rows",
        "claim_ready_command": _command(CLAIM_READY_ARTIFACT_COMMAND),
        "exclusions": exclusions,
    }


def _claim_status(readiness_summary):
    blockers = list(readiness_summary["blockers"])
    blockers.append(
        _blocker(
            reason="Formal empirical claims also require completed formal rows and passed claim-ready artifact gates.",
            minimal_fix="After readiness passes, run formal replay and then build claim-ready artifacts from the formal run directory.",
            rerun_command=_command(CLAIM_READY_ARTIFACT_COMMAND),
            evidence_location="work2_coding/outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json",
            code="formal_rows_and_artifacts_required",
            severity="blocking",
        )
    )
    return {
        "claim_ready": False,
        "claim_ready_false": True,
        "safe_manuscript_language": (
            "Implementation and diagnostic gates are auditable, but formal ranking claims remain blocked "
            "until readiness, formal replay, and claim-ready artifact gates pass."
        ),
        "blocked_by": blockers,
    }


def _downstream_gaps(pricing_summary):
    gaps = [
        _blocker(
            reason="The current seven-tag family does not define an explicit DSPO_PLUS ladder member.",
            minimal_fix="Define DSPO and DSPO_PLUS model-family contracts in Phase 7 before full-run validation.",
            rerun_command="gsd-execute-phase 7",
            evidence_location="work2_coding/Src/policy_adapters.py",
            code="dspo_plus_contract_missing",
            severity="gap",
            phase="Phase 7",
        ),
        _blocker(
            reason="No-pricing and static-pricing baselines have not yet been validated under the TR-C ladder.",
            minimal_fix="Run Phase 8 baseline validation with pricing_mode-separated rows.",
            rerun_command="gsd-execute-phase 8",
            evidence_location="work2_coding/Experiments/studies/formal_robust_menu.yaml",
            code="baseline_ladder_pending",
            severity="gap",
            phase="Phase 8",
        ),
        _blocker(
            reason="DSPO clip/wide configurations have not yet been run under paired replay.",
            minimal_fix="Run Phase 9 after baseline gates pass.",
            rerun_command="gsd-execute-phase 9",
            evidence_location=".planning/ROADMAP.md",
            code="dspo_full_run_pending",
            severity="gap",
            phase="Phase 9",
        ),
        _blocker(
            reason="DSPO_PLUS clip/wide configurations and target ranking are unverified.",
            minimal_fix="Run Phase 10 after DSPO family gates pass.",
            rerun_command="gsd-execute-phase 10",
            evidence_location=".planning/ROADMAP.md",
            code="dspo_plus_full_run_pending",
            severity="gap",
            phase="Phase 10",
        ),
        _blocker(
            reason="Manuscript ranking language must wait for claim-ready artifacts.",
            minimal_fix="Write Phase 11 results sections only from passed gates and generated artifacts.",
            rerun_command="gsd-execute-phase 11",
            evidence_location=".planning/ROADMAP.md",
            code="manuscript_claims_pending",
            severity="gap",
            phase="Phase 11",
        ),
    ]
    gaps.extend(pricing_summary.get("gaps") or [])
    return gaps


def _assert_gap_contract(audit):
    gap_like = []
    for section in ("pricing", "rc_dataset"):
        value = audit.get(section) or {}
        gap_like.extend(value.get("gaps") or [])
    gap_like.extend((audit.get("readiness") or {}).get("blockers") or [])
    gap_like.extend((audit.get("artifact_gates") or {}).get("exclusions") or [])
    gap_like.extend((audit.get("claim_status") or {}).get("blocked_by") or [])
    gap_like.extend(audit.get("downstream_gaps") or [])
    required = {"reason", "minimal_fix", "rerun_command", "evidence_location"}
    for item in gap_like:
        missing = [key for key in required if not item.get(key)]
        if missing:
            raise ValueError("audit gap/blocker missing keys: " + ", ".join(missing))


def build_phase6_audit(output_root=None, readiness_json=None):
    """Build an in-memory Phase 6 audit object without running formal replay."""

    runtime = {
        "root": "work2_coding/",
        "generated_at_utc": utc_now_iso(),
        **_import_smoke(),
        "canonical_files": _canonical_file_status(),
        "requirements": list(PHASE6_REQUIREMENTS),
    }
    manifest_summaries = {name: _manifest_summary(name) for name in STUDY_NAMES}
    formal_manifest = load_manifest("formal_robust_menu")
    policies = _policy_summary(formal_manifest)
    pricing = _pricing_summary(policies)
    rc_dataset = _rc_dataset_summary(manifest_summaries)
    paired_replay = _paired_replay_summary(manifest_summaries)
    readiness = _readiness_summary(readiness_json or DEFAULT_READINESS_JSON)
    artifact_gates = _artifact_gate_summary(readiness)
    claim_status = _claim_status(readiness)

    audit = {
        "schema_version": "phase6-audit-v1",
        "phase": "06",
        "phase_name": "Code And Experiment Audit",
        "requirements": list(PHASE6_REQUIREMENTS),
        "runtime": runtime,
        "manifests": manifest_summaries,
        "policies": policies,
        "pricing": pricing,
        "rc_dataset": rc_dataset,
        "paired_replay": paired_replay,
        "readiness": readiness,
        "artifact_gates": artifact_gates,
        "claim_status": claim_status,
        "downstream_gaps": _downstream_gaps(pricing),
        "commands": {
            "import_smoke": _command(IMPORT_SMOKE_COMMAND),
            "phase6_audit": _command(PHASE6_AUDIT_COMMAND),
            "readiness_preflight": _command(READINESS_COMMAND),
            "formal_replay": _command(FORMAL_REPLAY_COMMAND),
            "claim_ready_artifacts": _command(CLAIM_READY_ARTIFACT_COMMAND),
        },
        "non_actions": [
            "formal replay was not executed",
            "generated result rows were not hand-edited",
            "generated tables and figures were not hand-edited",
            "manuscript claims were not advanced",
        ],
    }
    _assert_gap_contract(audit)
    return audit


def write_phase6_audit(output_root=None, readiness_json=None):
    output_root = Path(output_root or DEFAULT_OUTPUT_ROOT)
    audit = build_phase6_audit(output_root=output_root, readiness_json=readiness_json)
    json_path = output_root / "PHASE6_AUDIT.json"
    md_path = output_root / "PHASE6_AUDIT.md"
    write_json(json_path, audit)
    md_path.write_text(markdown_report(audit), encoding="utf-8")
    result = deepcopy(audit)
    result["reports"] = {"json": str(json_path), "markdown": str(md_path)}
    write_json(json_path, result)
    return result


def _table(rows):
    lines = [
        "| Audited object | Status | Risk | Evidence location | Minimal fix | Rerun command |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {name} | {status} | {risk} | `{evidence}` | {fix} | `{cmd}` |".format(
                name=str(row.get("name", "")).replace("|", "\\|"),
                status=str(row.get("status", "")).replace("|", "\\|"),
                risk=str(row.get("risk", "")).replace("|", "\\|"),
                evidence=str(row.get("evidence", "")).replace("|", "\\|"),
                fix=str(row.get("fix", "")).replace("|", "\\|"),
                cmd=str(row.get("cmd", "")).replace("|", "\\|"),
            )
        )
    return "\n".join(lines)


def markdown_report(audit):
    rows = [
        {
            "name": "Runtime import",
            "status": audit["runtime"]["import_status"],
            "risk": "blocks all experiments if failed",
            "evidence": "work2_coding/Src/config.py",
            "fix": "Repair imports under work2_coding/Src.",
            "cmd": audit["commands"]["import_smoke"],
        },
        {
            "name": "Seven-tag mainline family",
            "status": "audited",
            "risk": "mislabeling as DSPO_PLUS would overclaim",
            "evidence": "work2_coding/Src/policy_adapters.py",
            "fix": "Use current mainline labels until Phases 7-10 define the ladder.",
            "cmd": audit["commands"]["phase6_audit"],
        },
        {
            "name": "RC formal manifest",
            "status": "audited" if audit["rc_dataset"]["status"] == "audited" else "blocked",
            "risk": "non-RC or missing split data would invalidate TR-C formal source",
            "evidence": "work2_coding/Experiments/studies/formal_robust_menu.yaml",
            "fix": "Keep instance=RC and restore data root if missing.",
            "cmd": "cd work2_coding && python scripts/test_experiment_contracts.py",
        },
        {
            "name": "Readiness preflight",
            "status": audit["readiness"]["status"],
            "risk": "claim_ready=false until blockers clear",
            "evidence": audit["readiness"]["path"],
            "fix": "Clear dirty-git/formal blockers, then rerun readiness.",
            "cmd": audit["commands"]["readiness_preflight"],
        },
        {
            "name": "Claim-ready artifacts",
            "status": audit["artifact_gates"]["status"],
            "risk": "formal rows and readiness are both required",
            "evidence": "work2_coding/Src/artifact_status.py",
            "fix": "Run formal replay, then build artifacts with --claim-ready.",
            "cmd": audit["commands"]["claim_ready_artifacts"],
        },
    ]
    lines = [
        "# Phase 6 Audit Matrix",
        "",
        f"- Schema: `{audit['schema_version']}`",
        f"- Runtime root: `{audit['runtime']['root']}`",
        f"- Claim-ready: `{str(audit['claim_status']['claim_ready']).lower()}`",
        f"- Readiness status: `{audit['readiness']['status']}`",
        f"- checkpoint_load_status: `{audit['readiness']['checkpoint_load_status']}`",
        f"- claim_ready=false: `{str(audit['claim_status']['claim_ready_false']).lower()}`",
        "",
        "## Audit Matrix",
        "",
        _table(rows),
        "",
        "## Mainline Policy Tags",
        "",
    ]
    for row in audit["policies"]["mainline"]:
        lines.append(
            "- `{tag}`: {product_mode}, {time_window_mode}, {menu_mode}, {pricing_mode}".format(**row)
        )
    lines.extend(
        [
            "",
            "## Excluded Diagnostic/V2 Tags",
            "",
        ]
    )
    for row in audit["policies"]["excluded_attention_diagnostic_tags"]:
        lines.append(f"- `{row['tag']}`: {row['reason_excluded']}")
    lines.extend(
        [
            "",
            "## Blockers And Gaps",
            "",
        ]
    )
    blockers = audit["readiness"]["blockers"] + audit["claim_status"]["blocked_by"] + audit["downstream_gaps"]
    for item in blockers:
        lines.extend(
            [
                f"### {item.get('code', 'gap')}",
                "",
                f"- reason: {item['reason']}",
                f"- minimal_fix: {item['minimal_fix']}",
                f"- rerun_command: `{item['rerun_command']}`",
                f"- evidence_location: `{item['evidence_location']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Copyable Commands",
            "",
            f"- Import smoke: `{audit['commands']['import_smoke']}`",
            f"- Phase 6 audit rerun: `{audit['commands']['phase6_audit']}`",
            f"- Formal readiness preflight: `{audit['commands']['readiness_preflight']}`",
            f"- Formal replay after readiness passes: `{audit['commands']['formal_replay']}`",
            f"- Claim-ready artifact build after formal rows exist: `{audit['commands']['claim_ready_artifacts']}`",
            "",
            "## Boundary",
            "",
            "Formal replay was not run. Generated rows, tables, figures, and manuscript claims were not hand-edited.",
            "",
        ]
    )
    return "\n".join(lines)
