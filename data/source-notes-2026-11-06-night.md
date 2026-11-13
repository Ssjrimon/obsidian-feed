# Collector source notes — 2026-11-06 night (America/Chicago)

## Night run (PASS after ReliefWeb fix)
- Archive: `20261106-21*.json` (final after curl fallback)
- events: 312 · sources_ok: 63 / 66
- MercoPress, Balkan Insight, Civil Georgia, The Astana Times: still OK
- ReliefWeb + ReliefWeb Headlines: recovered via curl fallback when Python requests gets HTTP 202 empty (HDX bot protection)

## Fix applied
- `collector/run.py`: `curl_get` helper; treat HTTP 202 as retryable; on final ReliefWeb attempt, curl-fetch public RSS if requests body empty/challenge.

## Still failing (no public RSS replacement without scrape/login)
| Source | Status | Reason |
| --- | --- | --- |
| BleepingComputer | Cloudflare 403 challenge | Intermittent; keep listed |
| NHK World text RSS | Dead 404 | `all.json` open API exists but stale (ids ~20260905); podcast audio-only |
| NATO HQ news RSS | Dead 404 | Site redesign; SHAPE/ACT RSS 403; no public English RSS found |

## Open OSINT draft PRs (3/3 max — no 4th opened)
- #68 Balkan Insight — approved; Feeds.kt already on branch; awaiting Compliance + merge
- #69 Civil Georgia — approved; Feeds.kt patch local only (pending push)
- #70 Astana Times — approved; STATE_AFFILIATED caveat; Feeds.kt patch local only (pending push)

## Blockers
- user-GitHub-xai: 404 on private repo (cannot push Feeds.kt/Outlets.kt for #69/#70)
- cursor-github: read OK; no create_or_update_file / push_files in this connector
- CloudAgent: previously refused (credits / Grok model)

## Skipped
- Weekly Monday-morning source-health note (today is Friday night)
