"""Status-driven manuscript framing and claim guard helpers."""

import json
import shutil
from pathlib import Path

from Src.artifact_status import utc_now_iso


FRAME_FILES = (
    "method_outline.md",
    "experiment_outline.md",
    "result_outline.md",
    "claim_checklist.md",
    "CLAIM_GUARD.json",
)


ALWAYS_ALLOWED_CLAIMS = (
    {
        "id": "robust_time_window_menu_framework",
        "label": "Robust time-window service-menu framework is implemented",
        "rationale": "Core menu logic, contracts, paired replay schema, and artifact gates exist in the repository.",
    },
    {
        "id": "robust_pruning_modes",
        "label": "Robust ETA pruning and soft-penalty modes are available",
        "rationale": "The method can describe hard, calibrated, interval-overlap, chance-constraint, soft-penalty, and none modes.",
    },
    {
        "id": "solver_auditability",
        "label": "Exact-small and greedy-large menu construction is auditable",
        "rationale": "Solver diagnostics record fallback, gap, overlap, candidate count, and build-time metadata.",
    },
    {
        "id": "paired_replay_contracts",
        "label": "Paired replay contracts are defined for fair policy comparisons",
        "rationale": "Study contracts require shared traces, seeds, checkpoints, pricing, and HGS settings.",
    },
    {
        "id": "artifact_status_transparency",
        "label": "Artifact status and blockers are reported transparently",
        "rationale": "Status artifacts expose blocked, incomplete, placeholder, checkpoint, provenance, model-family, outside-option, and accounting state.",
    },
    {
        "id": "model_consistency_contracts",
        "label": "MNL outside-option and method-family contracts are generated metadata",
        "rationale": "Normalized rows record outside_option_util and method_family, while opt-out remains separate from accepted home and meeting-point pickup.",
    },
)


ALWAYS_BLOCKED_CLAIMS = (
    {
        "id": "universal_dominance",
        "label": "Robust menu universally dominates all baselines",
        "reason": "Universal dominance is stronger than any bounded simulation or diagnostic artifact can support.",
    },
    {
        "id": "real_passenger_validation",
        "label": "The choice model is validated on real passenger behavior",
        "reason": "No external survey or revealed-preference validation is part of v1.",
    },
    {
        "id": "no_filter_operational_recommendation",
        "label": "No-filter is recommended as an operational policy",
        "reason": "no_filter_diagnostic is a diagnostic upper bound or stress test, not an operational recommendation.",
    },
    {
        "id": "full_dynamic_exact_optimality",
        "label": "The full dynamic DRT system is solved exactly",
        "reason": "Exact enumeration is limited to small menu candidate sets, with greedy fallback for larger sets.",
    },
    {
        "id": "ungated_dspo_plus_ranking",
        "label": "DSPO_PLUS dominance is established before generated method_family evidence and downstream validation",
        "reason": "DSPO_PLUS ranking is a Phase 10 validation gate, not a Phase 7 assumption.",
    },
)


STRICT_CLAIM_SCHEMA_VERSION = "phase10-strict-claim-guard-v1"

