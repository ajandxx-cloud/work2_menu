import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
PHASE_DIR = PROJECT_ROOT / ".planning" / "phases" / "04-phase08-pilot-and-decision-gate"
DEFAULT_OUTPUT_DIR = PHASE_DIR / "artifacts"
FORMAL_ARTIFACTS_DIR = ROOT / "artifacts"
PILOT_STUDY_NAME = "work2_phase08_pilot"
EXPECTED_SEEDS = [0, 1, 2]
REQUIRED_TAGS = [
    "nearest_L",
    "cost_L",
    "cnn_menu",
    "cnn_setmenu_net_current",
    "expected_profit_enumeration",
    "service_constrained_expected_profit",
    "cost_oracle",
    "profit_oracle",
]
NEW_METHOD_TAGS = ["expected_profit_enumeration", "service_constrained_expected_profit"]
COMPARATOR_TAGS = ["cost_L", "cnn_menu"]
DIAGNOSTIC_ORACLE_TAGS = ["cost_oracle", "profit_oracle"]
REQUIRED_METRICS = [
    "adjusted_profit",
    "service_quit_rate_guardrail",
    "service_guardrail_pass",
    "service_guardrail_violation",
    "service_constrained_net_profit",
    "opt_out_rate",
    "avg_exact_enumerated_menu_count",
    "service_constrained_fallback_rate",
]
PILOT_CSV_FIELDS = [
    "study_name",
    "run_id",
    "study_dir",
    "manifest_hash",
    "split_id",
    "seed",
    "variant_tag",
    "variant_label",
    "policy",
    "menu_k",
    "candidate_pool_size",
    "displayed_meeting_points",
    "home_always_shown",
    "net_profit",
    "adjusted_profit",
    "service_constrained_net_profit",
    "opt_out_rate",
    "service_quit_rate_guardrail",
    "service_guardrail_pass",
    "service_guardrail_violation",
    "avg_exact_enumerated_menu_count",
    "service_constrained_fallback_rate",
]


class GateError(ValueError):
    pass


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Build Phase08 pilot decision artifacts from an explicit study run.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--run-id", help="Run id under outputs/studies/work2_phase08_pilot/")
    source.add_argument("--study-dir", help="Explicit work2_phase08_pilot study output directory")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Phase-local artifact output directory")
    return parser.parse_args(argv)


def resolve_study_dir(args):
    if args.run_id:
        return ROOT / "outputs" / "studies" / PILOT_STUDY_NAME / args.run_id
    return Path(args.study_dir)


def resolve_output_dir(path):
    output_dir = Path(path)
    if not output_dir.is_absolute():
        output_dir = PROJECT_ROOT / output_dir
    resolved = output_dir.resolve()
    formal = FORMAL_ARTIFACTS_DIR.resolve()
    if resolved == formal or formal in resolved.parents:
        raise GateError("Phase08 artifacts must not be written under ooh_code/artifacts")
    return resolved


def load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def load_rows(study_dir):
    json_path = study_dir / "normalized_rows.json"
    csv_path = study_dir / "normalized_rows.csv"
    if json_path.exists():
        rows = load_json(json_path)
        source = json_path
    elif csv_path.exists():
        with open(csv_path, "r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        source = csv_path
    else:
        raise GateError("missing normalized_rows.json or normalized_rows.csv")
    if not isinstance(rows, list) or not rows:
        raise GateError("normalized rows are empty or invalid")
    return rows, source


def coerce_number(row, key, allow_null=False):
    value = row.get(key)
    if value is None or value == "":
        if allow_null:
            return None
        raise GateError(f"missing required numeric metric {key} for {row_identity(row)}")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise GateError(f"unparseable numeric metric {key} for {row_identity(row)}") from exc
    if not math.isfinite(number):
        raise GateError(f"non-finite numeric metric {key} for {row_identity(row)}")
    return number


def coerce_bool(row, key):
    value = row.get(key)
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    if text in {"1", "1.0", "true", "yes"}:
        return True
    if text in {"0", "0.0", "false", "no"}:
        return False
    raise GateError(f"unparseable boolean metric {key} for {row_identity(row)}")


def coerce_rate(row, key):
    value = coerce_number(row, key)
    if value < -1e-12 or value > 1.0 + 1e-12:
        raise GateError(f"rate metric {key} is outside [0, 1] for {row_identity(row)}")
    return min(max(value, 0.0), 1.0)


def row_identity(row):
    return f"seed={row.get('seed')} tag={row.get('variant_tag')}"


def is_reference_row(row):
    value = row.get("is_reference")
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "1.0", "true", "yes"}


