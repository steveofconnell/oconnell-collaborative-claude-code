#!/usr/bin/env python3
"""PostToolUse hook: flag acronyms and initialisms used in prose without an
expansion at first use.

Added 2026-07-24 after a funding proposal used "DTM" five times with no
expansion anywhere in the document. The convention checked for is the standard
one: the term is written out once, with the initialism in parentheses, e.g.
"Displacement Tracking Matrix (DTM)". If "(XYZ)" never appears in the file but
XYZ does, the term is undefined.

Non-blocking. Exits 2 so the message reaches Claude as feedback, after the edit
has already been written. Never prevents a write.
"""
import json
import os
import re
import sys

PROSE_EXT = {".tex", ".md", ".qmd", ".Rmd", ".rmd", ".txt"}

# Skip scaffolding: notes to self, task files, config. These are working files,
# not documents anyone else reads.
SKIP_PATH_PARTS = (
    "/.workspace/", "/.claudeconfig/", "/.claude/", "/node_modules/",
    "MEMORY.md", "TODO.md", "SESSION_LOG.md", "CLAUDE.md", "README",
    # Provenance maps written during a refactor (old->new tables full of
    # cross-reference labels like "Q3", "A7", "E2"). Working scaffolding, not
    # prose anyone reads cold. Added 2026-07-31.
    "MAPPING.md", "ARCHIVE_MAP.md",
)

