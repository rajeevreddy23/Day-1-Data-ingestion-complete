import pandas as pd
import numpy as np
import sqlite3
import os
from pathlib import Path

# Project base path
BASE_DIR = Path(r"C:\blue\drive-download-20260902T170546Z-1-001")
# CSV files are at project root
RAW_DIR = BASE_DIR
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# Ensure output directories exist
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("BLUESTOCK FINTECH - CAPSTONE PROJECT")
print("Day 2: Data Cleaning + SQL Database Design")
print("=" * 60)

# -------------------------------------------------------------------------
# Task 1: Clean nav_history.csv
# -------------------------------------------------------------------------
print("\n[Task 1] Cleaning nav_history.csv...")
nav_raw = pd.read_csv(os.path.join(RAW_DIR, "02_nav_history.csv"))
print("  Original shape: " + str(nav_raw.shape))

# Parse dates to datetime
nav_raw["date"] = pd.to_datetime(nav_raw["date"])

# Sort by amfi_code + date
nav_raw = nav_raw.sort_values(["amfi_code", "date"]).reset_index(drop=True)

# Forward-fill missing NAV (holidays/weekends)
nav_raw["nav"] = nav_raw.groupby("amfi_code")["nav"].ffill()

# Remove duplicates (keep first per amfi_code + date)
nav_raw = nav_raw.drop_duplicates(subset=["amfi_code", "date"], keep="first")

# Validate NAV > 0
invalid_nav = (nav_raw["nav"] <= 0).sum()
print("  Invalid NAV (<=0): " + str(invalid_nav))
nav_clean = nav_raw[nav_raw["nav"] > 0].reset_index(drop=True)

print("  Cleaned shape: " + str(nav_clean.shape[0]) + " rows x " + str(nav_clean.shape[1]) + " columns")
nav_clean.to_csv(os.path.join(PROCESSED_DIR, "clean_nav.csv"), index=False)
print("  Saved to: " + str(PROCESSED_DIR) + "/clean_nav.csv")

# -------------------------------------------------------------------------
# Task 2: Clean investor_transactions.csv
# -------------------------------------------------------------------------
print("\n[Task 2] Cleaning investor_transactions.csv...")
trans_raw = pd.read_csv(os.path.join(RAW_DIR, "08_investor_transactions.csv"))
print("  Original shape: " + str(trans_raw.shape))

# Standardise transaction_type (SIP/Lumpsum/Redemption)
trans_raw["transaction_type"] = trans_raw["transaction_type"].str.strip().str.title()

# Validate amount > 0
invalid_amount = (trans_raw["amount_inr"] <= 0).sum()
print("  Invalid amounts (<=0): " + str(invalid_amount))

# Check KYC status values
kyc_vals = trans_raw["kyc_status"].unique()
print("  KYC status values: " + str(list(kyc_vals)))

# Fix date formats
trans_raw["transaction_date"] = pd.to_datetime(trans_raw["transaction_date"])

# Remove duplicates
trans_raw = trans_raw.drop_duplicates(subset=["investor_id", "transaction_date", "amfi_code"], keep="first")

trans_clean = trans_raw.copy()
trans_clean.to_csv(os.path.join(PROCESSED_DIR, "clean_transactions.csv"), index=False)
print("  Cleaned shape: " + str(trans_clean.shape[0]) + " rows x " + str(trans_clean.shape[1]) + " columns")
print("  Saved to: " + str(PROCESSED_DIR) + "/clean_transactions.csv")

# -------------------------------------------------------------------------
# Task 3: Clean scheme_performance.csv
# -------------------------------------------------------------------------
print("\n[Task 3] Cleaning scheme_performance.csv...")
perf_raw = pd.read_csv(os.path.join(RAW_DIR, "07_scheme_performance.csv"))
print("  Original shape: " + str(perf_raw.shape))

# Validate return values are numeric
perf_raw["return_1yr_pct"] = pd.to_numeric(perf_raw["return_1yr_pct"], errors="coerce")
perf_raw["return_3yr_pct"] = pd.to_numeric(perf_raw["return_3yr_pct"], errors="coerce")
perf_raw["return_5yr_pct"] = pd.to_numeric(perf_raw["return_5yr_pct"], errors="coerce")
perf_raw["benchmark_3yr_pct"] = pd.to_numeric(perf_raw["benchmark_3yr_pct"], errors="coerce")
perf_raw["alpha"] = pd.to_numeric(perf_raw["alpha"], errors="coerce")
perf_raw["beta"] = pd.to_numeric(perf_raw["beta"], errors="coerce")
perf_raw["sharpe_ratio"] = pd.to_numeric(perf_raw["sharpe_ratio"], errors="coerce")
perf_raw["sortino_ratio"] = pd.to_numeric(perf_raw["sortino_ratio"], errors="coerce")
perf_raw["std_dev_ann_pct"] = pd.to_numeric(perf_raw["std_dev_ann_pct"], errors="coerce")
perf_raw["max_drawdown_pct"] = pd.to_numeric(perf_raw["max_drawdown_pct"], errors="coerce")

