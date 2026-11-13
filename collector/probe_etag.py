#!/usr/bin/env python3
"""One-off/nightly: record which collector feeds send ETag / Last-Modified."""
import json, os, time, requests
from run import RSS, UA
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = {"generatedMs": int(time.time()*1000), "feeds": {}}
for name, url in RSS.items():
    row = {"url": url, "etag": None, "lastModified": None, "http": None, "error": None}
    try:
        r = requests.head(url, headers=UA, timeout=15, allow_redirects=True)
        row["http"] = r.status_code
        row["etag"] = r.headers.get("ETag")
        row["lastModified"] = r.headers.get("Last-Modified")
        if row["etag"] is None and row["lastModified"] is None:
            g = requests.get(url, headers=UA, timeout=20)
            row["http"] = g.status_code
            row["etag"] = g.headers.get("ETag")
            row["lastModified"] = g.headers.get("Last-Modified")
    except Exception as ex:
        row["error"] = str(ex)[:160]
    out["feeds"][name] = row
    print(f"{name}: http={row['http']} etag={bool(row['etag'])} lm={bool(row['lastModified'])} err={row['error']}")
path = os.path.join(BASE, "data", "etag-support.json")
open(path, "w").write(json.dumps(out, indent=2))
print("wrote", path)
n = sum(1 for f in out["feeds"].values() if f.get("etag") or f.get("lastModified"))
print(json.dumps({"with_conditional": n, "total": len(out["feeds"])}))
