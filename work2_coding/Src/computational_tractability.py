"""Phase 9 exact-versus-greedy tractability artifact helpers."""

import csv
import json
import math
from collections import defaultdict
from copy import deepcopy
from pathlib import Path

import yaml

from Src.artifact_status import sha256_file, utc_now_iso, write_json


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
DEFAULT_STUDY = "phase9_exact_greedy_tractability"
DEFAULT_STUDIES_ROOT = ROOT / "outputs" / "studies"
DEFAULT_OUTPUT_ROOT = ROOT / "artifacts" / "work2_robust_menu" / "phase9_tractability"
DEFAULT_STATUS_GATE = ROOT / "outputs" / "phase9_dspo_family_validation" / "PHASE9_DSPO_FAMILY_VALIDATION.json"
DEFAULT_SUMMARY_PATH = REPO_ROOT / ".planning" / "results" / "COMPUTATIONAL_TRACTABILITY_SUMMARY.md"

SUMMARY_STATUS = "diagnostic_provisional_blocked"
EXPECTED_POLICY_TAG = "mainline_optimized_adaptive"
EXPECTED_SCALE_VALUES = ("8", "12", "16")
EXPECTED_PAIRED_GROUP_COUNT = 5
EXPECTED_ROW_COUNT = EXPECTED_PAIRED_GROUP_COUNT * len(EXPECTED_SCALE_VALUES)
EXPECTED_MENU_K = 3
SMALL_EXACT_SCALE = "8"
LARGE_GREEDY_SCALES = {"12", "16"}
FALLBACK_REASON_ABOVE_THRESHOLD = "above_exact_threshold"
HIGH_GAP_THRESHOLD = 0.05
LOW_OVERLAP_THRESHOLD = 0.5
COMPLETED_STATUSES = {"completed"}
EXPLICIT_BLOCKED_STATUSES = {"blocked", "failed"}


class TractabilityValidationError(ValueError):
    """Raised when Phase 9 tractability rows violate the contract."""

    def __init__(self, failures):
        self.failures = list(failures)
        message = "; ".join(failure.get("reason", failure.get("code", "validation failed")) for failure in self.failures)
        super().__init__(message)


def _as_path(path, default):
    return Path(default if path in (None, "") else path)


def _rel(path):
    if path in (None, ""):
        return ""
    path = Path(path)
    if not path.is_absolute():
        return str(path).replace("\\", "/")
    try:
        return str(path.resolve().relative_to(REPO_ROOT.resolve())).replace("\\", "/")
    except Exception:
        return str(path).replace("\\", "/")


def _load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _load_yaml(path):
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return data or {}


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


def _stable_join(values):
    clean = sorted({str(value) for value in values if value not in (None, "")})
    return "; ".join(clean) if clean else "NA"


def _scale_sort(values):
    def key(value):
        try:
            return (0, int(value))
        except (TypeError, ValueError):
            return (1, str(value))

    return sorted({str(value) for value in values if value not in (None, "")}, key=key)


def _failure(code, reason, path="", **extra):
    payload = {"code": code, "reason": reason, "path": _rel(path)}
    payload.update(extra)
    return payload


def _row_status(row):
    return str(row.get("status") or row.get("execution_status") or "").lower()


def _row_execution_status(row):
    return str(row.get("execution_status") or row.get("status") or "").lower()


def row_is_completed(row):
    return _row_status(row) in COMPLETED_STATUSES and _row_execution_status(row) in COMPLETED_STATUSES


def row_is_explicitly_blocked(row):
    statuses = {_row_status(row), _row_execution_status(row)}
    if statuses & EXPLICIT_BLOCKED_STATUSES:
        return True
    if row.get("error_type") or row.get("error_message"):
        return True
    if row.get("blocker_code") or row.get("blocker_reason"):
        return True
    return False


def row_candidate_count(row):
    return _num(row.get("solver_candidate_count")) or _num(row.get("max_candidates"))


def latest_run_dir(studies_root=None, study_name=DEFAULT_STUDY):
    root = _as_path(studies_root, DEFAULT_STUDIES_ROOT) / study_name
    candidates = []
    if root.exists():
        candidates = [
            path
            for path in root.iterdir()
            if path.is_dir() and (path / "normalized_rows.json").exists() and (path / "study_summary.json").exists()
        ]
    if not candidates:
        raise FileNotFoundError("no completed source run found for study " + str(study_name) + " under " + _rel(root))
    return sorted(candidates, key=lambda path: (path.stat().st_mtime, path.name), reverse=True)[0]


