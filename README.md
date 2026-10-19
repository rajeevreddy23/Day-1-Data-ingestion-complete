# Bluestock Fintech - Mutual Fund Analytics Capstone Project

> **Authors:** Poulami Dutta (PO) | Rajeev Reddy (RA) | Thadakamalla Likith Kumar (TH)  
> **Group Code:** 62FMBF  
> **GitHub Repository:** [https://github.com/rajeevreddy23/Day-1-Data-ingestion-complete](https://github.com/rajeevreddy23/Day-1-Data-ingestion-complete)  
> **Release Version:** `v1.0` (Production Tagged)  
> **Google Drive Submission:** Included in `Google_Drive_Submission_Files` & `Bluestock_Master_Google_Drive_Upload.zip`  

---

## Executive Summary & Overview
A complete, institutional-grade end-to-end **Mutual Fund Analytics & Intelligence Platform** developed as the Capstone Project for Bluestock Fintech Pvt. Ltd. The platform ingests publicly available AMFI India data and live REST APIs (`mfapi.in`), executes a robust ETL pipeline, normalizes and populates a high-performance relational star-schema database (`bluestock_mf.db`), models institutional quantitative risk metrics, and presents interactive insights via a multi-page analytical dashboard.

---

## Key Project Deliverables

| Deliverable ID | Component Name | Exact File Path | Format & Scope | Verification Status |
|----------------|----------------|-----------------|----------------|---------------------|
| **D1** | Master Execution Pipeline | `run_pipeline.py` | Python 3 orchestrator executing Steps 1 to 5 | **Verified (Exit code 0)** |
| **D2** | Executive Final Report | `Final_Report.pdf` | 18-page publication-quality PDF report | **Verified (18 Pages)** |
| **D3** | Presentation Deck | `Bluestock_MF_Presentation.pptx` | 12-slide executive presentation deck with embedded charts | **Verified (12 Slides)** |
| **D4** | Relational Star-Schema DB | `data/bluestock_mf.db` | SQLite star schema (8 tables, foreign keys, 87K+ rows) | **Verified (0 FK Violations)** |
| **D5** | Exploratory Data Analysis | `notebooks/03_eda_analysis.ipynb` | 15+ analytical charts, demographic & macro insights | **Verified (15+ Plots)** |
| **D6** | Quantitative Risk Engine | `scripts/compute_metrics.py` | 1Y/3Y/5Y CAGR, Alpha, Beta vs Nifty 100, Sharpe, Sortino | **Verified (40 Schemes)** |
| **D7** | Advanced Analytics & Risk | `notebooks/06_advanced_analytics.py` | VaR (95%), CVaR, Rolling Sharpe, Sector HHI, Cohort analysis | **Verified (Complete)** |
| **D8** | Interactive Dashboard | `dashboard/capstone_dashboard.py` | 4-screen Streamlit analytical web application | **Verified (Port 8501)** |

---

## Repository Structure

```
bluestock_mf_capstone/
├── data/
│   ├── raw/                           ← Original raw CSV datasets (10 sources) + live NAV files
│   ├── processed/                     ← Cleaned CSV datasets (clean_nav.csv, clean_transactions.csv, etc.)
│   └── bluestock_mf.db                ← Normalized SQLite star schema database (8 tables)
├── scripts/
│   ├── data_ingestion.py              ← Day 1: Automated extraction & live NAV API fetch (mfapi.in)
│   ├── data_cleaning.py               ← Day 2: Data cleaning, normalization & SQLite loading
│   ├── compute_metrics.py             ← Day 4: Quantitative CAGR, Sharpe, Sortino, Alpha, Beta engine
│   ├── recommender.py                 ← Day 6: Algorithmic fund recommender engine
│   └── queries.sql                    ← 10 verified analytical SQL queries
├── notebooks/
│   ├── 01_data_ingestion.ipynb        ← Day 1 ingestion notebook
│   ├── 02_data_cleaning.ipynb         ← Day 2 cleaning & star schema notebook
│   ├── 03_eda_analysis.ipynb          ← Day 3 exploratory data analysis
│   ├── 04_performance_analytics.ipynb ← Day 4 fund performance analytics
│   └── 06_advanced_analytics.ipynb    ← Day 6 VaR, CVaR, HHI, and cohort analytics
├── dashboard/
│   ├── capstone_dashboard.py          ← Multi-page interactive Streamlit dashboard
│   ├── dashboard_page_1.png           ← Page 1 screenshot (Industry Macro Trends)
│   ├── dashboard_page_2.png           ← Page 2 screenshot (Fund Performance & Scorecard)
│   ├── dashboard_page_3.png           ← Page 3 screenshot (Investor Analytics & Demographics)
│   └── dashboard_page_4.png           ← Page 4 screenshot (Market Trends & Recommender)
├── outputs/                           ← Generated analytical charts, CSV reports & findings
├── Final_Report.pdf                   ← 18-page executive capstone report (Publication quality)
├── Bluestock_MF_Presentation.pptx     ← 12-slide executive presentation deck
├── run_pipeline.py                    ← Master end-to-end execution script
├── requirements.txt                   ← Pinned project dependencies
└── README.md                          ← Master documentation & guide
```

---

## Dataset Descriptions (10 Core Sources)

| Dataset | Records / Span | Key Fields & Description |
|---------|----------------|--------------------------|
| `01_fund_master.csv` | 40 Schemes | `amfi_code`, `fund_house`, `scheme_name`, `category`, `sub_category`, `plan`, `expense_ratio` |
| `02_nav_history.csv` | 46,000 Records | Daily NAV history across 40 mutual fund schemes spanning 2020 to 2025 |
| `03_aum_by_fund_house.csv` | 44 Fund Houses | Quarterly AMC asset under management, market share percentage, rankings |
| `04_monthly_sip_inflows.csv` | 60 Months | Industry-wide monthly SIP contribution totals (in INR Crore) |
| `05_category_inflows.csv` | 36 Months | Net capital inflow dynamics across Equity, Debt, Hybrid, and Liquid fund categories |
| `06_industry_folio_count.csv` | 60 Months | Longitudinal growth in unique investor folios tracking retail penetration |
| `07_scheme_performance.csv` | 40 Schemes | Historical benchmark comparisons, stated 1Y/3Y/5Y returns, fund house metadata |
| `08_investor_transactions.csv` | 32,778 Records | Granular transaction logs: investor age, state, city tier (T30 vs B30), SIP cadence |
| `09_portfolio_holdings.csv` | 400+ Holdings | Scheme equity and debt asset composition, company names, sector allocations |
| `10_benchmark_indices.csv` | 1,250 Dates | Daily closing levels and returns for Nifty 50 and Nifty 100 benchmark indices |
| `live_nav_fetch.py` | Real-Time API | Direct integration with `https://api.mfapi.in/mf/{amfi_code}` |

---

## Quick Start & Execution Instructions

### 1. Environment Setup
```bash
# Clone the repository
git clone https://github.com/rajeevreddy23/Day-1-Data-ingestion-complete.git
cd Day-1-Data-ingestion-complete

# Install required dependencies
pip install -r requirements.txt
```

### 2. Run the Master End-to-End Pipeline
Execute the master execution pipeline to ingest live NAVs, clean datasets, populate SQLite, and compute all financial metrics:
```bash
python run_pipeline.py
```
*Expected Execution Time: ~50-60 seconds. All checks will log `[SUCCESS]` and report exit code `0`.*

### 3. Launch the Interactive Dashboard
Launch the multi-page Streamlit analytics application:
```bash
streamlit run dashboard/capstone_dashboard.py
```
Open your browser at `http://localhost:8501` to access:
- **Page 1: Industry Macro Trends** (AUM growth, monthly SIP inflows, folio expansion)
- **Page 2: Fund Performance & Scorecard** (CAGR, Alpha, Beta, Sharpe, Sortino rankings)
- **Page 3: Investor Demographic Analytics** (Age distribution, T30 vs B30, SIP continuity)
- **Page 4: Advanced Risk & Recommender** (Rolling Sharpe, VaR/CVaR, Sector HHI, Algorithmic Recommender)

### 4. Regenerate Final Deliverables
```bash
# Regenerate 18-page Final_Report.pdf
python generate_final_report_pdf.py

# Regenerate 12-slide Bluestock_MF_Presentation.pptx
python generate_presentation.py
```

---

## Self-Review Checklist & Quality Verification

| Check Item | Requirement | Actual Status | Verification Method |
|------------|-------------|---------------|---------------------|
| **Objective 1: Data Ingestion** | Ingest 10 AMFI datasets + live REST API | **MET** | 87K+ rows loaded; mfapi.in live sync verified |
| **Objective 2: Database Design** | Relational Star Schema in SQLite | **MET** | 8 tables in `bluestock_mf.db`; 0 FK errors |
| **Objective 3: Exploratory Data Analysis** | 15+ charts across macro & micro trends | **MET** | 15+ PNG & HTML charts generated in `outputs/` |
| **Objective 4: Risk-Adjusted Metrics** | CAGR, Alpha, Beta, Sharpe, Sortino | **MET** | `compute_metrics.py` generates full scorecard |
| **Objective 5: Advanced Analytics** | VaR (95%), CVaR, Rolling Sharpe, HHI | **MET** | `06_advanced_analytics.py` executes without errors |
| **Objective 6: Interactive Dashboard** | Multi-page Streamlit web app | **MET** | `dashboard/capstone_dashboard.py` runs on :8501 |
| **Objective 7: Presentation Deck** | 12-slide executive presentation | **MET** | `Bluestock_MF_Presentation.pptx` (12 slides) |
| **Objective 8: Comprehensive Report** | 15–20 page professional PDF report | **MET** | `Final_Report.pdf` (18 pages, ReportLab) |

---

## Git Release & Tagging

```bash
git add .
git commit -m "Final: Complete Bluestock MF Capstone"
git tag v1.0
git push origin main --tags
```

---

## License & Compliance
This capstone project is developed exclusively for educational and analytical purposes as part of the Bluestock Fintech Capstone Program. Mutual fund investments are subject to market risks; please read all scheme-related documents carefully before investing.