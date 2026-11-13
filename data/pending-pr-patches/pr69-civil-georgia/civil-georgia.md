# Source proposal: Civil Georgia

**Status:** approved by owner (2026-11-05 in America/Chicago chat) — added to `Feeds.kt` and `Outlets.kt`; awaiting Compliance review and owner merge.
**Proposed:** 2026-11-05 (America/Chicago night refresh)
**Region gap filled:** Caucasus (Georgia / South Caucasus). Current `Feeds.kt` has no Caucasus outlet.

## Feed

| Field | Value |
| --- | --- |
| Name | Civil Georgia |
| Suggested id | `civilgeorgia` |
| URL | https://civil.ge/feed |
| Format | RSS 2.0 (public) |
| Language | English |
| Update rate | Multiple items per day (live check 2026-11-06 afternoon: 10 items; newest same-day) |
| ETag / conditional | **Yes.** HEAD/GET return `ETag` and `Last-Modified` (re-verified 2026-11-06 ~13:10 America/Chicago). |
| Terms / licence | Site home https://civil.ge/ (English independent news). No separate terms-of-use URL found (404 on /terms-of-use/). Public RSS; Compliance should record reuse/attribution from site footer/about before merge. No login. |
| Reuse note | Public RSS for personal on-device briefing. Compliance review required before merge. |

## Sample items (live fetch 2026-11-06 afternoon, America/Chicago)

1. **China’s Vice President Visits Georgia** — https://civil.ge/archives/757368 — Fri, 06 Nov 2026 13:21:49 +0000
2. **Ivanishvili Meets Israeli Ambassador at Georgian Dream Office** — https://civil.ge/archives/757531 — Fri, 06 Nov 2026 09:22:03 +0000
3. **Proposed Election Changes to Limit Vote Appeal Chances, Georgian Watchdogs Warn** — https://civil.ge/archives/756748 — Thu, 05 Nov 2026 15:58:24 +0000

## What it adds vs existing sources

No Caucasus-specific source in `Feeds.kt` today (BBC/Guardian/DW only catch major spillover). Civil Georgia is a long-running English outlet focused on Georgian politics, Russia pressure, EU accession, and security — map-node relevant for Tbilisi / Caucasus.

Strong conditional-request support (ETag + Last-Modified).

## Evidence checklist

- [x] Public RSS, no login
- [x] Live HEAD shows ETag + Last-Modified
- [x] Three dated sample items from live GET
- [x] Terms gap noted for Compliance
- [x] Owner approval (approved 2026-11-05 by the owner in America/Chicago chat)
- [ ] Compliance review
- [x] `Feeds.kt` entry (only after approval)