def validate_summary(study_dir, summary):
    study = summary.get("study", {})
    metadata = summary.get("run_metadata", {})
    if study.get("name") != PILOT_STUDY_NAME:
        raise GateError(f"study_summary.json must describe {PILOT_STUDY_NAME}")
    if metadata.get("status") != "completed":
        raise GateError("study_summary.json status must be completed")
    if int(metadata.get("completed_splits", -1)) != len(EXPECTED_SEEDS):
        raise GateError("completed_splits must match Phase08 pilot seeds")
    if int(metadata.get("expected_splits", -1)) != len(EXPECTED_SEEDS):
        raise GateError("expected_splits must match Phase08 pilot seeds")
    if metadata.get("study_root"):
        expected = Path(metadata["study_root"]).resolve()
        if expected != study_dir.resolve():
            raise GateError("study_summary.json study_root does not match explicit study directory")


def validate_rows(rows):
    pilot_rows = [dict(row) for row in rows if not is_reference_row(row)]
    seen = {}
    errors = []
    for row in pilot_rows:
        try:
            seed = int(coerce_number(row, "seed"))
        except GateError as exc:
            errors.append(str(exc))
            continue
        tag = str(row.get("variant_tag", ""))
        key = (seed, tag)
        if tag in REQUIRED_TAGS:
            if key in seen:
                errors.append(f"duplicated policy x seed row for seed={seed} tag={tag}")
            seen[key] = row

    for seed in EXPECTED_SEEDS:
        for tag in REQUIRED_TAGS:
            if (seed, tag) not in seen:
                errors.append(f"missing policy x seed row for seed={seed} tag={tag}")

    if errors:
        raise GateError("; ".join(errors))

    for row in seen.values():
        guardrail = coerce_number(row, "service_quit_rate_guardrail")
        opt_out = coerce_number(row, "opt_out_rate")
        pass_rate = coerce_rate(row, "service_guardrail_pass")
        violation_rate = coerce_rate(row, "service_guardrail_violation")
        if abs((pass_rate + violation_rate) - 1.0) > 1e-9:
            raise GateError(f"service guardrail pass/violation rates must sum to 1 for {row_identity(row)}")
        if opt_out > guardrail + 1e-12 and violation_rate <= 0:
            raise GateError(f"service_guardrail_violation disagrees with opt_out_rate for {row_identity(row)}")
        for metric in REQUIRED_METRICS:
            if metric == "service_constrained_net_profit":
                coerce_number(row, metric, allow_null=violation_rate > 0)
            elif metric in {"service_guardrail_pass", "service_guardrail_violation"}:
                coerce_rate(row, metric)
            else:
                coerce_number(row, metric)

    return [seen[(seed, tag)] for seed in EXPECTED_SEEDS for tag in REQUIRED_TAGS]


def mean(values):
    values = list(values)
    return sum(values) / len(values) if values else None


