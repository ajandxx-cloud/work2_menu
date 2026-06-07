import argparse
import csv
import json
import math
import shutil
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
STUDY_NAME = "work2_phase6_redesign_diagnostic"
PHASE_OUTPUT_ROOT = ROOT / "outputs" / "phase6_redesign"
FORMAL_ARTIFACTS_DIR = ROOT / "artifacts"
MANUSCRIPT_DIR = ROOT / "manuscript"
EXPECTED_SEEDS = [0, 1, 2]
REQUIRED_TAGS = [
    "cost_L",
    "cnn_menu",
    "expected_profit_enumeration",
    "service_constrained_expected_profit",
    "risk_lambda_50",
    "risk_lambda_100",
    "risk_lambda_200",
    "risk_lambda_400",
    "min_quit_tol000",
    "min_quit_tol001",
    "min_quit_tol003",
    "service_guarded_diagnostic",
    "cost_oracle",
    "profit_oracle",
]
BASELINE_TAGS = ["cost_L", "cnn_menu", "nearest_L", "cnn_setmenu_net_current"]
MAIN_CANDIDATE_TAGS = [
    "risk_lambda_50",
    "risk_lambda_100",
    "risk_lambda_200",
    "risk_lambda_400",
    "min_quit_tol000",
    "min_quit_tol001",
    "min_quit_tol003",
]
DIAGNOSTIC_ONLY_TAGS = ["service_guarded_diagnostic"]
REDESIGNED_TAGS = MAIN_CANDIDATE_TAGS + DIAGNOSTIC_ONLY_TAGS
GATE_STATES = {"proceed_to_formal", "continue_redesign", "conclude_method_unsuitable"}
REQUIRED_OUTPUTS = [
    "redesign_rows.csv",
    "redesign_rows.json",
    "policy_component_summary.csv",
    "failure_mode_report.md",
    "redesign_gate.md",
    "objective_validity.md",
    "manifest_snapshot.yaml",
    "run_metadata.json",
]


class GateError(ValueError):
    pass


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Build Phase 6B redesign artifacts from an explicit diagnostic study run."
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--run-id", help=f"Run id under outputs/studies/{STUDY_NAME}/")
    source.add_argument("--study-dir", help=f"Explicit {STUDY_NAME} study output directory")
    parser.add_argument("--output-dir", default="", help="Phase-local output directory")
    return parser.parse_args(argv)


def resolve_study_dir(args):
    if args.run_id:
        return ROOT / "outputs" / "studies" / STUDY_NAME / args.run_id
    return Path(args.study_dir)


def is_under(path, parent):
    path = path.resolve()
    parent = parent.resolve()
    return path == parent or parent in path.parents


def resolve_output_dir(path, run_id):
    output_dir = Path(path) if path else PHASE_OUTPUT_ROOT / run_id
    if not output_dir.is_absolute():
        output_dir = PROJECT_ROOT / output_dir
    resolved = output_dir.resolve()
    if is_under(resolved, FORMAL_ARTIFACTS_DIR):
        raise GateError("Phase 6 redesign artifacts must not be written under ooh_code/artifacts")
    if is_under(resolved, MANUSCRIPT_DIR):
        raise GateError("Phase 6 redesign artifacts must not be written under manuscript/")
    return resolved


def load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)


def write_csv(path, rows):
    fieldnames = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                fieldnames.append(key)
                seen.add(key)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_rows(study_dir):
    json_path = study_dir / "normalized_rows.json"
    csv_path = study_dir / "normalized_rows.csv"
    if json_path.exists():
        rows = load_json(json_path)
        return rows, json_path
    if csv_path.exists():
        with open(csv_path, "r", encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle)), csv_path
    raise GateError("missing normalized_rows.json or normalized_rows.csv")


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
        raise GateError(f"missing numeric metric {key} for seed={row.get('seed')} tag={row.get('variant_tag')}")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise GateError(f"unparseable numeric metric {key} for seed={row.get('seed')} tag={row.get('variant_tag')}") from exc
    if not math.isfinite(number):
        raise GateError(f"non-finite numeric metric {key} for seed={row.get('seed')} tag={row.get('variant_tag')}")
    return number


def coerce_bool(value):
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "1.0", "true", "yes"}


