import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime

# Page config
st.set_page_config(page_title="Bluestock Fintech: Mutual Fund Analytics", layout="wide")

# Project base path
BASE_DIR = Path(r"C:\blue\drive-download-20260902T170546Z-1-001")
PROCESSED_DIR = BASE_DIR / "data" / "processed"
RAW_DIR = BASE_DIR

# ==========================================================
# Sidebar Navigation
# ==========================================================
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Fund Performance", "Investor Analytics", "Industry Trends"])

# Load data once
@st.cache_data
def load_data():
    nav = pd.read_csv(os.path.join(PROCESSED_DIR, "clean_nav.csv"))
    trans = pd.read_csv(os.path.join(PROCESSED_DIR, "clean_transactions.csv"))
    perf = pd.read_csv(os.path.join(PROCESSED_DIR, "clean_performance.csv"))
    fund = pd.read_csv(os.path.join(RAW_DIR, "01_fund_master.csv"))
    aum = pd.read_csv(os.path.join(RAW_DIR, "03_aum_by_fund_house.csv"))
    sip = pd.read_csv(os.path.join(RAW_DIR, "04_monthly_sip_inflows.csv"))
    folio = pd.read_csv(os.path.join(RAW_DIR, "06_industry_folio_count.csv"))
    cat = pd.read_csv(os.path.join(RAW_DIR, "05_category_inflows.csv"))
    bench = pd.read_csv(os.path.join(RAW_DIR, "10_benchmark_indices.csv")
    )
    # Parse dates
    nav["date"] = pd.to_datetime(nav["date"])
    trans["transaction_date"] = pd.to_datetime(trans["transaction_date"])
    aum["date"] = pd.to_datetime(aum["date"])
    folio["month"] = pd.to_datetime(folio["month"])
    sip["month"] = pd.to_datetime(sip["month"])
    bench["date"] = pd.to_datetime(bench["date"])
    return nav, trans, perf, fund, aum, sip, folio, cat, bench

nav, trans, perf, fund, aum, sip, folio, cat, bench = load_data()

# ==========================================================
# Page 1: Dashboard - Industry Overview
# ==========================================================
if page == "Dashboard":
    st.title("Bluestock Fintech: Mutual Fund Analytics Dashboard")
    st.markdown("### Interactive Platform for Fund Performance & Investor Analytics")
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_aum = aum["aum_lakh_crore"].max()
        st.metric("Total Industry AUM", f"Rs. {total_aum:.1f} Lakh Crore")
    
    with col2:
        max_sip = sip["sip_inflow_crore"].max()
        st.metric("Monthly SIP Inflow (Peak)", f"Rs. {max_sip:.0f} Crore")
    
    with col3:
        total_folios = folio["total_folios_crore"].max()
        st.metric("Total Investor Folios", f"{total_folios:.1f} Crore")
    
    with col4:
        top_perf = perf.nlargest(1, "sharpe_ratio")[["scheme_name", "sharpe_ratio"]]
        st.metric("Top Performer", str(top_perf["scheme_name"].iloc[0]))
    
    st.markdown("---")
    
    # Row 1: AUM by Fund House
    st.subheader("AUM Growth by Fund House (2022-2025)")
    aum_by_year = aum.groupby(["fund_house", "date"])["aum_lakh_crore"].max().reset_index()
    aum_by_year["year"] = aum_by_year["date"].dt.year
    
    fig = px.bar(aum_by_year, x="fund_house", y="aum_lakh_crore", color="year",
                 title="AUM by Fund House", labels={"aum_lakh_crore": "AUM (Lakh Crore Rs.)"})
    st.plotly_chart(fig, use_container_width=True)
    
    # Row 2: SIP vs Benchmark
    st.subheader("SIP Inflows vs Benchmark Indices")
    col_left, col_right = st.columns(2)
    
    with col_left:
        sip_monthly = sip.groupby("month")["sip_inflow_crore"].sum().reset_index()
        fig = px.line(sip_monthly, x="month", y="sip_inflow_crore",
                      title="Monthly SIP Inflow (Jan 2022 - Dec 2025)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        nifty_50 = bench[bench["index_name"] == "Nifty 50"].sort_values("date")
        first_val = nifty_50["close_value"].iloc[0]
        normalized = (nifty_50["close_value"] / first_val) * 100
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=nifty_50["date"], y=normalized, name="Nifty 50", line=dict(color="blue")))
        fig.add_trace(go.Scatter(x=sip_monthly["month"], y=sip_monthly["sip_inflow_crore"], name="SIP Inflow", line=dict(color="orange", dash="dot")))
        fig.update_layout(title="SIP Inflow vs Nifty 50 (Normalized)")
        st.plotly_chart(fig, use_container_width=True)
    
    # Row 3: Category Inflows Heatmap
    st.subheader("Category-wise Net Inflows")
    cat_pivot = cat.pivot(index="category", columns="month", values="net_inflow_crore")
    cat_pivot = cat_pivot.reindex(columns=sorted(cat["month"].unique()))
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(cat_pivot, annot=True, fmt=".0f", cmap="RdYlGn", ax=ax,
                cbar_kws={"label": "Net Inflow (Rs. Crore)"})
    ax.set_title("Category-wise Net Inflows Heatmap")
    st.pyplot(fig)
    
    # Row 4: Top funds table
    st.subheader("Top Funds by Sharpe Ratio")
    top_funds = perf.merge(fund[["amfi_code", "scheme_name", "fund_house"]], on="amfi_code")
    top_funds = top_funds.nlargest(10, "sharpe_ratio")[["scheme_name", "fund_house", "sharpe_ratio", "return_3yr_pct"]]
    st.dataframe(top_funds.style.highlight_max(subset=["sharpe_ratio"]))

