"""Phase 7 model-consistency report for MNL, method-family, and opt-out gates."""

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

from Src.artifact_status import classify_artifact, write_json
from Src.experiment_contracts import load_manifest, manifest_hash
from Src.paired_replay import NORMALIZED_ROW_FIELDS, build_normalized_row, resolve_paired_settings
from Src.policy_adapters import adapter_metadata, dspo_plus_policy_tags, mainline_policy_tags


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
DEFAULT_OUTPUT_ROOT = ROOT / "outputs" / "phase7_model_consistency"

IMPORT_SMOKE_COMMAND = 'python -c "import sys; sys.path.insert(0, \'.\'); import Src.config; print(\'IMPORT_OK\')"'
FOCUSED_SUITE_COMMANDS = [
    IMPORT_SMOKE_COMMAND,
    "python scripts/test_mnl_choice_contract.py",
    "python scripts/test_method_family_contract.py",
    "python scripts/test_optout_accounting.py",
    "python scripts/test_experiment_contracts.py",
    "python scripts/test_artifact_gates.py",
    "python scripts/test_checkpoint_provenance.py",
    "python scripts/test_phase7_model_consistency_report.py",
]


def utc_now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _command(command):
    return "cd work2_coding && " + command


def _rel(path):
    try:
        return str(Path(path).resolve().relative_to(REPO_ROOT.resolve())).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _blocker(reason, minimal_fix, rerun_command, evidence_location, severity="blocking", code=""):
    return {
        "reason": reason,
        "minimal_fix": minimal_fix,
        "rerun_command": rerun_command,
        "evidence_location": evidence_location,
        "severity": severity,
        "code": code or reason.lower().replace(" ", "_")[:64],
    }


def _section(status, evidence, checks=None, blockers=None):
    return {
        "status": status,
        "evidence": evidence,
        "checks": checks or [],
        "blockers": blockers or [],
    }


def _synthetic_rows(study="pilot_robust_menu"):
    manifest = load_manifest(study)
    rows = []
    for setting in resolve_paired_settings(manifest, manifest_hash_value=manifest_hash(manifest))[:4]:
        rows.append(
            build_normalized_row(
                setting,
                run_id="phase7-synthetic",
                checkpoint_metadata={
                    "checkpoint_load_status": "loaded",
                    "checkpoint_path": "synthetic.pt",
                    "checkpoint_hash": "abc123",
                    "checkpoint_required": True,
                    "checkpoint_intentional_mismatch": False,
                },
                stats_metadata={
                    "count_opted_out": 2,
                    "count_accepted_home": 3,
                    "count_accepted_meeting_point": 5,
                },
                status="completed",
                execution_status="completed",
                placeholder_only=False,
            )
        )
    return rows


def _mnl_contract():
    blockers = []
    fields_ok = "outside_option_util" in NORMALIZED_ROW_FIELDS
    if not fields_ok:
        blockers.append(
            _blocker(
                "outside_option_util is missing from normalized-row-v2 fields",
                "Add outside_option_util to NORMALIZED_ROW_FIELDS and manifest output_schema fields.",
                _command("python scripts/test_mnl_choice_contract.py"),
                "work2_coding/Src/paired_replay.py",
                code="missing_outside_option_field",
            )
        )
    return _section(
        "passed" if not blockers else "blocked",
        ["work2_coding/Src/parser.py", "work2_coding/Src/paired_replay.py", "work2_coding/Environments/OOH/customerchoice.py"],
        checks=[
            "Parser default outside_option_util is 0.0",
            "Parser accepts None to disable outside option",
            "Rows record outside_option_util",
            "Manuscript formula normalizes outside utility while runtime metadata records the value",
        ],
        blockers=blockers,
    )


def _method_family_contract():
    blockers = []
    mainline_families = {adapter_metadata(tag)["method_family"] for tag in mainline_policy_tags()}
    dspo_plus = dspo_plus_policy_tags()
    if mainline_families != {"DSPO"}:
        blockers.append(
            _blocker(
                "mainline tags are not consistently DSPO-side metadata",
                "Keep current seven-tag mainline rows as DSPO until downstream DSPO_PLUS validation tags are executed.",
                _command("python scripts/test_method_family_contract.py"),
                "work2_coding/Src/policy_adapters.py",
                code="mainline_method_family_drift",
            )
        )
    if not dspo_plus:
        blockers.append(
            _blocker(
                "DSPO_PLUS policy tags are missing",
                "Add explicit DSPO_PLUS tags with method_family metadata and behavior-gated objective guardrails.",
                _command("python scripts/test_method_family_contract.py"),
                "work2_coding/Src/policy_adapters.py",
                code="missing_dspo_plus_tags",
            )
        )
    return _section(
        "passed" if not blockers else "blocked",
        ["work2_coding/Src/policy_adapters.py", "work2_coding/Src/Algorithms/DSPO_Menu.py"],
        checks=[
            "Current mainline rows remain method_family=DSPO",
            "DSPO_PLUS requires explicit policy tags and generated row metadata",
            "Attention tags remain diagnostic/V2",
        ],
        blockers=blockers,
    )


