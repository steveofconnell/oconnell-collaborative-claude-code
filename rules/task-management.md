# Task Management and Dependency Tracking

Applies to: all task lists, TODO files, handoff next-steps sections, and any enumeration of pending work items — across all projects.

## Project TODO file

Every project has a single `.workspace/TODO.md`. This is the canonical source of within-project tasks. Not handoff documents, not memory files, not scattered individual `TODO_*.md` files — one file per project.

### Format

```markdown
# TODO

## Pending

- [ ] Task description — added YYYY-MM-DD
  - **Done when:** [the concrete, checkable artifact that will exist or be true when this is complete]
  - Optional context, blockers, or notes as indented sub-bullets
- [ ] Another task — added YYYY-MM-DD — blocked on: [specific dependency]

## Completed

- [x] Finished task — added YYYY-MM-DD, done YYYY-MM-DD
```

Rules:
- One line per task. Sub-bullets for context only.
- Every task gets an `added` date.
- **Every task carries a `Done when:` sub-bullet** naming the concrete, checkable artifact that proves completion — a file at a path, a ledger row updated, a value produced, a document sent, a state reached. This turns "is it done?" from a memory judgment into a mechanical check: the reconciliation sweep (and any human) verifies the artifact exists rather than recalling whether the work happened. If a task genuinely has no external artifact (a pure decision or conversation), state the observable outcome instead. Skip only for throwaway one-liners.
- Blocked tasks state their blocker inline (see dependency rules below).
- Completed tasks move to `## Completed` with a `done` date.

### Lifecycle

**Adding tasks:**
- When a to-do surfaces during a session (user states it, or it's a clear next step from work just done), write it to `.workspace/TODO.md` immediately. Do not defer to handoffs, memory, or conversation notes.
- Give each new task its `Done when:` acceptance criterion **at creation** (see Format), not at close. Naming the completion artifact when you write the task is what makes later reconciliation a check instead of a guess.
- If `.workspace/TODO.md` doesn't exist yet, create it (and `.workspace/` if needed).

**Completing tasks:**
- When the user says something is done (explicitly or by completing the work), update `.workspace/TODO.md` right then — move the item to `## Completed` with the done date. Do not wait for session close.
- **Same-action rule (the primary defense).** The tool call (or batch) that produces a task's deliverable and the edit that checks its box are ONE action, not two. Do not move on to the next task until the finished one's box is checked. This exists because the recurring failure is a task done quickly, attention moving to the next thing, and the box never ticked — the fix is to catch completion at the moment it happens, not to reconstruct it at close. Close-time reconciliation (below) is a backstop, not the primary mechanism. A `Done when:` artifact that now exists is the signal to check the box.

**Dropping tasks:**
- If the user says to drop or cancel a task, delete it from the file entirely. No "cancelled" status — if it's not worth doing, it's not worth tracking.

**Startup:**
- Read `.workspace/TODO.md` and surface pending items as part of the startup briefing.
- Do NOT pull tasks from handoff "Next Steps" sections, memory files, or email. `.workspace/TODO.md` is the only source.
- If a handoff mentions a next step that isn't in `.workspace/TODO.md`, it was either completed or intentionally not added. Do not auto-promote it.

**Session close:**
- Before writing a handoff, check that any work completed during the session is reflected in `.workspace/TODO.md` (items moved to Completed). The handoff's "Next Steps" section should be consistent with `.workspace/TODO.md` pending items but is not the source of truth — `.workspace/TODO.md` is.

### Cleanup

Completed items are a permanent audit trail and are **never deleted**. Do not remove a completed item from the record. To keep the active `.workspace/TODO.md` readable, completed items older than 30 days **may be MOVED (not deleted)**, verbatim, to a per-project archive file `.workspace/TODO_archive.md` (create it if it does not exist, mirroring the `## Completed` format). The archive grows without bound, and that is intended. Never delete completed items from either file. Moving to the archive is optional housekeeping, not required; if in doubt, leave completed items in `TODO.md`.

## Dependency-aware ordering

Every task list must be ordered by actionability:

1. **Unblocked tasks** — can be started immediately. List these first, in priority order.
2. **Blocked tasks** — waiting on one or more dependencies. List after all unblocked tasks, ordered by depth in the dependency chain (shallowest blockers first, so tasks closest to becoming unblocked appear next).

## Explicit dependency statements

Every blocked task must state what it is blocked on. Use the format:

> - [ ] Task name — added YYYY-MM-DD — blocked on: [specific dependency]

Do not list a task as a simple numbered item if it has prerequisites. The blocker must be visible in the list itself, not buried in a separate discussion.

## No false readiness

Never describe a task as "ready," "next," or "pending" if it has unresolved dependencies. A task with a draft artifact (e.g., a draft email) is not "ready to send" if the attachment or precondition is incomplete. Distinguish between "draft ready" and "actionable."

## Re-sort on state changes

When a blocker resolves or a dependency is completed, re-sort the list. Tasks that were blocked and are now unblocked move to the top section. Do not leave stale ordering in place.

## Dependency chains

When multiple tasks form a chain (A blocks B blocks C), make the chain visible. In longer lists, a one-line dependency summary at the top is useful:

> Dependency chain: pilot work -> finalized interview guide -> finalized rubric -> external review -> pre-registration

## Scope

This applies to:
- Project `.workspace/TODO.md` files (primary)
- Handoff documents (next-steps sections — secondary, must be consistent with `.workspace/TODO.md`)
- Task lists presented in conversation
- Any enumeration of pending work when advising the user on priorities

This does not apply to:
- Retrospective lists of completed work (e.g., "What Was Done" sections in handoffs)
- A personal to-do list kept outside the project (e.g., a separate notes doc or task manager)
