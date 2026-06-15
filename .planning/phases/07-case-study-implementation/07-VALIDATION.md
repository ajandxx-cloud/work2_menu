---
phase: 07
slug: case-study-implementation
status: draft
nyquist_compliant: true
wave_0_complete: false
created: 2026-06-15T22:17:18+08:00
timezone: Asia/Shanghai
---

# Phase 7 Validation Strategy

## Test Infrastructure

| Property | Value |
| --- | --- |
| Framework | Script-style Python assertions and planning-side validator |
| Config file | none |
| Quick run command | `python .planning/data/case_studies/validate_case_contracts.py --root .planning/data/case_studies --write-summary` |
| Full suite command | `cd work2_coding; python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"; cd ..; python .planning/data/case_studies/test_case_contracts.py; python .planning/data/case_studies/validate_case_contracts.py --root .planning/data/case_studies --write-summary` |
| Estimated runtime | under 10 seconds |

## Sampling Rate

- After every task commit: run the quick validator command.
- After every plan wave: run the full suite command.
- Before `$gsd-verify-work`: full suite must be green and `VALIDATION_SUMMARY.md`
  must contain no `blocking` findings.
- Max feedback latency: 10 seconds.

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Secure Behavior | Test Type | Automated Command | File Exists | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 07-01-01 | 07-01 | 1 | CASE-03 | Contracts stay planning-side and include required blockers and labels | contract | `python .planning/data/case_studies/validate_case_contracts.py --root .planning/data/case_studies --write-summary` | W0 | pending |
| 07-01-02 | 07-01 | 1 | CASE-03 | Seven-tag family and paired-field vocabulary are inherited without runtime YAML creation | contract | `python .planning/data/case_studies/validate_case_contracts.py --root .planning/data/case_studies --write-summary` | W0 | pending |
| 07-02-01 | 07-02 | 2 | CASE-03 | Validator reports blocking/warning/info and does not inspect real external data | unit | `python .planning/data/case_studies/test_case_contracts.py` | W0 | pending |
| 07-02-02 | 07-02 | 2 | CASE-05 | Planning docs record Phase 7 as scaffolded, not skipped, and execution remains blocked | source | `python .planning/data/case_studies/validate_case_contracts.py --root .planning/data/case_studies --write-summary` | W0 | pending |

## Wave 0 Requirements

- `.planning/data/case_studies/validate_case_contracts.py` - planning-side
  contract validator.
- `.planning/data/case_studies/test_case_contracts.py` - self-test for
  validator behavior.
- `.planning/data/case_studies/source_contracts.yaml` - route/source metadata
  input for validator.
- `.planning/data/case_studies/case_manifest_draft.yaml` - planning-side
  manifest draft input for validator.

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
| --- | --- | --- | --- |
| No overclaiming in prohibitive manuscript placeholders | CASE-03, CASE-05 | Claims can be semantically too strong while still schema-valid | Read `.planning/data/case_studies/claim_boundary_placeholders.md` and verify it says no case evidence yet, no real passenger validation, and no claim upgrade. |

## Validation Sign-Off

- [x] All planned tasks have automated or explicit manual verification.
- [x] Sampling continuity: no three consecutive tasks without automated verify.
- [x] Wave 0 covers all missing validation infrastructure.
- [x] No watch-mode flags.
- [x] Feedback latency under 10 seconds.
- [x] `nyquist_compliant: true` set in frontmatter.

**Approval:** pending Phase 7 execution.
