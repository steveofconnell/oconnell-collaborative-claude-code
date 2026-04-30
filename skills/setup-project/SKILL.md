---
description: "Initialize a new research project with standard folder structure, documentation, and CLAUDE.md"
---

# Setup Project

Create the standard research project folder structure with documentation scaffolding.

## Input
$ARGUMENTS — project name or path. If not provided, ask.

## Instructions

### Step 1: Determine Location
If `$ARGUMENTS` is a full path, use it. If it's just a name, create the project at `~/Dropbox/<name>/`.

Confirm the location with the user before creating anything.

### Step 2: Discovery (if directory already exists)
If the directory already exists:
- List its current contents.
- Identify which standard folders already exist and which are missing.
- Ask the user: "Create missing folders and scaffolding? Or just fill gaps?"
- Do not overwrite existing files.

### Step 3: Create Folder Structure
Create the following directories (skip any that exist):

```
<project>/
├── 0admin/                  # IRB, grants, correspondence, project management
├── 1rawdata/                # Source data — never modified after initial deposit
├── 2processing/             # Cleaning/construction code
├── 3data/                   # Analysis-ready datasets (output of 2processing/)
├── 4code/                   # Analysis scripts, numbered sequentially
├── 5manuscript/             # Drafts, .tex/.md files
│   ├── tables/              # Output tables from 4code/
│   └── figures/             # Output figures from 4code/
├── .claude/                 # Claude Code project config
├── .workspace/              # Working files, exploratory output, temp
│   ├── memory/              # Project memory files
│   ├── handoffs/            # Session handoff documents
│   ├── plans/               # Implementation plans
│   ├── scratch/             # Exploratory scripts, intermediate data
│   ├── reference/           # Source PDFs, text extractions, codebooks
│   ├── notes/               # Working prose: memos, outlines, lit notes
│   └── logs/                # Pipeline run logs, build logs
```

### Step 4: Create Scaffolding Files

**`CLAUDE.md`** (project root) — minimal project config:
```markdown
# Project: <name>

## Purpose
<ask user for 1-2 sentence description>

## Key Details
- Authors: Stephen O'Connell <and ask if co-authors>
- Status: <ask: planning / data collection / analysis / writing>

## Memory Storage
- `MEMORY.md` → project root
- Individual memory files → `.workspace/memory/`
```

**`MEMORY.md`** (project root) — empty index:
```markdown
# <Project Name> Memory Index
```

**`1rawdata/source.txt`** — source documentation reminder:
```
This directory contains raw source data. Every file here must have documentation:
- Where it came from (URL, agency, contact person)
- When it was obtained
- Any access conditions or restrictions
- File format and contents description

Add documentation as data files are deposited.
```

### Step 5: Lock Project-Level Permissions
Create a read-only empty `.claude/settings.local.json` to prevent Claude Code from accumulating one-off permission rules that override the global config:
```bash
mkdir -p <project>/.claude
echo '{}' > <project>/.claude/settings.local.json
chmod 444 <project>/.claude/settings.local.json
```

### Step 6: Make 1rawdata Read-Only (optional)
Ask the user: "Make 1rawdata/ files read-only? (Prevents accidental modification — recommended.)"

If yes, note that new files can still be added, but existing files will be protected:
```bash
chmod -R a-w <project>/1rawdata/
```

### Step 7: Report
Print a tree view of what was created and any next steps (e.g., "deposit raw data in 1rawdata/ with source documentation").