# Universal in the user's venues (applied micro / development / labor) or in
# ordinary administrative English. Never flagged.
WHITELIST = {
    "OLS", "GDP", "GNP", "RCT", "IRB", "SD", "SE", "CI", "ATE", "ITT", "LATE",
    "IV", "FE", "DID", "DD", "RD", "RDD", "GMM", "MLE", "TSLS", "OLS", "AER",
    "QJE", "JPE", "JEL", "NBER", "AEA", "IPA", "MIT", "PHD", "PI", "CV", "FAQ", "URL",
    "PDF", "CSV", "XML", "HTML", "API", "CLI", "GPS", "ID", "IDS", "OK",
    "US", "USA", "UK", "UN", "EU", "NGO", "NGOS", "GIS", "ML", "AI", "IT",
    # Currency codes read as plainly as "US" above; no economics paper writes
    # "United States dollars (USD)". Added 2026-08-10. Note that PPP is
    # deliberately NOT here: it is genuine jargon and should be flagged if it
    # ever reaches prose.
    "USD", "LBP", "EUR", "GBP",
    "TODO", "TKTK", "AND", "OR", "NOT", "THE", "A", "I", "II", "III", "IV",
    "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII",
    # Standard legal/business-contract abbreviations — never spelled out in
    # this venue's drafting (operating agreements, LLC filings): LLC, CPA,
    # IRC, UCC, and US state postal codes read as plainly as "US"/"UK" above.
    "LLC", "LLCS", "CPA", "CPAS", "IRC", "UCC", "GA", "EIN", "SSN", "IRS",
    # "WC" only ever appears here as part of "Form WC-10", a Georgia agency
    # form number (like "Form 1065") — not a standalone acronym to expand.
    "WC",
    # "MS" as an archival collection identifier ("MS 463", "MS 1094") is the
    # universal citation form for a manuscript collection and is never spelled
    # out in humanities or archival writing. Also covers the US state postal
    # code. Added 2026-08-04 while drafting the ACLS narrative, where forcing
    # the "Manuscript (MS)" pattern made the sentence worse than the acronym.
    "MS", "MSS",
    # "DC" in "Washington DC" is an address element, and JSTOR is the name of
    # the archive rather than an initialism anyone expands in academic prose.
    # Added 2026-08-13 from book/literature/ source notes.
    "DC", "JSTOR",
    # "CD" only ever appears as part of "Form CD 030", a Georgia Secretary of
    # State form number, on the same footing as "Form WC-10" above.
    "CD",
    # Course subject prefixes in syllabi and course materials ("ECON 320"
    # as a course number, or as a required e-mail subject tag). A course code
    # is a proper name, not an initialism to expand. Added 2026-07-31.
    "ECON", "MATH", "QTM", "STAT",
    # Clock, calendar and measurement notation: "5:00 PM", "EST", "25 MPH".
    # Nobody expands these. MPH added 2026-08-10 from a traffic-engineering
    # status log; it is on the same footing as AM/PM.
    "AM", "PM", "EST", "EDT", "UTC", "MPH", "KPH", "KM", "MI", "FT", "SQFT",
    # Registrar section-type and section identifiers as printed in the course
    # listing ("LEC", "LAB2", "DIS1"). Identifiers, not initialisms.
    "LEC", "LAB", "LAB1", "LAB2", "LAB3", "LAB4", "DIS", "DIS1", "DIS2",
    # Standard undergraduate-econometrics notation (Wooldridge). These are the
    # field's working vocabulary and appear unexpanded in every textbook,
    # lecture and exam: assumption labels ("SLR.1", "MLR.5"), the regression
    # functions, the sum-of-squares decomposition, and the usual estimators
    # and diagnostics. Same footing as "OLS" above. Added 2026-07-31.
    "SLR", "MLR", "SLRM", "MLRM", "PRF", "SRF", "TSS", "ESS", "RSS",
    "LPM", "VIF", "FWL", "BLUE", "OVB", "WLS", "FGLS", "GLS", "AME",
    "LLN", "CLT", "HC", "HC1", "HC3",
    # Course-material item labels: the ECON 320 graded assignments ("A1 (OLS)
    # due Monday") and the in-class project building blocks ("BB3 Model &
    # mechanisms"). Identifiers on the same footing as "LAB2" above, and they
    # ARE defined in the syllabus table that introduces them. In this course
    # A1-A5 is additionally overloaded onto the Gauss-Markov assumption labels
    # ("assumptions A1-A4"), which is textbook notation nobody expands either.
    # This deliberately narrows the `[A-Z]\d{2,}` rule's note at the call site
    # about keeping "A1" in scope: single-letter+single-digit labels are still
    # checked in general, just not these known course identifiers.
    # Added 2026-08-06 while drafting the A1-A5 assignment handouts.
    # A6 added 2026-08-10: the course moved off Wooldridge's SLR.n / MLR.n
    # labels onto a single A1-A6 list, so the normality assumption is now A6.
    "A1", "A2", "A3", "A4", "A5", "A6",
    "BB1", "BB2", "BB3", "BB4", "BB5",
    # Universal in this venue and never written out in economics prose.
    "IQ",
    # Literal date-format placeholders in blank contract fields
    # ("[YYYY-MM-DD]"), not acronyms.
    "YYYY", "MM", "DD",
    # AGS ground-screw model/SKU numbers — proper nouns, not initialisms;
    # already defined by their full spec label in Exhibit B (e.g. `IM3316 ·
    # 3"×63"`, `IF663 6x6 U-flange`).
    "IM3316", "IM3320", "IF443", "IF663",
    # SUTVA is the field's working vocabulary in applied micro, on the same
    # footing as "OLS" and "ITT" above; it appears unexpanded in the journals
    # this work targets. Added 2026-07-31.
    "SUTVA",
    # Names of funders, host institutions and seminar venues as they appear in
    # acknowledgments. These are proper nouns, not technical initialisms a
    # reader has to decode, and the venue FULL NAMES are separately tracked for
    # verification before submission (TKTK ACK in the ILA manuscript, added
    # 2026-06-24) — that check belongs to the authors, not to this hook.
    # "RM" is the survey company RM Team. Added 2026-07-31.
    "JPAL", "USAID", "IPL", "DLI", "UCCIC", "UCLA", "UCL", "UC", "CPE", "RM",
    # "OOB.ACE" (and its sibling "OOB.CLA") are single compound municipal
    # permitting form codes that the acronym regex splits into two tokens on
    # the period. Expanded once in prose at first use; whitelisted because
    # the compound, not either half alone, is the real term.
    "OOB", "ACE", "CLA",
    # Universally understood administrative abbreviations and document tokens.
    "TBD", "TBC", "NA", "README", "HTTP", "HTTPS", "PST", "EST", "EDT", "UTC",
    # Georgia Ground Screw venture terms — defined once in the project CLAUDE.md
    # and used constantly across its filings, contracts, and notes.
    "AGS", "OA", "DBA", "DBAS", "SOS", "APR", "GL", "BOI", "ECAS", "HNOA",
    "LTL", "PCO", "CRZ", "DBH", "VOIP", "CRM", "ESR", "ICC", "PE",
    # Standard in survey-methods and conflict-research venues, on the same
    # footing as ACLED/GIS above. QGIS is not an initialism at all any more —
    # the project retired "Quantum GIS" — and UCDP (Uppsala Conflict Data
    # Program) is named in full by its own dataset citations. GALLUP appears
    # only inside "GALLUP International", which is how the organisation being
    # described styles it.
    "QGIS", "UCDP", "GALLUP",
}

