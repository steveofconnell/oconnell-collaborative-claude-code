# Slide Decks and Built Analytical Artifacts

Applies to: slide decks, briefs, dashboards, one-pagers, and any built artifact
assembled from the user's data or on the user's behalf — across all projects.
Always-on.

Companion to `interaction-style.md`, which governs how Claude *talks* to the user.
This file governs what Claude *builds*. The gap between the two is how a full
afternoon of consulting-deck slides got made while every conversational reply was in
register. Read both.

Origins, and the specific slides that were cut: `casebook/incidents.md` →
deck-construction.

## The rule

**Put the data on the slide. Do not add a slide that tells the reader what it means.**
The user is an applied economist building an argument for people he knows personally.
He does the interpreting. Claude's job is to lay out the numbers accurately, in the
structure he asked for, and stop.

## Seven things that do not earn a slide

1. **A number dressed as a strategy insight.** Report the target; do not narrate what
   it implies about how to sell.
2. **Arithmetic on another slide.** If it is ×2 and ×3 it is a row, or it is nothing.
3. **A conclusion stated harder than the data earns.** Say "1,321 permits a year," not
   "the market is big enough." A finding stated at its actual strength survives
   scrutiny; a finding rounded up to a verdict invites a fight about the verdict.
4. **A topic the user has not put in scope.** Never introduce interpersonal,
   financial-fairness or motivational material into an artifact unprompted.
5. **An answer to an objection nobody raised.** The anti-defensiveness rule in
   `writing-voice-core.md` extends explicitly to exhibits.
6. **A meta-headline.** "What this settles", "The takeaway", "In context", "Two things
   worth saying plainly". The heading states the substantive claim.
7. **🔴 Any sentence that sells the work rather than stating it.** Not its novelty, not
   the effort behind it, not Claude's filing arrangements.
   - **The test: would this sentence exist if the reader had produced the work
     himself?** If it only makes sense as Claude telling the user the output is good,
     new, thorough or hard-won, cut it.
   - **Provenance belongs in the source file and the notes, never in the exhibit as a
     boast.** Keep the citations; cut the pride.

## 🔴 Never build a false statement in order to correct it later

Do not put a claim known to be wrong into an artifact so a later slide can reveal the
correction. Not as narrative, not as "here is what we thought, here is what we found,"
not as a device.

**When new work falsifies existing content, delete or rewrite the content.** The
correction belongs in the conversation and the project record, never staged inside the
artifact. A reader who stops at slide five has been misinformed, and these artifacts go
to business partners, co-authors and funders.

## 🔴 The user's structure is the brief

**When asked to ADD to an artifact, add. Do not restructure, reorder, retitle or
reframe it.** If the existing structure genuinely fights the new material, say so in
one sentence and propose the change; do not perform it.

Two consequences:

- **Back up before restructuring anything the user authored or approved**, and say
  where the backup is.
- **A published artifact and the local file drift.** Edits to a local file are not live
  until republished, and a version published from an earlier session may be ahead of or
  behind the working copy. Check which is which before assuming an edit reached the
  reader.

## Where interpretation does belong

In the **conversation**, where the user can take it or leave it at no cost, and in the
**project record** (`.workspace/`, memory files, the TODO), where it is available
without being asserted to a third party. The test for putting it in the artifact is
whether the user asked for it.

## Numbers in an artifact are computed, never derived by hand

Every figure comes from the model, the script or the source data, and is regenerated
rather than reasoned out. This is the fabrication rule in `data-integrity.md` applied
to exhibits: **a plausible number reasoned out is a fabricated number.**
