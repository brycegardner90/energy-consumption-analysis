"""
Script 03 - Merge & Clean All Data
Joins SEDS (1960-present) + EIA API (2001-present) + Census population
Outputs one clean Power BI/Tableau-ready CSV
"""

import pandas as pd

RAW_SEDS    = r"C:\Users\bryce\Desktop\Data Projects\Side Projects\Energy Consumption Analysis\data\raw\seds_residential.csv"
RAW_API     = r"C:\Users\bryce\Desktop\Data Projects\Side Projects\Energy Consumption Analysis\data\raw\eia_api_electricity.csv"
OUTPUT_PATH = r"C:\Users\bryce\Desktop\Data Projects\Side Projects\Energy Consumption Analysis\data\processed\energy_consumption_final.csv"

# US Population by year - US Census Bureau
population_data = {
    1960: 179323175, 1961: 182992000, 1962: 185771000, 1963: 188483000,
    1964: 191141000, 1965: 193526000, 1966: 195576000, 1967: 197457000,
    1968: 199399000, 1969: 201385000, 1970: 203211926, 1971: 206827000,
    1972: 209284000, 1973: 211357000, 1974: 213342000, 1975: 215465000,
    1976: 217563000, 1977: 219760000, 1978: 222095000, 1979: 224567000,
    1980: 226545805, 1981: 229466000, 1982: 231664000, 1983: 233792000,
    1984: 235825000, 1985: 237924000, 1986: 240133000, 1987: 242289000,
    1988: 244499000, 1989: 246819000, 1990: 248709873, 1991: 252153000,
    1992: 255030000, 1993: 257783000, 1994: 260327000, 1995: 262803000,
    1996: 265229000, 1997: 267784000, 1998: 270248000, 1999: 272691000,
    2000: 281421906, 2001: 284968955, 2002: 287625193, 2003: 290107933,
    2004: 292805298, 2005: 295516599, 2006: 298379912, 2007: 301231207,
    2008: 304093966, 2009: 306771529, 2010: 308745538, 2011: 311591917,
    2012: 313914040, 2013: 316128839, 2014: 318857056, 2015: 320742673,
    2016: 323071342, 2017: 325122128, 2018: 326838199, 2019: 328239523,
    2020: 329484123, 2021: 331893745, 2022: 333271411, 2023: 334914895,
    2024: 336000000,
}

# US Housing Units by year - Census, interpolated for non-census years
housing_units_raw = {
    1960: 58326000, 1965: 63445000, 1970: 68672000, 1975: 77662000,
    1980: 88411000, 1985: 96040000, 1990: 102263000, 1995: 108000000,
    2000: 115904641, 2005: 124377076, 2010: 131704730, 2015: 134141609,
    2020: 140498736, 2021: 141000000, 2022: 142000000, 2023: 143000000,
    2024: 144000000,
}

era_labels = {
    (1960, 1972): "Pre-Crisis Growth",
    (1973, 1979): "Energy Crisis Era",
    (1980, 1994): "Efficiency Standards Begin",
    (1995, 2007): "Digital Age Explosion",
    (2008, 2015): "Post-Recession Efficiency",
    (2016, 2099): "AI & EV Era",
}

def get_era(year):
    for (start, end), label in era_labels.items():
        if start <= year <= end:
            return label
    return "Unknown"

print("Loading SEDS data...")
df_seds = pd.read_csv(RAW_SEDS)

print("Loading EIA API data...")
df_api = pd.read_csv(RAW_API)

df_pop = pd.DataFrame(list(population_data.items()), columns=["year", "population"])

df_housing = pd.DataFrame({"year": range(1960, 2025)})
df_housing = df_housing.merge(
    pd.DataFrame(list(housing_units_raw.items()), columns=["year", "housing_units"]),
    on="year", how="left"
)
df_housing["housing_units"] = df_housing["housing_units"].interpolate(method="linear")

# Merge everything
df = df_seds.merge(df_pop, on="year", how="left")
df = df.merge(df_housing, on="year", how="left")
df = df.merge(df_api, on="year", how="left")

# Calculated fields - trillion BTU -> BTU (x1e12), then normalize
df["total_btu_per_household"]         = (df["total_res_trillion_btu"] * 1e12) / df["housing_units"]
df["electricity_btu_per_household"]   = (df["electricity_res_trillion_btu"] * 1e12) / df["housing_units"]
df["total_mmbtu_per_household"]       = df["total_btu_per_household"] / 1e6
df["electricity_mmbtu_per_household"] = df["electricity_btu_per_household"] / 1e6

df["total_btu_per_capita"]       = (df["total_res_trillion_btu"] * 1e12) / df["population"]
df["electricity_btu_per_capita"] = (df["electricity_res_trillion_btu"] * 1e12) / df["population"]

df["era"] = df["year"].apply(get_era)

final_cols = [
    "year", "era",
    "population", "housing_units",
    "total_res_trillion_btu", "electricity_res_trillion_btu",
    "natgas_res_trillion_btu", "petroleum_res_trillion_btu",
    "total_mmbtu_per_household", "electricity_mmbtu_per_household",
    "total_btu_per_capita", "electricity_btu_per_capita",
    "sales_million_kwh", "price_cents_per_kwh",
]

df_final = df[[c for c in final_cols if c in df.columns]].sort_values("year")

print(f"\nFinal shape: {df_final.shape}")
print(f"Years: {df_final['year'].min()} - {df_final['year'].max()}")
print(df_final.head())

df_final.to_csv(OUTPUT_PATH, index=False)
print(f"\nSaved to {OUTPUT_PATH}")
