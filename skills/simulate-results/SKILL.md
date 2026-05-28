---
description: "Prospective mechanism audit — simulates all combinations of planned analysis results, interprets each, and identifies what would have been needed ex ante to distinguish mechanisms"
---

# Simulate Results

Enumerate every plausible combination of results across a paper's planned analyses. For each combination: fabricate internally consistent mock results, interpret the narrative finding, probe it as a collegial reviewer, rate plausibility and likelihood, then identify what additions to the design or data collection would have made the interpretation unambiguous and mechanism-distinguishing. Synthesize across all combinations into a prioritized ex ante recommendation list.

This skill is most valuable before data collection closes but is useful at any stage — even with a draft in hand it surfaces mechanism gaps that can be addressed in the current version or flagged honestly.

## Input

`$ARGUMENTS` — optional path to a manuscript or PAP file to anchor ingestion. If omitted, auto-detect from project directory.

Optional flags:
- `--resume` — load most recent state file and continue from last completed phase
- `--quick` — skip per-combination Collegial Reviewer; use inline rating instead of separate Plausibility/Likelihood agents; reduces runtime by ~40%

---

## State File

Resumable. State lives at `.workspace/simulate_results/state_YYYY-MM-DD.json`:

```json
{
  "date": "YYYY-MM-DD",
  "project_root": "<cwd>",
  "phases_complete": [],
  "project_context": {},
  "analyses": [],
  "combinations": [],
  "results": {}
}
```

On every run: check `.workspace/simulate_results/` for existing state files. If found, report the most recent and offer to resume or start fresh. On resume, skip phases already in `phases_complete`.

---

## Phase 0 — Project Ingestion

**No agents. Sequential.**

Read the following sources in order, extracting project context:

1. `CLAUDE.md` at project root — research question, identification strategy, treatment, data, project stage
2. `5manuscript/*.tex` — prioritize `main.tex`, `paper.tex`, or any draft with >200 lines. Read Introduction and any section titled "Empirical Strategy," "Identification," "Outcomes," "Data," or "Results." For long files, read the abstract + introduction + section headers and the first paragraph of each section.
3. `0admin/` — look for `*PAP*`, `*pre_analysis*`, `*preanalysis*`, `*preregistration*`. Read any found (first 5 pages of PDFs).
4. `1rawdata/` and `3data/` — read any `*codebook*`, `*dictionary*`, `source.txt`, `README*` files.
5. Project root `README.md` or `README.txt`.

Extract and write to `state.project_context`:
- Research question (1–2 sentences)
- Identification strategy (RCT / DiD / IV / RDD / event study / OLS / other) and what the variation is
- Treatment(s) and control condition
- Data sources and sample
- Primary outcomes (named variables if findable)
- Secondary outcomes
- Subgroup dimensions explicitly planned
- Any process or mechanism measures in the data
- Treatment arms (if multi-arm)
- Project stage: design / data-collection / analysis / draft

Save `Phase0_project_context.md` to `.workspace/simulate_results/YYYY-MM-DD/`. Write phase 0 to `phases_complete`.

---

## Phase 1 — Extract and Confirm Planned Analyses

**No agents. Sequential. Requires user confirmation before proceeding.**

From the project context, extract the list of planned statistical analyses. Each analysis is a named test with a result type.

**What counts as an analysis:**
- Any named regression, test, or comparison that produces a headline result the paper's argument turns on
- Typically: the main ITT estimate, one or two key secondary outcomes, the primary subgroup analysis, any pre-specified heterogeneity test, any mechanism test, any robustness or falsification check the paper explicitly plans
- Do NOT include every robustness variant or coefficient in a table — only the tests where the result (direction and significance) would materially change the paper's story

**Result type for each analysis:**
- Default to **directional**: result can be Positive (statistically significant, expected sign), Null (not statistically significant), or Negative (statistically significant, unexpected/perverse sign)
- Use **binary** (Reject / Not Reject) only when direction is irrelevant to the paper's claim (e.g., a test of balance or a test of equality between two treatment arms)

**Format the extracted analyses as a numbered list:**

```
Planned Analyses:
1. [Label] — [One sentence: what is being tested, on what sample, what the directional prediction is if any] — Type: Directional
2. [Label] — [Description] — Type: Binary
...
```

