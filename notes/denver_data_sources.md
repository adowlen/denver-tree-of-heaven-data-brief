# Denver Open Data Sources — Tree of Heaven Brief

Located 2026-10-08. Both datasets are public, no authentication, anonymous query allowed.
Denver publishes via ArcGIS Online (org id `zdB7qR0BtYrg0Xpl`, services prefixed `ODC_`).
Portal: https://denvergov-geospatialdenver.opendata.arcgis.com/

---

## 1. Parcels — `ODC_PROP_PARCELS_A` (FeatureServer, layer 245)

- **REST endpoint:** `https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/ArcGIS/rest/services/ODC_PROP_PARCELS_A/FeatureServer`
- **Layer:** `.../FeatureServer/245` (name `PROP_PARCELS_A`, polygon geometry)
- **Item ID:** `7c53bd0894134e80ae1e478c0789bf49`
- **Access method:** ArcGIS REST query API (JSON). No download needed; supports `Extract` (CSV/Shapefile/GeoJSON/KML export) for full pulls.
- **Record count:** 240,436 parcels (verified 2026-10-08)
- **Update frequency:** rolling edits; `dataLastEditDate` = 2026-10-08 (current). Treat as continuously updated.
- **Coordinate system:** WKID 2877 (Colorado State Plane Central, US Survey Feet). Request `outSR=4326` for WGS84 lat/lon.
- **Auth / rate limits:** none for reads. `maxRecordCount` = 2000 per query — paginate with `resultOffset` / `resultRecordCount`. `maxIdsCount` = 1,000,000.
- **Spatial query recipe (point-in-parcel for observation overlay):**
  `.../245/query?geometry=<lon>,<lat>&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=OWNER_NAME,D_CLASS_CN,EXEMPT_AMT_LOCAL,TAXABLE_AMT_LOCAL&returnGeometry=false&f=json`
  For bulk work, pull the full layer once via the Extract operation (GeoJSON) and do the join locally.

### Key fields

| Field | Type | Notes |
|---|---|---|
| `OWNER_NAME` | string (470) | Display field. Owner of record — basis for public-vs-private classification |
| `PROP_CLASS` | string (4) | Property class code |
| `D_CLASS` / `D_CLASS_CN` | string | Detailed class code / class name (105 distinct values; e.g. `DENVER PARK` n=471, `FIRE STATION` n=30, `COUNTY JAIL` n=8) |
| `EXEMPT_AMT_LOCAL` / `EXEMPT_AMT_SCH` | int | Tax-exempt amount; > 0 on 10,104 parcels (~4.2%) |
| `TAXABLE_AMT_LOCAL` | int | Taxable amount (0 on fully exempt parcels) |
| `SITUS_ADDRESS_LINE1`, `SITUS_CITY`, `SITUS_ZIP` | string | Property street address |
| `SCHEDNUM` | string | Assessor schedule/account number (join key to assessor tables) |
| `ZONE_ID` | string | Zoning district |
| `LAND_AREA` | int | Parcel area (sq ft) |
| `LEGAL_DESC` | string | Legal description |

### Public-vs-private classification (recommended)

No single "government-owned" flag exists. Use this rule, in order:
1. **Government owner (highest confidence):** `UPPER(OWNER_NAME)` matches known public entities. Verified counts:
   - `CITY & COUNTY OF DENVER` — 3,324 (+ variants: `HOUSING AUTHORITY OF THE CITY & COUNTY OF DENVER` 196, `BOARD OF WATER COMMISSIONERS CITY & COUNTY OF DENVER` 49, `DENVER COUNTY SCHOOL DISTRICT NO 1` 2, library commission, public works, etc.)
   - `STATE OF COLORADO` — 507
   - `REGIONAL TRANSPORTATION DISTRICT` (RTD) — 270
   - US federal variants (`UNITED STATES%`, `US %`) — 69
   - `DENVER PUBLIC SCHOOL%` — 2
2. **Tax-exempt institutional:** `EXEMPT_AMT_LOCAL > 0` (10,104 parcels) — captures government + churches + nonprofits. Cross-check against OWNER_NAME to split government from nonprofit.
3. Everything else → **private**.

**Caveat:** street rights-of-way and some public land are not parceled at all — observation points falling on ROW will return no parcel. Treat "no intersecting parcel" as public ROW, not private.

