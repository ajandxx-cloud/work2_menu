import argparse
import csv
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
PHASE_DIR = PROJECT_ROOT / ".planning" / "phases" / "WORK2-CHOICE-05-formal-evidence-and-manuscript-artifacts"
DEFAULT_OUTPUT_DIR = PHASE_DIR / "artifacts"
FORMAL_ARTIFACTS_DIR = ROOT / "artifacts"
STUDY_NAME = "work2_phase08_gap_closure"
EXPECTED_SEEDS = [0, 1, 2]
EXPECTED_GRID = [
    (100.0, 0.3),
    (100.0, 0.4),
    (200.0, 0.3),
    (200.0, 0.4),
    (500.0, 0.3),
    (500.0, 0.4),
]
BASE_TAGS = [
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
ROWS_FIELDS = [
    "study_name",
    "run_id",
    "study_dir",
    "manifest_hash",
    "row_source",
    "split_id",
    "seed",
    "grid_id",
    "service_quit_penalty",
    "service_quit_rate_guardrail",
    "base_policy_tag",
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
    "service_guardrail_pass",
    "service_guardrail_violation",
    "avg_exact_enumerated_menu_count",
    "service_constrained_fallback_rate",
]


class GateError(ValueError):
    pass


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Build Phase08 gap-closure artifacts from an explicit study run."
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--run-id", help=f"Run id under outputs/studies/{STUDY_NAME}/")
    source.add_argument("--study-dir", help=f"Explicit {STUDY_NAME} study output directory")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Phase-local artifact output directory")
    return parser.parse_args(argv)


def resolve_study_dir(args):
    if args.run_id:
        return ROOT / "outputs" / "studies" / STUDY_NAME / args.run_id
    return Path(args.study_dir)


def resolve_output_dir(path):
    output_dir = Path(path)
    if not output_dir.is_absolute():
        output_dir = PROJECT_ROOT / output_dir
    resolved = output_dir.resolve()
    formal = FORMAL_ARTIFACTS_DIR.resolve()
    if resolved == formal or formal in resolved.parents:
        raise GateError("Phase08 gap-closure artifacts must not be written under ooh_code/artifacts")
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


def row_identity(row):
    return f"seed={row.get('seed')} tag={row.get('variant_tag')}"


def is_reference_row(row):
    value = row.get("is_reference")
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "1.0", "true", "yes"}


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


def coerce_rate(row, key):
    value = coerce_number(row, key)
    if value < -1e-12 or value > 1.0 + 1e-12:
        raise GateError(f"rate metric {key} is outside [0, 1] for {row_identity(row)}")
    return min(max(value, 0.0), 1.0)


def parse_policy_tag(tag):
    match = re.match(r"^p(?P<penalty>\d+)_g(?P<guardrail>\d{2})_(?P<base>.+)$", str(tag))
    if not match:
        raise GateError(f"variant tag does not use grid convention: {tag}")
    penalty = float(match.group("penalty"))
    guardrail = float(int(match.group("guardrail"))) / 10.0
    base_tag = match.group("base")
    if base_tag not in BASE_TAGS:
        raise GateError(f"unknown base policy tag in {tag}")
    if (penalty, guardrail) not in EXPECTED_GRID:
        raise GateError(f"unexpected grid configuration in {tag}")
    return {
        "grid_id": f"p{int(penalty)}_g{int(guardrail * 10):02d}",
        "service_quit_penalty": penalty,
        "service_quit_rate_guardrail": guardrail,
        "base_policy_tag": base_tag,
    }


def validate_summary(study_dir, summary):
    study = summary.get("study", {})
    metadata = summary.get("run_metadata", {})
    split_ids = {split.get("split_id") for split in summary.get("splits", [])}
    if study.get("name") != STUDY_NAME:
        raise GateError(f"study_summary.json must describe {STUDY_NAME}")
    if metadata.get("status") != "completed":
        raise GateError("study_summary.json status must be completed")
    if int(metadata.get("completed_splits", -1)) != len(EXPECTED_SEEDS):
        raise GateError("completed_splits must match gap-closure seeds")
    if int(metadata.get("expected_splits", -1)) != len(EXPECTED_SEEDS):
        raise GateError("expected_splits must match gap-closure seeds")
    if split_ids != {f"seed{seed}" for seed in EXPECTED_SEEDS}:
        raise GateError("study_summary.json splits must match gap-closure seeds")
    if metadata.get("study_root"):
        expected = Path(metadata["study_root"]).resolve()
        if expected != study_dir.resolve():
            raise GateError("study_summary.json study_root does not match explicit study directory")


