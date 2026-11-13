# Collector source notes — 2026-11-06 afternoon (America/Chicago)

## Morning failure investigation
- Morning archive `20261106-0715.json` actually completed (294 events, 58/63 OK).
- `run.py` mtime 07:37 CST shows MercoPress trailing-slash + SSL retry fix applied after first fail symptoms.
- `latest.json` mtime 07:52 without matching archive/health rewrite → partial second write / interrupted re-run after the fix.
- Root cause of morning FAIL report: MercoPress SSL EOF on `/rss` (no trailing slash) plus known dead/blocked feeds. Fix already in `run.py` (`/rss/` + SSL-aware retries).

## Afternoon run (PASS)
- Archive: `20261106-1310.json`
- events: 304 · bytes ~274k · sources_ok: 62 / 66
- MercoPress: recovered (10 items)
- Added to local collector (owner-approved): Balkan Insight (60), Civil Georgia (10), The Astana Times (10)

## Still failing (documented; no public RSS replacement without scrape/login)
| Source | Status | Reason |
| --- | --- | --- |
| BleepingComputer | Cloudflare 403 challenge | Intermittent; keep listed |
| NHK World text RSS | Dead 404 | `all.json` open API exists but stale (~2026-09); podcast audio-only |
| NATO HQ news RSS | Dead 404 | Site redesign; cps/.../news.xml and rssFeed.xsl paths 404; no public English RSS found |
| ReliefWeb Headlines | 500 / empty | HDX bot protection; updates RSS often OK |

## Open OSINT draft PRs (3/3 max — no 4th opened)
- #68 Balkan Insight — approved; Feeds.kt already on branch; awaiting Compliance + merge
- #69 Civil Georgia — approved; Feeds.kt patch prepared locally (pending push)
- #70 Astana Times — approved; STATE_AFFILIATED; Feeds.kt patch prepared locally (pending push)

## Skipped
- Weekly Monday-morning source-health note (today is Friday)
