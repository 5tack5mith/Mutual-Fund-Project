# Data Dictionary — Bluestock Mutual Fund Analytics

## dim_fund
Master table containing details of all 40 mutual fund schemes.

| Column | Type | Description |
|---|---|---|
| amfi_code | INTEGER (PK) | Unique AMFI scheme code identifying the fund |
| fund_house | TEXT | Asset Management Company managing the fund |
| scheme_name | TEXT | Official name of the fund scheme |
| category | TEXT | Equity / Debt / Hybrid |
| sub_category | TEXT | Large Cap / Mid Cap / Small Cap / Liquid etc. |
| plan | TEXT | Direct or Regular plan |
| launch_date | DATE | Date the fund was launched |
| benchmark | TEXT | Index the fund is benchmarked against |
| expense_ratio_pct | REAL | Annual fee charged by the fund (%) |
| risk_category | TEXT | SEBI risk classification |

## fact_nav
Daily Net Asset Value for each fund, including weekends/holidays (forward-filled).

| Column | Type | Description |
|---|---|---|
| amfi_code | INTEGER (FK) | References dim_fund |
| date | DATE | NAV date |
| nav | REAL | Net Asset Value in Rs. |

## fact_transactions
Investor transaction records — SIP, Lumpsum, and Redemption activity.

| Column | Type | Description |
|---|---|---|
| investor_id | TEXT | Unique investor identifier |
| transaction_date | DATE | Date of transaction |
| amfi_code | INTEGER (FK) | References dim_fund |
| transaction_type | TEXT | SIP / Lumpsum / Redemption |
| amount_inr | INTEGER | Transaction amount in Rupees |
| state | TEXT | Investor's state |
| city | TEXT | Investor's city |
| age_group | TEXT | Investor's age bracket |
| kyc_status | TEXT | Verified / Pending |

## fact_performance
Performance and risk metrics per fund.

| Column | Type | Description |
|---|---|---|
| amfi_code | INTEGER (FK) | References dim_fund |
| return_1yr_pct | REAL | 1-year absolute return (%) |
| return_3yr_pct | REAL | 3-year CAGR (%) |
| sharpe_ratio | REAL | Risk-adjusted return measure (higher is better) |
| expense_ratio_pct | REAL | Annual fee (%) |
| aum_crore | INTEGER | Assets Under Management in Rs. crore |

## Data Quality Notes

- nav_history expanded from 46,000 trading-day records to 64,320 calendar-day records via forward-fill for weekends/holidays
- All expense ratios validated within SEBI range (0.1% - 2.5%)
- KYC status standardised to two values: Verified, Pending
- No duplicate records found in source data
- yoy_growth_pct in monthly SIP data is null for 2022 (no prior year to compare against) — expected, not an error
