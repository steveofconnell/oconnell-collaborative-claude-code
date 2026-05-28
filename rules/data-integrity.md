---
description: "Rules for data transcription from visual sources and digitization project infrastructure — prevents fabrication of data values"
globs: ["*.csv", "*.xlsx", "*.xls", "*.tsv", "*.R", "*.py", "*.do", "*rawdata*", "*processing*"]
---

# Data Integrity: Transcription and Digitization

## PII Signpost Convention

Data files are assumed de-identified unless a `pii.txt` marker file is
present in the same directory. Before reading any data file (CSV, Excel,
Stata, RDS, etc.), check for `pii.txt` in the file's directory.

**If `pii.txt` exists:**

The directory contains identifiable human subjects data. Do NOT read data
files in this directory. Instead, use one of the safe patterns:

  a. Read the codebook, data dictionary, or `source.txt` — not the data.
  b. Read only the header row (e.g., `head -1 file.csv` via Bash).
  c. Ask the user to describe the structure verbally.
  d. Read a de-identified extract from a different directory.
  e. Ask the user to provide synthetic example rows.

The `pii.txt` file itself should describe what is sensitive (e.g., "Contains
GPS coordinates, respondent names, household IDs"). Read `pii.txt` to
understand which fields are identifying — this informs which columns are
safe to reference by name in code and which must never appear in context.

**If no `pii.txt` exists:**

Assume the data is de-identified or non-sensitive. Proceed normally — read
the file, inspect contents, write code against actual values as needed.

**When creating raw data directories** for human subjects projects, always
create a `pii.txt` alongside `source.txt` if the data contains any
identifiable information. The `pii.txt` file is a one-time setup cost that
protects the data for every future session.

## Data Transcription and Visual Source Reading — CRITICAL
**This section exists because of a documented failure.** In a prior session, Claude generated plausible-looking numerical data when reading degraded microfilm scans, producing values that were internally consistent and reasonable-looking but factually wrong. These fabricated values entered a research dataset and were only caught through manual spot-checking against source documents. This is an unacceptable failure mode that can corrupt research data and damage the user's professional reputation.

**Absolute rules when reading values from images, scans, PDFs, or any visual source:**

1. **Never fabricate or interpolate values.** If a number cannot be read from the source with reasonable confidence, report it as unreadable. Do not generate a plausible-seeming value. Do not fill in a gap with a number that "looks right" in context. A blank cell is infinitely better than a fabricated number.

2. **State confidence explicitly for every value read.** When transcribing from a visual source, mark each value as: (a) clearly legible, (b) probable but uncertain — state what it looks like and what alternatives are possible, or (c) illegible — do not attempt a value.

3. **Never silently produce a complete, gap-free dataset from a degraded source.** A clean-looking output from a dirty input is a red flag. If a scan is degraded, the transcription should have gaps, uncertainty markers, and explicit notes about illegibility. If the output looks too clean, something is wrong.

4. **Record provenance for every transcribed value.** Every value entered from a visual source must have: the source filename, the page number, and (ideally) the row/column identification within the table. If you cannot specify exactly where a value came from, do not enter it.

5. **Flag when row identification is ambiguous.** Dense tables (e.g., multiple tobacco subtypes, regional breakdowns) are high-risk for reading the wrong row. When a table has many similar-looking rows, explicitly confirm which row is being read before transcribing values. If the row label is illegible, stop and say so.

6. **Never continue past an error silently.** If partway through a transcription you realize a value might be wrong, stop, flag it, and reassess. Do not keep going and hope it averages out.

7. **Prefer leaving work for the user over fabricating data.** If a scan is too degraded to read reliably, say: "I cannot read this reliably. The user should verify these values against the physical source." This is always the right call when confidence is low.

## Data Digitization Projects — Required Infrastructure
Any project involving digitization of data from visual sources (scans, PDFs, microfilm, photographs) must include the following as integral components, not afterthoughts:

**PREREQUISITE — Confirm non-existence of digitized source.** Before embarking on any data digitization effort, vigorously confirm that the target data series does not already exist in machine-readable form. This means: searching ERS/NASS data products, FRED, ICPSR, Dataverse, relevant university research centers (farmdoc, CARD, etc.), CRS/CBO compiled tables, and any discipline-specific data repositories. Check not just the obvious sources but also yearbook Excel files that may contain unlabeled tables, and supplementary data appendices of published papers that use similar data. Document the search and its negative results before proceeding. A digitization project that duplicates an existing dataset is wasted effort and a reputational risk. Even if no machine-readable version exists, also search for the **best available source document** to digitize from — a cleanly typeset ERS staff report with comprehensive tables is far preferable to degraded microfilm scans of the same data scattered across multiple yearbook editions. Compile a source inventory before transcribing a single number.

1. **Source traceability.** Every digitized record must carry the source filename, page number, and (where applicable) table/row/column identification. If a value cannot be traced to a specific location in a specific source document, it does not belong in the dataset.

2. **Verification status tracking.** Every record must have a verification status field indicating: unverified, verified_correct (human-checked, value confirmed), or corrected (human-checked, value was wrong and has been fixed). No dataset should be treated as final until all records are verified.

3. **Human verification process.** A systematic process for human review must be designed and built as part of the digitization pipeline — not deferred to "later." This includes: a review interface or workflow, documentation of what has been checked and by whom, and error rate tracking by source and confidence level. The review process should be designed before large-scale extraction begins.

4. **No silent completion.** When a digitization task is finished, the output must include a summary of: total records extracted, records by confidence level, records with known issues, and the proportion requiring human verification. A digitization that reports "done, N rows extracted" without this context is incomplete.