def load_tractability_run(run_dir=None, studies_root=None, study_name=DEFAULT_STUDY):
    run_dir = Path(run_dir) if run_dir else latest_run_dir(studies_root=studies_root, study_name=study_name)
    rows_path = run_dir / "normalized_rows.json"
    summary_path = run_dir / "study_summary.json"
    manifest_path = run_dir / "manifest_snapshot.yaml"
    blockers_path = run_dir / "blockers.json"
    if not rows_path.exists():
        raise FileNotFoundError("missing normalized_rows.json: " + str(rows_path))
    if not summary_path.exists():
        raise FileNotFoundError("missing study_summary.json: " + str(summary_path))
    if not manifest_path.exists():
        raise FileNotFoundError("missing manifest_snapshot.yaml: " + str(manifest_path))
    rows = _load_json(rows_path)
    summary = _load_json(summary_path)
    manifest = _load_yaml(manifest_path)
    manifest["_path"] = str(manifest_path)
    blockers = []
    if blockers_path.exists():
        blockers_payload = _load_json(blockers_path)
        blockers = blockers_payload.get("blockers", blockers_payload if isinstance(blockers_payload, list) else [])
    if blockers and not summary.get("blockers"):
        summary["blockers"] = blockers
    return {
        "run_dir": run_dir,
        "rows": rows,
        "summary": summary,
        "manifest": manifest,
        "manifest_snapshot_path": manifest_path,
        "blockers": blockers,
    }


def load_status_gate(status_gate=None):
    path = _as_path(status_gate, DEFAULT_STATUS_GATE)
    if not path.exists():
        return {
            "schema_version": "phase9-status-gate-reference-v1",
            "phase9_gate_status": "missing",
            "status": "blocked",
            "claim_ready": False,
            "path": str(path),
            "hash": "",
            "failures": [
                _failure(
                    "phase9_status_gate_missing",
                    "PHASE9_DSPO_FAMILY_VALIDATION.json is missing; status context is blocked.",
                    path,
                )
            ],
        }
    try:
        payload = _load_json(path)
    except Exception as exc:
        return {
            "schema_version": "phase9-status-gate-reference-v1",
            "phase9_gate_status": "malformed",
            "status": "blocked",
            "claim_ready": False,
            "path": str(path),
            "hash": "",
            "failures": [
                _failure("phase9_status_gate_malformed", "Phase 9 status gate JSON is malformed.", path, error=str(exc))
            ],
        }
    result = deepcopy(payload)
    phase9_gate = result.get("phase9_gate") or result.get("phase9_gate_status") or result.get("dspo_validation_status")
    if phase9_gate == "open" or phase9_gate == "passed":
        gate_status = "open"
    else:
        gate_status = str(phase9_gate or "blocked")
    result.update(
        {
            "phase9_gate_status": gate_status,
            "status": "passed" if gate_status == "open" else "blocked",
            "claim_ready": False,
            "path": str(path),
            "hash": sha256_file(path),
            "failures": [] if gate_status == "open" else list(result.get("failures") or []),
        }
    )
    return result


def _split_lookup(manifest):
    return {split.get("split_id"): split for split in manifest.get("splits", [])}


def _split_args(manifest, split):
    args = {}
    args.update(manifest.get("base_args") or {})
    args.update(split.get("args_overrides") or {})
    for field in ("seed", "data_seed", "data_seed_test", "uptake_regime"):
        if split.get(field) is not None:
            args[field] = split.get(field)
    return args


def annotate_rows(run_data):
    manifest = run_data["manifest"]
    summary = run_data["summary"]
    split_by_id = _split_lookup(manifest)
    annotated = []
    for row in run_data["rows"]:
        item = deepcopy(row)
        split = split_by_id.get(row.get("split_id"), {})
        args = _split_args(manifest, split)
        scale_value = split.get("solver_scale_value")
        if scale_value is None:
            scale_value = item.get("solver_scale_value") or item.get("max_candidates") or args.get("max_candidates")
        item.update(
            {
                "solver_scale_variant": split.get("solver_scale_variant") or item.get("solver_scale_variant", ""),
                "solver_scale_value": str(scale_value) if scale_value not in (None, "") else "",
                "paired_group_id": split.get("paired_group_id") or item.get("paired_group_id", ""),
                "source_run_dir": _rel(run_data["run_dir"]),
                "source_run_id": summary.get("run_id") or item.get("run_id", ""),
                "source_study_name": summary.get("study_name") or manifest.get("name") or item.get("study_name", ""),
                "manifest_claim_ready": bool(manifest.get("claim_ready")),
                "manifest_output_intent": manifest.get("output_intent", ""),
                "summary_status": SUMMARY_STATUS,
                "claim_ready": False,
            }
        )
        if item.get("menu_k") in (None, ""):
            item["menu_k"] = args.get("menu_k")
        if item.get("max_candidates") in (None, ""):
            item["max_candidates"] = args.get("max_candidates")
        if item.get("uptake_regime") in (None, ""):
            item["uptake_regime"] = args.get("uptake_regime")
        annotated.append(item)
    return annotated


def _validate_policy(rows, failures):
    policies = sorted({row.get("policy_tag") for row in rows if row.get("policy_tag")})
    if policies != [EXPECTED_POLICY_TAG]:
        failures.append(
            _failure(
                "unexpected_policy_tag",
                "Phase 9 tractability rows must contain only " + EXPECTED_POLICY_TAG + ".",
                policies=policies,
            )
        )


