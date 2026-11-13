#!/usr/bin/env python3
"""OBSIDIAN OSINT feed collector. Run: python3 run.py  -> ../data/latest.json (SID schema v1)"""
import json, re, time, hashlib, html, os, sys, calendar
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
import requests, feedparser
sys.path.insert(0, os.path.dirname(__file__))
from geo import locate
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
UA = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/rss+xml, application/atom+xml, application/xml;q=0.9, text/xml;q=0.8, */*;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
}

def curl_get(url, timeout=25):
    """Fallback GET via curl for hosts that 202/empty Python requests (still public RSS)."""
    import subprocess
    try:
        cp = subprocess.run(
            ["curl","-sS","-L","--max-time",str(timeout),
             "-A", UA["User-Agent"],
             "-H", f"Accept: {UA['Accept']}",
             "-H", f"Accept-Language: {UA['Accept-Language']}",
             "-w", "\n__HTTP__%{http_code}",
             url],
            capture_output=True, timeout=timeout+5)
        out = cp.stdout or b""
        if b"\n__HTTP__" in out:
            body, _, codeb = out.rpartition(b"\n__HTTP__")
        else:
            body, codeb = out, b"0"
        try: code = int(codeb.decode().strip() or "0")
        except Exception: code = 0
        return code, body
    except Exception as ex:
        return 0, str(ex).encode()[:200]

NOW = time.time(); WINDOW = 48*3600; MAX_BYTES = 290_000

RSS = {
 "BBC News":"https://feeds.bbci.co.uk/news/world/rss.xml",
 "BBC News Middle East":"https://feeds.bbci.co.uk/news/world/middle_east/rss.xml",
 "BBC News Africa":"https://feeds.bbci.co.uk/news/world/africa/rss.xml",
 "BBC News Asia":"https://feeds.bbci.co.uk/news/world/asia/rss.xml",
 "BBC News Europe":"https://feeds.bbci.co.uk/news/world/europe/rss.xml",
 "BBC News Latin America":"https://feeds.bbci.co.uk/news/world/latin_america/rss.xml",
 "Al Jazeera":"https://www.aljazeera.com/xml/rss/all.xml",
 "France 24":"https://www.france24.com/en/rss",
 "DW":"https://rss.dw.com/rdf/rss-en-world",
 "The Guardian":"https://www.theguardian.com/world/rss",
 "NPR":"https://feeds.npr.org/1004/rss.xml",
 "UN News":"https://news.un.org/feed/subscribe/en/news/all/rss.xml",
 "ReliefWeb":"https://reliefweb.int/updates/rss.xml",
 "Kyiv Independent":"https://kyivindependent.com/news-archive/rss/",
 "Times of Israel":"https://www.timesofisrael.com/feed/",
 "Middle East Eye":"https://www.middleeasteye.net/rss",
 "The Diplomat":"https://thediplomat.com/feed/",
 "Defense News":"https://www.defensenews.com/arc/outboundfeeds/rss/?outputType=xml",
 "War on the Rocks":"https://warontherocks.com/feed/",
 "Breaking Defense":"https://breakingdefense.com/feed/",
 "The Record":"https://therecord.media/feed",
 "BleepingComputer":"https://www.bleepingcomputer.com/feed/",
 "Krebs on Security":"https://krebsonsecurity.com/feed/",
 "AllAfrica":"https://allafrica.com/tools/headlines/rdf/latest/headlines.rdf",
 # MercoPress: intermittent SSL EOF; trailing slash matches Feeds.kt; extra retries below.
 "MercoPress":"https://en.mercopress.com/rss/",
 # NHK World text RSS 404 since ~2026; podcast RSS is audio-only; all.json stale (last ~2026-09). Kept for health tracking.
 "Balkan Insight":"https://balkaninsight.com/feed/",
 "Civil Georgia":"https://civil.ge/feed",
 "The Astana Times":"https://astanatimes.com/feed/",
 "NHK World":"https://www3.nhk.or.jp/nhkworld/en/news/rss/all.xml",
 "Yonhap":"https://en.yna.co.kr/RSS/news.xml",
 "US State Dept Travel Advisories":"https://travel.state.gov/_res/rss/TAsTWs.xml",
 "US DoD":"https://www.defense.gov/DesktopModules/ArticleCS/RSS.ashx?ContentType=1&Site=945&max=10",
 "UK MoD":"https://www.gov.uk/government/organisations/ministry-of-defence.atom",
 # NATO redesigned site; cps/.../news.xml and rssFeed.xsl paths all 404; no public English RSS replacement found (SHAPE/ACT 403).
 "NATO":"https://www.nato.int/cps/rss/en/natohq/news.xml",
 "ReliefWeb Headlines":"https://reliefweb.int/headlines/rss.xml",
}
GNEWS_Q = ["airstrike OR missile strike","drone attack","military clashes","coup OR junta","ceasefire talks","sanctions announced",
 "warship OR naval drills","cyberattack","Gaza OR West Bank","Ukraine Russia front","Sudan RSF","Sahel militants","Red Sea Houthi",
 "Taiwan Strait","South China Sea","North Korea missile","Iran IAEA","Haiti gangs","Myanmar junta","Congo M23","Somalia al-Shabaab",
 "Venezuela military","Pakistan attack","Kashmir","Syria clashes","Lebanon Hezbollah","Iraq militia","Libya clashes","Ethiopia conflict","Nigeria gunmen"]
for _q in GNEWS_Q:
    RSS["GN:"+_q] = "https://news.google.com/rss/search?q="+requests.utils.quote(_q+" when:2d")+"&hl=en-US&gl=US&ceid=US:en"
PRIMARY = {"US DoD","UK MoD","NATO","US State Dept Travel Advisories"}
GDELT_Q = ['(airstrike OR missile OR shelling OR coup OR militants OR warship OR cyberattack)']

CAT = [("KINETIC",r"airstrike|air strike|missile|drone strike|drones?|shelling|bomb|killed|attack|offensive|artillery|rocket|strike|clashes|gunmen|troops|fighting|explosion|war\b"),
       ("CYBER",r"cyber|ransomware|hacker|hack|malware|breach|ddos|vulnerability|zero-day|phishing"),
       ("SECURITY",r"military|navy|naval|warship|sanction|terror|militant|insurgent|border|nuclear|weapon|defen[cs]e|coup|arrest|police|security|blockade|hostage|refugee|humanitarian"),
       ("POLITICAL",r"election|president|minister|parliament|government|talks|summit|protest|vote|diplomat|treaty|ceasefire|policy|opposition|court"),
       ("TECH",r"\bai\b|artificial intelligence|satellite|semiconductor|chip|space|launch")]
HARD = [("QUAKE",r"earthquake|quake"),("TSUNAMI",r"tsunami"),("STORM",r"hurricane|typhoon|cyclone|storm"),("FLOOD",r"flood"),
        ("VOLCANO",r"volcan|eruption"),("FIRE",r"wildfire|bushfire"),("DROUGHT",r"drought|famine"),("OUTBREAK",r"outbreak|cholera|ebola|mpox|measles|epidemic")]
SIG = r"nuclear (strike|attack|test|weapon use)|false nuclear|invasion|coup|declares war|mass casualt|dozens killed|hundreds killed|martial law|assassinat"
HIGH = r"killed|dead|airstrike|missile|offensive|explosion|hostage|state of emergency|evacuat"
MOD = r"attack|clashes|sanction|protest|drone|military|arrest|cyber|ransomware|strike"
STOP = set("says said after with from over into amid will that this have been their more than news live latest update week year what".split())
NOISE = r"obituar|dies aged|died aged|techno|album|music|film|movie|train crash|week in pictures|morning update|football|soccer|cricket|tennis|recipe|celebrity|box office|premier league|olympic|fashion|horoscope|review:"

def clean_url(u):
    try:
        s = urlsplit(u); q = [(k,v) for k,v in parse_qsl(s.query) if not re.match(r"utm_|fbclid|gclid|cmp|ocid|at_|mc_", k, re.I)]
        return urlunsplit((s.scheme, s.netloc, s.path, urlencode(q), ""))
    except Exception: return u
def strip(t): return re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",html.unescape(t or ""))).strip()
def two_sent(t):
    s = re.split(r"(?<=[.!?])\s+", t); out = " ".join(s[:2]); return out[:400]
def norm_title(t): return re.sub(r"[^a-z0-9 ]","",t.lower())

def fetch_rss(item):
    name,url = item; out=[]; last_err=None
    # Retry: Google News and some hosts return 503/empty under load; ReliefWeb blocks non-browser UAs.
    attempts = 3 if (name.startswith("GN:") or "reliefweb" in url or "news.google.com" in url or "mercopress" in url) else 2
    for attempt in range(attempts):
        try:
            r = requests.get(url, headers=UA, timeout=25)
            if r.status_code in (429, 503, 202) or (r.status_code >= 500 and attempt + 1 < attempts):
                last_err = f"http {r.status_code}"
                # Last attempt on ReliefWeb Headlines: curl often gets the RSS when requests gets 202/empty.
                if attempt + 1 >= attempts and "reliefweb.int" in url:
                    ccode, cbody = curl_get(url)
                    if ccode == 200 and cbody and (b"<rss" in cbody[:2000] or b"<feed" in cbody[:2000]):
                        body = cbody
                        # fall through to parse below
                    else:
                        time.sleep(2 + attempt * 3); continue
                else:
                    time.sleep(2 + attempt * 3); continue
                # if curl succeeded, skip normal body=r.content and parse curl body
                f = feedparser.parse(body)
                for e in f.entries[:60]:
                    tp = e.get("published_parsed") or e.get("updated_parsed")
                    ts = calendar.timegm(tp) if tp else NOW
                    src = name; title = strip(e.get("title"))
                    out.append({"title":title,"summary":strip(e.get("summary") or e.get("description")),
                                "link":clean_url(e.get("link","")),"ts":ts,"source":src})
                return name, out, None
            if r.status_code == 406 and "reliefweb" in url:
                return name, [], "blocked bot/UA (406)"
            if r.status_code == 404:
                return name, [], f"http 404 dead URL"
            body = r.content or b""
            if (not body) or (b"Just a moment..." in body[:2000] and b"<rss" not in body[:500] and b"<feed" not in body[:500]):
                last_err = f"http {r.status_code} empty/challenge"
                # ReliefWeb Headlines often 202/empty to requests but serves RSS to curl.
                if "reliefweb.int" in url:
                    ccode, cbody = curl_get(url)
                    if ccode == 200 and cbody and (b"<rss" in cbody[:2000] or b"<feed" in cbody[:2000]):
                        body = cbody
                        r = type("R", (), {"status_code": ccode, "content": cbody})()
                    elif attempt + 1 < attempts:
                        time.sleep(2 + attempt * 3); continue
                    else:
                        return name, [], last_err
                elif attempt + 1 < attempts:
                    time.sleep(2 + attempt * 3); continue
                else:
                    return name, [], last_err
            f = feedparser.parse(body)
            if not f.entries and attempt + 1 < attempts:
                last_err = f"http {r.status_code} empty"; time.sleep(1.5 + attempt * 2); continue
            for e in f.entries[:60]:
                tp = e.get("published_parsed") or e.get("updated_parsed")
                ts = calendar.timegm(tp) if tp else NOW
                src = name; title = strip(e.get("title"))
                if name.startswith("GN:"):
                    src = (e.get("source") or {}).get("title") or (title.rsplit(" - ",1)[-1] if " - " in title else "Google News")
                    title = title.rsplit(" - ",1)[0] if " - " in title else title
                out.append({"title":title,"summary":strip(e.get("summary") or e.get("description")),
                            "link":clean_url(e.get("link","")),"ts":ts,"source":src})
            return name, out, None
        except Exception as ex:
            last_err = str(ex)[:120]
            if attempt + 1 < attempts:
                # SSL EOF / connection resets (seen on MercoPress) need a bit more spacing than empty bodies.
                delay = 4 + attempt * 3 if ("SSL" in last_err or "Connection" in last_err) else 2 + attempt * 2
                time.sleep(delay); continue
            return name, [], last_err
    return name, out, last_err

def fetch_gdelt(q):
    out=[]
    try:
        r=None; last=None
        for _try in range(4):
          try:
            r = requests.get("https://api.gdeltproject.org/api/v2/doc/doc", params={"query":q+" sourcelang:english","mode":"artlist","format":"json","maxrecords":75,"timespan":"24h","sort":"datedesc"}, headers=UA, timeout=60)
            if r.text.lstrip().startswith("{"): break
            last="non-json %s"%r.status_code
          except Exception as e: last=str(e); r=None
          time.sleep(35 if (r is not None and r.status_code==429) else 12)
        if r is None or not r.text.lstrip().startswith("{"): raise Exception(last or "no response")
        for a in r.json().get("articles",[]):
            sd = a.get("seendate","")
            try: ts = calendar.timegm(time.strptime(sd,"%Y%m%dT%H%M%SZ"))
            except Exception: ts = NOW
            dom = a.get("domain","")
            out.append({"title":strip(a.get("title")),"summary":"","link":clean_url(a.get("url","")),"ts":ts,"source":dom,"gdelt_country":a.get("sourcecountry")})
        return "GDELT:"+q[:20], out, None
    except Exception as ex: return "GDELT:"+q[:20], [], str(ex)[:120]

def classify(text):
    t=text.lower()
    hk = next((k for k,p in HARD if re.search(p,t)), None)
    cat = next((c for c,p in CAT if re.search(p,t)), "GENERAL")
    lvl = "SIGNIFICANT" if re.search(SIG,t) else "HIGH" if re.search(HIGH,t) else "MODERATE" if re.search(MOD,t) else "LOW"
    return cat, hk, lvl

def main():
    os.makedirs(os.path.join(DATA,"by-country"),exist_ok=True); os.makedirs(os.path.join(DATA,"archive"),exist_ok=True)
    health={}; raw=[]
    with ThreadPoolExecutor(12) as ex:
        res = list(ex.map(fetch_rss, RSS.items()))
    for q in GDELT_Q:  # GDELT asks for ~1 req / 5s
        res.append(fetch_gdelt(q)); time.sleep(10)
    for name,items,err in res:
        health[name]={"ok":err is None,"items":len(items),"error":err}; raw+=items
    events={}; seen_titles={}; sigs={}
    raw.sort(key=lambda x: x["source"].startswith("Yonhap"))  # let multi-outlet items lead
    for it in raw:
        if not it["title"] or NOW-it["ts"]>WINDOW or it["ts"]>NOW+3600: continue
        text = it["title"]+" . "+it["summary"]
        if re.search(NOISE, text.lower()): continue
        cat,hk,lvl = classify(text)
        geo = locate(it["title"]) or locate(text)
        if not geo: 
            if cat=="GENERAL": continue
            geo={"iso2":None,"admin1":None,"city":None,"lat":None,"lon":None,"regionCode":"GLOBAL","placeCode":None}
        if cat=="GENERAL" and lvl=="LOW" and not hk: continue
        nt = norm_title(it["title"]); key = " ".join(nt.split()[:8])
        toks = set(w for w in nt.split() if len(w)>3 and w not in STOP)
        match = seen_titles.get(key)
        if not match:
            for eid0,(tk0,iso0,ts0) in sigs.items():
                if iso0==geo.get("iso2") and abs(ts0-it["ts"])<36*3600 and toks and len(toks&tk0)/max(1,min(len(toks),len(tk0)))>=0.5 and len(toks&tk0)>=3:
                    match=eid0; break
        if match:
            ev = events[match]
            if it["source"] not in ev["sources"]: ev["sources"].append(it["source"])
            if it["link"] and it["link"] not in ev["links"]: ev["links"].append(it["link"])
            continue
        eid = hashlib.sha1((key+"|"+str(geo.get("iso2"))).encode()).hexdigest()[:16]
        geo.pop("_country",None)
        events[eid]={"id":eid,"title":it["title"][:200],"summary":two_sent(it["summary"]) or it["title"][:200],"links":[it["link"]] if it["link"] else [],
            "publishedMs":int(it["ts"]*1000),"sources":[it["source"]],"primary":it["source"] in PRIMARY,"category":cat,
            "suggestedLevel":lvl,"hardKind":hk,"geo":geo}
        seen_titles[key]=eid; sigs[eid]=(toks,geo.get("iso2"),it["ts"])
    rank={"SIGNIFICANT":3,"HIGH":2,"MODERATE":1,"LOW":0}
    evs = sorted(events.values(), key=lambda e:(rank[e["suggestedLevel"]], len(e["sources"]), e["publishedMs"]), reverse=True)
    cap={}; kept=[]
    for e in evs:
        k=e["sources"][0]
        if len(e["sources"])==1:
            cap[k]=cap.get(k,0)+1
            if cap[k]>12: continue
        kept.append(e)
    evs=kept
    for e in evs: e["links"]=e["links"][:4]; e["sources"]=e["sources"][:6]
    out={"generatedMs":int(time.time()*1000),"version":1,"events":evs}
    while len(json.dumps(out,ensure_ascii=False).encode())>MAX_BYTES and out["events"]: out["events"]=out["events"][:int(len(out["events"])*0.9)]
    out["events"].sort(key=lambda e:e["publishedMs"], reverse=True)
    w=lambda p,o: open(p,"w").write(json.dumps(o,ensure_ascii=False,separators=(",",":")))
    w(os.path.join(DATA,"latest.json"),out)
    by={}
    for e in out["events"]:
        iso=e["geo"]["iso2"]
        if iso and iso!="JO": by.setdefault(iso,[]).append(e)
    for f in os.listdir(os.path.join(DATA,"by-country")): os.remove(os.path.join(DATA,"by-country",f))
    for iso,l in by.items(): w(os.path.join(DATA,"by-country",iso+".json"),{"generatedMs":out["generatedMs"],"version":1,"iso2":iso,"events":l})
    w(os.path.join(DATA,"archive",time.strftime("%Y%m%d-%H%M")+".json"),out)
    w(os.path.join(DATA,"health.json"),{"generatedMs":out["generatedMs"],"sources":health})
    regions={}
    for e in out["events"]: regions[e["geo"]["regionCode"]]=regions.get(e["geo"]["regionCode"],0)+1
    print(json.dumps({"events":len(out["events"]),"bytes":len(json.dumps(out,separators=(",",":")).encode()),"sources_ok":sum(h["ok"] and h["items"]>0 for h in health.values()),"sources_total":len(health),"regions":regions,"failed":[k for k,h in health.items() if not h["ok"] or h["items"]==0]},indent=1))
if __name__=="__main__": main()