STRICT_CLAIM_DEFINITIONS = (
    {
        "claim_id": "C1_central_adaptive_menu_superiority",
        "claim_text": "Adaptive robust-menu policy superiority over baselines",
        "support_status": "unsupported_blocked",
        "source_families": ("main_rc", "blocker_status"),
        "blocker_reasons": (
            "Main RC artifacts are blocked by checkpoint/formal readiness status.",
            "Positive empirical superiority requires claim-ready generated rows.",
        ),
        "safe_language": (
            "Report the adaptive robust-menu comparison as a generated artifact/status structure.",
            "Describe blockers and required formal-readiness evidence before any superiority claim.",
        ),
        "forbidden_language": (
            "adaptive menu dominates",
            "universal dominance",
            "claim-ready superiority",
            "robust menu is better than all baselines",
        ),
        "manuscript_allowed": False,
        "claim_ready": False,
    },
    {
        "claim_id": "C2_product_ablation_value",
        "claim_text": "Product and time-window ablations identify value drivers",
        "support_status": "conditional_diagnostic_blocked",
        "source_families": ("main_rc", "phase8_sensitivity", "blocker_status"),
        "blocker_reasons": (
            "Product/time-window ablation artifacts are diagnostic until the main RC claim gate is open.",
            "Phase 8 sensitivity artifacts are appendix diagnostics, not claim-ready evidence.",
        ),
        "safe_language": (
            "Use ablation tables as diagnostic structure and boundary evidence.",
            "State that formal claim-ready interpretation is blocked pending evidence gates.",
        ),
        "forbidden_language": (
            "product ablation proves",
            "adaptive window increment is validated",
            "claim-ready ablation value",
        ),
        "manuscript_allowed": False,
        "claim_ready": False,
    },
    {
        "claim_id": "C3_adaptive_window_increment",
        "claim_text": "Adaptive time windows add a positive increment over fixed windows",
        "support_status": "unsupported",
        "source_families": ("main_rc", "phase8_sensitivity"),
        "blocker_reasons": (
            "Current generated artifacts do not provide claim-ready fixed-vs-adaptive increment evidence.",
            "Adaptive-window increment must not be inferred from diagnostic appendices.",
        ),
        "safe_language": (
            "List fixed-window and adaptive-window full-product rows as planned comparison slots.",
            "Avoid directional effect language until claim-ready evidence exists.",
        ),
        "forbidden_language": (
            "adaptive windows improve",
            "adaptive window increment",
            "adaptive window advantage",
        ),
        "manuscript_allowed": False,
        "claim_ready": False,
    },
    {
        "claim_id": "C4_menu_construction_value",
        "claim_text": "Menu construction choices create measurable value",
        "support_status": "conditional_diagnostic_blocked",
        "source_families": ("main_rc", "phase8_sensitivity", "phase9_tractability"),
        "blocker_reasons": (
            "Menu construction diagnostics are available but not claim-ready.",
            "Exact/greedy evidence is computational-boundary evidence only.",
        ),
        "safe_language": (
            "Discuss menu construction as an auditable mechanism with diagnostic artifacts.",
            "Frame exact/greedy rows as computational-boundary evidence.",
        ),
        "forbidden_language": (
            "menu construction proves value",
            "near-optimal greedy",
            "greedy is optimal",
        ),
        "manuscript_allowed": False,
        "claim_ready": False,
    },
    {
        "claim_id": "C5_eta_robustness_boundary",
        "claim_text": "ETA filter and robust time-window modes define diagnostic boundaries",
        "support_status": "diagnostic_only",
        "source_families": ("phase8_sensitivity", "blocker_status"),
        "blocker_reasons": (
            "ETA/no-filter evidence is diagnostic and cannot support operational recommendation language.",
        ),
        "safe_language": (
            "Report ETA and no-filter variants as diagnostic boundary checks.",
            "Keep no-filter as diagnostic-only unless separate formal evidence is produced.",
        ),
        "forbidden_language": (
            "no-filter recommendation",
            "no-filter is operationally recommended",
            "no-filter policy should be deployed",
        ),
        "manuscript_allowed": True,
        "claim_ready": False,
    },
    {
        "claim_id": "C6_exact_greedy_computational_credibility",
        "claim_text": "Exact-small and greedy-large solver behavior supports computational credibility",
        "support_status": "blocked_diagnostic",
        "source_families": ("phase9_tractability", "blocker_status"),
        "blocker_reasons": (
            "Phase 9 exact/greedy outputs are diagnostic computational boundary artifacts.",
            "They cannot authorize near-optimality or full dynamic exact-optimality claims.",
        ),
        "safe_language": (
            "Describe exact-small and greedy-large behavior as auditable computational diagnostics.",
            "Report candidate counts, fallback reasons, build time, and relative gaps where generated.",
        ),
        "forbidden_language": (
            "near-optimal greedy",
            "full dynamic exact optimality",
            "greedy optimality",
        ),
        "manuscript_allowed": False,
        "claim_ready": False,
    },
    {
        "claim_id": "C7_provenance_status_transparency",
        "claim_text": "Artifact status, provenance, and claim gates are transparently reported",
        "support_status": "status_supported",
        "source_families": ("main_rc", "phase8_sensitivity", "phase9_tractability", "blocker_status", "case_scaffold"),
        "blocker_reasons": (),
        "safe_language": (
            "State that generated status artifacts disclose blockers, diagnostic scope, scaffold scope, and claim gates.",
            "Use this claim only for provenance/status transparency, not empirical effectiveness.",
        ),
        "forbidden_language": (
            "status transparency proves effectiveness",
            "provenance resolves empirical blockers",
        ),
        "manuscript_allowed": True,
        "claim_ready": True,
    },
    {
        "claim_id": "C8_semi_real_case_validation",
        "claim_text": "Semi-real case study validates the robust-menu findings",
        "support_status": "scaffold_only_blocked",
        "source_families": ("case_scaffold", "blocker_status"),
        "blocker_reasons": (
            "Case-study files are scaffold-only and contain no validation evidence.",
            "No real passenger behavior or external validation is part of v1.",
        ),
        "safe_language": (
            "Describe the semi-real case materials as a future-study scaffold.",
            "Keep case-study artifacts out of result-table or validation language.",
        ),
        "forbidden_language": (
            "case-study validation",
            "semi-real validation",
            "real passenger behavior",
            "validated on real data",
        ),
        "manuscript_allowed": False,
        "claim_ready": False,
    },
)


