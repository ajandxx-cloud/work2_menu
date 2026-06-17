import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent


MANUSCRIPT_DIR = REPO_ROOT / "manuscript"
PACKAGE_DIR = ROOT / "artifacts" / "work2_robust_menu" / "phase10_paper_artifacts"

REQUIRED_MANUSCRIPT_FILES = [
    MANUSCRIPT_DIR / "TR_E_WORK2_MANUSCRIPT_DRAFT.md",
    MANUSCRIPT_DIR / "TR_E_WORK2_CLAIM_AUDIT.md",
    MANUSCRIPT_DIR / "TR_E_WORK2_TABLE_FIGURE_SOURCE_MAP.md",
    MANUSCRIPT_DIR / "TR_E_WORK2_PROHIBITED_LANGUAGE_CHECK.md",
    MANUSCRIPT_DIR / "TR_E_WORK2_RESPONSE_TO_INTERNAL_REVIEW.md",
]

REQUIRED_DRAFT_SECTIONS = [
    "Abstract",
    "Introduction",
    "Literature Review",
    "Problem Description",
    "Mathematical Model",
    "Solution Method",
    "Experimental Design",
    "Results",
    "Discussion",
    "Conclusion",
    "Appendix",
]

CLAIM_IDS = [
    "C1_central_adaptive_menu_superiority",
    "C2_product_ablation_value",
    "C3_adaptive_window_increment",
    "C4_menu_construction_value",
    "C5_eta_robustness_boundary",
    "C6_exact_greedy_computational_credibility",
    "C7_provenance_status_transparency",
    "C8_semi_real_case_validation",
]

SOURCE_MAP_COLUMNS = [
    "Source artifact path",
    "Claim ID",
    "Claim status",
    "Allowed manuscript use",
    "Evidence class",
]

PROHIBITED_PATTERNS = [
    r"dominat\w*",
    r"superior(?:ity)?",
    r"outperform\w*",
    r"near[- ]optimal",
    r"real passenger(?: behavior)?",
    r"case-study validation",
    r"semi-real validation",
    r"no-filter recommendation",
    r"operationally recommended",
    r"DSPO_PLUS",
    r"Behavior-Aware",
    r"TR-C",
    r"ranking validation",
    r"adaptive windows improve",
    r"greedy optimal",
]

SAFE_CONTEXT_MARKERS = [
    "not claim",
    "does not claim",
    "not allowed",
    "blocked",
    "diagnostic",
    "scaffold-only",
    "prohibited",
    "avoid",
    "cannot",
    "no ",
    "claim id",
    "current status",
    "manuscript use",
]


def read_text(path):
    return Path(path).read_text(encoding="utf-8")


def assert_required_files_exist():
    missing = [str(path.relative_to(REPO_ROOT)) for path in REQUIRED_MANUSCRIPT_FILES if not path.exists()]
    assert not missing, f"missing manuscript files: {missing}"
    for path in [
        PACKAGE_DIR / "CLAIM_GUARD.json",
        PACKAGE_DIR / "PACKAGE_STATUS.json",
    ]:
        assert path.exists(), f"missing package file: {path.relative_to(REPO_ROOT)}"


def assert_required_sections_present():
    draft = read_text(MANUSCRIPT_DIR / "TR_E_WORK2_MANUSCRIPT_DRAFT.md")
    missing = [
        section
        for section in REQUIRED_DRAFT_SECTIONS
        if not re.search(rf"^##\s+{re.escape(section)}\b", draft, flags=re.MULTILINE)
    ]
    assert not missing, f"missing draft sections: {missing}"


def load_claim_guard():
    return json.loads((PACKAGE_DIR / "CLAIM_GUARD.json").read_text(encoding="utf-8"))


def assert_claim_guard_contract():
    guard = load_claim_guard()
    assert guard["schema_version"] == "phase10-strict-claim-guard-v1"
    assert guard["claim_ready"] is False
    assert guard["manuscript_positive_claims_allowed"] is False
    claims = {claim["claim_id"]: claim for claim in guard["claims"]}
    assert set(CLAIM_IDS).issubset(claims), "claim guard does not cover C1 through C8"


def assert_claim_audit_covers_all_claims():
    text = read_text(MANUSCRIPT_DIR / "TR_E_WORK2_CLAIM_AUDIT.md")
    missing = [claim_id for claim_id in CLAIM_IDS if claim_id not in text]
    assert not missing, f"claim audit missing claim IDs: {missing}"


def assert_source_map_columns_and_paths():
    source_map = read_text(MANUSCRIPT_DIR / "TR_E_WORK2_TABLE_FIGURE_SOURCE_MAP.md")
    missing_columns = [column for column in SOURCE_MAP_COLUMNS if column not in source_map]
    assert not missing_columns, f"source map missing columns: {missing_columns}"

    missing_paths = []
    for row in markdown_rows(source_map):
        cells = split_markdown_row(row)
        if len(cells) < 7 or cells[0].lower() == "manuscript object":
            continue
        source_cell = cells[2]
        for token in source_cell.split(";"):
            path_text = token.strip().strip("`")
            if should_skip_source_path(path_text):
                continue
            path = (REPO_ROOT / path_text).resolve()
            try:
                path.relative_to(REPO_ROOT.resolve())
            except ValueError:
                continue
            if not path.exists():
                missing_paths.append(path_text)
    assert not missing_paths, f"source map cites missing concrete paths: {missing_paths}"


def markdown_rows(text):
    return [line for line in text.splitlines() if line.startswith("|") and not re.match(r"^\|\s*-", line)]


def split_markdown_row(row):
    return [cell.strip() for cell in row.strip().strip("|").split("|")]


def should_skip_source_path(path_text):
    if not path_text:
        return True
    lowered = path_text.lower()
    if "conceptual" in lowered or "migration source only" in lowered:
        return True
    if lowered.startswith("manuscript-created"):
        return True
    if " " in path_text and "/" not in path_text and "\\" not in path_text:
        return True
    return not (
        path_text.startswith("work2_coding/")
        or path_text.startswith(".planning/")
        or path_text.startswith("manuscript/")
        or path_text.startswith("artifacts/")
    )


def assert_prohibited_language_check_has_final_scan():
    text = read_text(MANUSCRIPT_DIR / "TR_E_WORK2_PROHIBITED_LANGUAGE_CHECK.md")
    assert "Final Draft Scan Results" in text
    assert "No unqualified positive claim" in text


def assert_no_unauthorized_positive_language():
    guard = load_claim_guard()
    if guard.get("claim_ready") or guard.get("manuscript_positive_claims_allowed"):
        return
    draft = read_text(MANUSCRIPT_DIR / "TR_E_WORK2_MANUSCRIPT_DRAFT.md")
    regex = re.compile("|".join(f"(?:{pattern})" for pattern in PROHIBITED_PATTERNS), flags=re.IGNORECASE)
    violations = []
    for line_number, line in enumerate(draft.splitlines(), start=1):
        if not regex.search(line):
            continue
        lowered = line.lower()
        if any(marker in lowered for marker in SAFE_CONTEXT_MARKERS):
            continue
        violations.append(f"{line_number}: {line.strip()}")
    assert not violations, "unauthorized positive language found: " + "; ".join(violations)


def main():
    tests = [
        assert_required_files_exist,
        assert_required_sections_present,
        assert_claim_guard_contract,
        assert_claim_audit_covers_all_claims,
        assert_source_map_columns_and_paths,
        assert_prohibited_language_check_has_final_scan,
        assert_no_unauthorized_positive_language,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} manuscript readiness package tests")


if __name__ == "__main__":
    main()
