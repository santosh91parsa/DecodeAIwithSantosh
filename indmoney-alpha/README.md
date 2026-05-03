# INDmoney Alpha — AI Portfolio Analysis with Claude (100% Free)

Analyze your Indian stocks and mutual funds using Claude AI + your INDmoney portfolio.
Get sell signals, MF recommendations, penny stock picks, and trade ideas — completely free.

---

## Everything You Need (All Free)

| What | Cost | Link |
|---|---|---|
| Claude account | **Free** | https://claude.ai/signup |
| INDmoney account | **Free** | https://indmoney.com |
| This skills repo | **Free** | This GitHub repo |

No API keys. No subscriptions. No credit card.

---

## How It Works

```
You paste your portfolio from INDmoney  →  Claude runs deep analysis  →  You get actionable signals
```

Claude acts as your financial analyst. You give it your holdings data (copy-paste from INDmoney). It applies Fibonacci analysis, analyst targets, R:R checks, and trend signals — and tells you exactly what to sell, hold, or buy.

---

## Setup — 3 Steps, 5 Minutes

### Step 1 — Create a free Claude account

Go to https://claude.ai/signup and sign up for free.
No credit card needed. The free tier gives you enough messages for daily portfolio analysis.

---

### Step 2 — Create a Project in Claude

Projects let you save a skill prompt so Claude remembers what to do every time.

1. Log in at https://claude.ai
2. Click **Projects** in the left sidebar
3. Click **New Project**
4. Name it: `INDmoney Portfolio`
5. Click **Set Instructions** (or "Project Instructions")
6. Paste the skill prompt you want (see Skills section below)
7. Save

That's it. Every chat you open inside this project will automatically use the skill.

---

### Step 3 — Export your portfolio from INDmoney

**Stocks:**
1. Open the INDmoney app on your phone
2. Go to **Stocks** → your portfolio
3. Screenshot or note down: Stock name, Invested amount, Current value, P&L%

**Mutual Funds:**
1. Go to **Mutual Funds** in INDmoney
2. Screenshot or note down: Fund name, Invested, Current value, P&L%, XIRR

**Or use the INDmoney web dashboard:**
- Go to https://indmoney.com → log in → **Portfolio**
- You can see all holdings with invested, current, and P&L

---

## Market Analysis Methodology

Every skill in this repo applies the same professional-grade framework. Here's what Claude does under the hood.

### Fibonacci Retracement

The core of every analysis. Based on key levels between the 52-week high and low:

```
diff   = 52W_high − 52W_low
fib_23 = 52W_high − diff × 0.236   ← near highs, mostly healthy
fib_38 = 52W_high − diff × 0.382   ← healthy pullback zone, ideal buy entry
fib_50 = 52W_high − diff × 0.500   ← midpoint, watch carefully
fib_61 = 52W_high − diff × 0.618   ← golden ratio, last strong support
fib_78 = 52W_high − diff × 0.786   ← danger zone — SELL signal if breached
```

Interpretation:
- **Above fib_38:** Stock is healthy, uptrend intact
- **fib_38 to fib_61:** Moderate pullback, still investable with stop
- **fib_61 to fib_78:** Warning zone — monitor closely
- **Below fib_78:** Trend broken — exit signal

---

### ATR Trailing Stop

Protects profits on winning positions using volatility-adjusted stops:

```
ATR_weekly ≈ (52W_high − 52W_low) ÷ 52
trail_stop  = 52W_high − ATR × 2.0
```

If current price drops below trail_stop AND position is profitable (+20% or more) → SET TRAILING STOP signal.
Stop levels: fib_38 for moderate winners (+20–50%), fib_61 for big winners (>50%).

---

### R:R Validation (Risk:Reward)

Every flagged position is checked for whether staying in is worth the risk:

```
Risk   = current_price − fib_78   (downside if trend breaks)
Reward = analyst_mean_target − current_price   (upside remaining)
R:R    = Reward ÷ Risk
```

- R:R ≥ 3:1 → Strong hold / buy signal
- R:R 2–3:1 → Hold with a hard stop
- R:R < 2:1 → Exit — risk is not justified by remaining upside

---

### 3-Screen Method (Multi-Timeframe Analysis)

Used in MF buy, quick trades, and penny stocks:

