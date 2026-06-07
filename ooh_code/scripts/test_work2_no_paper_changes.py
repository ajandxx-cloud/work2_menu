import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

FORBIDDEN_PREFIXES = (
    "ooh_code/manuscript/",
    "manuscript/",
)

FORBIDDEN_SUFFIXES = (
    ".bib",
)

ALLOWED_TEX_PREFIXES = (
    "artifacts/work2_cnn_setmenunet/tables/",
    "ooh_code/artifacts/tables/",
)


def _git_lines(*args):
    result = subprocess.run(
        ["git", *args],
        cwd=PROJECT_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode not in {0, 1}:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return [line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()]


def _changed_paths():
    paths = set(_git_lines("diff", "--name-only"))
    paths.update(_git_lines("ls-files", "--others", "--exclude-standard"))
    return sorted(paths)


def _is_forbidden(path):
    if path.startswith(FORBIDDEN_PREFIXES):
        return True
    if path.endswith(".tex") and not path.startswith(ALLOWED_TEX_PREFIXES):
        return True
    return path.endswith(FORBIDDEN_SUFFIXES)


def main():
    offenders = [path for path in _changed_paths() if _is_forbidden(path)]
    if offenders:
        formatted = "\n".join(f"- {path}" for path in offenders)
        raise SystemExit(f"Forbidden paper/manuscript changes detected:\n{formatted}")
    print("PASS: no manuscript, bibliography, or non-artifact LaTeX changes detected")


if __name__ == "__main__":
    main()
