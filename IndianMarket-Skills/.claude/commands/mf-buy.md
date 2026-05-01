# Mutual Fund Buy Recommendation

Identify best mutual funds to buy based on portfolio gaps, category trend analysis (3-screen method), performance vs benchmark, and R:R of lump sum vs SIP timing.

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
- Large Cap: Is Nifty 50 in an uptrend? (higher highs/lows over 6 months)
- Mid Cap: Is Nifty Midcap 150 above its 6-month average?
- Small Cap: Is Nifty Smallcap 250 recovering or still in correction?
- Debt: Are interest rates falling? (RBI rate cut cycle = bullish for duration funds)
- Gold: Is gold above its 6-month moving average?

**Screen 2 — Current setup:**
- Is the category pulling back from a high? → Good entry opportunity (buy on dip)
- Is the category at all-time highs? → SIP preferred over lump sum (average the cost)
- Is the category in recovery from a 20%+ correction? → Lump sum opportunity

**Trend verdict per category:**
- Bullish + pullback → Best entry: Lump sum OR accelerated SIP
- Bullish + at highs → SIP only (avoid lump sum at peak)
- Sideways/correcting → SIP only, wait for trend confirmation
- Downtrend → Avoid until trend turns

### Step 4 — Fibonacci Entry Timing for Lump Sum
For each recommended category, check if it's in a Fibonacci buy zone:
```
diff = category_52W_high - category_52W_low  (use index as proxy)
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
- AUM: > ₹5,000 Cr for large/flexi cap; mid/small cap can be smaller
- Consistency: outperformed in both bull (2023-24) and consolidation (2025) phases
- Overlap with existing funds: low overlap preferred

### Step 6 — R:R of Lump Sum vs SIP

**Lump sum is better when:**
- Category is > 20% below 52W high (clear discount)
- Fib position: between 38.2%–61.8% retracement
- Interest rate cycle is turning (for debt funds)
- Strong catalyst visible (policy, budget, sector tailwind)

**SIP is better when:**
- Category near 52W highs or above Fib 23.6%
- Valuations stretched (PE above 5-year average for equity)
- No clear near-term catalyst

**Aggressive SIP (2× normal amount) when:**
- Category corrected > 15% from highs but trend still intact (higher lows on weekly)
- This is the best way to get a lump-sum-like effect with dollar-cost averaging protection

### Step 7 — Output

```
## Mutual Fund Buy Recommendations — [Date]

### Portfolio Gap Analysis
MF Total: ₹X | Indian Equity: Y% | Global: Z% | Gold: W% | Debt: V%
Critical gaps: [list categories]
Over-concentrated: [list if any]
Category trend summary: [bullish / mixed / cautious]

---

### NEW FUNDS TO ADD

#### 1. [Fund Name] — [Category]
- **Category trend:** Bullish / Recovering / Avoid (Screen 1+2 verdict)
- **Fib entry zone:** Category index at X% retracement → [Lump sum / SIP]
- **3Y XIRR:** X% vs category avg Y% (alpha: +Z%)
- **Expense ratio:** X% (Direct plan)
- **AUM:** ₹X Cr
- **Why this fund:** [specific edge vs peers]
- **Suggested entry:** ₹X lump sum OR ₹Y/month SIP
- **Horizon:** Minimum N years

#### 2. [Fund Name] — [Category]
[same format]

---

### EXISTING FUNDS TO TOP UP
[Fund already in portfolio]
- Current: ₹X | XIRR: Y% — performing well
- Category at Fib level: [entry opportunity?]
- Add: ₹X lump sum OR increase SIP by ₹Y/month

---

### AVOID RIGHT NOW
| Category | Reason | Wait for |
|---|---|---|
| [category] | [trend broken / overvalued] | [what signal to look for] |

---

### Monthly SIP Plan
| Fund | SIP | Category | Mode |
|---|---|---|---|
| [Fund 1] | ₹X | Mid Cap | Regular SIP |
| [Fund 2] | ₹Y | Short Duration | Regular SIP |
| [Fund 3] | ₹Z | Large Cap | Aggressive SIP (2× for 3 months) |
| **Total** | **₹XYZ** | | |

---
Review your MF portfolio every 6 months with /mf-sell to exit underperformers and redeploy.
```
