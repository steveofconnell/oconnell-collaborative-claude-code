---
description: "Bring a collaborator's (RA/student's) completed work from their own sandbox folder into the canonical project, with snapshot-before-write reversibility and a full provenance log — for projects where the collaborator has no write access to canonical"
---

# Integrate Collaborator

The general procedure for a PI-run Claude Code session to pull a collaborator's (RA,
student, junior coauthor) finished work into the canonical project from their own
**sandbox folder**, without ever giving them write access to canonical. This is the
right pattern when:

- The collaborator needs their own space to work, experiment, and make mistakes
  without touching the shared project.
- The project is not (or not fully) under version control, so reversibility has to
  come from snapshot-before-write rather than `git revert`.
- The PI wants a single, auditable choke point — every change that reaches canonical
  passed through one reviewed integration, not ad hoc edits from multiple people.

**Adapt, don't copy verbatim.** This skill is a template. Write a project-specific
playbook (e.g. `0admin/RA/integration_playbook.md`) that fills in your project's
actual sandbox path, task list, and any domain-specific verification steps (e.g.
"re-run the estimation script and confirm it reproduces the reported coefficient").
This skill operationalizes that playbook — read the playbook first; it is the
canonical source and this skill defers to it if the two diverge.

## Standing facts

- **Sandbox folder**: the collaborator works in their own folder — conventionally a
  sibling of canonical (e.g. `../<ProjectName>_<their-initials>/`), shared read-only-in-spirit
  so the PI can see it. They never write to canonical directly. Use a relative
  sibling path in scripts and instructions, not a hardcoded absolute path, so the
  skill stays portable across machines.
- **Mirror-path convention**: the sandbox mirrors canonical at identical relative
  paths, and the collaborator saves each deliverable at the canonical path the task
  names (inside their own folder). Integration is then an identity-map copy-back, not
  a source→target translation.
- **Reversibility without git**: if canonical is not under version control, reversibility
  comes from **snapshot-before-write** to an integration-backups folder (e.g.
  `0admin/RA/integration_backups/<YYYY-MM-DD>_<task>/`), preserving relative paths. If
  canonical *is* under git, a commit before each integration serves the same purpose —
  pick one and be consistent.
- **PII rule (hard)**: if a deliverable involves identifiable human-subjects data,
  integrate file *locations* and *change logs* only — never paste identifiable content
  (recordings, un-redacted transcripts, names tied to responses) into the AI tool.
  Respect any `pii.txt` markers in the project. Redaction/anonymization decisions stay
  with the PI.

## Procedure

### 1. Find what's new
- Read the collaborator's most recent session handoffs (they should be running their
  own `/start` and `/close` in their sandbox per the standard session-continuity
  protocol).
- Build the change set from their handoffs: every file created or changed, with its path.
- **Confirm by diffing** the sandbox against canonical at the named paths. If the diff
  and the handoffs disagree, reconcile before proceeding — do not guess which is right.

### 2. Classify each changed file
- **Reference / research output** (write-ups, coded notes, dossiers, bibliography
  logs, verification lists) — no re-run needed. Confirm the file is well-formed and at
  a sensible path, then go to step 4.
- **Data-correction proposal** (an audit log proposing changes to an existing dataset)
  — step 3a.
- **Data/analysis output produced by running code** (a script's numbers, a figure, a
  test result) — step 3b.

### 3a. Data corrections (proposal → canonical data file)
Never silently overwrite existing values (see `rules/data-pipeline.md`, value-level
data integrity). Established mechanism: in-place value change plus a
`verified`/`corrected` flag column, with the proposal log (copied into canonical) as
the per-row provenance map and the pre-write snapshot as the reversal path.

1. Parse the proposal into buckets: **deterministic** (source-unambiguous
   corrections), **judgment call** (a choice between competing values or conventions —
   the PI decides, ideally shown the competing values directly), **blocked**
   (unclear — needs a better source; leave as-is, flag it).
2. Get the PI's explicit authorization for the deterministic set and every judgment
   call. Apply nothing the PI has not authorized.
3. **Snapshot** the target data file to the backup folder before touching it.
4. **Read-only validate before writing**: for every edit, confirm it matches exactly
   one row at the *expected current value*; for additions, confirm the row is absent;
   for dedups, confirm the expected duplicate count. Refuse to write if anything has
   drifted since the proposal was written.
5. Apply in **one pass**, then re-read the written file and print every touched row to
   confirm, and check the final row count.
6. **Flag downstream**: search for scripts that read the changed data file and list
   them as needing a re-run. Do not silently leave stale figures or numbers that feed
   the manuscript.

### 3b. Script outputs (verify before accepting)
- **Re-run against canonical inputs** — point the collaborator's code at this
  project's live inputs and confirm it reproduces their reported numbers or figures.
- **Never run a collaborator's script with a hard-coded path.** It should read its
  root from one setting (e.g. `PROJECT_ROOT` / `INPUT_DIR`), not a literal path baked
  into the file. If it doesn't, fix that before running it, and confirm the script
  writes only to intended targets.
- **Check for version skew**: if an input the collaborator was given has since changed
  in canonical, flag it — do not integrate a result computed on stale inputs.

### 4. Snapshot, then copy to the identical path
Back up any canonical file that will be created or overwritten to the integration
backups folder, then copy each deliverable to its **same relative path** in canonical
(including the proposal/provenance artifact itself, for the audit trail).

### 5. Log
Append an entry to an integration log (e.g. `0admin/RA/integration_log.md`): date ·
task · files integrated · verification result · judgment calls applied · items
deferred to the PI · downstream re-runs flagged · backup location · the handoff this
was sourced from.

### 6. Archive the collaborator's version (do not delete)
Copy — never move — the integrated deliverable(s) and the source handoff into a
frozen archive inside the collaborator's own sandbox (e.g.
`<sandbox>/0admin/completed_tasks/<date>_<task>/`), plus a short receipt noting what
was applied, what was deferred to the PI, and the backup reference. Copying (not
moving) keeps the collaborator's working files at their mirror paths, so their next
`/start` sees canonical as matched and the integrated deliverable doesn't spuriously
resurface as "new."

### 7. Update tracking and hand back
- Close the corresponding item in the project's task tracker (`.workspace/TODO.md`)
  and any collaborator-facing dashboard; spin off any PI-side residual (blocked items,
  downstream re-runs) as its own pending item.
- Write a short PI → collaborator handoff into the sandbox's handoff folder: what was
  integrated, the judgment calls made, what's left to the PI (not them), and their
  next step. This surfaces on their next `/start` and is the trigger for the
  `[[collaborator-handoff-acknowledgment]]` read-stamp protocol — see
  `rules/collaborator-handoff-acknowledgment.md`.

## Output
A short report: files integrated, verification result, judgment calls chosen, what
was deferred to the PI, downstream re-runs flagged, and where the collaborator's
version was archived.
