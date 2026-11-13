# OBSIDIAN OSINT feed

Source notes, a collector, and region-organized public event data for OBSIDIAN.

This repository holds only public RSS and open API material. There is no scraping, no HTML harvesting, and no login-wall collection.

## What's in the tree

- `collector/` — Python collector that polls public RSS feeds and writes event JSON.
- `data/` — Latest events, per-country slices, run archives, source notes, and public official-brief excerpts.
- `sources/geospatial/` — Notes on geospatial and satellite APIs (Nominatim, NASA, Copernicus, and related catalogues). These notes are documentation only.

## News and humanitarian feeds

The collector reads public RSS/Atom feeds only, including BBC News (world and regional), Al Jazeera, France 24, DW, The Guardian, NPR, UN News, ReliefWeb, Kyiv Independent, Middle East Eye, Defense News, MercoPress, NHK World, Yonhap, US State Department travel advisories, and US Department of Defense. Some listed feeds may be stale or unreachable; the collector records health for those sources rather than switching to scraping.

Event records in `data/` are derived from those public feeds. Official-brief files under `data/official-briefs/` are public U.S. government documents (for example the 2025 National Security Strategy and the 2026 unclassified Country Reports on Terrorism) and short excerpts from them.

## Geospatial sources, licences, and attribution

Geospatial APIs are documented in `sources/geospatial/`. Nothing in those notes is a substitute for each provider's terms.

- **Nominatim (OpenStreetMap).** Data are under the [Open Database License (ODbL)](https://www.openstreetmap.org/copyright). Credit OpenStreetMap and its contributors. Use of `nominatim.openstreetmap.org` must follow the [Nominatim usage policy](https://operations.osmfoundation.org/policies/nominatim/): an identifying `User-Agent`, at most 1 request per second, cached results, and no autocomplete or bulk/systematic geocoding.
- **NASA** (GIBS imagery, FIRMS active-fire data, and [api.nasa.gov](https://api.nasa.gov/)). Acknowledge NASA as the source and do not imply endorsement. NASA-led mission data are generally CC0 unless a restriction is marked. See [NASA data use and citation guidance](https://www.earthdata.nasa.gov/engage/open-data-services-software-policies/data-use-guidance). GIBS clients should also use the official GIBS/ESDIS acknowledgment. FIRMS/LANCE data are not advised for tactical or local-scale decisions; include or link the LANCE/FIRMS disclaimer if redistributing.
- **Copernicus Data Space Ecosystem / Sentinel.** Sentinel data are free, full and open. When distributing, credit `Copernicus Sentinel data [Year]` or, if adapted, `Contains modified Copernicus Sentinel data [Year]`. [Sentinel legal notice](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice) and [CDSE terms](https://dataspace.copernicus.eu/terms-and-conditions) apply.
- **Microsoft Planetary Computer and Element 84 Earth Search.** STAC search is used only as a catalogue. Dataset licences and attribution are those of each collection (for example USGS for Landsat, the Sentinel legal notice for Sentinel).

Keyed NASA FIRMS, api.nasa.gov, and Copernicus services require a key or account supplied locally by the operator. Keys are never stored in this repository and must never be baked into an app binary.

## No secrets

This repository holds no API keys, passwords, tokens, or private credentials. A local `secrets/` directory and `*.env` / `.env*` files are gitignored and were excluded from the published tree.
