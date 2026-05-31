import argparse
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Src.research_pipeline import (
    ARTIFACTS_DIR,
    CSV_FIELD_ORDER,
    load_manifest,
    load_study_summary,
    save_json,
    suite_member_summaries,
    utc_now_iso,
    write_csv,
    write_text,
)


def latex_escape(text):
    replacements = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
    }
    escaped = str(text)
    for source, target in replacements.items():
        escaped = escaped.replace(source, target)
    return escaped


def format_metric(value, digits=3):
    if value is None:
        return "--"
    return f"{float(value):.{digits}f}"


def ensure_artifact_dirs():
    for path in [
        ARTIFACTS_DIR,
        ARTIFACTS_DIR / "results_snapshot",
        ARTIFACTS_DIR / "tables",
        ARTIFACTS_DIR / "figures",
    ]:
        path.mkdir(parents=True, exist_ok=True)


def render_placeholder_figure(path, title, message):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.axis("off")
    ax.text(0.5, 0.6, title, ha="center", va="center", fontsize=14, weight="bold")
    ax.text(0.5, 0.4, message, ha="center", va="center", fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def write_tex_table(path, caption, label, headers, rows):
    if not rows:
        placeholder = ["--"] * max(len(headers), 1)
        placeholder[0] = "No data"
        rows = [placeholder]

    if len(headers) >= 8:
        column_spec = "@{}p{0.16\\linewidth}" + "r" * (len(headers) - 1) + "@{}"
    elif len(headers) >= 6:
        column_spec = "@{}p{0.21\\linewidth}" + "r" * (len(headers) - 1) + "@{}"
    else:
        column_spec = "@{}l" + "r" * (len(headers) - 1) + "@{}"

    wide_table = len(headers) >= 5
    font_cmd = r"\footnotesize" if len(headers) >= 8 else r"\small"
    tabcolsep = "2.5pt" if len(headers) >= 8 else ("3pt" if wide_table else "4pt")

    lines = [
        r"\begin{table}[t]",
        r"\centering",
        font_cmd,
        rf"\setlength{{\tabcolsep}}{{{tabcolsep}}}",
        f"\\caption{{{latex_escape(caption)}}}",
        f"\\label{{{label}}}",
    ]

    if wide_table:
        lines.append(r"\resizebox{\linewidth}{!}{%")

    lines.extend(
        [
            f"\\begin{{tabular}}{{{column_spec}}}",
            r"\hline",
            " & ".join(latex_escape(header) for header in headers) + r" \\",
            r"\hline",
        ]
    )

    for row in rows:
        lines.append(" & ".join(latex_escape(cell) for cell in row) + r" \\")

    lines.extend([r"\hline", r"\end{tabular}"])

    if wide_table:
        lines.append(r"}")

    lines.append(r"\end{table}")
    write_text(path, "\n".join(lines) + "\n")


def pick_summary_bundle(study_name):
    manifest = load_manifest(study_name)
    if manifest.get("_kind") == "suite":
        suite_summary, _ = load_study_summary(manifest["name"])
        members = suite_member_summaries(manifest, suite_summary=suite_summary)
        return {
            "kind": "suite",
            "manifest": manifest,
            "suite_summary": suite_summary,
            "member_summaries": members,
        }

    study_summary, _ = load_study_summary(manifest["name"])
    members = []
    if study_summary is not None:
        members.append((manifest["name"], study_summary, None))
    return {
        "kind": "study",
        "manifest": manifest,
        "suite_summary": None,
        "member_summaries": members,
    }


def rows_from_summary(summary):
    if summary is None:
        return []
    return summary.get("aggregate_variant_summary", [])


def study_map(member_summaries):
    mapping = {}
    for study_name, summary, _ in member_summaries:
        mapping[study_name] = summary
    return mapping


def numeric_key(row, key):
    value = row.get(key)
    if value is None:
        return float("-inf")
    return float(value)


DEFAULT_BEHAVIOR_GATE = {
    "min_acceptance_rate": 0.05,
    "max_acceptance_rate": 0.30,
    "max_opt_out_rate": 0.90,
}


def infer_study_role(study_name, study_meta=None, manifest=None):
    explicit_role = None
    if study_meta is not None:
        explicit_role = study_meta.get("study_role")
    if explicit_role is None and manifest is not None:
        explicit_role = manifest.get("study_role")
    if explicit_role:
        return str(explicit_role)
    if study_name in {"austin_main", "seattle_main"}:
        return "impact"
    if study_name in {"filtering_baselines", "rc_main_optout", "rc_main"}:
        return "mechanism"
    return "support"


def resolve_behavior_gate(study_meta=None, manifest=None):
    gate = {}
    if manifest is not None:
        gate.update(manifest.get("behavior_gate", {}))
    if study_meta is not None:
        gate.update(study_meta.get("behavior_gate", {}))
    return {
        "min_acceptance_rate": float(gate.get("min_acceptance_rate", DEFAULT_BEHAVIOR_GATE["min_acceptance_rate"])),
        "max_acceptance_rate": float(gate.get("max_acceptance_rate", DEFAULT_BEHAVIOR_GATE["max_acceptance_rate"])),
        "max_opt_out_rate": float(gate.get("max_opt_out_rate", DEFAULT_BEHAVIOR_GATE["max_opt_out_rate"])),
    }


def compute_acceptance_rate(row):
    if row.get("acceptance_rate") is not None:
        return float(row["acceptance_rate"])
    home_pickup_share = row.get("home_pickup_share")
    if home_pickup_share is None:
        return None
    return float(1.0 - float(home_pickup_share))


def compute_behavior_non_degenerate(row, gate):
    if row.get("is_behavior_non_degenerate") is not None:
        return bool(row["is_behavior_non_degenerate"])
    acceptance_rate = compute_acceptance_rate(row)
    opt_out_rate = row.get("opt_out_rate")
    if acceptance_rate is None or opt_out_rate is None:
        return None
    return bool(
        gate["min_acceptance_rate"] <= float(acceptance_rate) <= gate["max_acceptance_rate"]
        and float(opt_out_rate) < gate["max_opt_out_rate"]
    )


def variant_display_label(row):
    tag = row.get("variant_tag", "")
    label = str(row.get("variant_label", tag)).strip()

    if tag in {"full_display", "offer_all_feasible_bundles"}:
        return "full display"
    if tag == "menu_optimization":
        return "strict-filter heuristic"
    if tag == "menu_optimization_v2":
        return "no-filter heuristic"
    if tag == "nearest_L":
        return "Nearest-L"
    if tag == "cost_L":
        return "Cost-L"
    if tag == "cnn_menu":
        return "CNN-Menu"
    if tag == "setmenu_net":
        return "SetMenuNet"
    if tag == "cnn_setmenu_net":
        return "CNN-SetMenuNet"
    if tag == "oracle_menu":
        return "Oracle Menu"

    lowered = label.lower()
    normalized = {
        "menu optimization": "strict-filter heuristic",
        "menu optimization v1": "strict-filter heuristic",
        "menu optimization v2": "no-filter heuristic",
        "menu optimization v2 (no filter)": "no-filter heuristic",
        "v1 hard eta filter": "strict hard ETA filter",
        "v1 calibrated eta filter": "strict calibrated ETA filter",
        "v1 interval-overlap eta filter": "strict interval-overlap filter",
        "v2 with time filtering restored": "no-filter heuristic + ETA filter restored",
        "v2 no capacity-risk penalty": "no-filter heuristic, no capacity-risk penalty",
        "v2 no forced home retention": "no-filter heuristic, no forced home retention",
        "v2 no route-delay penalty": "no-filter heuristic, no route-delay penalty",
        "exact assortment benchmark": "exact benchmark",
        "greedy forward selection": "greedy approximation",
        "auto exact-small greedy-large": "auto solver",
        "hard eta filter": "hard ETA filter",
        "calibrated eta filter": "calibrated ETA filter",
        "interval-overlap eta filter": "interval-overlap filter",
        "no eta filter": "no ETA filter",
        "random_top_k": "random-top-k floor",
        "insertion_cost_greedy": "insertion-cost greedy",
        "min_lateness": "min-lateness ranking",
    }
    if lowered in normalized:
        return normalized[lowered]
    return label


def uptake_regime_from_tag(tag, study_name=""):
    study_text = str(study_name)
    text = str(tag)
    if study_text.endswith("_low") or text.startswith("low_"):
        return "low"
    if study_text.endswith("_medium") or text.startswith("medium_"):
        return "medium"
    if study_text.endswith("_high") or text.startswith("high_"):
        return "high"
    return "--"


def uptake_policy_from_tag(tag):
    text = str(tag)
    if text in {"auto"} or text.endswith("_auto"):
        return "auto solver"
    if text in {"exact"} or text.endswith("_exact"):
        return "exact solver"
    if text in {"no_filter"} or text.endswith("_no_filter"):
        return "no ETA filter"
    if text in {"flat_markdown"} or text.endswith("_flat_markdown"):
        return "flat markdown"
    if text == "full_display":
        return "full display"
    return text


def row_display_label(row):
    return row.get("display_label") or variant_display_label(row)



def enrich_policy_rows(rows, study_name, study_meta=None, manifest=None):
    gate = resolve_behavior_gate(study_meta=study_meta, manifest=manifest)
    study_role = infer_study_role(study_name, study_meta=study_meta, manifest=manifest)
    enriched = []
    for row in rows:
        item = dict(row)
        item.setdefault("study_role", study_role)
        item["display_label"] = variant_display_label(item)
        item["acceptance_rate"] = compute_acceptance_rate(item)
        item["is_behavior_non_degenerate"] = compute_behavior_non_degenerate(item, gate)
        enriched.append(item)
    return enriched


def resolve_headline_variants(study_name, study_meta=None, manifest=None):
    headline_variants = []
    if manifest is not None:
        headline_variants = list(manifest.get("headline_variants", []))
    if not headline_variants and study_meta is not None:
        headline_variants = list(study_meta.get("headline_variants", []))
    if headline_variants:
        return headline_variants
    if infer_study_role(study_name, study_meta=study_meta, manifest=manifest) == "impact":
        return ["full_display", "menu_optimization", "menu_optimization_v2"]
    if study_name == "rc_main_optout":
        return ["full_display", "menu_optimization", "menu_optimization_v2"]
    return []


def sort_main_rows(rows):
    preferred = {
        "full_display": 0,
        "offer_all_feasible_bundles": 0,
        "menu_optimization": 1,
        "menu_optimization_v2": 2,
        "nearest_heuristic": 3,
        "top_k_cheapest": 4,
        "top_k_passenger_utility": 5,
        "revenue_greedy": 6,
        "insertion_cost_greedy": 7,
        "min_lateness": 8,
        "random_top_k": 9,
    }
    return sorted(rows, key=lambda row: (preferred.get(row["variant_tag"], 99), row["variant_tag"]))


def split_headline_rows(rows, headline_variants):
    if not rows:
        return [], []
    if not headline_variants:
        return sort_main_rows(rows), []

    headline_order = {tag: idx for idx, tag in enumerate(headline_variants)}
    headline_rows = [row for row in rows if row.get("variant_tag") in headline_order]
    secondary_rows = [row for row in rows if row.get("variant_tag") not in headline_order]

    if not headline_rows:
        return sort_main_rows(rows), []

    headline_rows = sorted(
        headline_rows,
        key=lambda row: (headline_order.get(row.get("variant_tag"), 999), row.get("variant_tag", "")),
    )
    return headline_rows, sort_main_rows(secondary_rows)


def build_main_policy_artifacts(
    rows,
    prefix="main_policy",
    caption="Main RC policy comparison.",
    plot_title="Main RC policy comparison",
    headline_variants=None,
):
    rows, secondary_rows = split_headline_rows(rows, headline_variants or [])
    table_rows = []
    plot_labels = []
    plot_values = []
    plot_gaps = []

    for row in sort_main_rows(rows):
        table_rows.append(
            [
                row["display_label"],
                format_metric(row.get("net_profit")),
                format_metric(row.get("mean_net_profit_gap_vs_reference")),
                format_metric(row.get("net_profit_win_rate_vs_reference")),
                format_metric(row.get("average_menu_size")),
                format_metric(row.get("avg_meeting_point_count_per_menu")),
            ]
        )
        plot_labels.append(row["display_label"])
        plot_values.append(row.get("net_profit", 0.0) or 0.0)
        plot_gaps.append(row.get("mean_net_profit_gap_vs_reference", 0.0) or 0.0)

    write_tex_table(
        ARTIFACTS_DIR / "tables" / f"{prefix}_summary.tex",
        caption=caption,
        label=f"tab:{prefix}",
        headers=[
            "Policy",
            "Mean net profit",
            "Gap vs full",
            "Win rate vs full",
            "Mean menu size",
            "Avg meeting-point count",
        ],
        rows=table_rows,
    )

    write_csv(
        ARTIFACTS_DIR / "tables" / f"{prefix}_summary.csv",
        rows,
    )

    if secondary_rows:
        secondary_table_rows = [
            [
                row["display_label"],
                format_metric(row.get("net_profit")),
                format_metric(row.get("mean_net_profit_gap_vs_reference")),
                format_metric(row.get("net_profit_win_rate_vs_reference")),
                format_metric(row.get("average_menu_size")),
                format_metric(row.get("avg_meeting_point_count_per_menu")),
            ]
            for row in secondary_rows
        ]
        write_tex_table(
            ARTIFACTS_DIR / "tables" / f"{prefix}_secondary_summary.tex",
            caption=f"{caption} Supplementary robustness policies.",
            label=f"tab:{prefix}_secondary",
            headers=[
                "Policy",
                "Mean net profit",
                "Gap vs full",
                "Win rate vs full",
                "Mean menu size",
                "Avg meeting-point count",
            ],
            rows=secondary_table_rows,
        )
        write_csv(
            ARTIFACTS_DIR / "tables" / f"{prefix}_secondary_summary.csv",
            secondary_rows,
        )

    if not rows:
        render_placeholder_figure(
            ARTIFACTS_DIR / "figures" / f"{prefix}_net_profit.png",
            plot_title,
            "Run the main study to populate this figure.",
        )
        render_placeholder_figure(
            ARTIFACTS_DIR / "figures" / f"{prefix}_gap_vs_full.png",
            "Policy gap vs full display",
            "Run the main study to populate this figure.",
        )
        return

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(plot_labels, plot_values, color="#4C78A8")
    ax.set_ylabel("Mean net profit")
    ax.set_title(plot_title)
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    fig.savefig(ARTIFACTS_DIR / "figures" / f"{prefix}_net_profit.png", dpi=200)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(plot_labels, plot_gaps, color="#F58518")
    ax.axhline(0.0, color="black", linewidth=1)
    ax.set_ylabel("Mean net-profit gap vs full display")
    ax.set_title("Policy net-profit gap against full display")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    fig.savefig(ARTIFACTS_DIR / "figures" / f"{prefix}_gap_vs_full.png", dpi=200)
    plt.close(fig)


def build_robustness_artifacts(rows, prefix="robustness_menu_k"):
    rows = [row for row in rows if not row.get("is_reference")]
    rows = sorted(rows, key=lambda row: int(row.get("menu_k", 0)))
    table_rows = [
        [
            f"k={row.get('menu_k')}",
            format_metric(row.get("net_profit")),
            format_metric(row.get("mean_net_profit_gap_vs_reference")),
            format_metric(row.get("net_profit_win_rate_vs_reference")),
            format_metric(row.get("average_menu_size")),
            format_metric(row.get("avg_meeting_point_count_per_menu")),
        ]
        for row in rows
    ]

    write_tex_table(
        ARTIFACTS_DIR / "tables" / f"{prefix}_summary.tex",
        caption="RC robustness sweep over menu size.",
        label=f"tab:{prefix}",
        headers=[
            "Variant",
            "Mean net profit",
            "Gap vs full",
            "Win rate vs full",
            "Mean menu size",
            "Avg meeting-point count",
        ],
        rows=table_rows,
    )
    write_csv(ARTIFACTS_DIR / "tables" / f"{prefix}_summary.csv", rows)

    if not rows:
        render_placeholder_figure(
            ARTIFACTS_DIR / "figures" / f"{prefix}_gap.png",
            "Menu-k robustness",
            "Run the robustness study to populate this figure.",
        )
        return

    xs = [int(row["menu_k"]) for row in rows]
    ys = [row.get("mean_net_profit_gap_vs_reference", 0.0) or 0.0 for row in rows]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(xs, ys, marker="o", color="#54A24B")
    ax.axhline(0.0, color="black", linewidth=1)
    ax.set_xlabel("menu_k")
    ax.set_ylabel("Mean net-profit gap vs full display")
    ax.set_title("RC robustness over menu size")
    fig.tight_layout()
    fig.savefig(ARTIFACTS_DIR / "figures" / f"{prefix}_gap.png", dpi=200)
    plt.close(fig)


def build_ablation_artifacts(rows, prefix="ablation"):
    sorted_rows = sorted(rows, key=lambda row: (0 if row.get("ablation_tag") == "baseline" else 1, row["variant_tag"]))
    table_rows = [
        [
            row["display_label"],
            format_metric(row.get("net_profit")),
            format_metric(row.get("mean_net_profit_gap_vs_reference")),
            format_metric(row.get("mean_net_profit_gap_vs_baseline")),
            format_metric(row.get("average_menu_size")),
            format_metric(row.get("avg_meeting_point_count_per_menu")),
        ]
        for row in sorted_rows
    ]

    write_tex_table(
        ARTIFACTS_DIR / "tables" / f"{prefix}_summary.tex",
        caption="RC menu-component ablation study.",
        label=f"tab:{prefix}",
        headers=[
            "Variant",
            "Mean net profit",
            "Gap vs full",
            "Gap vs baseline menu",
            "Mean menu size",
            "Avg meeting-point count",
        ],
        rows=table_rows,
    )
    write_csv(ARTIFACTS_DIR / "tables" / f"{prefix}_summary.csv", sorted_rows)

    if not rows:
        render_placeholder_figure(
            ARTIFACTS_DIR / "figures" / f"{prefix}_gap_vs_baseline.png",
            "Menu ablations",
            "Run the ablation study to populate this figure.",
        )
        return

    labels = [row["display_label"] for row in sorted_rows]
    ys = [row.get("mean_net_profit_gap_vs_baseline", 0.0) or 0.0 for row in sorted_rows]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(labels, ys, color="#E45756")
    ax.axhline(0.0, color="black", linewidth=1)
    ax.set_ylabel("Mean net-profit gap vs baseline menu")
    ax.set_title("RC menu-component ablations")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    fig.savefig(ARTIFACTS_DIR / "figures" / f"{prefix}_gap_vs_baseline.png", dpi=200)
    plt.close(fig)


def build_exact_greedy_artifacts(rows, prefix="phase29_exact_greedy_gap"):
    rows = sorted(rows, key=lambda row: {"full_display": 0, "exact": 1, "greedy": 2, "auto": 3}.get(row.get("variant_tag"), 99))
    table_rows = [
        [
            row["display_label"],
            format_metric(row.get("mean_net_profit_gap_vs_reference")),
            format_metric(row.get("mean_net_profit_gap_vs_baseline")),
            format_metric(row.get("avg_relative_optimality_gap"), digits=4),
            format_metric(row.get("avg_menu_overlap_rate")),
            format_metric(row.get("avg_exact_build_time"), digits=4),
            format_metric(row.get("avg_greedy_build_time"), digits=4),
            format_metric(row.get("exact_gap_logged_share")),
        ]
        for row in rows
    ]
    write_tex_table(
        ARTIFACTS_DIR / "tables" / f"{prefix}_summary.tex",
        caption="Exact-vs-greedy assortment diagnostics on the RC benchmark.",
        label=f"tab:{prefix}",
        headers=[
            "Solver",
            "Gap vs full",
            "Gap vs exact",
            "Rel. opt. gap",
            "Menu overlap",
            "Exact time",
            "Greedy time",
            "Logged share",
        ],
        rows=table_rows,
    )
    write_csv(ARTIFACTS_DIR / "tables" / f"{prefix}_summary.csv", rows)


def build_robust_filtering_artifacts(rows, prefix="phase30_robust_filtering"):
    order = {"full_display": 0, "hard_filter": 1, "calibrated_filter": 2, "interval_filter": 3, "no_filter": 4}
    rows = sorted(rows, key=lambda row: order.get(row.get("variant_tag"), 99))
    table_rows = [
        [
            row["display_label"],
            format_metric(row.get("mean_net_profit_gap_vs_reference")),
            format_metric(row.get("avg_fn_pruning_rate")),
            format_metric(row.get("home_pickup_only_share")),
            format_metric(row.get("average_menu_size")),
            format_metric(row.get("acceptance_rate")),
            format_metric(row.get("non_home_acceptance_rate")),
        ]
        for row in rows
    ]
    write_tex_table(
        ARTIFACTS_DIR / "tables" / f"{prefix}_summary.tex",
        caption="Robust ETA-filtering comparison on the RC benchmark.",
        label=f"tab:{prefix}",
        headers=[
            "Filter",
            "Gap vs full",
            "FN pruning",
            "Home-only share",
            "Menu size",
            "Acceptance",
            "Non-home acc.",
        ],
        rows=table_rows,
    )
    write_csv(ARTIFACTS_DIR / "tables" / f"{prefix}_summary.csv", rows)


def build_uptake_menu_value_artifacts(rows, prefix="phase31_uptake_menu_value"):
    regime_order = {"--": 0, "low": 1, "medium": 2, "high": 3}
    policy_order = {"full display": 0, "exact solver": 1, "auto solver": 2, "no ETA filter": 3, "flat markdown": 4}
    rows = sorted(
        rows,
        key=lambda row: (
            regime_order.get(uptake_regime_from_tag(row.get("variant_tag"), row.get("study_name", "")), 99),
            policy_order.get(uptake_policy_from_tag(row.get("variant_tag")), 99),
            row.get("variant_tag", ""),
        ),
    )
    table_rows = [
        [
            uptake_regime_from_tag(row.get("variant_tag"), row.get("study_name", "")),
            uptake_policy_from_tag(row.get("variant_tag")),
            format_metric(row.get("mean_net_profit_gap_vs_reference")),
            format_metric(row.get("acceptance_rate")),
            format_metric(row.get("non_home_acceptance_rate")),
            format_metric(row.get("consumer_surplus")),
            format_metric(row.get("avg_fn_pruning_rate")),
            format_metric(row.get("price_at_floor_fraction")),
        ]
        for row in rows
    ]
    write_tex_table(
        ARTIFACTS_DIR / "tables" / f"{prefix}_summary.tex",
        caption="Menu-value comparison across low, medium, and high uptake regimes.",
        label=f"tab:{prefix}",
        headers=[
            "Regime",
            "Policy",
            "Gap vs full",
            "Acceptance",
            "Non-home acc.",
            "Surplus",
            "FN pruning",
            "Floor hit",
        ],
        rows=table_rows,
    )
    write_csv(ARTIFACTS_DIR / "tables" / f"{prefix}_summary.csv", rows)


def outside_option_u0_from_study(study_name):
    text = str(study_name)
    if text.endswith("_m10"):
        return "$-1.0$"
    if text.endswith("_m05"):
        return "$-0.5$"
    if text.endswith("_00"):
        return "$0.0$"
    if text.endswith("_p05"):
        return "$+0.5$"
    if text.endswith("_p10"):
        return "$+1.0$"
    return "--"


def build_outside_option_scan_artifacts(rows, prefix="outside_option_scan"):
    u0_order = {"$-1.0$": 0, "$-0.5$": 1, "$0.0$": 2, "$+0.5$": 3, "$+1.0$": 4}
    policy_order = {"full display": 0, "strict_filter": 1, "no_filter": 2, "flat_markdown": 3}
    rows = sorted(
        rows,
        key=lambda row: (
            u0_order.get(outside_option_u0_from_study(row.get("study_name", "")), 99),
            policy_order.get(row.get("variant_tag", ""), 99),
        ),
    )
    table_rows = [
        [
            outside_option_u0_from_study(row.get("study_name", "")),
            row.get("variant_tag", "--"),
            format_metric(row.get("mean_net_profit_gap_vs_reference")),
            format_metric(row.get("acceptance_rate")),
            format_metric(row.get("non_home_acceptance_rate")),
            format_metric(row.get("consumer_surplus")),
            format_metric(row.get("opt_out_rate")),
            format_metric(row.get("price_at_floor_fraction")),
        ]
        for row in rows
    ]
    write_tex_table(
        ARTIFACTS_DIR / "tables" / f"{prefix}_summary.tex",
        caption="Outside-option utility sensitivity scan across five $u_0$ levels on the primary RC calibration. Gap vs full is the mean net-profit gap against exhaustive full display.",
        label=f"tab:{prefix}_summary",
        headers=[
            "$u_0$",
            "Policy",
            "Gap vs full",
            "Acceptance",
            "Non-home acc.",
            "Surplus",
            "Opt-out rate",
            "Floor hit",
        ],
        rows=table_rows,
    )
    write_csv(ARTIFACTS_DIR / "tables" / f"{prefix}_summary.csv", rows)


def build_welfare_artifacts(
    rows,
    prefix="welfare",
    caption="Passenger welfare and pricing metrics by policy.",
    headline_variants=None,
):
    """Generate LaTeX welfare table comparing policies on passenger-welfare metrics."""
    rows, _ = split_headline_rows(rows, headline_variants or [])
    table_rows = []
    for row in sort_main_rows(rows):
        opt_out = row.get("opt_out_rate")
        acceptance = row.get("acceptance_rate")
        table_rows.append([
            row["display_label"],
            format_metric(acceptance),
            format_metric(row.get("consumer_surplus")),
            format_metric(row.get("avg_walk_distance")),
            format_metric(row.get("avg_pickup_time_deviation")),
            format_metric(row.get("avg_in_vehicle_time")),
            format_metric(opt_out),
            format_metric(row.get("price_at_floor_fraction")),
            format_metric(row.get("price_at_ceil_fraction")),
        ])
    write_tex_table(
        ARTIFACTS_DIR / "tables" / f"{prefix}_table.tex",
        caption=caption,
        label=f"tab:{prefix}",
        headers=[
            "Policy",
            "Acceptance rate",
            "Consumer surplus",
            "Avg walk dist",
            "Avg pickup dev",
            "Avg IVT",
            "Opt-out rate",
            "Price-at-floor",
            "Price-at-ceil",
        ],
        rows=table_rows,
    )


def row_by_tag(rows, tag):
    return next((row for row in rows if row.get("variant_tag") == tag), None)


def build_city_impact_entry(study_name, rows):
    full_row = row_by_tag(rows, "full_display")
    v1_row = row_by_tag(rows, "menu_optimization")
    v2_row = row_by_tag(rows, "menu_optimization_v2")
    if full_row is None or v1_row is None or v2_row is None:
        return None

    entry = {
        "city": study_name,
        "v2_vs_full_profit_gap": v2_row.get("mean_net_profit_gap_vs_reference"),
        "v2_vs_v1_profit_gap": (
            None
            if v2_row.get("net_profit") is None or v1_row.get("net_profit") is None
            else float(v2_row["net_profit"]) - float(v1_row["net_profit"])
        ),
        "acceptance_delta_vs_full": (
            None
            if v2_row.get("acceptance_rate") is None or full_row.get("acceptance_rate") is None
            else float(v2_row["acceptance_rate"]) - float(full_row["acceptance_rate"])
        ),
        "consumer_surplus_delta_vs_full": (
            None
            if v2_row.get("consumer_surplus") is None or full_row.get("consumer_surplus") is None
            else float(v2_row["consumer_surplus"]) - float(full_row["consumer_surplus"])
        ),
        "full_is_behavior_non_degenerate": full_row.get("is_behavior_non_degenerate"),
        "v2_is_behavior_non_degenerate": v2_row.get("is_behavior_non_degenerate"),
    }
    full_gate = bool(full_row.get("is_behavior_non_degenerate"))
    v2_gate = bool(v2_row.get("is_behavior_non_degenerate"))
    if full_gate and v2_gate:
        entry["behavior_gate_status"] = "pass"
    elif full_gate or v2_gate:
        entry["behavior_gate_status"] = "mixed"
    else:
        entry["behavior_gate_status"] = "fail"

    profit_positive = (
        entry["v2_vs_full_profit_gap"] is not None
        and entry["v2_vs_v1_profit_gap"] is not None
        and float(entry["v2_vs_full_profit_gap"]) > 0.0
        and float(entry["v2_vs_v1_profit_gap"]) > 0.0
    )
    welfare_guard = (
        (entry["acceptance_delta_vs_full"] is not None and float(entry["acceptance_delta_vs_full"]) >= -0.02)
        or (
            entry["consumer_surplus_delta_vs_full"] is not None
            and float(entry["consumer_surplus_delta_vs_full"]) >= -0.1
        )
    )
    if profit_positive and welfare_guard:
        entry["impact_verdict"] = "positive"
    elif profit_positive:
        entry["impact_verdict"] = "profit_only"
    else:
        entry["impact_verdict"] = "unstable"
    return entry


def pooled_city_impact_entry(entries):
    if not entries:
        return None
    pooled = {"city": "pooled"}
    for key in [
        "v2_vs_full_profit_gap",
        "v2_vs_v1_profit_gap",
        "acceptance_delta_vs_full",
        "consumer_surplus_delta_vs_full",
    ]:
        values = [entry.get(key) for entry in entries if entry.get(key) is not None]
        pooled[key] = None if not values else float(sum(values) / len(values))

    statuses = {entry.get("behavior_gate_status") for entry in entries}
    if statuses == {"pass"}:
        pooled["behavior_gate_status"] = "pass"
    elif "pass" in statuses or "mixed" in statuses:
        pooled["behavior_gate_status"] = "mixed"
    else:
        pooled["behavior_gate_status"] = "fail"

    verdicts = {entry.get("impact_verdict") for entry in entries}
    if verdicts == {"positive"}:
        pooled["impact_verdict"] = "positive"
    elif "positive" in verdicts or "profit_only" in verdicts:
        pooled["impact_verdict"] = "profit_only"
    else:
        pooled["impact_verdict"] = "unstable"
    return pooled


def build_city_impact_artifacts(austin_summary=None, seattle_summary=None):
    city_rows = []
    if austin_summary is not None:
        city_rows.append(
            build_city_impact_entry(
                "Austin",
                enrich_policy_rows(
                    rows_from_summary(austin_summary),
                    "austin_main",
                    study_meta=austin_summary.get("study", {}),
                    manifest=load_manifest("austin_main"),
                ),
            )
        )
    if seattle_summary is not None:
        city_rows.append(
            build_city_impact_entry(
                "Seattle",
                enrich_policy_rows(
                    rows_from_summary(seattle_summary),
                    "seattle_main",
                    study_meta=seattle_summary.get("study", {}),
                    manifest=load_manifest("seattle_main"),
                ),
            )
        )
    city_rows = [row for row in city_rows if row is not None]
    pooled = pooled_city_impact_entry(city_rows)
    if pooled is not None:
        city_rows.append(pooled)

    table_rows = [
        [
            row["city"],
            format_metric(row.get("v2_vs_full_profit_gap")),
            format_metric(row.get("v2_vs_v1_profit_gap")),
            format_metric(row.get("acceptance_delta_vs_full")),
            format_metric(row.get("consumer_surplus_delta_vs_full")),
        ]
        for row in city_rows
    ]
    write_tex_table(
        ARTIFACTS_DIR / "tables" / "city_impact_summary.tex",
        caption="City-level management summary for the no-filter heuristic against full display and the strict-filter heuristic.",
        label="tab:city_impact_summary",
        headers=[
            "City",
            "No-filter vs full gap",
            "No-filter vs strict gap",
            "Acceptance delta",
            "Consumer-surplus delta",
        ],
        rows=table_rows,
    )
    write_csv(ARTIFACTS_DIR / "tables" / "city_impact_summary.csv", city_rows)
    return city_rows


PHASE19_STUDY_LABELS = {
    "rc_main_optout": "RC outside-option",
    "austin_main": "Austin",
    "seattle_main": "Seattle",
}


def format_interval(lower, upper, digits=2):
    if lower is None or upper is None:
        return "--"
    return f"[{float(lower):.{digits}f}, {float(upper):.{digits}f}]"



def bootstrap_mean_ci(values, B=10000, seed=42):
    if not values:
        return None, None
    arr = np.array(values, dtype=float)
    rng = np.random.default_rng(seed)
    boot = np.array([
        float(np.mean(rng.choice(arr, size=len(arr), replace=True)))
        for _ in range(B)
    ])
    return float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))