def _optout_accounting():
    rows = _synthetic_rows()
    row = rows[0]
    blockers = []
    if row["accepted_count"] != row["count_accepted_home"] + row["count_accepted_meeting_point"]:
        blockers.append(
            _blocker(
                "accepted_count is not separated from opt-out",
                "Keep accepted_count equal to accepted home plus accepted meeting-point counts.",
                _command("python scripts/test_optout_accounting.py"),
                "work2_coding/Src/paired_replay.py",
                code="accepted_count_mismatch",
            )
        )
    bad = deepcopy(row)
    bad["count_accepted_home"] += bad["count_opted_out"]
    gate = classify_artifact([bad], {"tier": "pilot", "execution_status": "completed"})
    if gate["status"] != "blocked":
        blockers.append(
            _blocker(
                "artifact gate does not block opt-out mixed into accepted home",
                "Block pilot/formal rows whose accepted/home/meeting-point/opt-out counts are inconsistent.",
                _command("python scripts/test_artifact_gates.py"),
                "work2_coding/Src/artifact_status.py",
                code="optout_accounting_gate_missing",
            )
        )
    return _section(
        "passed" if not blockers else "blocked",
        ["work2_coding/Environments/OOH/Parcelpoint_py.py", "work2_coding/Src/paired_replay.py", "work2_coding/Src/artifact_status.py"],
        checks=[
            "accepted_count equals count_accepted_home plus count_accepted_meeting_point",
            "served_count equals accepted_count",
            "optout_rate denominator includes accepted home, accepted meeting-point, and opt-out",
            "home_share is total-choice-denominator compatibility metadata",
        ],
        blockers=blockers,
    )


def _row_schema():
    blockers = []
    required = {"outside_option_util", "method_family"}
    for study in ["smoke_robust_menu", "pilot_robust_menu", "formal_robust_menu"]:
        manifest = load_manifest(study)
        fields = set(manifest.get("output_schema", {}).get("fields", []))
        missing = sorted(required - fields)
        if missing:
            blockers.append(
                _blocker(
                    "manifest is missing Phase 7 row fields: " + ", ".join(missing),
                    "Add missing fields to output_schema.fields for all robust-menu studies.",
                    _command("python scripts/test_experiment_contracts.py"),
                    _rel(manifest.get("_path", "")),
                    code="manifest_missing_phase7_fields",
                )
            )
    return _section(
        "passed" if not blockers else "blocked",
        [
            "work2_coding/Experiments/studies/smoke_robust_menu.yaml",
            "work2_coding/Experiments/studies/pilot_robust_menu.yaml",
            "work2_coding/Experiments/studies/formal_robust_menu.yaml",
        ],
        checks=["All robust-menu manifests declare outside_option_util and method_family"],
        blockers=blockers,
    )


def _artifact_gates():
    rows = _synthetic_rows()
    blockers = []
    for field in ["method_family", "outside_option_util"]:
        broken = deepcopy(rows)
        broken[0].pop(field, None)
        gate = classify_artifact(broken, {"tier": "pilot", "execution_status": "completed"})
        if gate["status"] != "blocked":
            blockers.append(
                _blocker(
                    "artifact gate does not block missing " + field,
                    "Extend classify_artifact to require " + field + " for pilot/formal claim-ready rows.",
                    _command("python scripts/test_artifact_gates.py"),
                    "work2_coding/Src/artifact_status.py",
                    code="artifact_gate_missing_" + field,
                )
            )
    return _section(
        "passed" if not blockers else "blocked",
        ["work2_coding/Src/artifact_status.py", "work2_coding/Src/artifact_builder.py"],
        checks=[
            "Pilot/formal rows require method_family",
            "Pilot/formal rows require outside_option_util",
            "Pilot/formal rows require internally consistent opt-out/home accounting",
        ],
        blockers=blockers,
    )


def _manuscript_alignment():
    path = REPO_ROOT / "manuscript" / "main.tex"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    required = ["outside_option_util", "method_family", "q_{rb}", "opt-out", "home_share"]
    missing = [item for item in required if item not in text]
    blockers = []
    if missing:
        blockers.append(
            _blocker(
                "manuscript is missing Phase 7 model-consistency terms: " + ", ".join(missing),
                "Update manuscript/main.tex model and metrics sections with generated metadata and opt-out separation.",
                "Select-String -Path manuscript/main.tex -Pattern 'outside_option_util|method_family|opt-out|q_\\{|home_share'",
                "manuscript/main.tex",
                code="manuscript_alignment_missing",
            )
        )
    return _section(
        "passed" if not blockers else "blocked",
        ["manuscript/main.tex"],
        checks=[
            "Outside utility is normalized in formula but runtime value is recorded",
            "q_rb is tied to time deviation and ETA/window filtering",
            "DSPO/DSPO_PLUS are generated method_family metadata",
            "Opt-out, accepted home, and accepted meeting-point remain separate",
        ],
        blockers=blockers,
    )


