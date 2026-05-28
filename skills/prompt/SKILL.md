---
description: "Format a rough or dictated request into a structured prompt, then execute it"
---

# Prompt Formatter

Format an informal, conversational, or dictated request into a clean structured prompt, then execute it.

## Input
$ARGUMENTS — the rough request text.

## Instructions

### Step 1: Parse Intent
Extract from the informal input:
- **Core task**: What does the user actually want done?
- **Audience/output**: Who is it for and what form should it take?
- **Constraints**: Any stated requirements, deadlines, or boundaries.
- **Implicit context**: What does the user likely mean given their role (academic economist) and current projects?

### Step 2: Calibrate Depth
- **Light** (default): Simple formatting. The request is clear, just messy.
- **Standard**: Request needs assumptions stated and rationale added. Use if the task has ambiguity.
- **Deep**: Request needs research, comparison, or verification. Use if the task involves factual claims or external information.

The user can override with `depth:light`, `depth:standard`, or `depth:deep`.

### Step 3: Format the Prompt
Rewrite the request as a clean, structured prompt. Match complexity to the task:
- A 1-sentence ask gets a 2-3 sentence prompt. Do not over-engineer.
- A complex multi-step request gets numbered steps, constraints, and output format.
- Include any implicit context that would help execution.

### Step 4: Show and Execute
1. Show the formatted prompt in a fenced code block so the user can see what will run.
2. Execute it immediately — respond to the formatted prompt as if the user had typed it directly.
3. Use available tools (file access, web search, MCP) as needed during execution.

**Exception:** If the user says "hold," "don't run," or "just format," show the prompt but do not execute.

### Step 5: Clarify Only If Necessary
Ask ONE clarifying question ONLY if the ambiguity would lead to a significantly different output. Otherwise, make reasonable assumptions and proceed.

## Examples
```
/prompt write me an email to the department chair about pushing the faculty meeting to next week, keep it short
/prompt depth:deep what are the main criticisms of synthetic control methods in recent applied micro papers
/prompt i need a table showing summary stats for my main variables, the usual stuff, output to latex
```
