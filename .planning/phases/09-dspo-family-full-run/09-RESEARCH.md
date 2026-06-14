# Phase 09: DSPO Family Full Run - Research

**Researched:** 2026-06-14  
**Domain:** Work2 paired replay, DSPO menu policy variants, validation gates  
**Confidence:** HIGH for codebase integration points; MEDIUM for report-field naming choices  

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

## Implementation Decisions

### DSPO Clip/Wide Identity

- **D-01:** Add explicit Phase 9 policy tags `dspo_clip` and `dspo_wide`.
  Do not reuse old mainline tags as the paper-facing DSPO clip/wide names.
- **D-02:** Both tags are DSPO-internal variants and must emit
  `method_family=DSPO`.
- **D-03:** Use `policy_tag` to distinguish `dspo_clip` from `dspo_wide`, and
  add or reuse a role such as `comparison_role=dspo_family` so gates and
  reports do not infer purpose only from tag strings.
- **D-04:** Define `clip` and `wide` by DSPO internal service-risk threshold,
  not by time-window mode, candidate-pool size, or DSPO_PLUS semantics.
- **D-05:** Use `dspo_clip` as the stricter DSPO setting with threshold `0.35`.
- **D-06:** Use `dspo_wide` as the looser DSPO setting with threshold `0.45`.
- **D-07:** `dspo_clip` and `dspo_wide` must not inherit, align with, compare
  to, or mention DSPO_PLUS parameters or penalty terms.

### Comparison Bundle Shape

- **D-08:** The Phase 9 primary manifest should contain only `dspo_clip` and
  `dspo_wide`.
- **D-09:** Do not rerun Phase 8 no-pricing or static-pricing baselines inside
  the Phase 9 primary manifest.
- **D-10:** Reuse the five Phase 8 formal-equivalent splits exactly, including
  `seed`, `data_seed`, `data_seed_test`, `uptake_regime`, `home_util`,
  `base_util`, and `incentive_sens`.
- **D-11:** The Phase 9 report may reference the latest passed Phase 8
  validation report and run ID as a cross-run sanity/status reference.
- **D-12:** Any sanity comparison against Phase 8 baselines must be described
  as a gate/status check only, not as same-run formal ranking evidence.

### Pass And Failure Gate

- **D-13:** Any failed, blocked, incomplete, placeholder-only, or contract-only
  DSPO row blocks Phase 9.
- **D-14:** Any checkpoint status other than `loaded`, paired setting drift,
  missing row-v2 field, manifest/hash/provenance anomaly, or opt-out/home/
  meeting-point accounting error blocks Phase 9.
- **D-15:** Every failed row or split must report `reason`, `minimal_fix`, and
  a concrete local `rerun_command`.
- **D-16:** A passed Phase 9 unlocks DSPO result organization and manuscript
  status language only. It does not unlock final ranking claims or language
  such as "DSPO improves over baselines."
- **D-17:** If Phase 9 is blocked, the report must provide a debug handoff and
  stop in a debug-ready state. It should not automatically repair or rerun the
  failure inside this phase.

### Runtime Budget And Outputs

- **D-18:** Use the Phase 8 formal-equivalent lightweight runtime budget rather
  than the heavier `formal_robust_menu` budget.
- **D-19:** Keep menu and candidate parameters aligned with Phase 8, including
  `menu_k=3`, `max_candidates=8`, `menu_exact_threshold=8`, and
  `menu_exact_gap_threshold=8`.
- **D-20:** Keep HGS and replay runtime settings aligned with Phase 8 unless
  planning discovers a direct incompatibility that must be documented.
- **D-21:** Require the same checkpoint/provenance strength as Phase 8:
  `require_checkpoint=true`, `checkpoint_load_status=loaded`, and recorded
  checkpoint path/hash.
- **D-22:** Keep claim-ready status separate from Phase 9 DSPO validation.
  Local provenance blockers may leave `claim_ready=false` even when Phase 9
  DSPO validation passes.
- **D-23:** Generate a Phase 9 JSON validation report and a Phase 9 Markdown
  validation report. Do not generate a new artifact bundle and do not invoke
  claim-ready artifact building for Phase 9 completion.

### Report Language

- **D-24:** Use gate-first report language: `dspo_validation_status`,
  `phase9_gate`, `claim_ready`, Phase 8 baseline reference status, and a short
  sanity summary.
- **D-25:** The report must explicitly state that any sanity comparison is
  status-only and is not a manuscript ranking conclusion.
- **D-26:** If DSPO clip/wide execution and gates pass but sanity comparison
  does not support DSPO advantage over the Phase 8 baselines, Phase 9 may still
  pass. The report must state that ranking sanity did not support an advantage
  conclusion.
- **D-27:** The Phase 9 context and runtime report must state that DSPO_PLUS is
  unrelated to this project and that Phase 9 does not inherit, compare, or
  validate DSPO_PLUS. Existing DSPO_PLUS planning text is a cleanup risk, not a
  Phase 9 objective.
- **D-28:** Include one clear next step in the report: debug handoff if blocked;
  if passed but sanity does not support advantage, proceed only to Phase 11
  status language/risk analysis and do not write a ranking claim.

