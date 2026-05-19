# Decode Claude Commands — A Plain-English Guide

> A learner-friendly walkthrough of slash commands in Claude Code. If the official reference feels like a wall of tables, start here.

**Author**: Santosh Parsa
**Audience**: Developers new to Claude Code who want to understand *what* slash commands are, *why* they exist, and *how* to start using them in under 15 minutes.

**Compatible with**: Claude Code v2.1.143 (May 2026).

---

## 1. What Is a Slash Command?

A **slash command** is a shortcut you type in Claude Code that starts with `/`. It tells Claude to do a specific job — clear the chat, run a code review, deploy your app, anything you can script.

```
/help          → show built-in help
/clear         → wipe the conversation
/commit        → create a git commit
```

Think of slash commands like CLI flags for your AI pair-programmer. Instead of writing a paragraph telling Claude what to do, you type a short command.

---

## 2. The Four Flavors of Slash Commands

There are exactly **four** sources a `/command` can come from. Knowing which is which saves a lot of confusion.

| Flavor | Who creates it | Example | Where it lives |
|--------|----------------|---------|----------------|
| **Built-in** | Anthropic | `/help`, `/clear`, `/model` | Shipped with Claude Code |
| **Skill** | You or your team | `/optimize`, `/deploy` | `.claude/skills/<name>/SKILL.md` |
| **Plugin** | A plugin author | `/frontend-design:frontend-design` | Installed plugin package |
| **MCP prompt** | An MCP server | `/mcp__github__list_prs` | External MCP server |

> **Mental model**: Built-ins are the standard library. Skills are your local scripts. Plugins are npm packages. MCP prompts are remote APIs.

---

## 3. The Top 10 Built-in Commands You'll Actually Use

Out of the 60+ built-in commands, these are the ones you'll reach for daily:

| Command | What it does | When to use |
|---------|--------------|-------------|
| `/help` | Lists every available command | When you're lost |
| `/clear` | Wipes conversation history | Starting a fresh task |
| `/model` | Switches between Opus / Sonnet / Haiku | Need more or less horsepower |
| `/context` | Shows how much context window is used | Before a long task |
| `/compact` | Compresses the conversation | Hitting context limits |
| `/diff` | Visual diff of uncommitted changes | Before committing |
| `/rewind` | Undo recent edits AND conversation | "Wait, that broke things" |
| `/resume` | Reopen a previous session | Continue yesterday's work |
| `/goal <text>` | Tell Claude what "done" looks like | Multi-turn objectives |
| `/cost` | See how much you've spent | End-of-day check |

> **Pro tip**: Just type `/` and start typing letters to filter — you don't need to memorize names.

---

## 4. Your First Custom Command (Skill) — In 60 Seconds

Let's say you want a `/standup` command that summarizes what you worked on yesterday.

**Step 1.** Make the directory:
```bash
mkdir -p .claude/skills/standup
```

**Step 2.** Create `SKILL.md`:
```markdown
---
name: standup
description: Generate a stand-up summary from yesterday's git activity
---

Run `git log --since=yesterday --author="$(git config user.name)" --oneline`
and turn the output into 3 bullet points for my morning stand-up.
```

**Step 3.** Use it:
```
/standup
```

That's it. No build step, no install. The file *is* the command.

---

## 5. Anatomy of a Skill File

```yaml
---
name: my-command           # becomes /my-command
description: What it does  # helps Claude know when to auto-invoke
argument-hint: [pr-number] # tab-completion hint
allowed-tools: Bash(git *) # which tools it can use without asking
disable-model-invocation: false  # if true, only YOU can trigger it
---

# Free-form markdown instructions for Claude go below the frontmatter.

Use $ARGUMENTS to receive everything the user typed after the command.
Use $0, $1, $2 to grab individual words.

Use !`shell command` to inject live shell output.
Use @path/to/file to inject a file's contents.
```

### The Three Most Useful Frontmatter Fields

1. **`description`** — Claude reads this to decide whether to auto-trigger your skill. Be specific: *"Use when reviewing PRs for SQL injection"* beats *"reviews code"*.
2. **`allowed-tools`** — Pre-approves tool use so the command runs without permission prompts. Example: `Bash(npm test), Read, Grep`.
3. **`disable-model-invocation`** — Set to `true` for destructive commands (deploys, deletes) so Claude can't run them on its own initiative.

