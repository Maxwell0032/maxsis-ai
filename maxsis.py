import pandas as pd
import numpy as np

# Load the sample financial data
df = pd.read_csv("sample_financials.csv")

# Create a burn rate column
df["burn_rate"] = df["expenses"] - df["revenue"]

# Average burn rate
avg_burn = df["burn_rate"].mean()

# Current cash from latest month
current_cash = df["cash"].iloc[-1]

# Runway in months
if avg_burn > 0:
    runway_months = current_cash / avg_burn
else:
    runway_months = 999

# Anomaly score for latest burn rate
std_burn = df["burn_rate"].std()
if std_burn == 0 or np.isnan(std_burn):
    z_score = 0
else:
    z_score = (df["burn_rate"].iloc[-1] - df["burn_rate"].mean()) / std_burn

# Simple concentration risk proxy:
# how much of total revenue comes from the latest month
total_revenue = df["revenue"].sum()
latest_revenue = df["revenue"].iloc[-1]

if total_revenue > 0:
    revenue_concentration = latest_revenue / total_revenue
else:
    revenue_concentration = 0

# Risk classification
risk_level = "LOW"

if runway_months < 6:
    risk_level = "HIGH"
elif runway_months < 12:
    risk_level = "MEDIUM"

# Build narrative summary
summary = f"""
MAXSIS AI — Financial Risk Summary

Estimated liquidity runway: {round(runway_months, 2)} months
Latest burn anomaly z-score: {round(z_score, 2)}
Revenue concentration proxy: {round(revenue_concentration, 2)}
Risk classification: {risk_level}

Narrative assessment:
The organization shows an estimated liquidity runway of {round(runway_months, 2)} months.
The most recent burn-rate anomaly score is {round(z_score, 2)}, which helps identify unusual
expense pressure relative to recent operating history. Revenue concentration is estimated at
{round(revenue_concentration, 2)}, signaling whether funding sources may be overly dependent
on near-term inflows. Overall risk is classified as {risk_level} based on current cash and burn trends.

Recommended next step:
Review expense concentration, monitor cash drawdown weekly, and prepare a liquidity stabilization
plan if runway remains below 6 months.
"""

print(summary)