---
name: portfolio-redflags
description: |
  Full portfolio scan for urgent sell signals across all Indian stocks and mutual funds using
  INDmoney live data. Detects Fibonacci breakdowns (78.6% retracement breach), trailing stop
  hits on profitable positions, analyst reversals, volume-confirmed crashes, and MF category
  trend failures. Returns prioritized SELL NOW / REVIEW / HOLD verdicts with R:R for staying.

  Use when the user asks: "portfolio red flags", "what should I sell", "portfolio health check",
  "which stocks to exit", "portfolio analysis", "sell recommendations", "what's wrong with my
  portfolio", "identify bad stocks", "portfolio review", "stocks and funds to sell",
  "check my portfolio for problems", or any request to audit holdings for exit candidates.

  Requires INDmoney MCP server connected. Uses: networth_holdings (IND_STOCK and MF),
  lookup_ind_keys, get_indian_stocks_details (analyst segment), get_indian_stocks_ohlc
  (1week interval, 1y lookback for flagged positions).
---

# Portfolio Red Flags — Quick Sell Scan (Stocks + Mutual Funds)

Full portfolio scan using technical analysis, multi-timeframe trend, Fibonacci breakdown levels, RSI signals, and trailing stop triggers — not just P&L numbers.

## Execution Steps

### Step 1 — Fetch portfolio holdings
Use `networth_holdings` for IND_STOCK and MF asset types.

### Step 2 — Fetch live stock data
Use `lookup_ind_keys` to resolve all stock holdings.
Use `get_indian_stocks_details` with `segments: ["analyst"]` for all holdings (batch of 10 max).
Use `get_indian_stocks_ohlc` with `interval: "1week", lookback: "1y"` for any stock with:
  - P&L loss > 10%, OR
  - day_change < -3%, OR
  - Currently in loss AND analyst upside < 10%

### Step 3 — Technical Red Flags for STOCKS

**SELL NOW — Exit this week if ANY of these:**

1. **Trend broken:** Stock making lower lows on weekly chart for 3+ consecutive weeks
2. **Fibonacci breakdown:** Price below 78.6% retracement from 52W high → trend likely over
   ```
   fib_78 = 52W_high - (52W_high - 52W_low) × 0.786
   Flag if: current_price < fib_78
   ```
3. **Analyst reversal:** Analyst sell% > 60% OR current price > analyst high target (no upside left)
4. **Death cross proxy:** Stock more than 25% below 52W high AND 52W low within 5% → near breakdown
5. **Today crash:** day_change_percentage < -5%
6. **Deep loss + no thesis:** P&L loss > 30% AND analyst upside < 5%

**REVIEW — Decide within 2 weeks if ANY of these:**

7. **Fibonacci warning zone:** Price between 61.8%–78.6% retracement — last strong support
   ```
   fib_61 = 52W_high - (52W_high - 52W_low) × 0.618
   Flag if: fib_61 > current_price > fib_78
   ```
8. **RSI signal:** Stock in loss AND trading near 52W low (within 10%) — momentum near exhaustion
9. **Analyst conviction drop:** Buy% fell below 40% (weak consensus)
10. **Trailing stop hit:** If entry was profitable, check if price has dropped > ATR×2 from recent high
    ```
    ATR approx = avg(weekly high - weekly low) last 8 weeks
    Trail check = 52W_high - ATR × 2.0
    Flag if current_price < trail_check AND position was profitable
    ```
11. **Concentration risk:** Single stock > 15% of total portfolio
12. **Momentum fading:** Stock flat/sideways for 3+ months with no catalyst visible

### Step 4 — Probabilistic Scenario for flagged stocks
For each SELL NOW or REVIEW stock, state:
```
Bull case (X% probability): [what would make it recover]
Bear case (Y% probability): [what would push it lower]
Base case: [most likely path]
```
Only maintain position if bull case probability > 40% AND has a clear catalyst.

### Step 5 — Red Flags for MUTUAL FUNDS

**SELL NOW:**
- XIRR negative over 2+ years
- Debt fund with credit event (NAV dropped >1% in a day)
- Category overlap >70% with another fund (pure duplication)
- Sectoral fund where the sector's weekly trend is broken (lower lows for 3+ months)

**REVIEW:**
- XIRR underperforming category average by >3% over 1 year
- Large cap active fund with >1.5% expense ratio
- Fund with shrinking AUM (institutional redemptions signal)
- More than 2 funds in same sub-category (e.g., 3 flexi cap funds)
- Thematic fund where the theme's momentum has reversed

**HOLD:**
- Performing within 2% of benchmark
- Serving a specific uncovered category in portfolio

### Step 6 — R:R Check for Marginal Cases
For stocks in the REVIEW zone:
```
Risk = current_price - stop_level (recent 52W low or Fib 78.6%)
Reward = analyst mean target - current_price
R:R = reward ÷ risk
```
- R:R ≥ 2:1 → HOLD and set a hard stop
- R:R < 2:1 → EXIT — risk not justified by remaining upside

### Step 7 — Output

```
## Portfolio Red Flag Report — [Date]

### SELL NOW (Act this week)
| Holding | Type | P&L | Technical Flag | R:R | Action |

### REVIEW (Decide within 2 weeks)
| Holding | Type | P&L | Concern | Bull Case % | Stop Level |

### SET TRAILING STOP (Protect profits)
| Holding | Type | P&L | Trail Stop Level | Method |

### HEALTHY (No action needed)
[Brief list]

### Portfolio Health Score: X/10
[Breakdown: trend alignment, diversification, concentration, MF quality]

### Capital freed if SELL NOW executed: ₹X
Suggested reallocation: [category]
```
