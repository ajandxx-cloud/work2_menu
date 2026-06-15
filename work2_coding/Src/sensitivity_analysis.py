"""Phase 8 sensitivity artifact and summary helpers."""

import csv
import json
import math
from collections import defaultdict
from copy import deepcopy
from pathlib import Path

import yaml

from Src.artifact_status import classify_artifact, sha256_file, utc_now_iso, write_json
from Src.experiment_contracts import load_manifest, load_suite, suite_members


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent

DEFAULT_SUITE = "phase8_sensitivity_must_have"
DEFAULT_STUDIES_ROOT = ROOT / "outputs" / "studies"
DEFAULT_BASELINE_REPORT = ROOT / "outputs" / "phase8_baseline_validation" / "PHASE8_BASELINE_VALIDATION.json"
DEFAULT_OUTPUT_ROOT = ROOT / "artifacts" / "work2_robust_menu" / "phase8_sensitivity"
DEFAULT_SUMMARY_PATH = REPO_ROOT / ".planning" / "results" / "SENSITIVITY_SUMMARY.md"

SUMMARY_STATUS = "diagnostic_provisional_blocked"
ALLOWED_AXES = ("menu_k", "eta_filter_mode", "uptake_regime", "guardrail")
EXPECTED_GUARDRAIL_FIELDS = ("service_quit_rate_guardrail", "menu_optout_guardrail")
EXPECTED_CHANCE_THRESHOLD = 0.25
EXPECTED_UPTAKE_REGIMES = ("low", "medium")
DEFERRED_DIMENSIONS = (
    "max_candidates",
    "fleet_capacity_stress",
    "pricing_bounds",
    "price_sensitivity",
)
NICE_TO_HAVE_ARG_FIELDS = {
    "max_candidates",
    "n_vehicles",
    "veh_capacity",
    "max_price",
    "min_price",
    "menu_pricing_constant",
}
MAIN_POLICY_TAG = "mainline_optimized_adaptive"


class SensitivityValidationError(ValueError):
    """Raised when Phase 8 sensitivity rows violate the diagnostic contract."""

    def __init__(self, failures):
        self.failures = failures
        message = "; ".join(failure["code"] + ": " + failure["reason"] for failure in failures)
        super().__init__(message)


def _rel(path):
    path = Path(path)
    try:
        return str(path.resolve().relative_to(REPO_ROOT.resolve())).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _as_path(path, default):
    return Path(path) if path else Path(default)


def _failure(code, reason, evidence_location="", **extra):
    item = {
        "code": code,
        "severity": "blocking",
        "reason": reason,
        "evidence_location": evidence_location,
    }
    item.update(extra)
    return item


def _load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _load_yaml(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}


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


def _format_value(value):
    if value is None:
        return "NA"
    if isinstance(value, float):
        return f"{value:.4g}"
    return str(value)


def _latex_value(value):
    return _format_value(value).replace("_", "\\_").replace("%", "\\%")


def write_csv(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row.keys()})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fields})
    return path


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
    if rows:
        for row in rows:
            lines.append(" & ".join(_latex_value(row.get(column)) for column in columns) + " \\\\")
    else:
        lines.append(" & ".join("NA" for _ in columns) + " \\\\")
    lines.extend([" \\hline", "\\end{tabular}", "\\caption{" + _latex_value(caption) + "}", "\\end{table}", ""])
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def load_baseline_validation(report_path=None):
    report_path = _as_path(report_path, DEFAULT_BASELINE_REPORT)
    if not report_path.exists():
        return {
            "schema_version": "phase8-baseline-validation-v1",
            "baseline_validation_status": "missing",
            "claim_ready": False,
            "passed": False,
            "sensitivity_gate_status": "blocked",
            "report_path": str(report_path),
            "failures": [
                _failure(
                    "baseline_report_missing",
                    "PHASE8_BASELINE_VALIDATION.json is missing, so Phase 8 sensitivity interpretation is blocked.",
                    _rel(report_path),
                )
            ],
        }
    try:
        report = _load_json(report_path)
    except Exception as exc:
        return {
            "schema_version": "phase8-baseline-validation-v1",
            "baseline_validation_status": "malformed",
            "claim_ready": False,
            "passed": False,
            "sensitivity_gate_status": "blocked",
            "report_path": str(report_path),
            "failures": [
                _failure(
                    "baseline_report_malformed",
                    "PHASE8_BASELINE_VALIDATION.json could not be parsed as JSON.",
                    _rel(report_path),
                    error=str(exc),
                )
            ],
        }
    if not isinstance(report, dict):
        return {
            "schema_version": "phase8-baseline-validation-v1",
            "baseline_validation_status": "malformed",
            "claim_ready": False,
            "passed": False,
            "sensitivity_gate_status": "blocked",
            "report_path": str(report_path),
            "failures": [
                _failure(
                    "baseline_report_not_object",
                    "PHASE8_BASELINE_VALIDATION.json must contain a JSON object.",
                    _rel(report_path),
                )
            ],
        }

    status = report.get("baseline_validation_status")
    if status not in {"passed", "blocked"}:
        status = "malformed"
    result = deepcopy(report)
    result["_path"] = str(report_path)
    result["_hash"] = sha256_file(report_path)
    result["baseline_validation_status"] = status
    result["passed"] = status == "passed"
    result["sensitivity_gate_status"] = "open" if status == "passed" else "blocked"
    result["claim_ready"] = bool(result.get("claim_ready")) and False
    if status != "passed" and not result.get("failures"):
        result["failures"] = [
            _failure(
                "baseline_validation_not_passed",
                "Phase 8 baseline validation did not pass, so sensitivity replay cannot be interpreted.",
                _rel(report_path),
                baseline_validation_status=status,
            )
        ]
    return result