def load_run_normalized_rows(study_name, run_id):
    path = ROOT / "outputs" / "studies" / study_name / run_id / "normalized_rows.json"
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))



def human_split_label(split_id):
    label = split_id
    for prefix in ["rc_", "austin_", "seattle_"]:
        if label.startswith(prefix):
            label = label[len(prefix):]
            break
    label = label.replace("_to_", "->")
    if "_seed" in label:
        base, seed = label.split("_seed", 1)
        label = f"{base} (seed {seed})"
    return label



def read_paired_gap(study_name, run_id, split_id, variant_tag):
    path = ROOT / "outputs" / "studies" / study_name / run_id / "splits" / split_id / f"{variant_tag}_paired_vs_full_display.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))



def build_phase19_support_artifacts():
    study_summaries = {}
    enriched_aggregate_rows = {}
    split_rows_by_study = {}
    for study_name in PHASE19_STUDY_LABELS:
        summary, _ = load_study_summary(study_name)
        if summary is None:
            continue
        manifest = load_manifest(study_name)
        study_summaries[study_name] = summary
        enriched_aggregate_rows[study_name] = enrich_policy_rows(
            rows_from_summary(summary),
            study_name,
            study_meta=summary.get("study", {}),
            manifest=manifest,
        )
        split_rows_by_study[study_name] = enrich_policy_rows(
            load_run_normalized_rows(study_name, summary["run_metadata"]["run_id"]),
            study_name,
            study_meta=summary.get("study", {}),
            manifest=manifest,
        )

    if not study_summaries:
        return

    uncertainty_records = []
    uncertainty_table_rows = []
    for study_name in ["rc_main_optout", "austin_main", "seattle_main"]:
        split_rows = [row for row in split_rows_by_study.get(study_name, []) if row.get("split_id")]
        if not split_rows:
            continue
        full_rows = [row for row in split_rows if row.get("variant_tag") == "full_display"]
        if not full_rows:
            continue
        reference_mean = float(np.mean([row["net_profit"] for row in full_rows]))
        for tag in ["menu_optimization", "menu_optimization_v2"]:
            values = [
                float(row["mean_net_profit_gap_vs_reference"])
                for row in split_rows
                if row.get("variant_tag") == tag and row.get("mean_net_profit_gap_vs_reference") is not None
            ]
            if not values:
                continue
            if len(values) <= 2:
                lower, upper = float(np.min(values)), float(np.max(values))
                interval_kind = "Two-pair descriptive range"
            else:
                lower, upper = bootstrap_mean_ci(values)
                interval_kind = "Split-level range (6 pairs)"
            row = row_by_tag(enriched_aggregate_rows.get(study_name, []), tag) or {"variant_tag": tag}
            positive_share = float(np.mean(np.array(values) > 0.0))
            relative_scale = 100.0 * float(np.mean(values)) / abs(reference_mean) if reference_mean else None
            sampling_unit = f"{len(values)} split pairs"
            if len(values) <= 2:
                sampling_unit += " (descriptive)"
            record = {
                "study": PHASE19_STUDY_LABELS[study_name],
                "policy": row_display_label(row),
                "mean_gap": float(np.mean(values)),
                "ci_lower": lower,
                "ci_upper": upper,
                "interval_kind": interval_kind,
                "positive_split_share": positive_share,
                "relative_scale_pct": relative_scale,
                "sampling_unit": sampling_unit,
            }
            uncertainty_records.append(record)
            uncertainty_table_rows.append([
                record["study"],
                record["policy"],
                format_metric(record["mean_gap"], digits=2),
                format_interval(record["ci_lower"], record["ci_upper"], digits=2),
                record["interval_kind"],
                format_metric(record["positive_split_share"], digits=2),
                format_metric(record["relative_scale_pct"], digits=2),
                record["sampling_unit"],
            ])

    write_tex_table(
        ARTIFACTS_DIR / "tables" / "policy_gap_uncertainty_summary.tex",
        caption=(
            "Split-level paired gap summary for the strict-filter and no-filter heuristics against full display. "
            "The inferential unit is the split-level paired mean net-profit gap; RC uses six split pairs, "
            "while Austin and Seattle each use two split pairs and are therefore descriptive only. "
            "Austin and Seattle each have only two split pairs; their gaps are reported as descriptive checks, not stable interval estimates."
        ),
        label="tab:policy_gap_uncertainty_summary",
        headers=[
            "Study",
            "Policy",
            "Mean gap",
            "Split-level range",
            "Range type",
            "Positive-split share",
            "Gap as % of |full|",
            "Sampling unit",
        ],
        rows=uncertainty_table_rows,
    )
    write_csv(ARTIFACTS_DIR / "tables" / "policy_gap_uncertainty_summary.csv", uncertainty_records)

    rc_summary = study_summaries.get("rc_main_optout")
    if rc_summary is not None:
        run_id = rc_summary["run_metadata"]["run_id"]
        rc_split_ids = sorted({row["split_id"] for row in split_rows_by_study["rc_main_optout"] if row.get("split_id")})
        rc_records = []
        rc_table_rows = []
        for split_id in rc_split_ids:
            strict_data = read_paired_gap("rc_main_optout", run_id, split_id, "menu_optimization")
            no_filter_data = read_paired_gap("rc_main_optout", run_id, split_id, "menu_optimization_v2")
            record = {
                "split": human_split_label(split_id),
                "strict_gap": None if strict_data is None else strict_data.get("mean_net_profit_gap"),
                "strict_ci_half_width": None if strict_data is None else strict_data.get("net_profit_gap_ci95_half_width"),
                "no_filter_gap": None if no_filter_data is None else no_filter_data.get("mean_net_profit_gap"),
                "no_filter_ci_half_width": None if no_filter_data is None else no_filter_data.get("net_profit_gap_ci95_half_width"),
            }
            rc_records.append(record)
            rc_table_rows.append([
                record["split"],
                format_metric(record["strict_gap"], digits=2),
                format_metric(record["strict_ci_half_width"], digits=2),
                format_metric(record["no_filter_gap"], digits=2),
                format_metric(record["no_filter_ci_half_width"], digits=2),
            ])
        write_tex_table(
            ARTIFACTS_DIR / "tables" / "rc_main_optout_split_gap_table.tex",
            caption=(
                "RC outside-option split-level paired gaps against full display. "
                "Within-split CI half-width is computed from episode-level pairing inside each split; main-text uncertainty uses the split-level paired means rather than pooled episode rows."
            ),
            label="tab:rc_split_gap_summary",
            headers=[
                "Split pair",
                "Strict gap",
                "Strict within-split CI/2",
                "No-filter gap",
                "No-filter within-split CI/2",
            ],
            rows=rc_table_rows,
        )
        write_csv(ARTIFACTS_DIR / "tables" / "rc_main_optout_split_gap_table.csv", rc_records)

    city_records = []
    city_table_rows = []
    for study_name in ["austin_main", "seattle_main"]:
        summary = study_summaries.get(study_name)
        if summary is None:
            continue
        run_id = summary["run_metadata"]["run_id"]
        split_ids = sorted({row["split_id"] for row in split_rows_by_study[study_name] if row.get("split_id")})
        for split_id in split_ids:
            strict_data = read_paired_gap(study_name, run_id, split_id, "menu_optimization")
            no_filter_data = read_paired_gap(study_name, run_id, split_id, "menu_optimization_v2")
            record = {
                "city": PHASE19_STUDY_LABELS[study_name],
                "split": human_split_label(split_id),
                "strict_gap": None if strict_data is None else strict_data.get("mean_net_profit_gap"),
                "no_filter_gap": None if no_filter_data is None else no_filter_data.get("mean_net_profit_gap"),
            }
            city_records.append(record)
            city_table_rows.append([
                record["city"],
                record["split"],
                format_metric(record["strict_gap"], digits=2),
                format_metric(record["no_filter_gap"], digits=2),
            ])
    write_tex_table(
        ARTIFACTS_DIR / "tables" / "city_split_gap_table.tex",
        caption=(
            "Austin and Seattle split-level paired gaps against full display. "
            "Each city has only two split pairs, so these rows should be read descriptively rather than as stable interval estimates."
        ),
        label="tab:city_split_gap_summary",
        headers=[
            "City",
            "Split pair",
            "Strict gap",
            "No-filter gap",
        ],
        rows=city_table_rows,
    )
    write_csv(ARTIFACTS_DIR / "tables" / "city_split_gap_table.csv", city_records)

    diagnostic_records = []
    diagnostic_table_rows = []
    for study_name in ["austin_main", "seattle_main"]:
        for tag in ["full_display", "menu_optimization", "menu_optimization_v2"]:
            row = row_by_tag(enriched_aggregate_rows.get(study_name, []), tag)
            if row is None:
                continue
            record = {
                "city": PHASE19_STUDY_LABELS[study_name],
                "policy": row_display_label(row),
                "fn_pruning_rate": row.get("avg_fn_pruning_rate"),
                "displayed_eta_mae": row.get("avg_displayed_eta_mae"),
                "displayed_ivt_mae": row.get("avg_displayed_ivt_mae"),
                "acceptance_rate": row.get("acceptance_rate"),
                "consumer_surplus": row.get("consumer_surplus"),
            }
            diagnostic_records.append(record)
            diagnostic_table_rows.append([
                record["city"],
                record["policy"],
                format_metric(record["fn_pruning_rate"], digits=3),
                format_metric(record["displayed_eta_mae"], digits=1),
                format_metric(record["displayed_ivt_mae"], digits=1),
                format_metric(record["acceptance_rate"], digits=3),
                format_metric(record["consumer_surplus"], digits=3),
            ])
    write_tex_table(
        ARTIFACTS_DIR / "tables" / "city_policy_diagnostic_summary.tex",
        caption=(
            "City-level policy-conditioned displayed-offer diagnostics. "
            "Displayed ETA/IVT MAE and false-negative pruning are diagnostics on displayed offers rather than direct welfare outcomes; acceptance rate and consumer surplus are realized passenger-facing outcomes."
        ),
        label="tab:city_policy_diagnostic_summary",
        headers=[
            "City",
            "Policy",
            "FN pruning",
            "Displayed ETA MAE",
            "Displayed IVT MAE",
            "Acceptance rate",
            "Consumer surplus",
        ],
        rows=diagnostic_table_rows,
    )
    write_csv(ARTIFACTS_DIR / "tables" / "city_policy_diagnostic_summary.csv", diagnostic_records)



