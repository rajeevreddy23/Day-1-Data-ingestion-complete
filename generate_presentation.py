"""
Script to generate the executive 12-slide PowerPoint deck:
Bluestock_MF_Presentation.pptx
Meets all exact capstone requirements:
1. Title
2. Problem & Objective
3. Data Sources
4. Architecture
5. EDA Highlights (Part 1)
6. EDA Highlights (Part 2)
7. Performance Metrics (Part 1)
8. Performance Metrics (Part 2)
9. Dashboard Screenshots (Part 1)
10. Dashboard Screenshots (Part 2)
11. Key Findings & Recommendations
12. Thank You
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = r"C:\blue\drive-download-20260902T170546Z-1-001"
PPTX_PATH = os.path.join(BASE_DIR, "Bluestock_MF_Presentation.pptx")
PPTX_ALT_PATH = os.path.join(BASE_DIR, "Bluestock_MF_Analytics_Capstone_Presentation.pptx")

# Corporate Color Palette
NAVY_DARK = RGBColor(15, 37, 55)      # #0F2537
NAVY_PRIMARY = RGBColor(26, 54, 93)   # #1A365D
BLUE_ACCENT = RGBColor(2, 132, 199)   # #0284C7
GRAY_LIGHT = RGBColor(248, 250, 252)  # #F8FAFC
GRAY_BORDER = RGBColor(226, 232, 240) # #E2E8F0
TEXT_DARK = RGBColor(30, 41, 59)      # #1E293B
TEXT_MUTED = RGBColor(100, 116, 139)  # #64748B
WHITE = RGBColor(255, 255, 255)
GREEN_ACCENT = RGBColor(22, 163, 74)  # #16A34A

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank slide

    def add_header(slide, title_text, category_text="BLUESTOCK FINTECH • MUTUAL FUND ANALYTICS CAPSTONE"):
        # Top banner background
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = NAVY_DARK
        top_bar.line.fill.background()

        # Accent line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.1), Inches(13.333), Inches(0.06))
        line.fill.solid()
        line.fill.fore_color.rgb = BLUE_ACCENT
        line.line.fill.background()

        # Category text
        tx_box_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.5), Inches(0.3))
        tf_cat = tx_box_cat.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = "Arial"
        p_cat.font.size = Pt(9)
        p_cat.font.bold = True
        p_cat.font.color.rgb = BLUE_ACCENT

        # Title text
        tx_box_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.5), Inches(0.6))
        tf_title = tx_box_title.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = "Arial"
        p_title.font.size = Pt(20)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE

        # Slide Footer
        footer = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.1), Inches(13.333), Inches(0.4))
        footer.fill.solid()
        footer.fill.fore_color.rgb = GRAY_LIGHT
        footer.line.color.rgb = GRAY_BORDER

        tx_foot = slide.shapes.add_textbox(Inches(0.8), Inches(7.15), Inches(11.5), Inches(0.3))
        p_foot = tx_foot.text_frame.paragraphs[0]
        p_foot.text = "Confidential • Bluestock Fintech Analytics • Group: 62FMBF • Author: Rajeev Reddy"
        p_foot.font.name = "Arial"
        p_foot.font.size = Pt(8.5)
        p_foot.font.color.rgb = TEXT_MUTED

    def add_card(slide, left, top, width, height, title, bg_color=WHITE, border_color=GRAY_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)

        # Card header text
        if title:
            tx_box = slide.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.15), Inches(width - 0.4), Inches(0.45))
            tf = tx_box.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = "Arial"
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = NAVY_PRIMARY
        return card

    # =========================================================================
    # SLIDE 1: Title
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY_DARK
    bg1.line.fill.background()

    # Title Card
    tx1 = slide1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11), Inches(2.2))
    tf1 = tx1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "BLUESTOCK FINTECH"
    p1.font.name = "Arial"
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = BLUE_ACCENT

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Mutual Fund Analytics & Intelligence Platform"
    p1_sub.font.name = "Arial"
    p1_sub.font.size = Pt(36)
    p1_sub.font.bold = True
    p1_sub.font.color.rgb = WHITE

    p1_desc = tf1.add_paragraph()
    p1_desc.text = "End-to-End Data Pipeline, Financial Risk Analytics, Scorecards & Interactive Dashboard"
    p1_desc.font.name = "Arial"
    p1_desc.font.size = Pt(15)
    p1_desc.font.color.rgb = RGBColor(203, 213, 225)

    # Metadata Card
    meta_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(4.5), Inches(10.9), Inches(1.8))
    meta_card.fill.solid()
    meta_card.fill.fore_color.rgb = NAVY_PRIMARY
    meta_card.line.color.rgb = BLUE_ACCENT

    tx_meta = slide1.shapes.add_textbox(Inches(1.5), Inches(4.7), Inches(10.3), Inches(1.4))
    tf_meta = tx_meta.text_frame
    p_m1 = tf_meta.paragraphs[0]
    p_m1.text = "CAPSTONE SPECIFICATIONS & PROJECT DETAILS"
    p_m1.font.name = "Arial"
    p_m1.font.size = Pt(11)
    p_m1.font.bold = True
    p_m1.font.color.rgb = BLUE_ACCENT

    p_m2 = tf_meta.add_paragraph()
    p_m2.text = "• Assigned To: Poulami Dutta (PO) | Rajeev Reddy (RA) | Thadakamalla Likith Kumar (TH)"
    p_m2.font.name = "Arial"
    p_m2.font.size = Pt(11.5)
    p_m2.font.color.rgb = WHITE

    p_m3 = tf_meta.add_paragraph()
    p_m3.text = "• Capstone Project I: Mutual Fund Analytics  |  Project Start Date: 01 Sep 2026  |  Final Release: v1.0"
    p_m3.font.name = "Arial"
    p_m3.font.size = Pt(11)
    p_m3.font.color.rgb = RGBColor(203, 213, 225)

    # =========================================================================
    # SLIDE 2: Problem & Objective
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "1. Executive Summary: Problem Statement & Objectives")
    
    # Left Card: Problem Statement
    add_card(slide2, 0.8, 1.4, 5.7, 5.4, "The Core Problem Statement")
    tx_p = slide2.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(5.3), Inches(4.5))
    tf_p = tx_p.text_frame
    tf_p.word_wrap = True
    bullets_p = [
        "<b>Data Fragmentation:</b> NAV, AUM, portfolio holdings, and transaction records reside across disparate AMFI portals, static CSVs, and legacy formats.",
        "<b>High Expense Ratio Traps:</b> Retail investors unknowingly forfeit 80–120 bps annually in Regular plan distributor commissions versus Direct growth plans.",
        "<b>Lagging Volatility & Drawdown Assessment:</b> Standard metric reporting focuses solely on trailing returns, ignoring peak-to-trough drawdowns and tail risk.",
        "<b>Sub-Optimal Asset Allocation:</b> Lack of algorithmic scoring leaves retail investors vulnerable to heavy sector concentration (e.g., Financials >35%)."
    ]
    for idx, b in enumerate(bullets_p):
        p = tf_p.paragraphs[0] if idx == 0 else tf_p.add_paragraph()
        p.text = b
        p.font.name = "Arial"
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(14)

    # Right Card: Objectives & Solutions
    add_card(slide2, 6.8, 1.4, 5.7, 5.4, "Strategic Objectives & Platform Solution")
    tx_o = slide2.shapes.add_textbox(Inches(7.0), Inches(2.1), Inches(5.3), Inches(4.5))
    tf_o = tx_o.text_frame
    tf_o.word_wrap = True
    bullets_o = [
        "<b>Automated Ingestion Pipeline:</b> Consolidate 10 heterogeneous AMFI datasets with live REST API extraction from mfapi.in.",
        "<b>Star Schema SQLite Warehouse:</b> Architect a high-speed relational store (bluestock_mf.db) with 10 analytical SQL views and zero FK violations.",
        "<b>Institutional Risk Engine:</b> Compute 1Y/3Y/5Y CAGR, Alpha, Beta vs Nifty 100, Sharpe, Sortino, Max Drawdown, VaR (95%), CVaR, and Sector HHI.",
        "<b>Actionable Composite Scorecard:</b> Rank all 40 schemes (0–100) and deploy an interactive multi-page Streamlit analytical dashboard."
    ]
    for idx, b in enumerate(bullets_o):
        p = tf_o.paragraphs[0] if idx == 0 else tf_o.add_paragraph()
        p.text = b
        p.font.name = "Arial"
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(14)

    # =========================================================================
    # SLIDE 3: Data Sources
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "2. Data Ingestion Architecture & Disparate Sources")

    add_card(slide3, 0.8, 1.4, 11.7, 5.4, "10 Unified AMFI Data Sources & Live API Integration")
    tx_ds = slide3.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.3), Inches(4.6))
    tf_ds = tx_ds.text_frame
    tf_ds.word_wrap = True

    datasets = [
        ("01_fund_master.csv", "40 Schemes", "Scheme metadata, AMFI code, fund house, category, plan type, TER"),
        ("02_nav_history.csv", "46,000 Records", "Daily historical NAV time series (2020–2025) across all 40 funds"),
        ("03_aum_by_fund_house.csv", "44 Fund Houses", "Total AUM, market share %, and quarterly growth rankings"),
        ("04_monthly_sip_inflows.csv", "60 Months", "Industry-wide monthly SIP mobilization figures (Rs. Crore)"),
        ("05_category_inflows.csv", "36 Months", "Net capital flows across Equity, Debt, Hybrid, and Liquid categories"),
        ("06_industry_folio_count.csv", "60 Months", "Unique investor folios tracking retail vs HNI participation trends"),
        ("07_scheme_performance.csv", "40 Schemes", "Historical 1Y, 3Y, 5Y return baselines and reported benchmark indices"),
        ("08_investor_transactions.csv", "32,778 Records", "Granular investor demographics (age, state, city tier, SIP continuity)"),
        ("09_portfolio_holdings.csv", "400+ Holdings", "Top 10 equity and debt holdings per scheme with sector weights"),
        ("10_benchmark_indices.csv", "1,250 Dates", "Daily closing price history for Nifty 50 and Nifty 100 benchmarks"),
        ("Live mfapi.in REST API", "Active Web Service", "Live automated endpoint fetching real-time NAVs and JSON metadata")
    ]

    p_d_head = tf_ds.paragraphs[0]
    p_d_head.text = "Comprehensive Ingestion Scope: 87,000+ Raw Records Cleaned, Validated & Normalized"
    p_d_head.font.name = "Arial"
    p_d_head.font.size = Pt(12)
    p_d_head.font.bold = True
    p_d_head.font.color.rgb = BLUE_ACCENT
    p_d_head.space_after = Pt(8)

    for fn, scope, detail in datasets:
        p_row = tf_ds.add_paragraph()
        p_row.text = f"• {fn:28} | {scope:16} | {detail}"
        p_row.font.name = "Consolas"
        p_row.font.size = Pt(10)
        p_row.font.color.rgb = TEXT_DARK
        p_row.space_after = Pt(2.5)

    # =========================================================================
    # SLIDE 4: Architecture
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "3. End-to-End System Architecture & Star Schema Design")

    # Pipeline Flow Cards (4 steps)
    steps = [
        ("Layer 1: Ingestion", "Raw AMFI CSVs + mfapi.in REST API.\nValidates schemas, handles nulls, logs file audit."),
        ("Layer 2: Storage", "bluestock_mf.db Star Schema.\n8 normalized tables with foreign keys and index optimization."),
        ("Layer 3: Analytics", "Quantitative Risk Engine.\nCAGR, Alpha/Beta, Sharpe, Sortino, VaR/CVaR, HHI, Scorecard."),
        ("Layer 4: Delivery", "Interactive Streamlit App + Power BI.\n4 executive screens, PDF tearsheets, automated recommendations.")
    ]
    for idx, (s_title, s_desc) in enumerate(steps):
        left_pos = 0.8 + idx * 2.95
        add_card(slide4, left_pos, 1.4, 2.85, 2.4, s_title, bg_color=GRAY_LIGHT)
        tx_s = slide4.shapes.add_textbox(Inches(left_pos + 0.15), Inches(2.0), Inches(2.55), Inches(1.6))
        tf_s = tx_s.text_frame
        tf_s.word_wrap = True
        p_s = tf_s.paragraphs[0]
        p_s.text = s_desc
        p_s.font.name = "Arial"
        p_s.font.size = Pt(10)
        p_s.font.color.rgb = TEXT_DARK

    # Bottom Database Card
    add_card(slide4, 0.8, 4.0, 11.7, 2.8, "Database Star Schema Specification (bluestock_mf.db)")
    tx_db = slide4.shapes.add_textbox(Inches(1.0), Inches(4.55), Inches(11.3), Inches(2.1))
    tf_db = tx_db.text_frame
    tf_db.word_wrap = True
    db_tables = [
        "<b>dim_fund:</b> 40 rows | amfi_code (PK), fund_house, scheme_name, category, sub_category, plan_type, expense_ratio",
        "<b>fact_nav_history:</b> 46,000 rows | nav_id (PK), amfi_code (FK), date, nav, daily_return_pct",
        "<b>fact_transactions:</b> 32,778 rows | txn_id (PK), amfi_code (FK), investor_id, txn_date, txn_type, amount_inr, city_tier, state",
        "<b>fact_fund_scorecard:</b> 40 rows | amfi_code (PK), cagr_3yr, sharpe, sortino, alpha, beta, max_drawdown, composite_score",
        "<b>dim_benchmark:</b> 1,250 rows | date (PK), nifty50_close, nifty100_close, daily_return_nifty100"
    ]
    for idx, t_info in enumerate(db_tables):
        p_t = tf_db.paragraphs[0] if idx == 0 else tf_db.add_paragraph()
        p_t.text = t_info
        p_t.font.name = "Arial"
        p_t.font.size = Pt(10.5)
        p_t.font.color.rgb = TEXT_DARK
        p_t.space_after = Pt(4)

    # =========================================================================
    # SLIDE 5: EDA Highlights (Part 1 - Industry Inflows & Category AUM)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "4. Exploratory Data Analysis (Part 1): Industry Macro Trends")

    # Left Card with AUM Chart
    add_card(slide5, 0.8, 1.4, 6.2, 5.4, "Industry AUM Trajectory & Market Share")
    aum_img = os.path.join(BASE_DIR, "outputs", "aum_growth_by_amc.png")
    if os.path.exists(aum_img):
        slide5.shapes.add_picture(aum_img, Inches(0.95), Inches(2.0), width=Inches(5.9), height=Inches(4.6))

    # Right Card: Key Findings
    add_card(slide5, 7.2, 1.4, 5.3, 5.4, "Key Macro Observations")
    tx_eda1 = slide5.shapes.add_textbox(Inches(7.4), Inches(2.0), Inches(4.9), Inches(4.6))
    tf_eda1 = tx_eda1.text_frame
    tf_eda1.word_wrap = True
    eda1_points = [
        "<b>Exponential AUM Expansion:</b> Indian Mutual Fund industry AUM scaled from Rs. 27 Lakh Cr (2020) to Rs. 81.3 Lakh Cr (2025), compounding at ~24.6% annually.",
        "<b>AMC Concentration:</b> Top 3 AMCs (SBI, ICICI Prudential, HDFC) command >52% of total industry AUM, displaying high market dominance.",
        "<b>SIP Inflow Resilience:</b> Monthly SIP inflows surged past Rs. 26,000 Cr in 2025, demonstrating retail stickiness even through market corrections.",
        "<b>Category Flow Shifts:</b> Equity schemes experienced the highest net inflows (+64%), while Debt funds saw intermittent redemptions amidst interest rate cycles."
    ]
    for idx, pt in enumerate(eda1_points):
        p = tf_eda1.paragraphs[0] if idx == 0 else tf_eda1.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(14)

    # =========================================================================
    # SLIDE 6: EDA Highlights (Part 2 - Investor Demographics & T30/B30 Split)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "5. Exploratory Data Analysis (Part 2): Investor Demographics & B30")

    # Left Card: Findings
    add_card(slide6, 0.8, 1.4, 5.3, 5.4, "Demographic Insights & Retention Patterns")
    tx_eda2 = slide6.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(4.9), Inches(4.6))
    tf_eda2 = tx_eda2.text_frame
    tf_eda2.word_wrap = True
    eda2_points = [
        "<b>B30 Penetration Surge:</b> Beyond Top 30 (B30) cities now contribute 28% of incremental SIP folios, signaling strong tier-2 and tier-3 adoption.",
        "<b>Millennial & Gen-Z Participation:</b> Investors aged 25–38 represent 47.8% of active folios, primarily investing through digital Direct platforms.",
        "<b>SIP Continuity Analysis:</b> Out of 2,950 analyzed active SIP accounts, 2,949 experienced at least one payment gap > 35 days, highlighting a massive retention opportunity.",
        "<b>Average Ticket Size:</b> T30 investors average Rs. 4,200/month per SIP versus Rs. 1,850/month in B30 geographies, presenting high expansion headroom."
    ]
    for idx, pt in enumerate(eda2_points):
        p = tf_eda2.paragraphs[0] if idx == 0 else tf_eda2.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(14)

    # Right Card: Chart Graphic
    add_card(slide6, 6.3, 1.4, 6.2, 5.4, "Sector Concentration & Geographic Distribution")
    hhi_img = os.path.join(BASE_DIR, "outputs", "sector_hhi_chart.png")
    if os.path.exists(hhi_img):
        slide6.shapes.add_picture(hhi_img, Inches(6.45), Inches(2.0), width=Inches(5.9), height=Inches(4.6))

    # =========================================================================
    # SLIDE 7: Performance Metrics (Part 1 - Returns & Risk-Adjusted Scoring)
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "6. Quantitative Performance Metrics: Returns & Alpha Generation")

    # Left Card: Chart
    add_card(slide7, 0.8, 1.4, 6.4, 5.4, "Top 5 Schemes vs Nifty 100 Benchmark")
    bench_img = os.path.join(BASE_DIR, "benchmark_comparison_chart.png")
    if os.path.exists(bench_img):
        slide7.shapes.add_picture(bench_img, Inches(0.95), Inches(2.0), width=Inches(6.1), height=Inches(4.6))

    # Right Card: Metrics Table & Discussion
    add_card(slide7, 7.4, 1.4, 5.1, 5.4, "Top Performing Schemes (Scorecard)")
    tx_perf1 = slide7.shapes.add_textbox(Inches(7.6), Inches(2.0), Inches(4.7), Inches(4.6))
    tf_perf1 = tx_perf1.text_frame
    tf_perf1.word_wrap = True
    perf1_points = [
        "<b>Composite Scorecard Top 3:</b><br/>"
        "1. ICICI Pru Midcap Fund (Score: 84.5)<br/>"
        "2. HDFC Mid-Cap Opportunities (Score: 82.0)<br/>"
        "3. Axis Midcap Fund (Score: 80.8)",
        "<b>Alpha Generation vs Nifty 100:</b><br/>"
        "Mid-cap and Small-cap funds generated positive annual alpha between +3.2% and +6.8% over the 5-year cycle.",
        "<b>Risk-Adjusted Efficiency (Sharpe & Sortino):</b><br/>"
        "Liquid and Hybrid funds achieved high Sharpe ratios (>2.5) due to minimal downside volatility (Sortino > 4.0).",
        "<b>Tracking Error:</b> Large-cap passive index funds maintained tight tracking errors (<0.45%), ensuring reliable benchmark replication."
    ]
    for idx, pt in enumerate(perf1_points):
        p = tf_perf1.paragraphs[0] if idx == 0 else tf_perf1.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(10)

    # =========================================================================
    # SLIDE 8: Performance Metrics (Part 2 - Downside Risk, Drawdown & VaR)
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "7. Advanced Risk Analytics: Downside Risk, Drawdown & VaR")

    # Left Card: Rolling Sharpe Chart
    add_card(slide8, 0.8, 1.4, 6.4, 5.4, "90-Day Rolling Sharpe Ratio Trajectory")
    roll_img = os.path.join(BASE_DIR, "rolling_sharpe_chart.png")
    if os.path.exists(roll_img):
        slide8.shapes.add_picture(roll_img, Inches(0.95), Inches(2.0), width=Inches(6.1), height=Inches(4.6))

    # Right Card: VaR & Drawdown Analysis
    add_card(slide8, 7.4, 1.4, 5.1, 5.4, "Institutional Risk Metrics Summary")
    tx_perf2 = slide8.shapes.add_textbox(Inches(7.6), Inches(2.0), Inches(4.7), Inches(4.6))
    tf_perf2 = tx_perf2.text_frame
    tf_perf2.word_wrap = True
    perf2_points = [
        "<b>Maximum Drawdown (Peak-to-Trough):</b><br/>"
        "Equity funds experienced peak drawdowns of -14.2% to -28.5% during macro shocks, with recovery horizons averaging 7.4 months.",
        "<b>Historical VaR (95% Daily):</b><br/>"
        "Small-cap funds exhibited 95% 1-day VaR up to -2.69%, indicating potential 1-day tail losses exceeding 2.7% on volatile trading days.",
        "<b>Conditional VaR (CVaR / Expected Shortfall):</b><br/>"
        "Quantifies average tail loss in the worst 5% of outcomes (ranging from -3.4% to -4.1% for high-beta equity).",
        "<b>Herfindahl-Hirschman Index (Sector HHI):</b><br/>"
        "Identified portfolios with HHI > 2,000 (e.g. Axis Bluechip HHI=2,064), highlighting elevated financial sector concentration."
    ]
    for idx, pt in enumerate(perf2_points):
        p = tf_perf2.paragraphs[0] if idx == 0 else tf_perf2.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(10)

    # =========================================================================
    # SLIDE 9: Dashboard Screenshots (Part 1 - Macro Trends & Fund Screener)
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "8. Interactive Dashboard: Industry Macro & Fund Screener")

    # Screenshot 1
    add_card(slide9, 0.8, 1.4, 5.7, 5.4, "Screen 1: Industry Macro Trends")
    d1_img = os.path.join(BASE_DIR, "dashboard", "dashboard_page_1.png")
    if os.path.exists(d1_img):
        slide9.shapes.add_picture(d1_img, Inches(0.95), Inches(2.0), width=Inches(5.4), height=Inches(4.6))

    # Screenshot 2
    add_card(slide9, 6.8, 1.4, 5.7, 5.4, "Screen 2: Fund Performance & Scorecard")
    d2_img = os.path.join(BASE_DIR, "dashboard", "dashboard_page_2.png")
    if os.path.exists(d2_img):
        slide9.shapes.add_picture(d2_img, Inches(6.95), Inches(2.0), width=Inches(5.4), height=Inches(4.6))

    # =========================================================================
    # SLIDE 10: Dashboard Screenshots (Part 2 - Investor Analytics & Recommender)
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "9. Interactive Dashboard: Investor Analytics & Recommender")

    # Screenshot 3
    add_card(slide10, 0.8, 1.4, 5.7, 5.4, "Screen 3: Investor Demographic Analytics")
    d3_img = os.path.join(BASE_DIR, "dashboard", "dashboard_page_3.png")
    if os.path.exists(d3_img):
        slide10.shapes.add_picture(d3_img, Inches(0.95), Inches(2.0), width=Inches(5.4), height=Inches(4.6))

    # Screenshot 4
    add_card(slide10, 6.8, 1.4, 5.7, 5.4, "Screen 4: Market Trends & Recommender")
    d4_img = os.path.join(BASE_DIR, "dashboard", "dashboard_page_4.png")
    if os.path.exists(d4_img):
        slide10.shapes.add_picture(d4_img, Inches(6.95), Inches(2.0), width=Inches(5.4), height=Inches(4.6))

    # =========================================================================
    # SLIDE 11: Key Findings & Recommendations
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    add_header(slide11, "10. Strategic Business Recommendations for Bluestock")

    recs = [
        ("1. Direct Plan Migration Tool",
         "Develop an automated calculator demonstrating the 15-year compounding differential of saving 80–100 bps TER.",
         "High Acquisition & AUM Growth"),
        ("2. Predictive SIP Retention Alerts",
         "Deploy automated WhatsApp and in-app nudges when a user's SIP gap exceeds 25 days to curb the 2,949 at-risk lapses.",
         "Reduces Investor Churn by ~35%"),
        ("3. Regional B30 Expansion",
         "Launch vernacular educational modules and micro-SIPs (Rs. 250/mo) tailored to emerging tier-2/3 cities.",
         "Captures Untapped Demographic"),
        ("4. Automated Portfolio Rebalancing",
         "Incorporate real-time Sector HHI alerts and VaR thresholds to prevent retail portfolios exceeding 30% single-sector risk.",
         "Institutional-Grade Safety")
    ]
    for idx, (r_title, r_desc, r_imp) in enumerate(recs):
        row_top = 1.4 + idx * 1.35
        add_card(slide11, 0.8, row_top, 11.7, 1.25, "", bg_color=WHITE)
        tx_r = slide11.shapes.add_textbox(Inches(1.0), Inches(row_top + 0.1), Inches(11.3), Inches(1.05))
        tf_r = tx_r.text_frame
        tf_r.word_wrap = True
        
        p_rt = tf_r.paragraphs[0]
        p_rt.text = f"{r_title} — Impact: {r_imp}"
        p_rt.font.name = "Arial"
        p_rt.font.size = Pt(12)
        p_rt.font.bold = True
        p_rt.font.color.rgb = BLUE_ACCENT

        p_rd = tf_r.add_paragraph()
        p_rd.text = r_desc
        p_rd.font.name = "Arial"
        p_rd.font.size = Pt(11)
        p_rd.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 12: Thank You
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    bg12 = slide12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg12.fill.solid()
    bg12.fill.fore_color.rgb = NAVY_DARK
    bg12.line.fill.background()

    tx12 = slide12.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.3), Inches(2.2))
    tf12 = tx12.text_frame
    tf12.word_wrap = True
    
    p12_top = tf12.paragraphs[0]
    p12_top.text = "BLUESTOCK FINTECH • MUTUAL FUND ANALYTICS"
    p12_top.font.name = "Arial"
    p12_top.font.size = Pt(14)
    p12_top.font.bold = True
    p12_top.font.color.rgb = BLUE_ACCENT

    p12_main = tf12.add_paragraph()
    p12_main.text = "Thank You!"
    p12_main.font.name = "Arial"
    p12_main.font.size = Pt(44)
    p12_main.font.bold = True
    p12_main.font.color.rgb = WHITE

    p12_sub = tf12.add_paragraph()
    p12_sub.text = "Questions & Discussions Welcome"
    p12_sub.font.name = "Arial"
    p12_sub.font.size = Pt(18)
    p12_sub.font.color.rgb = RGBColor(203, 213, 225)

    card12 = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(4.3), Inches(10.3), Inches(2.2))
    card12.fill.solid()
    card12.fill.fore_color.rgb = NAVY_PRIMARY
    card12.line.color.rgb = BLUE_ACCENT

    tx12_c = slide12.shapes.add_textbox(Inches(1.8), Inches(4.5), Inches(9.7), Inches(1.8))
    tf12_c = tx12_c.text_frame
    bullets_12 = [
        "<b>Repository & Deliverables:</b> GitHub: rajeevreddy23/Day-1-Data-ingestion-complete (Tag: v1.0)",
        "<b>Pipeline Execution:</b> python run_pipeline.py (Automated ingestion, cleaning, analytics & audit)",
        "<b>Interactive Dashboard:</b> streamlit run dashboard/capstone_dashboard.py",
        "<b>Capstone Team:</b> Poulami Dutta (PO) • Rajeev Reddy (RA) • Thadakamalla Likith Kumar (TH)"
    ]
    for idx, b in enumerate(bullets_12):
        p = tf12_c.paragraphs[0] if idx == 0 else tf12_c.add_paragraph()
        p.text = b
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE
        p.space_after = Pt(6)

    # Save
    prs.save(PPTX_PATH)
    import shutil
    shutil.copyfile(PPTX_PATH, PPTX_ALT_PATH)
    print(f"Saved 12-slide presentation to {PPTX_PATH} and {PPTX_ALT_PATH}")

if __name__ == '__main__':
    create_presentation()