def _validate_scale_coverage(rows, failures):
    scale_values = _scale_sort(row.get("solver_scale_value") for row in rows)
    if set(scale_values) != set(EXPECTED_SCALE_VALUES):
        failures.append(
            _failure(
                "missing_scale_variant",
                "Phase 9 tractability rows must include solver-scale values 8, 12, and 16.",
                observed_scale_values=scale_values,
            )
        )
    groups = defaultdict(set)
    for row in rows:
        if row.get("paired_group_id"):
            groups[row.get("paired_group_id")].add(str(row.get("solver_scale_value")))
    if len(groups) != EXPECTED_PAIRED_GROUP_COUNT:
        failures.append(
            _failure(
                "paired_group_count_mismatch",
                "Phase 9 tractability rows must include five paired groups.",
                observed_paired_group_count=len(groups),
                observed_paired_groups=sorted(groups),
            )
        )
    for group_id, scales in sorted(groups.items()):
        missing = [scale for scale in EXPECTED_SCALE_VALUES if scale not in scales]
        if missing:
            failures.append(
                _failure(
                    "paired_group_missing_scale",
                    "Each paired group must include all three solver-scale values.",
                    paired_group_id=group_id,
                    missing_scale_values=missing,
                )
            )


def _validate_row_statuses(rows, failures):
    if len(rows) != EXPECTED_ROW_COUNT:
        failures.append(
            _failure(
                "row_count_mismatch",
                "Phase 9 tractability validation requires 15 completed or explicitly blocked rows.",
                observed_row_count=len(rows),
                expected_row_count=EXPECTED_ROW_COUNT,
            )
        )
    for row in rows:
        if row_is_completed(row) or row_is_explicitly_blocked(row):
            continue
        failures.append(
            _failure(
                "row_not_completed_or_blocked",
                "Every tractability row must be completed or explicitly blocked.",
                row.get("source_run_dir", ""),
                split_id=row.get("split_id"),
                status=row.get("status"),
                execution_status=row.get("execution_status"),
            )
        )


def _validate_completed_row(row, failures):
    split_id = row.get("split_id")
    scale = str(row.get("solver_scale_value", ""))
    if row.get("checkpoint_load_status") != "loaded":
        failures.append(
            _failure(
                "completed_checkpoint_not_loaded",
                "Completed Phase 9 tractability rows must report checkpoint_load_status=loaded.",
                row.get("source_run_dir", ""),
                split_id=split_id,
                checkpoint_load_status=row.get("checkpoint_load_status"),
            )
        )
    for field in ("checkpoint_path", "checkpoint_hash"):
        if not row.get(field):
            failures.append(
                _failure(
                    "completed_checkpoint_metadata_missing",
                    "Completed rows must include checkpoint path, hash, and required flag.",
                    row.get("source_run_dir", ""),
                    split_id=split_id,
                    missing_field=field,
                )
            )
    if row.get("checkpoint_required") is not True:
        failures.append(
            _failure(
                "completed_checkpoint_required_missing",
                "Completed rows must keep checkpoint_required=true.",
                row.get("source_run_dir", ""),
                split_id=split_id,
            )
        )
    if str(row.get("menu_k")) != str(EXPECTED_MENU_K):
        failures.append(
            _failure(
                "bad_menu_k",
                "Phase 9 tractability rows must keep menu_k=3.",
                row.get("source_run_dir", ""),
                split_id=split_id,
                menu_k=row.get("menu_k"),
            )
        )
    if row_candidate_count(row) is None:
        failures.append(
            _failure(
                "candidate_count_missing",
                "Rows must include solver_candidate_count or max_candidates for reporting.",
                row.get("source_run_dir", ""),
                split_id=split_id,
            )
        )
    effective_solver = row.get("menu_selection_solver_effective")
    fallback_reason = row.get("solver_fallback_reason")
    if scale == SMALL_EXACT_SCALE and effective_solver != "exact":
        failures.append(
            _failure(
                "small_row_not_exact",
                "Small max_candidates=8 rows must use the exact effective solver.",
                row.get("source_run_dir", ""),
                split_id=split_id,
                effective_solver=effective_solver,
            )
        )
    if scale in LARGE_GREEDY_SCALES:
        if effective_solver != "greedy":
            failures.append(
                _failure(
                    "large_row_not_greedy",
                    "Large solver-scale rows must use the greedy effective solver when completed.",
                    row.get("source_run_dir", ""),
                    split_id=split_id,
                    effective_solver=effective_solver,
                )
            )
        if fallback_reason != FALLBACK_REASON_ABOVE_THRESHOLD:
            failures.append(
                _failure(
                    "large_fallback_reason_missing",
                    "Completed large solver-scale rows must report above_exact_threshold fallback metadata.",
                    row.get("source_run_dir", ""),
                    split_id=split_id,
                    solver_fallback_reason=fallback_reason,
                )
            )


