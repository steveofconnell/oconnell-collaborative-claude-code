#!/bin/bash
# statusline.sh — Claude Code status line.
#
# Claude Code pipes a JSON object to this script's stdin on every render; the
# script prints a single line shown at the bottom of the TUI. This one shows:
#
#   dir  |  model  |  $cost  |  ctx NN%  |  5hr NN% (Xh Ym)  |  7d NN% (Xh Ym)
#
#   - dir   : the project/repo name (basename of the working directory)
#   - model : the active model's display name
#   - cost  : approximate cumulative spend this session (see rate note below)
#   - ctx   : percentage of the context window used
#   - 5hr   : share of the rolling 5-hour usage limit consumed, with reset ETA
#   - 7d    : share of the rolling 7-day usage limit consumed, with reset ETA
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

# Cumulative session cost, as estimated by Claude Code (cost.total_cost_usd).
# Falls back to "—" on versions/plans that don't report it.
cost_raw=$(echo "$input" | jq -r '.cost.total_cost_usd // empty')
if [ -n "$cost_raw" ]; then
  cost=$(printf "%.2f" "$cost_raw")
else
  cost="—"
fi

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

if [ "$cost" = "—" ]; then
  out=$(printf "%s  |  ctx %s" "$model" "$ctx")
else
  out=$(printf "%s  |  \$%s  |  ctx %s" "$model" "$cost" "$ctx")
fi
[ -n "$five_hr_part" ] && out="$out  |  $five_hr_part"
[ -n "$seven_day_part" ] && out="$out  |  $seven_day_part"
[ -n "$proj" ] && out="$proj  |  $out"
printf "%s" "$out"
