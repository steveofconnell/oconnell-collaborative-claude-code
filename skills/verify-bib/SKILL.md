---
description: "Verify every bib entry against published sources, locate soft-copy PDFs, and verify every citation's claim against the PDF body text. Resumable. Works for books too, just more slowly."
---

# Verify Bibliography

End-to-end citation integrity check. For each `.bib` entry: confirm the entry's metadata against a published source, locate a soft-copy PDF (or flag for manual download if paywalled), then verify every claim made about that source in the manuscript body text against the PDF itself. Writes a memory-system report with discrepancies.

This enforces the user's academic integrity directives (no fabricated citations, no claims attributed to sources that don't support them) via workflow rather than self-discipline.

## Input

`$ARGUMENTS` — optional path to a `.bib` file or a manuscript `.tex` file. If omitted, auto-detect:
- Look for `book/references.bib`, `5manuscript/references.bib`, `references.bib`, or `<project>.bib` at project root
- If a single `.bib` file is present, use it. If multiple, prompt.
- For manuscript body, look for `book/main.tex`, `5manuscript/main.tex`, or equivalent

Optional phase flag:
- `--phase 1` — entry verification only
- `--phase 2` — PDF sourcing only (requires phase 1 complete for at least some entries)
- `--phase 3` — claim verification only (requires PDFs in place)
- No flag: run phases in order, stopping at natural checkpoints

## State file

Resumable. State lives at `<project>/.workspace/bib_verification_state.json`:

```json
{
  "bib_file": "book/references.bib",
  "manuscript_files": ["book/main.tex", "book/ch01.tex", ...],
  "pdf_dir": "book/pdfs/",
  "entries": {
    "Author2020": {
      "fields": { "author": "...", "title": "...", "year": 2020, ... },
      "entry_verified": true,
      "verified_at": "2026-04-18",
      "verification_url": "https://...",
      "discrepancies": [],
      "is_book": false,
      "pdf_status": "downloaded|paywalled|not_found|pending",
      "pdf_path": "book/pdfs/Author2020.pdf",
      "pdf_page_count": 42,
      "claims_checked": [
        { "location": "ch03.tex:142", "claim": "...", "status": "supported|partial|unsupported|uncheckable", "notes": "..." }
      ]
    }
  }
}
```

On every run, load state first. Only process entries not yet at the current phase's completion marker. Never re-do completed work unless the user explicitly asks.

## Phase 1 — Entry verification

Goal: confirm each bib entry matches a published source.

For each `@article{...}` / `@book{...}` / `@incollection{...}` / etc. in the `.bib` file, in order of appearance:

1. **Parse fields**: author list, title, year, journal or booktitle or publisher, volume, issue, pages, doi, url.
2. **Web-search** for the source. Build the query from `<first-author-lastname> <year> <short distinctive title words>`. Use `WebSearch`. Strongly prefer results from:
   - Google Scholar
   - The journal or publisher's site
   - The author's academic/personal website
   - Reputable working paper repositories (NBER, SSRN, arXiv, IZA, CEPR, IFS, VoxEU)
3. **Cross-check**. Compare each field in the bib entry to the authoritative source returned by the search. Record one of three outcomes:
   - **Match**: every field consistent.
   - **Discrepancy**: identify each mismatched field and what the correct value appears to be.
   - **Unable to confirm**: no confident match from search. Never guess — record as unable-to-confirm and move on.
4. **Write a silent comment** after the entry's closing `}` in the `.bib` file. BibTeX ignores lines starting with `%` between entries, so:
   ```
   @article{foo2020,
     ...
   }
   % verified 2026-04-18: all fields match. Source: https://...
   ```
   Or:
   ```
   % verified 2026-04-18: DISCREPANCY — bib says pages 201-245, source has 203-245. https://...
   ```
   Or:
   ```
   % verified 2026-04-18: UNABLE TO CONFIRM. No confident match found.
   ```
5. **Update state file.** Mark `entry_verified: true` (with discrepancy notes populated if any) or record the unable-to-confirm status.
6. **Checkpoint every 10 entries.** Print a one-line progress summary ("Entries 41-50 of 312: 9 match, 1 discrepancy, 0 unconfirmed") and continue unless the user interrupts.

