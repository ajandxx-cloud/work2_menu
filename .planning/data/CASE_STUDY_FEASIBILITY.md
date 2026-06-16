---
phase: 06-real-or-semi-real-case-study-feasibility-audit
decision: add semi-real case
status: approved_blocked_pending_gate_cleanup
created: 2026-06-15T21:35:00+08:00
timezone: Asia/Shanghai
requirements:
  - CASE-01
  - CASE-02
  - CASE-04
case_execution_gate: scaffolding_only_until_provenance_readiness_artifact_claim_gates_pass
primary_runtime_root: work2_coding/
supporting_audit:
  markdown: work2_coding/outputs/phase6_audit/PHASE6_AUDIT.md
  json: work2_coding/outputs/phase6_audit/PHASE6_AUDIT.json
---

# Case Study Feasibility

## Decision

Decision: `add semi-real case, approved_blocked_pending_gate_cleanup`.

Work2 should add a semi-real external scenario if Phase 7 can make the
geography, road network, candidate meeting points, distance matrix, simulated
demand, and simulated choice labels reproducible. This is not approval to run
case experiments yet. While provenance, readiness, artifact, and claim gates
remain blocked, Phase 7 may prepare ingestion design, validation contracts,
manifest scaffolding, cached-source checks, and rebuild commands only.

Blocked before gate cleanup:

- semi-real or real case experiment execution;
- generated case-study result rows, tables, figures, or manuscript claims;
- using case-study outcomes to tune RC calibration or final settings;
- any claim of real passenger acceptance, opt-out, choice, or profit.

Allowed before gate cleanup:

- source selection and licensing notes;
- ingestion and validation scaffolding;
- candidate-point rules and distance-matrix rebuild contract;
- demand-generation protocol drafts with pre-registered seeds;
- dry validation that does not create case-study evidence claims.

The paper value is supplemental external-scenario robustness. The RC formal
ladder remains the main empirical ladder. If later case results conflict with
RC evidence, the conflict must be reported honestly rather than averaged away.

## Gate Evidence

The supporting runtime/gate audit was generated from `work2_coding/` with:

```powershell
python scripts/audit_phase6_experiment_state.py --output-root outputs/phase6_audit --format markdown
```

The audit reports:

- runtime import: `IMPORT_OK`;
- readiness status: `blocked`;
- `checkpoint_load_status`: `loaded`;
- claim-ready: `false`;
- claim-ready artifacts: `blocked`;
- formal replay was not run;
- generated rows, tables, figures, and manuscript claims were not hand-edited.

Supporting paths:

- `work2_coding/outputs/phase6_audit/PHASE6_AUDIT.md`
- `work2_coding/outputs/phase6_audit/PHASE6_AUDIT.json`

## Source Audit

Access date for external sources: 2026-06-15.

