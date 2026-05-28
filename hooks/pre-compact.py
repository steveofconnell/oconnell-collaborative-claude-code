#!/usr/bin/env python3
"""Hook: PreCompact
Captures active plan, current task, and recent decisions before context compression.
Saves state to a JSON file that post-compact-restore.py reads on resume.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

def get_session_dir():
    """Create a session state directory based on the working directory."""
    cwd = os.getcwd()
    project_hash = hashlib.md5(cwd.encode()).hexdigest()[:12]
    session_dir = Path.home() / ".claude" / "sessions" / project_hash
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir

def find_active_plan(cwd):
    """Look for the most recent plan file in .workspace/ or quality_reports/plans/."""
    plan_dirs = [
        Path(cwd) / ".workspace",
        Path(cwd) / "quality_reports" / "plans",
    ]
    plans = []
    for d in plan_dirs:
        if d.exists():
            plans.extend(d.glob("*.md"))
    if not plans:
        return None
    # Return the most recently modified plan
    return str(max(plans, key=lambda p: p.stat().st_mtime))

def find_recent_handoff(cwd):
    """Find the most recent handoff file."""
    ws = Path(cwd) / ".workspace"
    if not ws.exists():
        return None
    handoffs = sorted(ws.glob("HANDOFF_*.txt"))
    return str(handoffs[-1]) if handoffs else None

def main():
    try:
        cwd = os.getcwd()
        session_dir = get_session_dir()

        state = {
            "working_directory": cwd,
            "active_plan": find_active_plan(cwd),
            "recent_handoff": find_recent_handoff(cwd),
        }

        # Read active plan content if found
        if state["active_plan"] and os.path.exists(state["active_plan"]):
            try:
                with open(state["active_plan"]) as f:
                    state["plan_content"] = f.read()[:2000]  # First 2000 chars
            except Exception:
                pass

        state_file = session_dir / "pre-compact-state.json"
        with open(state_file, "w") as f:
            json.dump(state, f, indent=2)

        # Print to stderr (hooks use stderr for logging)
        print(f"Pre-compact state saved to {state_file}", file=sys.stderr)

    except Exception:
        # Fail open — never block compaction
        pass

if __name__ == "__main__":
    main()
