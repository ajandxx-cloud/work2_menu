"""Validate Phase 7 planning-side case-study contracts.

The validator intentionally checks only metadata contracts under
.planning/data/case_studies. It does not fetch sources, inspect road graphs,
validate matrix content, import Src.config, or run Work2 study scripts.
"""

import argparse
import json
from pathlib import Path

import yaml


SEVERITIES = {"blocking", "warning", "info"}
STATUS = "scaffolding_only_blocked_execution"
BLOCKER_FIELDS = (
    "case_execution_allowed",
    "result_artifacts_allowed",
    "manuscript_claim_upgrade_allowed",
)
GATE_WORDS = ("provenance", "readiness", "artifact", "claim")
LABELS = ("semi-real", "simulated demand", "simulated choice")
REQUIRED_FILES = (
    "README.md",
    "source_contracts.yaml",
    "route_selection_scorecard.yaml",
    "simulated_demand_protocol.md",
    "case_manifest_draft.yaml",
    "reduced_family_gate.md",
    "claim_boundary_placeholders.md",
)
ROUTE_IDS = ("public_osm_open_network", "yanjiao_beijing_motivated")
ROUTE_FIELDS = (
    "url",
    "access_date",
    "license_access_notes",
    "raw_cache_path_placeholder",
    "hash_placeholder",
    "bbox_or_polygon",
    "tool_versions",
    "parameters",
    "rebuild_commands",
    "labels",
    "blockers",
)
SCORECARD_CRITERIA = (
    "reproducibility",
    "license_clarity",
    "matrix_rebuildability",
    "drt_scenario_plausibility",
    "paper_value",
)
MAINLINE_TAGS = (
    "mainline_no_menu",
    "mainline_fixed_menu",
    "mainline_random_menu",
    "mainline_optimized_m",
    "mainline_optimized_mw",
    "mainline_optimized_fixed_window",
    "mainline_optimized_adaptive",
)
PAIRED_FIELD_REQUIREMENTS = (
    ("seed",),
    ("data_seed",),
    ("data_seed_test",),
    ("instance", "source_route_id"),
    ("checkpoint_path",),
    ("checkpoint_load_status", "checkpoint_hash"),
    ("hgs_reopt_time",),
    ("hgs_final_time",),
    ("menu_k",),
    ("max_candidates",),
    ("home_util",),
    ("base_util",),
    ("incentive_sens",),
    ("outside_option_util",),
    ("uptake_regime",),
)


def _finding(severity, code, message, evidence_location, minimal_fix, rerun_command):
    if severity not in SEVERITIES:
        raise ValueError("invalid severity: " + str(severity))
    return {
        "severity": severity,
        "code": code,
        "message": message,
        "evidence_location": evidence_location,
        "minimal_fix": minimal_fix,
        "rerun_command": rerun_command,
    }


def _rerun(root):
    return "python .planning/data/case_studies/validate_case_contracts.py --root " + str(root).replace("\\", "/") + " --write-summary"


def _read_text(path):
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _read_yaml(path):
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def _require_file(root, filename, findings):
    path = root / filename
    if not path.exists():
        findings.append(
            _finding(
                "blocking",
                "missing_required_file",
                "Required case-study scaffold file is missing: " + filename,
                str(path),
                "Create the missing planning-side contract file.",
                _rerun(root),
            )
        )
    return path


def _check_status_and_blockers(root, filename, findings):
    path = root / filename
    text = _read_text(path)
    if not text:
        return
    if STATUS not in text:
        findings.append(
            _finding(
                "blocking",
                "missing_scaffold_status",
                filename + " does not contain " + STATUS,
                str(path),
                "Add the scaffold-only status to the file.",
                _rerun(root),
            )
        )
    for field in BLOCKER_FIELDS:
        expected = field + ": false"
        if expected not in text:
            findings.append(
                _finding(
                    "blocking",
                    "missing_blocker_field",
                    filename + " is missing " + expected,
                    str(path),
                    "Add all blocker fields with false values.",
                    _rerun(root),
                )
            )
    lowered = text.lower()
    missing_gates = [word for word in GATE_WORDS if word not in lowered]
    if missing_gates:
        findings.append(
            _finding(
                "blocking",
                "missing_unlock_gate_text",
                filename + " does not reference unlock gate(s): " + ", ".join(missing_gates),
                str(path),
                "Reference provenance, readiness, artifact, and claim gates in unlock or boundary text.",
                _rerun(root),
            )
        )


def _check_required_labels(root, filename, findings):
    path = root / filename
    lowered = _read_text(path).lower()
    if not lowered:
        return
    missing = [label for label in LABELS if label not in lowered]
    if missing:
        findings.append(
            _finding(
                "blocking",
                "missing_required_label",
                filename + " is missing required label(s): " + ", ".join(missing),
                str(path),
                "Add semi-real, simulated demand, and simulated choice labels.",
                _rerun(root),
            )
        )