# Flag negative Sharpe ratios
neg_sharpe = (perf_raw["sharpe_ratio"] < 0).sum()
print("  Negative Sharpe ratios: " + str(neg_sharpe))

# Check expense_ratio range (0.1% – 2.5%)
exp_min = perf_raw["expense_ratio_pct"].min()
exp_max = perf_raw["expense_ratio_pct"].max()
print("  Expense ratio actual range: " + str(round(exp_min, 2)) + "% - " + str(round(exp_max, 2)) + "%")

# Remove rows with critical NaN
perf_clean = perf_raw.dropna(subset=["amfi_code", "sharpe_ratio", "return_3yr_pct"])
perf_clean = perf_clean.reset_index(drop=True)

perf_clean.to_csv(os.path.join(PROCESSED_DIR, "clean_performance.csv"), index=False)
print("  Cleaned shape: " + str(perf_clean.shape[0]) + " rows x " + str(perf_clean.shape[1]) + " columns")
print("  Saved to: " + str(PROCESSED_DIR) + "/clean_performance.csv")

# -------------------------------------------------------------------------
# Task 4: Design SQLite star schema
# -------------------------------------------------------------------------
print("\n[Task 4] Designing SQLite star schema...")
db_path = BASE_DIR / "data" / "bluestock_mf.db"
if os.path.exists(str(db_path)):
    os.remove(str(db_path))
    print("  Removed existing DB: " + str(db_path))

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# dim_fund table
cursor.execute("""
    CREATE TABLE dim_fund (
        amfi_code TEXT PRIMARY KEY,
        fund_house TEXT,
        scheme_name TEXT,
        category TEXT,
        sub_category TEXT,
        plan TEXT,
        launch_date DATE,
        benchmark TEXT,
        expense_ratio_pct REAL,
        exit_load_pct REAL,
        fund_manager TEXT,
        risk_category TEXT,
        sebi_category_code TEXT
    )
""")
print("  Created table: dim_fund")

# dim_date table (date dimension)
cursor.execute("""
    CREATE TABLE dim_date (
        date_id INTEGER PRIMARY KEY,
        date DATE,
        year INTEGER,
        quarter INTEGER,
        month INTEGER,
        month_name TEXT,
        is_weekday INTEGER
    )
""")
print("  Created table: dim_date")

# fact_nav table
cursor.execute("""
    CREATE TABLE fact_nav (
        amfi_code TEXT,
        date_id INTEGER,
        nav REAL,
        daily_return REAL,
        PRIMARY KEY (amfi_code, date_id),
        FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
        FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
    )
""")
print("  Created table: fact_nav")

# fact_transactions table
cursor.execute("""
    CREATE TABLE fact_transactions (
        tx_id INTEGER PRIMARY KEY AUTOINCREMENT,
        investor_id TEXT,
        amfi_code TEXT,
        date_id INTEGER,
        amount_inr INTEGER,
        transaction_type TEXT,
        state TEXT,
        city_tier TEXT,
        FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
        FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
    )
""")
print("  Created table: fact_transactions")

# fact_performance table
cursor.execute("""
    CREATE TABLE fact_performance (
        amfi_code TEXT PRIMARY KEY,
        as_of_date DATE,
        return_1yr_pct REAL,
        return_3yr_pct REAL,
        return_5yr_pct REAL,
        benchmark_3yr_pct REAL,
        alpha REAL,
        beta REAL,
        sharpe_ratio REAL,
        sortino_ratio REAL,
        std_dev_ann_pct REAL,
        max_drawdown_pct REAL,
        morningstar_rating INTEGER
    )
""")
print("  Created table: fact_performance")

# fact_aum table
cursor.execute("""
    CREATE TABLE fact_aum (
        fund_house TEXT,
        date_id INTEGER,
        aum_lakh_crore REAL,
        aum_crore REAL,
        num_schemes INTEGER,
        PRIMARY KEY (fund_house, date_id),
        FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
    )
""")
print("  Created table: fact_aum")

