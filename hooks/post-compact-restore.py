#!/usr/bin/env python3
"""Hook: SessionStart (on resume after compaction)
Restores context from pre-compact snapshot so the session can continue
without losing track of the active plan or task.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

def get_session_dir():
    cwd = os.getcwd()
    project_hash = hashlib.md5(cwd.encode()).hexdigest()[:12]
    return Path.home() / ".claude" / "sessions" / project_hash

def main():
    try:
        session_dir = get_session_dir()
        state_file = session_dir / "pre-compact-state.json"

        if not state_file.exists():
            return

        with open(state_file) as f:
            state = json.load(f)

        parts = []
        parts.append("SESSION CONTEXT RESTORED AFTER COMPACTION:")

        if state.get("active_plan"):
            parts.append(f"  Active plan: {state['active_plan']}")
            if state.get("plan_content"):
                # Show first 500 chars of plan
                preview = state["plan_content"][:500]
                parts.append(f"  Plan preview: {preview}")

        if state.get("recent_handoff"):
            parts.append(f"  Recent handoff: {state['recent_handoff']}")

        if len(parts) > 1:
            print("\n".join(parts))

    except Exception:
        # Fail open
        pass

if __name__ == "__main__":
    main()
