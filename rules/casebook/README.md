# Casebook — why the rules say what they say

**This directory ships empty on purpose.** It holds your own record of the specific
failures that produced each rule, and those are necessarily personal: they name your
projects, your collaborators, and your own words.

## The convention

Several rules in this directory end with a pointer like:

> Origin, and the day this cost: `casebook/incidents.md` → literature-search.

Those pointers resolve to a file you write and keep **private** — in your own sync
folder, never in this repo. The split exists for two reasons.

**Context cost.** A rule that carries its full origin narrative is several times the
size of the rule itself. Eight such rules pushed one always-on startup load past
80,000 tokens before the user had typed anything. Moving the narratives out cut that
load without deleting anything.

**Credibility.** A rule stated bare invites re-litigation: a future session reads
"never do X," judges it overcautious, and works around it. A rule whose origin is one
lookup away does not. Keep the narratives — just not in context on every turn.

## How to use it

Create `casebook/incidents.md` in your own config folder (not here). Give it one
section per rule file, keyed by the rule's filename, and record each incident
verbatim rather than summarized:

```markdown
## literature-search.md

**The founding incident. <date>, <project>.** <What happened, what it cost, and
the mechanical cause — not the lesson. The lesson is the rule; this is the
evidence for it.>
```

Write the entry the day the failure happens, while the details are still exact. A
summarized incident stops being evidence.

## When to read it

Read a section when a rule is being questioned, when someone proposes relaxing it,
or when its scope is genuinely unclear. Do not read it to follow the rule — the rule
states what to do on its own. This directory is deliberately outside the always-on
load.

## Keep it out of the repo

If you clone this config and add your own casebook, add it to `.gitignore`:

```
rules/casebook/incidents.md
```

The maintainer's own casebook is not published here for exactly this reason.
