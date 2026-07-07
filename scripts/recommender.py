import pandas as pd

# Load data
funds = pd.read_csv('../data/processed/01_fund_master_clean.csv')
scorecard = pd.read_csv('../data/processed/fund_scorecard.csv')

def recommend_funds(risk_appetite):
    """
    Input: risk_appetite — Low, Moderate, or High
    Output: Top 3 funds by Sharpe ratio within matching risk grade
    """
    risk_map = {
        "Low": ["Low", "Moderately Low"],
        "Moderate": ["Moderate", "Moderately High"],
        "High": ["High", "Very High"]
    }

    valid_grades = risk_map.get(risk_appetite, [])
    eligible_funds = funds[funds["risk_category"].isin(valid_grades)]
    eligible_with_score = eligible_funds.merge(
        scorecard[["amfi_code", "sharpe_ratio", "cagr_3yr_pct", "score"]], 
        on="amfi_code"
    )
    top3 = eligible_with_score.nlargest(3, "sharpe_ratio")[
        ["scheme_name", "fund_house", "risk_category", "sharpe_ratio", "cagr_3yr_pct", "score"]
    ].reset_index(drop=True)

    print(f"Top 3 funds for {risk_appetite} risk appetite:")
    print(top3.to_string())
    return top3

if __name__ == "__main__":
    for risk in ["Low", "Moderate", "High"]:
        recommend_funds(risk)
        print()
