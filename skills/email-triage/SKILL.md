---
description: "Triage inbox: categorize recent emails, surface action items, propose unsubscribes"
---

# Email Triage

Read-only inbox triage. Categorizes recent emails, surfaces action items with quoted deadlines, and proposes unsubscribe candidates. **Never modifies the inbox** — no archiving, labeling, sending, or marking as read.

## Prerequisites
- Gmail MCP server must be connected (tools: `search_emails` or `search_gmail_messages`, `list_emails`, `read_email` or `get_gmail_message_content`)
- If Gmail MCP is not available, notify the user and stop

## Input
$ARGUMENTS — optional time window (e.g., "today", "since yesterday", "last 3 days"). Default: last 24 hours.

## Policy
- **Read-only.** Do not call any tool that modifies the inbox (send, label, archive, delete, mark read, draft).
- **False negatives are worse than false positives.** When uncertain whether an email is important, categorize it higher, not lower. An important email missed is worse than junk surfaced.
- **Quote deadlines verbatim.** Any date, time, or deadline mentioned in a triage summary must include the exact text from the email in a `[quoted: "..."]` tag. Do not paraphrase or recompute dates.
- **No hallucinated content.** If you cannot read an email's body, say so. Do not summarize based on subject line alone.

## Instructions

### Step 1: Check for Triage Rules
Read `<project>/.workspace/email_triage_rules.md` if it exists. This file contains calibrated priority rules specific to the user. Apply these rules when categorizing. If the file does not exist, use general judgment and note that calibration has not been done yet.

### Step 2: Fetch Recent Emails
Use the Gmail MCP tools to list/search emails from the specified time window. Fetch enough metadata to categorize (sender, subject, date, snippet). For emails that look potentially important, fetch full content.

### Step 3: Categorize
Assign each email to exactly one category:

**ACTION REQUIRED**
- Needs a reply, decision, or task from the user
- Has a deadline or time-sensitive request
- From a person (not an automated system) expecting a response
- Include: sender, subject, deadline (verbatim-quoted), and a 1-line suggested next step

**FYI**
- Worth knowing about but no action needed
- Announcements, updates, reports the user would want to see
- Include: sender, subject, 1-line summary

**NOISE**
- Newsletters, marketing, automated notifications, social media alerts
- Anything the user has never acted on from this sender
- Include: sender, subject only (no summary needed)

### Step 4: Unsubscribe Candidates
From the NOISE category, identify senders that appear repeatedly (3+ times in recent history, or clearly mass-marketing). List them as unsubscribe candidates with:
- Sender name and email
- Frequency estimate (daily, weekly, etc.)
- Whether there's likely an unsubscribe link

Track these in `<project>/.workspace/email_unsubscribe_candidates.md` — append new candidates, don't duplicate existing ones. Create the file if it doesn't exist.

### Step 5: Present Briefing
Format as:

```
## Email Triage — <date> (<N> emails, <time window>)

### ACTION REQUIRED (<count>)
1. **<sender>** — <subject>
   Deadline: <quoted text> [quoted: "<exact text from email>"]
   → Suggested: <next step>

2. ...

### FYI (<count>)
1. **<sender>** — <subject>
   <1-line summary>

### NOISE (<count>)
<sender> — <subject>
<sender> — <subject>
...

### Unsubscribe Candidates
- <sender> (<frequency>) — <recommendation>
```

### Step 6: Offer Next Steps
After presenting the briefing, ask:
- "Want me to draft replies for any ACTION items?"
- "Want to flag any re-categorizations?" (for calibration learning)

If the user re-categorizes any emails, note the disagreement. After 50 cumulative disagreements have been recorded across sessions, suggest running a calibration pass to formalize rules.
