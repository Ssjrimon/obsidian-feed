# Microsoft Planetary Computer STAC API

**STATUS: APPROVED (Nov 13, 2026, 8:39 AM CT). Keyed layers work only with a key the user pastes, never in the APK. Nominatim: 1 request/sec, OSM attribution, story place names only.**

Verified 2026-11-13 ~07:35 America/Chicago from official docs/usage-policy pages (public, unauthenticated reads only). No API keys were used and no authenticated calls were made.

## Provider

Microsoft Planetary Computer. Official pages: [STAC API reference](https://planetarycomputer.microsoft.com/docs/reference/stac/), [Using Tokens for Data Access](https://planetarycomputer.microsoft.com/docs/concepts/sas), [Supplemental Terms of Use](https://planetarycomputer.microsoft.com/terms).

## What it covers

A free STAC catalogue of open Earth-observation collections hosted on Azure, including Landsat, Sentinel, and other public datasets. STAC search returns item metadata and asset URLs. Actual imagery/files on Azure Blob Storage usually need a short-lived SAS token.

## Endpoint base URL

STAC API v1: `https://planetarycomputer.microsoft.com/api/stac/v1/`

Useful paths: `/collections`, `/collections/{id}`, `/search` (GET or POST), `/collections/{id}/items`.

SAS (for assets, not required for search):

- `https://planetarycomputer.microsoft.com/api/sas/v1/token/{collection_id}`
- `https://planetarycomputer.microsoft.com/api/sas/v1/sign?href={url}`

## Key / account requirement

Official SAS docs: **the STAC metadata API is available to all users and does not require an account or a token**. Anyone can also request a SAS token without registering; a subscription key is optional and improves SAS rate limits / token expiry. Tokens must not be shared or monetized (terms).

For OBSIDIAN's proposed use (catalogue search, not bulk blob egress), no credentials are required.

## Rate limits / quotas

**Not fully verified as numbers.**

- Official SAS documentation says rate limiting is applied to data/SAS access, that limits “should be generous,” and that limits and token expiry depend on (1) whether the request comes from Azure West Europe and (2) whether a valid API subscription key is supplied. Token lifetime is described in the [terms](https://planetarycomputer.microsoft.com/terms) as up to 1 week (Tier 1) or up to 6 months (Tier 2). **No numeric requests-per-second or quota figures are published in those official pages.**
- Official docs do **not** state a numeric rate limit for unauthenticated STAC search.

Do not treat third-party or GitHub-discussion remarks as official limits.

## Attribution and licence

[Supplemental Terms of Use for Microsoft Planetary Computer Previews](https://planetarycomputer.microsoft.com/terms) (last updated January 2023), which supplement the Microsoft Terms of Use. The service is described as a preview: as-is, no SLA, not meant for mission-critical use.

There is **no single dataset licence for the whole catalogue**. Each STAC collection carries its own licence and provider/attribution metadata. Credit the upstream data producer required by that collection (for example USGS for Landsat, Copernicus Sentinel legal notice for Sentinel).

## ETag / caching

**Not documented** in the official STAC or SAS pages. Observed on the unauthenticated landing GET: `Cache-Control: no-store`, no `ETag`.

## Unauthenticated sample request

```
GET https://planetarycomputer.microsoft.com/api/stac/v1/
```

Result: **HTTP 200**, `Content-Type: application/json; charset=utf-8` (2026-11-13 ~07:35 America/Chicago). STAC landing document with `conformsTo` classes.

No SAS-signed blob download was attempted.

## How it's connected

No credentials for STAC search. Not in the app until approved.

## App-promise constraints

No scraping, no server, no user location. If later used to pull assets, stay inside SAS terms and prefer signed URLs over bulk anonymous egress.
