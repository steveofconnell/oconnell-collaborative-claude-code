#!/usr/bin/env bash
# =============================================================================
# session_tracker.sh — collaborator session-presence tracker (global hook)
# =============================================================================
# In shared Dropbox project folders, several people may have Claude Code open at
# once. This shows who is *actively working right now*, so collaborators don't
# collide or duplicate effort.
#
# Configured globally in ~/.claude/settings.json (see .claudeconfig/settings.json):
#   SessionStart  -> open    (drop a lightweight "pending" file; NOT yet a marker)
#   PostToolUse   -> beat     (after a grace period, promote to a real marker;
#                              then refresh it, throttled, as work continues)
#   SessionEnd    -> close    (remove this session's marker + pending file)
# Manual query (run inside a project):
#   ~/.claude/hooks/session_tracker.sh status
#
# Design notes:
#  - GRACE PERIOD: opening a project and closing it after /start (a very common
#    "decided not to work on this" pattern) must NOT register a session. So
#    SessionStart only writes a `.pending` file; a real `.session` marker is
#    created only once the session has been active for GRACE_SECS — longer than
#    the /start routine takes. Abandon-after-start leaves nothing behind.
#  - SELF-CLEANING: closing a window often does not fire SessionEnd. So `status`
#    (and every beat) prunes markers and pendings older than ACTIVE_WINDOW_SECS.
#    A session only appears while it is genuinely being worked; stale/crashed
#    ones disappear on their own. No "forgot to close" bookkeeping needed.
#
# Markers live in each project's .workspace/sessions/ (keyed by CLAUDE_PROJECT_DIR),
# so config stays global while runtime state stays in the project's .workspace/.
# Only activates in projects that already have a .workspace/ directory.
# All modes except `status` are silent (zero stdout, zero tokens).
# macOS only (uses BSD `stat -f` / `date -r`).
# =============================================================================

set -u

action="${1:-status}"

GRACE_SECS=120            # session must outlive the /start routine before it counts
ACTIVE_WINDOW_SECS=900    # marker not refreshed within this is dead -> pruned
BEAT_THROTTLE_SECS=60     # min seconds between marker rewrites (limits Dropbox churn)

proj="${CLAUDE_PROJECT_DIR:-$PWD}"
if [ ! -d "$proj/.workspace" ]; then
  [ "$action" = "status" ] && echo "No active sessions."
  exit 0
fi

dir="$proj/.workspace/sessions"
mkdir -p "$dir"

user="$(whoami)"
host="$(hostname -s 2>/dev/null || hostname)"
marker="$dir/${user}@${host}.session"
pending="$dir/${user}@${host}.pending"
now_iso="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
now_epoch="$(date +%s)"

person_name() {
  # Optional: map local usernames to display names. Add your own entries, e.g.:
  #   case "$1" in
  #     jdoe)  echo "Jane Doe" ;;
  #     *)     echo "$1" ;;
  #   esac
  case "$1" in
    *)              echo "$1" ;;
  esac
}

mtime() { stat -f %m "$1" 2>/dev/null || echo 0; }
field() { grep "^$1:" "$2" 2>/dev/null | sed "s/^$1: //"; }

write_marker() {   # $1 = opened ISO
  {
    echo "person: $(person_name "$user")"
    echo "username: $user"
    echo "host: $host"
    echo "opened: $1"
    echo "last_activity: $now_iso"
  } > "$marker"
}

gc() {   # prune dead markers and abandoned pendings (handles missing SessionEnd)
  shopt -s nullglob 2>/dev/null || true
  for f in "$dir"/*.session "$dir"/*.pending; do
    [ $(( now_epoch - $(mtime "$f") )) -gt "$ACTIVE_WINDOW_SECS" ] && rm -f "$f"
  done
}

case "$action" in
  open)
    rm -f "$marker"          # reset any leftover marker for this window
    : > "$pending"           # pending mtime = session start time
    ;;

  beat)
    if [ -f "$marker" ]; then
      # throttle refreshes
      if [ $(( now_epoch - $(mtime "$marker") )) -ge "$BEAT_THROTTLE_SECS" ]; then
        opened="$(field opened "$marker")"; [ -z "$opened" ] && opened="$now_iso"
        write_marker "$opened"
      fi
    elif [ -f "$pending" ]; then
      start="$(mtime "$pending")"
      if [ $(( now_epoch - start )) -ge "$GRACE_SECS" ]; then
        write_marker "$(date -u -r "$start" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || echo "$now_iso")"
        rm -f "$pending"
      fi
    else
      : > "$pending"         # activity with no SessionStart -> start the clock
    fi
    gc
    ;;

  close)
    rm -f "$marker" "$pending"
    ;;

  status)
    gc
    shopt -s nullglob 2>/dev/null || true
    found=0
    for f in "$dir"/*.session; do
      found=1
      p="$(field person "$f")"
      o="$(field opened "$f")"
      mins=$(( (now_epoch - $(mtime "$f")) / 60 ))
      self=""; [ "$f" = "$marker" ] && self=" (this session)"
      echo "ACTIVE — ${p}${self}: working since ${o} (last active ${mins}m ago)"
    done
    [ "$found" -eq 0 ] && echo "No active sessions."
    ;;

  *)
    echo "usage: session_tracker.sh {open|beat|close|status}" >&2
    exit 2
    ;;
esac

exit 0
