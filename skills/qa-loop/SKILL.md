---
description: "Adversarial QA loop: critic agent finds issues, fixer resolves them, iterates until clean"
---

# QA Loop

Run an adversarial quality assurance loop on a file or set of files. A critic agent identifies issues, then you fix them, then the critic re-reviews. Iterates until the critic approves or the maximum number of rounds is reached.

## Input
$ARGUMENTS — path to the file(s) to QA, plus optional flags:
- `rounds:N` — maximum iterations (default: 5)
- `focus:X` — narrow the critic's focus (e.g., `focus:methodology`, `focus:writing`, `focus:code`)
- `agent:X` — use a specific agent as critic (default: auto-selects based on file type)

## Instructions

### Step 1: Determine Critic Agent
Based on the file type and focus:
- `.tex`, `.md`, `.qmd` → Writing Reviewer agent (or Methodology Reviewer if `focus:methodology`)
- `.R`, `.py` → Use inline code review (no dedicated agent needed — review for correctness, style, reproducibility)
- If `agent:writing` or `agent:methodology` is specified, use that agent regardless of file type.

Read the target file(s).

### Step 2: Critic Pass
Launch the critic agent with the file content. The agent produces a structured report of issues, ranked by severity.

Parse the report into:
- **Critical issues** — must fix (blocks approval)
- **Major issues** — should fix
- **Minor issues** — nice to fix

### Step 3: Fix
Address all critical issues and as many major issues as feasible. For each fix:
- State what the issue was
- Show the change made
- Explain why this resolves it

Do not fix minor issues unless they're trivial (< 1 line change).

### Step 4: Re-Review
Launch the critic agent again with the updated file. Check whether:
- All critical issues are resolved
- No new critical issues were introduced
- Major issue count decreased

### Step 5: Iterate or Approve
- If the critic reports no critical issues and ≤ 2 major issues: **APPROVED**. Print the final score and remaining minor issues for the user's consideration.
- If critical issues remain and rounds < max: go to Step 3.
- If max rounds reached: **STOPPED**. Print remaining issues and let the user decide.

### Step 6: Report
```
## QA Loop Report — <filename>
Rounds: <N>
Status: APPROVED / STOPPED after <N> rounds
Critical issues resolved: <N>
Major issues resolved: <N>
Remaining issues: <list any unresolved>
```

## Examples
```
/qa-loop 5manuscript/draft_v3.tex
/qa-loop 5manuscript/draft_v3.tex focus:methodology rounds:3
/qa-loop 4code/03_regress.R focus:code
/qa-loop 5manuscript/intro.tex agent:writing rounds:2
```