def baseline_passed(report):
    return bool(report and report.get("baseline_validation_status") == "passed")


def load_phase8_suite(suite_name=DEFAULT_SUITE):
    suite = load_suite(suite_name)
    members = suite_members(suite)
    return suite, members


def latest_run_dir(studies_root, study_name):
    root = Path(studies_root) / study_name
    candidates = []
    if root.exists():
        candidates = [
            path
            for path in root.iterdir()
            if path.is_dir() and (path / "normalized_rows.json").exists() and (path / "study_summary.json").exists()
        ]
    if not candidates:
        raise FileNotFoundError("no completed source run found for study " + study_name + " under " + str(root))
    return sorted(candidates, key=lambda path: (path.stat().st_mtime, path.name), reverse=True)[0]


def load_sensitivity_run(run_dir, study_name=None):
    run_dir = Path(run_dir)
    rows_path = run_dir / "normalized_rows.json"
    summary_path = run_dir / "study_summary.json"
    manifest_path = run_dir / "manifest_snapshot.yaml"
    if not rows_path.exists():
        raise FileNotFoundError("missing normalized_rows.json: " + str(rows_path))
    if not summary_path.exists():
        raise FileNotFoundError("missing study_summary.json: " + str(summary_path))
    rows = _load_json(rows_path)
    summary = _load_json(summary_path)
    manifest = _load_yaml(manifest_path) if manifest_path.exists() else load_manifest(study_name or summary.get("study_name"))
    manifest["_path"] = str(manifest_path if manifest_path.exists() else manifest.get("_path", ""))
    return {
        "run_dir": run_dir,
        "rows": rows,
        "summary": summary,
        "manifest": manifest,
        "manifest_snapshot_path": manifest_path if manifest_path.exists() else None,
    }


def collect_sensitivity_runs(suite_name=DEFAULT_SUITE, studies_root=None):
    studies_root = _as_path(studies_root, DEFAULT_STUDIES_ROOT)
    suite, members = load_phase8_suite(suite_name)
    runs = []
    failures = []
    for study_name in members:
        try:
            run_dir = latest_run_dir(studies_root, study_name)
            runs.append(load_sensitivity_run(run_dir, study_name=study_name))
        except Exception as exc:
            failures.append(
                _failure(
                    "source_run_missing",
                    "Phase 8 sensitivity source run is missing or unreadable.",
                    _rel(studies_root / study_name),
                    study_name=study_name,
                    error=str(exc),
                )
            )
    return {"suite": suite, "members": members, "runs": runs, "failures": failures}


def _split_lookup(manifest):
    return {split.get("split_id"): split for split in manifest.get("splits", [])}


def _split_args(manifest, split):
    args = {}
    args.update(manifest.get("base_args") or {})
    args.update(split.get("args_overrides") or {})
    for field in ("seed", "data_seed", "data_seed_test"):
        if field in split:
            args[field] = split[field]
    if split.get("uptake_regime"):
        args["uptake_regime"] = split["uptake_regime"]
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
        axis = split.get("sensitivity_axis") or manifest.get("sensitivity_axis")
        sensitivity_value = split.get("sensitivity_value")
        if sensitivity_value is None:
            if axis == "menu_k":
                sensitivity_value = item.get("menu_k")
            elif axis == "eta_filter_mode":
                sensitivity_value = item.get("filter_mode")
            elif axis == "uptake_regime":
                sensitivity_value = item.get("uptake_regime")
            elif axis == "guardrail":
                sensitivity_value = args.get("service_quit_rate_guardrail")
        guardrail_fields = manifest.get("guardrail_fields") or (manifest.get("sensitivity_contract") or {}).get("guardrail_fields") or []
        for field in guardrail_fields:
            item[field] = args.get(field, item.get(field))
        item.update(
            {
                "sensitivity_axis": axis,
                "sensitivity_value": str(sensitivity_value) if sensitivity_value is not None else "",
                "center_value": str(split.get("center_value", manifest.get("center_value", ""))),
                "paired_group_id": split.get("paired_group_id", ""),
                "source_run_dir": _rel(run_data["run_dir"]),
                "source_run_id": summary.get("run_id") or item.get("run_id", ""),
                "source_study_name": summary.get("study_name") or manifest.get("name") or item.get("study_name", ""),
                "manifest_claim_ready": bool(manifest.get("claim_ready")),
                "manifest_output_intent": manifest.get("output_intent"),
                "sensitivity_contract_status": (manifest.get("sensitivity_contract") or {}).get("status"),
                "menu_eta_chance_threshold": args.get("menu_eta_chance_threshold"),
                "guardrail_fields": list(guardrail_fields),
                "service_quit_rate_guardrail": args.get("service_quit_rate_guardrail", item.get("service_quit_rate_guardrail")),
                "menu_optout_guardrail": args.get("menu_optout_guardrail", item.get("menu_optout_guardrail")),
                "claim_ready": False,
                "summary_status": SUMMARY_STATUS,
            }
        )
        if not item.get("filter_mode"):
            item["filter_mode"] = args.get("menu_eta_filter_mode")
        annotated.append(item)
    return annotated