def validate_tractability_rows(rows, manifest=None, strict=False):
    rows = list(rows or [])
    failures = []
    if manifest and manifest.get("claim_ready") is not False:
        failures.append(
            _failure(
                "manifest_claim_ready_upgrade",
                "Phase 9 tractability manifests must keep claim_ready=false.",
                manifest.get("_path", ""),
            )
        )
    _validate_policy(rows, failures)
    _validate_scale_coverage(rows, failures)
    _validate_row_statuses(rows, failures)
    for row in rows:
        if row_is_completed(row):
            _validate_completed_row(row, failures)
        elif row_is_explicitly_blocked(row) and row_candidate_count(row) is None:
            # Blocked rows can lack solver diagnostics, but scale must remain reportable.
            if row.get("solver_scale_value") in (None, ""):
                failures.append(
                    _failure(
                        "blocked_row_scale_missing",
                        "Explicitly blocked rows must still identify their solver-scale value.",
                        row.get("source_run_dir", ""),
                        split_id=row.get("split_id"),
                    )
                )
    completed_count = sum(1 for row in rows if row_is_completed(row))
    blocked_count = sum(1 for row in rows if row_is_explicitly_blocked(row))
    validation = {
        "valid": not failures,
        "failures": failures,
        "row_count": len(rows),
        "completed_count": completed_count,
        "blocked_count": blocked_count,
        "checkpoint_statuses": sorted({row.get("checkpoint_load_status") for row in rows if row.get("checkpoint_load_status")}),
        "policy_tags": sorted({row.get("policy_tag") for row in rows if row.get("policy_tag")}),
        "solver_scale_values": _scale_sort(row.get("solver_scale_value") for row in rows),
        "paired_group_ids": sorted({row.get("paired_group_id") for row in rows if row.get("paired_group_id")}),
    }
    if strict and failures:
        raise TractabilityValidationError(failures)
    return validation


def claim_boundary_for_aggregates(aggregates):
    if any(row.get("blocked_count", 0) for row in aggregates):
        return "blocked_diagnostic"
    for row in aggregates:
        if str(row.get("solver_scale_value")) in LARGE_GREEDY_SCALES:
            gap = _num(row.get("relative_optimality_gap_mean"))
            overlap = _num(row.get("menu_overlap_rate_mean"))
            if gap is not None and gap > HIGH_GAP_THRESHOLD:
                return "fast_but_approximate_regime_dependent"
            if overlap is not None and overlap < LOW_OVERLAP_THRESHOLD:
                return "fast_but_approximate_regime_dependent"
    return "computationally_fast_diagnostic_not_claim_ready"


def aggregate_tractability_rows(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[str(row.get("solver_scale_value", ""))].append(row)
    aggregates = []
    for scale in EXPECTED_SCALE_VALUES:
        group = groups.get(scale, [])
        completed = [row for row in group if row_is_completed(row)]
        candidate_counts = [row_candidate_count(row) for row in group]
        aggregate = {
            "solver_scale_variant": _stable_join(row.get("solver_scale_variant") for row in group),
            "solver_scale_value": scale,
            "row_count": len(group),
            "completed_count": len(completed),
            "blocked_count": sum(1 for row in group if row_is_explicitly_blocked(row)),
            "candidate_count_mean": _mean(candidate_counts),
            "max_candidates": _mean(row.get("max_candidates") for row in group),
            "exact_enumerated_menu_count_mean": _mean(row.get("exact_enumerated_menu_count") for row in completed),
            "menu_build_time_mean": _mean(row.get("menu_build_time") for row in completed),
            "relative_optimality_gap_mean": _mean(row.get("relative_optimality_gap") for row in completed),
            "menu_overlap_rate_mean": _mean(row.get("menu_overlap_rate") for row in completed),
            "fallback_reasons": _stable_join(row.get("solver_fallback_reason") for row in group),
            "checkpoint_statuses": _stable_join(row.get("checkpoint_load_status") for row in group),
            "effective_solvers": _stable_join(row.get("menu_selection_solver_effective") for row in group),
            "status": _stable_join(row.get("status") for row in group),
            "execution_status": _stable_join(row.get("execution_status") for row in group),
            "claim_ready": False,
            "summary_status": SUMMARY_STATUS,
        }
        aggregates.append(aggregate)
    boundary = claim_boundary_for_aggregates(aggregates)
    for row in aggregates:
        row["claim_boundary"] = boundary
    return aggregates


def write_csv(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row.keys()})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fields})


def _latex_value(value):
    if value is None:
        return "NA"
    text = f"{value:.4g}" if isinstance(value, float) else str(value)
    return text.replace("_", "\\_").replace("%", "\\%")


