
-- Query 1: Funds with expense ratio below 1%
SELECT scheme_name, fund_house, category, expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;

-- Query 2: Number of funds and avg expense ratio per fund house
SELECT fund_house, COUNT(*) as num_funds, AVG(expense_ratio_pct) as avg_expense_ratio
FROM dim_fund
GROUP BY fund_house
ORDER BY num_funds DESC;

-- Query 3: Top 5 funds by 1-year return
SELECT f.scheme_name, f.fund_house, p.return_1yr_pct, p.sharpe_ratio
FROM dim_fund f
JOIN fact_performance p ON f.amfi_code = p.amfi_code
ORDER BY p.return_1yr_pct DESC
LIMIT 5;

-- Query 4: SIP transactions by state
SELECT state, COUNT(*) as num_transactions, SUM(amount_inr) as total_amount
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY state
ORDER BY total_amount DESC;

-- Query 5: Average NAV per month per fund
SELECT amfi_code, strftime('%Y-%m', date) as month, AVG(nav) as avg_nav
FROM fact_nav
GROUP BY amfi_code, month
ORDER BY amfi_code, month;

-- Query 6: Top 5 funds by AUM
SELECT f.scheme_name, f.fund_house, p.aum_crore
FROM dim_fund f
JOIN fact_performance p ON f.amfi_code = p.amfi_code
ORDER BY p.aum_crore DESC
LIMIT 5;

-- Query 7: Transaction breakdown by KYC status
SELECT kyc_status, transaction_type, COUNT(*) as count, SUM(amount_inr) as total_amount
FROM fact_transactions
GROUP BY kyc_status, transaction_type
ORDER BY kyc_status, total_amount DESC;

-- Query 8: Funds with Sharpe ratio above 1
SELECT f.scheme_name, f.category, p.sharpe_ratio, p.return_3yr_pct
FROM dim_fund f
JOIN fact_performance p ON f.amfi_code = p.amfi_code
WHERE p.sharpe_ratio > 1
ORDER BY p.sharpe_ratio DESC;

-- Query 9: Average transaction amount by age group
SELECT age_group, transaction_type, AVG(amount_inr) as avg_amount, COUNT(*) as num_txns
FROM fact_transactions
GROUP BY age_group, transaction_type
ORDER BY age_group, avg_amount DESC;

-- Query 10: Category-wise fund count and average return
SELECT f.category, COUNT(DISTINCT f.amfi_code) as num_funds, 
       ROUND(AVG(p.return_1yr_pct), 2) as avg_1yr_return,
       ROUND(AVG(p.expense_ratio_pct), 2) as avg_expense_ratio
FROM dim_fund f
JOIN fact_performance p ON f.amfi_code = p.amfi_code
GROUP BY f.category
ORDER BY avg_1yr_return DESC;
