# Bluestock Mutual Fund Analytics - Data Quality Summary Report
**Project Milestone:** Day 1 - Data Ingestion & Validation  
**Date Generated:** 2026-09-16 18:35:53  
**Author:** Bluestock Fintech Analytics Team  

---

## 1. Executive Data Quality Overview
All 10 fundamental mutual fund datasets provided by AMFI India and external financial databases were successfully loaded, profiled, and validated. In addition, real-time NAV records were programmatically fetched from the `mfapi.in` REST API for anchor scheme HDFC Top 100 Direct and 5 peer bluechip schemes.

| Metric | Measurement | Status |
| :--- | :--- | :--- |
| **Total Datasets Ingested** | 10 CSVs + 6 Live API Datasets | Passed |
| **Master Fund Schemes** | 40 unique schemes | 100% Coverage |
| **Total NAV Observations** | 46,000 rows (Jan 2022 – May 2026) | Complete |
| **Investor Transactions** | 32,778 records | Verified |
| **AMFI Referential Integrity** | 0 missing codes across Master & NAV | 100% Validated |

---

## 2. AMFI Scheme Code Validation
- **Fund Master Count:** 40 unique 6-digit AMFI codes.
- **NAV History Count:** 40 unique 6-digit AMFI codes.
- **Referential Integrity Result:** **PERFECT MATCH (100%)**. Every AMFI scheme in `01_fund_master.csv` maps directly to historical NAV series in `02_nav_history.csv`.
- **Granularity:** Each scheme contains exactly 1,150 trading day NAV observations spanning 4.5 years.

---

## 3. Dataset Anomaly Profiling & Resolutions
1. **04_monthly_sip_inflows.csv:**
   - *Observation:* 12 null entries in column `yoy_growth_pct`.
   - *Root Cause Analysis:* Year-over-Year (YoY) percentage calculation requires a 12-month lookback period. The dataset commences in Jan 2022; hence the first 12 months (2022-01 to 2022-12) have no preceding year data in this dataset.
   - *Resolution:* Expected behavior. Handled in transformation layer using imputation or explicit flagging.
2. **Date Typing:**
   - *Observation:* Dates in CSV files (`transaction_date`, `date`, `month`) are naturally formatted as string objects.
   - *Resolution:* Converted to ISO-8601 (`YYYY-MM-DD`) and mapped to relational `dim_date` table in Day 2 data cleaning ETL.
3. **Completeness:**
   - Zero duplicate rows across master tables.
   - No negative NAV or negative AUM values detected.

---

## 4. Live API Ingestion Performance (`mfapi.in`)
- **Anchor Scheme:** AMFI 125497 (HDFC Top 100 Direct) - 3,161 live records saved to `data/raw/live_nav_HDFC_Top_100.csv`.
- **5 Key Bluechip Schemes:**
  - SBI Bluechip (119551): 3,305 records
  - ICICI Bluechip (120503): 3,377 records
  - Nippon Large Cap (118632): 3,368 records
  - Axis Bluechip (119092): 3,634 records
  - Kotak Bluechip (120841): 3,371 records
- **Data Freshness:** Live daily NAV tracked up to latest trading day.

---

## 5. Conclusion & Next Steps
Day 1 data ingestion is fully complete. The foundation is primed for Day 2: Relational star-schema design and SQLite database population (`bluestock_mf.db`).
