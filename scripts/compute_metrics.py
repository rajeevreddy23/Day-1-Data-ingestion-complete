"""
Bluestock Fintech - Mutual Fund Analytics Platform
Deliverable: compute_metrics.py (Day 4: Performance Analytics)

Computes:
1. Daily returns (nav_t / nav_t-1 - 1)
2. CAGR for 1yr, 3yr, 5yr
3. Sharpe Ratio (Rf = 6.5%)
4. Sortino Ratio (Downside deviation)
5. Alpha and Beta vs Nifty 100 via scipy.stats.linregress
6. Maximum Drawdown and worst drawdown period
7. Fund Scorecard (0-100 composite ranking)
8. Benchmark Comparison Chart (Top 5 vs Nifty 50 and 100) + Tracking Error
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path

# Paths configuration
BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUTS_DIR = BASE_DIR / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("BLUESTOCK FINTECH - FUND PERFORMANCE ANALYTICS ENGINE")
print("=" * 70)

# Load cleaned datasets
nav_df = pd.read_csv(PROCESSED_DIR / "clean_nav.csv")
fund_master = pd.read_csv(BASE_DIR / "01_fund_master.csv")
bench_df = pd.read_csv(BASE_DIR / "10_benchmark_indices.csv")
perf_df = pd.read_csv(PROCESSED_DIR / "clean_performance.csv")

nav_df["date"] = pd.to_datetime(nav_df["date"])
bench_df["date"] = pd.to_datetime(bench_df["date"])

print(f"Loaded {len(nav_df)} NAV records across {nav_df['amfi_code'].nunique()} schemes.")

# 1. Daily returns
print("\n[1/8] Computing daily returns for all 40 schemes...")
nav_df = nav_df.sort_values(["amfi_code", "date"])
nav_df["daily_return"] = nav_df.groupby("amfi_code")["nav"].pct_change()
nav_df.to_csv(PROCESSED_DIR / "daily_returns.csv", index=False)
print(f"  Mean return: {nav_df['daily_return'].mean():.6f}, Std: {nav_df['daily_return'].std():.6f}")

# 2. CAGR (1yr, 3yr, 5yr)
print("\n[2/8] Calculating 1Y, 3Y, 5Y CAGR...")
cagr_list = []
schemes = nav_df["amfi_code"].unique()

for code in schemes:
    f_nav = nav_df[nav_df["amfi_code"] == code].sort_values("date")
    n_days = len(f_nav)
    end_nav = f_nav["nav"].iloc[-1]
    
    # 1Y (~252 trading days)
    nav_1y = f_nav["nav"].iloc[-252] if n_days >= 252 else f_nav["nav"].iloc[0]
    cagr_1y = (end_nav / nav_1y) ** (252 / min(n_days, 252)) - 1
    
    # 3Y (~756 trading days)
    nav_3y = f_nav["nav"].iloc[-756] if n_days >= 756 else f_nav["nav"].iloc[0]
    cagr_3y = (end_nav / nav_3y) ** (252 / min(n_days, 756)) - 1
    
    # Total period (approx 4.5Y)
    start_nav = f_nav["nav"].iloc[0]
    cagr_total = (end_nav / start_nav) ** (252 / n_days) - 1
    
    cagr_list.append({
        "amfi_code": code,
        "cagr_1yr": round(cagr_1y * 100, 2),
        "cagr_3yr": round(cagr_3y * 100, 2),
        "cagr_5yr": round(cagr_total * 100, 2)
    })

cagr_df = pd.DataFrame(cagr_list)
cagr_df.to_csv(PROCESSED_DIR / "cagr_report.csv", index=False)

# 3. Sharpe Ratio (Rf = 6.5%)
print("\n[3/8] Computing Sharpe Ratio (Rf = 6.5%)...")
Rf_daily = 0.065 / 252
sharpe_list = []

for code in schemes:
    ret = nav_df[nav_df["amfi_code"] == code]["daily_return"].dropna()
    mean_ret = ret.mean()
    std_ret = ret.std()
    sharpe = ((mean_ret - Rf_daily) / std_ret) * np.sqrt(252) if std_ret > 0 else 0
    sharpe_list.append({"amfi_code": code, "sharpe_ratio": round(sharpe, 4)})

sharpe_df = pd.DataFrame(sharpe_list)
sharpe_df.to_csv(PROCESSED_DIR / "sharpe_report.csv", index=False)

# 4. Sortino Ratio (Downside std)
print("\n[4/8] Computing Sortino Ratio (Downside std)...")
sortino_list = []

for code in schemes:
    ret = nav_df[nav_df["amfi_code"] == code]["daily_return"].dropna()
    mean_ret = ret.mean()
    neg_ret = ret[ret < 0]
    downside_std = neg_ret.std() if len(neg_ret) > 0 else ret.std()
    sortino = ((mean_ret - Rf_daily) / downside_std) * np.sqrt(252) if downside_std > 0 else 0
    sortino_list.append({"amfi_code": code, "sortino_ratio": round(sortino, 4)})

sortino_df = pd.DataFrame(sortino_list)
sortino_df.to_csv(PROCESSED_DIR / "sortino_report.csv", index=False)

# 5. Alpha & Beta vs Nifty 100
print("\n[5/8] Computing Alpha and Beta vs Nifty 100 using scipy.stats.linregress...")
nifty100 = bench_df[bench_df["index_name"] == "NIFTY 100"].copy()
if len(nifty100) == 0:
    nifty100 = bench_df[bench_df["index_name"].str.contains("100", case=False, na=False)].copy()
if len(nifty100) == 0:
    nifty100 = bench_df[bench_df["index_name"].str.contains("NIFTY", case=False, na=False)].copy()

nifty100 = nifty100.sort_values("date")
nifty100["bench_return"] = nifty100["close_value"].pct_change()

alpha_beta_list = []
for code in schemes:
    f_nav = nav_df[nav_df["amfi_code"] == code].sort_values("date")
    merged = pd.merge(f_nav[["date", "daily_return"]], nifty100[["date", "bench_return"]], on="date").dropna()
    if len(merged) > 30:
        slope, intercept, r_value, p_value, std_err = stats.linregress(merged["bench_return"], merged["daily_return"])
        beta = slope
        alpha = intercept * 252 * 100
    else:
        beta, alpha, r_value = 1.0, 0.0, 0.0
    alpha_beta_list.append({
        "amfi_code": code,
        "alpha": round(alpha, 2),
        "beta": round(beta, 2),
        "r_squared": round(r_value ** 2, 4)
    })

alpha_beta_df = pd.DataFrame(alpha_beta_list)
alpha_beta_df.to_csv(PROCESSED_DIR / "alpha_beta.csv", index=False)
alpha_beta_df.to_csv(OUTPUTS_DIR / "alpha_beta.csv", index=False)
alpha_beta_df.to_csv(BASE_DIR / "alpha_beta.csv", index=False)

# 6. Maximum Drawdown
print("\n[6/8] Calculating Maximum Drawdown and peak-to-trough dates...")
mdd_list = []
for code in schemes:
    f_nav = nav_df[nav_df["amfi_code"] == code].sort_values("date").copy()
    f_nav["peak"] = f_nav["nav"].cummax()
    f_nav["drawdown"] = (f_nav["nav"] - f_nav["peak"]) / f_nav["peak"]
    min_dd = f_nav["drawdown"].min()
    trough_row = f_nav.loc[f_nav["drawdown"] == min_dd].iloc[0]
    peak_row = f_nav.loc[(f_nav["date"] <= trough_row["date"]) & (f_nav["nav"] == trough_row["peak"])].iloc[-1]
    
    mdd_list.append({
        "amfi_code": code,
        "max_drawdown_pct": round(min_dd * 100, 2),
        "peak_date": peak_row["date"].strftime("%Y-%m-%d"),
        "trough_date": trough_row["date"].strftime("%Y-%m-%d")
    })

mdd_df = pd.DataFrame(mdd_list)
mdd_df.to_csv(PROCESSED_DIR / "max_drawdown_report.csv", index=False)

# 7. Fund Scorecard (0-100 composite ranking)
print("\n[7/8] Generating composite Fund Scorecard (0-100)...")
master_cols = [c for c in fund_master.columns if c in ["amfi_code", "scheme_name", "fund_house", "category", "risk_category", "expense_ratio_pct"]]
score_df = fund_master[master_cols].merge(cagr_df, on="amfi_code")
score_df = score_df.merge(sharpe_df, on="amfi_code")
score_df = score_df.merge(sortino_df, on="amfi_code")
score_df = score_df.merge(alpha_beta_df, on="amfi_code")
score_df = score_df.merge(mdd_df, on="amfi_code")

n = len(score_df)
score_df["rank_return"] = score_df["cagr_3yr"].rank(ascending=True) / n * 100
score_df["rank_sharpe"] = score_df["sharpe_ratio"].rank(ascending=True) / n * 100
score_df["rank_alpha"] = score_df["alpha"].rank(ascending=True) / n * 100
score_df["rank_expense"] = score_df["expense_ratio_pct"].rank(ascending=False) / n * 100
score_df["rank_mdd"] = score_df["max_drawdown_pct"].rank(ascending=False) / n * 100

score_df["composite_score"] = round(
    0.30 * score_df["rank_return"] +
    0.25 * score_df["rank_sharpe"] +
    0.20 * score_df["rank_alpha"] +
    0.15 * score_df["rank_expense"] +
    0.10 * score_df["rank_mdd"], 1
)

score_df = score_df.sort_values("composite_score", ascending=False).reset_index(drop=True)
score_df.index = score_df.index + 1
score_df.index.name = "Rank"

# Save scorecard
score_df.to_csv(PROCESSED_DIR / "fund_scorecard.csv")
score_df.to_csv(OUTPUTS_DIR / "fund_scorecard.csv")
score_df.to_csv(BASE_DIR / "fund_scorecard.csv")
print(f"  Top 3 Funds: {score_df.iloc[0]['scheme_name']} ({score_df.iloc[0]['composite_score']}), "
      f"{score_df.iloc[1]['scheme_name']} ({score_df.iloc[1]['composite_score']}), "
      f"{score_df.iloc[2]['scheme_name']} ({score_df.iloc[2]['composite_score']})")

# 8. Benchmark Comparison Chart & Tracking Error
print("\n[8/8] Generating Benchmark Comparison Chart (PNG) and Tracking Error...")
top5_codes = score_df.head(5)["amfi_code"].tolist()

plt.figure(figsize=(12, 7), dpi=300)
colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

for i, code in enumerate(top5_codes):
    f_nav = nav_df[nav_df["amfi_code"] == code].sort_values("date")
    s_name = fund_master.loc[fund_master["amfi_code"] == code, "scheme_name"].values[0]
    base_nav = f_nav["nav"].iloc[0]
    norm_nav = (f_nav["nav"] / base_nav) * 100
    plt.plot(f_nav["date"], norm_nav, label=f"{s_name[:25]}...", color=colors[i], linewidth=1.8)

n50 = bench_df[bench_df["index_name"].str.contains("50", case=False, na=False)].sort_values("date")
if len(n50) > 0:
    plt.plot(n50["date"], (n50["close_value"] / n50["close_value"].iloc[0]) * 100,
             label="Nifty 50 Benchmark", color="black", linewidth=2.2, linestyle="--")

n100 = bench_df[bench_df["index_name"].str.contains("100", case=False, na=False)].sort_values("date")
if len(n100) > 0:
    plt.plot(n100["date"], (n100["close_value"] / n100["close_value"].iloc[0]) * 100,
             label="Nifty 100 Benchmark", color="dimgray", linewidth=2.0, linestyle=":")

plt.title("Bluestock Capstone - Top 5 Funds vs Benchmark Indices (3-Year Normalized Growth, Base=100)", fontsize=13, fontweight="bold", pad=12)
plt.xlabel("Date", fontsize=11)
plt.ylabel("Normalized Performance (Base 100)", fontsize=11)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(loc="upper left", frameon=True, fontsize=9)
plt.tight_layout()

plt.savefig(OUTPUTS_DIR / "benchmark_comparison_chart.png")
plt.savefig(BASE_DIR / "benchmark_comparison_chart.png")
plt.close()
print("  Saved benchmark_comparison_chart.png successfully!")

print("\nTracking Error vs Nifty 100:")
for code in top5_codes:
    f_nav = nav_df[nav_df["amfi_code"] == code].sort_values("date")
    s_name = fund_master.loc[fund_master["amfi_code"] == code, "scheme_name"].values[0]
    merged = pd.merge(f_nav[["date", "daily_return"]], nifty100[["date", "bench_return"]], on="date").dropna()
    diff = merged["daily_return"] - merged["bench_return"]
    te = diff.std() * np.sqrt(252) * 100
    print(f"  - {s_name[:30]:<32}: Tracking Error = {te:.2f}%")

print("\n" + "=" * 70)
print("ALL PERFORMANCE METRICS, SCORECARDS & CHARTS GENERATED SUCCESSFULLY!")
print("=" * 70)
