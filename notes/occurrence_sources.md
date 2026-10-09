# Occurrence data sources — Tree of Heaven (Ailanthus altissima), Denver metro

Pulled 2026-10-08. Bounding box: lng -105.35 to -104.60, lat 39.55 to 39.95
(Denver County + inner suburbs: Aurora, Lakewood, Englewood, Commerce City, etc.)

## Files
- `../data/gbif_occurrences.json` — flat list, 440 records
- `../data/inat_observations.json` — flat list, 619 records
- `../data/gbif_pages_raw.json` — raw GBIF API pages (2 pages)
- `../data/inat_pages_raw.json` — raw iNaturalist API pages (4 pages)
- Pull script: `/tmp/toh_pull.py` (ephemeral; rerun recipe below)

## GBIF (api.gbif.org)
- Taxon: *Ailanthus altissima* (Mill.) Swingle, taxon key **3190653**, status ACCEPTED, exact match.
- Query: `occurrence/search?taxon_key=3190653&geometry=<WKT POLYGON of bbox>&hasCoordinate=true`, limit=300, paged to endOfRecords.
- **440 records**, 2 pages, no API limits hit.
- Date range: **1976-07-21 to 2026-09-19**. (Pre-2000 records are a handful of herbarium specimens.)
- Composition: 393 iNaturalist research-grade observations, 36 human observations (dataset unspecified), 10 preserved specimens, 1 material sample.
- 3 records missing dates; 0 missing coordinates.

## iNaturalist (api.inaturalist.org)
- Taxon: *Ailanthus altissima*, taxon id **57278** (species rank).
- Query: `observations?taxon_id=57278&nelat=39.95&nelng=-104.60&swlat=39.55&swlng=-105.35&per_page=200`, paged through all 4 pages (total_results=619). 1s delay between pages; no rate-limit errors.
- **619 records** (includes all quality grades).
- Date range: **2016-08-31 to 2026-10-08** (i.e., observations as recent as today).
- Quality grades: 550 research, 43 needs_id, 26 casual. **25 flagged captive/cultivated** (planted ornamentals — exclude from wild-infestation analysis or treat separately).
- 0 missing coordinates, 0 missing dates.

## Overlap between sources
GBIF ingests iNaturalist research-grade observations, so the two files overlap heavily:
393 of 440 GBIF records are iNat-sourced. iNat's file is the superset in practice (adds
casual/needs_id grades, captive flags, and observations newer than GBIF's last ingest).
Dedupe on source id before any combined analysis (GBIF keys vs `inat:<id>`).

## Data-quality caveats
1. **Observer bias is severe.** Top iNat contributors: schneetzer (61 obs), gustafsonja (49),
   stinger (43), mudflats47 (28). A handful of people drive the map — dense clusters may
   reflect where enthusiasts walk, not where trees are densest. Normalize or caveat any
   hotspot analysis accordingly.
2. **Coarse coordinates.** Median positional uncertainty is 10 m, but max is ~40 km
   (a few records). Records with uncertainty > ~1 km should be excluded from
   parcel-level or neighborhood-level mapping.
3. **Captive/planted trees.** 25 iNat records are flagged captive (deliberately planted
   ornamentals). They are not evidence of invasive spread; filter on `captive == false`
   for infestation mapping.
4. **Temporal bias.** iNat coverage starts 2016 and skews recent (platform growth +
   observer recruitment). "Spread over time" from first-observation dates partly measures
   observer effort, not just tree spread. Herbarium specimens (pre-2000) are sparse.
5. **Identification quality.** 43 iNat records are still `needs_id`; treat as provisional.
   Tree of heaven is frequently confused with sumac/walnut saplings by casual observers.
6. **No absence data.** These are presence-only records; empty areas are unsampled, not clean.

## Rerun recipe
```bash
python3 /tmp/toh_pull.py   # re-pulls both APIs, rewrites all four files
```
GBIF species match: https://api.gbif.org/v1/species/match?name=Ailanthus%20altissima
iNat taxon lookup: https://api.inaturalist.org/v1/taxa/autocomplete?q=Ailanthus%20altissima
