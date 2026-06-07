import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Src.research_pipeline import load_study_summary


MEMBERS = [
    "work2_menu_size_robustness",
    "work2_candidate_pool_robustness",
    "work2_outside_option_robustness",
    "work2_demand_robustness",
    "work2_cross_instance_robustness",
]

REPORT_JSON = ROOT / "outputs" / "studies" / "work2_robustness_closure_status.json"
REPORT_MD = ROOT / "outputs" / "studies" / "work2_robustness_closure_status.md"

REQUIRED_SETTINGS = {
    "work2_menu_size_robustness": ("menu_k", {2, 3, 5}),
    "work2_candidate_pool_robustness": ("candidate_pool_size", {6, 10, 15}),
    "work2_demand_robustness": ("max_steps_r", {490, 700, 910}),
    "work2_outside_option_robustness": ("outside_option_util", {-0.5, 0.0, 0.5}),
}


def utc_now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def row_count(summary):
    if not summary:
        return 0
    return len(summary.get("normalized_rows", []))


def summary_has_required_settings(member, summary):
    rows = summary.get("normalized_rows", []) if summary else []
    if not rows:
        return False
    if member == "work2_cross_instance_robustness":
        return any(row.get("instance") not in {"", None, "RC"} for row in rows)
    key, expected = REQUIRED_SETTINGS[member]
    values = {row.get(key) for row in rows}
    return expected <= values


def latest_completed_summary(member):
    summary, run_dir = load_study_summary(member)
    if summary is None:
        return None, run_dir
    status = summary.get("run_metadata", {}).get("status")
    if status == "completed" and summary_has_required_settings(member, summary):
        return summary, run_dir
    return None, run_dir


def command_for(member):
    return [sys.executable, "scripts/run_study.py", "--study", member, "--resume_latest"]


def command_text(command):
    return "python " + " ".join(command[1:])


def tail(text, limit=4000):
    text = text or ""
    return text[-limit:]


def run_member(member):
    existing, existing_dir = latest_completed_summary(member)
    command = command_for(member)
    if existing is not None:
        metadata = existing.get("run_metadata", {})
        return {
            "study_name": member,
            "status": "skipped_completed",
            "command": command_text(command),
            "run_id": metadata.get("run_id"),
            "study_root": metadata.get("study_root") or str(existing_dir),
            "row_count": row_count(existing),
            "summary_path": str(Path(metadata.get("study_root") or existing_dir) / "study_summary.json"),
        }

    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    summary, run_dir = load_study_summary(member)
    status = "completed" if result.returncode == 0 and summary is not None else "incomplete"
    metadata = summary.get("run_metadata", {}) if summary else {}
    if summary is not None and metadata.get("status") != "completed":
        status = "incomplete"
    if result.returncode != 0:
        status = "failed"

    return {
        "study_name": member,
        "status": status,
        "command": command_text(command),
        "returncode": result.returncode,
        "run_id": metadata.get("run_id"),
        "study_root": metadata.get("study_root") or (str(run_dir) if run_dir else None),
        "row_count": row_count(summary),
        "summary_path": None if run_dir is None else str(Path(run_dir) / "study_summary.json"),
        "stdout_tail": tail(result.stdout),
        "stderr_tail": tail(result.stderr),
        "retry_command": command_text(command) if status != "completed" else "",
    }


def write_reports(payload):
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# Work2 Robustness Closure Status",
        "",
        f"Generated: {payload['generated_at_utc']}",
        "",
        "| Study | Status | Rows | Run ID | Retry command |",
        "|---|---|---:|---|---|",
    ]
    for item in payload["members"]:
        lines.append(
            "| {study} | {status} | {rows} | {run_id} | {retry} |".format(
                study=item["study_name"],
                status=item["status"],
                rows=item.get("row_count", 0),
                run_id=item.get("run_id") or "--",
                retry=f"`{item.get('retry_command')}`" if item.get("retry_command") else "--",
            )
        )
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    results = []
    for member in MEMBERS:
        print(f"== {member} ==")
        result = run_member(member)
        results.append(result)
        print(json.dumps({k: result.get(k) for k in ["study_name", "status", "run_id", "row_count", "retry_command"]}, ensure_ascii=False))

    payload = {
        "generated_at_utc": utc_now_iso(),
        "members": results,
        "completed_members": sum(1 for item in results if item["status"] in {"completed", "skipped_completed"}),
        "expected_members": len(MEMBERS),
    }
    write_reports(payload)
    print(f"Status JSON: {REPORT_JSON}")
    print(f"Status Markdown: {REPORT_MD}")

    if payload["completed_members"] != payload["expected_members"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
