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
- Any `HANDOFF_*.txt` files in `<project>/.workspace/handoffs/`

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
  script-architecture     — Anti-proliferation guardrails, funnel principle (*.R, *.py, *.do)
  academic-writing-voice  — Voice/style guide + writing preferences (*.tex, *.md, *.qmd, *.Rmd, *.txt)
  data-integrity          — Transcription safety + digitization protocol (data files, rawdata/processing dirs)

HOOKS (automatic):
  protect-rawdata         — Blocks writes to 1rawdata/ directories (PreToolUse)
  pre-compact             — Saves active plan/task before context compression (PreCompact)
  post-compact-restore    — Restores context after compression (SessionStart)
  context-monitor         — Warns when approaching context limit (PostToolUse)
```

Do NOT scan `~/.claude/skills/`, `~/.claude/agents/`, or `~/.claude/rules/` — those paths are outside the project directory and trigger permission prompts. The list above is maintained manually; update it when adding new skills/agents/rules.

## Step 4: Read Recent Handoffs
Check for the **three most recent** `HANDOFF_*.txt` files in `<project>/.workspace/handoffs/` (sorted by filename descending). Read all three and briefly summarize each: what was done, by whom, and when. Present them in reverse chronological order (most recent first). This gives multi-session context rather than just the last session. **Always include who authored each handoff** (the `Author:` line) — this is essential in collaborative projects where multiple people work in the same directory. If any handoff was written by someone other than the current user, flag this prominently (e.g., "Session on [date] was run by [Name]"). If fewer than three handoffs exist, read whatever is available.

## Step 5: Read Memory Index
Read `<project>/MEMORY.md` if it exists. Scan the index for any **feedback-type memories that reference session behavior** (e.g., entries mentioning "session," "startup," "each session," "open with"). For each such entry, follow the link and read the full memory file **before composing any startup output**. These memories contain behavioral directives that modify the startup sequence itself — they are not background context. Execute their instructions as part of the startup. Then note any other relevant context for the current session.

## Step 6: AI Use Policy
Check for `aipolicy.txt` in the project root directory.

**If the file does not exist**, create it with this default content:

```
AI USE POLICY — [Project Name]

