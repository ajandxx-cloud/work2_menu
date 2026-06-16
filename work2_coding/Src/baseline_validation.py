"""Phase 8 baseline validation gate and report helpers."""

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

from Src.artifact_status import classify_artifact, write_json
from Src.experiment_contracts import load_manifest, manifest_hash
from Src.paired_replay import build_normalized_row, resolve_paired_settings


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
DEFAULT_STUDY_NAME = "phase8_baseline_validation"
DEFAULT_OUTPUT_ROOT = ROOT / "outputs" / "phase8_baseline_validation"
MAIN_BASELINE_TAGS = ("mainline_optimized_mw", "phase8_static_flat_markdown")
EXPECTED_SPLIT_COUNT = 5
REPORT_JSON = "PHASE8_BASELINE_VALIDATION.json"
REPORT_MD = "PHASE8_BASELINE_VALIDATION.md"
RERUN_COMMAND = (
    "cd work2_coding && python scripts/run_study.py --study phase8_baseline_validation "
    "--execute --output-root outputs/studies"
)


def utc_now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _rel(path):
    try:
        return str(Path(path).resolve().relative_to(REPO_ROOT.resolve())).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _blocker(reason, minimal_fix, evidence_location, code, rerun_command=RERUN_COMMAND, **extra):
    item = {
        "code": code,
        "severity": "blocking",
        "reason": reason,
        "minimal_fix": minimal_fix,
        "rerun_command": rerun_command,
        "evidence_location": evidence_location,
    }
    item.update(extra)
    return item


def _required_split_ids(manifest=None, rows=None):
    if manifest:
        return [split["split_id"] for split in manifest.get("splits", [])]
    row_ids = sorted({row.get("split_id") for row in (rows or []) if row.get("split_id")})
    return row_ids


def _is_main_row(row):
    return row.get("policy_tag") in MAIN_BASELINE_TAGS


def _require_field(row, field, failures):
    if row.get(field) in (None, ""):
        failures.append(
            _blocker(
                f"row is missing required field {field}",
                f"Regenerate Phase 8 rows so normalized-row-v2 includes {field}.",
                "work2_coding/Src/paired_replay.py",
                "missing_" + field,
                split_id=row.get("split_id"),
                policy_tag=row.get("policy_tag"),
            )
        )


def _check_row_status(row, failures):
    if row.get("status") != "completed" or row.get("execution_status") != "completed":
        failures.append(
            _blocker(
                "main baseline row is not completed actual replay",
                "Fix the replay failure and rerun Phase 8 baseline validation.",
                row.get("manifest_path") or "work2_coding/Experiments/studies/phase8_baseline_validation.yaml",
                "row_not_completed",
                split_id=row.get("split_id"),
                policy_tag=row.get("policy_tag"),
                row_status=row.get("status"),
                execution_status=row.get("execution_status"),
            )
        )
    if row.get("placeholder_only"):
        failures.append(
            _blocker(
                "main baseline row is placeholder-only or contract-only",
                "Run actual replay; contract-only rows are insufficient for Phase 8.",
                row.get("manifest_path") or "work2_coding/Experiments/studies/phase8_baseline_validation.yaml",
                "placeholder_row",
                split_id=row.get("split_id"),
                policy_tag=row.get("policy_tag"),
            )
        )


def _check_checkpoint(row, failures):
    if row.get("checkpoint_required") and row.get("checkpoint_load_status") != "loaded":
        failures.append(
            _blocker(
                "main baseline row does not report loaded checkpoint status",
                "Restore the shared checkpoint or repair checkpoint loading before rerunning Phase 8.",
                row.get("checkpoint_path") or "work2_coding/outputs/shared_training/",
                "checkpoint_not_loaded",
                split_id=row.get("split_id"),
                policy_tag=row.get("policy_tag"),
                checkpoint_load_status=row.get("checkpoint_load_status"),
            )
        )
    if row.get("checkpoint_required"):
        _require_field(row, "checkpoint_path", failures)
        _require_field(row, "checkpoint_hash", failures)