def benchmark_gate_status(full_row, no_filter_row):
    full_gate = bool(full_row.get("is_behavior_non_degenerate"))
    no_filter_gate = bool(no_filter_row.get("is_behavior_non_degenerate"))
    if full_gate and no_filter_gate:
        return "reference + policy pass"
    if full_gate:
        return "reference pass only"
    if no_filter_gate:
        return "policy pass only"
    return "degenerate"



def benchmark_bridge_use(study_name):
    if study_name == "rc_main_optout":
        return "mechanism only"
    if study_name == "austin_main":
        return "primary impact"
    if study_name == "seattle_main":
        return "supporting check"
    return "supporting"



def build_phase20_bridge_artifacts():
    bridge_records = []
    bridge_table_rows = []
    for study_name in ["rc_main_optout", "austin_main", "seattle_main"]:
        summary, _ = load_study_summary(study_name)
        if summary is None:
            continue
        manifest = load_manifest(study_name)
        rows = enrich_policy_rows(
            rows_from_summary(summary),
            study_name,
            study_meta=summary.get("study", {}),
            manifest=manifest,
        )
        full_row = row_by_tag(rows, "full_display")
        no_filter_row = row_by_tag(rows, "menu_optimization_v2")
        if full_row is None or no_filter_row is None:
            continue

        full_acceptance = full_row.get("acceptance_rate")
        no_filter_acceptance = no_filter_row.get("acceptance_rate")
        full_opt_out = full_row.get("opt_out_rate")
        gap_vs_full = no_filter_row.get("mean_net_profit_gap_vs_reference")
        full_net_profit = full_row.get("net_profit")
        gap_scale_pct = None
        if gap_vs_full is not None and full_net_profit not in {None, 0}:
            gap_scale_pct = 100.0 * float(gap_vs_full) / abs(float(full_net_profit))

        record = {
            "study": PHASE19_STUDY_LABELS.get(study_name, study_name),
            "role": infer_study_role(study_name, study_meta=summary.get("study", {}), manifest=manifest),
            "gate_status": benchmark_gate_status(full_row, no_filter_row),
            "full_acceptance_rate": full_acceptance,
            "no_filter_acceptance_rate": no_filter_acceptance,
            "full_opt_out_rate": full_opt_out,
            "no_filter_gap_vs_full": gap_vs_full,
            "gap_scale_pct": gap_scale_pct,
            "bridge_use": benchmark_bridge_use(study_name),
        }
        bridge_records.append(record)
        bridge_table_rows.append([
            record["study"],
            record["role"],
            record["gate_status"],
            format_metric(record["full_acceptance_rate"], digits=3),
            format_metric(record["no_filter_acceptance_rate"], digits=3),
            format_metric(record["full_opt_out_rate"], digits=3),
            format_metric(record["no_filter_gap_vs_full"], digits=2),
            format_metric(record["gap_scale_pct"], digits=2),
            record["bridge_use"],
        ])

    write_tex_table(
        ARTIFACTS_DIR / "tables" / "benchmark_bridge_summary.tex",
        caption=(
            "Benchmark-role bridge summary separating the degenerate RC mechanism benchmark from the city impact benchmarks. "
            "Gate status is evaluated on the full-display reference and the no-filter heuristic; reference-pass-only means the benchmark itself is behaviorally non-degenerate even if the no-filter policy falls outside the gate."
        ),
        label="tab:benchmark_bridge_summary",
        headers=[
            "Study",
            "Role",
            "Gate status",
            "Full acceptance",
            "No-filter acceptance",
            "Full opt-out",
            "No-filter gap",
            "Gap as % of |full|",
            "Bridge use",
        ],
        rows=bridge_table_rows,
    )
    write_csv(ARTIFACTS_DIR / "tables" / "benchmark_bridge_summary.csv", bridge_records)



