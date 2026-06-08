import argparse
import csv
import json
import math
import shutil
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
STUDY_NAME = "work2_phase6_redesign_formal"
PHASE_OUTPUT_ROOT = ROOT / "outputs" / "phase6_redesign_formal"
FORMAL_ARTIFACTS_DIR = ROOT / "artifacts"
MANUSCRIPT_DIR = ROOT / "manuscript"
PRIMARY_METRIC = "service_constrained_net_profit"
EXPECTED_SEEDS = [0, 1, 2, 3, 4]
EXPECTED_SPLITS = [f"seed{seed}" for seed in EXPECTED_SEEDS]

BASELINE_TAGS = ["nearest_L", "cost_L", "cnn_menu"]
LEGACY_DIAGNOSTIC_TAGS = [
    "expected_profit_enumeration",
    "service_constrained_expected_profit",
]
FORMAL_CANDIDATE_TAGS = [
    "risk_lambda_200",
    "risk_lambda_400",
    "min_quit_tol000",
    "min_quit_tol001",
    "min_quit_tol003",
]
ORACLE_TAGS = ["cost_oracle", "profit_oracle"]
REQUIRED_TAGS = (
    BASELINE_TAGS
    + LEGACY_DIAGNOSTIC_TAGS
    + FORMAL_CANDIDATE_TAGS
    + ORACLE_TAGS
)
FAMILY_MEMBERS = {
    "risk_adjusted_expected_profit": ["risk_lambda_200", "risk_lambda_400"],
    "min_quit_then_profit": ["min_quit_tol000", "min_quit_tol001", "min_quit_tol003"],
}
GATE_STATES = {"formal_support", "mixed_support", "no_support"}
REQUIRED_OUTPUTS = [
    "formal_rows.csv",
    "formal_rows.json",
    "formal_policy_summary.csv",
    "formal_policy_summary.md",
    "formal_gate.md",
    "formal_evidence_explanation.md",
    "manifest_snapshot.yaml",
    "run_metadata.json",
    "checkpoint_provenance.json",
]


class GateError(ValueError):
    pass


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Build Phase 6 redesign formal audit artifacts from an explicit study run."
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--run-id", help=f"Run id under outputs/studies/{STUDY_NAME}/")
    source.add_argument("--study-dir", help=f"Explicit {STUDY_NAME} study output directory")
    parser.add_argument("--output-dir", default="", help="Phase-local output directory")
    parser.add_argument(
        "--allow-manuscript-output",
        action="store_true",
        help="Allow artifact/manuscript output only after the formal gate is formal_support.",
    )
    return parser.parse_args(argv)


def resolve_study_dir(args):
    if args.run_id:
        return ROOT / "outputs" / "studies" / STUDY_NAME / args.run_id
    return Path(args.study_dir)


def is_under(path, parent):
    path = path.resolve()
    parent = parent.resolve()
    return path == parent or parent in path.parents


def resolve_output_dir(path, run_id, decision_state, allow_manuscript_output=False):
    output_dir = Path(path) if path else PHASE_OUTPUT_ROOT / run_id
    if not output_dir.is_absolute():
        output_dir = PROJECT_ROOT / output_dir
    resolved = output_dir.resolve()
    forbidden = is_under(resolved, FORMAL_ARTIFACTS_DIR) or is_under(resolved, MANUSCRIPT_DIR)
    if forbidden and not allow_manuscript_output:
        raise GateError("formal audit output must stay phase-local unless explicitly unlocked")
    if forbidden and decision_state != "formal_support":
        raise GateError("manuscript-facing output is allowed only for formal_support")
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
        return load_json(json_path), json_path
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


def mean(values):
    clean = [float(value) for value in values if value is not None]
    return sum(clean) / len(clean) if clean else None


def fmt(value):
    if value is None:
        return "--"
    return f"{float(value):.3f}"


def validate_summary(study_dir, summary):
    study = summary.get("study", {})
    metadata = summary.get("run_metadata", {})
    if study.get("name") != STUDY_NAME:
        raise GateError(f"study_summary.json must describe {STUDY_NAME}")
    if metadata.get("status") != "completed":
        raise GateError("study_summary.json status must be completed")
    if int(metadata.get("completed_splits", -1)) != len(EXPECTED_SEEDS):
        raise GateError("completed_splits must be 5")
    if int(metadata.get("expected_splits", -1)) != len(EXPECTED_SEEDS):
        raise GateError("expected_splits must be 5")

    split_ids = {split.get("split_id") for split in summary.get("splits", [])}
    if split_ids != set(EXPECTED_SPLITS):
        raise GateError("study_summary.json splits must be seed0 through seed4")
    if metadata.get("study_root") and Path(metadata["study_root"]).resolve() != study_dir.resolve():
        raise GateError("study_summary.json study_root does not match explicit study directory")


