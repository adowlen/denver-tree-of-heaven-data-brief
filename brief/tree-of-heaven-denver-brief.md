# Tree of Heaven in Denver: A Data Brief

*What 731 citizen-science observations, 5,580 city complaints, and the parcel map say about an invasive tree — and why Colorado should list it as a noxious weed.*

## The bottom line

Denver has a tree-of-heaven problem it cannot spray its way out of. At least **43% of reported trees stand on privately owned land** — and the real share is higher, because nobody photographs the trees in their neighbor's backyard. The city closes only **1 in 4 weed complaints**. And the species sits on Colorado's official **Watch List**: the state has flagged the threat and stopped there. Eight other states list it as a noxious weed. Colorado should join them.

## Finding 1: Nearly half the reported trees are on private land — the true share is higher

We overlaid 493 geocoded tree-of-heaven observations (iNaturalist + GBIF, deduped) on Denver's parcel map:

- **214 (43%)** on privately owned parcels, including tax-exempt institutional land
- **279 (57%)** on public land: streets and rights-of-way (214), government parcels (38), parks (27)

![Who owns the land](charts/private_share_donut.png)

![Map by ownership](charts/map_by_ownership.png)

**Why 43% is a floor, not the number.** iNaturalist observers record what they can see from the sidewalk — street trees, alley trees, park edges. The trees thriving on neglect behind fences and in backyards are systematically undercounted. The true private share is higher; how much higher, nobody knows, because nobody has looked. Any control strategy that only touches public land is fighting less than half the battle — probably much less.

## Finding 2: Reports are climbing — and spreading across the city

Reported observations rose from 24 in 2016 to 129 in 2025. Part of that is more people using iNaturalist, but the geographic footprint keeps widening: reports now span from Lincoln Park (45, the densest cluster) through City Park (28), Five Points (27), Baker, Capitol Hill, and into the suburbs.

![Observations by year](charts/observations_by_year.png)

![By neighborhood](charts/by_neighborhood.png)

## Finding 3: The city doesn't close weed complaints

Of 4,173 "Weeds/Vegetation Violation" 311 cases in the last 12 months, **75% were never closed**. For comparison, only 3% of "Damaged/Fallen Tree" cases remain open — the system can close things; it just doesn't close weed cases.

The geography is stark. Worst performers (≥20 cases): Harvey Park **93%** open (n=407), Harvey Park South 90%, Valverde 89%, Mar Lee 87%, Athmar Park 86%, Westwood and Five Points 84%. Best: Belcaro 48%, Goldsmith 52%. The neighborhoods where complaints go to die are concentrated in southwest Denver; the neighborhoods where they get resolved are in the wealthier southeast.

![311 open rate by neighborhood](charts/311_open_rate_by_neighborhood.png)

![311 open rate by category](charts/311_open_rate_by_category.png)

## Finding 4: The case for listing

**Colorado already knows.** Tree of heaven isn't merely unlisted — it sits on the Colorado Department of Agriculture's **Watch List**: species the state flags as threats while requiring nothing. That is the entire policy argument in one fact.

**Colorado would be joining a crowd, not going rogue.** California, Connecticut, Massachusetts, New Hampshire, Vermont, Oregon, Washington, and New Mexico all list it.

**Listing is the private-property tool.** Under the Colorado Noxious Weed Act, a List B designation means mandatory control on *all* private lands. Ignore the notice and the county does the work, liens the property for the cost plus 20%, and can levy $500–$1,000 per violation. Without listing, none of that machinery exists for this species.

**The lanternfly clock is ticking.** Spotted lanternfly — whose preferred host the state ag department itself identifies as tree of heaven — has zero confirmed Colorado detections, but it's in Iowa and Illinois. That's a "when, not if" argument for acting before the host network matters.

**Denver has the machinery but not the hook.** The city's ZNIS inspectors can already do notice → 10 days → clear → bill → lien for vegetation violations. But because tree of heaven isn't a listed noxious weed, enforcement leans on vaguer nuisance provisions — the same pipeline that leaves 75% of weed complaints unclosed.

## What would actually work

1. **List it (List B).** Unlocks the only legal framework that reaches private land at scale.
2. **Fund the unglamorous part.** Volunteer treatment days with owner permission; free herbicide kits; cost-share for professional removal of large seed-source females.
3. **Fix the 311 pipeline.** A 75% unclosed rate for weed violations means the existing system isn't functioning as an enforcement tool, whatever the statute says.
4. **Kill the mothers first.** Female trees are seed factories; every large female removed prevents thousands of seedlings. The observation data can prioritize them.

## Methods & caveats

- **Occurrences:** GBIF (440 records, 1976–2026) + iNaturalist (619, 2016–2026), deduped on coordinates/date/observer to 731; filtered to exclude planted/captive specimens and coarse (>1 km uncertainty) coordinates. 393 GBIF records are iNaturalist-sourced; iNaturalist is effectively the superset.
- **Parcel overlay:** each observation point queried against Denver's parcel layer (ArcGIS); classified by owner name, Denver Park designation, and tax-exempt status. Points hitting no parcel treated as street right-of-way (spot-checked: 10/12 have a parcel within 15 m, consistent with street trees). Coverage is Denver County only; 238 suburban observations excluded from the ownership analysis.
- **Bias:** presence-only data; heavy observer bias (top 4 contributors made ~180 of 619 iNaturalist observations); hotspots partly measure where enthusiasts walk. Time trends conflate observer effort with actual spread.
- **311:** rolling 12 months of Denver 311 service requests; "open" means no close date recorded — some may be resolved but administratively unclosed. The category contrast (75% vs 3%) suggests this doesn't explain the pattern away. Neighborhood field was empty in the source; neighborhoods assigned by spatial lookup.

*Data: GBIF, iNaturalist, Denver Open Data Catalog (parcels, 311), Colorado Department of Agriculture. Analysis code and raw pulls available on request; public repo to follow.*
