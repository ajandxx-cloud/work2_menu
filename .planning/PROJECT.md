# Akkerman RC No-Failure-Cost Reproduction

## What This Is

This project reproduces the Akkerman DSPO synthetic RC experiment in the current `work2_coding/` runtime while removing home-delivery failure cost from the actual objective, training reward, evaluation metrics, and result summaries.

## Core Value

Produce a defensible Table-2-style RC reproduction where failure cost is truly absent rather than subtracted after the fact.

## Requirements

### Validated

(None yet - ship to validate)

### Active

- [ ] Run the RC synthetic setting from `work2_coding/` without creating `ooh_code/`.
- [ ] Support exact NoOOH and OnlyOOH baselines without price-only approximations.
- [ ] Disable customer exit for the reproduction with `outside_option_util=None`.
- [ ] Produce raw CSV, summary CSV, and summary JSON with failure costs fixed at zero.
- [ ] Preserve manuscript, figures, revision notes, and historical result artifacts.

### Out of Scope

- New DSPO methodology - this is a reproduction and accounting repair.
- Attention, DRPO, SPO, Yanjiao/DRT extensions, and robust-menu claim generation.
- Hand-editing generated result rows or paper artifacts.

## Context

The current runnable code lives in `work2_coding/`. Existing `.planning/codebase/` maps mention `ooh_code/`, but those references are stale for this reproduction. The relevant runtime files are parser/config, `run.py`, `run_ppo.py`, legacy algorithms, choice/environment code, and new experiment scripts/tests under `work2_coding/`.

## Constraints

- **Runtime root**: Use `work2_coding/` only.
- **Accounting**: Home failure probability and cost must be zero in the real runtime configuration.
- **Choice model**: No outside option or quit-threshold behavior in the reproduction.
- **Artifacts**: Do not modify manuscript text, revision notes, figures, related-work files, or historical results.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Map `ooh_code/` scope to `work2_coding/` | Current filesystem has no `ooh_code/`; AGENTS says `work2_coding/` is active. | Pending |
| Add exact service modes | NoOOH/OnlyOOH must be verified by behavior, not extreme prices. | Pending |
| Keep PPO outside default table | Required for CLI compatibility, not for the requested minimum algorithm set. | Pending |

## Evolution

Update this document only when the reproduction scope changes or after the experiment is verified.

---
*Last updated: 2026-06-12 after reproduction initialization*
