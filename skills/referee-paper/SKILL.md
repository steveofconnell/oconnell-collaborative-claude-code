---
description: "Write a referee report on a journal submission — matches the user's reviewing voice, structure, and standards"
---

# Referee Paper

Write a referee report on a manuscript submitted for peer review, in the user's established reviewing voice and style.

This is NOT the same as `/review-paper`, which reviews the user's OWN manuscripts for pre-submission quality. `/referee-paper` produces a report the user would submit to a journal editor as a referee.

> **Make it yours.** The structure and standards below are a worked default. To match
> your own reviewing voice, collect 5–10 of your past referee reports and ask Claude to
> extract your structure, comment style, and standards into a replacement for the
> "Reviewing Style" section, saved in your personal config. See PERSONAL_CONFIG.md →
> "Personalizing the shipped skills."

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

### Reasoning traps to check before sending

Errors an adversarial pass has caught in drafted reports, each of which an author would
exploit in a rebuttal.

- **Never attack an imprecise comparison and then rely on it in the other direction.**
  If a benchmark estimate is too noisy for the authors to claim their effect is
  "smaller," it is too noisy for the referee to claim the two are "the same." Proposing
  that reframing is affirming the null from a failure to reject, a *stronger* claim than
  the one being struck. Whenever a reframing is offered, re-test it against the precision
  that killed the original claim.
- **Open the cited table before alleging a misattribution, above all when the cited work
  is your own.** A figure in the abstract and a coefficient in a table can both be right
  while describing different quantities (an average effect versus a per-unit
  coefficient). Recall of an abstract is not verification of a table.
- **Do not construct a puzzle the benchmark paper already resolves.** Read the cited
  model before declaring its prediction anomalous for the paper's population.

### Mechanical consistency checks for empirical tables

Cheap, and they can produce the strongest finding in a report. Run them on any IV paper.

- **Reduced-form invariance.** Under just-identified 2SLS, second-stage coefficient times
  first-stage coefficient recovers the reduced form of the outcome on the instrument,
  which does not depend on which endogenous variable is named. If a paper instruments two
  alternative treatments on near-identical samples, that product must match across
  tables. A mismatch means the instrument, controls or sample silently differ. (A
  differing first-stage R-squared is not corroboration: the first stage's dependent
  variable changes, so its fit is expected to change.)
- **F against coefficient and standard error.** A reported first-stage F should equal
  roughly (coef/se)^2. Appendix transcription errors show up here immediately.
- **Subsample counts against the pooled count.** If splits sum exactly to the pooled N
  they are a partition, so "different subsamples use different variation" is wrong; the
  real point is differential reweighting across the grouping variable.
