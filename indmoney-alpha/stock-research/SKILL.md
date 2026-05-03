---
name: stock-research
description: |
  Full pre-investment due diligence for any single Indian stock. Combines: Fibonacci technical
  analysis (52W range, fib levels, ATR trailing stop, R:R), INDmoney analyst consensus
  (buy%/sell%, mean target, upside), INDmoney curated news (scored [+]/[-]/[~]/[=]),
  web news deep scan (last 30 days — fraud, promoter selling, earnings, debt), and macro
  context (tariffs, RBI rate cycle, FII flows). Returns INVEST / SPECULATIVE / WAIT / AVOID
  verdict with entry price, stop loss (fib_78), targets, R:R, and position size.

  Use when the user asks about a specific stock: "should I buy [stock]", "research [stock]",
  "is [stock] good to invest", "check news on [stock]", "due diligence [stock]",
  "stock research [stock]", "analyse [stock]", "what do you think about [stock]",
  "is it safe to invest in [stock]", "any red flags for [stock]", "stock-research [stock]".

  Requires INDmoney MCP server connected. Uses: lookup_ind_keys, get_indian_stocks_details
  (analyst + news), get_indian_stocks_ohlc (1week, 1y). Also uses WebSearch (4 parallel
  searches: recent news, red flag scan, earnings check, analyst views). Total: 3 rounds always.
---

# Stock Research — Full Due Diligence Before Investing

## Execution — 3 Round Trips

**Round 1:**
`ToolSearch query="select:mcp__indmoney__lookup_ind_keys,mcp__indmoney__get_indian_stocks_details,mcp__indmoney__get_indian_stocks_ohlc" max_results=3`

**Round 2 (all parallel):**
- `lookup_ind_keys` stock name → ind_key
- WebSearch: `"[stock name] India news 2025"`
- WebSearch: `"[stock name] fraud legal promoter selling debt 2025"`
- WebSearch: `"[stock name] Q4 results earnings revenue 2025"`
- WebSearch: `"[stock name] analyst target upgrade downgrade 2025"`

**Round 3 (all parallel, after ind_key resolves):**
- `get_indian_stocks_details` ind_key, segments ["analyst", "news"]
- `get_indian_stocks_ohlc` ind_key, interval "1week", lookback "1y"

---

## Technical Analysis

```
diff = 52W_high − 52W_low
fib_78 = high − diff×0.786  ← below this = broken trend, AVOID
fib_61 = high − diff×0.618  ← warning zone
fib_38 = high − diff×0.382  ← ideal entry (pullback in uptrend)
fib_23 = high − diff×0.236  ← near highs
ATR    = diff÷52
trail  = 52W_high − ATR×2
R:R    = (analyst_mean − current) ÷ (current − fib_78)
```

Weekly trend (from OHLC last 8 candles): higher highs + higher lows → uptrend confirmed

---

## Analyst Consensus

- strong_buy: buy% > 70% + upside > 20%
- buy: buy% > 55% + upside > 10%
- hold: buy% 40–55%
- sell: sell% > 40% OR upside < 5%
- trapped: current > analyst HIGH target → exit, no room

---

## News Scoring

Score each item [+] / [-] / [~] / [=]:
- [+] Earnings beat, order wins, contracts, promoter buying, buyback
- [-] Fraud/SEBI/CBI, debt downgrade, promoter selling > 5%, CEO exit, earnings miss
- [~] M&A activity, management changes (uncertain)
- [=] General commentary, sector news not specific to stock

Hard AVOID blocks (regardless of technicals):
- Active fraud investigation | Debt default | Promoter selling > 10% | NPA risk emerging

---

## Verdict Rules

INVEST (High): fib_38+, buy% > 60%, upside > 15%, R:R ≥ 2.5:1, news NET_POSITIVE, no red flags
INVEST (Small): fib_38–fib_61, buy% > 50%, upside > 10%, R:R ≥ 2:1, news MIXED (no hard [-])
SPECULATIVE: below fib_50, R:R ≥ 3:1, mixed news, clear catalyst needed, max 2% portfolio
WAIT: fundamentals fine but fib_61–fib_78 zone OR short-term negative event — set alert at fib_38
AVOID: current < fib_78 OR hard block triggered OR sell% > 50% OR R:R < 1.5:1

Position sizing:
- INVEST High → 8-10% portfolio, lump sum if at fib_38, SIP if near highs
- INVEST Small → 4-6% portfolio, split 50% now + 50% on confirmation
- SPECULATIVE → 1-2% portfolio, hard stop at fib_78
- Stop loss for all: fib_78 (weekly close below = exit)

---

## Output Format

```
## Stock Research — [Stock] | [Date]
VERDICT: INVEST / INVEST (SMALL) / SPECULATIVE / WAIT / AVOID

### TECHNICAL
Current: ₹X | 52W: ₹low–₹high | Fib zone: [name]
fib_78=₹A | fib_61=₹B | fib_38=₹C | Trail stop=₹D
Trend: [uptrend/sideways/downtrend]

### ANALYST
Buy X% | Hold Y% | Sell Z% | N analysts
Target: Low ₹A | Mean ₹B | High ₹C | Upside X% | R:R X:1

### NEWS — INDmoney
[+/-/~/=] [headline] — [date]
Net sentiment: NET_POSITIVE / MIXED / NET_NEGATIVE

### NEWS — Web Scan (last 30 days)
[+/-/~/=] [headline] — [source]
Red flags: CLEAR / [what was found]

### MACRO
Sector: [tailwind/headwind/neutral] | Rate: [impact] | FII: [buying/selling]

### VERDICT RATIONALE
Technical: ... | Analyst: ... | News: ... | Macro: ...

### ENTRY PLAN
Entry ₹X | Stop ₹Y (fib_78) | T1 ₹Z | T2 ₹W (analyst mean)
R:R X:1 | Max X% portfolio | Style: [lump sum/split/SIP]
Watch: [what would change this verdict]
```
