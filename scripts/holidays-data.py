"""Writes Day's holiday files (index.json and one <CC>.json per country) from the MIT-licensed `holidays` library
(github.com/vacanza/holidays). The app downloads them from aiity.de/day/holidays/.

    python3 -I holidays-data.py --lib DIR_WITH_THE_LIBRARY --out DIR

Public holidays only: last year to three years ahead. `regions` null means nationwide; "workday" entries are weekend
days worked in exchange (China, for one)."""
import argparse
import datetime
import json
import os
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--lib", required=True)
parser.add_argument("--out", required=True)
args = parser.parse_args()
sys.path.insert(0, os.path.abspath(args.lib))
import holidays  # noqa: E402

THIS_YEAR = datetime.date.today().year
YEARS = range(THIS_YEAR - 1, THIS_YEAR + 4)


def words(name):
    return re.sub(r"(?<=[a-z])(?=[A-Z])", " ", name)


def calendar(code, subdiv=None, language=None):
    return holidays.country_holidays(code, subdiv=subdiv, years=YEARS, language=language)


def named(local, english):
    """(date, local name) -> English name, for one calendar."""
    result = {}
    for day in sorted(local):
        names = local.get_list(day)
        others = english.get_list(day) if english is not None else []
        for position, name in enumerate(names):
            result[(day, name)] = others[position] if len(others) == len(names) else None
    return result


os.makedirs(args.out, exist_ok=True)
countries, failed = [], []
for code, subdivisions in sorted(holidays.list_supported_countries(include_aliases=False).items()):
    if len(code) != 2:
        continue
    try:
        base = calendar(code)
        kind = type(base)
        languages = getattr(kind, "supported_languages", ()) or ()
        native = getattr(kind, "default_language", None)
        english_code = next((l for l in ("en_US", "en_GB") if l in languages), None) or next((l for l in languages if l.startswith("en")), None)

        def read(subdiv):
            local = calendar(code, subdiv, native)
            english = calendar(code, subdiv, english_code) if english_code else None
            return local, named(local, english)

        national_calendar, national = read(None)
        entries = [{"date": day.isoformat(), "name": name, "en": en, "regions": None, "kind": "holiday"}
                   for (day, name), en in national.items()]
        regional, regions = {}, []
        aliases = {}
        for alias, target in (getattr(kind, "subdivisions_aliases", {}) or {}).items():
            if len(alias) > len(aliases.get(target, "")):
                aliases[target] = alias
        for sub in subdivisions:
            try:
                _, own = read(sub)
            except Exception as error:  # one broken region doesn't cost the country
                failed.append(f"{code}-{sub}: {error}")
                continue
            regions.append({"code": f"{code}-{sub}", "name": aliases.get(sub, sub)})
            for key, en in own.items():
                if key not in national:
                    regional.setdefault(key, (en, []))[1].append(f"{code}-{sub}")
        entries += [{"date": day.isoformat(), "name": name, "en": en, "regions": codes, "kind": "holiday"}
                    for (day, name), (en, codes) in regional.items()]
        for day in sorted(getattr(national_calendar, "weekend_workdays", set()) or set()):
            if day.year in YEARS:
                entries.append({"date": day.isoformat(), "name": "调休上班" if code == "CN" else "Working day",
                                "en": "Make-up working day", "regions": None, "kind": "workday"})
        if not entries:
            continue
        entries.sort(key=lambda e: (e["date"], e["name"], e["regions"] or []))
        document = {"version": 1, "country": code, "generated": datetime.date.today().isoformat(), "holidays": entries}
        with open(os.path.join(args.out, f"{code}.json"), "w", encoding="utf-8") as file:
            json.dump(document, file, ensure_ascii=False, separators=(",", ":"))
        countries.append({"code": code, "name": words(kind.__name__), "regions": sorted(regions, key=lambda r: r["name"])})
    except Exception as error:
        failed.append(f"{code}: {error}")

with open(os.path.join(args.out, "index.json"), "w", encoding="utf-8") as file:
    json.dump({"version": 1, "source": f"github.com/vacanza/holidays {holidays.__version__} (MIT)", "countries": countries},
              file, ensure_ascii=False, separators=(",", ":"))
license_file = os.path.join(os.path.dirname(holidays.__file__), "..", f"holidays-{holidays.__version__}.dist-info", "licenses", "LICENSE")
if os.path.exists(license_file):
    with open(license_file, encoding="utf-8") as source, open(os.path.join(args.out, "LICENSE.txt"), "w", encoding="utf-8") as target:
        target.write(source.read())
print(len(countries), "countries written,", len(failed), "problems")
for line in failed[:10]:
    print(" ", line)
