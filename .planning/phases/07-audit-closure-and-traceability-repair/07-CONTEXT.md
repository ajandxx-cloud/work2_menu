# Phase 07: Audit Closure And Traceability Repair - Context

**Gathered:** 2026-06-11T21:37:19+08:00
**Status:** Ready for execution
**Mode:** Existing plan retained; discussion decisions constrain execution without replanning.
**Language:** Chinese discussion; downstream code, file paths, field names, and requirement IDs remain English.

<domain>
## Phase Boundary

Phase 07 closes the procedural audit gap left by v2.0 before any new empirical evidence work begins. It reconstructs Phase 2 evidence, creates missing Phase 2 verification and validation artifacts, reconciles ACCT/ETA/MENU requirement traceability, and writes a Phase 07 pass/fail gate for whether Phase 08 may proceed.

This phase must not change algorithm behavior. Code edits are allowed only for small deterministic script-style tests that prove existing behavior. It must not rerun or reinterpret generated empirical results, supply missing checkpoints, strengthen attention or robust-menu claims, or expand into repository hygiene work owned by Phase 08.

</domain>

<decisions>
## Implementation Decisions

### Existing Plan Handling
- **D-01:** Keep `.planning/phases/07-audit-closure-and-traceability-repair/07-PLAN.md` as the execution plan. This discussion captures execution constraints and does not require replanning.

### MENU-02 Evidence Standard
- **D-02:** `MENU-02` must use a strict completion standard. Mark it complete only if existing tests or a new small deterministic script-style test explicitly proves that compared policies use consistent pricing and system-aware cost definitions and that those fields are recorded in metadata or normalized rows.
- **D-03:** If `MENU-02` has only code-reading evidence, indirect manifest evidence, or incomplete metadata evidence, keep it pending and record it as an explicit residual gap in `02-VERIFICATION.md`, `02-VALIDATION.md`, and Phase 07 verification.
- **D-04:** If `MENU-02` reveals an actual behavior inconsistency rather than a documentation/test gap, Phase 07 must block Phase 08.

### Verification Depth
- **D-05:** Phase 07 may add or extend small deterministic tests under `work2_coding/scripts/test_*.py` when an already implemented behavior needs command-backed proof.
- **D-06:** These tests may verify contracts, row metadata, pricing/cost consistency, opt-out accounting, ETA diagnostics, checkpoint metadata, and solver telemetry. They must not change algorithm behavior, tune policies, modify generated result rows, or alter empirical conclusions.
- **D-07:** Existing script-style tests remain the preferred verification pattern: direct `python scripts/test_*.py` commands with deterministic assertions and `PASS: N tests` output.

### Nyquist Validation Scope
- **D-08:** Phase 07 must create `.planning/phases/02-core-semantics-and-robust-menu-logic/02-VALIDATION.md` because `workflow.nyquist_validation=true` and Phase 2 is the direct audit blocker.
- **D-09:** Phase 07 should not create Phase 1, 3, 4, 5, or 6 validation files. Instead, `07-VALIDATION.md` must register those missing validation files as milestone-level residual gaps and recommend follow-up handling.

### Phase 08 Gate
- **D-10:** Phase 08 may proceed only if ACCT-01..04, ETA-01..04, MENU-01, MENU-03, and MENU-04 are no longer orphaned and have Phase 2 verification rows with command-backed evidence or explicit status.
- **D-11:** A `MENU-02` evidence-only gap may be carried as a non-blocking residual gap because Phase 08 is repository hygiene/provenance freeze, not pricing semantics implementation.
- **D-12:** If any required command fails, if ACCT/ETA/MENU core behavior is contradicted by tests, or if `MENU-02` exposes actual policy-comparison inconsistency, Phase 07 verification must state that Phase 08 is blocked.

### the agent's Discretion
- The agent may choose exact test helper names, verification table formatting, and validation headings as long as the decisions above are preserved.
- The agent may decide whether `MENU-02` is proven by extending an existing test or by adding a focused companion script, provided the command output is recorded.
- The agent may mark requirements complete only where the verification artifact contains concrete evidence. Unsupported items must remain explicit gaps rather than being inferred from plans alone.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Scope And Audit Source
- `AGENTS.md` - Active runtime root, research guardrails, and verification baseline.
- `.planning/PROJECT.md` - v2.1 objective, active requirements, key decisions, and evidence-ladder constraints.
- `.planning/REQUIREMENTS.md` - TRACE-01..05 and Phase 2 ACCT/ETA/MENU traceability status.
- `.planning/ROADMAP.md` - Phase 07 goal, success criteria, and Phase 08 boundary.
- `.planning/STATE.md` - Current milestone state and Phase 07 plan reference.
- `.planning/v2.0-MILESTONE-AUDIT.md` - Source of truth for the Phase 2 orphan gap, `MENU-02` concern, and missing Nyquist validation.

### Phase 07 Plan
- `.planning/phases/07-audit-closure-and-traceability-repair/07-PLAN.md` - Existing execution plan retained after discussion.

