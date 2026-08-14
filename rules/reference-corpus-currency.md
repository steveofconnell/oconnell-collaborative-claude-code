# Reference Corpus Currency and Provenance

Applies to: any local corpus of external documents held as a reference — a cached
institutional policy library, literature collections, downloaded standards,
guidelines, templates, terms of use, statutes, or sponsor rules. Always-on.

## Why

A cached policy document is a **snapshot**, not the policy. An assessment built on a
superseded version is wrong in the way that is hardest to notice: the reasoning is
sound, the citation is real, and the conclusion is stale. Fuller account:
`casebook/incidents.md` → reference-corpus-currency.

## Rule 1 — Access date always; document date only if the document supplies one

Every item in a reference corpus carries:

- **`retrieved`** — the date the copy on disk was fetched. Always known, always
  recorded, never omitted, never estimated. This is the **"current as of"** stamp
  and it is the one date that is always available.
- **`rev_date`** — the document's own revision, effective, or publication date **as
  stated in the document**. Recorded when the document states one. Left
  **explicitly empty** when it does not.
- **`content_hash`** — a hash of the fetched bytes (or of the extracted text for
  HTML, which carries volatile navigation chrome). This is what makes change
  detectable on the large share of documents that state no date at all.

**Never manufacture a `rev_date`.** It is not inferred from the filename, not
back-filled from the fetch date, not estimated from surrounding context, not
guessed from a "last modified" HTTP header. If the document does not state a date,
the field stays blank and the `retrieved` stamp carries the whole weight. An empty
`rev_date` means "the document states none," never "nobody looked."

When a document carries several dates (effective, last revised, next review),
record the one that governs the text and note the others alongside it. Where the
index format allows, record `rev_date_source` — the page or line it was read
from — so the extraction can be checked rather than trusted.

## Rule 2 — Re-verify before any citation that carries weight

Before a corpus document is cited or relied on in anything that leaves the
session — a manuscript, a memo, a compliance assessment, correspondence, an
application, advice to a student or collaborator — check the source for a newer
version:

1. Read `retrieved`, `rev_date`, and `content_hash` from the index.
2. Re-fetch the source URL. Compare **content hash first** — that works whether or
   not the document is dated. If a `rev_date` exists, compare that too.
3. If nothing changed, update `retrieved` to today. The document is now current as
   of today, and that is worth recording even when the content is identical.
4. If it changed, re-download, re-extract, update all three fields, retain the
   superseded copy (Rule 5), and **re-check the inference** against the new text.
   A newer version does not merely update a citation; it can invalidate the
   conclusion drawn from the old one.
5. If the source is unreachable or gated, say so and cite the cached version
   explicitly as of its `retrieved` date.

For an undated document this is the whole point: we cannot say when it changed,
but we can say it was **unchanged as of** the last verified access, and that any
change happened between that access and now. That bound is what the corpus
provides in place of a revision date, and it is only as good as the frequency of
re-checking.

The check is cheap and the failure it prevents is expensive. Do not skip it
because the document "won't have changed."

## Rule 3 — Cite the snapshot, with its dates visible

Any statement of what an external document says carries its dates in the
citation, in whatever form the medium allows. Dated document:

> University Policy 4.90, rev. 2023-06-14, retrieved 2026-07-23.

Undated document — the common case, and the citation says so plainly rather than
implying a revision date exists:

> Faculty Handbook ch. 14, as published at <URL>, current as of 2026-07-23.

Never present a cached document's content as the current state of the rule
without a date attached. A reader must be able to tell how old the ground under
an assessment is, and whether the age is known precisely (a stated revision) or
only bounded (an access stamp).

## Rule 4 — Staleness is reported, not silently tolerated

When answering from a corpus, state the age of what the answer rests on if the
governing document was retrieved more than roughly six months ago, and flag it
when a domain is known to churn (sponsor terms, tax and immigration guidance,
information-security standards, AI-use guidance). A stale answer given without
its date reads as current, which is the whole problem.

## Rule 5 — Re-crawls update dates; they never overwrite history

A corpus rebuild refreshes `retrieved` and `rev_date` for changed items. When a
document's text changes materially, keep the superseded copy rather than
discarding it — an assessment written against the old version needs the old
version to remain checkable. Retain it under a dated filename and record the
supersession in the index.

## Applying this to an existing corpus

Where a corpus already exists without full date coverage, the gap is recorded as
a known limitation rather than papered over. State how many items carry a
`rev_date` and how many do not, and treat the undated remainder as **bounded only
by its access stamp** — not as unverified, and not as suspect. An undated document
with a recent access stamp is a perfectly good citation; it just carries a
different claim ("unchanged as of X") than a dated one ("revised on Y").

The undated share is expected to be large and is not a defect to be eliminated.
Most institutional web pages state no revision date, and no amount of effort will
make them. Content hashing is the substitute, and it is sufficient.

Backfilling proceeds opportunistically: any document actually used gets re-fetched
and re-stamped at the moment of use, per Rule 2, which puts the effort exactly
where it pays.
