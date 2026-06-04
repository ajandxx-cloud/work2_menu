# Work 2: Choice-Aware DRT Service Menu Optimization

## What This Is

This project rebuilds Work 2 from insertion-cost representation learning into choice-aware, profit-aware dynamic service menu optimization for demand-responsive transit. The immediate purpose is to complete an experiment program that can support a defensible TR Part E conclusion: DRT menu design should explicitly account for passenger choice, opt-out risk, pricing, and route-cost feedback rather than only ranking meeting points by predicted insertion cost.

CNN-SetMenuNet is no longer treated as the main positive contribution. It remains valuable as a learned baseline and diagnostic result showing where insertion-cost-based menu design can become misaligned with realized system profit.

## Core Value

Produce complete, reproducible experimental evidence that either supports or falsifies the new conclusion: choice-aware expected-profit menu optimization provides a more robust profit-service tradeoff than insertion-cost-only menu selection.

## Requirements

### Validated

- Existing Work 1 pricing, MNL passenger choice, HGS route-cost feedback, YAML study execution, artifact generation, and manuscript workflow are implemented in `ooh_code/`.
- Existing Work 2 CNN-SetMenuNet formal evidence is available and shows mixed/inconclusive support for the old claim.
- Formal RC diagnostics show CNN-SetMenuNet does not improve mean net profit over Cost-L or CNN-Menu under the current insertion-cost objective.
- The codebase has a mapped architecture and known experiment entry points: `ooh_code/Src/Algorithms/DSPO_Menu.py`, `ooh_code/Src/research_pipeline.py`, `ooh_code/scripts/run_study.py`, and `ooh_code/scripts/build_artifacts.py`.
- Phase 1 reframed Work 2 around choice-aware / profit-aware service menu optimization.
- Phase 2 added adjusted profit, service-constrained profit, and oracle taxonomy diagnostics.
- Phase 3 implemented explicit Expected-Profit Enumeration, Service-Constrained Expected-Profit, Cost Oracle, and Profit Oracle policy contracts.
- Phase 4 ran Phase08 smoke and the 3-seed pilot; the decision gate completed and routed to `recalibrate_objective`.

### Active

- [ ] Review Phase08 recalibration evidence before any formal rerun.
- [ ] Diagnose whether objective/service parameters, fallback behavior, MNL outside option, price range, candidate generation, or scenario design caused the Phase08 guardrail failures.
- [ ] Run formal multi-seed experiments and rebuild manuscript-facing artifacts only after the recalibration/scenario-design decision is resolved.

### Out of Scope

- Continuing to force CNN-SetMenuNet as the main positive method -- current formal evidence does not support that narrative.
- Changing the core Lambert-W pricing model -- keep pricing stable so the menu objective is isolated.
- Changing the core MNL passenger choice model -- use the existing choice model as the behavioral environment.
- Changing HGS/Hygese route-cost evaluation -- route feedback remains the evaluation backend, not the contribution.
- Running a large formal experiment before smoke and 3-seed pilot diagnostics pass.
- Contextual bandit / offline policy learning as the first refactor -- defer until expected-profit enumeration proves the objective is meaningful.

## Context

The previous Work 2 project attempted to prove that CNN-SetMenuNet's set-attention representation improves DRT service menu design by better predicting candidate insertion costs and selecting Top-L meeting points. Formal RC results do not support that as the primary claim: CNN-SetMenuNet underperforms Cost-L and CNN-Menu in mean net profit, while some learned methods show degenerate high quit rates that can make raw net profit misleading.

The key scientific pivot is not "make CNN-SetMenuNet win." The stronger question is: why does low insertion cost fail to imply high realized system profit, and how should menu value be defined when passenger choice, pricing, opt-out behavior, and route costs interact?

The recommended experiment path is:

1. Establish objective alignment with Expected-Profit Enumeration.
2. Add service constraints or quit penalties to prevent high-opt-out false positives.
3. Split cost oracle from profit oracle so "oracle" claims match the actual target.
4. Only after the non-learning objective works, learn a ProfitAware scoring or menu-level value model.

## Constraints

- **Existing worktree**: The repository currently contains many uncommitted code and artifact changes. Do not revert unrelated user work.
- **Scientific traceability**: Do not manually edit generated result rows toward a desired conclusion. Experiments must flow from manifests to outputs to artifacts.
- **Stable behavioral model**: MNL choice and outside-option behavior remain unchanged during the first refactor.
- **Stable routing backend**: HGS/Hygese route-cost evaluation remains unchanged during the first refactor.
- **Stable pricing backend**: Lambert-W pricing remains unchanged during the first refactor.
- **Pilot first**: New objective methods must pass smoke and 3-seed pilot diagnostics before formal evidence is claimed.
- **Conclusion honesty**: If Expected-Profit / Service-Constrained methods do not beat Cost-L or CNN-Menu on adjusted/service-constrained metrics, the output must diagnose simulation objective, MNL parameters, price range, candidate generation, or scenario design rather than inventing a positive result.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Reframe Work 2 around choice-aware expected profit | Formal evidence does not support insertion-cost representation learning as the main contribution | Complete in Phase 1 |
| Keep CNN-SetMenuNet as baseline / diagnostic | It remains useful evidence of objective mismatch | Complete in Phase 1 |
| Add adjusted profit and service guardrails | Raw net profit can be polluted by high quit-rate policies | Complete in Phase 2 diagnostics and Phase 3 service-constrained policy |
| Split Cost Oracle and Profit Oracle | A true-cost Top-L oracle is not a profit upper bound | Complete in Phase 3 policy/artifact semantics |
| Start with exact enumeration before new learning models | `K=10`, `L=3` yields only 120 menus, so the objective can be tested without neural instability | Complete in Phase 3 smoke |
| Stop formal evidence after Phase08 recalibration decision | Phase08 pilot completed but expected-profit methods violated service guardrails and Service-Constrained Expected-Profit used fallback | Complete in Phase 4 |
| Defer contextual bandits | Stronger but unnecessary before validating the objective | Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition**:
1. Requirements invalidated? Move to Out of Scope with reason.
2. Requirements validated? Move to Validated with phase reference.
3. New requirements emerged? Add to Active.
4. Decisions to log? Add to Key Decisions.
5. "What This Is" still accurate? Update if drifted.

**After each milestone**:
1. Full review of all sections.
2. Core Value check -- still the right priority?
3. Audit Out of Scope -- reasons still valid?
4. Update Context with current evidence.

---
*Last updated: 2026-06-05 after Phase 4 verification*
