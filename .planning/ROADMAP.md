# Roadmap: Work2 Robust Time-Window Service Menu Optimization for Many-to-One DRT

**Created:** 2026-06-10
**Granularity:** coarse
**Project mode:** mvp

## Overview

This roadmap preserves the user's staged evidence pipeline while grouping work into five coarse phases. Phase 1 is the requested first task: Stage 0 repository audit before algorithm behavior changes.

| # | Phase | Goal | Requirements |
|---|-------|------|--------------|
| 1 | Repository Audit And Runtime Baseline (Complete 2026-06-11) | Identify the active Work2 runtime and produce a minimal runnable patch plan | AUDIT-01, AUDIT-02, AUDIT-03, AUDIT-04 |
| 2 | Core Semantics And Robust Menu Logic | Fix accounting/checkpoint risks and implement robust filtering/objective/solver behavior | ACCT-01..04, ETA-01..04, MENU-01..04 |
| 3 | Experiment Contracts And Fair Replay (Complete 2026-06-11) | Define runnable study contracts and paired comparisons | EXP-01..04 |
| 4 | Evidence And Artifacts (Complete 2026-06-11) | Generate the evidence chain required for paper-facing Work2 claims | ART-01..04 |
| 5 | Manuscript Framing And Claim Guard | Produce paper-ready method/results/limitations text and enforce claim boundaries | PAPER-01..04 |

## Phases

### Phase 1: Repository Audit And Runtime Baseline
**Goal:** Produce the Stage 0 audit report and confirm the minimum runnable Work2 baseline before behavior changes.
**Mode:** mvp

**Success Criteria**:
1. Audit report names the active runtime root, current import status, and any stale competing path references.
2. Audit report lists relevant runner scripts, missing expected scripts, current menu policies, and relevant simulator/choice modules.
3. Audit report identifies broken imports, opt-out accounting risks, checkpoint loading risks, and experiment fairness risks.
4. Audit report proposes the minimal patch plan to make robust time-window menu experiments runnable.
5. Import smoke command is recorded with exact command and result.

**Requirements:** AUDIT-01, AUDIT-02, AUDIT-03, AUDIT-04

### Phase 2: Core Semantics And Robust Menu Logic
**Goal:** Make the simulator and menu algorithm scientifically safe enough for robust time-window comparisons.
**Mode:** mvp

**Success Criteria**:
1. Opt-out choices are distinct from accepted home and accepted meeting-point choices.
2. Deterministic tests verify opt-out does not mutate route/service accounting as an accepted pickup.
3. Checkpoint loading reports explicit status and fails closed for required shared predictor loads.
4. Robust ETA filter modes are implemented with candidate metadata and unit coverage.
5. Robust objective modes support opt-out penalty, ETA risk penalty, and service guardrails.
6. Exact-small and greedy-large selection paths respect menu size and log approximation diagnostics.

**Requirements:** ACCT-01, ACCT-02, ACCT-03, ACCT-04, ETA-01, ETA-02, ETA-03, ETA-04, MENU-01, MENU-02, MENU-03, MENU-04

### Phase 3: Experiment Contracts And Fair Replay
**Goal:** Convert the algorithm into a reproducible study pipeline with fair policy comparisons.
**Mode:** mvp

**Success Criteria**:
1. Smoke, pilot, and formal study contracts exist and validate policy names, seeds, split IDs, menu_k, filter modes, and output schema.
2. Baselines include full display, home only, nearest heuristic, top-k cheapest, min-lateness, hard filter, no-filter diagnostic, robust time-window menu, and optional random top-k.
3. Paired replay uses the same request traces, trained predictor, random seeds, pricing mode, and HGS parameters for compared policies.
4. Uptake regimes include at least low and medium behaviorally live settings when runtime permits.
5. A smoke study runs end-to-end and emits normalized rows.

**Requirements:** EXP-01, EXP-02, EXP-03, EXP-04

### Phase 4: Evidence And Artifacts
**Goal:** Generate the evidence chain required for paper-facing Work2 claims.
**Mode:** mvp

**Success Criteria**:
1. Normalized rows include seed, split, trace ID, policy tag, checkpoint metadata, filter mode, menu_k, and relevant metric fields.
2. Robust filtering, exact-greedy, uptake-regime, ETA diagnostics, profit decomposition, and uncertainty/gap tables are generated.
3. Required figures are generated with labels, units, and source study IDs.
4. Artifact status file records manifest hash, git marker, checkpoint provenance, completed/incomplete status, and placeholder status.
5. Formal artifact generation blocks placeholder-only evidence from supporting formal claims.

**Requirements:** ART-01, ART-02, ART-03, ART-04

### Phase 5: Manuscript Framing And Claim Guard
**Goal:** Translate verified evidence into restrained, paper-ready Work2 framing.
**Mode:** mvp

**Success Criteria**:
1. Method outline defines service bundles, menu decision, outside option, robust time-window handling, MNL choice, pricing, and exact/greedy solver.
2. Experiment outline defines scenarios, baselines, metrics, paired replay protocol, seeds, splits, and checkpoint handling.
3. Result outline covers exact-vs-greedy quality, robust filtering comparison, uptake-regime behavior, external/semi-real checks if available, and limitations.
4. Claim checklist explicitly allows robust-pruning, solver-auditability, and simulation-framework claims while blocking universal dominance and unsupported behavioral validation.
5. Manuscript claims are not strengthened until artifact status marks formal evidence complete.

**Requirements:** PAPER-01, PAPER-02, PAPER-03, PAPER-04

## Requirement Coverage

All 28 v1 requirements are mapped to exactly one phase.

---
*Roadmap created: 2026-06-10 after initialization*