def write_latex_table(path, caption, rows, columns):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "\\begin{table}[ht]",
        "\\centering",
        "\\begin{tabular}{" + "l" * len(columns) + "}",
        " \\hline",
        " & ".join(_latex_value(column) for column in columns) + " \\\\",
        " \\hline",
    ]
    for row in rows:
        lines.append(" & ".join(_latex_value(row.get(column)) for column in columns) + " \\\\")
    lines.extend([" \\hline", "\\end{tabular}", "\\caption{" + _latex_value(caption) + "}", "\\end{table}", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def _source_metadata(run_data, rows):
    summary = (run_data or {}).get("summary") or {}
    return {
        "source_run_dir": _rel((run_data or {}).get("run_dir", "")),
        "source_run_id": summary.get("run_id", ""),
        "source_row_count": len(rows or []),
        "manifest_hash": summary.get("manifest_hash") or next((row.get("manifest_hash") for row in rows if row.get("manifest_hash")), ""),
        "manifest_snapshot_path": _rel((run_data or {}).get("manifest_snapshot_path", "")),
        "checkpoint_statuses": sorted({row.get("checkpoint_load_status") for row in rows or [] if row.get("checkpoint_load_status")}),
        "git_provenance": summary.get("git_provenance", {}),
    }


def artifact_metadata(artifact_path, artifact_kind, run_data, rows, status_gate, status_info, validation):
    metadata = _source_metadata(run_data, rows)
    metadata.update(
        {
            "schema_version": "phase9-tractability-artifact-metadata-v1",
            "phase": "09",
            "artifact_path": _rel(artifact_path),
            "artifact_kind": artifact_kind,
            "generated_at_utc": utc_now_iso(),
            "status": SUMMARY_STATUS,
            "artifact_gate_status": status_info.get("status", "blocked"),
            "phase9_gate_path": _rel(status_gate.get("path", "")),
            "phase9_gate_hash": status_gate.get("hash", ""),
            "phase9_gate_status": status_gate.get("phase9_gate_status", "missing"),
            "claim_ready": False,
            "diagnostic_provisional": True,
            "validation": validation,
            "status_reasons": status_info.get("reasons", []),
        }
    )
    return metadata


def write_sidecar(artifact_path, artifact_kind, run_data, rows, status_gate, status_info, validation):
    path = Path(str(artifact_path) + ".metadata.json")
    write_json(path, artifact_metadata(artifact_path, artifact_kind, run_data, rows, status_gate, status_info, validation))
    return path


def _plot_line(path, labels, x_values, series, ylabel, title):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4.8))
    for label, values in series:
        ax.plot(x_values, values, marker="o", label=label)
    ax.set_xticks(x_values)
    ax.set_xticklabels(labels, rotation=25, ha="right")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def _write_figure_status(path, reason, run_data, rows, status_gate, status_info, validation):
    status_path = Path(str(path) + ".status.json")
    payload = artifact_metadata(status_path, "figure-status", run_data, rows, status_gate, status_info, validation)
    payload["figure_status"] = "incomplete"
    payload["missing_reason"] = reason
    write_json(status_path, payload)
    return status_path


def generate_tractability_figures(figures_dir, aggregates, run_data, rows, status_gate, status_info, validation):
    figures_dir = Path(figures_dir)
    generated = []
    labels = [str(row.get("candidate_count_mean") or row.get("solver_scale_value")) for row in aggregates]
    x_values = [idx + 1 for idx, _ in enumerate(labels)]

    time_values = [_num(row.get("menu_build_time_mean")) for row in aggregates]
    time_path = figures_dir / "menu_build_time_by_candidate_count.png"
    if labels and any(value is not None for value in time_values):
        try:
            values = [0.0 if value is None else value for value in time_values]
            _plot_line(
                time_path,
                labels,
                x_values,
                [("menu_build_time", values)],
                "seconds",
                "Menu build time by candidate count",
            )
            generated.extend([str(time_path), str(write_sidecar(time_path, "figure", run_data, rows, status_gate, status_info, validation))])
        except Exception as exc:  # pragma: no cover - depends on local matplotlib backend
            status_path = _write_figure_status(time_path, "figure generation failed: " + str(exc), run_data, rows, status_gate, status_info, validation)
            generated.append(str(status_path))
            generated.append(str(write_sidecar(status_path, "figure-status", run_data, rows, status_gate, status_info, validation)))
    else:
        status_path = _write_figure_status(time_path, "menu_build_time is unavailable", run_data, rows, status_gate, status_info, validation)
        generated.append(str(status_path))
        generated.append(str(write_sidecar(status_path, "figure-status", run_data, rows, status_gate, status_info, validation)))

    gap_values = [_num(row.get("relative_optimality_gap_mean")) for row in aggregates]
    overlap_values = [_num(row.get("menu_overlap_rate_mean")) for row in aggregates]
    gap_path = figures_dir / "gap_overlap_by_candidate_count.png"
    if labels and any(value is not None for value in gap_values + overlap_values):
        try:
            gaps = [0.0 if value is None else value for value in gap_values]
            overlaps = [0.0 if value is None else value for value in overlap_values]
            _plot_line(
                gap_path,
                labels,
                x_values,
                [("relative_optimality_gap", gaps), ("menu_overlap_rate", overlaps)],
                "diagnostic value",
                "Gap and overlap by candidate count",
            )
            generated.extend([str(gap_path), str(write_sidecar(gap_path, "figure", run_data, rows, status_gate, status_info, validation))])
        except Exception as exc:  # pragma: no cover - depends on local matplotlib backend
            status_path = _write_figure_status(gap_path, "figure generation failed: " + str(exc), run_data, rows, status_gate, status_info, validation)
            generated.append(str(status_path))
            generated.append(str(write_sidecar(status_path, "figure-status", run_data, rows, status_gate, status_info, validation)))
    else:
        status_path = _write_figure_status(gap_path, "gap or overlap metrics are unavailable", run_data, rows, status_gate, status_info, validation)
        generated.append(str(status_path))
        generated.append(str(write_sidecar(status_path, "figure-status", run_data, rows, status_gate, status_info, validation)))
    return generated


