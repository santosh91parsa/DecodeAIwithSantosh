# AI Mail Intelligence

An AI-powered layer on top of existing email infrastructure that triages, drafts, and routes messages using Claude.

## Problem

High-volume inboxes (support, sales, ops) create bottlenecks — humans spend time on repetitive triage, drafting standard replies, and routing to the right owner.

## What This Does

- **Triage** — classifies incoming mail by intent, urgency, and topic using an LLM
- **Draft** — generates context-aware reply drafts grounded in your knowledge base or CRM
- **Route** — assigns threads to the right team or workflow based on classification
- **Summarize** — condenses long threads into a one-paragraph brief before human review

## Architecture

```
Incoming Mail (IMAP/SMTP or webhook)
        │
        ▼
   Ingestion Layer
   (parse headers, body, attachments)
        │
        ▼
   Claude API (claude-sonnet-4-6)
   ├── classify intent + urgency
   ├── extract entities (sender, product, issue)
   └── generate draft reply or routing decision
        │
        ▼
   Action Dispatcher
   ├── push draft to Gmail/Outlook compose
   ├── create ticket in ServiceNow / Jira
   └── post summary to Slack channel
```

## Tech Stack

- **LLM**: Claude (Anthropic) — `claude-sonnet-4-6` for drafts, `claude-haiku-4-5` for fast triage
- **Email access**: Gmail API / Microsoft Graph API (OAuth 2.0) or generic IMAP
- **Orchestration**: Python with `anthropic` SDK; optionally Claude Code MCP for local dev
- **Storage**: Postgres for thread state; S3/GCS for attachment blobs

## Key Files (planned)

```
ai-mail-intelligence/
├── README.md           ← this file
├── ingest/
│   └── imap_reader.py  # connects to mailbox, yields raw messages
├── classify/
│   └── triage.py       # sends to Claude, returns intent + urgency label
├── draft/
│   └── reply_gen.py    # generates draft replies with system prompt + context
├── dispatch/
│   └── router.py       # routes to ticket system, Slack, or human queue
└── config/
    └── prompts.yaml    # system prompts for each task
```

## Example Triage Prompt

```yaml
system: |
  You are a mail triage assistant. Classify the email below.
  Return JSON with:
    intent: one of [support, sales, billing, spam, internal, other]
    urgency: one of [critical, high, normal, low]
    summary: one sentence
    suggested_owner: team name or "human-review"
```

## Status

Concept / early design phase. No production deployment yet.

## References

- [Anthropic Claude API docs](https://docs.anthropic.com)
- [Gmail API](https://developers.google.com/gmail/api)
- [Microsoft Graph Mail API](https://learn.microsoft.com/en-us/graph/api/resources/mail-api-overview)
