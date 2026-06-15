import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev


POLICY_TAGS = [
    "mainline_no_menu",
    "mainline_fixed_menu",
    "mainline_random_menu",
    "mainline_optimized_m",
    "mainline_optimized_mw",
    "mainline_optimized_fixed_window",
    "mainline_optimized_adaptive",
]

PRIMARY_POLICY = "mainline_optimized_adaptive"
BASELINES = [tag for tag in POLICY_TAGS if tag != PRIMARY_POLICY]

METRICS = [
    "net_profit",
    "operational_cost",
    "total_cost",
    "acceptance_rate",
    "served_rate",
    "optout_rate",
    "home_share",
    "meeting_point_uptake_rate",
    "service_time_total",
]

LOWER_IS_BETTER = {"operational_cost", "total_cost", "optout_rate", "service_time_total"}


def _load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _numeric(value):
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _fmt(value, digits=6):
    if value is None:
        return ""
    return f"{float(value):.{digits}f}"


def _direction(metric, diff, tolerance=1e-9):
    if diff is None:
        return "missing"
    if abs(diff) <= tolerance:
        return "tie"
    better = diff < 0 if metric in LOWER_IS_BETTER else diff > 0
    return "adaptive_better" if better else "baseline_better"


def _direction_counts(paired_rows, metric, baseline=None, regime=None):
    counts = {"adaptive_better": 0, "baseline_better": 0, "tie": 0, "missing": 0}
    for row in paired_rows:
        if row["metric"] != metric:
            continue
        if baseline and row["baseline_policy"] != baseline:
            continue
        if regime and row["uptake_regime"] != regime:
            continue
        counts[row["direction"]] += 1
    return counts


def _summarize_policy(rows):
    out = []
    by_policy = defaultdict(list)
    for row in rows:
        by_policy[row["policy_tag"]].append(row)

    for policy in POLICY_TAGS:
        group = by_policy.get(policy, [])
        for metric in METRICS:
            values = [_numeric(row.get(metric)) for row in group]
            values = [value for value in values if value is not None]
            out.append(
                {
                    "policy_tag": policy,
                    "metric": metric,
                    "n": len(values),
                    "mean": mean(values) if values else None,
                    "std_pop": pstdev(values) if len(values) > 1 else 0.0 if values else None,
                }
            )
    return out


def _paired_diffs(rows):
    by_split_policy = {(row["split_id"], row["policy_tag"]): row for row in rows}
    split_ids = sorted({row["split_id"] for row in rows})
    out = []
    for split_id in split_ids:
        adaptive = by_split_policy.get((split_id, PRIMARY_POLICY))
        if adaptive is None:
            raise ValueError(f"missing primary policy row for split {split_id}")
        for baseline in BASELINES:
            base = by_split_policy.get((split_id, baseline))
            if base is None:
                raise ValueError(f"missing baseline row {baseline} for split {split_id}")
            for metric in METRICS:
                adaptive_value = _numeric(adaptive.get(metric))
                baseline_value = _numeric(base.get(metric))
                diff = None if adaptive_value is None or baseline_value is None else adaptive_value - baseline_value
                out.append(
                    {
                        "split_id": split_id,
                        "uptake_regime": adaptive.get("uptake_regime", ""),
                        "baseline_policy": baseline,
                        "metric": metric,
                        "adaptive_value": adaptive_value,
                        "baseline_value": baseline_value,
                        "diff_adaptive_minus_baseline": diff,
                        "direction": _direction(metric, diff),
                    }
                )
    return out


def _gate_summary(readiness, artifact_status, claim_guard):
    readiness_blockers = readiness.get("blockers") or []
    artifact_reasons = list(artifact_status.get("reasons") or [])
    nested_status = artifact_status.get("artifact_status") or {}
    artifact_reasons.extend(nested_status.get("reasons") or [])
    blocked_claims = claim_guard.get("blocked_claims") or []
    return {
        "readiness_status": readiness.get("status", ""),
        "claim_ready_allowed": bool(readiness.get("claim_ready_allowed")),
        "readiness_blockers": readiness_blockers,
        "artifact_status": nested_status.get("status") or artifact_status.get("artifact_status", ""),
        "artifact_claim_ready": bool(artifact_status.get("claim_ready")),
        "formal_claim_ready": bool(artifact_status.get("formal_claim_ready")),
        "artifact_reasons": sorted(set(str(item) for item in artifact_reasons)),
        "claim_guard_ready": bool(claim_guard.get("claim_ready")),
        "claim_guard_artifact_status": claim_guard.get("artifact_status", ""),
        "blocked_claim_ids": [item.get("id", "") for item in blocked_claims],
    }


