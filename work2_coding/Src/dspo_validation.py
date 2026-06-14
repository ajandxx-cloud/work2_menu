"""Phase 9 DSPO family validation gate and report helpers."""

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

from Src.artifact_status import classify_artifact, write_json
from Src.experiment_contracts import load_manifest, manifest_hash
from Src.paired_replay import build_normalized_row, resolve_paired_settings


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
DEFAULT_STUDY_NAME = "phase9_dspo_family_validation"
DEFAULT_OUTPUT_ROOT = ROOT / "outputs" / "phase9_dspo_family_validation"
DSPO_POLICY_TAGS = ("dspo_clip", "dspo_wide")
EXPECTED_SPLIT_COUNT = 5
REPORT_JSON = "PHASE9_DSPO_FAMILY_VALIDATION.json"
REPORT_MD = "PHASE9_DSPO_FAMILY_VALIDATION.md"
DEFAULT_PHASE8_REPORT = ROOT / "outputs" / "phase8_baseline_validation" / "PHASE8_BASELINE_VALIDATION.json"
RERUN_COMMAND = (
    "cd work2_coding && python scripts/run_study.py --study phase9_dspo_family_validation "
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
    return sorted({row.get("split_id") for row in (rows or []) if row.get("split_id")})


def _is_dspo_row(row):
    return row.get("policy_tag") in DSPO_POLICY_TAGS


def _require_field(row, field, failures):
    if row.get(field) in (None, ""):
        failures.append(
            _blocker(
                f"DSPO row is missing required field {field}",
                f"Regenerate Phase 9 rows so normalized-row-v2 includes {field}.",
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
                "DSPO row is not completed actual replay",
                "Fix the replay failure and rerun Phase 9 DSPO family validation.",
                row.get("manifest_path") or "work2_coding/Experiments/studies/phase9_dspo_family_validation.yaml",
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
                "DSPO row is placeholder-only or contract-only",
                "Run actual replay; contract-only rows are insufficient for Phase 9.",
                row.get("manifest_path") or "work2_coding/Experiments/studies/phase9_dspo_family_validation.yaml",
                "placeholder_row",
                split_id=row.get("split_id"),
                policy_tag=row.get("policy_tag"),
            )
        )


def _check_checkpoint(row, failures):
    if row.get("checkpoint_required") and row.get("checkpoint_load_status") != "loaded":
        failures.append(
            _blocker(
                "DSPO row does not report loaded checkpoint status",
                "Restore the shared checkpoint or repair checkpoint loading before rerunning Phase 9.",
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
        _require_field(row, "checkpoint_load_status", failures)


def _check_accounting(row, failures):
    counts = [
        row.get("count_accepted_home"),
        row.get("count_accepted_meeting_point"),
        row.get("count_opted_out"),
    ]
    if any(value is None for value in counts):
        failures.append(
            _blocker(
                "DSPO row is missing opt-out/home/meeting-point counts",
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
        "acceptance_rate": accepted / float(total_choices),
        "served_rate": accepted / float(total_choices),
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
    expected = set(DSPO_POLICY_TAGS)
    if set(group) != expected:
        failures.append(
            _blocker(
                "paired split does not contain exactly dspo_clip and dspo_wide",
                "Rerun the Phase 9 study with both DSPO clip/wide policies for every split.",
                "work2_coding/Experiments/studies/phase9_dspo_family_validation.yaml",
                "missing_dspo_pair",
                split_id=split_id,
                observed_policy_tags=sorted(group),
            )
        )
        return

    clip = group["dspo_clip"]
    wide = group["dspo_wide"]
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
        "pricing",
        "uptake_regime",
        "outside_option_util",
    ]
    for field in shared_fields:
        if clip.get(field) != wide.get(field):
            failures.append(
                _blocker(
                    f"paired DSPO drift in shared field {field}",
                    "Rerun both DSPO variants from the same Phase 9 manifest and shared replay settings.",
                    "work2_coding/Experiments/studies/phase9_dspo_family_validation.yaml",
                    "paired_field_drift",
                    split_id=split_id,
                    field=field,
                    dspo_clip_value=clip.get(field),
                    dspo_wide_value=wide.get(field),
                )
            )
    for tag, row in group.items():
        if row.get("method_family") != "DSPO" or row.get("comparison_role") != "dspo_family":
            failures.append(
                _blocker(
                    "Phase 9 DSPO rows must use DSPO method_family and dspo_family comparison_role",
                    "Use the dspo_clip/dspo_wide Phase 9 adapters without DSPO_PLUS metadata.",
                    "work2_coding/Src/policy_adapters.py",
                    "invalid_dspo_semantics",
                    split_id=split_id,
                    policy_tag=tag,
                    method_family=row.get("method_family"),
                    comparison_role=row.get("comparison_role"),
                )
            )


def _check_unexpected_rows(rows, failures):
    unexpected = sorted({row.get("policy_tag") for row in rows if row.get("policy_tag") not in DSPO_POLICY_TAGS})
    for tag in unexpected:
        failures.append(
            _blocker(
                "Phase 9 report input contains a non-DSPO clip/wide policy row",
                "Use only dspo_clip and dspo_wide rows; Phase 8 baselines and DSPO_PLUS are not Phase 9 inputs.",
                "work2_coding/Experiments/studies/phase9_dspo_family_validation.yaml",
                "unexpected_phase9_policy",
                observed_policy_tag=tag,
            )
        )


def _load_phase8_report(phase8_report=None):
    if isinstance(phase8_report, dict):
        return phase8_report
    path = Path(phase8_report) if phase8_report else DEFAULT_PHASE8_REPORT
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _sanity_status(rows, phase8_report):
    phase8_report = phase8_report or {}
    explicit = phase8_report.get("sanity_reference") or {}
    supports_advantage = bool(explicit.get("supports_dspo_advantage", False))
    status = "status_only_no_advantage_conclusion"
    if supports_advantage:
        status = "status_only_supports_advantage_signal"
    if not phase8_report:
        status = "status_only_no_phase8_reference"
    return {
        "status": status,
        "supports_advantage_conclusion": supports_advantage,
        "statement": (
            "Sanity comparison is status-only and not a manuscript ranking conclusion; "
            "Phase 9 validation may pass without a DSPO advantage conclusion."
        ),
        "metrics_considered": explicit.get("metrics") or ["net_profit", "served_rate", "optout_rate"],
        "dspo_row_count": len(rows),
    }


def validate_phase9_dspo_rows(rows, manifest=None, study_summary=None, dependency_snapshot=None, phase8_report=None):
    rows = rows or []
    study_summary = study_summary or {}
    phase8_report = _load_phase8_report(phase8_report)
    failures = []
    _check_unexpected_rows(rows, failures)

    dspo_rows = [row for row in rows if _is_dspo_row(row)]
    split_ids = _required_split_ids(manifest=manifest, rows=dspo_rows)

    if not rows:
        failures.append(
            _blocker(
                "no normalized rows are available for Phase 9 DSPO validation",
                "Run the Phase 9 DSPO family validation study in actual replay mode.",
                "work2_coding/outputs/studies/phase9_dspo_family_validation/",
                "no_rows",
            )
        )
    if len(split_ids) < EXPECTED_SPLIT_COUNT:
        failures.append(
            _blocker(
                "fewer than five paired DSPO splits are available",
                "Run all five Phase 9 DSPO family splits before advancing status language.",
                "work2_coding/Experiments/studies/phase9_dspo_family_validation.yaml",
                "insufficient_split_count",
                observed_split_count=len(split_ids),
                expected_split_count=EXPECTED_SPLIT_COUNT,
            )
        )

    by_split = {}
    for row in dspo_rows:
        by_split.setdefault(row.get("split_id"), []).append(row)
        for field in [
            "run_id",
            "manifest_hash",
            "settings_hash",
            "trace_id",
            "trace_hash",
            "method_family",
            "comparison_role",
            "outside_option_util",
        ]:
            _require_field(row, field, failures)
        _check_row_status(row, failures)
        _check_checkpoint(row, failures)
        _check_accounting(row, failures)

    for split_id in split_ids:
        _check_pairing(by_split.get(split_id, []), split_id, failures)

    artifact_gate = classify_artifact(dspo_rows, study_summary, dependency_snapshot=dependency_snapshot)
    claim_ready_reasons = list(artifact_gate.get("reasons", []))
    if any(row.get("git_dirty") for row in dspo_rows):
        claim_ready_reasons.append("formal claim-ready artifacts require clean git provenance")
    claim_ready = bool(artifact_gate.get("claim_ready")) and not any(row.get("git_dirty") for row in dspo_rows)
    claim_ready_status = artifact_gate.get("status")
    if not claim_ready and claim_ready_status == "claim_ready":
        claim_ready_status = "blocked"

    status = "passed" if not failures else "blocked"
    sanity = _sanity_status(dspo_rows, phase8_report)
    next_step = (
        "Debug handoff: inspect failures, apply the minimal fixes, and rerun the Phase 9 study/report commands."
        if status == "blocked"
        else (
            "Proceed only with Phase 11 status/risk language; do not write DSPO ranking-claim language."
            if not sanity["supports_advantage_conclusion"]
            else "Proceed only with Phase 11 status/risk language; formal ranking claims remain gated downstream."
        )
    )
    return {
        "schema_version": "phase9-dspo-family-validation-v1",
        "phase": "09",
        "phase_name": "DSPO Family Full Run",
        "generated_at_utc": utc_now_iso(),
        "dspo_validation_status": status,
        "phase9_gate": "open" if status == "passed" else "blocked",
        "claim_ready": claim_ready,
        "claim_ready_status": claim_ready_status,
        "claim_ready_reasons": sorted(set(claim_ready_reasons)),
        "study_name": study_summary.get("study_name") or (manifest or {}).get("name", DEFAULT_STUDY_NAME),
        "run_id": study_summary.get("run_id") or next((row.get("run_id") for row in dspo_rows if row.get("run_id")), ""),
        "row_count": len(rows),
        "main_row_count": len(dspo_rows),
        "expected_split_count": EXPECTED_SPLIT_COUNT,
        "observed_split_ids": sorted({row.get("split_id") for row in dspo_rows if row.get("split_id")}),
        "dspo_policy_tags": list(DSPO_POLICY_TAGS),
        "phase8_reference_run_id": phase8_report.get("run_id", ""),
        "phase8_reference_status": phase8_report.get("baseline_validation_status", "unavailable"),
        "sanity_status": sanity,
        "next_step": next_step,
        "failures": failures,
        "artifact_gate": artifact_gate,
        "dspo_plus_exclusion": (
            "DSPO_PLUS is unrelated/stale for Phase 9 and is not inherited, compared, or validated."
        ),
        "manuscript_safe_status": (
            "Phase 9 DSPO validation passed for paired dspo_clip and dspo_wide rows; "
            "this unlocks DSPO result organization/status language only, not ranking claims."
            if status == "passed"
            else "Phase 9 DSPO validation is blocked; DSPO status language and ranking claims remain gated."
        ),
        "non_actions": [
            "Phase 8 baselines were not rerun inside Phase 9",
            "DSPO_PLUS was not inherited, compared, or validated",
            "artifact bundles were not generated",
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


def latest_phase9_run(studies_root=None):
    studies_root = Path(studies_root or ROOT / "outputs" / "studies")
    study_root = studies_root / DEFAULT_STUDY_NAME
    if not study_root.exists():
        return None
    candidates = [path for path in study_root.iterdir() if (path / "study_summary.json").exists()]
    if not candidates:
        return None
    return sorted(candidates, key=lambda path: path.stat().st_mtime, reverse=True)[0]


def blocked_missing_run_report(phase8_report=None):
    manifest = load_manifest(DEFAULT_STUDY_NAME)
    return validate_phase9_dspo_rows(
        [],
        manifest=manifest,
        study_summary={"study_name": DEFAULT_STUDY_NAME},
        phase8_report=phase8_report,
    )


def markdown_report(report):
    lines = [
        "# Phase 9 DSPO Family Validation Report",
        "",
        f"- Schema: `{report['schema_version']}`",
        f"- DSPO validation: `{report['dspo_validation_status']}`",
        f"- Phase 9 gate: `{report['phase9_gate']}`",
        f"- Claim-ready: `{str(report['claim_ready']).lower()}` (`{report['claim_ready_status']}`)",
        f"- Run ID: `{report.get('run_id', '')}`",
        f"- Phase 8 reference run: `{report.get('phase8_reference_run_id', '')}`",
        f"- Phase 8 reference status: `{report.get('phase8_reference_status', '')}`",
        "",
        "## Status Language",
        "",
        report["manuscript_safe_status"],
        "",
        "## Sanity Comparison",
        "",
        report["sanity_status"]["statement"],
        f"- Sanity status: `{report['sanity_status']['status']}`",
        f"- Supports advantage conclusion: `{str(report['sanity_status']['supports_advantage_conclusion']).lower()}`",
        "",
        "## DSPO Scope",
        "",
    ]
    for tag in report["dspo_policy_tags"]:
        lines.append("- `" + tag + "`")
    lines.extend(["", report["dspo_plus_exclusion"], "", "## Failures", ""])
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
    lines.extend(["", "## Next Step", "", report["next_step"], "", "## Boundary", ""])
    for item in report.get("non_actions", []):
        lines.append("- " + item)
    lines.append("")
    return "\n".join(lines)


def write_phase9_dspo_family_validation_report(output_root=None, run_dir=None, studies_root=None, phase8_report=None):
    output_root = Path(output_root or DEFAULT_OUTPUT_ROOT)
    output_root.mkdir(parents=True, exist_ok=True)
    phase8_report_data = _load_phase8_report(phase8_report)
    run_dir = Path(run_dir) if run_dir else latest_phase9_run(studies_root=studies_root)
    if run_dir:
        rows, summary, manifest = load_study_run(run_dir)
        report = validate_phase9_dspo_rows(
            rows,
            manifest=manifest,
            study_summary=summary,
            phase8_report=phase8_report_data,
        )
        report["source_run_dir"] = _rel(run_dir)
    else:
        report = blocked_missing_run_report(phase8_report=phase8_report_data)
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
                run_id="phase9-synthetic",
                checkpoint_metadata={
                    "checkpoint_load_status": "loaded",
                    "checkpoint_path": "outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt",
                    "checkpoint_hash": "phase9-checkpoint-hash",
                    "checkpoint_required": True,
                    "checkpoint_intentional_mismatch": False,
                },
                stats_metadata={
                    "count_opted_out": 1,
                    "count_accepted_home": 2,
                    "count_accepted_meeting_point": 3,
                    "net_price_revenue": 20.0,
                    "operational_cost": 6.0,
                },
                status="completed",
                execution_status="completed",
                placeholder_only=False,
            )
        )
    return rows, manifest
