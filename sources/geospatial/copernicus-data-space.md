# Copernicus Data Space Ecosystem (CDSE)

**STATUS: APPROVED (Nov 13, 2026, 8:39 AM CT). Keyed layers work only with a key the user pastes, never in the APK. Nominatim: 1 request/sec, OSM attribution, story place names only.**

Verified 2026-11-13 ~07:35 America/Chicago from official docs/usage-policy pages (public, unauthenticated reads only). No API keys were used and no authenticated calls were made.

## Provider

Copernicus Data Space Ecosystem (European Commission / ESA, operated with T-Systems and partners). Official pages: [Registration](https://documentation.dataspace.copernicus.eu/Registration.html), [Quotas and Limitations](https://documentation.dataspace.copernicus.eu/Quotas.html), [Terms and conditions](https://dataspace.copernicus.eu/terms-and-conditions), [STAC catalogue](https://documentation.dataspace.copernicus.eu/APIs/STAC.html), [Sentinel Hub authentication](https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Overview/Authentication.html), [openEO](https://documentation.dataspace.copernicus.eu/APIs/openEO/openEO.html).

## What it covers

Search, download, and processing of Copernicus data, especially **Sentinel-1** (SAR, including GRD/SLC; useful through clouds) and **Sentinel-2** (optical, 10 m). Also Sentinel-3/5P/6, Copernicus DEM, contributing missions, and many Copernicus Land Monitoring Service collections. Interfaces: STAC and OData catalogues, S3, Sentinel Hub APIs, and openEO.

## Endpoint base URL

- STAC (current): `https://stac.dataspace.copernicus.eu/v1/`
- Collections: `https://stac.dataspace.copernicus.eu/v1/collections`
- Item search: `https://stac.dataspace.copernicus.eu/v1/search`
- Legacy STAC `https://catalogue.dataspace.copernicus.eu/stac` is documented as deprecated from 17 November 2025.
- OData: `https://catalogue.dataspace.copernicus.eu/odata/v1/Products`
- Sentinel Hub: `https://sh.dataspace.copernicus.eu`
- openEO (core CDSE): `https://openeo.dataspace.copernicus.eu/`
- Identity / tokens: `https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token`
- Register: [dataspace.copernicus.eu](https://dataspace.copernicus.eu) (avatar → REGISTER).

## Key / account requirement

A free CDSE account is required to access Earth observation data (terms §4) and to use Sentinel Hub and openEO. Email verification is required. Sentinel Hub uses OAuth2 client credentials created in the dashboard; do not request a new token for every call (token requests are themselves rate-limited; HTTP 429 means too many token requests).

STAC catalogue landing and collection metadata were reachable without a token in this check (see sample below). Downloads, processing, and Sentinel Hub/openEO still need the account.

Any account must be registered under the project's bot contact email, not a personal identity. Creating multiple accounts to bypass quotas is forbidden.

## Rate limits / quotas

Verified from [Quotas and Limitations](https://documentation.dataspace.copernicus.eu/Quotas.html) for **Copernicus General Users**. Most numeric quotas are monthly and reset on the first day of the month. Transfer volume is a rolling 30-day window.

Sentinel Hub APIs:

- 10,000 requests per month
- 300 requests per minute
- 10,000 processing units (PU) per month
- 300 PU per minute
- Batch Processing API is not available to General Users

openEO / Algorithm Plaza:

- 10,000 credits per month (footnote 15: documented as a **temporary boost**; see the 3 September 2024 news item)
- 12 requests per minute, and only for synchronous `POST /result` and batch `POST /{job_id}/result` (also described as 1 request per 5 seconds)
- 2 concurrent API requests; 2 concurrent processing jobs

S3, OData, STAC (Immediately Available Data):

- 20 MB/s bandwidth per connection; 4 concurrent connections
- 12 TB transfer per 30 days; after that, speed drops to 1 MB/s and 1 connection
- “2000 requests per minute” in that table column is footnoted as **only applying to S3**, so it should not be treated as a published STAC cap

Direct HTTP access to COGs: 50,000 requests per month.

Access tokens stay active 10 minutes and can be refreshed within 60 minutes; max 100 active sessions.

## Attribution and licence

- [CDSE Terms and conditions](https://dataspace.copernicus.eu/terms-and-conditions)
- Sentinel data and service information: [Legal notice on the use of Copernicus Sentinel Data and Service Information](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice) (PDF; verified 2026-11-13). Access is free, full and open, without warranty. Required notices when communicating or distributing:
  - `Copernicus Sentinel data [Year]` / `Copernicus Service information [Year]`
  - If adapted or modified: `Contains modified Copernicus Sentinel data [Year]` / `Contains modified Copernicus Service information [Year]`
- Other portal content is for non-commercial use; credit the copyright owner. Do not resell or redistribute portal materials as a compiled product except as the Sentinel legal notice allows for the data themselves.
- Do not bypass [quotas](https://documentation.dataspace.copernicus.eu/Quotas.html) with many accounts.

## ETag / caching

**Not documented** on the STAC or quotas pages. Observed on the unauthenticated STAC landing GET: HTTP 200, no `ETag` or `Cache-Control` header.

## Unauthenticated sample request

Catalogue landing only (no account, no token):

```
GET https://stac.dataspace.copernicus.eu/v1/
```

Result: **HTTP 200**, `Content-Type: application/json`, STAC catalog id `cdse-stac` (2026-11-13 ~07:35 America/Chicago).

Sentinel Hub and openEO processing samples were skipped (account/token required).

## How it's connected

Key or account registered under the project's bot contact email, stored in `obsidian-feed/secrets/geospatial-keys.env` (chmod 600). That secrets file was not created in this pass. Not in the app until approved.

## App-promise constraints

No scraping and no server. A watch-app client should stay well inside General User quotas and must not download bulk scenes as a background service. No user location.
