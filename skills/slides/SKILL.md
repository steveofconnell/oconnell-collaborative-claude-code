---
description: "Construct or review academic beamer slide decks — enforces seminar-grade rhetoric, Shapiro structure, and the user's presentation voice"
---

# Academic Slides

Construct or review a beamer slide deck for an academic economics presentation. Enforces rhetorical standards derived from:
- Jesse Shapiro, "How to Give an Applied Micro Talk" (canonical reference)
- Paul Goldsmith-Pinkham, "Tips + Tricks with Beamer for Economists"
- The user's own slide decks across multiple projects
- Three documented correction cycles on slide rhetoric (April 2026)

## Input

`$ARGUMENTS` determines mode:

- **`new <topic or description>`** — Build a new deck. Read project context (CLAUDE.md, manuscript, data) to inform content.
- **`review <path>`** — Review an existing deck against the style guide. Flag violations, propose rewrites.
- **`<path>` alone** — Infer mode: if the file exists, review it; otherwise treat as topic for a new deck.

If no arguments, ask: "Seminar talk or internal meeting? What's the topic?"

## Presentation Types

### Seminar talk (default)
Shapiro structure. The audience is professional economists at a top-5 department.

1. **Motivation** (1-2 slides) — Why should the audience care? A striking fact, a policy question, or a puzzle. Not a literature survey.
2. **Research question** — State the question. Policy/counterfactual, deep parameter, or theory test. Not "What happens if we apply X to Y?"
3. **This paper** — What you do and why you have something to add. 2-4 numbered contributions.
4. **Preview of findings** — Tangible, terse. Specific numbers. Enough method so results don't feel like magic, not so much that findings are crowded out. Assume the audience is about to leave — make sure they walk out with something.
5. **Data** — Source, key variables, sample. No data processing details ("no one wants to see your underwear"). Get credit for novel measurement.
6. **Model / Design / Identification** — Write out the equation. Define every variable. State the identifying assumption formally. Discuss the most important vulnerabilities — not every possible criticism.
7. **Results** — Figures wherever possible. Tables for key magnitudes only, not every coefficient or robustness check. Always be telling the story. Have a bottom line: a single quantitative take-away.
8. **Conclusion** — Brief. What did we learn? One slide.

### Internal meeting / catchup
Collaborative, decision-seeking. The audience knows the project.

1. **Context** — What this meeting is about, what has changed since last time
2. **What changed and why** — Old approach → new approach, with evidence for the switch
3. **Current state** — Data, results, design details as needed
4. **Discussion points** — Specific, actionable questions. Name the decision and the tradeoff.
5. **Status and next steps** — What's done, what's waiting, what's blocking

### Conference presentation (shorter)
Same as seminar but compressed. Cut model details to backup slides. Lead with findings.

## Rhetorical Register

**The audience is professional economists.** Write like a peer presenting at a seminar, not a teacher explaining to students.

### Frame titles — context-dependent
Not all titles need to be claims. The rule depends on the slide's function:

- **Motivation / Research question / Results interpretation:** Substantive claims or questions. "Do grants improve social cohesion?" "No influence deficit for men in any condition."
- **Structural sections (Data, Model, Design, Empirical Strategy):** Nouns are fine when bullets carry the argument. "Analytical framework," "Application process," "Empirical setting" are all acceptable.
- **Results with figures/tables:** Outcome-naming is acceptable when the visual carries the claim. "Expenditure per capita," "Women's votes received for most influence."
- **Never catchy, clever, or metaphorical.** No "Who Got Hit," "Not All X Do Y," "The Punchline."
- **No repeated titles.** "This paper" should appear once per deck, not twice with different content.

### Bullet text
- Sentence fragments preferred. Full sentences only when a finding needs precise statement — e.g., "Women in male-majority teams are perceived to have only ~50% of proportionate influence."
- Lead with the specific, not the general. If a bullet could appear in an undergraduate lecture, cut it.
- Pair mechanisms with observable implications: "Human capital channel → $g$ increasing in education"
- Name populations and constructs concretely: "Syrian refugees in Lebanon," "women in male-majority teams," not "affected groups" or "participants"

### Quantification
Always name the denominator, the comparison class, and the uncertainty:
- Good: "$2,100 per HH over 12 months; 98th percentile in UCT literature; 40-50% of counterfactual expenditure"
- Good: "0.14 SD reduction in civic engagement ($q = 0.03$)"
- Weak: "significant effect" / "large gains" / "0.23 SD improvement" (improvement in what? relative to what?)

### Signature rhetorical moves
These are moves the user employs effectively. Use them when the content fits:

1. **Hypothesis decomposition.** Label competing mechanisms explicitly (H1, H2a, H2b) and adjudicate each with evidence. Structure: "Why does X happen? → H1: [mechanism]? No: [evidence against]. → H2: [mechanism]? Yes: [evidence for]." See KOPS and AltindagOConnellAchour examples.

