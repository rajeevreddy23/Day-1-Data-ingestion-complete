# Bluestock Fintech - Mutual Fund Analytics Platform
## Data Dictionary & Schema Reference

### Overview
This data dictionary provides comprehensive field-level documentation, data types, business definitions, constraints, and source attribution for the 10 core datasets and the SQLite Star Schema database (`bluestock_mf.db`).

---

### Table of Contents
1. [dim_fund (01_fund_master.csv)](#1-dim_fund-01_fund_mastercsv)
2. [fact_nav (02_nav_history.csv)](#2-fact_nav-02_nav_historycsv)
3. [fact_aum (03_aum_by_fund_house.csv)](#3-fact_aum-03_aum_by_fund_housecsv)
4. [fact_sip_industry (04_monthly_sip_inflows.csv)](#4-fact_sip_industry-04_monthly_sip_inflowscsv)
5. [fact_category_inflows (05_category_inflows.csv)](#5-fact_category_inflows-05_category_inflowscsv)
6. [fact_folio_count (06_industry_folio_count.csv)](#6-fact_folio_count-06_industry_folio_countcsv)
7. [fact_performance (07_scheme_performance.csv)](#7-fact_performance-07_scheme_performancecsv)
8. [fact_transactions (08_investor_transactions.csv)](#8-fact_transactions-08_investor_transactionscsv)
9. [fact_portfolio_holdings (09_portfolio_holdings.csv)](#9-fact_portfolio_holdings-09_portfolio_holdingscsv)
10. [fact_benchmarks (10_benchmark_indices.csv)](#10-fact_benchmarks-10_benchmark_indicescsv)

---

### 1. dim_fund (`01_fund_master.csv`)
* **Primary Key:** `amfi_code`
* **Source:** AMFI India Scheme Master & mfapi.in
* **Description:** Master metadata for 40 mutual fund schemes across 10 Asset Management Companies (AMCs).

| Column Name | SQL Type | Constraint | Description / Business Meaning | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | PRIMARY KEY | Unique 6-digit identifier assigned by AMFI India | `125497` |
| `fund_house` | TEXT | NOT NULL | Name of the Asset Management Company (AMC) | `HDFC Mutual Fund` |
| `scheme_name` | TEXT | NOT NULL | Official full name of the mutual fund scheme | `HDFC Top 100 Fund - Direct - Growth` |
| `category` | TEXT | NOT NULL | Broad asset class: `Equity`, `Debt`, `Hybrid` | `Equity` |
| `sub_category` | TEXT | NOT NULL | SEBI investment category classification | `Large Cap` |
| `plan` | TEXT | NOT NULL | Scheme investment route: `Direct` or `Regular` | `Direct` |
| `launch_date` | TEXT (DATE) | YYYY-MM-DD | Date the fund was officially launched | `2013-01-01` |
| `benchmark` | TEXT | NOT NULL | Official index benchmark for relative comparison | `NIFTY 100 TRI` |
| `expense_ratio_pct` | REAL | CHECK (>= 0) | Annual management and operating expense ratio (%) | `1.05` |
| `exit_load_pct` | REAL | CHECK (>= 0) | Fee levied on redemption before holding threshold | `1.00` |
| `fund_manager` | TEXT | - | Name of primary portfolio fund manager | `Rahul Baijal` |
| `risk_category` | TEXT | - | SEBI Risk-o-meter rating (`Low` to `Very High`) | `Very High` |
| `sebi_category_code` | TEXT | - | Standard regulatory classification code | `EC01` |

---

### 2. fact_nav (`02_nav_history.csv`)
* **Primary Key:** Composite (`amfi_code`, `date`)
* **Foreign Key:** `amfi_code` REFERENCES `dim_fund(amfi_code)`
* **Source:** AMFI Historical NAV & mfapi.in daily endpoint
* **Description:** Daily Net Asset Value (NAV) records for 40 schemes over 4.5 years (2022-2026).

| Column Name | SQL Type | Constraint | Description / Business Meaning | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | FK | AMFI scheme identifier | `125497` |
| `date` | TEXT (DATE) | NOT NULL | Trading date (business days, YYYY-MM-DD) | `2024-05-15` |
| `nav` | REAL | CHECK (> 0) | Net Asset Value per unit in Indian Rupees (INR) | `892.4560` |

---

### 3. fact_aum (`03_aum_by_fund_house.csv`)
* **Source:** AMFI India Average AUM Quarterly Disclosure
* **Description:** Total assets under management across top Indian fund houses.

| Column Name | SQL Type | Description / Business Meaning | Sample Value |
| :--- | :--- | :--- | :--- |
| `fund_house` | TEXT | Name of the fund house / AMC | `SBI Mutual Fund` |
| `date` | TEXT (DATE) | Quarter end date | `2024-12-31` |
| `aum_crore` | REAL | Total AUM in ₹ Crore | `1114250.00` |
| `aum_lakh_crore` | REAL | Total AUM in ₹ Lakh Crore (aum_crore / 100,000) | `11.14` |
| `num_schemes` | INTEGER | Number of active schemes managed by AMC | `186` |

---

### 4. fact_sip_industry (`04_monthly_sip_inflows.csv`)
* **Source:** AMFI India Monthly SIP Contribution Data (48 months)
* **Description:** Macro-level systematic investment plan (SIP) inflow trends across the Indian industry.

| Column Name | SQL Type | Description / Business Meaning | Sample Value |
| :--- | :--- | :--- | :--- |
| `month` | TEXT | Month identifier (YYYY-MM) | `2025-12` |
| `sip_inflow_crore` | REAL | Total gross monthly SIP contribution in ₹ Crore | `31002.0` |
| `active_sip_accounts_crore` | REAL | Total actively contributing SIP folios in Crore | `9.35` |
| `new_sip_accounts_lakh` | REAL | Newly registered SIP accounts in the month (Lakhs) | `9.80` |
| `sip_aum_lakh_crore` | REAL | Cumulative AUM accumulated via SIPs in ₹ Lakh Crore | `15.90` |
| `yoy_growth_pct` | REAL | Year-over-Year growth percentage in monthly SIP inflow | `38.45` |

---

### 5. fact_category_inflows (`05_category_inflows.csv`)
* **Source:** AMFI Monthly Category Flow Reports
* **Description:** Net monthly fund flows across mutual fund categories (Equity, Debt, Hybrid, Liquid).

| Column Name | SQL Type | Description / Business Meaning | Sample Value |
| :--- | :--- | :--- | :--- |
| `month` | TEXT | Calendar month (YYYY-MM) | `2024-12` |
| `category` | TEXT | Asset class category | `Equity` |
| `sub_category` | TEXT | Sub-category (e.g., Mid Cap, Small Cap, Liquid) | `Mid Cap` |
| `net_inflow_crore` | REAL | Net monthly inflows (Inflows - Outflows) in ₹ Crore | `5023.00` |

---

### 6. fact_folio_count (`06_industry_folio_count.csv`)
* **Source:** AMFI Investor Folio Disclosures
* **Description:** Growth and count of investor folios across retail and institutional segments.

| Column Name | SQL Type | Description / Business Meaning | Sample Value |
| :--- | :--- | :--- | :--- |
| `period` | TEXT | Semi-annual or annual reporting period | `Dec-2025` |
| `retail_folios_crore` | REAL | Folios held by retail individual investors (Crore) | `23.85` |
| `hni_folios_crore` | REAL | High Net-worth Individual folios (Crore) | `2.10` |
| `total_folios_crore` | REAL | Cumulative industry mutual fund folios (Crore) | `26.12` |

---

### 7. fact_performance (`07_scheme_performance.csv`)
* **Primary Key:** `amfi_code`
* **Source:** Computed from historical NAV & Benchmark series
* **Description:** Quantitative risk-adjusted performance metrics for fund comparison.

| Column Name | SQL Type | Description / Business Meaning | Sample Value |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | AMFI scheme identifier | `125497` |
| `return_1yr_pct` | REAL | 1-year trailing absolute return (%) | `24.50` |
| `return_3yr_pct` | REAL | 3-year Compound Annual Growth Rate (CAGR %) | `18.25` |
| `return_5yr_pct` | REAL | 5-year Compound Annual Growth Rate (CAGR %) | `16.80` |
| `benchmark_3yr_pct` | REAL | Corresponding benchmark 3-year CAGR (%) | `15.10` |
| `alpha` | REAL | Annualized excess return over benchmark (OLS intercept) | `3.15` |
| `beta` | REAL | Market systematic risk sensitivity (OLS slope) | `0.92` |
| `sharpe_ratio` | REAL | Risk-adjusted return: (Return - Rf) / Volatility (Rf = 6.5%) | `1.34` |
| `sortino_ratio` | REAL | Downside risk-adjusted return: (Return - Rf) / Downside Std | `1.85` |
| `std_dev_ann_pct` | REAL | Annualized standard deviation of daily returns (%) | `14.20` |
| `max_drawdown_pct` | REAL | Maximum peak-to-trough percentage loss (%) | `-16.50` |
| `morningstar_rating` | INTEGER | 1 to 5 star rating based on risk-adjusted performance | `5` |

---

### 8. fact_transactions (`08_investor_transactions.csv`)
* **Source:** Synthetic transaction logs modeled on Indian investor demographics
* **Description:** 32,770 individual investor transactions spanning SIPs, lumpsum purchases, and redemptions.

| Column Name | SQL Type | Description / Business Meaning | Sample Value |
| :--- | :--- | :--- | :--- |
| `investor_id` | TEXT | Unique investor identifier | `INV000142` |
| `transaction_date` | TEXT (DATE) | Date of transaction execution | `2024-08-10` |
| `amfi_code` | INTEGER | Scheme invested in | `119551` |
| `transaction_type` | TEXT | Type: `SIP`, `Lumpsum`, or `Redemption` | `SIP` |
| `amount_inr` | INTEGER | Transaction value in Indian Rupees | `5000` |
| `state` | TEXT | Investor state (12 major Indian states covered) | `Maharashtra` |
| `city` | TEXT | Investor residential city | `Mumbai` |
| `city_tier` | TEXT | AMFI classification: `T30` (Top 30) or `B30` (Beyond 30) | `T30` |
| `age_group` | TEXT | Demographic cohort: `18-25`, `26-35`, `36-45`, `46-55`, `56+` | `36-45` |
| `gender` | TEXT | `Male`, `Female`, `Other` | `Male` |
| `annual_income_lakh` | REAL | Annual reported income in ₹ Lakh | `18.5` |
| `payment_mode` | TEXT | Payment method: `UPI`, `Net Banking`, `Mandate`, `Cheque` | `UPI` |
| `kyc_status` | TEXT | Regulatory KYC status: `Verified` or `Pending` | `Verified` |

---

### 9. fact_portfolio_holdings (`09_portfolio_holdings.csv`)
* **Source:** Monthly Scheme Portfolio Disclosures
* **Description:** Underlying stock asset allocations and sector weights for each equity fund.

| Column Name | SQL Type | Description / Business Meaning | Sample Value |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | Scheme code | `125497` |
| `company_name` | TEXT | Name of portfolio company | `HDFC Bank Ltd.` |
| `sector` | TEXT | Industry sector (Banking, IT, Oil & Gas, etc.) | `Financial Services` |
| `weight_pct` | REAL | Allocation weight as percentage of scheme AUM | `8.95` |

---

### 10. fact_benchmarks (`10_benchmark_indices.csv`)
* **Source:** NSE India & BSE India Historical Index Prices
* **Description:** Benchmark indices tracked: Nifty 50, Nifty 100, Nifty Midcap 150, Nifty Smallcap 250, etc.

| Column Name | SQL Type | Description / Business Meaning | Sample Value |
| :--- | :--- | :--- | :--- |
| `index_name` | TEXT | Official index identifier | `NIFTY 100` |
| `date` | TEXT (DATE) | Trading day (YYYY-MM-DD) | `2024-05-15` |
| `close_price` | REAL | Daily closing index price value | `23450.75` |