# ==========================================================
# Page 2: Fund Performance
# ==========================================================
elif page == "Fund Performance":
    st.title("Fund Performance Analytics")
    
    # Fund selection
    fund_options = fund["scheme_name"].unique()
    selected_fund = st.selectbox("Select a Fund", fund_options)
    selected_code = fund[fund["scheme_name"] == selected_fund]["amfi_code"].iloc[0]
    
    # Get fund NAV data
    fund_nav = nav[nav["amfi_code"] == selected_code].sort_values("date")
    
    # NAV trend chart
    st.subheader("NAV Trend")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fund_nav["date"], y=fund_nav["nav"], 
                             mode='lines', name='NAV', line=dict(color='blue')))
    fig.update_layout(title=f"NAV Trend: {selected_fund}", 
                      xaxis_title="Date", yaxis_title="NAV (Rs.)")
    st.plotly_chart(fig, use_container_width=True)
    
    # Performance metrics
    fund_perf = perf[perf["amfi_code"] == selected_code].iloc[0]
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("1-Year Return", f"{fund_perf['return_1yr_pct']:.2f}%")
    with col2:
        st.metric("3-Year CAGR", f"{fund_perf['return_3yr_pct']:.2f}%")
    with col3:
        st.metric("5-Year CAGR", f"{fund_perf['return_5yr_pct']:.2f}%")
    
    # Risk metrics
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.metric("Sharpe Ratio", f"{fund_perf['sharpe_ratio']:.2f}")
    with col5:
        st.metric("Sortino Ratio", f"{fund_perf['sortino_ratio']:.2f}")
    with col6:
        st.metric("Alpha (vs Nifty 100)", f"{fund_perf['alpha']:.2f}%")
    
    col7, col8, col9 = st.columns(3)
    
    with col7:
        st.metric("Beta (vs Nifty 100)", f"{fund_perf['beta']:.2f}")
    with col8:
        st.metric("Max Drawdown", f"{fund_perf['max_drawdown_pct']*100:.2f}%")
    with col9:
        st.metric("Standard Deviation (Annual)", f"{fund_perf['std_dev_ann_pct']:.2f}%")
    
    # Expense ratio
    st.metric("Expense Ratio", f"{fund_perf['expense_ratio_pct']:.2f}%")
    
    # Morningstar rating
    st.metric("Morningstar Rating", f"{fund_perf['morningstar_rating']}/5 stars")

