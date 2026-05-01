# Mutual Fund Buy Recommendation

Identify the best mutual funds to invest in right now — based on portfolio gaps, market conditions, and goal alignment.

## What This Skill Does
- Fetches current MF holdings to identify gaps and over-concentration
- Recommends new funds to add OR top-up existing good funds
- Covers: Large Cap, Mid Cap, Small Cap, Flexi Cap, ELSS, Debt, International, Sectoral
- Gives specific fund names, suggested allocation %, and why each makes sense now

## Execution Steps

### Step 1 — Fetch current portfolio state
Use `networth_snapshot` for total portfolio value and asset allocation.
Use `networth_holdings` to see existing MF positions (names, invested amount, XIRR, category).
Use `networth_allocation_breakdown` to understand current equity/debt/gold split.

### Step 2 — Identify portfolio gaps

Check against ideal allocation for a balanced long-term portfolio:

| Category | Ideal Range | Action if Missing |
|---|---|---|
| Large Cap / Index Fund | 30–40% of MF | Add if under-represented |
| Mid Cap | 15–25% of MF | Add if missing |
| Small Cap | 10–15% of MF | Add if missing (only if horizon > 5 years) |
| Flexi Cap / Multi Cap | 15–20% of MF | Add for manager flexibility |
| Debt / Liquid | 10–15% of MF | Add for stability |
| International | 5–10% of MF | Add for global diversification |
| ELSS | Optional | Recommend if user needs tax saving |

Flag if any category is > 40% (over-concentrated).

### Step 3 — Fetch top funds in gap categories
Use `get_mf_by_category` to get top-rated funds in each missing/underweight category.
Use `get_mf_funds_details` for the top 3 candidates per gap category.

Evaluate each candidate on:
- 3-year and 5-year XIRR vs category average
- Expense ratio (direct plan preferred, < 1% for active, < 0.2% for index)
- AUM size (prefer > ₹5,000 Cr for stability; but mid/small cap can be smaller)
- Fund manager track record and tenure
- Consistency: did it outperform in both bull and bear phases?

### Step 4 — Market context overlay

Apply current market conditions (May 2026) to tilt recommendations:
- **RBI rate cut cycle underway** → Favour duration debt funds (gilt/long-term bond)
- **Mid/Small cap valuations stretched** → Be selective, prefer quality-focused funds
- **IT and pharma recovery** → Sector fund opportunity if user has appetite
- **Rupee stable** → International funds less risky now
- **Post-election stability** → Infrastructure/PSU theme funds have tailwind

### Step 5 — SIP vs Lump Sum guidance

For each recommended fund, specify:
- **SIP preferred:** If market at highs or valuations stretched (average the cost)
- **Lump Sum OK:** If market corrected > 10% from recent high or category is oversold
- **Suggested monthly SIP amount:** Based on portfolio size (typically 2–5% of monthly investable surplus per fund)

### Step 6 — Output

```
## Mutual Fund Buy Recommendations — [Date]

### Portfolio Gap Analysis
Current MF value: ₹X | Equity: Y% | Debt: Z% | International: W%
Missing: [categories]
Over-concentrated: [categories if any]

---

### NEW FUNDS TO ADD

#### 1. [Fund Name] — [Category]
- **Why now:** [market/portfolio reason]
- **3Y XIRR:** X% vs category avg Y%
- **Expense ratio:** Z% (Direct plan)
- **Suggested allocation:** ₹X lump sum OR ₹Y/month SIP
- **Mode:** SIP / Lump Sum / Both
- **Investment horizon:** Minimum N years

#### 2. [Fund Name] — [Category]
[same format]

#### 3. [Fund Name] — [Category]
[same format]

---

### EXISTING FUNDS TO TOP UP
[Fund Name already in portfolio]
- Current value: ₹X | XIRR: Y%
- Why top up: [performing well, underweight, category still has upside]
- Add: ₹X lump sum OR increase SIP by ₹Y/month

---

### FUNDS TO AVOID RIGHT NOW
[Category or specific fund type to skip]
- Reason: [valuation / risk / market timing]

---

### Suggested Monthly SIP Plan
| Fund | SIP Amount | Category |
|---|---|---|
| [Fund 1] | ₹X | Large Cap |
| [Fund 2] | ₹Y | Mid Cap |
| [Fund 3] | ₹Z | Debt |
| **Total** | **₹XYZ/month** | |
```

End with: "All fund recommendations are for long-term wealth creation. Review every 6 months using /mf-sell to weed out underperformers."