def _check_accounting(row, failures):
    counts = [
        row.get("count_accepted_home"),
        row.get("count_accepted_meeting_point"),
        row.get("count_opted_out"),
    ]
    if any(value is None for value in counts):
        failures.append(
            _blocker(
                "main baseline row is missing opt-out/home/meeting-point counts",
                "Regenerate rows with row-v2 accounting fields populated.",
                "work2_coding/Src/paired_replay.py",
                "missing_accounting_counts",
                split_id=row.get("split_id"),
                policy_tag=row.get("policy_tag"),
            )
        )
        return

    home = int(row.get("count_accepted_home"))
    meeting = int(row.get("count_accepted_meeting_point"))
    opted_out = int(row.get("count_opted_out"))
    accepted = home + meeting
    total_choices = accepted + opted_out
    if int(row.get("accepted_count", -1)) != accepted:
        failures.append(
            _blocker(
                "accepted_count does not equal accepted home plus accepted meeting-point",
                "Keep opt-out separate from accepted service accounting.",
                "work2_coding/Src/paired_replay.py",
                "accepted_count_mismatch",
                split_id=row.get("split_id"),
                policy_tag=row.get("policy_tag"),
            )
        )
    if int(row.get("served_count", -1)) != accepted:
        failures.append(
            _blocker(
                "served_count does not equal accepted_count",
                "Regenerate row accounting so served_count excludes opt-out.",
                "work2_coding/Src/paired_replay.py",
                "served_count_mismatch",
                split_id=row.get("split_id"),
                policy_tag=row.get("policy_tag"),
            )
        )
    if total_choices <= 0:
        return
    expected_rates = {
        "optout_rate": opted_out / float(total_choices),
        "home_share": home / float(total_choices),
        "meeting_point_uptake_rate": meeting / float(total_choices),
    }
    for field, expected in expected_rates.items():
        value = row.get(field)
        if value is not None and abs(float(value) - expected) > 1e-9:
            failures.append(
                _blocker(
                    f"{field} does not use the total-choice denominator",
                    "Regenerate row rates with accepted home, accepted meeting-point, and opt-out in the denominator.",
                    "work2_coding/Src/paired_replay.py",
                    "invalid_" + field,
                    split_id=row.get("split_id"),
                    policy_tag=row.get("policy_tag"),
                )
            )


def _check_pairing(rows, split_id, failures):
    group = {row.get("policy_tag"): row for row in rows}
    expected = set(MAIN_BASELINE_TAGS)
    if set(group) != expected:
        failures.append(
            _blocker(
                "paired split does not contain exactly the two main Phase 8 baselines",
                "Rerun the Phase 8 study with mainline_optimized_mw and phase8_static_flat_markdown.",
                "work2_coding/Experiments/studies/phase8_baseline_validation.yaml",
                "missing_main_baseline_pair",
                split_id=split_id,
                observed_policy_tags=sorted(group),
            )
        )
        return

    no_pricing = group["mainline_optimized_mw"]
    static = group["phase8_static_flat_markdown"]
    shared_fields = [
        "run_id",
        "seed",
        "data_seed",
        "data_seed_test",
        "trace_id",
        "trace_hash",
        "manifest_hash",
        "checkpoint_path",
        "checkpoint_hash",
        "checkpoint_load_status",
        "checkpoint_required",
        "hgs_reopt_time",
        "hgs_final_time",
        "menu_k",
        "max_candidates",
    ]
    for field in shared_fields:
        if no_pricing.get(field) != static.get(field):
            failures.append(
                _blocker(
                    f"paired baseline drift in shared field {field}",
                    "Rerun both baselines from the same Phase 8 manifest and shared replay settings.",
                    "work2_coding/Experiments/studies/phase8_baseline_validation.yaml",
                    "paired_field_drift",
                    split_id=split_id,
                    field=field,
                    no_pricing_value=no_pricing.get(field),
                    static_value=static.get(field),
                )
            )
    if no_pricing.get("product_mode") != "m+w" or no_pricing.get("pricing_mode") != "no_pricing":
        failures.append(
            _blocker(
                "no-pricing baseline row does not use mainline_optimized_mw semantics",
                "Use product_mode=m+w and pricing_mode=no_pricing for the no-pricing baseline.",
                "work2_coding/Src/policy_adapters.py",
                "invalid_no_pricing_semantics",
                split_id=split_id,
            )
        )
    if static.get("product_mode") != "m+w+p" or static.get("pricing_mode") != "flat_markdown":
        failures.append(
            _blocker(
                "static-pricing baseline row does not use m+w+p flat_markdown semantics",
                "Use product_mode=m+w+p and pricing_mode=flat_markdown for the static baseline.",
                "work2_coding/Src/policy_adapters.py",
                "invalid_static_semantics",
                split_id=split_id,
            )
        )


