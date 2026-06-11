import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))

from Src.artifact_builder import (  # noqa: E402
    DEFAULT_MIRROR_ROOT,
    DEFAULT_OUTPUT_ROOT,
    build_artifacts,
    mirror_lightweight_artifacts,
)
from Src.artifact_status import write_json  # noqa: E402
from Src.experiment_contracts import load_manifest  # noqa: E402
from scripts.run_study import execute_study  # noqa: E402


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Run the Phase 4 evidence/artifact pipeline.")
    parser.add_argument("--study", default="pilot_robust_menu", help="Study to run before artifact generation")
    parser.add_argument("--allow-incomplete", action="store_true", help="Allow blocker/incomplete evidence bundles")
    parser.add_argument("--skip-formal", action="store_true", help="Record formal evidence as skipped/blocked")
    parser.add_argument("--output-root", default=str(ROOT / "outputs" / "studies"), help="Raw study output root")
    parser.add_argument("--artifact-root", default=str(DEFAULT_OUTPUT_ROOT), help="Artifact output root")
    parser.add_argument("--mirror-root", default=str(DEFAULT_MIRROR_ROOT), help="Lightweight mirror root")
    parser.add_argument("--max-policies", type=int, default=0, help="Limit policies for pacing")
    parser.add_argument("--contract-only", action="store_true", help="Use contract-only rows instead of actual attempt")
    return parser.parse_args(argv)


def _load_status(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write_pipeline_status(status_path, result, run_summary, args):
    status_path = Path(status_path)
    status = _load_status(status_path)
    formal_blockers = []
    if args.skip_formal:
        formal_blockers.append(
            {
                "code": "formal_skipped",
                "severity": "blocking",
                "message": "Formal evidence was skipped for this Phase 4 run; formal claim readiness is false.",
            }
        )
    status["phase4_pipeline"] = {
        "commands": [
            {
                "name": "run_study",
                "study": args.study,
                "mode": "contract_only" if args.contract_only else "actual_or_blocked",
                "output_root": str(args.output_root),
            },
            {
                "name": "build_artifacts",
                "output_root": str(args.artifact_root),
                "mirror_root": str(args.mirror_root),
                "allow_incomplete": bool(args.allow_incomplete),
            },
        ],
        "run_dir": run_summary["run_dir"],
        "artifact_root": str(args.artifact_root),
        "mirror_root": str(args.mirror_root),
        "pilot_claim_ready": status.get("pilot_claim_ready", False),
        "formal_claim_ready": False if args.skip_formal else status.get("formal_claim_ready", False),
        "formal_blockers": formal_blockers,
    }
    if formal_blockers:
        status.setdefault("blockers", [])
        status["blockers"] = list(status["blockers"]) + formal_blockers
    write_json(status_path, status)
    return status


def run_pipeline(args):
    manifest = load_manifest(args.study)
    max_policies = args.max_policies if args.max_policies > 0 else None
    summary = execute_study(
        manifest,
        output_root=args.output_root,
        contract_only=bool(args.contract_only),
        max_policies=max_policies,
        actual_execution=not bool(args.contract_only),
    )
    result = build_artifacts(
        summary["run_dir"],
        output_root=args.artifact_root,
        mirror_root=None,
        allow_incomplete=args.allow_incomplete,
        claim_ready=False,
    )
    status = _write_pipeline_status(result["status_path"], result, summary, args)
    mirror_lightweight_artifacts(args.artifact_root, args.mirror_root)
    mirror_status = Path(args.mirror_root) / "ARTIFACT_STATUS.json"
    if mirror_status.exists():
        write_json(mirror_status, status)
    result["mirror_root"] = str(args.mirror_root)
    result["pipeline_status"] = status.get("phase4_pipeline", {})
    return result


def main(argv=None):
    args = parse_args(argv)
    result = run_pipeline(args)
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


if __name__ == "__main__":
    main()

