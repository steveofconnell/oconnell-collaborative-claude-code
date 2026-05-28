#!/bin/bash
# open-projects.sh — Opens Claude Code in iTerm2 tabs for active projects.
#
# Reads project list from ~/.claude/CLAUDE.md under "## Active Projects".
# Each line should look like:    - ~/path/to/project   # comment
#
# Optional per-project tab colors are read from a config file alongside this
# script (open-projects.config.sh). See open-projects.config.sh.example.
#
# Usage:
#   open-projects                      # all projects, default model
#   open-projects tractors             # fuzzy-match a single project
#   open-projects --model sonnet tra   # fuzzy-match + model override
#
# This script assumes setup.sh has already run on this device (so the
# symlinks under ~/.claude/ point at the synced config). If those are
# missing it prints instructions and exits.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
CONFIG="$CLAUDE_DIR/CLAUDE.md"
COLOR_CONFIG="$SCRIPT_DIR/open-projects.config.sh"
STAGGER_SECONDS="${CLAUDE_STAGGER:-2}"
PROFILE="${CLAUDE_ITERM_PROFILE:-Claude}"

# ---- argument parsing -------------------------------------------------------
MODEL=""
PROJECT_FILTER=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --model) MODEL="$2"; shift 2 ;;
        -h|--help)
            sed -n '2,18p' "$0" | sed 's/^# \{0,1\}//'
            exit 0 ;;
        *) PROJECT_FILTER="$1"; shift ;;
    esac
done

# ---- preflight --------------------------------------------------------------
if [ ! -f "$CONFIG" ]; then
    echo "Error: $CONFIG not found." >&2
    echo "Run setup.sh from the cloned repo first." >&2
    exit 1
fi

if [ ! -d "/Applications/iTerm.app" ]; then
    echo "Error: iTerm2 not installed." >&2
    echo "Install with: brew install --cask iterm2  (or run setup.sh)." >&2
    exit 1
fi

# ---- per-project tab colors -------------------------------------------------
# A user-provided open-projects.config.sh may define get_tab_color(name) and
# return "bg_r,bg_g,bg_b;fg_r,fg_g,fg_b" (each 0-255). Default: no colors.
get_tab_color() { echo ""; }
if [ -f "$COLOR_CONFIG" ]; then
    # shellcheck disable=SC1090
    source "$COLOR_CONFIG"
fi

