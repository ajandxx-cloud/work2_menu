import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
FROZEN = REPO_ROOT / ".planning" / "results" / "FROZEN_FINAL_SETTINGS.md"


def _text():
    assert FROZEN.exists(), f"missing frozen settings: {FROZEN}"
    return FROZEN.read_text(encoding="utf-8").lower()


def test_status_is_valid():
    text = _text()
    match = re.search(r"final_status:\s*([a-z_]+)", text)
    assert match, "missing final_status"
    assert match.group(1) in {"frozen", "blocked_pending_gate_cleanup", "conditional_reframe_selected"}


def test_required_contract_details_present():
    text = _text()
    for phrase in [
        "final manifest path",
        "final manifest hash",
        "calibration manifest path",
        "calibration manifest hash",
        "seven policy tags",
        "split ids and seeds",
        "checkpoint path",
        "checkpoint hash",
        "paired fields",
        "varied fields",
        "gate commands",
    ]:
        assert phrase in text, phrase


def test_blocked_gates_do_not_authorize_final_rerun():
    text = _text()
    if "final_status: blocked_pending_gate_cleanup" in text:
        assert "final rerun is not authorized" in text
        assert "dirty_git" in text
        assert "artifact status" in text


def test_downgrade_rule_after_second_final_failure():
    text = _text()
    assert "second final" in text
    assert "conditional service-menu design framing" in text


def main():
    tests = [
        test_status_is_valid,
        test_required_contract_details_present,
        test_blocked_gates_do_not_authorize_final_rerun,
        test_downgrade_rule_after_second_final_failure,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} frozen final settings tests")


if __name__ == "__main__":
    main()