1. HUMAN SUBJECTS DATA PROTECTION

  No identifiable human subjects data may be entered into any AI tool. This
  includes names, geographic coordinates, household or individual IDs,
  contact information, photographs, voice recordings, and any combination
  of variables that could permit re-identification.

  De-identified and aggregate data (regression output, summary statistics,
  codebooks, variable lists, anonymized datasets where re-identification
  risk is negligible) may be used in AI-assisted work.

  Data directories are assumed de-identified unless marked otherwise. Any
  directory containing identifiable data must include a pii.txt file that
  describes what is sensitive (e.g., "Contains GPS coordinates, respondent
  names, household IDs"). The AI tool checks for this marker before reading
  data files: if pii.txt is present, it will not read the data and will use
  safe alternatives (see Section 2). If no pii.txt exists, the data is
  treated as non-sensitive. Place pii.txt when setting up raw data
  directories — it is a one-time step that protects the data in every
  future session.

  Qualitative data (interview transcripts, open-ended survey responses,
  case narratives) may not be entered into any AI tool unless (a) the text
  has been reviewed for re-identification risk by a member of the research
  team and (b) the project's IRB protocol explicitly permits AI-assisted
  analysis of such data. In small-sample qualitative work, even redacted
  transcripts may be identifying; err on the side of exclusion.

2. SAFE PATTERNS FOR WORKING WITH PII-CONTAINING FILES

  When AI assistance is needed to write or debug code that processes files
  containing identifiable data, use the following approaches to avoid
  transmitting PII to the AI tool:

    a. Read the codebook or data dictionary, not the data. If a codebook,
       source.txt, or variable documentation exists, provide that instead
       of the data file. Column names, types, and value descriptions are
       sufficient to write processing code.

    b. Read only the header row. Extracting the first line of a CSV or
       the variable list from a Stata/R file gives the AI the structure
       it needs with zero data records.

    c. Describe the structure verbally. Stating "the file has columns
       hhid, district, age, income, in long format by year" is enough
       to write correct code without any data leaving your machine.

    d. Use a de-identified extract. If the project has already produced
       a cleaned dataset with identifiers stripped, the AI may read that
       file. Confirm that the extract cannot be re-identified before
       sharing.

    e. Provide synthetic or fabricated example rows. A few made-up rows
       that match the real schema allow the AI to test parsing logic
       without exposure to real records.

  The general principle: the AI needs to know the structure of the data
  (column names, types, formats, relationships between files) but never
  needs to see the actual values of identifying fields. When in doubt,
  describe rather than show.

3. IRB AND DATA USE AGREEMENT COMPLIANCE

  Before using AI tools on any project involving human subjects data,
  confirm that the project's IRB approval does not prohibit AI-assisted
  analysis. If the protocol is silent on AI use, seek guidance from the
  IRB or file an amendment before proceeding.

  If the project operates under a data use agreement (DUA) with a partner
  organization, review the DUA for restrictions on third-party data
  processing. AI-assisted analysis may constitute third-party processing
  even when data is not retained by the AI provider.

4. PERMITTED USES

  AI assistance (currently: Claude by Anthropic, via the Claude Code CLI
  running locally) is used under direct supervision of the PI(s) for:

    - Code writing, debugging, and refactoring (R, Stata, Python, LaTeX)
    - Data processing pipeline construction and review
    - Literature search and organization (all citations independently
      verified before use)
    - Drafting and editing prose (all text reviewed, substantively revised,
      and approved by the author before submission or circulation)
    - Administrative tasks (correspondence drafts, formatting, scheduling)

5. PROHIBITED USES

  AI tools are not used to:

    - Generate, fabricate, or interpolate data, results, or statistical
      output
    - Produce final manuscript text without human review and substantive
      revision by the author(s)
    - Make independent analytical, methodological, or interpretive
      decisions
    - Process identifiable human subjects data (see Section 1)
    - Replace the researcher's intellectual contribution or judgment

6. AUTHORSHIP AND INTEGRITY

  All written output attributed to the author(s) has been reviewed,
  revised, and approved by the author(s). The author(s) take full
  responsibility for the content, accuracy, and integrity of all work
  product. AI tools are not authors and receive no attribution.

  All citations have been verified against primary sources. No AI-
  generated or unverifiable references appear in any output.

7. DISCLOSURE

  AI use will be disclosed in whatever form the target journal, funder,
  or institution requires. The signatories below have reviewed the
  relevant policies and accept responsibility for compliance.

8. TOOLS AND ENVIRONMENT

  Tool:      Claude (Anthropic) via Claude Code CLI
  Interface: Local terminal (not shared web sessions)
  Data flow: Prompts sent to Anthropic API; Anthropic does not train on
             API inputs per its data retention policy (verify current
             terms at anthropic.com/policies)
  Models:    [Model family, e.g. Claude Opus 4 / Sonnet 4]

  This section should be updated when tools or interfaces change.

9. SCOPE

  This policy applies to all members of the research team, including
  coauthors, research assistants, and students working on the project.
  Anyone using AI tools on this project must read this policy and add
  their name below before doing so.

Last modified: [DATE]

AGREED (by adding their name below, each team member confirms they have
read this policy and will comply with all provisions):

  - [Full Name], [DATE]
```

Replace `[Project Name]` with the project directory name, `[DATE]` with today's date, and `[Model family]` with the current model (e.g., "Claude Opus 4 / Sonnet 4"). Leave `AGREED` entries as placeholders — prompt the user to add their name and have coauthors/RAs review and sign. After creating the file, print: "Created default aipolicy.txt — review and customize for this project. Add your name to the AGREED section, and have coauthors and RAs sign before they use AI tools on this project."

**If the file exists**, read it and print it under the heading **AI Use Policy** so the policy is reiterated at the start of every session. Keep the printout compact — print the full text as-is, no commentary.

## Step 7: Check Pending TODOs
Read `.workspace/TODO.md` if it exists. Surface all pending items (unchecked `- [ ]` entries) to the user as part of the startup briefing. This is the single source of within-project tasks — do not pull tasks from handoffs, memory, or email.

## Step 8: Project-Specific Startup
After completing the above, check the project's `CLAUDE.md` for any additional startup behavior (e.g., TaskHQ fetches a Google Doc to-do list). Execute those directives.

## Step 9: Ready
Ask the user what they want to work on, offering context from the handoff and any time-sensitive items as a starting point.
