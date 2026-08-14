# Persist Collaborative State In the Moment

Applies to: all projects, all sessions. Always-on.

## The rule

When the user and I jointly produce structured content during a
conversation — an inventory, a plan, a roster, a playbook, a ranked list,
a configuration, a decision matrix — write it to a memory file *the
moment the structure becomes visible*. Not at the end of the session,
not in the next handoff, not "if it turns out to matter." In the moment.

Origin: a dictated wardrobe inventory and a six-day plan built with it were
never written to disk, and both were unrecoverable on day one of the trip.
Full account: `casebook/incidents.md` → persist-collaborative-state.

## Triggers — save without being asked

Save the moment any of the following happens in conversation. Do not
wait to "see if it gets used." Do not assume the conversation will
preserve it.

- **The user dictates an inventory.** Clothing, pantry, equipment,
  books, files, contacts, software, equipment, financial accounts,
  recurring subscriptions, vehicles, properties — anything enumerable
  that the user is reading off or recalling.
- **The user and I structure a multi-day, multi-step, or multi-item
  plan.** Wardrobe by day, meal plan, itinerary, packing list, debug
  sequence, rollout plan, sequence of revisions to a manuscript,
  course-prep schedule.
- **The user states an original idea, framing, construct or analytic move.**
  Record it with the date and *his own wording*, in that session. Where the
  project keeps an authorship or provenance ledger, it goes there; otherwise a
  memory file. Session transcripts are not a substitute: they are
  machine-local, unsynced, and expire. And never expand someone else's remark
  into an idea and then record the expansion as their words — record what they
  said, and attribute the expansion to whoever made it.
- **The user articulates preferences attached to specific situations
  or entities.** What to order at restaurant X, how to handle email
  from person Y, what to do when situation Z arises. (Distinct from
  generalized preferences, which go in the global `CLAUDE.md` Learned
  Preferences section.)
- **The user describes a process or playbook they follow.** How to prep
  a class, how to handle a specific email correspondence, how to
  onboard an RA, how to file an invoice with a particular funder, what
  the recurring steps in a monthly task are.
- **The user lists named people, organizations, vendors, or things
  with attributes.** A roster, an org chart, a contact list, a vendor
  comparison, a list of journals with notes on each.

The unifying test: *would I be unable to regenerate this content
without asking the user the same questions again?* If yes, save it.

## Save the raw inputs, not just the synthesis

When a plan or recommendation is built from an inventory or set of
preferences, save the inputs separately from the output.

- The plan can be regenerated from the inventory.
- The inventory cannot be regenerated from anywhere except the user.
- If only the plan is saved, losing it forces a full re-dictation.
- If only the inventory is saved, the plan can be rebuilt in minutes.

The inventory is the expensive thing. Save it separately, and first.

## Where to save

- **Project-specific content** → `<project>/.workspace/memory/` with a
  descriptive filename: `inventory_<topic>.md`, `plan_<topic>.md`,
  `roster_<topic>.md`, `playbook_<topic>.md`, `reference_<topic>.md`.
- **Personal / cross-project state** (pantry, personal contacts,
  household equipment, recurring personal admin) → the `.workspace/memory/`
  of whichever project you keep as a personal admin workspace, with the same
  naming conventions.
- **Add a one-line entry to the corresponding `MEMORY.md` index** so
  the file is discoverable in future sessions.

Use the standard memory frontmatter (`name`, `description`, `metadata:
type:`). For inventories and reference content, type is `reference`.
For plans tied to a specific event or initiative, type is `project`.

## Confirm the save

After saving, tell the user in one line: "Saved [X] to [path]." This is
not a request for permission. It is a receipt — the user needs to know
the content persisted, and which file to point at later.

## Save early, append as it grows

A conversation may start with a single item ("I have a navy blazer")
and accumulate structure as the user talks. Do not wait until the
inventory is "complete" before saving — the user may pause, switch
topics, or be interrupted. Create the file at the first item and
append as the conversation continues. An incomplete saved inventory is
infinitely more useful than a complete inventory that exists only in
the conversation log.

## When in doubt, save

The cost of an unnecessary memory file is trivial. It can be deleted in
one command. The cost of losing twenty minutes of dictated inventory is
high — the user has to spend twenty more minutes recreating it, and is
justifiably frustrated. Default to save.

## Scope

This rule does not apply to:

- Ephemeral conversation context (what the user is currently working
  on this minute, intermediate scratch reasoning).
- Content that already exists in another file the user is editing.
- Generalized preferences that belong in `CLAUDE.md` Learned
  Preferences (those have their own dedicated mechanism — see the
  Preference Learning section of global `CLAUDE.md`).
- Task lists (those have their own dedicated mechanism — see
  `task-management.md`).

For everything else where the user is constructing structured content
with me, the default is: save now.
