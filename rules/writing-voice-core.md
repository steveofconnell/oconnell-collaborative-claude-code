---
description: "Always-on writing bans and register rules — governs every reply, email, memo, slide and manuscript. Manuscript-specific craft lives in academic-writing-voice.md (path-scoped)."
---

# Writing Voice — Core (always-on)

Applies to **everything either of us writes**: manuscripts, proposals, referee
responses, memos, email, slides, file content, and Claude's own conversational
replies. Nothing here is scoped to a file type, because most of it gets violated
in chat, where no file is open.

Companion files:
- **`academic-writing-voice.md`** — manuscript and correspondence craft (sentence
  and paragraph structure, framing contributions, abstracts, tables and figures,
  email register by audience). Path-scoped to writing files; **read it before
  drafting any manuscript prose or any email.**
- **`interaction-style.md`** — no flattery, no hype labels, no MBA register, popup
  form for genuine choices. Always-on; not repeated here.
- **`casebook/`** — your own dated record of where each ban below came from. Read
  it when a rule is being questioned or looks wrong, not on every turn. See
  `casebook/README.md` for the convention.

> **The word and metaphor lists below are one maintainer's, shipped as a worked
> example.** The mechanism is the point: a short always-on file of bans, each
> carrying the date it was set and the literal sense that survives. Replace the
> entries with the ones your own drafts keep tripping over.

---

## 1. The general rule: prefer the literal word over the figurative one

When a figurative word stands in for a plain verb or noun that already exists, use
the plain one — without being asked, and without waiting for that particular word
to reach the list below. If no literal equivalent exists, the figure is doing real
work and is fine. (2026-07-24)

**Exempt — established terms of art.** Words whose figurative origin is dead and
which carry precise technical meaning in economics and statistics are the field's
vocabulary, never flagged: *shock, spillover, channel, mechanism, elasticity,
bound, weight, panel, sampling frame, field, identification, robustness, leverage
(statistical), anchor, margin, slack, noise, signal, tail.* Terms coined in the
user's own work (e.g. "grievance register", "framing register") are likewise exempt.

**When unsure whether a word is a term of art or a reach, flag it rather than
substituting silently.**

### Banned metaphors

The enumerated entries stay because each records a specific correction and states
which literal senses survive. Dates are when the ban was set.

| Banned | Use instead | Literal sense that survives |
|---|---|---|
| **scoped / scope / scoped to** (2026-05-28) | say what it covers, applies to, excludes | fine in planning notes and scaffolding, not prose |
| **register** = tone/voice/formality (2026-06-02) | "the tone you want", "writing as a peer" | a record or list; the coined "grievance/framing register" |
| **surface** as a verb (2026-06-02) | raise, bring up, show, reveal, flag, point out, find | the noun (a physical surface) |
| **spine** as default metaphor (2026-06-02) | the core, the foundation, what it is built on | a deliberate defined term |
| **land** as a verb (2026-06-07) | does this work, is this convincing, does this read right | the noun — required and central (land, farmland, cropland) |
| **plumbing** (2026-06-07) | implementation, the build steps, name what it does | an actual water system. **Hook-enforced.** |
| **gate / gating / gatekeeper / gated** (2026-06-11, hardened 2026-07-24) | threshold, screen, screening, non-compensatory screen | **Hard-blocked by hook** — the blunt block also catches literal farm gates and Qualtrics routing gates. Ask for a softening if it blocks a genuine literal use. |
| **horserace / horse race** (2026-06-15) | comparison, head-to-head comparison, benchmark | an actual horse race |
| **playbook** (2026-06-16) | procedure, routine, guide, the steps, standard process | an actual sports playbook. Pre-existing `playbook_*` filenames need not be renamed. |
| **gloss / glossed / gloss over** (2026-06-19) | treats briefly, skips, passes over, leaves unexamined / interpret, read as, describe as | the noun (a marginal or lexical gloss) |
| **lock / lock in / lock down / locked** (2026-06-24) | settle, decide, agree on, finalize, fix, commit to, confirm, pin down | file lock, lockfile, git lock, mutex, a physical lock |
| **dial / dialed in / dial up / dial back** (2026-06-29) | set, adjusted, tuned, calibrated, ready / raise / reduce | an actual dial or knob, dialing a number |
| **carry / carries / carried** = bearing weight (2026-07-24) | establish, show, provide, produce, or name the work | physically carrying; a value carried through a computation; a journal carrying an article; disease carrier |
| **standing up / stand up / stood up** (2026-07-17) | form, create, open, set up, build, launch, establish, start, get running | **only** a person or animal physically rising. "Standing up for/to", "won't stand up in court" are also out → defend, confront, won't survive scrutiny |

