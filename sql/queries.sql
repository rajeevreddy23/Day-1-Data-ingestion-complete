-- Bluestock Fintech Mutual Fund Analytics Platform
-- 10 Analytical SQL Queries

-- 1. Top 5 Fund Houses by Total AUM (Latest Quarter)
SELECT fund_house, aum_crore, aum_lakh_crore, num_schemes
FROM fact_aum
WHERE date = (SELECT MAX(date) FROM fact_aum)
ORDER BY aum_crore DESC
LIMIT 5;

-- 2. Average Monthly NAV by Scheme (Selected Bluechip Fund)
SELECT 
    strftime('%Y-%m', date) AS year_month,
    COUNT(*) AS trading_days,
    ROUND(AVG(nav), 4) AS avg_nav,
    ROUND(MIN(nav), 4) AS min_nav,
    ROUND(MAX(nav), 4) AS max_nav
FROM fact_nav
WHERE amfi_code = 119551
GROUP BY strftime('%Y-%m', date)
ORDER BY year_month;

-- 3. Monthly SIP Inflow YoY Growth Analysis
SELECT 
    month,
    sip_inflow_crore,
    active_sip_accounts_crore,
    yoy_growth_pct
FROM fact_sip_industry
ORDER BY month DESC
LIMIT 12;

-- 4. Transaction Volume and Total Inflows by Investor State
SELECT 
    state,
    city_tier,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount_inr) / 10000000.0, 2) AS total_inflow_crore,
    ROUND(AVG(amount_inr), 2) AS avg_ticket_size_inr
FROM fact_transactions
GROUP BY state, city_tier
ORDER BY total_inflow_crore DESC
LIMIT 10;

-- 5. Schemes with Expense Ratio Below 1.00%
SELECT 
    amfi_code,
    scheme_name,
    fund_house,
    category,
    sub_category,
    plan,
    expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1.00
ORDER BY expense_ratio_pct ASC;

-- 6. Monthly NAV Performance Trend for Anchor Scheme (125497)
SELECT 
    strftime('%Y-%m', date) AS month,
    MIN(date) AS start_date,
    MAX(date) AS end_date,
    ROUND(AVG(nav), 4) AS monthly_avg_nav
FROM fact_nav
WHERE amfi_code = 125497
GROUP BY strftime('%Y-%m', date)
ORDER BY month;

-- 7. SIP vs. Lumpsum Investment Split by Transaction Type
SELECT 
    transaction_type,
    COUNT(*) AS total_tx_count,
    ROUND(SUM(amount_inr) / 10000000.0, 2) AS total_volume_crore,
    ROUND(AVG(amount_inr), 2) AS avg_ticket_inr,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM fact_transactions), 2) AS pct_share_tx
FROM fact_transactions
GROUP BY transaction_type;

-- 8. Top 10 Schemes by Sharpe Ratio (Risk-Adjusted Return)
SELECT 
    f.amfi_code,
    f.scheme_name,
    f.fund_house,
    f.sub_category,
    p.return_3yr_pct,
    p.sharpe_ratio,
    p.sortino_ratio,
    p.alpha,
    p.morningstar_rating
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.sharpe_ratio DESC
LIMIT 10;

-- 9. Geographic Tier 1 (T30) vs Tier 2+ (B30) SIP Penetration
SELECT 
    city_tier,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_inr) / 10000000.0, 2) AS volume_crore,
    ROUND(AVG(amount_inr), 2) AS avg_sip_amount
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY city_tier;

-- 10. Average 3-Year Annualized Return and Volatility by Sub-Category
SELECT 
    f.sub_category,
    COUNT(f.amfi_code) AS total_schemes,
    ROUND(AVG(p.return_3yr_pct), 2) AS avg_return_3yr_pct,
    ROUND(AVG(p.std_dev_ann_pct), 2) AS avg_annual_volatility_pct,
    ROUND(AVG(p.sharpe_ratio), 2) AS avg_sharpe_ratio
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
GROUP BY f.sub_category
ORDER BY avg_return_3yr_pct DESC;