def validate_summary(study_dir, summary):
    study = summary.get("study", {})
    metadata = summary.get("run_metadata", {})
    if study.get("name") != STUDY_NAME:
        raise GateError(f"study_summary.json must describe {STUDY_NAME}")
    if metadata.get("status") != "completed":
        raise GateError("study_summary.json status must be completed")
    if int(metadata.get("completed_splits", -1)) != len(EXPECTED_SEEDS):
        raise GateError("completed_splits must be 3")
    if int(metadata.get("expected_splits", -1)) != len(EXPECTED_SEEDS):
        raise GateError("expected_splits must be 3")
    split_ids = {split.get("split_id") for split in summary.get("splits", [])}
    if split_ids != {f"seed{seed}" for seed in EXPECTED_SEEDS}:
        raise GateError("study_summary.json splits must be seed0, seed1, seed2")
    if metadata.get("study_root") and Path(metadata["study_root"]).resolve() != study_dir.resolve():
        raise GateError("study_summary.json study_root does not match explicit study directory")


def validate_rows(rows, summary, row_source, study_dir):
    if not isinstance(rows, list) or not rows:
        raise GateError("normalized rows are empty or invalid")
    seen = {}
    clean_rows = []
    for raw in rows:
        if is_reference_row(raw):
            continue
        row = dict(raw)
        tag = str(row.get("variant_tag", ""))
        seed = int(coerce_number(row, "seed"))
        key = (seed, tag)
        if key in seen:
            raise GateError(f"duplicate row for seed={seed} tag={tag}")
        seen[key] = row
        row["study_dir"] = str(study_dir)
        row["row_source"] = str(row_source)
        row["manifest_hash"] = row.get("manifest_hash") or summary.get("study", {}).get("manifest_hash", "")
        clean_rows.append(row)

    for seed in EXPECTED_SEEDS:
        for tag in REQUIRED_TAGS:
            if (seed, tag) not in seen:
                raise GateError(f"missing row for seed={seed} tag={tag}")

    required_numeric = ["net_profit", "opt_out_rate", "acceptance_rate", "episodes"]
    for row in clean_rows:
        for key in required_numeric:
            coerce_number(row, key)
        tag = row.get("variant_tag")
        if tag in REDESIGNED_TAGS:
            coerce_number(row, "redesign_fallback_rate")
            coerce_number(row, "avg_redesign_predicted_outside_probability")
            coerce_number(row, "avg_redesign_predicted_expected_system_profit")
            coerce_number(row, "avg_redesign_score")
    return clean_rows


def mean(values):
    values = [float(value) for value in values if value is not None]
    return sum(values) / len(values) if values else None


def summarize_policy(rows):
    return {
        "variant_tag": rows[0]["variant_tag"],
        "policy": rows[0].get("policy", ""),
        "seeds": len(rows),
        "mean_net_profit": mean(coerce_number(row, "net_profit") for row in rows),
        "mean_opt_out_rate": mean(coerce_number(row, "opt_out_rate") for row in rows),
        "mean_acceptance_rate": mean(coerce_number(row, "acceptance_rate") for row in rows),
        "max_redesign_fallback_rate": max(coerce_number(row, "redesign_fallback_rate", allow_null=True) or 0.0 for row in rows),
        "mean_predicted_outside_probability": mean(
            coerce_number(row, "avg_redesign_predicted_outside_probability", allow_null=True) for row in rows
        ),
        "mean_predicted_expected_system_profit": mean(
            coerce_number(row, "avg_redesign_predicted_expected_system_profit", allow_null=True) for row in rows
        ),
        "mean_redesign_score": mean(coerce_number(row, "avg_redesign_score", allow_null=True) for row in rows),
        "behavior_non_degenerate_all": all(coerce_bool(row.get("is_behavior_non_degenerate", True)) for row in rows),
    }


def summarize_rows(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["variant_tag"]].append(row)
    return {tag: summarize_policy(tag_rows) for tag, tag_rows in grouped.items()}


def strongest_baseline(policy_summary):
    candidates = [policy_summary[tag] for tag in BASELINE_TAGS if tag in policy_summary]
    if not candidates:
        raise GateError("no non-oracle baseline rows available")
    return max(candidates, key=lambda item: item["mean_net_profit"])


def severe_reverse_signal(rows_by_tag, redesigned_tag, baseline_tag):
    redesigned_by_seed = {int(row["seed"]): row for row in rows_by_tag[redesigned_tag]}
    baseline_by_seed = {int(row["seed"]): row for row in rows_by_tag[baseline_tag]}
    for seed in EXPECTED_SEEDS:
        red = redesigned_by_seed[seed]
        base = baseline_by_seed[seed]
        if (
            coerce_number(red, "net_profit") < coerce_number(base, "net_profit") - 1e-9
            and coerce_number(red, "opt_out_rate") > coerce_number(base, "opt_out_rate") + 1e-9
        ):
            return True
    return False


