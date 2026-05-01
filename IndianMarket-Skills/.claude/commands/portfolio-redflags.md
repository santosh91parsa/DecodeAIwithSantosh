# Portfolio Red Flags — Quick Sell Scan (Stocks + Mutual Funds)

Scan the full portfolio for stocks and mutual funds that should be exited quickly. Surface red flags clearly with urgency levels.

## What This Skill Does
- Fetches full portfolio: stocks + mutual funds via networth holdings
- Checks each position against: analyst sentiment, 52W trend, P&L, concentration risk
- For MFs: checks category, overlap, underperformance vs peers, expense ratio concerns
- Returns a prioritized sell list with urgency: SELL NOW / REVIEW / HOLD

## Execution Steps

### Step 1 — Fetch portfolio holdings
Use `networth_holdings` to get all current positions including:
- Indian stocks (units, avg cost, current value, P&L, XIRR)
- Mutual funds (units, NAV, invested, current, XIRR)

### Step 2 — Fetch details for all stock holdings
Use `lookup_ind_keys` to resolve stock names from holdings.
Use `get_indian_stocks_details` with `segments: ["analyst"]` for all holdings in one call.
Use `get_indian_stocks_ohlc` with `interval: "1week"`, `lookback: "1y"` for top 5 loss-making or sideways positions.

### Step 3 — Red flag criteria for STOCKS

Flag as **SELL NOW** if ANY of:
- Loss > 30% AND analyst target below current price (OR no analyst coverage)
- Analyst sell% > 60%
- Stock making 52W lows with no reversal signal
- Fundamental story broken (sector in structural decline)

Flag as **REVIEW** if ANY of:
- Loss 15–30% AND stock underperforming Nifty over 6 months
- Analyst upside < 5% (priced in, no more room)
- High concentration (>15% of portfolio in single stock)
- Analyst buy% dropped below 40%

### Step 4 — Red flag criteria for MUTUAL FUNDS

Flag as **SELL NOW** if ANY of:
- XIRR negative over 2+ years (consistently losing money)
- Category overlap >70% with another fund in portfolio (duplication)
- Debt fund with credit risk / downgrade exposure

Flag as **REVIEW** if ANY of:
- XIRR underperforming category benchmark by >3% over 1 year
- Large cap fund with >1.5% expense ratio (ETF would be cheaper)
- Sectoral/thematic fund where sector thesis has played out or reversed
- More than 4 funds in portfolio that overlap significantly

### Step 5 — Output

```
## Portfolio Red Flag Report — [Date]

### SELL NOW (Act within this week)
| Holding | Type | Your P&L | Red Flag | Suggested Action |
|---|---|---|---|---|

### REVIEW (Decide within 1 month)
| Holding | Type | Your P&L | Concern | What to watch |
|---|---|---|---|---|

### HEALTHY (No action needed)
[Brief list of clean positions]

### Portfolio Health Score: X/10
[2 lines on overall portfolio quality]
```

End with estimated capital freed if all SELL NOW positions are exited, and reinvestment suggestion category (e.g., "move to large-cap quality stocks or index fund").
