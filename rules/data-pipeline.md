# Data Pipeline Integrity

Applies to: scripts in `2dataProcessing/`, `3dataAnalysis/`, `4code/`, and any R/Python/Stata scripts that produce data or figures.

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
