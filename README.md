# Denver's Tree-of-Heaven Problem: A Data Brief

*What 731 citizen-science observations, 5,580 city complaints, and the parcel map say about an invasive tree — and why Colorado should list it as a noxious weed.*

Full brief: [brief/tree-of-heaven-denver-brief.md](brief/tree-of-heaven-denver-brief.md)

## Findings

**1. At least 43% of Denver's reported tree-of-heaven is on private land — and the true share is higher.** 214 of 493 geocoded observations fall on privately owned parcels. iNaturalist observers record what they can see from the sidewalk, so backyard trees are systematically undercounted: 43% is a floor, not the number. No public-land-only strategy can work.

**2. Reports are climbing and spreading.** From 24 observations in 2016 to 129 in 2025, spanning Lincoln Park, City Park, Five Points, and outward.

**3. The city doesn't close weed complaints.** 75% of 4,173 "Weeds/Vegetation Violation" 311 cases were never closed (vs. 3% for fallen trees). Worst: Harvey Park (93% open); best: Belcaro (48%) — a stark southwest/southeast gradient.

**4. The case for listing.** Tree of heaven sits on Colorado's official Watch List — the state flags the threat and requires nothing. Eight states list it as a noxious weed. A Colorado List B designation would trigger mandatory control on all private lands, with county abatement, property liens, and fines. Spotted lanternfly (whose preferred host is tree of heaven, per the state ag department) is confirmed in Iowa and Illinois — not yet Colorado.

## Contents

- `brief/` — the full data brief with methods and caveats
- `charts/` — 6 charts (hotspot map, ownership map, time trend, 311 analyses)
- `data/` — neighborhood-level aggregates (no precise coordinates published: many trees are on private property, and this brief maps the problem, not individual yards)
- `code/` — analysis pipeline
- `notes/` — data source documentation and policy research

## Reproduce it

The point-level pull is fully scripted: GBIF (`api.gbif.org`) + iNaturalist (`api.inaturalist.org`) for *Ailanthus altissima* in the Denver metro bbox, Denver Open Data parcel and 311 ArcGIS services, documented in `notes/`. The analysis joins observations to parcels for the ownership split.

## Caveats

Presence-only citizen-science data with heavy observer bias; time trends conflate observer effort with spread; 311 "open" means no close date recorded. See the brief for the full methods section.