def load_artifact_status(path):
    path = Path(path)
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _top_level_flag(status, key):
    artifact_status = status.get("artifact_status") or {}
    return bool(status.get(key, artifact_status.get(key, False)))


def _status_name(status):
    artifact_status = status.get("artifact_status") or {}
    return status.get("status") or artifact_status.get("status") or "unknown"


def _combined_blockers(status):
    blockers = []
    seen = set()
    for item in list(status.get("blockers") or []) + list((status.get("artifact_status") or {}).get("blockers") or []):
        key = (item.get("code"), item.get("message"), item.get("checkpoint_path"))
        if key in seen:
            continue
        seen.add(key)
        blockers.append(item)
    return blockers


def build_claim_guard(status):
    """Return a machine-readable claim guard derived from artifact status JSON."""

    claim_ready = _top_level_flag(status, "claim_ready")
    pilot_claim_ready = _top_level_flag(status, "pilot_claim_ready")
    formal_claim_ready = _top_level_flag(status, "formal_claim_ready")
    blockers = _combined_blockers(status)
    policies = sorted(status.get("policies") or [])
    diagnostic_policies = sorted(
        set((status.get("artifact_status") or {}).get("diagnostic_policy_labels") or [])
        | {policy for policy in policies if "diagnostic" in str(policy)}
    )
    readiness = status.get("formal_readiness") or (status.get("artifact_status") or {}).get("formal_readiness")

    conditional_claims = [
        {
            "id": "pilot_formal_effect_sizes",
            "label": "Pilot/formal effect-size conclusions",
            "allowed": bool(claim_ready and (pilot_claim_ready or formal_claim_ready)),
            "required_status": "claim_ready plus pilot or formal claim readiness",
        },
        {
            "id": "formal_policy_ranking",
            "label": "Formal recommended-policy ranking",
            "allowed": bool(claim_ready and formal_claim_ready),
            "required_status": "formal_claim_ready",
        },
        {
            "id": "diagnostic_result_tables",
            "label": "Diagnostic/status tables and blocked-artifact explanations",
            "allowed": True,
            "required_status": "artifact status available",
        },
    ]

    blocked_claims = list(ALWAYS_BLOCKED_CLAIMS)
    if not claim_ready:
        blocked_claims = blocked_claims + [
            {
                "id": "empirical_superiority",
                "label": "Robust menu empirically improves profit, acceptance, or opt-out versus baselines",
                "reason": "Current artifact status is not claim-ready.",
            },
            {
                "id": "pilot_formal_completed",
                "label": "Pilot/formal experiments are complete and support manuscript results",
                "reason": "Current artifact status is blocked or incomplete.",
            },
        ]

    return {
        "artifact_status": _status_name(status),
        "claim_ready": claim_ready,
        "pilot_claim_ready": pilot_claim_ready,
        "formal_claim_ready": formal_claim_ready,
        "placeholder_only": bool(status.get("placeholder_only", (status.get("artifact_status") or {}).get("placeholder_only", False))),
        "allowed_claims": list(ALWAYS_ALLOWED_CLAIMS),
        "conditional_claims": conditional_claims,
        "blocked_claims": blocked_claims,
        "blockers": blockers,
        "diagnostic_policies": diagnostic_policies,
        "uptake_regimes": sorted(status.get("uptake_regimes") or (status.get("artifact_status") or {}).get("uptake_regimes") or []),
        "source_run_id": status.get("run_id"),
        "source_study": status.get("study"),
        "formal_readiness": readiness,
        "formal_readiness_status": (readiness or {}).get("status"),
    }


