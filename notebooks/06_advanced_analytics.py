import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
import os

# Project base path
BASE_DIR = Path(r"C:\blue\drive-download-20260902T170546Z-1-001")
PROCESSED_DIR = BASE_DIR / "data" / "processed"
RAW_DIR = BASE_DIR

print("=" * 60)
print("BLUESTOCK FINTECH - CAPSTONE PROJECT")
print("Day 6: Advanced Analytics + Risk Metrics")
print("=" * 60)

# -------------------------------------------------------------------------
# Load data
# -------------------------------------------------------------------------
print("\n[Loading data...")
dr_df = pd.read_csv(os.path.join(PROCESSED_DIR, "daily_returns.csv"))
perf_clean = pd.read_csv(os.path.join(PROCESSED_DIR, "clean_performance.csv"))
fund_master = pd.read_csv(os.path.join(RAW_DIR, "01_fund_master.csv"))
trans_clean = pd.read_csv(os.path.join(PROCESSED_DIR, "clean_transactions.csv"))
bench_raw = pd.read_csv(os.path.join(RAW_DIR, "10_benchmark_indices.csv"))
nav_clean = pd.read_csv(os.path.join(PROCESSED_DIR, "clean_nav.csv"))
nav_clean["date"] = pd.to_datetime(nav_clean["date"])
bench_raw["date"] = pd.to_datetime(bench_raw["date"])

print("  Daily returns: " + str(dr_df.shape[0]) + " records")
print("  Performance: " + str(perf_clean.shape[0]) + " funds")
print("  Transactions: " + str(trans_clean.shape[0]) + " records")

# -------------------------------------------------------------------------
# Task 1: Compute Historical VaR (95%) and Conditional VaR (CVaR)
# -------------------------------------------------------------------------
print("\n[Task 1] Computing Historical VaR (95%) and CVaR...")

var_cvar_results = []
for code in perf_clean["amfi_code"].unique():
    fund_returns = dr_df[dr_df["amfi_code"] == code]["daily_return"].dropna()
    if len(fund_returns) > 0:
        # Historical VaR at 95%: 5th percentile of daily return distribution
        var_95 = np.percentile(fund_returns, 5)
        # CVaR: mean of returns below VaR threshold
        cvar = fund_returns[fund_returns <= var_95].mean()
    else:
        var_95 = np.nan
        cvar = np.nan
    var_cvar_results.append({
        "amfi_code": code,
        "var_95_pct": var_95,
        "cvar_95_pct": cvar
    })

var_cvar_df = pd.DataFrame(var_cvar_results)
var_cvar_df.to_csv(os.path.join(PROCESSED_DIR, "var_cvar_report.csv"), index=False)
print("  [OK] VaR/CVaR report saved: " + str(var_cvar_df.shape[0]) + " funds")

print("  Funds with worst (most negative) VaR:")
worst_var = var_cvar_df.nsmallest(5, "var_95_pct")[["amfi_code", "var_95_pct"]]
for _, row in worst_var.iterrows():
    fund_name = fund_master[fund_master["amfi_code"] == row["amfi_code"]]["scheme_name"].iloc[0]
    print("  " + fund_name + ": " + str(round(row["var_95_pct"]*100, 2)) + "%")

# -------------------------------------------------------------------------
# Task 2: Rolling 90-day Sharpe Ratio for 5 selected funds
# -------------------------------------------------------------------------
print("\n[Task 2] Computing Rolling 90-day Sharpe Ratio...")

Rf_daily = 0.065 / 252

rolling_sharpe_results = {}
selected_fund_codes = ["125497", "119551", "120503", "119092", "120841"]  # HDFC Top 100, SBI Bluechip, ICICI Bluechip, Axis Bluechip, Kotak Bluechip

for code in selected_fund_codes:
    fund_returns = dr_df[dr_df["amfi_code"] == code]["daily_return"].dropna()
    if len(fund_returns) > 90:
        rolling_sharpe = []
        for i in range(90, len(fund_returns) + 1):
            window = fund_returns.iloc[i-90:i]
            if window.std() > 0:
                rs = (window.mean() - Rf_daily) / window.std() * np.sqrt(252)
            else:
                rs = np.nan
            rolling_sharpe.append(rs)
        rolling_sharpe_results[code] = rolling_sharpe

# Plot rolling Sharpe for selected funds
import plotly.graph_objects as go
fig = go.Figure()
code_to_label = {
    "125497": "HDFC Top 100",
    "119551": "SBI Bluechip",
    "120503": "ICICI Bluechip",
    "119092": "Axis Bluechip",
    "120841": "Kotak Bluechip"
}
for code, label in code_to_label.items():
    if code in rolling_sharpe_results:
        dates = nav_clean[nav_clean["amfi_code"] == code].sort_values("date")["date"].iloc[90:].values
        fig.add_trace(go.Scatter(x=dates, y=rolling_sharpe_results[code], name=label))