| Source route | URLs | Data type | License/access notes | Reproducibility path | Expected preprocessing | Limitation for TR-E claim language |
| --- | --- | --- | --- | --- | --- | --- |
| OSM / Geofabrik extracts | https://download.geofabrik.de/ ; https://www.openstreetmap.org/copyright | Road network, POIs, land-use and map features from OpenStreetMap extracts | OSM data are under ODbL; outputs need OSM attribution and database-license review before distributing derived matrices or map artifacts. Geofabrik provides frequently updated extracts, so the extract date and hash must be pinned. | Download a bounded region extract, store raw `.osm.pbf` metadata, source URL, access date, file hash, and extraction command. | Clip corridor/service area; filter drivable network; extract candidate POIs/stops/parking/community entrances; build node and edge tables; create matrix inputs. | Real geography/network only. Does not provide real DRT demand, real passenger choice, real acceptance, or real profit. |
| Overpass / OSMnx extraction | https://wiki.openstreetmap.org/wiki/Overpass_API ; https://osmnx.readthedocs.io/en/stable/getting-started.html | Programmatic OSM network and feature extraction | Public Overpass endpoints have rate/resource limits. For reproducibility, cache query results or prefer a pinned Geofabrik extract where possible. OSMnx dependency versions must be recorded. | Save polygon/bbox, Overpass query or OSMnx call, package versions, raw GeoJSON/GraphML cache, hash, and rebuild script. | Build drivable graph; impute speeds/travel times if needed; simplify topology; extract POI categories for meeting points. | API extraction is reproducible only if queries, cache, package versions, and OSM snapshot/date are pinned. |
| OSRM or equivalent local routing/matrix generation | https://github.com/Project-OSRM/osrm-backend | Road-network shortest path, duration, and distance matrix generation | OSRM backend is open-source; local setup should be containerized or scripted. Matrix services depend on the same OSM extract and profile. | Preprocess the pinned OSM extract locally, record OSRM profile, Docker/image version or binary version, command log, matrix cache path, and matrix hash. | Snap depot, destination, demand origins, and candidate meeting points to the road graph; compute many-to-many distance/duration matrices; validate unreachable pairs. | Required for formal/semi-real evidence. Euclidean distance is diagnostic only and cannot support paper-facing operational claims. |
| GTFS / Mobility Database transit-stop enrichment | https://gtfs.org/documentation/overview/ ; https://mobilitydatabase.org/ | Transit stops, routes, trips, optional feed metadata | GTFS is an open standard, but each feed has agency-specific license, freshness, and coverage. Mobility Database is a feed catalog, not proof of local DRT demand. | Select feed, record feed URL, agency/license notes, feed version/date, validator status if available, and cache hash. | Extract stops and transfer nodes; optionally use them as explainable candidate meeting points; deduplicate with OSM POIs. | Useful for candidate realism, not passenger behavior validation. Transit stops do not imply DRT demand or acceptance. |
| Yanjiao / Beijing commuting materials | https://www.theworldofchinese.com/2022/05/how-the-pandemic-delayed-the-dreams-of-a-beijing-bedroom-community/ ; https://www.mdpi.com/2071-1050/11/21/5884 ; https://www.esmap.org/sites/esmap.org/files/10282009102930_Beijing_Transport_finalReport.pdf | Narrative commuting context, regional commute/travel-equity literature, Beijing public-transport background | Public narrative and academic materials can motivate a corridor, but they are not a complete open DRT dataset. Individual anecdotes must not be converted into demand calibration. | Record citation metadata, access date, and the exact role of each source: motivation, geography, or transport context. | Use only to motivate a Yanjiao/Beijing corridor or explain why a many-to-one commute scenario is plausible. Combine with reproducible OSM/OSRM network data if selected. | Not audited passenger microdata. Cannot support real acceptance, opt-out, choice, or profit claims. |
| Existing Amazon and HombergerGehring benchmark roots | `work2_coding/Environments/OOH/Amazon_data/`; `work2_coding/Environments/OOH/HombergerGehring_data/` | Existing benchmark/customer and RC benchmark data already in the repository | Already useful for benchmark and RC evidence, but not a real-city DRT passenger case. Do not relabel as Yanjiao, Beijing, or real passenger behavior. | Keep as baseline/benchmark references with repository paths and hashes. | Use for comparison, smoke, or fallback external benchmark only. | Synthetic/benchmark evidence; not a semi-real real-network case unless paired with a documented real network and simulated demand labels. |

## Candidate Ranking

Scoring scale: 1 low, 5 high.

| Rank | Route | Reproducibility | Licensing/access | Matrix rebuildability | DRT plausibility | Paper value | Decision |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | Public OSM/open-network corridor with local OSRM matrix | 5 | 4 | 5 | 4 | 4 | Default Phase 7 route |
| 2 | OSM network plus GTFS/transit-stop candidate enrichment | 4 | 3 | 4 | 4 | 4 | Strong if feed licensing is clean |
| 3 | Yanjiao/Beijing motivated semi-real corridor over OSM/OSRM | 3 | 3 | 4 | 5 | 5 | Valuable narrative route if source documentation is sufficient |
| 4 | Existing Amazon/HombergerGehring benchmark scenario | 4 | 4 | 2 | 2 | 2 | Benchmark fallback, not a real-city DRT case |

