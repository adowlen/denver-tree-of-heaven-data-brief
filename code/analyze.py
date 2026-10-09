#!/usr/bin/env python3
"""Tree-of-heaven analysis pipeline, stage 1: clean, geocode to neighborhoods, parcel overlay.

Outputs:
  hidden_files/data/observations_clean.json     — deduped + filtered observations
  hidden_files/data/observations_enriched.json  — + neighborhood + parcel class
  hidden_files/data/analysis_summary.json       — headline stats
"""
import json
import math
import time
import urllib.parse
import urllib.request

BASE = "/home/hatch/workspace/goals/tree-of-heaven-data-brief/hidden_files"
PARCELS = "https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/ArcGIS/rest/services/ODC_PROP_PARCELS_A/FeatureServer/245/query"
NBHD = "https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/ArcGIS/rest/services/Enriched_Statistical_Neighborhood/FeatureServer/0/query"

GOV_PATTERNS = [
    "CITY AND COUNTY OF DENVER", "CITY & COUNTY OF DENVER", "CITY/COUNTY OF DENVER",
    "DENVER HOUSING AUTHORITY", "DENVER WATER", "DENVER PUBLIC SCHOOLS",
    "DENVER PUBLIC LIBRARY", "REGIONAL TRANSPORTATION DISTRICT",
    "STATE OF COLORADO", "COLORADO DEPARTMENT", "UNITED STATES OF AMERICA",
    "U.S.", "URBAN DRAINAGE", "MILE HIGH FLOOD",
]


def get_json(url, params, retries=3):
    qs = urllib.parse.urlencode(params)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url + "?" + qs, timeout=30) as r:
                return json.load(r)
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError("unreachable")


def point_in_ring(lon, lat, ring):
    inside = False
    n = len(ring)
    j = n - 1
    for i in range(n):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if ((yi > lat) != (yj > lat)) and (lon < (xj - xi) * (lat - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


def load_clean():
    gbif = json.load(open(f"{BASE}/data/gbif_occurrences.json"))
    inat = json.load(open(f"{BASE}/data/inat_observations.json"))
    seen = set()
    clean = []
    dropped = {"captive": 0, "coarse": 0, "dup": 0, "nocoords": 0}
    for rec in gbif + inat:
        lat, lon = rec.get("latitude"), rec.get("longitude")
        if lat is None or lon is None:
            dropped["nocoords"] += 1
            continue
        if rec.get("captive"):
            dropped["captive"] += 1
            continue
        unc = rec.get("coordinate_uncertainty_m")
        if unc is not None and unc > 1000:
            dropped["coarse"] += 1
            continue
        key = (round(lat, 4), round(lon, 4),
               str(rec.get("date") or "")[:10],
               str(rec.get("observer") or "").lower())
        if key in seen:
            dropped["dup"] += 1
            continue
        seen.add(key)
        clean.append({
            "id": rec["id"],
            "lat": lat, "lon": lon,
            "date": str(rec.get("date") or "")[:10],
            "observer": rec.get("observer"),
            "quality": rec.get("quality_grade"),
        })
    print(f"clean: {len(clean)}, dropped: {dropped}")
    json.dump(clean, open(f"{BASE}/data/observations_clean.json", "w"), indent=1)
    return clean


def load_neighborhoods():
    d = get_json(NBHD, {
        "where": "1=1", "outFields": "*", "returnGeometry": "true",
        "outSR": "4326", "f": "json", "resultRecordCount": 200,
    })
    feats = d.get("features", [])
    if not feats:
        raise RuntimeError("no neighborhood features: " + str(d)[:200])
    name_field = None
    for f in feats[0]["attributes"]:
        if "name" in f.lower():
            name_field = f
            break
    print("neighborhood name field:", name_field, "| count:", len(feats))
    polys = []
    for ft in feats:
        rings = ft["geometry"]["rings"]
        polys.append((ft["attributes"][name_field], rings[0]))
    return polys


def assign_neighborhood(clean, polys):
    for rec in clean:
        rec["neighborhood"] = None
        for name, ring in polys:
            if point_in_ring(rec["lon"], rec["lat"], ring):
                rec["neighborhood"] = name
                break
    n_none = sum(1 for r in clean if not r["neighborhood"])
    print(f"neighborhood assigned; {n_none} outside Denver neighborhoods")


def classify_parcel(attrs):
    owner = str(attrs.get("OWNER_NAME") or "").upper()
    dclass = str(attrs.get("D_CLASS_CN") or "").upper()
    exempt = attrs.get("EXEMPT_AMT_LOCAL") or 0
    taxable = attrs.get("TAXABLE_AMT_LOCAL") or 0
    if dclass == "DENVER PARK":
        return "park"
    if any(p in owner for p in GOV_PATTERNS):
        return "government"
    if exempt and not taxable:
        return "institutional"
    return "private"


def parcel_lookup(clean):
    for i, rec in enumerate(clean):
        try:
            d = get_json(PARCELS, {
                "geometry": f"{rec['lon']},{rec['lat']}",
                "geometryType": "esriGeometryPoint",
                "inSR": "4326",
                "spatialRel": "esriSpatialRelIntersects",
                "outFields": "OWNER_NAME,D_CLASS_CN,EXEMPT_AMT_LOCAL,TAXABLE_AMT_LOCAL",
                "returnGeometry": "false",
                "f": "json",
            })
        except Exception as e:
            print(f"parcel query failed for {rec['id']}: {e}")
            rec["parcel_class"] = "query_failed"
            continue
        feats = d.get("features", [])
        if not feats:
            rec["parcel_class"] = "row"
        else:
            rec["parcel_class"] = classify_parcel(feats[0]["attributes"])
        if (i + 1) % 100 == 0:
            print(f"  parcels: {i + 1}/{len(clean)}")
        time.sleep(0.12)


def summarize(clean):
    total = len(clean)
    by_class = {}
    for r in clean:
        by_class[r["parcel_class"]] = by_class.get(r["parcel_class"], 0) + 1
    public = by_class.get("government", 0) + by_class.get("park", 0) + by_class.get("row", 0)
    private = total - public - by_class.get("query_failed", 0)
    by_nbhd = {}
    for r in clean:
        n = r["neighborhood"] or "outside Denver"
        e = by_nbhd.setdefault(n, {"total": 0, "private": 0})
        e["total"] += 1
        if r["parcel_class"] in ("private", "institutional"):
            e["private"] += 1
    summary = {
        "n_observations": total,
        "by_parcel_class": by_class,
        "public_count": public,
        "private_count": private,
        "private_share": round(private / total, 3) if total else 0,
        "by_neighborhood": dict(sorted(by_nbhd.items(), key=lambda x: -x[1]["total"])[:25]),
        "date_range": [min(r["date"] for r in clean if r["date"]),
                       max(r["date"] for r in clean if r["date"])],
    }
    json.dump(summary, open(f"{BASE}/data/analysis_summary.json", "w"), indent=1)
    print(json.dumps(summary, indent=1)[:1500])
    return summary


def main():
    clean = load_clean()
    polys = load_neighborhoods()
    assign_neighborhood(clean, polys)
    parcel_lookup(clean)
    json.dump(clean, open(f"{BASE}/data/observations_enriched.json", "w"), indent=1)
    summarize(clean)


if __name__ == "__main__":
    main()