# TR-E Manuscript Structure

## Manuscript Rule

The final manuscript body must be written in academic English paragraphs, not
as bullet-style prose. This file is an outline and control document only.

## 1. Introduction

Purpose:

- Motivate many-to-one DRT and last-mile service operations.
- Explain why displayed service menus are operational decision objects.
- Define the service product as meeting point plus pickup time window plus
  price.
- State contributions in claim-safe language.

Claim-ready path:

- State only the specific claims authorized by regenerated strict claim guard.

Diagnostic path:

- State formulation, paired replay evaluation, artifact-gated reporting, and
  transparent claim-boundary analysis as the contribution.

## 2. Literature Review

Cover:

- DRT and last-mile operations.
- Meeting-point and flexible pickup service.
- Time-window design and service reliability.
- Passenger choice and menu or assortment-style service design.
- Pricing and operational decision integration.
- Reproducible and artifact-gated computational experimentation.

Avoid claiming that the current paper closes all empirical gaps.

## 3. Problem Description

Cover:

- Sequential requests.
- Fleet state.
- Candidate meeting points.
- Pickup windows.
- Prices.
- Home service.
- Outside option.
- Accepted service versus opt-out accounting.

## 4. Mathematical Model

Cover:

- Sets and indices.
- Service bundle `b = (m,w,p)`.
- Menu variable.
- Feasibility constraints.
- MNL choice probabilities.
- Expected profit objective.
- Service guardrails.
- ETA/window feasibility.
- Exact and greedy menu construction contracts.

## 5. Solution Method

Cover:

- Candidate bundle generation.
- Menu construction.
- Adaptive versus fixed windows.
- Lambert-W pricing.
- Exact enumeration and greedy fallback contract.
- Computational diagnostics and limitations.

## 6. Experimental Design

Cover:

- RC paired replay.
- Seven policy tags.
- Metrics: `net_profit`, `adjusted_profit`,
  `service_constrained_net_profit`, `acceptance_rate`, `opt_out_rate`,
  `home_share`, `non_home_uptake`, `served_rate`, status fields, checkpoint
  fields.
- Evidence tiers: formal, diagnostic, blocked, scaffold-only.
- Claim gates: readiness, row status, artifact status, strict claim guard.

## 7. Results

If `claim_ready=true`:

- Present only claims authorized by strict claim guard.

If `claim_ready=false`:

- Lead with claim-gate status.
- Present diagnostic boundary evidence only.
- Do not hide negative or mixed results.
- Do not convert blocked main RC artifacts into positive results.
- Label Phase 8 and Phase 9 evidence diagnostic unless upgraded.
- Label case-study material as scaffold/future work unless upgraded.

## 8. Discussion

Cover:

- What the formulation contributes.
- Why certain claims are blocked.
- When service-menu optimization may help or fail.
- Reviewer risks.
- Future steps for real calibration, larger formal evidence, executed case
  study, and computational scaling.

## 9. Conclusion

Claim-safe summary only.

If `claim_ready=false`, conclude with formulation, diagnostic evidence, and
reproducibility boundary, not performance superiority.

If a conditional claim is authorized, state the condition precisely.

## 10. Appendix

Include:

- Artifact and claim source map.
- Status transparency table.
- Diagnostic sensitivity details.
- Computational diagnostics.
- Case-study scaffold documentation if still scaffold-only.
- Prohibited language check.