def annotate_all_runs(runs):
    rows = []
    for run_data in runs:
        rows.extend(annotate_rows(run_data))
    return rows


def _completed(row):
    return row.get("status") == "completed" and row.get("execution_status") == "completed"


def _check_completed_row_accounting(row, failures):
    if row.get("checkpoint_required") and row.get("checkpoint_load_status") != "loaded":
        failures.append(
            _failure(
                "checkpoint_not_loaded",
                "completed Phase 8 sensitivity rows must report a loaded checkpoint.",
                row.get("checkpoint_path") or row.get("source_run_dir", ""),
                split_id=row.get("split_id"),
                source_study_name=row.get("source_study_name"),
            )
        )
    if row.get("checkpoint_required") and not row.get("checkpoint_hash"):
        failures.append(
            _failure(
                "checkpoint_hash_missing",
                "completed Phase 8 sensitivity rows must record checkpoint hash provenance.",
                row.get("checkpoint_path") or row.get("source_run_dir", ""),
                split_id=row.get("split_id"),
                source_study_name=row.get("source_study_name"),
            )
        )

    counts = [
        row.get("count_accepted_home"),
        row.get("count_accepted_meeting_point"),
        row.get("count_opted_out"),
    ]
    if any(value is None for value in counts):
        failures.append(
            _failure(
                "accounting_counts_missing",
                "completed Phase 8 sensitivity rows must keep opt-out, accepted-home, and accepted-meeting counts separate.",
                row.get("source_run_dir", ""),
                split_id=row.get("split_id"),
                source_study_name=row.get("source_study_name"),
            )
        )
        return
    accepted = int(row.get("count_accepted_home")) + int(row.get("count_accepted_meeting_point"))
    if int(row.get("accepted_count", -1)) != accepted:
        failures.append(
            _failure(
                "accepted_count_mismatch",
                "accepted_count must equal accepted home plus accepted meeting-point.",
                row.get("source_run_dir", ""),
                split_id=row.get("split_id"),
                source_study_name=row.get("source_study_name"),
            )
        )
    if int(row.get("served_count", -1)) != accepted:
        failures.append(
            _failure(
                "served_count_mismatch",
                "served_count must match accepted_count and exclude opt-out.",
                row.get("source_run_dir", ""),
                split_id=row.get("split_id"),
                source_study_name=row.get("source_study_name"),
            )
        )


def _manifest_failures(manifest):
    failures = []
    name = manifest.get("name", "")
    axis = manifest.get("sensitivity_axis")
    contract = manifest.get("sensitivity_contract") or {}
    if axis not in ALLOWED_AXES:
        failures.append(
            _failure(
                "executable_axis_not_allowed",
                "Phase 8 may execute only the four must-have sensitivity dimensions.",
                manifest.get("_path", ""),
                study_name=name,
                sensitivity_axis=axis,
            )
        )
    if manifest.get("claim_ready") is not False or contract.get("claim_ready") is not False:
        failures.append(
            _failure(
                "manifest_claim_ready_upgrade",
                "Phase 8 sensitivity manifests must keep claim_ready=false.",
                manifest.get("_path", ""),
                study_name=name,
            )
        )
    if manifest.get("run_mode") != "diagnostic" or manifest.get("output_intent") != SUMMARY_STATUS:
        failures.append(
            _failure(
                "manifest_status_not_diagnostic_provisional",
                "Phase 8 sensitivity manifests must remain diagnostic/provisional.",
                manifest.get("_path", ""),
                study_name=name,
            )
        )
    if not contract.get("one_factor_at_a_time"):
        failures.append(
            _failure(
                "one_factor_contract_missing",
                "Phase 8 sensitivity manifests must explicitly require one-factor-at-a-time reporting.",
                manifest.get("_path", ""),
                study_name=name,
            )
        )
    for split in manifest.get("splits", []):
        split_axis = split.get("sensitivity_axis", axis)
        if split_axis in DEFERRED_DIMENSIONS:
            failures.append(
                _failure(
                    "nice_to_have_axis_executed",
                    "Nice-to-have sensitivity dimensions are deferred and must not execute in Phase 8.",
                    manifest.get("_path", ""),
                    study_name=name,
                    split_id=split.get("split_id"),
                    sensitivity_axis=split_axis,
                )
            )
        overrides = split.get("args_overrides") or {}
        if axis == "eta_filter_mode" and overrides.get("menu_eta_filter_mode") == "chance_constraint":
            if _num(overrides.get("menu_eta_chance_threshold")) != EXPECTED_CHANCE_THRESHOLD:
                failures.append(
                    _failure(
                        "bad_chance_constraint_threshold",
                        "chance-constraint ETA sensitivity rows must use menu_eta_chance_threshold=0.25.",
                        manifest.get("_path", ""),
                        study_name=name,
                        split_id=split.get("split_id"),
                    )
                )
        if axis == "eta_filter_mode" and overrides.get("menu_eta_filter_mode") == "none":
            failures.append(
                _failure(
                    "no_filter_in_main_axis",
                    "no-filter is diagnostic boundary evidence only and cannot be part of main Phase 8 sensitivity.",
                    manifest.get("_path", ""),
                    study_name=name,
                    split_id=split.get("split_id"),
                )
            )
        if axis == "uptake_regime" and split.get("uptake_regime") not in EXPECTED_UPTAKE_REGIMES:
            failures.append(
                _failure(
                    "uptake_regime_not_allowed",
                    "Phase 8 uptake sensitivity is limited to low and medium regimes.",
                    manifest.get("_path", ""),
                    study_name=name,
                    split_id=split.get("split_id"),
                    uptake_regime=split.get("uptake_regime"),
                )
            )
    for field in NICE_TO_HAVE_ARG_FIELDS:
        values = {
            _split_args(manifest, split).get(field)
            for split in manifest.get("splits", [])
            if _split_args(manifest, split).get(field) is not None
        }
        if len(values) > 1:
            failures.append(
                _failure(
                    "nice_to_have_arg_varied",
                    "Nice-to-have experiment dimensions remain deferred in Phase 8.",
                    manifest.get("_path", ""),
                    study_name=name,
                    field=field,
                    values=sorted(str(value) for value in values),
                )
            )
    if axis == "guardrail":
        guardrail_fields = tuple(manifest.get("guardrail_fields") or contract.get("guardrail_fields") or [])
        if set(guardrail_fields) != set(EXPECTED_GUARDRAIL_FIELDS):
            failures.append(
                _failure(
                    "guardrail_fields_incomplete",
                    "Guardrail sensitivity must state that both service and opt-out guardrails vary.",
                    manifest.get("_path", ""),
                    study_name=name,
                    guardrail_fields=list(guardrail_fields),
                )
            )
        for split in manifest.get("splits", []):
            overrides = split.get("args_overrides") or {}
            missing = [field for field in EXPECTED_GUARDRAIL_FIELDS if field not in overrides]
            if missing:
                failures.append(
                    _failure(
                        "guardrail_split_missing_field",
                        "Each guardrail split must vary both guardrail fields together.",
                        manifest.get("_path", ""),
                        study_name=name,
                        split_id=split.get("split_id"),
                        missing_fields=missing,
                    )
                )
    return failures


