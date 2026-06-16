import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Src.paper_artifacts import (  # noqa: E402
    DEFAULT_CASE_SCAFFOLD_ROOT,
    DEFAULT_MAIN_ARTIFACT_ROOT,
    DEFAULT_MIRROR_ROOT,
    DEFAULT_PHASE8_ROOT,
    DEFAULT_PHASE9_ROOT,
    DEFAULT_PHASE10_OUTPUT_ROOT,
    DEFAULT_RESULTS_ROOT,
    write_phase10_package,
)


def build_parser():
    parser = argparse.ArgumentParser(description="Build Phase 10 paper artifact package indexes.")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_PHASE10_OUTPUT_ROOT)
    parser.add_argument("--mirror-root", type=Path, default=None)
    parser.add_argument("--default-mirror", action="store_true", help="Write the default lightweight root-level mirror.")
    parser.add_argument("--no-mirror", action="store_true", help="Disable mirror generation.")
    parser.add_argument("--main-artifact-root", type=Path, default=DEFAULT_MAIN_ARTIFACT_ROOT)
    parser.add_argument("--phase8-root", type=Path, default=DEFAULT_PHASE8_ROOT)
    parser.add_argument("--phase9-root", type=Path, default=DEFAULT_PHASE9_ROOT)
    parser.add_argument("--case-scaffold-root", type=Path, default=DEFAULT_CASE_SCAFFOLD_ROOT)
    parser.add_argument("--results-root", type=Path, default=DEFAULT_RESULTS_ROOT)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    source_roots = {
        "main_rc": args.main_artifact_root,
        "phase8_sensitivity": args.phase8_root,
        "phase9_tractability": args.phase9_root,
        "case_scaffold": args.case_scaffold_root,
        "blocker_status": args.results_root,
    }
    if args.no_mirror:
        mirror_root = False
    elif args.mirror_root is not None:
        mirror_root = args.mirror_root
    elif args.default_mirror:
        mirror_root = DEFAULT_MIRROR_ROOT
    else:
        mirror_root = None
    result = write_phase10_package(
        output_root=args.output_root,
        mirror_root=mirror_root,
        source_roots=source_roots,
    )
    print(
        json.dumps(
            {
                "output_root": result["output_root"],
                "mirror_root": result["mirror_root"],
                "claim_ready": result["claim_ready"],
                "artifact_count": result["artifact_count"],
                "missing_artifact_count": result["missing_artifact_count"],
                "blocker_count": result["blocker_count"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return result


if __name__ == "__main__":
    main()
