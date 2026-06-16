import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.phase6_audit import write_phase6_audit  # noqa: E402


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Audit Phase 6 Work2 experiment and claim-gate state.")
    parser.add_argument("--output-root", default="outputs/phase6_audit", help="Directory for Phase 6 audit reports")
    parser.add_argument(
        "--readiness-json",
        default="outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json",
        help="FORMAL_READINESS.json to audit",
    )
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Terminal output format")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    report = write_phase6_audit(output_root=args.output_root, readiness_json=args.readiness_json)
    summary = {
        "claim_ready": report["claim_status"]["claim_ready"],
        "claim_status": report["claim_status"]["safe_manuscript_language"],
        "readiness_status": report["readiness"]["status"],
        "checkpoint_load_status": report["readiness"]["checkpoint_load_status"],
        "blocker_codes": report["readiness"]["blocker_codes"],
        "reports": report["reports"],
    }
    if args.format == "markdown":
        print("- Claim-ready: `" + str(summary["claim_ready"]).lower() + "`")
        print("- Readiness status: `" + str(summary["readiness_status"]) + "`")
        print("- Audit JSON: `" + summary["reports"]["json"] + "`")
        print("- Audit Markdown: `" + summary["reports"]["markdown"] + "`")
    else:
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
