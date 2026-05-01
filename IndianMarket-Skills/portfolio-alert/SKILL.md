---
name: portfolio-alert
description: |
  Automated real-time portfolio scanner that detects urgent sell signals and sends push
  notifications. Checks for Fibonacci breakdowns (61.8% and 78.6% retracement breaches),
  single-day crashes (>5%), volume spikes on down-moves (institutional exit signal), trailing
  stop hits on profitable holdings, and analyst target breaches using INDmoney live data.

  Use when the user asks: "portfolio alert", "alert me if something drops", "monitor my portfolio",
  "notify me of red flags", "set up sell alerts", "watch my stocks", "automated portfolio check",
  "scan portfolio for urgent sells", "portfolio notification", or any request to actively monitor
  holdings and get notified when action is needed.

  Requires INDmoney MCP server connected. Uses: networth_holdings (IND_STOCK), lookup_ind_keys,
  get_indian_stocks_details (analyst segment). Sends desktop push notifications via PushNotification
  tool when urgent triggers fire. Can be scheduled with CronCreate for automatic daily scans.
---

# Portfolio Alert — Automated Urgent Sell Scanner

Real-time portfolio scan with technical triggers: Fibonacci breakdown, RSI extremes, MA-based trailing stop hits, volume spikes, and intraday crash detection.

## Alert Trigger Conditions

### URGENT Triggers (send push notification immediately)
1. `day_change_percentage < -5` — single-day crash
2. Price within 3% of 52W low (breakdown risk) → `(current - 52W_low) / 52W_low < 0.03`
3. Fibonacci 78.6% breakdown: `current_price < 52W_high - (52W_high - 52W_low) × 0.786`
4. Analyst sell% > 60% OR current price > analyst HIGH target (overvalued trap)
5. Volume spike on a down-move: day_change < -3% AND volume > 2× normal (institutional exit signal)

### WARNING Triggers (send notification if 2+ warnings)
6. `day_change_percentage < -3` AND stock already in loss (compounding damage)
7. Price between Fib 61.8%–78.6% (last strong support zone — approaching danger)
8. Profitable position down > 8% from recent high → trailing stop check
   ```
   Approx trail: 52W_high - (52W_high - 52W_low) × 0.15
   Flag if current_price < trail_level AND pnl_per > 20
   ```
9. Analyst upside < 5% (stock has reached target — exit before reversal)

### MF Alert Triggers
10. Any equity MF with XIRR turning negative in portfolio data
11. Gold/Silver MF drop > 2% in a day (commodity event)

## Execution Steps

### Step 1 — Fetch holdings
Use `networth_holdings` for IND_STOCK to get current positions with P&L.

### Step 2 — Fetch live details
Use `lookup_ind_keys` to resolve all stock names.
Use `get_indian_stocks_details` with `segments: ["analyst"]` for all holdings (batches of 10).

### Step 3 — Evaluate all triggers
For each stock holding, check ALL triggers above.
Classify each as: URGENT / WARNING / CLEAR

### Step 4 — Fibonacci levels (quick calc)
For any stock with day_change < -2%, compute:
```
fib_61 = 52W_high - (52W_high - 52W_low) × 0.618
fib_78 = 52W_high - (52W_high - 52W_low) × 0.786
```
Flag as WARNING if current < fib_61
Flag as URGENT if current < fib_78

### Step 5 — Trailing stop check for winners
For holdings with pnl_per > 20% (profitable positions):
```
Weekly ATR approx = (52W_high - 52W_low) ÷ 52
Trail level = recent_high - ATR_weekly × 2.0
```
If current_price < trail_level → flag as WARNING (consider locking in profits)

### Step 6 — Notify

**If ANY URGENT trigger:**
Use PushNotification with status "proactive":
`"SELL ALERT: [Stock A] Fib breakdown ₹X | [Stock B] -6% crash | Open Claude now"`

**If 2+ WARNINGS but no URGENT:**
Use PushNotification with status "proactive":
`"Portfolio warning: [N] stocks at key support levels. Run /portfolio-redflags"`

**If 1 WARNING:**
No notification — print summary in session only.

**If ALL CLEAR:**
No notification. Print: `"[HH:MM] Scan complete — all clear. No urgent signals."`

### Step 7 — Session Output
Always print regardless of notification:
```
[HH:MM] Portfolio Alert Scan — [Date]
URGENT (X): [stock names + trigger]
WARNING (Y): [stock names + trigger]
CLEAR  (Z): [count] stocks healthy

Fib levels breached: [list]
Trailing stops hit: [list]
```

## Scheduling Automated Scans
To run this automatically at market open and pre-close, ask Claude:
"Schedule portfolio alerts at 9:15 AM and 2:45 PM on weekdays"

Claude will create cron jobs using CronCreate. Jobs are session-only by default (active while Claude Code is open) and auto-expire after 7 days.