2. **Paired negation + positive claim.** State the question, answer with "No" or "Yes" plus the specific finding. "Are women accorded proportionate influence? → No. Women in male-majority teams are perceived to have only ~50% of proportionate influence." Strong and direct.

3. **Design-as-contribution.** Frame the research design as a substantive advantage, not a methodological detail. "This setting isolates skill mismatch from selection and quality — same providers, same materials, requestor identity blinded." Mention early, not buried in a methods slide.

4. **Model-as-interpretation.** Simple models (voting model with discrimination penalty, informed vs. uninformed optimization) derive predictions that are then tested against data. These are interpretive tools, not theoretical novelty claims. Keep them short — derive the prediction, show the data.

5. **Belief vs. behavior distinction.** When a null result on beliefs coexists with a treatment effect on behavior, state it plainly: "Treatments constrain expression of discrimination, not change beliefs themselves." This is a policy-relevant framing grounded in measurement.

6. **Explicit priors before results.** State what existing evidence or theory predicts before showing the finding. "Prior: transfer size sufficient to have sustained effects." Then the result lands harder when it confirms or contradicts.

### What to cut
- Throat-clearing generalizations: "Causal methods estimate effects," "Treatment effects are heterogeneous," "Averages can conceal variation"
- Colloquial signposting: "The standard move:", "The problem:", "Here's the key insight:", "Bottom line:", "Why now:", "Core idea:", "Key question:", "What I'd like feedback on:" — if the content needs a label to be understood, the content isn't clear enough
- Theatrical one-liners: "This paper disaggregates." "At some point you have to talk to people."
- Theatrical flourishes and rhetorical escalation: "beyond the reach of a text box," "A finding. A theory." — every phrase must carry information, not decoration
- Tricolons that escalate: "hard to measure, hard to anticipate, and impossible to capture" — say it once, directly
- Negative-first framing: "X cannot do Y; Z can" — state the positive claim directly. Applies to titles too: "Qualitative data collection is not one thing" is negative-first
- Disparaging existing work: "People already do this — just not very well," "The literature fails to," "Reasonable, but not derived from..." — frame contributions additively
- Explaining concepts the audience knows: what an RCT is, what heterogeneity means, what a causal forest does
- The word "different" — globally banned. It is vague and adds nothing. "Different commodities" is just "commodities." Replace with "distinct," "heterogeneous," "varying," or cut entirely
- Jargon that adds nothing over simpler words: "disconfirm" → "falsify," "activates" → "operates," "pre-specify" → "anticipate," "transferability requires mechanism-level specificity" → "external validity requires mechanism specificity"

### Argument structure principles
- **Objective-first, not tool-first.** Motivation starts from the research objective, not from the availability of a new method. "Now I have CATEs so let's use them" is wrong. Build from the purpose; the tool emerges as the right instrument.
- **Define the intellectual space before the contribution.** Opening slides establish what world we're in, why the question matters, what existing approaches are. Only then does "this paper" follow.
- **Never lead with what others didn't do.** Don't say "Bergman didn't use CATEs" — say "CATEs make a formal criterion operational."
- **Each slide motivates the next.** If a slide could go in two places, it belongs wherever it motivates the next slide rather than summarizes the previous one. Abrupt introduction of technical concepts kills momentum; bridge from the preceding slide's conclusion.
- **Don't restate what was established.** If the previous slide made a point, build on it, don't repeat it.

### Slide formatting principles
- **No paragraphs.** Even two-sentence paragraphs are too much. Use a header line followed by bullets, or single standalone lines with spacing.
- **Header lines introduce bulleted lists.** 1-2 lines of prose set up the point, then bullets for specifics. Not wall-to-wall bullets, not wall-to-wall prose.
- **Fragment style over prose.** "Bergman et al.: five mechanisms, families used distinct subsets" preferred over "Bergman et al. found five mechanisms; families used different subsets."

### Cross-disciplinary adjustment
- Political science venues: more institutional context upfront, theoretical framing (Durkheim, Gurr, etc.), explicit engagement with qualitative tradition. Core voice unchanged.
- Policy venues (World Bank, J-PAL): more policy motivation, less econometric detail. Effect sizes in dollars or percentages, not standard deviations.

## Format Rules

### Text density
- **No text block longer than two compiled lines.** If it needs more space, decompose into bullets.
- **Use fragments, not prose sentences.** The academic-writing-voice sentence structure rules do NOT apply to slides — those are for manuscripts. Slides are visual aids for a speaker.
- **45-75 characters per line** (Goldsmith-Pinkham rule of thumb).
- **Don't shrink font to fit text.** If it doesn't fit, you have too much. Move detail to a backup slide.

### Figures and tables
- Figures wherever possible to show what's in the data (Shapiro: "more honest, more complete, more interesting, more persuasive").
- Tables for key magnitudes only. Not every coefficient, not every robustness check.
- Table/figure notes: source, key features of the calculation, reading guide.
- Summarize robustness in bullets, not additional table columns.

