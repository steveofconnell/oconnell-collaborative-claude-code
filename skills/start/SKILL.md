---
description: "Full session startup: config discovery, handoff check, integrity acknowledgment, pending TODOs"
---

# Session Startup

Execute the following steps in order. Do not prompt for input until all steps are complete.

## Step 1: Config Discovery Report
Print a brief checklist showing which of the following files were found or not found:
- `~/.claude/CLAUDE.md` (symlink → global config) — verify symlink resolves
- `<project>/CLAUDE.md` (project-level config)
- `<project>/MEMORY.md` (project memory index)
- Any `HANDOFF_*.txt` files in `<project>/.s-workspace/`

Use the Read and Glob tools (not Bash) for all checks. Bash commands that reference paths outside the project directory trigger permission prompts.

## Step 2: Academic Integrity Acknowledgment
Print: "Academic integrity directives loaded — all written content will be held to peer-review standards for originality, citation accuracy, and intellectual rigor."

## Step 3: Capabilities Summary
Print a compact reference of available custom tools. Use this exact format (update if new items are added):

```
SKILLS (slash commands):
  /start            — Full session startup sequence
  /close            — Write handoff + persistent session log, update memory
  /review-paper     — Simulated referee report (writing + methodology agents)
  /review-plan      — Stress-test a plan with structured expert critique
  /prompt           — Format rough/dictated text into structured prompt (light/standard/deep)
  /setup-project    — Initialize new research project with standard folder structure
  /qa-loop          — Adversarial critic-fixer loop (iterates until clean or max rounds)
  /email-triage     — Read-only inbox triage: categorize, surface actions, propose unsubscribes

AGENTS (fresh-context reviewers):
  Writing Reviewer      — Prose quality, AI patterns, voice, argument structure
  Methodology Reviewer  — Causal claims, identification strategy, statistical practice

RULES (auto-loaded):
  academic-integrity      — Citations, originality, attribution (always-on)
  project-structure       — Folder structure, naming, documentation (always-on)
  academic-writing-voice  — Voice/style guide + writing preferences (*.tex, *.md, *.qmd, *.Rmd, *.txt)
  data-integrity          — Transcription safety + digitization protocol (data files, rawdata/processing dirs)

HOOKS (automatic):
  protect-rawdata         — Blocks writes to 1rawdata/ directories (PreToolUse)
  pre-compact             — Saves active plan/task before context compression (PreCompact)
  post-compact-restore    — Restores context after compression (SessionStart)
  context-monitor         — Warns when approaching context limit (PostToolUse)
```

Do NOT scan `~/.claude/skills/`, `~/.claude/agents/`, or `~/.claude/rules/` — those paths are outside the project directory and trigger permission prompts. The list above is maintained manually; update it when adding new skills/agents/rules.

## Step 4: Read Latest Handoff
Check for the most recent `HANDOFF_*.txt` in `<project>/.s-workspace/`. If one exists, read it and briefly summarize what was done last session and what the next steps are.

## Step 5: Read Memory Index
Read `<project>/MEMORY.md` if it exists. Scan the index for any **feedback-type memories that reference session behavior** (e.g., entries mentioning "session," "startup," "each session," "open with"). For each such entry, follow the link and read the full memory file **before composing any startup output**. These memories contain behavioral directives that modify the startup sequence itself — they are not background context. Execute their instructions as part of the startup. Then note any other relevant context for the current session.

## Step 6: Check Pending TODOs
Glob for `.s-workspace/TODO_*.md`. For any with `status: pending` and `remind_on_startup: true` in their frontmatter, surface them to the user.

## Step 7: Project-Specific Startup
After completing the above, check the project's `CLAUDE.md` for any additional startup behavior (e.g., TaskHQ fetches a Google Doc to-do list). Execute those directives.

## Step 8: Ready
Ask the user what they want to work on, offering context from the handoff and any time-sensitive items as a starting point.
