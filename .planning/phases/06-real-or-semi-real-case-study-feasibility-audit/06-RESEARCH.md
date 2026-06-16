---
phase: 06-real-or-semi-real-case-study-feasibility-audit
status: complete
researched: 2026-06-15T21:45:00+08:00
timezone: Asia/Shanghai
research_mode: inline
requirements:
  - CASE-01
  - CASE-02
  - CASE-04
---

# Phase 6 Research: Real Or Semi-Real Case Study Feasibility

## Research Question

Can Work2 add a real or semi-real TR-E case study in a reproducible way without
fabricating passenger behavior, tuning RC evidence, or weakening the current
claim gates?

## Short Answer

Yes, but only as a semi-real external scenario approved in principle and
blocked from case execution until upstream gate cleanup. The strongest route is
public OSM/open-network geography with simulated, pre-registered DRT demand and
simulated choice behavior. Yanjiao/Beijing commuting material is useful for
narrative motivation, but current public evidence found during planning is
better suited as context than as a fully reproducible case-study data source.

Recommended decision label:

`approved_blocked_pending_gate_cleanup`

## Source Findings

| Source route | Evidence found | Feasibility | Main limitation |
| --- | --- | --- | --- |
| OSM + Geofabrik extracts | Geofabrik provides regional OpenStreetMap extracts, updated frequently, in `.osm.pbf` and GIS formats. | High | Must respect OSM/ODbL attribution and database-share obligations where applicable. |
| OSMnx | OSMnx can download street networks, POIs, transit stops, speeds/travel times, and shortest paths from OSM-backed APIs. | High | Python dependency and API/network availability must be pinned or cached. |
| OSRM | OSRM is an open-source routing engine on OSM data; its Table service computes distance/duration matrices. | High | Requires local preprocessing/Docker or equivalent reproducible routing setup. |
| GTFS + Mobility Database | GTFS is an open standard for static transit data; Mobility Database catalogs thousands of GTFS/GTFS-RT/GBFS feeds. | Medium | Good for transit stops/routes where available, but coverage/licensing varies by agency and region. |
| Yanjiao/Beijing commuting material | Public narrative and research sources identify Yanjiao/Beijing long-commute context and Beijing public transport constraints. | Medium for motivation, low-to-medium for reproducible case data | Public sources do not by themselves provide audited DRT demand, passenger choice, or a complete distance matrix. |
| Existing Amazon/RC/HombergerGehring data | Existing benchmark data are already in `work2_coding/Environments/OOH/`. | Medium as external benchmark reference | They must not be relabeled as real-city DRT passenger behavior. |

## Source Links

Accessed during planning on 2026-06-15.

- Geofabrik OSM extracts: https://www.geofabrik.de/data/download.html
- OpenStreetMap copyright/license: https://www.openstreetmap.org/copyright
- Overpass API: https://wiki.openstreetmap.org/wiki/Overpass_API
- OSMnx getting started: https://osmnx.readthedocs.io/en/stable/getting-started.html
- OSRM backend: https://github.com/Project-OSRM/osrm-backend
- GTFS overview: https://gtfs.org/documentation/overview/
- Mobility Database: https://mobilitydatabase.org/
- Yanjiao commuting narrative: https://www.theworldofchinese.com/2022/05/how-the-pandemic-delayed-the-dreams-of-a-beijing-bedroom-community/
- Beijing/Yanjiao commuting equity context: https://www.mdpi.com/2071-1050/11/21/5884
- Beijing public transport background: https://www.esmap.org/sites/esmap.org/files/10282009102930_Beijing_Transport_finalReport.pdf

## Recommended Candidate Ranking

1. Public OSM/open-network city corridor:
   highest reproducibility because road network, POIs, transit stops, routing
   matrix generation, and licensing can be documented and rebuilt.
2. OSM plus GTFS/transit-stop enrichment:
   useful if a candidate city has a stable feed in Mobility Database or an
   agency open-data portal; stronger for meeting-point candidate realism.
3. Yanjiao/Beijing motivated semi-real case:
   valuable paper story if local materials are available, but the feasibility
   report must not rely on unaudited anecdotal demand or non-reproducible
   sources.
4. Existing public benchmark data:
   acceptable as a fallback external scenario, not as a real-city DRT case.

## Minimum Semi-Real Contract

A Phase 7 case is acceptable only if it records:

- documented real geography;
- plausible depot/destination and corridor definition;
- candidate meeting points from public POIs, transit stops, parking/community
  entrances, or pre-registered synthetic grid/cluster rules;
- road-network distance or a reproducible distance matrix with source,
  version/date, parameters, cache path, and hash;
- simulated sequential demand labeled as simulated;
- simulated passenger choice labeled as simulated;
- seven-tag mainline comparison by default, with a documented reduced-family
  gate if any tag cannot run fairly for data/contract reasons;
- no use of case-study outcomes to tune RC final settings.

## Planning Implications

- Phase 6 should write `.planning/data/CASE_STUDY_FEASIBILITY.md` as the
  primary decision artifact.
- `work2_coding/outputs/phase6_audit/PHASE6_AUDIT.md` and `.json` are useful
  support evidence for runtime/gate state, but they do not replace the
  feasibility report.
- Phase 6 should approve the semi-real route only with the gate-aware status
  `approved_blocked_pending_gate_cleanup`.
- Phase 7 may prepare ingestion, validation, manifest scaffolding, and
  reproducibility checks before gate cleanup, but must not run semi-real case
  experiments or create case-study result claims while gates remain blocked.

## Research Complete

