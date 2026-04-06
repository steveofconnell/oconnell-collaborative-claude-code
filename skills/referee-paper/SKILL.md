---
description: "Write a referee report on a journal submission — matches the user's reviewing voice, structure, and standards"
---

# Referee Paper

Write a referee report on a manuscript submitted for peer review, in the user's established reviewing voice and style.

This is NOT the same as `/review-paper`, which reviews the user's OWN manuscripts for pre-submission quality. `/referee-paper` produces a report the user would submit to a journal editor as a referee.

## Input
$ARGUMENTS — path to the manuscript PDF/file. If not provided, check the current working directory for a manuscript PDF, or ask the user.

## The User's Reviewing Style

Based on analysis of 8+ submitted referee reports across AER, REStud, JPE, JPubEc, EJ, EDCC, JDE, and World Development:

### Structure (strict — do not deviate)
1. **Summary** — single paragraph, 50-120 words. Present tense. Describes what the paper does and finds. Never evaluates quality in the summary.
2. **Major comments** — bulleted (not numbered). Each bullet is a self-contained argument, typically 80-250 words. Sub-bullets for follow-up points. Usually 2-5 major comments. First bullet often opens with a brief positive assessment of execution quality before pivoting to the substantive critique.
3. **Minor comments** — optional. Short, practical: figure labeling, variable naming, table construction, specific page references. Usually 2-6 items.
4. **No separate "recommendation" section.** No "strengths and weaknesses" framework. No numbered sections. No wrap-up paragraph. The report ends on the last substantive point.

### Voice
- **First person singular throughout.** "My main comment," "I think," "I would have liked to see," "for this reader." Never "we" or "this reviewer."
- **Collegial but direct.** Criticism is stated plainly: "I don't see it contributing a level of novelty expected at the current outlet." No excessive hedging of the core message.
- **Conversational register** — smart colleague at a seminar, not a formal document. Occasional contractions. Phrases like "it leaves one wondering," "reading between the lines."
- **Generous acknowledgment of what works**, stated specifically: "I really liked it and engaged with the content substantially." This generosity makes subsequent criticism land harder.
- **Humor and personality in small doses** — rare but distinctive when deployed.

### How Criticism Is Framed
- **Novelty is frequently the central concern.** When raising it, demonstrate deep knowledge of the specific literature — cite 5-10 papers with authors and years.
- **Criticism is constructive and specific.** Walk through exactly why an assumption is questionable, what data would test it, what the alternative interpretation could be. Build logical chains: if A, then B should be testable; if B fails, then C is the interpretation.
- **Suggestions come as specific analyses to do**, not vague requests: "I would have liked to see self-gen volumes in the firm data" not "the authors should do more robustness checks."
- **Reframe the paper's own numbers** to reveal gaps: do the arithmetic the authors did not foreground, use their estimates against their claims about importance.
- **Scrutinize policy implications.** Flag where findings might be misinterpreted for policy.
- **Each major comment follows**: (a) state the issue, (b) explain why it matters, (c) suggest what could be done. The suggestion is concrete but not prescriptive.

### Length
- **Reports are SHORT.** Typical range: 350-1,200 words total. Median around 450 words. The user does not write long reports. 2-4 major comments, 0-4 minor comments. High density of insight per word.
- **Longer reports (~1,000+ words) are for papers the user finds genuinely interesting** and engages with deeply. Shorter reports (~400 words) are for papers where the verdict is clear.

### Distinctive Habits
- **Literature citations within the report.** Cite specific papers (author, year, journal) to support claims about existing literature. This signals deep field knowledge.
- **Economic reasoning applied to empirical design.** Push authors to think through what the identification really recovers, what is the economic mechanism, is the policy effect signaling or material.
- **Sensitivity to rhetoric vs. evidence.** Note when a paper's claims outpace its results — magnitude smaller than suggested, novelty overstated relative to existing work.
- **Page and table references** are specific but not obsessive: "on page 16," "Table 3," "Figure 1 panel A."

## Instructions

### Step 1: Locate and Read the Manuscript
Read the full manuscript. For PDFs, read in 20-page chunks to cover the entire paper including appendices. Track:
- Title, authors, journal (if known from cover page or context)
- Research question, identification strategy, key findings
- Data sources and sample construction
- Tables and figures referenced
- Specific page numbers for key claims

### Step 2: Identify the Core Issues
Think like an applied microeconomist refereeing for the journal this was submitted to. Prioritize:
1. **Novelty** — does the contribution clear the bar for the target journal? What existing work gets close?
2. **Identification** — is the source of variation clearly stated? Are assumptions testable? What are the most plausible threats?
3. **Magnitude and interpretation** — do the paper's own numbers support the claims about importance? Do the arithmetic.
4. **Mechanisms** — does the paper distinguish between competing explanations convincingly?
5. **Data and measurement** — are key variables well-defined? Sample selection issues?
6. **Policy interpretation** — could findings be misread for policy?

### Step 3: Draft the Report
Write the report in the user's voice. Use the structure above exactly:
- **Summary** paragraph
- **Major comments** (bulleted)
- **Minor comments** (if warranted)

Do NOT include:
- A recommendation (accept/reject/R&R) — that goes in a separate editor letter
- A "strengths" or "weaknesses" section
- Numbered sections or headers beyond Summary / Major comments / Minor comments
- A wrap-up paragraph or closing pleasantries (exception: a brief positive closing line is acceptable if the paper genuinely warrants it, as in "Otherwise this is a nice and interesting work!")
- Generic filler ("the authors should think more carefully about...")

DO include:
- Specific page, table, and figure references
- Literature citations (author, year) when arguing about novelty or existing evidence
- The paper's own numbers used to interrogate its claims
- Concrete suggested analyses or framings

### Step 4: Draft the Editor Letter
Write a brief cover letter to the editor (2-4 sentences) that:
- States the overall assessment
- Gives the recommendation (accept / minor revision / major revision / reject)
- Briefly states the primary reason

Format:
```
Dear Editor,

[Assessment and recommendation in 2-4 sentences.]

Sincerely,
Stephen O'Connell
```

### Step 5: Save and Present
- Save the report to the same directory as the manuscript, named `referee_report_draft.md`
- Also save the editor letter as `editor_letter_draft.md` in the same directory
- Present both to the user
- Ask: "Want me to adjust the tone, add/remove any points, or refine specific comments?"

### Step 6: Calibrate (optional, if user provides past reviews for this journal)
If the user's past reviews for the same journal are in `~/Dropbox/ReviewReports/_submitted/`, read 1-2 of them to calibrate length, tone, and the bar for that specific outlet.

## Examples
```
/referee-paper /path/to/manuscript.pdf
/referee-paper
```