# Real acronyms in the user's venues that COLLIDE with ordinary English words,
# so the dictionary test below would wrongly clear them. These are always
# checked. Add to this set whenever a genuine acronym turns out to be a word.
#   PAP  pre-analysis plan        ("pap", a soft food)
#   TOR  terms of reference       ("tor", a rocky peak)
#   ITT  intention to treat       (also whitelisted; listed for the record)
#   PIN, TIN, CAP, AID, CARE, ACT, BEST — same hazard if ever used as acronyms
ALWAYS_CHECK = {"PAP", "PAPS", "TOR", "TORS", "TIN", "PIN"}

# Dictionary of ordinary English words, used to tell an acronym from a word
# that merely happens to be capitalized for emphasis or in a heading. See the
# note in main().
_DICT_PATHS = ("/usr/share/dict/words", "/usr/dict/words")


def english_words():
    for p in _DICT_PATHS:
        try:
            with open(p, "r", errors="ignore") as fh:
                return {w.strip().lower() for w in fh if w.strip()}
        except OSError:
            continue
    return set()


# macOS ships web2 as /usr/share/dict/words, and web2 carries base forms but
# few inflections — "record" is in it, "filed" is not. Without this, ordinary
# past participles in headings (FILED, SIGNED, ISSUED, APPROVED) keep tripping
# the check, which was half the noise this hook was producing.
_SUFFIXES = (
    ("s", ""), ("es", ""), ("ed", ""), ("ed", "e"), ("d", ""),
    ("ing", ""), ("ing", "e"), ("ly", ""), ("er", ""), ("er", "e"),
    ("est", ""), ("est", "e"), ("ies", "y"), ("ied", "y"),
)


