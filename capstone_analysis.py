#!/usr/bin/env python3
"""Bluestock MF Capstone Project - Comprehensive Analysis"""

import pandas as pd
import numpy as np
import os
from pathlib import Path
import json

DATA_DIR = r'C:\blue\drive-download-20260902T170546Z-1-001'

def load_all_data():
    """Load all CSV files and return dict of DataFrames"""
    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
    dfs = {}
    for f in sorted(files):
        path = os.path.join(DATA_DIR, f)
        df = pd.read_csv(path, dtype=str)
        dfs[f] = df
        print(f"Loaded {f}: {df.shape[0]} rows x {df.shape[1]} cols")
    return dfs

def analyze_fund_master(dfs):
    """Analyze fund master data"""
    df = dfs['01_fund_master.csv']
    df['amfi_code'] = df['amfi_code'].astype(int)
    
    print("\n=== FUND MASTER ANALYSIS ===")
    print(f"Total schemes: {len(df)}")
    print(f"Fund houses: {df['fund_house'].nunique()}")
    print(f"Categories: {df['category'].nunique()}")
    print(f"Plans: {df['plan'].value_counts().to_dict()}")
    print(f"Benchmark distribution: {df['benchmark'].value_counts().to_dict()}")
    print(f"Expense ratio stats: {df['expense_ratio_pct'].describe()}")
    print(f"Min SIP amounts: {df['min_sip_amount'].unique()}")
    print(f"Min lump sum: {df['min_lumpsum_amount'].unique()}")
    
    # Category breakdown
    print("\nSchemes by category:")
    print(df['category'].value_counts())
    
    return df

def analyze_nav_history(dfs):
    """Analyze NAV history and performance"""
    df = dfs['02_nav_history.csv']
    df['date'] = pd.to_datetime(df['date'])
    df['nav'] = df['nav'].astype(float)
    df['amfi_code'] = df['amfi_code'].astype(int)
    
    print("\n=== NAV HISTORY ANALYSIS ===")
    print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
    print(f"Unique funds: {df['amfi_code'].nunique()}")
    
    # Latest NAV per fund
    latest = df.groupby('amfi_code')['nav'].last().reset_index()
    latest = latest.sort_values('nav', ascending=False).head(10)
    print("\nTop 10 funds by latest NAV:")
    for _, row in latest.iterrows():
        print(f"  AMFI {row['amfi_code']}: ₹{row['nav']:,.2f}")
    
    # Calculate returns for funds with fund master data
    fund_master = dfs['01_fund_master.csv']
    fund_master['amfi_code'] = fund_master['amfi_code'].astype(int)
    
    # Merge with performance data from scheme_performance.csv would be better
    # But we can calculate simple NAV returns
    print("\nNAV return 2022-2025 (sample):")
    for amfi in [119551, 119552, 100016]:  # SBI Bluechip Regular, Direct, HDFC Top 100 Regular
        fund_nav = df[df['amfi_code'] == amfi]['nav'].values
        if len(fund_nav) > 0:
            start_nav = fund_nav[0]
            end_nav = fund_nav[-1]
            ret = (end_nav - start_nav) / start_nav * 100
            print(f"  AMFI {amfi}: {ret:.2f}% return")

def analyze_aum_trends(dfs):
    """Analyze AUM by fund house"""
    df = dfs['03_aum_by_fund_house.csv']
    df['date'] = pd.to_datetime(df['date'])
    df['aum_crore'] = df['aum_crore'].astype(float) / 10000000  # Convert to lakh crore
    df['aum_lakh_crore'] = df['aum_lakh_crore'].astype(float)
    df['num_schemes'] = df['num_schemes'].astype(int)
    
    print("\n=== AUM TRENDS ===")
    print(f"AUM categories: {sorted(df['aum_lakh_crore'].unique())}")
    
    # Growth analysis
    for fund_house in df['fund_house'].unique():
        fdf = df[df['fund_house'] == fund_house]
        first_aum = fdf.iloc[0]['aum_lakh_crore']
        last_aum = fdf.iloc[-1]['aum_lakh_crore']
        growth = (last_aum - first_aum) / first_aum * 100
        print(f"  {fund_house}: {first_aum} → {last_aum} lakh crore ({growth:.1f}%)")
    
    # Latest AUM snapshot
    latest = df[df['date'] == df['date'].max()]
    print(f"\nTop 5 by latest AUM:")
    for _, row in latest.sort_values('aum_lakh_crore', ascending=False).head(5).iterrows():
        print(f"  {row['fund_house']}: ₹{row['aum_lakh_crore']} lakh crore ({row['num_schemes']} schemes)")