def validate_phase8_baseline_rows(rows, manifest=None, study_summary=None, dependency_snapshot=None):
    rows = rows or []
    study_summary = study_summary or {}
    failures = []
    main_rows = [row for row in rows if _is_main_row(row)]
    split_ids = _required_split_ids(manifest=manifest, rows=main_rows)

    if not rows:
        failures.append(
            _blocker(
                "no normalized rows are available for Phase 8 baseline validation",
                "Run the Phase 8 baseline validation study in actual replay mode.",
                "work2_coding/outputs/studies/phase8_baseline_validation/",
                "no_rows",
            )
        )
    if len(split_ids) < EXPECTED_SPLIT_COUNT:
        failures.append(
            _blocker(
                "fewer than five paired baseline splits are available",
                "Run all five Phase 8 baseline splits before releasing Phase 9.",
                "work2_coding/Experiments/studies/phase8_baseline_validation.yaml",
                "insufficient_split_count",
                observed_split_count=len(split_ids),
                expected_split_count=EXPECTED_SPLIT_COUNT,
            )
        )

    by_split = {}
    for row in main_rows:
        by_split.setdefault(row.get("split_id"), []).append(row)
        for field in [
            "run_id",
            "manifest_hash",
            "settings_hash",
            "trace_id",
            "trace_hash",
            "method_family",
            "outside_option_util",
        ]:
            _require_field(row, field, failures)
        _check_row_status(row, failures)
        _check_checkpoint(row, failures)
        _check_accounting(row, failures)

    for split_id in split_ids:
        _check_pairing(by_split.get(split_id, []), split_id, failures)

    artifact_gate = classify_artifact(main_rows, study_summary, dependency_snapshot=dependency_snapshot)
    claim_ready_reasons = list(artifact_gate.get("reasons", []))
    if any(row.get("git_dirty") for row in main_rows):
        claim_ready_reasons.append("formal claim-ready artifacts require clean git provenance")
    claim_ready = bool(artifact_gate.get("claim_ready")) and not any(row.get("git_dirty") for row in main_rows)
    claim_ready_status = artifact_gate.get("status")
    if not claim_ready and claim_ready_status == "claim_ready":
        claim_ready_status = "blocked"
    status = "passed" if not failures else "blocked"
    return {
        "schema_version": "phase8-baseline-validation-v1",
        "phase": "08",
        "phase_name": "Baseline Validation",
        "generated_at_utc": utc_now_iso(),
        "baseline_validation_status": status,
        "phase9_release_gate": "open" if status == "passed" else "blocked",
        "claim_ready": claim_ready,
        "claim_ready_status": claim_ready_status,
        "claim_ready_reasons": sorted(set(claim_ready_reasons)),
        "study_name": study_summary.get("study_name") or (manifest or {}).get("name", DEFAULT_STUDY_NAME),
        "run_id": study_summary.get("run_id") or next((row.get("run_id") for row in main_rows if row.get("run_id")), ""),
        "row_count": len(rows),
        "main_row_count": len(main_rows),
        "expected_split_count": EXPECTED_SPLIT_COUNT,
        "observed_split_ids": sorted({row.get("split_id") for row in main_rows if row.get("split_id")}),
        "main_baseline_tags": list(MAIN_BASELINE_TAGS),
        "failures": failures,
        "artifact_gate": artifact_gate,
        "manuscript_safe_status": (
            "Phase 8 baseline validation passed for paired no-pricing and static-pricing baselines; "
            "formal ranking claims remain gated by downstream DSPO and DSPO_PLUS validation."
            if status == "passed"
            else "Phase 8 baseline validation is blocked; downstream DSPO and DSPO_PLUS ranking claims remain gated."
        ),
        "non_actions": [
            "DSPO clip/wide validation was not performed",
            "DSPO_PLUS clip/wide validation was not performed",
            "target ranking was not asserted",
            "generated result rows were not hand-edited",
        ],
    }


def load_study_run(run_dir):
    run_dir = Path(run_dir)
    rows_path = run_dir / "normalized_rows.json"
    summary_path = run_dir / "study_summary.json"
    manifest_path = run_dir / "manifest_snapshot.yaml"
    rows = json.loads(rows_path.read_text(encoding="utf-8")) if rows_path.exists() else []
    summary = json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.exists() else {}
    manifest = None
    if manifest_path.exists():
        try:
            import yaml

            manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
            manifest["_path"] = str(manifest_path)
        except Exception:
            manifest = None
    return rows, summary, manifest