**Present this list to the user and ask:**
> "Here are the planned analyses I extracted. Please confirm, correct, or add any I missed before I enumerate combinations. Note: the more analyses you include, the larger the combination space (3^N for directional, 2^N for binary). A typical well-scoped paper has 4–7 headline analyses."

**Wait for confirmation.** Update the list based on any corrections. Record the final confirmed list in `state.analyses`. Save `Phase1_analyses.md`. Write phase 1 to `phases_complete`.

---

## Phase 2 — Enumerate Combinations

**No agents. Sequential.**

Enumerate all combinations of results across the confirmed analyses.

For N analyses with result types d_i ∈ {Directional, Binary}, total combinations = ∏ (3 if Directional else 2).

Label each combination with a compact notation, e.g., `[P, N, Pos, Pos, Rej]` meaning Analysis 1 Null, Analysis 2 Null, Analysis 3 Positive, Analysis 4 Positive, Analysis 5 Rejected-null.

**Scale management:**
- If total combinations ≤ 32: run all combinations through the full pipeline
- If total combinations > 32 and ≤ 64: run a bulk screening pass first (see below), then run the full pipeline on the top 32 by plausibility × likelihood
- If total combinations > 64: run bulk screening, select top 24

**Bulk screening pass (when needed):**
Launch one lightweight agent per combination, all in parallel. Each agent sees only its own combination — never the full list. Prompt for each:

> "A study uses [identification strategy] to examine [research question]. The planned analyses are: [analysis list with labels only — no result states from other combinations].
>
> For this specific result pattern: [combination label — e.g., Analysis 1: Positive, Analysis 2: Null, Analysis 3: Negative]
>
> Assign two scores on a 1–10 scale:
> (1) Plausibility — how internally consistent and logically coherent is this combination, given how these outcomes relate to each other in this type of study?
> (2) Likelihood — given what the literature on similar interventions finds, how probable is this combination as the actual result?
>
> Return: Plausibility score | Likelihood score | One sentence explaining the plausibility rating | One sentence explaining the likelihood rating.
>
> Rate this combination on its own terms. Do not compare it to any other scenario."

Collect all scores. Sort by Plausibility × Likelihood, descending. Select the top N as specified above. Flag all excluded combinations in the state file as `screened_out` with their scores — they are not lost, just deprioritized.

Save full combination list and screening results to `state.combinations` and `Phase2_combinations.md`. Write phase 2 to `phases_complete`.

---

## Phase 3 — Per-Combination Pipeline

**Core computation. Multiple agents per combination. Combinations processed in parallel batches of 4.**

**Isolation rule — strictly enforced throughout this phase:** Every agent in Steps 3a–3d receives information about exactly one combination. No agent is told how many other combinations exist, what the other combinations look like, or how this combination compares to any other. Each agent treats its combination as if it were the paper's actual findings — full stop. There is no "out of N scenarios" framing, no hedging, no comparative language in any prompt. The combination is real; the agent assesses it on its own terms.

This isolation is not a style choice — it is the entire point. Contamination across combinations corrupts every downstream assessment. When in doubt, give less context, not more.

Process combinations in batches: launch 4 combinations simultaneously, wait for all 4 to complete, then launch the next 4.

Save each combination's output to `.workspace/simulate_results/YYYY-MM-DD/combinations/combo_[ID].md` as it completes. Record completion in `state.results[combo_ID]`.

If interrupted, resume picks up from the first incomplete combination.

---

### Step 3a — Results Generator (Agent)

Launch as a subagent. Prompt:

> "You are generating the results for a research paper. These are the paper's actual findings — there is no other scenario, no comparison, no alternative. Treat them as real.
>
> The paper uses [identification strategy] to study [research question]. The data come from [data sources]. The sample is [sample description].
>
> The findings are: [combination label with analysis names and result states].
>
> Generate a self-consistent results table. For each analysis:
> - A point estimate with magnitude and sign consistent with the result state
> - A standard error and implied p-value consistent with the result state (significant p < 0.05 for Positive/Negative, p > 0.10 for Null)
> - A brief plain-English summary of what the number means (e.g., 'treatment increases primary outcome by 0.3 SD')
>
> The numbers must be internally consistent — effect sizes and standard errors should be plausible for this type of study, and if multiple outcomes are related (e.g., income and consumption), their results should cohere. Do not explain your choices; just produce the table and summaries.
>
> Primary outcomes: [list]
> Secondary outcomes: [list]
> Sample size: [if known from project context]"

