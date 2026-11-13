# NASA Open APIs (api.nasa.gov)

**STATUS: APPROVED (Nov 13, 2026, 8:39 AM CT). Keyed layers work only with a key the user pastes, never in the APK. Nominatim: 1 request/sec, OSM attribution, story place names only.**

Verified 2026-11-13 ~07:35 America/Chicago from official docs/usage-policy pages (public, unauthenticated reads only). No API keys were used and no authenticated calls were made.

## Provider

NASA Open APIs at [api.nasa.gov](https://api.nasa.gov/). Authentication and rate limits are documented on that page (api.data.gov / API Umbrella style keys).

## What it covers

A shared developer key portal for many NASA HTTP APIs, including (among others) EONET (natural-event tracker, relevant to hazard briefing), EPIC (Earth full-disk imagery), NeoWs, DONKI space weather, APOD, and others. GIBS imagery itself is listed on the same site but is accessed at `gibs.earthdata.nasa.gov` and does not use this key (see [nasa-gibs.md](nasa-gibs.md)).

## Endpoint base URL

`https://api.nasa.gov/`

Key signup and documentation: `https://api.nasa.gov/`

Examples from the official page (patterns only; a key is required at request time):

- NeoWs feed: `https://api.nasa.gov/neo/rest/v1/feed`
- EONET is documented from this portal and has its own API docs linked there
- EPIC: `https://api.nasa.gov/EPIC/api/natural/images`

## Key / account requirement

A key is required for API calls. The docs allow a shared `DEMO_KEY` for initial exploration, with much lower limits, and encourage a free personal key for real use. Signup is at [api.nasa.gov](https://api.nasa.gov/). Anyone can register.

For this vault, a personal key must be registered under the project's bot contact email, not a personal email. Recovery contact listed on the site: `hq-open-innovation@mail.nasa.gov`.

`DEMO_KEY` is still an API key. It was **not** sent in this verification pass.

## Rate limits / quotas

Verified from [api.nasa.gov — Authentication / Web Service Rate Limits](https://api.nasa.gov/):

- Default for a registered key: **1,000 requests per hour**, applied across all api.nasa.gov services for that key. Exceeding the limit temporarily blocks the key for an hour (rolling window; worked example is on the same page). Contact NASA for higher limits.
- `DEMO_KEY`: **30 requests per IP address per hour** and **50 requests per IP address per day**.
- Current usage is exposed on every response as `X-RateLimit-Limit` and `X-RateLimit-Remaining`.
- Individual services may set different limits (example on the same page: InSight weather was listed at 2,000 hits per hour per IP). Check the specific service if one is later proposed for the app.

## Attribution and licence

api.nasa.gov does not publish a separate attribution sentence beyond general NASA reuse rules. Use [Data Use and Citation Guidance](https://www.earthdata.nasa.gov/engage/open-data-services-software-policies/data-use-guidance): NASA should be acknowledged as the source; material used factually must not suggest or imply endorsement; NASA-led mission data are generally CC0 unless marked with a restriction; do not claim copyright in NASA material.

## ETag / caching

**Not documented** on api.nasa.gov for these APIs. Rate-limit headers are documented. No successful API response was fetched in this pass, so cache headers were not observed.

## Unauthenticated sample request

Skipped as a successful call: the service needs a key. A probe **without** a key was run only to confirm that requirement (no `DEMO_KEY`, no personal key):

```
GET https://api.nasa.gov/neo/rest/v1/feed?start_date=2015-09-07&end_date=2015-09-08
```

Result: **HTTP 403**, JSON `API_KEY_MISSING` — “No api_key was supplied. Get one at https://api.nasa.gov:443” (2026-11-13 ~07:35 America/Chicago).

## How it's connected

Key or account registered under the project's bot contact email, stored in `obsidian-feed/secrets/geospatial-keys.env` (chmod 600). That secrets file was not created in this pass. Not in the app until approved.

## App-promise constraints

No scraping, no server, no user location. Prefer a registered key over `DEMO_KEY` if this source is approved, so the shared demo quota is not consumed.
