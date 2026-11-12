#!/usr/bin/env python3
"""Builds changelog/index.html (English) and changelog/de/index.html (German) from changelog/releases.json.

To publish a version: add it to the top of changelog/releases.json (same shape as the other entries; leave out
"released" if the day isn't known), run `python3 scripts/changelog.py`, commit. Day's Settings > What's New opens
https://enrzh.github.io/Day/changelog/ (the German page for German devices), so the app shows it right away.
"""
import html, json, datetime, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
releases = json.loads((root / "changelog" / "releases.json").read_text(encoding="utf-8"))["releases"]

T = {
    "en": dict(lang="en", title="What’s New — Day", desc="What changed in each version of Day, newest first.",
               h1="What’s New", meta="What changed in each version of Day, newest first. Day comes from the App Store, which delivers the updates.",
               home="Home", other="Deutsch", other_href="de/", features="New features", fixes="Fixes",
               platform={"ios": "iPhone and iPad", "mac": "Mac"}, back="../", css="../site.css", icon="../images/icon.png",
               month=["January","February","March","April","May","June","July","August","September","October","November","December"],
               fmt=lambda d, m: f"{m[d.month-1]} {d.day}, {d.year}"),
    "de": dict(lang="de", title="Neuigkeiten — Day", desc="Was sich in jeder Version von Day geändert hat, die neueste zuerst.",
               h1="Neuigkeiten", meta="Was sich in jeder Version von Day geändert hat, die neueste zuerst. Day kommt aus dem App Store, der die Updates ausliefert.",
               home="Startseite", other="English", other_href="../", features="Neue Funktionen", fixes="Fehlerbehebungen",
               platform={"ios": "iPhone und iPad", "mac": "Mac"}, back="../../", css="../../site.css", icon="../../images/icon.png",
               month=["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"],
               fmt=lambda d, m: f"{d.day}. {m[d.month-1]} {d.year}"),
}

def items(lines):
    return "<ul>" + "".join(f"<li>{html.escape(x)}</li>" for x in lines) + "</ul>"

def build(lang):
    t = T[lang]
    out = []
    for r in releases:
        plat = "mac" if "mac" in r["platforms"] else "ios"
        date = ""
        if r.get("released"):
            d = datetime.date.fromisoformat(r["released"])
            date = f' · {t["fmt"](d, t["month"])}'
        feats = r["features"].get(lang) or r["features"]["en"]
        fixes = (r.get("fixes") or {}).get(lang) or (r.get("fixes") or {}).get("en") or []
        body = f'<h3>{t["features"]}</h3>{items(feats)}' if feats else ""
        if fixes:
            body += f'<h3>{t["fixes"]}</h3>{items(fixes)}'
        out.append(f'    <article id="{r["id"]}">\n      <h2>{r["version"]} <span class="meta">{t["platform"][plat]}{date}</span></h2>\n      {body}\n    </article>')
    page = f'''<!doctype html>
<html lang="{t["lang"]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{t["title"]}</title>
  <meta name="description" content="{t["desc"]}">
  <meta name="color-scheme" content="light dark">
  <link rel="icon" href="{t["icon"]}">
  <link rel="stylesheet" href="{t["css"]}">
  <style>article {{ margin-top: 2rem; }} article h2 {{ font-size: 1.35rem; margin-bottom: .4rem; }} article h2 .meta {{ font-size: .9rem; font-weight: 400; color: var(--muted); }} article h3 {{ font-size: .95rem; color: var(--muted); margin: .9rem 0 .2rem; }} article ul {{ margin: 0; padding-left: 1.2rem; }} article li {{ margin-bottom: .35rem; }}</style>
</head>
<body>
  <header class="top"><div class="wrap bar"><a class="brand" href="{t["back"]}"><img src="{t["icon"]}" width="32" height="32" alt="">Day</a><nav><a href="{t["back"]}">{t["home"]}</a><a href="{t["other_href"]}" hreflang="{ "de" if lang == "en" else "en" }">{t["other"]}</a></nav></div></header>
  <main id="main" class="wrap doc">
    <h1>{t["h1"]}</h1>
    <p class="meta">{t["meta"]}</p>
{chr(10).join(out)}
  </main>
</body>
</html>
'''
    path = root / "changelog" / ("de/index.html" if lang == "de" else "index.html")
    path.write_text(page, encoding="utf-8")

for lang in ("en", "de"):
    build(lang)
print("changelog/index.html and changelog/de/index.html written")