def analyze_sip_inflows(dfs):
    """Analyze SIP inflows data"""
    df = dfs['04_monthly_sip_inflows.csv']
    df['month'] = pd.to_datetime(df['month'] + '-01')
    df['sip_inflow_crore'] = df['sip_inflow_crore'].astype(float)
    df['active_sip_accounts_crore'] = df['active_sip_accounts_crore'].astype(float)
    df['new_sip_accounts_lakh'] = df['new_sip_accounts_lakh'].astype(float)
    df['sip_aum_lakh_crore'] = df['sip_aum_lakh_crore'].astype(float)
    df['yoy_growth_pct'] = df['yoy_growth_pct'].astype(float)
    
    print("\n=== SIP INFLOWS ANALYSIS ===")
    print(f"Date range: {df['month'].min().date()} to {df['month'].max().date()}")
    print(f"Total months: {len(df)}")
    
    # Growth trends
    first = df.iloc[0]
    last = df.iloc[-1]
    print(f"\nSIP Inflows: {first['sip_inflow_crore']:.0f} → {last['sip_inflow_crore']:.0f} crore")
    print(f"Active SIP Accounts: {first['active_sip_accounts_crore']:.2f} → {last['active_sip_accounts_crore']:.2f} crore")
    print(f"SIP AUM: {first['sip_aum_lakh_crore']:.2f} → {last['sip_aum_lakh_crore']:.2f} lakh crore")
    print(f"YoY Growth: {first['yoy_growth_pct']:.2f}% → {last['yoy_growth_pct']:.2f}%")
    
    # High growth periods
    print("\nTop 5 growth periods:")
    top_growth = df.nlargest(5, 'yoy_growth_pct')[['month', 'sip_inflow_crore', 'yoy_growth_pct']]
    for _, row in top_growth.iterrows():
        print(f"  {row['month'].strftime('%b-%y')}: ₹{row['sip_inflow_crore']:.0f} crore, YoY {row['yoy_growth_pct']:.2f}%")

def analyze_category_inflows(dfs):
    """Analyze category-wise inflows"""
    df = dfs['05_category_inflows.csv']
    df['month'] = pd.to_datetime(df['month'] + '-01')
    df['net_inflow_crore'] = df['net_inflow_crore'].astype(float)
    
    print("\n=== CATEGORY INFLOWS ANALYSIS ===")
    print(f"Date range: {df['month'].min().date()} to {df['month'].max().date()}")
    print(f"Unique categories: {df['category'].nunique()}")
    
    # Latest month snapshot
    latest = df[df['month'] == df['month'].max()]
    print(f"\nCategory inflows ({latest['month'].strftime('%b-%y')}):")
    for _, row in latest.sort_values('net_inflow_crore', ascending=False).iterrows():
        print(f"  {row['category']:25s}: ₹{row['net_inflow_crore']:.1f} crore")
    
    # Average inflows by category
    avg_inflows = df.groupby('category')['net_inflow_crore'].mean().sort_values(ascending=False)
    print("\nAverage inflows by category (all months):")
    for cat, val in avg_inflows.items():
        print(f"  {cat:25s}: ₹{val:.1f} crore")

def analyze_portfolio_holdings(dfs):
    """Analyze portfolio holdings and sector allocation"""
    df = dfs['09_portfolio_holdings.csv']
    df['amfi_code'] = df['amfi_code'].astype(int)
    df['weight_pct'] = df['weight_pct'].astype(float)
    df['market_value_cr'] = df['market_value_cr'].astype(float)
    df['current_price_inr'] = df['current_price_inr'].astype(float)
    
    print("\n=== PORTFOLIO HOLDINGS ANALYSIS ===")
    print(f"Unique schemes: {df['amfi_code'].nunique()}")
    print(f"Unique stocks: {df['stock_symbol'].nunique()}")
    print(f"Portfolio date: {df['portfolio_date'].mode()[0]}")
    
    # Top holdings across all schemes
    print("\nTop 15 stocks by total market value:")
    stock_totals = df.groupby('stock_symbol')['market_value_cr'].sum().sort_values(ascending=False).head(15)
    for stock, val in stock_totals.items():
        print(f"  {stock:20s}: ₹{val:.1f} crore")
    
    # Sector analysis
    df['sector'] = df['sector'].astype(str)
    sector_totals = df.groupby('sector')['weight_pct'].sum().sort_values(ascending=False)
    print("\nSector allocation weights:")
    for sector, val in sector_totals.items():
        print(f"  {sector:20s}: {val:.2f}%")
    
    # Scheme-wise analysis
    print("\nScheme portfolio concentration (top 5 schemes):")
    scheme_conc = df.groupby('amfi_code')['weight_pct'].sum().sort_values(ascending=False).head(5)
    fund_master = dfs['01_fund_master.csv']
    fund_master['amfi_code'] = fund_master['amfi_code'].astype(int)
    
    for amfi_code, conc in scheme_conc.items():
        fm_row = fund_master[fund_master['amfi_code'] == amfi_code]
        if len(fm_row) > 0:
            print(f"  {fm_row['scheme_name'].values[0]}: {conc:.2f}% total weight")

