#!/usr/bin/env bash
# update.sh — bring an existing clone up to date with the shared config, INCLUDING
# the case where the published history has been rewritten (which a plain `git pull`
# cannot handle: it errors with "unrelated histories" or makes a tangled merge).
#
# Plug-and-play. From your clone of this repo:
#   git fetch origin && git checkout origin/main -- tools/update.sh && bash tools/update.sh
#
# It only touches THIS clone — never your sync folder or personal config. Steps:
#   1. Fetch origin.
#   2. Stash any local changes to tracked files (reported at the end).
#   3. Hard-reset local main to origin/main — adopting the current clean history even
#      if your branch diverged because history was rewritten.
#   4. Prune unreachable objects (reflog expire + gc --prune=now) so personal content
#      that shipped in earlier commits is cleared from this clone's .git as well.
#   5. Re-run setup.sh to re-register shared hooks and activate the publish guard.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"

if [ ! -d .git ]; then
    echo "ERROR: $REPO_DIR is not a git repository." >&2
    exit 1
fi

BRANCH="main"

echo "Updating shared config in: $REPO_DIR"

echo "1/5 Fetching origin..."
git fetch --prune origin

STASHED=""
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "2/5 Stashing local changes to tracked files..."
    git stash push -m "pre-update-$(date +%Y%m%d-%H%M%S)" >/dev/null && STASHED=1
else
    echo "2/5 No local changes to stash."
fi

echo "3/5 Resetting local '$BRANCH' to origin/$BRANCH (adopts current history)..."
git checkout -B "$BRANCH" "origin/$BRANCH"

echo "4/5 Pruning old/unreachable objects from this clone..."
git reflog expire --expire=now --all || true
git gc --prune=now --quiet || true

echo "5/5 Re-running setup.sh (re-registers hooks, activates publish guard)..."
SYNC=""
if [ -L "$HOME/.claude/CLAUDE.md" ]; then
    target="$(readlink "$HOME/.claude/CLAUDE.md")"
    SYNC="$(cd "$(dirname "$target")" 2>/dev/null && pwd || true)"
fi
if [ -n "$SYNC" ] && [ -d "$SYNC" ]; then
    bash "$REPO_DIR/setup.sh" --sync-folder "$SYNC"
else
    bash "$REPO_DIR/setup.sh"
fi

echo ""
echo "Update complete. This clone now matches the current shared config; old history"
echo "and any personal content from earlier versions have been cleared locally."
if [ -n "$STASHED" ]; then
    echo ""
    echo "NOTE: your local changes were stashed. Inspect with:"
    echo "  git stash list   /   git stash show -p   /   git stash pop"
fi
