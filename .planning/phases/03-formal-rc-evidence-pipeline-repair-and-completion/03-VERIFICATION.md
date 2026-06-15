---
phase: 3
phase_name: Formal RC Evidence Pipeline Repair And Completion
status: passed
verified: 2026-06-15T12:15:00+08:00
timezone: Asia/Shanghai
requirements:
  - RC-01
  - RC-02
  - RC-03
  - RC-04
  - RC-05
---

# Phase 3 Verification

## Result

Phase 3 passed its goal: the formal RC evidence pipeline now has inspected
manifests, explicit checkpoint/readiness status, completed comparable formal
rows, generated diagnostic artifacts, and a Phase 4 handoff with readiness,
artifact, and claim-guard boundaries.

This is not a claim-ready manuscript gate. Readiness remains blocked by dirty
git, and generated artifact status remains `blocked`; the phase still passes
because the roadmap success bar allows claim-ready status to remain blocked
while completed comparable formal rows and gate metadata are available.

## Requirement Verification

| Requirement | Status | Evidence |
| --- | --- | --- |
| RC-01 | passed | Formal, pilot, and smoke robust-menu manifests inspected; formal seven-tag family matches `mainline_policy_tags()`. |
| RC-02 | passed | Required checkpoint exists, SHA-256 `d351dd62c3b2cdb008d6952cf81b1b041b64244aa20b82fab9f742b502b7acf4`, readiness load status `loaded`. |
| RC-03 | passed diagnostically | Readiness rerun and blocked non-destructively by `dirty_git`; `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md` records blocker and recommendations. |
| RC-04 | passed | Selected run `formal_robust_menu-20260614T032323Z-c672286a` has 35 completed comparable rows across five splits and seven policies. |
| RC-05 | passed diagnostically | `work2_coding/outputs/phase3_formal_artifacts/` generated through builders; `ARTIFACT_STATUS.json` and `CLAIM_GUARD.json` block unsupported claims. |

## Key Artifacts

| Artifact | Purpose |
| --- | --- |
| `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md` | Dirty-git/readiness diagnosis and checkpoint provenance. |
| `.planning/results/FORMAL_FAILURE_DIAGNOSIS.md` | Selected completed run and preserved failed-run history. |
| `.planning/results/PHASE3_FORMAL_EVIDENCE_HANDOFF.md` | Phase 4 handoff with source run, readiness, artifact status, and claim guard. |
| `work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a/normalized_rows.json` | Formal source rows for Phase 4 diagnosis. |
| `work2_coding/outputs/phase3_formal_artifacts/ARTIFACT_STATUS.json` | Generated artifact gate status. |
| `work2_coding/outputs/phase3_formal_artifacts/manuscript/CLAIM_GUARD.json` | Generated claim boundary. |

## Automated Checks

Run from `work2_coding/`:

| Command | Result |
| --- | --- |
| `python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` | `IMPORT_OK` |
| `python scripts/test_formal_readiness.py` | PASS: 4 formal readiness tests |
| `python scripts/test_checkpoint_provenance.py` | PASS: 6 checkpoint provenance tests |
| `python scripts/test_optout_accounting.py` | PASS: 7 opt-out accounting tests |
| `python scripts/test_policy_fairness_contract.py` | PASS: 15 policy fairness contract tests |
| `python scripts/test_paired_replay_contract.py` | PASS: 12 paired replay contract tests |
| `python scripts/test_study_execution_status.py` | PASS: 9 study execution status tests |
| `python scripts/test_artifact_gates.py` | PASS: 22 artifact gate tests |

## Residual Gates

The following are expected residual gates, not Phase 3 failures:

- Formal readiness status is `blocked` with blocker code `dirty_git`.
- Artifact status is `blocked` because formal rows require
  `outside_option_util` metadata and valid `method_family` metadata for
  claim-ready artifact use.
- Claim guard blocks `empirical_superiority`, `pilot_formal_completed`, and
  other over-strong manuscript claims.

## Phase 4 Readiness

Phase 4 should diagnose the selected 35 formal rows for effect size, paired
split differences, uptake-regime behavior, and claim classification. It should
not upgrade manuscript claims until readiness and artifact gates allow it.