def validate_inputs(summary, rows, readiness, artifact_status, claim_guard):
    errors = []
    if summary.get("execution_status") != "completed":
        errors.append("study_summary execution_status is not completed")
    if int(summary.get("row_count") or 0) != 35:
        errors.append("study_summary row_count is not 35")
    if len(rows) != 35:
        errors.append("normalized_rows length is not 35")
    if set(summary.get("policy_tags") or []) != set(POLICY_TAGS):
        errors.append("study_summary policy_tags do not match seven mainline policies")
    if {row.get("policy_tag") for row in rows} != set(POLICY_TAGS):
        errors.append("normalized_rows policy tags do not match seven mainline policies")
    if len({row.get("split_id") for row in rows}) != 5:
        errors.append("normalized_rows do not contain five splits")
    if {"low", "medium"} - {row.get("uptake_regime") for row in rows}:
        errors.append("normalized_rows do not cover low and medium uptake regimes")
    if set(summary.get("checkpoint_statuses") or []) != {"loaded"}:
        errors.append("study_summary checkpoint_statuses are not exactly ['loaded']")
    if summary.get("placeholder_only") is not False:
        errors.append("study_summary placeholder_only is not false")
    for idx, row in enumerate(rows):
        prefix = f"row {idx} {row.get('split_id')} {row.get('policy_tag')}"
        if row.get("status") != "completed":
            errors.append(prefix + " status is not completed")
        if row.get("execution_status") != "completed":
            errors.append(prefix + " execution_status is not completed")
        if row.get("checkpoint_load_status") != "loaded":
            errors.append(prefix + " checkpoint_load_status is not loaded")
        if row.get("placeholder_only") is not False:
            errors.append(prefix + " placeholder_only is not false")
    blocker_codes = {item.get("code") for item in readiness.get("blockers") or []}
    if readiness.get("status") != "blocked" or "dirty_git" not in blocker_codes:
        errors.append("readiness JSON must be blocked by dirty_git for this diagnostic run")
    if artifact_status.get("claim_ready") is not False:
        errors.append("artifact status unexpectedly reports claim_ready true")
    if claim_guard.get("claim_ready") is not False:
        errors.append("claim guard unexpectedly reports claim_ready true")
    if errors:
        raise ValueError("; ".join(errors))


def _write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _render_markdown(summary, rows, policy_summary, paired_rows, gates):
    run_dir = summary.get("run_dir", "")
    checkpoint_hashes = sorted({row.get("checkpoint_hash", "") for row in rows if row.get("checkpoint_hash")})
    lines = [
        "# RC Formal Diagnostic Tables",
        "",
        "## Blocker And Provenance Status",
        "",
        f"- Source run: `{run_dir}`",
        f"- Run ID: `{summary.get('run_id', '')}`",
        f"- Execution status: `{summary.get('execution_status', '')}` with `{summary.get('row_count', '')}` rows",
        f"- Readiness status: `{gates['readiness_status']}`; claim-ready allowed: `{str(gates['claim_ready_allowed']).lower()}`",
        f"- Artifact status: `{gates['artifact_status']}`; artifact claim-ready: `{str(gates['artifact_claim_ready']).lower()}`; formal claim-ready: `{str(gates['formal_claim_ready']).lower()}`",
        f"- Claim guard ready: `{str(gates['claim_guard_ready']).lower()}`; blocked claim IDs: `{', '.join(gates['blocked_claim_ids'])}`",
        f"- Checkpoint load status: `loaded`; checkpoint hash: `{checkpoint_hashes[0] if checkpoint_hashes else ''}`",
        "- Claim interpretation status: diagnostic only. Dirty-git readiness and artifact gates block final manuscript claim use.",
        "- Confidence intervals are intentionally omitted because this formal diagnosis has only five paired splits.",
        "- Older smoke artifacts and smoke claim guards are not used as Phase 4 claim evidence.",
        "",
    ]
    if gates["readiness_blockers"]:
        lines.extend(["### Readiness Blockers", ""])
        for blocker in gates["readiness_blockers"]:
            lines.append(f"- `{blocker.get('code', '')}`: {blocker.get('message', '')}")
        lines.append("")
    if gates["artifact_reasons"]:
        lines.extend(["### Artifact Gate Reasons", ""])
        for reason in gates["artifact_reasons"]:
            lines.append(f"- {reason}")
        lines.append("")

    lines.extend(["## Policy Means And Population Standard Deviations", ""])
    lines.append("| Policy | Metric | N | Mean | Std Pop |")
    lines.append("| --- | --- | ---: | ---: | ---: |")
    for row in policy_summary:
        lines.append(
            f"| `{row['policy_tag']}` | `{row['metric']}` | {row['n']} | {_fmt(row['mean'])} | {_fmt(row['std_pop'])} |"
        )
    lines.append("")

    lines.extend(["## Paired Direction Counts", ""])
    lines.append("| Baseline | Metric | Adaptive Better | Baseline Better | Tie | Missing |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: |")
    for baseline in BASELINES:
        for metric in METRICS:
            counts = _direction_counts(paired_rows, metric, baseline=baseline)
            lines.append(
                f"| `{baseline}` | `{metric}` | {counts['adaptive_better']} | {counts['baseline_better']} | {counts['tie']} | {counts['missing']} |"
            )
    lines.append("")

    lines.extend(["## Uptake-Regime Direction Counts", ""])
    lines.append("| Regime | Baseline | Metric | Adaptive Better | Baseline Better | Tie |")
    lines.append("| --- | --- | --- | ---: | ---: | ---: |")
    for regime in sorted({row["uptake_regime"] for row in paired_rows}):
        for baseline in BASELINES:
            for metric in ["net_profit", "acceptance_rate", "served_rate", "optout_rate", "meeting_point_uptake_rate"]:
                counts = _direction_counts(paired_rows, metric, baseline=baseline, regime=regime)
                lines.append(
                    f"| `{regime}` | `{baseline}` | `{metric}` | {counts['adaptive_better']} | {counts['baseline_better']} | {counts['tie']} |"
                )
    lines.append("")

    random_profit = _direction_counts(paired_rows, "net_profit", baseline="mainline_random_menu")
    fixed_profit = _direction_counts(paired_rows, "net_profit", baseline="mainline_optimized_fixed_window")
    fixed_all_ties = all(
        _direction_counts(paired_rows, metric, baseline="mainline_optimized_fixed_window")["tie"] == 5
        for metric in METRICS
    )
    lines.extend(
        [
            "## Diagnostic Notes",
            "",
            f"- Adaptive versus random-menu net profit direction counts: adaptive better `{random_profit['adaptive_better']}`, random better `{random_profit['baseline_better']}`, tie `{random_profit['tie']}`.",
            f"- Adaptive versus optimized fixed-window net profit direction counts: adaptive better `{fixed_profit['adaptive_better']}`, fixed-window better `{fixed_profit['baseline_better']}`, tie `{fixed_profit['tie']}`.",
            f"- Adaptive and optimized fixed-window rows are identical across all tracked metrics: `{str(fixed_all_ties).lower()}`.",
            "- Product ablation evidence should be read from adaptive comparisons with `mainline_optimized_m` and `mainline_optimized_mw`.",
            "- Menu construction evidence should be read from adaptive comparisons with no-menu, fixed-menu, and random-menu baselines.",
            "- Acceptance, opt-out, home-share, and meeting-point uptake trade-offs are reported separately from profit/cost metrics.",
            "- These tables do not upgrade manuscript claims while readiness, artifact, or claim-guard gates remain blocked.",
            "",
        ]
    )
    return "\n".join(lines)