def summarize_by_tag(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["variant_tag"]].append(row)
    summaries = {}
    for tag, tag_rows in grouped.items():
        service_values = [
            coerce_number(row, "service_constrained_net_profit", allow_null=True)
            for row in tag_rows
            if coerce_number(row, "service_constrained_net_profit", allow_null=True) is not None
        ]
        summaries[tag] = {
            "tag": tag,
            "label": tag_rows[0].get("variant_label", tag),
            "mean_service_constrained_net_profit": mean(service_values),
            "mean_adjusted_profit": mean(coerce_number(row, "adjusted_profit") for row in tag_rows),
            "mean_net_profit": mean(coerce_number(row, "net_profit", allow_null=True) for row in tag_rows),
            "mean_opt_out_rate": mean(coerce_number(row, "opt_out_rate") for row in tag_rows),
            "max_opt_out_rate": max(coerce_number(row, "opt_out_rate") for row in tag_rows),
            "guardrail": max(coerce_number(row, "service_quit_rate_guardrail") for row in tag_rows),
            "guardrail_violations": sum(1 for row in tag_rows if coerce_rate(row, "service_guardrail_violation") > 0),
            "max_guardrail_violation_rate": max(coerce_rate(row, "service_guardrail_violation") for row in tag_rows),
            "max_fallback_rate": max(coerce_number(row, "service_constrained_fallback_rate") for row in tag_rows),
            "mean_exact_enumerated_menu_count": mean(coerce_number(row, "avg_exact_enumerated_menu_count") for row in tag_rows),
            "eligible": all(coerce_rate(row, "service_guardrail_violation") <= 0 for row in tag_rows)
            and len(service_values) == len(tag_rows),
        }
    return summaries


def classify_decision(rows):
    summaries = summarize_by_tag(rows)
    reasons = []
    recalibration_evidence = []
    scenario_evidence = []

    service_constrained = summaries["service_constrained_expected_profit"]
    if service_constrained["max_fallback_rate"] > 0:
        recalibration_evidence.append("Service-Constrained Expected-Profit used fallback on at least one seed.")

    for tag in NEW_METHOD_TAGS:
        if summaries[tag]["guardrail_violations"]:
            recalibration_evidence.append(f"{tag} violated the quit-rate guardrail.")
        if not summaries[tag]["eligible"]:
            recalibration_evidence.append(f"{tag} has ineligible service-constrained profit rows.")

    all_high_opt_out = all(summaries[tag]["mean_opt_out_rate"] > summaries[tag]["guardrail"] for tag in REQUIRED_TAGS)
    if all_high_opt_out:
        scenario_evidence.append("All Phase08 policies have mean opt-out above the quit-rate guardrail.")

    comparator_values = [
        summaries["cost_L"]["mean_service_constrained_net_profit"],
        summaries["cnn_menu"]["mean_service_constrained_net_profit"],
    ]
    comparators_available = all(value is not None for value in comparator_values)
    comparator_best = max(comparator_values) if comparators_available else None
    if not comparators_available:
        scenario_evidence.append("Cost-L or CNN-Menu has unavailable service-constrained profit, so the hard comparison gate cannot proceed.")

    profit_oracle = summaries["profit_oracle"]
    profit_oracle_mean = profit_oracle["mean_service_constrained_net_profit"]
    if (
        not profit_oracle["eligible"]
        or profit_oracle_mean is None
        or (comparators_available and profit_oracle_mean <= comparator_best)
    ):
        scenario_evidence.append("Profit Oracle did not provide a clear service-constrained reference above Cost-L and CNN-Menu.")

    candidate_results = []
    for tag in NEW_METHOD_TAGS:
        summary = summaries[tag]
        beats = (
            summary["eligible"]
            and comparators_available
            and summary["mean_service_constrained_net_profit"] > summaries["cost_L"]["mean_service_constrained_net_profit"]
            and summary["mean_service_constrained_net_profit"] > summaries["cnn_menu"]["mean_service_constrained_net_profit"]
        )
        candidate_results.append((tag, beats))
    winning_new_methods = [tag for tag, beats in candidate_results if beats]

    if winning_new_methods and not recalibration_evidence:
        decision_state = "proceed_to_formal"
        reasons.append(
            "At least one expected-profit method beats Cost-L and CNN-Menu on mean service-constrained net profit with no guardrail violation."
        )
    elif scenario_evidence and not recalibration_evidence:
        decision_state = "diagnose_scenario_design"
        reasons.extend(scenario_evidence)
    else:
        decision_state = "recalibrate_objective"
        if recalibration_evidence:
            reasons.extend(recalibration_evidence)
        else:
            reasons.append("Expected-profit methods did not beat both Cost-L and CNN-Menu on the service-constrained gate.")
        reasons.extend(scenario_evidence)

    return {
        "decision_state": decision_state,
        "pilot_complete": True,
        "human_confirmation_required": decision_state == "proceed_to_formal",
        "winning_new_methods": winning_new_methods,
        "reasons": reasons,
        "summaries": summaries,
    }


