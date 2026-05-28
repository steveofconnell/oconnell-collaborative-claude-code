#!/bin/bash
# setup.sh — One-shot bootstrap for the collaborative Claude Code config.
#
# This script does ALL of the following on the machine you run it on:
#
#   1. Creates a cross-device sync folder (default ~/Dropbox/.claudeconfig).
#      Personal config files (CLAUDE.md, settings.json, settings.local.json,
#      open-projects.sh, iTerm/Rectangle configs) live there. Every machine's
#      ~/.claude/ is symlinked into it, so configs move between devices via
#      Dropbox/iCloud automatically.
#   2. Installs Homebrew (if missing).
#   3. Installs iTerm2 (required — colored per-project tabs do not work in
#      Terminal.app).
#   4. Installs Rectangle (window manager, required for the keyboard
#      shortcut workflow).
#   5. Installs the iTerm2 "Claude" Dynamic Profile and tab-switching
#      shortcuts (Option+Cmd+Left/Right).
#   6. Imports Rectangle keyboard shortcuts.
#   7. Installs the multi-project launcher (open-projects.sh) into the sync
#      folder, adds an `open-projects` alias to ~/.zshrc, and seeds an
#      example tab-color config.
#   8. Symlinks shared config (rules/, hooks/, skills/, agents/) from this
#      cloned repo into ~/.claude/, so updates land via `git pull`.
#
# Usage:
#   bash setup.sh                                        # interactive
#   bash setup.sh --sync-folder ~/Dropbox/.claudeconfig  # non-interactive
#   bash setup.sh --minimal                              # skip iTerm/Rectangle/launcher
#                                                        # (only symlinks shared dirs)
#
# Safe to re-run: every step is idempotent.

set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

# ---- argument parsing -------------------------------------------------------
SYNC_FOLDER=""
MINIMAL=false
while [[ $# -gt 0 ]]; do
    case "$1" in
        --sync-folder) SYNC_FOLDER="$2"; shift 2 ;;
        --minimal)     MINIMAL=true; shift ;;
        -h|--help)
            sed -n '2,30p' "$0" | sed 's/^# \{0,1\}//'
            exit 0 ;;
        *) echo "Unknown argument: $1" >&2; exit 1 ;;
    esac
done

echo ""
echo "==============================================================="
echo "  Claude Code collaborative config — bootstrap"
echo "==============================================================="
echo ""
echo "Repo: $REPO_DIR"
echo ""

# ---- guard against legacy state --------------------------------------------
if [ -L "$CLAUDE_DIR" ]; then
    echo "ERROR: ~/.claude is itself a symlink to: $(readlink "$CLAUDE_DIR")"
    echo ""
    echo "An older version of this script symlinked ~/.claude wholesale,"
    echo "which breaks Claude Code's per-project state. Restore your"
    echo "backup before re-running:"
    echo "  ls ~/.claude.backup.*"
    echo "  rm ~/.claude && mv ~/.claude.backup.XXXXXXXXXX ~/.claude"
    exit 1
fi
mkdir -p "$CLAUDE_DIR"

# ---- activate the publish guard (git pre-push scanner) ----------------------
# tools/pre-push runs tools/personal-content-scan.sh before every push from this
# clone, blocking personal content from reaching the shared repo. Setting
# core.hooksPath makes git use the tracked tools/ hook. Harmless for collaborators
# (the scanner runs in generic mode unless they add their own patterns file).
if [ -f "$REPO_DIR/tools/pre-push" ]; then
    if git -C "$REPO_DIR" config core.hooksPath tools 2>/dev/null; then
        echo "Publish guard active: git pre-push -> tools/personal-content-scan.sh"
    else
        echo "WARNING: could not set core.hooksPath; publish guard inactive."
    fi
    echo ""
fi

