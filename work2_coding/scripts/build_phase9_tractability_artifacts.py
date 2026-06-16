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
    build_tractability_artifacts,
)


def main():
    parser = argparse.ArgumentParser(description="Build Phase 9 exact-greedy tractability artifacts.")
    parser.add_argument("--study", default=DEFAULT_STUDY)
    parser.add_argument("--studies-root", default=str(DEFAULT_STUDIES_ROOT))
    parser.add_argument("--status-gate", default=str(DEFAULT_STATUS_GATE))
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--run-dir", default="")
    args = parser.parse_args()

    result = build_tractability_artifacts(
        study=args.study,
        studies_root=args.studies_root,
        status_gate=args.status_gate,
        output_root=args.output_root,
        run_dir=args.run_dir or None,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