fig.update_layout(
    title="Rolling 90-Day Sharpe Ratio (5 Selected Funds)",
    xaxis_title="Date",
    yaxis_title="Rolling Sharpe Ratio",
    hovermode="x",
    height=500
)
fig.write_html(os.path.join("outputs", "rolling_sharpe_chart.html"))
print("  [OK] Rolling Sharpe chart saved: outputs/rolling_sharpe_chart.html")

# -------------------------------------------------------------------------
# Task 3: Investor Cohort Analysis
# -------------------------------------------------------------------------
print("\n[Task 3] Investor Cohort Analysis...")

# Group investors by first transaction year
trans_clean["transaction_date"] = pd.to_datetime(trans_clean["transaction_date"])
first_tx = trans_clean.groupby("investor_id")["transaction_date"].min().reset_index()
first_tx["cohort_year"] = first_tx["transaction_date"].dt.year

# Merge cohort year back to trans_clean
trans_clean = trans_clean.merge(first_tx[["investor_id", "cohort_year"]], on="investor_id")

# Aggregate by cohort year
cohort_summary = trans_clean.groupby("cohort_year").agg(
    investor_count=("investor_id", "nunique"),
    avg_sip_amount=("amount_inr", "mean"),
    total_invested=("amount_inr", "sum")
).reset_index()

print("  Cohort Analysis (by year):")
print(cohort_summary.to_string())

# -------------------------------------------------------------------------
# Task 4: SIP Continuation Analysis
# -------------------------------------------------------------------------
print("\n[Task 4] SIP Continuity Analysis...")

# For each investor with 6+ SIP transactions, compute average gap between transactions
investor_transaction_counts = trans_clean.groupby("investor_id").size()
eligible_investors = investor_transaction_counts[investor_transaction_counts >= 6].index.tolist()

investor_gaps_list = []
for inv_id in eligible_investors:
    inv_trans = trans_clean[trans_clean["investor_id"] == inv_id].sort_values("transaction_date")
    gaps = [(inv_trans.iloc[i+1]["transaction_date"] - inv_trans.iloc[i]["transaction_date"]).days 
            for i in range(len(inv_trans)-1)]
    if gaps:
        avg_gap = np.mean(gaps)
        max_gap = max(gaps)
        risk_flag = "at-risk" if max_gap > 35 else "active"
        investor_gaps_list.append({
            "investor_id": inv_id,
            "total_transactions": len(gaps) + 1,
            "avg_gap_days": round(avg_gap, 1),
            "max_gap_days": max_gap,
            "risk_flag": risk_flag
        })

sip_continuity_df = pd.DataFrame(investor_gaps_list)
sip_continuity_df.to_csv(os.path.join(PROCESSED_DIR, "sip_continuity.csv"), index=False)
at_risk_count = (sip_continuity_df["risk_flag"] == "at-risk").sum()
print("  [OK] SIP continuity report saved: " + str(sip_continuity_df.shape[0]) + " investors")
print("  At-risk investors (gap > 35 days): " + str(at_risk_count))

# -------------------------------------------------------------------------
# Task 5: Simple fund recommendation logic
# -------------------------------------------------------------------------
print("\n[Task 5] Fund Recommendation Logic...")

def recommend_funds(risk_appetite="Moderate"):
    """Recommend top 3 funds by Sharpe ratio within matching risk grade"""
    risk_map = {
        "Low": "Low",
        "Moderate": "Moderate",
        "High": "High"
    }
    risk_category = risk_map.get(risk_appetite, "Moderate")
    
    matching_funds = fund_master[fund_master["risk_category"] == risk_category]
    
    perf_with_risk = perf_clean.merge(matching_funds[["amfi_code"]], on="amfi_code")
    valid = perf_with_risk[perf_with_risk["sharpe_ratio"].notna()].sort_values(
        "sharpe_ratio", ascending=False
    ).head(10)
    
    top_3 = valid.head(3)[["amfi_code", "scheme_name", "fund_house", "sharpe_ratio", "return_3yr_pct"]]
    return top_3

for risk_lv in ["Low", "Moderate", "High"]:
    recs = recommend_funds(risk_lv)
    print("  Recommendations for risk appetite: " + risk_lv)
    if len(recs) > 0:
        for _, row in recs.iterrows():
            fund_name = fund_master[fund_master["amfi_code"] == row["amfi_code"]]["scheme_name"].iloc[0]
            print("  " + fund_name + " (" + str(row["fund_house"]) + "): Sharpe=" + str(round(row["sharpe_ratio"], 2)))
    else:
        print("  No funds found matching risk criteria")

# -------------------------------------------------------------------------
# Task 6: Sector concentration analysis (HHI)
# -------------------------------------------------------------------------
print("\n[Task 6] Sector Concentration Analysis (HHI)...")

port_holdings = pd.read_csv(os.path.join(RAW_DIR, "09_portfolio_holdings.csv"))

# Compute HHI for each fund: HHI = sum(weight_i^2)
hhi_by_fund = port_holdings.groupby("amfi_code").apply(
    lambda x: np.sum(x["weight_pct"]**2)
).reset_index()
hhi_by_fund.columns = ["amfi_code", "hhi"]

