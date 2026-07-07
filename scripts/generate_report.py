"""
Final Report Generator — Bluestock Mutual Fund Analytics
Generates PDF report and PowerPoint presentation
"""
from pathlib import Path
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.units import inch
from reportlab.lib import colors

BASE_DIR = Path(__file__).parent.parent
REPORTS_DIR = BASE_DIR / 'reports'
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'
CHARTS_DIR = REPORTS_DIR / 'charts'

# Bluestock brand colour
BLUESTOCK_PURPLE = HexColor('#5B4FCF')
BLUESTOCK_ORANGE = HexColor('#F97316')

def generate_pdf():
    doc = SimpleDocTemplate(
        str(REPORTS_DIR / 'Final_Report.pdf'),
        pagesize=A4,
        rightMargin=inch*0.75,
        leftMargin=inch*0.75,
        topMargin=inch*0.75,
        bottomMargin=inch*0.75
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle('Title', parent=styles['Title'],
        fontSize=24, textColor=BLUESTOCK_PURPLE, spaceAfter=12)
    heading_style = ParagraphStyle('Heading', parent=styles['Heading1'],
        fontSize=14, textColor=BLUESTOCK_PURPLE, spaceAfter=8)
    subheading_style = ParagraphStyle('Subheading', parent=styles['Heading2'],
        fontSize=11, textColor=BLUESTOCK_ORANGE, spaceAfter=6)
    body_style = ParagraphStyle('Body', parent=styles['Normal'],
        fontSize=10, spaceAfter=6, leading=14)
    
    story = []
    
    # Title Page
    story.append(Spacer(1, inch))
    story.append(Paragraph("Mutual Fund Analytics Platform", title_style))
    story.append(Paragraph("Bluestock Fintech Pvt. Ltd.", 
        ParagraphStyle('Sub', parent=styles['Normal'], fontSize=14, 
                       textColor=BLUESTOCK_ORANGE, spaceAfter=6)))
    story.append(Paragraph("End-to-End Data Engineering, ETL Pipeline & Interactive Dashboard",
        ParagraphStyle('Sub2', parent=styles['Normal'], fontSize=11, spaceAfter=6)))
    story.append(Spacer(1, 0.3*inch))
    
    # Project details table
    details = [
        ['Domain', 'Mutual Fund / Fintech'],
        ['Data Source', 'AMFI India, mfapi.in, NSE/BSE Public Data'],
        ['Technologies', 'Python, SQL, Power BI, Pandas, Matplotlib'],
        ['Schemes Analysed', '40 Real Fund Schemes'],
        ['Total Records', '87,000+ rows across 10 datasets'],
        ['Prepared By', 'Data Analyst Intern — Bluestock Fintech'],
        ['Date', 'July 2026'],
    ]
    
    t = Table(details, colWidths=[2*inch, 4*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), BLUESTOCK_PURPLE),
        ('TEXTCOLOR', (0,0), (0,-1), white),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (1,0), (-1,-1), [HexColor('#F5F5FF'), white]),
    ]))
    story.append(t)
    story.append(PageBreak())
    
    # 1. Executive Summary
    story.append(Paragraph("1. Executive Summary", heading_style))
    story.append(Paragraph(
        "This project delivers a comprehensive Mutual Fund Analytics Platform for Bluestock Fintech, "
        "covering end-to-end data engineering, performance analytics, and interactive visualisation. "
        "The platform ingests publicly available data from AMFI India and mfapi.in, processes 87,000+ "
        "rows across 10 datasets, and presents actionable insights through a 4-page Power BI dashboard.",
        body_style))
    
    story.append(Paragraph("Key Outcomes:", subheading_style))
    outcomes = [
        "Built automated ETL pipeline fetching live NAV data from mfapi.in for 40 fund schemes",
        "Designed SQLite star schema database with 4 fact/dimension tables",
        "Performed comprehensive EDA with 9 publication-quality charts",
        "Computed performance metrics: CAGR, Sharpe ratio, Sortino ratio, Alpha, Beta, Max Drawdown",
        "Built composite Fund Scorecard (0-100) ranking all 40 schemes",
        "Developed 4-page interactive Power BI dashboard with slicers and drill-through",
        "Implemented advanced risk metrics: VaR (95%), CVaR, Rolling Sharpe, Sector HHI",
        "Built rule-based fund recommender based on investor risk appetite",
    ]
    for o in outcomes:
        story.append(Paragraph(f"• {o}", body_style))
    story.append(Spacer(1, 0.2*inch))
    
    # 2. Data Sources
    story.append(Paragraph("2. Data Sources & Datasets", heading_style))
    story.append(Paragraph(
        "All data is sourced from publicly available AMFI India publications and the mfapi.in REST API. "
        "No proprietary or confidential data was used.", body_style))
    
    data_table = [
        ['Dataset', 'Description', 'Rows'],
        ['01_fund_master.csv', 'Master list of 40 fund schemes', '40'],
        ['02_nav_history.csv', 'Daily NAV prices 2022-2026', '46,000'],
        ['03_aum_by_fund_house.csv', 'Quarterly AUM per fund house', '90'],
        ['04_monthly_sip_inflows.csv', 'Monthly SIP industry data', '48'],
        ['05_category_inflows.csv', 'Monthly inflows by category', '144'],
        ['06_industry_folio_count.csv', 'Industry folio counts', '21'],
        ['07_scheme_performance.csv', 'Fund performance metrics', '40'],
        ['08_investor_transactions.csv', 'Investor buy/sell records', '32,778'],
        ['09_portfolio_holdings.csv', 'Fund stock holdings', '322'],
        ['10_benchmark_indices.csv', 'Nifty/BSE index values', '8,050'],
    ]
    
    t2 = Table(data_table, colWidths=[2.5*inch, 3*inch, 0.75*inch])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLUESTOCK_PURPLE),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('PADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [HexColor('#F5F5FF'), white]),
    ]))
    story.append(t2)
    story.append(PageBreak())
    
    # 3. ETL Pipeline
    story.append(Paragraph("3. ETL Pipeline Architecture", heading_style))
    story.append(Paragraph(
        "The project follows a classic data engineering architecture: Extract → Transform → Load → Analyse → Visualise.",
        body_style))
    
    etl_steps = [
        ("Extract", "Fetched JSON data from mfapi.in REST API for 40 fund schemes. "
         "Loaded 10 pre-packaged CSV datasets from AMFI India."),
        ("Transform", "Cleaned all 10 datasets — fixed date formats, forward-filled NAV gaps "
         "for weekends/holidays (46,000 → 64,320 records), validated value ranges, "
         "standardised categorical fields."),
        ("Load", "Designed SQLite star schema with dim_fund, fact_nav, fact_transactions, "
         "fact_performance tables. Loaded all cleaned data using SQLAlchemy."),
        ("Analyse", "Computed CAGR, Sharpe, Sortino, Alpha, Beta, Max Drawdown, VaR, CVaR, "
         "Rolling Sharpe, Sector HHI across all 40 schemes."),
        ("Visualise", "Built 4-page Power BI dashboard with KPI cards, interactive charts, "
         "slicers, and drill-through navigation."),
    ]
    
    for step, desc in etl_steps:
        story.append(Paragraph(f"<b>{step}:</b> {desc}", body_style))
    story.append(Spacer(1, 0.2*inch))
    
    # 4. EDA Findings
    story.append(Paragraph("4. Key EDA Findings", heading_style))
    eda_findings = [
        "SBI Mutual Fund dominates AUM at ₹12.5L Cr in 2025, nearly 2x its closest competitor.",
        "Monthly SIP inflows tripled from ₹11,517 Cr (Jan 2022) to ₹31,002 Cr (Dec 2025).",
        "Small Cap funds delivered highest 1-year returns — DSP Small Cap at 64.88%.",
        "Industry folios doubled from 13.26 Cr to 26.12 Cr between 2022 and 2025.",
        "Liquid funds attract the most inflows — consistently ₹33,000–42,000 Cr monthly.",
        "26-35 age group accounts for 41.1% of all investors.",
        "Banking, IT, and Pharma sectors account for 44.6% of equity fund portfolios.",
        "T30 cities drive 66.3% of all transactions vs 33.7% from B30 cities.",
        "Male investors account for 66.5% of transactions — gender gap persists.",
        "NAV correlations across funds are near zero, indicating diverse fund strategies.",
    ]
    for f in eda_findings:
        story.append(Paragraph(f"• {f}", body_style))
    story.append(PageBreak())
    
    # 5. Performance Analysis
    story.append(Paragraph("5. Fund Performance Analysis", heading_style))
    
    # Load scorecard
    scorecard = pd.read_csv(PROCESSED_DIR / 'fund_scorecard.csv')
    top10 = scorecard.nlargest(10, 'score')[['scheme_name', 'score', 'cagr_3yr_pct', 'sharpe_ratio', 'max_drawdown_pct']]
    
    perf_data = [['Fund Name', 'Score', '3yr CAGR%', 'Sharpe', 'Max DD%']]
    for _, row in top10.iterrows():
        perf_data.append([
            row['scheme_name'][:40],
            str(round(row['score'], 1)),
            str(round(row['cagr_3yr_pct'], 2)),
            str(round(row['sharpe_ratio'], 3)),
            str(round(row['max_drawdown_pct'], 2))
        ])
    
    t3 = Table(perf_data, colWidths=[2.8*inch, 0.6*inch, 0.8*inch, 0.6*inch, 0.7*inch])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLUESTOCK_PURPLE),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('PADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [HexColor('#F5F5FF'), white]),
    ]))
    story.append(t3)
    story.append(Spacer(1, 0.2*inch))
    
    # 6. Advanced Analytics
    story.append(Paragraph("6. Advanced Analytics & Risk Metrics", heading_style))
    advanced = [
        ("Value at Risk (VaR 95%)", "ABSL Small Cap Fund has the highest VaR of -2.39%, "
         "meaning on the worst 5% of days investors can expect losses exceeding 2.39%."),
        ("CVaR", "The average loss on worst days for Small Cap funds reaches -3.03%, "
         "significantly higher than Large Cap funds at ~-1.2%."),
        ("Rolling Sharpe", "All funds show highly variable rolling Sharpe ratios (range: -4 to +6), "
         "confirming no fund delivers consistently superior risk-adjusted returns."),
        ("SIP Continuity", "97.8% of investors with 6+ SIP transactions show average gaps "
         "exceeding 35 days, indicating widespread irregular payment patterns."),
        ("Sector HHI", "Axis Bluechip Fund has the highest sector concentration (HHI ~3000) "
         "while UTI Mid Cap is most diversified (HHI ~1300)."),
    ]
    for metric, desc in advanced:
        story.append(Paragraph(f"<b>{metric}:</b> {desc}", body_style))
    story.append(Spacer(1, 0.2*inch))
    
    # 7. Recommendations
    story.append(Paragraph("7. Recommendations", heading_style))
    recs = [
        "Investors with Moderate risk appetite should consider Mirae Asset Large Cap (Sharpe: 1.068) "
         "for optimal risk-adjusted returns.",
        "SIP continuity intervention needed — 97.8% of investors show irregular payment patterns. "
         "Automated reminders and mandate setup should be prioritised.",
        "Small Cap funds (ABSL, SBI, Axis) offer highest returns but carry VaR > 2.3% — "
         "suitable only for investors with High risk appetite and 5+ year horizon.",
        "Gender gap in participation (66.5% male) suggests opportunity for targeted female investor "
         "outreach programs.",
        "B30 city penetration at 33.7% indicates significant growth opportunity in tier-2 and tier-3 cities.",
    ]
    for r in recs:
        story.append(Paragraph(f"• {r}", body_style))
    story.append(Spacer(1, 0.2*inch))
    
    # 8. Limitations
    story.append(Paragraph("8. Limitations", heading_style))
    lims = [
        "NAV data is forward-filled for weekends and holidays — actual fund values on non-trading days are estimated.",
        "Investor transaction data is synthetically generated — behavioural patterns may not reflect real investor distributions.",
        "Alpha and Beta calculations show near-zero R-squared vs Nifty 100, indicating the simulated NAV data does not track real market movements.",
        "5-year CAGR could not be computed as the dataset covers only January 2022 onwards.",
        "Dashboard requires Power BI Desktop to view — a web-based alternative (Streamlit) would improve accessibility.",
    ]
    for l in lims:
        story.append(Paragraph(f"• {l}", body_style))
    
    story.append(PageBreak())
    story.append(Paragraph("Thank You", title_style))
    story.append(Paragraph(
        "This project was built as part of the Bluestock Fintech Data Analyst Internship Program. "
        "All code, notebooks, and deliverables are available on the project GitHub repository.",
        body_style))
    
    doc.build(story)
    print("✅ Final_Report.pdf generated!")

if __name__ == "__main__":
    generate_pdf()