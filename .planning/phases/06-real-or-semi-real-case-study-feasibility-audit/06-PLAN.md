---
phase: 6
phase_name: Real Or Semi-Real Case Study Feasibility Audit
plan: 1
type: docs
status: ready
wave: 1
depends_on:
  - phase-5-calibration-and-robustness-without-p-hacking
files_modified:
  - .planning/data/CASE_STUDY_FEASIBILITY.md
  - work2_coding/outputs/phase6_audit/PHASE6_AUDIT.md
  - work2_coding/outputs/phase6_audit/PHASE6_AUDIT.json
  - .planning/PROJECT.md
  - .planning/ROADMAP.md
  - .planning/STATE.md
autonomous: true
requirements_addressed:
  - CASE-01
  - CASE-02
  - CASE-04
requirements:
  - CASE-01
  - CASE-02
  - CASE-04
must_haves:
  truths:
    - "D-01: Default to a semi-real case study route, not full real passenger-behavior validation."
    - "D-02: Yanjiao/commuting materials are useful if available, but the case is not hard-bound to Yanjiao."
    - "D-03: The semi-real case is supplemental external scenario evidence and must not override the RC formal ladder."
    - "D-04: Use decision label approved_blocked_pending_gate_cleanup."
    - "D-05: Do not automatically downgrade Phase 7 to diagnostic-only execution if gates remain blocked."
    - "D-06: Before gate cleanup, Phase 7 may build ingestion/validation scaffolding but may not run case experiments or claims."
    - "D-07: Use a dual-track source audit covering public OSM/open networks and Yanjiao/Beijing commuting materials."
    - "D-08: If both source routes are feasible, default Phase 7 to public OSM/open network data."
    - "D-09: Rank candidates by reproducibility, licensing/access, matrix rebuildability, DRT plausibility, and paper value."
    - "D-10: Record external source links, reproducibility paths, licensing/access constraints, and limitations."
    - "D-11: Only geography, network, coordinates, and distances may be described as real or semi-real foundations."
    - "D-12: Existing Amazon and HombergerGehring sources may be benchmarks but not real-city DRT passenger cases."
    - "D-13: Define the minimum semi-real contract: real geography, depot/destination, candidates, distance matrix, simulated demand, simulated choice."
    - "D-14: Preserve the seven mainline tags by default and require a documented reduced-family gate for any reduction."
    - "D-15: Demand generation must be pre-registered before case experiments and never tuned from outcomes."
    - "D-16: Formal/semi-real case evidence requires real road-network distance or a reproducible distance matrix; Euclidean fallback is diagnostic only."
    - "D-17: Candidate meeting points should prioritize explainable public points, with synthetic candidates pre-registered and labeled if needed."
    - "D-18: Use work2_coding/Src/phase6_audit.py as supporting experiment-state evidence only."
    - "D-19: Do not implement case-study ingestion, validation, manifests, or run code in Phase 6."
    - "D-20: If gates remain blocked, approve only with approved_blocked_pending_gate_cleanup."
    - "D-21: Primary output is .planning/data/CASE_STUDY_FEASIBILITY.md; phase6 audit outputs are support evidence."
    - "D-22: Position the semi-real case as supplemental robustness/external scenario evidence."
    - "D-23: If case results later conflict with RC evidence, report the conflict honestly."
    - "D-24: Do not claim real passenger behavior, real acceptance/opt-out, or real operating profit from simulated case data."
    - "D-25: Case tables, figures, metadata, and manuscript text must label semi-real, simulated demand, and simulated choice status."
  artifacts:
    - .planning/phases/06-real-or-semi-real-case-study-feasibility-audit/06-CONTEXT.md
    - .planning/phases/06-real-or-semi-real-case-study-feasibility-audit/06-RESEARCH.md
    - .planning/data/CASE_STUDY_FEASIBILITY.md
  key_links:
    - .planning/PROJECT.md
    - .planning/REQUIREMENTS.md
    - .planning/ROADMAP.md
    - .planning/STATE.md
    - .planning/paper/TR_E_RESEARCH_DESIGN.md
    - .planning/results/CALIBRATION_PROTOCOL.md
    - .planning/results/FROZEN_FINAL_SETTINGS.md
    - work2_coding/Src/phase6_audit.py
    - work2_coding/scripts/audit_phase6_experiment_state.py
    - work2_coding/scripts/test_phase6_audit.py
---

# Phase 6 Plan: Case Study Feasibility Decision

<objective>
Write a defensible feasibility decision for whether Work2 should add a real or
semi-real case study to the TR-E paper. The plan produces the primary report
`.planning/data/CASE_STUDY_FEASIBILITY.md`, preserves the no-fabricated-data
boundary, and records that semi-real case execution remains blocked until
upstream gate cleanup.
</objective>

