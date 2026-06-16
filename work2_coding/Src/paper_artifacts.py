import json
import shutil
from collections import Counter, defaultdict
from pathlib import Path

from Src.artifact_status import utc_now_iso, write_json


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
DEFAULT_MAIN_ARTIFACT_ROOT = ROOT / "artifacts" / "work2_robust_menu"
DEFAULT_PHASE10_OUTPUT_ROOT = DEFAULT_MAIN_ARTIFACT_ROOT / "phase10_paper_artifacts"
DEFAULT_MIRROR_ROOT = REPO_ROOT / "artifacts" / "work2_robust_menu" / "phase10_paper_artifacts"
DEFAULT_PHASE8_ROOT = DEFAULT_MAIN_ARTIFACT_ROOT / "phase8_sensitivity"
DEFAULT_PHASE9_ROOT = DEFAULT_MAIN_ARTIFACT_ROOT / "phase9_tractability"
DEFAULT_CASE_SCAFFOLD_ROOT = REPO_ROOT / ".planning" / "data" / "case_studies"
DEFAULT_RESULTS_ROOT = REPO_ROOT / ".planning" / "results"

SCHEMA_VERSION = "phase10-paper-artifact-package-v1"

MAIN_RC_SECTIONS = [
    "experimental_design",
    "main_rc_results",
    "product_time_window_ablation",
    "eta_time_window_robustness",
    "provenance_and_claim_gates",
]
PHASE8_SECTIONS = [
    "sensitivity_appendix",
    "product_time_window_ablation",
    "eta_time_window_robustness",
    "provenance_and_claim_gates",
]
PHASE9_SECTIONS = [
    "computational_performance_appendix",
    "provenance_and_claim_gates",
]
CASE_SECTIONS = [
    "case_scaffold_appendix",
    "provenance_and_claim_gates",
]
BLOCKER_SECTIONS = [
    "provenance_and_claim_gates",
]

BLOCKED_STATUS = "blocked"
DIAGNOSTIC_STATUS = "diagnostic_provisional_blocked"
SCAFFOLD_STATUS = "scaffold_only_no_result_evidence"

MAIN_GLOBS = [
    ("ARTIFACT_STATUS.json", "status"),
    ("README.md", "readme"),
    ("aggregates/*.json", "aggregate"),
    ("aggregates/*.csv", "aggregate"),
    ("tables/*.tex", "table"),
    ("tables/*.metadata.json", "table_metadata"),
    ("figures/*.png", "figure"),
    ("figures/*.status.json", "figure_status"),
    ("figures/*.metadata.json", "figure_metadata"),
    ("manuscript/CLAIM_GUARD.json", "claim_guard"),
    ("manuscript/*.md", "manuscript_frame"),
]
PHASE8_GLOBS = [
    ("ARTIFACT_STATUS.json", "status"),
    ("ARTIFACT_STATUS.json.metadata.json", "status_metadata"),
    ("aggregates/*.json", "aggregate"),
    ("aggregates/*.csv", "aggregate"),
    ("aggregates/*.metadata.json", "aggregate_metadata"),
    ("tables/*.tex", "table"),
    ("tables/*.metadata.json", "table_metadata"),
    ("figures/*.png", "figure"),
    ("figures/*.metadata.json", "figure_metadata"),
]
PHASE9_GLOBS = [
    ("ARTIFACT_STATUS.json", "status"),
    ("ARTIFACT_STATUS.json.metadata.json", "status_metadata"),
    ("aggregates/*.json", "aggregate"),
    ("aggregates/*.csv", "aggregate"),
    ("aggregates/*.metadata.json", "aggregate_metadata"),
    ("tables/*.tex", "table"),
    ("tables/*.metadata.json", "table_metadata"),
    ("figures/*.png", "figure"),
    ("figures/*.status.json", "figure_status"),
    ("figures/*.metadata.json", "figure_metadata"),
]
CASE_GLOBS = [
    ("*.md", "case_scaffold_doc"),
    ("*.yaml", "case_scaffold_config"),
    ("*.yml", "case_scaffold_config"),
    ("*.json", "case_scaffold_contract"),
    ("*.py", "case_scaffold_validator"),
]
BLOCKER_FILES = [
    "RC_FORMAL_DIAGNOSIS.md",
    "SENSITIVITY_SUMMARY.md",
    "COMPUTATIONAL_TRACTABILITY_SUMMARY.md",
    "FORMAL_BLOCKER_DIAGNOSIS.md",
    "FORMAL_FAILURE_DIAGNOSIS.md",
    "FROZEN_FINAL_SETTINGS.md",
]