**Do not** modify any bib field content. Only add comment lines after closing braces. If a discrepancy is serious (e.g., wrong author, wrong year), add the note and let the user decide whether to edit the entry itself.

## Phase 2 — PDF sourcing

Goal: have a soft-copy PDF on disk for every verified entry, or a tracked TODO for manual retrieval.

For each entry where `entry_verified: true` and `pdf_status != "downloaded"`:

1. **Identify the target PDF**. Preferred sources, in order:
   - Author's academic website (`.edu`, `.ac.uk`, personal site linked from institutional page)
   - Working paper repositories (NBER, SSRN, arXiv, IZA, etc.) — these are usually the author-posted version
   - Institutional repositories (e.g., Harvard DASH, MIT Open Access)
   - Publisher's open-access landing page (if the paper is OA)
   - Google Scholar's "All versions" link for open versions
   - For books: publisher's open sample chapter page, HathiTrust, Internet Archive (for out-of-copyright)
2. **Download**. Use `WebFetch` to retrieve the PDF. Save to `<project>/<pdf_dir>/<entry_key>.pdf`. Create the directory if needed (default `5manuscript/pdfs/` for article-heavy projects, `book/pdfs/` for book projects).
3. **Verify the download**: confirm the file opens, has a nonzero page count, and the first page contains the expected title and authors. If not, the download failed or was a wrong file — mark `pdf_status: "not_found"` and explain.
3a. **Emory library proxy fallback (WebFetch)**. If step 2 finds only paywalled or access-gated URLs, before flagging as paywalled, attempt to fetch through the user's library proxy: prepend `http://proxy.library.emory.edu/login?url=` to the direct URL and try `WebFetch`. If the response contains the expected PDF (check content-type and first-page text), save and proceed as in steps 2-3. If the response is a login/CAS redirect page or HTML, `WebFetch` can't authenticate — continue to step 3b.
3b. **Delegate to Claude Chrome**. When WebFetch can't get through the proxy, write (or append to) a Claude Chrome brief at `<project>/.workspace/claude_chrome_bib_pdf_brief.md`. The brief lists, for each paywalled entry:
    - Bib key
    - Authors, year, title
    - Direct publisher URL
    - Proxied URL (with `http://proxy.library.emory.edu/login?url=` prefix)
    - Target save path (the PDF destination inside the project)
    Instructions in the brief: the user's browser has an authenticated Emory session, so Claude Chrome can navigate to the proxied URL, download the PDF, and save it to the target path. After Claude Chrome finishes, the user reruns `/verify-bib` and phase 2 picks up the newly-saved PDFs (detects them by file presence at the expected path) and proceeds.
    Mark `pdf_status: "paywalled_delegated"` in state; it flips to `"downloaded"` when a subsequent run detects the file.
4. **Add a silent comment** to the bib entry:
   ```
   % pdf: book/pdfs/Author2020.pdf (42 pages)
   ```
5. **If only paywalled versions exist** (publisher requires subscription, only paid preview available, Sci-Hub/LibGen should NOT be used): add to `<project>/.workspace/bib_paywalled_todos.md` a line with both the direct and Emory-proxied URLs:
   ```
   - [ ] Author (2020) — manual download needed.
     - Direct: https://journal.com/article/...
     - Emory proxy: http://proxy.library.emory.edu/login?url=https://journal.com/article/...
   ```
   The proxy prefix (`http://proxy.library.emory.edu/login?url=`) routes the request through Emory's library authentication; when the user logs in with Emory credentials they can download the PDF. Always construct the proxied URL by prepending the prefix to the direct URL — don't URL-encode the inner URL, the proxy accepts it raw.
   Mark `pdf_status: "paywalled"` in state.
6. **If no source found at all**: mark `pdf_status: "not_found"`. Flag to user for manual resolution — they may need to check their own files, contact the author, or reconsider the citation.
7. **Books are slower**. A book PDF may be 300+ MB and only partially available open-access. Many will land in the paywalled or not-found bucket. That is fine — the principle (don't cite what you can't verify) still holds. Books may require the user to supply their own PDF copy into the `pdf_dir`; this skill should detect user-supplied copies on subsequent runs and update state accordingly.

**Never use pirate sites** (Sci-Hub, LibGen, Z-Library). These violate publisher copyright and would taint the research record.

## Phase 3 — Claim verification

