"""Writes Day's school holiday files (school/index.json and school/<CC>.json) from OpenHolidaysAPI.org, whose data is
under the Open Database License (ODbL): the files written here are under the same license.

    python3 -I school-holidays-data.py --out DIR

Regions are the country's top-level subdivisions; an entry for a smaller part counts for the region it is in."""
import argparse
import datetime
import json
import os
import time
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument("--out", required=True)
args = parser.parse_args()
BASE = "https://openholidaysapi.org"
SOURCE = "OpenHolidaysAPI.org, Open Database License (ODbL) https://opendatacommons.org/licenses/odbl/1-0/"
today = datetime.date.today()
YEARS = range(today.year - 1, today.year + 3)


def get(path):
    for attempt in range(3):
        try:
            request = urllib.request.Request(BASE + path, headers={"Accept": "application/json", "User-Agent": "holiday-files/1"})
            with urllib.request.urlopen(request, timeout=40) as response:
                return json.load(response)
        except Exception:
            if attempt == 2:
                raise
            time.sleep(3)


def text(names, languages):
    by_language = {n["language"].upper(): n["text"] for n in names or []}
    for language in languages:
        if language.upper() in by_language:
            return by_language[language.upper()]
    return next(iter(by_language.values()), None)


def write(name, document):
    with open(os.path.join(args.out, name), "w", encoding="utf-8") as file:
        json.dump(document, file, ensure_ascii=False, separators=(",", ":"))


os.makedirs(args.out, exist_ok=True)
countries, failed = [], []
for country in sorted(get("/Countries"), key=lambda c: c["isoCode"]):
    code = country["isoCode"]
    languages = list(country.get("officialLanguages") or [])
    try:
        regions = [{"code": s["code"], "name": text(s["name"], languages + ["EN"]) or s["code"]}
                   for s in get(f"/Subdivisions?countryIsoCode={code}")]
        known = [r["code"] for r in regions]
        entries = {}
        for year in YEARS:
            for item in get(f"/SchoolHolidays?countryIsoCode={code}&validFrom={year}-01-01&validTo={year}-12-31"):
                parts = [s["code"] for s in item.get("subdivisions") or []]
                tops = sorted({r for r in known for p in parts if p == r or p.startswith(r + "-")})
                if not item.get("nationwide") and not tops:
                    continue
                name = text(item["name"], languages + ["EN"])
                english = text(item["name"], ["EN"])
                # A school type of one region (vocational schools, say) is told apart by its short name.
                types = [g.get("shortName") or g["code"] for g in item.get("groups") or []
                         if any(g["code"].startswith(p + "-") for p in parts)]
                if types:
                    suffix = f" ({', '.join(sorted(types))})"
                    name, english = name + suffix, (english + suffix if english else None)
                key = (item["startDate"], item["endDate"], name)
                entry = entries.setdefault(key, {"date": item["startDate"], "end": item["endDate"], "name": name, "en": english,
                                                 "regions": set(), "kind": "school"})
                if item.get("nationwide"):
                    entry["regions"] = None
                elif entry["regions"] is not None:
                    entry["regions"].update(tops)
        if not entries:
            continue
        holidays = sorted(entries.values(), key=lambda e: (e["date"], e["name"]))
        for entry in holidays:
            if entry["regions"] is not None:
                entry["regions"] = sorted(entry["regions"])
        used = {r for e in holidays for r in e["regions"] or []}
        write(f"{code}.json", {"version": 1, "source": SOURCE, "country": code, "generated": today.isoformat(), "holidays": holidays})
        countries.append({"code": code, "name": text(country["name"], ["EN"]),
                          "regions": sorted([r for r in regions if r["code"] in used], key=lambda r: r["name"])})
    except Exception as error:
        failed.append(f"{code}: {error}")
write("index.json", {"version": 1, "source": SOURCE, "countries": countries})
with open(os.path.join(args.out, "LICENSE.txt"), "w", encoding="utf-8") as file:
    file.write(SOURCE + "\n")
print(len(countries), "countries written,", len(failed), "problems")
for line in failed[:10]:
    print(" ", line)