### the agent's Discretion

The agent may choose exact helper names, report file names, JSON schema field
names, and test file names as long as the implementation preserves the
decisions above, follows existing script-style test patterns, keeps
`work2_coding/` as the runtime root, and does not hand-edit generated rows,
generated tables, generated figures, or claim-ready artifacts.

### Deferred Ideas (OUT OF SCOPE)

- Cleaning DSPO_PLUS references from `.planning/PROJECT.md`,
  `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, prior contexts, and any
  runtime contracts is a follow-up documentation/scope cleanup task outside
  the Phase 9 discussion artifact.
- Final manuscript result claims and reviewer-risk synthesis belong to a later
  paper-writing/status phase after the DSPO validation report exists.
- Expanding experiments beyond the Phase 8 lightweight formal-equivalent budget
  belongs in a separate future phase or explicit user request.
</user_constraints>

## Summary

Phase 9 should be implemented as a narrow DSPO-only validation slice: add two policy adapters, add one Phase 9 study manifest, execute actual paired replay across the five Phase 8 split definitions, then validate the resulting normalized rows with a Phase 8-style gate/report helper. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md] The primary manifest must contain only `dspo_clip` and `dspo_wide`; Phase 8 baseline rows should be referenced by the report as status context, not rerun in the Phase 9 manifest. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md]

The codebase already has the required seams: `policy_adapters.py` is the adapter registry; `paired_replay.py` resolves paired settings and builds normalized-row-v2 records; `study_execution.py` runs actual replay and produces completed/failed rows; `baseline_validation.py` is the closest report/gate template; and `DSPO_Menu.py` already consumes `service_quit_rate_guardrail` and `menu_optout_guardrail` thresholds for service-guarded menu behavior. [VERIFIED: codebase grep]

**Primary recommendation:** Create a Phase 9 manifest and `dspo_validation.py`/`build_phase9_dspo_family_validation_report.py` pair that mirrors Phase 8 validation structure while enforcing DSPO-only tags, `method_family=DSPO`, thresholds `0.35` and `0.45`, five paired splits, loaded checkpoints, row-v2 completeness, and no claim-ready artifact generation. [VERIFIED: codebase grep]

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|--------------|----------------|-----------|
| DSPO clip/wide identity | Experiment config / adapter layer | Algorithm runtime | `policy_adapters.py` should define paper-facing tags and thresholds; `DSPO_Menu.py` already consumes the guardrail knobs. [VERIFIED: codebase grep] |
| Paired replay fairness | Study orchestration | Row schema | `resolve_paired_settings()` validates paired fields before rows are generated. [VERIFIED: codebase grep] |
| Actual DSPO execution | Algorithm runtime | Environment simulator | `study_execution.actual_rows_for_manifest()` instantiates `Config`, loads checkpoint, runs test environment steps, and writes completed/failed normalized rows. [VERIFIED: codebase grep] |
| Phase 9 gate/report | Validation helper / CLI | Artifact status helper | Phase 8 keeps validation separate from artifact claim readiness through `baseline_validation.py` plus `classify_artifact()`. [VERIFIED: codebase grep] |
| DSPO_PLUS exclusion | Adapter/test/report layer | Planning docs cleanup later | Phase 9 must exclude DSPO_PLUS from manifest and report scope; existing DSPO_PLUS adapters are stale residue for this phase. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md] |

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| EXP-04 | DSPO clip/wide configurations are executable under paired replay. | Add `dspo_clip`/`dspo_wide` adapters and `phase9_dspo_family_validation.yaml`; run via `scripts/run_study.py --execute`. [CITED: .planning/REQUIREMENTS.md] [VERIFIED: codebase grep] |
| GATE-01 | Checkpoint load status is explicit in normalized rows and metadata. | `checkpoint_metadata_for_setting()` and actual replay rows record load status/path/hash. [VERIFIED: codebase grep] |
| GATE-02 | Placeholder, blocked, diagnostic, and no-filter rows are excluded from claims. | `classify_artifact()` already blocks failed/placeholder/checkpoint-bad rows and separates claim readiness. [VERIFIED: codebase grep] |
| GATE-04 | Failures report reason, minimal fix, and rerun instruction. | Phase 8 `_blocker()` objects provide the reusable pattern. [VERIFIED: codebase grep] |
</phase_requirements>

## Project Constraints (from AGENTS.md)

- Use `work2_coding/` as the active runtime root; do not create or rely on `ooh_code/`. [CITED: AGENTS.md]
- Read planning context and treat `.planning/codebase/` `ooh_code/` references as stale unless mapped by `.planning/repository_audit.md`. [CITED: AGENTS.md]
- Preserve paired replay fairness across policy comparisons. [CITED: AGENTS.md]
- Keep opt-out accounting separate from accepted home pickup. [CITED: AGENTS.md]
- Make checkpoint load status explicit in result metadata. [CITED: AGENTS.md]
- Treat no-filter as diagnostic unless formal evidence justifies stronger claims. [CITED: AGENTS.md]
- Keep attention-based choice/scoring out of v1 scope. [CITED: AGENTS.md]
- Do not hand-edit generated result rows or paper artifacts. [CITED: AGENTS.md]

## Standard Stack

### Core

| Component | Version / Status | Purpose | Why Standard |
|-----------|------------------|---------|--------------|
| Python | 3.12.4 | Run scripts and Work2 modules | Current local interpreter used by import smoke. [VERIFIED: local command] |
| `work2_coding/Src/policy_adapters.py` | Existing local module | Policy tag registry and adapter metadata | Existing manifests resolve tags through this module. [VERIFIED: codebase grep] |
| `work2_coding/Src/paired_replay.py` | Existing local module | Paired setting resolution and normalized-row-v2 construction | Central row contract used by tests and execution. [VERIFIED: codebase grep] |
| `work2_coding/Src/study_execution.py` | Existing local module | Actual replay rows, checkpoint metadata, blocked/failed rows | `scripts/run_study.py` delegates execution here. [VERIFIED: codebase grep] |
| `work2_coding/Src/artifact_status.py` | Existing local module | Claim-ready/status classification | Phase 8 validator already uses it to separate gate pass from claim readiness. [VERIFIED: codebase grep] |
| `work2_coding/Src/Algorithms/DSPO_Menu.py` | Existing local module | DSPO service-menu runtime | Consumes `service_quit_rate_guardrail`, `menu_optout_guardrail`, `method_family`, and menu metadata. [VERIFIED: codebase grep] |

### Supporting

| Component | Version / Status | Purpose | When to Use |
|-----------|------------------|---------|-------------|
| NumPy | 2.4.4 | Existing numerical dependency | Runtime already imports NumPy in DSPO menu code. [VERIFIED: local command] |
| PyTorch | 2.10.0+cu126 | Existing model/checkpoint dependency | Checkpoint loading and predictor execution use torch-backed models. [VERIFIED: local command] |
| PyYAML | 6.0.3 | Existing manifest parsing dependency | Study manifests and snapshots are YAML. [VERIFIED: local command] |
| Shared checkpoint | `outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt`; SHA256 `d351dd62c3b2cdb008d6952cf81b1b041b64244aa20b82fab9f742b502b7acf4` | Required formal replay checkpoint | Phase 8 and Phase 9 should require loaded checkpoint provenance. [VERIFIED: local command] |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| New validation module | Extend `baseline_validation.py` directly | Reusing the file risks mixing baseline and DSPO semantics; a sibling helper keeps Phase 8 stable. [ASSUMED] |
| New study manifest | Reuse `formal_robust_menu.yaml` | Formal manifest has heavier runtime budget and seven mainline tags, contradicting Phase 9 scope. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md] [VERIFIED: codebase grep] |
| Rerun Phase 8 baselines | Include four policies in Phase 9 manifest | Contradicts locked D-08/D-09 and would make cross-run status language ambiguous. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md] |

**Installation:** No new external packages are recommended or required. [VERIFIED: codebase grep]

## Package Legitimacy Audit

Phase 9 should not install external packages. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md] Existing dependencies are already present in the local environment and should not be changed by the implementation plan. [VERIFIED: local command]

| Package | Registry | Age | Downloads | Source Repo | slopcheck | Disposition |
|---------|----------|-----|-----------|-------------|-----------|-------------|
| None | N/A | N/A | N/A | N/A | N/A | No install planned |

**Packages removed due to slopcheck [SLOP] verdict:** none  
**Packages flagged as suspicious [SUS]:** none  

## Recommended Files To Change In Phase 9

| File | Action | Rationale |
|------|--------|-----------|
| `work2_coding/Src/policy_adapters.py` | Add `dspo_clip` and `dspo_wide` optional tags; expose helper if useful. | Existing tag registry and adapter metadata source. [VERIFIED: codebase grep] |
| `work2_coding/Experiments/studies/phase9_dspo_family_validation.yaml` | Add manifest with only `dspo_clip` and `dspo_wide`; copy the five Phase 8 splits and lightweight budget exactly. | Locked comparison bundle and paired split reuse. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md] |
| `work2_coding/Src/dspo_validation.py` | New Phase 9 validator/report helper, patterned after `baseline_validation.py`. | Keeps Phase 9 gate semantics separate from Phase 8 baseline gate. [ASSUMED] |
| `work2_coding/scripts/build_phase9_dspo_family_validation_report.py` | New CLI wrapper writing JSON and Markdown reports. | Mirrors existing Phase 8 report CLI pattern. [VERIFIED: codebase grep] |
| `work2_coding/scripts/test_phase9_dspo_family_validation.py` | New focused report/gate test file. | Mirrors script-style tests used in Phase 8. [VERIFIED: codebase grep] |
| `work2_coding/scripts/test_experiment_contracts.py` | Extend manifest loading and Phase 9 manifest contract checks. | Existing manifest registry test lists known valid manifests. [VERIFIED: codebase grep] |
| `work2_coding/scripts/test_policy_fairness_contract.py` | Extend paired field and limited-drift checks for DSPO tags. | Existing fairness test checks paired fields and policy-only drift. [VERIFIED: codebase grep] |
| `work2_coding/scripts/test_method_family_contract.py` | Extend or revise to assert Phase 9 DSPO tags are DSPO-only and independent of DSPO_PLUS. | Existing tests still validate DSPO_PLUS tags; Phase 9 should explicitly exclude them from scope. [VERIFIED: codebase grep] |
| `work2_coding/scripts/test_checkpoint_provenance.py` and `test_optout_accounting.py` | Usually no change; include in verification command set. | These already cover checkpoint and accounting contracts. [VERIFIED: codebase grep] |

## Architecture Patterns

### System Architecture Diagram

```text
Phase 9 manifest
  -> experiment_contracts.load_manifest / resolve_policy_args
  -> policy_adapters.dspo_clip / dspo_wide
  -> paired_replay.resolve_paired_settings
       -> paired-field drift check
       -> trace/settings/manifest hashes
  -> scripts/run_study.py --execute
       -> study_execution.actual_rows_for_manifest
       -> Config + DSPO_Menu + checkpoint load
       -> normalized_rows.json / study_summary.json
  -> dspo_validation.write_phase9_dspo_family_validation_report
       -> row completion/checkpoint/accounting/pairing checks
       -> artifact_status.classify_artifact for claim-ready separation
       -> Phase 8 report reference loaded as status context
  -> PHASE9_DSPO_FAMILY_VALIDATION.json / .md