def primary_available(row):
    return coerce_number(row, PRIMARY_METRIC, allow_null=True) is not None


def normalize_row(raw, summary, row_source, study_dir):
    row = dict(raw)
    row["seed"] = int(coerce_number(row, "seed"))
    row["variant_tag"] = str(row.get("variant_tag", ""))
    row["study_dir"] = str(study_dir)
    row["row_source"] = str(row_source)
    row["manifest_hash"] = row.get("manifest_hash") or summary.get("study", {}).get("manifest_hash", "")

    for key in ["net_profit", "opt_out_rate", "acceptance_rate", "episodes"]:
        row[key] = coerce_number(row, key)
    primary_value = coerce_number(row, PRIMARY_METRIC, allow_null=True)
    row[PRIMARY_METRIC] = primary_value
    row["primary_metric_available"] = primary_value is not None
    row["formal_claim_eligible"] = primary_value is not None

    for key in ["checkpoint_path", "checkpoint_reused", "checkpoint_source"]:
        if key not in row:
            raise GateError(f"missing checkpoint provenance field {key} for tag={row['variant_tag']} seed={row['seed']}")
    row["checkpoint_reused"] = coerce_bool(row.get("checkpoint_reused"))

    if row["variant_tag"] in FORMAL_CANDIDATE_TAGS:
        for key in [
            "redesign_fallback_rate",
            "avg_redesign_predicted_outside_probability",
            "avg_redesign_predicted_expected_system_profit",
            "avg_redesign_score",
        ]:
            row[key] = coerce_number(row, key)
    else:
        for key in [
            "redesign_fallback_rate",
            "avg_redesign_predicted_outside_probability",
            "avg_redesign_predicted_expected_system_profit",
            "avg_redesign_score",
        ]:
            row[key] = coerce_number(row, key, allow_null=True)
    return row


def validate_rows(rows, summary, row_source, study_dir):
    if not isinstance(rows, list) or not rows:
        raise GateError("normalized rows are empty or invalid")
    seen = {}
    clean_rows = []
    for raw in rows:
        if is_reference_row(raw):
            continue
        tag = str(raw.get("variant_tag", ""))
        if tag == "service_guarded_diagnostic":
            raise GateError("service_guarded_diagnostic must remain absent from formal rows")
        if tag not in REQUIRED_TAGS:
            raise GateError(f"unexpected formal policy tag: {tag}")
        row = normalize_row(raw, summary, row_source, study_dir)
        key = (row["seed"], tag)
        if key in seen:
            raise GateError(f"duplicate row for seed={row['seed']} tag={tag}")
        seen[key] = row
        clean_rows.append(row)

    for seed in EXPECTED_SEEDS:
        for tag in REQUIRED_TAGS:
            if (seed, tag) not in seen:
                raise GateError(f"missing row for seed={seed} tag={tag}")
    return clean_rows


def summarize_policy(rows):
    primary_values = [row[PRIMARY_METRIC] for row in rows if row["primary_metric_available"]]
    return {
        "variant_tag": rows[0]["variant_tag"],
        "policy": rows[0].get("policy", ""),
        "seeds": len(rows),
        "primary_metric_name": PRIMARY_METRIC,
        "primary_metric_available_seeds": len(primary_values),
        "mean_primary_metric": mean(primary_values),
        "mean_net_profit": mean(row["net_profit"] for row in rows),
        "mean_opt_out_rate": mean(row["opt_out_rate"] for row in rows),
        "mean_acceptance_rate": mean(row["acceptance_rate"] for row in rows),
        "max_redesign_fallback_rate": max(row.get("redesign_fallback_rate") or 0.0 for row in rows),
        "mean_predicted_outside_probability": mean(
            row.get("avg_redesign_predicted_outside_probability") for row in rows
        ),
        "mean_predicted_expected_system_profit": mean(
            row.get("avg_redesign_predicted_expected_system_profit") for row in rows
        ),
        "mean_redesign_score": mean(row.get("avg_redesign_score") for row in rows),
        "checkpoint_sources": ",".join(sorted({str(row.get("checkpoint_source", "")) for row in rows})),
    }


def summarize_rows(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["variant_tag"]].append(row)
    return {tag: summarize_policy(tag_rows) for tag, tag_rows in grouped.items()}