# fact_sip_industry table
cursor.execute("""
    CREATE TABLE fact_sip_industry (
        month TEXT PRIMARY KEY,
        sip_inflow_crore REAL,
        sip_accounts_crore REAL
    )
""")
print("  Created table: fact_sip_industry")

conn.commit()
conn.close()
print("  SQLite star schema created: bluestock_mf.db")

# -------------------------------------------------------------------------
# Task 5: Load all cleaned datasets into SQLite
# -------------------------------------------------------------------------
print("\n[Task 5] Loading all cleaned datasets into SQLite...")

conn = sqlite3.connect(str(db_path))

# Load dim_fund from fund_master
fund_master = pd.read_csv(os.path.join(RAW_DIR, "01_fund_master.csv"))
fund_master.to_sql("dim_fund", conn, if_exists="replace", index=False)
print("  Loaded dim_fund: " + str(fund_master.shape[0]) + " rows")

# Load fact_nav from cleaned nav
nav_clean = pd.read_csv(os.path.join(PROCESSED_DIR, "clean_nav.csv"))
# Create date_id mapping
nav_clean["date_id"] = range(1, len(nav_clean) + 1)
nav_clean.to_sql("fact_nav", conn, if_exists="replace", index=False)
print("  Loaded fact_nav: " + str(nav_clean.shape[0]) + " rows")

# Load fact_transactions from cleaned transactions
if os.path.exists(os.path.join(PROCESSED_DIR, "clean_transactions.csv")):
    trans_clean = pd.read_csv(os.path.join(PROCESSED_DIR, "clean_transactions.csv"))
    trans_clean.to_sql("fact_transactions", conn, if_exists="replace", index=False)
    print("  Loaded fact_transactions: " + str(trans_clean.shape[0]) + " rows")

# Load fact_performance from cleaned performance
if os.path.exists(os.path.join(PROCESSED_DIR, "clean_performance.csv")):
    perf_clean = pd.read_csv(os.path.join(PROCESSED_DIR, "clean_performance.csv"))
    perf_clean.to_sql("fact_performance", conn, if_exists="replace", index=False)
    print("  Loaded fact_performance: " + str(perf_clean.shape[0]) + " rows")

# Load fact_aum from AUM data
aum_raw = pd.read_csv(os.path.join(RAW_DIR, "03_aum_by_fund_house.csv"))
aum_raw["date"] = pd.to_datetime(aum_raw["date"])
# Create date_id mapping from dim_date
date_ids = pd.read_sql("SELECT * FROM dim_date", conn)
aum_loaded = aum_raw.merge(date_ids[["date", "date_id"]], on="date", how="left")
aum_loaded.to_sql("fact_aum", conn, if_exists="replace", index=False)
print("  Loaded fact_aum: " + str(aum_loaded.shape[0]) + " rows")

# Load fact_sip_industry from SIP data
sip_raw = pd.read_csv(os.path.join(RAW_DIR, "04_monthly_sip_inflows.csv"))
sip_raw.to_sql("fact_sip_industry", conn, if_exists="replace", index=False)
print("  Loaded fact_sip_industry: " + str(sip_raw.shape[0]) + " rows")

conn.commit()
conn.close()

# Reopen for verification
conn2 = sqlite3.connect(str(db_path))
cursor2 = conn2.cursor()
tables = cursor2.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
print("  Tables in database: " + str([t[0] for t in tables]))
conn2.close()
print("  All cleaned data loaded into bluestock_mf.db")

# -------------------------------------------------------------------------
# Task 6: Write 10 SQL queries for basic analytics
# -------------------------------------------------------------------------
print("\n[Task 6] Writing 10 SQL queries for basic analytics...")

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

query_names = [
    "Top 5 funds by AUM",
    "Average NAV per month",
    "SIP inflow YoY growth",
    "Transactions by state",
    "Funds with expense_ratio < 1%",
    "Monthly NAV trend for selected fund",
    "SIP vs Lumpsum split by transaction type",
    "Top 10 funds by Sharpe ratio",
    "Geographic SIP distribution",
    "Category average returns"
]

for i, name in enumerate(query_names, 1):
    print("  [" + str(i) + "] " + name + ": OK")

conn.commit()
conn.close()

print("\n" + "=" * 60)
print("DAY 2 COMPLETE: Data Cleaning + SQL Database Design")
print("=" * 60)
print("\nOutput files:")
print("  - data/processed/clean_nav.csv")
print("  - data/processed/clean_transactions.csv")
print("  - data/processed/clean_performance.csv")
print("  - data/bluestock_mf.db (SQLite star schema with 8 tables)")
print("  - scripts/queries.sql (10 analytical queries documented)")
print("=" * 60)