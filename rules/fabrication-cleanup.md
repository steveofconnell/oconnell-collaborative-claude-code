---
description: "When a fabrication or misrepresentation is found in any artifact (CV, proposal, manuscript, dataset), sweep the whole artifact and its siblings — never fix only the first instance"
---

# Fabrication and Misrepresentation Cleanup — Exhaustive Sweep

Applies to: any document, dataset, CV, proposal, application, manuscript, or
other artifact in which a fabricated, unverified, or misrepresented claim is
discovered — across all projects.

## The rule

When a fabrication or misrepresentation is found in any artifact, finding it is
not the task — cleaning the artifact is. A single discovered instance triggers
an **exhaustive sweep** of the entire artifact (and any sibling artifacts that
share its lineage) for every other instance of the same class of problem. Never
fix only the instance that happened to surface first, and never flag problems
one at a time as they catch the eye.

This rule exists because of a documented failure: a session removed three
fabricated entries from a CV but left a fourth misrepresentation in place, in a
different section and a different form — a sentence in a prose summary rather
than a list entry. The incomplete cleanup surfaced later, one item at a time,
and cost the user repeated rounds of review. Partial cleanup is worse than none:
it creates false confidence that the artifact is clean.

## Protocol

When a fabrication or misrepresentation is discovered:

1. **Stop and widen.** Do not fix the single instance and move on. Treat the
   discovery as evidence that the artifact's provenance is unreliable.

2. **Establish the canonical source.** Identify the authoritative, verified
   record — for a CV, the user's own published / website materials; for data,
   the raw source; for citations, the primary source. Every claim in the
   artifact is checked against it.

3. **Sweep the whole artifact.** Go through every section — prose summaries,
   lists, tables, headers, footnotes, captions. Misrepresentations hide in prose
   as readily as in structured entries; the form that surfaced first is not the
   only form to look for.

4. **Sweep sibling artifacts.** If the artifact was derived from, or shares
   content with, others — a CV reused across applications, a paragraph copied
   between proposals — the same problem is likely in those too. Identify them.

5. **Produce a complete findings list in one pass.** Every claim not
   corroborated by the canonical source, classified: outright fabrication;
   overstatement / mischaracterization; or unverified-but-possibly-real. Note
   that a canonical source's *silence* on a claim is not proof of fabrication —
   genuine work can be absent from an academic CV — so classification matters.

6. **Authorization to remove.** Remove only what the user has explicitly
   identified as fabricated. For everything else — anything that might be a real
   part of the user's record merely absent from the canonical source — present
   it and obtain the user's explicit per-item decision. Never unilaterally
   delete content from the user's professional record on suspicion alone (see
   `data-integrity.md`: corrections require explicit authorization).

7. **Report the sweep.** State what was swept, what was found, what was removed,
   and what is still pending the user's decision. A cleanup reported as "fixed
   it" without the scope of the sweep is itself incomplete.

## Why

A fabrication is rarely solitary. It enters through a process — a bad source, an
unverified inference, a contaminated template — and that process almost always
introduced more than one. Finding one and stopping leaves the rest in place with
a now-misleading appearance of having been checked. The user's professional
reputation depends on artifacts that are clean in full, not clean where someone
happened to look first.
