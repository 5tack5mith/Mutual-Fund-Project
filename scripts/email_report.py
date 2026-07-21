"""
B5 — Automated HTML Email Report Generator
Generates weekly mutual fund performance summary as HTML
"""
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'
REPORTS_DIR = BASE_DIR / 'reports'

def generate_html_report():
    # Load data
    funds = pd.read_csv(PROCESSED_DIR / '01_fund_master_clean.csv')
    scorecard = pd.read_csv(PROCESSED_DIR / 'fund_scorecard.csv')
    nav = pd.read_csv(PROCESSED_DIR / '02_nav_history_clean.csv', parse_dates=['date'])
    sip = pd.read_csv(PROCESSED_DIR / '04_monthly_sip_inflows_clean.csv', parse_dates=['month'])
    var_cvar = pd.read_csv(PROCESSED_DIR / 'var_cvar_report.csv')
    
    # Top 5 funds by score
    top5 = scorecard.nlargest(5, 'score')[['scheme_name', 'score', 'cagr_3yr_pct', 'sharpe_ratio', 'max_drawdown_pct']]
    
    # Latest SIP inflow
    latest_sip = sip['sip_inflow_crore'].iloc[-1]
    latest_month = sip['month'].iloc[-1].strftime('%b %Y')
    
    # Latest NAV date
    latest_date = nav['date'].max().strftime('%d %b %Y')
    
    # Riskiest funds
    riskiest = var_cvar.nsmallest(3, 'var_95_pct')[['scheme_name', 'var_95_pct', 'cvar_95_pct']]
    
    # Generate HTML
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; background: #f4f4f4; margin: 0; padding: 20px; }}
        .container {{ max-width: 700px; margin: auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ background: #5B4FCF; color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 24px; }}
        .header p {{ margin: 5px 0 0; opacity: 0.8; font-size: 14px; }}
        .section {{ padding: 25px 30px; border-bottom: 1px solid #eee; }}
        .section h2 {{ color: #5B4FCF; font-size: 16px; margin: 0 0 15px; }}
        .kpi-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }}
        .kpi {{ background: #f8f7ff; border-radius: 8px; padding: 15px; text-align: center; border-left: 4px solid #5B4FCF; }}
        .kpi-value {{ font-size: 22px; font-weight: bold; color: #5B4FCF; }}
        .kpi-label {{ font-size: 11px; color: #666; margin-top: 4px; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
        th {{ background: #5B4FCF; color: white; padding: 10px; text-align: left; }}
        td {{ padding: 9px 10px; border-bottom: 1px solid #eee; }}
        tr:nth-child(even) {{ background: #f8f7ff; }}
        .risk {{ color: #e53e3e; font-weight: bold; }}
        .footer {{ background: #1E1E2E; color: #aaa; padding: 20px; text-align: center; font-size: 12px; }}
        .badge {{ display: inline-block; background: #F97316; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; }}
    </style>
</head>
<body>
<div class="container">
    
    <div class="header">
        <h1>📈 Bluestock MF Weekly Report</h1>
        <p>Generated: {datetime.today().strftime('%A, %d %B %Y')} | Data as of {latest_date}</p>
    </div>

    <div class="section">
        <h2>📊 Industry Snapshot</h2>
        <div class="kpi-grid">
            <div class="kpi">
                <div class="kpi-value">₹{latest_sip:,.0f} Cr</div>
                <div class="kpi-label">SIP Inflow ({latest_month})</div>
            </div>
            <div class="kpi">
                <div class="kpi-value">40</div>
                <div class="kpi-label">Schemes Tracked</div>
            </div>
            <div class="kpi">
                <div class="kpi-value">32,778</div>
                <div class="kpi-label">Investor Transactions</div>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>🏆 Top 5 Funds This Week <span class="badge">By Composite Score</span></h2>
        <table>
            <tr>
                <th>Fund</th>
                <th>Score</th>
                <th>3yr CAGR%</th>
                <th>Sharpe</th>
                <th>Max DD%</th>
            </tr>
            {''.join(f"""
            <tr>
                <td>{row['scheme_name'][:45]}</td>
                <td><b>{round(row['score'], 1)}</b></td>
                <td>{round(row['cagr_3yr_pct'], 2)}%</td>
                <td>{round(row['sharpe_ratio'], 3)}</td>
                <td class="risk">{round(row['max_drawdown_pct'], 2)}%</td>
            </tr>
            """ for _, row in top5.iterrows())}
        </table>
    </div>

    <div class="section">
        <h2>⚠️ Risk Alert — Highest VaR Funds</h2>
        <table>
            <tr>
                <th>Fund</th>
                <th>VaR 95%</th>
                <th>CVaR 95%</th>
            </tr>
            {''.join(f"""
            <tr>
                <td>{row['scheme_name'][:45]}</td>
                <td class="risk">{round(row['var_95_pct'], 4)}%</td>
                <td class="risk">{round(row['cvar_95_pct'], 4)}%</td>
            </tr>
            """ for _, row in riskiest.iterrows())}
        </table>
    </div>

    <div class="section">
        <h2>💡 Key Insights This Week</h2>
        <ul style="font-size: 13px; color: #444; line-height: 1.8;">
            <li>ICICI Pru Midcap leads the Fund Scorecard at <b>85.1</b> — best risk-return balance</li>
            <li>SIP inflows reached <b>₹{latest_sip:,.0f} Cr</b> in {latest_month} — industry momentum strong</li>
            <li>Small Cap funds carry highest VaR — suitable only for high risk appetite investors</li>
            <li>97.8% of investors show irregular SIP patterns — continuity intervention recommended</li>
            <li>Axis Bluechip most concentrated portfolio (HHI ~3000) — sector risk elevated</li>
        </ul>
    </div>

    <div class="footer">
        <p>Bluestock Fintech Pvt. Ltd. | Mutual Fund Analytics Platform</p>
        <p>This report is auto-generated for internal use only. Not financial advice.</p>
        <p>© 2026 Bluestock Fintech | Data Source: AMFI India, mfapi.in</p>
    </div>

</div>
</body>
</html>
"""
    
    # Save HTML report
    output_path = REPORTS_DIR / f"weekly_report_{datetime.today().strftime('%Y%m%d')}.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ HTML report generated: {output_path.name}")
    return output_path

if __name__ == "__main__":
    path = generate_html_report()
    print(f"\nOpen this file in your browser to preview:")
    print(f"  {path}")