def format_float(value, digits=3):
    if value is None:
        return "--"
    return f"{float(value):.{digits}f}"


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_pilot_rows(path, rows, study_dir):
    fieldnames = list(PILOT_CSV_FIELDS)
    discovered = set(fieldnames)
    for row in rows:
        for key in row:
            if key not in discovered:
                fieldnames.append(key)
                discovered.add(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            out = dict(row)
            out["study_dir"] = str(study_dir)
            writer.writerow(out)


def markdown_table(headers, rows):
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def report_metadata(summary, row_source):
    study = summary.get("study", {})
    run = summary.get("run_metadata", {})
    return [
        f"- Study: `{study.get('name', PILOT_STUDY_NAME)}`",
        f"- Run id: `{run.get('run_id', '')}`",
        f"- Manifest hash: `{study.get('manifest_hash', '')}`",
        f"- Row source: `{row_source}`",
        f"- Status: `{run.get('status', '')}`",
    ]


def build_reports(summary, row_source, study_dir, decision, output_dir):
    summaries = decision["summaries"]
    table_rows = []
    for tag in REQUIRED_TAGS:
        item = summaries[tag]
        table_rows.append(
            [
                tag,
                format_float(item["mean_service_constrained_net_profit"]),
                format_float(item["mean_adjusted_profit"]),
                format_float(item["mean_net_profit"]),
                format_float(item["mean_opt_out_rate"]),
                item["guardrail_violations"],
                format_float(item["max_fallback_rate"]),
            ]
        )

    pilot_summary = [
        "# Phase08 Pilot Summary",
        "",
        "## Run Metadata",
        *report_metadata(summary, row_source),
        "",
        "## Gate Outcome",
        f"- Decision state: `{decision['decision_state']}`",
        f"- Pilot complete: `{str(decision['pilot_complete']).lower()}`",
        f"- Human confirmation required: `{str(decision['human_confirmation_required']).lower()}`",
        "",
        "## Policy Means",
        markdown_table(
            [
                "Policy",
                "Mean service-constrained profit",
                "Mean adjusted profit",
                "Mean raw profit",
                "Mean opt-out",
                "Guardrail violations",
                "Max fallback",
            ],
            table_rows,
        ),
        "",
        "## Reasons",
        *[f"- {reason}" for reason in decision["reasons"]],
        "",
        "## Next Action",
        next_action(decision["decision_state"]),
        "",
    ]

    oracle_rows = []
    for tag in DIAGNOSTIC_ORACLE_TAGS:
        item = summaries[tag]
        oracle_rows.append(
            [
                tag,
                format_float(item["mean_service_constrained_net_profit"]),
                format_float(item["mean_opt_out_rate"]),
                item["guardrail_violations"],
            ]
        )
    oracle_diagnostics = [
        "# Phase08 Oracle Diagnostics",
        "",
        "Cost Oracle is an insertion-cost diagnostic. Profit Oracle is a choice-aware expected-profit reference.",
        "",
        markdown_table(
            ["Oracle", "Mean service-constrained profit", "Mean opt-out", "Guardrail violations"],
            oracle_rows,
        ),
        "",
        "## Interpretation",
        "- Cost Oracle should not be treated as the primary profit upper bound.",
        "- Profit Oracle failing to clear Cost-L and CNN-Menu is scenario-design evidence, not proof of the expected-profit heuristic.",
        "",
    ]

    tradeoff_rows = []
    for tag in REQUIRED_TAGS:
        item = summaries[tag]
        tradeoff_rows.append(
            [
                tag,
                format_float(item["mean_net_profit"]),
                format_float(item["mean_adjusted_profit"]),
                format_float(item["mean_service_constrained_net_profit"]),
                format_float(item["mean_opt_out_rate"]),
                "yes" if item["eligible"] else "no",
            ]
        )
    profit_vs_quit = [
        "# Phase08 Profit Versus Quit Tradeoff",
        "",
        "Raw profit is diagnostic only; the gate uses service-constrained profit and quit-rate eligibility.",
        "",
        markdown_table(
            ["Policy", "Raw profit", "Adjusted profit", "Service-constrained profit", "Opt-out", "Eligible"],
            tradeoff_rows,
        ),
        "",
        "## Guardrail",
        f"- Quit-rate guardrail: `{format_float(next(iter(summaries.values()))['guardrail'])}`",
        "- Policies exceeding the guardrail are ineligible for proceed-to-formal decisions.",
        "",
    ]

    decision_lines = [
        "---",
        f"decision_state: {decision['decision_state']}",
        "pilot_complete: true",
        f"human_confirmation_required: {str(decision['human_confirmation_required']).lower()}",
        f"run_id: {summary.get('run_metadata', {}).get('run_id', '')}",
        f"study_dir: {study_dir}",
        f"manifest_hash: {summary.get('study', {}).get('manifest_hash', '')}",
        "---",
        "",
        "# Phase08 Decision Memo",
        "",
        "## Gate Result",
        f"- State: `{decision['decision_state']}`",
        f"- Winning new methods: `{', '.join(decision['winning_new_methods']) or 'none'}`",
        "",
        "## Reasons",
        *[f"- {reason}" for reason in decision["reasons"]],
        "",
        "## Guardrails",
        "- Proceed requires a new expected-profit method to beat Cost-L and CNN-Menu on mean service-constrained net profit.",
        "- Proceed is blocked by any guardrail violation for the winning method.",
        "- Service-Constrained Expected-Profit fallback above zero is recalibration evidence.",
        "",
        "## Stop Condition",
        next_action(decision["decision_state"]),
        "",
    ]

    write_text(output_dir / "pilot_summary.md", "\n".join(pilot_summary))
    write_text(output_dir / "oracle_diagnostics.md", "\n".join(oracle_diagnostics))
    write_text(output_dir / "profit_vs_quit_tradeoff.md", "\n".join(profit_vs_quit))
    write_text(output_dir / "phase08_decision.md", "\n".join(decision_lines))


def next_action(decision_state):
    if decision_state == "proceed_to_formal":
        return "Stop for human confirmation before starting Phase 5 formal evidence."
    if decision_state == "recalibrate_objective":
        return "Stop and review objective parameters, fallback behavior, and service penalties before formal runtime."
    return "Stop and diagnose scenario design, candidate generation, pricing range, or outside-option calibration."


def run(argv=None):
    args = parse_args(argv)
    study_dir = resolve_study_dir(args).resolve()
    output_dir = resolve_output_dir(args.output_dir)
    summary_path = study_dir / "study_summary.json"
    if not summary_path.exists():
        raise GateError(f"missing study_summary.json at {summary_path}")
    summary = load_json(summary_path)
    validate_summary(study_dir, summary)
    rows, row_source = load_rows(study_dir)
    validated_rows = validate_rows(rows)
    decision = classify_decision(validated_rows)
    output_dir.mkdir(parents=True, exist_ok=True)
    write_pilot_rows(output_dir / "pilot_rows.csv", sorted(rows, key=lambda row: (int(row.get("seed", -1)), str(row.get("variant_tag", "")))), study_dir)
    build_reports(summary, row_source, study_dir, decision, output_dir)
    return {
        "output_dir": str(output_dir),
        "decision_state": decision["decision_state"],
        "pilot_complete": decision["pilot_complete"],
        "human_confirmation_required": decision["human_confirmation_required"],
        "files": [
            str(output_dir / "pilot_rows.csv"),
            str(output_dir / "pilot_summary.md"),
            str(output_dir / "oracle_diagnostics.md"),
            str(output_dir / "profit_vs_quit_tradeoff.md"),
            str(output_dir / "phase08_decision.md"),
        ],
    }


def main(argv=None):
    try:
        result = run(argv)
    except GateError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
