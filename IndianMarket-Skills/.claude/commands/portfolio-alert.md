# Portfolio Alert — Urgent Sell Scanner

Run an automated scan of the portfolio and push a notification if any holding needs urgent action.

## Trigger Conditions (sends alert)

### Stocks — Alert if ANY of:
- Stock down > 5% today (single-day crash)
- Stock down > 15% from your average buy price AND analyst target below current price
- Stock at 52W low with no recovery signal (making new lows)
- Analyst consensus flipped to SELL majority (>60% sell)

### Mutual Funds — Alert if ANY of:
- Any debt fund NAV drops > 1% in a day (credit event signal)
- Equity fund XIRR goes negative over 1-year period

## Execution Steps

### Step 1 — Fetch holdings
Use `networth_holdings` to get all current stock and MF positions with P&L data.

### Step 2 — Fetch live stock details
Use `lookup_ind_keys` to resolve all stock names.
Use `get_indian_stocks_details` with `segments: ["analyst"]` for all stock holdings.

### Step 3 — Evaluate trigger conditions
For each stock holding check:
- `day_change_percentage` < -5 → URGENT
- Current price vs avg cost → if loss > 15% AND analyst upside < 0 → URGENT
- `52week_low` proximity → if current within 3% of 52W low → WARNING
- `sell_per` > 60 → URGENT

### Step 4 — Decide notification
If ANY urgent trigger fires:
  → Use PushNotification with message listing the affected stocks
  → Format: "SELL ALERT: [Stock] -X% today | [Stock2] at 52W low | Check portfolio now"

If only warnings (no urgent):
  → Use PushNotification with: "Portfolio check: [N] stocks need review. Open Claude to run /portfolio-redflags"

If all clear:
  → No notification. Just output "All clear at [time] — no urgent sell signals."

## Output in session
Always print a brief status line even when no notification is sent:
```
[HH:MM] Portfolio scan complete — X urgent, Y warnings, Z all clear
Urgent: [stock names if any]
Warnings: [stock names if any]
```