def validate_sensitivity_rows(rows, manifests_by_study, strict=False, require_full_suite=True):
    rows = rows or []
    manifests = list((manifests_by_study or {}).values())
    failures = []
    axes = {manifest.get("sensitivity_axis") for manifest in manifests if manifest.get("sensitivity_axis")}
    unknown_axes = sorted(axes - set(ALLOWED_AXES))
    if unknown_axes:
        failures.append(
            _failure(
                "unknown_phase8_axis",
                "Phase 8 sensitivity axes must be limited to the must-have axis set.",
                "work2_coding/Experiments/studies/",
                observed_axes=unknown_axes,
            )
        )
    if require_full_suite and axes != set(ALLOWED_AXES):
        failures.append(
            _failure(
                "must_have_axes_incomplete",
                "Phase 8 sensitivity artifacts require exactly the four must-have axes.",
                "work2_coding/Experiments/suites/phase8_sensitivity_must_have.yaml",
                observed_axes=sorted(axes),
                expected_axes=list(ALLOWED_AXES),
            )
        )
    for manifest in manifests:
        failures.extend(_manifest_failures(manifest))

    if not rows:
        failures.append(
            _failure(
                "no_sensitivity_rows",
                "No normalized sensitivity rows are available.",
                "work2_coding/outputs/studies/",
            )
        )
    for row in rows:
        axis = row.get("sensitivity_axis")
        if axis not in ALLOWED_AXES:
            failures.append(
                _failure(
                    "row_axis_not_allowed",
                    "Sensitivity row uses an axis outside the Phase 8 must-have set.",
                    row.get("source_run_dir", ""),
                    split_id=row.get("split_id"),
                    sensitivity_axis=axis,
                )
            )
        if row.get("filter_mode") == "none" and row.get("policy_tag") == MAIN_POLICY_TAG:
            failures.append(
                _failure(
                    "no_filter_main_row",
                    "no-filter rows cannot be promoted as main deployable Phase 8 sensitivity evidence.",
                    row.get("source_run_dir", ""),
                    split_id=row.get("split_id"),
                    sensitivity_axis=axis,
                )
            )
        if axis == "eta_filter_mode" and row.get("sensitivity_value") == "chance_constraint":
            if _num(row.get("menu_eta_chance_threshold")) != EXPECTED_CHANCE_THRESHOLD:
                failures.append(
                    _failure(
                        "bad_chance_constraint_threshold",
                        "chance-constraint ETA sensitivity rows must use menu_eta_chance_threshold=0.25.",
                        row.get("source_run_dir", ""),
                        split_id=row.get("split_id"),
                        threshold=row.get("menu_eta_chance_threshold"),
                    )
                )
        if row.get("uptake_regime") not in EXPECTED_UPTAKE_REGIMES:
            failures.append(
                _failure(
                    "uptake_regime_not_allowed",
                    "Phase 8 sensitivity rows must use low or medium uptake regimes only.",
                    row.get("source_run_dir", ""),
                    split_id=row.get("split_id"),
                    uptake_regime=row.get("uptake_regime"),
                )
            )
        if row.get("manifest_claim_ready") or row.get("claim_ready"):
            failures.append(
                _failure(
                    "row_claim_ready_upgrade",
                    "Phase 8 sensitivity rows and summaries must remain claim_ready=false.",
                    row.get("source_run_dir", ""),
                    split_id=row.get("split_id"),
                )
            )
        if row.get("run_mode") != "diagnostic" or row.get("manifest_output_intent") != SUMMARY_STATUS:
            failures.append(
                _failure(
                    "row_not_diagnostic_provisional",
                    "Phase 8 sensitivity rows must remain diagnostic/provisional.",
                    row.get("source_run_dir", ""),
                    split_id=row.get("split_id"),
                    run_mode=row.get("run_mode"),
                    manifest_output_intent=row.get("manifest_output_intent"),
                )
            )
        if _completed(row):
            _check_completed_row_accounting(row, failures)

    report = {"valid": not failures, "failures": failures}
    if strict and failures:
        raise SensitivityValidationError(failures)
    return report


