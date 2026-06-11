"""Attention-vs-original DSPO artifact helpers."""

import csv
import json
import math
import shutil
from collections import defaultdict
from pathlib import Path

from Src.artifact_builder import load_run, latest_run_dir, write_latex_table
from Src.artifact_status import utc_now_iso, write_json
from Src.study_execution import collect_git_provenance


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = ROOT / "artifacts" / "work2_attention_dspo"
DEFAULT_STUDY_OUTPUT_ROOT = ROOT / "outputs" / "studies"
DEFAULT_MIRROR_ROOT = ROOT.parent / "artifacts" / "work2_attention_dspo"

PRIMARY_METRIC = "net_objective_proxy"
DELTA_METRICS = [
    "net_objective_proxy",
    "acceptance_rate",
    "optout_rate",
    "meeting_point_uptake_rate",
    "service_time_total",
    "net_price_revenue",
]
SERVICE_CONSTRAINTS = {
    "acceptance_rate": {"direction": "not_lower", "tolerance": 0.05},
    "optout_rate": {"direction": "not_higher", "tolerance": 0.05},
    "meeting_point_uptake_rate": {"direction": "not_lower", "tolerance": 0.05},
    "service_time_total": {"direction": "not_higher_relative", "tolerance": 0.05},
}
CLAIM_READY_CHECKPOINT_STATUSES = {"loaded", "not_requested"}


def _num(value):
    if value in (None, "", "NA"):
        return None
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(value):
        return None
    return value


def _mean(values):
    values = [_num(value) for value in values]
    values = [value for value in values if value is not None]
    return sum(values) / len(values) if values else None


def _delta(attention_value, original_value):
    attention_value = _num(attention_value)
    original_value = _num(original_value)
    if attention_value is None or original_value is None:
        return None
    return float(attention_value - original_value)


def _row_by_method(rows):
    by_method = {}
    for row in rows:
        method = row.get("method_variant") or row.get("policy_tag")
        by_method[method] = row
    return by_method


def attention_pair_deltas(rows):
    groups = defaultdict(list)
    for row in rows:
        pair_id = row.get("attention_pair_id") or "missing-pair-id"
        groups[pair_id].append(row)

    deltas = []
    for pair_id in sorted(groups):
        group = groups[pair_id]
        by_method = _row_by_method(group)
        original = by_method.get("DSPO_original")
        attention = by_method.get("DSPO_attention")
        pair_complete = bool(original and attention)
        template = attention or original or group[0]
        delta_row = {
            "attention_pair_id": pair_id,
            "pair_complete": pair_complete,
            "study_name": template.get("study_name"),
            "tier": template.get("tier"),
            "run_mode": template.get("run_mode"),
            "split_id": template.get("split_id"),
            "seed": template.get("seed"),
            "trace_id": template.get("trace_id"),
            "original_status": None if original is None else original.get("status"),
            "attention_status": None if attention is None else attention.get("status"),
            "original_execution_status": None if original is None else original.get("execution_status"),
            "attention_execution_status": None if attention is None else attention.get("execution_status"),
            "original_placeholder_only": True if original is None else bool(original.get("placeholder_only")),
            "attention_placeholder_only": True if attention is None else bool(attention.get("placeholder_only")),
            "original_checkpoint_load_status": None if original is None else original.get("checkpoint_load_status"),
            "attention_checkpoint_load_status": None if attention is None else attention.get("checkpoint_load_status"),
            "checkpoint_required": bool((original or {}).get("checkpoint_required") or (attention or {}).get("checkpoint_required")),
        }
        for metric in DELTA_METRICS:
            original_value = None if original is None else original.get(metric)
            attention_value = None if attention is None else attention.get(metric)
            delta_row[metric + "_original"] = original_value
            delta_row[metric + "_attention"] = attention_value
            delta_row[metric + "_delta"] = _delta(attention_value, original_value)
        original_summary = (original or {}).get("attention_weight_summary") or {}
        attention_summary = (attention or {}).get("attention_weight_summary") or {}
        delta_row["attention_weight_mean_original"] = original_summary.get("attention_weight_mean")
        delta_row["attention_weight_mean_attention"] = attention_summary.get("attention_weight_mean")
        delta_row["attention_weight_mean_delta"] = _delta(
            attention_summary.get("attention_weight_mean"),
            original_summary.get("attention_weight_mean"),
        )
        deltas.append(delta_row)
    return deltas


