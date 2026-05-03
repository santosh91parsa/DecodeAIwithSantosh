---
name: market-intel
description: |
  Master weekly analysis combining ALL 6 skills in one scan: macro news context (US tariffs,
  RBI policy, FII flows), market trend (Nifty 50 + Midcap 150 OHLC), portfolio red flags,
  portfolio alert, MF buy/sell, penny stock verdicts with news validation, quick trade setups
  with news confirmation, and 6-month predictions using technical + macro + news layers.

  Use when the user asks: "market intel", "full analysis", "weekly scan", "run everything",
  "all skills", "comprehensive analysis", "market overview and portfolio", "full report",
  "what's the market doing and what should I do", "sunday scan", "weekly review",
  "market trend and portfolio", "everything at once", "complete portfolio review",
  "check news and recommend", "tariffs impact my portfolio", "macro analysis".

  Requires INDmoney MCP server connected. Uses: networth_holdings, networth_snapshot,
  get_indian_stocks_details (analyst + news), get_indian_stocks_ohlc, get_mf_by_category.
  Also uses WebSearch for macro news (Round 2) and stock news validation (Round 5).
  Total: 5 rounds max, 4 typical, 3 if no deep losers and no flags.
---

# Market Intel — Full Portfolio + Market Analysis (All Skills in One)

## Speed Rules — Minimum Round Trips

**Round 1 (one ToolSearch call):**
Load MCP tools. WebSearch is always available — no need to load it.
`ToolSearch query="select:mcp__indmoney__networth_holdings,mcp__indmoney__networth_snapshot,mcp__indmoney__get_indian_stocks_details,mcp__indmoney__get_indian_stocks_ohlc,mcp__indmoney__get_mf_by_category" max_results=5`

**Round 2 (all parallel — MCP + WebSearch together):**
- `networth_holdings` asset_type "IND_STOCK"
- `networth_holdings` asset_type "MF"
- `networth_snapshot`
- `get_indian_stocks_ohlc` ind_key "INDI00012" interval "1week" lookback "1y"
- `get_indian_stocks_ohlc` ind_key "INDI00273" interval "1week" lookback "1y"
- WebSearch: `"India Nifty stock market outlook [current month year]"`
- WebSearch: `"US tariffs India impact sectors IT pharma 2025"`
- WebSearch: `"RBI repo rate decision India 2025"`
- WebSearch: `"FII DII India equity net flows week"`

**Round 3 (all parallel):**
- `get_indian_stocks_details` batch 1: first 10 portfolio investment_codes, segments ["analyst", "news"]
- `get_indian_stocks_details` batch 2: remaining portfolio investment_codes, segments ["analyst", "news"]
- `get_indian_stocks_details` penny batch 1: ["INDS02952","INDS02413","INDS02886","INDS02937","INDS03017"], segments ["analyst", "news"]
- `get_indian_stocks_details` penny batch 2: ["INDS02198","INDS00196","INDS01262","INDS02742","INDS01547"], segments ["analyst", "news"]

**Round 4 (conditional):**
- `get_indian_stocks_ohlc` interval "1week" lookback "1y" — ONLY for pnl_per < −10% OR day_change < −3%
- Skip if no stock meets threshold

**Round 5 (conditional — news validation for flagged stocks):**
- WebSearch `"[stock name] India news fraud results promoter 2025"` for each:
  - SELL NOW portfolio stocks
  - BUY penny stocks
  - Quick Trade candidates (score ≥ 4)
- Fire all in one parallel message. Cap at 6 searches. Skip if no flags.

---

## Part 0 — Macro Context

From Round 2 WebSearch results:
```
macro_bullish = RBI cutting rates OR FII net buyers OR Nifty new highs
macro_bearish = US tariffs hitting exports OR FII selling OR global recession signal
```

Sector impact: US tariffs on IT/pharma → subtract 1 from confluence for those stocks.
FII net sellers > ₹5,000 Cr/week → reduce confidence one level on all BUY signals.

---

## Part 1 — Market Trend

```
diff = 52W_high − 52W_low | fib_78 = high − diff×0.786 | fib_61 = high − diff×0.618
fib_38 = high − diff×0.382 | ATR = diff÷52
```

Trend: current > fib_38 + 4-week uptrend → BULLISH | fib_38–fib_61 → NEUTRAL
       fib_61–fib_78 → CAUTION | < fib_78 → BEARISH

Macro overlay: macro_bearish → downgrade verdict one level.
6M prediction: Fibonacci position + trend direction + macro context combined.

---

## Part 2 — Portfolio Red Flags

```
fib_78 = 52W_high − diff×0.786 | trail = 52W_high − ATR×2
R:R = (analyst_mean − current) ÷ (current − fib_78)
```

SELL NOW: current < fib_78 | sell% > 60% | pnl < −30% + upside < 5% | day_change < −5%
          | INDmoney news has fraud/downgrade/legal/CEO exit

