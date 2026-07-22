# Data Pipeline Integrity

Applies to: scripts in `2dataProcessing/`, `3dataAnalysis/`, `4code/`, and any R/Python/Stata scripts that produce data or figures.

## No embedded titles or subtitles in figures
Never add overall figure titles or subtitles via `ggtitle()`, `labs(title=..., subtitle=...)`, or `plot_annotation(title=..., subtitle=...)`. All figure titles are handled by the LaTeX/Beamer context (`\frametitle`, `\caption`, `\subcaption`). Embedding titles in the PNG creates duplication and prevents the figure from being reused across slide decks, papers, and appendices without re-rendering.

Panel-level sub-labels within multi-panel patchwork compositions (e.g., `"A. Total Farms"` passed through `plot_es_panel(title="A. Total Farms")`) are acceptable — these label individual panels, not the figure as a whole.

Helper function signatures should use `title = NULL` as the default (not remove the parameter entirely), so call sites that pass sub-panel labels positionally continue to work.

## No data in analysis scripts
Never hardcode data values (numbers, tibbles, tribbles, dataframes) inside analysis or visualization scripts. All data must live in files under `1rawdata/` or `3data/` with source documentation. If a script needs data that isn't in a file yet, create the file first — don't embed a "temporary" tribble. Temporary tribbles become permanent.

## Every raw data directory needs source.txt
When creating or populating a subdirectory under `1rawdata/`, always create a `source.txt` documenting: what the data is, where it came from (URL, agency, contact), when it was obtained, access conditions, and any known issues. No raw data file should exist without provenance documentation.

## API keys and credentials
Never hardcode API keys, passwords, or credentials in scripts. Use environment variables with a documented fallback (e.g., `Sys.getenv("KEY", unset = "default")`). Document the required environment variable in the script header and in `README_replication.md`.

## Figure paths in LaTeX
When a LaTeX document sets `\graphicspath`, all `\includegraphics` calls must use paths relative to that setting — never prepend the graphics path directory name. Inconsistent path conventions compile by accident but break on directory changes.

## Script outputs referenced in manuscripts
When a script produces values that are cited in manuscript text or hardcoded in LaTeX tables, add a comment in the tex source pointing to the script and output file (e.g., `% Source: 3dataAnalysis/ParityPricePanel/03_exposure_index_regional_analysis.py`). When creating or modifying a table in tex, check whether the values should be auto-generated or at minimum verified against script output.

## README and documentation must track the code
When modifying a script's inputs, outputs, or dependencies, check whether `README_replication.md` or equivalent documentation references the old state. Update documentation in the same commit as the code change. Stale documentation is worse than no documentation — it actively misleads.

## Software dependencies
When a script uses a package not already listed in `README_replication.md` software requirements, add it immediately. Don't assume the replicator will figure it out from error messages.

## Value-level data integrity: imputation vs. correction — CRITICAL

**This section exists because of a documented failure.** A prior session overwrote existing data values when the instruction was to impute missing values, silently destroying valid observations. This is data manipulation and constitutes research malpractice.

**The core distinction:**

- **Imputation** — filling in values where the data are missing (`NA`, `.`, blank). Only ever apply imputations to missing values. A line like `df$x <- ifelse(is.na(df$x), 0, df$x)` is correct. A line like `df$x <- 0` or `df$x[condition] <- 0` that can overwrite non-missing values is not imputation — it is data manipulation.
- **Correction** — changing a value that exists but is wrong (e.g., a data entry error). This is fundamentally different from imputation and requires explicit authorization. Never apply a correction unless the user has specifically asked for it, identified the affected records, and confirmed the correct values.

**Absolute rules:**

1. **Never overwrite existing data values.** Before writing any assignment to a variable in a processing script, check that the left-hand side condition — whether an `ifelse`, a `mutate`, a `replace`, a bracket subset, or any other construct — cannot evaluate to `TRUE` for a row where the variable already has a non-missing value. If it can, stop and ask.

2. **Imputations target `NA` (or `.` in Stata) only.** The condition `is.na(x)` (R) or `mi(x)` / `x == .` (Stata) must appear explicitly in any imputation expression. An imputation without an explicit missing-value condition is a red flag.

3. **Corrections require explicit authorization and a new variable.** When the user explicitly authorizes a targeted correction (e.g., to fix a data entry error), do not overwrite the original variable. Save the corrected values in a new variable with a recognizable name — e.g., `income_corrected`, `age_adj` — and leave the original untouched. Document the correction in a comment: what was changed, why, and on which records.

4. **State what you are doing before writing imputation or correction code.** Before writing any line that modifies data values, state: (a) which variable is being changed, (b) which rows are affected (the condition), (c) whether those rows are guaranteed to be missing, and (d) what the new value will be. If you cannot answer all four, do not write the code.

5. **Clean-looking output from messy data is a red flag.** If a dataset has many missing values before processing and none afterward, verify that each imputation was applied only to missing values and that no existing values were silently overwritten.

## Logs and machine output must be genuine — never hand-assemble a log

A log or run transcript (Stata `.log`, R/Python console output, build log, estimation output, "validation output" file, any artifact that represents "what the computer did when this ran") is a **computer-written record of an actual execution**. It is never something you author, assemble, or curate by hand.

**This section exists because of a documented failure.** A "validation output" file meant to show a single run of a script had been hand-assembled from excerpts of more than one run, with a hand-written header. The stitched pieces were internally inconsistent (a subgroup table reported more observations than the full-sample table), which read as an error and cost a round of investigation — the numbers were actually correct; the file was the problem. A genuine single-run log would never have looked that way.

**Absolute rules:**

1. **Never hand-assemble, stitch, splice, reorder, retype, or fabricate a log.** Do not combine output from different runs into one "log." Do not paste a hand-written narration and label it a log. Do not edit values, counts, or results inside a log.
2. **To produce a log, run the code and capture the real output.** If you need a log/validation file, actually execute the script (with `log using`, or by redirecting console output) and use what the machine writes, start to finish, from one run.
3. **A log must correspond to exactly one real execution of the exact artifact shipped.** If the code changes, re-run it; do not patch the old log to match.
4. **The only permitted post-processing of a genuine log is sanitization that removes local absolute paths or secrets** (e.g., replacing `/Users/<name>/...` with a `<root>` placeholder), and, if length requires it, keeping a **contiguous** genuine excerpt while stating that it is an excerpt. Never present a non-contiguous stitch as a run.
5. **If a real log cannot be produced** (no license, no data, environment missing), say so and hand the user an empty/placeholder with that stated — never a fabricated one.

## Never write deliberately-wrong or test values into real data

Never write a value you know to be wrong — a test string, a dummy number, a
deliberate blank, a "does this round-trip" placeholder — into a real dataset, a
live production sheet, a database, or any store that feeds analysis, **even to
verify that software behaves correctly**. Verifying app/pipeline behavior is not a
license to pollute the data.

- Verify on a **throwaway copy**, a scratch row/table you fully control and delete,
  a local fixture, a staging store, or by **code inspection** — never by writing
  known-wrong values into the real data.
- This is strongest for **shared/live data others are actively using** (a
  collaborator's review sheet, a production DB): a test write there both corrupts a
  record and disrupts the other person's work.
- If the only "verification" available would require a bad write, say so and fall
  back to the code trace; do not do the write.

This is the sibling of the genuine-logs rule above: machine output is captured from
real runs, and real data carries only real values.