def analyze_investor_transactions(dfs):
    """Analyze investor transaction patterns"""
    df = dfs['08_investor_transactions.csv']
    df['investor_id'] = df['investor_id'].astype(str)
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df['amount_inr'] = df['amount_inr'].astype(float)
    df['annual_income_lakh'] = df['annual_income_lakh'].astype(float)
    df['amfi_code'] = df['amfi_code'].astype(int)
    df['transaction_type'] = df['transaction_type'].astype(str)
    df['state'] = df['state'].astype(str)
    df['city_tier'] = df['city_tier'].astype(str)
    df['age_group'] = df['age_group'].astype(str)
    df['gender'] = df['gender'].astype(str)
    df['payment_mode'] = df['payment_mode'].astype(str)
    df['kyc_status'] = df['kyc_status'].astype(str)
    
    print("\n=== INVESTOR TRANSACTIONS ANALYSIS ===")
    print(f"Total transactions: {len(df)}")
    print(f"Date range: {df['transaction_date'].min().date()} to {df['transaction_date'].max().date()}")
    
    # Transaction type distribution
    print(f"\nTransaction types: {df['transaction_type'].value_counts().to_dict()}")
    
    # Amount statistics
    print(f"\nAmount stats: Total ₹{df['amount_inr'].sum():,.0f} crore, Avg ₹{df['amount_inr'].mean():,.0f}")
    
    # KYC status
    print(f"\nKYC status: {df['kyc_status'].value_counts().to_dict()}")
    
    # Age group distribution
    print(f"\nAge groups: {df['age_group'].value_counts().to_dict()}")
    
    # Top states
    print(f"\nTop 10 states:")
    top_states = df['state'].value_counts().head(10)
    for state, count in top_items:
        print(f"  {state}: {count} transactions")
    
    # Payment mode
    print(f"\nPayment modes: {df['payment_mode'].value_counts().to_dict()}")
    
    # Gender distribution
    print(f"\nGender distribution: {df['gender'].value_counts().to_dict()}")

def analyze_benchmark_indices(dfs):
    """Analyze benchmark index data"""
    df = dfs['10_benchmark_indices.csv']
    df['date'] = pd.to_datetime(df['date'])
    df['close_value'] = df['close_value'].astype(float)
    
    print("\n=== BENCHMARK INDICES ANALYSIS ===")
    print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
    print(f"Unique indices: {df['index_name'].nunique()}")
    
    # Latest values
    latest = df[df['date'] == df['date'].max()]
    print(f"\nLatest ({latest['date'].iloc[0].strftime('%b-%y')}):")
    for _, row in latest.iterrows():
        print(f"  {row['index_name']:15s}: {row['close_value']:.2f}")
    
    # 4-year CAGR (2022-2025/2026)
    first_year = df[df['date'].dt.year == 2022].iloc[0]['close_value']
    last_year = df[df['date'].dt.year >= 2025].iloc[-1]['close_value']
    cagr = (last_year / first_year) ** (1/3) - 1  # 3-year CAGR from 2022 to 2025
    print(f"\nNIFTY50 3yr CAGR (2022-2025): {cagr*100:.2f}%")
    
    # Compare with fund performance
    print("\nBenchmark comparison with top performers would require merging with scheme_performance.csv")

def main():
    print("=" * 60)
    print("B L U E S T O C K  M F  -  C A P S T O N E  P R O J E C T")
    print("=" * 60)
    
    # Load all data
    dfs = load_all_data()
    
    # Run all analyses
    analyze_fund_master(dfs)
    analyze_nav_history(dfs)
    analyze_aum_trends(dfs)
    analyze_sip_inflows(dfs)
    analyze_category_inflows(dfs)
    analyze_portfolio_holdings(dfs)
    analyze_investor_transactions(dfs)
    analyze_benchmark_indices(dfs)
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()