TRIM: current > analyst MEAN | pnl > 50% + within 5% of 52W high
REVIEW: fib_61–fib_78 zone | buy% < 40% | R:R < 2:1 | near 52W low
        | promoter pledging > 10% OR promoter selling > 5% in news

TRAIL: pnl > 20% AND current < trail level

News overrides: [-] news on REVIEW → upgrade to SELL NOW. [+] news on REVIEW → hold with note.

---

## Part 3 — Portfolio Alert

URGENT: day_change < −5% | within 3% of 52W low | current < fib_78 | sell% > 60%
WARNING: day_change < −3% + in loss | pnl > 20% + current < trail

---

## Part 4 — MF Analysis

From holdings (no extra calls): XIRR negative → SELL | Gold > 15% MF → TRIM
Active large cap ER > 1.5% → SWITCH | 3+ same sub-category → CONSOLIDATE weakest

Macro overlay: RBI rate cut → upgrade debt funds to BUY | US tariff → reduce IT sector funds
FII selling 2+ weeks → prefer debt over equity for new lump sum

Buy gaps: LargeCap 25-35% | MidCap 15-20% | SmallCap 5-10% | Flexi 15-20% | Debt 10-15% | Intl 5-10% | Gold 5-8%
Entry: fib_38–fib_61 + macro_neutral/bullish → lump sum | near highs or macro_bearish → SIP only

---

## Part 5 — Penny Stock Verdicts

Penny ind_keys: Suzlon INDS02952 | HUDCO INDS02413 | IRFC INDS02886 | Yes Bank INDS02937
Vodafone Idea INDS03017 | Bank of Maharashtra INDS02198 | Trident INDS00196
SAIL INDS01262 | PFC INDS02742 | Hindustan Copper INDS01547

BUY: buy% > 60% + upside > 15% + not within 10% of 52W low + R:R ≥ 3:1
BUY BLOCKED (Round 5 news): fraud | promoter selling > 5% | debt default | management exit
SPECULATIVE: buy% 30–60% OR upside 8–15% OR R:R 2–3:1
AVOID: sell dominant OR upside < 8% OR negative news dominant

Include news verdict line per BUY stock: `News: [+] Q4 beat | → BUY confirmed`

---

## Part 6 — Quick Trade Setups

Candidates: Eternal, HDFC Bank, BEL, Bajaj Finance, Tata Motors, IRCTC, Dixon Tech, Persistent,
Mankind Pharma, Coforge, Adani Power, SBI, Vishal Mega Mart, Tata Steel, Sai Life Sciences.

Confluence (0-7): weekly bullish +1 | above fib_38 +1 | upside > 15% + buy% > 60% +1
not down today +1 | in fib_38–fib_61 entry +1 | near-term catalyst +1 | news clean +1 (or −1 if negative)
Macro: US tariff on sector −1 | FII net sellers −1

Only report score ≥ 4 post-adjustment + R:R ≥ 2:1.
Entry = current | Stop = fib_78 or current − ATR×2 | T1 = 52W_high × 1.05 | T2 = analyst mean

---

## Part 7 — News Intelligence (Round 5)

Score each stock news: [+] / [-] / [~] / [=]
Override rules:
- [-] fraud/legal/downgrade on SELL NOW → confirm + cite
- [-] fraud/legal/downgrade on BUY penny → BLOCK → AVOID or SPECULATIVE
- [-] promoter selling on BUY penny → BLOCK → SPECULATIVE
- [-] earnings miss on Quick Trade → subtract 1 from score
- [+] earnings beat on REVIEW → hold, add to bull case
- [+] order win on BUY penny → confirm

---

## Part 8 — 6-Month Predictions

Three-layer prediction: Fibonacci position + macro context + news signal.
Cover: market indices (targets) | sector overweight/underweight | each holding (bull/bear/base) | MF category allocation

---

## Output Format

```
## Market Intel — [Date]
Stocks: X | MFs: Y | Total: ₹Z | Market: BULLISH/NEUTRAL/CAUTION/BEARISH
Macro: [US tariffs/RBI rate/FII flow — one line]

### MARKET OVERVIEW
| Index | Current | 52W Range | Fib Zone | Trend | Macro adj | 6M Target |
6-Month Prediction: [2 lines with macro context]

### SELL NOW
| Holding | P&L | Tech Flag | News | Action |

### TRIM / TRAIL
| Holding | P&L | Level | Action |

### REVIEW
| Holding | P&L | Flag | News | Stop |

### HEALTHY
[comma-separated]

### PORTFOLIO ALERT
URGENT: ... | WARNING: ...

### MUTUAL FUNDS
| Action | Fund | XIRR | Macro Note | Why |

### PENNY STOCKS
| Verdict | Stock | Upside | R:R | News |

### QUICK TRADES
| Stock | Score | Entry | Stop | T1 | R:R | News | Catalyst |

### 6-MONTH OUTLOOK
| Index/Holding | Base Case | 6M Target | Key Risk | News Signal |
Overweight sectors: ... | Underweight: ...

Score: X/10 | Free capital: ₹X | Redeploy → [categories]
```