def enrich_row(row, row_source, study_dir, summary):
    enriched = dict(row)
    tag_info = parse_policy_tag(enriched.get("variant_tag", ""))
    enriched.update(tag_info)
    enriched["study_dir"] = str(study_dir)
    enriched["row_source"] = str(row_source)
    enriched["manifest_hash"] = enriched.get("manifest_hash") or summary.get("study", {}).get("manifest_hash", "")
    return enriched


def validate_rows(rows, row_source, study_dir, summary):
    enriched_rows = []
    seen = {}
    errors = []
    for raw_row in rows:
        if is_reference_row(raw_row):
            continue
        try:
            row = enrich_row(raw_row, row_source, study_dir, summary)
            seed = int(coerce_number(row, "seed"))
            key = (row["grid_id"], seed, row["base_policy_tag"])
            if key in seen:
                errors.append(f"duplicated grid x seed x policy row for {key}")
            seen[key] = row
            enriched_rows.append(row)
        except GateError as exc:
            errors.append(str(exc))

    for penalty, guardrail in EXPECTED_GRID:
        grid_id = f"p{int(penalty)}_g{int(guardrail * 10):02d}"
        for seed in EXPECTED_SEEDS:
            for base_tag in BASE_TAGS:
                if (grid_id, seed, base_tag) not in seen:
                    errors.append(f"missing row for grid={grid_id} seed={seed} policy={base_tag}")

    if errors:
        raise GateError("; ".join(errors))

    for row in seen.values():
        guardrail = coerce_number(row, "service_quit_rate_guardrail")
        expected_guardrail = float(row["service_quit_rate_guardrail"])
        if abs(guardrail - expected_guardrail) > 1e-9:
            raise GateError(f"row guardrail disagrees with grid tag for {row_identity(row)}")
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
    return sorted(
        enriched_rows,
        key=lambda row: (row["grid_id"], int(coerce_number(row, "seed")), row["base_policy_tag"]),
    )


def mean(values):
    values = list(values)
    return sum(values) / len(values) if values else None


def format_float(value, digits=3):
    if value is None:
        return "--"
    return f"{float(value):.{digits}f}"


def summarize_group(rows):
    service_values = [
        coerce_number(row, "service_constrained_net_profit", allow_null=True)
        for row in rows
        if coerce_number(row, "service_constrained_net_profit", allow_null=True) is not None
    ]
    return {
        "mean_service_constrained_net_profit": mean(service_values),
        "mean_adjusted_profit": mean(coerce_number(row, "adjusted_profit") for row in rows),
        "mean_net_profit": mean(coerce_number(row, "net_profit", allow_null=True) for row in rows),
        "mean_opt_out_rate": mean(coerce_number(row, "opt_out_rate") for row in rows),
        "guardrail_violations": sum(1 for row in rows if coerce_rate(row, "service_guardrail_violation") > 0),
        "max_fallback_rate": max(coerce_number(row, "service_constrained_fallback_rate") for row in rows),
        "eligible": all(coerce_rate(row, "service_guardrail_violation") <= 0 for row in rows)
        and len(service_values) == len(rows),
    }


def summarize_by_grid(rows):
    grouped = defaultdict(lambda: defaultdict(list))
    for row in rows:
        grouped[row["grid_id"]][row["base_policy_tag"]].append(row)

    summary = {}
    for grid_id, policy_rows in grouped.items():
        grid_summary = {
            "grid_id": grid_id,
            "service_quit_penalty": next(iter(policy_rows.values()))[0]["service_quit_penalty"],
            "service_quit_rate_guardrail": next(iter(policy_rows.values()))[0]["service_quit_rate_guardrail"],
            "policies": {},
        }
        for base_tag in BASE_TAGS:
            grid_summary["policies"][base_tag] = summarize_group(policy_rows[base_tag])
        summary[grid_id] = grid_summary
    return summary