def _rel(path):
    path = Path(path)
    try:
        return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _load_json(path, optional=False):
    path = Path(path)
    if not path.exists():
        if optional:
            return {}
        raise FileNotFoundError(path)
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _status_from_payload(payload, default_status):
    if not payload:
        return default_status
    artifact_status = payload.get("artifact_status") or {}
    return payload.get("status") or artifact_status.get("status") or default_status


def _claim_ready_from_payload(payload, default=False):
    if not payload:
        return default
    artifact_status = payload.get("artifact_status") or {}
    return bool(payload.get("claim_ready", artifact_status.get("claim_ready", default)))


def _blockers_from_payload(payload):
    if not payload:
        return []
    blockers = []
    for blocker in payload.get("blockers", []):
        if isinstance(blocker, dict):
            code = blocker.get("code") or blocker.get("reason") or "blocker"
            message = blocker.get("message") or blocker.get("reason") or code
            blockers.append(f"{code}: {message}")
        else:
            blockers.append(str(blocker))
    for blocker in (payload.get("artifact_status") or {}).get("blockers", []):
        if isinstance(blocker, dict):
            code = blocker.get("code") or blocker.get("reason") or "artifact_status_blocker"
            message = blocker.get("message") or blocker.get("reason") or code
            blockers.append(f"{code}: {message}")
        else:
            blockers.append(str(blocker))
    return sorted(set(blockers))


def _artifact_kind(path, role):
    path = Path(path)
    name = path.name
    suffix = path.suffix.lower()
    if name == "ARTIFACT_STATUS.json":
        return "status-json"
    if name.endswith(".status.json"):
        return "figure-status-json"
    if name.endswith(".metadata.json"):
        return "metadata-json"
    if role == "claim_guard":
        return "claim-guard-json"
    if suffix == ".tex":
        return "latex-table"
    if suffix == ".png":
        return "figure"
    if suffix == ".csv":
        return "aggregate-csv"
    if suffix == ".json":
        return "json"
    if suffix == ".md":
        return "markdown"
    if suffix in {".yaml", ".yml"}:
        return "yaml"
    if suffix == ".py":
        return "python"
    return suffix.lstrip(".") or "unknown"


def _artifact_id(source_family, role, path):
    relative = _rel(path)
    safe = "".join(char if char.isalnum() else "_" for char in relative).strip("_").lower()
    return f"{source_family}:{role}:{safe}"


def _entry(
    path,
    source_family,
    role,
    package_tier,
    status,
    claim_ready,
    claim_linkage,
    section_targets,
    blocker_reasons=None,
):
    path = Path(path)
    return classify_phase10_entry(
        {
            "artifact_id": _artifact_id(source_family, role, path),
            "source_family": source_family,
            "source_path": _rel(path),
            "exists": path.exists(),
            "artifact_kind": _artifact_kind(path, role),
            "package_tier": package_tier,
            "package_role": role,
            "status": status,
            "claim_ready": bool(claim_ready),
            "claim_linkage": claim_linkage,
            "section_targets": list(section_targets),
            "blocker_reasons": list(blocker_reasons or []),
        }
    )


