from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PROTOCOL = REPO_ROOT / ".planning" / "results" / "CALIBRATION_PROTOCOL.md"


def _text():
    assert PROTOCOL.exists(), f"missing protocol: {PROTOCOL}"
    return PROTOCOL.read_text(encoding="utf-8").lower()


def test_required_headings():
    text = _text()
    for heading in [
        "## allowed calibration knobs",
        "## prohibited tuning actions",
        "## pilot selection rule",
        "## pilot and final separation",
        "## final freeze and rerun rule",
        "## second-round limit",
        "## downgrade rule",
    ]:
        assert heading in text, heading


def test_prohibited_boundaries_are_explicit():
    text = _text()
    for phrase in [
        "final-result tuning",
        "seed deletion",
        "split deletion",
        "baseline deletion",
        "metric deletion",
        "generated-row edits",
        "single profit ranking",
    ]:
        assert phrase in text, phrase


def test_allowed_knobs_are_declared():
    text = _text()
    for phrase in [
        "menu_k",
        "max_candidates",
        "eta filter",
        "threshold",
        "opt-out guardrail",
        "uptake regime",
    ]:
        assert phrase in text, phrase


def test_phase4_is_diagnostic_not_tuning_input():
    text = _text()
    assert "phase 4" in text
    assert "diagnostic" in text
    assert "non-tuning input" in text
    assert "not a better ranking" in text


def main():
    tests = [
        test_required_headings,
        test_prohibited_boundaries_are_explicit,
        test_allowed_knobs_are_declared,
        test_phase4_is_diagnostic_not_tuning_input,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} calibration protocol tests")


if __name__ == "__main__":
    main()
