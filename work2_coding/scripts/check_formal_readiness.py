import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.formal_readiness import check_formal_readiness  # noqa: E402


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Check formal Work2 readiness without running formal replay.")
    parser.add_argument("--study", default="formal_robust_menu", help="Formal study manifest name or path")
    parser.add_argument("--output-root", default="outputs/formal_readiness", help="Directory for readiness reports")
    parser.add_argument("--allow-dirty", action="store_true", help="Diagnostic/test-only: do not block on dirty git")
    parser.add_argument("--diagnostic-ok", action="store_true", help="Return zero even when readiness is blocked")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    command = "python scripts/check_formal_readiness.py " + " ".join(sys.argv[1:] if argv is None else argv)
    report = check_formal_readiness(
        study=args.study,
        output_root=args.output_root,
        allow_dirty=args.allow_dirty,
        command=command,
    )
    payload = {
        "status": report["status"],
        "claim_ready_allowed": report["claim_ready_allowed"],
        "blocker_count": len(report.get("blockers") or []),
        "blocker_codes": [item.get("code") for item in report.get("blockers") or []],
        "checkpoint_status": report["checkpoint"]["load_status"],
        "checkpoint_hash": report["checkpoint"].get("hash"),
        "dependency_snapshot_hash": report["dependency_snapshot"]["hash"],
        "git_dirty": report["git_provenance"].get("git_dirty"),
        "readiness_json": report["reports"]["json"],
        "readiness_markdown": report["reports"]["markdown"],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    if report["status"] != "passed" and not args.diagnostic_ok:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
