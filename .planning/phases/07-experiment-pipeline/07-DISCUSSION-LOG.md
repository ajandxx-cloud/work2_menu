# Phase 7: Experiment Pipeline - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-30
**Phase:** 07-experiment-pipeline
**Areas discussed:** Smoke test strategy

---

## Smoke Test Strategy

| Option | Description | Selected |
|--------|-------------|----------|
| Run-then-fix | Run smoke_work2_main immediately, fix errors as they appear. Fastest path to discovering real gaps. | ✓ |
| Pre-audit then run | Pre-audit all import chains before running. Slower but catches issues before runtime. | |
| Incremental by method | Start with heuristics, add learning methods one by one. | |

**User's choice:** Run-then-fix
**Notes:** User confirmed infrastructure is ~90% built and preferred fast feedback over pre-audit.

---

## Smoke Test Scope

| Option | Description | Selected |
|--------|-------------|----------|
| Full 6-method run | Run all 6 methods in one go via run_study.py. Single pass, fix whatever breaks. | ✓ |
| Heuristics first, then learning | Split into two runs. Two passes. | |
| One method at a time | Run one method at a time to isolate issues. Slowest. | |

**User's choice:** Full 6-method run
**Notes:** User preferred single-pass execution.

---

## Claude's Discretion

- Oracle menu variant semantics (auto-decided: matches Phase 1 D-03)
- Table/figure output format (auto-decided: use existing build_work2_results_artifacts)
- Specific error fixes during smoke test

## Deferred Ideas

None — discussion stayed within phase scope.