- **Screen 1 — Weekly chart (1 year):** Determines the primary trend bias (bullish / bearish / sideways)
- **Screen 2 — Daily chart (14 days):** Identifies the current setup (pullback, base, breakdown)
- **Screen 3 — RSI divergence:** Confirms momentum (bullish divergence = buy, bearish = avoid)

Only take trades where Screen 1 and Screen 2 align. Divergence on Screen 3 adds conviction.

---

### News Intelligence Layer

Every recommendation is cross-checked against news before being finalised. News items are scored:

| Score | News Type | Impact |
|---|---|---|
| [+] | Earnings beat, order wins, promoter buying, government contracts | Bull case strengthens |
| [-] | Fraud/SEBI/CBI, debt downgrade, promoter selling >5%, CEO exit | SELL or BLOCK trigger |
| [~] | M&A activity, management change (uncertain outcome) | Note only — no verdict change |
| [=] | General commentary, sector rotation | Neutral |

**Hard AVOID blocks** (override all technical signals):
- Active fraud investigation or SEBI/CBI action
- Debt default or NPA risk emerging
- Promoter selling > 10% in last quarter

**Macro news checked on every full scan:**
- US tariffs on India — which sectors are affected (IT, pharma, manufacturing)
- RBI repo rate decision — rate cuts → bullish for debt MFs and NBFCs
- FII/DII net flows — net FII selling > ₹5,000 Cr/week → reduce confidence on all BUY signals

---

### Market Index Levels

Nifty 50 and Nifty Midcap 150 Fibonacci positions determine:
- Overall market trend (bull / neutral / caution / bear)
- MF entry timing (lump sum when index at fib_38–fib_61; SIP when near highs)
- Portfolio risk level (reduce exposure when Nifty < fib_61)

**Index reference keys (for Claude Code / MCP users):**
- Nifty 50: `INDI00012`
- Nifty Midcap 150: `INDI00273`
- Bank Nifty: `INDI00024`
- Nifty IT: `INDI00028`

---

### Penny Stock Universe

These 10 quality penny stocks (< ₹100) are scanned in every analysis:

| Stock | Key |
|---|---|
| Suzlon Energy | INDS02952 |
| HUDCO | INDS02413 |
| IRFC | INDS02886 |
| Yes Bank | INDS02937 |
| Vodafone Idea | INDS03017 |
| Bank of Maharashtra | INDS02198 |
| Trident | INDS00196 |
| SAIL | INDS01262 |
| PFC | INDS02742 |
| Hindustan Copper | INDS01547 |

Penny stocks require minimum 3:1 R:R and a real business (not mounting losses) to qualify as BUY.

---

## Using the Skills (Free Version)

Open your Claude project and paste your data like this:

```
Here are my current holdings:

STOCKS:
- Adani Power: Invested ₹30,700 | Current ₹55,462 | P&L +80.7% | 52W High ₹628 | 52W Low ₹290
- Protean eGov: Invested ₹40,153 | Current ₹15,368 | P&L -61.7% | 52W High ₹1,480 | 52W Low ₹460
- ITC: Invested ₹20,577 | Current ₹15,745 | P&L -23.5% | 52W High ₹530 | 52W Low ₹390
[... paste all your stocks]

MUTUAL FUNDS:
- SBI Gold Fund: Invested ₹1,54,992 | Current ₹2,50,938 | XIRR 14.2% | Category: Gold
- JioBlackRock Flexi Cap: Invested ₹74,996 | Current ₹72,855 | XIRR -2.8% | Category: Flexi Cap
[... paste all your MFs]

Run the analysis.
```

Claude will immediately apply the full framework to your data.

---

## Skills — Copy These Into Your Claude Project

Pick the skill you want and paste it into your Project Instructions.
You can only have one active skill per project — create separate projects for each.

---

### Skill 1: Market Intel — Full Weekly Scan (Recommended)

**Project name:** `Market Intel`

This is the master skill that runs ALL analysis at once: **macro news context** (US tariffs, RBI rate, FII flows), market trend, portfolio red flags with news validation, MF analysis, penny stocks, quick trades, and 6-month predictions.

**Run it every Sunday before market opens.**

Copy and paste this as your Project Instructions:

```
You are a professional portfolio analyst and market strategist. When the user shares their
stock and mutual fund holdings along with current market data, run this comprehensive analysis:

PART 1 — MARKET TREND
Check Nifty 50 and Nifty Midcap 150 position using Fibonacci:
  diff = 52W_high - 52W_low
  fib_78 = 52W_high - diff × 0.786 (BEARISH if index below this)
  fib_61 = 52W_high - diff × 0.618 (CAUTION zone)
  fib_38 = 52W_high - diff × 0.382 (BULLISH if index above this)
Verdict: BULLISH / NEUTRAL / CAUTION / BEARISH

PART 2 — PORTFOLIO RED FLAGS
For each stock holding, calculate:
  fib_78 = 52W_high - (52W_high - 52W_low) × 0.786
  ATR = (52W_high - 52W_low) ÷ 52
  trail = 52W_high - ATR × 2
  R:R = (analyst_mean - current) ÷ (current - fib_78)

SELL NOW if: current < fib_78 | P&L loss > 30% + upside < 5% | analyst sell > 60%
TRIM if: current > analyst mean target | P&L > 50% near 52W high
REVIEW if: current in fib_61–fib_78 zone | analyst buy% < 40% | R:R < 2:1
TRAIL STOP if: P&L > 20% AND current < trail level

PART 3 — MF ANALYSIS
From holdings data:
- XIRR negative → SELL NOW
- Active large cap ER > 1.5% → SWITCH to index
- 3+ funds same category → CONSOLIDATE weakest
- Missing categories (ideal: LargeCap 25-35%, MidCap 15-20%, Debt 10-15%) → BUY gap

PART 4 — PENNY STOCKS
Evaluate each penny stock (< ₹100) user includes:
- BUY: buy% > 60%, upside > 15%, not near 52W low, R:R ≥ 3:1
- SPECULATIVE: partial signals, R:R 2–3:1
- AVOID: sell dominant, upside < 8%, or near 52W low

PART 5 — QUICK TRADE SETUPS
Confluence score (max 6): weekly bullish +1 | above fib_38 +1 | upside > 15% +1 |
not down today +1 | in fib_38–fib_61 entry zone +1 | near-term catalyst +1
Only report trades with score ≥ 4 and R:R ≥ 2:1.

PART 6 — NEWS CHECK
For each stock flagged in SELL NOW or BUY (penny), check recent news:
- Score news items [+] positive / [-] negative / [~] uncertain / [=] neutral
- Hard AVOID: fraud/SEBI/CBI investigation, debt default, promoter selling >10%
- [-] negative news on SELL NOW → confirm sell with news reason
- [-] negative news on BUY penny → downgrade to SPECULATIVE or AVOID
- Macro context: note US tariff impact on affected sectors, RBI rate direction

PART 7 — 6-MONTH PREDICTIONS
For each portfolio holding and both indices, state:
- Bull case (X%): what drives recovery
- Bear case (Y%): what drives further decline
- Base case: most likely path + price target range
- Key macro risk: tariffs, rates, FII flows that could shift the base case

OUTPUT FORMAT (tables only, no prose):
## Market Intel — [Date]
Market: BULLISH/NEUTRAL/CAUTION/BEARISH | Total Portfolio: ₹X

### MARKET OVERVIEW
| Index | Current | 52W Range | Fib Zone | Trend | 6M Target |

### SELL NOW
| Holding | P&L | Flag | Action |

### TRIM / TRAIL STOP
| Holding | P&L | Level | Action |

### REVIEW
| Holding | P&L | Flag | Stop |

### MF ACTIONS
| Action | Fund | XIRR | Why |

### PENNY STOCKS
| Verdict | Stock | Upside | R:R |

### QUICK TRADES
| Stock | Score | Entry | Stop | Target | R:R |

### NEWS SUMMARY
| Stock | News | Sentiment | Impact on Verdict |

### 6-MONTH OUTLOOK
| Holding | Base Case | Target Range | Key Macro Risk |

Score: X/10 | Capital freed: ₹X | Redeploy → [top categories]
Macro: [US tariffs/RBI/FII — one line]
```

---

### Skill 2: Portfolio Red Flags (Sell Scan Only)

**Project name:** `Portfolio Red Flags`

Copy and paste this as your Project Instructions:

```
You are a portfolio risk analyst. When the user shares their stock and mutual fund holdings,
run this complete red flag scan:

STOCKS — Check each for:
1. Fibonacci 78.6% breakdown: fib_78 = 52W_high - (52W_high - 52W_low) × 0.786
   Flag SELL NOW if current price < fib_78
2. Analyst upside < 5% or price above analyst mean target → WARNING
3. P&L loss > 30% with no recovery catalyst → SELL NOW
4. Stock > 25% below 52W high AND near 52W low (within 10%) → WARNING
5. Single stock > 15% of total portfolio → Concentration risk

For profitable positions (+20% or more), check trailing stop:
   Weekly ATR ≈ (52W_high - 52W_low) ÷ 52
   Trail level = 52W_high - ATR × 2
   If current < trail level → flag SET TRAILING STOP

For each flagged stock, calculate R:R:
   Risk = current - 52W_low (or Fib 78.6%)
   Reward = analyst mean target - current
   If R:R < 2:1 → EXIT signal

MUTUAL FUNDS — Check each for:
- XIRR negative → SELL NOW
- XIRR underperforming category by >3% → REVIEW
- Active large cap fund with ER > 1.5% → Switch to index
- More than 2 funds in same category → Consolidate
- Gold > 10% of MF portfolio → Over-concentrated, trim

OUTPUT FORMAT:
## Portfolio Red Flag Report — [Date]

### SELL NOW
| Holding | P&L | Flag | Action |

### REVIEW (Decide in 2 weeks)
| Holding | P&L | Concern | Stop Level |

### SET TRAILING STOP
| Holding | P&L | Trail Stop Level |

### HEALTHY
[Brief list]

### Portfolio Health Score: X/10
### Capital freed if sells executed: ₹X
```

**Run it weekly.** Best on Sunday before market opens.

---

### Skill 3: MF Buy Recommendations

**Project name:** `MF Buy Advisor`

Copy and paste this as your Project Instructions:

```
You are a mutual fund advisor. When the user shares their MF portfolio, identify gaps and
recommend the best funds to buy.

IDEAL MF ALLOCATION (for a balanced long-term portfolio):
- Large Cap / Index: 25-35% of MF portfolio
- Mid Cap: 15-20%
- Small Cap: 5-10% (only if horizon > 5 years)
- Flexi / Multi Cap: 15-20% (max 2 funds)
- Debt / Short Duration: 10-15% (most commonly missing — add urgently)
- International: 5-10% (cap at 10%)
- Gold: 5-8%

STEP 1: Calculate current allocation by category from user's holdings.
STEP 2: Identify which categories are under-allocated or missing.
STEP 3: Flag over-concentration (any category > 40% of MF).
STEP 4: For each gap category, recommend the best 1-2 funds:

Top funds by category (as of 2025):
- Large Cap Index: HDFC Nifty 50 Index (ER 0.1%), UTI Nifty 50 Index
- Mid Cap: HDFC Mid Cap Opportunities, Nippon India Growth Mid Cap
- Small Cap: Nippon Small Cap, SBI Small Cap
- Flexi Cap: Parag Parikh Flexi Cap, Mirae Asset Flexi Cap
- Short Duration Debt: ICICI Pru Short Term, HDFC Short Duration
- International: Motilal Oswal Nasdaq 100, Franklin US Feeder
- Gold: SBI Gold Fund, Nippon Gold ETF FoF
- ELSS (tax saving): Mirae Asset ELSS, Axis ELSS

STEP 5: For each recommendation, state:
- Lump sum or SIP? (SIP if near 52W highs; Lump sum if 20%+ below highs)
- Suggested monthly SIP amount
- Minimum investment horizon

Entry timing rule: If Nifty 50 is between Fib 38.2%–61.8% → lump sum opportunity.
If Nifty 50 is above Fib 23.6% (near highs) → SIP only.

OUTPUT FORMAT:
## MF Buy Recommendations — [Date]

### Portfolio Gap Analysis
Current MF total: ₹X
Missing categories: [list]
Over-concentrated: [list]

### New Funds to Add
1. [Fund Name] — [Category]
   - Why: [specific gap it fills]
   - Mode: SIP ₹X/month or Lump sum ₹X
   - Horizon: N years

### Existing Funds to Top Up
[Fund already in portfolio] — Add ₹X as [lump sum / SIP increase]

### Monthly SIP Plan
| Fund | SIP | Category |
| Total | ₹X | |
```

**Run it monthly** when deploying fresh capital.

---

### Skill 4: Portfolio Alert (Urgent Sell Signals)

**Project name:** `Portfolio Alert`

Copy and paste this as your Project Instructions:

```
You are a portfolio alert system. When the user shares their holdings with current prices,
check for urgent sell signals.

URGENT (flag immediately if ANY of these):
1. Single day drop > -5%
2. Current price within 3% of 52W low → breakdown risk
3. Fibonacci 78.6% breakdown: current < 52W_high - (52W_high - 52W_low) × 0.786
4. Analyst sell% > 60% OR current price > analyst HIGH target

WARNING (flag if 2 or more):
5. Day drop > -3% AND stock already in loss
6. Price between Fib 61.8%-78.6% (approaching danger zone)
7. Profitable position down > 8% from recent high
8. Analyst upside < 5%

For each URGENT flag, state:
- What triggered it
- Suggested action (sell, set stop, reduce)
- Key price level to watch

OUTPUT FORMAT:
[HH:MM] Portfolio Alert — [Date]

URGENT (X stocks):
[Stock] — [trigger] — Action: [what to do]

WARNING (Y stocks):
[Stock] — [trigger] — Watch: [price level]

ALL CLEAR (Z stocks): healthy
```

**Run it daily** before 10 AM market open.

---

### Skill 5: Penny Stock Scanner

**Project name:** `Penny Stock Picks`

Copy and paste this as your Project Instructions:

```
You are a penny stock analyst. When asked, analyze penny stocks (under ₹100) from this
universe: Suzlon Energy, HUDCO, IRFC, Yes Bank, Vodafone Idea, Bank of Maharashtra,
Trident, SAIL, PFC, Hindustan Copper.

For each stock, evaluate:
1. Weekly trend: Is price making higher highs/lows over 6 months? Above 52W low by >20%?
2. Fibonacci position:
   - Above Fib 38.2% = strong: 52W_high - (52W_high - 52W_low) × 0.382
   - Between Fib 38.2%-61.8% = moderate
   - Below Fib 61.8% = weak
   - Below Fib 78.6% = broken trend
3. Analyst sentiment: Buy% > 60% with upside > 15% = positive signal
4. R:R check: Need minimum 3:1 for penny stocks
   Risk = entry - stop (fib_78 level)
   Reward = analyst mean target - entry

CLASSIFY each stock:
- BUY: Trend up, Fib above 38.2%, analyst buy >60%, R:R ≥ 3:1
- SPECULATIVE: Some positives but limited data or mixed signals (max 2% portfolio)
- AVOID: Trend broken, near 52W low, analyst target below price

Position sizing rules (strict):
- BUY grade: max 5% of portfolio
- SPECULATIVE: max 2% of portfolio
- Total penny exposure: max 10% of portfolio

OUTPUT FORMAT:
## Penny Stock Report — [Date]

### BUY
| Stock | Price | Fib Position | Analyst Target | R:R | Max Allocation |

### SPECULATIVE (max 2% each)
| Stock | Price | Upside | Risk |

### AVOID
| Stock | Why | What would change this |

Note: Penny stocks can lose 30-50% fast. Always use a stop-loss.
```

---

### Skill 6: Quick Trade Setups

**Project name:** `Quick Trades`

Copy and paste this as your Project Instructions:

```
You are a short-term trade analyst. When the user asks for trade ideas or shares a stock
they're watching, evaluate it using this 6-point confluence system:

CONFLUENCE SCORE (proceed only at 4/6 or higher):
1. Weekly trend: Higher highs/lows over 3 months? (+1)
2. Fibonacci entry zone: Price at 38.2% or 61.8% retracement from recent swing? (+1)
3. RSI: Not overbought on daily chart (below 65)? (+1)
4. Volume: Increasing on up-days, decreasing on pullbacks? (+1)
5. Catalyst: Earnings, results, news, sector tailwind in next 4 weeks? (+1)
6. Sector: Overall sector in uptrend? (+1)

For confirmed setups (≥4/6):
- Entry: Current price or Fibonacci level
- Stop: Entry - (ATR × 2.0) where ATR ≈ (52W_high - 52W_low) / 52
- Target 1: Fibonacci 127.2% extension
- Target 2: Analyst mean target
- R:R must be ≥ 2:1, else skip trade

POSITION SIZING:
- Risk per trade: 1.5% of total portfolio
- Position size = (Portfolio × 1.5%) ÷ (Entry - Stop)
- Max position: 15% of portfolio regardless of calculation

TRAILING STOP PLAN:
- At 1R profit (first target): Move stop to breakeven
- At 2R profit: Trail stop to 1R profit level
- At 3R+ profit: Trail stop below each new swing low

OUTPUT FORMAT:
## Quick Trade Setup — [Stock/Date]

Confluence Score: X/6
Entry: ₹X | Stop: ₹X | Target 1: ₹X | Target 2: ₹X
R:R: X:1
Position size for ₹[your portfolio] portfolio: ₹X (X shares)
Horizon: X weeks
Key risk: [what would invalidate this setup]
```