def classify_phase10_entry(entry):
    normalized = dict(entry)
    reasons = list(normalized.get("blocker_reasons") or [])
    if not normalized.get("exists"):
        normalized["claim_ready"] = False
        normalized["status"] = BLOCKED_STATUS
        if "source file missing" not in reasons:
            reasons.append("source file missing")

    if normalized["source_family"] in {"phase8_sensitivity", "phase9_tractability"}:
        normalized["package_tier"] = "diagnostic_appendix"
        normalized["claim_ready"] = False
        if normalized.get("status") == "claim_ready":
            normalized["status"] = DIAGNOSTIC_STATUS
        if not any("diagnostic" in reason for reason in reasons):
            reasons.append("diagnostic evidence only; not claim-ready")

    if normalized["source_family"] == "case_scaffold":
        normalized["package_tier"] = "scaffold_only"
        normalized["claim_ready"] = False
        normalized["status"] = SCAFFOLD_STATUS
        if normalized["package_role"] in {"result_table", "result_figure", "figure", "table"}:
            normalized["package_role"] = "case_scaffold"
            normalized["artifact_id"] = normalized["artifact_id"].replace(":figure:", ":case_scaffold:")
            normalized["artifact_id"] = normalized["artifact_id"].replace(":table:", ":case_scaffold:")
        if not any("scaffold" in reason for reason in reasons):
            reasons.append("case-study inputs are scaffold-only and cannot validate results")

    if normalized["source_family"] == "blocker_status":
        normalized["package_tier"] = "blocked_status"
        normalized["claim_ready"] = False
        if not any("blocker" in reason for reason in reasons):
            reasons.append("blocker/status document only")

    normalized["blocker_reasons"] = sorted(set(reasons))
    return normalized


def _append_matches(entries, root, glob_specs, family, tier, status, claim_ready, linkage, sections, missing_role_prefix):
    root = Path(root)
    for pattern, role in glob_specs:
        matches = sorted(path for path in root.glob(pattern) if path.is_file())
        if not matches:
            missing_path = root / pattern.replace("*", "missing")
            entries.append(
                _entry(
                    missing_path,
                    family,
                    role if role != "status" else f"{missing_role_prefix}_status",
                    "blocked_status",
                    BLOCKED_STATUS,
                    False,
                    linkage,
                    sections,
                    ["expected source pattern had no files"],
                )
            )
            continue
        for path in matches:
            entries.append(_entry(path, family, role, tier, status, claim_ready, linkage, sections))


