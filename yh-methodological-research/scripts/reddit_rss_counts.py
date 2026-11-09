"""Count Reddit posts per pain cluster per product family, from search .rss feeds (stdlib only).

Usage: python3 reddit_rss_counts.py config.json out.json > reddit.log 2>&1   (run in the background)

Reddit's .rss search needs no login, but it rate-limits unauthenticated readers: requests are
paced (config "pace_seconds", default 8), a 429 waits 60s, and out.json is rewritten after every
request, so rerunning the same command resumes. Expect about 30 minutes for 48 searches. Log to a
file, never through `| tail`: tail holds everything until the run exits.

The counts are too noisy to score with (keyword false positives, a 100-result cap, searches that
come back empty). Use them as a rough second signal, and use the example thread TITLES as
confirmation in users' own words. STRICT = a cluster keyword is in the title; LOOSE = in the title
or the first 600 characters of the body.

config.json (see examples/reddit.kavela-181026.json):
  {"window": "year", "pace_seconds": 8,
   "families": {"Workflow tools": "n8n+zapier+Integromat"},
   "clusters": {"silent": {"query": "\\"stopped working\\" OR silently",
                           "keywords": ["stopped working", "silently"]}}}
"""

import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) research/1.0"
NS = {"a": "http://www.w3.org/2005/Atom"}


def fetch(subs, query, window):
    url = f"https://www.reddit.com/r/{subs}/search.rss?" + urllib.parse.urlencode(
        {"q": query, "restrict_sr": "on", "sort": "relevance", "t": window, "limit": "100"})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for _ in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except urllib.error.HTTPError as e:  # 429: Reddit's unauthenticated limit; wait it out
            print(f"  http {e.code}, waiting 60s", flush=True)
            time.sleep(60)
        except Exception as e:
            print(f"  error {e}, waiting 20s", flush=True)
            time.sleep(20)
    return b""


def text_of(entry):
    raw = entry.findtext("a:content", default="", namespaces=NS)
    return re.sub(r"<[^>]+>", " ", html.unescape(raw)).lower()


def count(body, kws):
    strict = loose = 0
    examples = []
    try:
        root = ET.fromstring(body) if body else None
    except ET.ParseError:
        root = None
    for e in (root.findall("a:entry", NS) if root is not None else []):
        title = (e.findtext("a:title", default="", namespaces=NS) or "").strip()
        hit_t = any(k in title.lower() for k in kws)
        hit_b = any(k in text_of(e)[:600] for k in kws)
        strict += hit_t
        if hit_t or hit_b:
            loose += 1
            cat = e.find("a:category", NS)
            examples.append({"title": title, "link": e.find("a:link", NS).get("href"),
                             "sub": cat.get("term") if cat is not None else "",
                             "date": (e.findtext("a:updated", default="", namespaces=NS) or "")[:10], "strict": hit_t})
    return strict, loose, sorted(examples, key=lambda x: not x["strict"])[:4]


def main(cfg_path, out_path):
    with open(cfg_path) as f:
        cfg = json.load(f)
    families, clusters = cfg["families"], cfg["clusters"]
    window, pace = cfg.get("window", "year"), cfg.get("pace_seconds", 8)
    out = {"families": list(families), "cells": {}, "examples": {}}
    if os.path.exists(out_path):
        with open(out_path) as f:
            out = json.load(f)

    for cid, c in clusters.items():
        kws = [k.lower() for k in c["keywords"]]
        for fam, subs in families.items():
            key = f"{cid}|{fam}"
            if out["cells"].get(key, {}).get("fetched"):
                continue
            body = fetch(subs, c["query"], window)
            strict, loose, ex = count(body, kws)
            out["cells"][key] = {"strict": strict, "loose": loose, "fetched": bool(body)}
            out["examples"][key] = ex
            with open(out_path, "w") as f:
                json.dump(out, f, indent=1)
            print(f"{cid:<10} {fam[:40]:<40} strict {strict:>3}  loose {loose:>3}  {'ok' if body else 'FETCH FAILED'}", flush=True)
            time.sleep(pace)

    missing = [k for k in (f"{c}|{f}" for c in clusters for f in families) if not out["cells"].get(k, {}).get("fetched")]
    print(f"\ndone: {len(clusters) * len(families) - len(missing)} of {len(clusters) * len(families)} searches fetched"
          + (f"; not fetched: {', '.join(missing)}" if missing else ""))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
