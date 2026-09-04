# Bluestock Fintech - Mutual Fund Analytics Capstone Project

## Project Overview
A comprehensive end-to-end Mutual Fund Analytics Platform built as a 7-week capstone project by Bluestock Fintech Pvt. Ltd. The platform ingests publicly available AMFI India data, transforms it through a robust ETL pipeline, stores it in a relational database, and presents insights via an interactive dashboard.

## Project Structure
```
bluestock_mf_capstone/
├── data/
│   ├── raw/              ← Original downloaded CSV files (10 datasets)
│   ├── processed/        ← Cleaned/merged CSVs and computed metrics
│   └── bluestock_mf.db   ← SQLite star schema database (8 tables)
├── scripts/              ← Python ETL and compute scripts
│   ├── data_ingestion.py    ← Day 1: Data ingestion & project setup
│   └── data_cleaning.py     ← Day 2: Data cleaning + SQL DB design
├── notebooks/            ← Jupyter Notebooks for EDA and analytics
│   ├── 01_data_ingestion.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda_analysis.ipynb     ← 15+ charts, trend analysis
│   ├── 04_performance_analytics.ipynb  ← Sharpe, Sortino, Alpha, Beta
│   └── 06_advanced_analytics.ipynb     ← VaR, Cohort, HHI, Recommendations
├── dashboard/            ← Streamlit web application
│   └── streamlit_dashboard.py  ← 4-page interactive dashboard
├── outputs/              ← Generated charts, reports, and findings
├── reports/              ← Final report and presentations
│   └── FINAL_REPORT.md
├── requirements.txt      ← Python dependencies
├── .gitignore            ← Git ignore rules
└── README.md             ← This file
```

## Key Deliverables

| Deliverable | Description | Format |
|-------------|-------------|--------|
| D1 | ETL Pipeline Script | `scripts/data_ingestion.py` - ingests 10 CSVs, fetches live NAV from mfapi.in |
| D2 | SQLite Database | `data/bluestock_mf.db` - 8-table star schema with all data loaded |
| D3 | EDA Notebook | `notebooks/03_eda_analysis.ipynb` - 15+ charts, 10 key findings |
| D4 | Performance Metrics | Sharpe/Sortino/Alpha/Beta/Max DD/CAGR for 40 funds |
| D5 | Interactive Dashboard | Streamlit app with 4 pages: Industry, Fund Performance, Investor, Trends |
| D6 | Advanced Analytics | VaR/CVaR, Rolling Sharpe, Cohort analysis, HHI concentration, Fund recommendations |
| D7 | Final Report + Slides | `FINAL_REPORT.md` + 12-slide presentation deck |

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the ETL Pipeline
```bash
python scripts/data_ingestion.py
```

### 3. Clean and Load Data
```bash
python scripts/data_cleaning.py
```

### 4. Run Performance Analytics
```bash
python notebooks/04_performance_analytics.py
```

### 5. Run Advanced Analytics
```bash
python notebooks/06_advanced_analytics.py
```

### 6. Launch the Dashboard
```bash
streamlit run dashboard/streamlit_dashboard.py
```
Dashboard will be available at `http://localhost:8501`

### 7. Explore the Database
```python
import sqlite3
conn = sqlite3.connect('data/bluestock_mf.db')
# Explore tables: dim_fund, fact_nav, fact_transactions, etc.
conn.close()
```

## Data Sources
All data sourced from publicly available information:
- **AMFI India** (www.amfiindia.com): NAV, AUM, Folio, SIP data
- **mfapi.in** (api.mfapi.in/mf/{code}): Historical NAV JSON API
- **NSE India** (nseindia.com): Benchmark index prices
- **BSE India**: BSE SmallCap index data

Coverage: 40 mutual fund schemes, 4.5 years (Jan 2022 - May 2026), 87,000+ rows

## Project Timeline (7 Working Days)
- **Day 1**: Project Setup + Data Ingestion (ETL)
- **Day 2**: Data Cleaning + SQL Database Design
- **Day 3**: Exploratory Data Analysis (EDA)
- **Day 4**: Fund Performance Analytics
- **Day 5**: Dashboard Development (Streamlit)
- **Day 6**: Advanced Analytics + Risk Metrics
- **Day 7**: Final Report + Presentation + GitHub Deployment

## Key Metrics
- 40 mutual fund schemes across 10 AMCs
- 46,000 daily NAV records (Jan 2022 - May 2026)
- 32,000+ investor transactions
- 320 portfolio holdings with sector weights
- 8 benchmark indices tracked
- 15+ charts and visualizations generated
- 8 SQL analytical queries verified
- 4-streamlit dashboard pages

## License
This project is for educational purposes only and does not constitute financial advice. 
Mutual Fund investments are subject to market risks.

All data is sourced from publicly available AMFI India, mfapi.in, and NSE/BSE data.