# ============================================================================
# MINIMAL MODE: just symlink shared dirs and exit (the old behavior).
# ============================================================================
if $MINIMAL; then
    echo "Minimal mode: symlinking shared subdirs only."
    SHARED_DIRS=("rules" "hooks" "skills" "agents")
    for dir in "${SHARED_DIRS[@]}"; do
        src="$REPO_DIR/$dir"
        dst="$CLAUDE_DIR/$dir"
        [ ! -d "$src" ] && continue
        if [ -L "$dst" ]; then
            [ "$(readlink "$dst")" = "$src" ] && { echo "  $dir/ already linked"; continue; }
            rm "$dst"; ln -s "$src" "$dst"; echo "  $dir/ -> $src (updated)"
        elif [ -d "$dst" ]; then
            echo "  WARNING: ~/.claude/$dir/ exists as a real dir — skipping. Remove it to use the shared version."
        else
            ln -s "$src" "$dst"; echo "  $dir/ -> $src"
        fi
    done
    echo ""
    echo "Done (minimal). Open Claude Code in any project and run /start."
    exit 0
fi

# ============================================================================
# FULL BOOTSTRAP
# ============================================================================

# ---- 1. sync folder ---------------------------------------------------------
echo "----- Step 1/8: cross-device sync folder ----------------------"
echo ""
echo "Personal config (CLAUDE.md, settings.json, the launcher script) lives"
echo "in a folder synced across your devices. Default: ~/Dropbox/.claudeconfig"
echo "Other options: any iCloud Drive / OneDrive / Google Drive path."
echo ""

if [ -z "$SYNC_FOLDER" ]; then
    default_sync="$HOME/Dropbox/.claudeconfig"
    if [ ! -d "$HOME/Dropbox" ]; then
        icloud="$HOME/Library/Mobile Documents/com~apple~CloudDocs/.claudeconfig"
        if [ -d "$HOME/Library/Mobile Documents/com~apple~CloudDocs" ]; then
            default_sync="$icloud"
        fi
    fi
    read -r -p "Sync folder path [$default_sync]: " SYNC_FOLDER
    SYNC_FOLDER="${SYNC_FOLDER:-$default_sync}"
    SYNC_FOLDER="${SYNC_FOLDER/#\~/$HOME}"
fi

if [ ! -d "$SYNC_FOLDER" ]; then
    mkdir -p "$SYNC_FOLDER"
    echo "  Created $SYNC_FOLDER"
else
    echo "  Using existing $SYNC_FOLDER"
fi
echo ""

# ---- 2. move/seed personal config files into the sync folder ---------------
echo "----- Step 2/8: personal config files ------------------------"
echo ""

seed_or_move() {
    local fname="$1" stub_content="$2"
    local sync_path="$SYNC_FOLDER/$fname"
    local home_path="$CLAUDE_DIR/$fname"

    if [ -f "$sync_path" ] && [ ! -L "$sync_path" ]; then
        echo "  $fname: using existing in sync folder"
    elif [ -f "$home_path" ] && [ ! -L "$home_path" ]; then
        echo "  $fname: moving real file from ~/.claude/ -> sync folder"
        mv "$home_path" "$sync_path"
    elif [ ! -f "$sync_path" ]; then
        echo "  $fname: seeding stub in sync folder"
        printf '%s\n' "$stub_content" > "$sync_path"
    fi

    if [ -L "$home_path" ] && [ "$(readlink "$home_path")" = "$sync_path" ]; then
        :
    else
        rm -f "$home_path"
        ln -s "$sync_path" "$home_path"
    fi
}

CLAUDE_MD_STUB='# Global Claude Code Config

This file is your personal global config. It is loaded for every Claude Code
session on every device. Edit freely; changes sync across machines via the
folder this file lives in.

## Active Projects
# List one project per line (open-projects.sh reads this section):
# - ~/Dropbox/MyProject     # short comment shown in tab title
'
seed_or_move "CLAUDE.md" "$CLAUDE_MD_STUB"

SETTINGS_JSON_STUB='{
  "hooks": {
    "Notification": [{"hooks": [{"type": "command", "command": "afplay /System/Library/Sounds/Sosumi.aiff"}]}],
    "Stop":         [{"hooks": [{"type": "command", "command": "afplay /System/Library/Sounds/Tink.aiff"}]}]
  }
}'
seed_or_move "settings.json" "$SETTINGS_JSON_STUB"

SETTINGS_LOCAL_STUB='{
  "permissions": {}
}'
seed_or_move "settings.local.json" "$SETTINGS_LOCAL_STUB"
echo ""

