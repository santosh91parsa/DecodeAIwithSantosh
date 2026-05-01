# Penny Stocks — High-Potential Low-Price Investment Picks

Scan penny stocks (<₹100) using technical analysis, RSI divergence, multi-timeframe trend, position sizing constraints, and R:R validation — not just price and hope.

## Definition
- Penny stock = priced under ₹100
- Quality penny stock = real business + analyst coverage + positive weekly trend + acceptable R:R

## Candidate Universe
Suzlon Energy, HUDCO, IRFC, Yes Bank, Vodafone Idea, Bank of Maharashtra, Trident, SAIL, National Fertilizers, REC Limited, PFC, NALCO, Hind Copper

## Execution Steps

### Step 1 — Fetch live data
Use `lookup_ind_keys` to resolve all names.
Use `get_indian_stocks_details` with `segments: ["analyst", "news"]` for all resolved keys.
Use `get_indian_stocks_ohlc` with `interval: "1week", lookback: "1y"` for weekly trend.

### Step 2 — Multi-Timeframe Trend Check (3-Screen)

**Screen 1 — Weekly trend:**
- Is price making higher highs and higher lows over the last 6 months?
- Is price recovering from its 52W low (>20% above the low)?
- Bullish weekly = strong base for investment

**Screen 2 — Daily momentum:**
- Is the stock in a base-building phase or actively recovering?
- Volume increasing on up-weeks, decreasing on down-weeks?

Only stocks with bullish or recovering weekly trend qualify for BUY.

### Step 3 — RSI Divergence Check
From weekly OHLC data, check for:
- **Bullish regular divergence** (price lower low, RSI higher low) = strong BUY signal at bottom
- **Bullish hidden divergence** (price higher low on pullback) = trend continuation
- **No divergence / bearish divergence** = downgrade to SPECULATIVE or AVOID

### Step 4 — Fibonacci Position in Trend
Calculate from 52W high and 52W low:
```
diff = 52W_high - 52W_low
fib_38 = 52W_high - diff × 0.382
fib_61 = 52W_high - diff × 0.618
fib_78 = 52W_high - diff × 0.786
```

| Current Price Position | Interpretation |
|---|---|
| Above Fib 38.2% (recovering well) | Strong — BUY zone |
| Between Fib 38.2%–61.8% | Moderate — SPECULATIVE with tight stop |
| Below Fib 61.8% (deep correction) | Weak — SPECULATIVE only |
| Below Fib 78.6% (near 52W low) | Broken — AVOID unless strong divergence |

### Step 5 — Classify Each Stock

**BUY (Investment Grade):**
- Price < ₹100
- Analyst buy% > 60% with upside > 15%
- Weekly trend: bullish or recovering (>20% above 52W low)
- RSI: not overbought, no bearish divergence
- Above Fib 38.2% retracement level
- Real profitable business (not mounting losses)

**SPECULATIVE (Small Bet Only — max 2% of portfolio):**
- Price < ₹100
- Some analyst coverage but buy% 30–60% OR limited analysts
- Weekly trend recovering but below Fib 50%
- Business has upside thesis but execution risk
- High-risk, high-reward — position size accordingly

**AVOID:**
- Analyst sell% dominant or target below current price
- Weekly trend: lower lows with no recovery signal
- Below Fib 78.6% with bearish divergence
- Business in structural decline (debt spiral, sector disruption)

### Step 6 — ATR Stop for BUY picks
Estimate ATR from weekly candle range:
```
Weekly ATR ≈ average (high - low) over last 8 weeks
Stop = current_price - ATR × 2.0
```
For penny stocks add extra buffer: ATR × 2.5 (more volatile)

### Step 7 — R:R Validation
Penny stocks need minimum 3:1 R:R given higher risk:
```
Risk = entry - stop
Target = analyst mean target
R:R = (target - entry) ÷ (entry - stop)
```
If R:R < 2:1, downgrade from BUY to SPECULATIVE regardless of other signals.

### Step 8 — Position Sizing (Hard Limits)
| Category | Max position | Max risk per trade |
|---|---|---|
| BUY grade | 5% of portfolio | 1.5% |
| SPECULATIVE | 2% of portfolio | 1% |
| Total penny exposure | 10% of portfolio | — |

Never concentrate more than 10% of total portfolio across all penny stocks combined.

### Step 9 — Output

```
## Penny Stock Verdicts — [Date]

### BUY (Investment Grade)
| Stock | Price | 52W Range | Fib Position | RSI Signal | Analyst Target | R:R | Stop | Max Allocation |
|---|---|---|---|---|---|---|---|---|

### SPECULATIVE (Max 2% per position)
| Stock | Price | Upside | Risk | What could go right | What could go wrong |
|---|---|---|---|---|---|

### AVOID
| Stock | Price | Why | What would change this |
|---|---|---|---|
```

End with: "Penny stocks carry amplified risk. Max 10% total portfolio exposure. Always use a stop-loss — penny stocks can lose 30-50% fast if momentum turns."