def classify_gate(rows, policy_summary):
    rows_by_tag = defaultdict(list)
    for row in rows:
        rows_by_tag[row["variant_tag"]].append(row)
    baseline = strongest_baseline(policy_summary)
    baseline_tag = baseline["variant_tag"]
    guardrail = max(
        coerce_number(row, "menu_optout_guardrail", allow_null=True) or 0.40
        for tag in MAIN_CANDIDATE_TAGS
        for row in rows_by_tag[tag]
    )

    passing = []
    local_signal = []
    fallback_heavy = []
    reasons = [f"Strongest available non-oracle baseline: {baseline_tag}."]
    for tag in MAIN_CANDIDATE_TAGS:
        item = policy_summary[tag]
        profit_gap = item["mean_net_profit"] - baseline["mean_net_profit"]
        opt_out_gap = item["mean_opt_out_rate"] - baseline["mean_opt_out_rate"]
        no_fallback = item["max_redesign_fallback_rate"] <= 1e-12
        no_reverse = not severe_reverse_signal(rows_by_tag, tag, baseline_tag)
        if item["max_redesign_fallback_rate"] >= 0.5:
            fallback_heavy.append(tag)
        if profit_gap > 0 or opt_out_gap < 0:
            local_signal.append(tag)
        if (
            profit_gap > 0
            and item["mean_opt_out_rate"] <= guardrail + 1e-12
            and item["behavior_non_degenerate_all"]
            and no_fallback
            and no_reverse
        ):
            passing.append(tag)
        reasons.append(
            f"{tag}: profit_gap={profit_gap:.3f}, opt_out_gap={opt_out_gap:.3f}, "
            f"fallback_max={item['max_redesign_fallback_rate']:.3f}."
        )

    for tag in DIAGNOSTIC_ONLY_TAGS:
        item = policy_summary[tag]
        reasons.append(
            f"{tag}: diagnostic-only, not eligible to win this gate; "
            f"fallback_max={item['max_redesign_fallback_rate']:.3f}, "
            f"mean_opt_out={item['mean_opt_out_rate']:.3f}."
        )

    if passing:
        return {
            "decision_state": "proceed_to_formal",
            "human_confirmation_required": True,
            "winning_redesigned_methods": passing,
            "strongest_baseline": baseline_tag,
            "reasons": reasons + ["At least one redesigned method passes all Phase 6 criteria."],
        }
    if local_signal and len(fallback_heavy) < len(MAIN_CANDIDATE_TAGS):
        return {
            "decision_state": "continue_redesign",
            "human_confirmation_required": False,
            "winning_redesigned_methods": [],
            "strongest_baseline": baseline_tag,
            "reasons": reasons + ["Local profit or service signal exists, but gate stability is insufficient."],
        }
    return {
        "decision_state": "conclude_method_unsuitable",
        "human_confirmation_required": False,
        "winning_redesigned_methods": [],
        "strongest_baseline": baseline_tag,
        "reasons": reasons + ["No stable redesigned method improves both profit and service behavior."],
    }


def markdown_table(headers, rows):
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def fmt(value):
    if value is None:
        return "--"
    return f"{float(value):.3f}"


