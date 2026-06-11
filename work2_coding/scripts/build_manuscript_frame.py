import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Src.manuscript_claims import write_manuscript_frame  # noqa: E402


def parse_args():
    parser = argparse.ArgumentParser(description="Build Work2 manuscript framing and claim guard artifacts.")
    parser.add_argument(
        "--artifact-root",
        default="artifacts/work2_robust_menu",
        help="Artifact bundle root containing ARTIFACT_STATUS.json.",
    )
    parser.add_argument(
        "--mirror-root",
        default=None,
        help="Optional mirror artifact root; files are copied under <mirror-root>/manuscript.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    result = write_manuscript_frame(args.artifact_root, mirror_root=args.mirror_root)
    print(
        json.dumps(
            {
                "output_dir": result["output_dir"],
                "files": result["files"],
                "mirror_files": result["mirror_files"],
                "artifact_status": result["claim_guard"]["artifact_status"],
                "claim_ready": result["claim_guard"]["claim_ready"],
                "blocked_claims": [claim["id"] for claim in result["claim_guard"]["blocked_claims"]],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