def build_results_summary(snapshot):
    lines = [
        "# Results Summary",
        "",
        f"Built at: `{snapshot['built_at_utc']}`",
        "",
        f"Requested artifact scope: `{snapshot['requested_study']}`",
        "",
    ]

    if snapshot["kind"] == "suite":
        lines.append("This snapshot combines the latest resolved runs for the paper suite members listed below.")
        lines.append("")
        for member in snapshot.get("member_sources", []):
            lines.append(f"- `{member['study_name']}` from run `{member['run_id']}`")
        lines.append("")

    main_rows = snapshot.get("main_policy_rows", [])
    if main_rows:
        best_row = max(main_rows, key=lambda row: numeric_key(row, "net_profit"))
        menu_row = next((row for row in main_rows if row.get("variant_tag") == "menu_optimization"), None)
        lines.append("## Main Policy Comparison")
        lines.append("")
        lines.append(
            f"- Best mean net profit currently comes from `{best_row['variant_tag']}` with `{format_metric(best_row.get('net_profit'))}`."
        )
        if menu_row is not None:
            lines.append(
                f"- `menu_optimization` shows a mean net-profit gap vs full display of `{format_metric(menu_row.get('mean_net_profit_gap_vs_reference'))}`."
            )
        lines.append("")
    else:
        lines.extend(
            [
                "## Main Policy Comparison",
                "",
                "- No main-study results were found yet. Run the main study and rebuild artifacts.",
                "",
            ]
        )

    city_impact_rows = snapshot.get("city_impact_rows", [])
    if city_impact_rows:
        lines.append("## City Impact Summary")
        lines.append("")
        for row in city_impact_rows:
            if row.get("city") == "pooled":
                continue
            lines.append(
                f"- `{row['city']}`: `v2-full` profit gap `{format_metric(row.get('v2_vs_full_profit_gap'))}`, "
                f"`v2-v1` profit gap `{format_metric(row.get('v2_vs_v1_profit_gap'))}`, "
                f"acceptance delta `{format_metric(row.get('acceptance_delta_vs_full'))}`, "
                f"behavior gate `{row.get('behavior_gate_status', '--')}`."
            )
        pooled_row = next((row for row in city_impact_rows if row.get("city") == "pooled"), None)
        if pooled_row is not None:
            lines.append(
                f"- `pooled`: `v2-full` profit gap `{format_metric(pooled_row.get('v2_vs_full_profit_gap'))}`, "
                f"`v2-v1` profit gap `{format_metric(pooled_row.get('v2_vs_v1_profit_gap'))}`, "
                f"acceptance delta `{format_metric(pooled_row.get('acceptance_delta_vs_full'))}`, "
                f"verdict `{pooled_row.get('impact_verdict', '--')}`."
            )
        lines.append("")

    robustness_rows = snapshot.get("robustness_rows", [])
    if robustness_rows:
        best_k_row = max(robustness_rows, key=lambda row: numeric_key(row, "mean_net_profit_gap_vs_reference"))
        lines.append("## Menu-k Robustness")
        lines.append("")
        lines.append(
            f"- The best observed mean net-profit gap vs full display currently occurs at `k={best_k_row['menu_k']}` with `{format_metric(best_k_row.get('mean_net_profit_gap_vs_reference'))}`."
        )
        lines.append("")
    else:
        lines.extend(
            [
                "## Menu-k Robustness",
                "",
                "- No robustness results were found yet.",
                "",
            ]
        )

    ablation_rows = snapshot.get("ablation_rows", [])
    ablation_candidates = [row for row in ablation_rows if row.get("ablation_tag") not in {"", "baseline"}]
    if ablation_candidates:
        worst_row = min(ablation_candidates, key=lambda row: numeric_key(row, "mean_net_profit_gap_vs_baseline"))
        lines.append("## Menu Ablations")
        lines.append("")
        lines.append(
            f"- The largest drop versus baseline menu currently comes from `{worst_row['variant_tag']}` with `{format_metric(worst_row.get('mean_net_profit_gap_vs_baseline'))}`."
        )
        lines.append("")
    else:
        lines.extend(
            [
                "## Menu Ablations",
                "",
                "- No ablation results were found yet.",
                "",
            ]
        )

    lines.extend(
        [
            "## Traceability",
            "",
            "- Numeric tables and figures in `artifacts/` are generated from normalized study summaries under `outputs/studies/`.",
            "- Rebuild with `python scripts/build_artifacts.py --study rc_paper_v1` after rerunning any study.",
            "",
        ]
    )
    write_text(ARTIFACTS_DIR / "RESULTS_SUMMARY.md", "\n".join(lines))


