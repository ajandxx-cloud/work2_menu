import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.experiment_contracts import (  # noqa: E402
    load_manifest,
    load_suite,
    manifest_hash,
    suite_members,
)
from Src.paired_replay import (  # noqa: E402
    NORMALIZED_ROW_FIELDS,
    annotate_attention_pair_completeness,
    build_normalized_row,
    checkpoint_row_metadata,
    resolve_paired_settings,
    validate_rows,
)
from Src.study_execution import (  # noqa: E402
    actual_rows_for_manifest,
    blocked_rows_for_manifest,
    collect_git_provenance,
    inspect_manifest_prerequisites,
)


def utc_run_id(study_name, manifest_hash_value):
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return study_name + "-" + stamp + "-" + manifest_hash_value[:8]


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=NORMALIZED_ROW_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in NORMALIZED_ROW_FIELDS})


def write_manifest_snapshot(path, manifest):
    data = dict(manifest)
    data.pop("_path", None)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def contract_rows_for_manifest(manifest, run_id, max_policies=None):
    mh = manifest_hash(manifest)
    settings = resolve_paired_settings(manifest, manifest_hash_value=mh)
    if max_policies is not None:
        allowed_tags = []
        for setting in settings:
            tag = setting["policy_tag"]
            if tag not in allowed_tags:
                allowed_tags.append(tag)
            if len(allowed_tags) >= max_policies:
                break
        settings = [setting for setting in settings if setting["policy_tag"] in set(allowed_tags)]

    rows = []
    provenance = collect_git_provenance()
    for setting in settings:
        checkpoint = checkpoint_row_metadata(setting["args"])
        row = build_normalized_row(
            setting,
            run_id=run_id,
            checkpoint_metadata=checkpoint,
            stats_metadata={
                "acceptance_rate": None,
                "optout_rate": None,
                "count_opted_out": None,
                "count_accepted_home": None,
                "count_accepted_meeting_point": None,
            },
            menu_metadata={
                "eta_filter_mode": setting["args"].get("menu_eta_filter_mode"),
                "effective_menu_policy": setting["args"].get("menu_policy"),
                "menu_selection_solver_effective": "contract_only",
            },
            provenance_metadata=provenance,
            status="contract_only",
            execution_status="contract_only",
            placeholder_only=True,
        )
        rows.append(row)
    annotate_attention_pair_completeness(rows)
    validate_rows(rows)
    return rows


def _write_run_outputs(run_dir, manifest, rows, summary, blockers=None):
    write_manifest_snapshot(run_dir / "manifest_snapshot.yaml", manifest)
    write_json(run_dir / "normalized_rows.json", rows)
    write_csv(run_dir / "normalized_rows.csv", rows)
    write_json(run_dir / "study_summary.json", summary)
    if blockers:
        write_json(run_dir / "blockers.json", {"blockers": blockers})


