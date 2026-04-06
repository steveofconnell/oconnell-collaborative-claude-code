---
description: "Stress-test a plan with structured expert critique and fresh-context review"
---

# Review Plan

Stress-test a plan with structured expert critique. Catches blind spots, missing steps, and wishful thinking. Use after developing a plan, or on any plan file.

## Input
$ARGUMENTS — optional flags:
- `file:path/to/plan.md` — explicit plan location
- `role:"..."` — override the expert persona
- `focus:dimension` — weight one dimension (e.g., `focus:feasibility`)
- `quick` — skip web research
- `help` — show this options table and stop

## Instructions

### Step 1: Locate the Plan
Three-tier priority:
1. **Explicit file** — `file:path` argument
2. **Recent plan** — most recent file in `~/.claude/plans/` or `.s-workspace/`
3. **Conversation history** — scan current session for the plan

If no plan found: "No plan found. Usage: `/review-plan` (after plan mode) or `/review-plan file:path/to/plan.md`"

### Step 2: Assign Expert Role
Infer from plan content:

| Domain signals | Assigned role |
|---|---|
| paper, manuscript, identification, regression | Academic research methodology specialist |
| proposal, grant, funder, budget | Research funding specialist |
| data, analysis, pipeline, code, replication | Data science and reproducibility specialist |
| IRB, ethics, compliance, survey | Research compliance and field operations specialist |
| project management, workflow, timeline | Operations and project management specialist |
| Default | Strategic planning specialist |

If `role:"..."` is provided, use that instead. Announce the role.

### Step 3: Research (unless `quick`)
Build 2 web searches from the plan's domain:
- "[approach] best practices [current year]"
- "[domain] common pitfalls"

Distill into 3-5 key principles relevant to this plan.

### Step 4: Fresh-Context Review
Launch a subagent to perform the critique. This avoids the bias of reviewing a plan you helped create.

The subagent reviews against 6 dimensions:

**1. Pre-mortem** — "It's 3 months later and this failed. What were the top 3 causes?"

**2. Completeness** — What's missing that a domain expert would expect?

**3. Feasibility** — Are there steps depending on unconfirmed resources, approvals, or timelines?

**4. Best-practice alignment** — How does this compare to standards from Step 3?

**5. Sequencing** — Are there hidden blockers? Would reordering reduce risk?

**6. Specificity** — Could someone unfamiliar execute each step without asking clarifying questions?

If the subagent is unavailable, perform the review inline using this critic stance:
> You are the critic, not the planner. Do not rationalize. Find what's missing, what will break, and what's wishful thinking.

### Step 5: Classify and Present

```
PLAN REVIEW — [Plan Title]

Reviewing as: [role]
Plan source: [file / conversation]

BEST PRACTICES CONTEXT
[3-5 key principles from research, or "Skipped (quick mode)"]

STRENGTHS
[Numbered — what the plan does well]

WEAKNESSES & GAPS
[Red] [Label] — [Issue] → Fix: [Recommendation]
[Yellow] [Label] — [Issue] → Fix: [Recommendation]
[Green] [Label] — [Issue] → Fix: [Recommendation]

VERDICT
APPROVE — [Rationale]
  OR
REVISE — [Rationale]. See revised plan below.

REVISED PLAN (only if REVISE)
[Full revised plan with [CHANGED] and [NEW] markers]
```

Classification:
- **Red** — Critical. Will likely cause failure if unaddressed.
- **Yellow** — Important. Creates risk but plan can proceed.
- **Green** — Minor. Nice-to-have improvement.

### Step 6: Next Step
Ask: "Apply these revisions? Or provide feedback to refine further."

## Examples
```
/review-plan
/review-plan file:5manuscript/revision_plan.md
/review-plan quick
/review-plan role:"field survey logistics specialist" file:.s-workspace/survey_plan.md
```
