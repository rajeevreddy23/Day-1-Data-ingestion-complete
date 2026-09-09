"""
Bluestock Fintech - Mutual Fund Analytics Platform
Deliverable: live_nav_fetch.py
Day 1: Automated Live NAV Extraction from mfapi.in REST API

Description:
  Fetches historical and latest daily NAV data from the open API
  https://api.mfapi.in/mf/{scheme_code} for target mutual fund schemes:
    1. Anchor Scheme: HDFC Top 100 Direct (AMFI Code: 125497)
    2. SBI Bluechip (AMFI Code: 119551)
    3. ICICI Bluechip (AMFI Code: 120503)
    4. Nippon Large Cap (AMFI Code: 118632)
    5. Axis Bluechip (AMFI Code: 119092)
    6. Kotak Bluechip (AMFI Code: 120841)

  Parses JSON response, extracts metadata and daily NAV records,
  structures into a clean Pandas DataFrame, and saves to data/raw/.
"""

import os
import sys
import time
import requests
import pandas as pd
from pathlib import Path

# Paths configuration
BASE_DIR = Path(__file__).resolve().parent
# If running from scripts/, adjust BASE_DIR to project root
if BASE_DIR.name == "scripts":
    BASE_DIR = BASE_DIR.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Target Schemes Specification
SCHEMES_TO_FETCH = [
    {
        "amfi_code": 125497,
        "scheme_label": "HDFC_Top_100",
        "scheme_display_name": "HDFC Top 100 Fund - Direct Plan (AMFI 125497)",
        "is_anchor": True
    },
    {
        "amfi_code": 119551,
        "scheme_label": "SBI_Bluechip",
        "scheme_display_name": "SBI Bluechip Fund (AMFI 119551)",
        "is_anchor": False
    },
    {
        "amfi_code": 120503,
        "scheme_label": "ICICI_Bluechip",
        "scheme_display_name": "ICICI Prudential Bluechip Fund (AMFI 120503)",
        "is_anchor": False
    },
    {
        "amfi_code": 118632,
        "scheme_label": "Nippon_Large_Cap",
        "scheme_display_name": "Nippon India Large Cap Fund (AMFI 118632)",
        "is_anchor": False
    },
    {
        "amfi_code": 119092,
        "scheme_label": "Axis_Bluechip",
        "scheme_display_name": "Axis Bluechip Fund (AMFI 119092)",
        "is_anchor": False
    },
    {
        "amfi_code": 120841,
        "scheme_label": "Kotak_Bluechip",
        "scheme_display_name": "Kotak Bluechip Fund (AMFI 120841)",
        "is_anchor": False
    }
]

API_BASE_URL = "https://api.mfapi.in/mf"


