# Quick Trade — Near-Term Profit Opportunities

Find Indian stocks with strong setups for 1–4 week trades with clear entry, target, and stop-loss levels.

## What This Skill Does
- Scans high-momentum stocks across key sectors (defense, banking, FMCG, IT, energy, consumer tech)
- Uses technical analysis: 52W position, volume, breakout/retest patterns
- Uses fundamental filters: analyst consensus, upside %, near-term catalysts
- Filters OUT stocks where analyst mean target < current price (no room to run)
- Returns top 3 picks with trade setup: entry zone, quick target (5–15%), stop loss, timeframe

## Execution Steps

### Step 1 — Resolve candidate tickers
Use `lookup_ind_keys` to resolve a curated list of high-momentum candidates:
- Eternal (Zomato), HDFC Bank, BEL, Bajaj Finance, Tata Motors, IRCTC, Dixon Technologies, Persistent Systems, Mankind Pharma, Coforge

### Step 2 — Fetch live details + analyst data
Use `get_indian_stocks_details` with `segments: ["analyst"]` for all resolved keys in one call.

Filter out any stock where:
- `analyst upside_per < 5%`  (already near or above analyst target)
- `buy_per < 50%` (weak conviction)

### Step 3 — Fetch OHLC for top 5 filtered candidates
Use `get_indian_stocks_ohlc` with `interval: "1week"`, `lookback: "1y"` for technical setup.

Identify for each:
- Current price vs 52W high/low position
- Pattern: breakout, retest, recovery from correction, consolidation breakout
- Volume trend (expanding = bullish)

### Step 4 — Score and rank

Score each stock 1–10 on:
| Factor | Weight |
|---|---|
| Analyst upside % | 30% |
| Buy % consensus | 20% |
| Technical pattern quality | 30% |
| Near-term catalyst (results, order win, policy) | 20% |

Pick top 3.

### Step 5 — Output trade cards

For each pick, output:

```
## [Stock Name] — [Sector]
**Current price:** ₹X  |  **52W:** ₹low – ₹high

| | |
|---|---|
| Entry zone | ₹X – ₹Y |
| Quick target | ₹Z (+N%) |
| Stop loss | ₹W |
| Timeframe | N weeks |
| Analyst target | ₹T (N% upside, X% BUY) |
| Catalyst | [what could move it] |

**Setup:** [2 lines on why this is a good trade right now]
```

End with a 1-line risk note: "These are short-term trades, not investments. Always use stop-loss."