# ---- 3. shared subdirs from the repo (rules, hooks, skills, agents) --------
echo "----- Step 3/8: shared subdirs from repo --------------------"
SHARED_DIRS=("rules" "hooks" "skills" "agents")
for dir in "${SHARED_DIRS[@]}"; do
    src="$REPO_DIR/$dir"
    dst="$CLAUDE_DIR/$dir"
    [ ! -d "$src" ] && { echo "  Skipping $dir/ (not in repo)"; continue; }
    if [ -L "$dst" ]; then
        if [ "$(readlink "$dst")" = "$src" ]; then
            echo "  $dir/ already linked"
        else
            rm "$dst"; ln -s "$src" "$dst"; echo "  $dir/ -> $src (updated)"
        fi
    elif [ -d "$dst" ]; then
        echo "  WARNING: ~/.claude/$dir/ is a real dir — remove it to use the shared version."
    else
        ln -s "$src" "$dst"; echo "  $dir/ -> $src"
    fi
done
echo ""

# ---- 3b. register shared hooks in personal settings.json -------------------
# Hook SCRIPTS arrive via the symlinked hooks/ dir above, but the hook entries
# that trigger them live in settings.json (personal, not shared). This merges
# the repo's shared hook entries in additively and idempotently so the shared
# hooks actually fire. Safe to re-run: it never removes your hooks/sounds/
# settings and backs up before any change. See installer/merge-shared-hooks.py.
echo "----- Step 3b/8: register shared hooks -----------------------"
if command -v python3 &>/dev/null; then
    python3 "$REPO_DIR/installer/merge-shared-hooks.py" \
        "$CLAUDE_DIR/settings.json" "$REPO_DIR/installer/shared-hooks.json" \
        || echo "  WARNING: hook merge failed; settings.json left as-is."
else
    echo "  WARNING: python3 not found — skipping hook merge."
    echo "           Shared hooks will not fire until added to ~/.claude/settings.json."
fi
echo ""

# ---- 4. Homebrew ------------------------------------------------------------
echo "----- Step 4/8: Homebrew -------------------------------------"
if command -v brew &>/dev/null; then
    echo "  Homebrew already installed: $(brew --prefix)"
else
    echo "  Homebrew not found. Installing..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    if [ -x /opt/homebrew/bin/brew ]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    elif [ -x /usr/local/bin/brew ]; then
        eval "$(/usr/local/bin/brew shellenv)"
    fi
fi
echo ""

# ---- 5. iTerm2 + Rectangle --------------------------------------------------
echo "----- Step 5/8: iTerm2 and Rectangle -------------------------"
if [ ! -d "/Applications/iTerm.app" ]; then
    echo "  Installing iTerm2..."
    brew install --cask iterm2
else
    echo "  iTerm2 already installed."
fi
if [ ! -d "/Applications/Rectangle.app" ]; then
    echo "  Installing Rectangle..."
    brew install --cask rectangle
else
    echo "  Rectangle already installed."
fi
echo ""

# ---- 6. iTerm2 Dynamic Profile + tab-switching shortcuts -------------------
echo "----- Step 6/8: iTerm2 profile + shortcuts -------------------"
ITERM_DYNPROFILES="$HOME/Library/Application Support/iTerm2/DynamicProfiles"
ITERM_PROFILE_SRC="$REPO_DIR/installer/iterm2_claude_profile.json"
ITERM_PROFILE_DST="$ITERM_DYNPROFILES/claude.json"
if [ -f "$ITERM_PROFILE_SRC" ]; then
    mkdir -p "$ITERM_DYNPROFILES"
    if [ -L "$ITERM_PROFILE_DST" ] && [ "$(readlink "$ITERM_PROFILE_DST")" = "$ITERM_PROFILE_SRC" ]; then
        echo "  iTerm2 'Claude' profile already linked."
    else
        rm -f "$ITERM_PROFILE_DST"
        ln -s "$ITERM_PROFILE_SRC" "$ITERM_PROFILE_DST"
        echo "  Installed iTerm2 'Claude' Dynamic Profile."
    fi
fi

iterm_keymap=$(defaults read com.googlecode.iterm2 GlobalKeyMap 2>/dev/null || true)
if [ -z "$iterm_keymap" ] || ! echo "$iterm_keymap" | grep -q "0xf702-0x180000"; then
    echo "  Setting iTerm2 tab-switching shortcuts (Option+Cmd+Arrow)."
    python3 - <<'PY'