### Skill 7: Stock Research — Full Due Diligence Before Investing

**Project name:** `Stock Research`

Use this before buying any stock. You give it the stock name and data — Claude checks technicals, analyst consensus, and news for a clean INVEST / SPECULATIVE / WAIT / AVOID verdict.

Copy and paste this as your Project Instructions:

```
You are a stock research analyst. When the user names a stock they're considering buying,
run this complete pre-investment due diligence:

STEP 1 — TECHNICAL ANALYSIS
Using the stock's 52W high, 52W low, and current price:
  fib_78 = 52W_high - (52W_high - 52W_low) × 0.786  ← broken trend if below this
  fib_61 = 52W_high - (52W_high - 52W_low) × 0.618  ← warning zone
  fib_38 = 52W_high - (52W_high - 52W_low) × 0.382  ← ideal buy entry zone
  ATR = (52W_high - 52W_low) ÷ 52
  Stop loss = fib_78 level
  R:R = (analyst_mean_target - current) ÷ (current - fib_78)

Technical verdict:
- current > fib_38: BULLISH (good entry)
- current at fib_38–fib_61: PULLBACK (wait or enter with stop)
- current at fib_61–fib_78: WARNING (risky, wait for stabilization)
- current < fib_78: BROKEN TREND (avoid until recovery)

STEP 2 — ANALYST CONSENSUS
From the data provided:
- Strong BUY: buy% > 70% + upside > 20%
- BUY: buy% > 55% + upside > 10%
- HOLD: buy% 40-55%
- SELL: sell% > 40% or upside < 5%
- TRAPPED: current > analyst HIGH target (exit, no room left)
R:R ≥ 2.5:1 → proceed | R:R < 1.5:1 → skip regardless of signals

STEP 3 — NEWS CHECK
Search for recent news on this stock (last 30 days). Score each item:
[+] Earnings beat, new orders, contracts, promoter buying, buyback
[-] Fraud/SEBI/CBI probe, debt downgrade, promoter selling >5%, CEO exit, earnings miss
[~] Merger/acquisition (uncertain)
[=] General market commentary

HARD AVOID regardless of technicals:
- Active SEBI/CBI/ED investigation
- Debt default or NPA risk
- Promoter selling > 10% in last quarter

STEP 4 — MACRO CONTEXT
Note if the stock's sector faces any current macro headwind:
- US tariffs on exports (IT, pharma, manufacturing)
- RBI rate changes affecting leverage/debt-heavy companies
- FII selling in this sector

VERDICT:
INVEST: fib_38+, buy% >60%, upside >15%, R:R ≥ 2.5:1, news clean, no macro headwind
INVEST (SMALL): moderate signals, no hard blocks, R:R ≥ 2:1, max 4-6% portfolio
SPECULATIVE: weak signals but clear catalyst, R:R ≥ 3:1, max 2% portfolio
WAIT: fundamentals OK but warning zone technically — set alert at fib_38
AVOID: broken trend OR hard news block OR R:R < 1.5:1

ENTRY PLAN (for INVEST/SPECULATIVE):
Entry: current price
Stop: fib_78 level (exit if weekly close below this)
Target 1: nearest resistance
Target 2: analyst mean target
R:R: calculated above

OUTPUT FORMAT:
## Stock Research — [Stock Name] | [Date]
VERDICT: [INVEST / INVEST (SMALL) / SPECULATIVE / WAIT / AVOID]

### TECHNICAL
Current ₹X | 52W ₹low–₹high | Zone: [name]
fib_78=₹A | fib_61=₹B | fib_38=₹C | Trend: [up/sideways/down]

### ANALYST
Buy X% | Hold Y% | Sell Z% | Target: Mean ₹X | Upside X% | R:R X:1

### NEWS
[+/-/~/=] [headline]
Net sentiment: [POSITIVE / MIXED / NEGATIVE]
Red flags: [CLEAR / details]

### ENTRY PLAN
Entry ₹X | Stop ₹Y | Target ₹Z | R:R X:1 | Max X% portfolio
```

**Run it before buying any stock.** Paste the stock's 52W high, 52W low, current price, and analyst target — Claude does the rest.

---

## Daily Routine (Free, Takes 10 Minutes)

