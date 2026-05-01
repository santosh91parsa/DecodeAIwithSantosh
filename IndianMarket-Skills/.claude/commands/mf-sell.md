# Mutual Fund Sell Recommendation

Deep analysis of all mutual fund holdings using performance metrics, trend analysis of underlying indices, category overlap, expense ratios, and R:R of staying vs exiting.

## Execution Steps

### Step 1 — Fetch MF holdings
Use `networth_holdings` with asset_type "MF" for all fund positions.
Use `networth_allocation_breakdown` with asset_type "MF" and breakdown_by "assets" for category view.

### Step 2 — For each fund, evaluate across 5 dimensions

#### A. Performance vs Benchmark
- XIRR < 8% over 2+ years → underperforming even FD (serious red flag)
- XIRR < category average by > 3% → fund manager not adding value
- XIRR negative over 1 year → structural underperformance

#### B. Cost Check
- Large cap / Flexi cap active fund with ER > 1.5% → switch to direct or index
- Index fund with ER > 0.3% → cheaper alternatives exist
- Any fund still in Regular plan (not Direct) → switch to Direct immediately (saves 0.5-1% annually)

#### C. Multi-Timeframe Trend of Underlying Category
Apply the 3-Screen trend method to the fund's category:
- **Large Cap funds:** Check if Nifty 50 is above its 6-month average (weekly trend bullish)
- **Mid Cap funds:** Check if Nifty Midcap 150 trend — if weekly trend broken, reduce exposure
- **Small Cap funds:** Highest risk — check if category is in correction (lower highs for 3+ months)
- **Sectoral/Thematic funds:** Check the sector index trend:
  - Infrastructure: Nifty Infra index weekly trend
  - Technology: Nifty IT weekly trend
  - If sector index in downtrend (lower lows for 8+ weeks) → EXIT the sectoral fund
- **Gold/Silver funds:** Commodity trend — if 52W position < 30th percentile, hold; if >90th, reduce

#### D. Overlap and Concentration
- 2+ funds in same category (e.g., 3 flexi cap funds) → consolidate to 1 best performer
- Calculate overlap: if two funds hold similar top-10 stocks → duplication with no diversification benefit
- Too much in one category (>40% of MF in single category) → rebalance

#### E. R:R of Staying vs Exiting
For each underperforming fund, calculate the opportunity cost:
```
Cost of staying = Category average - Fund XIRR
Annual drag = invested_amount × (category_avg - fund_xirr) / 100
3-year drag = annual_drag × 3
```
If 3-year drag > ₹10,000 → switching fund is clearly worth it

#### F. AUM and Manager Stability
- Shrinking AUM over 6 months (institutional outflows) → investigate
- Recent fund manager change → monitor for 2 quarters before adding more; if existing, review
- NFO (New Fund Offer) fund with < 1 year track record → higher risk, watch closely

### Step 3 — Classify each fund

**SELL (Exit completely):**
- Multiple red flags (performance + cost + overlap)
- Category trend broken and no recovery catalyst
- Sectoral fund where sector thesis is over

**SWITCH (Exit → Move to better fund in same category):**
- Category is good, this specific fund underperforms peers
- Suggest specific replacement: better 3Y return, lower ER, stronger AUM trend

**TRIM (Reduce by 40-50%):**
- Good fund but over-concentrated (>25% of MF portfolio)
- Sectoral fund where theme has partially played out — lock partial profits

**MOVE TO BREAKEVEN STOP (Set mental exit rule):**
- For profitable funds that are pulling back: set a NAV level below which you'll exit
- Trailing approach: if NAV drops > 15% from recent high, exit

**HOLD (Keep as is):**
- Performing within 2% of category benchmark
- Serving a unique category not covered elsewhere

### Step 4 — Output

```
## Mutual Fund Sell Report — [Date]

### SELL (Exit Completely)
[Fund Name]
- Invested: ₹X | Current: ₹Y | XIRR: Z% | Category avg: W%
- 3-year opportunity cost: ₹X drag vs category
- Sector trend: [bullish / broken]
- Why sell: [specific reason]
- Move proceeds to: [suggestion + category]

### SWITCH (Better fund available)
[Fund Name] → [Suggested Replacement]
- Your XIRR: Z% | Replacement XIRR: W% | ER saved: X%
- Overlap with replacement: Low / Medium / High
- Why switch: [performance gap / cost / overlap]

### TRIM (Reduce position)
[Fund Name]
- Current: X% of MF portfolio | Recommended: Y%
- Reason: [over-concentration / partial theme play-out]
- Trailing NAV stop: ₹X (15% below recent NAV high)

### HOLD
[Fund list with brief reason each]

---
### Summary
Total MF invested: ₹X | Current: ₹Y | Blended XIRR: Z%
Funds to exit/switch: N | Capital to redeploy: ₹X
Best category to redeploy into: [gap category from portfolio analysis]
```
