# NASA GIBS (Global Imagery Browse Services)

**STATUS: APPROVED (Nov 13, 2026, 8:39 AM CT). Keyed layers work only with a key the user pastes, never in the APK. Nominatim: 1 request/sec, OSM attribution, story place names only.**

Verified 2026-11-13 ~07:35 America/Chicago from official docs/usage-policy pages (public, unauthenticated reads only). No API keys were used and no authenticated calls were made.

## Provider

NASA Earth Science Data and Information System (ESDIS). Official docs: [GIBS API documentation](https://nasa-gibs.github.io/gibs-api-docs/) and [Access Basics](https://nasa-gibs.github.io/gibs-api-docs/access-basics/). Earthdata overview: [GIBS API](https://www.earthdata.nasa.gov/engage/open-data-services-software/earthdata-developer-portal/gibs-api).

## What it covers

Global, full-resolution satellite imagery as pre-generated map tiles. Daily and near-real-time layers (true-color reflectance, fires/thermal anomalies, smoke, clouds, nighttime lights, and many science layers). Services: OGC WMTS (REST and KVP), WMS, TWMS, and generic XYZ/TMS. Projections: EPSG:4326, EPSG:3857, EPSG:3413 (Arctic), EPSG:3031 (Antarctic).

## Endpoint base URL

`https://gibs.earthdata.nasa.gov/`

WMTS “best available” roots (replace `best` with `std`, `nrt`, or `all` if needed):

- Geographic: `https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/`
- Web Mercator: `https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/`
- Arctic: `https://gibs.earthdata.nasa.gov/wmts/epsg3413/best/`
- Antarctic: `https://gibs.earthdata.nasa.gov/wmts/epsg3031/best/`

GetCapabilities (Geographic): `https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/1.0.0/WMTSCapabilities.xml`

REST tile pattern: `https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/{Layer}/default/{Time}/{TileMatrixSet}/{TileMatrix}/{TileRow}/{TileCol}.{ext}`

HTTP/1.1 clients may also use shard aliases `gibs-a`, `gibs-b`, and `gibs-c`.earthdata.nasa.gov. Official docs state GIBS does not currently support HTTP/2.

## Key / account requirement

None. Public, unauthenticated WMTS/WMS access. No sign-up.

## Rate limits / quotas

Official docs do **not** publish a per-request rate limit for ordinary interactive or light scripted use.

[Bulk downloading](https://nasa-gibs.github.io/gibs-api-docs/map-library-usage/) is defined as more than 1,000,000 imagery tiles in a 24-hour period. Those jobs should be coordinated at least 48 hours ahead with `earthdata-support@nasa.gov` (subject: “GIBS Bulk Download Request”). Bulk guidelines in that same page:

- Limit sustained download bandwidth to 50 Mbps.
- Limit concurrent downloads to 500 threads.
- Spread requests evenly; start small and ramp up.

OBSIDIAN use, if approved, should stay far below bulk thresholds and must not add a server-side tile harvester.

## Attribution and licence

Terms / acknowledgment: [GIBS Introduction — Data Use Guidance and Acknowledgements](https://nasa-gibs.github.io/gibs-api-docs/). NASA asks users who use GIBS in a client or presentation to add:

> We acknowledge the use of imagery provided by services from NASA's Global Imagery Browse Services (GIBS), part of NASA's Earth Science Data and Information System (ESDIS).

Broader ESDIS reuse guidance (acknowledge NASA as the source; do not imply endorsement; NASA-led mission data generally CC0 unless a restriction is marked): [Data Use and Citation Guidance](https://www.earthdata.nasa.gov/engage/open-data-services-software-policies/data-use-guidance).

## ETag / caching

**Not documented** in the official GIBS API docs as ETag or conditional-request support.

Observed on 2026-11-13 (not an official guarantee):

- Example WMTS tile: `ETag: 01e2o01o3c37i`, but `Cache-Control: max-age=0, no-store, no-cache, must-revalidate` and `Expires: Thu, 1 Jan 1970 00:00:00 GMT`.
- GetCapabilities: `Cache-Control: public, max-age=1800`; no `ETag` on that response.

Treat tile caching as best-effort only until GIBS documents it.

## Unauthenticated sample request

Documented example tile from [Access Basics](https://nasa-gibs.github.io/gibs-api-docs/access-basics/):

```
GET https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/2012-07-09/250m/6/13/36.jpg
```

Result: **HTTP 200**, `Content-Type: image/jpeg`, 47,192 bytes (2026-11-13 ~07:35 America/Chicago).

A ranged GET of GetCapabilities also returned **HTTP 206**.

## How it's connected

No credentials. Public WMTS tiles only. Not in the app until approved.

## App-promise constraints

No scraping. No server. Imagery, if approved, is for on-device briefing only — not a bulk archive.
