#!/usr/bin/env python3
"""Builds the changelog pages from changelog/releases.json: English at changelog/index.html, and one page for each other
language Day is in at changelog/<lang>/index.html (de, es, fr, it, ja, ko, pt-BR, zh-Hans, zh-Hant).

To publish a version: add it to the top of changelog/releases.json (same shape as the other entries, with a "features" and
"fixes" list in every language; leave out "released" if the day isn't known), run `python3 scripts/changelog.py`, commit.
Day's Settings > What's New opens https://enrzh.github.io/Day/changelog/ (or the page for the device's language), so the app
shows it right away. A language missing from an entry falls back to English.

The pages use no script, font or image from anywhere but this site, so nothing outside it has to be reachable to read them.
"""
import html, json, datetime, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
releases = json.loads((root / "changelog" / "releases.json").read_text(encoding="utf-8"))["releases"]

EN_MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]

# lang -> UI strings. "dir" is the folder under changelog/ ("" for English). "name" is the language's own name for the switcher.
T = {
    "en": dict(dir="", name="English", title="What’s New — Day", desc="What changed in each version of Day, newest first.",
               h1="What’s New", meta="What changed in each version of Day, newest first. Day comes from the App Store, which delivers the updates.",
               home="Home", features="New features", fixes="Fixes", platform={"ios": "iPhone and iPad", "mac": "Mac"},
               month=EN_MONTHS, fmt=lambda d, m: f"{m[d.month-1]} {d.day}, {d.year}"),
    "de": dict(dir="de", name="Deutsch", title="Neuigkeiten — Day", desc="Was sich in jeder Version von Day geändert hat, die neueste zuerst.",
               h1="Neuigkeiten", meta="Was sich in jeder Version von Day geändert hat, die neueste zuerst. Day kommt aus dem App Store, der die Updates ausliefert.",
               home="Startseite", features="Neue Funktionen", fixes="Fehlerbehebungen", platform={"ios": "iPhone und iPad", "mac": "Mac"},
               month=["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"],
               fmt=lambda d, m: f"{d.day}. {m[d.month-1]} {d.year}"),
    "es": dict(dir="es", name="Español", title="Novedades — Day", desc="Qué cambió en cada versión de Day, la más reciente primero.",
               h1="Novedades", meta="Qué cambió en cada versión de Day, la más reciente primero. Day viene de la App Store, que entrega las actualizaciones.",
               home="Inicio", features="Novedades", fixes="Correcciones", platform={"ios": "iPhone y iPad", "mac": "Mac"},
               month=["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"],
               fmt=lambda d, m: f"{d.day} de {m[d.month-1]} de {d.year}"),
    "fr": dict(dir="fr", name="Français", title="Nouveautés — Day", desc="Ce qui a changé dans chaque version de Day, la plus récente en premier.",
               h1="Nouveautés", meta="Ce qui a changé dans chaque version de Day, la plus récente en premier. Day vient de l’App Store, qui fournit les mises à jour.",
               home="Accueil", features="Nouvelles fonctionnalités", fixes="Corrections", platform={"ios": "iPhone et iPad", "mac": "Mac"},
               month=["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"],
               fmt=lambda d, m: f"{d.day} {m[d.month-1]} {d.year}"),
    "it": dict(dir="it", name="Italiano", title="Novità — Day", desc="Cosa è cambiato in ogni versione di Day, la più recente per prima.",
               h1="Novità", meta="Cosa è cambiato in ogni versione di Day, la più recente per prima. Day arriva dall’App Store, che consegna gli aggiornamenti.",
               home="Home", features="Nuove funzioni", fixes="Correzioni", platform={"ios": "iPhone e iPad", "mac": "Mac"},
               month=["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"],
               fmt=lambda d, m: f"{d.day} {m[d.month-1]} {d.year}"),
    "ja": dict(dir="ja", name="日本語", title="新機能 — Day", desc="Day の各バージョンでの変更点（新しいものから）。",
               h1="新機能", meta="Day の各バージョンでの変更点を、新しいものから順に掲載しています。Day は App Store から入手でき、アップデートも App Store が配信します。",
               home="ホーム", features="新機能", fixes="修正", platform={"ios": "iPhone と iPad", "mac": "Mac"},
               month=[str(i) for i in range(1, 13)], fmt=lambda d, m: f"{d.year}年{d.month}月{d.day}日"),
    "ko": dict(dir="ko", name="한국어", title="새로운 기능 — Day", desc="Day 각 버전의 변경 사항, 최신순.",
               h1="새로운 기능", meta="Day 각 버전의 변경 사항을 최신순으로 보여 줍니다. Day는 App Store에서 받으며, 업데이트도 App Store가 전달합니다.",
               home="홈", features="새로운 기능", fixes="수정 사항", platform={"ios": "iPhone 및 iPad", "mac": "Mac"},
               month=[str(i) for i in range(1, 13)], fmt=lambda d, m: f"{d.year}년 {d.month}월 {d.day}일"),
    "pt-BR": dict(dir="pt-BR", name="Português", title="Novidades — Day", desc="O que mudou em cada versão do Day, a mais recente primeiro.",
               h1="Novidades", meta="O que mudou em cada versão do Day, a mais recente primeiro. O Day vem da App Store, que entrega as atualizações.",
               home="Início", features="Novos recursos", fixes="Correções", platform={"ios": "iPhone e iPad", "mac": "Mac"},
               month=["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"],
               fmt=lambda d, m: f"{d.day} de {m[d.month-1]} de {d.year}"),
    "zh-Hans": dict(dir="zh-Hans", name="简体中文", title="新功能 — Day", desc="Day 各版本的更新内容，最新的在前。",
               h1="新功能", meta="Day 各版本的更新内容，最新的在前。Day 来自 App Store，由 App Store 提供更新。",
               home="首页", features="新功能", fixes="修复", platform={"ios": "iPhone 和 iPad", "mac": "Mac"},
               month=[str(i) for i in range(1, 13)], fmt=lambda d, m: f"{d.year}年{d.month}月{d.day}日"),
    "zh-Hant": dict(dir="zh-Hant", name="繁體中文", title="新功能 — Day", desc="Day 各版本的更新內容，最新的在前。",
               h1="新功能", meta="Day 各版本的更新內容，最新的在前。Day 來自 App Store，由 App Store 提供更新。",
               home="首頁", features="新功能", fixes="修正", platform={"ios": "iPhone 與 iPad", "mac": "Mac"},
               month=[str(i) for i in range(1, 13)], fmt=lambda d, m: f"{d.year}年{d.month}月{d.day}日"),
}

