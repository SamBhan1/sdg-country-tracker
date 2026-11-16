# SDG Country Tracker

Track how any country is doing on the UN Sustainable Development Goals (SDGs), and compare it with another country and the world.

**Live site: <https://sambhan1.github.io/sdg-country-tracker/>**

This project downloads nine headline SDG indicators for every country from the official **UN SDG Global Database** and turns them into one tidy dataset, plus an interactive dashboard built on it.

> Independent project built on public UN data. It is not an official United Nations product and is not endorsed by the UN.

## What's tracked

| Goal | Indicator | UN series | Unit | Better when |
|---|---|---|---|---|
| 1 · No poverty | Extreme poverty | `SI_POV_DAY1` | % of people under $2.15 a day | lower |
| 2 · Zero hunger | Undernourishment | `SN_ITK_DEFC` | % of people | lower |
| 3 · Good health | Under-5 mortality | `SH_DYN_MORT` | deaths per 1,000 live births | lower |
| 4 · Quality education | Lower-secondary completion | `SE_TOT_CPLR` | % of age group | higher |
| 5 · Gender equality | Women in parliament | `SG_GEN_PARL` | % of seats | higher |
| 6 · Clean water | Safely managed drinking water | `SH_H2O_SAFE` | % of people | higher |
| 7 · Clean energy | Access to electricity | `EG_ACS_ELEC` | % of people | higher |
| 8 · Decent work | Unemployment | `SL_TLF_UEM` | % of labour force aged 15+ | lower |
| 9 · Infrastructure | Internet use | `IT_USE_ii99` | % of people | higher |

## The site

`index.html` is a single-page site, served by GitHub Pages straight from this repo. For the chosen country it shows:

- a world map coloured by the chosen indicator; select any country to open it
- a one-line summary of how many indicators have improved or slipped since 2015, when the Goals were adopted
- a card per indicator with the latest value, change since 2015, the world figure and the share of countries it is ahead of
- a trend chart against the world average and a comparison country
- a head-to-head table of two countries across all nine indicators

The address keeps the current view, so a link such as `#c=India&vs=Brazil&i=internet` opens that exact comparison.

To run it on your own computer, serve the folder and open <http://localhost:8000>:

```bash
python -m http.server 8000
```

It uses [D3](https://d3js.org) and country shapes from [world-atlas](https://github.com/topojson/world-atlas) (Natural Earth), both loaded from a CDN.

`dashboard/index.html` is an earlier version of the same page written for a Claude data dashboard. It needs that dashboard's runtime and won't open on its own.

## Data files

All in `data/`:

| File | Contents |
|---|---|
| `sdg_indicators.csv` | `indicator, m49, country, year, value`: about 34,000 yearly values. `m49 = 1` is the World total. |
| `indicators.csv` | The nine indicators: goal, UN series code, name, unit, and whether higher or lower is better. |
| `countries.csv` | Every country with its M49 code and SDG region. |

## Refresh the data

Requires Python 3.8+ with no extra packages.

```bash
python fetch_sdg.py                    # everything (about 15–20 minutes)
python fetch_sdg.py hunger internet    # only these indicators; keeps the rest
```

The script calls `https://unstats.un.org/sdgapi/v1/sdg`. The UN updates most series about once a year.

## How the numbers are processed

- **National totals only:** both sexes, all ages, urban and rural combined. Unemployment uses ages 15+, and school completion uses lower secondary.
- **Comparable estimates first:** where a year has both a country's own figure and the UN's globally comparable estimate, the comparable estimate is used.
- **Non-numeric values are dropped,** for example undernourishment reported as `<2.5` or `NaN`.
- **"Since 2015"** compares the latest value with the first value from 2015 or later.

## Limitations

- Many values are modelled estimates by UN agencies, not direct counts.
- Coverage varies widely. Some countries haven't reported some indicators for years, and the latest year differs by country.
- This is a snapshot, last downloaded in November 2026.

For research, policy or journalism, check key figures against the official portal: <https://unstats.un.org/sdgs/dataportal>.

## Source and credit

Data: **UN SDG Global Database, United Nations Statistics Division** (<https://unstats.un.org/sdgs/dataportal>), accessed November 2026. The data remains subject to the UN's own terms of use. The MIT license below covers only this project's code.

## License

Code is released under the [MIT License](LICENSE).