Output: mock results table + plain-English summaries.

---

### Step 3b — Parallel: Interpreter + Plausibility Rater + Likelihood Rater

**Launch all three simultaneously after Step 3a completes.**

**Interpreter (Agent):**

> "You are interpreting the findings of an applied economics paper. These are the paper's results. There is no other version of this paper, no alternative scenario — this is what the study found.
>
> The paper studies [research question] using [identification strategy].
>
> The results are:
> [paste Step 3a output]
>
> Write the narrative interpretation of these findings as it would appear in the paper's abstract and opening of the results section. Two to four sentences. Be precise about magnitudes and significance. Translate the numbers into economic meaning. Hedge calibrated to the precision of the estimates — do not overclaim a null, do not understate a significant effect. Write in first-person singular (this is a solo-authored paper). Do not editorialize about whether the results are surprising."

Output: 2–4 sentence narrative interpretation.

**Plausibility Rater (Agent):**

> "You are evaluating the internal consistency of a set of research results. The study is [one-sentence description of research question and design].
>
> The results are:
> [paste Step 3a output]
>
> Rate the plausibility of these results on a scale of 1–10, where:
> 1 = logically incoherent or requires special circumstances that strain credulity
> 5 = possible but requires a specific story to make sense
> 10 = entirely natural and would not raise eyebrows
>
> Evaluate these results on their own terms — not relative to any other scenario. Provide: (1) the score, (2) a one-sentence explanation of what drives the score — specifically, if any result is in tension with another or requires an unusual mechanism to be true simultaneously."

Output: score (1–10) + one-sentence explanation.

**Likelihood Rater (Agent):**

> "You are assessing the prior probability of a set of research results. The study is a [identification strategy] paper studying [research question] in [context/setting from project profile].
>
> The results are:
> [paste Step 3a output]
>
> Rate how likely it is that these results would be found in a study like this, on a scale of 1–10, where:
> 1 = extremely unlikely given what we know about similar interventions
> 5 = plausible, neither expected nor surprising
> 10 = highly expected given prior literature and context
>
> Rate these results on their own terms — not relative to any other scenario. Provide: (1) the score, (2) a one-sentence explanation grounding your rating in what the literature on similar interventions would predict."

Output: score (1–10) + one-sentence explanation.

---

### Step 3c — Collegial Reviewer (Agent)

*Skip in `--quick` mode.*

**Launch after Interpreter (Step 3b) completes.**

> "You are a thoughtful senior colleague — an applied economist — who has just read a draft results section. These are the paper's actual findings. You are not comparing them to any other scenario; you are reacting to what is in front of you. You are not hostile, but you are sharp.
>
> Research question: [description]
> Design: [identification strategy and key features]
> Results and narrative interpretation:
> [paste Step 3a + Interpreter outputs]
>
> Write a collegial reaction of 3–5 sentences. Focus on:
> (1) The most natural 'but why?' question these results invite — what is the first mechanism or explanation question a reader would want answered?
> (2) Any tension between the narrative interpretation and what the results actually show — is the interpretation over- or under-claiming?
> (3) One specific thing about the results that, if you were a referee, you would push on hardest.
>
> Be specific to these results. Do not give generic advice about robustness checks."

Output: 3–5 sentence collegial reaction.

---

### Step 3d — Ex Ante Advisor (Agent)

**Launch after all of Steps 3b and 3c complete.**

> "You are advising an applied economist before they finalize their research design and data collection. You have just reviewed their study's findings.
>
> These are the findings. There is no other version of this study — this is what it found. Advise on this basis alone.
>
> Research design:
> [paste full project context from Phase 0]
>
> Results:
> [paste Step 3a mock results]
>
> Narrative interpretation:
> [paste Interpreter output]
>
> Collegial review:
> [paste Collegial Reviewer output — or omit if --quick mode]
>
> Plausibility: [score] — [explanation]
> Likelihood: [score] — [explanation]
>
> Your task: given these findings and this design, what would the researcher wish they had done differently at the design or data-collection stage to be able to give a cleaner, more mechanistically grounded account of why the results look this way?
>
> For each gap you identify:
> (1) State the mechanism question that goes unanswered given these results and this design
> (2) Specify concretely what would close the gap — a survey module, a treatment arm, a process measure, a record linkage, a timing variation. Be specific: what questions, what data, what variation
> (3) Classify the timing: Pre-collection (can still be added before data collection closes) / Post-collection using existing data (creative use of variation already present) / Future study only (cannot be recovered)
>
> Focus on gaps that are genuinely consequential — that a referee or discussant would press on, or that go to the core claim of the paper. Do not flag generic 'more data would be nice' additions. Aim for 2–4 high-value specific recommendations."