def _package_entries(package_indexes):
    if not package_indexes:
        return []
    if "package_index" in package_indexes:
        return list((package_indexes.get("package_index") or {}).get("entries") or [])
    if "entries" in package_indexes:
        return list(package_indexes.get("entries") or [])
    return []


def _package_status(package_indexes):
    if not package_indexes:
        return {}
    if "package_status" in package_indexes:
        return package_indexes.get("package_status") or {}
    return package_indexes.get("status") or {}


def _source_artifacts_for_claim(entries, source_families):
    families = set(source_families)
    artifacts = []
    for entry in entries:
        if entry.get("source_family") not in families:
            continue
        artifacts.append(
            {
                "artifact_id": entry.get("artifact_id"),
                "source_family": entry.get("source_family"),
                "source_path": entry.get("source_path"),
                "package_tier": entry.get("package_tier"),
                "package_role": entry.get("package_role"),
                "status": entry.get("status"),
                "claim_ready": bool(entry.get("claim_ready")),
            }
        )
    return sorted(artifacts, key=lambda item: (item["source_family"] or "", item["source_path"] or "", item["artifact_id"] or ""))


def _artifact_status_blockers(artifact_statuses):
    reasons = []
    if not artifact_statuses:
        return reasons
    for family, status in sorted(artifact_statuses.items()):
        if not isinstance(status, dict):
            continue
        for blocker in _combined_blockers(status):
            code = blocker.get("code", "blocker")
            message = blocker.get("message", code)
            reasons.append(f"{family}: {code}: {message}")
        status_name = _status_name(status)
        if status_name not in {"claim_ready", "completed", "passed", "diagnostic"}:
            reasons.append(f"{family}: status is {status_name}")
        if not _top_level_flag(status, "claim_ready") and family in {"main_rc", "case_scaffold"}:
            reasons.append(f"{family}: claim_ready is false")
    return reasons


def build_strict_claim_guard(package_indexes, artifact_statuses=None):
    """Build the Phase 10 strict per-claim guard without changing the legacy guard."""

    entries = _package_entries(package_indexes)
    package_status = _package_status(package_indexes)
    package_blockers = [
        f"{item.get('artifact_id', 'artifact')}: {item.get('reason', 'blocked')}"
        for item in package_status.get("blockers", [])
    ]
    status_blockers = _artifact_status_blockers(artifact_statuses)
    claims = []
    overall_blockers = []

    for definition in STRICT_CLAIM_DEFINITIONS:
        source_artifacts = _source_artifacts_for_claim(entries, definition["source_families"])
        source_blockers = []
        for artifact in source_artifacts:
            if not artifact["claim_ready"]:
                source_blockers.append(
                    f"{artifact['artifact_id']}: {artifact['package_tier']} artifact is not claim-ready"
                )
        blocker_reasons = sorted(
            set(definition["blocker_reasons"]) | set(source_blockers)
        )
        claim = {
            "claim_id": definition["claim_id"],
            "claim_text": definition["claim_text"],
            "support_status": definition["support_status"],
            "source_artifacts": source_artifacts,
            "blocker_reasons": blocker_reasons,
            "safe_language": list(definition["safe_language"]),
            "forbidden_language": list(definition["forbidden_language"]),
            "manuscript_allowed": bool(definition["manuscript_allowed"]),
            "claim_ready": bool(definition["claim_ready"]),
        }
        claims.append(claim)
        overall_blockers.extend(blocker_reasons)

    overall_blockers.extend(package_blockers)
    overall_blockers.extend(status_blockers)
    blocked_claim_ids = [
        claim["claim_id"]
        for claim in claims
        if not claim["manuscript_allowed"] or claim["support_status"] in {"unsupported", "unsupported_blocked", "blocked_diagnostic", "scaffold_only_blocked"}
    ]

    return {
        "schema_version": STRICT_CLAIM_SCHEMA_VERSION,
        "claim_ready": False,
        "generated_at_utc": utc_now_iso(),
        "source_package_index": {
            "schema_version": (package_indexes.get("package_index") or package_indexes).get("schema_version") if package_indexes else None,
            "artifact_count": len(entries),
            "package_claim_ready": bool(package_status.get("claim_ready", False)),
        },
        "claims": claims,
        "overall_blocker_reasons": sorted(set(overall_blockers)),
        "manuscript_positive_claims_allowed": False,
        "blocked_claim_ids": blocked_claim_ids,
    }


