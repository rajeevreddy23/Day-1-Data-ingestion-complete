#!/usr/bin/env python3
"""Bluestock MF Capstone - Interactive Dashboard (Plotly)"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from pathlib import Path

DATA_DIR = r'C:\blue\drive-download-20260902T170546Z-1-001'

def create_dashboard():
    """Create interactive dashboard with all analyses"""
    
    # Load data
    dfs = {}
    for f in ['01_fund_master.csv', '02_nav_history.csv', '03_aum_by_fund_house.csv',
              '04_monthly_sip_inflows.csv', '05_category_inflows.csv', 
              '06_industry_folio_count.csv', '07_scheme_performance.csv',
              '08_investor_transactions.csv', '09_portfolio_holdings.csv', '10_benchmark_indices.csv']:
        df = pd.read_csv(os.path.join(DATA_DIR, f))
        # Convert types
        dfs[f] = df
    
    dfs['02_nav_history.csv']['date'] = pd.to_datetime(dfs['02_nav_history.csv']['date'])
    dfs['02_nav_history.csv']['nav'] = dfs['02_nav_history.csv']['nav'].astype(float)
    dfs['03_aum_by_fund_house.csv']['date'] = pd.to_datetime(dfs['03_aum_by_fund_house.csv']['date'])
    dfs['04_monthly_sip_inflows.csv']['month'] = pd.to_datetime(dfs['04_monthly_sip_inflows.csv']['month'] + '-01')
    dfs['05_category_inflows.csv']['month'] = pd.to_datetime(dfs['05_category_inflows.csv']['month'] + '-01')
    dfs['06_industry_folio_count.csv']['month'] = pd.to_datetime(dfs['06_industry_folio_count.csv']['month'] + '-01')
    dfs['07_scheme_performance.csv'] = dfs['07_scheme_performance.csv'].astype({'amfi_code': 'int'})
    dfs['08_investor_transactions.csv']['transaction_date'] = pd.to_datetime(dfs['08_investor_transactions.csv']['transaction_date'])
    dfs['08_investor_transactions.csv']['amount_inr'] = dfs['08_investor_transactions.csv']['amount_inr'].astype(float)
    dfs['09_portfolio_holdings.csv']['amfi_code'] = dfs['09_portfolio_holdings.csv']['amfi_code'].astype(int)
    dfs['09_portfolio_holdings.csv']['weight_pct'] = dfs['09_portfolio_holdings.csv']['weight_pct'].astype(float)
    dfs['10_benchmark_indices.csv']['date'] = pd.to_datetime(dfs['10_benchmark_indices.csv']['date'])
    dfs['10_benchmark_indices.csv']['close_value'] = dfs['10_benchmark_indices.csv']['close_value'].astype(float)
    
    # ==========================================
    # Figure 1: AUM Trends by Fund House
    # ==========================================
    fig1 = go.Figure()
    aum = dfs['03_aum_by_fund_house.csv']
    for fund_house in aum['fund_house'].unique():
        fdf = aum[aum['fund_house'] == fund_house]
        fig1.add_trace(go.Scatter(
            x=fdf['date'], 
            y=fdf['aum_lakh_crore'],
            name=fund_house,
            mode='lines+markers'
        ))
    fig1.update_layout(
        title='AUM Growth by Fund House (2022-2025)',
        xaxis_title='Date',
        yaxis_title='AUM (Lakh Crore ₹)',
        hovermode='x unified',
        height=500
    )
    
    # ==========================================
    # Figure 2: SIP Inflows Over Time
    # ==========================================
    fig2 = go.Figure()
    sip = dfs['04_monthly_sip_inflows.csv']
    fig2.add_trace(go.Bar(
        x=sip['month'], 
        y=sip['sip_inflow_crore'],
        name='SIP Inflow (Crore)',
        marker_color='green'
    ))
    fig2.update_layout(
        title='Monthly SIP Inflows (Jan 2022 - Dec 2025)',
        xaxis_title='Month',
        yaxis_title='SIP Inflow (Crore ₹)',
        height=500,
        showlegend=False
    )
    
    # ==========================================
    # Figure 3: Category Inflows (Latest Month)
    # ==========================================
    fig3 = go.Figure()
    cat = dfs['05_category_inflows.csv']
    latest_month = cat['month'].max()
    latest = cat[cat['month'] == latest_month]
    
    fig3.add_trace(go.Bar(
        y=latest['category'],
        x=latest['net_inflow_crore'],
        orientation='h',
        marker_color='blue'
    ))
    fig3.update_layout(
        title=f'Category-wise Net Inflows ({latest_month.strftime("%b-%y")})',
        xaxis_title='Net Inflow (Crore ₹)',
        yaxis_title='Category',
        height=500,
        width=800
    )
    
    # ==========================================
    # Figure 4: Portfolio Sector Allocation
    # ==========================================
    fig4 = go.Figure()
    pf = dfs['09_portfolio_holdings.csv']
    sector_alloc = pf.groupby('sector')['weight_pct'].sum().sort_values(ascending=False).head(10)
    
    fig4.add_trace(go.Pie(
        labels=sector_alloc.index,
        values=sector_alloc.values,
        hole=0.4,
        title='Top 10 Sector Allocation Across Schemes'
    ))
    fig4.update_layout(
        title='Portfolio Sector Distribution',
        height=500
    )
    
    # ==========================================
    # Figure 5: Investor Transaction Analysis
    # ==========================================
    fig5 = make_subplots(rows=2, cols=2, subplot_titles=(
        'Transaction Types', 'Top States', 'Age Group Distribution', 'KYC Status'
    ))
    
    txn = dfs['08_investor_transactions.csv']
    
    # Transaction types
    fig5.add_trace(
        go.Pie(labels=txn['transaction_type'].unique(), 
               values=txn['transaction_type'].value_counts(),
               name="Types"),
        row=1, col=1
    )
    
    # Top states
    top_states = txn['state'].value_counts().head(8)
    fig5.add_trace(
        go.Bar(x=top_states.index, y=top_states.values, name="States"),
        row=1, col=2
    )
    
    # Age groups
    fig5.add_trace(
        go.Pie(labels=txn['age_group'].unique(),
               values=txn['age_group'].value_counts(),
               name="Age Groups"),
        row=2, col=1
    )
    
    # KYC status
    fig5.add_trace(
        go.Pie(labels=txn['kyc_status'].unique(),
               values=txn['kyc_status'].value_counts(),
               name="KYC Status"),
        row=2, col=2
    )
    
    fig5.update_layout(height=800, showlegend=False)
    
    # ==========================================
    # Figure 6: NAV Performance Comparison
    # ==========================================
    fig6 = go.Figure()
    nav = dfs['02_nav_history.csv']
    fund_master = dfs['01_fund_master.csv']
    
    # Select representative funds
    selected_funds = [119551, 119552, 100016, 118632]  # SBI Bluechip Regular, Direct, HDFC Top 100 Regular, Nippon Large Cap
    
    for amfi in selected_funds:
        fund_nav = nav[nav['amfi_code'] == amfi].sort_values('date')
        fm_row = fund_master[fund_master['amfi_code'] == amfi]
        scheme_name = fm_row['scheme_name'].values[0] if len(fm_row) > 0 else f"AMFI {amfi}"
        
        start_nav = fund_nav.iloc[0]['nav']
        end_nav = fund_nav.iloc[-1]['nav']
        ret = (end_nav - start_nav) / start_nav * 100
        
        fig6.add_trace(go.Scatter(
            x=fund_nav['date'],
            y=fund_nav['nav'],
            name=f"{scheme_name[:30]}...: {ret:.1f}%",
            lines=dict(width=2)
        ))
    
    # Add benchmark
    bench = dfs['10_benchmark_indices.csv']
    nifty50 = bench[bench['index_name'] == 'NIFTY50'].sort_values('date')
    fig6.add_trace(go.Scatter(
        x=nifty50['date'],
        y=nifty50['close_value'],
        name="NIFTY50 Benchmark",
        line=dict(color='red', dash='dash', width=2)
    ))
    
    fig6.update_layout(
        title='NAV Performance vs NIFTY50 Benchmark',
        xaxis_title='Date',
        yaxis_title='NAV / Index Value',
        height=600,
        hovermode='x unified'
    )
    
    # ==========================================
    # Figure 7: Benchmark Index Values
    # ==========================================
    fig7 = go.Figure()
    for idx in dfs['10_benchmark_indices.csv']['index_name'].unique()[:6]:
        idx_data = dfs['10_benchmark_indices.csv'][dfs['10_benchmark_indices.csv']['index_name'] == idx]
        fig7.add_trace(go.Scatter(
            x=idx_data['date'],
            y=idx_data['close_value'],
            name=idx,
            mode='lines'
        ))
    
    fig7.update_layout(
        title='Benchmark Indices (NIFTY50, NIFTY100) Trend',
        xaxis_title='Date',
        yaxis_title='Close Value',
        height=500,
        hovermode='x unified'
    )
    
    # ==========================================
    # Figure 8: SIP Growth + Folio Count
    # ==========================================
    fig8 = make_subplots(rows=1, cols=2, subplot_titles=('SIP Inflows', 'Industry Folio Count'))
    
    sip = dfs['04_monthly_sip_inflows.csv']
    fig8.add_trace(go.Scatter(
        x=sip['month'], 
        y=sip['sip_inflow_crore'],
        name='SIP Inflow',
        line=dict(color='green')
    ), row=1, col=1)
    
    folio = dfs['06_industry_folio_count.csv']
    fig8.add_trace(go.Scatter(
        x=folio['month'], 
        y=folio['equity_folios_crore'],
        name='Equity Folios (Crore)',
        line=dict(color='blue')
    ), row=1, col=2)
    
    fig8.update_layout(height=500, showlegend=False)
    
    # ==========================================
    # Save all figures as HTML
    # ==========================================
    output_dir = Path(DATA_DIR) / "outputs"
    output_dir.mkdir(exist_ok=True)
    
    fig1.write_html(str(output_dir / "aum_trends.html"))
    fig2.write_html(str(output_dir / "sip_inflows.html"))
    fig3.write_html(str(output_dir / "category_inflows.html"))
    fig4.write_html(str(output_dir / "portfolio_allocation.html"))
    fig5.write_html(str(output_dir / "investor_analysis.html"))
    fig6.write_html(str(output_dir / "nav_performance.html"))
    fig7.write_html(str(output_dir / "benchmarks.html"))
    fig8.write_html(str(output_dir / "sip_folio_correlation.html"))
    
    print(f"Dashboard HTML files saved to: {output_dir}")
    return output_dir

if __name__ == "__main__":
    import os
    output = create_dashboard()
    print("\nDashboard generated successfully!")
    print(f"Open the HTML files in any web browser to interact with the charts.")