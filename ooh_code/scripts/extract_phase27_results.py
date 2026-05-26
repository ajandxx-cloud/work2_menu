"""Extract Phase 27 MNL-sensitivity evidence.

The script first looks for completed current-pipeline sensitivity studies. If
they have not been run yet, it writes a scoped current-evidence summary from the
saved v1.6 artifacts and marks the missing studies explicitly. This keeps the
manuscript evidence hierarchy honest while preserving a reproducible command for
the heavier sensitivity runs.

Usage:
    python scripts/extract_phase27_results.py
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Src.research_pipeline import load_study_summary, write_csv, write_text

PHASE27_OUT = ROOT / "outputs" / "phase27"
TABLES_OUT = ROOT / "artifacts" / "tables"

SENSITIVITY_STUDIES = {
    "low": "phase27_mnl_sensitivity_low",
    "medium": "phase27_mnl_sensitivity_medium",
    "higher": "phase27_mnl_sensitivity_high",
}


def _fmt(value, digits=3):
    if value is None:
        return "--"
    return f"{float(value):.{digits}f}"


def _escape(text):
    return str(text).replace("&", r"\&").replace("%", r"\%").replace("_", r"\_")


def _row_by_tag(rows, tag):
    for row in rows:
        if row.get("variant_tag") == tag:
            return row
    return None


def _payload_from_row(row, label=None):
    if row is None:
        return None
    return {
        "label": label or row.get("variant_label", row.get("variant_tag")),
        "net_profit": _float(row.get("net_profit")),
        "mean_net_profit_gap_vs_reference": _float(row.get("mean_net_profit_gap_vs_reference")),
        "net_profit_win_rate_vs_reference": _float(row.get("net_profit_win_rate_vs_reference")),
        "acceptance_rate": _float(row.get("acceptance_rate")),
        "opt_out_rate": _float(row.get("opt_out_rate")),
        "non_home_acceptance_rate": _float(row.get("non_home_acceptance_rate")),
        "consumer_surplus": _float(row.get("consumer_surplus")),
        "price_at_floor_fraction": _float(row.get("price_at_floor_fraction")),
        "price_at_ceil_fraction": _float(row.get("price_at_ceil_fraction")),
    }


def _float(value):
    if value is None:
        return None
    return float(value)


def _load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _study_regime_payload(regime, study_name):
    summary, _ = load_study_summary(study_name)
    if summary is None:
        return None
    rows = summary.get("aggregate_variant_summary", [])
    payload = {
        "regime": regime,
        "source": study_name,
        "status": "completed_current_pipeline",
        "run_id": summary.get("run_metadata", {}).get("run_id"),
        "variants": {
            "full_display": _payload_from_row(_row_by_tag(rows, "full_display"), "full display"),
            "strict_filter": _payload_from_row(_row_by_tag(rows, "strict_filter"), "strict-filter heuristic"),
            "no_filter": _payload_from_row(_row_by_tag(rows, "no_filter"), "no-filter heuristic"),
            "flat_markdown": _payload_from_row(_row_by_tag(rows, "flat_markdown"), "flat markdown pricing"),
        },
    }
    return payload


def _fallback_payload():
    phase22 = _load_json(ROOT / "outputs" / "phase22" / "phase22_summary.json")
    phase23 = _load_json(ROOT / "outputs" / "phase23" / "pricing_baselines.json")
    low_eta = phase22["eta_compare"]["variants"]["deployed"]
    high_uptake = phase22["uptake_calibration"]
    pricing = phase23["variants"]
    return {
        "low": {
            "regime": "low",
            "source": "phase22_eta_compare:deployed",
            "status": "current_evidence_baseline",
            "variants": {
                "strict_filter": {
                    "label": "strict-filter heuristic",
                    "mean_net_profit_gap_vs_reference": low_eta["mean_net_profit_gap"],
                    "net_profit_win_rate_vs_reference": low_eta["win_rate"],
                    "acceptance_rate": low_eta["acceptance_rate"],
                    "opt_out_rate": low_eta["opt_out_rate"],
                    "non_home_acceptance_rate": low_eta["non_home_acceptance_rate"],
                    "consumer_surplus": low_eta["consumer_surplus"],
                }
            },
        },
        "higher": {
            "regime": "higher",
            "source": "phase22_uptake_calibration + phase23_pricing_baselines",
            "status": "current_evidence_baseline",
            "variants": {
                "full_display": {
                    "label": "full display",
                    **high_uptake["full_display"],
                },
                "strict_filter": {
                    "label": "strict-filter heuristic",
                    **high_uptake["menu_optimization"],
                },
                "lambertw": pricing["lambertw"],
                "cost_plus": pricing["cost_plus"],
                "flat_markdown": pricing["flat_markdown"],
            },
        },
    }


def _flatten_records(regimes):
    records = []
    for regime, payload in regimes.items():
        for tag, row in payload.get("variants", {}).items():
            if row is None:
                continue
            records.append({
                "regime": regime,
                "source": payload.get("source", ""),
                "status": payload.get("status", ""),
                "variant": tag,
                "label": row.get("label", tag),
                "gap_vs_full": row.get("mean_net_profit_gap_vs_reference"),
                "win_rate_vs_full": row.get("net_profit_win_rate_vs_reference"),
                "acceptance_rate": row.get("acceptance_rate"),
                "opt_out_rate": row.get("opt_out_rate"),
                "non_home_acceptance_rate": row.get("non_home_acceptance_rate"),
                "consumer_surplus": row.get("consumer_surplus"),
                "floor_hit_rate": row.get("price_at_floor_fraction"),
                "ceil_hit_rate": row.get("price_at_ceil_fraction"),
            })
    return records


def _write_table(records):
    status_labels = {
        "current_evidence_baseline": "current evidence",
        "completed_current_pipeline": "completed sensitivity",
    }
    rows = []
    for rec in records:
        if rec["variant"] == "full_display":
            continue
        rows.append([
            rec["regime"],
            rec["label"],
            status_labels.get(rec["status"], rec["status"]),
            _fmt(rec["gap_vs_full"], 2),
            _fmt(rec["acceptance_rate"], 3),
            _fmt(rec["non_home_acceptance_rate"], 3),
            _fmt(rec["consumer_surplus"], 3),
            _fmt(rec["floor_hit_rate"], 3),
        ])
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\small",
        r"\setlength{\tabcolsep}{3pt}",
        r"\caption{MNL-regime sensitivity summary. Rows marked current-evidence baseline are extracted from completed v1.6 outputs; completed-current-pipeline rows are produced by the Phase 27 sensitivity manifests. Higher-uptake rows should be read as stress-test evidence rather than externally validated demand calibration.}",
        r"\label{tab:mnl_sensitivity_summary}",
        r"\resizebox{\linewidth}{!}{%",
        r"\begin{tabular}{@{}llrrrrrr@{}}",
        r"\hline",
        r"Regime & Policy/pricing rule & Evidence status & Gap vs full & Acceptance & Non-home acc. & Surplus & Floor hit \\",
        r"\hline",
    ]
    for row in rows:
        lines.append(" & ".join(_escape(cell) for cell in row) + r" \\")
    lines.extend([r"\hline", r"\end{tabular}", r"}", r"\end{table}", ""])
    write_text(TABLES_OUT / "mnl_sensitivity_summary.tex", "\n".join(lines))


def main():
    os.makedirs(PHASE27_OUT, exist_ok=True)
    os.makedirs(TABLES_OUT, exist_ok=True)

    regimes = {}
    missing = []
    for regime, study_name in SENSITIVITY_STUDIES.items():
        payload = _study_regime_payload(regime, study_name)
        if payload is None:
            missing.append(study_name)
        else:
            regimes[regime] = payload

    if missing:
        fallback = _fallback_payload()
        for regime, payload in fallback.items():
            regimes.setdefault(regime, payload)

    records = _flatten_records(regimes)
    result = {
        "schema_version": 1,
        "status": "partial_current_pipeline" if missing else "completed_current_pipeline",
        "missing_studies": missing,
        "reproducible_suite": "phase27_mnl_sensitivity",
        "regimes": regimes,
        "records": records,
        "interpretation": {
            "demand_calibration": "literature-bounded simulator sensitivity, not external demand estimation",
            "higher_uptake_role": "stress-test behavioral regime",
            "rank_stability": "Only completed-current-pipeline regimes should be used for rank-stability claims.",
        },
    }
    out_path = PHASE27_OUT / "mnl_sensitivity.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
    write_csv(TABLES_OUT / "mnl_sensitivity_summary.csv", records)
    _write_table(records)
    print(f"Saved: {out_path}")
    print(f"Saved: {TABLES_OUT / 'mnl_sensitivity_summary.tex'}")


if __name__ == "__main__":
    main()
