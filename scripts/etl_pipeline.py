"""
ETL Pipeline — Bluestock Mutual Fund Analytics
Fetches live NAV data from mfapi.in and saves to data/raw/
"""
import requests
import pandas as pd
import os
from datetime import datetime
from pathlib import Path

# Use pathlib for cross-platform paths
BASE_DIR = Path(__file__).parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw'
RAW_DIR.mkdir(parents=True, exist_ok=True)

FUNDS = {
    125497: 'sbi_small_cap',
    119551: 'sbi_bluechip',
    120503: 'icici_bluechip',
    118632: 'nippon_large_cap',
    119092: 'axis_bluechip',
    120841: 'kotak_bluechip'
}

def fetch_nav(scheme_code, filename):
    """Fetch NAV history from mfapi.in and save as CSV"""
    try:
        url = f"https://api.mfapi.in/mf/{scheme_code}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        fund_data = response.json()
        fund_name = fund_data['meta']['scheme_name']
        
        df = pd.DataFrame(fund_data['data'])
        df['nav'] = pd.to_numeric(df['nav'], errors='coerce')
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
        df = df.dropna(subset=['nav'])
        
        output_path = RAW_DIR / f"{filename}.csv"
        df.to_csv(output_path, index=False)
        print(f"✅ {fund_name} — {len(df)} records saved")
        return df
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch {scheme_code}: {e}")
        return None

def run_pipeline():
    print(f"ETL Pipeline started — {datetime.today().strftime('%d %b %Y %H:%M')}")
    print("="*50)
    
    for code, name in FUNDS.items():
        fetch_nav(code, name)
    
    print("="*50)
    print("Pipeline complete!")

if __name__ == "__main__":
    run_pipeline()