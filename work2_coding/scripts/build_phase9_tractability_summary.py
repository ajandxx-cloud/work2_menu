import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.computational_tractability import (  # noqa: E402
    DEFAULT_OUTPUT_ROOT,
    DEFAULT_STATUS_GATE,
    DEFAULT_STUDIES_ROOT,
    DEFAULT_STUDY,
    DEFAULT_SUMMARY_PATH,
    write_tractability_summary,
)


def main():
    parser = argparse.ArgumentParser(description="Write the Phase 9 computational tractability summary.")
    parser.add_argument("--study", default=DEFAULT_STUDY)
    parser.add_argument("--studies-root", default=str(DEFAULT_STUDIES_ROOT))
    parser.add_argument("--status-gate", default=str(DEFAULT_STATUS_GATE))
    parser.add_argument("--artifact-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--planning-output", default=str(DEFAULT_SUMMARY_PATH))
    parser.add_argument("--run-dir", default="")
    args = parser.parse_args()

    result = write_tractability_summary(
        study=args.study,
        studies_root=args.studies_root,
        status_gate=args.status_gate,
        artifact_root=args.artifact_root,
        planning_output=args.planning_output,
        run_dir=args.run_dir or None,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
