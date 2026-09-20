# How This Code Works — A Complete Line-by-Line Guide
### AI Mail Intelligence — Decode AI with Santosh

> Everything explained in plain English. No prior Python or AI experience needed.

**Author**: Santosh Parsa  
**Script**: [`mail_intelligence.py`](file:///Users/santusahi/Desktop/forgeops/DecodeAIwithSantosh/mail-intelligence/mail_intelligence.py)

---

## Table of Contents

1. [The Big Picture — What Does This Script Do?](#1-the-big-picture)
2. [How Emails Are Stored on a Linux Server (Maildir)](#2-how-emails-are-stored-maildir)
3. [The 4-Step Pipeline](#3-the-4-step-pipeline)
4. [Every Function Explained](#4-every-function-explained)
5. [The Imports — What Each Tool Does](#5-the-imports)
6. [The EmailRecord Dataclass](#6-the-emailrecord-dataclass)
7. [Step 1: generate_sample_maildir() — Creating Test Data](#7-step-1-generate-sample-maildir)
8. [Step 2: extract_body() — Parsing Emails](#8-step-2-extract-body)
9. [Step 3: setup_llm_client() — Connecting to AI](#9-step-3-setup-llm-client)
10. [Step 4: classify_email() — Asking the AI](#10-step-4-classify-email)
11. [Step 5: route_email() — Moving Files](#11-step-5-route-email)
12. [Step 6: main() — The Orchestra Conductor](#12-step-6-main)
13. [The CLI Arguments (argparse)](#13-the-cli-arguments)
14. [Cost, Speed, and Privacy](#14-cost-speed-and-privacy)
15. [How to Write This From Scratch](#15-how-to-write-this-from-scratch)

---

## 1. The Big Picture

Imagine you are the head of customer support at a company. Every morning, 1,000 emails arrive. Someone needs to look at each one and sort it into 3 piles:

| Pile | What goes here | Action |
| :--- | :--- | :--- |
| **🗑️ Spam** | Scams, phishing, fake prizes | Move to Junk folder |
| **📢 Marketing** | Newsletters, promotions, webinars | Move to Marketing folder |
| **✅ Legitimate** | Real work emails, invoices, alerts | Keep in Inbox |

**Our script is that person.** It reads every email, asks an AI model to classify it, and moves it to the right folder — automatically.

```text
Postfix Mail Server
       │
       ▼
  Maildir (folder on disk)
  └── new/
       ├── email_001.eml
       ├── email_002.eml
       └── ...
       │
       ▼
  Python Script (mail_intelligence.py)
       │
       ├── 1. READ the .eml file
       ├── 2. PARSE sender, subject, body
       ├── 3. ASK AI: "Is this spam, marketing, or legit?"
       └── 4. MOVE the file to Junk/, Marketing/, or Inbox/
```

---

## 2. How Emails Are Stored (Maildir)

On a Linux server running **Postfix** (a popular mail server), emails are NOT stored in a database. They are stored as **individual files** inside a folder structure called **Maildir**:

```text
/home/user/Maildir/
├── new/          ← Unread emails land here (one file per email)
├── cur/          ← Emails that have been read
└── tmp/          ← Temporary files while email is being delivered
```

Each `.eml` file inside `new/` is a plain-text file that looks like this:

```text
From: winner@scam.com
To: santosh@example.com
Subject: Win a free iPhone!
Date: Sat, 20 Sep 2026 16:00:00 +0530

You have been selected to win a free iPhone 15!
Click here now to claim your prize before it expires.
```

This is the **RFC 2822** email format — a standard invented in 1982 that every email system on Earth still uses today.

**Why does this matter?**  
Because our script just needs to open these text files, read them, and extract the important parts. No database, no complex API — just files on disk.

---

## 3. The 4-Step Pipeline

Every AI batch-processing tool follows the same mental model. Memorize this:

```text
┌─────────────────────────────────────────────────────────────┐
│                    THE 4-STEP FORMULA                       │
│                                                             │
│  1. FIND    →  Locate email files in Maildir/new/           │
│  2. PARSE   →  Extract From, Subject, Body using `email`    │
│  3. CLASSIFY →  Send to LLM, get back JSON                  │
│  4. ACT     →  Move file to Junk/, Marketing/, or Inbox/    │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Every Function Explained

Here is a map of every function in the script and what it does:

| Function | Purpose | When it runs |
| :--- | :--- | :--- |
| `generate_sample_maildir()` | Creates 10 fake emails for testing | Only on first run (if no Maildir exists) |
| `extract_body()` | Pulls plain text from an email | Once per email |
| `setup_llm_client()` | Connects to OpenAI or Ollama | Once at startup |
| `classify_email()` | Sends email to AI, gets back JSON | Once per email |
| `route_email()` | Moves the file to the right folder | Once per email |
| `main()` | Orchestrates everything above | Entry point |

---

## 5. The Imports

```python
import os          # Read environment variables, check if files/folders exist
import sys         # Exit the script with error codes
import json        # Convert AI responses (text) into Python dictionaries
import time        # Measure how long the pipeline takes
import email       # Python's built-in email parser (reads .eml files)
import mailbox     # Python's Maildir reader (we use it for structure reference)
import argparse    # Parse command-line flags like --maildir and --dry-run
import shutil      # Move files from one folder to another
from dataclasses import dataclass, asdict  # Create structured data containers
from email.policy import default           # Modern email parsing policy
from openai import OpenAI                  # Talk to LLMs (OpenAI or Ollama)
```

> [!TIP]
> Every import here except `openai` is part of **Python's standard library** — pre-installed, zero cost, no `pip install` needed. The only external dependency is the `openai` package.

---

## 6. The EmailRecord Dataclass

```python
@dataclass
class EmailRecord:
    id: str                    # Filename (e.g., "msg_0.eml")
    sender: str                # Who sent it (From header)
    recipient: str             # Who received it (To header)
    subject: str               # Subject line
    date: str                  # When it was sent
    body_snippet: str          # First ~1500 characters of the email body
    classification: str = ""   # "spam", "marketing", or "legitimate" (filled later)
    reason: str = ""           # AI's explanation (filled later)
    original_path: str = ""    # Full file path on disk (for moving the file)
```

### What is a `@dataclass`?

Think of it as a **pre-printed form**. Instead of using a messy dictionary like:
```python
email_data = {"id": "msg_0.eml", "sender": "...", "subject": "...", ...}
```

A dataclass gives you a **clean, named container** with autocomplete support:
```python
record = EmailRecord(id="msg_0.eml", sender="boss@company.com", ...)
print(record.sender)  # "boss@company.com"
```

The `asdict()` function converts it back into a dictionary when we need to save to JSON.

---

## 7. Step 1: `generate_sample_maildir()`

**Purpose:** If you don't have a real Maildir (most people testing this don't), the script creates one with 10 realistic sample emails.

```python
def generate_sample_maildir(maildir_path: str):
    # Create the 3 standard Maildir folders
    for subdir in ['new', 'cur', 'tmp']:
        os.makedirs(os.path.join(maildir_path, subdir), exist_ok=True)
```

**What's happening:**
1. Creates the standard Maildir directory structure (`new/`, `cur/`, `tmp/`).
2. Defines 10 sample emails spanning 4 categories:
   - **3 Spam:** Fake prizes, investment scams, phishing
   - **3 Marketing:** Sales promotions, newsletters, webinar invites
   - **3 Legitimate:** Team meetings, invoices, code review requests
   - **1 System Alert:** Disk space warning
3. Writes each email as a properly formatted `.eml` file inside `new/`.

```python
msg = email.message.EmailMessage()    # Create a blank email
msg['Subject'] = subject              # Set the subject line
msg['From'] = sender                  # Set the sender
msg['To'] = "santosh@example.com"     # Set the recipient
msg.set_content(body)                 # Set the body text

filepath = os.path.join(maildir_path, 'new', f'msg_{i}.eml')
with open(filepath, 'w') as f:
    f.write(msg.as_string())          # Save as a proper .eml file
```

---

## 8. Step 2: `extract_body()`

**Purpose:** Emails can be simple (plain text) or complex (HTML + attachments + images). This function safely extracts just the plain text body.

```python
def extract_body(msg) -> str:
    body = ""
    if msg.is_multipart():
        # Email has multiple parts (text + HTML + attachments)
        for part in msg.walk():              # Walk through every part
            if part.get_content_type() == "text/plain":  # Only grab plain text
                if "attachment" not in str(part.get("Content-Disposition")):
                    body += part.get_payload(decode=True).decode()
    else:
        # Simple single-part email
        body = msg.get_payload(decode=True).decode()
    
    return body[:1500].strip()   # ← KEY: Only keep first 1500 characters
```

### Why only 1500 characters?

1. **Cost:** LLMs charge per token. Sending a 10,000-character email costs ~7x more than 1,500 chars.
2. **Speed:** Shorter inputs = faster responses.
3. **Accuracy:** The important information (intent, sender, subject) is almost always in the first few paragraphs.
4. **Token limits:** Models have maximum context windows. Keeping inputs small leaves room for more emails.

### What is `msg.is_multipart()`?

Modern emails are like **Russian nesting dolls**. A single email can contain:
- A plain text version
- An HTML version (with formatting)
- Attached files (PDFs, images)
- Inline images

`is_multipart()` returns `True` if the email has multiple nested parts. We use `msg.walk()` to iterate through all of them and grab only the `text/plain` part.

---

## 9. Step 3: `setup_llm_client()`

**Purpose:** Automatically detect whether to use paid OpenAI or free local Ollama.

```python
def setup_llm_client(model_override: str):
    api_key = os.environ.get("OPENAI_API_KEY")   # Check environment variable
    
    if api_key:
        # Paid cloud mode
        client = OpenAI(api_key=api_key)
        model = model_override or "gpt-4o-mini"
        is_openai = True
    else:
        # Free local mode (Ollama running on your machine)
        client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
        model = model_override or "llama3.2:1b"
        is_openai = False
        
    return client, model, is_openai
```

### The Ollama Trick

Ollama speaks the same "language" (API format) as OpenAI. So we just point the OpenAI client to `localhost:11434` instead of `api.openai.com`. The rest of the code doesn't need to change at all!

```text
OpenAI Mode:    Your Code  ──internet──>  api.openai.com  (costs money)
Ollama Mode:    Your Code  ──localhost──>  your own laptop  (free forever)
```

---

## 10. Step 4: `classify_email()`

**Purpose:** The core AI step. Sends email context to the LLM and parses the JSON response.

### The Prompt

```python
prompt = f"""
You are an intelligent email classification assistant.
Analyze the following email and classify it into EXACTLY ONE of these three categories:
1. spam
2. marketing
3. legitimate

Email Details:
From: {email_record.sender}
Subject: {email_record.subject}
Body: {email_record.body_snippet}

Respond in the following JSON format ONLY:
{{
  "category": "<spam|marketing|legitimate>",
  "reason": "<short 1-sentence reason>"
}}
"""
```

### What makes this prompt effective?

| Technique | Why it works |
| :--- | :--- |
| **"EXACTLY ONE of these three"** | Prevents the AI from inventing new categories |
| **Providing From + Subject + Body** | Gives the AI the same context a human would use |
| **"Respond in JSON format ONLY"** | Prevents conversational filler like "Sure! Here is..." |
| **`response_format={"type": "json_object"}`** | Hard constraint — forces valid JSON output |
| **`temperature=0.0`** | Makes the AI deterministic (same input = same output every time) |

### The Safety Net

```python
category = result_json.get("category", "legitimate").lower()
if category not in ["spam", "marketing", "legitimate"]:
    category = "legitimate"  # Default to safe choice
```

If the AI returns an unexpected value, we default to `"legitimate"` — better to keep a marketing email in your inbox than accidentally junk a real one.

### Error Handling

```python
except Exception as e:
    print(f"Error classifying email {email_record.id}: {e}")
    return "legitimate", "Error during classification, defaulted to legitimate."
```

If the AI call fails (network error, model timeout, etc.), the email stays in Inbox. **Never lose a potentially important email.**

---

## 11. Step 5: `route_email()`

**Purpose:** Physically moves the `.eml` file from the Maildir into the classified folder.

```python
folder_mapping = {
    "spam": "Junk",         # spam emails → Junk/new/
    "marketing": "Marketing",  # marketing → Marketing/new/
    "legitimate": "Inbox"      # real emails → Inbox/new/
}
```

The function:
1. Looks up the classification in the mapping dictionary.
2. Creates the target folder if it doesn't exist (e.g., `Junk/new/`).
3. Uses `shutil.move()` to physically move the file.

### The `--dry-run` Flag

```python
if dry_run:
    return  # Don't move anything, just classify and print
```

When testing, you don't want to actually move files around. `--dry-run` lets you see what the AI *would* do without touching any files.

---

## 12. Step 6: `main()` — The Orchestra Conductor

This is where everything comes together. Here's the flow:

```text
main()
  │
  ├── 1. Parse CLI arguments (--maildir, --dry-run, --model)
  │
  ├── 2. If Maildir doesn't exist → generate_sample_maildir()
  │
  ├── 3. setup_llm_client() → Get AI client ready
  │
  ├── 4. Start timer
  │
  ├── 5. List all files in Maildir/new/
  │
  ├── 6. FOR EACH email file:
  │       ├── Open and parse with email.message_from_binary_file()
  │       ├── Create EmailRecord with extracted fields
  │       ├── classify_email() → Get category + reason
  │       ├── route_email() → Move file to target folder
  │       └── Print result
  │
  ├── 7. Stop timer, calculate cost
  │
  ├── 8. Save all results to classification_results.json
  │
  └── 9. Print summary report
```

### The Email Parsing Line

```python
with open(filepath, 'rb') as f:
    msg = email.message_from_binary_file(f, policy=default)
```

- **`'rb'`** = Read Binary mode. Emails can contain non-ASCII characters (international text, encoded attachments), so we read raw bytes.
- **`email.message_from_binary_file()`** = Python's built-in parser that understands the RFC 2822 email format.
- **`policy=default`** = Use Python's modern email handling policy (proper Unicode support).

### The Summary Report

```python
print(f"Total Emails Processed : {total_emails}")
print(f"Processing Time        : {duration:.2f} seconds")
print(f"Avg Time Per Email     : {duration/total_emails:.2f} seconds")

if is_openai:
    print(f"Estimated API Cost     : ${estimated_cost:.6f}")
```

The cost estimate uses a rough formula:
- ~300 tokens per email
- OpenAI's `gpt-4o-mini` pricing: ~\$0.30 per million tokens (blended)
- 1,000 emails × 300 tokens × \$0.30/1M ≈ **\$0.09**

---

## 13. The CLI Arguments

The script uses `argparse` to accept command-line options:

```bash
# Use defaults (sample_maildir, classify only, auto-detect model)
python mail_intelligence.py

# Point to a real Postfix Maildir
python mail_intelligence.py --maildir /home/user/Maildir

# Classify without moving files (safe testing)
python mail_intelligence.py --dry-run

# Override the model
python mail_intelligence.py --model llama3.2:3b

# Combine flags
python mail_intelligence.py --maildir /home/user/Maildir --dry-run --model gpt-4o
```

---

## 14. Cost, Speed, and Privacy

| Metric | OpenAI Cloud (`gpt-4o-mini`) | Free Local (`llama3.2:1b`) |
| :--- | :--- | :--- |
| **Cost per 1,000 emails** | ~\$0.09 | \$0.00 |
| **Speed** | ~0.5 sec/email | ~1-2 sec/email (depends on Mac/GPU) |
| **Privacy** | Emails sent to OpenAI servers | 100% local, nothing leaves your machine |
| **Accuracy** | Higher (larger model) | Good but may miss subtle cases |
| **Internet required** | Yes | No |

---

## 15. How to Write This From Scratch

If you had to write this entire script from memory (interview, hackathon, weekend project), here is the skeleton:

### Phase 1: Write `main()` as a checklist (30 seconds)
```python
def main():
    # 1. Find email files
    # 2. For each file, parse it
    # 3. Send to AI for classification
    # 4. Move file to the right folder
    # 5. Print summary

if __name__ == "__main__":
    main()
```

### Phase 2: Add the helper functions above `main()` (5 minutes)
```python
def extract_body(msg):     pass  # Pull text from email
def classify_email(...):   pass  # Ask AI, return JSON
def route_email(...):      pass  # Move file to folder
```

### Phase 3: Fill in each function one at a time (15 minutes)

### The I-H-M-S Rule
*(Mnemonic: **I** **H**ave **M**y **S**cript)*

```text
1. [I]mports        → import json, email, argparse, openai
2. [H]elpers        → extract_body(), classify_email(), route_email()
3. [M]ain           → def main(): ... the orchestration
4. [S]tart button   → if __name__ == "__main__": main()
```

---

## Quick Reference Card

```text
┌──────────────────────────────────────────────────────────────┐
│  AI MAIL INTELLIGENCE — QUICK REFERENCE                     │
│                                                              │
│  Run:        python mail_intelligence.py                     │
│  Test:       python mail_intelligence.py --dry-run           │
│  Real:       python mail_intelligence.py --maildir /path     │
│                                                              │
│  Pipeline:   Maildir → Parse → LLM → Route                  │
│  Output:     classification_results.json                     │
│                                                              │
│  OpenAI:     export OPENAI_API_KEY="sk-..."                  │
│  Ollama:     just run the script (auto-detects)              │
│                                                              │
│  Cost:       $0.09 per 1,000 emails (OpenAI)                 │
│              $0.00 forever (Ollama)                           │
└──────────────────────────────────────────────────────────────┘
```
