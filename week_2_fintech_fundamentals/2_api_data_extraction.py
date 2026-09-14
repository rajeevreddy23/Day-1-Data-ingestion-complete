"""
Bluestock Fintech - Week 2: FinTech Domain and Software Fundamentals
Deliverable 3: REST API Ingestion, JSON Inspection and CSV Transformation Engine
"""

import json
import requests
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

print("=" * 75)
print("BLUESTOCK FINTECH - REST API AND JSON DATA EXTRACTION TASK")
print("=" * 75)

# Target Endpoint: Public Financial Market API
API_URL = "https://api.mfapi.in/mf/125497"
print(f"\n[1] Initiating HTTP GET request to: {API_URL}")

headers = {"User-Agent": "Bluestock-Fintech-Analyst/1.0"}
response = requests.get(API_URL, headers=headers, timeout=15)

print(f"  HTTP Status Code : {response.status_code} ({response.reason})")
print(f"  Content-Type     : {response.headers.get('Content-Type')}")

if response.status_code == 200:
    data = response.json()
    
    # Save raw JSON inspection sample
    json_path = BASE_DIR / "api_response_sample.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"\n[2] Raw JSON Response saved to: {json_path.name}")
    
    # Inspect JSON Architecture
    meta = data.get("meta", {})
    records = data.get("data", [])
    
    print("\n[3] JSON Schema Inspection:")
    print(f"  - Top-Level Keys : {list(data.keys())}")
    print(f"  - Fund House     : {meta.get('fund_house')}")
    print(f"  - Scheme Name    : {meta.get('scheme_name')}")
    print(f"  - Scheme Type    : {meta.get('scheme_type')}")
    print(f"  - Scheme Category: {meta.get('scheme_category')}")
    print(f"  - Total Records  : {len(records)} daily observations")
    
    # Transform to Pandas DataFrame
    print("\n[4] Converting JSON records to Pandas DataFrame...")
    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
    df["nav"] = pd.to_numeric(df["nav"])
    df = df.sort_values("date").reset_index(drop=True)
    
    # Feature Engineering for Financial Analysis
    df["daily_return_pct"] = df["nav"].pct_change() * 100
    df["7d_moving_avg"] = df["nav"].rolling(7).mean()
    df["30d_moving_avg"] = df["nav"].rolling(30).mean()
    
    # Save to CSV
    csv_path = BASE_DIR / "api_extracted_data.csv"
    df.to_csv(csv_path, index=False)
    print(f"  [OK] Exported cleaned dataset to: {csv_path.name} ({len(df)} rows)")
    
    # Dataset Profiling and Statistical Highlights
    print("\n[5] Data Profiling and Statistical Highlights:")
    print(f"  - Time Horizon   : {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
    print(f"  - Minimum NAV    : INR {df['nav'].min():.4f}")
    print(f"  - Maximum NAV    : INR {df['nav'].max():.4f}")
    print(f"  - Latest NAV     : INR {df['nav'].iloc[-1]:.4f}")
    print(f"  - Total Return   : {((df['nav'].iloc[-1] / df['nav'].iloc[0]) - 1) * 100:.2f}%")
    print(f"  - Null Values    : {df.isnull().sum().to_dict()}")
    
    print("\n[6] Sample Data (First 3 rows):")
    print(df.head(3).to_string(index=False))

print("\n" + "=" * 75)
print("API EXTRACTION AND CSV CONVERSION COMPLETED SUCCESSFULLY!")
print("=" * 75)
