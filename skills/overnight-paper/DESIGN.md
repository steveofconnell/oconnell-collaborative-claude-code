# Overnight Paper Development — Design

Design rationale for the `overnight-paper` skill and its workflow.

## Objective

One autonomous system, run unattended (overnight), whose goal is **a better paper** —
not "edit the prose." The unit is the whole research project; the manuscript is its
final surface.

## Scope: the whole artifact graph

Everything is in play, end to end:

    raw data → processing scripts → analysis → production tables/figures
             → technical content in the text → rhetorical construction → paper

The loop has **full reach** across this graph. What differs by change is not *whether*
the loop can touch a layer, but *how much authority* it has over the change.

## The one authority principle

Earlier drafts tiered changes by layer (prose vs. code vs. data). Wrong axis. With the
whole pipeline in play, the line is one question asked at every layer:

> **Does this change alter what the paper CLAIMS or SHOWS?**

- **No → GREEN.** The agent does it and it compounds across rounds. Output-neutral:
  prose polish, voice enforcement, refactors with identical output, formatting, notes,
  cross-refs, docs, regenerating outputs from unchanged logic.
- **Yes → YELLOW.** A proposal the user signs off on. Moves a number (even an
  obviously-correct bug fix — *if a result moves, it is yellow*), changes a
  spec/sample/estimator/FE/clustering/weighting/functional form, alters a claim, adds
  new argument-bearing content, acquires new raw data, corrects a data value, adds a
  dependency.
- **Never → RED.** Fabricate a citation/value, mutate `1rawdata/`, overwrite an
  existing value, or state an untraceable claim/citation (→ `TKTK`).

This single test reproduces the user's standing rules (specification integrity, data
integrity, academic integrity, voice) as one axis instead of a per-layer rulebook.

## Three modes, selected per section by state

The same engine behaves differently depending on a part's current state:

- **Build** — a missing/partial section. Generate content, *grounded* in the outline,
  the real analysis outputs, and a real `.bib`. New argument is always YELLOW;
  unverifiable cites and untraceable numbers become `TKTK`. Highest fabrication risk;
  most fenced. Converges on coverage (every gap filled).
- **Refine** — a complete-but-rough section. Elevate toward the user's voice and
  top-journal conventions. Reject lateral rewrites and any edit that trades the
  author's voice for generic polish. Converges at a quality plateau.
- **Review** — a finished section. Defects only. Converges when defects run out.

## What makes it ONE system, not two loops

1. **Propagation.** The unit of work is a change *pushed through the pipeline*, not a
   file edited. Fix `02_clean.R` → data changes → regression changes → table changes →
   the number in the text changes. The loop regenerates downstream and re-syncs the
   manuscript, presenting the whole cascade as one coupled change.
2. **Cross-layer consistency** is the verifier's central job: text numbers == tables ==
   script outputs == data; figures == current data. A paper whose text and tables
   disagree is worse, not better — and only a system that sees all layers can catch it.

## Convergence

Stop after `staleStop` consecutive rounds with no material improvement, or at
`maxRounds`. Refinement has no natural floor, so the per-change bar is "genuine
improvement, not lateral rewrite," and lateral rewrites are reverted the way nitpicks
are. Build mode has a cleaner floor (the outline checklist).

## Safety architecture

- **Worktree isolation.** All work on a dedicated git worktree/branch; the live tree is
  never touched; the loop NEVER merges. Morning review is one cumulative diff.
- **`1rawdata/` is append-only**, enforced by the `protect-rawdata.sh` hook. Sourced
  data stages to `.workspace/staging/rawdata/<source>/` with `source.txt` and the
  "already digitized?" check, for the user to vet into `1rawdata/`.
- **The bright line that never moves:** no specification search, no sample change.
  Alternatives may be *proposed* (run in the worktree, before/after shown, everything
  tried disclosed) but never decided silently. The loop does the user's grunt work,
  not the user's judgment.

## The payoff

A correct integrated loop can find a genuine pipeline bug at 2am, fix it, propagate the
corrected numbers to the manuscript, re-sync the prose, and leave a morning diff:
"this bug moved your main coefficient 0.20 → 0.17; here is every number and sentence
that changed" — real scientific work done overnight, with nothing about the
specification or sample decided behind the user's back.

## Open items / not yet built

- Remote triggering (start it from a phone while the Mac is at home) — only completion
  notification is wired; starting remotely is a separate mechanism, TBD.
- Token-budget ceiling for unattended runs (parameter exists conceptually; wire into
  CronCreate scheduling).
- The workflow's reviser does green application and propagation in one agent; for large
  cascades this may want a dedicated propagate→regenerate→re-sync sub-pipeline.