def build_reports(output_dir, study_dir, summary, rows, policy_summary, decision):
    output_dir.mkdir(parents=True, exist_ok=True)
    run_id = summary["run_metadata"]["run_id"]
    manifest_snapshot = study_dir / "manifest_snapshot.yaml"
    if manifest_snapshot.exists():
        shutil.copyfile(manifest_snapshot, output_dir / "manifest_snapshot.yaml")
    else:
        (output_dir / "manifest_snapshot.yaml").write_text("", encoding="utf-8")

    write_csv(output_dir / "redesign_rows.csv", rows)
    save_json(output_dir / "redesign_rows.json", rows)

    component_rows = list(policy_summary.values())
    write_csv(output_dir / "policy_component_summary.csv", component_rows)

    table_rows = []
    for tag in sorted(policy_summary):
        item = policy_summary[tag]
        table_rows.append([
            tag,
            fmt(item["mean_net_profit"]),
            fmt(item["mean_opt_out_rate"]),
            fmt(item["mean_acceptance_rate"]),
            fmt(item["max_redesign_fallback_rate"]),
            fmt(item["mean_predicted_outside_probability"]),
        ])

    failure_report = [
        "# Phase 6B Failure Mode Report",
        "",
        f"- Study: `{STUDY_NAME}`",
        f"- Run id: `{run_id}`",
        f"- Gate state: `{decision['decision_state']}`",
        f"- Strongest baseline: `{decision['strongest_baseline']}`",
        "",
        markdown_table(
            ["Policy", "Net profit", "Opt-out", "Acceptance", "Fallback", "Predicted outside"],
            table_rows,
        ),
        "",
        "## Reasons",
    ]
    failure_report.extend(f"- {reason}" for reason in decision["reasons"])
    (output_dir / "failure_mode_report.md").write_text("\n".join(failure_report) + "\n", encoding="utf-8")

    gate_lines = [
        "---",
        f"decision_state: {decision['decision_state']}",
        f"human_confirmation_required: {str(decision['human_confirmation_required']).lower()}",
        f"strongest_baseline: {decision['strongest_baseline']}",
        f"winning_redesigned_methods: {','.join(decision['winning_redesigned_methods']) or 'none'}",
        f"run_id: {run_id}",
        f"study_dir: {study_dir}",
        f"manifest_hash: {summary['study'].get('manifest_hash', '')}",
        "---",
        "",
        "# Phase 6B Redesign Gate",
        "",
        "## Reasons",
    ]
    gate_lines.extend(f"- {reason}" for reason in decision["reasons"])
    (output_dir / "redesign_gate.md").write_text("\n".join(gate_lines) + "\n", encoding="utf-8")

    if decision["decision_state"] == "proceed_to_formal":
        interpretation = "A redesigned non-learning objective passed the local diagnostic gate. Formal evidence remains blocked until human confirmation."
    elif decision["decision_state"] == "continue_redesign":
        interpretation = "The redesign has local signal but remains insufficient for formal evidence."
    else:
        interpretation = "The current redesigned objective route is unsuitable as a positive main method without a conceptual pivot."
    objective_lines = [
        "# Phase 6B Objective Validity",
        "",
        f"## Interpretation\n{interpretation}",
        "",
        "## Evidence Boundary",
        "- Phase-local artifacts only.",
        "- No manuscript-facing evidence was generated.",
        "- MNL choice, Lambert-W pricing, HGS/Hygese routing, and CNN learning are unchanged by artifact generation.",
    ]
    (output_dir / "objective_validity.md").write_text("\n".join(objective_lines) + "\n", encoding="utf-8")

    run_metadata = {
        "study_name": STUDY_NAME,
        "run_id": run_id,
        "study_dir": str(study_dir),
        "manifest_hash": summary["study"].get("manifest_hash", ""),
        "decision_state": decision["decision_state"],
        "required_outputs": REQUIRED_OUTPUTS,
    }
    save_json(output_dir / "run_metadata.json", run_metadata)

    missing = [name for name in REQUIRED_OUTPUTS if not (output_dir / name).exists()]
    if missing:
        raise GateError(f"missing generated Phase 6 artifacts: {missing}")


def run(argv=None):
    args = parse_args(argv)
    study_dir = resolve_study_dir(args).resolve()
    summary_path = study_dir / "study_summary.json"
    if not summary_path.exists():
        raise GateError(f"missing study_summary.json at {summary_path}")
    summary = load_json(summary_path)
    validate_summary(study_dir, summary)
    rows, row_source = load_rows(study_dir)
    clean_rows = validate_rows(rows, summary, row_source, study_dir)
    policy_summary = summarize_rows(clean_rows)
    decision = classify_gate(clean_rows, policy_summary)
    if decision["decision_state"] not in GATE_STATES:
        raise GateError("invalid gate state")

    output_dir = resolve_output_dir(args.output_dir, summary["run_metadata"]["run_id"])
    build_reports(output_dir, study_dir, summary, clean_rows, policy_summary, decision)
    result = {
        "decision_state": decision["decision_state"],
        "human_confirmation_required": decision["human_confirmation_required"],
        "output_dir": str(output_dir),
        "files": [str(output_dir / name) for name in REQUIRED_OUTPUTS],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def main():
    try:
        run()
    except GateError as exc:
        print(f"ERROR: {exc}", file=__import__("sys").stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
