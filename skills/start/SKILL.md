---
description: "Full session startup: handoff check, integrity acknowledgment, pending TODOs, project-specific startup"
---

# Session Startup

Work through these in order, then ask what to work on. Read only what the briefing
actually uses — this skill runs at the top of every session, so anything read here
is paid for on every session in every project.

## Step 1: Config check (report from context, do not go looking)

The global config, the project `CLAUDE.md`, and every always-on rule are already in
context by the time this skill runs. Say so in one line and name anything that looks
wrong (a rule that should have loaded and did not, a contradiction between two
files). Do **not** issue Read or Glob calls to confirm files exist — that costs
permission prompts and confirms something already visible.

Path-scoped rules (those with `paths:` frontmatter — the language, data and
manuscript rules) correctly do **not** load at startup. Their absence is not a fault
and does not need reporting.

## Step 2: Academic integrity acknowledgment

Print, verbatim:

> Academic integrity directives loaded — all written content will be held to
> peer-review standards for originality, citation accuracy, and intellectual rigor.

## Step 3: Handoffs

Skip this step entirely for projects whose `CLAUDE.md` says they do not use handoffs
(a general-purpose admin workspace is a typical example).

Otherwise, list `<project>/.workspace/handoffs/HANDOFF_*.txt` by filename descending
and read **three**, extending further back only if the user authored none of the
three most recent — in that case read back to and including their most recent one,
capped at ~10.

Summarize each in two or three lines, most recent first, and **always name the
author**. Flag prominently any handoff written by someone else.

Then apply `rules/collaborator-handoff-acknowledgment.md`:
- **As recipient** — read every handoff addressed to you that lacks a `READ BY` stamp,
  regardless of age, act on it, and append the stamp.
- **As author** — raise any handoff you wrote that still lacks the recipient's stamp
  as "not yet read by <name> — still pending delivery."

## Step 4: Memory index

Read `<project>/MEMORY.md`. It is an index: one line per memory, and it should stay
that way — if entries have grown into paragraphs, say so and offer to compress it.

Scan for **feedback-type entries that modify session behavior** (mentioning "session",
"startup", "each session", "open with"). Follow those links and read the full files
**before composing any startup output** — they are directives that change this
sequence, not background reading. Execute them.

Do not read other memory files at startup. They load on demand when their topic
comes up.

## Step 5: AI use policy

Check for `aipolicy.txt` in the project root.

**If it exists:** do not print it. Confirm in one line — the policy is on file, its
`Last modified` date, and who has signed the AGREED section. Read the body only if
the session is about to do something the policy bears on (touching human-subjects
data, adding a new tool, an IRB or DUA question) or if the user asks.

**If it does not exist:** copy `aipolicy_default.txt` from your config folder's
`templates/` directory to the project root as `aipolicy.txt`, replacing
`[Project Name]` with the project directory name, `[DATE]` with today's date, and
`[Model family]` with the current model. Leave the `AGREED` entries as placeholders.
(If you have no such template yet, say so and skip this step rather than inventing
a policy.) Then print:

> Created default aipolicy.txt — review and customize for this project. Add your name
> to the AGREED section, and have coauthors and RAs sign before they use AI tools on
> this project.

## Step 6: Pending TODOs

`.workspace/TODO.md` is the single source of within-project tasks. Never pull tasks
from handoffs, memory, or email.

**Read the `## Pending` section only.** These files carry a permanent completed
archive and per-item detail that the briefing does not use, so reading the whole file
wastes a large amount of context every session. Use a targeted read or a Grep for the
`## Pending` / `## Deferred` / `## Completed` boundaries rather than reading top to
bottom.

Surface **all** pending items, including ones assigned to someone else, showing any
`**assigned:**` tag inline so the split between your plate and delegated work is
visible. Honor the `## Deferred` convention: items there stay out of the briefing
until their `surface:` date, at which point move them into `## Pending`.

Order by actionability per `rules/task-management.md` — unblocked first, blocked
after, with each blocker named inline.

## Step 7: Project-specific startup

Follow any additional startup directives in the project's `CLAUDE.md` (for example, a
project might fetch an external to-do list or run `/email-triage`). If a step depends
on an MCP server that is not connected, skip it silently unless the project says
otherwise.

## Step 8: Ready

Ask what to work on. Lead with anything time-sensitive from the TODO and, where
relevant, the handoff.