⚠ **"carry" has a trap:** *support*, *sustain* and *bear* are the same weight-bearing
figure one step deader, so they are not fixes for it. Reach past them to a literal
verb. ("The data support the hypothesis" is conventional enough to survive, but it
is not the plain alternative either.)

### Banned words

| Banned | Use instead |
|---|---|
| **"key"** as an adjective (2026-04-26) | state the distinction, finding or implication directly |
| **"track/s"** as a verb (2026-04-09) | correlate with, predict, co-move with, rise with |
| **"specific"** (2026-04-10) | cut it — "specific network ties" is just "network ties" |
| **"broader"** (2026-04-10) | cut it — unless doing genuine contrastive work |
| **"rest/rests/rested on"** in analytical sentences (2026-04-15) | say what the analysis *does* or *uses*. Narrative/historical use is fine |
| **"load-bearing"** (2026-04-14) | never, anywhere — a classic AI phrase. Describe what the claim does |
| **"dominant"** as an adjective (2026-04-14) | standard, common, widely used, core, leading, primary. Technical senses OK (dominant strategy, dominant eigenvalue) |
| **"different"** (2026-03-25) | use sparingly; cut unless it does real contrastive work |
| **"actual" / "actually"** (2026-07-01) | cut — "the actual data" is just "the data" |
| **"pipeline"** in prose (2026-07-01) | the code, the estimation code, the analysis, the build. Fine in code comments, scripts, and speech about code |
| **"headline"** as framing (2026-07-01) | name the measure; or "primary", "main". Gray area only for macro "headline inflation" |
| **"In other words"** | cut |
| **"Reassuringly"** | cut |

Also out: superlatives; "prove"; decorative adjectives and adverbs; hollow
intensifiers ("significantly" unless statistical, "crucial", "robust" unless
robustness checks); filler transitions ("It is important to note that").

---

## 2. Em dashes — reduce to zero

Em dashes were a documented part of the voice; as of **2026-06-23** the user wants
them cut, ideally entirely. Replace by function:

- **Two sentences** when both halves carry a real claim. Reach for this first.
- **Colon** when the second half explains or itemizes the first.
- **Parentheses** for a genuine aside the sentence reads fine without.
- **Comma-bounded clause** for a light, tightly-bound qualifier.

Do not swap an em dash for an en dash or a spaced hyphen; that is the same
punctuation in disguise. Exempt: numeric ranges (pp. 12–15), quoted material from
others, and config/scaffolding files like this one.

---

## 3. No relevance tags (2026-06-30)

State a fact and stop. Do not append a clause asserting its relevance: *"directly
the subject matter of this assignment," "which is the substance of this work,"
"exactly what this calls for," "highly relevant here," "precisely what X needs."*

**The test:** can the reader work out why this matters without being told? If yes,
cut the tag. It usually hides as a trailing subordinate clause welded onto an
otherwise-fine fact, which is why it survives a read-through. Keep an explicit
relevance statement only when the link is genuinely non-obvious *and* material,
and then state it once, plainly.

---

## 4. No pre-emptive defensiveness. A structural rule, not a tonal one

Do not build an apparatus whose job is to raise an objection and then rebut it: a
subsection, paragraph, caveat, footnote or table note laid out as concern→rebuttal.
A passage can be defensive while every individual sentence reads positively. The
defensiveness lives in the **architecture**, not the word choice.

**Symptoms:** "X is a viable alternative hypothesis [+ rebuttal]"; "One might worry
that Y; however…"; "this is by design, not [what a critic would suspect]"; "the
assumption is not Z but rather…"; cataloguing "what the design cannot rule out"
beyond the single item that genuinely bears on the result; any identification,
robustness or interpretation section laid out as objection→answer,
objection→answer.

**The fix is never a better rebuttal.** It is to not raise a non-live objection at
all. State what the design does, positively; name only the alternative that
genuinely competes and the one test that adjudicates it; let the rest go unstated.
Default posture is confidence: the burden is on a referee to raise an objection,
not on the author to pre-litigate every one. If a concern is genuinely live,
address it once, where it bears, framed as a feature of the design.

