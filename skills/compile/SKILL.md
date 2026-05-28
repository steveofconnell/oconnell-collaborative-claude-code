---
description: "Compile and open the active written document (LaTeX, Quarto, R Markdown)"
---

# Compile and Open Document

Compile the document currently being worked on and open the resulting PDF (or HTML). Follow these steps:

## Step 1: Identify the Active Document

Determine which document to compile. In order of priority:
1. If the user specifies a file, use that.
2. If the conversation has been editing or discussing a specific `.tex`, `.qmd`, or `.Rmd` file, use that.
3. If the project has a `5manuscript/` directory, look for the main `.tex` or `.qmd` file there.
4. If ambiguous, ask the user which file to compile. Do not guess.

## Step 2: Determine the Compile Command

Based on the file type:

### LaTeX (`.tex`)
- Use `latexmk -pdf -interaction=nonstopmode -cd <file>` as the default.
- If a `Makefile` exists in the same directory and has a default or `pdf` target, prefer `make` instead.
- If a `latexmkrc` file exists in the same directory, `latexmk` will pick it up automatically.
- Run from the document's directory.

### Quarto (`.qmd`)
- Use `quarto render <file>`.
- If a `_quarto.yml` exists in the project, Quarto will use it automatically.

### R Markdown (`.Rmd`)
- Use `Rscript -e "rmarkdown::render('<file>')"`.

### Other formats
- If the document type is not recognized, ask the user how to compile it.

## Step 3: Compile

Run the compile command via Bash. Set a timeout of 120 seconds (most compilations finish well under this).

- If compilation succeeds, proceed to Step 4.
- If compilation fails:
  - Show the **last 40 lines** of the log output (not the full log).
  - Identify the first LaTeX/Quarto/R error in the output.
  - If the fix is obvious (missing package, undefined reference needing a second pass, missing closing brace), fix it and recompile once.
  - If the fix is not obvious, present the error to the user and ask how to proceed.
  - Do not retry more than once without user input.

## Step 4: Open the Output

Open the resulting PDF (or HTML) with the system viewer:
```bash
open <output_file>
```

On macOS, `open` will use the default PDF viewer (typically Preview or Skim).

## Step 5: Report

Print one line confirming success:
```
Compiled <filename> -> <output_filename> (opened)
```

If there were warnings (e.g., undefined references, overfull hboxes), list them briefly after the success line. Do not suppress warnings silently — the user should know about them, but keep the summary compact (group similar warnings, e.g., "3 overfull hboxes").