def classify_grid(grid_summary):
    policies = grid_summary["policies"]
    reasons = []
    service_constrained = policies["service_constrained_expected_profit"]
    if service_constrained["max_fallback_rate"] > 0:
        reasons.append("Service-Constrained Expected-Profit used fallback on at least one seed.")

    for tag in NEW_METHOD_TAGS:
        if policies[tag]["guardrail_violations"]:
            reasons.append(f"{tag} violated the quit-rate guardrail.")
        if not policies[tag]["eligible"]:
            reasons.append(f"{tag} has ineligible service-constrained profit rows.")

    comparator_values = [
        policies["cost_L"]["mean_service_constrained_net_profit"],
        policies["cnn_menu"]["mean_service_constrained_net_profit"],
    ]
    comparators_available = all(value is not None for value in comparator_values)
    if not comparators_available:
        reasons.append("Cost-L or CNN-Menu has unavailable service-constrained profit.")

    winning = []
    if comparators_available and service_constrained["max_fallback_rate"] <= 0:
        for tag in NEW_METHOD_TAGS:
            item = policies[tag]
            value = item["mean_service_constrained_net_profit"]
            if item["eligible"] and value is not None and value > max(comparator_values):
                winning.append(tag)

    if winning:
        return {
            "decision_state": "proceed_to_formal",
            "winning_new_methods": winning,
            "reasons": [
                "At least one expected-profit method beats Cost-L and CNN-Menu on mean service-constrained net profit with no guardrail violation."
            ],
        }

    if not reasons:
        reasons.append("Expected-profit methods did not beat both Cost-L and CNN-Menu on the service-constrained gate.")
    return {
        "decision_state": "recalibrate_objective",
        "winning_new_methods": [],
        "reasons": reasons,
    }


def classify_overall(grid_summaries):
    grid_results = {}
    passing = []
    for grid_id, grid_summary in sorted(grid_summaries.items()):
        result = classify_grid(grid_summary)
        grid_results[grid_id] = result
        if result["decision_state"] == "proceed_to_formal":
            passing.append(grid_id)

    if passing:
        selected = passing[0]
        return {
            "decision_state": "proceed_to_formal",
            "human_confirmation_required": True,
            "selected_grid": selected,
            "winning_new_methods": grid_results[selected]["winning_new_methods"],
            "reasons": grid_results[selected]["reasons"],
            "grid_results": grid_results,
        }

    reasons = []
    for grid_id, result in grid_results.items():
        for reason in result["reasons"]:
            reasons.append(f"{grid_id}: {reason}")
    return {
        "decision_state": "recalibrate_objective",
        "human_confirmation_required": False,
        "selected_grid": "",
        "winning_new_methods": [],
        "reasons": reasons,
        "grid_results": grid_results,
    }


def markdown_table(headers, rows):
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_rows(path, rows):
    fieldnames = list(ROWS_FIELDS)
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
            writer.writerow(row)