If both a Yanjiao/Beijing route and a generic public OSM/open-network route are
feasible, Phase 7 should default to public OSM/open-network data unless the
Yanjiao/Beijing materials can be documented with equal reproducibility.

## Minimum Semi-Real Contract

A Phase 7 case is acceptable only if it records all of the following before any
case experiment execution:

1. Documented real geography with a bounded corridor or service area.
2. Plausible depot/destination and candidate meeting-point definition.
3. Candidate meeting points from public POIs, transit stops, parking/community
   entrances, pickup points, or pre-registered synthetic grid/cluster rules.
4. Real road-network distance or a reproducible distance matrix with source
   URL, extraction date/version, parameters, cache path, hash, and rebuild
   command.
5. Simulated sequential demand with pre-registered seeds, OD/time pattern,
   volume/range, and sampling rules.
6. Simulated choice behavior labeled as simulated.
7. Seven-tag mainline comparison by default:
   `mainline_no_menu`, `mainline_fixed_menu`, `mainline_random_menu`,
   `mainline_optimized_m`, `mainline_optimized_mw`,
   `mainline_optimized_fixed_window`, and
   `mainline_optimized_adaptive`.
8. A reduced-family gate for any tag reduction, documenting which tag is
   infeasible, why the reason is data/contract based rather than outcome
   selection, whether the reduced family still answers the case question, and
   why no unfavorable baseline is selectively removed.
9. No use of case-study outcomes to tune RC settings, calibration settings, or
   final formal settings.
10. Mandatory labels for `semi-real`, `simulated demand`, and
    `simulated choice` in future tables, figures, artifact metadata, and
    manuscript text.

Euclidean distance is allowed only as a diagnostic fallback for smoke testing
the scaffolding. Formal or paper-facing semi-real evidence requires real
road-network distance or a reproducible matrix.

## Phase 7 Preprocessing Plan

Phase 7 should prepare these steps without running case experiments while gates
remain blocked:

1. Choose a corridor or service area and record the source route decision.
2. Cache raw OSM/GTFS inputs with access dates, hashes, and license notes.
3. Build a road graph and candidate-point layer from documented rules.
4. Build and validate a road-network distance/duration matrix.
5. Define simulated demand generation with fixed seeds and OD/time rules.
6. Define manifest scaffolding for the seven-tag family.
7. Add validation checks for source hashes, matrix shape, reachable pairs,
   candidate labels, simulated-demand labels, and reduced-family gate status.
8. Keep all case output directories separate from RC calibration and final
   evidence.

Required Phase 7 code changes, if Phase 7 proceeds:

- case-source metadata schema;
- source ingestion/cache script;
- distance-matrix builder or OSRM/OSMnx adapter;
- candidate meeting-point builder;
- simulated-demand generator with pre-registered seeds;
- validation script and script-style tests;
- case-study manifest scaffold that preserves paired replay fairness.

## Claim Language Boundary

Allowed future wording after Phase 7 scaffolding:

> The case-study extension uses real geography and a reproducible road-network
> matrix with simulated demand and simulated choice behavior.

Not allowed:

- real passenger behavior was observed;
- real acceptance or opt-out rates were measured;
- real operating profit was measured;
- simulated demand validates actual Yanjiao/Beijing passenger choices;
- case-study evidence overrides blocked RC formal gates.

## Requirement Coverage

- `CASE-01`: covered by the source audit across Yanjiao/commuting materials,
  public network/mobility options, and synthetic-over-real-network routes.
- `CASE-02`: covered by the no-fabricated-data boundary and mandatory labels
  for simulated demand and simulated choice.
- `CASE-04`: covered by the minimum semi-real contract.

## Closeout

Phase 6 approves the semi-real route in principle but keeps case execution
blocked pending upstream gate cleanup. Phase 7 should not be skipped. It may
prepare scaffolding and validation contracts, but it must not run semi-real
case experiments or upgrade manuscript claims while readiness, artifact, and
claim gates remain blocked.
