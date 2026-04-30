# Task Management and Dependency Tracking

Applies to: all task lists, TODO files, handoff next-steps sections, and any enumeration of pending work items — across all projects.

## Project TODO file

Every project has a single `.workspace/TODO.md`. This is the canonical source of within-project tasks. Not handoff documents, not memory files, not scattered individual `TODO_*.md` files — one file per project.

### Format

```markdown
# TODO

## Pending

- [ ] Task description — added YYYY-MM-DD
  - Optional context, blockers, or notes as indented sub-bullets
- [ ] Another task — added YYYY-MM-DD — blocked on: [specific dependency]

## Completed

- [x] Finished task — added YYYY-MM-DD, done YYYY-MM-DD
```

Rules:
- One line per task. Sub-bullets for context only.
- Every task gets an `added` date.
- Blocked tasks state their blocker inline (see dependency rules below).
- Completed tasks move to `## Completed` with a `done` date.

### Lifecycle

**Adding tasks:**
- When a to-do surfaces during a session (user states it, or it's a clear next step from work just done), write it to `.workspace/TODO.md` immediately. Do not defer to handoffs, memory, or conversation notes.
- If `.workspace/TODO.md` doesn't exist yet, create it (and `.workspace/` if needed).

**Completing tasks:**
- When the user says something is done (explicitly or by completing the work), update `.workspace/TODO.md` right then — move the item to `## Completed` with the done date. Do not wait for session close.

**Dropping tasks:**
- If the user says to drop or cancel a task, delete it from the file entirely. No "cancelled" status — if it's not worth doing, it's not worth tracking.

**Startup:**
- Read `.workspace/TODO.md` and surface pending items as part of the startup briefing.
- Do NOT pull tasks from handoff "Next Steps" sections, memory files, or email. `.workspace/TODO.md` is the only source.
- If a handoff mentions a next step that isn't in `.workspace/TODO.md`, it was either completed or intentionally not added. Do not auto-promote it.

**Session close:**
- Before writing a handoff, check that any work completed during the session is reflected in `.workspace/TODO.md` (items moved to Completed). The handoff's "Next Steps" section should be consistent with `.workspace/TODO.md` pending items but is not the source of truth — `.workspace/TODO.md` is.

### Cleanup

Completed items accumulate as an audit trail. Prune items older than 30 days from the `## Completed` section to keep the file readable. When pruning, do it silently — no need to confirm each deletion.

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
- The Google Doc personal to-do list (managed separately via TaskHQ)
