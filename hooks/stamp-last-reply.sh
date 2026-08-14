#!/bin/bash
# Records the wall-clock time Claude finished its last reply.
#
# Wired to the Stop hook. statusline.sh reads this file and shows how long ago
# it was, so that coming back to a window after a while tells you whether the
# last message is two minutes or two hours old.
#
# One file per project directory, keyed by a hash of the path, so parallel
# sessions in several projects do not overwrite each other's stamp.
dir="${CLAUDE_PROJECT_DIR:-$PWD}"
key=$(printf "%s" "$dir" | shasum | cut -c1-12)
mkdir -p ~/.claude/state
date +%s > ~/.claude/state/last_reply_"$key"
