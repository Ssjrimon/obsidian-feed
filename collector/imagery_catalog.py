#!/usr/bin/env python3
"""Build Sentinel-1 region catalogs and Sentinel-2 before/after pairs.

Public STAC search only (Earth Search, then Planetary Computer, then CDSE
catalogue). No scraping, no imagery processing, no secrets in output.
Run: python3 imagery_catalog.py
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from urllib.parse import urljoin

import requests

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
OUT_S1 = os.path.join(DATA, "imagery", "sentinel1")
OUT_BA = os.path.join(DATA, "imagery", "before-after")

UA = {
    "User-Agent": "OBSIDIAN-OSINT-feed/1.0 (+https://github.com/Ssjrimon/obsidian-feed)",
    "Accept": "application/geo+json, application/json",
}

WINDOW_DAYS = 30
PAIR_LOOKBACK_DAYS = 18  # same-orbit pair may sit just outside the 30-day window
PAIR_TARGET_DAYS = 12
PAIR_TOLERANCE_DAYS = 3
REQUEST_GAP_SEC = 0.25
HALF_DEG = 0.25
S2_CLOUD_PREF = 20.0
S2_CLOUD_MAX = 80.0

CATALOGS = [
    {
        "id": "earth-search",
        "search": "https://earth-search.aws.element84.com/v1/search",
        "s1_collection": "sentinel-1-grd",
        "s2_collections": ["sentinel-2-c1-l2a", "sentinel-2-l2a"],
    },
    {
        "id": "planetary-computer",
        "search": "https://planetarycomputer.microsoft.com/api/stac/v1/search",
        "s1_collection": "sentinel-1-grd",
        "s2_collections": ["sentinel-2-l2a"],
    },
    {
        "id": "cdse-stac",
        "search": "https://catalogue.dataspace.copernicus.eu/stac/search",
        "s1_collection": "sentinel-1-grd",
        "s2_collections": ["sentinel-2-l2a"],
    },
]

CAVEATS = [
    "Overhead is not imaging: a scene shows what was overhead and not why.",
    "Radar change is a lead and not confirmation.",
]

# Confirmed T-019 places only. Coordinates are public place locations, not
# the feed's country-centroid geocoding (which can land on the wrong country
# when a title names the attacker). No Jordan/Amman-specific places.
CONFIRMED_EVENTS = [
    {
        "id": "0034dd6a83af6560",
        "relatedFeedIds": ["33e823f244855f31", "b49f0d78d90bebd5"],
        "trendId": "t019-01",
        "title": "Winter storm floods Gaza displacement camps",
        "eventTimeUtc": "2026-11-06T16:00:00Z",
        "region": "ISR-GAZA",
        "placeName": "Gaza Strip (Deir al-Balah, Gaza City, Khan Younis)",
        "lat": 31.417,
        "lon": 34.352,
        "bbox": [34.22, 31.22, 34.57, 31.59],
    },
    {
        "id": "899a4f48ee899435",
        "relatedFeedIds": ["1f7ae82ec81cf6bd", "6fff2dc8d4b7168a"],
        "trendId": "t019-02",
        "title": "Israeli strike hits Nasser Hospital surgical building in Khan Younis",
        "eventTimeUtc": "2026-11-11T22:39:00Z",
        "region": "ISR-GAZA",
        "placeName": "Nasser Medical Complex, Khan Younis, Gaza Strip",
        "lat": 31.346,
        "lon": 34.306,
        "bbox": [34.26, 31.31, 34.35, 31.38],
    },
    {
        "id": "1056ac62ed5eeedc",
        "relatedFeedIds": ["5f84e7011e0d5d0b"],
        "trendId": "t019-03",
        "title": "Russian strikes hit residential buildings in Zaporizhzhia",
        "eventTimeUtc": "2026-11-13T08:00:00Z",
        "region": "UKR-RUS",
        "placeName": "Zaporizhzhia, Ukraine (Kosmichnyi district)",
        "lat": 47.839,
        "lon": 35.140,
        "bbox": [35.05, 47.76, 35.24, 47.92],
    },
    {
        "id": "b90f4c650f0d016b",
        "relatedFeedIds": ["0106bfb322a6e13a"],
        "trendId": "t019-04",
        "title": "Russian drone hits a hospital in central Kyiv",
        "eventTimeUtc": "2026-11-13T01:00:00Z",
        "region": "UKR-RUS",
        "placeName": "National Institute of Traumatology and Orthopedics, Shevchenkivskyi, Kyiv",
        "lat": 50.454,
        "lon": 30.505,
        "bbox": [30.45, 50.42, 30.56, 50.49],
    },
    {
        "id": "c28921558a06ad25",
        "relatedFeedIds": ["d40215120166dd71"],
        "trendId": "t019-05",
        "title": "Houthi forces tighten the siege of Taiz, Yemen",
        "eventTimeUtc": "2026-10-18T00:00:00Z",
        "region": "RED SEA",
        "placeName": "Taiz (Taizz), Yemen",
        "lat": 13.579,
        "lon": 44.022,
        "bbox": [43.95, 13.52, 44.09, 13.64],
    },
    {
        "id": "7c87c9ad239a32ee",
        "relatedFeedIds": ["3ee7bbecae4ab828", "54414d74aa25a198"],
        "trendId": "t019-06",
        "title": "Ukrainian drone hits a Russian warship in the Gulf of Finland",
        "eventTimeUtc": "2026-11-11T03:30:00Z",
        # Feed items for this event landed in both EUROPE and UKR-RUS.
        "region": "EUROPE",
        "alsoRegions": ["UKR-RUS"],
        "placeName": "Gulf of Finland, near Gogland Island",
        "lat": 60.058,
        "lon": 26.993,
        "bbox": [26.70, 59.90, 27.30, 60.20],
    },
    {
        "id": "90d68d3e1c85699c",
        "relatedFeedIds": ["fbca691f68dfed3e"],
        "trendId": "t019-07",
        "title": "Bundibugyo Ebola outbreak in the Democratic Republic of the Congo",
        "eventTimeUtc": "2026-11-11T00:00:00Z",
        "region": "AFRICA",
        "placeName": "Bunia, Ituri province, Democratic Republic of the Congo (WHO-described epicentre)",
        "lat": 1.560,
        "lon": 30.252,
        "bbox": [30.15, 1.46, 30.35, 1.66],
        "notes": "Ongoing outbreak across eight provinces; Ituri is the epicentre cited by WHO. Imagery is a place snapshot, not a case map.",
    },
]

SESSION = requests.Session()
SESSION.headers.update(UA)


def now_utc():
    return datetime.now(timezone.utc)


def parse_dt(value):
    if not value:
        return None
    text = str(value).replace("Z", "+00:00")
    if "." in text:
        # keep up to microseconds
        head, tail = text.split(".", 1)
        frac, _, tz = tail.partition("+")
        if not tz and "-" in tail[1:] and tail[0].isdigit():
            # timezone with minus
            frac, _, rest = tail.partition("-")
            tz = "-" + rest if rest else ""
            text = f"{head}.{frac[:6]}{tz}"
        else:
            text = f"{head}.{frac[:6]}+{tz}" if tz else f"{head}.{frac[:6]}"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def iso_z(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def region_slug(code):
    return code.strip().lower().replace(" ", "-")


def point_bbox(lat, lon, half=HALF_DEG):
    return [
        round(max(-180.0, lon - half), 5),
        round(max(-90.0, lat - half), 5),
        round(min(180.0, lon + half), 5),
        round(min(90.0, lat + half), 5),
    ]


def bbox_intersection_area(a, b):
    west = max(a[0], b[0])
    south = max(a[1], b[1])
    east = min(a[2], b[2])
    north = min(a[3], b[3])
    if east <= west or north <= south:
        return 0.0
    return (east - west) * (north - south)


def contains_point(bbox, lon, lat):
    return bbox[0] <= lon <= bbox[2] and bbox[1] <= lat <= bbox[3]


def sleep_gap():
    time.sleep(REQUEST_GAP_SEC)


def stac_post_or_get(url, body):
    sleep_gap()
    resp = SESSION.post(url, json=body, timeout=60)
    if resp.status_code in (429, 500, 502, 503, 504):
        time.sleep(1.5)
        resp = SESSION.post(url, json=body, timeout=60)
    resp.raise_for_status()
    return resp.json()


def stac_search(catalog, collection, bbox, start, end, limit=100, extra_query=None):
    """POST STAC search with pagination. Returns (features, catalog_id, error)."""
    body = {
        "collections": [collection],
        "bbox": bbox,
        "datetime": f"{iso_z(start)}/{iso_z(end)}",
        "limit": limit,
    }
    if extra_query:
        body["query"] = extra_query
    url = catalog["search"]
    features = []
    for _page in range(8):
        try:
            payload = stac_post_or_get(url, body)
        except Exception as exc:
            return features, catalog["id"], f"{type(exc).__name__}: {exc}"
        features.extend(payload.get("features") or [])
        next_link = None
        for link in payload.get("links") or []:
            if link.get("rel") == "next" and link.get("href"):
                next_link = link
                break
        matched = (payload.get("context") or {}).get("matched")
        if not next_link or (matched is not None and len(features) >= matched):
            break
        next_url = next_link["href"]
        url = next_url if next_url.startswith("http") else urljoin(catalog["search"], next_url)
        if isinstance(next_link.get("body"), dict):
            body = next_link["body"]
            continue
        # GET the next page when the catalog only supplies a href.
        sleep_gap()
        try:
            resp = SESSION.get(url, timeout=60)
            if resp.status_code in (429, 500, 502, 503, 504):
                time.sleep(1.5)
                resp = SESSION.get(url, timeout=60)
            resp.raise_for_status()
            payload = resp.json()
        except Exception as exc:
            return features, catalog["id"], f"{type(exc).__name__}: {exc}"
        features.extend(payload.get("features") or [])
        # If that GET page also has a POST-style next body, loop; else stop after one GET.
        nxt = next((l for l in payload.get("links") or [] if l.get("rel") == "next" and l.get("href")), None)
        if not nxt:
            break
        url = nxt["href"] if nxt["href"].startswith("http") else urljoin(catalog["search"], nxt["href"])
        if isinstance(nxt.get("body"), dict):
            body = nxt["body"]
            continue
        break
    return features, catalog["id"], None


def search_with_fallback(kind, bbox, start, end, extra_query=None):
    """Use the next catalogue only when the current one errors, not when it is empty."""
    errors = []
    last_empty = ( [], None, None, "no scenes" )
    for catalog in CATALOGS:
        collections = (
            [catalog["s1_collection"]] if kind == "s1" else list(catalog["s2_collections"])
        )
        catalog_failed = True
        for collection in collections:
            features, cat_id, err = stac_search(
                catalog, collection, bbox, start, end, extra_query=extra_query
            )
            if err:
                errors.append(f"{cat_id}/{collection}: {err}")
                continue
            catalog_failed = False
            if features:
                return features, cat_id, collection, None
            last_empty = ( [], cat_id, collection, None )
            # Healthy empty collection: try the next collection in this catalogue.
        if not catalog_failed:
            return last_empty
    return [], None, None, "; ".join(errors) if errors else "no scenes"


def public_item_url(feat, catalog_id, collection):
    for link in feat.get("links") or []:
        href = link.get("href") or ""
        if link.get("rel") == "self" and href.startswith("http"):
            return href
    item_id = feat.get("id")
    if catalog_id == "earth-search" and item_id:
        return f"https://earth-search.aws.element84.com/v1/collections/{collection}/items/{item_id}"
    if catalog_id == "planetary-computer" and item_id:
        return f"https://planetarycomputer.microsoft.com/api/stac/v1/collections/{collection}/items/{item_id}"
    if catalog_id == "cdse-stac" and item_id:
        return f"https://catalogue.dataspace.copernicus.eu/stac/collections/{collection}/items/{item_id}"
    return None


def public_preview_url(feat, catalog_id, collection):
    # Prefer a public https thumbnail/preview, never s3:// (often requester-pays).
    for link in feat.get("links") or []:
        href = link.get("href") or ""
        if link.get("rel") in ("thumbnail", "preview") and href.startswith("http"):
            return href
    assets = feat.get("assets") or {}
    for key in ("thumbnail", "preview", "rendered_preview", "overview"):
        asset = assets.get(key) or {}
        href = asset.get("href") or ""
        if href.startswith("http"):
            return href
    item_url = public_item_url(feat, catalog_id, collection)
    if item_url and catalog_id == "earth-search":
        return item_url.rstrip("/") + "/thumbnail"
    return None


def feat_bbox(feat):
    bbox = feat.get("bbox")
    if isinstance(bbox, list) and len(bbox) >= 4:
        return [float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3])]
    geom = feat.get("geometry") or {}
    coords = geom.get("coordinates")
    if not coords:
        return None
    xs, ys = [], []

    def walk(node):
        if not node:
            return
        if isinstance(node[0], (int, float)):
            xs.append(float(node[0]))
            ys.append(float(node[1]))
            return
        for child in node:
            walk(child)

    walk(coords)
    if not xs:
        return None
    return [min(xs), min(ys), max(xs), max(ys)]


def s1_record(feat, catalog_id, collection):
    props = feat.get("properties") or {}
    acquired = parse_dt(props.get("datetime") or props.get("start_datetime"))
    direction = (props.get("sat:orbit_state") or props.get("orbit_state") or "").lower() or None
    rel_orbit = props.get("sat:relative_orbit")
    platform = props.get("platform") or props.get("constellation")
    return {
        "sceneId": feat.get("id"),
        "acquisitionTimeUtc": iso_z(acquired) if acquired else None,
        "acquired": acquired,
        "platform": platform,
        "orbitDirection": direction,
        "relativeOrbit": rel_orbit,
        "instrumentMode": props.get("sar:instrument_mode"),
        "datatakeId": props.get("s1:datatake_id"),
        "footprintBbox": feat_bbox(feat),
        "stacItemUrl": public_item_url(feat, catalog_id, collection),
        "previewUrl": public_preview_url(feat, catalog_id, collection),
    }


def s2_record(feat, catalog_id, collection):
    props = feat.get("properties") or {}
    acquired = parse_dt(props.get("datetime") or props.get("start_datetime"))
    cloud = props.get("eo:cloud_cover")
    rec = {
        "sceneId": feat.get("id"),
        "date": acquired.date().isoformat() if acquired else None,
        "acquisitionTimeUtc": iso_z(acquired) if acquired else None,
        "cloudCoverPct": round(float(cloud), 4) if cloud is not None else None,
        "platform": props.get("platform"),
        "mgrsTile": props.get("s2:mgrs_tile") or props.get("grid:code"),
        "footprintBbox": feat_bbox(feat),
        "stacItemUrl": public_item_url(feat, catalog_id, collection),
        "thumbnailUrl": public_preview_url(feat, catalog_id, collection),
        "acquired": acquired,
    }
    return rec


def pass_key(rec):
    day = (rec["acquired"].date().isoformat() if rec.get("acquired") else rec.get("acquisitionTimeUtc") or "")[:10]
    return (rec.get("platform"), rec.get("relativeOrbit"), rec.get("orbitDirection"), day)


def public_s1(rec, aoi_ids=None, previous=None):
    out = {
        "sceneId": rec["sceneId"],
        "acquisitionTimeUtc": rec["acquisitionTimeUtc"],
        "platform": rec.get("platform"),
        "orbitDirection": rec.get("orbitDirection"),
        "relativeOrbit": rec.get("relativeOrbit"),
        "instrumentMode": rec.get("instrumentMode"),
        "footprintBbox": rec.get("footprintBbox"),
        "stacItemUrl": rec.get("stacItemUrl"),
        "previewUrl": rec.get("previewUrl"),
    }
    if aoi_ids is not None:
        out["aoiIds"] = sorted(aoi_ids)
    if previous is not None:
        out["previousSameOrbit"] = previous
    return out


def public_previous(rec, days_earlier):
    return {
        "sceneId": rec["sceneId"],
        "acquisitionTimeUtc": rec["acquisitionTimeUtc"],
        "platform": rec.get("platform"),
        "orbitDirection": rec.get("orbitDirection"),
        "relativeOrbit": rec.get("relativeOrbit"),
        "footprintBbox": rec.get("footprintBbox"),
        "stacItemUrl": rec.get("stacItemUrl"),
        "previewUrl": rec.get("previewUrl"),
        "daysEarlier": round(days_earlier, 2),
    }


def public_s2(rec):
    if not rec:
        return None
    return {
        "sceneId": rec["sceneId"],
        "date": rec["date"],
        "acquisitionTimeUtc": rec["acquisitionTimeUtc"],
        "cloudCoverPct": rec["cloudCoverPct"],
        "platform": rec.get("platform"),
        "mgrsTile": rec.get("mgrsTile"),
        "footprintBbox": rec.get("footprintBbox"),
        "stacItemUrl": rec.get("stacItemUrl"),
        "thumbnailUrl": rec.get("thumbnailUrl"),
    }


def pick_best_slice(records, aoi_bbox):
    def score(rec):
        fb = rec.get("footprintBbox") or [0, 0, 0, 0]
        return bbox_intersection_area(fb, aoi_bbox)

    return max(records, key=score)


def pair_for(current, pool):
    if not current.get("acquired"):
        return None
    target = current["acquired"] - timedelta(days=PAIR_TARGET_DAYS)
    lo = current["acquired"] - timedelta(days=PAIR_TARGET_DAYS + PAIR_TOLERANCE_DAYS)
    hi = current["acquired"] - timedelta(days=PAIR_TARGET_DAYS - PAIR_TOLERANCE_DAYS)
    candidates = []
    for rec in pool:
        if rec is current or not rec.get("acquired"):
            continue
        if rec.get("platform") != current.get("platform"):
            continue
        if rec.get("relativeOrbit") != current.get("relativeOrbit"):
            continue
        if rec.get("orbitDirection") != current.get("orbitDirection"):
            continue
        if lo <= rec["acquired"] <= hi:
            candidates.append(rec)
    if not candidates:
        return None
    best = min(candidates, key=lambda r: abs((r["acquired"] - target).total_seconds()))
    days = (current["acquired"] - best["acquired"]).total_seconds() / 86400.0
    return public_previous(best, days)


def pick_s2(records, event_dt, side, lon, lat):
    """Latest scene before or after event_time, preferring low cloud cover."""
    eligible = []
    for rec in records:
        acquired = rec.get("acquired")
        if not acquired:
            continue
        if side == "before" and acquired >= event_dt:
            continue
        if side == "after" and acquired < event_dt:
            continue
        fb = rec.get("footprintBbox")
        if fb and not contains_point(fb, lon, lat) and bbox_intersection_area(fb, point_bbox(lat, lon, 0.05)) <= 0:
            continue
        eligible.append(rec)
    if not eligible:
        return None, "no scene in window"
    preferred = [
        r for r in eligible
        if r.get("cloudCoverPct") is not None and r["cloudCoverPct"] <= S2_CLOUD_PREF
    ]
    acceptable = [
        r for r in eligible
        if r.get("cloudCoverPct") is None or r["cloudCoverPct"] <= S2_CLOUD_MAX
    ]
    if preferred:
        chosen = max(preferred, key=lambda r: r["acquired"])
        return chosen, "latest scene with cloud cover at or under 20%"
    if acceptable:
        chosen = max(acceptable, key=lambda r: r["acquired"])
        return chosen, "no scene at or under 20% cloud cover; latest scene at or under 80%"
    chosen = max(eligible, key=lambda r: r["acquired"])
    return chosen, "only scenes above 80% cloud cover in window; latest kept as a catalogue lead, not a clear view"


def skip_place(iso2, place_code, label):
    blob = " ".join(str(x) for x in (iso2, place_code, label) if x).lower()
    if iso2 == "JO":
        return True
    if "amman" in blob:
        return True
    # Allow the word "jordan" only if it is clearly not the country (none expected).
    if "jordan" in blob:
        return True
    return False


def load_region_aois():
    path = os.path.join(DATA, "latest.json")
    with open(path) as fh:
        payload = json.load(fh)
    events = payload.get("events") or []
    # unique watch points from the live feed, plus confirmed-event places
    buckets = {}
    for ev in events:
        geo = ev.get("geo") or {}
        region = geo.get("regionCode")
        lat, lon = geo.get("lat"), geo.get("lon")
        iso2 = geo.get("iso2")
        if not region or region == "GLOBAL" or lat is None or lon is None:
            continue
        if skip_place(iso2, geo.get("placeCode"), ""):
            continue
        key = (region, round(float(lat), 2), round(float(lon), 2))
        buckets.setdefault(key, {
            "region": region,
            "lat": float(lat),
            "lon": float(lon),
            "iso2": iso2,
            "placeCode": geo.get("placeCode"),
            "kind": "feed-watch-point",
            "label": None,
        })

    aois_by_region = {}
    for item in buckets.values():
        region = item["region"]
        aoi_id = f"{region_slug(region)}-{item.get('iso2') or 'xx'}-{item['lat']:.2f}-{item['lon']:.2f}"
        item["id"] = aoi_id
        item["bbox"] = point_bbox(item["lat"], item["lon"])
        item["label"] = (
            f"Feed watch point {item.get('iso2') or ''} {item.get('placeCode') or ''}".strip()
        )
        aois_by_region.setdefault(region, []).append(item)

    for ev in CONFIRMED_EVENTS:
        for region in [ev["region"]] + list(ev.get("alsoRegions") or []):
            aoi = {
                "id": f"confirmed-{ev['trendId']}",
                "region": region,
                "lat": ev["lat"],
                "lon": ev["lon"],
                "bbox": ev["bbox"],
                "kind": "confirmed-event-place",
                "label": ev["placeName"],
                "eventId": ev["id"],
                "iso2": None,
                "placeCode": None,
            }
            aois_by_region.setdefault(region, []).append(aoi)

    # If a confirmed AOI already covers a nearby feed watch point, drop the
    # coarser point so we do not double-query the same ground.
    for region, aois in aois_by_region.items():
        confirmed = [a for a in aois if a["kind"] == "confirmed-event-place"]
        kept = []
        for aoi in aois:
            if aoi["kind"] == "confirmed-event-place":
                kept.append(aoi)
                continue
            covered = any(contains_point(c["bbox"], aoi["lon"], aoi["lat"]) for c in confirmed)
            if not covered:
                kept.append(aoi)
        aois_by_region[region] = kept
    return aois_by_region


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def catalog_s1_region(region, aois, cutoff, fetch_start, now):
    problems = []
    all_recs = []  # (rec, aoi_id, catalog, collection)
    catalogs_used = set()
    collections_used = set()
    for aoi in aois:
        features, cat_id, collection, err = search_with_fallback(
            "s1", aoi["bbox"], fetch_start, now
        )
        if err and not features:
            problems.append(f"{aoi['id']}: {err}")
            continue
        if cat_id:
            catalogs_used.add(cat_id)
        if collection:
            collections_used.add(collection)
        for feat in features:
            rec = s1_record(feat, cat_id, collection)
            rec["_aoi"] = aoi["id"]
            rec["_aoi_bbox"] = aoi["bbox"]
            rec["_catalog"] = cat_id
            rec["_collection"] = collection
            all_recs.append(rec)

    # One scene per pass (platform + relative orbit + direction + date).
    grouped = {}
    for rec in all_recs:
        if not rec.get("sceneId"):
            continue
        key = pass_key(rec)
        grouped.setdefault(key, []).append(rec)

    current_passes = []
    pool = []
    for recs in grouped.values():
        # pick the slice with the strongest overlap of any contributing AOI
        def score(rec):
            return bbox_intersection_area(rec.get("footprintBbox") or [0, 0, 0, 0], rec["_aoi_bbox"])
        best = max(recs, key=score)
        pool.append(best)
        if best.get("acquired") and best["acquired"] >= cutoff:
            current_passes.append(best)

    # Merge aoi ids when the same pass was seen from several AOIs
    pass_to_aois = {}
    for rec in all_recs:
        if rec.get("acquired") and rec["acquired"] >= cutoff:
            pass_to_aois.setdefault(pass_key(rec), set()).add(rec["_aoi"])

    current_passes.sort(key=lambda r: r["acquired"] or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    # De-duplicate objects that share a pass key (keep first / already-best)
    seen = set()
    unique = []
    for rec in current_passes:
        key = pass_key(rec)
        if key in seen:
            continue
        seen.add(key)
        unique.append(rec)

    passes_out = []
    for rec in unique:
        prev = pair_for(rec, pool)
        passes_out.append(public_s1(rec, pass_to_aois.get(pass_key(rec), {rec["_aoi"]}), prev))

    year = now.year
    doc = {
        "schema": "obsidian-imagery-sentinel1-v1",
        "region": region,
        "generatedAt": iso_z(now),
        "windowDays": WINDOW_DAYS,
        "purpose": "infrastructure and disaster change-detection leads only",
        "catalog": sorted(catalogs_used)[0] if len(catalogs_used) == 1 else sorted(catalogs_used),
        "collection": sorted(collections_used)[0] if len(collections_used) == 1 else sorted(collections_used),
        "attribution": f"Copernicus Sentinel data {year}",
        "caveats": CAVEATS,
        "aois": [
            {
                "id": a["id"],
                "kind": a["kind"],
                "label": a["label"],
                "lat": a["lat"],
                "lon": a["lon"],
                "bbox": a["bbox"],
                "eventId": a.get("eventId"),
            }
            for a in aois
        ],
        "passCount": len(passes_out),
        "pairedPassCount": sum(1 for p in passes_out if p.get("previousSameOrbit")),
        "passes": passes_out,
    }
    if problems:
        doc["problems"] = problems
    return doc


def catalog_before_after(event, now):
    event_dt = parse_dt(event["eventTimeUtc"])
    start = event_dt - timedelta(days=WINDOW_DAYS)
    end = min(now, event_dt + timedelta(days=WINDOW_DAYS))
    features, cat_id, collection, err = search_with_fallback(
        "s2", event["bbox"], start, end
    )
    records = [s2_record(f, cat_id, collection) for f in features] if features else []
    before, before_reason = pick_s2(records, event_dt, "before", event["lon"], event["lat"])
    after, after_reason = pick_s2(records, event_dt, "after", event["lon"], event["lat"])
    year = now.year
    doc = {
        "schema": "obsidian-imagery-before-after-v1",
        "eventId": event["id"],
        "trendId": event["trendId"],
        "relatedFeedIds": event.get("relatedFeedIds") or [],
        "title": event["title"],
        "label": "Confirmed",
        "eventTimeUtc": event["eventTimeUtc"],
        "place": {
            "name": event["placeName"],
            "region": event["region"],
            "lat": event["lat"],
            "lon": event["lon"],
            "bbox": event["bbox"],
        },
        "generatedAt": iso_z(now),
        "windowDays": WINDOW_DAYS,
        "catalog": cat_id,
        "collection": collection,
        "attribution": f"Copernicus Sentinel data {year}",
        "caveats": CAVEATS,
        "selection": {
            "before": before_reason,
            "after": after_reason,
            "cloudCoverPreferencePct": S2_CLOUD_PREF,
        },
        "before": public_s2(before),
        "after": public_s2(after),
    }
    if event.get("notes"):
        doc["notes"] = event["notes"]
    if err and not features:
        doc["problems"] = [err]
    elif not before or not after:
        missing = []
        if not before:
            missing.append(f"before: {before_reason}")
        if not after:
            missing.append(f"after: {after_reason}")
        doc["problems"] = missing
    return doc


def main():
    now = now_utc()
    cutoff = now - timedelta(days=WINDOW_DAYS)
    fetch_start = now - timedelta(days=WINDOW_DAYS + PAIR_LOOKBACK_DAYS)
    aois_by_region = load_region_aois()
    os.makedirs(OUT_S1, exist_ok=True)
    os.makedirs(OUT_BA, exist_ok=True)

    region_stats = []
    for region in sorted(aois_by_region):
        print(f"S1 {region} ({len(aois_by_region[region])} AOIs)...", flush=True)
        doc = catalog_s1_region(region, aois_by_region[region], cutoff, fetch_start, now)
        path = os.path.join(OUT_S1, f"{region_slug(region)}.json")
        write_json(path, doc)
        region_stats.append((region, doc["passCount"], doc["pairedPassCount"], doc.get("problems") or []))

    event_stats = []
    for event in CONFIRMED_EVENTS:
        print(f"S2 {event['id']} {event['trendId']}...", flush=True)
        doc = catalog_before_after(event, now)
        path = os.path.join(OUT_BA, f"{event['id']}.json")
        write_json(path, doc)
        event_stats.append((
            event["id"],
            event["trendId"],
            bool(doc.get("before")),
            bool(doc.get("after")),
            doc.get("problems") or [],
        ))

    print("\nSentinel-1 regions:")
    for region, n, paired, problems in region_stats:
        print(f"  {region}: {n} passes, {paired} paired" + (f" problems={problems}" if problems else ""))
    print("\nBefore/after:")
    for eid, tid, has_b, has_a, problems in event_stats:
        print(f"  {eid} ({tid}) before={has_b} after={has_a}" + (f" problems={problems}" if problems else ""))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        raise
