import pandas as pd
import numpy as np
import requests
import json
import subprocess
from pathlib import Path

# Project base path
BASE_DIR = Path(r"C:\blue\drive-download-20260902T170546Z-1-001")
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# Ensure output directories exist
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("BLUESTOCK FINTECH - CAPSTONE PROJECT")
print("Day 1: Data Ingestion & Project Setup")
print("=" * 60)

# ============================================================
# Task 1: Project folder structure already created above
# ============================================================
print("\n[Task 1] Project folder structure created:")
print("  - data/raw/      : Raw downloaded files")
print("  - data/processed/ : Cleaned, merged CSVs")
print("  - notebooks/     : EDA and analytics notebooks")
print("  - scripts/       : ETL and compute scripts")
print("  - dashboard/     : Power BI / Tableau dashboard")
print("  - reports/       : Final report and presentations")

# ============================================================
# Task 2: Install dependencies
# ============================================================
print("\n[Task 2] Installing dependencies...")
packages = ["pandas", "numpy", "matplotlib", "seaborn", "plotly", "sqlalchemy"]
for pkg in packages:
    try:
        __import__(pkg)
        print(f"  {pkg} - already installed")
    except ImportError:
        print(f"  Installing {pkg}...")
        subprocess.check_call([ "python", "-m", "pip", "install", pkg, "-q"])
print("  Dependencies installed complete")

# ============================================================
# Task 3: Load all 10 CSV datasets
# ============================================================
print("\n[Task 3] Loading all 10 CSV datasets...")

csv_files = [
    "01_fund_master.csv",
    "02_nav_history.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "07_scheme_performance.csv",
    "08_investor_transactions.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv"
]

dfs = {}
for i, fname in enumerate(csv_files, 1):
    fpath = BASE_DIR / fname
    df = pd.read_csv(fpath)
    dfs[fname] = df
    print(f"  {i}. {fname}: {df.shape[0]} rows x {df.shape[1]} columns")
    # Print column names for verification
    cols = list(df.columns)
    print(f"     Columns: {cols[:8]}{'...' if len(cols) > 8 else ''}")

# ============================================================
# Task 4: Fetch live NAV from mfapi.in
# ============================================================
print("\n[Task 4] Fetching live NAV from mfapi.in API...")

# HDFC Top 100 (AMFI code 125497) as anchor
scheme_codes = {
    "HDFC_Top_100": "125497",
    "SBI_Bluechip": "119551",
    "ICICI_Bluechip": "120503",
    "Nippon_Large_Cap": "118632",
    "Axis_Bluechip": "119092",
    "Kotak_Bluechip": "120841"
}

for name, code in scheme_codes.items():
    url = f"https://api.mfapi.in/mf/{code}"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            # Extract NAV history
            if "data" in data and len(data["data"]) > 0:
                nav_data = []
                for entry in data["data"]:
                    nav_data.append({
                        "date": entry.get("navDate", ""),
                        "nav": float(entry.get("nav", 0))
                    })
                df_nav = pd.DataFrame(nav_data)
                df_nav.to_csv(RAW_DIR / f"live_nav_{name}.csv", index=False)
                print(f"  [OK] Fetched {name} ({code}): {df_nav.shape[0]} NAV records")
            else:
                print(f"  [FAIL] {name}: No data found in API response")
        else:
            print(f"  [FAIL] {name}: HTTP {response.status_code}")
    except Exception as e:
        print(f"  [FAIL] {name}: Error - {e}")

# ============================================================
# Task 5: Fetch NAV for 5 specific schemes
# ============================================================
print("\n[Task 5] Fetching NAV for 5 selected schemes...")
scheme_codes_5 = {
    "SBI_Bluechip": "119551",
    "ICICI_Bluechip": "120503",
    "Nippon_Large_Cap": "118632",
    "Axis_Bluechip": "119092",
    "Kotak_Bluechip": "120841"
}

for name, code in scheme_codes_5.items():
    url = f"https://api.mfapi.in/mf/{code}"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if "data" in data and len(data["data"]) > 0:
                nav_data = []
                for entry in data["data"]:
                    nav_data.append({
                        "date": entry.get("navDate", ""),
                        "nav": float(entry.get("nav", 0))
                    })
                df_nav = pd.DataFrame(nav_data)
                df_nav.to_csv(RAW_DIR / f"live_nav_{name}.csv", index=False)
                print(f"  [OK] {name} ({code}): {df_nav.shape[0]} NAV records")
        else:
            print(f"  [FAIL] {name}: HTTP {response.status_code}")
    except Exception as e:
        print(f"  [FAIL] {name}: Error - {e}")

# ============================================================
# Task 6: Understand fund master
# ============================================================
print("\n[Task 6] Understanding fund master dataset...")
fund_master = dfs["01_fund_master.csv"]
print(f"  Unique fund houses: {fund_master['fund_house'].nunique()}")
print(f"  Unique categories: {list(fund_master['category'].unique())}")
print(f"  Unique sub-categories: {list(fund_master['sub_category'].unique())}")
print(f"  Unique risk categories: {list(fund_master['risk_category'].unique())}")
print(f"  Expense ratio range: {fund_master['expense_ratio_pct'].min():.2f}% - {fund_master['expense_ratio_pct'].max():.2f}%")
print(f"  Fund managers represented: {fund_master['fund_manager'].nunique()}")

# ============================================================
# Task 7: Validate AMFI codes
# ============================================================
print("\n[Task 7] Validating AMFI codes between fund_master and nav_history...")
nav_history = dfs["02_nav_history.csv"]
fund_codes = set(fund_master["amfi_code"].unique())
nav_codes = set(nav_history["amfi_code"].unique())

codes_in_master_not_nav = fund_codes - nav_codes
codes_in_nav_not_master = nav_codes - fund_codes

print(f"  Codes in fund_master but NOT in nav_history: {len(codes_in_master_not_nav)}")
print(f"  Codes in nav_history but NOT in fund_master: {len(codes_in_nav_not_master)}")

if len(codes_in_master_not_nav) == 0 and len(codes_in_nav_not_master) == 0:
    print("  [OK] All AMFI codes match between datasets")
else:
    if codes_in_master_not_nav:
        print(f"  Sample missing codes: {list(codes_in_master_not_nav)[:5]}")
    if codes_in_nav_not_master:
        print(f"  Sample extra codes: {list(codes_in_nav_not_master)[:5]}")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("DAY 1 COMPLETE: Data Ingestion & Project Setup")
print("=" * 60)
print(f"\nRaw CSV files loaded: {len(dfs)} datasets")
print(f"Live NAV data fetched from mfapi.in for 6 schemes")
print(f"Fund master: {fund_master.shape[0]} schemes analyzed")
print(f"Validation: AMFI code consistency checked")
print(f"\nOutput files stored in:")
print(f"  - {RAW_DIR}/ : Raw data and live NAV CSVs")
print(f"  - {PROCESSED_DIR}/ : Will hold cleaned data")
print("=" * 60)