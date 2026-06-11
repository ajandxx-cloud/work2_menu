"""Build Phase 4 evidence artifacts from normalized study rows."""

import csv
import json
import math
import shutil
from collections import defaultdict
from pathlib import Path

import yaml

from Src.artifact_status import (
    classify_artifact,
    collect_environment_provenance,
    utc_now_iso,
    write_json,
)
from Src.study_execution import collect_git_provenance


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = ROOT / "artifacts" / "work2_robust_menu"
DEFAULT_STUDY_OUTPUT_ROOT = ROOT / "outputs" / "studies"
DEFAULT_MIRROR_ROOT = ROOT.parent / "artifacts" / "work2_robust_menu"


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_run(run_dir):
    run_dir = Path(run_dir)
    rows = load_json(run_dir / "normalized_rows.json")
    summary = load_json(run_dir / "study_summary.json")
    manifest_path = run_dir / "manifest_snapshot.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    blockers_path = run_dir / "blockers.json"
    blockers = load_json(blockers_path).get("blockers", []) if blockers_path.exists() else []
    if blockers and not summary.get("blockers"):
        summary["blockers"] = blockers
    return {"run_dir": run_dir, "rows": rows, "summary": summary, "manifest": manifest}


def latest_run_dir(study, study_output_root=None):
    root = Path(study_output_root or DEFAULT_STUDY_OUTPUT_ROOT) / study
    candidates = [path for path in root.iterdir() if path.is_dir()] if root.exists() else []
    if not candidates:
        raise FileNotFoundError("no runs found for study: " + str(study))
    return sorted(candidates, key=lambda path: path.name)[-1]


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


