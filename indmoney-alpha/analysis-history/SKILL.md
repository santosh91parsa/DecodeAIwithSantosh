---
name: analysis-history
description: |
  Reads all saved analysis snapshots from .claude/analysis-history/, fetches current live
  prices from INDmoney, and compares every past verdict/target/stop against today's reality.
  Classifies each prediction as HIT / MISS / STOPPED / IN_PROGRESS, diagnoses the cause of
  misses (news event, macro shift, technical over-extension, timing), and recommends the best
  current action for each divergence. Also detects systematic patterns (over-selling,
  over-buying, timing issues) and suggests calibration adjustments. Tracks overall accuracy
  by category: SELL NOW, BUY, Quick Trade, Penny BUY.

  Use when the user asks: "analysis history", "how accurate were predictions", "check past
  analysis", "what was wrong last time", "compare predictions", "prediction accuracy",
  "did my sells work", "review past recommendations", "what should I do about missed calls",
  "track analysis", "prediction vs actual", "how did market-intel do".

  Requires INDmoney MCP + analysis history files saved by /market-intel. Uses:
  networth_holdings (current prices), get_indian_stocks_details (analyst), WebSearch (macro
  context for miss diagnosis). Total: 3 rounds.
---

# Analysis History — Prediction vs Actual Tracker

## Execution — 3 Round Trips

**Round 1:**
Read all files in `.claude/analysis-history/` (skip README.md). Parse each `YYYY-MM-DD.md`:
- Extract: run_date, all stocks with ind_key/price/verdict/stop/target/fib_78/rr
- Extract: Nifty50 and Midcap150 verdict/target
- Extract: penny stocks, quick trades, MF actions
- Build a list of all unique ind_keys across all files

`ToolSearch query="select:mcp__indmoney__get_indian_stocks_details,mcp__indmoney__networth_holdings" max_results=2`

**Round 2 (all parallel):**
- `networth_holdings` asset_type "IND_STOCK" — current prices
- `get_indian_stocks_details` batch: all unique ind_keys from history, segments ["analyst"]
- WebSearch: `"India Nifty stock market news [current month year]"` — macro context for diagnosis

**Round 3 (conditional):**
- `get_indian_stocks_ohlc` interval "1week" lookback "1y" — ONLY for stocks classified as MISS
  where price diverged > 15% from prediction direction
- Skip if no significant misses

---

## Comparison Logic

For each stock in each history file:

```
days_since = today - run_date

✅ HIT_TARGET:  (verdict=SELL_NOW/TRIM AND current < price_then × 0.90)
                OR (verdict=BUY/TRAIL AND current >= saved_target)
✅ CORRECT_STOP: verdict had stop AND current < stop (correctly warned to exit)
⏳ IN_PROGRESS: price moved in predicted direction, target not yet reached,
                days_since < 28 (for portfolio) or < 21 (for quick trades)
❌ MISS_REVERSAL: verdict=SELL_NOW AND current > fib_61_then (price recovered above support)
                  OR verdict=BUY AND current < price_then × 0.85 without stop trigger
❌ MISS_TIMING: Quick Trade verdict, direction correct, but days_since > 21 and target not hit
🛑 STOPPED_OUT: current < saved_stop AND verdict was BUY/TRAIL/HEALTHY
⚠️  STALE: days_since > 28 — analysis too old, re-run needed
```

### Miss Diagnosis

For each ❌ MISS, determine category:

**A — News Event:**
Signal: price moved >10% in a single week after analysis date
Diagnosis: Earnings surprise / SEBI action / promoter event not in original analysis
Best action: run `/stock-research [stock]` for fresh verdict

**B — Macro Shift:**
Signal: Nifty moved >8% opposite to predicted verdict since analysis date
Diagnosis: Global event (tariffs/rate decision) changed market direction
Best action: recalibrate — re-run `/market-intel` with current data