import plistlib, subprocess, tempfile, os
result = subprocess.run(['defaults', 'export', 'com.googlecode.iterm2', '-'], capture_output=True)
prefs = plistlib.loads(result.stdout) if result.stdout else {}
gkm = prefs.get('GlobalKeyMap', {})
gkm['0xf702-0x180000'] = {'Action': 2, 'Text': ''}
gkm['0xf703-0x180000'] = {'Action': 0, 'Text': ''}
prefs['GlobalKeyMap'] = gkm
with tempfile.NamedTemporaryFile(suffix='.plist', delete=False) as f:
    plistlib.dump(prefs, f); tmp = f.name
subprocess.run(['defaults', 'import', 'com.googlecode.iterm2', tmp])
os.unlink(tmp)
PY
else
    echo "  iTerm2 tab-switching shortcuts already set."
fi
echo ""

# ---- 7. Rectangle config ----------------------------------------------------
echo "----- Step 7/8: Rectangle shortcuts --------------------------"
RECT_PLIST="$REPO_DIR/installer/rectangle_config.plist"
if [ -f "$RECT_PLIST" ] && [ -d "/Applications/Rectangle.app" ]; then
    echo "  Importing Rectangle shortcuts."
    defaults import com.knollsoft.Rectangle "$RECT_PLIST"
fi
echo ""

# ---- 8. open-projects launcher ---------------------------------------------
echo "----- Step 8/8: open-projects launcher -----------------------"
LAUNCHER_SRC="$REPO_DIR/installer/open-projects.sh"
LAUNCHER_SYNC="$SYNC_FOLDER/open-projects.sh"
LAUNCHER_HOME="$CLAUDE_DIR/open-projects.sh"
COLOR_EXAMPLE="$REPO_DIR/installer/open-projects.config.sh.example"
COLOR_SYNC="$SYNC_FOLDER/open-projects.config.sh"

if [ ! -f "$LAUNCHER_SYNC" ] || ! cmp -s "$LAUNCHER_SRC" "$LAUNCHER_SYNC"; then
    cp "$LAUNCHER_SRC" "$LAUNCHER_SYNC"
    chmod +x "$LAUNCHER_SYNC"
    echo "  Installed launcher -> $LAUNCHER_SYNC"
else
    echo "  Launcher already up to date."
fi

if [ ! -f "$COLOR_SYNC" ] && [ -f "$COLOR_EXAMPLE" ]; then
    cp "$COLOR_EXAMPLE" "$COLOR_SYNC"
    echo "  Seeded tab-color config -> $COLOR_SYNC (edit to add your projects)"
fi

if [ -L "$LAUNCHER_HOME" ] && [ "$(readlink "$LAUNCHER_HOME")" = "$LAUNCHER_SYNC" ]; then
    :
else
    rm -f "$LAUNCHER_HOME"
    ln -s "$LAUNCHER_SYNC" "$LAUNCHER_HOME"
fi

if ! grep -q '^alias open-projects=' "$HOME/.zshrc" 2>/dev/null; then
    echo "alias open-projects=\"$LAUNCHER_HOME\"" >> "$HOME/.zshrc"
    echo "  Added 'open-projects' alias to ~/.zshrc (run: source ~/.zshrc)"
else
    echo "  'open-projects' alias already in ~/.zshrc"
fi
echo ""

# ---- done -------------------------------------------------------------------
echo "==============================================================="
echo "  Bootstrap complete."
echo "==============================================================="
echo ""
echo "Sync folder:  $SYNC_FOLDER"
echo "Repo:         $REPO_DIR"
echo ""
echo "Next steps:"
echo "  1. source ~/.zshrc                                  (pick up the alias)"
echo "  2. Open $SYNC_FOLDER/CLAUDE.md and add your projects"
echo "     under '## Active Projects'."
echo "  3. Edit $SYNC_FOLDER/open-projects.config.sh to set"
echo "     per-project tab colors (optional)."
echo "  4. Run: open-projects"
echo ""
echo "Re-run this script any time after \`git pull\` to refresh symlinks"
echo "and re-import iTerm/Rectangle settings."