def build_reports(summary, row_source, study_dir, rows, grid_summaries, decision, output_dir):
    metadata = summary.get("run_metadata", {})
    study = summary.get("study", {})

    summary_rows = []
    for grid_id, grid in sorted(grid_summaries.items()):
        grid_result = decision["grid_results"][grid_id]
        for tag in BASE_TAGS:
            item = grid["policies"][tag]
            summary_rows.append(
                [
                    grid_id,
                    tag,
                    format_float(item["mean_service_constrained_net_profit"]),
                    format_float(item["mean_adjusted_profit"]),
                    format_float(item["mean_net_profit"]),
                    format_float(item["mean_opt_out_rate"]),
                    item["guardrail_violations"],
                    format_float(item["max_fallback_rate"]),
                    grid_result["decision_state"] if tag in NEW_METHOD_TAGS else "",
                ]
            )

    gap_closure_summary = [
        "# Phase08 Gap-Closure Summary",
        "",
        "## Run Metadata",
        f"- Study: `{study.get('name', STUDY_NAME)}`",
        f"- Run id: `{metadata.get('run_id', '')}`",
        f"- Manifest hash: `{study.get('manifest_hash', '')}`",
        f"- Row source: `{row_source}`",
        f"- Status: `{metadata.get('status', '')}`",
        "",
        "## Overall Gate",
        f"- Decision state: `{decision['decision_state']}`",
        f"- Selected grid: `{decision['selected_grid'] or 'none'}`",
        f"- Human confirmation required: `{str(decision['human_confirmation_required']).lower()}`",
        "",
        "## Policy Means By Grid",
        markdown_table(
            [
                "Grid",
                "Policy",
                "Mean service profit",
                "Mean adjusted profit",
                "Mean raw profit",
                "Mean opt-out",
                "Guardrail violations",
                "Max fallback",
                "Grid result",
            ],
            summary_rows,
        ),
        "",
        "## Reasons",
        *[f"- {reason}" for reason in decision["reasons"]],
        "",
    ]

    decision_lines = [
        "---",
        f"decision_state: {decision['decision_state']}",
        f"human_confirmation_required: {str(decision['human_confirmation_required']).lower()}",
        f"selected_grid: {decision['selected_grid'] or 'none'}",
        f"winning_new_methods: {', '.join(decision['winning_new_methods']) or 'none'}",
        f"run_id: {metadata.get('run_id', '')}",
        f"study_dir: {study_dir}",
        f"manifest_hash: {study.get('manifest_hash', '')}",
        "---",
        "",
        "# Phase08 Gap-Closure Gate Decision",
        "",
        "## Gate Result",
        f"- State: `{decision['decision_state']}`",
        f"- Selected grid: `{decision['selected_grid'] or 'none'}`",
        f"- Winning new methods: `{', '.join(decision['winning_new_methods']) or 'none'}`",
        "",
        "## Reasons",
        *[f"- {reason}" for reason in decision["reasons"]],
        "",
        "## Stop Condition",
        next_action(decision),
        "",
    ]

    objective_validity = [
        "# Phase08 Objective Validity",
        "",
        "## Interpretation",
        objective_interpretation(decision),
        "",
        "## Evidence Boundary",
        "- These diagnostics are phase-local and do not update manuscript-facing artifacts.",
        "- Formal evidence remains blocked unless `gate_decision.md` reports `proceed_to_formal` and the user confirms.",
        "- The MNL choice model, outside option, Lambert-W pricing, and HGS/Hygese routing backend are not changed by this artifact build.",
        "",
        "## Row Source",
        f"- `{row_source}`",
        f"- Rows analyzed: `{len(rows)}`",
        "",
    ]

    write_rows(output_dir / "gap_closure_rows.csv", rows)
    write_text(output_dir / "gap_closure_summary.md", "\n".join(gap_closure_summary))
    write_text(output_dir / "gate_decision.md", "\n".join(decision_lines))
    write_text(output_dir / "objective_validity.md", "\n".join(objective_validity))
    write_text(
        output_dir / "gap_closure_summary.json",
        json.dumps(
            {
                "decision": decision,
                "grid_summaries": grid_summaries,
                "row_source": str(row_source),
                "study_dir": str(study_dir),
            },
            indent=2,
            sort_keys=True,
        ),
    )


def next_action(decision):
    if decision["decision_state"] == "proceed_to_formal":
        return "Stop for human confirmation before formal evidence planning or runtime."
    return "Formal evidence remains blocked; plan objective redesign before manuscript-facing evidence."


def objective_interpretation(decision):
    if decision["decision_state"] == "proceed_to_formal":
        return (
            "At least one service-parameter configuration passed the Phase08-style gate. "
            "This is diagnostic readiness only; human confirmation is required before formal evidence."
        )
    return (
        "The locked service-parameter grid did not pass the Phase08-style gate. "
        "The current expected-profit/service objective remains unsupported for formal evidence, "
        "so the next phase should redesign or diagnose the objective rather than run manuscript experiments."
    )


def run(argv=None):
    args = parse_args(argv)
    study_dir = resolve_study_dir(args).resolve()
    output_dir = resolve_output_dir(args.output_dir)
    summary_path = study_dir / "study_summary.json"
    if not summary_path.exists():
        raise GateError(f"missing study_summary.json at {summary_path}")
    summary = load_json(summary_path)
    validate_summary(study_dir, summary)
    raw_rows, row_source = load_rows(study_dir)
    rows = validate_rows(raw_rows, row_source, study_dir, summary)
    grid_summaries = summarize_by_grid(rows)
    decision = classify_overall(grid_summaries)
    output_dir.mkdir(parents=True, exist_ok=True)
    build_reports(summary, row_source, study_dir, rows, grid_summaries, decision, output_dir)
    return {
        "output_dir": str(output_dir),
        "decision_state": decision["decision_state"],
        "human_confirmation_required": decision["human_confirmation_required"],
        "selected_grid": decision["selected_grid"],
        "files": [
            str(output_dir / "gap_closure_rows.csv"),
            str(output_dir / "gap_closure_summary.md"),
            str(output_dir / "gate_decision.md"),
            str(output_dir / "objective_validity.md"),
            str(output_dir / "gap_closure_summary.json"),
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
