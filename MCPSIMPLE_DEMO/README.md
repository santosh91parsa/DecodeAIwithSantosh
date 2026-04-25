# MCPSIMPLE DEMO — Give Claude Live Access to Your Linux Server

> **Decode AI with Santosh** — Full demo from the YouTube video:  
> *"I Gave Claude Access to My Live Linux Server Using MCP — Full Demo"*

---

## What This Is

A minimal Python MCP (Model Context Protocol) server that gives Claude.ai **live, real-time access** to your Linux server's health metrics — CPU, memory, and disk — without any copy-pasting.

**40 lines of code. Three tools. One decorator each.**

---

## Architecture

```
Claude.ai (cloud)
     |
     | HTTPS
     ↓
 ngrok tunnel  ←── free, one command, auto HTTPS
     |
     | HTTP
     ↓
 server.py (port 8000)  ←── FastMCP + psutil
     |
     ↓
 Linux kernel metrics (real data)
```

---

## Prerequisites

- Python 3.8+
- A Linux server (local or remote)
- A [Claude.ai](https://claude.ai) account (free or Pro)
- [ngrok](https://ngrok.com) free account (no credit card needed)

---

## Step-by-Step Demo Guide

### Step 1 — Clone the Repo

```bash
git clone https://github.com/santosh91parsa/DecodeAIwithSantosh.git
cd DecodeAIwithSantosh/MCPSIMPLE_DEMO
```

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install mcp psutil uvicorn
```

> ⚠️ Use `pip3` if your system defaults to Python 2.

---

### Step 3 — Run the MCP Server

```bash
python3 server.py
```

You should see output like:

```
INFO:     Started server process [12345]
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Keep this terminal open.

---

### Step 4 — Start the ngrok Tunnel

Open a **new terminal tab** (keep server.py running in the first one).

```bash
ngrok http 8000
```

You'll see a forwarding URL like:

```
Forwarding    https://goes-discover-tidbit.ngrok-free.dev -> http://localhost:8000
```

**Copy the `https://...ngrok-free.dev` URL** — you'll need it in the next step.

> 📝 Free ngrok URLs change every restart. For production, use a paid ngrok plan or a fixed domain.

---

### Step 5 — Connect to Claude.ai

1. Go to [claude.ai](https://claude.ai) in your browser
2. Click **Settings** (bottom-left)
3. Navigate to **Custom Connectors**
4. Click **+ Add Custom Integration**
5. Fill in:
   - **Name:** `server-health`
   - **URL:** your ngrok URL + `/sse`  
     Example: `https://goes-discover-tidbit.ngrok-free.dev/sse`
6. Click **Save**

---

### Step 6 — Enable the Connector in Chat

1. Start a **New Chat** in Claude.ai
2. Click the **+** button (bottom-left of chat input)
3. Go to **Connectors**
4. Enable **server-health**
5. You should see 3 tools listed:
   - `get_cpu`
   - `get_memory`
   - `get_disk`

---

### Step 7 — Run the Demo

Type this into Claude:

```
What is the current state of my server? Check CPU, memory and disk.
```

Watch the **tool call badges** appear — each one is a real HTTP request going from Anthropic's cloud, through ngrok, to your Python server running `psutil` on your machine.

Then ask:

```
Is anything looking concerning? Should I be worried about anything?
```

Claude will reason about the live data and give you a real infrastructure analysis.

---

## (Optional) Claude Desktop — Local Setup

If you want to run this **locally** without ngrok, use Claude Desktop instead of Claude.ai.

**Config file locations:**
- Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Edit the config file:

```json
{
  "mcpServers": {
    "server-health": {
      "command": "python3",
      "args": ["/absolute/path/to/MCPSIMPLE_DEMO/server.py"],
      "env": {}
    }
  }
}
```

Replace `/absolute/path/to/` with your actual path, then restart Claude Desktop.

---

## Files in This Folder

| File | Description |
|------|-------------|
| `server.py` | The MCP server — 40 lines, 3 tools |
| `requirements.txt` | Python dependencies |
| `claude_desktop_config.json` | Config template for Claude Desktop (local mode) |
| `README.md` | This guide |

---

## Common Issues & Fixes

### SSL error on curl test
Check your **server logs** first — if you see `200 OK`, the server is fine. This is often a local SSL client issue (old LibreSSL on Mac). The server itself is healthy.

### TypeError on MCP SDK
You may be on an older MCP SDK version with breaking API changes. This demo uses **FastMCP** which abstracts that instability. Make sure you're on `mcp>=1.27.0`.

### Claude.ai won't accept my URL
Claude.ai requires **HTTPS**. Plain `http://` URLs are rejected. This is why ngrok is necessary for remote servers.

### ngrok URL not working after restart
Free ngrok URLs change every restart. Copy the new URL from `ngrok http 8000` output and update your Claude.ai custom connector.

---

## What Each Tool Does

```python
@mcp.tool()
def get_cpu() -> str:
    """Returns current CPU usage percentage"""
    # Claude uses this docstring to decide WHEN to call this tool

@mcp.tool()
def get_memory() -> str:
    """Returns RAM usage percentage and GB used"""

@mcp.tool()
def get_disk() -> str:
    """Returns disk usage percentage for root filesystem"""
```

The `@mcp.tool()` decorator is all FastMCP needs. It reads your function name, docstring, and type hints — and builds the full MCP protocol automatically.

---

## About

**Santosh Parsa** — Linux and DevOps engineer, 13 years at ServiceNow. Learning AI in public.

📺 YouTube: [Decode AI with Santosh](https://youtube.com/@DecodeAIwithSantosh)  
💼 LinkedIn: [santosh91parsa](https://www.linkedin.com/in/santosh-parsa-1b615554/)  
🐙 GitHub: [santosh91parsa](https://github.com/santosh91parsa)

---

*Drop errors in the YouTube comments — I read and reply to all of them.*
