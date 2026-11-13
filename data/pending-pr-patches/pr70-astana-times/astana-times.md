# Source proposal: The Astana Times

**Status:** approved by owner (2026-11-05 in America/Chicago chat) — added to `Feeds.kt` and `Outlets.kt` as **state-affiliated** (not independent confirmation); awaiting Compliance review and owner merge.
**Proposed:** 2026-11-05 (America/Chicago night refresh)
**Region gap filled:** Central Asia (Kazakhstan and regional). Current `Feeds.kt` has no Central Asia outlet.

## Feed

| Field | Value |
| --- | --- |
| Name | The Astana Times |
| Suggested id | `astanatimes` |
| URL | https://astanatimes.com/feed/ |
| Format | RSS 2.0 (public) |
| Language | English |
| Update rate | Several items per day (live check 2026-11-06 afternoon: 10 items; newest same-day) |
| ETag / conditional | **Yes.** HEAD/GET return `ETag` and `Last-Modified` (re-verified 2026-11-06 ~13:10 America/Chicago). |
| Terms / licence | About: https://astanatimes.com/about-us/ · Privacy: https://astanatimes.com/privacy-policy/ (no dedicated terms-of-use URL; 404). Public RSS; Compliance should confirm reuse/attribution. No login. |
| Reuse note | Public English RSS. Personal on-device briefing; Compliance review before merge. **State-adjacent:** do not count as independent confirmation (Outlets.kt `Tier.STATE_AFFILIATED`). |

## Sample items (live fetch 2026-11-06 afternoon, America/Chicago)

1. **News Digest: Foreign Media on Kazakhstan’s AI Ambitions, Football, Global Trade and Water Challenges** — https://astanatimes.com/2026/11/news-digest-foreign-media-on-kazakhstans-ai-ambitions-football-global-trade-and-water-challenges/ — Fri, 06 Nov 2026 14:34:48 +0000
2. **Kazakhstan, UNODC Discuss Stronger Cooperation Against Transnational Crime** — https://astanatimes.com/2026/11/kazakhstan-unodc-discuss-stronger-cooperation-against-transnational-crime/ — Fri, 06 Nov 2026 13:47:36 +0000
3. **Kazakhstan to Hold Biennial Symposia on Al-Farabi and Yasawi Heritage, Vice President Says** — https://astanatimes.com/2026/11/kazakhstan-to-hold-biennial-symposia-on-al-farabi-and-yasawi-heritage-vice-president-says/ — Fri, 06 Nov 2026 13:28:33 +0000

## What it adds vs existing sources

`Feeds.kt` has South Asia (The Hindu) and Indo-Pacific outlets but **nothing** for Kazakhstan / Central Asia. Astana Times fills Astana/Almaty map nodes with English security, diplomacy, and regional cooperation copy that BBC Asia rarely carries at this granularity. Mapped to `Region.CAUCASUS` (label CAUCASUS-C.ASIA).

ETag + Last-Modified supported.

## Evidence checklist

- [x] Public RSS, no login
- [x] Live HEAD shows ETag + Last-Modified
- [x] Three dated sample items from live GET
- [x] About/privacy links recorded; state-adjacent caveat noted
- [x] Owner approval (approved 2026-11-05 by the owner in America/Chicago chat)
- [ ] Compliance review
- [x] `Feeds.kt` entry (only after approval; STATE_AFFILIATED in Outlets.kt)