```

### Recommended Project Structure

```text
work2_coding/
|-- Experiments/studies/
|   `-- phase9_dspo_family_validation.yaml
|-- Src/
|   |-- policy_adapters.py
|   |-- paired_replay.py
|   |-- study_execution.py
|   |-- artifact_status.py
|   `-- dspo_validation.py
|-- scripts/
|   |-- build_phase9_dspo_family_validation_report.py
|   |-- test_phase9_dspo_family_validation.py
|   |-- test_experiment_contracts.py
|   |-- test_policy_fairness_contract.py
|   `-- test_method_family_contract.py
`-- outputs/
    |-- studies/phase9_dspo_family_validation/<run_id>/
    `-- phase9_dspo_family_validation/
        |-- PHASE9_DSPO_FAMILY_VALIDATION.json
        `-- PHASE9_DSPO_FAMILY_VALIDATION.md
```

### Pattern 1: Adapter-Driven Policy Identity

**What:** Add `dspo_clip` and `dspo_wide` in `POLICY_ADAPTERS` with `comparison_role=dspo_family`, `menu_policy=service_guarded_expected_profit`, `menu_eta_filter_mode=interval_overlap`, `menu_contract_mode=optimized_menu`, `product_mode=m+w+p`, `time_window_mode=adaptive_window`, `menu_pricing_mode=lambertw`, `method_family=DSPO`, `method_variant=DSPO_original`, and `attention_enabled=False`. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md] [VERIFIED: codebase grep]

**When to use:** Always for Phase 9 DSPO clip/wide rows; do not reuse `mainline_optimized_adaptive`, `dspo_plus_clip`, or `dspo_plus_wide`. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md]

**Example:**

```python
# Pattern only; implement in work2_coding/Src/policy_adapters.py.
"dspo_clip": {
    "optional": True,
    "comparison_role": "dspo_family",
    "method_family": "DSPO",
    "menu_mode": "optimized_menu",
    "overrides": {
        "menu_policy": "service_guarded_expected_profit",
        "menu_eta_filter_mode": "interval_overlap",
        "service_quit_rate_guardrail": 0.35,
        "menu_optout_guardrail": 0.35,
        "method_family": "DSPO",
        "attention_enabled": False,
    },
}
```

### Pattern 2: Manifest Copies Splits, Not Baselines

**What:** Copy Phase 8 `base_args`, `paired_fields`, `varied_fields`, and all five `splits` into `phase9_dspo_family_validation.yaml`, but set `required_policy_tags` and `policies` to only `dspo_clip` and `dspo_wide`. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md] [VERIFIED: codebase grep]

**When to use:** Phase 9 primary execution. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md]

### Pattern 3: Validator Mirrors Phase 8 But Renames Gate Fields

**What:** Implement `validate_phase9_dspo_rows(rows, manifest, study_summary, phase8_report=None)` with blockers built like Phase 8 `_blocker()` objects, but report fields should be `dspo_validation_status`, `phase9_gate`, `claim_ready`, `phase8_reference_run_id`, `phase8_reference_status`, `sanity_status`, and `next_step`. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md] [VERIFIED: codebase grep]

**When to use:** Report generation and focused unit tests. [VERIFIED: codebase grep]

### Anti-Patterns to Avoid

- **Reusing `dspo_plus_clip` or `dspo_plus_wide`:** These tags encode `method_family=DSPO_PLUS` and penalty fields, which Phase 9 explicitly excludes. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md] [VERIFIED: codebase grep]
- **Putting Phase 8 baselines in the Phase 9 manifest:** Locked decisions D-08/D-09 forbid this. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md]
- **Treating sanity deltas as ranking claims:** The report can state status-only sanity context, but not manuscript ranking conclusions. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md]
- **Editing generated rows or artifacts:** Generated output must come from `run_study.py` and report builders. [CITED: AGENTS.md]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Paired replay drift checking | Custom split comparison loop in the runner | `paired_replay.resolve_paired_settings()` | It already validates paired fields and computes trace/settings hashes. [VERIFIED: codebase grep] |
| Row-v2 construction | Ad hoc dictionaries in validation code | `paired_replay.build_normalized_row()` via `study_execution` | It centralizes row fields and validation. [VERIFIED: codebase grep] |
| Actual replay execution | Bespoke DSPO loop in Phase 9 script | `scripts/run_study.py --execute` | Existing script handles manifest load, actual rows, summaries, and blockers. [VERIFIED: codebase grep] |
| Checkpoint provenance | Manual file hash fields in report only | `study_execution` checkpoint helpers plus row checks | Existing rows record path/hash/status. [VERIFIED: codebase grep] |
| Claim-ready classification | New claim logic in Phase 9 validator | `artifact_status.classify_artifact()` | Existing gate handles placeholder, failed, checkpoint, model metadata, and accounting blockers. [VERIFIED: codebase grep] |

**Key insight:** Phase 9 should add DSPO semantics at the adapter and validation layers while leaving replay, row, checkpoint, and artifact-status machinery centralized. [VERIFIED: codebase grep]

## Manifest / Report Shape

### Manifest

Recommended manifest name: `phase9_dspo_family_validation`. [ASSUMED]  
Recommended path: `work2_coding/Experiments/studies/phase9_dspo_family_validation.yaml`. [ASSUMED]

Required manifest facts:

- `tier: formal`, `run_mode: formal`, and `shared_checkpoint.required: true`. [VERIFIED: codebase grep]
- `base_args` copied from Phase 8 lightweight budget, including `max_episodes=1`, `max_steps_r=20`, `max_steps_p=0.7`, `n_vehicles=2`, `veh_capacity=3`, `hgs_reopt_time=0.1`, `hgs_final_time=0.1`, `menu_k=3`, `max_candidates=8`, `menu_exact_threshold=8`, and `menu_exact_gap_threshold=8`. [VERIFIED: codebase grep] [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md]
- `splits` copied exactly from Phase 8, including split IDs unless the planner decides to preserve values but rename IDs; locked decision says reuse split attributes exactly. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md]
- `required_policy_tags: [dspo_clip, dspo_wide]` and `policies` containing only those two tags. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md]
- `varied_fields` must include `service_quit_rate_guardrail` and `menu_optout_guardrail`, because those differ by clip/wide threshold. [VERIFIED: codebase grep] [ASSUMED]

### Report

Recommended output files:

- `work2_coding/outputs/phase9_dspo_family_validation/PHASE9_DSPO_FAMILY_VALIDATION.json`. [ASSUMED]
- `work2_coding/outputs/phase9_dspo_family_validation/PHASE9_DSPO_FAMILY_VALIDATION.md`. [ASSUMED]

Recommended top-level JSON fields:

| Field | Meaning |
|-------|---------|
| `schema_version` | Use `phase9-dspo-family-validation-v1`. [ASSUMED] |
| `dspo_validation_status` | `passed` only when all Phase 9 DSPO rows pass hard gates. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md] |
| `phase9_gate` | `open` if DSPO validation passed, otherwise `blocked`. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md] |
| `claim_ready` / `claim_ready_status` / `claim_ready_reasons` | Copied from artifact-status classification plus git/provenance separation. [VERIFIED: codebase grep] |
| `phase8_reference_run_id` / `phase8_reference_status` | Loaded from `PHASE8_BASELINE_VALIDATION.json` when available. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md] |
| `sanity_status` | Status-only summary, not ranking conclusion. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md] |
| `dspo_policy_tags` | `["dspo_clip", "dspo_wide"]`. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md] |
| `failures` | List of blockers, each with `reason`, `minimal_fix`, `rerun_command`, and `evidence_location`. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md] |
| `non_actions` | Include no baseline rerun, no DSPO_PLUS validation, no target ranking assertion, no generated-row edits. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md] |
| `next_step` | Debug handoff if blocked; otherwise status/risk-language next step only. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md] |

## Common Pitfalls

### Pitfall 1: DSPO_PLUS Residue Leaking Into Phase 9

**What goes wrong:** Implementation copies existing `dspo_plus_clip` or `dspo_plus_wide` adapters, bringing `method_family=DSPO_PLUS`, penalty fields, and Phase 10 semantics into a DSPO-only phase. [VERIFIED: codebase grep]  
**Why it happens:** `policy_adapters.py` already contains DSPO_PLUS tags from prior planning. [VERIFIED: codebase grep]  
**How to avoid:** Add fresh `dspo_clip` and `dspo_wide` tags with `method_family=DSPO` and no `dspo_plus_contract`. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md]  
**Warning signs:** Phase 9 manifest contains `dspo_plus_*`; row `method_family` contains `DSPO_PLUS`; report uses Phase 10 or ranking-ladder language. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md]

### Pitfall 2: Split Drift From Phase 8

**What goes wrong:** DSPO rows use different seeds, data seeds, uptake regimes, HGS times, menu size, candidate count, or checkpoint settings from Phase 8. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md]  
**Why it happens:** `formal_robust_menu.yaml` has heavier runtime settings than `phase8_baseline_validation.yaml`. [VERIFIED: codebase grep]  
**How to avoid:** Copy Phase 8 lightweight split and budget definitions, not the formal robust-menu runtime budget. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md]  
**Warning signs:** `max_episodes=10`, `max_candidates=10`, HGS `1.1/1.5`, or fewer/more than five splits in Phase 9 manifest. [VERIFIED: codebase grep]

### Pitfall 3: Claim-Ready And Validation Status Collapsed

**What goes wrong:** Phase 9 passes DSPO validation and then emits claim-ready or ranking language. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md]  
**Why it happens:** The artifact gate can classify rows separately from the phase gate; git dirty or dependency snapshot blockers may remain. [VERIFIED: codebase grep]  
**How to avoid:** Report `dspo_validation_status` and `claim_ready` separately, exactly as Phase 8 separated `baseline_validation_status` from `claim_ready`. [VERIFIED: codebase grep]  
**Warning signs:** Report says "DSPO improves over baselines" or omits `claim_ready=false` despite dirty/provenance blockers. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md]

### Pitfall 4: Accounting Regression

**What goes wrong:** Opt-out gets counted as accepted home pickup or served demand. [CITED: AGENTS.md]  
**Why it happens:** Row aggregations can be tempting to recompute in report code. [ASSUMED]  
**How to avoid:** Validate `accepted_count = count_accepted_home + count_accepted_meeting_point`, `served_count = accepted_count`, and rates over total choices, following Phase 8 and `test_optout_accounting.py`. [VERIFIED: codebase grep]  
**Warning signs:** `served_count` includes opt-outs or `home_share` denominator excludes opt-outs. [VERIFIED: codebase grep]

## Code Examples

### Phase 9 Run

```powershell
cd work2_coding
python scripts/run_study.py --study phase9_dspo_family_validation --execute --output-root outputs/studies
```

Source pattern: Phase 8 ran `scripts/run_study.py --study phase8_baseline_validation --execute --output-root outputs/studies`. [CITED: .planning/phases/08-baseline-validation/08-SUMMARY.md]

### Phase 9 Report

```powershell
cd work2_coding
python scripts/build_phase9_dspo_family_validation_report.py --output-root outputs/phase9_dspo_family_validation
```

Source pattern: Phase 8 uses `scripts/build_phase8_baseline_validation_report.py --output-root outputs/phase8_baseline_validation`. [VERIFIED: codebase grep]

### Validator Core Checks

```python
expected_tags = {"dspo_clip", "dspo_wide"}
for row in dspo_rows:
    require(row["status"] == "completed")
    require(row["execution_status"] == "completed")
    require(row["placeholder_only"] is False)
    require(row["method_family"] == "DSPO")
    require(row["checkpoint_load_status"] == "loaded")
    require(row["policy_tag"] in expected_tags)
