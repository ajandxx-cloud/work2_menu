import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Src.research_pipeline import MANUSCRIPT_DIR, utc_now_iso, write_text


def build_artifacts(study_name):
    command = [sys.executable, "scripts/build_artifacts.py", "--study", study_name]
    subprocess.run(command, cwd=MANUSCRIPT_DIR.parent, check=True)


def detect_compiler():
    for candidate in ["latexmk", "pdflatex"]:
        path = shutil.which(candidate)
        if path:
            return candidate, path
    return None, None


def compile_with_latexmk():
    build_dir = MANUSCRIPT_DIR / "build"
    build_dir.mkdir(parents=True, exist_ok=True)
    references_source = MANUSCRIPT_DIR / "references.bib"
    references_target = build_dir / "references.bib"
    if references_source.exists():
        shutil.copyfile(references_source, references_target)

    command = [
        "latexmk",
        "-pdf",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-output-directory=build",
        "main.tex",
    ]
    subprocess.run(command, cwd=MANUSCRIPT_DIR, check=True)


def sync_build_artifacts_to_root():
    for suffix in ["aux", "bbl", "blg", "out", "toc", "lof", "lot"]:
        source = MANUSCRIPT_DIR / "build" / f"main.{suffix}"
        target = MANUSCRIPT_DIR / f"main.{suffix}"
        if source.exists():
            shutil.copyfile(source, target)


def clear_root_aux_files():
    for suffix in ["aux", "bbl", "blg", "out", "toc", "lof", "lot"]:
        target = MANUSCRIPT_DIR / f"main.{suffix}"
        if target.exists():
            target.unlink()


def compile_with_pdflatex():
    build_dir = MANUSCRIPT_DIR / "build"
    build_dir.mkdir(parents=True, exist_ok=True)
    references_source = MANUSCRIPT_DIR / "references.bib"
    references_target = build_dir / "references.bib"
    if references_source.exists():
        shutil.copyfile(references_source, references_target)
    clear_root_aux_files()
    pdflatex_command = [
        "pdflatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-output-directory=build",
        "main.tex",
    ]
    subprocess.run(pdflatex_command, cwd=MANUSCRIPT_DIR, check=True)
    sync_build_artifacts_to_root()
    bibtex_path = shutil.which("bibtex")
    if bibtex_path:
        subprocess.run(["bibtex", "build/main"], cwd=MANUSCRIPT_DIR, check=True)
        sync_build_artifacts_to_root()
    subprocess.run(pdflatex_command, cwd=MANUSCRIPT_DIR, check=True)
    sync_build_artifacts_to_root()
    subprocess.run(pdflatex_command, cwd=MANUSCRIPT_DIR, check=True)
    sync_build_artifacts_to_root()


def main():
    parser = argparse.ArgumentParser(description="Build manuscript assets and compile the LaTeX draft when possible.")
    parser.add_argument(
        "--study",
        default="rc_paper_v1",
        help="Study or suite name used to regenerate artifacts before compiling the manuscript.",
    )
    parser.add_argument(
        "--skip_compile",
        action="store_true",
        help="Refresh artifacts and manuscript metadata without invoking a LaTeX compiler.",
    )
    args = parser.parse_args()

    build_artifacts(args.study)

    metadata = {
        "built_at_utc": utc_now_iso(),
        "study": args.study,
        "manuscript_root": str(MANUSCRIPT_DIR),
        "compile_requested": not args.skip_compile,
    }

    compiler_name, compiler_path = detect_compiler()
    metadata["compiler"] = compiler_name or ""
    metadata["compiler_path"] = compiler_path or ""

    if args.skip_compile:
        metadata["status"] = "prepared_without_compile"
        write_text(MANUSCRIPT_DIR / "build" / "build_status.json", json.dumps(metadata, indent=2))
        print("Artifacts refreshed for manuscript.")
        print("Skipped LaTeX compilation by request.")
        return

    if compiler_name is None:
        metadata["status"] = "compiler_missing"
        write_text(MANUSCRIPT_DIR / "build" / "build_status.json", json.dumps(metadata, indent=2))
        raise SystemExit("No LaTeX compiler was found. Install latexmk or pdflatex, or rerun with --skip_compile.")

    used_compiler = compiler_name
    if compiler_name == "latexmk":
        try:
            compile_with_latexmk()
        except subprocess.CalledProcessError:
            if shutil.which("pdflatex"):
                compile_with_pdflatex()
                used_compiler = "pdflatex_fallback"
            else:
                raise
    else:
        compile_with_pdflatex()

    metadata["status"] = "compiled"
    metadata["compiler_used"] = used_compiler
    metadata["output_pdf"] = str(MANUSCRIPT_DIR / "build" / "main.pdf")
    write_text(MANUSCRIPT_DIR / "build" / "build_status.json", json.dumps(metadata, indent=2))
    print("Compiled manuscript with", used_compiler)
    print("PDF:", MANUSCRIPT_DIR / "build" / "main.pdf")


if __name__ == "__main__":
    main()