def _axis_sort_key(row):
    axis_order = {axis: idx for idx, axis in enumerate(ALLOWED_AXES)}
    value = row.get("sensitivity_value")
    number = _num(value)
    value_key = number if number is not None else str(value)
    return (axis_order.get(row.get("sensitivity_axis"), 99), str(value_key))


def aggregate_sensitivity_rows(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[(row.get("sensitivity_axis"), str(row.get("sensitivity_value")))].append(row)

    aggregates = []
    for (axis, value), group in groups.items():
        completed_count = sum(1 for row in group if _completed(row))
        aggregate = {
            "sensitivity_axis": axis,
            "sensitivity_value": value,
            "center_value": _stable_join(row.get("center_value") for row in group),
            "row_count": len(group),
            "completed_row_count": completed_count,
            "source_studies": _stable_join(row.get("source_study_name") for row in group),
            "source_run_ids": _stable_join(row.get("source_run_id") for row in group),
            "source_run_dirs": _stable_join(row.get("source_run_dir") for row in group),
            "paired_group_count": len({row.get("paired_group_id") for row in group if row.get("paired_group_id")}),
            "policy_tags": _stable_join(row.get("policy_tag") for row in group),
            "filter_modes": _stable_join(row.get("filter_mode") for row in group),
            "uptake_regimes": _stable_join(row.get("uptake_regime") for row in group),
            "checkpoint_statuses": _stable_join(row.get("checkpoint_load_status") for row in group),
            "service_quit_rate_guardrail": _stable_join(row.get("service_quit_rate_guardrail") for row in group),
            "menu_optout_guardrail": _stable_join(row.get("menu_optout_guardrail") for row in group),
            "status": "completed" if completed_count == len(group) else _stable_join(row.get("status") for row in group),
            "summary_status": SUMMARY_STATUS,
            "claim_ready": False,
            "acceptance_rate_mean": _mean(row.get("acceptance_rate") for row in group),
            "optout_rate_mean": _mean(row.get("optout_rate") for row in group),
            "home_share_mean": _mean(row.get("home_share") for row in group),
            "meeting_point_uptake_rate_mean": _mean(row.get("meeting_point_uptake_rate") for row in group),
            "net_profit_mean": _mean(row.get("net_profit") for row in group),
            "operational_cost_mean": _mean(row.get("operational_cost") for row in group),
            "total_cost_mean": _mean(row.get("total_cost") for row in group),
            "service_time_total_mean": _mean(row.get("service_time_total") for row in group),
            "menu_build_time_mean": _mean(row.get("menu_build_time") for row in group),
            "menu_utilization_mean": _mean(row.get("menu_utilization") for row in group),
        }
        aggregates.append(aggregate)

    centers = {}
    for row in aggregates:
        if str(row.get("sensitivity_value")) == str(row.get("center_value")):
            centers[row.get("sensitivity_axis")] = row
    for row in aggregates:
        center = centers.get(row.get("sensitivity_axis"))
        row["net_profit_delta_vs_center"] = None
        row["optout_rate_delta_vs_center"] = None
        if center:
            if row.get("net_profit_mean") is not None and center.get("net_profit_mean") is not None:
                row["net_profit_delta_vs_center"] = row["net_profit_mean"] - center["net_profit_mean"]
            if row.get("optout_rate_mean") is not None and center.get("optout_rate_mean") is not None:
                row["optout_rate_delta_vs_center"] = row["optout_rate_mean"] - center["optout_rate_mean"]
        row["boundary_interpretation"] = _boundary_label(row)
    return sorted(aggregates, key=_axis_sort_key)


def _boundary_label(row):
    if str(row.get("sensitivity_value")) == str(row.get("center_value")):
        return "center_value"
    profit_delta = row.get("net_profit_delta_vs_center")
    optout_delta = row.get("optout_rate_delta_vs_center")
    if profit_delta is None or optout_delta is None:
        return "diagnostic_metric_gap"
    tolerance = 1e-9
    if abs(profit_delta) <= tolerance and abs(optout_delta) <= tolerance:
        return "no_observed_change"
    if profit_delta > tolerance and optout_delta <= tolerance:
        return "potential_help"
    if profit_delta > tolerance and optout_delta > tolerance:
        return "profit_service_tradeoff"
    return "failure_or_lower_profit"


def _source_metadata(runs, rows):
    return {
        "source_run_dirs": sorted({_rel(run["run_dir"]) for run in runs}),
        "source_run_ids": sorted({run["summary"].get("run_id", "") for run in runs if run["summary"].get("run_id")}),
        "source_row_counts": {run["summary"].get("study_name", run["manifest"].get("name", "")): len(run["rows"]) for run in runs},
        "manifest_hashes": {
            run["summary"].get("study_name", run["manifest"].get("name", "")): run["summary"].get("manifest_hash")
            or next((row.get("manifest_hash") for row in run["rows"] if row.get("manifest_hash")), "")
            for run in runs
        },
        "git_provenance": {
            run["summary"].get("study_name", run["manifest"].get("name", "")): run["summary"].get("git_provenance", {})
            for run in runs
        },
        "row_count": len(rows),
    }


def artifact_metadata(artifact_path, artifact_kind, baseline_report, runs, rows, status_info):
    metadata = _source_metadata(runs, rows)
    metadata.update(
        {
            "schema_version": "phase8-sensitivity-artifact-metadata-v1",
            "phase": "08",
            "artifact_path": _rel(artifact_path),
            "artifact_kind": artifact_kind,
            "generated_at_utc": utc_now_iso(),
            "status": SUMMARY_STATUS,
            "artifact_gate_status": status_info.get("status", "blocked"),
            "claim_ready": False,
            "baseline_validation_status": baseline_report.get("baseline_validation_status"),
            "baseline_report_path": _rel(baseline_report.get("_path", baseline_report.get("report_path", ""))),
            "baseline_report_hash": baseline_report.get("_hash", ""),
            "source_rows": len(rows),
            "diagnostic_provisional": True,
        }
    )
    return metadata


def write_sidecar(artifact_path, artifact_kind, baseline_report, runs, rows, status_info):
    path = Path(str(artifact_path) + ".metadata.json")
    write_json(path, artifact_metadata(artifact_path, artifact_kind, baseline_report, runs, rows, status_info))
    return path


def _plot_bars(path, labels, series, ylabel, title):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 4.8))
    x = list(range(len(labels)))
    width = min(0.32, 0.8 / max(len(series), 1))
    for idx, (label, values) in enumerate(series):
        offset = (idx - (len(series) - 1) / 2) * width
        ax.bar([item + offset for item in x], values, width=width, label=label)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=35, ha="right")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def generate_sensitivity_figures(figures_dir, aggregates):
    figures_dir = Path(figures_dir)
    labels = [row["sensitivity_axis"] + "=" + str(row["sensitivity_value"]) for row in aggregates]
    if not labels:
        return []
    profit = [_num(row.get("net_profit_mean")) or 0.0 for row in aggregates]
    service = [_num(row.get("total_cost_mean")) or _num(row.get("service_time_total_mean")) or 0.0 for row in aggregates]
    acceptance = [_num(row.get("acceptance_rate_mean")) or 0.0 for row in aggregates]
    optout = [_num(row.get("optout_rate_mean")) or 0.0 for row in aggregates]
    paths = [
        _plot_bars(
            figures_dir / "profit_service_tradeoff.png",
            labels,
            [("net_profit", profit), ("service_or_total_cost", service)],
            "diagnostic metric",
            "Phase 8 diagnostic profit-service trade-off",
        ),
        _plot_bars(
            figures_dir / "optout_acceptance_by_axis.png",
            labels,
            [("acceptance_rate", acceptance), ("optout_rate", optout)],
            "rate",
            "Phase 8 diagnostic opt-out and acceptance by axis",
        ),
    ]
    return paths