---

## 6. Skills vs. Legacy Commands — What Changed?

In older versions of Claude Code, custom commands lived in `.claude/commands/<name>.md` as single files. They still work. But **skills** are now the recommended path because they add:

| Feature | Legacy command | Skill |
|---------|---------------|-------|
| Single `.md` file | Yes | Yes |
| Bundle scripts, templates, assets | No | Yes (directory form) |
| Auto-invocation by Claude | No | Yes |
| Run in isolated subagent | No | Yes (`context: fork`) |
| Skill-scoped hooks | No | Yes |

If a skill and a legacy command share the same name, **the skill wins**.

---

## 7. Plugins — Skills as a Package

A plugin is a bundle of skills, subagents, hooks, and configuration that someone else has built and you can install. You invoke a plugin command like:

```
/plugin-name:command-name
```

Or, when there's no naming conflict, just:
```
/command-name
```

Use plugins when you find a complete workflow (e.g., a "frontend-design" plugin that ships a designer subagent, a `/frontend-design` command, and a pre-commit hook) instead of cobbling pieces together yourself.

---

## 8. MCP Prompts — Commands From External Services

When you connect an MCP (Model Context Protocol) server — say, GitHub or Jira — that server can expose prompts as slash commands. They follow a strict naming pattern:

```
/mcp__<server-name>__<prompt-name> [arguments]
```

Real examples:
```bash
/mcp__github__list_prs
/mcp__github__pr_review 456
/mcp__jira__create_issue "Login button broken" high
```

> The double-underscore separators (`__`) aren't a typo — they're required.

---

## 9. Common Gotchas

| Gotcha | Fix |
|--------|-----|
| `/mycommand` says "not found" | Check `name:` in frontmatter matches filename; restart Claude Code |
| Claude keeps asking for permission when I run my skill | Add `allowed-tools` in frontmatter |
| Claude runs my deploy command without asking | Add `disable-model-invocation: true` |
| Both a skill and a command exist — which runs? | The **skill** wins |
| My `$ARGUMENTS` is empty | You typed `/cmd` without args, or used `$0` when you meant `$ARGUMENTS` |
| `` !`git status` `` shows up as literal text | You need backticks, not quotes, and the leading `!` |

---

## 10. A Real-World Workflow

Here's how slash commands stitch together a typical PR workflow:

```
/clear                          # fresh context
/goal Finish the auth refactor and get tests green
[work, work, work]
/diff                           # eyeball the changes
/simplify                       # bundled skill: review for code quality
/security-review                # built-in: check for vulns
/commit                         # custom skill: commit with context
/ultrareview                    # cloud-based multi-agent review
/cost                           # how much did that cost me?
```

Each command does one job. Together they form a pipeline.

---

## 11. Where to Go Next

- **Full slash-command reference**: see the parent `readme.md` for the exhaustive built-in command list and frontmatter spec.
- **Skills deep dive**: `../03-skills/` in the Claude How To guide series.
- **Plugins**: `../07-plugins/`.
- **Hooks** (event-driven automation): `../06-hooks/`.
- **Official docs**: <https://code.claude.com/docs/en/slash-commands>

---

## Cheat Sheet — Print This

```
┌─────────────────────────────────────────────────────────────┐
│  TYPING /              shows command picker                 │
│  /help                 list everything                      │
│  /clear  /reset  /new  start fresh                          │
│  /model                switch model                         │
│  /context              context-window usage                 │
│  /compact              compress conversation                │
│  /diff                 visual diff                          │
│  /rewind  /undo        undo                                 │
│  /resume               re-open old session                  │
│  /cost  /stats         usage dashboards                     │
│                                                             │
│  CUSTOM:                                                    │
│  .claude/skills/<name>/SKILL.md  → /name                    │
│  .claude/commands/<name>.md      → /name (legacy)           │
│                                                             │
│  PLUGINS:    /plugin-name:command                           │
│  MCP:        /mcp__server__prompt                           │
└─────────────────────────────────────────────────────────────┘
```

---

*Written by **Santosh Parsa** for the **Decode AI with Santosh** series. Last updated 2026-05-19 for Claude Code v2.1.143.*
