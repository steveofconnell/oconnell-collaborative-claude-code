#!/usr/bin/env python3
"""Hook: PostToolUse (Bash, Edit, Write)
Tracks approximate context usage via tool call count and warns
when approaching the compression threshold.

Heuristic: Each tool call uses ~500-2000 tokens of context.
Typical context budget is ~180K tokens, so ~200 tool calls is a rough ceiling.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path

def get_session_dir():
    cwd = os.getcwd()
    project_hash = hashlib.md5(cwd.encode()).hexdigest()[:12]
    session_dir = Path.home() / ".claude" / "sessions" / project_hash
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir

def main():
    try:
        session_dir = get_session_dir()
        state_file = session_dir / "context-monitor-state.json"

        # Load or initialize state
        if state_file.exists():
            with open(state_file) as f:
                state = json.load(f)
        else:
            state = {"tool_calls": 0, "last_warning_at": 0, "session_start": time.time()}

        state["tool_calls"] = state.get("tool_calls", 0) + 1
        count = state["tool_calls"]

        # Estimate context usage (rough heuristic)
        estimated_pct = min(count / 200 * 100, 100)

        # Throttle warnings to every 60 seconds
        now = time.time()
        last_warn = state.get("last_warning_at", 0)
        throttled = (now - last_warn) < 60

        message = None

        if estimated_pct >= 90 and not throttled:
            message = f"CONTEXT WARNING (est. ~{estimated_pct:.0f}%): Auto-compaction is imminent. Save any important context to files now."
            state["last_warning_at"] = now
        elif estimated_pct >= 80 and not throttled:
            message = f"CONTEXT NOTE (est. ~{estimated_pct:.0f}%): Approaching context limit. Consider saving key decisions or findings to .workspace/."
            state["last_warning_at"] = now
        elif estimated_pct >= 55 and not throttled and state.get("last_warning_at", 0) == 0:
            message = f"Context usage est. ~{estimated_pct:.0f}%. Midpoint — if you've learned anything memory-worthy, now is a good time to save it."
            state["last_warning_at"] = now

        with open(state_file, "w") as f:
            json.dump(state, f)

        if message:
            print(message)

    except Exception:
        # Fail open
        pass

if __name__ == "__main__":
    main()
