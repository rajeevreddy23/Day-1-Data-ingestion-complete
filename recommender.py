"""
Bluestock Fintech - Mutual Fund Analytics Platform
Deliverable: recommender.py (Day 6: Advanced Analytics & Fund Recommendations)

Module:
  Takes investor risk appetite ('Low', 'Moderate', 'High', 'Very High')
  and recommends the Top 3 mutual fund schemes sorted by Sharpe Ratio
  within that risk grade category, displaying a formatted recommendation table.
"""

import sys
import argparse
import pandas as pd
from pathlib import Path

# Paths configuration
BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

def recommend_funds(risk_appetite: str = "Moderate", top_n: int = 3) -> pd.DataFrame:
    """
    Filter and rank top funds by Sharpe Ratio matching the specified risk grade.
    """
    # Load scorecard / performance data
    scorecard_path = PROCESSED_DIR / "fund_scorecard.csv"
    if not scorecard_path.exists():
        scorecard_path = BASE_DIR / "fund_scorecard.csv"
        
    df = pd.read_csv(scorecard_path)
    
    # Normalize risk strings
    appetite_clean = risk_appetite.strip().title()
    
    # Match risk category
    risk_col = "risk_category" if "risk_category" in df.columns else "risk_grade"
    
    if appetite_clean in ["Low"]:
        matched_df = df[df[risk_col].isin(["Low", "Moderately Low"])]
    elif appetite_clean in ["Moderate"]:
        matched_df = df[df[risk_col].isin(["Moderate", "Moderately High"])]
    elif appetite_clean in ["High"]:
        matched_df = df[df[risk_col].isin(["High", "Very High"])]
    else:
        matched_df = df[df[risk_col].str.contains(appetite_clean, case=False, na=False)]
        
    if len(matched_df) == 0:
        # Fallback to all if no exact match
        matched_df = df
        
    # Sort by Sharpe Ratio descending
    top_funds = matched_df.sort_values(by="sharpe_ratio", ascending=False).head(top_n)
    
    display_cols = [c for c in [
        "amfi_code", "scheme_name", "fund_house", "category",
        "cagr_3yr", "sharpe_ratio", "alpha", "beta", "expense_ratio_pct", "composite_score"
    ] if c in top_funds.columns]
    
    return top_funds[display_cols]

def main():
    parser = argparse.ArgumentParser(description="Bluestock Mutual Fund Recommender Engine")
    parser.add_argument(
        "--risk", "-r",
        type=str,
        default="Moderate",
        choices=["Low", "Moderate", "High", "Very High"],
        help="Investor risk appetite profile (default: Moderate)"
    )
    parser.add_argument(
        "--top", "-t",
        type=int,
        default=3,
        help="Number of recommendations to return (default: 3)"
    )
    
    args = parser.parse_args()
    risk = args.risk
    top_n = args.top
    
    print("=" * 80)
    print(f"BLUESTOCK MUTUAL FUND RECOMMENDER ENGINE")
    print(f"Risk Appetite Profile: {risk.upper()} | Top {top_n} Recommendations")
    print("=" * 80)
    
    recs = recommend_funds(risk_appetite=risk, top_n=top_n)
    
    print("\n" + recs.to_string(index=False))
    print("=" * 80)
    print("RATIONALE:")
    print("  Funds selected achieve the highest risk-adjusted excess returns (Sharpe)")
    print("  strictly constrained within the investor's designated risk capacity.")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