def collect_phase10_sources(source_roots=None):
    roots = {
        "main_rc": DEFAULT_MAIN_ARTIFACT_ROOT,
        "phase8_sensitivity": DEFAULT_PHASE8_ROOT,
        "phase9_tractability": DEFAULT_PHASE9_ROOT,
        "case_scaffold": DEFAULT_CASE_SCAFFOLD_ROOT,
        "blocker_status": DEFAULT_RESULTS_ROOT,
    }
    if source_roots:
        roots.update({key: Path(value) for key, value in source_roots.items() if value is not None})

    entries = []

    main_status_payload = _load_json(roots["main_rc"] / "ARTIFACT_STATUS.json", optional=True)
    main_status = _status_from_payload(main_status_payload, BLOCKED_STATUS)
    main_claim_ready = _claim_ready_from_payload(main_status_payload, default=False)
    main_blockers = _blockers_from_payload(main_status_payload)
    _append_matches(
        entries,
        roots["main_rc"],
        MAIN_GLOBS,
        "main_rc",
        "main_paper_candidate",
        main_status,
        main_claim_ready,
        "main RC artifact package; promotion depends on explicit claim gate",
        MAIN_RC_SECTIONS,
        "main_rc",
    )
    for entry in entries:
        if entry["source_family"] == "main_rc" and entry["blocker_reasons"] == [] and main_blockers:
            entry["blocker_reasons"] = list(main_blockers)

    phase8_status_payload = _load_json(roots["phase8_sensitivity"] / "ARTIFACT_STATUS.json", optional=True)
    _append_matches(
        entries,
        roots["phase8_sensitivity"],
        PHASE8_GLOBS,
        "phase8_sensitivity",
        "diagnostic_appendix",
        _status_from_payload(phase8_status_payload, DIAGNOSTIC_STATUS),
        False,
        "Phase 8 diagnostic sensitivity appendix only",
        PHASE8_SECTIONS,
        "phase8",
    )

    phase9_status_payload = _load_json(roots["phase9_tractability"] / "ARTIFACT_STATUS.json", optional=True)
    _append_matches(
        entries,
        roots["phase9_tractability"],
        PHASE9_GLOBS,
        "phase9_tractability",
        "diagnostic_appendix",
        _status_from_payload(phase9_status_payload, DIAGNOSTIC_STATUS),
        False,
        "Phase 9 diagnostic computational appendix only",
        PHASE9_SECTIONS,
        "phase9",
    )

    _append_matches(
        entries,
        roots["case_scaffold"],
        CASE_GLOBS,
        "case_scaffold",
        "scaffold_only",
        SCAFFOLD_STATUS,
        False,
        "semi-real case scaffold; no empirical validation claim authorized",
        CASE_SECTIONS,
        "case",
    )

    for name in BLOCKER_FILES:
        path = roots["blocker_status"] / name
        entries.append(
            _entry(
                path,
                "blocker_status",
                "blocker_status",
                "blocked_status",
                BLOCKED_STATUS,
                False,
                "formal blocker and claim-boundary provenance",
                BLOCKER_SECTIONS,
                [] if path.exists() else ["required blocker/status document missing"],
            )
        )

    unique = {}
    for entry in entries:
        unique[entry["artifact_id"]] = entry
    return sorted(unique.values(), key=lambda item: (item["source_family"], item["source_path"], item["package_role"]))


def build_package_indexes(entries):
    entries = sorted((classify_phase10_entry(entry) for entry in entries), key=lambda item: item["artifact_id"])
    source_index = defaultdict(list)
    section_map = defaultdict(list)
    blockers = []

    for entry in entries:
        source_index[entry["source_family"]].append(entry["artifact_id"])
        if entry["source_family"] == "case_scaffold" and entry["package_role"] in {"result_table", "result_figure"}:
            continue
        for target in entry["section_targets"]:
            section_map[target].append(entry["artifact_id"])
        for reason in entry["blocker_reasons"]:
            blockers.append(
                {
                    "artifact_id": entry["artifact_id"],
                    "source_family": entry["source_family"],
                    "reason": reason,
                }
            )

    family_counts = Counter(entry["source_family"] for entry in entries)
    tier_counts = Counter(entry["package_tier"] for entry in entries)
    role_counts = Counter(entry["package_role"] for entry in entries)
    family_status = {}
    for family in sorted(family_counts):
        family_entries = [entry for entry in entries if entry["source_family"] == family]
        family_status[family] = {
            "artifact_count": len(family_entries),
            "existing_artifact_count": sum(1 for entry in family_entries if entry["exists"]),
            "claim_ready": all(entry["claim_ready"] for entry in family_entries) if family_entries else False,
            "statuses": sorted({entry["status"] for entry in family_entries}),
            "package_tiers": sorted({entry["package_tier"] for entry in family_entries}),
        }

    package_status = {
        "schema_version": SCHEMA_VERSION,
        "generated_at_utc": utc_now_iso(),
        "claim_ready": False,
        "claim_ready_reason": "Phase 10 package is a provenance and paper-artifact index; positive claims remain blocked unless strict guards allow them.",
        "artifact_count": len(entries),
        "existing_artifact_count": sum(1 for entry in entries if entry["exists"]),
        "missing_artifact_count": sum(1 for entry in entries if not entry["exists"]),
        "source_family_counts": dict(sorted(family_counts.items())),
        "package_tier_counts": dict(sorted(tier_counts.items())),
        "package_role_counts": dict(sorted(role_counts.items())),
        "source_family_status": family_status,
        "blocker_count": len(blockers),
        "blockers": blockers,
    }

    return {
        "package_index": {
            "schema_version": SCHEMA_VERSION,
            "generated_at_utc": package_status["generated_at_utc"],
            "claim_ready": False,
            "entries": entries,
        },
        "source_index": {
            "schema_version": SCHEMA_VERSION,
            "generated_at_utc": package_status["generated_at_utc"],
            "source_families": {family: sorted(ids) for family, ids in sorted(source_index.items())},
        },
        "artifact_to_section_map": {
            "schema_version": SCHEMA_VERSION,
            "generated_at_utc": package_status["generated_at_utc"],
            "sections": {section: sorted(ids) for section, ids in sorted(section_map.items())},
        },
        "package_status": package_status,
    }


