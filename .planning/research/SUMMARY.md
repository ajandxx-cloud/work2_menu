# Research Summary: Work2 TR-E Service Menu Optimization

**Created:** 2026-06-14
**Sources:** `工作二讨论6.14.txt`, attached GSD new-project prompt, current
filesystem audit, existing `.planning/codebase/` maps, and deleted prior GSD
core documents read from Git history for continuity.

## Key Findings

Work2 should be positioned as a TR Part E service-operations and transportation
optimization paper, not as a passenger-behavior-only paper, not as a
pricing-only extension, and not as an attention-method paper.

The central contribution is dynamic front-end service menu optimization. For
each sequentially arriving request in a many-to-one DRT system, the platform
chooses a limited menu of service bundles:

```text
(meeting point, pickup time window, price)
```

The primary V1 method is `mainline_optimized_adaptive`, interpreted as optimized
menu plus adaptive pickup-time window plus Lambert-W pricing. The planned
evidence ladder should compare it against no-menu, fixed-menu, random-menu,
product ablations, and fixed-window baselines under paired RC replay.

## Current Repository Status

The active runtime root is `work2_coding/`. Import smoke passed on 2026-06-14:

```powershell
python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"
```

Current filesystem checks show:

- `work2_coding/Src/Algorithms/DSPO_Menu.py` exists.
- `work2_coding/Experiments/studies/formal_robust_menu.yaml` exists.
- `work2_coding/scripts/train_shared_checkpoint.py` exists.
- `work2_coding/scripts/check_formal_readiness.py` exists.
- `work2_coding/scripts/run_study.py` exists.
- `work2_coding/scripts/build_artifacts.py` exists.
- `work2_coding/scripts/build_manuscript_frame.py` exists.

The older `.planning/codebase/` maps still reference `ooh_code/` heavily.
Those maps are useful for architectural memory, but Phase 1 must verify all
current paths against `work2_coding/`.

## Main Scientific Boundary

The current project may have smoke, pilot, and artifact pipeline evidence, but
the 6.14 discussion is explicit: current results are not yet sufficient for a
TR Part E empirical superiority claim.

Allowed current statement:

> The implementation and experiment pipeline support paired comparison of
> service-menu policies and artifact-gated reporting.

Not allowed until gates pass:

> The optimized adaptive service menu is empirically superior to all baselines.

## Recommended Evidence Structure

1. Mainline performance comparison across the seven V1 tags.
2. Product composition ablation: `m`, `m+w`, `m+w+p`.
3. Time-window mechanism ablation: fixed versus adaptive, with ETA robustness.
4. Exact versus greedy tractability.
5. Sensitivity analysis across menu size, candidate size, ETA uncertainty,
   uptake behavior, guardrails, and fleet/capacity stress.
6. Optional real or semi-real case study after RC formal evidence is stable.

## Main Risks

- Formal checkpoint or readiness blockers may prevent claim-ready artifacts.
- Results may be mixed; the paper may need conditional rather than strong
  claims.
- If the same choice model is used for optimization and simulation, reviewers
  may ask for misspecification or sensitivity experiments.
- RC-only evidence may look too synthetic for TR Part E without a semi-real
  case or strong robustness section.
- Attention must not distract from the V1 service-menu contribution.

## Planning Implication

The roadmap should begin with state locking, then lock the paper-level research
design before formal experiments. Formal evidence must be generated and
diagnosed before calibration, case-study expansion, sensitivity, artifact
generation, manuscript writing, and final readiness review.

---
*Research summary initialized: 2026-06-14*