def render_method_outline(guard):
    return "\n".join(
        [
            "# Method Outline",
            "",
            "## Service Bundles",
            "",
            "Each displayed alternative is a service bundle combining a pickup location, pickup time-window handling, and price. Home pickup and meeting-point pickup remain distinct accepted outcomes, while the outside option is represented as opt-out rather than accepted service.",
            "",
            "## Menu Decision",
            "",
            "For each request, the platform chooses a limited displayed menu from feasible candidate bundles. The menu objective combines expected profit, opt-out penalty, ETA risk penalty, and service guardrails.",
            "",
            "## Robust Time Windows",
            "",
            "The method supports hard, calibrated, interval-overlap, chance-constraint, soft-penalty, and no-ETA-pruning diagnostic modes. The no-filter mode disables ETA pruning only and does not disable routing or capacity feasibility.",
            "",
            "## Choice And Pricing",
            "",
            "Passenger selection is modeled with an MNL choice layer over displayed bundles plus an outside option. Normalized rows record the runtime outside_option_util value, and pricing plus system-aware cost definitions are held fixed across paired policy comparisons.",
            "",
            "## Method-Family Metadata",
            "",
            "DSPO and DSPO_PLUS are separated by generated method_family metadata. Current mainline robust-menu rows remain DSPO-side evidence unless an explicit DSPO_PLUS policy tag and row contract are present; attention variants remain diagnostic/V2.",
            "",
            "## Solver",
            "",
            "Small candidate sets use exact enumeration for auditability. Larger candidate sets use greedy forward selection with diagnostics for candidate count, enumerated menu count, build time, relative gap when available, and overlap with exact selections.",
            "",
        ]
    )


def render_experiment_outline(guard):
    policies = guard.get("diagnostic_policies") or ["no_filter_diagnostic"]
    diagnostic_text = ", ".join(policies)
    return "\n".join(
        [
            "# Experiment Outline",
            "",
            "## Scenarios",
            "",
            "The study ladder is smoke, pilot, and formal. Smoke validates contracts and schema and is diagnostic/status evidence only. Pilot rows may support claim-ready artifacts when row, checkpoint, and provenance gates pass. Formal rows require loaded checkpoint provenance plus a dependency snapshot before formal claims are allowed.",
            "",
            "## Mainline Policies",
            "",
            "The V1 mainline family compares no-menu, fixed-menu, random-menu, optimized location-only, optimized location-plus-window, optimized fixed-window full product, and optimized adaptive-window full product settings. These rows carry method_family metadata rather than relying on manual label interpretation.",
            "",
            "## Ranking Boundary",
            "",
            "Recommended-policy ranking excludes the no-menu baseline and includes fixed-menu, random-menu, and the optimized product/time-window variants when source rows are otherwise eligible. no_filter_diagnostic remains diagnostic only.",
            "",
            "## Metrics",
            "",
            "Metrics include net profit, operational cost, total cost, acceptance, opt-out, home share with its total-choice denominator, meeting-point uptake, menu utilization, choice entropy, outside_option_util, method_family, solver build time, exact/greedy quality, and provenance/status fields when available.",
            "",
            "## Paired Replay",
            "",
            "Compared policies must share request traces, seeds, split IDs, pricing mode, checkpoint provenance, routing/HGS settings, and manifest/settings hashes.",
            "",
            "## Checkpoints And Uptake Regimes",
            "",
            f"Current uptake regimes recorded by artifacts: {', '.join(guard.get('uptake_regimes') or ['not available'])}. Diagnostic policies such as {diagnostic_text} are reported as diagnostics only.",
            "",
        ]
    )


