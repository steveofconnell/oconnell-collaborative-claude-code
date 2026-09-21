---
description: "Guardrails against script proliferation — fires when creating or editing R, Python, or Stata scripts"
paths:
  - "**/*.{R,r,Rmd,qmd}"
  - "**/*.{py,ipynb}"
  - "**/*.{do,ado}"
---

# Script Architecture Guardrails

## Before creating a new numbered script

Stop and answer these three questions:

1. **Is this script's only input the output of the previous script?** If yes, it should be a new section in that script, not a new file. Linear chains (A→B→C where each step only feeds the next) are the primary symptom of over-splitting.

2. **Will any other script also consume this script's output?** If no — if only one downstream script reads it — there is no reason for the intermediate file to exist. Fold the logic into the consumer.

3. **Does this step take >2 minutes to run?** If yes, a separate script is justified so downstream iteration doesn't require rerunning it. If no, the runtime cost of combining is negligible.

A new script is justified when the output is a **shared intermediate** (consumed by multiple downstream scripts), or the step is **expensive** (worth caching), or the task is **conceptually distinct** (cleaning source A vs. cleaning source B; data processing vs. statistical analysis). If none of these hold, add a section to an existing script.

## Section structure within scripts

When a script has multiple logical phases, use clearly labeled sections:

```r
# =============================================================================
# A. DESCRIPTIVE SECTION TITLE
# =============================================================================
```

Each section should be runnable in sequence but conceptually self-contained. This gives the readability benefits of separate files without the proliferation cost.

## Script count targets

- **Processing (`2processing/`)**: 4-8 scripts, depending on the number of raw data sources. One script per source or closely related source group.
- **Analysis (`4code/` or a manuscript code folder)**: 3-6 scripts. One baseline + one robustness per analysis dataset, plus one tables-and-figures script.

**Hard limit: 8 scripts per folder,** enforced by the `guard-new-scripts.py` hook, which also
refuses any new script file that lacks the user's approval line (see `project-structure.md`,
"New script files"). A folder at the limit is consolidated, not extended.

## Variants, checks and referee responses are options, not files

The common way a folder reaches dozens of scripts is not linear chains but variants: a
`_clustered` copy, a `_pooled` copy, a `_withX` copy, a `_Note` copy for a different table
note, a `promote_` script that copies another script's output into the manuscript, and one
new file per diagnostic or per referee question. Each of these belongs inside an existing
script:

- **A variant** (clustering level, pooling, sample subset, estimator) is an argument or a
  loop over specifications in the parent script, with every specification written to the
  same output.
- **A table-note or formatting change** is an edit to the script that writes the table.
- **Output destined for the manuscript** is written there by the script that produces it.
- **Diagnostics, placebo and permutation checks, and referee-response checks** go into the
  analysis dataset's one robustness script, one labeled section each.

## Refactoring protocol

When consolidating scripts:
1. Archive originals to `archived_pre_refactor/` in the same directory
2. Write `ARCHIVE_MAP.md` documenting old → new mapping, bug fixes applied, and new pipeline order
3. Use a `new_` prefix during development; rename to final name after testing
4. Test the consolidated script before removing originals
