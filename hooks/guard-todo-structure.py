#!/usr/bin/env python3
"""PreToolUse hook (Write, Edit): keep a TODO.md's Pending section a list of open tasks.

Computes the file as it would be after the write, and refuses the write if it adds any
of these to the Pending section (existing violations are tolerated, so old files can
still be edited; the write may not make them worse):

  - a checked item ("- [x]"): it belongs under Completed
  - prose: a paragraph line that is not a task, a sub-bullet, a heading, or a
    "Dependency chain:" line
  - an item with more than MAX_SUBBULLETS sub-bullets

See rules/task-management.md.
"""
import json
import os
import re
import sys

MAX_SUBBULLETS = 3
TASK = re.compile(r"^- \[[ xX]\]")
SUB = re.compile(r"^\s+[-*] ")


def pending_lines(text):
    out, on = [], False
    for line in text.splitlines():
        if re.match(r"^## ", line):
            on = line.strip().lower().startswith("## pending")
            continue
        if on:
            out.append(line)
    return out


def violations(text):
    checked, prose, long_items = 0, 0, 0
    subs, in_item, prev_blank = 0, False, True
    for line in pending_lines(text):
        s = line.strip()
        if TASK.match(line):
            if subs > MAX_SUBBULLETS:
                long_items += 1
            subs, in_item = 0, True
            if re.match(r"^- \[[xX]\]", line):
                checked += 1
        elif SUB.match(line) and in_item:
            subs += 1
        elif not s or s.startswith("#") or s.lower().startswith("dependency chain"):
            if s.startswith("#"):
                if subs > MAX_SUBBULLETS:
                    long_items += 1
                subs, in_item = 0, False
        elif line[:1].isspace() and in_item:
            pass  # wrapped continuation of a sub-bullet
        else:
            prose += 1
    if subs > MAX_SUBBULLETS:
        long_items += 1
    return {"checked items under Pending": checked,
            "prose lines under Pending": prose,
            f"items with more than {MAX_SUBBULLETS} sub-bullets": long_items}


def main():
    try:
        d = json.load(sys.stdin)
    except Exception:
        return 0
    ti = d.get("tool_input", {}) or {}
    path = ti.get("file_path", "")
    if os.path.basename(path) != "TODO.md":
        return 0
    try:
        before = open(path, encoding="utf-8").read()
    except (FileNotFoundError, UnicodeDecodeError):
        before = ""
    tool = d.get("tool_name")
    if tool == "Write":
        after = str(ti.get("content", ""))
    elif tool == "Edit":
        old, new = ti.get("old_string", ""), ti.get("new_string", "")
        if not old or old not in before:
            return 0
        after = before.replace(old, new) if ti.get("replace_all") else before.replace(old, new, 1)
    else:
        return 0

    vb, va = violations(before), violations(after)
    worse = [f"{k}: {vb[k]} -> {va[k]}" for k in va if va[k] > vb[k]]
    if not worse:
        return 0
    sys.stderr.write(
        f"BLOCKED: this write to {path} makes the Pending section worse ("
        + "; ".join(worse) + "). Pending holds open tasks only: one line each, a 'Done when' "
        "sub-bullet and at most two more short sub-bullets. Finished items move to Completed; "
        "history and narrative go in the handoff or DECISIONS.md, not the TODO. See "
        "rules/task-management.md.\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