def aggregate_attention_deltas(delta_rows):
    completed = [
        row for row in delta_rows
        if row.get("pair_complete") and row.get(PRIMARY_METRIC + "_delta") is not None
    ]
    aggregate = {
        "pair_count": len(delta_rows),
        "complete_pair_count": len([row for row in delta_rows if row.get("pair_complete")]),
        "metric_means": {},
    }
    for metric in DELTA_METRICS:
        aggregate["metric_means"][metric + "_delta_mean"] = _mean(row.get(metric + "_delta") for row in completed)
        aggregate["metric_means"][metric + "_original_mean"] = _mean(row.get(metric + "_original") for row in completed)
        aggregate["metric_means"][metric + "_attention_mean"] = _mean(row.get(metric + "_attention") for row in completed)
    return aggregate


def _checkpoint_valid(row):
    if not row.get("checkpoint_required"):
        return True
    statuses = {row.get("original_checkpoint_load_status"), row.get("attention_checkpoint_load_status")}
    return statuses.issubset(CLAIM_READY_CHECKPOINT_STATUSES)


def _constraint_result(metric, mean_delta, original_mean):
    spec = SERVICE_CONSTRAINTS[metric]
    tolerance = float(spec["tolerance"])
    if mean_delta is None:
        return {"metric": metric, "passed": False, "reason": "metric unavailable"}
    if spec["direction"] == "not_lower":
        passed = mean_delta >= -tolerance
        reason = "" if passed else "attention materially lowers " + metric
    elif spec["direction"] == "not_higher":
        passed = mean_delta <= tolerance
        reason = "" if passed else "attention materially raises " + metric
    else:
        base = abs(_num(original_mean) or 0.0)
        allowed = max(tolerance * base, tolerance)
        passed = mean_delta <= allowed
        reason = "" if passed else "attention materially raises " + metric
    return {
        "metric": metric,
        "passed": bool(passed),
        "delta_mean": mean_delta,
        "tolerance": tolerance,
        "reason": reason,
    }


def attention_claim_guard(rows, delta_rows, summary=None):
    summary = summary or {}
    blockers = []
    blocked_claims = []
    aggregate = aggregate_attention_deltas(delta_rows)
    metric_means = aggregate["metric_means"]
    tiers = sorted({row.get("tier") for row in rows if row.get("tier")})
    statuses = sorted({row.get("status") for row in rows if row.get("status")})
    execution_statuses = sorted({row.get("execution_status") for row in rows if row.get("execution_status")})
    checkpoint_statuses = sorted({row.get("checkpoint_load_status") for row in rows if row.get("checkpoint_load_status")})
    placeholder = any(bool(row.get("placeholder_only")) for row in rows)

    if not rows:
        blockers.append({"code": "no_rows", "message": "No normalized attention rows are available."})
    if not delta_rows:
        blockers.append({"code": "no_pairs", "message": "No attention pairs can be constructed."})
    if "smoke" in tiers and not (set(tiers) & {"pilot", "formal"}):
        blockers.append({"code": "smoke_only", "message": "Smoke evidence validates schema/execution only, not improvement claims."})
    if placeholder:
        blockers.append({"code": "placeholder_rows", "message": "Placeholder rows cannot support attention improvement claims."})
    if statuses != ["completed"] or execution_statuses != ["completed"]:
        blockers.append({"code": "incomplete_rows", "message": "All attention rows must be completed."})
    incomplete_pairs = [row["attention_pair_id"] for row in delta_rows if not row.get("pair_complete")]
    if incomplete_pairs:
        blockers.append({"code": "incomplete_pairs", "message": "Missing original or attention row.", "pairs": incomplete_pairs})
    bad_checkpoint_pairs = [row["attention_pair_id"] for row in delta_rows if not _checkpoint_valid(row)]
    if bad_checkpoint_pairs:
        blockers.append({"code": "checkpoint_invalid", "message": "Pilot/formal attention claims require loaded checkpoint provenance.", "pairs": bad_checkpoint_pairs})

    primary_delta = metric_means.get(PRIMARY_METRIC + "_delta_mean")
    if primary_delta is None or primary_delta <= 0.0:
        blockers.append({"code": "primary_metric_not_positive", "message": "Attention does not improve the primary net objective proxy."})

    service_constraints = {}
    for metric in SERVICE_CONSTRAINTS:
        result = _constraint_result(
            metric,
            metric_means.get(metric + "_delta_mean"),
            metric_means.get(metric + "_original_mean"),
        )
        service_constraints[metric] = result
        if not result["passed"]:
            blockers.append({"code": "service_constraint_failed", "message": result["reason"], "metric": metric})

    if blockers:
        blocked_claims.append({
            "id": "attention_improves_dspo",
            "label": "Attention improves DSPO over the original method",
            "reason": "Fail-closed guard found blockers.",
        })

    allowed = not blockers
    return {
        "generated_at": utc_now_iso(),
        "claim_ready": bool(allowed),
        "attention_improves_dspo_allowed": bool(allowed),
        "primary_metric": {
            "name": PRIMARY_METRIC,
            "delta_mean": primary_delta,
            "direction": "higher_is_better",
        },
        "service_constraints": service_constraints,
        "pair_completeness": {
            "pair_count": aggregate["pair_count"],
            "complete_pair_count": aggregate["complete_pair_count"],
            "all_pairs_complete": aggregate["pair_count"] > 0 and aggregate["pair_count"] == aggregate["complete_pair_count"],
        },
        "checkpoint_statuses": checkpoint_statuses,
        "row_statuses": statuses,
        "execution_statuses": execution_statuses,
        "tiers": tiers,
        "blocked_claims": blocked_claims,
        "blockers": blockers,
        "source_run_id": summary.get("run_id"),
        "source_study": summary.get("study_name"),
        "aggregate": aggregate,
    }


