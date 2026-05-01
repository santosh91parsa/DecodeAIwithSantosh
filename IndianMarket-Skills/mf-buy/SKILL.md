---
name: mf-buy
description: |
  Identify the best mutual funds to buy based on portfolio gaps, category trend analysis using
  the 3-screen method, Fibonacci entry timing to decide lump sum vs SIP, and fund performance
  vs benchmark from INDmoney data. Covers all categories: large cap, mid cap, small cap, flexi
  cap, debt, international, gold, and ELSS. Returns a concrete monthly SIP plan and lump sum
  opportunities with minimum investment horizons.

  Use when the user asks: "which mutual fund to buy", "mf buy recommendation", "best mutual fund
  to invest", "where to invest in mutual funds", "new fund to start SIP", "mutual fund suggestion",
  "top performing funds", "fund recommendation", "should I do lump sum or SIP", "which fund is
  missing from my portfolio", "mutual fund portfolio gaps", or any question about adding new MF.

  Requires INDmoney MCP server connected. Uses: networth_snapshot, networth_holdings (MF),
  networth_allocation_breakdown (MF by assets), get_mf_by_category, get_mf_funds_details
  (with fund_performance and asset_allocation includes).
---

# Mutual Fund Buy Recommendation

Identify best mutual funds based on portfolio gaps, category trend (3-screen method), Fibonacci entry timing for lump sum vs SIP, and performance vs benchmark.

## Execution Steps

### Step 1 — Fetch current portfolio state
Use `networth_snapshot` for total portfolio and asset class breakdown.
Use `networth_holdings` for all MF positions (names, invested, XIRR, category).
Use `networth_allocation_breakdown` with asset_type "MF" and breakdown_by "assets".

### Step 2 — Identify portfolio gaps

Ideal MF allocation for a balanced long-term portfolio:

| Category | Ideal Range | Gap Action |
|---|---|---|
| Large Cap / Index | 25-35% of MF | Add if missing |
| Mid Cap | 15-20% of MF | Add — strong India growth story |
| Small Cap | 5-10% of MF | Add only if horizon > 5 years |
| Flexi / Multi Cap | 15-20% of MF | Max 1-2 funds (avoid overlap) |
| Debt / Short Duration | 10-15% of MF | Most commonly missing — add urgently |
| International | 5-10% of MF | Cap at 10% — currency risk |
| Gold | 5-8% of MF | Good inflation hedge, don't over-allocate |
| ELSS | Optional | Add if need 80C tax benefit |

Flag over-concentration: any single category > 40% of MF portfolio.

### Step 3 — Category Trend Analysis (3-Screen Method)
Before recommending any category, check its trend:

**Screen 1 — Long-term category health (weekly, 1Y):**
- Large Cap: Is Nifty 50 making higher highs/lows over 6 months?
- Mid Cap: Is Nifty Midcap 150 above its 6-month average?
- Small Cap: Is Nifty Smallcap 250 recovering or still in correction?
- Debt: Are interest rates falling? (RBI rate cut cycle = bullish for duration funds)
- Gold: Is gold above its 6-month moving average?

**Screen 2 — Current setup:**
- Category pulling back from highs? → Good entry opportunity
- Category at all-time highs? → SIP preferred over lump sum
- Category in recovery from 20%+ correction? → Lump sum opportunity

**Trend verdict per category:**
- Bullish + pullback → Best entry: Lump sum OR accelerated SIP
- Bullish + at highs → SIP only
- Sideways/correcting → SIP only, wait for trend confirmation
- Downtrend → Avoid until trend turns

### Step 4 — Fibonacci Entry Timing for Lump Sum
For each recommended category, check if it's in a Fibonacci buy zone using the category index:
```
diff = category_52W_high - category_52W_low
fib_38 = category_52W_high - diff × 0.382  ← ideal lump sum entry
fib_61 = category_52W_high - diff × 0.618  ← deep correction entry (great value)
```
- Category index in Fib 38.2%–61.8% zone → Lump sum recommended
- Category index above Fib 23.6% (near highs) → SIP only
- Category index below Fib 61.8% (deep correction) → Aggressive SIP or small lump sum

### Step 5 — Fetch top funds in gap categories
Use `get_mf_by_category` for each gap category, sorted by `category_ind_rank`.
Use `get_mf_funds_details` with `includes: ["fund_performance", "asset_allocation"]` for top 2-3 candidates.

Evaluate each candidate:
- 3Y XIRR vs category average (fund manager alpha)
- Expense ratio: Active < 1%, Index < 0.3%
- AUM: > ₹5,000 Cr for large/flexi cap
- Consistency: outperformed in both bull and consolidation phases
- Low overlap with existing funds

### Step 6 — Lump Sum vs SIP Decision

**Lump sum is better when:**
- Category is > 20% below 52W high (clear discount)
- Fib position: between 38.2%–61.8% retracement
- Interest rate cycle is turning (for debt funds)

**SIP is better when:**
- Category near 52W highs or above Fib 23.6%
- Valuations stretched (PE above 5-year average)

**Aggressive SIP (2× normal amount) when:**
- Category corrected > 15% from highs but trend still intact (higher lows on weekly)

### Step 7 — Output

```
## Mutual Fund Buy Recommendations — [Date]

### Portfolio Gap Analysis
MF Total: ₹X | Indian Equity: Y% | Global: Z% | Gold: W% | Debt: V%
Critical gaps: [list]
Over-concentrated: [list if any]
Category trend: [bullish / mixed / cautious]

---

### NEW FUNDS TO ADD

#### 1. [Fund Name] — [Category]
- **Category trend:** Bullish / Recovering (Screen 1+2 verdict)
- **Fib entry zone:** Category at X% retracement → [Lump sum / SIP]
- **3Y XIRR:** X% vs category avg Y%
- **Expense ratio:** X% (Direct plan) | AUM: ₹X Cr
- **Suggested entry:** ₹X lump sum OR ₹Y/month SIP
- **Horizon:** Minimum N years

#### 2. [Fund Name] — [Category]
[same format]

---

### EXISTING FUNDS TO TOP UP
[Fund already in portfolio — why top up and how much]

---

### AVOID RIGHT NOW
| Category | Reason | Wait for |

---

### Monthly SIP Plan
| Fund | SIP | Category | Mode |
|---|---|---|---|
| [Fund 1] | ₹X | Mid Cap | Regular SIP |
| [Fund 2] | ₹Y | Debt | Regular SIP |
| **Total** | **₹XYZ** | | |
```

Review every 6 months with /mf-sell to exit underperformers and redeploy.
