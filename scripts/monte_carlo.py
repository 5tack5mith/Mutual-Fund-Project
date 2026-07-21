"""
B3 — Monte Carlo Simulation
Projects NAV growth over 5 years with uncertainty bands
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'
CHARTS_DIR = BASE_DIR / 'reports' / 'charts'

def run_monte_carlo(nav_series, n_simulations=1000, n_days=252*5):
    """
    Simulate n_simulations possible NAV paths over n_days
    using historical daily returns
    """
    # Calculate historical daily returns
    daily_returns = nav_series.pct_change().dropna()
    
    # Get mean and std of daily returns
    mu = daily_returns.mean()
    sigma = daily_returns.std()
    
    # Starting NAV
    start_nav = nav_series.iloc[-1]
    
    # Run simulations
    simulations = np.zeros((n_days, n_simulations))
    
    for i in range(n_simulations):
        # Generate random daily returns
        random_returns = np.random.normal(mu, sigma, n_days)
        
        # Calculate NAV path
        price_path = start_nav * np.cumprod(1 + random_returns)
        simulations[:, i] = price_path
    
    return simulations

def plot_monte_carlo(simulations, fund_name, start_nav):
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Plot all simulations in light grey
    ax.plot(simulations, color='lightgrey', alpha=0.1, linewidth=0.5)
    
    # Plot percentile bands
    p5 = np.percentile(simulations, 5, axis=1)
    p25 = np.percentile(simulations, 25, axis=1)
    p50 = np.percentile(simulations, 50, axis=1)
    p75 = np.percentile(simulations, 75, axis=1)
    p95 = np.percentile(simulations, 95, axis=1)
    
    days = range(len(p50))
    
    ax.fill_between(days, p5, p95, alpha=0.2, color='blue', label='5th-95th percentile')
    ax.fill_between(days, p25, p75, alpha=0.3, color='blue', label='25th-75th percentile')
    ax.plot(days, p50, color='blue', linewidth=2.5, label='Median projection')
    ax.plot(days, p5, color='red', linewidth=1.5, linestyle='--', label='Worst case (5th %ile)')
    ax.plot(days, p95, color='green', linewidth=1.5, linestyle='--', label='Best case (95th %ile)')
    
    # Add horizontal line for starting NAV
    ax.axhline(y=start_nav, color='black', linestyle=':', linewidth=1, label=f'Current NAV ₹{start_nav:.2f}')
    
    # Format x-axis as years
    year_ticks = [252*i for i in range(6)]
    ax.set_xticks(year_ticks)
    ax.set_xticklabels([f'Year {i}' for i in range(6)])
    
    ax.set_title(f'Monte Carlo Simulation — {fund_name}\n1,000 simulations over 5 years', 
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('Time')
    ax.set_ylabel('Projected NAV (₹)')
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def run():
    print("Running Monte Carlo simulations...")
    
    nav = pd.read_csv(PROCESSED_DIR / '02_nav_history_clean.csv', parse_dates=['date'])
    funds = pd.read_csv(PROCESSED_DIR / '01_fund_master_clean.csv')
    
    # Run for 5 selected funds
    selected_codes = [119551, 120503, 118632, 119092, 125497]
    
    results = []
    
    for code in selected_codes:
        fund_nav = nav[nav['amfi_code'] == code].sort_values('date')['nav']
        fund_name = funds[funds['amfi_code'] == code]['scheme_name'].values[0]
        short_name = fund_name[:40]
        start_nav = fund_nav.iloc[-1]
        
        print(f"Simulating {short_name}...")
        
        # Run simulation
        simulations = run_monte_carlo(fund_nav)
        
        # Plot
        fig = plot_monte_carlo(simulations, short_name, start_nav)
        chart_path = CHARTS_DIR / f'monte_carlo_{code}.png'
        fig.savefig(chart_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        # Summary stats
        final_values = simulations[-1, :]
        results.append({
            'amfi_code': code,
            'fund_name': short_name,
            'current_nav': round(start_nav, 2),
            'median_5yr_nav': round(np.percentile(final_values, 50), 2),
            'best_case_nav': round(np.percentile(final_values, 95), 2),
            'worst_case_nav': round(np.percentile(final_values, 5), 2),
            'prob_double': round((final_values > start_nav * 2).mean() * 100, 1)
        })
        
        print(f"  Current NAV: ₹{start_nav:.2f}")
        print(f"  Median 5yr projection: ₹{results[-1]['median_5yr_nav']}")
        print(f"  Probability of doubling: {results[-1]['prob_double']}%")
    
    # Save results
    df_results = pd.DataFrame(results)
    df_results.to_csv(PROCESSED_DIR / 'monte_carlo_results.csv', index=False)
    print("\n✅ Monte Carlo complete!")
    print(df_results[['fund_name', 'current_nav', 'median_5yr_nav', 'prob_double']])

if __name__ == "__main__":
    run()