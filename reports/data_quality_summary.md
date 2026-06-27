# Data Quality Summary — Day 1

## Files in data/raw/
- axis_bluechip.csv (75.0 KB)
- fund_master.csv (2939.8 KB)
- icici_bluechip.csv (65.0 KB)
- kotak_bluechip.csv (65.7 KB)
- nippon_large_cap.csv (64.6 KB)
- sbi_bluechip.csv (66.4 KB)
- sbi_small_cap.csv (61.6 KB)
- sbi_small_cap_nav.csv (61.6 KB)

## NAV Data Quality
- SBI Small Cap: 3109 records, 0 missing values
- SBI Bluechip: 3254 records, 0 missing values
- ICICI Bluechip: 3325 records, 0 missing values
- Nippon Large Cap: 3316 records, 0 missing values
- Axis Bluechip: 3583 records, 0 missing values
- Kotak Bluechip: 3319 records, 0 missing values

## Anomalies Found
- Scheme codes in task did not match expected fund names
- ISIN data missing for 78-89% of funds (likely legacy/inactive schemes)
- Date column reverts to string after CSV save/load (requires parse_dates on read)

## Fund Master
- Total funds: 37,647
- Missing ISIN Growth: 29,220 (77.6%)
- Missing ISIN Div Reinvestment: 33,506 (89.0%)
