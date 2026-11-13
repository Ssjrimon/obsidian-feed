# Element 84 Earth Search STAC API

**STATUS: APPROVED (Nov 13, 2026, 8:39 AM CT). Keyed layers work only with a key the user pastes, never in the APK. Nominatim: 1 request/sec, OSM attribution, story place names only.**

Verified 2026-11-13 ~07:35 America/Chicago from official docs/usage-policy pages (public, unauthenticated reads only). No API keys were used and no authenticated calls were made.

## Provider

Element 84 (FilmDrop). Official pages: [Earth Search](https://element84.com/earth-search/), [Examples](https://element84.com/earth-search/examples/), [GitHub README](https://github.com/Element84/earth-search) / [raw README](https://raw.githubusercontent.com/Element84/earth-search/master/README.md). Task target is the v1 API at `earth-search.aws.element84.com/v1`. A v2 endpoint is documented as beta elsewhere; this note stays on v1 unless later approved a switch.

## What it covers

A free STAC search API over public datasets on the AWS Registry of Open Data. README collections include USGS Landsat Collection 2 (`landsat-c2-l2`), Sentinel-2 L1C and L2A, Sentinel-1 GRD, Copernicus DEM (30 m / 90 m), NAIP, and `sentinel-2-c1-l2a`. Search by collection, bbox, datetime, intersects, and query parameters such as cloud cover. Some assets are public `https://` URLs; requester-pays buckets use `s3://` and need AWS credentials (STAC storage extension).

## Endpoint base URL

`https://earth-search.aws.element84.com/v1`

Search: `https://earth-search.aws.element84.com/v1/search`

## Key / account requirement

None for STAC search. Official README and product page describe it as a free-to-use public STAC API. No sign-up is documented for catalogue search.

## Rate limits / quotas

**Could not verify.** No official rate-limit, quota, or acceptable-use page was found on element84.com, the v1 API, or the GitHub README. The README says the public API is provided as a best effort and “does not come with any guaranteed service.”

Do not treat unofficial third-party remarks about page size as official policy.

## Attribution and licence

**No dedicated Earth Search terms-of-use page was found.** The official README does not state a catalogue-wide licence. Data and metadata licences are those of each underlying AWS Open Data / STAC collection. For Sentinel collections, use the [Copernicus Sentinel legal notice](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice) (`Copernicus Sentinel data [Year]` or `Contains modified Copernicus Sentinel data [Year]`). Credit USGS for Landsat, and the collection's stated licensor for other sets.

README also states there is no guaranteed service; production users are invited to talk to Element 84 about a private catalogue.

## ETag / caching

**Not documented** in the official README or product pages. Observed on the unauthenticated v1 landing GET: `ETag: W/"d29-QPs+H0wJLUX32EZKNgzG3k6wfQ8"` (weak ETag). No `Cache-Control` or `Last-Modified` header on that response.

## Unauthenticated sample request

```
GET https://earth-search.aws.element84.com/v1
```

Result: **HTTP 200**, `Content-Type: application/json; charset=utf-8` (2026-11-13 ~07:35 America/Chicago). Catalog id `earth-search-aws`, title “Earth Search by Element 84”.

## How it's connected

No credentials for STAC search. Not in the app until approved. Requester-pays S3 assets are out of scope unless separately approved (they would need AWS credentials, which this proposal does not add).

## App-promise constraints

No scraping, no server, no user location. Light STAC search only if approved.
