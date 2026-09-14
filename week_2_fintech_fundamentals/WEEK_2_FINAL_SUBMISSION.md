# Bluestock Fintech - Data Analyst Internship
# Week 2: FinTech Domain & Software Development Fundamentals
**Internship Group:** 62FMBF  
**Assigned To:** Rajeev Reddy (`rajeevreddyakepati`)  
**Due Date:** 16 September 2026  
**Status:** COMPLETED (All 6 Deliverables Ready)

---

## 🌟 Executive Overview & Deliverables Matrix

This submission fulfills all mandatory tasks for **Week 2: FinTech Domain & Software Development Fundamentals**, preparing data analysts with end-to-end domain expertise, API data engineering skills, software architecture comprehension, and business intelligence capabilities.

| # | Deliverable Name | File Format | Status | Primary File Link |
| :--- | :--- | :--- | :--- | :--- |
| **D1** | **Stock Market Summary Document** | Markdown / PDF | ✅ Completed | [`1_stock_market_and_financial_analysis.md`](file:///c:/blue/drive-download-20260902T170546Z-1-001/week_2_fintech_fundamentals/1_stock_market_and_financial_analysis.md#L1-L60) |
| **D2** | **Financial Statement Analysis** | Markdown (TCS Case Study) | ✅ Completed | [`1_stock_market_and_financial_analysis.md`](file:///c:/blue/drive-download-20260902T170546Z-1-001/week_2_fintech_fundamentals/1_stock_market_and_financial_analysis.md#L61-L120) |
| **D3** | **API Data Extraction Assignment** | Python + JSON + CSV | ✅ Executed | [`2_api_data_extraction.py`](file:///c:/blue/drive-download-20260902T170546Z-1-001/week_2_fintech_fundamentals/2_api_data_extraction.py), [`api_extracted_data.csv`](file:///c:/blue/drive-download-20260902T170546Z-1-001/week_2_fintech_fundamentals/api_extracted_data.csv) |
| **D4** | **Software Architecture Diagram** | Markdown + Mermaid Flowchart | ✅ Completed | [`3_software_architecture_data_flow.md`](file:///c:/blue/drive-download-20260902T170546Z-1-001/week_2_fintech_fundamentals/3_software_architecture_data_flow.md) |
| **D5** | **FinTech Research Report** | Markdown (Zerodha Case Study) | ✅ Completed | [`4_fintech_research_report_zerodha.md`](file:///c:/blue/drive-download-20260902T170546Z-1-001/week_2_fintech_fundamentals/4_fintech_research_report_zerodha.md) |
| **D6** | **GitHub Repository & Version History** | Git Commits & Remote Repo | ✅ Pushed | `https://github.com/rajeevreddy23/Day-1-Data-ingestion-complete` |

---

## 📌 Summary of Core Modules Completed

### 1. Stock Market Fundamentals & Listed Company Analysis
* **Core Concepts Documented:** NSE/BSE exchange mechanisms, NIFTY 50 and SENSEX benchmark indices, IPO vs. SME IPO regulations, SEBI Market Cap categorization (Large, Mid, Small Cap), EPS, P/E, P/B ratios, dividend yields, bonus issues vs stock splits, and trading volume liquidity.
* **Financial Statement Deep Dive:** Comprehensive breakdown of **Tata Consultancy Services Ltd. (TCS)**:
  * Consolidated Balance Sheet (Zero debt, cash surplus > ₹45,000 Cr, Current Ratio 2.42x).
  * P&L Statement (Revenue ₹2.40L Cr, EBIT margin 24.6%, PAT ₹46,099 Cr).
  * Cash Flows (Operating cash conversion >95%, Free Cash Flow > ₹41,000 Cr).
  * Efficiency Ratios: Return on Equity (ROE) **49.8%**, ROCE **58.2%**.

### 2. REST APIs, JSON Inspection & Data Ingestion
* Developed and executed [`2_api_data_extraction.py`](file:///c:/blue/drive-download-20260902T170546Z-1-001/week_2_fintech_fundamentals/2_api_data_extraction.py):
  * Issues authenticated HTTP `GET` request to public financial API.
  * Inspects status codes (`200 OK`), headers, and nested JSON schemas.
  * Preserves raw JSON response in [`api_response_sample.json`](file:///c:/blue/drive-download-20260902T170546Z-1-001/week_2_fintech_fundamentals/api_response_sample.json).
  * Transforms 3,164 records into Pandas DataFrame with feature engineering (daily returns, 7-day and 30-day moving averages).
  * Exports clean dataset to [`api_extracted_data.csv`](file:///c:/blue/drive-download-20260902T170546Z-1-001/week_2_fintech_fundamentals/api_extracted_data.csv).

### 3. Software Architecture & End-to-End Data Flow
* Created comprehensive Mermaid sequence and pipeline diagrams in [`3_software_architecture_data_flow.md`](file:///c:/blue/drive-download-20260902T170546Z-1-001/week_2_fintech_fundamentals/3_software_architecture_data_flow.md):
  * **Layer 1:** Client Web/Mobile App (User clicks "Invest via SIP").
  * **Layer 2:** API Gateway & JWT Authentication Microservice.
  * **Layer 3:** Transactional Database (PostgreSQL/SQLite OLTP write).
  * **Layer 4:** Streaming & ETL Pipeline (Change Data Capture, star-schema warehouse load).
  * **Layer 5:** Analytical Reporting Engine (Streamlit / Power BI dashboard rendering).
  * Defined core SDLC phases, OLTP vs. OLAP paradigms, and logging/monitoring best practices.

### 4. FinTech Business Landscape & Zerodha Case Study
* Documented in [`4_fintech_research_report_zerodha.md`](file:///c:/blue/drive-download-20260902T170546Z-1-001/week_2_fintech_fundamentals/4_fintech_research_report_zerodha.md):
  * Structural distinctions between discount and full-service brokers.
  * Demat vs. Trading accounts; depositories (**NSDL & CDSL**).
  * SEBI mandate and investor protection regulations.
  * Market participant ecosystem (Retail, HNI, DII, FII, Prop Desks).
  * Complete **T+1 Settlement Lifecycle** from order placement to depository credit.
  * **Zerodha Case Study:** Analytical inspection of its **Nudge Behavioral Engine**, real-time **RMS margin VaR analytics**, **Console Tax-Loss Harvesting**, and peak-hour **order throughput telemetry**.

---

## 🚀 Submission Verification & GitHub Remote
All files are organized in the workspace under:
`C:\blue\drive-download-20260902T170546Z-1-001\week_2_fintech_fundamentals\`
and synchronized with the master repository:
`https://github.com/rajeevreddy23/Day-1-Data-ingestion-complete`
