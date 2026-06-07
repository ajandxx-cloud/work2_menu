# Roadmap: Work2_ChoiceAware_DRT_Menu_Optimization

**Created:** 2026-06-04
**Mode:** standard research phases
**Default next command:** `$gsd-plan-phase 1`

## Phase 1: Reframe Project And 6.4 Discussion

**Goal:** Replace the old CNN-SetMenuNet-first narrative with a choice-aware / profit-aware Work 2 project framing and a clean 6.4 experimental redesign document.
**Requirements:** FRAME-01..FRAME-04, VER-01..VER-04
**Status:** Complete - 2026-06-04
**Verification:** `.planning/phases/01-reframe-project-and-6-4-discussion/VERIFICATION.md`

**Success Criteria:**
1. `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, and `.planning/STATE.md` exist and reflect the new objective.
2. `实验讨论重构6.4.md` is rewritten as a structured action plan, not just a raw discussion transcript.
3. The document states that CNN-SetMenuNet is retained as a baseline / diagnostic method.
4. The document defines the main claim around expected profit, service guardrails, and oracle alignment.
5. Verification records that no Work 1 pricing, choice, or routing core was changed.

## Phase 2: Objective Metrics And Oracle Diagnostics

**Goal:** Add objective-aligned metrics and oracle taxonomy so profit, service quality, and menu-quality claims no longer point to different targets.
**Requirements:** OBJ-01..OBJ-04, ORCL-01..ORCL-04, VER-01..VER-04
**Status:** Complete - 2026-06-04
**Verification:** `.planning/phases/02-objective-metrics-and-oracle-diagnostics/VERIFICATION.md`
**Plans:** 1/1 plans complete

**Success Criteria:**
1. Normalized rows include raw `net_profit` plus adjusted or service-constrained profit.
2. Diagnostic reports identify high-quit false-positive outcomes.
3. Cost Oracle and Profit Oracle are named and computed or clearly separated in artifact prose.
4. Existing formal results can be reinterpreted without claiming Cost Oracle is a profit upper bound.
5. Smoke checks confirm existing artifact generation still works.

## Phase 3: Expected-Profit Enumeration Policies

**Goal:** Implement exact choice-aware menu enumeration and service-constrained selection for the default Work 2 setting.
**Requirements:** METH-01..METH-06, VER-01..VER-04
**Status:** Complete - 2026-06-04
**Context:** `.planning/phases/03-expected-profit-enumeration-policies/03-CONTEXT.md`
**Verification:** `.planning/phases/03-expected-profit-enumeration-policies/VERIFICATION.md`
**Plans:** 1/1 plans complete

**Success Criteria:**
1. A new Expected-Profit Enumeration policy enumerates all `C(10,3)=120` menus when `K=10`, `L=3`.
2. Home is always shown outside `L`, preserving existing public menu semantics.
3. Each menu is scored using MNL choice probability, expected revenue, expected route cost, and opt-out penalty/guardrail.
4. A Service-Constrained Expected-Profit policy selects a feasible high-profit menu or emits a diagnostic fallback.
5. New policies are available through CLI/parser, study manifests, normalized rows, and artifact summaries.

## Phase 4: Phase08 Pilot And Decision Gate

**Goal:** Run smoke and 3-seed pilot evidence before committing to formal experiments.
**Requirements:** PILOT-01..PILOT-04, VER-01..VER-04
**Status:** Complete - 2026-06-05
**Context:** `.planning/phases/04-phase08-pilot-and-decision-gate/04-CONTEXT.md`
**Research:** `.planning/phases/04-phase08-pilot-and-decision-gate/04-RESEARCH.md`
**Validation:** `.planning/phases/04-phase08-pilot-and-decision-gate/04-VALIDATION.md`
**Plans:** 1/1 plans complete

**Success Criteria:**
1. Smoke study completes on a minimal RC setting.
2. Pilot study runs RC, `K=10`, `L=3`, home always shown, seeds `0,1,2`.
3. Outputs are written to `results/work2_phase08_redesign/` or an equivalent committed artifact path:
   - `pilot_rows.csv`
   - `pilot_summary.md`
   - `oracle_diagnostics.md`
   - `profit_vs_quit_tradeoff.md`
   - `phase08_decision.md`
4. `phase08_decision.md` decides whether to proceed to formal, recalibrate objective parameters, or diagnose scenario design.
5. No formal claim is made before the pilot decision is positive.

## Phase 5: Formal Evidence And Manuscript Artifacts

**Goal:** Produce formal multi-seed evidence and paper-ready artifacts if the pilot supports the new objective.
**Requirements:** FORM-01..FORM-04, VER-01..VER-04

**Success Criteria:**
1. Formal study runs at least five seeds with approved RC settings.
2. Tables compare Nearest-L, Cost-L, CNN-Menu, old CNN-SetMenuNet, Expected-Profit Enumeration, Service-Constrained Expected-Profit, Cost Oracle, and Profit Oracle.
3. Main tables include raw net profit, adjusted/service-constrained profit, quit rate, average walk, route cost, menu regret, and runtime.
4. Artifact builder creates committed snapshots, tables, figures, and summary markdown.
5. Manuscript-facing conclusion wording states the evidence level precisely.

## Phase 6: Objective / Service-Constraint Redesign

**Goal:** Locally pivot from ProfitAware Learning to objective/service-constraint redesign after Phase 5 failed closed. Determine whether current choice-aware profit menu optimization can be repaired without changing MNL choice, Lambert-W pricing, HGS/Hygese routing, or CNN learning. ProfitAware Learning is deferred until a redesigned non-learning objective passes the Phase 6 gate.
**Requirements:** REDESIGN-01..REDESIGN-07, VER-01..VER-04
**Status:** Complete - 2026-06-07
**Verification:** `.planning/phases/06-objective-service-constraint-redesign/VERIFICATION.md`

**Success Criteria:**
1. Phase 6 planning records that Phase 1-5 remain diagnostic background and formal evidence remains blocked.
2. Three non-learning redesigned policies are implemented and tested: Risk-Adjusted Expected-Profit, Min-Quit-Then-Profit, and Service-Guarded Expected-Profit.
3. Smoke and 3-seed diagnostic manifests run only phase-local redesign evidence.
4. Phase-local artifacts decide exactly one gate state: `proceed_to_formal`, `continue_redesign`, or `conclude_method_unsuitable`.
5. No manuscript-facing artifacts are written unless a later confirmed gate explicitly unlocks formal evidence.

## Phase Verification Rule

Every phase must produce a verification note answering:

1. Which files changed?
2. Did pricing, MNL choice, or HGS routing core change?
3. Which smoke or study command was run?
4. Which CSV/markdown artifacts were generated?
5. Does the current result support the paper conclusion?
6. What is the next phase decision?

## Requirement Coverage

All v1 requirements in `.planning/REQUIREMENTS.md` are mapped to exactly one phase.

---
*Roadmap created: 2026-06-04*
