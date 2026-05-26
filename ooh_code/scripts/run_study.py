import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Src.research_pipeline import execute_study_manifest, load_manifest, latest_resumable_run_id


def main():
    parser = argparse.ArgumentParser(
        description="Run a named work2 study or suite from experiments/studies or experiments/suites."
    )
    parser.add_argument("--study", required=True, help="Study or suite manifest name, with or without .yaml.")
    parser.add_argument(
        "--force_retrain",
        action="store_true",
        help="Ignore existing shared checkpoints and retrain shared predictors for this run.",
    )
    parser.add_argument(
        "--resume_latest",
        action="store_true",
        help="Resume the latest incomplete run for this study or suite when available.",
    )
    parser.add_argument(
        "--resume_run_id",
        default="",
        help="Resume a specific existing run id instead of starting a new run.",
    )
    args = parser.parse_args()

    manifest = load_manifest(args.study)
    resume_run_id = args.resume_run_id
    if args.resume_latest and resume_run_id == "":
        resume_run_id = latest_resumable_run_id(
            manifest["name"],
            kind="suite" if manifest.get("_kind") == "suite" else "study",
            manifest_hash=manifest.get("_manifest_hash"),
        ) or ""

    summary = execute_study_manifest(
        manifest,
        reuse_existing=not args.force_retrain,
        resume_run_id=resume_run_id,
    )

    if manifest.get("_kind") == "suite":
        print("Completed suite:", summary["suite"]["name"])
        print("Suite run id:", summary["run_metadata"]["run_id"])
        print("Suite root:", summary["run_metadata"]["suite_root"])
        print("Member runs:")
        for member in summary["member_runs"]:
            print(" ", json.dumps(member, ensure_ascii=False))
    else:
        print("Completed study:", summary["study"]["name"])
        print("Study run id:", summary["run_metadata"]["run_id"])
        print("Study root:", summary["run_metadata"]["study_root"])
        print("Variants:", len(summary["aggregate_variant_summary"]))


if __name__ == "__main__":
    main()