def write_csv(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row.keys()})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fields})


def mirror_lightweight_artifacts(src_root, mirror_root):
    mirror_root = Path(mirror_root)
    if mirror_root.exists():
        shutil.rmtree(mirror_root)
    for path in Path(src_root).rglob("*"):
        if path.is_dir():
            continue
        rel = path.relative_to(src_root)
        dest = mirror_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)


def build_attention_artifacts(run_dir, output_root=None, mirror_root=None, allow_incomplete=False):
    run_data = load_run(run_dir)
    rows = run_data["rows"]
    summary = run_data["summary"]
    delta_rows = attention_pair_deltas(rows)
    aggregate = aggregate_attention_deltas(delta_rows)
    guard = attention_claim_guard(rows, delta_rows, summary=summary)
    if not allow_incomplete and not guard["attention_improves_dspo_allowed"]:
        raise ValueError("attention artifact generation is not claim-ready; pass --allow-incomplete")

    output_root = Path(output_root or DEFAULT_OUTPUT_ROOT)
    output_root.mkdir(parents=True, exist_ok=True)

    deltas_json = output_root / "paired_deltas" / "attention_pair_deltas.json"
    deltas_csv = output_root / "paired_deltas" / "attention_pair_deltas.csv"
    aggregate_json = output_root / "paired_deltas" / "attention_delta_summary.json"
    status_json = output_root / "PAIR_COMPLETENESS.json"
    guard_json = output_root / "ATTENTION_CLAIM_GUARD.json"
    table_path = output_root / "tables" / "attention_pair_deltas.tex"

    write_json(deltas_json, delta_rows)
    write_csv(deltas_csv, delta_rows)
    write_json(aggregate_json, aggregate)
    write_json(status_json, guard["pair_completeness"])
    write_json(guard_json, guard)
    write_latex_table(
        table_path,
        "Attention-vs-original paired deltas",
        delta_rows,
        [
            "attention_pair_id",
            "split_id",
            "net_objective_proxy_delta",
            "acceptance_rate_delta",
            "optout_rate_delta",
            "meeting_point_uptake_rate_delta",
            "pair_complete",
        ],
    )

    status_path = output_root / "ARTIFACT_STATUS.json"
    artifact_status = {
        "artifact_family": "work2_attention_dspo",
        "study": summary.get("study_name"),
        "tier": summary.get("tier"),
        "run_id": summary.get("run_id"),
        "source_run_dir": str(run_data["run_dir"]),
        "row_count": len(rows),
        "pair_count": len(delta_rows),
        "claim_ready": guard["claim_ready"],
        "attention_improves_dspo_allowed": guard["attention_improves_dspo_allowed"],
        "checkpoint_statuses": guard["checkpoint_statuses"],
        "blockers": guard["blockers"],
        "generated_at": utc_now_iso(),
        "git_provenance": summary.get("git_provenance") or collect_git_provenance(),
        "generated_artifacts": [
            str(deltas_json),
            str(deltas_csv),
            str(aggregate_json),
            str(status_json),
            str(guard_json),
            str(table_path),
        ],
    }
    write_json(status_path, artifact_status)

    readme_path = output_root / "README.md"
    readme_path.write_text(
        "# Work2 Attention DSPO Artifacts\n\n"
        + f"Study: {summary.get('study_name')}\n\n"
        + f"Run: {summary.get('run_id')}\n\n"
        + f"Claim ready: {guard['claim_ready']}\n",
        encoding="utf-8",
    )

    if mirror_root:
        mirror_lightweight_artifacts(output_root, mirror_root)

    return {
        "output_root": str(output_root),
        "mirror_root": str(mirror_root) if mirror_root else "",
        "status_path": str(status_path),
        "claim_guard_path": str(guard_json),
        "claim_guard": guard,
        "artifacts": artifact_status["generated_artifacts"] + [str(status_path), str(readme_path)],
    }


def latest_attention_run_dir(study, study_output_root=None):
    return latest_run_dir(study, study_output_root=study_output_root or DEFAULT_STUDY_OUTPUT_ROOT)