def render_readme(indexes):
    status = indexes["package_status"]
    lines = [
        "# Phase 10 Paper Artifact Package",
        "",
        f"- schema_version: {SCHEMA_VERSION}",
        f"- claim_ready: {str(status['claim_ready']).lower()}",
        f"- artifact_count: {status['artifact_count']}",
        f"- missing_artifact_count: {status['missing_artifact_count']}",
        "",
        "This package indexes generated artifacts, diagnostic appendices, case scaffold files, and blocker/status documents for the Work2 robust menu paper.",
        "It does not promote diagnostic or scaffold artifacts into claim-ready manuscript evidence.",
        "",
        "## Source Families",
    ]
    for family, family_status in status["source_family_status"].items():
        lines.append(
            f"- {family}: {family_status['artifact_count']} artifacts, "
            f"claim_ready={str(family_status['claim_ready']).lower()}, "
            f"tiers={', '.join(family_status['package_tiers'])}"
        )
    return "\n".join(lines) + "\n"


def render_artifact_to_section_map(indexes):
    entries_by_id = {entry["artifact_id"]: entry for entry in indexes["package_index"]["entries"]}
    lines = [
        "# Artifact To Section Map",
        "",
        "Each section lists artifact IDs and their source paths. Diagnostic and scaffold entries remain marked as not claim-ready.",
    ]
    for section, artifact_ids in indexes["artifact_to_section_map"]["sections"].items():
        lines.extend(["", f"## {section}"])
        for artifact_id in artifact_ids:
            entry = entries_by_id[artifact_id]
            lines.append(
                f"- `{artifact_id}`: {entry['source_path']} "
                f"({entry['package_tier']}, claim_ready={str(entry['claim_ready']).lower()})"
            )
    return "\n".join(lines) + "\n"


def render_claim_checklist(indexes, strict_guard=None):
    status = indexes["package_status"]
    lines = [
        "# Phase 10 Claim Checklist",
        "",
        "- overall_claim_ready: false",
        "- positive empirical manuscript claims: blocked pending strict claim guard and formal evidence",
        "- no-filter policy: diagnostic only",
        "- semi-real case scaffold: scaffold only; no validation claim authorized",
    ]
    if strict_guard:
        lines.extend(
            [
                f"- strict_claim_guard_claim_ready: {str(strict_guard['claim_ready']).lower()}",
                f"- manuscript_positive_claims_allowed: {str(strict_guard['manuscript_positive_claims_allowed']).lower()}",
                "",
                "## Strict Claims",
            ]
        )
        for claim in strict_guard["claims"]:
            lines.append(
                f"- `{claim['claim_id']}`: {claim['support_status']}; "
                f"manuscript_allowed={str(claim['manuscript_allowed']).lower()}; "
                f"claim_ready={str(claim['claim_ready']).lower()}"
            )
    lines.extend(
        [
            "",
            "## Blocking Reasons",
        ]
    )
    if not status["blockers"]:
        lines.append("- No source blockers were indexed, but Phase 10 remains claim_ready=false by policy.")
    else:
        for blocker in status["blockers"][:80]:
            lines.append(f"- `{blocker['artifact_id']}`: {blocker['reason']}")
        if len(status["blockers"]) > 80:
            lines.append(f"- ... {len(status['blockers']) - 80} additional blocker entries omitted from markdown")
    return "\n".join(lines) + "\n"