# Normalize: convert to 0-1 scale by dividing by 100 (since weights sum to 100%)
hhi_by_fund["hhi_normalized"] = hhi_by_fund["hhi"] / 100

# Classify concentration level
def classify_concentration(hhi_norm):
    if hhi_norm > 0.25:
        return "Highly Concentrated"
    elif hhi_norm > 0.15:
        return "Moderately Concentrated"
    else:
        return "Diversified"

hhi_by_fund["concentration"] = hhi_by_fund["hhi_normalized"].apply(classify_concentration)
hhi_by_fund = hhi_by_fund.merge(fund_master[["amfi_code", "scheme_name", "fund_house", "category"]], on="amfi_code")
hhi_by_fund = hhi_by_fund.sort_values("hhi", ascending=False)

print("  Top 10 funds by sector concentration (HHI):")
for _, row in hhi_by_fund.head(10).iterrows():
    fund_name = fund_master[fund_master["amfi_code"] == row["amfi_code"]]["scheme_name"].iloc[0]
    print("  " + fund_name + ": HHI=" + str(round(row["hhi"], 2)) + ", " + row["concentration"])

hhi_by_fund.to_csv(os.path.join(PROCESSED_DIR, "sector_hhi.csv"), index=False)
print("  [OK] Sector HHI report saved: outputs/sector_hhi.csv")

# -------------------------------------------------------------------------
# Task 7: Advanced Analytics Summary - 5 Key Insights
# -------------------------------------------------------------------------
print("\n[Task 7] Summarising 5 Key Advanced Analytics Insights...")

# Insight 1: Which funds have highest VaR
worst_funds_var = var_cvar_df.nlargest(3, "var_95_pct")[["amfi_code", "var_95_pct"]]
var_insight = "Funds with highest downside risk (VaR) include "
for _, row in worst_funds_var.iterrows():
    fund_name = fund_master[fund_master["amfi_code"] == row["amfi_code"]]["scheme_name"].iloc[0]
    var_insight += fund_name + " (" + str(round(row["var_95_pct"]*100, 2)) + "% VaR), "
var_insight = var_insight.rstrip(", ")

# Insight 2: Cohort investment patterns
if len(cohort_summary) > 0:
    earliest_cohort = int(cohort_summary.iloc[0]["cohort_year"])
    latest_cohort = int(cohort_summary.iloc[-1]["cohort_year"])
    avg_early_sip = cohort_summary.iloc[0]["avg_sip_amount"]
    cohort_insight = f"Investors who started SIPs in {earliest_cohort}-{latest_cohort} had " + \
                    f"average SIP of Rs. {avg_early_sip:.0f}, showing " + \
                    "strong retail participation in recent years"
else:
    cohort_insight = "Insufficient cohort data available"

# Insight 3: SIP continuity
sip_insight = f"{at_risk_count} investors have SIP gaps > 35 days, flagged as 'at-risk', " + \
              "indicating potential liquidity or interest issues in systematic investing"

# Insight 4: Fund recommendations by risk
rec_low = recommend_funds("Low")
rec_high = recommend_funds("High")
if len(rec_low) > 0 and len(rec_high) > 0:
    risk_insight = "Low-risk investors should consider " + rec_low.iloc[0]["scheme_name"] + \
                   " while high-risk investors may prefer " + rec_high.iloc[0]["scheme_name"]
else:
    risk_insight = "Recommendations based on available data - see fund scorecard for details"

# Insight 5: Sector concentration
if len(hhi_by_fund) > 0:
    highest_hhi_row = hhi_by_fund.iloc[0]
    concentration_insight = "Fund " + highest_hhi_row["scheme_name"] + " has the most concentrated sector portfolio " + \
                            "with HHI=" + str(round(highest_hhi_row["hhi"], 2)) + ", " + \
                            highest_hhi_row["concentration"] + " allocation, indicating " + \
                            "concentration risk in sector exposure"
else:
    concentration_insight = "Insufficient portfolio data for concentration analysis"

findings = [var_insight, cohort_insight, sip_insight, risk_insight, concentration_insight]

for i, f in enumerate(findings, 1):
    print("  " + str(i) + ". " + f)

# Save findings to markdown
with open(os.path.join("outputs", "advanced_analytics_findings.md"), "w") as f_out:
    f_out.write("# Bluestock Fintech Capstone - Advanced Analytics Findings\n\n")
    f_out.write("## 5 Key Insights from Advanced Analytics\n\n")
    for idx, finding in enumerate(findings, 1):
        f_out.write(f"{idx}. {finding}\n\n")
print("  [OK] Advanced analytics findings saved to outputs/advanced_analytics_findings.md")

print("\n" + "=" * 60)
print("DAY 6 COMPLETE: Advanced Analytics + Risk Metrics")
print("=" * 60)
print("\nOutput files generated:")
import os
for f in os.listdir("outputs"):
    if f.endswith(".csv") or f.endswith(".html"):
        print("  - outputs/" + f)
print("=" * 60)