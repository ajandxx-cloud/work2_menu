---
phase: 2
phase_name: Paper-Level Research Design Lock
plan: 1
type: docs
status: ready
wave: 1
depends_on:
  - phase-1-repository-audit-and-state-locking
files_modified:
  - .planning/paper/TR_E_RESEARCH_DESIGN.md
autonomous: true
requirements_addressed:
  - PAPER-01
  - PAPER-02
  - PAPER-03
  - PAPER-04
  - PAPER-05
requirements:
  - PAPER-01
  - PAPER-02
  - PAPER-03
  - PAPER-04
  - PAPER-05
must_haves:
  truths:
    - "D-01: Use strong-claim reserved framing; any conclusion for optimized adaptive m+w+p service menus must be explicitly gated on formal readiness, paired formal rows, artifact status, and claim guard approval."
    - "D-02: Do not present smoke, pilot, diagnostic, blocked, placeholder, or status-only outputs as empirical superiority evidence."
    - "D-03: Include a four-level claim ladder: strong, conditional, weak-diagnostic, unsupported."
    - "D-04: Define a strong central claim as profit-service-quality joint improvement, not net-profit dominance alone."
    - "D-05: If strong evidence is unsupported, route to Phase 5 calibrated rerun before manuscript claim progression."
    - "D-06: Produce a complete paper-level mathematical skeleton with sets, indices, requests, vehicles, candidate points, service bundles, menu variables, MNL probability, expected profit, guardrails, ETA/window feasibility, and exact/greedy solver definitions."
    - "D-07: Define a displayed service bundle as (meeting point, pickup time window, price), with accepted home pickup allowed as a service bundle."
    - "D-08: Keep outside option separate from service bundles and accepted home pickup; it is a refusal/lost-demand state for choice and opt-out accounting."
    - "D-09: Treat pickup time window and ETA/window feasibility as core service-product dimensions; keep no-filter diagnostic only."
    - "D-10: Define exact menu optimization as the small-scale benchmark and greedy forward selection as the online scalable algorithm, with candidate count, enumerated count, build time, exact gap, and overlap diagnostics."
    - "D-11: Map the central claim to the full seven-tag mainline family: mainline_optimized_adaptive versus mainline_no_menu, mainline_fixed_menu, mainline_random_menu, mainline_optimized_m, mainline_optimized_mw, and mainline_optimized_fixed_window."
    - "D-12: Use profit primary plus service guardrails: net_profit, adjusted_profit, service_constrained_net_profit, acceptance_rate, opt_out_rate, home_only_share, non_home_uptake, and service guardrail behavior."
    - "D-13: Require paired replay evidence with the same split, seed/request trace, checkpoint provenance, pricing settings, routing/HGS settings, and paired differences for all main claims."
    - "D-14: Exclude unsupported claims from positive manuscript claims; unsupported results may appear only in diagnosis, limitations, or redesign rationale."
    - "D-15: Define a complete paper table plan covering experimental design, policy comparison, main paired results, product/window ablation, ETA robustness, exact-vs-greedy, and provenance/status."
    - "D-16: Define mechanism, result, and diagnostic figure families covering service-menu schematic, profit-service tradeoff, acceptance/opt-out behavior, ETA/risk filtering, and exact-greedy diagnostics."
    - "D-17: Keep attention V2/diagnostic only unless a later phase explicitly changes scope with independent evidence."
    - "D-18: Keep no-filter as diagnostic, upper-bound, or stress-test evidence only, not an operational recommendation."
    - "D-19: Keep real or semi-real case study optional and gated by Phase 6 feasibility; do not pre-commit it as main evidence in Phase 2."
  artifacts:
    - .planning/paper/TR_E_RESEARCH_DESIGN.md
  key_links:
    - .planning/PROJECT.md
    - .planning/REQUIREMENTS.md
    - .planning/ROADMAP.md
    - .planning/STATE.md
    - .planning/STATE_LOCK.md
    - .planning/research/SUMMARY.md
    - .planning/phases/02-paper-level-research-design-lock/02-CONTEXT.md
    - .planning/phases/02-paper-level-research-design-lock/02-RESEARCH.md
    - work2_coding/Src/Algorithms/DSPO_Menu.py
    - work2_coding/Src/policy_adapters.py
    - work2_coding/Src/paired_replay.py
    - work2_coding/Src/artifact_status.py
---

# Phase 2 Plan: Paper-Level Research Design Lock

<objective>
Write `.planning/paper/TR_E_RESEARCH_DESIGN.md` as the paper-level design
contract for the Work2 TR Part E service-menu optimization paper. The document
must define the contribution boundary, mathematical model skeleton, V1 evidence
family, claim-to-evidence map, table/figure plan, and non-claim gates before any
formal experiment or manuscript claim upgrade.
</objective>

<scope>
## In Scope

