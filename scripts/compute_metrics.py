"""
Compute Metrics — Bluestock Mutual Fund Analytics
Computes CAGR, Sharpe, Sortino, Max Drawdown for all funds
"""
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'

def compute_cagr(nav_series, years):
    days = int(years * 365)
    if len(nav_series) < days:
        return np.nan
    return (nav_series.iloc[-1] / nav_series.iloc[-days]) ** (1/years) - 1

def compute_sharpe(returns, rf=0.065/252):
    excess = returns - rf
    return (excess.mean() / returns.std()) * np.sqrt(252)

def compute_max_drawdown(nav_series):
    running_max = nav_series.cummax()
    drawdown = nav_series / running_max - 1
    return drawdown.min()

def run():
    print("Computing metrics for all funds...")
    
    nav = pd.read_csv(PROCESSED_DIR / '02_nav_history_clean.csv', parse_dates=['date'])
    funds = pd.read_csv(PROCESSED_DIR / '01_fund_master_clean.csv')
    
    nav = nav.sort_values(['amfi_code', 'date']).reset_index(drop=True)
    nav['daily_return'] = nav.groupby('amfi_code')['nav'].pct_change()
    
    results = []
    for code in nav['amfi_code'].unique():
        fund_data = nav[nav['amfi_code'] == code]
        returns = fund_data['daily_return'].dropna()
        nav_series = fund_data['nav']
        
        results.append({
            'amfi_code': code,
            'cagr_1yr': compute_cagr(nav_series, 1),
            'cagr_3yr': compute_cagr(nav_series, 3),
            'sharpe_ratio': compute_sharpe(returns),
            'max_drawdown': compute_max_drawdown(nav_series)
        })
    
    df = pd.DataFrame(results)
    df = df.merge(funds[['amfi_code', 'scheme_name']], on='amfi_code')
    df.to_csv(PROCESSED_DIR / 'computed_metrics.csv', index=False)
    print(f"✅ Metrics computed for {len(df)} funds")
    print(df[['scheme_name', 'cagr_3yr', 'sharpe_ratio']].head())

if __name__ == "__main__":
    run()