def strongest_baseline(policy_summary):
    candidates = [
        policy_summary[tag]
        for tag in BASELINE_TAGS
        if policy_summary[tag]["mean_primary_metric"] is not None
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda item: item["mean_primary_metric"])


def seed_index(rows_by_tag, tag):
    return {int(row["seed"]): row for row in rows_by_tag[tag]}


def member_evidence(tag, rows_by_tag, baseline_tag, baseline_summary, policy_summary):
    item = policy_summary[tag]
    baseline_by_seed = seed_index(rows_by_tag, baseline_tag)
    member_by_seed = seed_index(rows_by_tag, tag)
    unstable = 0
    comparable = 0
    for seed in EXPECTED_SEEDS:
        red = member_by_seed[seed]
        base = baseline_by_seed[seed]
        if red[PRIMARY_METRIC] is None or base[PRIMARY_METRIC] is None:
            continue
        comparable += 1
        if red[PRIMARY_METRIC] < base[PRIMARY_METRIC] - 1e-9 and red["opt_out_rate"] > base["opt_out_rate"] + 1e-9:
            unstable += 1

    mean_gap = None
    if item["mean_primary_metric"] is not None and baseline_summary["mean_primary_metric"] is not None:
        mean_gap = item["mean_primary_metric"] - baseline_summary["mean_primary_metric"]
    opt_out_gap = item["mean_opt_out_rate"] - baseline_summary["mean_opt_out_rate"]
    fallback_heavy = item["max_redesign_fallback_rate"] >= 0.50
    eligible = item["primary_metric_available_seeds"] == len(EXPECTED_SEEDS) and comparable == len(EXPECTED_SEEDS)
    passes = (
        eligible
        and mean_gap is not None
        and mean_gap > 0
        and unstable < 3
        and opt_out_gap <= 1e-12
        and not fallback_heavy
    )
    return {
        "variant_tag": tag,
        "family": family_for_tag(tag),
        "mean_primary_metric": item["mean_primary_metric"],
        "mean_primary_gap_vs_baseline": mean_gap,
        "mean_net_profit": item["mean_net_profit"],
        "mean_opt_out_rate": item["mean_opt_out_rate"],
        "mean_acceptance_rate": item["mean_acceptance_rate"],
        "max_redesign_fallback_rate": item["max_redesign_fallback_rate"],
        "unstable_seed_count": unstable,
        "comparable_seed_count": comparable,
        "primary_metric_available_seeds": item["primary_metric_available_seeds"],
        "eligible_for_positive_claim": eligible,
        "passes_formal_gate": passes,
    }


def family_for_tag(tag):
    for family, members in FAMILY_MEMBERS.items():
        if tag in members:
            return family
    return ""


def classify_gate(rows, policy_summary):
    rows_by_tag = defaultdict(list)
    for row in rows:
        rows_by_tag[row["variant_tag"]].append(row)

    baseline = strongest_baseline(policy_summary)
    reasons = []
    if baseline is None:
        baseline_tag = "none"
        member_rows = []
        family_rows = []
        reasons.append("All non-oracle baseline primary metrics are unavailable; positive evidence is fail-closed.")
        return {
            "decision_state": "no_support",
            "strongest_baseline": baseline_tag,
            "winning_families": [],
            "winning_members": [],
            "member_evidence": member_rows,
            "family_evidence": family_rows,
            "reasons": reasons,
        }

    baseline_tag = baseline["variant_tag"]
    reasons.append(f"Strongest non-oracle baseline by {PRIMARY_METRIC}: {baseline_tag}.")
    member_rows = [
        member_evidence(tag, rows_by_tag, baseline_tag, baseline, policy_summary)
        for tag in FORMAL_CANDIDATE_TAGS
    ]

    family_rows = []
    for family, members in FAMILY_MEMBERS.items():
        evidence = [row for row in member_rows if row["variant_tag"] in members]
        winners = [row["variant_tag"] for row in evidence if row["passes_formal_gate"]]
        best_gap = max(
            [row["mean_primary_gap_vs_baseline"] for row in evidence if row["mean_primary_gap_vs_baseline"] is not None],
            default=None,
        )
        service_signal = any(
            row["mean_opt_out_rate"] <= baseline["mean_opt_out_rate"] + 1e-12 for row in evidence
        )
        family_rows.append({
            "family": family,
            "members": ",".join(members),
            "winning_members": ",".join(winners),
            "best_primary_gap_vs_baseline": best_gap,
            "service_signal": service_signal,
            "passes_formal_gate": bool(winners),
        })

    winning_families = [row["family"] for row in family_rows if row["passes_formal_gate"]]
    winning_members = [row["variant_tag"] for row in member_rows if row["passes_formal_gate"]]
    for row in member_rows:
        reasons.append(
            f"{row['variant_tag']}: primary_gap={fmt(row['mean_primary_gap_vs_baseline'])}, "
            f"opt_out={fmt(row['mean_opt_out_rate'])}, unstable_seeds={row['unstable_seed_count']}, "
            f"fallback_max={fmt(row['max_redesign_fallback_rate'])}."
        )

    if winning_families:
        state = "formal_support"
        reasons.append("At least one redesigned family passed the primary, service, stability, and fallback gates.")
    elif any(
        (row["mean_primary_gap_vs_baseline"] is not None and row["mean_primary_gap_vs_baseline"] > 0)
        or row["mean_opt_out_rate"] < baseline["mean_opt_out_rate"] - 1e-12
        for row in member_rows
    ):
        state = "mixed_support"
        reasons.append("Partial profit or service signal exists, but the full formal gate did not pass.")
    else:
        state = "no_support"
        reasons.append("No stable redesigned family improvement was sufficient for a positive main conclusion.")

    return {
        "decision_state": state,
        "strongest_baseline": baseline_tag,
        "winning_families": winning_families,
        "winning_members": winning_members,
        "member_evidence": member_rows,
        "family_evidence": family_rows,
        "reasons": reasons,
    }