def _check_source_contracts(root, findings):
    path = root / "source_contracts.yaml"
    data = _read_yaml(path)
    routes = data.get("routes") or []
    ids = [route.get("route_id") for route in routes]
    for route_id in ROUTE_IDS:
        if ids.count(route_id) != 1:
            findings.append(
                _finding(
                    "blocking",
                    "invalid_route_contract_ids",
                    "Route ID " + route_id + " must appear exactly once in source_contracts.yaml.",
                    str(path),
                    "Add exactly one route contract with that route_id.",
                    _rerun(root),
                )
            )
    for route in routes:
        route_id = route.get("route_id", "<missing>")
        for field in ROUTE_FIELDS:
            if field not in route:
                findings.append(
                    _finding(
                        "blocking",
                        "missing_route_field",
                        "Route " + str(route_id) + " is missing field " + field,
                        str(path),
                        "Add all required route metadata fields.",
                        _rerun(root),
                    )
                )
        blockers = route.get("blockers") or {}
        for field in BLOCKER_FIELDS:
            if blockers.get(field) is not False:
                findings.append(
                    _finding(
                        "blocking",
                        "route_blocker_not_false",
                        "Route " + str(route_id) + " does not set " + field + " to false.",
                        str(path),
                        "Set all route blocker fields to false.",
                        _rerun(root),
                    )
                )
        labels = " ".join(str(value).lower() for value in route.get("labels") or [])
        for label in LABELS:
            if label not in labels:
                findings.append(
                    _finding(
                        "blocking",
                        "route_missing_label",
                        "Route " + str(route_id) + " is missing label " + label,
                        str(path),
                        "Add all required case-study labels to each route.",
                        _rerun(root),
                    )
                )
        hash_placeholder = route.get("hash_placeholder") or {}
        if not hash_placeholder.get("algorithm") or not hash_placeholder.get("value"):
            findings.append(
                _finding(
                    "blocking",
                    "missing_hash_placeholder",
                    "Route " + str(route_id) + " lacks hash algorithm or placeholder value.",
                    str(path),
                    "Add hash_placeholder.algorithm and hash_placeholder.value.",
                    _rerun(root),
                )
            )
    findings.append(
        _finding(
            "info",
            "source_contract_scope",
            "Source contracts checked at metadata level only; no real source availability was inspected.",
            str(path),
            "No action needed.",
            _rerun(root),
        )
    )


def _check_scorecard(root, findings):
    path = root / "route_selection_scorecard.yaml"
    data = _read_yaml(path)
    if data.get("no_result_based_selection") is not True:
        findings.append(
            _finding(
                "blocking",
                "missing_no_result_rule",
                "Route selection scorecard must set no_result_based_selection: true.",
                str(path),
                "Add no_result_based_selection: true.",
                _rerun(root),
            )
        )
    criteria = data.get("criteria") or {}
    for criterion in SCORECARD_CRITERIA:
        if criterion not in criteria:
            findings.append(
                _finding(
                    "blocking",
                    "missing_scorecard_criterion",
                    "Route selection scorecard is missing criterion " + criterion,
                    str(path),
                    "Add the required predeclared scorecard criterion.",
                    _rerun(root),
                )
            )


def _check_manifest(root, findings):
    path = root / "case_manifest_draft.yaml"
    data = _read_yaml(path)
    if data.get("runtime_manifest_allowed") is not False or data.get("runtime_manifest_path") is not None:
        findings.append(
            _finding(
                "blocking",
                "runtime_manifest_allowed",
                "Planning manifest draft must keep runtime_manifest_allowed false and runtime_manifest_path null.",
                str(path),
                "Reset runtime_manifest_allowed to false and runtime_manifest_path to null.",
                _rerun(root),
            )
        )
    policies = [item.get("tag") for item in data.get("policies") or []]
    for tag in MAINLINE_TAGS:
        if tag not in policies:
            findings.append(
                _finding(
                    "blocking",
                    "missing_mainline_tag",
                    "Case manifest draft is missing policy tag " + tag,
                    str(path),
                    "Add all seven formal mainline policy tags.",
                    _rerun(root),
                )
            )
    paired = set(data.get("paired_fields") or [])
    for accepted_names in PAIRED_FIELD_REQUIREMENTS:
        if not any(name in paired for name in accepted_names):
            findings.append(
                _finding(
                    "blocking",
                    "missing_paired_field",
                    "Case manifest draft is missing paired-field vocabulary: one of " + ", ".join(accepted_names),
                    str(path),
                    "Add paired-field vocabulary inherited from formal_robust_menu.yaml.",
                    _rerun(root),
                )
            )
    blockers = data.get("blockers") or {}
    for field in BLOCKER_FIELDS:
        if blockers.get(field) is not False:
            findings.append(
                _finding(
                    "blocking",
                    "manifest_blocker_not_false",
                    "Manifest draft does not set " + field + " to false.",
                    str(path),
                    "Set all manifest blocker fields to false.",
                    _rerun(root),
                )
            )


