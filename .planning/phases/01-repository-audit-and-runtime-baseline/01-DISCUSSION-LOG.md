# Phase 1: Repository Audit And Runtime Baseline - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md; this log preserves the alternatives considered.

**Date:** 2026-06-11
**Phase:** 1-Repository Audit And Runtime Baseline
**Areas discussed:** runtime root, baseline depth, menu asset audit, report shape, side-effect boundary, runner smoke boundary, audit output location, stale codebase maps, patch-plan scope, blocker priority, verification command reporting, phase completion standard

---

## Runtime Root

| Option | Description | Selected |
|--------|-------------|----------|
| 1A | Lock `work2_coding/` as the only current runtime root; mark `ooh_code/` as stale map references. | yes |
| 1B | Temporarily lock `work2_coding/`, but keep an external-root caveat. | |
| 1C | Continue treating `work2_coding/` and `ooh_code/` as competing roots. | |

**User's choice:** 1A
**Notes:** Phase 1 should not create or preserve a parallel `ooh_code/` implementation path.

---

## Baseline Verification Depth

| Option | Description | Selected |
|--------|-------------|----------|
| 2A | Record only the lightweight `import Src.config` smoke. | |
| 2B | Add minimal config/entrypoint audit: `Config`, `run.py`, `run_ppo.py`, `parser.py`, and `DSPO_Menu` parameter gaps. | yes |
| 2C | Try a tiny episode or runner smoke, accepting dependency/HGS/parameter failures. | |

**User's choice:** 2B
**Notes:** The audit should be more informative than a single import smoke, but still avoid running episodes.

---

## Menu Asset Audit Position

| Option | Description | Selected |
|--------|-------------|----------|
| 3A | Write the Phase 1 conclusion that `DSPO_Menu.py` exists, but CLI/parser/runner contracts are missing or inconsistent. | yes |
| 3B | List this only as a Phase 2 risk. | |
| 3C | Make `DSPO_Menu.py` the main audit object and summarize all strategy/ETA/solver details. | |

**User's choice:** 3A
**Notes:** Capture the asset/blocker clearly without turning Phase 1 into a full behavior review.

---

## Stage 0 Report Shape

| Option | Description | Selected |
|--------|-------------|----------|
| 4A | Short audit checklist plus minimal patch plan. | yes |
| 4B | Full code-map update plus risk matrix plus verification commands. | |
| 4C | Short body with detailed appendix. | |

**User's choice:** 4A
**Notes:** Optimize for a concise audit that gets the project ready for planning Phase 2.

---

## Config Construction Side Effects

| Option | Description | Selected |
|--------|-------------|----------|
| 5A | Use static/low-side-effect checks; avoid creating experiment directories or redirecting stdout. | yes |
| 5B | Allow a minimal temporary run directory if recorded. | |
| 5C | Require actual `Config` construction even if it creates directories. | |

**User's choice:** 5A
**Notes:** `Config(args)` creates directories and alters stdout behavior, so Phase 1 should inspect rather than execute it.

---

## Runner Smoke Boundary

| Option | Description | Selected |
|--------|-------------|----------|
| 6A | Inspect `run.py` / `run_ppo.py` entrypoints and imports only; do not execute episodes. | yes |
| 6B | Try a `--max_episodes 1`-level run and record failure without fixing. | |
| 6C | Require one minimal episode to pass. | |

**User's choice:** 6A
**Notes:** Episode-level execution is outside Phase 1.

---

## Audit Report File

| Option | Description | Selected |
|--------|-------------|----------|
| 7A | Create `.planning/phases/01-repository-audit-and-runtime-baseline/01-STAGE0-AUDIT.md`. | yes |
| 7B | Update `.planning/research/SUMMARY.md` instead. | |
| 7C | Create `work2_coding/STAGE0_AUDIT.md`. | |

**User's choice:** 7A
**Notes:** Keep the audit in the phase directory as a GSD phase artifact.

---

## Stale Codebase Map Handling

| Option | Description | Selected |
|--------|-------------|----------|
| 8A | Mark `.planning/codebase/*` `ooh_code/` references as stale in the report only; do not bulk-edit maps. | yes |
| 8B | Rewrite `.planning/codebase/` paths to `work2_coding/`. | |
| 8C | Regenerate the code maps as part of Phase 1. | |

**User's choice:** 8A
**Notes:** The maps remain historical context, not authoritative current path truth.

---

## Minimal Patch Plan Scope

| Option | Description | Selected |
|--------|-------------|----------|
| 9A | List future fixes only; do not modify algorithm behavior in Phase 1. | yes |
| 9B | Allow a tiny compatibility patch such as exposing `DSPO_Menu`. | |
| 9C | Fix blockers immediately if found. | |

**User's choice:** 9A
**Notes:** Phase 1 output is audit plus patch plan, not runtime repair.

---

## Menu Entrypoint Priority

| Option | Description | Selected |
|--------|-------------|----------|
| 10A | Treat parser/runner menu exposure as the highest-priority blocker. | yes |
| 10B | Rank it equally with opt-out and checkpoint risks. | |
| 10C | Put opt-out/checkpoint first; menu exposure is engineering cleanup. | |

**User's choice:** 10A
**Notes:** Existing menu assets are not useful for robust comparisons until exposed through a stable runtime contract.

---

## Verification Command Reporting

| Option | Description | Selected |
|--------|-------------|----------|
| 11A | Record executed commands separately from suggested commands; mark unrun commands `not run`. | yes |
| 11B | List only suggested commands. | |
| 11C | Keep command listing minimal to avoid staleness. | |

**User's choice:** 11A
**Notes:** Avoid implying that runner or episode smokes have already passed.

---

## Phase 1 Completion Standard

| Option | Description | Selected |
|--------|-------------|----------|
| 12A | Planner should plan audit plus minimal patch plan only; no runtime fix required for Phase 1 completion. | yes |
| 12B | Planner should include a small parser/runner patch. | |
| 12C | Planner should include audit, parser/runner repair, and smoke execution to runnable state. | |

**User's choice:** 12A
**Notes:** Runtime fixes belong to later phases unless explicitly re-scoped.

---

## The Agent's Discretion

- The agent may choose the concise structure for the Stage 0 audit.
- The agent may perform additional low-side-effect static inspections when useful.

## Deferred Ideas

- Parser/runner menu-mode repair.
- Opt-out accounting repair.
- Explicit checkpoint load status and provenance.
- Robust ETA filter, menu objective, exact/greedy behavior, and replay contracts.
