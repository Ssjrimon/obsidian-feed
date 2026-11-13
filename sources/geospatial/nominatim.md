# Nominatim (OpenStreetMap geocoding)

**STATUS: APPROVED (Nov 13, 2026, 8:39 AM CT). Keyed layers work only with a key the user pastes, never in the APK. Nominatim: 1 request/sec, OSM attribution, story place names only.**

Verified 2026-11-13 ~07:35 America/Chicago from official docs/usage-policy pages (public, unauthenticated reads only). No API keys were used and no authenticated calls were made.

## Provider

OpenStreetMap Foundation public Nominatim service. Official policy: [Nominatim Usage Policy (aka Geocoding Policy)](https://operations.osmfoundation.org/policies/nominatim/). Licence and credit: [OpenStreetMap Copyright and License](https://www.openstreetmap.org/copyright). The usage policy also points to the OSMF Terms of Use.

This policy applies only to `nominatim.openstreetmap.org`, not to a self-hosted Nominatim.

## What it covers

Forward and reverse geocoding of OpenStreetMap data (place search, address lookup). JSON/JSON v2 and other formats. This is a place-name lookup, not satellite imagery.

## Endpoint base URL

`https://nominatim.openstreetmap.org/`

Search example pattern: `https://nominatim.openstreetmap.org/search?q={query}&format=jsonv2`

## Key / account requirement

None. No API key. Each request **must** send a valid HTTP `User-Agent` or `Referer` that identifies the application. Stock User-Agents from HTTP libraries are not acceptable. Ideally include a contact address.

Proposed identifying header if this source is approved: an OBSIDIAN app `User-Agent` plus project contact, not a generic library default.

## Rate limits / quotas

Verified from the official usage policy:

- **No heavy use: an absolute maximum of 1 request per second.**
- Limits apply to the whole website or application (all users combined), not per device.
- Cache results on the client. Repeated identical queries may be treated as faulty and blocked.
- Bulk geocoding of larger amounts is not encouraged. Smaller one-time bulk jobs, if done at all, must be a single thread on one machine. Scripts running longer than a day, or at regular intervals, are restricted to **4 requests per minute**.
- Apps must be able to switch the service off or to another endpoint without a software update. A proxy plus caching is recommended if possible — but OBSIDIAN has **no server**, so the client itself must stay well under the cap and cache locally.
- Periodic requests from apps are treated as bulk geocoding and are strongly discouraged.

Unacceptable and ban-worthy uses include: client-side autocomplete; systematic grid or “download all places” queries; scraping the details page; reselling geocoding.

## Attribution and licence

- [Nominatim usage policy](https://operations.osmfoundation.org/policies/nominatim/): clearly display attribution suitable for the medium. Data are under the **ODbL**, which requires share-alike (small extractions may be covered by fair use / fair dealing).
- [OpenStreetMap copyright](https://www.openstreetmap.org/copyright): credit OpenStreetMap and its contributors, and make clear the data are available under the ODbL (for example by linking that copyright page). Suggested credit is of the form “© OpenStreetMap contributors.”

A licence string is also returned on JSON results (observed: `Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright`).

## ETag / caching

The official policy **requires client-side caching** of results. It does not document `ETag` or `Last-Modified` support on the public API.

Observed on the single probe GET: no `ETag` or `Last-Modified`; Varnish `x-cache: MISS`. Do not rely on HTTP validators; cache by query string on device.

## Unauthenticated sample request

One light probe only, with an identifying User-Agent (`OBSIDIAN-feed-source-notes/1.0 (project bot contact; single documentation probe)`):

```
GET https://nominatim.openstreetmap.org/search?q=Washington%20DC&format=jsonv2&limit=1
```

Result: **HTTP 200**, `Content-Type: application/json; charset=utf-8` (2026-11-13 ~07:35 America/Chicago). Returned Washington, D.C. (`lat` 38.8950982, `lon` -77.0363849) with the ODbL licence string above. No further Nominatim calls were made.

## How it's connected

No credentials. Identifying app `User-Agent` only. Not in the app until approved.

## App-promise constraints

- Light use only, max 1 request per second, cache hits, no autocomplete, no bulk, no scheduled polling.
- **No user location:** do not reverse-geocode the device GPS. If used at all, geocode place names already in a story or brief.
- No scraping and no server. If OSMF asks that the app stop using the public instance, it must be possible to disable this source without waiting for a store release if later required that hook.
