import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.sensitivity_analysis import (  # noqa: E402
    DEFAULT_BASELINE_REPORT,
    DEFAULT_OUTPUT_ROOT,
    DEFAULT_STUDIES_ROOT,
    DEFAULT_SUITE,
    DEFAULT_SUMMARY_PATH,
    write_sensitivity_summary,
)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Write the generated Phase 8 sensitivity summary.")
    parser.add_argument("--suite", default=DEFAULT_SUITE)
    parser.add_argument("--studies-root", default=str(DEFAULT_STUDIES_ROOT))
    parser.add_argument("--baseline-report", default=str(DEFAULT_BASELINE_REPORT))
    parser.add_argument("--artifact-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--planning-output", default=str(DEFAULT_SUMMARY_PATH))
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    result = write_sensitivity_summary(
        suite_name=args.suite,
        studies_root=args.studies_root,
        baseline_report=args.baseline_report,
        artifact_root=args.artifact_root,
        planning_output=args.planning_output,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


if __name__ == "__main__":
    main()