# ==========================================================
# Page 3: Investor Analytics
# ==========================================================
elif page == "Investor Analytics":
    st.title("Investor Analytics")
    
    # Transaction type split
    st.subheader("Transaction Type Distribution")
    tx_type_counts = trans["transaction_type"].value_counts()
    fig = px.pie(values=tx_type_counts.values, names=tx_type_counts.index,
                 title="SIP vs Lumpsum vs Redemption Split")
    st.plotly_chart(fig, use_container_width=True)
    
    # SIP amount by state
    st.subheader("SIP Amount by State (Top 15)")
    sip_by_state = trans.groupby("state")["amount_inr"].sum().sort_values(ascending=False).head(15)
    fig = px.bar(sip_by_state, orientation="h",
                 title="SIP Amount by State",
                 labels={"amount_inr": "SIP Amount (Rs.)", "state": "State"})
    st.plotly_chart(fig, use_container_width=True)
    
    # Age group distribution
    st.subheader("Investor Age Group Distribution")
    age_dist = trans["age_group"].value_counts()
    fig = px.pie(values=age_dist.values, names=age_dist.index,
                 title="Age Group Distribution")
    st.plotly_chart(fig, use_container_width=True)
    
    # City tier distribution
    st.subheader("T30 vs B30 City Distribution")
    tier_counts = trans["city_tier"].value_counts()
    fig = px.pie(values=tier_counts.values, names=tier_counts.index,
                 title="T30 vs B30 Investor Distribution")
    st.plotly_chart(fig, use_container_width=True)
    
    # Monthly transaction volume
    st.subheader("Monthly Transaction Volume")
    monthly_tx = trans.groupby(trans["transaction_date"].dt.month).size().reset_index(name="count")
    monthly_tx["month_name"] = monthly_tx["month"].map({1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
                                                         7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"})
    fig = px.line(monthly_tx, x="month_name", y="count",
                  title="Monthly Transaction Volume")
    st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# Page 4: Industry Trends
# ==========================================================
elif page == "Industry Trends":
    st.title("Industry Trends & Analysis")
    
    # Folio count growth
    st.subheader("Folio Count Growth (Jan 2022 - Dec 2025)")
    folio_sorted = folio.sort_values("month")
    fig = px.line(folio_sorted, x="month", y="total_folios_crore",
                  title="Industry Folio Count Growth",
                  labels={"total_folios_crore": "Folios (Crore)", "month": "Month"})
    # Annotate start and end
    start_folio = folio_sorted["total_folios_crore"].iloc[0]
    end_folio = folio_sorted["total_folios_crore"].iloc[-1]
    fig.add_annotation(x=folio_sorted["month"].iloc[0], y=start_folio,
                       text="Start: " + str(round(start_folio, 2)) + " Cr", showarrow=True, font=dict(color="blue"))
    fig.add_annotation(x=folio_sorted["month"].iloc[-1], y=end_folio,
                       text="End: " + str(round(end_folio, 2)) + " Cr", showarrow=True, font=dict(color="green"))
    st.plotly_chart(fig, use_container_width=True)
    
    # SIP Industry stats
    st.subheader("SIP Industry Metrics")
    col1, col2 = st.columns(2)
    with col1:
        total_sip_monthly = sip["sip_inflow_crore"].sum()
        st.metric("Total SIP Inflow (5yr)", f"Rs. {total_sip_monthly:.0f} Crore")
    with col2:
        avg_sip_accounts = sip["active_sip_accounts_crore"].mean()
        st.metric("Avg Active SIP Accounts (Crore)", f"{avg_sip_accounts:.2f}")
    
    # Category inflows
    st.subheader("Category-wise Inflows (FY 2024-25)")
    cat_summary = cat.groupby("category")["net_inflow_crore"].sum().sort_values(ascending=False)
    fig = px.bar(cat_summary, x=cat_summary.index, y=cat_summary.values,
                 title="Total Net Inflows by Category",
                 labels={"x": "Category", "y": "Net Inflow (Rs. Crore)"})
    st.plotly_chart(fig, use_container_width=True)
    
    # AUM by fund house overview
    st.subheader("AUM by Fund House (Latest)")
    aum_latest = aum.sort_values("date").groupby("fund_house").tail(1)
    fig = px.bar(aum_latest, x="fund_house", y="aum_lakh_crore",
                 title="AUM by Fund House (Latest Data)",
                 labels={"aum_lakh_crore": "AUM (Lakh Crore Rs.)"})
    st.plotly_chart(fig, use_container_width=True)
    
    # SIP continuity analysis
    st.subheader("SIP Continuity Analysis")
    investor_trans = trans.groupby("investor_id").agg(
        total_transactions=("transaction_date", "count"),
        first_transaction=("transaction_date", "min"),
        last_transaction=("transaction_date", "max")
    ).reset_index()
    investor_trans["gap_days"] = (investor_trans["last_transaction"] - investor_trans["first_transaction"]).dt.days
    fig = px.histogram(investor_trans, x="gap_days", nbins=30,
                       title="SIP Transaction Gap Distribution",
                       labels={"gap_days": "Gap Between First & Last SIP (days)"})
    st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# Sidebar - Filters (show on all pages)
# ==========================================================
st.sidebar.header("Filters")
city_tier = st.sidebar.multiselect("City Tier", options=["T30", "B30"], default=["T30", "B30"])
state_sel = st.sidebar.multiselect("State", options=sorted(trans["state"].unique())[:10], default=[])
min_amount = st.sidebar.slider("Min SIP Amount (Rs.)", 0, 1000000, 0)

# Apply filters to transaction data
filtered_trans = trans.copy()
if "T30" not in city_tier and "B30" not in city_tier:
    filtered_trans = filtered_trans[filtered_trans["city_tier"].isin(city_tier)]
if state_sel:
    filtered_trans = filtered_trans[filtered_trans["state"].isin(state_sel)]
if min_amount > 0:
    filtered_trans = filtered_trans[filtered_trans["amount_inr"] >= min_amount]

st.sidebar.markdown(f"**Filtered transactions:** {filtered_trans.shape[0]:,} of {trans.shape[0]:,}")