_WORK2_METHOD_ORDER = [
    "oracle_menu",
    "cnn_setmenu_net",
    "cnn_menu",
    "cost_L",
    "nearest_L",
]

_WORK2_LEARNING_METHODS = {"cnn_menu", "cnn_setmenu_net", "oracle_menu"}


def _sort_work2_rows(rows):
    preferred = {tag: idx for idx, tag in enumerate(_WORK2_METHOD_ORDER)}
    return sorted(rows, key=lambda row: (preferred.get(row.get("variant_tag"), 99), row.get("variant_tag", "")))


def build_work2_results_artifacts(rows, prefix="work2_main"):
    """Generate Work 2 prediction accuracy, operational, and menu regret tables."""
    rows = _sort_work2_rows([row for row in rows if not row.get("is_reference")])
    if not rows:
        for name in ["prediction_accuracy", "operational", "menu_regret"]:
            render_placeholder_figure(
                ARTIFACTS_DIR / "figures" / f"{prefix}_{name}.png",
                f"Work 2 {name.replace('_', ' ')}",
                "Run the work2_main study to populate this figure.",
            )
        return

    # --- Prediction accuracy table ---
    pred_table_rows = []
    for row in rows:
        tag = row.get("variant_tag", "")
        if tag in _WORK2_LEARNING_METHODS:
            pred_table_rows.append([
                row["display_label"],
                format_metric(row.get("cost_pred_mae")),
                format_metric(row.get("cost_pred_rmse")),
                format_metric(row.get("spearman_cost_ranking")),
                format_metric(row.get("top_L_overlap")),
                format_metric(row.get("ndcg_at_L")),
            ])
        else:
            pred_table_rows.append([
                row["display_label"],
                "--", "--", "--", "--", "--",
            ])
    write_tex_table(
        ARTIFACTS_DIR / "tables" / f"{prefix}_prediction_accuracy.tex",
        caption="Cost prediction accuracy across methods on the RC benchmark.",
        label=f"tab:{prefix}_prediction_accuracy",
        headers=[
            "Method",
            "Cost MAE",
            "Cost RMSE",
            "Spearman $\\rho$",
            "Top-L Overlap",
            "NDCG@L",
        ],
        rows=pred_table_rows,
    )

    # --- Operational + passenger experience table ---
    op_table_rows = []
    for row in rows:
        op_table_rows.append([
            row["display_label"],
            format_metric(row.get("net_profit")),
            format_metric(row.get("total_cost")),
            format_metric(row.get("acceptance_rate")),
            format_metric(row.get("opt_out_rate")),
            format_metric(row.get("home_pickup_share")),
            format_metric(row.get("avg_walk_distance")),
            format_metric(row.get("avg_in_vehicle_time")),
            format_metric(row.get("avg_chosen_price")),
        ])
    write_tex_table(
        ARTIFACTS_DIR / "tables" / f"{prefix}_operational.tex",
        caption="Operational and passenger experience metrics across methods on the RC benchmark.",
        label=f"tab:{prefix}_operational",
        headers=[
            "Method",
            "Net Profit",
            "Total Cost",
            "Accept. Rate",
            "Opt-out Rate",
            "Home Share",
            "Avg Walk",
            "Avg IVT",
            "Avg Price",
        ],
        rows=op_table_rows,
    )

    # --- Menu regret table ---
    regret_table_rows = []
    for row in rows:
        regret_table_rows.append([
            row["display_label"],
            format_metric(row.get("menu_regret")),
            format_metric(row.get("average_menu_size")),
            format_metric(row.get("avg_meeting_point_count_per_menu")),
        ])
    write_tex_table(
        ARTIFACTS_DIR / "tables" / f"{prefix}_menu_regret.tex",
        caption="Menu selection quality across methods on the RC benchmark.",
        label=f"tab:{prefix}_menu_regret",
        headers=[
            "Method",
            "Menu Regret",
            "Avg Menu Size",
            "MP Count",
        ],
        rows=regret_table_rows,
    )

    # --- Net profit comparison figure ---
    labels = [row["display_label"] for row in rows]
    profits = [float(row.get("net_profit", 0.0) or 0.0) for row in rows]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(labels, profits, color="#4C78A8")
    ax.set_ylabel("Mean net profit")
    ax.set_title("Work 2: 6-Method Net Profit Comparison")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    fig.savefig(ARTIFACTS_DIR / "figures" / f"{prefix}_net_profit.png", dpi=200)
    plt.close(fig)


