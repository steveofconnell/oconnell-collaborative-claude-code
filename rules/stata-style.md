---
description: "Stata coding style — write idiomatic Stata, do not import Python/R/pandas idioms"
paths:
  - "**/*.do"
  - "**/*.ado"
---

# Stata Coding Style

Applies to: all `.do` and `.ado` files, every project. The governing principle:
**write Stata as Stata.** Stata is its own paradigm with its own idioms and its own
users. Do not transliterate Python, R, pandas, or tidyverse patterns into Stata.
Code that fights the language reads wrong to Stata users and is harder to maintain.
When a generic project rule (e.g. "rename every variable to be long and
descriptive") conflicts with Stata convention, the Stata convention wins for source
survey data; see the naming section.

## The data-in-memory paradigm
- Stata holds **one dataset in memory** and acts on it in place. Think in terms of
  that dataset, not a workspace of many named objects (R) or many DataFrames
  (pandas). Use `preserve`/`restore` and `tempfile` for intermediate states; use
  `frames` only when genuinely holding two datasets at once is needed, not as a
  default multi-object habit.
- A "variable" in Stata is a **column of data**. Programming values are held in
  **macros** (`local`, `global`) and **scalars**. Never call a macro a "variable,"
  and never reach for a Python-style scalar variable where a `local` is meant.

## Vectorized commands, not row iteration
- Operate on whole variables with `generate`/`replace`/`egen`, and across groups
  with `bysort ... : ...`. Do **not** loop over observations to emulate pandas
  `apply` or an R `for` over rows. Stata is already vectorized; row loops are almost
  always a sign of imported thinking.
- Use `foreach`/`forvalues` for looping over **variables, values, or files**, not
  over rows.
- Reach for `collapse`, `contract`, `egen`, `tabstat`, `total` rather than
  hand-rolled aggregation.

## Merging and reshaping the Stata way
- Merge with explicit cardinality: `merge 1:1`, `m:1`, `1:m`, never an unqualified
  join. **Always** check the result (`assert _merge==3`, or inspect, then `drop
  _merge`). This is the survey-data workhorse; ENAHO-style module merges are `m:1`
  or `1:1` on the household/person keys.
- `reshape long`/`wide` for panel/wide transforms, not a pandas-melt mental model.

## Weights, design, and factor variables
- Survey estimation uses `svyset` once, then the `svy:` prefix. Do not hand-build
  weighted means or manual design corrections when `svy:` does it correctly.
- Use **factor-variable notation** (`i.var`, `c.var`, `i.a##i.b`) directly in
  estimation and margins. Do not pre-generate dummy columns the way one would in R;
  let Stata expand them.
- Respect Stata weight types (`pw`, `aw`, `fw`, `iw`) and use the right one.

## Missing values
- Stata missing is `.` (and extended `.a`–`.z`), and **missing is larger than any
  number**: `x > 5` is TRUE when `x` is missing. Guard every comparison that could
  admit missing with `!missing(x)` (or `if x<. `). This is the most common bug when
  importing R/Python comparison habits.

## Naming — source survey variables keep their standard names
- **Do not bulk-rename standardized survey variables into snake_case or "long
  descriptive" names.** ENAHO's `p208a`, `factor07`, `conglome`/`vivienda`/`hogar`,
  CASEN's `e6a`, etc. are the domain lingua franca; renaming them obscures the data
  for the people who use it and breaks correspondence with the official dictionary.
  This is the explicit exception to the global "rename variables to be descriptive"
  rule: that rule targets cryptic *derived* names (`var563`, `val6`) in a project's
  own constructed data, not the published codes of a national survey.
- **Derived variables you create** should be clearly named and **labeled**: give
  every constructed variable a `label variable`, and attach value labels
  (`label define` / `label values`) to categorical constructs. Clarity comes from
  labels and well-named derived variables, not from rewriting the source schema.
- Stata names are case-sensitive, ≤32 chars, lowercase by convention.

## Program/ado abstraction — only for genuine reuse
- A reusable `program`/ado is idiomatic and correct when the *same* computation runs
  across many datasets (e.g. one MPI engine applied to eight countries). Write it as
  a proper program with `syntax`, `local`/`tempvar`/`tempname`, and `rclass`/`eclass`
  returns.
- Do **not** functionalize gratuitously the way one might in Python. A linear,
  well-sectioned do-file is the right unit for a single analysis step; do not wrap
  every few lines in a sub-program.

## Do-file structure and reproducibility
- Header each do-file: a `version` statement, a comment block (purpose, inputs,
  outputs, author), then the body. Use `///` for line continuation and clearly
  delimited `*===`-style section banners.
- Use `tempfile`/`tempvar` for intermediates instead of writing scratch files to
  disk. Use `set seed` for anything stochastic.
- Logging: `capture log close` then `log using ..., replace` at the top of a
  runnable script; close it at the end. Do not litter `set more off` reasoning from
  old Stata — modern Stata defaults handle paging.
- Install dependencies with `ssc install` / `net install` and **document the
  required ado packages in the script header and the replication README** (mirrors
  the data-pipeline rule for packages). There is no Python/R-style import.

## Batch execution and file-output hygiene — HARD RULE (control every output path)
This rule exists because of a documented failure (2026-06-29): running Stata as
`cd "$STATA_DIR" && ./StataMP.app/.../stata-mp -b do X.do` dumped ~60 batch
auto-logs into the **shared Stata install folder on a synced drive**, polluting it
across collaborators. Never again.
- **`-b` batch mode writes an auto-log named `<dofile-basename>.log` into the CURRENT
  WORKING DIRECTORY**, in addition to any `log using` inside the do-file. So the cwd at
  launch determines where that log lands. NEVER launch Stata with the cwd set to the
  Stata install directory (or any shared/synced or tool-install location).
- **Launch Stata MP from a scratch working directory that has the Stata sysdir markers
  SYMLINKED into it.** Stata needs to find its "Stata directory" (the license `stata.lic`,
  the `isstata.*` marker, `ado/`, `utilities/`) — these live in the Stata install
  directory (`$STATA_DIR`),
  NOT inside the `.app` bundle. Launching by absolute path alone from an unrelated cwd
  FAILS SILENTLY: Stata can't find its directory, writes an empty log, exits 0, and the
  do-file never runs (verified 2026-06-29 — an earlier "absolute-path-from-scratch just
  works" claim was a false positive; the body never executed). The robust pattern that
  keeps logs out of the install folder is to make the scratch cwd *look like* a Stata dir
  via symlinks (read-only references into the install — nothing is written there):
  ```
  STATA_DIR="/path/to/your/Stata"      # the folder holding stata.lic, ado/, utilities/
  WORK="<project>/.workspace/scratch/statawork"; mkdir -p "$WORK"
  for m in stata.lic isstata.180 ado utilities; do ln -sf "$STATA_DIR/$m" "$WORK/$m"; done
  cd "$WORK"
  "$STATA_DIR"/StataMP.app/Contents/MacOS/stata-mp -b do "/abs/path/to/script.do"
  ```
  The `<basename>.log` auto-log then lands in `$WORK`, never the install folder.
  ALWAYS verify the run actually executed — check log CONTENT (a known `di` line), not just
  the exit code or that a log file exists. (Adjust `isstata.180` to the installed version's
  marker, e.g. `isstata.150` for Stata 15.)
- **Every persistent output path is explicit, via a global** — never the cwd default.
  Logs: `log using "$logs/..."`. Tables/figures: globbed paths (`$RegResults`,
  `5manuscript/tables/...`). Intermediates: `tempfile`. Assistant scratch do-files: the
  project `.workspace/scratch/` or the session scratch dir — NEVER `/tmp` loosely and
  NEVER the Stata install dir.
- **Clean up after a run**: remove batch auto-logs from scratch when done; never leave
  artifacts in tool-install or shared/synced directories. When cleaning, delete only
  files this session created (check mtime/ownership) — never another project's outputs.

## Output the Stata way
- Tables: `esttab`/`estout`, `putexcel`, `collect`/`table`. Figures: `twoway`,
  `graph`. Do not carry a ggplot mental model into Stata graphics; use Stata's
  graph grammar and save with `graph export`.
- The data-pipeline rule still holds: no figure titles baked in via `title()` when
  the title belongs in the LaTeX/Beamer caption; no hardcoded data values in do-files.

## What "don't treat Stata like Python/R" rules out (quick list)
- Row-wise loops to compute column values → use `gen`/`egen`/`bysort`.
- Holding many datasets as named objects by default → one dataset in memory + `tempfile`.
- Calling macros "variables" / data columns "fields."
- Pre-generating dummy variables for regression → factor-variable notation.
- Bulk-renaming official survey codes to snake_case.
- Unguarded comparisons that mishandle `.` as a large value.
- Wrapping trivial steps in functions/programs out of habit.
- `import`-style dependency thinking → `ssc install` + documented header.

# Stephen's house conventions (extracted from his own project code, 2026-06-29)

These are his actual, durable Stata conventions, taken from four archived projects
(IndiaPowerShortages/AER 2016, Reservations, Baruch_Hybrid, EBC). Follow them; they
take precedence over generic defaults. Dated markers to modernize are listed at the end.

## Project scaffolding
- **A master "code header" do-file**, included/run first by every script: `clear`,
  `clear matrix`, `clear mata`, `cap log close`, then cross-user root detection so the
  code runs on any collaborator's machine —
  `if "`c(username)'"=="soconn8" { global root "..." }` / `else if ... ` / an `else`
  that errors telling a new user to add their username — then `include` the paths file.
- **A single "set paths" file** included everywhere: a `version` statement,
  `assert "$root"!=""` (fail loudly if root capture failed), folder globals, `set seed`,
  and `global date=c(current_date)` / `global time` used to stamp log filenames.
- **One centralized globals file** (his `DefineGlobals.do`) holding shared varlists and
  design constants — `$covariates`, the cluster variables, indicator lists, the
  instrument — each with a one-line rationale comment, so a specification is changed in
  ONE place and never drifts across scripts.
- **A `subroutines/` library** of reusable, non-numbered do-files pulled in with
  `include` (when macros/globals must persist) or `qui do` (self-contained prep).
- **Numbered, stage-prefixed scripts**, letters for source-specific sub-steps and spec
  families: `01a_read…`, `01b_read…` → `03_merge…` → `05_analysis…`, with a `FE` infix
  for a specification family. Funnel shape: many source readers → fewer assembly scripts
  → one estimation driver per analysis dataset plus per-spec robustness siblings. (Map
  this onto the standard `1rawdata/2processing/3data/4code` tree; do not recreate his old
  `01.Data/02.Programs` numbering when a project already uses the standard one.)

## Defensive helpers he defines and reuses (carry these forward)
- `repl_conf` — a "replace … if" that **errors if zero observations match**
  (`if r(N)==0 { di as err "NO MATCHES -- NO REPLACE" exit 9 }`) and reports how many were
  replaced. Reach for it on any conditional replace where a silent no-op would be a bug.
- `drop_conf` — same idea for drops.
- `checkmerge3` — after a merge, assert/keep `_merge==3` (or master+matched), then drop
  `_merge`. `checkmergevar` — a pre-merge diagnostic reporting non-matching keys.
- **Obs-count bookkeeping around every drop**: `local count_orig=_N` … `count` …
  `dis "orig `count_orig'… final `count_final'"` — an attrition ledger printed to the log.
- **`assert` tripwires** pinning expected pipeline state (`assert _N==615721`,
  `assert permid!=.`) so the run fails loudly if upstream data changes.
- **`cap` prefix** for idempotent commands (`cap drop _merge`, `cap log close`,
  `cap program drop`, `cap encode`).

## Data prep idioms
- `g` (not `generate`); indicators as boolean expressions or `cond()`
  (`g elec = q>0 & q!=.`). Explicit `replace … if` chains with an inline `//` justification,
  not `recode`.
- **Dense labeling**: `la var` on essentially every constructed variable, often a dedicated
  `labelvars.do` of nothing but `label var` lines, with a **provenance prefix in the label
  text** (e.g. `"IR: …"` raw institutional record, `"IRc: …"` cleaned, `"Exp: …"`
  experiment-assigned). Value labels via the `lab def` + `lab values` pair.
- **Typed merges, always** with a mandatory keep/assert and `nogen`, pulling only needed
  columns: `merge m:1 key using "…", assert(3) nogen keepusing(…)` /
  `keep(match master)`. Never an untyped or unchecked merge.
- `preserve … collapse/keep/duplicates drop … tempfile … save … restore` for side
  computations; named intermediate `.dta` at meaningful stages with `compress` +
  `label data "…"` immediately before `save … , replace`.
- **Flag-don't-delete**: build `*_flag` / `neg_*_flag` indicators and filter at estimation
  (`if …_flag<3.5`) rather than dropping observations early.

## Comments and sections
- Every do-file: the asterisk banner header, then a filename + one-line purpose comment
  (`/* 05_peru_mpi.do */` then `* what this file does`).
- Section headers: a row of `*****` then a CAPS title. Inline `//` comments **carry the
  reasoning and provenance of every judgment call** (including external references —
  "REFER TO … EMAIL", "this is an errant code; replace into neighbor"). This is a signature;
  keep it.

## Estimation
- **`reghdfe` is the workhorse**: `reghdfe y x [pw=wt], absorb(fe) cluster(clustervars)`.
  Factor variables for any remaining dummies (NOT `xi: i.state`).
- **Clustering is set once in a global and reused across every spec**, never varied
  opportunistically: `global FEClusterVars "panelgroup statenumxyear"`. Cluster IDs built
  with `egen group()`. (This matches the global "defer on clustering level" rule — he fixes
  the level and holds it; do not propose alternatives.)
- **Population weights are routine** (`[pw=…]`, `[pweight=…]`); for survey estimation use
  `svyset` + `svy:` (this project). IV via the `ivreg2`/`xtivreg2` family with `first`/`ffirst`.

## Output
- **Tables: `esttab`/`estout`** with `eststo`/`eststo clear`, a fixed template —
  `star(* .1 ** .05 *** .01) b(%9.3f) se(%9.3f) label nogaps style(tex)` — and
  **self-contained table notes written inline as a LaTeX `minipage`** stating estimator, SE
  type, clustering, and the significance legend. Multi-panel via `append` + `posthead`.
  Summary stats via `sutex`. Output always written to a globbed path
  (`$RegResults`, `5manuscript/tables/`), never the working dir.
- **Figures: base `twoway`/`line`/`scatter`**, `graphregion(color(white))` on every graph,
  **no embedded titles** (titling on the LaTeX side, per the figure rule), `graph export …
  , replace` to PDF.

## Reproducibility scaffolding
- `set seed` always; `cap log close` then a **date/time-stamped** `log using`; `compress` +
  `label data` before every `save`.

## Dated markers — modernize, do not copy
- `version 12`, `set matsize`, `set maxvar` → drop (Stata 16+ auto-manages).
- `#delim ;` used only to cram the username block onto one line → keep `#delim cr`; a clean
  multi-line `if/else` username block (or `$dbroot` from his Stata profile) supersedes it.
- Windows `"C:/…/My Dropbox/…"` paths and mixed `/`+`\` separators → forward slashes only.
- `xi: i.state` → native factor variables. `outsheet`/`insheet` → `export/import delimited`.
  `saveold`, `.eps` export → `save`, PDF. Version-and-date-in-filename → rely on VCS; do not
  carry his `_jan2014` / `_EER_Submission` filename tagging or left-in "conflicted copy"
  duplicates and commented-out dead-code blocks into new work.
