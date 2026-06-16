import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.baseline_validation import write_phase8_baseline_validation_report  # noqa: E402


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", default="", help="Study run directory containing normalized_rows.json")
    parser.add_argument("--studies-root", default="", help="Root containing phase8_baseline_validation runs")
    parser.add_argument("--output-root", default="outputs/phase8_baseline_validation")
    args = parser.parse_args(argv)
    report = write_phase8_baseline_validation_report(
        output_root=args.output_root,
        run_dir=args.run_dir or None,
        studies_root=args.studies_root or None,
    )
    print("PHASE8_BASELINE_VALIDATION_STATUS=" + report["baseline_validation_status"])
    print("PHASE8_PHASE9_RELEASE_GATE=" + report["phase9_release_gate"])
    print("PHASE8_CLAIM_READY=" + str(report["claim_ready"]).lower())
    print("PHASE8_BASELINE_VALIDATION_JSON=" + report["reports"]["json"])
    print("PHASE8_BASELINE_VALIDATION_MD=" + report["reports"]["markdown"])
    return report


if __name__ == "__main__":
    main()