Output: 2–4 concrete ex ante recommendations with mechanism question, specific addition, and timing classification.

---

## Phase 4 — Synthesis

**One synthesis agent. Sequential after all Phase 3 combinations complete.**

Collect all per-combination outputs. Build the summary table:

| Combo ID | Result Pattern | Plausibility | Likelihood | Narrative (1 sentence) | Top Mechanism Gap |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

Sort by Likelihood descending.

Then launch the synthesis agent:

> "You have before you a set of ex ante design recommendations, each independently generated from a different result scenario for the same study. Each recommendation was produced in isolation — do not second-guess or re-evaluate any individual assessment. Your job is solely to aggregate: identify what these independent recommendations have in common, and prioritize by coverage and importance.
>
> Study: [research question and identification strategy]
> [paste all Step 3d outputs, one per combination, labeled with combo ID, plausibility, and likelihood]
>
> Produce a prioritized recommendation list. For each recommendation:
> (1) State the recommendation concretely (what to add, what variation to build in, what to measure)
> (2) Note which result combinations it addresses and the combined likelihood weight of those combinations
> (3) Classify timing: Pre-collection / Post-collection using existing data / Future study only
> (4) Rate importance: Critical (a top-5 referee would likely require this), Important (strengthens the paper substantially), Nice-to-have (adds depth but paper stands without it)
>
> Then write a 2–3 paragraph synthesis: What is the honest distance between what this design can establish and what a full mechanistic account would require? What is the minimum credible mechanism claim the paper can make given the current design? What one or two additions would most transform the paper's interpretive reach?
>
> Do not repeat every recommendation — synthesize. The synthesis paragraphs should read like a frank conversation with a senior colleague, not a checklist."

Output: prioritized recommendation table + 2–3 paragraph synthesis.

---

## Phase 5 — Final Report

**No agents. Assemble and save.**

Compile into `.workspace/simulate_results/simulate_results_YYYY-MM-DD.md`:

```
# Mechanism Audit: [Project Name]
Date: YYYY-MM-DD
Identification strategy: [strategy]
Project stage: [stage]
Analyses simulated: [N]
Combinations run: [M of total K]

---

## Project Context
[Condensed from Phase 0 — research question, design, data, outcomes. 1 paragraph.]

## Confirmed Analyses
[Numbered list from Phase 1 with result types.]

## Results Space
[Summary table from Phase 4 — all combinations with plausibility, likelihood, narrative, top gap.]

## Per-Combination Dossiers
[For each combination, in order of likelihood:]

### [Combo ID]: [Result Pattern]
**Plausibility:** [score] — [explanation]
**Likelihood:** [score] — [explanation]
**Mock Results:** [table from Step 3a]
**Narrative:** [from Interpreter]
**Collegial reaction:** [from Collegial Reviewer]
**Ex Ante Recommendations:** [from Ex Ante Advisor]

---

## Synthesis

### Priority-Ordered Recommendations
[Table: Recommendation | Combinations addressed | Likelihood weight | Timing | Importance]

### Synthesis
[2–3 paragraphs from synthesis agent: distance between current design and mechanistic account, minimum credible mechanism claim, highest-leverage additions.]
```

Update `MEMORY.md`:
```
- [Mechanism audit YYYY-MM-DD](.workspace/simulate_results/simulate_results_YYYY-MM-DD.md) — [N] analyses, [M] combinations, top recommendation: [one sentence]
```

Add any Critical-rated recommendations to `.workspace/TODO.md` as `- [ ]` items with today's date.

Present the final report to the user and ask: "Want to drill into any specific combination or recommendation?"

---

## Examples

```
/simulate-results
/simulate-results 5manuscript/draft_v2.tex
/simulate-results --resume
/simulate-results --quick
```