def latest_phase8_run(studies_root=None):
    studies_root = Path(studies_root or ROOT / "outputs" / "studies")
    study_root = studies_root / DEFAULT_STUDY_NAME
    if not study_root.exists():
        return None
    candidates = [path for path in study_root.iterdir() if (path / "study_summary.json").exists()]
    if not candidates:
        return None
    return sorted(candidates, key=lambda path: path.stat().st_mtime, reverse=True)[0]


def blocked_missing_run_report():
    manifest = load_manifest(DEFAULT_STUDY_NAME)
    return validate_phase8_baseline_rows([], manifest=manifest, study_summary={"study_name": DEFAULT_STUDY_NAME})


def markdown_report(report):
    lines = [
        "# Phase 8 Baseline Validation Report",
        "",
        f"- Schema: `{report['schema_version']}`",
        f"- Baseline validation: `{report['baseline_validation_status']}`",
        f"- Phase 9 release gate: `{report['phase9_release_gate']}`",
        f"- Claim-ready: `{str(report['claim_ready']).lower()}` (`{report['claim_ready_status']}`)",
        f"- Run ID: `{report.get('run_id', '')}`",
        "",
        "## Status Language",
        "",
        report["manuscript_safe_status"],
        "",
        "## Main Baselines",
        "",
    ]
    for tag in report["main_baseline_tags"]:
        lines.append("- `" + tag + "`")
    lines.extend(["", "## Failures", ""])
    if not report["failures"]:
        lines.append("- None.")
    for failure in report["failures"]:
        lines.extend(
            [
                f"- code: `{failure['code']}`",
                f"  reason: {failure['reason']}",
                f"  minimal_fix: {failure['minimal_fix']}",
                f"  rerun_command: `{failure['rerun_command']}`",
                f"  evidence_location: `{failure['evidence_location']}`",
            ]
        )
    lines.extend(["", "## Claim-Ready Separation", ""])
    reasons = report.get("claim_ready_reasons") or []
    if not reasons:
        lines.append("- No claim-ready blockers reported by artifact gate.")
    for reason in reasons:
        lines.append("- " + reason)
    lines.extend(["", "## Boundary", ""])
    for item in report.get("non_actions", []):
        lines.append("- " + item)
    lines.append("")
    return "\n".join(lines)


def write_phase8_baseline_validation_report(output_root=None, run_dir=None, studies_root=None):
    output_root = Path(output_root or DEFAULT_OUTPUT_ROOT)
    output_root.mkdir(parents=True, exist_ok=True)
    run_dir = Path(run_dir) if run_dir else latest_phase8_run(studies_root=studies_root)
    if run_dir:
        rows, summary, manifest = load_study_run(run_dir)
        report = validate_phase8_baseline_rows(rows, manifest=manifest, study_summary=summary)
        report["source_run_dir"] = _rel(run_dir)
    else:
        report = blocked_missing_run_report()
        report["source_run_dir"] = ""

    json_path = output_root / REPORT_JSON
    md_path = output_root / REPORT_MD
    result = deepcopy(report)
    result["reports"] = {"json": str(json_path), "markdown": str(md_path)}
    write_json(json_path, result)
    md_path.write_text(markdown_report(result), encoding="utf-8")
    return result


def synthetic_completed_rows():
    manifest = load_manifest(DEFAULT_STUDY_NAME)
    mh = manifest_hash(manifest)
    rows = []
    for setting in resolve_paired_settings(manifest, manifest_hash_value=mh):
        rows.append(
            build_normalized_row(
                setting,
                run_id="phase8-synthetic",
                checkpoint_metadata={
                    "checkpoint_load_status": "loaded",
                    "checkpoint_path": "outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt",
                    "checkpoint_hash": "phase8-checkpoint-hash",
                    "checkpoint_required": True,
                    "checkpoint_intentional_mismatch": False,
                },
                stats_metadata={
                    "count_opted_out": 1,
                    "count_accepted_home": 2,
                    "count_accepted_meeting_point": 3,
                    "net_price_revenue": 10.0,
                    "operational_cost": 5.0,
                },
                status="completed",
                execution_status="completed",
                placeholder_only=False,
            )
        )
    return rows, manifest