def markdown_table(headers, rows):
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def checkpoint_exists(path_text):
    if not path_text:
        return False
    path = Path(path_text)
    if not path.is_absolute():
        path = ROOT / path
    return path.exists()


def checkpoint_provenance(rows):
    records = {}
    for row in rows:
        key = (
            str(row.get("checkpoint_path", "")),
            str(row.get("checkpoint_source", "")),
            str(row.get("checkpoint_reused", "")),
        )
        if key not in records:
            records[key] = {
                "checkpoint_path": key[0],
                "checkpoint_source": key[1],
                "checkpoint_reused": bool(row.get("checkpoint_reused")),
                "checkpoint_exists": checkpoint_exists(key[0]),
                "rows": 0,
                "variant_tags": [],
            }
        records[key]["rows"] += 1
        records[key]["variant_tags"].append(row["variant_tag"])
    for record in records.values():
        record["variant_tags"] = sorted(set(record["variant_tags"]))
    return list(records.values())


def build_policy_summary_rows(policy_summary, decision):
    rows = []
    member_by_tag = {row["variant_tag"]: row for row in decision["member_evidence"]}
    for tag in REQUIRED_TAGS:
        item = dict(policy_summary[tag])
        evidence = member_by_tag.get(tag, {})
        item.update({
            "role": role_for_tag(tag),
            "family": family_for_tag(tag),
            "mean_primary_gap_vs_strongest_baseline": evidence.get("mean_primary_gap_vs_baseline"),
            "unstable_seed_count": evidence.get("unstable_seed_count"),
            "eligible_for_positive_claim": evidence.get("eligible_for_positive_claim", False),
            "passes_formal_gate": evidence.get("passes_formal_gate", False),
        })
        rows.append(item)
    for row in decision["family_evidence"]:
        rows.append({
            "variant_tag": row["family"],
            "policy": "family_summary",
            "role": "formal_family",
            "family": row["family"],
            "seeds": len(EXPECTED_SEEDS),
            "primary_metric_name": PRIMARY_METRIC,
            "mean_primary_gap_vs_strongest_baseline": row["best_primary_gap_vs_baseline"],
            "winning_members": row["winning_members"],
            "passes_formal_gate": row["passes_formal_gate"],
        })
    return rows


def role_for_tag(tag):
    if tag in BASELINE_TAGS:
        return "non_oracle_baseline"
    if tag in LEGACY_DIAGNOSTIC_TAGS:
        return "legacy_diagnostic"
    if tag in FORMAL_CANDIDATE_TAGS:
        return "formal_candidate"
    if tag in ORACLE_TAGS:
        return "oracle_reference"
    return "unknown"