def items(lines):
    return "<ul>" + "".join(f"<li>{html.escape(x)}</li>" for x in lines) + "</ul>"

def paths(lang):
    """Where the page sits: its file, and the way back to the site's root (css, icon, home)."""
    d = T[lang]["dir"]
    return (root / "changelog" / (d + "/index.html" if d else "index.html")), ("../../" if d else "../")

def href(frm, to):
    """Link from the page of `frm` to the page of `to`."""
    dst = T[to]["dir"]
    if frm == "en":
        return (dst + "/") if dst else "./"
    return ("../" + dst + "/") if dst else "../"

def build(lang):
    t = T[lang]
    path, back = paths(lang)
    css, icon = back + "site.css", back + "images/icon.png"
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
    langs = "".join(f'<a href="{href(lang, other)}" hreflang="{other}" lang="{other}">{T[other]["name"]}</a>' for other in T if other != lang)
    alternates = "".join(f'\n  <link rel="alternate" hreflang="{other}" href="https://enrzh.github.io/Day/changelog/{T[other]["dir"] + "/" if T[other]["dir"] else ""}">' for other in T)
    page = f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{t["title"]}</title>
  <meta name="description" content="{t["desc"]}">
  <meta name="color-scheme" content="light dark">
  <link rel="icon" href="{icon}">
  <link rel="stylesheet" href="{css}">{alternates}
  <style>article {{ margin-top: 2rem; }} article h2 {{ font-size: 1.35rem; margin-bottom: .4rem; }} article h2 .meta {{ font-size: .9rem; font-weight: 400; color: var(--muted); }} article h3 {{ font-size: .95rem; color: var(--muted); margin: .9rem 0 .2rem; }} article ul {{ margin: 0; padding-left: 1.2rem; }} article li {{ margin-bottom: .35rem; }} .langs {{ display: flex; flex-wrap: wrap; gap: .3rem 1rem; margin: 0 0 1rem; font-size: .9rem; }}</style>
</head>
<body>
  <header class="top"><div class="wrap bar"><a class="brand" href="{back}"><img src="{icon}" width="32" height="32" alt="">Day</a><nav><a href="{back}">{t["home"]}</a></nav></div></header>
  <main id="main" class="wrap doc">
    <h1>{t["h1"]}</h1>
    <p class="meta">{t["meta"]}</p>
    <nav class="langs" aria-label="Language">{langs}</nav>
{chr(10).join(out)}
  </main>
</body>
</html>
'''
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(page, encoding="utf-8")

for lang in T:
    build(lang)
print("changelog pages written:", ", ".join(("changelog/" + (T[l]["dir"] + "/" if T[l]["dir"] else "")) for l in T))