Goal: for every sentence in the manuscript body that attributes a claim to a cited source, verify the PDF actually supports that claim.

1. **Scan the manuscript.** Parse every `.tex` file in the manuscript directory. Identify every `\cite{Key}`, `\citep{Key}`, `\citet{Key}`, `\citeauthor{Key}`, etc. Also handle multi-citation commands like `\citep{Key1, Key2, Key3}`.
2. **For each citation instance**:
   - Locate in the manuscript: file and line number.
   - Extract surrounding prose: 1-2 sentences before and 1-2 sentences after the citation. This is the **claim being made about that source**.
   - If the citation includes a page reference (e.g., `\citep[p.~132]{Smith2004}`), record it — claim verification should target those pages.
3. **For each (citation, claim) pair where `pdf_status == "downloaded"`**:
   - Read the PDF. For short articles, read the whole paper. For books or long documents, use the following strategy:
     - If the manuscript cites a specific page, read that page plus two pages of context.
     - Otherwise, read the abstract, introduction, and conclusion first to determine the paper's main claims. If those don't address the manuscript's claim, read section headers / table of contents (for books) to identify the relevant chapter/section.
     - Books in particular: never read the whole book. Use the table of contents plus keyword search (via `Grep` on a `pdftotext` conversion cached to `.workspace/bib_text_cache/<key>.txt`) to locate the passage most likely to support or refute the manuscript claim.
   - For each claim, judge and record:
     - ✓ **Supported**: PDF contains the claim substantively.
     - ⚠ **Partial**: PDF contains a related but weaker / differently-scoped claim.
     - ✗ **Unsupported**: PDF does not support the claim. (High severity.)
     - ? **Uncheckable**: couldn't locate the passage despite reasonable searching. (Flag for user; possibly citation needs a page number.)
4. **Never edit the manuscript text** to fix a claim discrepancy. Report only.
5. **Skip claims where `pdf_status != "downloaded"`**. They stay in state as `claims_checked` entries with `status: "pending_pdf"`.

## Phase 4 — Memory report

At the end of phase 3 (or when phases 1-2 are complete enough to be worth summarizing):

1. Write `<project>/.workspace/memory/bib_verification_report_YYYY-MM-DD.md`. Contents:
   - Summary counts: entries total / verified / discrepancy / unconfirmed; PDFs downloaded / paywalled / not found; claims supported / partial / unsupported / uncheckable / pending.
   - **List every discrepancy** from phase 1 (bib field errors).
   - **List every paywalled item** needing manual download.
   - **List every unsupported or uncheckable claim** (phase 3), with manuscript location, claim text, and best-effort PDF excerpt.
2. Add an entry to `MEMORY.md` (project root) pointing to the report:
   ```
   - [Bibliography verification (YYYY-MM-DD)](.workspace/memory/bib_verification_report_YYYY-MM-DD.md) — N entries verified, M discrepancies, K unsupported claims
   ```
3. Update `.workspace/TODO.md` with any follow-up items surfaced: manual PDF downloads, manuscript claim revisions, bib field corrections.

## Operating notes

- **Resumable by design.** The state file is the source of truth. Every run reloads state and only processes what's not yet done.
- **Never silently accept a citation.** If a source cannot be confirmed and cannot be obtained, say so explicitly and flag in the memory report. The user's academic integrity rules forbid quiet failure here.
- **Never fabricate.** If a search doesn't return a confident match, record "unable to confirm" — do not guess at a DOI, page range, or publisher.
- **Never modify bib field values.** Only add silent comment lines. The user makes content changes.
- **Never modify manuscript body text.** Claim discrepancies are reported, not fixed.
- **Respect paywalls.** No pirate-site retrievals. If paywalled, create a user TODO.
- **Books are slower but follow the same principle.** A 400-page book cannot be read top-to-bottom every time a claim is checked; use table-of-contents navigation, indices, and keyword search on cached `pdftotext` output to locate relevant passages. Cache long-text conversions to avoid redoing the OCR/extraction.
- **Checkpoint frequently.** Bibliographies with 100+ entries take a long time. Pause every 10-20 entries and print a one-line summary. The user can interrupt at any checkpoint.
- **Rate-limit web searches.** If running many entries in a row, don't spam search providers — a brief pause every 10-20 requests is appropriate.