def build_single_study_artifacts(study_summary, study_name, manifest=None):
    rows = enrich_policy_rows(
        rows_from_summary(study_summary),
        study_name,
        study_meta=study_summary.get("study", {}),
        manifest=manifest,
    )
    headline_variants = resolve_headline_variants(study_name, study_meta=study_summary.get("study", {}), manifest=manifest)
    if study_name == "phase29_exact_greedy_gap":
        build_exact_greedy_artifacts(rows, prefix=study_name)
    elif study_name == "phase30_robust_filtering":
        build_robust_filtering_artifacts(rows, prefix=study_name)
    elif study_name == "phase31_uptake_menu_value":
        build_uptake_menu_value_artifacts(rows, prefix=study_name)
    elif study_name == "phase32_operational_baselines":
        build_operational_baselines_artifacts(rows, prefix=study_name)
        build_operational_baselines_artifacts(rows, prefix="operational_baselines")
    elif study_name in {"work2_main", "smoke_work2_main"}:
        build_work2_results_artifacts(rows, prefix=study_name)
    elif study_summary["study"]["type"] == "policy_compare":
        title = study_summary["study"].get("title", study_name.replace("_", " "))
        caption = title if "comparison" in title.lower() else f"{title} policy comparison."
        build_main_policy_artifacts(
            rows,
            prefix=study_name,
            caption=caption,
            plot_title=title,
            headline_variants=headline_variants,
        )
        if study_name == "rc_main_optout":
            build_welfare_artifacts(
                rows,
                prefix="rc_main_optout_welfare",
                caption="Passenger welfare and pricing metrics by policy on the RC outside-option study.",
                headline_variants=headline_variants,
            )
            build_profit_decomposition_artifacts(rows)
    elif study_summary["study"]["type"] == "menu_k_robustness":
        build_robustness_artifacts(rows, prefix=study_name)
    elif study_summary["study"]["type"] == "ablation":
        build_ablation_artifacts(rows, prefix=study_name)
    return rows


