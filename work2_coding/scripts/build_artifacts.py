import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.artifact_builder import (  # noqa: E402
    DEFAULT_MIRROR_ROOT,
    DEFAULT_OUTPUT_ROOT,
    build_artifacts,
    latest_run_dir,
)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Build Work2 robust-menu artifacts from normalized rows.")
    source = parser.add_mutually_exclusive_group(required=False)
    source.add_argument("--study", help="Use the latest run directory for a study")
    source.add_argument("--run-dir", help="Explicit run directory containing normalized rows")
    parser.add_argument("--study-output-root", default="", help="Override outputs/studies root for --study lookup")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT), help="Artifact output root")
    parser.add_argument("--mirror-root", default="", help="Optional lightweight mirror root")
    parser.add_argument("--default-mirror", action="store_true", help="Mirror to artifacts/work2_robust_menu")
    parser.add_argument("--allow-incomplete", action="store_true", help="Allow diagnostic/incomplete artifacts")
    parser.add_argument("--claim-ready", action="store_true", help="Require claim-ready artifact gates")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    if args.run_dir:
        run_dir = Path(args.run_dir)
    elif args.study:
        run_dir = latest_run_dir(args.study, study_output_root=args.study_output_root or None)
    else:
        raise ValueError("provide --run-dir or --study")

    mirror_root = args.mirror_root or (str(DEFAULT_MIRROR_ROOT) if args.default_mirror else "")
    result = build_artifacts(
        run_dir,
        output_root=args.output_root,
        mirror_root=mirror_root or None,
        allow_incomplete=args.allow_incomplete,
        claim_ready=args.claim_ready,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


if __name__ == "__main__":
    main()