def _check_text_contracts(root, findings):
    reduced = root / "reduced_family_gate.md"
    reduced_text = _read_text(reduced).lower()
    for needle in ("policy_tag", "data issue", "contract issue", "unfavorable baseline"):
        if needle not in reduced_text:
            findings.append(
                _finding(
                    "blocking",
                    "missing_reduced_family_field",
                    "Reduced-family gate is missing required text: " + needle,
                    str(reduced),
                    "Add the required reduced-family gate field or protection statement.",
                    _rerun(root),
                )
            )
    claims = root / "claim_boundary_placeholders.md"
    claim_text = _read_text(claims).lower()
    for needle in ("no case evidence yet", "no real passenger", "no manuscript claim upgrade"):
        if needle not in claim_text:
            findings.append(
                _finding(
                    "blocking",
                    "missing_prohibitive_claim_language",
                    "Claim boundary placeholders are missing: " + needle,
                    str(claims),
                    "Add prohibitive placeholder language only.",
                    _rerun(root),
                )
            )


def _check_runtime_manifest_absence(root, repo_root, findings):
    studies_dir = repo_root / "work2_coding" / "Experiments" / "studies"
    leaked = []
    if studies_dir.exists():
        leaked.extend(studies_dir.glob("case_*.yaml"))
        leaked.extend(studies_dir.glob("case_*.yml"))
    if leaked:
        findings.append(
            _finding(
                "blocking",
                "runtime_manifest_leak",
                "Runtime case-study manifest(s) exist under work2_coding/Experiments/studies: "
                + ", ".join(str(path) for path in leaked),
                str(studies_dir),
                "Remove runtime case-study manifests from Phase 7; keep drafts under .planning/data/case_studies/.",
                _rerun(root),
            )
        )
    else:
        findings.append(
            _finding(
                "info",
                "runtime_manifest_absent",
                "No work2_coding/Experiments/studies/case_* runtime manifest was found.",
                str(studies_dir),
                "No action needed.",
                _rerun(root),
            )
        )


def validate(root, repo_root=None):
    root = Path(root)
    repo_root = Path(repo_root) if repo_root is not None else root.resolve().parents[2]
    findings = []
    for filename in REQUIRED_FILES:
        _require_file(root, filename, findings)
    for filename in REQUIRED_FILES:
        _check_status_and_blockers(root, filename, findings)
    for filename in (
        "README.md",
        "source_contracts.yaml",
        "simulated_demand_protocol.md",
        "case_manifest_draft.yaml",
        "claim_boundary_placeholders.md",
    ):
        _check_required_labels(root, filename, findings)
    _check_source_contracts(root, findings)
    _check_scorecard(root, findings)
    _check_manifest(root, findings)
    _check_text_contracts(root, findings)
    _check_runtime_manifest_absence(root, repo_root, findings)
    return findings


def summarize(findings):
    grouped = {severity: [] for severity in ("blocking", "warning", "info")}
    for finding in findings:
        grouped.setdefault(finding["severity"], []).append(finding)
    return grouped


def render_markdown(findings, root):
    grouped = summarize(findings)
    lines = [
        "# Phase 7 Case Contract Validation Summary",
        "",
        "status: scaffolding_only_blocked_execution",
        "case_execution_allowed: false",
        "result_artifacts_allowed: false",
        "manuscript_claim_upgrade_allowed: false",
        "",
        "Labels: semi-real geography/network, simulated demand, simulated choice.",
        "",
        "Validation scope: planning-side metadata contracts only. No external data, road graphs, matrices, demand rows, replay outputs, or runtime manifests were inspected or created.",
        "",
    ]
    for severity in ("blocking", "warning", "info"):
        items = grouped.get(severity, [])
        lines.extend([f"## {severity}", ""])
        if not items:
            lines.extend(["None.", ""])
            continue
        for item in items:
            lines.extend(
                [
                    "- code: `" + item["code"] + "`",
                    "  message: " + item["message"],
                    "  evidence_location: `" + item["evidence_location"] + "`",
                    "  minimal_fix: " + item["minimal_fix"],
                    "  rerun_command: `" + item["rerun_command"] + "`",
                    "",
                ]
            )
    lines.extend(
        [
            "## Machine-Readable Findings",
            "",
            "```json",
            json.dumps(findings, indent=2, sort_keys=True),
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def write_summary(root, findings):
    path = Path(root) / "VALIDATION_SUMMARY.md"
    path.write_text(render_markdown(findings, root), encoding="utf-8")
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".planning/data/case_studies")
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--write-summary", action="store_true")
    args = parser.parse_args(argv)

    root = Path(args.root)
    findings = validate(root, repo_root=args.repo_root)
    if args.write_summary:
        write_summary(root, findings)

    grouped = summarize(findings)
    print(
        "case contract validation: "
        + f"blocking={len(grouped['blocking'])} "
        + f"warning={len(grouped['warning'])} "
        + f"info={len(grouped['info'])}"
    )
    for finding in grouped["blocking"]:
        print("BLOCKING " + finding["code"] + ": " + finding["message"])
    return 1 if grouped["blocking"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
