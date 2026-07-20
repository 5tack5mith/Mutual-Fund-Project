import requests
import pandas as pd
import os
from datetime import datetime

def fetch_and_save_nav(scheme_code, filename):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    response = requests.get(url)
    fund_data = response.json()
    
    fund_name = fund_data['meta']['scheme_name']
    
    df = pd.DataFrame(fund_data['data'])
    df['nav'] = pd.to_numeric(df['nav'])
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    
    os.makedirs('data/raw', exist_ok=True)
    df.to_csv(f'data/raw/{filename}.csv', index=False)
    
    print(f"✅ {fund_name} — {len(df)} records saved")
    return df

if __name__ == "__main__":
    funds = {
        125497: 'sbi_small_cap',
        119551: 'sbi_bluechip',
        120503: 'icici_bluechip',
        118632: 'nippon_large_cap',
        119092: 'axis_bluechip',
        120841: 'kotak_bluechip'
    }
    
    print(f"Fetching NAV data — {datetime.today().strftime('%d %b %Y')}")
    for code, name in funds.items():
        fetch_and_save_nav(code, name)
    print("\nDone! All files saved to data/raw/")