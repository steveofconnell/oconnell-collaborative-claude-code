---
description: "Review writing style, tone, voice, and AI-typical patterns in a document — lightweight alternative to /review-paper"
---

# Review Writing

Run the Writing Reviewer agent on a document to check prose quality, voice consistency, argument structure, and AI-typical patterns. No methodology review.

## Input
$ARGUMENTS — optional path to the file to review. If not provided, ask the user which file to review.

## Instructions

### Step 1: Locate the File
If `$ARGUMENTS` contains a file path, use it. Otherwise:
- Glob for `*.tex`, `*.md`, `*.qmd`, `*.txt` in `5manuscript/`, `6tex/`, or the current directory.
- If multiple candidates, ask the user which one.
- Read the full file.

### Step 2: Determine Authorship
Check for author count. If single-authored, note that the review should enforce first-person singular throughout.

### Step 3: Launch Writing Reviewer
Launch the Writing Reviewer agent (`~/.claude/agents/writing-reviewer.md`) with the document text.

### Step 4: Present Results
Present the agent's report directly to the user. Save to `<project>/.workspace/writing_review_<filename>_<date>.md`.

Ask: "Want me to address any of these issues?"

## Examples
```
/review-writing 5manuscript/draft_v3.tex
/review-writing 6tex/slides/brownbag_slides.tex
/review-writing
```
