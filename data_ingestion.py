import requests
import pandas as pd
import os

def fetch_fund_master():
    """Fetch all funds from AMFI via mfapi"""
    url = "https://api.mfapi.in/mf"
    response = requests.get(url)
    fund_master = response.json()
    
    df = pd.DataFrame(fund_master)
    
    os.makedirs('data/raw', exist_ok=True)
    df.to_csv('data/raw/fund_master.csv', index=False)
    
    print(f"✅ Fund master saved — {len(df)} funds")
    return df

def explore_fund_master(df):
    """Print summary statistics of fund master"""
    print("\n" + "="*50)
    print("FUND MASTER EXPLORATION")
    print("="*50)
    print(f"Total funds: {len(df)}")
    
    keywords = ['SBI', 'HDFC', 'ICICI', 'Axis', 'Nippon', 'Kotak']
    print("\nFunds per house:")
    for keyword in keywords:
        count = df['schemeName'].str.contains(keyword, case=False).sum()
        print(f"  {keyword}: {count}")
    
    print("\nMissing values:")
    print(df.isnull().sum())

def data_quality_summary(nav_files):
    """Print data quality report for all NAV files"""
    print("\n" + "="*50)
    print("DATA QUALITY SUMMARY")
    print("="*50)
    
    for name, path in nav_files.items():
        df = pd.read_csv(path)
        missing = df.isnull().sum().sum()
        print(f"  {name}: {len(df)} records, {missing} missing values")

if __name__ == "__main__":
    # Step 1 - Fetch fund master
    df_master = fetch_fund_master()
    
    # Step 2 - Explore it
    explore_fund_master(df_master)
    
    # Step 3 - Quality summary
    nav_files = {
        'SBI Small Cap': 'data/raw/sbi_small_cap.csv',
        'SBI Bluechip': 'data/raw/sbi_bluechip.csv',
        'ICICI Bluechip': 'data/raw/icici_bluechip.csv',
        'Nippon Large Cap': 'data/raw/nippon_large_cap.csv',
        'Axis Bluechip': 'data/raw/axis_bluechip.csv',
        'Kotak Bluechip': 'data/raw/kotak_bluechip.csv',
    }
    data_quality_summary(nav_files)