def is_english_word(token, words):
    """True if token is ordinary English, allowing for common inflections."""
    if not words:
        return False
    t = token.lower()
    if t in words:
        return True
    for suf, repl in _SUFFIXES:
        if len(t) > len(suf) + 1 and t.endswith(suf):
            stem = t[: -len(suf)] + repl
            if len(stem) >= 3 and stem in words:
                return True
    # Doubled final consonant before -ed/-ing: "stopped" -> "stop".
    for suf in ("ed", "ing"):
        if t.endswith(suf):
            base = t[: -len(suf)]
            if len(base) >= 4 and base[-1] == base[-2] and base[:-1] in words:
                return True
    return False


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    path = (
        payload.get("tool_input", {}).get("file_path")
        or payload.get("tool_input", {}).get("notebook_path")
        or ""
    )
    if not path:
        sys.exit(0)

    ext = os.path.splitext(path)[1]
    if ext not in PROSE_EXT:
        sys.exit(0)
    if any(part in path for part in SKIP_PATH_PARTS):
        sys.exit(0)

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError:
        sys.exit(0)

    # Strip LaTeX commands, math, and fenced code so macro names and symbols
    # are not read as initialisms. Math-mode ($...$) and %-comment stripping
    # only makes sense for genuinely LaTeX-flavored files: a plain .md/.txt
    # file full of dollar amounts (an operating agreement, a budget memo)
    # will pair up unrelated "$" signs across whole paragraphs and silently
    # delete huge spans of real prose before the acronym check ever runs —
    # found 2026-07-26 when it ate 24,000 of 58,000 chars in a financial
    # contract and kept reporting a term as "undefined" no matter how it was
    # expanded, because the text containing the expansion had been erased.
    stripped = re.sub(r"```.*?```", " ", text, flags=re.S)
    if ext in (".tex", ".qmd", ".Rmd", ".rmd"):
        # Comments BEFORE math. In TeX the comment character is lexically
        # prior, and `[^$]*` happily matches newlines: with math stripped
        # first, a "$" anywhere earlier in the document pairs with one inside
        # a %-comment, deletes the "%" that opened the line, and leaves the
        # comment's remainder standing as prose. Found 2026-08-10 on a JPE
        # manuscript, where a `% Source:` provenance comment (the convention
        # the data-pipeline rule requires) leaked "PPP" into the candidate set
        # and blocked every edit to the file.
        stripped = re.sub(r"%.*", " ", stripped)  # LaTeX comments
        # An escaped "\$" is a literal dollar sign in prose ("\$250 million"),
        # not a math delimiter. Treating it as one pairs it with a real "$"
        # further on and erases everything between. On the same manuscript this
        # left only 36% of the file for the check to see; respecting the escape
        # raises that to 90%. Same failure class as the .md/$-amount note
        # below, which this file already documents.
        stripped = re.sub(r"(?<!\\)\$[^$]*?(?<!\\)\$", " ", stripped)
        # Colour declarations carry a model name and a value, never prose:
        # \definecolor{brandblue}{RGB}{0,51,160} and the HTML/hex form both
        # leak "RGB", "HTML" and every six-hex-digit code into the candidate
        # set. The general macro rule below consumes only one brace group, so
        # strip the three-argument colour form first. Added 2026-07-31 after a
        # syllabus preamble reported RGB and four hex codes as undefined.
        stripped = re.sub(
            r"\\definecolor\*?(\[[^\]]*\])?\{[^}]*\}\{[^}]*\}\{[^}]*\}", " ", stripped
        )
        # Text-formatting commands wrap prose, so their brace content is the
        # sentence, not an argument. Unwrap them (keep the content, drop the
        # command) before the general macro rule below erases both. Added
        # 2026-08-10 after \textbf{Data Generating Process (DGP)} in
        # ch2_slrm.tex was erased whole, so a term expanded correctly on its
        # first use was still reported as undefined. Same failure class the
        # comment above already documents: stripping that removes the
        # expansion cannot then judge whether the expansion is present.
        for _ in range(4):  # nested \textbf{\emph{...}}
            stripped, n_unwrapped = re.subn(
                r"\\(?:textbf|textit|textsc|textrm|textsf|emph|underline"
                r"|uline|text)\*?\{([^{}]*)\}",
                r"\1",
                stripped,
            )
            if not n_unwrapped:
                break
        stripped = re.sub(r"\\[A-Za-z]+\*?(\[[^\]]*\])?(\{[^}]*\})?", " ", stripped)

    # Roman numerals naming a division of a cited work ("Book XX, Ch. II",
    # "Livre XX, Chapitre II", "Vol. IV"). These are numbers, never
    # initialisms. Added 2026-08-10 after a French-language epigraph in a
    # manuscript flagged XX as an undefined acronym on every write to the file.
    #
    # Deliberately keyed on the preceding structural word rather than on the
    # shape of the token alone: several genuine acronyms are also well-formed
    # Roman numerals (CV, MD, CD, MC), and a blanket numeral exemption would
    # silence those everywhere.
    stripped = re.sub(
        r"\b(?:Book|Chapter|Chap|Ch|Part|Volume|Vol|Section|Sec|Canto|Act|Scene"
        r"|Livre|Chapitre|Tome|Partie|Libro|Buch)\.?\s+[IVXLCDM]{2,6}\b",
        " ",
        stripped,
    )

    # Hyphenated alphanumeric designations — traffic-sign codes ("R3-1g",
    # "R5-12", "S1-1"), agency form numbers ("WC-10", "CD-030"), model and part
    # numbers. The candidate regex below stops at the hyphen and reports the
    # prefix ("R3", "S1") as an undefined acronym, which it is not: the whole
    # token is one identifier. Added 2026-08-10 after a MUTCD sign list
    # reported R3, R5 and S1 on every write.
    #
    # Requires digits on BOTH sides of the hyphen (or a digit-led suffix), so
    # ordinary compounds keep their first element in scope: "US-based",
    # "UN-led", "AI-assisted" are untouched and their prefixes still checked.
    stripped = re.sub(r"\b[A-Z]{1,4}\d*-\d+[A-Za-z]?\b", " ", stripped)

    candidates = set(re.findall(r"\b[A-Z][A-Z0-9]{1,5}\b", stripped))

    # An all-caps token is not necessarily an acronym. Two exemptions, added
    # 2026-07-29 because the bare regex above flagged ordinary capitalized
    # English on essentially every write ("RECORD", "FILING", "WHAT", "WHY",
    # "OPEN", "DECIDE", "AFTER", "THIS", "NO", "ONLY", "DRAFT", "CHOICE"), and
    # noise on every write is how a real finding gets ignored.
    words = english_words()

    # (2) Tokens inside a run of two or more consecutive all-caps words are a
    # heading or emphasis, not acronyms — "OPEN CHOICE", "DRAFT ONLY", "WHAT
    # WAS DONE". Required: at least one token in the run is a real word, so a
    # genuine pair of adjacent acronyms is still caught.
    caps_run = set()
    run = []
    for tok in re.findall(r"[A-Za-z][A-Za-z0-9]*", stripped):
        if tok.isupper() and len(tok) >= 2:
            run.append(tok)
            continue
        if len(run) >= 2 and any(is_english_word(t, words) for t in run):
            caps_run.update(run)
        run = []
    if len(run) >= 2 and any(is_english_word(t, words) for t in run):
        caps_run.update(run)

    undefined = []
    for acr in sorted(candidates):
        if acr in WHITELIST or acr.rstrip("S") in WHITELIST:
            continue
        # Room, building and catalogue codes: one to three letters followed by
        # two or more digits ("Callaway C101", "Rich B240", and Library of
        # Congress call numbers such as "HD1476", "JK2316", "PS3511").
        # Identifiers, never initialisms. The two-digit minimum keeps genuine
        # short labels such as "A1" in scope. Added 2026-07-31 from a syllabus
        # room listing; widened to three letters 2026-08-13 after LC call
        # numbers in a book/literature/ source.txt were read as acronyms.
        if re.fullmatch(r"[A-Z]{1,3}\d{2,}", acr):
            continue
        # UK postcode outward codes on an address line ("Oxford OX1 2HD"):
        # one or two letters followed by one or two digits, optionally a
        # trailing letter. Address identifiers, never initialisms. Added
        # 2026-08-10 from a journal title page carrying an Oxford address.
        if re.fullmatch(r"[A-Z]{1,2}\d{1,2}[A-Z]?", acr):
            continue
        # (1) It is an ordinary English word, capitalized for emphasis — unless
        # it is a known acronym that collides with one.
        if acr not in ALWAYS_CHECK:
            if is_english_word(acr, words):
                continue
            if acr in caps_run:
                continue
        # Defined if the file ever writes "(ACR)" or "(ACRs)" — the expansion
        # convention — or spells it with periods.
        if re.search(r"\(%s[sS]?\)" % re.escape(acr), stripped):
            continue
        # Same convention, two forms the bare "(ACR)" test misses. Both are
        # genuine definitions and were flagged as false positives on a
        # manuscript that defines all three this way. Added 2026-08-10.
        #   1. parenthetical that continues past the acronym:
        #      "own-account enterprise (OAE, which corresponds to ...)"
        #   2. an explicit naming clause, quoted or not:
        #      "Gram Panchayats (hereafter referred to as ``GPs'')"
        #      "$SCST_i$ is an indicator for Scheduled Caste or Scheduled Tribe"
        a = re.escape(acr)
        if re.search(r"\(%s[sS]?[,;:]" % a, stripped):
            continue
        if re.search(r"(?:referred to as|hereafter|denote[sd]?|abbreviated)"
                     r"[^.]{0,40}%s[sS]?" % a, stripped):
            continue
        #   3. a math identifier, not an initialism: "$SCST_i$", "\delta_{SCST}".
        #      Regression-equation variables are defined in the where-clause
        #      that follows the equation, not by an expansion in parentheses.
        if re.search(r"(?:\$|_\{|\\[a-zA-Z]+_)%s" % a, stripped):
            continue
        n = len(re.findall(r"\b%s\b" % re.escape(acr), stripped))
        undefined.append((acr, n))

    if not undefined:
        sys.exit(0)

    lines = [
        "Undefined acronyms in %s" % os.path.basename(path),
        "(no \"Expansion (ACR)\" anywhere in the file):",
    ]
    for acr, n in undefined:
        lines.append("  %-8s used %d time%s" % (acr, n, "" if n == 1 else "s"))
    lines.append(
        "Expand each at first use, and separately at first use in the abstract. "
        "If one is universal for this venue, add it to WHITELIST in "
        "~/.claude/hooks/check-undefined-acronyms.py."
    )
    sys.stderr.write("\n".join(lines) + "\n")
    sys.exit(2)


if __name__ == "__main__":
    main()
