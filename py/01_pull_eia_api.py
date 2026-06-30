"""
Script 01 - Pull EIA API Data
Pulls residential electricity retail sales (kWh) and price (cents/kWh)
national level, annual, 2001-present
"""

import requests
import pandas as pd

API_KEY = "YOUR_EIA_API_KEY"  # Get yours free at https://www.eia.gov/opendata/
BASE_URL = "https://api.eia.gov/v2/electricity/retail-sales/data"
OUTPUT_PATH = r"C:\Users\bryce\Desktop\Data Projects\Side Projects\Energy Consumption Analysis\data\raw\eia_api_electricity.csv"

def fetch_eia(metric):
    """Fetch a single metric (sales or price) for US residential, annual."""
    params = {
        "api_key": API_KEY,
        "data[0]": metric,
        "facets[sectorid][]": "RES",
        "facets[stateid][]": "US",
        "frequency": "annual",
        "sort[0][column]": "period",
        "sort[0][direction]": "asc",
        "length": 5000,
    }
    r = requests.get(BASE_URL, params=params)
    r.raise_for_status()
    data = r.json()["response"]["data"]
    df = pd.DataFrame(data)
    df = df[["period", metric]].rename(columns={"period": "year"})
    df["year"] = df["year"].astype(int)
    df[metric] = pd.to_numeric(df[metric], errors="coerce")
    return df

print("Fetching electricity sales...")
df_sales = fetch_eia("sales")

print("Fetching electricity price...")
df_price = fetch_eia("price")

# Merge sales and price
df = df_sales.merge(df_price, on="year")
df.columns = ["year", "sales_million_kwh", "price_cents_per_kwh"]

print(df.head())
print(f"\nRows: {len(df)} | Years: {df['year'].min()} - {df['year'].max()}")

df.to_csv(OUTPUT_PATH, index=False)
print(f"Saved to {OUTPUT_PATH}")