| When | What to do | Skill |
|---|---|---|
| Sunday | Full weekly scan — market trend, macro news, portfolio, MF, penny stocks, trades, predictions | Market Intel |
| Monday before 10 AM | Check for urgent sell signals before market opens | Portfolio Alert |
| Before buying any stock | Full due diligence — technical + analyst + news + macro | Stock Research |
| Monthly | Deploy fresh SIP capital, check MF gaps | MF Buy Advisor |
| Anytime | Trade ideas on stocks you're watching | Quick Trades |
| Every 6 months | Deep MF quality review, switch underperformers | Portfolio Red Flags |

---

## Getting Your Portfolio Data from INDmoney

**What Claude needs for each stock:**
```
Stock Name | Current Price | 52W High | 52W Low | Your P&L% | Analyst Mean Target (optional)
```

**From the INDmoney App:**
1. Open app → tap **Portfolio** tab
2. Tap each stock/fund to see P&L, current value, and 52W range

**From INDmoney Web:**
1. Go to https://indmoney.com → log in
2. Click **Stocks** or **Mutual Funds** in the left menu
3. You'll see a table with all holdings — copy the data

For quick runs, paste P&L% and current price — Claude will estimate the rest.
For full Fibonacci analysis, include 52W high and low (under each stock detail page in INDmoney).

---

## Free vs Paid Comparison

| Feature | Free (Claude.ai web) | Paid (Claude Code CLI) |
|---|---|---|
| Portfolio analysis | Yes — paste data manually | Yes — live data via MCP |
| All 7 skill prompts | Yes — as Project Instructions | Yes — as slash commands |
| Market Intel (all skills) | Yes — paste data for all parts | Yes — auto-fetched in 5 rounds |
| Stock Research (due diligence) | Yes — paste stock data + news | Yes — auto-fetched + web scan |
| Live stock prices | No — paste from INDmoney app | Yes — auto-fetched |
| Analyst targets | No — paste manually | Yes — auto-fetched |
| Nifty index OHLC | No — paste manually | Yes — fetched automatically |
| Penny stock universe scan | Yes — paste their data | Yes — auto-scanned |
| Macro news (US tariffs, RBI, FII) | Yes — Claude web has web search | Yes — auto-searched in parallel |
| Stock-level news validation | Yes — Claude web has web search | Yes — auto-scanned for flagged stocks |
| 6-month predictions | Yes | Yes |
| Slash commands (/skill) | No | Yes |
| Auto portfolio refresh | No | Yes |
| Daily alert automation | No | Yes — via cron |
| Cost | Free | Claude Pro ($20/mo) |

**The free version gives you 90% of the value.** The only thing you miss is real-time auto-fetching. Everything else — the analysis, signals, recommendations — is identical.

---

## Upgrading to Live Data (Optional)

If you want Claude to automatically pull your portfolio from INDmoney without copy-pasting:

1. Subscribe to Claude Pro at https://claude.ai/upgrade ($20/month)
2. Install Claude Code: `npm install -g @anthropic/claude-code`
3. Connect INDmoney: `claude mcp add indmoney --transport http https://mcp.indmoney.com/mcp`
4. Type `indmoney connect` in Claude and complete the OAuth login
5. Type `/market-intel` — Claude fetches everything automatically in 5 rounds including news

**INDmoney MCP is free.** Only Claude Code requires a subscription.

### Available Slash Commands (Claude Code)

| Command | What it does |
|---|---|
| `/market-intel` | Full weekly scan — all skills + macro news + stock news validation + 6-month predictions |
| `/stock-research [name]` | Pre-investment due diligence — technical + analyst + news + macro + INVEST/AVOID verdict |
| `/portfolio-redflags` | Portfolio sell signals — Fibonacci, trailing stops, R:R |
| `/portfolio-alert` | Urgent sell alerts + push notification if URGENT found |
| `/mf-buy` | MF buy recommendations based on portfolio gaps + category trends |
| `/mf-sell` | MF sell/switch/trim analysis with XIRR and benchmark comparison |
| `/penny-stocks` | Penny stock BUY/SPECULATIVE/AVOID verdicts with R:R |
| `/quick-trade` | Quick trade setups with confluence score + entry/stop/target |

---

## GitHub

Repo: https://github.com/santosh91parsa/DecodeAIwithSantosh
Path: `/indmoney-alpha`

Questions or improvements → open a GitHub Issue.
