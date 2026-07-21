# Collaborator Handoff Acknowledgment

Applies to: any project where work is handed to another person (RA, student, co-author,
collaborator) who runs their own Claude Code session in a shared folder, and coordination
runs through handoff documents. Read this when **setting up** such a collaboration and
whenever writing or reading a cross-person handoff. Always-on.

## The rule

A handoff document addressed to a specific person must stay in that person's startup
surface **until they have acknowledged reading it** — it never ages out on a time
window. "Read handoffs from the last N days" is the wrong test: if the recipient is away
for N+1 days, or busy, the handoff silently drops off their startup and the message is
lost. The correct test is an explicit **read-acknowledgment stamp**.

A time-windowed startup surface loses any handoff the recipient did not happen to open
inside the window. A directive left on a Friday is gone by the following Monday if the
window is two days. Delivery must be confirmed, not inferred from timing.

## Mechanism

**Writing a handoff (author side).** Write it into the recipient's folder as
`HANDOFF_<date>_<AUTHOR>.txt` with an `Author:` line. It carries **no read-stamp when
written** — absence of a stamp means "not yet read."

**Reading a handoff (recipient side).** On the recipient's `/start`, their Claude reads
**every** handoff addressed to them (authored by someone else) that **lacks a
read-stamp**, regardless of age. It summarizes and acts on each, then appends to the
file, on its own line at the end:

```

---
READ BY <RECIPIENT NAME> (CLAUDE) on <YYYY-MM-DD>
```

The stamp is a **delivery receipt, not a completion record** — it means "seen," not "the
task is done." Task status is tracked separately (the project TODO). A stamped handoff is
delivered; an unstamped one is still pending, no matter how old.

**Checking delivery (author side).** On the author's `/start`, their Claude surfaces any
handoff it wrote to the recipient that **still lacks the recipient's read-stamp** as "not
yet read — still pending delivery," regardless of age. The author's own Claude reading
the file does **not** stamp it; only the recipient's side stamps. This lets the author
see, at a glance, which directives have actually reached the person.

## Setup checklist (wiring it into a new collaboration)

Put the protocol on **both** sides so neither depends on memory:

1. **Recipient-side startup instructions** (the shared-folder `CLAUDE.md`, or the config
   the recipient installs): "On `/start`, read every handoff authored by someone else
   that has no `READ BY <you> (CLAUDE)` stamp, act on it, and append the stamp."
2. **Author-side startup instructions** (the canonical project `CLAUDE.md`): "On
   `/start`, surface any handoff I wrote to the collaborator that still lacks their
   read-stamp as pending delivery."
3. **Grandfather date.** Record the date the protocol takes effect in the project;
   handoffs dated before it are considered already processed, so adoption does not flood
   the next startup with the whole back-catalogue.

## Scope and edge cases

- Assumes Claude-mediated startup on both sides. If a handoff is read by hand outside
  Claude, stamp it anyway so the author's delivery check stays accurate.
- Keep the existing separate mechanisms intact: the recipient still writes their own work
  handoffs, and the author still diffs the shared folder and reconciles the shared TODO.
  This rule governs **delivery of directives to a person**, the direction that silently
  fails; it does not replace file integration or task tracking.
- One receipt per handoff is enough. Do not re-stamp on every subsequent `/start`.