def aggregate_by_policy(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[row["policy_tag"]].append(row)

    aggregates = []
    for policy_tag in sorted(groups):
        policy_rows = groups[policy_tag]
        aggregates.append(
            {
                "policy_tag": policy_tag,
                "row_count": len(policy_rows),
                "filter_mode": _stable_join(row.get("filter_mode") for row in policy_rows),
                "diagnostic": any(bool(row.get("diagnostic")) for row in policy_rows),
                "rank_eligible": not any(bool(row.get("diagnostic")) for row in policy_rows),
                "placeholder_only": any(bool(row.get("placeholder_only")) for row in policy_rows),
                "status": _stable_join(row.get("status") for row in policy_rows),
                "checkpoint_statuses": _stable_join(row.get("checkpoint_load_status") for row in policy_rows),
                "uptake_regimes": _stable_join(row.get("uptake_regime") for row in policy_rows),
                "acceptance_rate_mean": _mean(row.get("acceptance_rate") for row in policy_rows),
                "optout_rate_mean": _mean(row.get("optout_rate") for row in policy_rows),
                "menu_build_time_mean": _mean(row.get("menu_build_time") for row in policy_rows),
                "relative_optimality_gap_mean": _mean(row.get("relative_optimality_gap") for row in policy_rows),
                "home_share_mean": _mean(row.get("count_accepted_home") for row in policy_rows),
            }
        )
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


def artifact_metadata(artifact_path, run_data, status_info, source_rows, artifact_kind):
    summary = run_data["summary"]
    rows = run_data["rows"]
    return {
        "artifact_path": str(Path(artifact_path)),
        "artifact_kind": artifact_kind,
        "source_run_dir": str(run_data["run_dir"]),
        "source_rows": source_rows,
        "source_run_id": summary.get("run_id"),
        "study": summary.get("study_name"),
        "manifest_hash": summary.get("manifest_hash"),
        "generated_at": utc_now_iso(),
        "status": status_info["status"],
        "claim_ready": status_info["claim_ready"],
        "reasons": status_info["reasons"],
        "placeholder_only": status_info["placeholder_only"],
        "checkpoint_summary": status_info["checkpoint_statuses"],
        "uptake_regimes": status_info["uptake_regimes"],
        "diagnostic_policy_labels": status_info["diagnostic_policy_labels"],
        "row_count": len(rows),
        "git_provenance": summary.get("git_provenance") or collect_git_provenance(),
    }


def write_sidecar(artifact_path, run_data, status_info, artifact_kind):
    metadata_path = Path(str(artifact_path) + ".metadata.json")
    write_json(metadata_path, artifact_metadata(artifact_path, run_data, status_info, len(run_data["rows"]), artifact_kind))
    return metadata_path


def _plot_bar(path, labels, series, ylabel, title):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = list(range(len(labels)))
    width = 0.35
    if len(series) == 1:
        ax.bar(x, series[0][1], width=0.55, label=series[0][0])
    else:
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


def _write_incomplete_figure_status(path, reason, run_data, status_info):
    status_path = Path(str(path) + ".status.json")
    payload = artifact_metadata(path, run_data, status_info, len(run_data["rows"]), "figure-status")
    payload["figure_status"] = "incomplete"
    payload["missing_reason"] = reason
    write_json(status_path, payload)
    return status_path


def generate_figures(figures_dir, aggregates, run_data, status_info):
    artifacts = []
    figures_dir = Path(figures_dir)
    labels = [row["policy_tag"] for row in aggregates]

    acceptance = [_num(row.get("acceptance_rate_mean")) for row in aggregates]
    optout = [_num(row.get("optout_rate_mean")) for row in aggregates]
    path = figures_dir / "acceptance_optout.png"
    if all(value is not None for value in acceptance + optout) and labels:
        _plot_bar(path, labels, [("acceptance", acceptance), ("optout", optout)], "rate", "Acceptance and opt-out rates")
        artifacts.append(path)
        artifacts.append(write_sidecar(path, run_data, status_info, "figure"))
    else:
        artifacts.append(_write_incomplete_figure_status(path, "acceptance_rate or optout_rate is unavailable", run_data, status_info))

    build_time = [_num(row.get("menu_build_time_mean")) for row in aggregates]
    path = figures_dir / "exact_greedy_time.png"
    if any(value is not None for value in build_time) and labels:
        values = [0.0 if value is None else value for value in build_time]
        _plot_bar(path, labels, [("menu_build_time", values)], "seconds", "Menu build time by policy")
        artifacts.append(path)
        artifacts.append(write_sidecar(path, run_data, status_info, "figure"))
    else:
        artifacts.append(_write_incomplete_figure_status(path, "menu_build_time is unavailable", run_data, status_info))

    for figure_name, reason in {
        "profit_gap.png": "net_profit metric is unavailable",
        "eta_pruning.png": "ETA pruning metric is unavailable",
        "home_only_share.png": "home-only share metric is unavailable",
    }.items():
        artifacts.append(_write_incomplete_figure_status(figures_dir / figure_name, reason, run_data, status_info))
    return artifacts


def _copy_lightweight(src_root, mirror_root):
    mirror_root = Path(mirror_root)
    if mirror_root.exists():
        shutil.rmtree(mirror_root)
    for path in Path(src_root).rglob("*"):
        if path.is_dir():
            continue
        rel = path.relative_to(src_root)
        if rel.name in {"normalized_rows.json", "normalized_rows.csv", "manifest_snapshot.yaml"}:
            continue
        dest = mirror_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)


