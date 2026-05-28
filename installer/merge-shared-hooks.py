#!/usr/bin/env python3
"""
merge-shared-hooks.py — merge the repo's shared hook entries into a personal
settings.json, additively and idempotently.

Usage:
    python3 merge-shared-hooks.py <settings.json> <shared-hooks.json>

Why this exists: hook *scripts* propagate to collaborators (the repo's hooks/
dir is symlinked into ~/.claude/hooks/), but the hook *entries* that trigger them
live in settings.json, which is personal and not shared. Without this merge,
collaborators have the scripts but nothing triggers them. setup.sh calls this on
every run so the entries stay in sync, including for people who already have a
settings.json.

Safety properties (this edits a user's personal config, so it must not destroy):
  - ADDITIVE: only ever appends hook entries; never removes or rewrites the
    user's existing hooks, sounds, model, statusLine, permissions, or anything else.
  - IDEMPOTENT: a hook command already present under its event is never added
    again, so re-running makes no changes.
  - BACKUP FIRST: writes settings.json.bak.<timestamp> before any change.
  - ATOMIC + VALIDATED: writes to a temp file, re-parses it, then os.replace()s.
  - SYMLINK-SAFE: resolves the real file via realpath so a symlinked
    settings.json stays a symlink (its target is rewritten, not the link).
"""
import json
import os
import shutil
import sys
import time


def main():
    if len(sys.argv) != 3:
        print("usage: merge-shared-hooks.py <settings.json> <shared-hooks.json>", file=sys.stderr)
        return 2

    settings_path = os.path.realpath(os.path.expanduser(sys.argv[1]))
    shared_path = os.path.expanduser(sys.argv[2])

    with open(shared_path) as f:
        shared = json.load(f)

    settings = {}
    if os.path.exists(settings_path) and os.path.getsize(settings_path) > 0:
        try:
            with open(settings_path) as f:
                settings = json.load(f)
        except json.JSONDecodeError as e:
            print(f"merge-shared-hooks: ERROR — {settings_path} is not valid JSON ({e}); "
                  "leaving it untouched.", file=sys.stderr)
            return 1

    if not isinstance(settings, dict):
        print("merge-shared-hooks: ERROR — settings.json is not a JSON object; leaving untouched.",
              file=sys.stderr)
        return 1

    hooks = settings.setdefault("hooks", {})
    added = 0

    for event, groups in shared.items():
        if event.startswith("_") or not isinstance(groups, list):
            continue  # skip comment keys / non-event entries
        existing_groups = hooks.setdefault(event, [])
        existing_cmds = {
            h.get("command")
            for g in existing_groups if isinstance(g, dict)
            for h in g.get("hooks", []) if isinstance(h, dict) and h.get("command")
        }
        for g in groups:
            new_hooks = [h for h in g.get("hooks", []) if h.get("command") not in existing_cmds]
            if new_hooks:
                grp = {k: v for k, v in g.items() if k != "hooks"}
                grp["hooks"] = new_hooks
                existing_groups.append(grp)
                for h in new_hooks:
                    existing_cmds.add(h["command"])
                    added += 1

    if added == 0:
        print("merge-shared-hooks: all shared hooks already present; no changes.")
        return 0

    if os.path.exists(settings_path):
        bak = f"{settings_path}.bak.{int(time.time())}"
        shutil.copy2(settings_path, bak)
        print(f"merge-shared-hooks: backed up -> {bak}")

    tmp = settings_path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(settings, f, indent=2)
        f.write("\n")
    with open(tmp) as f:  # validate before replacing
        json.load(f)
    os.replace(tmp, settings_path)
    print(f"merge-shared-hooks: added {added} hook command(s) to {settings_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
