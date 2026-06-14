import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.dspo_validation import write_phase9_dspo_family_validation_report  # noqa: E402


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", default="", help="Study run directory containing normalized_rows.json")
    parser.add_argument("--studies-root", default="", help="Root containing phase9_dspo_family_validation runs")
    parser.add_argument("--output-root", default="outputs/phase9_dspo_family_validation")
    parser.add_argument("--phase8-report", default="", help="Optional Phase 8 validation report JSON path")
    args = parser.parse_args(argv)
    report = write_phase9_dspo_family_validation_report(
        output_root=args.output_root,
        run_dir=args.run_dir or None,
        studies_root=args.studies_root or None,
        phase8_report=args.phase8_report or None,
    )
    print("PHASE9_DSPO_VALIDATION_STATUS=" + report["dspo_validation_status"])
    print("PHASE9_GATE=" + report["phase9_gate"])
    print("PHASE9_CLAIM_READY=" + str(report["claim_ready"]).lower())
    print("PHASE9_DSPO_VALIDATION_JSON=" + report["reports"]["json"])
    print("PHASE9_DSPO_VALIDATION_MD=" + report["reports"]["markdown"])
    return report


if __name__ == "__main__":
    main()
