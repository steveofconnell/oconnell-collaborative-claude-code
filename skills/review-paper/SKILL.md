---
description: "Simulated top-journal referee report on a manuscript — runs writing and methodology agents"
---

# Review Paper

Generate a simulated top-journal referee report on a manuscript draft.

## Input
$ARGUMENTS — optional path to the manuscript file. If not provided, ask the user which file to review.

## Instructions

### Step 1: Locate the Manuscript
If `$ARGUMENTS` contains a file path, use it. Otherwise:
- Glob for `*.tex`, `*.md`, `*.qmd` in `5manuscript/` or the current directory.
- If multiple candidates, ask the user which one.
- Read the full manuscript.

### Step 2: Determine Authorship
Check the manuscript for author count. If single-authored (or if the user has previously indicated this is solo work), note that the review should enforce first-person singular throughout.

### Step 3: Launch Parallel Reviews
Launch two agents in parallel:

**Agent 1: Writing Reviewer** (`~/.claude/agents/writing-reviewer.md`)
- Pass the manuscript text.
- This agent reviews prose quality, voice consistency, AI-typical patterns, argument structure.

**Agent 2: Methodology Reviewer** (`~/.claude/agents/methodology-reviewer.md`)
- Pass the manuscript text.
- This agent reviews identification strategy, causal language, statistical claims, robustness.

### Step 4: Synthesize Referee Report
Combine both agent reports into a single structured referee report:

```
# REFEREE REPORT — [Paper Title]
Date: [today]
Reviewed as: Top-5 applied micro journal submission

## Summary
[3-5 sentences: What the paper does, main contribution, overall assessment]

## Recommendation
[ACCEPT / MINOR REVISION / MAJOR REVISION / REJECT — with 1-sentence rationale]

## Major Issues
[Numbered. Issues that must be addressed for publication. Draw from both agents.]

## Minor Issues
[Numbered. Issues that would strengthen the paper but are not fatal.]

## Referee Objections
[3-5 specific objections phrased as a real referee would write them. These should be the toughest, most plausible attacks on the paper — the ones the author needs to prepare for.]

## Writing Quality
[Brief assessment from the writing reviewer — AI-pattern flags, voice issues, precision problems]

## Strengths
[What the paper does well — empirical approach, writing, contribution]
```

### Step 5: Save and Present
- Save the report to `<project>/.s-workspace/referee_report_<filename>_<date>.md`
- Present the full report to the user.
- Ask: "Want me to dig deeper on any specific issue, or start addressing the major issues?"

## Examples
```
/review-paper 5manuscript/draft_v3.tex
/review-paper
```
