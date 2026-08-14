#!/bin/bash
# Hook: PreToolUse (Edit, Write, MultiEdit)
# Blocks writes containing banned phrases (AI tells, hard-banned vocabulary).
# Scoped to prose-bearing files only (.md, .tex, .qmd, .Rmd, .txt, no extension).
# Code files and structured data are exempt.

# Banned phrases. Add new ones here, one per line.
# These are HARD blocks — phrases that should never appear in user-attributed prose.
# Entries are extended regex (grep -E). Use \b...\b word boundaries for single
# words so substrings (e.g. "wireless", "firewire") don't trigger false blocks.
BANNED_PHRASES=(
    "load-bearing"
    "load bearing"
    # Block the metaphorical "plumbing" (implementation/infrastructure). Literal
    # uses (a water system) are rare in this prose; the metaphor is the target.
    "\\bplumbing\\b"
    # Block the connection/configuration metaphor (verb forms only), e.g.
    # "wire up the hooks", "wired up", "wiring up", "wired together".
    # The NOUN is allowed: electrical ("the wiring", "a wire") and money
    # ("wire transfer", "funds were wired") uses do not match these.
    "\\bwir(e|es|ed) up\\b"
    "\\bwiring up\\b"
    "\\bwir(e|es|ed) together\\b"
    "\\bwiring together\\b"
    # "gate" / "gated" — hard-blocked 2026-07-24 at the user's direction (was
    # rule-only since 2026-06-11). Blunt by design: catches the metaphor
    # ("gated on X", "the gate is open") at the cost of also blocking literal
    # uses (a physical farm/field gate, a Qualtrics routing gate, "gated
    # community"). Request a softening if a genuine literal use is blocked.
    "\\bgate\\b"
    "\\bgated\\b"
)

INPUT=$(cat)

FILE_PATH=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path','') or d.get('file_path','') or d.get('filePath',''))" 2>/dev/null)

# Get the new content. For Write: 'content'. For Edit: 'new_string'. For MultiEdit: each edit's 'new_string'.
NEW_CONTENT=$(echo "$INPUT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
ti = d.get('tool_input', d)
parts = []
if 'content' in ti:
    parts.append(str(ti['content']))
if 'new_string' in ti:
    parts.append(str(ti['new_string']))
if 'edits' in ti and isinstance(ti['edits'], list):
    for e in ti['edits']:
        if isinstance(e, dict) and 'new_string' in e:
            parts.append(str(e['new_string']))
print('\n'.join(parts))
" 2>/dev/null)

if [ -z "$NEW_CONTENT" ]; then
    exit 0
fi

# EXEMPTION: the rule-definition files themselves. A file whose job is to DEFINE
# the banned vocabulary must be able to contain it — otherwise academic-writing-
# voice.md and its casebook cannot be edited at all (self-referential deadlock,
# hit 2026-08-10). Scoped as narrowly as possible: only .md files living under a
# rules/ directory. These are meta-documents about vocabulary, not the
# user-attributed prose this hook exists to protect. Everything else, including
# every manuscript, memo, email draft and slide, is still checked.
case "$FILE_PATH" in
    */rules/*.md|*/rules/*/*.md)
        exit 0
        ;;
esac

# Scope: only check prose-bearing extensions. Code/data files exempt.
case "$FILE_PATH" in
    *.md|*.tex|*.qmd|*.Rmd|*.txt|*MEMORY*|*HANDOFF*|*TODO*|*README*|*CLAUDE*)
        ;;
    *)
        # Files without an extension or unknown types: also check (covers things like 'aipolicy' style files)
        if [[ "$FILE_PATH" == *.* ]]; then
            # Has an extension we didn't list — skip.
            exit 0
        fi
        ;;
esac

# Check each banned phrase (case-insensitive).
for phrase in "${BANNED_PHRASES[@]}"; do
    if echo "$NEW_CONTENT" | grep -iqE -- "$phrase"; then
        echo "BLOCKED: write contains banned phrase: \"$phrase\""
        echo "File: $FILE_PATH"
        echo ""
        echo "This phrase is on the user's banned list (see ~/.claude/rules/academic-writing-voice.md)."
        echo "Rewrite the passage to describe what the claim or variable actually does, rather than labeling it with this phrase."
        exit 2
    fi
done

exit 0
