#!/usr/bin/env python3
"""Rebuild index.html from the Claude dashboard artifact's page file.

Usage: python3 scripts/sync_from_artifact.py <artifact index.html> [repo index.html]

The artifact page is the source of truth (the daily Strava refresh edits it).
This script strips the publish wrapper, adds the app tags (manifest, icons,
service worker), and checks that the RUNS data still parses. It prints
"unchanged" or "updated: N runs, latest YYYY-MM-DD".
"""
import json
import re
import sys

APP_HEAD = '''<meta name="theme-color" content="#E8B10C">
<meta name="description" content="Tanaby's training log for the TCS Toronto Waterfront Half, Oct 18 2026.">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="icons/icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Road to HM">
'''
SW = ('<script>if("serviceWorker" in navigator){window.addEventListener("load",()=>'
      '{navigator.serviceWorker.register("sw.js").catch(()=>{});});}</script>\n')


def build(src: str) -> str:
    # The artifact read may wrap the page in a minimal outer document; keep the inner one.
    starts = [m.start() for m in re.finditer(r"<!doctype html>", src, re.I)]
    if not starts:
        sys.exit("no <!doctype html> found in artifact page")
    s = src[starts[-1]:]
    end = s.lower().find("</html>")
    if end < 0:
        sys.exit("no </html> found in artifact page")
    s = s[: end + len("</html>")] + "\n"
    if 'rel="manifest"' not in s:
        k = s.find("<title>")
        if k < 0:
            sys.exit("no <title> found")
        s = s[:k] + APP_HEAD + s[k:]
    if "serviceWorker" not in s:
        if s.count("</body>") != 1:
            sys.exit("expected exactly one </body>")
        s = s.replace("</body>", SW + "</body>")
    return s


def runs_summary(s: str) -> str:
    m = re.search(r"const RUNS\s*=\s*(\[.*?\]);", s, re.S)
    if not m:
        sys.exit("RUNS array not found")
    runs = json.loads(m.group(1))
    if not runs:
        sys.exit("RUNS array is empty")
    return f"{len(runs)} runs, latest {max(r['d'] for r in runs)}"


def main():
    src_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else "index.html"
    new = build(open(src_path, encoding="utf-8").read())
    summary = runs_summary(new)
    try:
        old = open(out_path, encoding="utf-8").read()
    except FileNotFoundError:
        old = ""
    if old == new:
        print("unchanged:", summary)
        return
    open(out_path, "w", encoding="utf-8").write(new)
    print("updated:", summary)


if __name__ == "__main__":
    main()
