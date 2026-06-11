# Roadmap: Work2 Attention-Enhanced DSPO Menu Optimization for Many-to-One DRT

**Created:** 2026-06-10
**Granularity:** coarse
**Project mode:** mvp

## Overview

This roadmap preserves the user's staged evidence pipeline while grouping work into coarse phases. Phase 1 is the requested first task: Stage 0 repository audit before algorithm behavior changes.

**Direction update 2026-06-11:** The paper-method target is now to show that adding an attention mechanism improves the original DSPO method under fair paired replay. The robust time-window/menu pipeline remains useful as reproducible infrastructure, diagnostics, and guardrails, but it is no longer the sole main contribution claim. `home_only` and any meeting-point-only variant should be reported as cost-approximation boundary references, not ranked comparison methods.

| # | Phase | Goal | Requirements |
|---|-------|------|--------------|
| 1 | Repository Audit And Runtime Baseline (Complete 2026-06-11) | Identify the active Work2 runtime and produce a minimal runnable patch plan | AUDIT-01, AUDIT-02, AUDIT-03, AUDIT-04 |
| 2 | Core Semantics And Robust Menu Logic | Fix accounting/checkpoint risks and implement robust filtering/objective/solver behavior | ACCT-01..04, ETA-01..04, MENU-01..04 |
| 3 | Experiment Contracts And Fair Replay (Complete 2026-06-11) | Define runnable study contracts and paired comparisons | EXP-01..04 |
| 4 | Evidence And Artifacts (Complete 2026-06-11) | Generate the evidence chain required for paper-facing Work2 claims | ART-01..04 |
| 5 | Manuscript Framing And Claim Guard (Complete 2026-06-11) | Produce paper-ready method/results/limitations text and enforce claim boundaries | PAPER-01..04 |
| 6 | Attention-Enhanced DSPO Evidence Pivot (Complete 2026-06-11) | Implement and evaluate attention-enhanced DSPO against the original DSPO baseline | ATTN-01..04, BEHAV-01 |
| 7 | Audit Closure And Traceability Repair | Close v2.0 procedural audit gaps before new experiments | TRACE-01..05 |
| 8 | Repository Hygiene And Provenance Freeze | Reduce provenance risk before producing empirical evidence | PROV-01..04 |
| 9 | Shared Checkpoint Training Pipeline | Create real shared pilot/formal predictor checkpoints with provenance | CKPT-01..05 |
| 10 | 2/1 | Complete    | 2026-06-11 |
| 11 | 1/1 | Complete    | 2026-06-11 |
| 12 | Formal Actual Replay Enablement | Enable strict-gated formal actual replay without placeholder rows | FORM-01..05 |
| 13 | Formal Attention Evidence And Claim Decision | Run formal evidence and decide the paper claim from artifact guards | CLAIM-01..05 |

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

### Phase 6: Attention-Enhanced DSPO Evidence Pivot
**Goal:** Make the main method comparison `DSPO_original` vs `DSPO_attention`, with paired replay evidence that attention improves the original DSPO method.
**Mode:** mvp

**Success Criteria**:
1. Original DSPO baseline and attention-enhanced DSPO treatment are exposed through explicit, named policy/model variants.
2. The attention module is integrated into DSPO scoring or cost/candidate evaluation without breaking existing opt-out accounting, checkpoint metadata, or paired replay fairness.
3. Study manifests compare `DSPO_original` and `DSPO_attention` on the same request traces, seeds, split IDs, pricing mode, routing/HGS settings, and checkpoint policy.
4. Artifacts report attention-vs-original DSPO deltas for acceptance, opt-out, non-home uptake, service cost, net objective/profit proxy, and relevant prediction/decision diagnostics.
5. Claim gates only allow "attention improves DSPO" statements when completed non-placeholder paired evidence supports that direction; robust/no-filter diagnostics remain clearly labeled.

**Requirements:** ATTN-01, ATTN-02, ATTN-03, ATTN-04, BEHAV-01

### Phase 7: Audit Closure And Traceability Repair
**Goal:** Close the procedural GSD audit gaps before running more experiments.
**Mode:** mvp

**Success Criteria**:
1. `.planning/phases/02-core-semantics-and-robust-menu-logic/02-VERIFICATION.md` exists.
2. ACCT-01..04, ETA-01..04, and MENU-01..04 have command-backed evidence rows or explicit gaps.
3. MENU-02 has explicit evidence or remains an explicit blocker.
4. Phase 2 validation exists because Nyquist validation is enabled.
5. Phase 07 verification states whether Phase 08 may proceed.