def render_result_outline(guard):
    if guard["claim_ready"]:
        evidence_line = "Current artifact status is claim-ready, so result sections may report supported pilot/formal comparisons while still avoiding universal claims."
    else:
        evidence_line = "Current artifact status is not claim-ready. Result sections must remain a report structure and limitation/status discussion, not empirical superiority claims."

    blocker_lines = _render_blocker_lines(guard)
    return "\n".join(
        [
            "# Result Outline",
            "",
            "## Current Evidence Status",
            "",
            evidence_line,
            "",
            *blocker_lines,
            "",
            "## Result Families",
            "",
            "- Mainline ranking: report eligible fixed, random, and optimized product/time-window variants only when source rows are claim-ready.",
            "- Baseline and boundary rows: report no-menu separately from recommended-policy ranking.",
            "- Product ablations: compare optimized m, m+w, and m+w+p variants without treating passenger-facing price as system profit.",
            "- Time-window comparison: separate fixed-window and adaptive-window optimized full-product rows.",
            "- Profit and service decomposition: report profit, operational cost, total cost, acceptance, opt-out, home share, meeting-point uptake, utilization, and choice entropy only when source rows are eligible.",
            "- Model consistency: report outside_option_util and method_family only from generated rows, and keep opt-out separate from accepted home pickup.",
            "- External or semi-real checks: mark as unavailable unless new external validation data is added.",
            "",
            "## Limitations",
            "",
            "- Current evidence is simulation-pipeline evidence, not real passenger behavioral validation.",
            "- no_filter_diagnostic is a diagnostic upper bound or stress test, not an operational recommendation.",
            "- Exact optimality applies only to bounded menu candidate subsets, not the full dynamic DRT system.",
            "- Pilot/formal empirical claims require loaded checkpoint provenance and non-placeholder rows.",
            "",
        ]
    )


def render_claim_checklist(guard):
    lines = [
        "# Claim Checklist",
        "",
        f"- Artifact status: `{guard['artifact_status']}`",
        f"- Claim ready: `{str(guard['claim_ready']).lower()}`",
        f"- Pilot claim ready: `{str(guard['pilot_claim_ready']).lower()}`",
        f"- Formal claim ready: `{str(guard['formal_claim_ready']).lower()}`",
        "",
        "## Allowed Now",
        "",
    ]
    for claim in guard["allowed_claims"]:
        lines.append(f"- [{claim['id']}] {claim['label']} - {claim['rationale']}")
    lines.extend(["", "## Conditional", ""])
    for claim in guard["conditional_claims"]:
        status = "allowed" if claim["allowed"] else "blocked"
        lines.append(f"- [{claim['id']}] {claim['label']} - {status}; requires {claim['required_status']}.")
    lines.extend(["", "## Blocked", ""])
    for claim in guard["blocked_claims"]:
        lines.append(f"- [{claim['id']}] {claim['label']} - {claim['reason']}")
    lines.extend(["", "## Blockers", ""])
    lines.extend(_render_blocker_lines(guard) or ["- None recorded."])
    lines.append("")
    return "\n".join(lines)


def write_manuscript_frame(artifact_root, mirror_root=None):
    artifact_root = Path(artifact_root)
    status = load_artifact_status(artifact_root / "ARTIFACT_STATUS.json")
    guard = build_claim_guard(status)
    output_dir = artifact_root / "manuscript"
    output_dir.mkdir(parents=True, exist_ok=True)

    files = {
        "method_outline.md": render_method_outline(guard),
        "experiment_outline.md": render_experiment_outline(guard),
        "result_outline.md": render_result_outline(guard),
        "claim_checklist.md": render_claim_checklist(guard),
        "CLAIM_GUARD.json": json.dumps(guard, indent=2, sort_keys=True),
    }
    for filename, content in files.items():
        (output_dir / filename).write_text(content.rstrip() + "\n", encoding="utf-8")

    mirror_files = []
    if mirror_root:
        mirror_dir = Path(mirror_root) / "manuscript"
        mirror_dir.mkdir(parents=True, exist_ok=True)
        for filename in files:
            shutil.copy2(output_dir / filename, mirror_dir / filename)
            mirror_files.append(str(mirror_dir / filename))

    return {
        "output_dir": str(output_dir),
        "files": [str(output_dir / filename) for filename in files],
        "mirror_files": mirror_files,
        "claim_guard": guard,
    }


def _render_blocker_lines(guard):
    lines = []
    for blocker in guard.get("blockers") or []:
        code = blocker.get("code", "unknown")
        message = blocker.get("message", "no message")
        path = blocker.get("checkpoint_path")
        if path:
            lines.append(f"- `{code}`: {message} Path: `{path}`.")
        else:
            lines.append(f"- `{code}`: {message}")
    return lines