def execute_study(manifest, output_root=None, contract_only=True, max_policies=None, actual_execution=False):
    if contract_only and manifest["tier"] == "formal":
        raise ValueError("formal studies cannot emit placeholder contract-only rows")

    mh = manifest_hash(manifest)
    run_id = utc_run_id(manifest["name"], mh)
    output_root = Path(output_root) if output_root else ROOT / "outputs" / "studies"
    run_dir = output_root / manifest["name"] / run_id
    blockers = inspect_manifest_prerequisites(
        manifest,
        root=ROOT,
        actual_execution=actual_execution,
        contract_only=contract_only,
    )
    if actual_execution and not blockers:
        try:
            rows = actual_rows_for_manifest(
                manifest,
                run_id,
                mh,
                max_policies=max_policies,
            )
            execution_status = "completed"
            placeholder_only = False
        except Exception as exc:
            blockers = [
                {
                    "code": "actual_replay_failed",
                    "severity": "blocking",
                    "tier": manifest.get("tier", ""),
                    "message": str(exc),
                }
            ]
            rows = blocked_rows_for_manifest(
                manifest,
                run_id,
                mh,
                blockers,
                max_policies=max_policies,
                root=ROOT,
            )
            execution_status = "blocked"
            placeholder_only = True
    elif blockers:
        rows = blocked_rows_for_manifest(
            manifest,
            run_id,
            mh,
            blockers,
            max_policies=max_policies,
            root=ROOT,
        )
        execution_status = "blocked" if any(item.get("severity") == "blocking" for item in blockers) else "incomplete"
        placeholder_only = True
    else:
        rows = contract_rows_for_manifest(manifest, run_id, max_policies=max_policies)
        execution_status = "contract_only"
        placeholder_only = True

    summary = {
        "study_name": manifest["name"],
        "tier": manifest["tier"],
        "run_mode": manifest["run_mode"],
        "run_id": run_id,
        "run_dir": str(run_dir),
        "manifest_hash": mh,
        "execution_status": execution_status,
        "contract_only": bool(contract_only),
        "placeholder_only": placeholder_only,
        "row_count": len(rows),
        "policy_tags": sorted({row["policy_tag"] for row in rows}),
        "split_ids": sorted({row["split_id"] for row in rows}),
        "uptake_regimes": sorted({row["uptake_regime"] for row in rows}),
        "checkpoint_statuses": sorted({row["checkpoint_load_status"] for row in rows}),
        "git_provenance": collect_git_provenance(),
        "blocker_count": len(blockers),
        "blockers": blockers,
        "outputs": [
            "manifest_snapshot.yaml",
            "study_summary.json",
            "normalized_rows.json",
            "normalized_rows.csv",
        ],
        "runtime_blocker": blockers[0]["message"] if blockers else "",
    }
    if blockers:
        summary["outputs"].append("blockers.json")
    _write_run_outputs(run_dir, manifest, rows, summary, blockers=blockers)
    return summary


def execute_suite(suite, output_root=None, contract_only=True, max_policies=None, actual_execution=False):
    summaries = []
    for member in suite_members(suite):
        manifest = load_manifest(member)
        if manifest["tier"] == "formal":
            continue
        summaries.append(
            execute_study(
                manifest,
                output_root=output_root,
                contract_only=contract_only,
                max_policies=max_policies,
                actual_execution=actual_execution,
            )
        )
    return {
        "suite_name": suite["name"],
        "execution_status": "blocked" if any(item["execution_status"] == "blocked" for item in summaries) else "contract_only",
        "studies": summaries,
    }


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Run Work2 robust-menu study contracts.")
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--study", help="Study manifest name or path")
    target.add_argument("--suite", help="Suite manifest name or path")
    parser.add_argument("--output-root", default="", help="Override output root")
    parser.add_argument("--contract-only", action="store_true", help="Emit contract-level normalized rows")
    parser.add_argument("--execute", action="store_true", help="Attempt actual replay; writes blockers if prerequisites are unavailable")
    parser.add_argument("--run-mode", choices=["contract", "actual"], default="contract", help="Execution mode")
    parser.add_argument("--max-policies", type=int, default=0, help="Limit unique policy tags for smoke pacing")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    output_root = args.output_root or None
    max_policies = args.max_policies if args.max_policies and args.max_policies > 0 else None
    actual_execution = args.execute or args.run_mode == "actual"
    contract_only = not actual_execution

    if args.study:
        manifest = load_manifest(args.study)
        summary = execute_study(
            manifest,
            output_root=output_root,
            contract_only=contract_only,
            max_policies=max_policies,
            actual_execution=actual_execution,
        )
        print(summary["run_dir"])
        return summary

    suite = load_suite(args.suite)
    summary = execute_suite(
        suite,
        output_root=output_root,
        contract_only=contract_only,
        max_policies=max_policies,
        actual_execution=actual_execution,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


if __name__ == "__main__":
    main()
