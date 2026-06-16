import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.model_consistency_report import write_phase7_model_consistency_report  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", default="outputs/phase7_model_consistency")
    args = parser.parse_args()
    report = write_phase7_model_consistency_report(args.output_root)
    print("PHASE7_MODEL_CONSISTENCY_STATUS=" + report["status"])
    print("PHASE7_MODEL_CONSISTENCY_JSON=" + report["reports"]["json"])
    print("PHASE7_MODEL_CONSISTENCY_MD=" + report["reports"]["markdown"])


if __name__ == "__main__":
    main()
