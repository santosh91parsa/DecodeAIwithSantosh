# Quick Trade — Near-Term Profit Opportunities

Find Indian stocks with high-confluence setups for 1–4 week trades. Uses multi-timeframe analysis, Fibonacci entries, RSI divergence, ATR-based stops, and R:R validation before recommending any trade.

## Candidate Universe
Scan these high-momentum stocks across key sectors:
Eternal (Zomato), HDFC Bank, BEL, Bajaj Finance, Tata Motors, IRCTC, Dixon Technologies, Persistent Systems, Mankind Pharma, Coforge, Adani Power, SBI, Vishal Mega Mart, Tata Steel, Sai Life Sciences

## Execution Steps

### Step 1 — Resolve and fetch live data
Use `lookup_ind_keys` for all candidates.
Use `get_indian_stocks_details` with `segments: ["analyst"]` for all in one call.

**Pre-filter — drop any stock where:**
- Analyst upside < 8% (already near target)
- Buy% < 50% (weak consensus)
- Stock is above analyst mean target (no room)

### Step 2 — Multi-Timeframe Analysis (3-Screen Method)
Use `get_indian_stocks_ohlc` with `interval: "1week", lookback: "1y"` (Screen 1 — trend bias)
Use `get_indian_stocks_ohlc` with `interval: "1day", lookback: "14d"` (Screen 2 — setup)

**Screen 1 — Weekly Bias:**
- Higher highs & higher lows = bullish bias → only look for longs
- Price above 20W MA (approximate from OHLC) = trend intact
- RSI proxy: if last 4 weeks are net positive → bullish

**Screen 2 — Daily Setup:**
- Is price pulling back into a support zone? (Healthy retracement in an uptrend)
- Is volume declining on the pullback? (Healthy — sellers losing conviction)
- Pattern: flag, ascending base, double bottom, inside bar at support

Only take trades where Screen 1 (weekly) and Screen 2 (daily) align.

### Step 3 — Confluence Scoring
Score each stock (max 6 points). Only proceed with score ≥ 4.

| Factor | +1 Point |
|---|---|
| Weekly trend is bullish (higher highs/lows) | +1 |
| Daily setup pattern is valid (pullback to support, flag, base) | +1 |
| RSI not overbought on daily (<65) | +1 |
| Volume declining on pullback (healthy retracement) | +1 |
| Analyst upside > 15% with strong BUY consensus | +1 |
| Near-term catalyst exists (results due, sector tailwind, news) | +1 |

| Score | Action |
|---|---|
| 5-6 | Strong — full position |
| 4 | Good — proceed |
| 3 | Marginal — skip or paper trade |
| ≤2 | No setup — skip |

### Step 4 — Fibonacci Entry Zones
From the weekly OHLC data, identify the most recent swing high and swing low (at least 5% move).

Calculate retracement levels for each qualifying stock:
```
diff = swing_high - swing_low
fib_23 = swing_high - diff × 0.236   ← shallow pullback, aggressive entry
fib_38 = swing_high - diff × 0.382   ← healthy pullback, standard entry
fib_50 = swing_high - diff × 0.500   ← deep pullback, cautious entry
fib_61 = swing_high - diff × 0.618   ← golden ratio, last strong support
```

**Entry zone:** Between Fib 38.2% and 61.8% is the ideal entry band.
**Avoid entry:** If current price is below 78.6% retracement — trend may be broken.

### Step 5 — RSI Divergence Check
From daily OHLC data, check the last 3 swing lows:
- **Bullish regular divergence:** Price making lower lows but momentum recovering → BUY signal ↑
- **Bullish hidden divergence:** Price making higher lows on pullback → trend continuation confirmed ↑
- **Bearish divergence found:** Skip this stock — momentum is fading

### Step 6 — ATR-Based Stop Loss
Estimate ATR(14) from daily candles:
```
ATR approx = average of (high - low) over last 14 days
Stop (long) = entry_price - ATR × 2.0
Buffer for mid/small caps: ATR × 2.5
```

Stop must be at a technically meaningful level (below swing low or key support). If the calculated ATR stop cuts through the middle of a support zone, widen to the support boundary.

### Step 7 — R:R Validation
Only recommend trades with R:R ≥ 2:1.

```
Risk = entry_price - stop_loss
Quick target = nearest resistance OR Fib extension 127.2%
Full target = analyst mean target OR Fib extension 161.8%

R:R = (target - entry) ÷ (entry - stop)
```

| R:R | Decision |
|---|---|
| < 1.5:1 | Skip — not worth the risk |
| 1.5–2:1 | Acceptable only if confluence score = 6 |
| 2:1–3:1 | Good — take the trade |
| 3:1+ | Excellent — full position size |

### Step 8 — Position Sizing
For a standard portfolio, size each quick trade at 1-2% portfolio risk per trade:
```
Risk per trade = portfolio_value × 0.015  (1.5% risk)
Shares = risk_per_trade ÷ (entry - stop)
Capital = shares × entry_price
Max capital per trade = 15% of portfolio (hard limit)
```

### Step 9 — Trailing Stop Plan
Include a trailing stop plan with each trade card:
- **At breakeven (1R gained):** Move stop to entry price — trade now risk-free
- **At 2R gained:** Trail stop to Highest close - ATR × 1.5 (ATR trail)
- **At 3R gained:** Trail to most recent swing low (structure trail)

### Step 10 — Output Top 3 Picks

```
## [Stock] — [Sector] | Confluence: X/6

**Current:** ₹X | 52W: ₹low–₹high | Today: ±X%

| Setup | |
|---|---|
| Weekly bias | Bullish / Bearish |
| Daily pattern | [flag / base / pullback] |
| RSI divergence | [Bullish / None / Warning] |
| Fib entry zone | ₹X (38.2%) – ₹Y (61.8%) |
| Entry | ₹X |
| Stop loss | ₹Y (ATR×2.0, -X%) |
| Quick target | ₹Z (+X%, Fib 127.2%) |
| Full target | ₹W (+X%, analyst mean) |
| R:R ratio | X:1 |
| Position size | ~X shares (1.5% portfolio risk) |

**Trailing plan:** Breakeven at ₹X → ATR trail at ₹Y → Structure trail at ₹Z

**Catalyst:** [what could move it near-term]
**Invalidation:** Close below ₹X (stop level) — exit immediately
```

End with: "These are short-term trades. Use stop-losses. Never risk more than 2% of capital per trade."
