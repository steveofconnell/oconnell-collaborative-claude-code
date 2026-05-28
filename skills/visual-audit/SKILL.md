name: visual-audit

description: Adversarial visual-layout audit of a Beamer (.tex) or Quarto (.qmd) slide deck. Flags overflow, font inconsistency, box fatigue, spacing, and alignment issues. Use when user says "visual audit", "check the layout", "does this overflow?", "look for visual issues", or "audit the slides." Does NOT check writing or pedagogy — pair with /review-paper or the Writing Reviewer agent for that.

argument-hint: [TEX or QMD filename]

allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write

# Task: Visual Audit of Slide Deck

Perform a thorough visual layout audit of a slide deck.

## Steps

1. **Locate the file** specified in `$ARGUMENTS`. If no argument given, look for `.tex` or `.qmd` files in the current directory and ask the user to confirm which one.

2. **Read the source file** in full.

3. **For Beamer (.tex) files:**
   - Compile with `pdflatex -interaction=nonstopmode <file> 2>&1` and capture output.
   - Flag all `Overfull \hbox` and `Overfull \vbox` warnings — these are overflow indicators.
   - Note any `Underfull` warnings that suggest awkward spacing.

4. **For Quarto (.qmd) files:**
   - Render with `quarto render <file> 2>&1` and capture output.
   - Check rendered output for layout warnings.

5. **Audit the source for every slide/frame for:**
   - **OVERFLOW:** Content likely to exceed slide boundaries (too many items, long lines, large figures without size constraints)
   - **FONT CONSISTENCY:** Inline `\fontsize`, `\small`, `\tiny`, `\footnotesize` overrides — flag each; note if font is pushed below 0.85em equivalent
   - **BOX FATIGUE:** 2+ colored boxes (`\begin{block}`, `\begin{alertblock}`, `tcolorbox`, etc.) on one slide
   - **SPACING:** Missing `\vspace` adjustments, figures without `width=` constraints, equations that could be inlined
   - **LAYOUT:** Slides with no topic sentence or framing line, inconsistent use of color for emphasis

6. **Produce a report** organized by slide/frame with:
   - Frame title
   - Issues found (severity: HIGH / MEDIUM / LOW)
   - Specific fix recommendation

7. **Apply the spacing-first principle** when recommending fixes — in this order:
   1. Reduce vertical spacing (`\vspace{-Xem}`, tighter `itemsep`)
   2. Consolidate list items
   3. Move displayed equations inline
   4. Reduce figure/image size
   5. Last resort only: reduce font size (never below `\fontsize{8.5}{10}` or equivalent 0.85em)
