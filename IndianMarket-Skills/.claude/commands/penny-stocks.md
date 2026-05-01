# Penny Stocks — High-Potential Low-Price Investment Picks

Find fundamentally sound penny stocks (under ₹100) with real upside potential — not just speculation.

## What This Skill Does
- Identifies penny stocks with genuine business fundamentals, not just hype
- Filters for analyst coverage (minimum 1 analyst), positive revenue trend, sector tailwinds
- Separates "high risk / high reward" from "pure speculation / avoid"
- Gives a clear verdict: BUY (investment grade), SPECULATIVE (small position only), AVOID

## Definition Used
- Penny stock = priced under ₹100
- Quality penny stock = has analyst coverage + positive business fundamentals + sector tailwind

## Execution Steps

### Step 1 — Resolve candidates
Use `lookup_ind_keys` for this curated list of known penny-range stocks with real businesses:
- Suzlon Energy, HUDCO, IRFC, Yes Bank, Vodafone Idea, Bank of Maharashtra, Trident, SAIL, National Fertilizers, REC Limited, PFC, NALCO, Hind Copper

### Step 2 — Fetch live details + analyst data
Use `get_indian_stocks_details` with `segments: ["analyst", "news"]` for all resolved keys.

### Step 3 — Classify each stock

**BUY (Investment Grade):** 
- Price < ₹100
- Analyst buy% > 60%
- Upside to analyst mean > 15%
- Has real business with revenue/profit

**SPECULATIVE (Small Bet Only):**
- Price < ₹100
- Analyst buy% 30–60% OR limited coverage
- Upside exists but risks are high (debt, sector disruption, regulatory)
- Max allocation: 2–3% of portfolio

**AVOID:**
- Analyst sell% dominant (>50%)
- Analyst target BELOW current price
- Fundamental business problems (losses mounting, debt spiral)

### Step 4 — Output

```
## Penny Stocks Verdict — [Today's Date]

### BUY (Investment Grade)
[List with: Price | 52W range | Analyst target | Upside | Why buy]

### SPECULATIVE (Small Bet — Max 2% of portfolio)
[List with: Price | Upside | Risk factor | What could go right]

### AVOID
[List with: Price | Why avoid | What would change this view]
```

End with: "Penny stocks carry higher risk. Never put more than 5% of total portfolio in any single penny stock."
