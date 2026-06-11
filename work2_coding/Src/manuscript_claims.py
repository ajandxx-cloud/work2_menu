"""Status-driven manuscript framing and claim guard helpers."""

import json
import shutil
from pathlib import Path


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
        "rationale": "Phase 4 status artifacts expose blocked, incomplete, placeholder, checkpoint, and provenance state.",
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
            "Passenger selection is modeled with an MNL choice layer over displayed bundles plus an outside option. Pricing and system-aware cost definitions are held fixed across paired policy comparisons.",
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
            "The study ladder is smoke, pilot, and formal. Smoke validates contracts and schema. Pilot and formal tiers require loaded checkpoint provenance before they can support manuscript claims.",
            "",
            "## Baselines",
            "",
            "Policy comparisons include full display, home only, nearest heuristic, top-k cheapest, min-lateness, hard filter, robust risk-adjusted, robust service-guarded, optional random top-k, and diagnostic no-filter.",
            "",
            "## Metrics",
            "",
            "Metrics include expected or realized net profit, acceptance, opt-out, non-home uptake, ETA pruning behavior, service-quality diagnostics, solver build time, exact/greedy quality, and provenance/status fields.",
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
            "- Exact-vs-greedy quality: report candidate counts, build time, gap/overlap diagnostics, and fallback reason.",
            "- Robust filtering comparison: report pruning diagnostics, ETA-risk behavior, and feasibility-preserving no-filter diagnostics.",
            "- Uptake-regime behavior: report low/medium regime coverage when available and avoid extrapolating beyond covered regimes.",
            "- Profit decomposition: report profit, acceptance, opt-out, route/service cost, and uncertainty/gap outputs only when source rows are claim-ready.",
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