def _blocked_artifact_result(output_root, baseline_report, failures, runs=None, rows=None, status_info=None):
    output_root = Path(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    runs = runs or []
    rows = rows or []
    status_info = status_info or {
        "status": "blocked",
        "claim_ready": False,
        "reasons": [failure["reason"] for failure in failures],
        "checkpoint_statuses": [],
        "uptake_regimes": [],
        "diagnostic_policy_labels": [],
        "blockers": failures,
    }
    status_path = output_root / "ARTIFACT_STATUS.json"
    result = {
        "schema_version": "phase8-sensitivity-artifacts-v1",
        "phase": "08",
        "status": SUMMARY_STATUS,
        "builder_status": "blocked",
        "claim_ready": False,
        "baseline_validation_status": baseline_report.get("baseline_validation_status"),
        "baseline_report_path": _rel(baseline_report.get("_path", baseline_report.get("report_path", ""))),
        "artifact_root": str(output_root),
        "artifact_status": status_info,
        "allowed_axes": list(ALLOWED_AXES),
        "deferred_dimensions": list(DEFERRED_DIMENSIONS),
        "failures": failures,
        "aggregate_rows": [],
        "artifacts": {"status": str(status_path)},
        "generated_artifacts": [str(status_path)],
    }
    result.update(_source_metadata(runs, rows))
    write_json(status_path, result)
    sidecar = write_sidecar(status_path, "status", baseline_report, runs, rows, status_info)
    result["artifacts"]["status_metadata"] = str(sidecar)
    result["generated_artifacts"].append(str(sidecar))
    write_json(status_path, result)
    return result


def build_sensitivity_artifacts(
    suite_name=DEFAULT_SUITE,
    studies_root=None,
    baseline_report=None,
    output_root=None,
):
    output_root = _as_path(output_root, DEFAULT_OUTPUT_ROOT)
    output_root.mkdir(parents=True, exist_ok=True)
    baseline = load_baseline_validation(baseline_report)
    if not baseline_passed(baseline):
        return _blocked_artifact_result(output_root, baseline, list(baseline.get("failures") or []))

    collection = collect_sensitivity_runs(suite_name=suite_name, studies_root=studies_root)
    runs = collection["runs"]
    rows = annotate_all_runs(runs)
    manifests = {run["manifest"].get("name", run["summary"].get("study_name", "")): run["manifest"] for run in runs}
    validation = validate_sensitivity_rows(rows, manifests, strict=False, require_full_suite=True)
    failures = list(collection["failures"]) + list(validation["failures"])
    status_info = classify_artifact(
        rows,
        {
            "tier": "pilot",
            "run_mode": "diagnostic",
            "execution_status": _stable_join(row.get("execution_status") for row in rows),
        },
        dependency_snapshot={"phase": "08", "baseline_validation_status": baseline.get("baseline_validation_status")},
    )
    status_info["claim_ready"] = False
    if failures:
        status_info["status"] = "blocked"
        status_info["reasons"] = sorted(set(status_info.get("reasons", []) + [failure["reason"] for failure in failures]))
        status_info["blockers"] = failures
        return _blocked_artifact_result(output_root, baseline, failures, runs=runs, rows=rows, status_info=status_info)

    aggregates = aggregate_sensitivity_rows(rows)
    artifacts = {}
    generated = []

    aggregate_json = output_root / "aggregates" / "sensitivity_axis_summary.json"
    aggregate_csv = output_root / "aggregates" / "sensitivity_axis_summary.csv"
    write_json(aggregate_json, aggregates)
    write_csv(aggregate_csv, aggregates)
    artifacts["aggregate_json"] = str(aggregate_json)
    artifacts["aggregate_csv"] = str(aggregate_csv)
    generated.extend([str(aggregate_json), str(aggregate_csv)])
    for path, kind in [(aggregate_json, "aggregate-json"), (aggregate_csv, "aggregate-csv")]:
        sidecar = write_sidecar(path, kind, baseline, runs, rows, status_info)
        artifacts[kind + "_metadata"] = str(sidecar)
        generated.append(str(sidecar))

    axis_table = output_root / "tables" / "sensitivity_axis_summary.tex"
    boundary_table = output_root / "tables" / "sensitivity_boundary_map.tex"
    write_latex_table(
        axis_table,
        "Phase 8 diagnostic sensitivity axis summary",
        aggregates,
        [
            "sensitivity_axis",
            "sensitivity_value",
            "row_count",
            "acceptance_rate_mean",
            "optout_rate_mean",
            "net_profit_mean",
            "status",
        ],
    )
    write_latex_table(
        boundary_table,
        "Phase 8 diagnostic sensitivity boundary map",
        aggregates,
        [
            "sensitivity_axis",
            "sensitivity_value",
            "center_value",
            "net_profit_delta_vs_center",
            "optout_rate_delta_vs_center",
            "boundary_interpretation",
        ],
    )
    artifacts["axis_table"] = str(axis_table)
    artifacts["boundary_table"] = str(boundary_table)
    generated.extend([str(axis_table), str(boundary_table)])
    for path, kind in [(axis_table, "latex-axis-table"), (boundary_table, "latex-boundary-table")]:
        sidecar = write_sidecar(path, kind, baseline, runs, rows, status_info)
        artifacts[kind + "_metadata"] = str(sidecar)
        generated.append(str(sidecar))

    for figure in generate_sensitivity_figures(output_root / "figures", aggregates):
        key = Path(figure).stem
        artifacts[key] = str(figure)
        generated.append(str(figure))
        sidecar = write_sidecar(figure, "figure", baseline, runs, rows, status_info)
        artifacts[key + "_metadata"] = str(sidecar)
        generated.append(str(sidecar))

    status_path = output_root / "ARTIFACT_STATUS.json"
    result = {
        "schema_version": "phase8-sensitivity-artifacts-v1",
        "phase": "08",
        "status": SUMMARY_STATUS,
        "builder_status": "completed",
        "claim_ready": False,
        "baseline_validation_status": baseline.get("baseline_validation_status"),
        "baseline_report_path": _rel(baseline.get("_path", baseline.get("report_path", ""))),
        "baseline_report_hash": baseline.get("_hash", ""),
        "artifact_root": str(output_root),
        "artifact_status": status_info,
        "allowed_axes": list(ALLOWED_AXES),
        "deferred_dimensions": list(DEFERRED_DIMENSIONS),
        "failures": [],
        "aggregate_rows": aggregates,
        "artifacts": artifacts,
        "generated_artifacts": generated + [str(status_path)],
    }
    result.update(_source_metadata(runs, rows))
    write_json(status_path, result)
    status_sidecar = write_sidecar(status_path, "status", baseline, runs, rows, status_info)
    result["artifacts"]["status"] = str(status_path)
    result["artifacts"]["status_metadata"] = str(status_sidecar)
    result["generated_artifacts"].append(str(status_sidecar))
    write_json(status_path, result)
    return result


def _frontmatter(result):
    lines = [
        "---",
        "status: " + SUMMARY_STATUS,
        "claim_ready: false",
        "baseline_validation_status: " + str(result.get("baseline_validation_status", "missing")),
        "artifact_root: " + str(result.get("artifact_root", "")),
        "generated_at_utc: " + utc_now_iso(),
        "source_run_ids:",
    ]
    run_ids = result.get("source_run_ids") or []
    if run_ids:
        lines.extend("  - " + str(run_id) for run_id in run_ids)
    else:
        lines.append("  - none")
    lines.extend(["---", ""])
    return lines


def _axis_markdown_rows(aggregates):
    if not aggregates:
        return [
            {
                "sensitivity_axis": axis,
                "sensitivity_value": "blocked",
                "row_count": 0,
                "acceptance_rate_mean": None,
                "optout_rate_mean": None,
                "net_profit_mean": None,
                "boundary_interpretation": "blocked_by_gate",
            }
            for axis in ALLOWED_AXES
        ]
    return aggregates


def render_sensitivity_summary(result):
    aggregates = result.get("aggregate_rows") or []
    lines = _frontmatter(result)
    lines.extend(
        [
            "# Phase 8 Sensitivity Summary",
            "",
            "This file is generated from Phase 8 normalized rows and manifest snapshots. It is a diagnostic conditional boundary map, not claim-ready evidence.",
            "",
            "## Baseline Gate",
            "",
        ]
    )
    baseline_status = result.get("baseline_validation_status", "missing")
    if result.get("builder_status") == "completed" and baseline_status == "passed":
        lines.append("Baseline validation status is `passed`; diagnostic sensitivity artifacts were generated with `claim_ready: false`.")
    else:
        lines.append(
            "Sensitivity replay interpretation is blocked because baseline validation status is `"
            + str(baseline_status)
            + "` or a source contract failed."
        )
        for failure in result.get("failures") or []:
            lines.append("- `" + failure.get("code", "failure") + "`: " + failure.get("reason", ""))
    lines.extend(["", "## Must-Have Axis Table", ""])
    lines.append("| sensitivity_axis | sensitivity_value | rows | acceptance_rate | optout_rate | net_profit | boundary |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | --- |")
    for row in _axis_markdown_rows(aggregates):
        lines.append(
            "| "
            + str(row.get("sensitivity_axis"))
            + " | "
            + str(row.get("sensitivity_value"))
            + " | "
            + str(row.get("row_count", 0))
            + " | "
            + _format_value(row.get("acceptance_rate_mean"))
            + " | "
            + _format_value(row.get("optout_rate_mean"))
            + " | "
            + _format_value(row.get("net_profit_mean"))
            + " | "
            + str(row.get("boundary_interpretation", "blocked"))
            + " |"
        )
    lines.extend(["", "## Conditional Boundary Map", ""])
    if aggregates:
        for row in aggregates:
            lines.append(
                "- `"
                + str(row.get("sensitivity_axis"))
                + "="
                + str(row.get("sensitivity_value"))
                + "` is classified as `"
                + str(row.get("boundary_interpretation"))
                + "` relative to center `"
                + str(row.get("center_value"))
                + "`."
            )
    else:
        lines.append("- Boundary interpretation is blocked until baseline validation and source-row contracts pass.")
    lines.extend(
        [
            "",
            "## Deferred Nice-To-Have Dimensions",
            "",
            "- `max_candidates`: candidate pool size sensitivity is deferred.",
            "- `fleet_capacity_stress`: fleet and capacity stress sensitivity is deferred.",
            "- `pricing_bounds`: price-bound sensitivity is deferred.",
            "- `price_sensitivity`: pricing response sensitivity is deferred.",
            "",
            "## Claim Boundary",
            "",
            "No abstract, conclusion, or managerial claim upgrade is authorized by Phase 8. Results remain `diagnostic_provisional_blocked` with `claim_ready: false`.",
            "",
            "## Source Artifacts",
            "",
        ]
    )
    artifacts = result.get("artifacts") or {}
    if artifacts:
        for key in sorted(artifacts):
            lines.append("- `" + key + "`: `" + str(artifacts[key]).replace("\\", "/") + "`")
    else:
        lines.append("- No generated sensitivity artifacts are available.")
    lines.append("")
    return "\n".join(lines)


def write_sensitivity_summary(
    suite_name=DEFAULT_SUITE,
    studies_root=None,
    baseline_report=None,
    artifact_root=None,
    planning_output=None,
):
    result = build_sensitivity_artifacts(
        suite_name=suite_name,
        studies_root=studies_root,
        baseline_report=baseline_report,
        output_root=artifact_root,
    )
    output = _as_path(planning_output, DEFAULT_SUMMARY_PATH)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_sensitivity_summary(result), encoding="utf-8")
    return {"summary_path": str(output), "artifact_result": result}