def run(run_dir, readiness_json, artifact_status, claim_guard, output_dir):
    run_dir = Path(run_dir)
    output_dir = Path(output_dir)
    summary = _load_json(run_dir / "study_summary.json")
    rows = _load_json(run_dir / "normalized_rows.json")
    readiness = _load_json(readiness_json)
    artifact_status_data = _load_json(artifact_status)
    claim_guard_data = _load_json(claim_guard)
    validate_inputs(summary, rows, readiness, artifact_status_data, claim_guard_data)

    policy_summary = _summarize_policy(rows)
    paired_rows = _paired_diffs(rows)
    gates = _gate_summary(readiness, artifact_status_data, claim_guard_data)

    policy_out = [
        {
            "policy_tag": row["policy_tag"],
            "metric": row["metric"],
            "n": row["n"],
            "mean": _fmt(row["mean"]),
            "std_pop": _fmt(row["std_pop"]),
        }
        for row in policy_summary
    ]
    paired_out = [
        {
            "split_id": row["split_id"],
            "uptake_regime": row["uptake_regime"],
            "baseline_policy": row["baseline_policy"],
            "metric": row["metric"],
            "adaptive_value": _fmt(row["adaptive_value"]),
            "baseline_value": _fmt(row["baseline_value"]),
            "diff_adaptive_minus_baseline": _fmt(row["diff_adaptive_minus_baseline"]),
            "direction": row["direction"],
        }
        for row in paired_rows
    ]

    output_dir.mkdir(parents=True, exist_ok=True)
    policy_path = output_dir / "RC_FORMAL_POLICY_SUMMARY.csv"
    paired_path = output_dir / "RC_FORMAL_PAIRED_DIFFS.csv"
    markdown_path = output_dir / "RC_FORMAL_DIAGNOSTIC_TABLES.md"
    _write_csv(policy_path, policy_out, ["policy_tag", "metric", "n", "mean", "std_pop"])
    _write_csv(
        paired_path,
        paired_out,
        [
            "split_id",
            "uptake_regime",
            "baseline_policy",
            "metric",
            "adaptive_value",
            "baseline_value",
            "diff_adaptive_minus_baseline",
            "direction",
        ],
    )
    markdown_path.write_text(_render_markdown(summary, rows, policy_summary, paired_rows, gates), encoding="utf-8")
    return {
        "policy_summary": str(policy_path),
        "paired_diffs": str(paired_path),
        "diagnostic_tables": str(markdown_path),
        "row_count": len(rows),
        "split_count": len({row["split_id"] for row in rows}),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Diagnose formal RC service-menu claim evidence without editing generated rows.")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--readiness-json", required=True)
    parser.add_argument("--artifact-status", required=True)
    parser.add_argument("--claim-guard", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args(argv)
    result = run(args.run_dir, args.readiness_json, args.artifact_status, args.claim_guard, args.output_dir)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
