# Mutual Fund Sell Recommendation

Deep analysis of all mutual fund holdings — identify funds to exit, trim, or switch with specific reasons and alternatives.

## What This Skill Does
- Fetches all MF holdings from the portfolio
- Evaluates each fund on: XIRR vs benchmark, expense ratio, category fit, overlap, AUM trend
- Gives SELL / SWITCH / TRIM / HOLD verdict for each fund
- Suggests replacement fund when recommending a switch

## Execution Steps

### Step 1 — Fetch MF holdings
Use `networth_holdings` to get all mutual fund positions.
Also use `networth_allocation_breakdown` to understand MF allocation by category.

### Step 2 — For each fund, evaluate

**Performance Check:**
- XIRR < 8% over 3 years → underperforming even fixed deposit
- XIRR < category average → fund manager not adding value
- Consistent negative returns over 1 year → structural problem

**Cost Check:**
- Regular plan with >1.5% expense ratio for large cap → switch to direct
- Index fund with >0.5% expense ratio → switch to lower-cost alternative

**Overlap Check:**
- Multiple large cap / flexi cap funds in portfolio → likely 80%+ overlap
- Keeping overlapping funds dilutes returns without diversification benefit

**Category Fit Check:**
- Sectoral/thematic fund where the theme is over → exit
- Credit risk debt fund → exit (unless intentional)
- International fund with currency drag + underperformance → review

**AUM and Manager Check:**
- Fund with shrinking AUM over 2 years (institutional outflows signal)
- Fund manager change without performance continuity

### Step 3 — Verdicts

**SELL (Exit completely):**
- Multiple red flags present
- No recovery thesis

**SWITCH (Exit and move to better fund in same category):**
- Category is fine, but this specific fund underperforms peers
- Suggest specific replacement with better track record

**TRIM (Reduce to 30–40% of current allocation):**
- Good fund but over-concentrated
- Sectoral fund where partial booking makes sense

**HOLD (No action):**
- Performing well vs benchmark
- Meeting investment goal

### Step 4 — Output

```
## Mutual Fund Sell Report — [Date]

### SELL (Exit Completely)
[Fund Name]
- Invested: ₹X | Current: ₹Y | XIRR: Z%
- Why sell: [specific reason]
- Move proceeds to: [suggestion]

### SWITCH (Better alternative exists)
[Fund Name] → [Suggested Fund]
- Invested: ₹X | Current: ₹Y | XIRR: Z%
- Why switch: [underperformance / high cost / overlap]
- Suggested fund: [Name] — [why it's better]

### TRIM (Reduce position)
[Fund Name]
- Current allocation: X% of MF portfolio
- Recommended: Reduce to Y%
- Reason: [over-concentration or partial profit booking]

### HOLD (Keep as is)
[List with brief reason]

---
### Summary
Total MF invested: ₹X | Current value: ₹Y | Blended XIRR: Z%
Funds to exit/switch: N funds | Capital to redeploy: ₹Z
```
