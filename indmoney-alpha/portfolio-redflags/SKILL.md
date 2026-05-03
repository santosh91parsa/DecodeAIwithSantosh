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
  get_indian_stocks_details (analyst segment), get_indian_stocks_ohlc (1week, 1y, flagged only).
---

# Portfolio Red Flags — Fast Sell Scan (Stocks + Mutual Funds)

## Speed Rules — Minimum Round Trips

**Round 1 (one ToolSearch call):**
Load all tools at once:
`ToolSearch query="select:mcp__indmoney__networth_holdings,mcp__indmoney__get_indian_stocks_details,mcp__indmoney__get_indian_stocks_ohlc" max_results=3`

**Round 2 (parallel — fire together in one message):**
- `networth_holdings` asset_type "IND_STOCK"
- `networth_holdings` asset_type "MF"

**Round 3 (parallel — fire together in one message):**
- `get_indian_stocks_details` batch 1: first 10 ind_keys, segments ["analyst"]
- `get_indian_stocks_details` batch 2: remaining ind_keys, segments ["analyst"]
- Use investment_code from holdings directly as ind_key — skip lookup_ind_keys

**Round 4 (parallel, ONLY if needed):**
- `get_indian_stocks_ohlc` interval "1week" lookback "1y" — ONLY for stocks where pnl_per < −10% OR day_change < −3%
- **Skip entirely if no stock meets this threshold**

Total: 4 rounds max, 3 rounds if no deep losers. Never add extra rounds.

---

## Calculations (mental math — no extra tool calls)

```
diff   = 52W_high − 52W_low
fib_78 = 52W_high − diff × 0.786   ← SELL NOW if current < this
fib_61 = 52W_high − diff × 0.618   ← REVIEW if fib_61 > current > fib_78
fib_38 = 52W_high − diff × 0.382   ← healthy pullback
ATR    = diff ÷ 52                  ← weekly ATR approximation
trail  = 52W_high − ATR × 2        ← flag if current < trail AND pnl > 20%
R:R    = (analyst_mean − current) ÷ (current − fib_78)
```

---

## Red Flag Rules

**SELL NOW (any one triggers):**
- current < fib_78
- analyst sell% > 60% OR current > analyst HIGH target
- pnl_per < −30% AND analyst upside < 5%
- day_change < −5%

**TRIM (profit at risk):**
- current > analyst MEAN target (upside exhausted)
- pnl_per > 50% AND current within 5% of 52W high

**REVIEW (any one triggers):**
- fib_61 < current < fib_78
- analyst buy% < 40%
- R:R < 2:1 on a losing position
- Stock in loss AND within 10% of 52W low

**TRAIL STOP (winners):**
- pnl_per > 20% AND current < trail level
- Stop = fib_38 for moderate winners, fib_61 for winners > 50%

**MF flags (from holdings data only, no extra calls):**
- XIRR negative → SELL NOW
- Gold MF > 15% of total MF → TRIM
- More than 2 funds same sub-category → Consolidate weakest
- Active large cap ER > 1.5% → Switch to index

---

## Output (compact — tables only, no paragraphs)

```
## Portfolio Red Flags — [Date]
Stocks: X | MFs: Y | ₹Total

### SELL NOW
| Holding | P&L | Flag | Action |
|---------|-----|------|--------|

### TRIM
| Holding | P&L | Why | Action |

### REVIEW
| Holding | P&L | Flag | Stop |

### TRAIL STOP
| Holding | P&L | Stop ₹ |

### HEALTHY
[one comma-separated line]

### MF
- [flag]: [fund] — [one-line action]

Score: X/10 | Free capital: ₹X | Redeploy → [category]
```

One sentence per SELL NOW on bull/bear case. No multi-paragraph analysis.
