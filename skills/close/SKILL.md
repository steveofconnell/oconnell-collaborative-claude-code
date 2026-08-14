---
description: "Finalize session: write handoff document, update memory"
---

# Session Close

Finalize the current session. Follow these steps:

## Step 1: Check if Substantive Work Was Done
If only startup checks ran and no tasks were actioned, skip the handoff and memory updates. Just acknowledge the close.

## Step 2: Reconcile TODO.md Against Session Work
Read `<project>/.workspace/TODO.md` and reconcile it against what actually happened. The most common close-time failure is a task that got **done quickly mid-session and never marked** — by the time you reach close it is no longer salient in the transcript, so a memory-based pass misses it. Therefore: **do NOT reconcile from recollection of the conversation. Reconcile from evidence** — the files, ledgers, and artifacts that now exist — in TWO passes.

### Pass A — reverse (work → items): the pass that catches the misses
First build the list of every file you created or modified this session (the same list Step 3's handoff needs — build it now). For EACH artifact ask: "which pending TODO item does this satisfy or advance?" If an artifact completes an item, that item is **Done even if it never came up again after the work was finished**. This pass exists specifically to catch fast tasks that were completed and abandoned. Fold in non-file outcomes too (a decision reached, an external action taken, a question definitively answered).

### Pass B — forward (item → evidence): verify, don't recall
For each pending `- [ ]` item, do not ask "did we discuss this?" — ask **"does its deliverable exist now?"** Check the actual evidence: is the named output file present, is the ledger row/table updated, does the script produce the cited value? Inspect it if cheap. An item is Done when its artifact exists, regardless of whether it was mentioned at close. If an item names no concrete deliverable, judge from the session but say so.

### Classify each pending item (cite the evidence)
1. **Completed** — evidence shows the task is satisfied. Move it to `## Completed` with `done YYYY-MM-DD`, and **cite the proving artifact** (file path / ledger row / output) in the note. Do not ask for confirmation. Never mark done without pointing to what proves it.
2. **Dropped** — a decision (explicit or implicit) was made not to pursue it. Delete it entirely. No "cancelled" status.
3. **Reformulated** — redefined / rescoped / renamed this session. Update in-place; add a sub-bullet if the change is significant.
4. **Still pending** — no change. Confirm this by *absence of evidence*, not by absence of discussion.

### New tasks
Scan the session for tasks that surfaced (follow-ups, deferred work, items born from work done) not yet in TODO.md. Add them under `## Pending` with today's date. Where possible give each a **`Done when:` sub-bullet naming the concrete artifact** that will prove completion — this makes the next close's sweep a mechanical check instead of a judgment call.

### Report
Report the reconciliation: N done (each with its cited evidence), N dropped, N reformulated, N added. **If Pass A surfaced any item that was done-but-unmarked, call it out explicitly** — that is the exact failure mode this step targets, and naming it confirms the sweep worked.

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
