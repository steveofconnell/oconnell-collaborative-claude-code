---
description: "Research project folder structure, script naming, variable naming, and data organization conventions"
---

# Data and Project Organization

The organizing principles are: **self-evidence** (filenames, variable names, and folder structure should be interpretable without external explanation), **reproducibility** (any output traceable back to unaltered raw data via code), **transparency** (no undocumented manual steps), and **seamless multi-user and multi-device compatibility** (a collaborator or the user on a different machine can pick up the project and understand it immediately). The system should resist the tendency to dump all file types and versions into a single location and rely on search later — every file's purpose and stage should be apparent from where it lives. The exception is `.s-workspace/`, which is explicitly the catch-all for working drafts, exploratory output, curiosities, and temp files that don't yet have a permanent home.

## Standard folder structure
`0admin/` (IRB, grants, correspondence, project management), `1rawdata/` (source data, never modified), `2processing/` (cleaning/construction code — scripts that transform raw data into analysis-ready datasets), `3data/` (analysis-ready datasets, output of processing code), `4code/` (analysis scripts, numbered sequentially — output goes directly to `5manuscript/tables/` and `5manuscript/figures/`), `5manuscript/` (drafts, .tex/.md files, `tables/` subfolder, `figures/` subfolder). When generating a table or figure and it is not clear whether it is intended for the manuscript, ask: "Manuscript output, or just exploratory?" Manuscript output goes to `5manuscript/tables/` or `5manuscript/figures/`; exploratory output goes to `.s-workspace/`. Create these directories when starting a new research project. Intermediate/temp files go in `.s-workspace/`.

## File and folder naming
- No spaces in file or folder names. Use underscores.
- Raw data and source PDFs go in `1rawdata/` (with descriptive subfolder), not `.s-workspace/`.

## Script naming and organization
- Within each code folder (`2processing/`, `4code/`), name scripts with numeric prefixes that reflect pipeline order: `01_clean.R`, `02_merge.R`, `03_regress.R`, etc. The numbering makes execution order self-documenting within that stage. When creating a new script, check existing files in that folder and assign the next number in sequence. If a script is inserted between existing steps, use an intermediate number (e.g., `02a_geocode.R`) rather than renumbering everything.
- One script, one task. Each script should do one step of the pipeline (read, clean, merge, geocode, regress, etc.). Do not combine data preparation and analysis in the same file.

## Pipeline architecture — the funnel principle
The pipeline should be shaped like a funnel: many source-specific read/clean scripts at the top → fewer merge/assembly scripts in the middle → one baseline + one robustness script per analysis dataset at the bottom. Script count should decrease at each stage, not stay flat or grow. Linear chains — where each script's sole purpose is to incrementally transform the previous script's output — are the primary symptom of over-splitting and must be consolidated into one script with labeled sections. See `rules/script-architecture.md` (scoped to `.R`, `.py`, `.do`) for operational guardrails.

## Variable and dataset naming
- Descriptive variable and dataset names. Never leave cryptic or indexed names (`var563`, `val6`, `hh`, `person`) — rename variables early in processing to be long and descriptive. Do not rely on variable labels as a substitute for clear names.

## Self-containment and raw data documentation
- Projects are self-contained. Never copy prepared datasets from another project into a new one. All data preparation must be reproducible from raw data within the project.
- Every file in `1rawdata/` must have source documentation: a `source.txt` note, a `documentation/` subfolder, or equivalent. No raw data file should exist without a record of where it came from, when it was obtained, and any access conditions. When downloading or receiving data, create this documentation immediately. Consider making raw files read-only to prevent accidental modification.