Sample: `../data/parcels_sample.json` (50 records, fields above, `returnGeometry=false`).

---

## 2. 311 Service Requests — `ODC_service_requests_311` (FeatureServer, table 53)

- **REST endpoint:** `https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/ArcGIS/rest/services/ODC_service_requests_311/FeatureServer`
- **Table:** `.../FeatureServer/53` (name `service_requests_311`; non-spatial table, but carries `Latitude`/`Longitude` fields)
- **Item ID:** `46a685dd1b284ff2a3bf68e062051635`
- **Access method:** ArcGIS REST query API (JSON). Supports Extract (CSV etc.).
- **Coverage: rolling 12 months only** (service description). 395,257 records as of 2026-10-08; newest record in sample = 2026-10-05 (fresh, ~3-day lag).
- **For multi-year history:** the separate dataset page "City and County of Denver 311 Service Requests 2007 to Current" (denvergov.org/opendata) historically offered yearly files — verify current availability on the portal before depending on it.
- **Auth / rate limits:** none for reads; `maxRecordCount` = 2000 per query, paginate with `resultOffset`.
- **Date filtering:** `Case_Created_Date` / `Case_Closed_Date` are epoch milliseconds. Example: `Case_Created_Date >= 1735689600000` (2025-01-01). Response-time analysis: `Case_Closed_Date - Case_Created_Date`.
- **Geography:** `Latitude`, `Longitude` (WGS84), plus `Neighborhood`, `Council_District`, `Police_District`, `Incident_Zip_Code`, `Incident_Address_1`.

### Category fields — IMPORTANT

`Type`, `Topic`, `Major_Area`, `Division` are **~100% NULL** in the current table — do not use them. Categorization lives in **`Case_Summary`** (free-text category label, 8000 chars). Filter with exact-match `IN` lists, not LIKE on "tree" (the substring "tree" matches "street" — use word-aware matching or explicit value lists).

### Vegetation/forestry-relevant `Case_Summary` values (rolling 12 mo counts)

| Case_Summary | Records |
|---|---|
| Weeds/Vegetation Violation | 4,173 |
| Damaged/Fallen Tree | 800 |
| Vegetation | 317 |
| Weeds & Vegetation | 144 |
| Tree growing / tree wire issue | 77 |
| Weeds | 43 |
| Forestry - Hours/Phone number/General Information | 26 |
| **Total vegetation-relevant** | **~5,580** |

Filter recipe:
`Case_Summary IN ('Weeds/Vegetation Violation','Damaged/Fallen Tree','Vegetation','Weeds & Vegetation','Tree growing / tree wire issue','Weeds','Forestry - Hours/Phone number/General Information')`

`Agency` values (for routing context): Safety, Finance, Public Works, 311, Public Health & Environment, DLCP, Clerk & Recorder, Community Planning & Development, Excise & License, External Agency, **Parks & Recreation** (7,886), City Council, Mayor's Office, Tech Services.

Sample: `../data/311_vegetation_sample.json` (50 most recent vegetation-related requests, ordered by `Case_Created_Date DESC`).

### Notes for the equity analysis
- `Neighborhood` is populated on records — direct neighborhood-level aggregation is possible without a spatial join.
- `Case_Source` distinguishes how the request came in (311 agent vs. web/app) — useful for reporting-bias discussion.
- Denver Auditor's Aug 2025 audit of 311 case management (denvergov.org auditor page) found inconsistent cross-agency case handling — citable context for the response-time analysis.

---

## Quick query cheat sheet

```bash
BASE_P="https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/ArcGIS/rest/services/ODC_PROP_PARCELS_A/FeatureServer/245"
BASE_3="https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/ArcGIS/rest/services/ODC_service_requests_311/FeatureServer/53"

# parcel count
curl -s -G "$BASE_P/query" --data-urlencode "where=1=1" --data-urlencode "returnCountOnly=true" --data-urlencode "f=json"
# 311 count
curl -s -G "$BASE_3/query" --data-urlencode "where=1=1" --data-urlencode "returnCountOnly=true" --data-urlencode "f=json"
# paginate: add  --data-urlencode "resultOffset=N" --data-urlencode "resultRecordCount=2000"
# WGS84 coords: add  --data-urlencode "outSR=4326"
```