```

Source pattern: Phase 8 validator checks row completion, placeholder status, checkpoint status, required fields, pairing, and accounting before passing the gate. [VERIFIED: codebase grep]

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Baselines and DSPO ladder discussed together | Phase 8 baselines passed first; Phase 9 runs DSPO clip/wide only | Phase 8 completion on 2026-06-14 | Phase 9 can reference Phase 8 report but must not rerun baselines in the primary manifest. [CITED: .planning/phases/08-baseline-validation/08-SUMMARY.md] |
| Mainline tags used as paper-facing method labels | Explicit Phase 9 `dspo_clip`/`dspo_wide` tags | Phase 9 context on 2026-06-14 | Planner should add new tags rather than reusing `mainline_optimized_adaptive`. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md] |
| DSPO_PLUS included in future roadmap text | DSPO_PLUS excluded from Phase 9 and treated as stale residue | Latest Phase 9 context on 2026-06-14 | Phase 9 implementation must not plan DSPO_PLUS work. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md] |

**Deprecated/outdated:**

- `ooh_code/` references in `.planning/codebase/` are stale; use `work2_coding/` mapped by `.planning/repository_audit.md`. [CITED: .planning/repository_audit.md]
- DSPO_PLUS references in Phase 9 scope are stale planning residue and should be excluded from Phase 9. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md]
- No-filter formal claims remain out of scope; no-filter is diagnostic unless separately justified. [CITED: AGENTS.md]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Create a sibling `Src/dspo_validation.py` rather than extending `baseline_validation.py`. | Recommended Files / Standard Stack | Minor: planner could choose another helper name, but must preserve report/gate behavior. |
| A2 | Use `phase9_dspo_family_validation` as study/report directory stem. | Manifest / Report Shape | Minor: context allows helper/report names at agent discretion. |
| A3 | Add `service_quit_rate_guardrail` and `menu_optout_guardrail` to `varied_fields`. | Manifest / Report Shape | Medium: if `validate_manifest()` already permits these through policy-only overrides differently, planner should verify with tests. |
| A4 | Report sanity comparison should use net objective/profit deltas only as status context. | Manifest / Report Shape | Medium: exact sanity metric is not locked, but ranking language must remain gated. |

## Open Questions

1. **Should Phase 9 split IDs remain `phase8_baseline_*` or be renamed while preserving split values?**
   - What we know: D-10 locks seed/data/uptake/util values exactly. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md]
   - What's unclear: Whether split ID strings themselves must be identical.
   - Recommendation: Preserve split IDs exactly unless implementation tests require Phase 9-specific IDs; if renamed, validator must record the Phase 8 source split mapping. [ASSUMED]

2. **What exact sanity metric should the report summarize?**
   - What we know: Sanity comparison is allowed only as status context and cannot block Phase 9 merely because it does not support DSPO advantage. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md]
   - What's unclear: Whether to compare `net_profit`, `net_objective_proxy`, `served_rate`, or a compact multi-metric summary.
   - Recommendation: Use a small status summary over `net_profit`, `served_rate`, and `optout_rate`, with no ranking conclusion. [ASSUMED]

3. **Should existing DSPO_PLUS tests be rewritten now or only shielded from Phase 9?**
   - What we know: Phase 9 excludes DSPO_PLUS and treats it as stale planning residue. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md]
   - What's unclear: Whether to remove existing DSPO_PLUS-focused assertions from `test_method_family_contract.py` during Phase 9 or leave them while adding DSPO-only Phase 9 assertions.
   - Recommendation: Add Phase 9 DSPO-only assertions and avoid broad DSPO_PLUS cleanup unless tests conflict with the Phase 9 manifest/report. [ASSUMED]

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| Python | Runtime/tests | yes | 3.12.4 | None needed. [VERIFIED: local command] |
| `Src.config` import from `work2_coding/` | Runtime smoke | yes | Import passed | Blocks Phase 9 if failing. [VERIFIED: local command] |
| NumPy | DSPO menu runtime | yes | 2.4.4 | None planned. [VERIFIED: local command] |
| PyTorch | Checkpoint/model runtime | yes | 2.10.0+cu126 | None planned. [VERIFIED: local command] |
| PyYAML | Manifest parsing | yes | 6.0.3 | None planned. [VERIFIED: local command] |
| Shared checkpoint | Formal actual replay | yes | SHA256 recorded above | Missing checkpoint blocks Phase 9. [VERIFIED: local command] |
| Git clean state | Claim-ready artifact status | no | Worktree dirty | Phase 9 validation may pass with `claim_ready=false`. [VERIFIED: local command] |

**Missing dependencies with no fallback:** none for Phase 9 validation execution found during research. [VERIFIED: local command]

**Missing dependencies with fallback:** clean git provenance is not available, but Phase 9 locked decisions allow DSPO validation to pass while `claim_ready=false`. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md] [VERIFIED: local command]

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Script-style Python test files with direct assertions; no pytest dependency required. [VERIFIED: codebase grep] |
| Config file | none found for a test framework in required files. [VERIFIED: codebase grep] |
| Quick run command | `cd work2_coding; python scripts/test_phase9_dspo_family_validation.py` |
| Full suite command | `cd work2_coding; python scripts/test_phase9_dspo_family_validation.py; python scripts/test_experiment_contracts.py; python scripts/test_policy_fairness_contract.py; python scripts/test_method_family_contract.py; python scripts/test_artifact_gates.py; python scripts/test_checkpoint_provenance.py; python scripts/test_optout_accounting.py` |

### Phase Requirements -> Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|--------------|
| EXP-04 | Phase 9 manifest resolves exactly two DSPO tags over five paired splits. | contract | `python scripts/test_experiment_contracts.py` | Exists, needs extension |
| EXP-04 | `dspo_clip` and `dspo_wide` emit `method_family=DSPO` and thresholds 0.35/0.45. | unit/contract | `python scripts/test_method_family_contract.py` | Exists, needs extension |
| EXP-04 | Phase 9 actual replay rows complete under paired settings. | smoke/integration | `python scripts/run_study.py --study phase9_dspo_family_validation --execute --output-root outputs/studies` | Manifest missing |
| GATE-01 | All DSPO rows record loaded checkpoint path/hash/status. | unit/integration | `python scripts/test_checkpoint_provenance.py` plus Phase 9 report test | Existing checkpoint test exists; Phase 9 report test missing |
| GATE-02 | Failed, blocked, incomplete, placeholder, contract-only rows block Phase 9 and stay non-claim-ready. | unit | `python scripts/test_phase9_dspo_family_validation.py` | Missing |
| GATE-04 | Each failure has reason, minimal fix, rerun command, and evidence location. | unit | `python scripts/test_phase9_dspo_family_validation.py` | Missing |

### Sampling Rate

- **Per task commit:** `cd work2_coding; python scripts/test_phase9_dspo_family_validation.py` after validator exists. [ASSUMED]
- **Per wave merge:** Full suite command above. [ASSUMED]
- **Phase gate:** Import smoke, focused tests, actual Phase 9 run, and Phase 9 report builder all pass. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md]

### Wave 0 Gaps

- [ ] `work2_coding/scripts/test_phase9_dspo_family_validation.py` - covers DSPO gate/report behavior. [ASSUMED]
- [ ] `work2_coding/Experiments/studies/phase9_dspo_family_validation.yaml` - covers EXP-04 manifest contract. [ASSUMED]
- [ ] `work2_coding/Src/dspo_validation.py` - covers reusable report validation logic. [ASSUMED]
- [ ] `work2_coding/scripts/build_phase9_dspo_family_validation_report.py` - covers report CLI. [ASSUMED]

## Verification Commands

Recommended Phase 9 verification sequence:

```powershell
cd work2_coding
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_phase9_dspo_family_validation.py
python scripts/test_experiment_contracts.py
python scripts/test_policy_fairness_contract.py
python scripts/test_method_family_contract.py
python scripts/test_artifact_gates.py
python scripts/test_checkpoint_provenance.py
python scripts/test_optout_accounting.py
python scripts/run_study.py --study phase9_dspo_family_validation --execute --output-root outputs/studies
python scripts/build_phase9_dspo_family_validation_report.py --output-root outputs/phase9_dspo_family_validation
```

Phase 8 command pattern and required checks are verified in Phase 8 summary/verification. [CITED: .planning/phases/08-baseline-validation/08-SUMMARY.md] [CITED: .planning/phases/08-baseline-validation/08-VERIFICATION.md]

## Security Domain

Phase 9 is an offline/local experiment validation phase; it does not add authentication, sessions, remote APIs, or user input surfaces beyond existing local CLI manifest execution. [CITED: .planning/ROADMAP.md] [VERIFIED: codebase grep]

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|------------------|
| V2 Authentication | no | No auth surface in Phase 9. [VERIFIED: codebase grep] |
| V3 Session Management | no | No session surface in Phase 9. [VERIFIED: codebase grep] |
| V4 Access Control | no | Local-only research workflow; no new access boundary. [CITED: .planning/ROADMAP.md] |
| V5 Input Validation | yes | Use existing manifest/parser validation and policy-only override guards. [VERIFIED: codebase grep] |
| V6 Cryptography | yes, provenance only | Use SHA256 file hashes already used for checkpoint/readiness provenance; do not hand-roll new crypto. [VERIFIED: codebase grep] |

### Known Threat Patterns for Local Experiment Gating

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Stale or wrong manifest inputs | Tampering | Validate known policy tags, paired fields, required tags, parser choices, and manifest hash. [VERIFIED: codebase grep] |
| Missing or random checkpoint used as evidence | Tampering/Repudiation | Require `checkpoint_load_status=loaded` and checkpoint hash for every DSPO row. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md] |
| Generated evidence edited by hand | Repudiation | Consume generated `normalized_rows.json` and write validation reports from code only. [CITED: AGENTS.md] |

## Sources

### Primary (HIGH confidence)

- `.planning/phases/09-dspo-family-full-run/09-CONTEXT.md` - locked Phase 9 decisions, DSPO-only boundary, thresholds, report language, output boundaries.
- `.planning/phases/08-baseline-validation/08-SUMMARY.md` - Phase 8 run ID, commands, and handoff.
- `.planning/phases/08-baseline-validation/08-VERIFICATION.md` - Phase 8 passed checks and evidence paths.
- `.planning/repository_audit.md` - active `work2_coding/` root and stale `ooh_code/` mapping.
- `work2_coding/Src/policy_adapters.py` - adapter registry, existing DSPO and DSPO_PLUS tag patterns.
- `work2_coding/Src/paired_replay.py` - row-v2 schema, paired setting resolution, row validation.
- `work2_coding/Src/study_execution.py` - actual replay, checkpoint metadata, failed-row handling.
- `work2_coding/Src/baseline_validation.py` - Phase 8 validator/report template.
- `work2_coding/Src/artifact_status.py` - artifact/claim-ready classification.
- `work2_coding/Src/Algorithms/DSPO_Menu.py` - guardrail thresholds and DSPO menu metadata.
- `work2_coding/Experiments/studies/phase8_baseline_validation.yaml` - split and runtime budget source.
- Required script tests under `work2_coding/scripts/` - current test style and contracts.

### Secondary (MEDIUM confidence)

- Local environment commands for Python/package versions, import smoke, checkpoint hash, and git dirty status.

### Tertiary (LOW confidence)

- None from web search. No external web research was needed because this is a codebase-only phase.

## Metadata

**Confidence breakdown:**

- Standard stack: HIGH - all recommended components are existing local modules or locally available dependencies. [VERIFIED: local command]
- Architecture: HIGH - integration points are directly verified from required source files. [VERIFIED: codebase grep]
- Pitfalls: HIGH for DSPO_PLUS leakage, split drift, checkpoint, and accounting risks; MEDIUM for exact report helper naming because the context leaves names to implementer discretion. [CITED: .planning/phases/09-dspo-family-full-run/09-CONTEXT.md]

**Research date:** 2026-06-14  
**Valid until:** 2026-07-14, or earlier if Phase 9 context, Phase 8 outputs, or adapter contracts change. [ASSUMED]