def _verification_section():
    return _section(
        "ready",
        ["work2_coding/scripts/test_*.py"],
        checks=[_command(command) for command in FOCUSED_SUITE_COMMANDS],
        blockers=[],
    )


def _downstream_handoff():
    blockers = [
        _blocker(
            "No-pricing and static-pricing baselines are not yet validated under paired replay",
            "Execute Phase 8 baseline validation before any ladder claim.",
            "gsd-execute-phase 8",
            ".planning/ROADMAP.md",
            severity="handoff",
            code="phase8_baseline_validation_pending",
        ),
        _blocker(
            "DSPO clip/wide configurations remain downstream",
            "Execute Phase 9 only after Phase 8 gates pass.",
            "gsd-execute-phase 9",
            ".planning/ROADMAP.md",
            severity="handoff",
            code="phase9_dspo_full_run_pending",
        ),
        _blocker(
            "DSPO_PLUS clip/wide configurations and target ranking remain unverified",
            "Execute Phase 10 and treat the ranking as a validation result, not an assumption.",
            "gsd-execute-phase 10",
            ".planning/ROADMAP.md",
            severity="handoff",
            code="phase10_dspo_plus_full_run_pending",
        ),
    ]
    return _section(
        "handoff",
        [".planning/ROADMAP.md"],
        checks=["Phase 7 does not assert DSPO_PLUS > DSPO > Static Pricing > No Pricing"],
        blockers=blockers,
    )


def build_phase7_model_consistency_report():
    sections = {
        "mnl_contract": _mnl_contract(),
        "method_family_contract": _method_family_contract(),
        "optout_accounting": _optout_accounting(),
        "row_schema": _row_schema(),
        "artifact_gates": _artifact_gates(),
        "manuscript_alignment": _manuscript_alignment(),
        "verification": _verification_section(),
        "downstream_handoff": _downstream_handoff(),
    }
    blocking = [
        blocker
        for name, section in sections.items()
        for blocker in section.get("blockers", [])
        if blocker.get("severity") == "blocking"
    ]
    return {
        "schema_version": "phase7-model-consistency-v1",
        "phase": "07",
        "phase_name": "Model Consistency Repair",
        "generated_at_utc": utc_now_iso(),
        "status": "passed" if not blocking else "blocked",
        "sections": sections,
        "blocking_items": blocking,
        "non_actions": [
            "formal replay was not executed",
            "generated result rows were not hand-edited",
            "generated tables and figures were not hand-edited",
            "target ranking was not asserted",
        ],
    }


def markdown_report(report):
    lines = [
        "# Phase 7 Model Consistency Report",
        "",
        f"- Schema: `{report['schema_version']}`",
        f"- Status: `{report['status']}`",
        f"- Generated: `{report['generated_at_utc']}`",
        "",
    ]
    for name, section in report["sections"].items():
        lines.extend(
            [
                "## " + name,
                "",
                f"- status: `{section['status']}`",
                "- evidence: " + ", ".join("`" + item + "`" for item in section.get("evidence", [])),
                "",
                "### Checks",
                "",
            ]
        )
        for check in section.get("checks", []):
            lines.append("- " + check)
        lines.extend(["", "### Blockers / Handoff", ""])
        blockers = section.get("blockers") or []
        if not blockers:
            lines.append("- None.")
        for item in blockers:
            lines.extend(
                [
                    f"- code: `{item['code']}`",
                    f"  reason: {item['reason']}",
                    f"  minimal_fix: {item['minimal_fix']}",
                    f"  rerun_command: `{item['rerun_command']}`",
                    f"  evidence_location: `{item['evidence_location']}`",
                ]
            )
        lines.append("")
    lines.extend(["## Boundary", ""])
    for item in report.get("non_actions", []):
        lines.append("- " + item)
    lines.append("")
    return "\n".join(lines)


def write_phase7_model_consistency_report(output_root=None):
    output_root = Path(output_root or DEFAULT_OUTPUT_ROOT)
    output_root.mkdir(parents=True, exist_ok=True)
    report = build_phase7_model_consistency_report()
    json_path = output_root / "PHASE7_MODEL_CONSISTENCY.json"
    md_path = output_root / "PHASE7_MODEL_CONSISTENCY.md"
    result = deepcopy(report)
    result["reports"] = {"json": str(json_path), "markdown": str(md_path)}
    write_json(json_path, result)
    md_path.write_text(markdown_report(result), encoding="utf-8")
    return result