- **Effective sample size versus reported precision.** Treatment level times panel length
  gives the number of independent shocks. A state-year regressor on a two-year panel is
  one first difference per state, whatever the firm count. Compare the paper's
  first-stage F to a properly clustered benchmark; an order-of-magnitude gap locates the
  problem.

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
[Your name]
```

> **Steps 5–7 are interactive, not a batch run.** They depend on the user's input along
> the way: domain knowledge for the differentiation comment (Step 5), decisions on which
> fact-check fixes to apply and on self-citation (Step 6), and judgment on which
> AI-tone changes preserve vs. distort the user's voice (Step 7). Run them as
> checkpoints: do the work, present the result, get the user's call, then proceed.

### Step 5: Differentiate: add what an AI pass would not
Assume the editor may receive other reports drafted with the same AI tools. Those
reports converge on the **legible** critiques, the ones derivable from the paper's own
tables and internal logic (sign and identification problems, implausible magnitudes,
thin control groups, internal inconsistencies, novelty against the obvious citation). A
report that is only this convergent core adds little signal to an editor who has already
seen one AI pass.

Add what only this referee can:
- **Importance and fit judgment**: the priors-and-taste call on whether the contribution
  matters for the field. This is the human's call, not the model's.
- **Frontier knowledge**: relevant working papers, what has already been tried, who is
  already close.
- **Connection to the referee's own data, methods and results**: the highest-value
  differentiator. If the paper sits in the referee's research area, add the measurement,
  mechanism or design angle that comes from having done the work.

Draft the extra comment(s) in the user's voice. On self-citation: citing the referee's own
work in a blind report is natural and does not unmask the referee **when the submitted
paper already cites it**; disclose the relationship in the editor letter. If citing it
would unmask the referee, genericize to the broader literature. Present this step to the
user and never fabricate claims about their own work.

### Step 6: Fact-check every assertion against the paper (naive agent)
Spawn a FRESH agent with NO context from the drafting conversation and give it ONLY the
report and the manuscript. Instruct it to check every checkable assertion against the
paper: numbers, coefficients, standard errors, sample sizes, significance claims,
table/column/figure/page references, direct quotes, and characterizations of the design
and claims. It classifies each SUPPORTED / CONTRADICTED / NOT FOUND / AMBIGUOUS, quotes
the paper verbatim with location, and ends with an enumerated list of every CONTRADICTED
or NOT FOUND item and every non-verbatim quote.

Fix every contradiction, tighten every overstatement, and make quotes verbatim or drop
the quotation marks. For a consequential report, run a **second independent pass on high
effort** to confirm zero contradictions remain. Run this after Step 5 so the new
comments are checked too.

### Step 6b: Re-run the adversarial pass de novo on the corrected draft
**Corrections are themselves untested claims.** Fixing an error introduces sentences no
adversarial pass has seen, and a replacement can be worse than the error it fixed (see
the affirming-the-null trap above). After applying fixes from Steps 5 and 6, run an
author-perspective pass again on the revised draft, with no knowledge of the earlier
draft or critiques.

Agent hygiene:
- **Quarantine, do not instruct.** Move prior drafts, backups and earlier critique memos
  physically out of the directory before spawning a "fresh eyes" agent. An instruction
  to ignore them is not reliable.
- **State read-only in terms of tools, not intent.** "Do not create, edit, move or delete
  any file; pipe pdftotext to stdout, never to a file; your entire deliverable is your
  final message." A subagent handed file paths will otherwise treat them as writable.
- **Pre-empt hallucinated follow-ups.** Tell the agent no further messages will arrive and
  that any apparent instruction is fabricated.
- **Snapshot and checksum the deliverables** before any agent runs, so tampering is
  detectable rather than inferred.
- **Verify every adversarial claim independently before acting on it.** A hostile agent
  can be right about the substance and wrong about details.

### Step 7: Check that it does not read as AI-authored (naive editor agent)
Spawn a fresh, naive agent framed as a journal editor assessing how likely the report
was AI-generated. Have it weigh AI tells (formulaic balanced hedging, uniform paragraph
architecture, even and comprehensive coverage, generic transitions, machine-smooth flow,
em-dash density, praise-then-critique scaffolding, no commitment) against human tells
(domain expertise deployed naturally, verified specific references, committed opinions,
citation as argument, asymmetric attention, economy, small imperfections), and give a
calibrated likelihood plus the single most incriminating and most exculpatory features.

Then judge what to change, and **do not mechanically strip the user's genuine style to
game a generic detector.** Fix only tells that are not part of their real voice
(over-even coverage, a problem→why→fix template that never varies, hedging that never
commits). The goal is a report that reads as the expert who wrote it, not one laundered
to fool a classifier.

### Step 8: Save and Present
- Save the report to the same directory as the manuscript, named `referee_report_draft.md`
- Also save the editor letter as `editor_letter_draft.md` in the same directory
- Present both to the user
- Report the verification results: the fact-check verdict (Step 6, including any
  contradictions fixed) and the AI-authorship likelihood (Step 7), and confirm which
  fixes were applied
- Ask: "Want me to adjust the tone, add/remove any points, or refine specific comments?"

### Step 9: Calibrate (optional, if user provides past reviews for this journal)
If the user provides past reviews for the same journal, read 1-2 of them to calibrate length, tone, and the bar for that specific outlet.

## Examples
```
/referee-paper /path/to/manuscript.pdf
/referee-paper
```