Keep the substantive pre-registration machinery (decision rules, exclusion caps,
outcome→conclusion mappings); the apologetic register *around* it is what goes.

### This governs evidence too: figures, photographs, tables, exhibits, captions

- **Do not stage or dramatize evidence to make a claim vivid.** If the argument is
  that an obstruction hides a pedestrian, do not pose a person behind it. A staged
  artifact reads as posed to exactly the reader you need to persuade, and invites
  them to discount the whole set. Capture the condition as it is.
- **Do not caption what the evidence fails to show.** A note that "no pedestrian
  appears in these frames" volunteers a weakness the reader had not raised.
  Describe what is in the frame and stop. Genuine limits belong in a methods or
  sources note, stated once and positively.

Same test as for prose: would the reader have raised this on their own? If not,
raising it is the author arguing with a critic who has not spoken.

---

## 5. Openers, titles, and theatrical filler

- **No standalone dramatic openers.** "The results are sharp." "The collapse was
  structured." Start every paragraph with substance.
- **No pretextual openers** that announce the move instead of making it: "The
  pattern admits a wider reading," "There is a deeper question here," "It is worth
  stepping back," "Taking a step back," "At a higher level of abstraction." Cut the
  wind-up. If a transition is genuinely needed, embed it in the first sentence of
  substance.
- **No theatrical one-liners.** "This paper disaggregates." If it could be a bumper
  sticker, it is too thin.
- **Section and subsection titles state the substantive content.** No clever,
  metaphorical or rhetorical-question titles ("Who Got Hit", "Not All Commodities
  Collapse Alike", "What Disaggregation Reveals"). If a title could apply to any
  paper in any field, it is too vague. "Summary" is never sufficient.
- **No meta-headlines** in any built artifact: "What this settles", "The takeaway",
  "In context", "Two things worth saying plainly".

---

## 6. Correspondence register — compact directives

Full guidance by audience is in `academic-writing-voice.md`; **read it before
drafting any email.** The rules that get violated most:

- **Minimise first-person singular.** Lead with the work as the grammatical
  subject. "The panel covers" not "I built that panel." Cut running
  self-narration ("I've tried to", "I'm thinking", "I want to be deliberate
  about"). Substantive first-person claims are fine.
- **Peer register with senior scholars.** No crediting the correspondent for
  moving you, no "that's a great point", no excessive thanks. One brief
  acknowledgment at most.
- **Never admit fault or shortcoming** in conceptual approach or analysis. No "your
  read pushes me to be more careful", no future commitments to fix something (they
  signal the current work has gaps). State what the work does, in the present.
- **Do not over-concede to a rival.** Grant a competing result by *declining to
  contest it*, not by affirming it. No trailing reassurance clauses ("and the two
  channels are not in tension"), no self-positioning framing, no pat summary closer.
- **Short institutional/administrative email is ONE continuous paragraph.** No bold
  labels, no headings, no per-question breakout. Answer only what was asked; do not
  explain the absence of a thing the correspondent named as an example; do not
  volunteer unrequested credentials; no generic "let me know if anything further is
  needed."
- **With RAs and juniors:** lead with the substance and the ask; do not manage their
  process or sequence their tasks; offer concrete help over instruction; defer
  substantive back-and-forth to live meetings.
- **With coauthors:** do not explain your own rhetorical moves; downplay your edits
  to shared framing; calibrate claims to what is established; work inside the
  correspondent's own categories; no deal-closing sign-offs; no structural labels
  ("Net:") and no aphorisms.

---

## 7. General

- **Avoid AI-typical writing.** Nothing that reads as generic, over-hedged,
  excessively structured or formulaic. No bullet-point prose dressed as paragraphs.
  One hedge per claim, not three.
- **No uninterpreted numbers.** Every number gets a referent and a substantive
  translation. "30 percent" must say 30 percent of what.
- **Avoid noticeable word repetition** within a paragraph or abstract.
- **Never disparage existing work**, directly or indirectly. Contributions are
  additive.
- **Do not reduce the agency of people being studied.** People make choices; places
  do not predispose.
- **Cut statements obvious to an educated reader.**
- **Never embed code-style identifiers in prose**: variable names, filter
  expressions, function calls. Translate to plain words. Script provenance goes in
  `%`-style LaTeX comments, never a visible footnote.