**C — Technical Bounce from fib_78:**
Signal: SELL_NOW called, price dropped to fib_78 but bounced back above fib_61
Diagnosis: Strong support at 78.6% — classic reversal zone, oversold bounce
Best action: re-classify as SPECULATIVE BUY with stop exactly at fib_78; R:R usually improves here

**D — Timing (trade still valid):**
Signal: Price moving in right direction but slowly; trend intact on weekly
Diagnosis: Correct call, patience needed
Best action: extend horizon 2 more weeks, set time stop (exit if flat)

**E — Analysis Wrong (exit now):**
Signal: Analyst upgrades after SELL call with no fundamental change, OR new negative structural trend
Diagnosis: Thesis was incorrect
Best action: exit the position at current price, do not average

---

## Best Action Matrix

| Outcome | Original Verdict | Current | Best Action |
|---|---|---|---|
| MISS_REVERSAL | SELL_NOW | Recovered > fib_61 | Re-evaluate; if news cleared → HOLD with new trail stop at fib_38 |
| MISS_REVERSAL | SELL_NOW | Recovered but < fib_38 | Partial exit: sell 50%, hold 50% with stop at fib_61 |
| MISS_REVERSAL | BUY | Dropped, no stop hit | Check news; if thesis intact → average at fib_61 (max 1% add) |
| MISS_TIMING | QUICK_TRADE | Direction right, slow | Hold 2 more weeks max; then exit regardless |
| STOPPED_OUT | Any BUY | Below stop | Exit immediately if not already done |
| IN_PROGRESS | SELL_NOW | Still declining | Hold sell; trail the stop down with each lower high |
| IN_PROGRESS | BUY/TRAIL | Rising toward target | Hold; trail stop up to each new swing low |
| HIT_TARGET | BUY | At or above target | Book 50%; trail remaining with fib_38 stop |
| STALE | Any | > 4 weeks old | Re-run /market-intel — levels stale, new fib levels needed |

---

## Accuracy Scoring

```
accuracy_rate = hits ÷ (hits + misses + stopped) × 100

Per category:
  sell_accuracy  = correct_sells ÷ total_sell_calls × 100
  buy_accuracy   = correct_buys ÷ total_buy_calls × 100
  trade_accuracy = trades_hit_T1 ÷ total_trade_calls × 100
  penny_accuracy = penny_buys_hit ÷ total_penny_buys × 100
```

### Pattern Detection

- sell_accuracy < 50% → threshold too aggressive; suggest raising to fib_78 + R:R < 1.5:1 only
- buy_accuracy < 50% → news layer missing events; suggest adding promoter holding check
- trade_accuracy < 40% → entry zone too loose; tighten to fib_38–fib_50 only
- 3+ misses in same week → macro event not captured; check if news round fired

---

## Output Format

```
## Analysis History — [Date]
Files: X | Verdicts tracked: Y | Accuracy: Z%

### ACCURACY SUMMARY
| Category | Calls | Hits | Misses | Stopped | Accuracy |
| SELL NOW | | | | | |
| BUY/TRAIL | | | | | |
| Quick Trade | | | | | |
| Penny BUY | | | | | |

### ✅ HITS
| Date | Stock | Verdict | Price Then | Price Now | Outcome |

### ❌ MISSES — Action Required
| Date | Stock | Verdict | Price Then | Price Now | Cause | Best Action |
(one sentence diagnosis per miss)

### ⏳ IN PROGRESS
| Date | Stock | Verdict | Entry | Now | Target | % to Target |

### 🛑 STOPPED OUT
| Date | Stock | Stop | Current | Action Needed |

### ⚠️ STALE (re-run /market-intel)
[comma-separated stock names from analyses > 4 weeks old]

### MISS PATTERNS
[bullet points on systematic issues found]
Calibration suggestion: [one line]

### PORTFOLIO IMPACT
Capital at risk in active misses: ₹X | Profits protected by hits: ₹X
```