<scope>
## In Scope

- Audit public OSM/open-network, GTFS/transit, Yanjiao/Beijing commuting, and
  existing benchmark-data source routes.
- Record source links, access/licensing constraints, reproducibility path,
  distance-matrix rebuild path, and limitations.
- Decide between add real case, add semi-real case, or defer case study.
- Define the minimum acceptable semi-real case contract.
- Optionally run the existing Phase 6 audit scaffold to capture runtime,
  manifest, readiness, artifact, and claim-gate state as supporting evidence.
- Update planning docs only to record the Phase 6 decision and Phase 7 gate.

## Out Of Scope

- Implementing new case-study ingestion, validation, manifests, or run scripts.
- Running semi-real or real case experiments.
- Generating case-study result rows, tables, figures, or manuscript claims.
- Tuning RC calibration/final settings from case-study considerations.
- Describing simulated demand, simulated choice, acceptance, opt-out, or profit
  as real passenger or real operational behavior.
- Hand-editing generated result rows or paper artifacts.
</scope>

<tasks>
## Task 1: Build The Source Feasibility Matrix

**Type:** research
**Files:** `.planning/data/CASE_STUDY_FEASIBILITY.md`,
`.planning/phases/06-real-or-semi-real-case-study-feasibility-audit/06-RESEARCH.md`

**Action:**

1. Use `06-RESEARCH.md` as the starting source list and refresh links if they
   have changed.
2. Create `.planning/data/CASE_STUDY_FEASIBILITY.md` with frontmatter:
   `phase`, `decision`, `status`, `created`, `timezone`, `requirements`, and
   `case_execution_gate`.
3. Add a source-audit table for:
   - OSM/Geofabrik extracts;
   - Overpass/OSMnx extraction;
   - OSRM or equivalent local routing/matrix generation;
   - GTFS or Mobility Database transit-stop enrichment;
   - Yanjiao/Beijing commuting materials;
   - existing `Amazon_data` and `HombergerGehring_data` benchmark roots.
4. For each route, record:
   - source URL and access date;
   - data type;
   - license/access notes;
   - reproducibility path;
   - expected preprocessing;
   - limitation for TR-E claim language.
5. Rank source routes using reproducibility, licensing/access, matrix
   rebuildability, DRT scenario plausibility, and paper value.

**Verify:**

- Every external source route has at least one URL and a limitation statement.
- The report does not treat anecdotal commuting material as audited passenger
  behavior.

**Acceptance Criteria:**

- `CASE-01` is covered by a visible audit of Yanjiao/commuting materials,
  public mobility/network options, and synthetic-over-real-network options.

## Task 2: Record The Case Study Decision

**Type:** docs
**Files:** `.planning/data/CASE_STUDY_FEASIBILITY.md`

**Action:**

Add a decision section with:

1. Decision:
   `add semi-real case, approved_blocked_pending_gate_cleanup`.
2. Rationale:
   - public OSM/open-network route is most reproducible;
   - Yanjiao/Beijing materials are useful narrative support but not enough by
     themselves for reproducible passenger-behavior evidence;
   - upstream provenance/readiness/artifact/claim gates remain blocked.
3. Phase 7 authorization:
   - allowed before gate cleanup: ingestion design, validation contracts,
     manifest scaffolding, reproducibility checks;
   - blocked before gate cleanup: case experiment execution, generated
     case-study result artifacts, manuscript claim upgrades.
4. Paper-value statement:
   - supplemental external scenario / robustness evidence only;
   - RC formal evidence remains the main empirical ladder.

**Verify:**

- The decision is one of the roadmap's allowed choices, with gate status made
  explicit.
- The report states that final claim language remains blocked while upstream
  gates remain blocked.

**Acceptance Criteria:**

- Phase 6 provides the decision needed to route Phase 7.

## Task 3: Define The Minimum Semi-Real Contract

**Type:** docs
**Files:** `.planning/data/CASE_STUDY_FEASIBILITY.md`

**Action:**

Add a contract section requiring:

1. Documented real geography and a bounded corridor or service area.
2. Plausible depot/destination and candidate meeting-point definition.
3. Candidate meeting points sourced from public POIs, transit stops,
   parking/community entrances, pickup points, or pre-registered synthetic
   grid/cluster rules.
4. Real road-network distance or reproducible distance matrix, with source,
   extraction date/version, parameters, cache path, hash, and rebuild command.
5. Simulated sequential demand with pre-registered seeds, OD/time pattern,
   volume/range, and sampling rules.