def build_suite_artifacts(bundle):
    if bundle["manifest"]["name"] == "phase31_uptake_menu_value":
        combined_rows = []
        for study_name, summary, _ in bundle["member_summaries"]:
            combined_rows.extend(
                enrich_policy_rows(
                    rows_from_summary(summary),
                    study_name,
                    study_meta=(summary.get("study", {}) if summary else {}),
                    manifest=None,
                )
            )
        build_uptake_menu_value_artifacts(combined_rows, prefix="phase31_uptake_menu_value")
        snapshot = {
            "schema_version": 1,
            "built_at_utc": utc_now_iso(),
            "requested_study": "phase31_uptake_menu_value",
            "kind": "suite",
            "member_sources": [
                {
                    "study_name": study_name,
                    "run_id": summary["run_metadata"]["run_id"],
                    "study_type": summary["study"]["type"],
                }
                for study_name, summary, _ in bundle["member_summaries"]
            ],
            "uptake_rows": combined_rows,
        }
        save_json(ARTIFACTS_DIR / "results_snapshot" / "phase31_uptake_menu_value_summary.json", snapshot)
        write_csv(ARTIFACTS_DIR / "results_snapshot" / "phase31_uptake_menu_value_rows.csv", combined_rows)
        return snapshot

    if bundle["manifest"]["name"] == "phase34_outside_option_scan":
        combined_rows = []
        for study_name, summary, _ in bundle["member_summaries"]:
            combined_rows.extend(
                enrich_policy_rows(
                    rows_from_summary(summary),
                    study_name,
                    study_meta=(summary.get("study", {}) if summary else {}),
                    manifest=None,
                )
            )
        build_outside_option_scan_artifacts(combined_rows, prefix="outside_option_scan")
        snapshot = {
            "schema_version": 1,
            "built_at_utc": utc_now_iso(),
            "requested_study": "phase34_outside_option_scan",
            "kind": "suite",
            "member_sources": [
                {
                    "study_name": study_name,
                    "run_id": summary["run_metadata"]["run_id"],
                    "study_type": summary["study"]["type"],
                }
                for study_name, summary, _ in bundle["member_summaries"]
            ],
            "outside_option_rows": combined_rows,
        }
        save_json(ARTIFACTS_DIR / "results_snapshot" / "outside_option_scan_summary.json", snapshot)
        write_csv(ARTIFACTS_DIR / "results_snapshot" / "outside_option_scan_rows.csv", combined_rows)
        return snapshot

    member_map = study_map(bundle["member_summaries"])
    main_summary = member_map.get("rc_main")
    robustness_summary = member_map.get("rc_menu_k_robustness")
    ablation_summary = member_map.get("rc_menu_ablation")
    ablation_v2_summary = member_map.get("rc_menu_ablation_v2")

    main_rows = enrich_policy_rows(
        rows_from_summary(main_summary),
        "rc_main",
        study_meta=(main_summary.get("study", {}) if main_summary else {}),
        manifest=bundle["manifest"],
    )
    robustness_rows = enrich_policy_rows(
        rows_from_summary(robustness_summary),
        "rc_menu_k_robustness",
        study_meta=(robustness_summary.get("study", {}) if robustness_summary else {}),
        manifest=bundle["manifest"],
    )
    ablation_rows = enrich_policy_rows(
        rows_from_summary(ablation_summary),
        "rc_menu_ablation",
        study_meta=(ablation_summary.get("study", {}) if ablation_summary else {}),
        manifest=bundle["manifest"],
    )
    ablation_v2_rows = enrich_policy_rows(
        rows_from_summary(ablation_v2_summary),
        "rc_menu_ablation_v2",
        study_meta=(ablation_v2_summary.get("study", {}) if ablation_v2_summary else {}),
        manifest=bundle["manifest"],
    )

    build_main_policy_artifacts(main_rows, prefix="main_policy")
    build_robustness_artifacts(robustness_rows, prefix="robustness_menu_k")
    build_ablation_artifacts(ablation_rows, prefix="ablation")
    build_ablation_artifacts(ablation_v2_rows, prefix="ablation_v2")
    build_welfare_artifacts(main_rows, prefix="welfare")

    snapshot = {
        "schema_version": 1,
        "built_at_utc": utc_now_iso(),
        "requested_study": bundle["manifest"]["name"],
        "kind": "suite",
        "member_sources": [
            {
                "study_name": study_name,
                "run_id": summary["run_metadata"]["run_id"],
                "study_type": summary["study"]["type"],
            }
            for study_name, summary, _ in bundle["member_summaries"]
        ],
        "main_policy_rows": main_rows,
        "robustness_rows": robustness_rows,
        "ablation_rows": ablation_rows,
        "ablation_v2_rows": ablation_v2_rows,
        "city_impact_rows": [],
    }
    save_json(ARTIFACTS_DIR / "results_snapshot" / f"{bundle['manifest']['name']}_summary.json", snapshot)
    combined_rows = main_rows + robustness_rows + ablation_rows + ablation_v2_rows
    write_csv(ARTIFACTS_DIR / "results_snapshot" / f"{bundle['manifest']['name']}_rows.csv", combined_rows)
    build_results_summary(snapshot)
    return snapshot