- Create or update `.planning/paper/TR_E_RESEARCH_DESIGN.md`.
- Use current `work2_coding/` runtime contracts as evidence anchors.
- Define the mathematical model skeleton and notation at paper-design level.
- Map each planned claim to policy comparisons, metrics, artifacts, and gates.
- Define main tables and figures before formal execution.
- Keep all user-facing prose in Chinese where practical; keep code paths,
  metric names, policy tags, and commands in English.

## Out Of Scope

- Running formal replay, pilot replay, smoke replay, or checkpoint training.
- Editing algorithm behavior, manifests, generated rows, generated tables,
  generated figures, or manuscript claim text.
- Treating current smoke/pilot/diagnostic/status outputs as empirical claims.
- Reviving or creating an `ooh_code/` runtime root.
- Adding attention-based choice/scoring to the V1 contribution.
</scope>

<tasks>
## Task 1: Establish Design Evidence And Output Location

**Type:** docs
**Files:** `.planning/paper/TR_E_RESEARCH_DESIGN.md`,
`.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`,
`.planning/STATE_LOCK.md`,
`.planning/phases/02-paper-level-research-design-lock/02-CONTEXT.md`,
`.planning/phases/02-paper-level-research-design-lock/02-RESEARCH.md`

**Action:**

1. Create `.planning/paper/` if it does not exist.
2. Read the Phase 2 context, research notes, roadmap success criteria, and
   requirements `PAPER-01` through `PAPER-05`.
3. Add frontmatter to `TR_E_RESEARCH_DESIGN.md` with phase, status,
   generated timestamp, requirements covered, evidence status, and claim gate
   boundary.
4. State explicitly that the design is documentary and does not run or alter
   formal evidence.

**Verify:**

- The target file exists at `.planning/paper/TR_E_RESEARCH_DESIGN.md`.
- The frontmatter lists `PAPER-01`, `PAPER-02`, `PAPER-03`, `PAPER-04`,
  and `PAPER-05`.
- The document states that current evidence is not yet claim-ready.

**Acceptance Criteria:**

- A downstream executor or reviewer can identify the source, scope, and
  evidence status of the design document without reading the whole repository.

## Task 2: Define Paper Positioning, Service Product, And Non-Claims

**Type:** docs
**Files:** `.planning/paper/TR_E_RESEARCH_DESIGN.md`,
`.planning/research/SUMMARY.md`,
`work2_coding/artifacts/work2_robust_menu/manuscript/method_outline.md`,
`work2_coding/artifacts/work2_robust_menu/manuscript/result_outline.md`

**Action:**

1. Write the paper positioning as TR Part E service-menu optimization for
   many-to-one DRT.
2. Define the displayed service bundle as `(meeting point, pickup time window,
   price)`.
3. Explain accepted home pickup as a service bundle and outside option as
   refusal/lost demand, not accepted service.
4. Define V1 main evidence, V2 attention diagnostics, appendix/diagnostic
   evidence, and non-claims.
5. Include explicit boundaries for no-filter diagnostics, optional case study,
   and blocked/status-only evidence.

**Verify:**

- The document satisfies `PAPER-01`, `PAPER-02`, and `PAPER-04`.
- It contains the terms `mainline_optimized_adaptive`, `outside option`,
  `accepted home`, `attention`, and `no-filter`.
- It does not claim current empirical superiority.

**Acceptance Criteria:**

- The paper contribution can no longer be confused with attention, pricing-only,
  or status-pipeline evidence.

## Task 3: Write The Mathematical Model Skeleton

**Type:** docs
**Files:** `.planning/paper/TR_E_RESEARCH_DESIGN.md`,
`work2_coding/Src/Algorithms/DSPO_Menu.py`,
`work2_coding/Src/paired_replay.py`

**Action:**

1. Define sets and indices for requests, vehicles, candidate meeting points,
   service bundles, displayed menus, and scenarios/splits.
2. Define service bundle attributes, including location, pickup time window,
   price, ETA feasibility, insertion cost, and acceptance/home/outside
   outcomes.
3. Define menu decision variables and feasibility constraints, including menu
   size, route/capacity feasibility, ETA/time-window feasibility, and service
   guardrails.
4. Define passenger utility and MNL choice probability over displayed bundles
   plus outside option.
5. Define expected-profit objective with revenue, operating cost, discount,
   opt-out penalty, and service-constrained profit variants.
6. Define exact enumeration and greedy forward selection, including required
   diagnostics for exact gap and menu overlap.

**Verify:**

- The model skeleton satisfies `PAPER-05`.
- It includes sets/indices, bundle definition, menu variable, utility model,
  choice probability, objective, guardrail, ETA/window feasibility, exact
  solver, and greedy solver.
- Outside option is not modeled as an accepted service bundle.

**Acceptance Criteria:**

- The design document contains enough formal structure to seed the manuscript
  model section without inventing new scope during writing.

## Task 4: Build Claim-To-Evidence And Metric Map

**Type:** docs
**Files:** `.planning/paper/TR_E_RESEARCH_DESIGN.md`,
`work2_coding/Src/policy_adapters.py`,
`work2_coding/Src/paired_replay.py`,
`work2_coding/Src/study_execution.py`,
`work2_coding/Src/artifact_status.py`,
`work2_coding/Src/manuscript_claims.py`,
`work2_coding/Experiments/studies/formal_robust_menu.yaml`

