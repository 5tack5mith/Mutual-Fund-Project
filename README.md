# Mutual Fund Analysis Project

A data analysis project that ingests, processes, and analyses Indian mutual fund NAV data using Python and Pandas.

## Project Structure
mutual_fund_project/

├── data/

│   ├── raw/          # Raw data fetched from API (not tracked in Git)

│   └── processed/    # Cleaned and transformed data

├── notebooks/        # Jupyter notebooks for exploration

├── sql/              # SQL queries

├── dashboard/        # Visualisation files

├── reports/          # Final outputs

├── data_ingestion.py     # Fetches AMFI fund master data

├── live_nav_fetch.py     # Fetches live NAV for key schemes

└── requirements.txt      # Python dependencies

## Data Sources

- [mfapi.in](https://api.mfapi.in) — Free public API for Indian mutual fund NAV history
- AMFI — Association of Mutual Funds in India (37,647 funds)

## Setup

1. Clone the repo
git clone https://github.com/5tack5mith/Mutual-Fund-Project

cd mutual-fund-project

2. Install dependencies
pip install -r requirements.txt

3. Fetch data
python live_nav_fetch.py

python data_ingestion.py

## Funds Tracked

| Scheme Code | Fund |
|---|---|
| 125497 | SBI Small Cap Fund - Direct Plan |
| 119551 | Aditya Birla Sun Life Banking & PSU Debt Fund |
| 120503 | Axis ELSS Tax Saver Fund - Direct Plan |
| 118632 | Nippon India Large Cap Fund - Direct Plan |
| 119092 | HDFC Money Market Fund - Direct Plan |
| 120841 | Quant Mid Cap Fund - Direct Plan |
