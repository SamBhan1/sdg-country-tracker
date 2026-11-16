# SDG Country Tracker

Track how any country is doing on the UN Sustainable Development Goals (SDGs), and compare it with another country and the world.

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

## The dashboard

For the chosen country it shows:

- a one-line summary of how many indicators have improved or slipped since 2015, when the Goals were adopted
- a card per indicator with the latest value, change since 2015, the world figure and the share of countries it is ahead of
- a trend chart against the world average and a comparison country
- a head-to-head table of two countries across all nine indicators

`dashboard/index.html` is the dashboard's page source. It runs inside a Claude data dashboard artifact, which supplies the `dash` runtime and d3, so it won't open on its own in a browser. The data files and script work anywhere.

## Data files

All in `data/`:

| File | Contents |
|---|---|
| `sdg_indicators.csv` | `indicator, m49, country, year, value`: about 35,000 yearly values. `m49 = 1` is the World total. |
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
- **Non-numeric values are dropped,** for example undernourishment reported as `<2.5`.
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