### Phase 2 Evidence To Reconstruct
- `.planning/phases/02-core-semantics-and-robust-menu-logic/02-CONTEXT.md` - Phase 2 locked decisions for opt-out accounting, checkpoint metadata, robust ETA filters, objective penalties, and solver diagnostics.
- `.planning/phases/02-core-semantics-and-robust-menu-logic/02-01-SUMMARY.md` - Runtime/parser and DSPO menu exposure evidence.
- `.planning/phases/02-core-semantics-and-robust-menu-logic/02-02-SUMMARY.md` - Opt-out and structured passenger outcome implementation evidence.
- `.planning/phases/02-core-semantics-and-robust-menu-logic/02-03-SUMMARY.md` - Checkpoint provenance implementation evidence.
- `.planning/phases/02-core-semantics-and-robust-menu-logic/02-04-SUMMARY.md` - Robust ETA filter, objective, and solver telemetry evidence; note that `MENU-02` was not completed here.
- `.planning/phases/02-core-semantics-and-robust-menu-logic/02-RESEARCH.md` - Phase 2 research findings and risk context.

### Runtime Integration Points
- `work2_coding/Src/Algorithms/DSPO_Menu.py` - Menu pricing, ETA filtering, objective scoring, soft-penalty behavior, exact/greedy diagnostics, and metadata.
- `work2_coding/Src/paired_replay.py` - Normalized row fields, checkpoint metadata, pricing field propagation, and paired row validation.
- `work2_coding/Src/experiment_contracts.py` - Manifest validation, paired fields, checkpoint requirements, and uptake-regime validation.
- `work2_coding/Src/policy_adapters.py` - Policy tag overrides and fairness boundaries.
- `work2_coding/Src/study_execution.py` - Actual/contract execution metadata and aggregate row behavior.

### Verification Commands And Tests
- `work2_coding/scripts/test_menu_runtime_contract.py` - Runtime parser/menu contract checks.
- `work2_coding/scripts/test_optout_accounting.py` - ACCT outcome and route/service accounting checks.
- `work2_coding/scripts/test_checkpoint_provenance.py` - Checkpoint status and provenance checks.
- `work2_coding/scripts/test_robust_menu_logic.py` - ETA filter, soft-penalty, objective, and solver diagnostics checks.
- `work2_coding/scripts/test_experiment_contracts.py` - Study manifest and parser contract checks.
- `work2_coding/scripts/test_policy_fairness_contract.py` - Policy override and paired fairness checks.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `work2_coding/scripts/test_*.py` scripts already follow direct deterministic assertions and `PASS: N tests` output. Phase 07 should reuse this style for any added evidence.
- `work2_coding/Src/Algorithms/DSPO_Menu.py` already exposes pricing mode fields, ETA filter modes, soft-penalty metadata, and solver diagnostics that can be audited for MENU/ETA requirements.
- `work2_coding/Src/paired_replay.py` already carries normalized row fields such as `checkpoint_load_status`, `pricing`, `filter_mode`, and opt-out/accepted outcome counts.

### Established Patterns
- Use `work2_coding/` as the active runtime root. `.planning/codebase/` documents still contain stale `ooh_code/` paths and should be treated as historical risk context unless revalidated against current files.
- Raw outputs and empirical artifacts must not be hand-edited. Verification should rely on command outputs, code-backed tests, and planning artifacts.
- Requirement status should be conservative: complete only with verification evidence; otherwise pending or explicit gap.

### Integration Points
- Phase 07 should write `02-VERIFICATION.md` and `02-VALIDATION.md` in the Phase 2 directory, then write `07-SUMMARY.md`, `07-VERIFICATION.md`, and `07-VALIDATION.md` in the Phase 07 directory.
- `.planning/REQUIREMENTS.md` should be updated only where Phase 2 verification rows support the new status.
- Phase 07 verification is the gate that determines whether Phase 08 repository hygiene work may begin.

</code_context>

<specifics>
## Specific Ideas

- For `MENU-02`, prefer a focused deterministic test that compares two policy settings and asserts shared pricing/system-aware cost fields are either identical where required or explicitly recorded as varied fields.
- In `07-VALIDATION.md`, list missing Phase 1/3/4/5/6 validation files as residual Nyquist gaps rather than generating them in this phase.
- In `02-VERIFICATION.md`, make `MENU-02` visually distinct from the other rows so future audits can see whether it was completed or carried as a residual gap.
- Phase 08 can proceed with a non-blocking `MENU-02` evidence gap only if there is no evidence of actual pricing/cost inconsistency.

</specifics>

<deferred>
## Deferred Ideas

- Creating validation files for Phase 1, 3, 4, 5, and 6 is deferred beyond Phase 07 unless a later milestone audit requires full Nyquist closure before archive.
- Repository hygiene classification, `.gitignore` cleanup, and provenance freeze are deferred to Phase 08.
- Real shared checkpoint training remains deferred to Phase 09.
- Pilot/formal attention evidence and claim decisions remain deferred to Phases 10-13.

</deferred>

---

*Phase: 07-Audit Closure And Traceability Repair*
*Context gathered: 2026-06-11T21:37:19+08:00*
