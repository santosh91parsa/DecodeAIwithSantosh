---
name: mf-sell
description: |
  Deep analysis of all mutual fund holdings from INDmoney with SELL / SWITCH / TRIM / HOLD
  verdicts. Evaluates each fund on XIRR vs benchmark, category trend (3-screen method applied
  to underlying index), expense ratio, 3-year opportunity cost drag, AUM trend, overlap with
  other funds, and trailing NAV stop for profitable funds. Suggests specific replacement funds
  when recommending a switch.

  Use when the user asks: "which mutual fund to sell", "mf sell recommendation", "underperforming
  funds", "should I exit this fund", "mutual fund review", "which SIP to stop", "mf red flags",
  "consolidate my mutual funds", "mutual fund portfolio cleanup", "exit mutual fund",
  "switch mutual fund", or any question about exiting or replacing existing fund holdings.

  Requires INDmoney MCP server connected. Uses: networth_holdings (MF asset type),
  networth_allocation_breakdown (MF by assets), get_mf_by_category, get_mf_funds_details.
---

# Mutual Fund Sell Recommendation

Deep analysis of all mutual fund holdings using performance metrics, trend analysis of underlying indices, category overlap, expense ratios, and R:R of staying vs exiting.

## Execution Steps

### Step 1 — Fetch MF holdings
Use `networth_holdings` with asset_type "MF" for all fund positions.
Use `networth_allocation_breakdown` with asset_type "MF" and breakdown_by "assets" for category view.

### Step 2 — Evaluate each fund across 5 dimensions

#### A. Performance vs Benchmark
- XIRR < 8% over 2+ years → underperforming even FD (serious red flag)
- XIRR < category average by > 3% → fund manager not adding value
- XIRR negative over 1 year → structural underperformance

#### B. Cost Check
- Large cap / Flexi cap active fund with ER > 1.5% → switch to direct or index
- Index fund with ER > 0.3% → cheaper alternatives exist
- Any fund still in Regular plan (not Direct) → switch to Direct immediately (saves 0.5-1% annually)

#### C. Multi-Timeframe Trend of Underlying Category (3-Screen Method)
- **Large Cap funds:** Check if Nifty 50 weekly trend is bullish (higher highs/lows over 6 months)
- **Mid Cap funds:** Check if Nifty Midcap 150 trend — if weekly trend broken, reduce exposure
- **Small Cap funds:** If category in correction (lower highs for 3+ months) — caution
- **Sectoral/Thematic funds:** Check the sector index weekly trend
  - If sector index making lower lows for 8+ weeks → EXIT the sectoral fund
- **Gold/Silver funds:** If 52W position < 30th percentile, hold; if >90th percentile, reduce

#### D. Overlap and Concentration
- 2+ funds in same category (e.g., 3 flexi cap funds) → consolidate to 1 best performer
- Too much in one category (>40% of MF) → rebalance
- High overlap between two funds' top holdings → duplication with no diversification benefit

#### E. R:R of Staying vs Exiting (Opportunity Cost)
```
Annual drag = invested_amount × (category_avg_xirr - fund_xirr) / 100
3-year drag = annual_drag × 3
```
If 3-year drag > ₹10,000 → switching is clearly worth it

#### F. AUM and Manager Stability
- Shrinking AUM over 6 months → investigate (institutional outflows signal)
- Recent fund manager change → monitor for 2 quarters
- NFO (< 1 year track record) → higher risk, watch closely

### Step 3 — Classify each fund

**SELL (Exit completely):**
- Multiple red flags (performance + cost + overlap)
- Category trend broken with no recovery catalyst
- Sectoral fund where sector thesis is over

**SWITCH (Exit → Move to better fund in same category):**
- Category is good, this specific fund underperforms peers
- Suggest specific replacement with better 3Y return and lower ER

**TRIM (Reduce by 40-50%):**
- Good fund but over-concentrated (>25% of MF portfolio)
- Sectoral fund where theme has partially played out — lock partial profits

**MOVE TO TRAILING NAV STOP:**
- For profitable funds pulling back: set a NAV level below which you'll exit
- If NAV drops > 15% from recent high, exit next month

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
- Why switch: [performance gap / cost / overlap]

### TRIM (Reduce position)
[Fund Name]
- Current: X% of MF portfolio | Recommended: Y%
- Trailing NAV stop: ₹X (15% below recent NAV high)

### HOLD
[Fund list with brief reason each]

---
Total MF invested: ₹X | Current: ₹Y | Blended XIRR: Z%
Funds to exit/switch: N | Capital to redeploy: ₹X
Best category to redeploy: [gap from portfolio analysis]
```
