"""
Script 02 - Pull SEDS Data via bulk ZIP download (1960-present)
No API key needed - pulls directly from EIA's public bulk file

Note: the MSN codes in this bulk file are truncated (e.g. TERCB, not TERCBUS)
and the state column is named "State", not "StateCode".
"""

import requests
import pandas as pd
import zipfile
import io

OUTPUT_PATH = r"C:\Users\bryce\Desktop\Data Projects\Side Projects\Energy Consumption Analysis\data\raw\seds_residential.csv"

ZIP_URL = "https://www.eia.gov/state/seds/sep_use/total/csv/use_all_btu.zip"

# Truncated MSN codes as they appear in this specific bulk file
TARGET_MSNS = {
    "TERCB": "total_res_trillion_btu",
    "ESRCB": "electricity_res_trillion_btu",
    "NGRCB": "natgas_res_trillion_btu",
    "PARCB": "petroleum_res_trillion_btu",
}

print("Downloading SEDS bulk ZIP...")
headers = {"User-Agent": "Mozilla/5.0"}
r = requests.get(ZIP_URL, headers=headers, timeout=60)
r.raise_for_status()

z = zipfile.ZipFile(io.BytesIO(r.content))
csv_filename = [f for f in z.namelist() if f.endswith('.csv')][0]
df_raw = pd.read_csv(z.open(csv_filename))

# Clean whitespace
df_raw["State"] = df_raw["State"].str.strip()
df_raw["MSN"] = df_raw["MSN"].str.strip()

# Filter to US national totals + our target fuel-type series
df_us = df_raw[
    (df_raw["State"] == "US") &
    (df_raw["MSN"].isin(TARGET_MSNS.keys()))
].copy()

print(f"Filtered rows: {len(df_us)}")

# Melt wide (year columns) to long format
year_cols = [c for c in df_us.columns if c.isdigit()]
df_melted = df_us.melt(
    id_vars=["MSN"],
    value_vars=year_cols,
    var_name="year",
    value_name="value"
)
df_melted["year"] = df_melted["year"].astype(int)
df_melted["value"] = pd.to_numeric(df_melted["value"], errors="coerce")
df_melted["MSN"] = df_melted["MSN"].map(TARGET_MSNS)

# Pivot so each fuel type is its own column
df_pivot = df_melted.pivot_table(
    index="year", columns="MSN", values="value"
).reset_index()
df_pivot.columns.name = None
df_pivot = df_pivot.sort_values("year")
df_pivot = df_pivot.dropna(subset=["total_res_trillion_btu"])

print(f"\nFinal shape: {df_pivot.shape}")
print(f"Years: {df_pivot['year'].min()} - {df_pivot['year'].max()}")
print(df_pivot.head(10))

df_pivot.to_csv(OUTPUT_PATH, index=False)
print(f"\nSaved to {OUTPUT_PATH}")
