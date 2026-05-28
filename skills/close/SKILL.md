---
description: "Finalize session: write handoff document, update memory"
---

# Session Close

Finalize the current session. Follow these steps:

## Step 1: Check if Substantive Work Was Done
If only startup checks ran and no tasks were actioned, skip the handoff and memory updates. Just acknowledge the close.

## Step 2: Reconcile TODO.md Against Session Work
Read `<project>/.workspace/TODO.md` and sweep it against everything that happened in this session. This step exists because close sessions have historically failed to update TODO.md, causing completed or dropped tasks to resurface as pending in future sessions.

For each pending `- [ ]` item in TODO.md, assess its current status based on the full session context:

1. **Completed** — work was done this session that satisfies the task. Move it to `## Completed` with today's date (`done YYYY-MM-DD`). Do not ask for confirmation; if the session clearly resolved it, mark it done.

2. **Dropped** — a decision was made this session (explicit or implicit) to not pursue this task. Delete it from the file entirely. No "cancelled" status — if it's not worth doing, it's not worth tracking.

3. **Reformulated** — the task was redefined, scoped differently, or renamed during the session. Update the description in-place. If the reformulation is significant, add a note as an indented sub-bullet.

4. **Still pending** — no change. Leave as-is.

Also scan the session for any new tasks that surfaced (things decided to do later, follow-ups noted, items that emerged from work done) that are not yet in TODO.md. Add them under `## Pending` with today's date.

After updating TODO.md, report the changes: how many items were marked done, dropped, reformulated, and added.

## Step 3: Write Handoff Document
Create `HANDOFF_<YYYY-MM-DD>.txt` in `<project>/.workspace/handoffs/` with:

```
HANDOFF — <date>
Author: <name of the person who ran this session>

## What Was Done
<Numbered list of what was accomplished this session>

## Files Created This Session
<Every file created — scripts, data outputs, figures, intermediate files, configs, everything>

## Files Modified This Session
<Every file modified>

## Next Steps
<What should happen next session — specific, actionable>
```

**Completeness requirement:** Every file created or modified during the session MUST be listed. Omitting outputs breaks cross-session continuity. If unsure, err on the side of including too much.

**Next Steps consistency:** The "Next Steps" section must be consistent with the pending items now in `.workspace/TODO.md` (after the reconciliation in Step 2). Do not list items as next steps that were just marked done or dropped.

**Author identification:** The `Author:` line must identify who ran the session. Pull this from the user's global `~/.claude/CLAUDE.md` if it states their name, or from the project's `CLAUDE.md` collaborator list. If neither is available, ask the user once and cache the answer in project memory.

## Step 4: Append to Persistent Session Log
Append a summary entry to `<project>/.workspace/SESSION_LOG.md`. This is a running, reverse-chronological log across all sessions. Create the file if it doesn't exist.

Format for each entry:
```
---
## <YYYY-MM-DD> (<author name>)
**Tasks:** <1-line summary of what was done>
**Files:** <comma-separated list of files created or modified>
**Next:** <1-line next step>
```

Insert the new entry at the top of the file (after any header line). Keep existing entries intact — this log only grows.

## Step 5: Update Memory
- Update `<project>/MEMORY.md` if any new memory-worthy information was learned.
- Create or update individual memory files in `<project>/.workspace/memory/` as needed.
- Memory files go in the **project directory**, never in `~/.claude/projects/`.

## Step 6: Confirm
Print a brief summary of what was saved and where.

---

# Intermediate Handoffs

Not every handoff is a session close. After a sustained block of work (roughly 30+ minutes or several completed tasks), write an **intermediate handoff** — same format as above, but:

- Use a letter suffix on the filename: `HANDOFF_<YYYY-MM-DD>b.txt`, `HANDOFF_<YYYY-MM-DD>c.txt`, etc.
- Do NOT run memory updates or the session log — those happen at final close only.

The purpose is continuity insurance: if the session ends unexpectedly (context limit, crash, user walks away), there is a recent record of what happened. It also helps the user — or a coauthor — pick up mid-stream if they open the project while work is in progress.

**Intermediate handoffs are written at the user's discretion.** Claude may suggest one after a sustained block of work ("Want me to write an intermediate handoff for this chunk?"), but never writes one without being asked. The user decides when a checkpoint is warranted.
