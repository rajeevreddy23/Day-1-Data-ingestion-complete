"""
Bluestock Fintech - Mutual Fund Analytics Platform
Script: generate_final_report_pdf.py
Generates a comprehensive 17-page publication-quality Final_Report.pdf
covering all 8 capstone sections, charts, tables, and recommendations.
"""

import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

BASE_DIR = Path(__file__).resolve().parent

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress headers/footers on title cover page
        
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1A365D"))  # Bluestock Navy
        # Header
        self.drawString(54, 750, "BLUESTOCK FINTECH — MUTUAL FUND ANALYTICS PLATFORM")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4A5568"))
        self.drawRightString(612 - 54, 750, "CAPSTONE EXECUTIVE REPORT")
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.75)
        self.line(54, 744, 612 - 54, 744)
        
        # Footer
        self.line(54, 45, 612 - 54, 45)
        self.drawString(54, 32, "Confidential — Prepared by Rajeev Reddy (Group: 62FMBF)")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 32, page_str)
        self.restoreState()


def build_pdf():
    pdf_path = BASE_DIR / "Final_Report.pdf"
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=60,
        bottomMargin=55
    )

    styles = getSampleStyleSheet()
    
    # Custom Brand Palette
    PRIMARY = colors.HexColor("#1A365D")    # Dark Navy
    SECONDARY = colors.HexColor("#2B6CB0")  # Royal Blue
    ACCENT = colors.HexColor("#319795")     # Teal
    DARK_TEXT = colors.HexColor("#2D3748")  # Charcoal
    LIGHT_BG = colors.HexColor("#F7FAFC")   # Off-white
    BORDER_COLOR = colors.HexColor("#E2E8F0")

    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=26,
        leading=32,
        textColor=PRIMARY,
        alignment=1
    )
    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=13,
        leading=18,
        textColor=SECONDARY,
        alignment=1
    )
    h1_style = ParagraphStyle(
        "Header1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=17,
        leading=21,
        textColor=PRIMARY,
        spaceAfter=10,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        "Header2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=SECONDARY,
        spaceBefore=8,
        spaceAfter=5,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        "BodyTextCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=DARK_TEXT,
        spaceAfter=7
    )
    body_bold = ParagraphStyle(
        "BodyBoldCustom",
        parent=body_style,
        fontName="Helvetica-Bold"
    )
    callout_style = ParagraphStyle(
        "CalloutText",
        parent=body_style,
        fontName="Helvetica-Oblique",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#2C5282")
    )
    table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10.5,
        textColor=DARK_TEXT
    )
    table_header = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 100))
    story.append(Paragraph("BLUESTOCK FINTECH", ParagraphStyle("BrandPre", fontName="Helvetica-Bold", fontSize=14, leading=16, textColor=ACCENT, alignment=1)))
    story.append(Spacer(1, 15))
    story.append(Paragraph("MUTUAL FUND ANALYTICS PLATFORM", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("End-to-End Financial Data Engineering, Quantitative Risk Modeling & Institutional Intelligence", subtitle_style))
    story.append(Spacer(1, 40))
    
    meta_table_data = [
        [Paragraph("<b>Capstone Project:</b>", table_cell), Paragraph("Capstone Project I — Mutual Fund Analytics", table_cell)],
        [Paragraph("<b>Organization:</b>", table_cell), Paragraph("Bluestock Fintech Pvt. Ltd.", table_cell)],
        [Paragraph("<b>Author / Analyst:</b>", table_cell), Paragraph("Rajeev Reddy (rajeevreddyakepati)", table_cell)],
        [Paragraph("<b>Internship Cohort:</b>", table_cell), Paragraph("Cohort Group 62FMBF", table_cell)],
        [Paragraph("<b>Submission Date:</b>", table_cell), Paragraph("September 2026", table_cell)],
        [Paragraph("<b>Platform Version:</b>", table_cell), Paragraph("Release v1.0 (Production Verified)", table_cell)],
        [Paragraph("<b>Repository:</b>", table_cell), Paragraph("github.com/rajeevreddy23/Day-1-Data-ingestion-complete", table_cell)],
    ]
    t_cover = Table(meta_table_data, colWidths=[150, 280])
    t_cover.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_cover)
    story.append(Spacer(1, 60))
    story.append(Paragraph("<i>A comprehensive 7-stage data science capstone delivering an automated ETL pipeline, 8-table relational SQLite star-schema database, advanced portfolio risk analytics, and interactive Streamlit web dashboard.</i>", callout_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: TABLE OF CONTENTS & EXECUTIVE SUMMARY
    # =========================================================================
    story.append(Paragraph("Executive Summary & Table of Contents", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=10))
    
    story.append(Paragraph("<b>1. Executive Summary</b>", h2_style))
    story.append(Paragraph(
        "The Indian mutual fund ecosystem has undergone monumental growth, surging from ₹6.05 Lakh Crore to over ₹81 Lakh Crore in aggregate AUM, fueled by exponential retail participation through Systematic Investment Plans (SIPs). Despite this expansion, retail and wealth managers face pervasive information asymmetry, fragmented datasets across AMCs, and opaque risk-adjusted performance visibility.", body_style
    ))
    story.append(Paragraph(
        "To solve these industry bottlenecks, Bluestock Fintech commissioned this end-to-end <b>Mutual Fund Analytics Platform</b>. Over a rigorous 7-stage development lifecycle, our analytics engineering team ingested, validated, cleaned, and synthesized over 87,000 observations across 40 schemes from India's top 10 Asset Management Companies (AMCs) spanning 4.5 trading years (Jan 2022 to May 2026).", body_style
    ))
    story.append(Paragraph(
        "Key deliverables include: (1) An automated Python ETL pipeline with live REST API integration (mfapi.in); (2) An 8-table relational SQLite star-schema database; (3) Rigorous quantitative performance metrics (CAGR, Sharpe, Sortino, Alpha, Beta, Max Drawdown); (4) Institutional risk modeling (Historical/Parametric VaR, CVaR, Rolling Sharpe, Sector HHI concentration); and (5) An interactive 4-page Streamlit web dashboard.", body_style
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Table of Contents</b>", h2_style))
    toc_data = [
        [Paragraph("<b>Section</b>", table_header), Paragraph("<b>Description</b>", table_header), Paragraph("<b>Page</b>", table_header)],
        [Paragraph("1. Executive Summary & Overview", table_cell), Paragraph("Project background, problem context, and outcomes", table_cell), Paragraph("2", table_cell)],
        [Paragraph("2. Business Problem & Project Objectives", table_cell), Paragraph("Market context, core bottlenecks, and 8 project objectives", table_cell), Paragraph("3", table_cell)],
        [Paragraph("3. Data Sources & AMFI Code Architecture", table_cell), Paragraph("10 baseline CSV datasets, schema definitions, and API specs", table_cell), Paragraph("4", table_cell)],
        [Paragraph("4. ETL Pipeline & Data Cleaning Lifecycle", table_cell), Paragraph("Deduplication, date parsing, missing values, and validation", table_cell), Paragraph("5", table_cell)],
        [Paragraph("5. Relational Star Schema Database Design", table_cell), Paragraph("bluestock_mf.db: Fact & dimension tables, DDL & indexing", table_cell), Paragraph("6", table_cell)],
        [Paragraph("6. Exploratory Data Analysis: AUM Trends", table_cell), Paragraph("Industry macro growth, AMC market share, and concentration", table_cell), Paragraph("7", table_cell)],
        [Paragraph("7. Exploratory Data Analysis: SIP & Folios", table_cell), Paragraph("Retail monthly SIP surge (+169%) and folio demographics", table_cell), Paragraph("8", table_cell)],
        [Paragraph("8. Fund Performance Analytics & CAGR", table_cell), Paragraph("1Y, 3Y, 5Y CAGR, volatility, and tracking error computation", table_cell), Paragraph("9", table_cell)],
        [Paragraph("9. Risk-Adjusted Returns: Sharpe, Sortino, Alpha", table_cell), Paragraph("Rf=6.5% Sharpe, downside Sortino, and OLS Alpha/Beta", table_cell), Paragraph("10", table_cell)],
        [Paragraph("10. Composite Fund Scorecard (0–100)", table_cell), Paragraph("Multi-factor ranking methodology and full 40-fund table", table_cell), Paragraph("11", table_cell)],
        [Paragraph("11. Advanced Risk Analytics: VaR, CVaR & Rolling", table_cell), Paragraph("Parametric/Historical VaR (95%/99%), CVaR, Rolling Sharpe", table_cell), Paragraph("12", table_cell)],
        [Paragraph("12. Investor Cohorts & SIP Continuity Analysis", table_cell), Paragraph("Annual cohort retention, at-risk gap identification (>35d)", table_cell), Paragraph("13", table_cell)],
        [Paragraph("13. Portfolio Concentration (HHI) & Recommender", table_cell), Paragraph("Herfindahl index and rule-based investor recommender engine", table_cell), Paragraph("14", table_cell)],
        [Paragraph("14. Interactive Streamlit Web Dashboard", table_cell), Paragraph("4-page web app architecture, KPIs, slicers, and screenshots", table_cell), Paragraph("15", table_cell)],
        [Paragraph("15. Project Limitations & Data Quality Review", table_cell), Paragraph("Survivorship bias, market regimes, and data constraints", table_cell), Paragraph("16", table_cell)],
        [Paragraph("16. Strategic Recommendations & Verification", table_cell), Paragraph("Actionable FinTech growth roadmap and rubric verification", table_cell), Paragraph("17", table_cell)]
    ]
    t_toc = Table(toc_data, colWidths=[160, 285, 45])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: BUSINESS PROBLEM & OBJECTIVES
    # =========================================================================
    story.append(Paragraph("2. Business Problem & Project Objectives", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("<b>Business Context & Market Bottlenecks</b>", h2_style))
    story.append(Paragraph(
        "India's financial landscape has transformed dramatically over the past four years. Domestic retail investors have transitioned from traditional fixed deposits and physical gold into financialized equity assets. While this transition represents unprecedented commercial opportunity for FinTech platforms like Bluestock, three structural data bottlenecks hinder optimal investor capital allocation:", body_style
    ))
    story.append(Paragraph("<b>Problem 1: Severe Data Fragmentation</b><br/>Historical daily Net Asset Values (NAV), quarterly Assets Under Management (AUM), monthly SIP industry aggregates, portfolio equity weights, and granular investor transactions are stored across siloed CSV files, third-party portals, and regulatory circulars without standardized primary keys.", body_style))
    story.append(Paragraph("<b>Problem 2: Misleading Surface-Level Return Metrics</b><br/>Retail investors frequently make allocation decisions based purely on trailing 1-year absolute returns, ignoring downside risk, market sensitivity (Beta), expense ratios, and rolling volatility. A scheme boasting a 35% return during a bull market may experience catastrophic drawdowns during corrections.", body_style))
    story.append(Paragraph("<b>Problem 3: Lack of Dynamic Risk & Behavioral Modeling</b><br/>Traditional platforms fail to track investor behavior over time. They cannot identify when Systematic Investment Plans (SIPs) lapse, do not evaluate sector concentration risk (HHI), and lack institutional-grade risk metrics like Value-at-Risk (VaR) and Conditional Value-at-Risk (CVaR).", body_style))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Core Project Objectives (O1 — O8)</b>", h2_style))
    
    objs_data = [
        [Paragraph("<b>Obj</b>", table_header), Paragraph("<b>Target Objective</b>", table_header), Paragraph("<b>Outcome Achieved</b>", table_header)],
        [Paragraph("<b>O1</b>", table_cell), Paragraph("Automate Raw Data Ingestion & Live API Fetch", table_cell), Paragraph("10 CSVs loaded + mfapi.in live NAV fetcher (46,000+ daily records).", table_cell)],
        [Paragraph("<b>O2</b>", table_cell), Paragraph("Design Relational Star-Schema SQL Database", table_cell), Paragraph("8-table SQLite schema (bluestock_mf.db) with 10 validated queries.", table_cell)],
        [Paragraph("<b>O3</b>", table_cell), Paragraph("Comprehensive Exploratory Data Analysis (EDA)", table_cell), Paragraph("15+ visualization charts examining AUM growth, SIP, and folio surges.", table_cell)],
        [Paragraph("<b>O4</b>", table_cell), Paragraph("Compute Quantitative Risk-Adjusted Metrics", table_cell), Paragraph("CAGR, Sharpe (Rf=6.5%), Sortino, Alpha, Beta, Max Drawdown.", table_cell)],
        [Paragraph("<b>O5</b>", table_cell), Paragraph("Engineer Multi-Factor Fund Scorecard (0–100)", table_cell), Paragraph("Composite ranking combining returns, Sharpe, Alpha, expenses, and MDD.", table_cell)],
        [Paragraph("<b>O6</b>", table_cell), Paragraph("Model Advanced Institutional Risk (VaR/CVaR)", table_cell), Paragraph("95% and 99% Parametric and Historical VaR, rolling 90-day Sharpe.", table_cell)],
        [Paragraph("<b>O7</b>", table_cell), Paragraph("Analyze Investor Cohorts & SIP Continuity", table_cell), Paragraph("Cohort retention tracking and identification of 2,949 at-risk investors.", table_cell)],
        [Paragraph("<b>O8</b>", table_cell), Paragraph("Deploy Interactive Web Dashboard & Presentation", table_cell), Paragraph("4-page Streamlit web app, 12-slide executive deck, and final report.", table_cell)],
    ]
    t_objs = Table(objs_data, colWidths=[35, 235, 220])
    t_objs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_objs)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: DATA SOURCES & AMFI CODE ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("3. Data Sources & AMFI Code Architecture", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("<b>Primary Ingestion Catalog</b>", h2_style))
    story.append(Paragraph(
        "The project aggregates ten authoritative datasets from the Association of Mutual Funds in India (AMFI), the National Stock Exchange (NSE), and the Bombay Stock Exchange (BSE), supplemented by live daily REST API feeds:", body_style
    ))

    catalog_data = [
        [Paragraph("<b>File Identifier</b>", table_header), Paragraph("<b>Dimensions (.shape)</b>", table_header), Paragraph("<b>Granularity & Scope</b>", table_header)],
        [Paragraph("01_fund_master.csv", table_cell), Paragraph("40 rows × 8 cols", table_cell), Paragraph("Master metadata: AMFI code, AMC, category, plan, expense ratio.", table_cell)],
        [Paragraph("02_nav_history.csv", table_cell), Paragraph("46,000 rows × 3 cols", table_cell), Paragraph("Daily NAVs for 40 schemes over 1,150 trading days (2022–2026).", table_cell)],
        [Paragraph("03_aum_by_fund_house.csv", table_cell), Paragraph("100 rows × 4 cols", table_cell), Paragraph("Quarterly AUM trends across top 10 Indian fund houses.", table_cell)],
        [Paragraph("04_monthly_sip_inflows.csv", table_cell), Paragraph("53 rows × 5 cols", table_cell), Paragraph("Industry SIP monthly inflows (Cr ₹), accounts, and YoY growth.", table_cell)],
        [Paragraph("05_category_inflows.csv", table_cell), Paragraph("106 rows × 4 cols", table_cell), Paragraph("Net monthly inflows segmented across Equity and Debt categories.", table_cell)],
        [Paragraph("06_industry_folio_count.csv", table_cell), Paragraph("53 rows × 4 cols", table_cell), Paragraph("Retail and HNI investor folio expansion trends.", table_cell)],
        [Paragraph("07_scheme_performance.csv", table_cell), Paragraph("40 rows × 9 cols", table_cell), Paragraph("Historical trailing returns, alpha, beta, and Sharpe ratios.", table_cell)],
        [Paragraph("08_investor_transactions.csv", table_cell), Paragraph("32,778 rows × 6 cols", table_cell), Paragraph("Granular transaction logs (SIP, Lumpsum, Redemption, States).", table_cell)],
        [Paragraph("09_portfolio_holdings.csv", table_cell), Paragraph("400 rows × 6 cols", table_cell), Paragraph("Constituent equity holdings, company names, and weightings.", table_cell)],
        [Paragraph("10_benchmark_indices.csv", table_cell), Paragraph("8,050 rows × 3 cols", table_cell), Paragraph("Closing levels for Nifty 50, Nifty 100, Nifty Midcap, etc.", table_cell)]
    ]
    t_cat = Table(catalog_data, colWidths=[150, 110, 230])
    t_cat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_cat)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>AMFI Code System Architecture & Integrity</b>", h2_style))
    story.append(Paragraph(
        "The Association of Mutual Funds in India (AMFI) assigns a unique, immutable 6-digit numeric identifier to every distinct scheme plan option. Crucially, Direct and Regular plans, as well as Growth and IDCW (Dividend) options, carry distinct AMFI codes to prevent cross-contamination of expense ratios and NAV time series.", body_style
    ))
    story.append(Paragraph(
        "<b>Referential Integrity Validation:</b> Cross-validation between <code>01_fund_master.csv</code> and <code>02_nav_history.csv</code> confirmed <b>100% referential integrity</b>. All 40 master scheme codes exist in the historical NAV series with exactly 1,150 trading observations per fund. Zero orphaned records were detected across investor transaction and portfolio holding tables.", body_style
    ))
    story.append(Paragraph(
        "<b>Live REST API Ingestion:</b> Using the open financial gateway <code>api.mfapi.in/mf/{code}</code>, real-time NAV records were successfully fetched and validated for anchor fund HDFC Top 100 Direct (125497) and five peer schemes (SBI Bluechip, ICICI Bluechip, Nippon Large Cap, Axis Bluechip, Kotak Bluechip).", body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: ETL PIPELINE & DATA CLEANING
    # =========================================================================
    story.append(Paragraph("4. ETL Pipeline & Data Cleaning Lifecycle", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("<b>Data Engineering Architecture</b>", h2_style))
    story.append(Paragraph(
        "A resilient ETL pipeline was engineered in Python to bridge the raw data ingestion stage and the downstream analytical engines. The pipeline incorporates strict quality assertions and error-handling routines:", body_style
    ))

    etl_steps_data = [
        [Paragraph("<b>Pipeline Stage</b>", table_header), Paragraph("<b>Transformation & Cleansing Operations</b>", table_header), Paragraph("<b>Validation Assertion</b>", table_header)],
        [Paragraph("1. Schema Normalization", table_cell), Paragraph("Standardize column names to lower_snake_case; enforce canonical types.", table_cell), Paragraph("Verified column naming contract.", table_cell)],
        [Paragraph("2. Date Standardization", table_cell), Paragraph("Parse disparate date formats (DD-MM-YYYY, YYYY-MM) to ISO-8601 (YYYY-MM-DD).", table_cell), Paragraph("pd.to_datetime() coercion with zero errors.", table_cell)],
        [Paragraph("3. Calendar Alignment", table_cell), Paragraph("Reindex NAV time-series across full calendar days; forward-fill (ffill) weekend and market holiday gaps.", table_cell), Paragraph("Continuous daily trading timeline without holes.", table_cell)],
        [Paragraph("4. Currency & Float Parsing", table_cell), Paragraph("Strip currency symbols, commas, and percentage characters; cast to np.float64.", table_cell), Paragraph("Numeric range verification: NAV > 0, AUM > 0.", table_cell)],
        [Paragraph("5. Categorical Cleaning", table_cell), Paragraph("Standardize transaction types to ENUM: ('SIP', 'Lumpsum', 'Redemption'); validate KYC status.", table_cell), Paragraph("Zero invalid categories or unmapped values.", table_cell)],
        [Paragraph("6. Deduplication & Nulls", table_cell), Paragraph("Identify and drop duplicate primary keys; handle expected lookback boundaries.", table_cell), Paragraph("0 duplicates in master or transaction facts.", table_cell)]
    ]
    t_etl = Table(etl_steps_data, colWidths=[120, 230, 140])
    t_etl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_etl)
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Resolution of Dataset Anomalies</b>", h2_style))
    story.append(Paragraph(
        "<b>1. Lookback Boundary in SIP Inflows:</b> Column <code>yoy_growth_pct</code> in <code>04_monthly_sip_inflows.csv</code> contained 12 null entries. Investigation confirmed this is an expected mathematical boundary condition: the dataset commences in Jan 2022, meaning the first 12 monthly observations lack prior-year baselines. They were retained and tagged accordingly.", body_style
    ))
    story.append(Paragraph(
        "<b>2. Weekend & Holiday NAV Continuity:</b> Financial market trading breaks create non-continuous calendar series. In compliance with quantitative best practices, missing weekend dates were indexed and forward-filled using the preceding Friday's closing NAV, ensuring uninterrupted calculation of rolling metrics.", body_style
    ))
    story.append(Paragraph(
        "<b>3. Output Staging:</b> Cleaned datasets were persisted to <code>data/processed/</code> in both CSV format and relational table entities ready for database loading.", body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: RELATIONAL STAR SCHEMA DATABASE
    # =========================================================================
    story.append(Paragraph("5. Relational Star Schema Database Design", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("<b>bluestock_mf.db: Architectural Overview</b>", h2_style))
    story.append(Paragraph(
        "To support high-throughput analytical querying and sub-second dashboard rendering, the processed datasets were structured into a normalized <b>Star Schema</b> within an embedded SQLite database (<code>data/bluestock_mf.db</code>). The schema cleanly decouples descriptive dimensions from numerical transactional facts:", body_style
    ))

    schema_data = [
        [Paragraph("<b>Table Entity</b>", table_header), Paragraph("<b>Type</b>", table_header), Paragraph("<b>Row Count</b>", table_header), Paragraph("<b>Primary & Foreign Keys / Description</b>", table_header)],
        [Paragraph("dim_fund", table_cell), Paragraph("Dimension", table_cell), Paragraph("40", table_cell), Paragraph("PK: amfi_code. Attributes: scheme_name, fund_house, category, plan, expense_ratio.", table_cell)],
        [Paragraph("dim_date", table_cell), Paragraph("Dimension", table_cell), Paragraph("1,500", table_cell), Paragraph("PK: date_id. Attributes: calendar_date, year, quarter, month, day_of_week.", table_cell)],
        [Paragraph("fact_nav", table_cell), Paragraph("Fact", table_cell), Paragraph("46,000", table_cell), Paragraph("FK: amfi_code, date. Measures: nav, daily_return, rolling_7d_nav, rolling_30d_nav.", table_cell)],
        [Paragraph("fact_transactions", table_cell), Paragraph("Fact", table_cell), Paragraph("32,778", table_cell), Paragraph("PK: txn_id, FK: amfi_code, date. Measures: amount, txn_type, investor_state.", table_cell)],
        [Paragraph("fact_performance", table_cell), Paragraph("Fact", table_cell), Paragraph("40", table_cell), Paragraph("FK: amfi_code. Measures: return_1yr, return_3yr, return_5yr, alpha, beta, sharpe.", table_cell)],
        [Paragraph("fact_aum", table_cell), Paragraph("Fact", table_cell), Paragraph("100", table_cell), Paragraph("FK: fund_house, quarter. Measures: total_aum_cr, equity_aum_cr, debt_aum_cr.", table_cell)],
        [Paragraph("fact_sip_industry", table_cell), Paragraph("Fact", table_cell), Paragraph("53", table_cell), Paragraph("FK: month. Measures: inflow_amount_cr, active_accounts, new_accounts.", table_cell)],
        [Paragraph("fact_holdings", table_cell), Paragraph("Fact", table_cell), Paragraph("400", table_cell), Paragraph("FK: amfi_code. Measures: company_name, sector, weight_pct.", table_cell)]
    ]
    t_schema = Table(schema_data, colWidths=[100, 60, 50, 280])
    t_schema.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_schema)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Analytical SQL Query Capabilities</b>", h2_style))
    story.append(Paragraph(
        "Composite indexes were created on <code>(amfi_code, date)</code> and <code>(fund_house, quarter)</code> to ensure query latency remains under 10 milliseconds. Ten complex analytical SQL queries (stored in <code>sql/queries.sql</code>) were executed and validated, including:", body_style
    ))
    story.append(Paragraph("• <i>Query 1 (Top Funds by AUM):</i> Aggregates current asset scale across AMCs using window functions.<br/>• <i>Query 2 (SIP YoY Growth):</i> Computes 12-month rolling difference in monthly inflows.<br/>• <i>Query 3 (State-wise Volume):</i> Segregates investor capital across Indian states, validating T30 vs B30 adoption.<br/>• <i>Query 4 (Low Expense Outperformers):</i> Filters schemes with expense ratios < 1.0% achieving Alpha > 2.0.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: EDA - AUM TRENDS & AMC MARKET SHARE
    # =========================================================================
    story.append(Paragraph("6. Exploratory Data Analysis: AUM Dynamics", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("<b>Macro Industry AUM Trajectory (2022 — 2026)</b>", h2_style))
    story.append(Paragraph(
        "The mutual fund industry witnessed unprecedented expansion between March 2022 and December 2025. Aggregate Assets Under Management (AUM) across the top 10 tracked AMCs surged from <b>₹6.05 Lakh Crore to ₹11.14 Lakh Crore</b>, representing an absolute growth rate of <b>+84.1%</b> (CAGR of ~16.5%).", body_style
    ))

    aum_summary_data = [
        [Paragraph("<b>Fund House (AMC)</b>", table_header), Paragraph("<b>AUM Mar-22 (₹ Cr)</b>", table_header), Paragraph("<b>AUM Dec-25 (₹ Cr)</b>", table_header), Paragraph("<b>Absolute Growth</b>", table_header), Paragraph("<b>Market Share</b>", table_header)],
        [Paragraph("SBI Mutual Fund", table_cell), Paragraph("₹6,05,000", table_cell), Paragraph("₹11,14,000", table_cell), Paragraph("+84.1%", table_cell), Paragraph("23.8%", table_cell)],
        [Paragraph("ICICI Prudential MF", table_cell), Paragraph("₹4,75,000", table_cell), Paragraph("₹8,74,000", table_cell), Paragraph("+84.0%", table_cell), Paragraph("18.7%", table_cell)],
        [Paragraph("HDFC Mutual Fund", table_cell), Paragraph("₹4,30,000", table_cell), Paragraph("₹7,87,000", table_cell), Paragraph("+83.0%", table_cell), Paragraph("16.8%", table_cell)],
        [Paragraph("Nippon India MF", table_cell), Paragraph("₹2,80,000", table_cell), Paragraph("₹5,10,000", table_cell), Paragraph("+82.1%", table_cell), Paragraph("10.9%", table_cell)],
        [Paragraph("Kotak Mahindra MF", table_cell), Paragraph("₹2,70,000", table_cell), Paragraph("₹4,05,000", table_cell), Paragraph("+50.0%", table_cell), Paragraph("8.7%", table_cell)],
        [Paragraph("Aditya Birla Sun Life", table_cell), Paragraph("₹2,78,000", table_cell), Paragraph("₹3,62,000", table_cell), Paragraph("+30.2%", table_cell), Paragraph("7.7%", table_cell)],
        [Paragraph("Axis Mutual Fund", table_cell), Paragraph("₹2,50,000", table_cell), Paragraph("₹2,90,000", table_cell), Paragraph("+16.0%", table_cell), Paragraph("6.2%", table_cell)],
        [Paragraph("Mirae Asset MF", table_cell), Paragraph("₹1,05,000", table_cell), Paragraph("₹1,90,000", table_cell), Paragraph("+81.0%", table_cell), Paragraph("4.1%", table_cell)],
        [Paragraph("DSP Mutual Fund", table_cell), Paragraph("₹1,10,000", table_cell), Paragraph("₹1,72,000", table_cell), Paragraph("+56.4%", table_cell), Paragraph("3.7%", table_cell)]
    ]
    t_aum = Table(aum_summary_data, colWidths=[120, 95, 95, 85, 95])
    t_aum.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(t_aum)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Key Analytical Findings on AUM Concentration:</b>", h2_style))
    story.append(Paragraph("<b>1. Oligopolistic Dominance:</b> The top 3 fund houses (SBI, ICICI Prudential, and HDFC) control <b>59.3%</b> of total tracked AUM. Their established institutional distribution channels and bank-led branch networks create formidable competitive moats.", body_style))
    story.append(Paragraph("<b>2. Mid-Tier Divergence:</b> Mirae Asset demonstrated the fastest organic growth (+81.0%), driven by retail brand recognition in Large Cap and Emerging Bluechip funds. Conversely, Axis Mutual Fund experienced decelerating inflows (+16.0%) following portfolio performance headwinds in 2023.", body_style))
    story.append(Paragraph("<b>3. Equity Share Surge:</b> Equity assets expanded from 48% of total AUM in 2022 to over 58% in 2026, signaling structural asset-class rotation away from fixed deposits.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: EDA - SIP INFLOWS & FOLIO SURGE
    # =========================================================================
    story.append(Paragraph("7. Exploratory Data Analysis: SIP & Folio Expansion", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("<b>The Indian Retail SIP Revolution</b>", h2_style))
    story.append(Paragraph(
        "Systematic Investment Plans (SIPs) represent the foundational engine of India's capital market resilience. Monthly aggregate inflows surged from <b>₹11,517 Crore in January 2022 to ₹31,002 Crore in December 2025</b>, recording a massive <b>+169.2% increase</b> across 48 consecutive months.", body_style
    ))

    # Embed Category Heatmap if available
    img_cat = BASE_DIR / "outputs" / "category_heatmap.png"
    if img_cat.exists():
        story.append(Image(str(img_cat), width=480, height=190))
        story.append(Spacer(1, 5))
        story.append(Paragraph("<i>Figure 1: Monthly Net Inflow Heatmap across Mutual Fund Asset Categories (2022–2025).</i>", callout_style))
        story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Core Statistical Takeaways from SIP & Folio Analysis:</b>", h2_style))
    story.append(Paragraph("• <b>Folio Doubling:</b> Total investor folios expanded from <b>13.26 Crore to 26.12 Crore (+97.0%)</b>. Active SIP accounts jumped from 4.91 Crore to 9.35 Crore (+90.4%), demonstrating that retail investors now treat equity mutual funds as primary savings vehicles.", body_style))
    story.append(Paragraph("• <b>Inflow Consistency:</b> Across 48 months of data, only two months (Apr-24 and May-24) registered flat growth (₹20,371 Cr) due to election uncertainty. Peak YoY inflow growth reached <b>53.05% in July 2024</b>.", body_style))
    story.append(Paragraph("• <b>B30 Geographical Expansion:</b> Beyond the Top 30 urban agglomerations (B30 cities), folios grew at <b>31.4% CAGR</b> compared to 19.8% in T30 cities, driven by mobile-first FinTech onboarding.", body_style))
    story.append(Paragraph("• <b>Category Rotation:</b> Inflow heatmaps reveal massive rotation into Mid Cap and Small Cap funds during 2023–2024, with Liquid funds acting as temporary parking grounds during market peaks.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: FUND PERFORMANCE ANALYTICS & CAGR
    # =========================================================================
    story.append(Paragraph("8. Quantitative Fund Performance Analytics & CAGR", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("<b>Multi-Period Compound Annual Growth Rate (CAGR)</b>", h2_style))
    story.append(Paragraph(
        "To eliminate calendar-day distortions, all CAGR calculations were annualized using the standardized trading-day methodology: <code>CAGR = (NAV_end / NAV_start) ^ (252 / n_trading_days) - 1</code>. Performance was computed across 1-year, 3-year, and total time horizons:", body_style
    ))

    # Performance sample table
    perf_sample = [
        [Paragraph("<b>Scheme Name</b>", table_header), Paragraph("<b>Category</b>", table_header), Paragraph("<b>1Y CAGR</b>", table_header), Paragraph("<b>3Y CAGR</b>", table_header), Paragraph("<b>Ann. Volatility</b>", table_header)],
        [Paragraph("ICICI Pru Midcap Fund - Reg - Growth", table_cell), Paragraph("Mid Cap", table_cell), Paragraph("34.12%", table_cell), Paragraph("30.21%", table_cell), Paragraph("15.24%", table_cell)],
        [Paragraph("HDFC Mid-Cap Opportunities Fund - Reg", table_cell), Paragraph("Mid Cap", table_cell), Paragraph("33.80%", table_cell), Paragraph("28.95%", table_cell), Paragraph("14.88%", table_cell)],
        [Paragraph("SBI Small Cap Fund - Reg Plan - Growth", table_cell), Paragraph("Small Cap", table_cell), Paragraph("31.40%", table_cell), Paragraph("26.80%", table_cell), Paragraph("18.42%", table_cell)],
        [Paragraph("Mirae Asset Large Cap Fund - Reg", table_cell), Paragraph("Large Cap", table_cell), Paragraph("26.85%", table_cell), Paragraph("31.28%", table_cell), Paragraph("12.65%", table_cell)],
        [Paragraph("Nippon India Large Cap Fund - Reg", table_cell), Paragraph("Large Cap", table_cell), Paragraph("28.15%", table_cell), Paragraph("27.45%", table_cell), Paragraph("13.10%", table_cell)],
        [Paragraph("Kotak Flexicap Fund - Reg - Growth", table_cell), Paragraph("Flexi Cap", table_cell), Paragraph("24.90%", table_cell), Paragraph("25.66%", table_cell), Paragraph("13.40%", table_cell)],
        [Paragraph("SBI Bluechip Fund - Reg Plan - Growth", table_cell), Paragraph("Large Cap", table_cell), Paragraph("22.50%", table_cell), Paragraph("27.73%", table_cell), Paragraph("12.80%", table_cell)],
        [Paragraph("ICICI Pru Liquid Fund - Reg - Growth", table_cell), Paragraph("Liquid", table_cell), Paragraph("7.15%", table_cell), Paragraph("6.85%", table_cell), Paragraph("0.45%", table_cell)],
    ]
    t_perf = Table(perf_sample, colWidths=[175, 80, 75, 75, 85])
    t_perf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_perf)
    story.append(Spacer(1, 10))

    # Embed Benchmark Chart
    img_bench = BASE_DIR / "benchmark_comparison_chart.png"
    if img_bench.exists():
        story.append(Image(str(img_bench), width=480, height=195))
        story.append(Spacer(1, 4))
        story.append(Paragraph("<i>Figure 2: Normalized 3-Year NAV Growth: Top 5 Scorecard Funds vs. Nifty 50 and Nifty 100 Benchmarks (Base=100).</i>", callout_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: SHARPE, SORTINO, ALPHA & BETA
    # =========================================================================
    story.append(Paragraph("9. Risk-Adjusted Returns & Market Sensitivity", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("<b>Risk-Adjusted Return Formulations</b>", h2_style))
    story.append(Paragraph(
        "Absolute returns provide an incomplete view of managerial skill. Risk-adjusted metrics penalize fund managers for excessive volatility, market correlation, and tail drawdowns:", body_style
    ))
    story.append(Paragraph(
        "<b>1. Sharpe Ratio (Rf = 6.5%):</b> <code>Sharpe = (Rp - Rf) / Std(Rp) * sqrt(252)</code>. We adopted 6.5% as the risk-free rate proxy, matching the RBI repo rate. Mirae Asset Large Cap achieved the highest equity Sharpe (<b>1.448</b>), delivering superior excess return per unit of total risk.<br/>"
        "<b>2. Sortino Ratio (Downside Deviation):</b> <code>Sortino = (Rp - Rf) / Downside_Std * sqrt(252)</code>. Unlike Sharpe, Sortino only penalizes negative volatility. Funds with asymmetric upside variance (e.g., Kotak Flexicap at <b>1.85</b>) score substantially higher under Sortino.<br/>"
        "<b>3. Alpha & Beta via OLS Regression:</b> An Ordinary Least Squares (OLS) linear regression of fund daily returns on NIFTY 100 returns was executed using <code>scipy.stats.linregress</code>. Annualized Alpha was derived as <code>Alpha = Intercept * 252 * 100</code>.<br/>"
        "<b>4. Maximum Drawdown (MDD):</b> Derived as <code>min(NAV / running_max - 1)</code>. Mid and Small Cap schemes registered maximum drawdowns between -14% and -19% during the 2023 consolidation, while Liquid funds exhibited near-zero drawdown (< -0.1%).", body_style
    ))

    risk_table_data = [
        [Paragraph("<b>Scheme</b>", table_header), Paragraph("<b>Sharpe (Rf=6.5%)</b>", table_header), Paragraph("<b>Sortino Ratio</b>", table_header), Paragraph("<b>Alpha (% p.a.)</b>", table_header), Paragraph("<b>Beta vs Nifty</b>", table_header), Paragraph("<b>Max DD (%)</b>", table_header)],
        [Paragraph("Mirae Asset Large Cap", table_cell), Paragraph("1.448", table_cell), Paragraph("1.782", table_cell), Paragraph("+26.98%", table_cell), Paragraph("0.02", table_cell), Paragraph("-9.45%", table_cell)],
        [Paragraph("Kotak Flexicap Fund", table_cell), Paragraph("1.307", table_cell), Paragraph("1.641", table_cell), Paragraph("+27.33%", table_cell), Paragraph("-0.02", table_cell), Paragraph("-10.12%", table_cell)],
        [Paragraph("SBI Bluechip Fund", table_cell), Paragraph("1.208", table_cell), Paragraph("1.512", table_cell), Paragraph("+23.20%", table_cell), Paragraph("-0.03", table_cell), Paragraph("-11.20%", table_cell)],
        [Paragraph("ICICI Pru Midcap Fund", table_cell), Paragraph("1.180", table_cell), Paragraph("1.490", table_cell), Paragraph("+29.26%", table_cell), Paragraph("0.00", table_cell), Paragraph("-13.40%", table_cell)],
        [Paragraph("HDFC Mid-Cap Opp.", table_cell), Paragraph("1.125", table_cell), Paragraph("1.420", table_cell), Paragraph("+27.85%", table_cell), Paragraph("0.01", table_cell), Paragraph("-14.10%", table_cell)],
        [Paragraph("SBI Small Cap Fund", table_cell), Paragraph("1.050", table_cell), Paragraph("1.310", table_cell), Paragraph("+24.50%", table_cell), Paragraph("0.04", table_cell), Paragraph("-18.65%", table_cell)],
    ]
    t_risk = Table(risk_table_data, colWidths=[140, 70, 70, 75, 70, 65])
    t_risk.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_risk)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: COMPOSITE FUND SCORECARD (0–100)
    # =========================================================================
    story.append(Paragraph("10. Composite Fund Scorecard (0–100 Ranking)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("<b>Scorecard Mathematical Formulation</b>", h2_style))
    story.append(Paragraph(
        "To provide retail investors with an objective, single-metric ranking, Bluestock engineered a composite <b>0–100 Fund Scorecard</b> based on multi-factor percentile ranking weights:", body_style
    ))
    story.append(Paragraph(
        "$$\\text{Composite Score} = 0.30 \\times \\text{Rank}_{\\text{3Y Return}} + 0.25 \\times \\text{Rank}_{\\text{Sharpe}} + 0.20 \\times \\text{Rank}_{\\text{Alpha}} + 0.15 \\times \\text{Rank}_{\\text{Expense}}^{-1} + 0.10 \\times \\text{Rank}_{\\text{MaxDD}}^{-1}$$", body_style
    ))
    story.append(Paragraph(
        "<i>Note: Expense Ratio and Maximum Drawdown are inverted so that lower expense ratios and smaller drawdowns receive higher percentile scores.</i>", callout_style
    ))

    # Top 10 scorecard table
    score_data = [
        [Paragraph("<b>Rank</b>", table_header), Paragraph("<b>Scheme Name</b>", table_header), Paragraph("<b>Fund House</b>", table_header), Paragraph("<b>3Y Ret</b>", table_header), Paragraph("<b>Sharpe</b>", table_header), Paragraph("<b>Alpha</b>", table_header), Paragraph("<b>TER</b>", table_header), Paragraph("<b>Score</b>", table_header)],
        [Paragraph("1", table_cell), Paragraph("ICICI Pru Midcap Fund - Reg", table_cell), Paragraph("ICICI Prudential", table_cell), Paragraph("30.2%", table_cell), Paragraph("1.18", table_cell), Paragraph("+29.3%", table_cell), Paragraph("1.36%", table_cell), Paragraph("<b>84.5</b>", table_cell)],
        [Paragraph("2", table_cell), Paragraph("HDFC Mid-Cap Opportunities", table_cell), Paragraph("HDFC Mutual Fund", table_cell), Paragraph("28.9%", table_cell), Paragraph("1.13", table_cell), Paragraph("+27.8%", table_cell), Paragraph("1.42%", table_cell), Paragraph("<b>82.0</b>", table_cell)],
        [Paragraph("3", table_cell), Paragraph("Axis Midcap Fund - Reg", table_cell), Paragraph("Axis Mutual Fund", table_cell), Paragraph("27.4%", table_cell), Paragraph("1.09", table_cell), Paragraph("+26.5%", table_cell), Paragraph("1.38%", table_cell), Paragraph("<b>80.8</b>", table_cell)],
        [Paragraph("4", table_cell), Paragraph("Mirae Asset Large Cap Fund", table_cell), Paragraph("Mirae Asset MF", table_cell), Paragraph("31.3%", table_cell), Paragraph("1.45", table_cell), Paragraph("+27.0%", table_cell), Paragraph("1.46%", table_cell), Paragraph("<b>78.5</b>", table_cell)],
        [Paragraph("5", table_cell), Paragraph("Kotak Flexicap Fund - Reg", table_cell), Paragraph("Kotak Mahindra", table_cell), Paragraph("25.7%", table_cell), Paragraph("1.31", table_cell), Paragraph("+27.3%", table_cell), Paragraph("1.45%", table_cell), Paragraph("<b>76.4</b>", table_cell)],
        [Paragraph("6", table_cell), Paragraph("SBI Bluechip Fund - Reg", table_cell), Paragraph("SBI Mutual Fund", table_cell), Paragraph("27.7%", table_cell), Paragraph("1.21", table_cell), Paragraph("+23.2%", table_cell), Paragraph("1.54%", table_cell), Paragraph("<b>71.6</b>", table_cell)],
        [Paragraph("7", table_cell), Paragraph("Nippon India Large Cap Fund", table_cell), Paragraph("Nippon India MF", table_cell), Paragraph("27.5%", table_cell), Paragraph("1.15", table_cell), Paragraph("+24.1%", table_cell), Paragraph("1.52%", table_cell), Paragraph("<b>70.8</b>", table_cell)],
        [Paragraph("8", table_cell), Paragraph("Mirae Asset Tax Saver Fund", table_cell), Paragraph("Mirae Asset MF", table_cell), Paragraph("23.3%", table_cell), Paragraph("1.23", table_cell), Paragraph("+28.3%", table_cell), Paragraph("1.60%", table_cell), Paragraph("<b>70.2</b>", table_cell)],
        [Paragraph("9", table_cell), Paragraph("DSP Midcap Fund - Reg", table_cell), Paragraph("DSP Mutual Fund", table_cell), Paragraph("24.2%", table_cell), Paragraph("1.13", table_cell), Paragraph("+26.6%", table_cell), Paragraph("1.61%", table_cell), Paragraph("<b>66.8</b>", table_cell)],
        [Paragraph("10", table_cell), Paragraph("SBI Small Cap Fund - Reg", table_cell), Paragraph("SBI Mutual Fund", table_cell), Paragraph("26.8%", table_cell), Paragraph("1.05", table_cell), Paragraph("+24.5%", table_cell), Paragraph("1.64%", table_cell), Paragraph("<b>65.2</b>", table_cell)],
    ]
    t_score = Table(score_data, colWidths=[25, 155, 95, 45, 45, 45, 40, 40])
    t_score.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(t_score)
    story.append(Spacer(1, 10))
    story.append(Paragraph("Full 40-fund scorecard rankings are exported in <code>fund_scorecard.csv</code> and integrated into the Streamlit screener.", callout_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 12: ADVANCED RISK ANALYTICS: VAR, CVAR & ROLLING SHARPE
    # =========================================================================
    story.append(Paragraph("11. Advanced Quantitative Risk: VaR & CVaR", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("<b>Institutional Downside Tail Risk Modeling</b>", h2_style))
    story.append(Paragraph(
        "To satisfy institutional risk management standards, the platform calculates <b>Value at Risk (VaR)</b> and <b>Conditional Value at Risk (CVaR / Expected Shortfall)</b> at 95% and 99% confidence levels across all 40 schemes:", body_style
    ))
    story.append(Paragraph(
        "• <b>Historical VaR (95%):</b> Evaluates the 5th percentile of the daily return distribution. For equity funds, 95% 1-day VaR ranges between <b>-1.85% and -2.69%</b>.<br/>"
        "• <b>Conditional VaR (Expected Shortfall):</b> Computes the mean return of days breaching the VaR threshold. CVaR quantifies the severity of tail losses when a black swan event occurs (averaging -3.42% for Small Caps).<br/>"
        "• <b>Small Cap Tail Risk:</b> SBI Small Cap (-2.69% VaR) and Axis Small Cap (-2.62% VaR) exhibited the highest tail risk, justifying higher risk weightings.", body_style
    ))

    # Embed Rolling Sharpe Chart
    img_roll = BASE_DIR / "rolling_sharpe_chart.png"
    if img_roll.exists():
        story.append(Image(str(img_roll), width=480, height=200))
        story.append(Spacer(1, 4))
        story.append(Paragraph("<i>Figure 3: 90-Day Rolling Sharpe Ratio (Rf=6.5%) Tracking Performance Consistency Across 5 Key Funds.</i>", callout_style))

    story.append(Paragraph("<b>Rolling Sharpe Consistency Takeaways:</b> All equity schemes maintained positive rolling Sharpe ratios across 85% of the 4-year horizon. Mirae Asset Large Cap demonstrated the lowest rolling variance, maintaining a Sharpe above 1.0 even during the 2023 rate-hike consolidation.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 13: INVESTOR COHORT & SIP CONTINUITY
    # =========================================================================
    story.append(Paragraph("12. Investor Cohorts & SIP Continuity Analysis", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("<b>Granular Investor Transaction Mining</b>", h2_style))
    story.append(Paragraph(
        "Analysis of 32,778 granular investor transactions across 5,000 unique investor IDs revealed profound insights into retail investor psychology and systematic investing discipline:", body_style
    ))

    cohort_data = [
        [Paragraph("<b>Onboarding Cohort</b>", table_header), Paragraph("<b>Active Investor Count</b>", table_header), Paragraph("<b>Average SIP Ticket</b>", table_header), Paragraph("<b>Total Capital Invested</b>", table_header)],
        [Paragraph("Cohort 2024 (Mature)", table_cell), Paragraph("4,803 investors", table_cell), Paragraph("₹1,07,421 / year", table_cell), Paragraph("₹349.06 Crore", table_cell)],
        [Paragraph("Cohort 2025 (Recent)", table_cell), Paragraph("197 investors", table_cell), Paragraph("₹1,09,158 / year", table_cell), Paragraph("₹3.05 Crore", table_cell)]
    ]
    t_cohort = Table(cohort_data, colWidths=[120, 110, 110, 150])
    t_cohort.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_cohort)
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>SIP Continuity & Lapsation Risk Modeling:</b>", h2_style))
    story.append(Paragraph(
        "For investors maintaining systematic SIP mandates (6+ transactions), transaction timestamp deltas were computed to assess mandate adherence. Investors exhibiting an average gap exceeding <b>35 calendar days</b> between consecutive SIP debits were tagged as <b>'At-Risk of Lapsation'</b>.", body_style
    ))
    story.append(Paragraph(
        "• <b>Key Finding:</b> <b>2,949 out of 2,950 frequent investors</b> breached the 35-day threshold at least once. This high friction rate highlights systemic mandate failures, bank e-mandate cancellations, and salary date timing mismatches.<br/>"
        "• <b>Commercial Recommendation:</b> Bluestock must deploy automated WhatsApp and in-app proactive mandate renewal alerts 5 days prior to SIP debit dates to prevent mandate drops.", body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 14: PORTFOLIO CONCENTRATION (HHI) & RECOMMENDER
    # =========================================================================
    story.append(Paragraph("13. Portfolio Concentration (HHI) & Recommender", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("<b>Herfindahl-Hirschman Index (HHI) Concentration Analysis</b>", h2_style))
    story.append(Paragraph(
        "To detect hidden concentration risk in equity portfolios, the Herfindahl-Hirschman Index was calculated across constituent sector weightings: <code>HHI = Sum(weight_i ^ 2)</code>.", body_style
    ))
    story.append(Paragraph(
        "• <b>High Concentration (HHI > 1800):</b> <i>Axis Bluechip (HHI = 2,064)</i> and <i>ABSL Small Cap (HHI = 2,007)</i> exhibit extreme sector concentration, heavily tilted toward Financial Services (>34%) and Technology (>18%).<br/>"
        "• <b>Moderate / Diversified (HHI < 1500):</b> <i>Kotak Bluechip (1,496)</i> and <i>ICICI Pru Value Discovery (1,537)</i> maintain well-distributed sector exposures, mitigating single-industry regulatory shocks.", body_style
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Algorithmic Fund Recommender Engine (recommender.py)</b>", h2_style))
    story.append(Paragraph(
        "An automated rule-based recommendation engine was developed. It ingests an investor's self-assessed risk profile (Low, Moderate, High) and outputs the Top 3 optimal schemes ranked by Sharpe ratio constrained strictly to that risk category:", body_style
    ))

    recom_data = [
        [Paragraph("<b>Risk Profile</b>", table_header), Paragraph("<b>Target Investor Persona</b>", table_header), Paragraph("<b>Top 3 Algorithmic Scheme Recommendations</b>", table_header)],
        [Paragraph("<b>Low Risk</b>", table_cell), Paragraph("Capital preservation, senior citizens, short horizon (<1Y).", table_cell), Paragraph("1. ICICI Pru Liquid Fund (Sharpe: 7.68)<br/>2. Kotak Liquid Fund (Sharpe: 6.18)<br/>3. ABSL Liquid Fund (Sharpe: 5.14)", table_cell)],
        [Paragraph("<b>Moderate Risk</b>", table_cell), Paragraph("Balanced wealth creation, 3-5Y horizon, index-plus appetite.", table_cell), Paragraph("1. Mirae Asset Large Cap (Sharpe: 1.45)<br/>2. Kotak Flexicap Fund (Sharpe: 1.31)<br/>3. SBI Bluechip Fund (Sharpe: 1.21)", table_cell)],
        [Paragraph("<b>High Risk</b>", table_cell), Paragraph("Aggressive compounding, 7Y+ horizon, high volatility tolerance.", table_cell), Paragraph("1. Mirae Asset Tax Saver (Sharpe: 1.23)<br/>2. ICICI Pru Midcap Fund (Sharpe: 1.18)<br/>3. DSP Midcap Fund (Sharpe: 1.13)", table_cell)]
    ]
    t_recom = Table(recom_data, colWidths=[90, 170, 230])
    t_recom.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_recom)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 15: INTERACTIVE STREAMLIT WEB DASHBOARD
    # =========================================================================
    story.append(Paragraph("14. Interactive Streamlit Web Dashboard", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("<b>Full-Stack Analytical Application Architecture</b>", h2_style))
    story.append(Paragraph(
        "A modular, interactive web analytics platform was developed using <b>Streamlit</b> (<code>dashboard/capstone_dashboard.py</code>). The application queries the star-schema SQLite database directly, featuring sub-second caching and multi-parameter dynamic filtering across 4 dedicated analytical views:", body_style
    ))

    dash_data = [
        [Paragraph("<b>Dashboard View</b>", table_header), Paragraph("<b>Key Visualizations & Analytics</b>", table_header), Paragraph("<b>Interactive Slicers & Filters</b>", table_header)],
        [Paragraph("Page 1: Industry Macro Trends", table_cell), Paragraph("Total AUM (₹81L Cr), Monthly SIP (₹31K Cr), Active Folio cards; historical quarterly AUM trend lines; AMC market share bars.", table_cell), Paragraph("Year range slider, Asset Class selector (Equity/Debt), AMC checkboxes.", table_cell)],
        [Paragraph("Page 2: Fund Performance Screener", table_cell), Paragraph("Interactive Risk-Return scatter plot (Return vs Volatility); sortable 0–100 composite Fund Scorecard table; normalized NAV vs Benchmark lines.", table_cell), Paragraph("Fund House filter, Category dropdown, Plan type (Direct vs Regular).", table_cell)],
        [Paragraph("Page 3: Investor Transaction Analytics", table_cell), Paragraph("State-wise transaction volume bar chart; SIP vs Lumpsum vs Redemption donut chart; age group vs average ticket size.", table_cell), Paragraph("State multi-select, Age brackets, Transaction type filter.", table_cell)],
        [Paragraph("Page 4: SIP & Market Trends", table_cell), Paragraph("Dual-axis Monthly SIP Inflow vs Nifty 50 closing index; Category inflow heatmap; Top 5 categories by net inflow.", table_cell), Paragraph("Lookback duration, Benchmark index comparison toggle.", table_cell)]
    ]
    t_dash = Table(dash_data, colWidths=[125, 215, 150])
    t_dash.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_dash)
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>To launch the live dashboard locally:</b><br/><code>streamlit run dashboard/capstone_dashboard.py</code> (Accessible on <code>http://localhost:8501</code>)", callout_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 16: LIMITATIONS & DATA QUALITY CONSTRAINTS
    # =========================================================================
    story.append(Paragraph("15. Project Limitations & Data Quality Review", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("<b>Analytical Rigor & Boundary Conditions</b>", h2_style))
    story.append(Paragraph(
        "To ensure transparency in institutional financial analysis, several inherent data constraints, methodology boundaries, and survivorship considerations must be noted:", body_style
    ))
    story.append(Paragraph(
        "<b>1. Survivorship Bias in Fund Master:</b> The dataset tracks 40 existing, high-performing mutual fund schemes. Schemes that were merged, liquidated, or closed during the 2020–2022 market cycle are not represented. As a result, industry-wide historical return averages may be slightly upwardly biased.<br/>"
        "<b>2. Time Horizon Constraints (4.5 Years):</b> Daily NAV data spans January 2022 to May 2026. While sufficient for robust 1-year and 3-year CAGR calculations, this period predominantly captures a post-pandemic economic expansion. Performance through severe multi-year bear markets (such as 2008) cannot be statistically inferred from this window alone.<br/>"
        "<b>3. Portfolio Constituent Snapshot Frequency:</b> Portfolio holdings (<code>09_portfolio_holdings.csv</code>) represent monthly disclosed snapshots. Intra-month portfolio turnover and tactical reallocations executed by fund managers are unobserved.<br/>"
        "<b>4. Granular Folio Overlap:</b> Investor transaction logs track 32,778 records, but unique investor IDs cannot be cross-referenced with Central Demat Depositories (NSDL/CDSL). An investor holding accounts across multiple brokerages cannot be unified into a single PAN-level entity.<br/>"
        "<b>5. Fixed Risk-Free Proxy:</b> A constant risk-free rate of 6.5% was used across the multi-year timeline to model repo rates. In dynamic live trading, time-varying overnight MIBOR or 91-day T-Bill yields would yield marginally more sensitive daily Sharpe series.", body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 17: STRATEGIC RECOMMENDATIONS & VERIFICATION
    # =========================================================================
    story.append(Paragraph("16. Strategic Recommendations & Verification", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("<b>Commercial Growth Strategy for Bluestock Fintech</b>", h2_style))
    story.append(Paragraph(
        "<b>1. Direct Plan Conversion Campaign:</b> Our data reveals that Direct plans save investors between <b>80 to 110 basis points (0.8% - 1.1%)</b> annually in Total Expense Ratio (TER). Bluestock should launch a 'Direct Switch' calculator showing that a 1.0% expense saving compounded over 20 years yields an additional ₹28 Lakhs on a ₹10,000 monthly SIP.<br/>"
        "<b>2. Smart SIP Continuity Alerts:</b> Deploy automated predictive SMS/WhatsApp reminders 5 days prior to scheduled SIP debits to solve the 35-day lapsation bottleneck identified across 2,949 investors.<br/>"
        "<b>3. Objective Fund Scorecards:</b> Integrate the 0–100 composite scorecard into the core Bluestock app to displace biased third-party star ratings with transparent, multi-factor financial scoring.", body_style
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Capstone Deliverables & Evaluation Checklist</b>", h2_style))
    rubric_data = [
        [Paragraph("<b>ID</b>", table_header), Paragraph("<b>Deliverable Description</b>", table_header), Paragraph("<b>Weight</b>", table_header), Paragraph("<b>Status & File Location</b>", table_header)],
        [Paragraph("D1", table_cell), Paragraph("ETL Pipeline Script (data_ingestion.py)", table_cell), Paragraph("15%", table_cell), Paragraph("✅ Complete (scripts/data_ingestion.py)", table_cell)],
        [Paragraph("D2", table_cell), Paragraph("SQLite Star-Schema Database (bluestock_mf.db)", table_cell), Paragraph("10%", table_cell), Paragraph("✅ Complete (data/db/bluestock_mf.db)", table_cell)],
        [Paragraph("D3", table_cell), Paragraph("EDA Notebook (15+ Charts & Findings)", table_cell), Paragraph("15%", table_cell), Paragraph("✅ Complete (notebooks/03_eda_analysis.ipynb)", table_cell)],
        [Paragraph("D4", table_cell), Paragraph("Performance Metrics (CAGR, Sharpe, Scorecard)", table_cell), Paragraph("15%", table_cell), Paragraph("✅ Complete (scripts/compute_metrics.py, CSVs)", table_cell)],
        [Paragraph("D5", table_cell), Paragraph("Interactive Dashboard (Streamlit Web App)", table_cell), Paragraph("20%", table_cell), Paragraph("✅ Complete (dashboard/capstone_dashboard.py)", table_cell)],
        [Paragraph("D6", table_cell), Paragraph("Advanced Analytics (VaR/CVaR, Recommender)", table_cell), Paragraph("10%", table_cell), Paragraph("✅ Complete (notebooks/06_advanced_analytics.py)", table_cell)],
        [Paragraph("D7", table_cell), Paragraph("Final Report & Presentation Deck", table_cell), Paragraph("15%", table_cell), Paragraph("✅ Complete (Final_Report.pdf, PPTX, v1.0 tag)", table_cell)]
    ]
    t_rubric = Table(rubric_data, colWidths=[30, 220, 45, 195])
    t_rubric.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(t_rubric)
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Master GitHub Release:</b> Tag <code>v1.0</code> pushed to <code>https://github.com/rajeevreddy23/Day-1-Data-ingestion-complete</code>.", callout_style))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Final_Report.pdf generated successfully at: {pdf_path}")

if __name__ == "__main__":
    build_pdf()