def build_artifacts(run_dir, output_root=None, mirror_root=None, allow_incomplete=False, claim_ready=False):
    run_data = load_run(run_dir)
    rows = run_data["rows"]
    summary = run_data["summary"]
    status_info = classify_artifact(
        rows,
        summary,
        claim_ready_requested=claim_ready,
        dependency_snapshot=collect_environment_provenance(include_freeze=claim_ready),
    )
    if claim_ready and not status_info["claim_ready"]:
        raise ValueError("claim-ready artifact generation blocked: " + "; ".join(status_info["reasons"]))
    if not allow_incomplete and not status_info["claim_ready"]:
        raise ValueError("artifact generation is not claim-ready; pass --allow-incomplete for diagnostic artifacts")

    output_root = Path(output_root or DEFAULT_OUTPUT_ROOT)
    output_root.mkdir(parents=True, exist_ok=True)
    aggregates = aggregate_by_policy(rows)
    artifacts = []

    aggregate_json = output_root / "aggregates" / "policy_summary.json"
    aggregate_csv = output_root / "aggregates" / "policy_summary.csv"
    write_json(aggregate_json, aggregates)
    write_csv(aggregate_csv, aggregates)
    artifacts.extend([aggregate_json, write_sidecar(aggregate_json, run_data, status_info, "aggregate-json")])
    artifacts.extend([aggregate_csv, write_sidecar(aggregate_csv, run_data, status_info, "aggregate-csv")])

    tables = [
        ("policy_summary.tex", "Policy summary", ["policy_tag", "row_count", "acceptance_rate_mean", "optout_rate_mean", "rank_eligible"]),
        ("robust_filtering.tex", "Robust filtering summary", ["policy_tag", "filter_mode", "diagnostic", "rank_eligible"]),
        ("exact_greedy.tex", "Exact and greedy solver diagnostics", ["policy_tag", "menu_build_time_mean", "relative_optimality_gap_mean"]),
        ("uptake_regime.tex", "Uptake regime coverage", ["policy_tag", "uptake_regimes", "row_count"]),
        ("provenance_status.tex", "Provenance and status", ["policy_tag", "status", "placeholder_only", "checkpoint_statuses"]),
    ]
    for filename, caption, columns in tables:
        path = output_root / "tables" / filename
        write_latex_table(path, caption, aggregates, columns)
        artifacts.extend([path, write_sidecar(path, run_data, status_info, "latex-table")])

    artifacts.extend(generate_figures(output_root / "figures", aggregates, run_data, status_info))

    ranking = [row for row in aggregates if row["rank_eligible"]]
    ranking_path = output_root / "aggregates" / "recommended_policy_ranking.json"
    write_json(ranking_path, ranking)
    artifacts.extend([ranking_path, write_sidecar(ranking_path, run_data, status_info, "ranking")])

    status_path = output_root / "ARTIFACT_STATUS.json"
    top_status = {
        "artifact_status": status_info,
        "study": summary.get("study_name"),
        "tier": summary.get("tier"),
        "run_id": summary.get("run_id"),
        "source_run_dir": str(run_data["run_dir"]),
        "row_count": len(rows),
        "policies": sorted({row.get("policy_tag") for row in rows}),
        "uptake_regimes": status_info["uptake_regimes"],
        "checkpoint_statuses": status_info["checkpoint_statuses"],
        "placeholder_only": status_info["placeholder_only"],
        "claim_ready": status_info["claim_ready"],
        "pilot_claim_ready": summary.get("tier") == "pilot" and status_info["claim_ready"],
        "formal_claim_ready": summary.get("tier") == "formal" and status_info["claim_ready"],
        "manifest_hash": summary.get("manifest_hash"),
        "git_provenance": summary.get("git_provenance") or collect_git_provenance(),
        "environment_provenance": collect_environment_provenance(include_freeze=claim_ready),
        "generated_artifacts": [str(path) for path in artifacts if Path(path).exists()],
        "blockers": status_info["blockers"],
    }
    write_json(status_path, top_status)
    artifacts.append(status_path)

    readme_path = output_root / "README.md"
    readme_path.write_text(
        "# Work2 Robust Menu Artifacts\n\n"
        + f"Study: {summary.get('study_name')}\n\n"
        + f"Run: {summary.get('run_id')}\n\n"
        + f"Status: {status_info['status']}\n",
        encoding="utf-8",
    )
    artifacts.append(readme_path)

    if mirror_root:
        _copy_lightweight(output_root, mirror_root)

    return {
        "output_root": str(output_root),
        "mirror_root": str(mirror_root) if mirror_root else "",
        "status_path": str(status_path),
        "artifact_status": status_info,
        "artifacts": [str(path) for path in artifacts],
    }