**Requirements:** TRACE-01, TRACE-02, TRACE-03, TRACE-04, TRACE-05

### Phase 8: Repository Hygiene And Provenance Freeze
**Goal:** Reduce provenance risk before producing new empirical evidence.
**Mode:** mvp

**Success Criteria**:
1. Dirty files are classified and unexplained files are resolved or documented.
2. `.gitignore` handles venv, cache, temporary outputs, and large local artifacts.
3. Deleted user documents are documented before restore/removal decisions.
4. Generated artifact tracking policy is recorded.
5. STATE records repository hygiene status.

**Requirements:** PROV-01, PROV-02, PROV-03, PROV-04

### Phase 9: Shared Checkpoint Training Pipeline
**Goal:** Create real shared predictor checkpoints for pilot and formal attention evidence.
**Mode:** mvp

**Success Criteria**:
1. `scripts/train_shared_checkpoint.py` exists if no stable training entry point already satisfies the contract.
2. Pilot and formal `supervised_ml.pt` files exist under `outputs/shared_training/work2_attention_dspo/`.
3. Metadata sidecars record hashes, commands, seeds, splits, dataset, run ID, git provenance, args, and timestamp.
4. Checkpoints load through the run-study code path.
5. Missing or random-weight checkpoints are refused.

**Requirements:** CKPT-01, CKPT-02, CKPT-03, CKPT-04, CKPT-05

### Phase 10: Pilot Attention Evidence Run
**Goal:** Run the checkpoint-backed pilot comparison for `DSPO_original` versus `DSPO_attention`.
**Mode:** mvp

**Success Criteria**:
1. `pilot_attention_dspo` completes with loaded checkpoint provenance and non-placeholder rows.
2. Every `attention_pair_id` group contains both compared policies.
3. Low and medium uptake regimes are present.
4. Attention artifacts and claim guard are rebuilt from the completed run.
5. A written go/no-go decision controls the next phase.

**Requirements:** PILOT-01, PILOT-02, PILOT-03, PILOT-04, PILOT-05, PILOT-06

### Phase 11: Attention Ablation And Design Fix
**Goal:** If pilot evidence is weak, identify whether attention design, weights, behavioral regime, or metric design is responsible.
**Mode:** mvp

**Success Criteria**:
1. Pilot-only attention strength, feature, and ETA-variant manifests exist.
2. Varied fields and selection criteria are pre-registered before ablations run.
3. Paired replay fairness is preserved within ablations.
4. Exactly one formal candidate is selected before formal evidence, or the claim is stopped.

**Requirements:** ABLT-01, ABLT-02, ABLT-03, ABLT-04

### Phase 12: Formal Actual Replay Enablement
**Goal:** Enable formal actual replay safely with strict evidence gates.
**Mode:** mvp

**Success Criteria**:
1. The old unconditional formal actual replay block is replaced by strict gated execution.
2. Formal execution requires loaded checkpoint provenance and non-placeholder rows.
3. Missing checkpoint still fails closed with blocker metadata.
4. Formal placeholder rows are impossible.
5. Formal contract, missing-checkpoint, loaded-checkpoint, and placeholder-impossibility tests exist.

**Requirements:** FORM-01, FORM-02, FORM-03, FORM-04, FORM-05

### Phase 13: Formal Attention Evidence And Claim Decision
**Goal:** Run final formal evidence and decide the manuscript claim from artifact status.
**Mode:** mvp

**Success Criteria**:
1. Formal attention rows are completed, paired, non-placeholder, and checkpoint-loaded.
2. Formal artifacts report primary/secondary deltas, regime results, and variance/confidence summaries.
3. Diagnostic and cost-bound policies are not ranked as method baselines.
4. `ATTENTION_CLAIM_GUARD.json` makes the final claim decision.
5. Final milestone audit passes before archive.

**Requirements:** CLAIM-01, CLAIM-02, CLAIM-03, CLAIM-04, CLAIM-05

## Requirement Coverage

All 28 v1 requirements are mapped to exactly one phase. Phase 6 adds the v2 attention-evidence pivot. Milestone v2.1 adds 34 evidence-ladder requirements mapped to Phases 7-13.

---
*Roadmap last updated: 2026-06-11 starting milestone v2.1*