def render_safe_language_boundaries(strict_guard):
    lines = [
        "# Safe Language Boundaries",
        "",
        f"- schema_version: {strict_guard['schema_version']}",
        f"- claim_ready: {str(strict_guard['claim_ready']).lower()}",
        f"- manuscript_positive_claims_allowed: {str(strict_guard['manuscript_positive_claims_allowed']).lower()}",
    ]
    for claim in strict_guard["claims"]:
        lines.extend(["", f"## {claim['claim_id']}", "", "Allowed framing:"])
        for text in claim["safe_language"]:
            lines.append(f"- {text}")
        lines.extend(["", "Forbidden framing:"])
        for text in claim["forbidden_language"]:
            lines.append(f"- {text}")
    return "\n".join(lines) + "\n"


def _write_markdown_outputs(output_root, indexes, strict_guard=None):
    paths = {}
    markdown = {
        "README.md": render_readme(indexes),
        "artifact_to_section_map.md": render_artifact_to_section_map(indexes),
        "claim_checklist.md": render_claim_checklist(indexes, strict_guard=strict_guard),
    }
    if strict_guard:
        markdown["safe_language_boundaries.md"] = render_safe_language_boundaries(strict_guard)
    for name, text in markdown.items():
        path = output_root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        paths[name] = path
    return paths


def _mirror_outputs(output_root, mirror_root):
    mirror_root = Path(mirror_root)
    if mirror_root.exists():
        shutil.rmtree(mirror_root)
    mirror_root.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(output_root, mirror_root)
    return mirror_root


def write_phase10_package(output_root=None, mirror_root=DEFAULT_MIRROR_ROOT, source_roots=None):
    output_root = Path(output_root or DEFAULT_PHASE10_OUTPUT_ROOT)
    mirror_enabled = mirror_root is not False and mirror_root is not None
    mirror_root = Path(mirror_root) if mirror_enabled else None
    output_root.mkdir(parents=True, exist_ok=True)

    entries = collect_phase10_sources(source_roots=source_roots)
    indexes = build_package_indexes(entries)
    from Src.manuscript_claims import build_strict_claim_guard

    strict_guard = build_strict_claim_guard(indexes)
    claim_guard_path = output_root / "CLAIM_GUARD.json"
    indexes["package_status"].update(
        {
            "strict_claim_guard_path": _rel(claim_guard_path),
            "strict_claim_guard_claim_ready": bool(strict_guard["claim_ready"]),
            "manuscript_positive_claims_allowed": bool(strict_guard["manuscript_positive_claims_allowed"]),
            "blocked_claim_ids": list(strict_guard["blocked_claim_ids"]),
        }
    )
    json_outputs = {
        "PACKAGE_INDEX.json": indexes["package_index"],
        "SOURCE_INDEX.json": indexes["source_index"],
        "ARTIFACT_TO_SECTION_MAP.json": indexes["artifact_to_section_map"],
        "PACKAGE_STATUS.json": indexes["package_status"],
        "CLAIM_GUARD.json": strict_guard,
    }
    paths = {}
    for name, payload in json_outputs.items():
        path = output_root / name
        write_json(path, payload)
        paths[name] = path
    paths.update(_write_markdown_outputs(output_root, indexes, strict_guard=strict_guard))
    mirror_path = _mirror_outputs(output_root, mirror_root) if mirror_enabled else None
    return {
        "output_root": str(output_root),
        "mirror_root": str(mirror_path) if mirror_path else None,
        "claim_ready": indexes["package_status"]["claim_ready"],
        "artifact_count": indexes["package_status"]["artifact_count"],
        "missing_artifact_count": indexes["package_status"]["missing_artifact_count"],
        "blocker_count": indexes["package_status"]["blocker_count"],
        "paths": {name: str(path) for name, path in sorted(paths.items())},
    }
