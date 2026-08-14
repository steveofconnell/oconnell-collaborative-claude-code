#!/bin/bash
# statusline.sh — Claude Code status line.
#
# Claude Code pipes a JSON object to this script's stdin on every render; the
# script prints a single line shown at the bottom of the TUI. This one shows:
#
#   dir  |  model  |  ctx NN%  |  5hr NN% (Xh Ym)  |  7d NN% (Xh Ym)  |  replied HH:MM (Xh Ym ago)
#
#   - dir   : the project/repo name (basename of the working directory)
#   - model : the active model's display name
#   - ctx   : percentage of the context window used
#   - 5hr   : share of the rolling 5-hour usage limit consumed, with reset ETA
#   - 7d    : share of the rolling 7-day usage limit consumed, with reset ETA
#   - replied: when the last reply finished, and how long ago. Requires the
#             stamp-last-reply.sh Stop hook; the field is omitted without it.
#
# The 5hr/7d parts only appear when Claude Code supplies rate-limit data, so
# this degrades gracefully on plans or versions that don't report it.
#
# Wired up by setup.sh, which symlinks this into ~/.claude/ and points the
# statusLine command in settings.json at it. Requires `jq`.

input=$(cat)

# Project name: prefer the git repo name, else the basename of the working dir.
proj=$(echo "$input" | jq -r '.workspace.repo.name // .workspace.current_dir // empty')
[ -n "$proj" ] && proj=$(basename "$proj")

model=$(echo "$input" | jq -r '.model.display_name // "Unknown model"')

used=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
if [ -n "$used" ]; then
  ctx=$(printf "%.0f%%" "$used")
else
  ctx="—"
fi

five_hr=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
seven_day=$(echo "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty')
five_hr_reset=$(echo "$input" | jq -r '.rate_limits.five_hour.resets_at // empty')
seven_day_reset=$(echo "$input" | jq -r '.rate_limits.seven_day.resets_at // empty')
now=$(date +%s)

# Format "Xh Ym" or "Ym" for a reset timestamp (epoch seconds).
fmt_eta() {
  local target=$1
  local delta=$(( target - now ))
  if [ "$delta" -le 0 ]; then
    echo "now"
  elif [ "$delta" -ge 3600 ]; then
    local h=$(( delta / 3600 ))
    local m=$(( (delta % 3600) / 60 ))
    echo "${h}h${m}m"
  else
    local m=$(( delta / 60 ))
    echo "${m}m"
  fi
}

five_hr_part=""
if [ -n "$five_hr" ]; then
  five_hr_part=$(printf "5hr %.0f%%" "$five_hr")
  [ -n "$five_hr_reset" ] && five_hr_part="$five_hr_part ($(fmt_eta "$five_hr_reset"))"
fi

seven_day_part=""
if [ -n "$seven_day" ]; then
  seven_day_part=$(printf "7d %.0f%%" "$seven_day")
  [ -n "$seven_day_reset" ] && seven_day_part="$seven_day_part ($(fmt_eta "$seven_day_reset"))"
fi

# Time since the last reply finished, stamped by the Stop hook. Shows when a
# window has been left idle: "replied 14:32 (2h11m ago)".
last_part=""
key=$(printf "%s" "${CLAUDE_PROJECT_DIR:-$PWD}" | shasum | cut -c1-12)
stamp_file=~/.claude/state/last_reply_"$key"
if [ -f "$stamp_file" ]; then
  stamp=$(cat "$stamp_file" 2>/dev/null)
  if [ -n "$stamp" ]; then
    ago=$(( now - stamp ))
    clock=$(date -r "$stamp" +%H:%M 2>/dev/null)
    if [ "$ago" -ge 3600 ]; then
      last_part="replied $clock ($(( ago / 3600 ))h$(( (ago % 3600) / 60 ))m ago)"
    elif [ "$ago" -ge 60 ]; then
      last_part="replied $clock ($(( ago / 60 ))m ago)"
    else
      last_part="replied $clock (just now)"
    fi
  fi
fi

out=$(printf "%s  |  ctx %s" "$model" "$ctx")
[ -n "$last_part" ] && out="$out  |  $last_part"
[ -n "$five_hr_part" ] && out="$out  |  $five_hr_part"
[ -n "$seven_day_part" ] && out="$out  |  $seven_day_part"
[ -n "$proj" ] && out="$proj  |  $out"
printf "%s" "$out"