6. Simulated choice behavior labeled as simulated.
7. Seven-tag mainline comparison by default.
8. Reduced-family gate if any tag cannot run fairly:
   - which tag is infeasible;
   - why the reason is data/contract, not unfavorable outcome selection;
   - whether the reduced family still answers the case question;
   - why no unfavorable baseline is selectively removed.
9. No use of case-study outcomes to tune RC settings.
10. Mandatory labels for `semi-real`, `simulated demand`, and
    `simulated choice` in any future table, figure, artifact metadata, or
    manuscript text.

**Verify:**

- The contract is stricter than a synthetic benchmark and does not claim real
  passenger validation.
- Euclidean distance is allowed only as a diagnostic fallback.

**Acceptance Criteria:**

- `CASE-02` and `CASE-04` are covered.

## Task 4: Generate Supporting Runtime/Gate Audit

**Type:** audit
**Files:** `work2_coding/outputs/phase6_audit/PHASE6_AUDIT.md`,
`work2_coding/outputs/phase6_audit/PHASE6_AUDIT.json`,
`.planning/data/CASE_STUDY_FEASIBILITY.md`

**Action:**

From `work2_coding/`, run:

```powershell
python scripts/audit_phase6_experiment_state.py --output-root outputs/phase6_audit --format markdown
```

Then cite the generated Markdown/JSON paths in
`.planning/data/CASE_STUDY_FEASIBILITY.md`. Use the audit only as support for
runtime imports, manifest family, readiness blockers, artifact gates, and claim
guard state.

If the command fails, do not replace the feasibility report with speculation.
Record the failure command, error type, and current mitigation in the report.

**Verify:**

```powershell
cd work2_coding
python scripts/test_phase6_audit.py
```

**Acceptance Criteria:**

- The feasibility report has current gate-state evidence without running case
  experiments or formal replay.

## Task 5: Update Planning State

**Type:** docs
**Files:** `.planning/PROJECT.md`, `.planning/ROADMAP.md`, `.planning/STATE.md`

**Action:**

After `.planning/data/CASE_STUDY_FEASIBILITY.md` is written and verified,
update planning docs to record:

- Phase 6 decision:
  `add semi-real case, approved_blocked_pending_gate_cleanup`;
- Phase 7 may prepare scaffolding but may not execute case experiments while
  gates remain blocked;
- manuscript external-validation language remains limited to semi-real
  geography/network evidence with simulated demand and simulated choice.

Do not mark Phase 7 skipped unless the feasibility report explicitly changes
the decision to `defer case study`.

**Verify:**

- Roadmap and state match the decision in the feasibility report.
- No planning doc says real passenger validation has been obtained.

**Acceptance Criteria:**

- Downstream workflow can route safely into Phase 7 without overclaiming.

## Task 6: Run Phase Verification

**Type:** verify
**Files:** `work2_coding/scripts/test_phase6_audit.py`,
`.planning/data/CASE_STUDY_FEASIBILITY.md`

**Action:**

Run from `work2_coding/`:

```powershell
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_phase6_audit.py
```

Manually verify that `.planning/data/CASE_STUDY_FEASIBILITY.md` includes:

- source audit;
- decision;
- data source;
- preprocessing plan;
- required Phase 7 code changes;
- paper value;
- gate status;
- minimum semi-real contract;
- explicit no-fabricated-data and simulated-choice labels.

**Verify:**

- Import smoke passes.
- Phase 6 audit tests pass.
- Feasibility report covers all success criteria in ROADMAP Phase 6.

**Acceptance Criteria:**

- Phase 6 can close as a feasibility decision without executing case-study
  experiments.
</tasks>

<verification>
## Required Verification

Run from `work2_coding/`:

```powershell
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_phase6_audit.py
```

If `PHASE6_AUDIT.md` is generated during execution, also confirm both outputs
exist:

```powershell
Test-Path outputs/phase6_audit/PHASE6_AUDIT.md
Test-Path outputs/phase6_audit/PHASE6_AUDIT.json
```
</verification>

<success_criteria>
- `.planning/data/CASE_STUDY_FEASIBILITY.md` audits public network, transit,
  Yanjiao/commuting, and synthetic-over-real-network routes.
- The decision is explicit:
  `add semi-real case, approved_blocked_pending_gate_cleanup`.
- The report defines data source, preprocessing plan, required Phase 7 code
  changes, paper value, and gate status.
- The minimum acceptable semi-real case contract is documented.
- The report forbids fabricated real data and labels simulated demand/choice.
- No case experiment, generated result artifact, or manuscript claim upgrade is
  performed in Phase 6.
</success_criteria>

## PLANNING COMPLETE

