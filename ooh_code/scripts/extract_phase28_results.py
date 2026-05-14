"""Extract Phase 28 predictor/filter-validity diagnostics.

Usage:
    python scripts/extract_phase28_results.py
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Src.research_pipeline import write_csv, write_text

PHASE28_OUT = ROOT / "outputs" / "phase28"
TABLES_OUT = ROOT / "artifacts" / "tables"


def _fmt(value, digits=3):
    if value is None:
        return "--"
    return f"{float(value):.{digits}f}"


def _escape(text):
    return str(text).replace("&", r"\&").replace("%", r"\%").replace("_", r"\_")


def _load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _diagnostic_rows():
    phase22 = _load_json(ROOT / "outputs" / "phase22" / "eta_compare.json")
    rows = []
    for tag, payload in phase22["variants"].items():
        rows.append({
            "eta_variant": tag,
            "label": payload["label"],
            "fn_pruning_rate": payload.get("avg_fn_pruning_rate"),
            "displayed_eta_bias": payload.get("avg_displayed_eta_bias"),
            "displayed_eta_mae": payload.get("avg_displayed_eta_mae"),
            "displayed_eta_p50": payload.get("displayed_eta_p50"),
            "displayed_eta_p90": payload.get("displayed_eta_p90"),
            "displayed_eta_p95": payload.get("displayed_eta_p95"),
            "selected_eta_mae": payload.get("avg_selected_eta_mae"),
            "displayed_ivt_bias": payload.get("avg_displayed_ivt_bias"),
            "displayed_ivt_mae": payload.get("avg_displayed_ivt_mae"),
            "displayed_ivt_p50": payload.get("displayed_ivt_p50"),
            "displayed_ivt_p90": payload.get("displayed_ivt_p90"),
            "displayed_ivt_p95": payload.get("displayed_ivt_p95"),
            "selected_ivt_mae": payload.get("avg_selected_ivt_mae"),
            "acceptance_rate": payload.get("acceptance_rate"),
            "non_home_acceptance_rate": payload.get("non_home_acceptance_rate"),
            "mean_net_profit_gap": payload.get("mean_net_profit_gap"),
            "fn_pruned_near": payload.get("avg_fn_pruned_near"),
            "fn_pruned_mid": payload.get("avg_fn_pruned_mid"),
            "fn_pruned_far": payload.get("avg_fn_pruned_far"),
        })
    return rows


def _write_table(rows):
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{1.8pt}",
        r"\caption{Filter-validity diagnostics on the RC mechanism benchmark. Bias is mean signed error (predicted $-$ actual); positive values indicate over-prediction. P50/P90/P95 are quantiles of displayed-offer absolute errors (seconds). FN breakdown shows false-negative pruning by meeting-point distance band: near ($<$500\,m), mid (500--1500\,m), far ($>$1500\,m).}",
        r"\label{tab:filter_validity_summary}",
        r"\resizebox{\linewidth}{!}{%",
        r"\begin{tabular}{@{}lrrrrrrrrrrrrrrr@{}}",
        r"\hline",
        r"Signal & FN & ETA & ETA & ETA & ETA & ETA & IVT & IVT & IVT & IVT & IVT & FN & FN & FN & Gap \\",
        r" & rate & Bias & MAE & P50 & P90 & P95 & Bias & MAE & P50 & P90 & P95 & Near & Mid & Far & vs full \\",
        r"\hline",
    ]
    for row in rows:
        lines.append(
            " & ".join([
                _escape(row["label"]),
                _fmt(row["fn_pruning_rate"], 3),
                _fmt(row["displayed_eta_bias"], 0),
                _fmt(row["displayed_eta_mae"], 0),
                _fmt(row["displayed_eta_p50"], 0),
                _fmt(row["displayed_eta_p90"], 0),
                _fmt(row["displayed_eta_p95"], 0),
                _fmt(row["displayed_ivt_bias"], 0),
                _fmt(row["displayed_ivt_mae"], 0),
                _fmt(row["displayed_ivt_p50"], 0),
                _fmt(row["displayed_ivt_p90"], 0),
                _fmt(row["displayed_ivt_p95"], 0),
                _fmt(row["fn_pruned_near"], 3),
                _fmt(row["fn_pruned_mid"], 3),
                _fmt(row["fn_pruned_far"], 3),
                _fmt(row["mean_net_profit_gap"], 2),
            ]) + r" \\"
        )
    lines.extend([r"\hline", r"\end{tabular}", r"}", r"\end{table}", ""])
    write_text(TABLES_OUT / "filter_validity_summary.tex", "\n".join(lines))


def main():
    os.makedirs(PHASE28_OUT, exist_ok=True)
    os.makedirs(TABLES_OUT, exist_ok=True)
    rows = _diagnostic_rows()
    result = {
        "schema_version": 2,
        "source": "outputs/phase22/eta_compare.json",
        "rows": rows,
        "interpretation": {
            "displayed_errors": "policy-conditioned diagnostics over displayed non-home offers",
            "selected_errors": "reported but weakly identified when non-home uptake is close to zero",
            "confusion_proxy": "avg_fn_pruning_rate is the available false-negative pruning proxy over feasible non-home bundles",
            "bias_definition": "displayed_eta_bias and displayed_ivt_bias are mean signed errors (predicted - actual); positive means over-prediction",
        },
    }
    out_path = PHASE28_OUT / "filter_validity.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
    write_csv(TABLES_OUT / "filter_validity_summary.csv", rows)
    _write_table(rows)
    print(f"Saved: {out_path}")
    print(f"Saved: {TABLES_OUT / 'filter_validity_summary.tex'}")


if __name__ == "__main__":
    main()
