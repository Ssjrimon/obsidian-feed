# Collector source notes — 2026-11-05 night (America/Chicago)

## Fixed tonight
- User-Agent + Accept made browser-like (ReliefWeb was 406 on OBSIDIAN-specific UA earlier).
- Retries (2–3) on HTTP 429/503/empty for Google News and ReliefWeb.
- Google News queries that were empty on first pass recovered after retries (Gaza, Sudan, Ukraine, Red Sea, Taiwan, Somalia, Syria, Sahel).

## Still failing / documented
| Source | Status | Reason |
| --- | --- | --- |
| ReliefWeb updates RSS | Intermittent 202 empty / 406 bot block | HDX bot protection; no stable public alternate without approved appname (API v1 decommissioned; v2 needs approved appname). |
| ReliefWeb Headlines | Same | Same host protection; often 202 with empty body. |
| NHK World text RSS | Dead 404 | `.../nhkworld/en/news/rss/all.xml` gone. Podcast RSS is audio-only. `all.json` open API exists but latest items ~2026-09 (stale). |
| NATO HQ news RSS | Dead 404 | Site redesign; cps/.../news.xml and rssFeed.xsl paths 404. SHAPE/ACT feeds 403. No public English RSS replacement found without scraping. |
| BleepingComputer | Cloudflare challenge (403) | Intermittent; feed still listed. |
| GDELT doc API | Rate limit / non-JSON | Existing 10s spacing; still returns 429 or empty under load. |

## ETag probe
See `data/etag-support.json` (15/62 feeds advertise ETag or Last-Modified on HEAD/GET tonight).
