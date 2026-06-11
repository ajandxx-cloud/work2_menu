# Experiment Outline

## Scenarios

The study ladder is smoke, pilot, and formal. Smoke validates contracts and schema. Pilot and formal tiers require loaded checkpoint provenance before they can support manuscript claims.

## Baselines

Policy comparisons include full display, home only, nearest heuristic, top-k cheapest, min-lateness, hard filter, robust risk-adjusted, robust service-guarded, optional random top-k, and diagnostic no-filter.

## Metrics

Metrics include expected or realized net profit, acceptance, opt-out, non-home uptake, ETA pruning behavior, service-quality diagnostics, solver build time, exact/greedy quality, and provenance/status fields.

## Paired Replay

Compared policies must share request traces, seeds, split IDs, pricing mode, checkpoint provenance, routing/HGS settings, and manifest/settings hashes.

## Checkpoints And Uptake Regimes

Current uptake regimes recorded by artifacts: low, medium. Diagnostic policies such as no_filter_diagnostic are reported as diagnostics only.