def write_policy_summary_markdown(path, summary_rows, decision):
    table_rows = []
    for row in summary_rows:
        if row.get("policy") == "family_summary":
            continue
        table_rows.append([
            row["variant_tag"],
            row["role"],
            fmt(row.get("mean_primary_metric")),
            fmt(row.get("mean_primary_gap_vs_strongest_baseline")),
            fmt(row.get("mean_net_profit")),
            fmt(row.get("mean_opt_out_rate")),
            fmt(row.get("mean_acceptance_rate")),
            fmt(row.get("max_redesign_fallback_rate")),
            str(row.get("passes_formal_gate", False)).lower(),
        ])
    lines = [
        "# Phase 6 Formal Policy Summary",
        "",
        f"- Primary metric: `{PRIMARY_METRIC}`",
        f"- Strongest non-oracle baseline: `{decision['strongest_baseline']}`",
        "",
        markdown_table(
            [
                "Policy",
                "Role",
                "Primary",
                "Gap",
                "Net profit",
                "Opt-out",
                "Acceptance",
                "Fallback",
                "Pass",
            ],
            table_rows,
        ),
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_reports(output_dir, study_dir, summary, rows, policy_summary, decision):
    output_dir.mkdir(parents=True, exist_ok=True)
    run_id = summary["run_metadata"]["run_id"]
    manifest_snapshot = study_dir / "manifest_snapshot.yaml"
    if manifest_snapshot.exists():
        shutil.copyfile(manifest_snapshot, output_dir / "manifest_snapshot.yaml")
    else:
        (output_dir / "manifest_snapshot.yaml").write_text("", encoding="utf-8")

    write_csv(output_dir / "formal_rows.csv", rows)
    save_json(output_dir / "formal_rows.json", rows)

    summary_rows = build_policy_summary_rows(policy_summary, decision)
    write_csv(output_dir / "formal_policy_summary.csv", summary_rows)
    write_policy_summary_markdown(output_dir / "formal_policy_summary.md", summary_rows, decision)

    manuscript_unlocked = decision["decision_state"] == "formal_support"
    gate_lines = [
        "---",
        f"decision_state: {decision['decision_state']}",
        f"strongest_baseline: {decision['strongest_baseline']}",
        f"winning_families: [{', '.join(decision['winning_families'])}]",
        f"winning_members: [{', '.join(decision['winning_members'])}]",
        f"run_id: {run_id}",
        f"study_dir: {study_dir}",
        f"manifest_hash: {summary['study'].get('manifest_hash', '')}",
        f"primary_metric_name: {PRIMARY_METRIC}",
        f"manuscript_artifacts_unlocked: {str(manuscript_unlocked).lower()}",
        "---",
        "",
        "# Phase 6 Formal Gate",
        "",
        "## Reasons",
    ]
    gate_lines.extend(f"- {reason}" for reason in decision["reasons"])
    (output_dir / "formal_gate.md").write_text("\n".join(gate_lines) + "\n", encoding="utf-8")

    if decision["decision_state"] == "formal_support":
        interpretation = "The RC formal evidence may support the Part E choice-aware redesign conclusion."
    elif decision["decision_state"] == "mixed_support":
        interpretation = "The RC formal evidence is diagnostic mechanism evidence only, not a main positive conclusion."
    else:
        interpretation = "The RC formal evidence cannot support the desired paper conclusion and authorizes a future method change or new route."
    explanation = [
        "# Phase 6 Formal Evidence Explanation",
        "",
        f"Formal outcome: `{decision['decision_state']}`.",
        "",
        interpretation,
        "",
        "The audit package is phase-local unless the gate unlocks manuscript-facing artifacts.",
    ]
    (output_dir / "formal_evidence_explanation.md").write_text("\n".join(explanation) + "\n", encoding="utf-8")

    provenance = checkpoint_provenance(rows)
    save_json(output_dir / "checkpoint_provenance.json", provenance)
    run_metadata = {
        "study_name": STUDY_NAME,
        "run_id": run_id,
        "study_dir": str(study_dir),
        "manifest_hash": summary["study"].get("manifest_hash", ""),
        "decision_state": decision["decision_state"],
        "primary_metric_name": PRIMARY_METRIC,
        "manuscript_artifacts_unlocked": manuscript_unlocked,
        "required_outputs": REQUIRED_OUTPUTS,
    }
    save_json(output_dir / "run_metadata.json", run_metadata)

    missing = [name for name in REQUIRED_OUTPUTS if not (output_dir / name).exists()]
    if missing:
        raise GateError(f"missing generated Phase 6 formal artifacts: {missing}")


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
        raise GateError("invalid formal gate state")
    output_dir = resolve_output_dir(
        args.output_dir,
        summary["run_metadata"]["run_id"],
        decision["decision_state"],
        allow_manuscript_output=args.allow_manuscript_output,
    )
    build_reports(output_dir, study_dir, summary, clean_rows, policy_summary, decision)
    result = {
        "decision_state": decision["decision_state"],
        "strongest_baseline": decision["strongest_baseline"],
        "manuscript_artifacts_unlocked": decision["decision_state"] == "formal_support",
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
