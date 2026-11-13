# Geospatial and satellite API source notes

**STATUS: APPROVED (Nov 13, 2026, 8:39 AM CT). Keyed layers work only with a key the user pastes, never in the APK. Nominatim: 1 request/sec, OSM attribution, story place names only.**

The Sentinel-1 / Sentinel-2 scene catalog built from the approved public STAC APIs is documented in [imagery-catalog.md](imagery-catalog.md) and written under `data/imagery/`. Those JSON files are catalogue metadata only.

Index of proposed free geospatial / satellite sources for the OBSIDIAN feed vault. These notes are vault documentation only. Nothing here is wired into the app. Do not add any of these to `Feeds.kt` until the source is approved.

Verification: Verified 2026-11-13 ~07:35 America/Chicago from official docs/usage-policy pages (public, unauthenticated reads only). No API keys were used and no authenticated calls were made.

## App promises (apply to every source here)

- No scraping, no HTML harvesting, no login walls.
- No server component in the app.
- No user location: do not send the device location to any geocoder or imagery API.
- Nominatim: light use only, with an identifying app `User-Agent`, at most 1 request per second, and results cached. No autocomplete, no bulk or systematic geocoding, no periodic background bursts.
- Suggested threat levels stay separate from the app's classifier (existing vault rule).

## How credentials are connected

- NASA GIBS, Microsoft Planetary Computer STAC search, Element 84 Earth Search STAC, and Nominatim: no credentials.
- NASA FIRMS, api.nasa.gov, and Copernicus Data Space Ecosystem: key or account to be registered under the project's bot contact email, not a personal identity, and stored in `obsidian-feed/secrets/geospatial-keys.env` (chmod 600).
- That secrets file was **not** created in this pass. It does not exist in the vault yet. When keys are issued, store them there and do not commit or copy them into these notes.

## Providers

| Note | Provider | Key / account | Official rate limit (verified) | Attribution / licence (verified) |
| --- | --- | --- | --- | --- |
| [nasa-gibs.md](nasa-gibs.md) | NASA GIBS | None | No per-request limit published for ordinary use. Bulk is defined as more than 1,000,000 tiles in 24 hours and should be coordinated 48 hours ahead; bulk guidelines are 50 Mbps sustained and 500 concurrent threads. | Credit GIBS/ESDIS with the official acknowledgment. [GIBS docs](https://nasa-gibs.github.io/gibs-api-docs/) |
| [nasa-firms.md](nasa-firms.md) | NASA FIRMS | Free `MAP_KEY` by email | 5,000 transactions per 10-minute interval; larger queries may count as multiple transactions. | Acknowledge NASA; follow ESDIS citation guidance; include or link the LANCE/FIRMS disclaimer if redistributing. Not advised for tactical or local-scale decisions. [FIRMS MAP_KEY](https://firms.modaps.eosdis.nasa.gov/api/map_key/) · [Readme citation](https://firms.modaps.eosdis.nasa.gov/download/Readme.txt) |
| [copernicus-data-space.md](copernicus-data-space.md) | Copernicus Data Space Ecosystem | Free account for downloads, Sentinel Hub, and openEO | General-user monthly quotas (reset on the 1st): Sentinel Hub 10,000 requests and 10,000 PU/month, 300 requests and 300 PU/minute; openEO 10,000 credits/month (documented as a temporary boost), 12 requests/minute on result jobs, 2 concurrent API requests. Catalogue path: 12 TB / 30 days, then slower. | Sentinel data are free, full and open; credit `Copernicus Sentinel data [Year]` or `Contains modified Copernicus Sentinel data [Year]`. Portal terms also apply. [CDSE terms](https://dataspace.copernicus.eu/terms-and-conditions) · [Quotas](https://documentation.dataspace.copernicus.eu/Quotas.html) |
| [microsoft-planetary-computer.md](microsoft-planetary-computer.md) | Microsoft Planetary Computer STAC | None for STAC search. SAS token needed for blob assets (anonymous token available). | Official docs do **not** publish a numeric rate limit for STAC search. SAS/data-access rate limits exist and vary by Azure region and optional subscription key, but no numbers are given beyond “should be generous” and tiered token expiry. | [Planetary Computer terms](https://planetarycomputer.microsoft.com/terms) plus Microsoft TOU. Dataset licences and attribution are per STAC collection, not a single catalogue licence. |
| [element84-earth-search.md](element84-earth-search.md) | Element 84 Earth Search STAC | None for STAC search | **Not verified:** no official rate-limit or usage-policy page was found. README says the API is free with no guaranteed service. | **Not verified as a single Earth Search licence.** README points licences to each AWS Open Data / STAC collection (for example Sentinel legal notice, USGS Landsat). [README](https://github.com/Element84/earth-search) |
| [nasa-api.md](nasa-api.md) | NASA api.nasa.gov | `DEMO_KEY` or free personal key | `DEMO_KEY`: 30 requests per IP per hour and 50 per IP per day. Registered key default: 1,000 requests per hour across all api.nasa.gov services. Limit headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`. | Acknowledge NASA as the source; do not imply endorsement. NASA-led mission data are generally CC0 unless marked. [api.nasa.gov](https://api.nasa.gov/) · [Data use guidance](https://www.earthdata.nasa.gov/engage/open-data-services-software-policies/data-use-guidance) |
| [nominatim.md](nominatim.md) | Nominatim (OpenStreetMap) | None (identifying `User-Agent` required) | Absolute maximum 1 request per second, applied to the whole app. Recurring scripts: 4 requests per minute. Cache results. No autocomplete or bulk/systematic queries. | Credit OpenStreetMap and its contributors; data under ODbL. [Nominatim usage policy](https://operations.osmfoundation.org/policies/nominatim/) · [OSM copyright](https://www.openstreetmap.org/copyright) |

## Unverified or incomplete items

- NASA GIBS: no official documentation of ETag/conditional request support (an `ETag` was observed on a tile response; tile `Cache-Control` was `max-age=0, no-store, no-cache, must-revalidate`).
- Microsoft Planetary Computer: no numeric STAC search rate limit in official docs.
- Element 84 Earth Search: no official rate-limit page and no dedicated terms-of-use page found.
- api.nasa.gov: unauthenticated sample was skipped because a key is required (a no-key request returned HTTP 403 `API_KEY_MISSING`). `DEMO_KEY` was not sent.
- FIRMS and Copernicus authenticated APIs: samples skipped because a key or account is required. CDSE STAC catalogue landing did respond unauthenticated (HTTP 200).