# ---- read project list from CLAUDE.md ---------------------------------------
projects=()
in_section=false
while IFS= read -r line; do
    if [[ "$line" =~ ^##[[:space:]]+Active[[:space:]]+Projects ]]; then
        in_section=true; continue
    fi
    if $in_section && [[ "$line" =~ ^## ]]; then break; fi
    if $in_section && [[ "$line" =~ ^-[[:space:]]+ ]]; then
        path="${line#- }"
        path="${path%%#*}"
        path="$(echo "$path" | xargs)"
        path="${path/#\~/$HOME}"
        if [ -d "$path" ]; then
            projects+=("$path")
        else
            echo "Warning: directory not found: $path" >&2
        fi
    fi
done < "$CONFIG"

if [ ${#projects[@]} -eq 0 ]; then
    echo "No projects found in $CONFIG under '## Active Projects'." >&2
    echo "Add lines like:    - ~/Dropbox/MyProject" >&2
    exit 1
fi

# ---- fuzzy-match filter -----------------------------------------------------
if [ -n "$PROJECT_FILTER" ]; then
    filter_lower=$(echo "$PROJECT_FILTER" | tr '[:upper:]' '[:lower:]')
    matched=()
    for proj in "${projects[@]}"; do
        name_lower=$(basename "$proj" | tr '[:upper:]' '[:lower:]')
        if [[ "$name_lower" == *"$filter_lower"* ]]; then
            matched+=("$proj")
        fi
    done
    if [ ${#matched[@]} -eq 0 ]; then
        echo "No project matching '$PROJECT_FILTER'. Active projects:" >&2
        for proj in "${projects[@]}"; do echo "  $(basename "$proj")" >&2; done
        exit 1
    elif [ ${#matched[@]} -gt 1 ]; then
        echo "Ambiguous: '$PROJECT_FILTER' matches multiple:" >&2
        for proj in "${matched[@]}"; do echo "  $(basename "$proj")" >&2; done
        exit 1
    fi
    projects=("${matched[@]}")
    echo "Matched: $(basename "${projects[0]}")"
fi

echo "Opening ${#projects[@]} project(s) with ${STAGGER_SECONDS}s stagger..."

# ---- AppleScript helpers ----------------------------------------------------
color_applescript() {
    local color; color=$(get_tab_color "$1")
    [ -z "$color" ] && return 0
    local bg="${color%;*}" fg="${color#*;}"
    IFS=',' read -r br bg_ bb <<< "$bg"
    IFS=',' read -r fr fg_ fb <<< "$fg"
    echo "set background color to {$((br*257)), $((bg_*257)), $((bb*257)), 0}
set foreground color to {$((fr*257)), $((fg_*257)), $((fb*257)), 0}"
}

# Remap ANSI black on dark backgrounds so terminal output stays legible.
ansi_black_escape() {
    local color; color=$(get_tab_color "$1")
    [ -z "$color" ] && return 0
    echo "printf '\\\\033]1337;SetColors=ansi0=808080:ansi8=a0a0a0\\\\007'"
}

# Capture caller's iTerm window so we can park the caffeinate tab there.
ORIGINAL_WINDOW_ID=$(osascript <<'APPLESCRIPT' 2>/dev/null
    tell application "System Events"
        if not (exists process "iTerm2") then return ""
    end tell
    tell application "iTerm"
        if (count of windows) is 0 then return ""
        return id of current window as string
    end tell
APPLESCRIPT
)

# ---- launch first project in a new window -----------------------------------
proj="${projects[0]}"; name=$(basename "$proj")
echo "  Tab 1: $name"
COLOR_CMD=$(color_applescript "$name")
ANSI_CMD=$(ansi_black_escape "$name")
osascript <<APPLESCRIPT
    tell application "iTerm"
        activate
        create window with profile "$PROFILE"
        delay 0.5
        tell current session of current tab of current window
            set name to "$name"
            ${COLOR_CMD}
            write text "${ANSI_CMD}"
            write text "cd '${proj}' && exec claude ${MODEL:+--model ${MODEL}} --permission-mode bypassPermissions '/start'"
        end tell
    end tell
APPLESCRIPT

# ---- launch remaining projects as tabs --------------------------------------
for ((i=1; i<${#projects[@]}; i++)); do
    proj="${projects[$i]}"; name=$(basename "$proj")
    echo "  Waiting ${STAGGER_SECONDS}s before Tab $((i+1))..."
    sleep "$STAGGER_SECONDS"
    echo "  Tab $((i+1)): $name"
    COLOR_CMD=$(color_applescript "$name")
    ANSI_CMD=$(ansi_black_escape "$name")
    osascript <<APPLESCRIPT
        tell application "iTerm"
            tell current window
                create tab with profile "$PROFILE"
                delay 0.3
                tell current session of current tab
                    set name to "$name"
                    ${COLOR_CMD}
                    write text "${ANSI_CMD}"
                    write text "cd '${proj}' && exec claude ${MODEL:+--model ${MODEL}} --permission-mode bypassPermissions '/start'"
                end tell
            end tell
        end tell
APPLESCRIPT
done

# Single-project mode: skip caffeinate.
if [ -n "$PROJECT_FILTER" ]; then
    echo "Single project launched: $(basename "${projects[0]}")"
    exit 0
fi

# ---- park a caffeinate tab in the original window ---------------------------
if [ -n "$ORIGINAL_WINDOW_ID" ]; then
    osascript <<APPLESCRIPT
        tell application "iTerm"
            try
                set origWin to (first window whose id is ${ORIGINAL_WINDOW_ID})
                tell origWin
                    create tab with profile "$PROFILE"
                    delay 0.3
                    tell current session of current tab
                        set name to "caffeinate"
                        write text "exec caffeinate -di"
                    end tell
                end tell
            end try
        end tell
APPLESCRIPT
    echo "All projects launched. Caffeinate running in original terminal window."
else
    osascript <<APPLESCRIPT
        tell application "iTerm"
            tell current window
                create tab with profile "$PROFILE"
                delay 0.3
                tell current session of current tab
                    set name to "caffeinate"
                    write text "exec caffeinate -di"
                end tell
                select first tab
            end tell
        end tell
APPLESCRIPT
    echo "All projects launched. Caffeinate running in last tab (no original window detected)."
fi