def fetch_scheme_nav(amfi_code: int, max_retries: int = 3, timeout: int = 15):
    """
    Fetch NAV time-series data for a given AMFI scheme code from mfapi.in.
    Returns (meta_dict, nav_df) or (None, None) on failure.
    """
    url = f"{API_BASE_URL}/{amfi_code}"
    headers = {"User-Agent": "Bluestock-MF-Analytics/1.0"}

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code == 200:
                payload = response.json()
                meta = payload.get("meta", {})
                data_records = payload.get("data", [])

                if not data_records:
                    print(f"  [WARN] Scheme {amfi_code}: Empty data list returned from API.")
                    return meta, pd.DataFrame()

                # Parse records into standard DataFrame
                rows = []
                for entry in data_records:
                    raw_date = entry.get("date", "")
                    raw_nav = entry.get("nav", "")
                    try:
                        nav_float = float(raw_nav)
                    except (ValueError, TypeError):
                        nav_float = None

                    rows.append({
                        "amfi_code": amfi_code,
                        "date": raw_date,
                        "nav": nav_float
                    })

                df = pd.DataFrame(rows)
                # Convert date format dd-mm-yyyy to standardized ISO format yyyy-mm-dd
                df["date_parsed"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")
                df = df.sort_values("date_parsed", ascending=True).reset_index(drop=True)
                df["date"] = df["date_parsed"].dt.strftime("%Y-%m-%d")
                df = df.drop(columns=["date_parsed"])
                return meta, df

            elif response.status_code == 404:
                print(f"  [ERROR] Scheme {amfi_code} not found on mfapi.in (HTTP 404).")
                return None, None
            else:
                print(f"  [WARN] Attempt {attempt}/{max_retries}: HTTP {response.status_code} for scheme {amfi_code}.")

        except (requests.RequestException, Exception) as exc:
            print(f"  [WARN] Attempt {attempt}/{max_retries}: Network error ({exc}) for scheme {amfi_code}.")

        if attempt < max_retries:
            time.sleep(1.5 * attempt)

    print(f"  [FAIL] Failed to fetch scheme {amfi_code} after {max_retries} attempts.")
    return None, None


def run_live_nav_pipeline():
    """
    Executes live NAV ingestion for all configured schemes and persists CSV files.
    """
    print("=" * 75)
    print("BLUESTOCK FINTECH - LIVE NAV EXTRACTION PIPELINE (mfapi.in)")
    print("Day 1 Ingestion: REST API Fetch, JSON Parsing, and Raw CSV Storage")
    print("=" * 75)

    summary_rows = []

    for item in SCHEMES_TO_FETCH:
        code = item["amfi_code"]
        label = item["scheme_label"]
        display_name = item["scheme_display_name"]
        is_anchor = item["is_anchor"]

        tag = "[ANCHOR]" if is_anchor else "[KEY-SCHEME]"
        print(f"\n{tag} Fetching {display_name}...")
        print(f"  GET {API_BASE_URL}/{code}")

        meta, df_nav = fetch_scheme_nav(code)

        if df_nav is not None and not df_nav.empty:
            out_filename = f"live_nav_{label}.csv"
            out_path = RAW_DATA_DIR / out_filename
            df_nav.to_csv(out_path, index=False)

            earliest_date = df_nav["date"].iloc[0]
            latest_date = df_nav["date"].iloc[-1]
            latest_nav = df_nav["nav"].iloc[-1]
            record_count = len(df_nav)
            api_scheme_name = meta.get("scheme_name", display_name)
            fund_house = meta.get("fund_house", "Unknown AMC")

            print(f"  [SUCCESS] Saved {record_count} records to {out_path}")
            print(f"  Metadata: {api_scheme_name} | {fund_house}")
            print(f"  Date Range: {earliest_date} to {latest_date} | Latest NAV: INR {latest_nav:.4f}")

            summary_rows.append({
                "AMFI Code": code,
                "Label": label,
                "API Scheme Name": api_scheme_name,
                "Fund House": fund_house,
                "Record Count": record_count,
                "Earliest Date": earliest_date,
                "Latest Date": latest_date,
                "Latest NAV (INR)": latest_nav,
                "Status": "SUCCESS"
            })
        else:
            print(f"  [ERROR] Could not extract NAV data for AMFI code {code}.")
            summary_rows.append({
                "AMFI Code": code,
                "Label": label,
                "API Scheme Name": "N/A",
                "Fund House": "N/A",
                "Record Count": 0,
                "Earliest Date": "N/A",
                "Latest Date": "N/A",
                "Latest NAV (INR)": None,
                "Status": "FAILED"
            })

    # Display Summary Table
    print("\n" + "=" * 75)
    print("LIVE NAV INGESTION SUMMARY")
    print("=" * 75)
    df_summary = pd.DataFrame(summary_rows)
    print(df_summary[[
        "AMFI Code", "Label", "Record Count",
        "Earliest Date", "Latest Date", "Latest NAV (INR)", "Status"
    ]].to_string(index=False))

    print(f"\nAll downloaded CSV files are saved in: {RAW_DATA_DIR.resolve()}")
    print("=" * 75)
    return df_summary


if __name__ == "__main__":
    run_live_nav_pipeline()