
CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code INTEGER PRIMARY KEY,
    fund_house TEXT,
    scheme_name TEXT,
    category TEXT,
    sub_category TEXT,
    plan TEXT,
    launch_date DATE,
    benchmark TEXT,
    expense_ratio_pct REAL,
    risk_category TEXT
);

CREATE TABLE IF NOT EXISTS fact_nav (
    amfi_code INTEGER,
    date DATE,
    nav REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE IF NOT EXISTS fact_transactions (
    investor_id TEXT,
    transaction_date DATE,
    amfi_code INTEGER,
    transaction_type TEXT,
    amount_inr INTEGER,
    state TEXT,
    city TEXT,
    age_group TEXT,
    kyc_status TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE IF NOT EXISTS fact_performance (
    amfi_code INTEGER,
    return_1yr_pct REAL,
    return_3yr_pct REAL,
    sharpe_ratio REAL,
    expense_ratio_pct REAL,
    aum_crore INTEGER,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);
