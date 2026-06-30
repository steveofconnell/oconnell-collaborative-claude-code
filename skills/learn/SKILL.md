---
description: "Extract durable principles from the current session's corrections/edits and write them into the right global config file"
---

# Learn — distill a principle from the session into global config

Turn what just happened in this session into a durable, generalized rule in the user's
global config. The user types `/learn <short topic>` (e.g. `/learn email and thread
response voice`, `/learn figure formatting`, `/learn how I like commit messages`). The
topic is a pointer, not the content — the content is mined from the session.

## Input
$ARGUMENTS — a short topic/description naming the area to generalize. May be vague; the
session is the evidence.

## Core idea
The richest signal is the **diff between what Claude produced and what the user changed it
to** — their edits, rewrites, rejections, restatements, and explicit "always/never"
statements in this session. `/learn` reads those, extracts the *transferable* principle
behind each (not the one-off situational fact), and files it where it will auto-load in
future sessions.

## Instructions

### Step 1: Gather evidence from the session
Scan the current conversation for everything relevant to the topic:
- **User edits to Claude's output** — every place the user rewrote, trimmed, softened,
  or reordered text Claude wrote. Reconstruct the before→after. If the user mentions
  "two rounds" (or more), mine *each* round; later rounds often sharpen earlier ones.
- **Explicit directives** — "always X," "never Y," "I prefer Z," "stop doing W."
- **Repeated corrections** — the same fix applied more than once is a strong signal.
- **Rejections** — approaches the user declined, and what they chose instead.
If there is no clear evidence in the session for the named topic, say so and ask the user
to point at the moment they mean, rather than inventing a principle.

### Step 2: Generalize (instance → principle)
For each signal, state the **durable principle** plus a concrete **before→after example**
from this session. Filter hard:
- Keep only what is **transferable** to future work. Drop one-off situational decisions.
- Prefer the *why* behind a fix over the surface fix.
- If several edits share a root, state the root once with the instances as examples.

### Step 3: Route to the right file
Pick the destination by kind. All global config lives in your cross-device sync folder
(the one `setup.sh` chose, symlinked into `~/.claude/`); write principles there, never to a
local-only `~/.claude/` path that doesn't resolve back to the sync folder.
- **Writing voice / prose / email / manuscript style** → `rules/academic-writing-voice.md`
- **Conversational / interaction style** (how Claude talks to the user) → `rules/interaction-style.md`
- **Code style, workflow, communication, standards, econometric judgment** (cross-project)
  → `CLAUDE.md`, under `## Learned Preferences`, in the right category header
- **Data integrity, script architecture, project structure, data pipeline, task
  management** → the matching `rules/*.md`
- **Project-specific** (only matters for one project) → that project's
  `.workspace/memory/` + a line in its `MEMORY.md` — NOT global config
If a principle could land in two files, put it in the most specific one and stop.

### Step 4: Dedup before writing
Read the target file's existing entries on the topic. If one already covers it, **update
that entry** rather than adding a duplicate. If the new principle contradicts an existing
one, do not silently overwrite — surface the conflict and ask which wins.

### Step 5: Format to the file's conventions
Match the destination's existing style exactly:
- In the rules files and `CLAUDE.md` Learned Preferences: a **dated bullet** (`(YYYY-MM-DD)`),
  present tense, with before→after examples in quotes. Use today's date — get it with
  `date +%F`, never guess.
- Where several principles share a topic, group them as one bullet with sub-numbered
  points `(1) … (2) …`, matching the file's existing grouped entries.
- Note provenance briefly ("distilled from the user's edits to X this session").

### Step 6: Apply and report
Write the entries, then report: what was added or updated, in which file, in one or two
lines each. If any candidate principle was **uncertain** — borderline situational, or you
weren't sure it generalizes — do not bake it in; list it separately and ask. The
invocation is consent to record the clear ones; reserve questions for the genuinely
ambiguous.

## Notes
- This skill operationalizes the **Preference Learning** protocol in `CLAUDE.md`. Honor its
  maintenance rules (check for existing coverage, update not duplicate, flag conflicts).
- Do not record what the repo already encodes (code structure, git history, an existing
  rule). If asked to "learn" something already covered, point at the existing entry.
- Give the user a one-line receipt, the same way the memory system does — they need to know
  the principle persisted and which file to point at later.
