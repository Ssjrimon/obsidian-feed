# NASA FIRMS (Fire Information for Resource Management System)

**STATUS: APPROVED (Nov 13, 2026, 8:39 AM CT). Keyed layers work only with a key the user pastes, never in the APK. Nominatim: 1 request/sec, OSM attribution, story place names only.**

Verified 2026-11-13 ~07:35 America/Chicago from official docs/usage-policy pages (public, unauthenticated reads only). No API keys were used and no authenticated calls were made.

## Provider

NASA LANCE / FIRMS (Land, Atmosphere Near real-time Capability for EOS). Official pages: [MAP_KEY](https://firms.modaps.eosdis.nasa.gov/api/map_key/), [Area API](https://firms.modaps.eosdis.nasa.gov/api/area/), [FIRMS API tutorial](https://firms.modaps.eosdis.nasa.gov/content/academy/data_api/firms_api_use.html), project site [firms.modaps.eosdis.nasa.gov](https://firms.modaps.eosdis.nasa.gov/).

## What it covers

Near-real-time and standard active-fire / thermal-anomaly detections from MODIS (Terra/Aqua), VIIRS (Suomi-NPP, NOAA-20, NOAA-21), and Landsat (US/Canada NRT). APIs include Area (CSV and other formats), availability, plus WMS/WFS map services. Day range per Area request is 1–5 days; bounding box or `world`.

## Endpoint base URL

`https://firms.modaps.eosdis.nasa.gov/`

Area API pattern:

`https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/{SOURCE}/{AREA_COORDINATES}/{DAY_RANGE}/{DATE}`

Example shape (do not call without a key): `/api/area/csv/{MAP_KEY}/MODIS_NRT/-85,-57,-32,14/1`

MAP_KEY status: `https://firms.modaps.eosdis.nasa.gov/mapserver/mapkey_status/?MAP_KEY=`

Sign-up: [Request FIRMS Map Key](https://firms.modaps.eosdis.nasa.gov/api/map_key/).

## Key / account requirement

A free `MAP_KEY` is required. Request it with an email; the key is sent to that address. For this vault, any key must be registered under the project's bot contact email, not a personal email. Resend/modify is via FIRMS `/download` login.

## Rate limits / quotas

Verified on the official MAP_KEY and Area API pages:

- **5,000 transactions per 10-minute interval.**
- Larger transactions may count as multiple requests (example given: requesting 7 days). Contact FIRMS if a higher limit is needed.
- The tutorial states the 10-minute window resets after you hit the limit.

No other numeric daily cap was published on those pages.

## Attribution and licence

Official citation and disclaimer are in [FIRMS download Readme.txt](https://firms.modaps.eosdis.nasa.gov/download/Readme.txt) (section “DATA CITATION AND DISCLAIMER”):

- NASA promotes full and open sharing. If LANCE/FIRMS data are provided to a third party, follow the citation guidelines and replicate or link the disclaimer.
- Citation information is pointed to: [Data Use and Citation Guidance](https://www.earthdata.nasa.gov/engage/open-data-services-software-policies/data-use-guidance) (the Readme’s `data-use-policy` URL currently redirects here).
- Disclaimer (also on [LANCE Disclaimer](https://www.earthdata.nasa.gov/data/projects/lance/disclaimer)): data are provided “as is”; users bear responsibility for use; **not advised for tactical decision-making or informing about conditions at a local scale**.

Acknowledge NASA as the source. Do not imply NASA endorsement.

## ETag / caching

**Not documented** on the official API or MAP_KEY pages. No unauthenticated API response was fetched to observe headers, because a key is required.

## Unauthenticated sample request

Skipped. The Area and status APIs require a `MAP_KEY`. No key was used.

## How it's connected

Key or account registered under the project's bot contact email, stored in `obsidian-feed/secrets/geospatial-keys.env` (chmod 600). That secrets file was not created in this pass. Not in the app until approved.

## App-promise constraints

No scraping and no user location. If approved, query by story geography or a declared area of interest — never the device GPS. Near-real-time fire points are detections, not confirmed wildfire reports; keep the official disclaimer visible in any UI.