### Structure
- Busy or detailed content → backup slide with `\hyperlink` + `\beamergotobutton`
- `\appendix` restarts slide numbering for backup slides
- Transition slides (section dividers) only if the talk has 4+ distinct sections

## LaTeX Conventions

### Standard preamble
```latex
\documentclass[compress, aspectratio = 169]{beamer}
\usetheme{CapeTown}
\usepackage{makecell}
\usepackage{amssymb}
\usepackage{mathpazo}
\usepackage{amsfonts}
\usepackage{amsmath}
\usepackage{booktabs}
\usepackage{tikz}
\usetikzlibrary{shapes, positioning, arrows.meta, calc}
\usepackage{graphicx}
\usepackage[default]{lato}
\usepackage[T1]{fontenc}
\usepackage{appendixnumberbeamer}
```

Check whether the project has `beamerthemeCapeTown.sty` in its slides directory. If not, check `~/Dropbox/LivelihoodsSocialCohesion/7tex/slides/` for a copy. If unavailable, use the Metropolis theme (`\usetheme{metropolis}`) as fallback.

### Colors
Define project-specific semantic colors (not generic red/blue). Name them for what they represent:
```latex
\definecolor{violating}{RGB}{200, 60, 60}
\definecolor{confirming}{RGB}{60, 120, 200}
```
Use colorblind-safe values. Goldsmith-Pinkham palette: Blue (0,114,178), Red (213,94,0), Green (0,158,115).

### Graphics
- TikZ for conceptual diagrams (scatter illustrations, design flowcharts, timelines)
- Embedded PNG/PDF for data figures (produced by analysis scripts)
- `\resizebox` or `\includegraphics[width=...]` for consistent sizing
- Figure backgrounds should match slide background or be transparent

## Anti-Pattern Checklist

Before presenting any slide output, verify every frame against this list:

- [ ] No colloquial framings or signposting ("The standard move:", "Here's the key:")
- [ ] No theatrical one-liners or standalone dramatic sentences
- [ ] No undergraduate-level generalizations the audience already knows
- [ ] No text blocks > 2 compiled lines
- [ ] No full prose sentences where fragments suffice
- [ ] No disparaging framing of existing work
- [ ] No negative-first framing ("X can't; Y can")
- [ ] Frame titles match their context (claims for motivation/interpretation; nouns OK for structural slides)
- [ ] No repeated frame titles within the same deck
- [ ] All numbers have referents (X% of what? N SD of what outcome? relative to what?)
- [ ] No content the presenter won't talk about
- [ ] No "catchy" or metaphorical section/frame titles
- [ ] No use of the word "different" — replace with precise alternative or cut

If any item fails, rewrite the frame before presenting it.

## Examples

Reference examples are in `examples/` within this skill directory:

**Full slide decks by the user (primary calibration source):**
- `KOPS.tex` — Gender composition and influence in teams (Karpowitz, O'Connell, Preece, Stoddard). **Best overall exemplar** — clean research-question-as-structure, paired negation+claim moves, simple interpretive model.
- `OM_Employer_informed_job_training.tex` — Employer-informed job training in Brazil (O'Connell, Mation). Strong hypothesis decomposition and design-as-contribution framing.
- `AltindagOConnellAchour.tex` — Cash transfers to refugees (Altindag, O'Connell, Achour). Explicit prior-before-result move, mechanism adjudication structure.
- `AO_HumanitarianAidEfx_JDC.Rmd` — Same project, R Markdown version. Shows register in non-beamer format.

**Excerpted frames (secondary):**
- `good_seminar_frames.tex` — Individual frames from LivelihoodsSocialCohesion seminar decks
- `good_meeting_frames.tex` — Individual frames from LivelihoodsSocialCohesion study design presentations

Read at least KOPS.tex and one other full deck before composing slides to calibrate register and density. The full decks show how the rhetorical moves sequence across a talk; the excerpts show individual frame quality.

## Instructions

### For `/slides new`
1. Read project context: CLAUDE.md, manuscript tex files, data documentation, any existing slides
2. Ask or infer: seminar, internal meeting, or conference?
3. Read the example files in `examples/` to calibrate register
4. Draft the full deck following the appropriate structure
5. Run every frame against the anti-pattern checklist
6. Compile with `pdflatex` and open
7. Present the deck to the user

### For `/slides review`
1. Read the target file
2. Read the example files in `examples/` to calibrate register
3. Flag every frame that violates the anti-pattern checklist, with the specific violation
4. Propose rewritten frames for each violation
5. Note any structural issues (Shapiro ordering, missing preview, no bottom line)
6. Ask whether to apply all fixes or review individually

```
/slides new "seminar on qualitative sampling design"
/slides review 6tex/slides/brownbag_slides.tex
/slides daniel_catchup_slides.tex
```
