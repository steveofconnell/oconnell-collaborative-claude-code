---
description: "Guardrails against script proliferation — fires when creating or editing R, Python, or Stata scripts"
globs: ["*.R", "*.py", "*.do"]
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

- **Processing (`2processing/`)**: 6-12 scripts is typical, depending on number of raw data sources. One script per source or closely related source group.
- **Analysis (`4code/`)**: 3-6 scripts. One baseline + one robustness per analysis dataset, plus graph/table scripts if needed.

If a folder exceeds these ranges, audit for consolidation opportunities before adding more.

## Refactoring protocol

When consolidating scripts:
1. Archive originals to `archived_pre_refactor/` in the same directory
2. Write `ARCHIVE_MAP.md` documenting old → new mapping, bug fixes applied, and new pipeline order
3. Use a `new_` prefix during development; rename to final name after testing
4. Test the consolidated script before removing originals