def build_generic_artifacts(bundle):
    summary = bundle["member_summaries"][0][1] if bundle["member_summaries"] else None
    study_name = bundle["manifest"]["name"]
    rows = []
    if summary is not None:
        rows = build_single_study_artifacts(summary, study_name, manifest=bundle["manifest"])
    elif study_name == "phase29_exact_greedy_gap":
        build_exact_greedy_artifacts([], prefix=study_name)
    elif study_name == "phase30_robust_filtering":
        build_robust_filtering_artifacts([], prefix=study_name)
    elif study_name == "phase31_uptake_menu_value":
        build_uptake_menu_value_artifacts([], prefix=study_name)
    city_impact_rows = []
    if study_name in {"austin_main", "seattle_main"}:
        austin_summary = summary if study_name == "austin_main" else load_study_summary("austin_main")[0]
        seattle_summary = summary if study_name == "seattle_main" else load_study_summary("seattle_main")[0]
        city_impact_rows = build_city_impact_artifacts(austin_summary=austin_summary, seattle_summary=seattle_summary)
    snapshot = {
        "schema_version": 1,
        "built_at_utc": utc_now_iso(),
        "requested_study": study_name,
        "kind": "study",
        "member_sources": [] if summary is None else [
            {
                "study_name": study_name,
                "run_id": summary["run_metadata"]["run_id"],
                "study_type": summary["study"]["type"],
            }
        ],
        "main_policy_rows": rows if summary and summary["study"]["type"] == "policy_compare" else [],
        "robustness_rows": rows if summary and summary["study"]["type"] == "menu_k_robustness" else [],
        "ablation_rows": rows if summary and summary["study"]["type"] == "ablation" else [],
        "city_impact_rows": city_impact_rows,
    }
    save_json(ARTIFACTS_DIR / "results_snapshot" / f"{study_name}_summary.json", snapshot)
    write_csv(ARTIFACTS_DIR / "results_snapshot" / f"{study_name}_rows.csv", rows)
    build_results_summary(snapshot)
    return snapshot


def build_filter_validity_artifacts():
    """Build filter-validity table with bias (mean signed error) diagnostics.

    Reads filter_validity.json (produced by extract_phase28_results.py) and
    rebuilds the LaTeX table with ETA Bias and IVT Bias columns.
    """
    fv_path = ROOT / "outputs" / "phase28" / "filter_validity.json"
    if not fv_path.exists():
        return
    fv_data = json.loads(fv_path.read_text(encoding="utf-8"))
    rows = fv_data.get("rows", [])
    if not rows:
        return

    table_rows = []
    for row in rows:
        table_rows.append([
            str(row.get("label", "")),
            format_metric(row.get("fn_pruning_rate"), digits=3),
            format_metric(row.get("displayed_eta_bias"), digits=1),
            format_metric(row.get("displayed_eta_mae"), digits=1),
            format_metric(row.get("selected_eta_mae"), digits=1),
            format_metric(row.get("displayed_ivt_bias"), digits=1),
            format_metric(row.get("displayed_ivt_mae"), digits=1),
            format_metric(row.get("selected_ivt_mae"), digits=1),
            format_metric(row.get("acceptance_rate"), digits=3),
            format_metric(row.get("mean_net_profit_gap"), digits=2),
        ])

    write_tex_table(
        ARTIFACTS_DIR / "tables" / "filter_validity_summary.tex",
        caption=(
            "Blended-filter validity diagnostics on the RC mechanism benchmark. "
            "Bias is mean signed error (predicted $-$ actual); positive values indicate over-prediction. "
            "Displayed-offer errors are computed over all displayed non-home offers, "
            "while selected-offer errors are weakly identified in the low-uptake RC benchmark "
            "because few non-home offers are accepted."
        ),
        label="tab:filter_validity_summary",
        headers=[
            "ETA/filter signal",
            "FN pruning",
            "ETA Bias",
            "ETA MAE",
            "Sel. ETA MAE",
            "IVT Bias",
            "IVT MAE",
            "Sel. IVT MAE",
            "Acceptance",
            "Gap vs full",
        ],
        rows=table_rows,
    )
    write_csv(ARTIFACTS_DIR / "tables" / "filter_validity_summary.csv", rows)


def build_operational_baselines_artifacts(rows, prefix="operational_baselines"):
    """Build operational-baseline comparison table.

    Renders a LaTeX table comparing dispatch heuristic baselines against
    full display and the strict-filter heuristic.
    """
    order = {
        "full_display": 0,
        "offer_all_feasible_bundles": 0,
        "strict_filter": 1,
        "menu_optimization": 1,
        "insertion_cost_greedy": 2,
        "min_lateness": 3,
        "random_top_k": 4,
    }
    rows = sorted(rows, key=lambda row: (order.get(row.get("variant_tag"), 99), row.get("variant_tag", "")))
    table_rows = [
        [
            row.get("display_label", row.get("variant_tag", "")),
            format_metric(row.get("net_profit")),
            format_metric(row.get("mean_net_profit_gap_vs_reference")),
            format_metric(row.get("net_profit_win_rate_vs_reference")),
            format_metric(row.get("acceptance_rate")),
            format_metric(row.get("average_menu_size")),
            format_metric(row.get("avg_meeting_point_count_per_menu")),
        ]
        for row in rows
    ]
    write_tex_table(
        ARTIFACTS_DIR / "tables" / f"{prefix}_summary.tex",
        caption=(
            "Operational baseline comparison on the RC low-uptake benchmark. "
            "Insertion-cost greedy, minimum-lateness ranking, and random-top-k provide "
            "dispatch-floor and greedy-policy context for the menu-optimization heuristic."
        ),
        label=f"tab:{prefix}",
        headers=[
            "Policy",
            "Mean net profit",
            "Gap vs full",
            "Win rate vs full",
            "Acceptance",
            "Menu size",
            "Meeting-point count",
        ],
        rows=table_rows,
    )
    write_csv(ARTIFACTS_DIR / "tables" / f"{prefix}_summary.csv", rows)


def build_profit_decomposition_artifacts(rows, prefix="profit_decomposition"):
    """Generate LaTeX profit-decomposition table from aggregate variant summary.

    Columns: policy, fare revenue, discount cost, travel cost, service cost,
    failure cost, net profit, accepted requests.
    """
    rows, secondary_rows = split_headline_rows(
        rows, ["full_display", "menu_optimization", "menu_optimization_v2"]
    )
    all_rows = list(sort_main_rows(rows))
    if secondary_rows:
        all_rows.extend(sort_main_rows(secondary_rows))

    table_rows = []
    for row in all_rows:
        served = row.get("served_customers")
        if served is not None:
            served = int(float(served))
        table_rows.append([
            row["display_label"],
            format_metric(row.get("charge_revenue"), digits=3),
            format_metric(row.get("discount_cost"), digits=3),
            format_metric(row.get("travel_cost"), digits=3),
            format_metric(row.get("service_cost"), digits=3),
            format_metric(row.get("failure_cost"), digits=3),
            format_metric(row.get("net_profit"), digits=3),
            str(served) if served is not None else "--",
        ])

    write_tex_table(
        ARTIFACTS_DIR / "tables" / f"{prefix}_summary.tex",
        caption=(
            "Profit decomposition by policy in the RC outside-option study. "
            "All values are split-level means over six evaluation pairs."
        ),
        label="tab:profit_decomposition",
        headers=[
            "Policy",
            "Fare revenue",
            "Discount cost",
            "Travel cost",
            "Service cost",
            "Failure cost",
            "Net profit",
            "Accepted reqs",
        ],
        rows=table_rows,
    )
    write_csv(ARTIFACTS_DIR / "tables" / f"{prefix}_summary.csv", all_rows)


def main():
    parser = argparse.ArgumentParser(description="Build lightweight paper artifacts from normalized study summaries.")
    parser.add_argument("--study", required=True, help="Study or suite name to materialize under artifacts/.")
    args = parser.parse_args()

    ensure_artifact_dirs()
    bundle = pick_summary_bundle(args.study)
    if bundle["kind"] == "suite":
        snapshot = build_suite_artifacts(bundle)
    else:
        snapshot = build_generic_artifacts(bundle)

    build_phase19_support_artifacts()
    build_phase20_bridge_artifacts()
    build_filter_validity_artifacts()

    print("Built artifacts for:", snapshot["requested_study"])
    print("Snapshot file:", ARTIFACTS_DIR / "results_snapshot" / f"{snapshot['requested_study']}_summary.json")
    print("Results summary:", ARTIFACTS_DIR / "RESULTS_SUMMARY.md")


if __name__ == "__main__":
    main()
