---
description: "Finalize session: write handoff document, update memory"
---

# Session Close

Finalize the current session. Follow these steps:

## Step 1: Check if Substantive Work Was Done
If only startup checks ran and no tasks were actioned, skip the handoff and memory updates. Just acknowledge the close.

## Step 2: Write Handoff Document
Create `HANDOFF_<YYYY-MM-DD>.txt` in `<project>/.s-workspace/` with:

```
HANDOFF — <date>

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

## Step 3: Append to Persistent Session Log
Append a summary entry to `<project>/.s-workspace/SESSION_LOG.md`. This is a running, reverse-chronological log across all sessions. Create the file if it doesn't exist.

Format for each entry:
```
---
## <YYYY-MM-DD>
**Tasks:** <1-line summary of what was done>
**Files:** <comma-separated list of files created or modified>
**Next:** <1-line next step>
```

Insert the new entry at the top of the file (after any header line). Keep existing entries intact — this log only grows.

## Step 4: Update Memory
- Update `<project>/MEMORY.md` if any new memory-worthy information was learned.
- Create or update individual memory files in `<project>/.s-workspace/memory/` as needed.
- Memory files go in the **project directory**, never in `~/.claude/projects/`.

## Step 5: Confirm
Print a brief summary of what was saved and where.
