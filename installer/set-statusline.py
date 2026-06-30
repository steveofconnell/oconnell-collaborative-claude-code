#!/usr/bin/env python3
"""
set-statusline.py — point a personal settings.json at the shared status line,
idempotently and without clobbering a status line the user already configured.

Usage:
    python3 set-statusline.py <settings.json> [command]

`command` defaults to "bash ~/.claude/statusline.sh" (statusline.sh is symlinked
into ~/.claude/ by setup.sh, so this path is the same on every device).

Why this exists: the status line is a personal setting (it lives in each user's
settings.json, not in the shared repo), but this config ships a status line and
we want a fresh install to get it by default. setup.sh calls this so a new
settings.json gets the status line wired up, while an existing custom one is left
alone.

Safety properties (this edits a user's personal config, so it must not destroy):
  - NON-DESTRUCTIVE: if a statusLine is already set to something else, it is left
    untouched — the user's choice wins. It is only (re)written when absent or when
    it already points at this repo's statusline.sh (so updates to the command stay
    in sync).
  - IDEMPOTENT: re-running when the value already matches makes no changes.
  - BACKUP FIRST: writes settings.json.bak.<timestamp> before any change.
  - ATOMIC + VALIDATED: writes a temp file, re-parses it, then os.replace()s.
  - SYMLINK-SAFE: resolves the real file via realpath so a symlinked settings.json
    stays a symlink (its target is rewritten, not the link).
"""
import json
import os
import shutil
import sys
import time

DEFAULT_COMMAND = "bash ~/.claude/statusline.sh"


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("usage: set-statusline.py <settings.json> [command]", file=sys.stderr)
        return 2

    settings_path = os.path.realpath(os.path.expanduser(sys.argv[1]))
    command = sys.argv[2] if len(sys.argv) == 3 else DEFAULT_COMMAND

    settings = {}
    if os.path.exists(settings_path) and os.path.getsize(settings_path) > 0:
        try:
            with open(settings_path) as f:
                settings = json.load(f)
        except json.JSONDecodeError as e:
            print(f"set-statusline: ERROR — {settings_path} is not valid JSON ({e}); "
                  "leaving it untouched.", file=sys.stderr)
            return 1

    if not isinstance(settings, dict):
        print("set-statusline: ERROR — settings.json is not a JSON object; leaving untouched.",
              file=sys.stderr)
        return 1

    existing = settings.get("statusLine")
    existing_cmd = existing.get("command") if isinstance(existing, dict) else None

    # Leave a user's own custom status line alone; only manage ours.
    if existing_cmd and "statusline.sh" not in existing_cmd:
        print("set-statusline: a custom statusLine is already set; leaving it untouched.")
        return 0

    desired = {"type": "command", "command": command}
    if existing == desired:
        print("set-statusline: status line already configured; no changes.")
        return 0

    if os.path.exists(settings_path):
        bak = f"{settings_path}.bak.{int(time.time())}"
        shutil.copy2(settings_path, bak)
        print(f"set-statusline: backed up -> {bak}")

    settings["statusLine"] = desired

    tmp = settings_path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(settings, f, indent=2)
        f.write("\n")
    with open(tmp) as f:  # validate before replacing
        json.load(f)
    os.replace(tmp, settings_path)
    print(f"set-statusline: set statusLine -> '{command}' in {settings_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
