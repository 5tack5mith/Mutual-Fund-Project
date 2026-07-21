"""
B4 — Markowitz Efficient Frontier
Portfolio optimisation for 5 selected funds
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'
CHARTS_DIR = BASE_DIR / 'reports' / 'charts'

def run():
    print("Running Markowitz Efficient Frontier...")
    
    nav = pd.read_csv(PROCESSED_DIR / '02_nav_history_clean.csv', parse_dates=['date'])
    funds = pd.read_csv(PROCESSED_DIR / '01_fund_master_clean.csv')
    
    # Select 5 funds
    selected_codes = [119551, 120503, 118632, 119092, 125497]
    
    # Get fund names
    code_to_name = funds[funds['amfi_code'].isin(selected_codes)].set_index('amfi_code')['scheme_name'].to_dict()
    short_names = {k: v[:25] for k, v in code_to_name.items()}
    
    # Pivot NAV to wide format
    nav_selected = nav[nav['amfi_code'].isin(selected_codes)].copy()
    nav_pivot = nav_selected.pivot_table(index='date', columns='amfi_code', values='nav')
    nav_pivot.columns = [short_names[c] for c in nav_pivot.columns]
    
    # Calculate daily returns
    returns = nav_pivot.pct_change().dropna()
    
    # Annualised metrics
    mean_returns = returns.mean() * 252
    cov_matrix = returns.cov() * 252
    
    print("\nAnnualised Returns:")
    for name, ret in mean_returns.items():
        print(f"  {name[:30]}: {ret*100:.2f}%")
    
    # Monte Carlo portfolio simulation
    n_portfolios = 5000
    results = np.zeros((3, n_portfolios))
    weights_record = []
    
    np.random.seed(42)
    
    for i in range(n_portfolios):
        # Random weights
        weights = np.random.random(len(selected_codes))
        weights /= weights.sum()
        weights_record.append(weights)
        
        # Portfolio return
        port_return = np.dot(weights, mean_returns)
        
        # Portfolio volatility
        port_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        
        # Sharpe ratio
        sharpe = (port_return - 0.065) / port_volatility
        
        results[0, i] = port_return
        results[1, i] = port_volatility
        results[2, i] = sharpe
    
    # Find optimal portfolios
    max_sharpe_idx = results[2].argmax()
    min_vol_idx = results[1].argmin()
    
    print(f"\nMax Sharpe Portfolio:")
    print(f"  Return: {results[0, max_sharpe_idx]*100:.2f}%")
    print(f"  Volatility: {results[1, max_sharpe_idx]*100:.2f}%")
    print(f"  Sharpe: {results[2, max_sharpe_idx]:.3f}")
    print(f"  Weights:")
    for name, w in zip(short_names.values(), weights_record[max_sharpe_idx]):
        print(f"    {name[:30]}: {w*100:.1f}%")
    
    print(f"\nMin Volatility Portfolio:")
    print(f"  Return: {results[0, min_vol_idx]*100:.2f}%")
    print(f"  Volatility: {results[1, min_vol_idx]*100:.2f}%")
    print(f"  Sharpe: {results[2, min_vol_idx]:.3f}")
    
    # Plot
    plt.figure(figsize=(12, 7))
    scatter = plt.scatter(
        results[1] * 100, results[0] * 100,
        c=results[2], cmap='viridis', alpha=0.5, s=10
    )
    plt.colorbar(scatter, label='Sharpe Ratio')
    
    # Mark optimal portfolios
    plt.scatter(results[1, max_sharpe_idx]*100, results[0, max_sharpe_idx]*100,
                marker='*', color='red', s=300, label='Max Sharpe', zorder=5)
    plt.scatter(results[1, min_vol_idx]*100, results[0, min_vol_idx]*100,
                marker='*', color='green', s=300, label='Min Volatility', zorder=5)
    
    plt.title('Markowitz Efficient Frontier — 5 Fund Portfolio', fontsize=14, fontweight='bold')
    plt.xlabel('Annual Volatility (%)')
    plt.ylabel('Annual Return (%)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'markowitz_frontier.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("\n✅ Markowitz Efficient Frontier complete!")
    
    # Save optimal weights
    optimal = pd.DataFrame({
        'fund': list(short_names.values()),
        'max_sharpe_weight': [w*100 for w in weights_record[max_sharpe_idx]],
        'min_vol_weight': [w*100 for w in weights_record[min_vol_idx]]
    })
    optimal.to_csv(PROCESSED_DIR / 'markowitz_optimal_weights.csv', index=False)
    print("✅ Saved markowitz_optimal_weights.csv")

if __name__ == "__main__":
    run()