def _status_info(validation, status_gate, rows):
    reasons = []
    if status_gate.get("phase9_gate_status") != "open":
        reasons.append("Phase 9 DSPO prerequisite status gate is not open.")
    if not validation.get("valid"):
        reasons.extend(failure.get("reason", failure.get("code", "")) for failure in validation.get("failures", []))
    if validation.get("blocked_count", 0) > 0:
        reasons.append("One or more tractability rows are explicitly blocked.")
    if not reasons:
        reasons.append("diagnostic run mode is not claim-ready evidence")
    status = "blocked" if status_gate.get("phase9_gate_status") != "open" or not validation.get("valid") or validation.get("blocked_count", 0) else "diagnostic"
    return {
        "status": status,
        "claim_ready": False,
        "reasons": sorted(set(reasons)),
        "checkpoint_statuses": sorted({row.get("checkpoint_load_status") for row in rows if row.get("checkpoint_load_status")}),
        "row_statuses": sorted({row.get("status") for row in rows if row.get("status")}),
        "execution_statuses": sorted({row.get("execution_status") for row in rows if row.get("execution_status")}),
        "blockers": validation.get("failures", []),
    }


def _blocked_artifact_result(output_root, status_gate, failures, run_data=None, rows=None, validation=None):
    output_root = Path(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    rows = rows or []
    validation = validation or {
        "valid": False,
        "failures": failures,
        "row_count": len(rows),
        "completed_count": 0,
        "blocked_count": 0,
        "checkpoint_statuses": [],
        "policy_tags": [],
        "solver_scale_values": [],
        "paired_group_ids": [],
    }
    status_info = {
        "status": "blocked",
        "claim_ready": False,
        "reasons": sorted({failure.get("reason", failure.get("code", "")) for failure in failures}),
        "checkpoint_statuses": validation.get("checkpoint_statuses", []),
        "row_statuses": [],
        "execution_statuses": [],
        "blockers": failures,
    }
    status_path = output_root / "ARTIFACT_STATUS.json"
    result = {
        "schema_version": "phase9-tractability-artifacts-v1",
        "phase": "09",
        "study": DEFAULT_STUDY,
        "status": SUMMARY_STATUS,
        "builder_status": "blocked",
        "claim_ready": False,
        "phase9_gate_status": status_gate.get("phase9_gate_status", "missing"),
        "phase9_gate_path": _rel(status_gate.get("path", "")),
        "artifact_root": _rel(output_root),
        "artifact_status": status_info,
        "validation": validation,
        "failures": failures,
        "aggregate_rows": [],
        "coverage_rows": rows,
        "claim_boundary": "blocked_diagnostic",
        "artifacts": {"status": _rel(status_path)},
        "generated_artifacts": [_rel(status_path)],
    }
    result.update(_source_metadata(run_data or {}, rows))
    write_json(status_path, result)
    sidecar = write_sidecar(status_path, "status", run_data or {}, rows, status_gate, status_info, validation)
    result["artifacts"]["status_metadata"] = _rel(sidecar)
    result["generated_artifacts"].append(_rel(sidecar))
    write_json(status_path, result)
    return result


def build_tractability_artifacts(
    study=DEFAULT_STUDY,
    studies_root=None,
    status_gate=None,
    output_root=None,
    run_dir=None,
):
    output_root = _as_path(output_root, DEFAULT_OUTPUT_ROOT)
    status_gate_data = load_status_gate(status_gate)
    try:
        run_data = load_tractability_run(run_dir=run_dir, studies_root=studies_root, study_name=study)
    except Exception as exc:
        return _blocked_artifact_result(
            output_root,
            status_gate_data,
            [_failure("source_run_missing", "Phase 9 tractability source run is missing or unreadable.", studies_root or DEFAULT_STUDIES_ROOT, error=str(exc))],
        )

    rows = annotate_rows(run_data)
    validation = validate_tractability_rows(rows, manifest=run_data["manifest"], strict=False)

    output_root.mkdir(parents=True, exist_ok=True)
    aggregates = aggregate_tractability_rows(rows)
    status_info = _status_info(validation, status_gate_data, rows)
    claim_boundary = "blocked_diagnostic" if not validation["valid"] else claim_boundary_for_aggregates(aggregates)
    for row in aggregates:
        row["claim_boundary"] = claim_boundary
    artifacts = {}
    generated = []

    aggregate_json = output_root / "aggregates" / "exact_greedy_tractability_summary.json"
    aggregate_csv = output_root / "aggregates" / "exact_greedy_tractability_summary.csv"
    write_json(aggregate_json, aggregates)
    write_csv(aggregate_csv, aggregates)
    artifacts["aggregate_json"] = str(aggregate_json)
    artifacts["aggregate_csv"] = str(aggregate_csv)
    generated.extend([str(aggregate_json), str(aggregate_csv)])
    for path, kind in [(aggregate_json, "aggregate-json"), (aggregate_csv, "aggregate-csv")]:
        sidecar = write_sidecar(path, kind, run_data, rows, status_gate_data, status_info, validation)
        artifacts[kind + "_metadata"] = str(sidecar)
        generated.append(str(sidecar))

    table_path = output_root / "tables" / "exact_greedy_tractability.tex"
    write_latex_table(
        table_path,
        "Phase 9 exact-greedy tractability diagnostics",
        aggregates,
        [
            "solver_scale_value",
            "candidate_count_mean",
            "exact_enumerated_menu_count_mean",
            "menu_build_time_mean",
            "relative_optimality_gap_mean",
            "menu_overlap_rate_mean",
            "fallback_reasons",
            "claim_boundary",
        ],
    )
    artifacts["tractability_table"] = str(table_path)
    generated.append(str(table_path))
    table_sidecar = write_sidecar(table_path, "latex-table", run_data, rows, status_gate_data, status_info, validation)
    artifacts["latex-table_metadata"] = str(table_sidecar)
    generated.append(str(table_sidecar))

    figure_paths = generate_tractability_figures(output_root / "figures", aggregates, run_data, rows, status_gate_data, status_info, validation)
    for figure_path in figure_paths:
        key = Path(figure_path).name.replace(".metadata.json", "_metadata").replace(".status.json", "_status").replace(".png", "")
        artifacts[key] = figure_path
    generated.extend(figure_paths)

    status_path = output_root / "ARTIFACT_STATUS.json"
    result = {
        "schema_version": "phase9-tractability-artifacts-v1",
        "phase": "09",
        "study": study,
        "status": SUMMARY_STATUS,
        "builder_status": "blocked" if status_info["status"] == "blocked" else "completed",
        "claim_ready": False,
        "phase9_gate_status": status_gate_data.get("phase9_gate_status", "missing"),
        "phase9_gate_path": _rel(status_gate_data.get("path", "")),
        "phase9_gate_hash": status_gate_data.get("hash", ""),
        "artifact_root": _rel(output_root),
        "artifact_status": status_info,
        "validation": validation,
        "failures": validation.get("failures", []),
        "aggregate_rows": aggregates,
        "coverage_rows": rows,
        "claim_boundary": claim_boundary,
        "artifacts": artifacts,
        "generated_artifacts": generated + [str(status_path)],
    }
    result.update(_source_metadata(run_data, rows))
    write_json(status_path, result)
    status_sidecar = write_sidecar(status_path, "status", run_data, rows, status_gate_data, status_info, validation)
    result["artifacts"]["status"] = str(status_path)
    result["artifacts"]["status_metadata"] = str(status_sidecar)
    result["generated_artifacts"].append(str(status_sidecar))
    write_json(status_path, result)
    return result


def _format_value(value):
    value = _num(value)
    if value is None:
        return "NA"
    return f"{value:.4g}"


def _frontmatter(result):
    lines = [
        "---",
        "status: " + str(result.get("status", SUMMARY_STATUS)),
        "claim_ready: false",
        "phase9_gate_status: " + str(result.get("phase9_gate_status", "missing")),
        "source_run_id: " + str(result.get("source_run_id") or "none"),
        "artifact_root: " + _rel(result.get("artifact_root", "")),
        "generated_at_utc: " + utc_now_iso(),
        "---",
        "",
    ]
    return lines


def _coverage_table_rows(rows):
    header = ["| paired_group_id | scale_values | completed | blocked | total |", "| --- | --- | ---: | ---: | ---: |"]
    if not rows:
        return header + ["| none | blocked | 0 | 0 | 0 |"]
    groups = defaultdict(list)
    for row in rows:
        groups[row.get("paired_group_id", "missing")].append(row)
    lines = list(header)
    for group_id in sorted(groups):
        group = groups[group_id]
        lines.append(
            "| "
            + str(group_id)
            + " | "
            + _stable_join(row.get("solver_scale_value") for row in group)
            + " | "
            + str(sum(1 for row in group if row_is_completed(row)))
            + " | "
            + str(sum(1 for row in group if row_is_explicitly_blocked(row)))
            + " | "
            + str(len(group))
            + " |"
        )
    return lines


def _aggregate_markdown_rows(aggregates):
    if not aggregates:
        aggregates = [
            {
                "solver_scale_value": scale,
                "candidate_count_mean": None,
                "exact_enumerated_menu_count_mean": None,
                "menu_build_time_mean": None,
                "relative_optimality_gap_mean": None,
                "menu_overlap_rate_mean": None,
                "effective_solvers": "blocked",
                "fallback_reasons": "blocked",
                "claim_boundary": "blocked_diagnostic",
            }
            for scale in EXPECTED_SCALE_VALUES
        ]
    lines = [
        "| solver_scale_value | candidate count | exact_enumerated_menu_count | menu_build_time | relative_optimality_gap | menu_overlap_rate | effective solver | fallback reason |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in aggregates:
        lines.append(
            "| "
            + str(row.get("solver_scale_value"))
            + " | "
            + _format_value(row.get("candidate_count_mean"))
            + " | "
            + _format_value(row.get("exact_enumerated_menu_count_mean"))
            + " | "
            + _format_value(row.get("menu_build_time_mean"))
            + " | "
            + _format_value(row.get("relative_optimality_gap_mean"))
            + " | "
            + _format_value(row.get("menu_overlap_rate_mean"))
            + " | "
            + str(row.get("effective_solvers", "NA"))
            + " | "
            + str(row.get("fallback_reasons", "NA"))
            + " |"
        )
    return lines


def render_tractability_summary(result):
    aggregates = result.get("aggregate_rows") or []
    rows = result.get("coverage_rows") or []
    lines = _frontmatter(result)
    lines.extend(
        [
            "# Phase 9 Computational Tractability Summary",
            "",
            "This file is generated from Phase 9 normalized rows, manifest snapshots, and generated artifact status. It is diagnostic/provisional evidence with `claim_ready: false`.",
            "",
            "## Status Gate",
            "",
            "Prerequisite status context: `PHASE9_DSPO_FAMILY_VALIDATION.json` at `" + str(result.get("phase9_gate_path", "")) + "` reports `"
            + str(result.get("phase9_gate_status", "missing"))
            + "`. This gate is prerequisite status context only; it does not authorize claim-ready manuscript language.",
            "",
            "## 15-Row Coverage",
            "",
        ]
    )
    lines.extend(_coverage_table_rows(rows))
    validation = result.get("validation") or {}
    lines.extend(
        [
            "",
            "Completed rows: `" + str(validation.get("completed_count", 0)) + "`; blocked rows: `"
            + str(validation.get("blocked_count", 0))
            + "`; total rows: `"
            + str(validation.get("row_count", 0))
            + "`.",
            "",
            "## Exact-Greedy Table",
            "",
        ]
    )
    lines.extend(_aggregate_markdown_rows(aggregates))
    lines.extend(["", "## Claim Boundary", ""])
    boundary = result.get("claim_boundary", "blocked_diagnostic")
    if boundary == "fast_but_approximate_regime_dependent":
        lines.append(
            "Large greedy diagnostics narrow the computational statement to: computationally fast but approximate; quality is regime-dependent."
        )
    elif boundary == "blocked_diagnostic":
        lines.append("Tractability interpretation is blocked or explicitly diagnostic because source rows or gates are blocked.")
    else:
        lines.append("Tractability diagnostics are computationally fast, but they remain diagnostic and not claim-ready.")
    lines.append("No claim-ready manuscript upgrade is authorized by Phase 9; `claim_ready: false` remains in force.")
    lines.extend(["", "## Source Artifacts", ""])
    artifacts = result.get("artifacts") or {}
    if artifacts:
        for key in sorted(artifacts):
            lines.append("- `" + key + "`: `" + _rel(artifacts[key]) + "`")
    else:
        lines.append("- No generated tractability artifacts are available.")
    lines.extend(["", "## Validation Notes", ""])
    failures = result.get("failures") or []
    if failures:
        for failure in failures:
            lines.append("- `" + failure.get("code", "failure") + "`: " + failure.get("reason", ""))
    else:
        lines.append("- Row coverage and exact-greedy diagnostic contracts passed for generated artifacts.")
    lines.append("")
    return "\n".join(lines)


def write_tractability_summary(
    study=DEFAULT_STUDY,
    studies_root=None,
    status_gate=None,
    artifact_root=None,
    planning_output=None,
    run_dir=None,
):
    result = build_tractability_artifacts(
        study=study,
        studies_root=studies_root,
        status_gate=status_gate,
        output_root=artifact_root,
        run_dir=run_dir,
    )
    output = _as_path(planning_output, DEFAULT_SUMMARY_PATH)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_tractability_summary(result), encoding="utf-8")
    return {"summary_path": str(output), "artifact_result": result}
