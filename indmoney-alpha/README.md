# indmoney-alpha — AI-Powered Market Analysis Skills for INDmoney

6 AI-powered slash commands for Indian stock market analysis, portfolio management, and mutual fund recommendations — powered by your live INDmoney portfolio data via MCP.

---

## What Are These Skills?

[Claude Code Skills](https://docs.anthropic.com/en/docs/claude-code/skills) are slash commands that teach Claude how to perform specialized tasks. These skills connect to your real INDmoney account and give you:

- Live portfolio red flag detection with Fibonacci breakdown alerts
- Quick trade setups with multi-timeframe analysis and R:R validation
- Penny stock verdicts with RSI divergence and ATR-based stops
- Mutual fund buy/sell recommendations with category trend analysis
- Automated push notifications when urgent sell signals fire

**Powered by:** INDmoney MCP server (live market data, your portfolio, analyst forecasts)

**Analysis frameworks from:** [nse-trading-skills](https://github.com/Bhala-Srinivash/nse-trading-skills) — multi-timeframe analysis, Fibonacci levels, RSI divergence, position sizing, stop-loss strategies, trailing stops, risk-reward ratio

---

## Skills Included

| Command | What It Does |
|---|---|
| `/quick-trade` | Top 3 stock trade setups — confluence scoring, Fibonacci entry zones, ATR stops, R:R ≥ 2:1 |
| `/penny-stocks` | BUY / SPECULATIVE / AVOID verdicts on <₹100 stocks with RSI divergence and 3:1 R:R filter |
| `/portfolio-redflags` | Full portfolio scan — Fibonacci breakdown triggers, trailing stop checks, probabilistic scenarios |
| `/portfolio-alert` | Automated scanner with push notifications for crashes, Fib breakdowns, volume spikes |
| `/mf-sell` | SELL / SWITCH / TRIM / HOLD for each fund with 3-year opportunity cost and NAV trailing stops |
| `/mf-buy` | Fund recommendations with Fibonacci entry timing (lump sum vs SIP), category trend analysis |

---

## Prerequisites

### 1. Claude Code
Install Claude Code CLI:
```bash
npm install -g @anthropic/claude-code
```
Or download the [Claude Code desktop app](https://claude.ai/download).

### 2. INDmoney MCP Server

The INDmoney MCP server provides live access to:
- Your portfolio holdings (stocks, mutual funds, P&L, XIRR)
- Live stock prices, 52-week ranges, analyst targets
- Historical OHLC candle data for technical analysis
- Mutual fund NAV, returns, category rankings

#### Step 1 — Add the MCP server to Claude Code

Run this command in your terminal:

```bash
claude mcp add indmoney --transport http https://mcp.indmoney.com/mcp
```

#### Step 2 — Authenticate with your INDmoney account

Start Claude Code in your project directory:
```bash
claude
```

Then type:
```
indmoney connect
```

Claude will open a browser window. Log in with your INDmoney credentials (mobile number + OTP). After login, you'll be redirected to a `localhost` callback URL — paste that full URL back into Claude Code to complete authentication.

**Example callback URL:**
```
http://localhost:59330/callback?code=ABC123&state=XYZ789
```

#### Step 3 — Verify connection

```bash
claude mcp list
```

You should see:
```
indmoney: https://mcp.indmoney.com/mcp (HTTP) - ✓ Connected
```

---

## Installing the Skills

### Option 1 — npx skills add (easiest)
Uses the [skills.sh](https://skills.sh) standard — installs all 6 skills in one command:

```bash
npx skills add santosh91parsa/DecodeAIwithSantosh/indmoney-alpha
```

This automatically copies all SKILL.md files into your project's `.claude/skills/` directory.

### Option 2 — Global install (available in every session)
Skills available in every Claude Code session from any directory:

```bash
# Clone this repo
git clone https://github.com/santosh91parsa/DecodeAIwithSantosh.git

# Copy skills to global Claude commands directory
mkdir -p ~/.claude/commands
cp DecodeAIwithSantosh/indmoney-alpha/.claude/commands/*.md ~/.claude/commands/
```

### Option 3 — Project-level install
Skills available only when Claude Code is opened from this specific folder:

```bash
git clone https://github.com/santosh91parsa/DecodeAIwithSantosh.git

mkdir -p your-project/.claude/commands
cp DecodeAIwithSantosh/indmoney-alpha/.claude/commands/*.md your-project/.claude/commands/
```

### Option 4 — Install individual skills only

```bash
# Example: only install quick-trade and portfolio-alert
mkdir -p ~/.claude/commands
cp DecodeAIwithSantosh/indmoney-alpha/.claude/commands/quick-trade.md ~/.claude/commands/
cp DecodeAIwithSantosh/indmoney-alpha/.claude/commands/portfolio-alert.md ~/.claude/commands/
```

> **Note:** Restart Claude Code after copying skills for them to be picked up.

---

## Usage

Once installed and INDmoney is connected, just type the command in Claude Code:

```
/quick-trade
```
```
/penny-stocks
```
```
/portfolio-redflags
```
```
/portfolio-alert
```
```
/mf-sell
```
```
/mf-buy
```

### Example session

```
You: /portfolio-redflags

Claude: Fetching your portfolio...
[Scans all holdings, checks Fibonacci levels, RSI, analyst data]

## Portfolio Red Flag Report — 1 May 2026

### SELL NOW
| Stock       | P&L    | Flag                          | R:R  |
|-------------|--------|-------------------------------|------|
| Adani Power | +80.7% | 25% above analyst target      | 0.3:1|
| Protean eGov| -61.7% | Below Fib 78.6%, near 52W low | —    |

### REVIEW
| Stock      | P&L    | Concern                        |
|------------|--------|--------------------------------|
| Tata Steel | +61.5% | Only ₹4 to analyst target      |
| ITC        | -23.5% | 37% BUY, 20% SELL, weak setup  |
...
```

---

## How the Analysis Works

Each skill combines INDmoney live data with institutional-grade trading frameworks:

```
INDmoney MCP              NSE Trading Frameworks
─────────────             ──────────────────────
Live price & volume   →   Volume analysis
52W high / low        →   Fibonacci entry zones (38.2%, 61.8%, 78.6%)
Weekly OHLC candles   →   Multi-timeframe trend (3-screen method)
Daily OHLC candles    →   RSI divergence detection
Analyst targets       →   Risk-Reward ratio validation (≥ 2:1)
Your P&L & cost       →   Position sizing & trailing stop plans
MF holdings & XIRR   →   Category trend + opportunity cost
```

---

## Setting Up Automated Alerts

The `/portfolio-alert` skill supports scheduled scanning with push notifications.

In Claude Code, set up daily market-hours scans:

```
Ask Claude: "Set up daily portfolio alerts at 9:15 AM and 2:45 PM on weekdays"
```

Claude will create cron jobs that:
1. Scan your portfolio at those times
2. Check Fibonacci breakdowns, crashes, volume spikes
3. Send a push notification to your desktop (and phone if Remote Control is active) only when urgent action is needed

---

## Data Privacy

- **No credentials stored in skill files** — the `.md` files contain only instructions, no tokens or passwords
- **Authentication token** is stored securely by Claude Code in `~/.claude/` on your machine
- **All data flows directly** between Claude Code and INDmoney's servers — nothing passes through third parties

---

## Disclaimer

These skills are for educational and analytical purposes. They do not constitute financial advice. Always do your own research before making investment decisions. Trading and investing involve risk of loss.

---

## Contributing

PRs welcome! Ideas for new skills:
- `/options-analysis` — F&O chain analysis using INDmoney options data
- `/tax-harvesting` — Identify loss positions to harvest for tax offset
- `/sector-rotation` — Sector momentum scanner across Nifty indices
- `/sip-optimizer` — Optimize monthly SIP amounts across funds

## License

MIT