**Action:**

1. Create a claim matrix with claim ID, claim type, comparison policies,
   required metrics, required artifacts, and allowed manuscript use.
2. Include the full seven-tag mainline family and identify
   `mainline_optimized_adaptive` as the primary V1 method.
3. Map central, ablation, robustness, solver, and provenance/status claims.
4. Require paired replay fields, checkpoint load status, row completion,
   artifact status, claim guard, and source artifact path for every positive
   main claim.
5. Add the four-level claim ladder: `strong`, `conditional`,
   `weak-diagnostic`, `unsupported`.

**Verify:**

- The document satisfies `PAPER-03`.
- Every positive claim has a comparison policy family and metric family.
- Unsupported claims are blocked from positive manuscript sections.
- The metrics include `net_profit`, `adjusted_profit`,
  `service_constrained_net_profit`, `acceptance_rate`, `opt_out_rate`,
  `home_only_share`, and `non_home_uptake`.

**Acceptance Criteria:**

- Later Phase 3 and Phase 4 can use the design document to decide exactly what
  rows, metrics, gates, and artifacts are needed for each claim.

## Task 5: Define Paper Tables, Figures, And Downstream Handoff

**Type:** docs
**Files:** `.planning/paper/TR_E_RESEARCH_DESIGN.md`,
`work2_coding/Src/artifact_builder.py`,
`work2_coding/artifacts/work2_robust_menu/manuscript/experiment_outline.md`,
`work2_coding/artifacts/work2_robust_menu/manuscript/result_outline.md`

**Action:**

1. Define the required paper tables:
   - policy design and seven-tag comparison family
   - main paired results
   - product/time-window ablations
   - ETA robustness and no-filter diagnostics
   - exact-vs-greedy computation
   - provenance/status/claim gate
2. Define the required figures:
   - service-menu framework or bundle schematic
   - profit-service trade-off
   - acceptance, opt-out, home share, and meeting-point uptake
   - ETA/risk filtering diagnostics
   - exact/greedy runtime and gap diagnostics
3. Add downstream handoff notes for Phase 3 formal pipeline repair and Phase 4
   claim diagnosis.
4. State that paper-facing tables and figures must be generated from rows and
   artifact builders only.

**Verify:**

- The design document contains both a table plan and a figure plan.
- Every table or figure family names its source evidence or future artifact.
- No generated result rows, tables, figures, or manuscript files are edited.

**Acceptance Criteria:**

- Formal experiments can be planned against known paper-facing deliverables
  rather than retrofitting claims after results appear.

## Task 6: Self-Check, Lightweight Verification, And Closeout

**Type:** verify
**Files:** `.planning/paper/TR_E_RESEARCH_DESIGN.md`

**Action:**

1. Search the design document for all requirements `PAPER-01` through
   `PAPER-05`.
2. Search the design document for all tracked decisions `D-01` through `D-19`
   or their explicit content.
3. From `work2_coding/`, run the lightweight import smoke:

   ```powershell
   python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
   ```

4. Confirm `git status --short` only shows expected Phase 2 planning additions
   from this plan plus pre-existing unrelated dirty files.

**Verify:**

- Import smoke prints `IMPORT_OK`.
- The design document covers `PAPER-01` through `PAPER-05`.
- The design document covers decisions `D-01` through `D-19`.
- No formal replay, checkpoint training, artifact regeneration, generated-row
  edit, or manuscript claim upgrade occurred.

**Acceptance Criteria:**

- Phase 2 can be summarized as complete after execution and verification.
</tasks>

<verification>
## Required Verification

Run from the repository root:

```powershell
cd work2_coding
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
```

Expected output:

```text
IMPORT_OK
```

Then verify `.planning/paper/TR_E_RESEARCH_DESIGN.md` contains:

- `PAPER-01`, `PAPER-02`, `PAPER-03`, `PAPER-04`, `PAPER-05`
- all decision anchors `D-01` through `D-19`
- the seven mainline tags
- a mathematical model skeleton
- a claim-to-evidence matrix
- table and figure plans
- explicit non-claim boundaries for attention, no-filter, status-only evidence,
  and optional case-study evidence
</verification>

<success_criteria>
- `.planning/paper/TR_E_RESEARCH_DESIGN.md` defines problem, service product,
  decisions, passenger choice, objective, guardrails, solver, benchmarks,
  metrics, claims, and non-claims.
- V1 evidence, V2 attention diagnostics, appendix evidence, and non-claims are
  separated.
- Main tables and figures are defined before formal experiments.
- Every paper claim maps to a policy comparison and metric.
- The design includes a mathematical model skeleton with sets and indices,
  service-bundle definition, menu decision variable, utility model, choice
  probability, expected-profit objective, service guardrail, ETA/time-window
  feasibility, and exact/greedy solver definitions.
</success_criteria>
