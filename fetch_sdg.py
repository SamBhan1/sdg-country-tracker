"""Fetch headline SDG indicators for every country from the UN SDG Global Database
(https://unstats.un.org/sdgapi) and write them as one tidy CSV for the dashboard.

Run:  python fetch_sdg.py      ->  data/sdg_indicators.csv, data/indicators.csv, data/countries.csv
      python fetch_sdg.py hunger internet   (re-fetch only those indicators)
"""
import csv
import json
import os
import sys
import urllib.request

API = "https://unstats.un.org/sdgapi/v1/sdg"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# id, series code, goal, short name, unit, better ("higher"/"lower"), allowed dimension values
INDICATORS = [
    ("poverty", "SI_POV_DAY1", 1, "Extreme poverty", "% of population", "lower",
     {"Age": {"ALLAGE"}, "Sex": {"BOTHSEX"}, "Location": {"ALLAREA"}}),
    ("hunger", "SN_ITK_DEFC", 2, "Undernourishment", "% of population", "lower",
     {"Age": {"ALLAGE"}, "Sex": {"BOTHSEX"}}),
    ("child_mortality", "SH_DYN_MORT", 3, "Under-5 mortality", "deaths per 1,000 live births", "lower",
     {"Sex": {"BOTHSEX"}}),
    ("school_completion", "SE_TOT_CPLR", 4, "Lower-secondary completion", "% of age group", "higher",
     {"Education level": {"LOWSEC"}, "Sex": {"BOTHSEX"}, "Location": {"ALLAREA"}, "Quantile": {"_T"}}),
    ("women_parliament", "SG_GEN_PARL", 5, "Women in parliament", "% of seats", "higher", {}),
    ("safe_water", "SH_H2O_SAFE", 6, "Safely managed drinking water", "% of population", "higher",
     {"Location": {"ALLAREA"}}),
    ("electricity", "EG_ACS_ELEC", 7, "Access to electricity", "% of population", "higher",
     {"Location": {"ALLAREA"}}),
    ("unemployment", "SL_TLF_UEM", 8, "Unemployment", "% of labour force (15+)", "lower",
     {"Age": {"15+"}, "Sex": {"BOTHSEX"}}),
    ("internet", "IT_USE_ii99", 9, "Internet use", "% of population", "higher",
     {"Age": {"ALLAGE"}, "Sex": {"BOTHSEX"}, "Units": {"PERCENT"}}),
]


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "sdg-dashboard-script"}), timeout=300) as r:
        return json.load(r)


def countries():
    """Countries with their SDG region, from the API's geographic tree."""
    out = {}
    for world in get(f"{API}/GeoArea/Tree"):
        if world["geoAreaCode"] != 1:
            continue

        def walk(node, sdg_region):
            for ch in node.get("children") or []:
                if ch["type"] == "Country":
                    out[ch["geoAreaCode"]] = (ch["geoAreaName"], sdg_region)
                else:
                    walk(ch, sdg_region or ch["geoAreaName"])

        walk(world, None)
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    geo = countries()
    print(len(geo), "countries")
    rows = []
    only = set(sys.argv[1:])  # optional: re-fetch just these indicator ids, keep the rest
    if only:
        with open(os.path.join(OUT, "sdg_indicators.csv"), encoding="utf-8") as f:
            rows = [r for r in csv.DictReader(f) if r["indicator"] not in only]
    for ind_id, code, goal, name, unit, better, allowed in INDICATORS:
        if only and ind_id not in only:
            continue
        data, page = [], 1
        while True:
            d = get(f"{API}/Series/Data?seriesCode={code}&pageSize=20000&page={page}")
            data += d["data"]
            if page >= d["totalPages"]:
                break
            page += 1
        best = {}  # (area, year) -> (priority, value)
        for r in data:
            area = int(r["geoAreaCode"])
            if area not in geo and area != 1:
                continue
            dims = {**r["dimensions"], **r["attributes"]}
            if any(k in dims and dims[k] not in v for k, v in allowed.items()):
                continue
            try:
                val = float(r["value"])
            except (TypeError, ValueError):
                continue
            year = int(r["timePeriodStart"])
            prio = 0 if dims.get("Reporting Type") == "G" else 1
            key = (area, year)
            if key not in best or prio < best[key][0]:
                best[key] = (prio, val)
        for (area, year), (_, val) in best.items():
            cname = "World" if area == 1 else geo[area][0]
            rows.append({"indicator": ind_id, "m49": area, "country": cname, "year": year, "value": round(val, 2)})
        print(f"{code}: {len(data)} raw -> {len(best)} kept")

    rows.sort(key=lambda r: (r["indicator"], r["country"], int(r["year"])))
    with open(os.path.join(OUT, "sdg_indicators.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["indicator", "m49", "country", "year", "value"])
        w.writeheader()
        w.writerows(rows)

    with open(os.path.join(OUT, "indicators.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["indicator", "series", "goal", "name", "unit", "better"])
        for ind_id, code, goal, name, unit, better, _ in INDICATORS:
            w.writerow([ind_id, code, goal, name, unit, better])

    with open(os.path.join(OUT, "countries.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["m49", "country", "sdg_region"])
        for m49, (n, reg) in sorted(geo.items(), key=lambda kv: kv[1][0]):
            w.writerow([m49, n, reg])
    print(len(rows), "rows written")


if __name__ == "__main__":
    main()
