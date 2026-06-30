---
name: overnight-paper
description: Launch an autonomous overnight loop that improves a whole research project toward a better paper — across raw data sourcing, processing and analysis scripts, production tables and figures, technical text, and rhetorical construction. Runs in an isolated git worktree; applies output-neutral improvements automatically; proposes (never merges) anything that moves a number, changes a specification or sample, or adds new content; and stops at convergence. Produces one morning diff + changelog + quarantined-proposals report. Use when the user wants an unattended overnight development pass on a research project at any stage of completeness.
---

# Overnight Paper Development

One system to make a research project a better paper. The whole artifact graph is in
scope — raw data → `2processing/` → `3data/` → `4code/` → production tables/figures →
`5manuscript/` text → rhetoric. The intelligence is in spawned finder/reviser/verifier
agents; the orchestration is the deterministic Workflow shipped alongside this skill at
`~/.claude/skills/overnight-paper/overnight_paper.js`.

## The one authority principle

Every change is tiered by one question: **does it alter what the paper claims or shows?**

- **GREEN — applied automatically, compounds across rounds.** Output-neutral changes:
  prose tightening, voice enforcement, refactors with identical output, figure/table
  formatting and notes, cross-reference and path fixes, docs, regenerating an output
  from unchanged logic.
- **YELLOW — proposed for your sign-off, never merged.** Anything that moves a reported
  number (including an obviously-correct bug fix — if a result moves, it is yellow),
  changes a specification/sample/estimator/FE/clustering/weighting/functional form,
  alters a claim, adds new argument-bearing prose or a section, acquires new raw data,
  corrects a data value, or adds a dependency.
- **RED — never, flag only.** Fabricate a citation or value, write to `1rawdata/`,
  overwrite an existing value, or state an empirical claim/citation it can't verify
  (→ `TKTK` marker instead).

Two non-negotiables on top: **no specification search or sample change** (alternatives
may only be proposed, with everything tried disclosed), and **propagation** (a change
isn't done until pushed through the pipeline and the manuscript's numbers/prose
re-synced — presented as one coupled change).

## Procedure

1. **Confirm prerequisites.**
   - Current project must be a git repo (`git rev-parse --is-inside-work-tree`); if not,
     offer `git init` (do not init silently — the worktree model needs it).
   - Working tree clean (`git status --porcelain`); if dirty, ask to commit/stash so the
     work branch forks from a known state.
   - Scripts must run non-interactively (paths resolved, no prompts) — the loop runs them
     to propagate changes.
   - For BUILD work (a partly-done paper), confirm the grounding materials exist: an
     outline/section skeleton, the analysis outputs to draft from, and a real `.bib`.
     Without these, build-mode invents structure and claims — do not run build-mode
     ungrounded.

2. **Get the objective.** One line on what "better" means for THIS paper this run
   (e.g. "finish the results section and tighten the identification argument"). Pass it
   through to the workflow.

3. **Create the worktree and branch.** Compute the date with `date +%Y%m%d` (do not
   guess). From the project root:
   `git worktree add ../<project>-overnight-<date> -b overnight-paper-<date>`.
   Record the absolute worktree path.

4. **Pick run parameters.** First test on a project: `maxRounds: 2, staleStop: 2`
   (short pass, small diff). Real overnight run: `maxRounds: 6, staleStop: 2`.

5. **Launch the workflow.** Resolve `$HOME` to an absolute path first (a `~` inside the
   `scriptPath` string literal will not expand); the workflow ships in this skill's own
   directory:
   ```
   Workflow({
     scriptPath: "/absolute/path/to/.claude/skills/overnight-paper/overnight_paper.js",
     args: { worktreePath: "<abs path>", branch: "overnight-paper-<date>",
             maxRounds: <n>, staleStop: 2, objective: "<one line>" }
   })
   ```
   It runs in the background and notifies on completion. For an actual overnight run,
   schedule with CronCreate at the desired hour instead of launching now. Add a token
   budget for unattended runs.

6. **On completion, write the morning artifact** into the worktree's `.workspace/`:
   - `REVIEW_REPORT.md` — objective, rounds, converged?, the changelog (every applied
     green change, flagging any the reviser held back because it moved a result), and the
     quarantine list (every yellow proposal with rationale and before/after).
   - Tell the user the branch, how to see the cumulative diff
     (`git diff main...overnight-paper-<date>`), and that nothing is merged.

7. **Cleanup.** After the user merges what they want: `git worktree remove <path>` and
   delete the branch if unwanted.

## Notes

- New data an agent sources lands in `.workspace/staging/rawdata/<source>/` with
  `source.txt` and the "does this already exist in machine-readable form" check done
  first — never in `1rawdata/` (the `protect-rawdata.sh` hook enforces this).
- Resumable: relaunch the workflow with `resumeFromRunId` (in the original tool result)
  if a run dies mid-way.
- See `DESIGN.md` in this directory for the full rationale.
