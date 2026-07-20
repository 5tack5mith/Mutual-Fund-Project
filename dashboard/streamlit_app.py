"""
Streamlit Dashboard — Bluestock Mutual Fund Analytics
Interactive web app alternative to Power BI
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Bluestock MF Analytics",
    page_icon="📈",
    layout="wide"
)

# Paths
BASE_DIR = Path(__file__).parent.parent
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'

# Load data
@st.cache_data
def load_data():
    funds = pd.read_csv(PROCESSED_DIR / '01_fund_master_clean.csv')
    nav = pd.read_csv(PROCESSED_DIR / '02_nav_history_clean.csv', parse_dates=['date'])
    aum = pd.read_csv(PROCESSED_DIR / '03_aum_by_fund_house_clean.csv', parse_dates=['date'])
    sip = pd.read_csv(PROCESSED_DIR / '04_monthly_sip_inflows_clean.csv', parse_dates=['month'])
    transactions = pd.read_csv(PROCESSED_DIR / '08_investor_transactions_clean.csv', parse_dates=['transaction_date'])
    scorecard = pd.read_csv(PROCESSED_DIR / 'fund_scorecard.csv')
    return funds, nav, aum, sip, transactions, scorecard

funds, nav, aum, sip, transactions, scorecard = load_data()

# Header
st.markdown("# 📈 Bluestock Mutual Fund Analytics Platform")
st.markdown("*End-to-End Mutual Fund Analytics | Bluestock Fintech Internship*")
st.divider()

# Sidebar navigation
page = st.sidebar.selectbox("Navigate to", [
    "🏠 Industry Overview",
    "📊 Fund Performance",
    "👥 Investor Analytics",
    "📈 SIP & Market Trends"
])

# ============================================
# PAGE 1 — Industry Overview
# ============================================
if page == "🏠 Industry Overview":
    st.header("Industry Overview")
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        latest_aum = aum.groupby('fund_house')['aum_lakh_crore'].last().sum()
        st.metric("Total AUM", f"₹{latest_aum:.1f}L Cr")
    with col2:
        latest_sip = sip['sip_inflow_crore'].iloc[-1]
        st.metric("Latest SIP Inflow", f"₹{latest_sip:,.0f} Cr")
    with col3:
        st.metric("Fund Schemes", "40")
    with col4:
        st.metric("Total Investors", f"{transactions['investor_id'].nunique():,}")
    
    st.divider()
    
    # AUM trend
    st.subheader("AUM Growth by Fund House")
    fig = px.line(aum, x='date', y='aum_lakh_crore', color='fund_house',
                  title='AUM Trend 2022–2025')
    st.plotly_chart(fig, use_container_width=True)
    
    # AUM bar chart
    st.subheader("Latest AUM by Fund House")
    latest_aum_df = aum.groupby('fund_house')['aum_lakh_crore'].last().reset_index().sort_values('aum_lakh_crore', ascending=True)
    fig2 = px.bar(latest_aum_df, x='aum_lakh_crore', y='fund_house', orientation='h',
                  title='AUM by AMC (Latest)', color='aum_lakh_crore', color_continuous_scale='Blues')
    st.plotly_chart(fig2, use_container_width=True)

# ============================================
# PAGE 2 — Fund Performance
# ============================================
elif page == "📊 Fund Performance":
    st.header("Fund Performance")
    
    # Slicers
    col1, col2 = st.columns(2)
    with col1:
        selected_category = st.multiselect("Filter by Category", 
            options=scorecard['category'].unique(),
            default=scorecard['category'].unique())
    with col2:
        selected_house = st.multiselect("Filter by Fund House",
            options=funds['fund_house'].unique(),
            default=funds['fund_house'].unique())
    
    # Filter data
    filtered = scorecard[scorecard['category'].isin(selected_category)]
    filtered = filtered.merge(funds[['amfi_code', 'fund_house']], on='amfi_code')
    filtered = filtered[filtered['fund_house'].isin(selected_house)]
    
    # Scatter plot
    st.subheader("Return vs Risk (Bubble size = Score)")
    fig3 = px.scatter(filtered, x='cagr_3yr_pct', y='sharpe_ratio',
                      size='score', color='category', hover_name='scheme_name',
                      title='3yr CAGR vs Sharpe Ratio')
    st.plotly_chart(fig3, use_container_width=True)
    
    # Scorecard table
    st.subheader("Fund Scorecard")
    st.dataframe(
        filtered[['scheme_name', 'score', 'cagr_3yr_pct', 'sharpe_ratio', 'max_drawdown_pct']]
        .sort_values('score', ascending=False)
        .reset_index(drop=True),
        use_container_width=True
    )

# ============================================
# PAGE 3 — Investor Analytics
# ============================================
elif page == "👥 Investor Analytics":
    st.header("Investor Analytics")
    
    # Slicers
    col1, col2 = st.columns(2)
    with col1:
        selected_state = st.multiselect("Filter by State",
            options=transactions['state'].unique(),
            default=transactions['state'].unique())
    with col2:
        selected_type = st.multiselect("Filter by Transaction Type",
            options=transactions['transaction_type'].unique(),
            default=transactions['transaction_type'].unique())
    
    filtered_txn = transactions[
        transactions['state'].isin(selected_state) &
        transactions['transaction_type'].isin(selected_type)
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Transaction by state
        state_data = filtered_txn.groupby('state')['amount_inr'].sum().reset_index().sort_values('amount_inr')
        fig4 = px.bar(state_data, x='amount_inr', y='state', orientation='h',
                      title='Transaction Amount by State')
        st.plotly_chart(fig4, use_container_width=True)
    
    with col2:
        # Transaction type donut
        type_data = filtered_txn['transaction_type'].value_counts().reset_index()
        fig5 = px.pie(type_data, values='count', names='transaction_type',
                      hole=0.4, title='SIP vs Lumpsum vs Redemption')
        st.plotly_chart(fig5, use_container_width=True)
    
    # Age group
    age_data = filtered_txn.groupby('age_group')['amount_inr'].mean().reset_index()
    fig6 = px.bar(age_data, x='age_group', y='amount_inr',
                  title='Average Transaction Amount by Age Group')
    st.plotly_chart(fig6, use_container_width=True)

# ============================================
# PAGE 4 — SIP & Market Trends
# ============================================
elif page == "📈 SIP & Market Trends":
    st.header("SIP & Market Trends")
    
    # SIP trend
    fig7 = px.line(sip, x='month', y='sip_inflow_crore',
                   title='Monthly SIP Inflows 2022–2025', markers=True)
    fig7.add_hline(y=31002, line_dash='dash', line_color='green',
                   annotation_text='All-time high ₹31,002 Cr')
    st.plotly_chart(fig7, use_container_width=True)
    
    # Fund recommender
    st.subheader("🎯 Fund Recommender")
    risk = st.selectbox("Select your risk appetite", ["Low", "Moderate", "High"])
    
    risk_map = {
        'Low': ['Low', 'Moderately Low'],
        'Moderate': ['Moderate', 'Moderately High'],
        'High': ['High', 'Very High']
    }
    
    eligible = funds[funds['risk_category'].isin(risk_map[risk])]
    recommendations = eligible.merge(
        scorecard[['amfi_code', 'sharpe_ratio', 'cagr_3yr_pct', 'score']], 
        on='amfi_code'
    ).nlargest(3, 'sharpe_ratio')[['scheme_name', 'fund_house', 'risk_category', 'sharpe_ratio', 'cagr_3yr_pct']]
    
    st.dataframe(recommendations.reset_index(drop=True), use_container_width=True)