---
description: "R coding style — tidyverse base, house defensive-practice conventions, figure/table and reproducibility rules"
paths:
  - "**/*.{R,r,Rmd,qmd}"
---

# R Coding Style

Applies to: all `.R`, `.r`, `.Rmd` and `.qmd` files, every project.

The base is the **tidyverse style guide** (https://style.tidyverse.org/), which is
the de facto standard for modern R. Where a project is written in base R or
`data.table`, follow the project. Sections marked as house conventions state the
reasoning that makes them worth keeping.

## The override that beats every rule here

**Match the file you are editing.** Internal consistency beats individual
correctness. Do not convert a base-R script to tidyverse, or a `data.table`
script to `dplyr`, as a side effect of unrelated work. Raise it if it matters;
do not resolve it unilaterally.

## Formatting

- 2-space indentation, never tabs. Maximum line length 80 characters.
- Spaces around infix operators (`<-`, `=`, `+`, `==`) and after commas, none
  before. No space between a function name and its opening parenthesis.
- `<-` for assignment, not `=`. Reserve `=` for function arguments.
- Do not use `;` to put multiple statements on one line.
- Place `{` at the end of the line that opens the block and `}` on its own line.

## Naming

- `snake_case` for objects and functions. Never `camelCase`, never dots in new
  names: `n.groups` is legacy S3 method syntax and is confusing in new code.
- Functions are verbs, data objects are nouns: `build_panel()`, `panel_annual`.
- Descriptive names throughout, per `project-structure.md`. No `df`, `df2`,
  `tmp`, `x1` surviving into committed code. The exception is the same one as
  elsewhere: standardized survey variable codes keep their published names.
- Avoid overwriting base functions (`c`, `data`, `df`, `mean`, `t`).

## Structure

- One script, one task, per `project-structure.md` and `script-architecture.md`.
- All `library()` calls at the very top, one per line, no `require()` in scripts
  (`require()` returns FALSE rather than failing, which hides a missing package
  until something downstream breaks confusingly).
- Use `# ---- Section name ----` or `# ====` banners; RStudio and Positron fold on
  the former and it populates the document outline.
- Prefer explicit namespacing (`dplyr::filter`) where a function's origin is
  ambiguous or conflicts are likely, especially `filter`, `select`, `lag`.

## Paths and project hygiene

- **Never `setwd()`.** Never hardcode an absolute path or a home directory. Use
  `here::here()`, or an `renv`/RStudio project root, so the script runs on any
  collaborator's machine. This is what makes multi-device and multi-user work
  possible and it is not optional.
- **Never `rm(list = ls())` at the top of a script.** It does not give a clean
  session (it leaves attached packages, options and loaded objects in place) and
  it destroys the user's work if run in the wrong console. Start a fresh R session
  instead; in RStudio, disable workspace saving so sessions are clean by default.
- Do not rely on `.RData` restoring state between sessions. A script must run from
  a fresh session.
- Never `attach()`.

## Pipes and control flow

- Use the pipe for a sequence of transformations on one object. `|>` (base, R
  4.1+) is preferred in new code; `%>%` is fine in a project already using it.
- Break the pipe across lines, one verb per line, with the pipe at the end of the
  line.
- Keep a pipe to a readable length. Past roughly ten steps, name an intermediate
  object; a long pipe is hard to debug because it has no inspectable middle.
- Vectorize rather than looping over rows. Use `dplyr` verbs, `apply`/`purrr::map`
  over elements, or matrix operations. An explicit `for` loop over observations is
  almost always the wrong tool.

## Errors and defensive practice

House conventions, adapted from `stata-style.md` because the reasoning is
language-independent.

- **Fail loudly on a violated precondition.** `stopifnot()`, or
  `if (!file.exists(p)) stop("Run 02_clean.R first: ", p, " missing")`. A missing
  input must never yield an empty output.
- **Assert expected state.** Pin row counts, key uniqueness and merge results:
  `stopifnot(nrow(dat) == 615721)`, with a comment on where the figure came from
  and when it was verified.
- **Count before and after anything that changes row counts**, and print the
  ledger. A silent `filter()` is the most common way a result goes wrong unnoticed.
- **Check every join.** State the expected cardinality and verify it. `dplyr`
  joins silently produce a many-to-many fan-out; pass `relationship = "one-to-one"`
  or `"many-to-one"` (dplyr 1.1+) and check for unmatched keys explicitly rather
  than trusting the row count afterwards.
- **Flag, do not delete.** Build `*_flag` columns and filter at the analysis step
  rather than dropping observations during processing.
- Avoid `suppressWarnings()` around anything but a known, commented cause.

## Data handling

- Never hardcode data values (numbers, `tribble()`s, data frames) in an analysis
  or plotting script. They belong in files with provenance. A "temporary" tribble
  becomes permanent. See `data-pipeline.md`.
- Imputation targets missing values only, and `is.na()` appears explicitly in the
  expression. Corrections require authorization and go to a new column. See
  `data-pipeline.md`.
- Check whether a directory has a `pii.txt` marker before reading any data file
  in it, per `data-integrity.md`.
- Be explicit about factors and strings. `stringsAsFactors` defaults to FALSE from
  R 4.0, but do not rely on a reader knowing that; set factor levels deliberately
  where order matters.

## Figures and tables

- **No titles or subtitles baked into a figure.** No `ggtitle()`, no
  `labs(title=)`. Titling belongs to the LaTeX or Beamer context. Panel-level
  sub-labels inside a multi-panel composition are fine. See `data-pipeline.md`.
- Save with `ggsave()` at an explicit width, height and dpi, to a globbed output
  path, never to the working directory.
- Every table and figure gets notes describing source, calculation and a reading
  guide, per `academic-writing-voice.md`.

## Reproducibility

- `set.seed()` for anything stochastic, at the top, stated.
- Scripts are idempotent: running twice gives the same output.
- For work over ~10 minutes, separate the computation phase (which saves to
  `.RData`/`.rds`) from the output phase (which loads and renders), per the global
  learned preference. Never require a multi-hour rerun to change a chart label.
- Record package dependencies in `README_replication.md` in the same change that
  introduces them. Use `renv` where a project warrants pinned versions.
- Prefer `.rds` over `.RData` for single objects: it saves one object under a name
  the reader chooses, rather than restoring names into the global environment.
