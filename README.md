# The Efficiency Paradox: U.S. Residential Energy Consumption, 1960–2024

How much energy does the average American household actually use — and has all the "efficiency" we keep hearing about really moved the needle?

## The Idea

This one started as a peaky curiosity. I kept thinking back to the 1960s and 70s, when energy was cheap and nobody thought twice about leaving the lights on. That ran straight into the oil crisis era, then decades of efficiency standards — better refrigerators, better HVAC, better everything. So the assumption is we should be using way less energy per household today than we were back then.

But at the same time, we've added a ton of new load to the grid that didn't exist in 1970: computers, streaming, smart home devices, EVs charging in the garage, and now AI and data centers pulling serious power behind the scenes. So which force wins? Did the efficiency gains actually stick, or did we just trade old energy use for new energy use?

I wanted to pull the real numbers and find out — not guess, not assume, just look at 60+ years of data and see what the trend actually says.

## What I Found

Household energy consumption peaked hard in the early-to-mid 1970s, right around the oil crisis, then fell off a cliff once efficiency standards kicked in through the 80s and 90s. From there it's been a long, bumpy decline — total residential energy per household is down about 35% from its peak.

But zoom into just the last 20+ years and a different story shows up: electricity consumption per household has barely moved, while the price per kilowatt-hour has climbed 92%. So even in the era of supposedly "smart" and efficient everything, people are paying a lot more to use roughly the same amount of power. That's the paradox — efficiency won the long game, but the savings haven't kept showing up where you'd expect them to in the recent era.

## Tools

| Tool | Role |
|---|---|
| Python (pandas, requests) | API/bulk data pulls, cleaning, merging |
| EIA API v2 | Electricity retail sales & price data (2001–2024) |
| EIA SEDS bulk data | Residential energy by fuel type (1960–2024) |
| Power BI Desktop | Dashboard build, DAX measures |
| US Census data | Population & housing unit normalization |

## Methodology

Three Python scripts handle the pipeline:

1. **EIA API pull** — grabs national residential electricity sales (million kWh) and average price (¢/kWh), annual, 2001–2024.
2. **SEDS bulk pull** — downloads EIA's State Energy Data System ZIP directly (no API key needed for this one) and extracts US-level residential consumption by fuel type — electricity, natural gas, and petroleum — going all the way back to 1960.
3. **Merge & clean** — joins both datasets together, layers in Census population and housing unit figures, and calculates the per-household and per-capita metrics that actually make the numbers comparable across 64 years of population growth. Also tags every year with an "era" label (Energy Crisis, Efficiency Standards Begin, Digital Age Explosion, AI & EV Era, etc.) for context.

## Dashboards

**Dashboard 1 — The Efficiency Paradox**
The headline arc: total residential energy use per household from 1960–2024, with the fuel-type breakdown (electricity, natural gas, petroleum) stacked underneath to show how the energy mix shifted over time. Peak, latest, and percent decline called out directly.

**Dashboard 2 — The Price of Standing Still**
Zooms into the modern era, 2001–2024, where price data actually exists. A dual-axis line chart puts electricity consumption per household next to price per kWh — consumption is essentially flat, price is not. Total electricity sales volume sits underneath for context.

## Key Findings

- Peak household energy consumption: ~197K MMBtu (early-to-mid 1970s)
- Latest (2024): ~128K MMBtu — a 35% decline from peak
- Electricity price per kWh: up 92% since 2001 (8.58¢ → 16.48¢)
- Electricity consumption per household over that same window: virtually flat (+1%)

## What I Learned as an Analyst

EIA's public data is genuinely messy to work with — the API and the bulk file formats don't always agree with each other, MSN codes get silently truncated, and column names shift between datasets that are supposedly part of the same system. A lot of this project was less about the visualization and more about being stubborn enough to keep tracing errors back to their root instead of settling for a workaround. That persistence is its own kind of analyst skill.

The other thing I took away is how much normalization matters. Raw consumption totals go up almost every year just because the country has more people and more houses — that's not a story, that's just population growth. Per-household and per-capita framing is what turns a pile of numbers into something that actually means something.

## Files

| File | Description |
|---|---|
| `py/01_pull_eia_api.py` | Pulls electricity sales & price from EIA API |
| `py/02_pull_seds.py` | Pulls residential energy by fuel type from SEDS bulk file |
| `py/03_merge_clean.py` | Merges, normalizes, and outputs the final dataset |
| `csv/energy_consumption_final.csv` | Final Tableau/Power BI-ready dataset, 1960–2024 |
| `Energy_Consumption_Analysis.pbix` | Power BI dashboard file |
| `screenshots/dashboard-1-the-long-arc.png` | Dashboard 1 screenshot |
| `screenshots/dashboard-2-the-price-of-standing-still.png` | Dashboard 2 screenshot |

## Connect

- [LinkedIn](https://www.linkedin.com/in/bryce-gardner-16a889183)
- [GitHub](https://github.com/brycegardner90)
- Related project: [Southeast AC & Population Boom](https://github.com/brycegardner90/southeast-ac-population-boom)
