#!/usr/bin/env python3
"""PreToolUse hook (Write): refuse new script files in a project's analysis folders.

Blocks the CREATION of a new .R/.py/.do file (editing or overwriting an existing file
is never blocked) in any folder that belongs to a project's processing, analysis or
manuscript tree, unless both hold:

  1. the folder holds fewer than MAX_SCRIPTS scripts already, and
  2. the new file's first lines carry an approval line, written only after the
     user has approved the new file in the conversation:
         # New script approved by <name> YYYY-MM-DD: <why a new file>

Exempt: .workspace/ (scratch and working files), config folders, and anything not
under a numbered or analysis-type project folder. See rules/project-structure.md,
"New script files".
"""
import json
import os
import re
import sys

MAX_SCRIPTS = 8
SCRIPT_EXT = (".r", ".py", ".do")
APPROVAL = re.compile(r"new script approved by .+\d{4}-\d{2}-\d{2}\s*:\s*\S", re.I)
# A path component that marks a project's pipeline or manuscript tree.
SCOPED_DIR = re.compile(r"^\d|processing|analysis|code|manuscript|cleaning", re.I)
EXEMPT_PART = {".workspace", ".claude", ".claudeconfig", "claude-research-config",
               "scratch", "hooks", "tools", "installer", "skills", "node_modules"}


def main():
    try:
        d = json.load(sys.stdin)
    except Exception:
        return 0
    if d.get("tool_name") != "Write":
        return 0
    ti = d.get("tool_input", {}) or {}
    path = ti.get("file_path", "")
    if not path.lower().endswith(SCRIPT_EXT) or os.path.exists(path):
        return 0
    parts = os.path.normpath(os.path.abspath(path)).split(os.sep)[:-1]
    if any(p in EXEMPT_PART for p in parts):
        return 0
    if not any(SCOPED_DIR.search(p) for p in parts[-3:]):
        return 0

    folder = os.path.dirname(os.path.abspath(path))
    try:
        existing = [f for f in os.listdir(folder)
                    if f.lower().endswith(SCRIPT_EXT) and os.path.isfile(os.path.join(folder, f))]
    except FileNotFoundError:
        existing = []

    name = os.path.basename(path)
    if len(existing) >= MAX_SCRIPTS:
        sys.stderr.write(
            f"BLOCKED: {folder} already holds {len(existing)} scripts (limit {MAX_SCRIPTS}). "
            f"No new script file there, approved or not. Put this work into an existing script "
            f"as a labeled section or an option. If the folder genuinely needs consolidating, "
            f"propose the consolidation to the user; the refactoring protocol moves the "
            f"originals into archived_pre_refactor/ first, which brings the count down.\n")
        return 2

    head = "\n".join(str(ti.get("content", "")).splitlines()[:15])
    if APPROVAL.search(head):
        return 0

    sys.stderr.write(
        f"BLOCKED: new script file {name} in {folder}. New script files need the user's "
        f"approval. First try to add this as a section or an option in an existing script "
        f"there ({', '.join(sorted(existing)) or 'none yet'}). A variant, a note version, a "
        f"copy/promote step, a one-off check or a referee-response check never gets its own "
        f"file. If a new file is genuinely warranted (new data source, a step over two "
        f"minutes, or a new analysis family), ask the user in the conversation, and only "
        f"after they say yes put this line in the file's first lines:\n"
        f"  # New script approved by <name> YYYY-MM-DD: <why a new file>\n"
        f"Exploratory work goes in .workspace/scratch/, which is not checked.\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
