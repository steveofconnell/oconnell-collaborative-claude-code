---
description: "Re-run the script that produces a specific figure or table, then open the output"
---

# Reproduce Figure or Table

Re-generate a specific figure or table from its production script and open the result. Follow these steps:

## Step 1: Identify the Target Output

Determine which figure or table to reproduce. In order of priority:
1. If the user specifies a file or figure/table number, use that.
2. If the conversation has been discussing or editing a specific figure or table, use that.
3. If ambiguous, ask the user which output to reproduce. Do not guess.

## Step 2: Find the Production Script

Search the project for the script that generates the target output. Grep for the output filename across all code files in the project — it could be anywhere, not just `4code/`. Also check for a `Makefile` that maps targets to scripts.

If the script includes a long computation phase that saves intermediate results, and a separate output/plotting phase that loads those results — run only the output phase. Look for comments, section headers, or separate scripts that indicate this split (e.g., `04a_estimate.R` vs `04b_plot.R`, or a clearly marked output section after a `load()` or `readRDS()` call).

If the producing script cannot be identified, ask the user. Do not guess.

## Step 3: Determine the Run Command

Based on the script type:

### R (`.R`)
- `Rscript <script>`

### Stata (`.do`)
- `cd ~/Dropbox/stata/Stata && ./StataMP.app/Contents/MacOS/stata-mp -b do "<script>"`

### Python (`.py`)
- `python3 <script>`
- If a virtual environment exists in the project (`.venv/`, `venv/`, `env/`), activate it first.

### Other
- Ask the user how to run it.

## Step 4: Run the Script

Execute via Bash. Set a timeout of 300 seconds (5 minutes) — most output-phase scripts should finish well under this.

- If the script succeeds, proceed to Step 5.
- If it fails:
  - Show the last 40 lines of output.
  - Identify the error.
  - If the fix is obvious (missing library, wrong path, trivial typo), fix and rerun once.
  - Otherwise, present the error to the user.

## Step 5: Open the Output

Open the generated file:
```bash
open <output_file>
```

For tables (`.tex`, `.csv`, `.txt`): open in the default text editor.
For figures (`.pdf`, `.png`, `.svg`, `.jpg`): open in the default viewer.

If multiple outputs were produced by the script (e.g., a script generates both `figure_3a.pdf` and `figure_3b.pdf`), open all of them.

## Step 6: Report

Print one line:
```
Ran <script> -> <output_file(s)> (opened)
```

If the script produced warnings, summarize them compactly.
