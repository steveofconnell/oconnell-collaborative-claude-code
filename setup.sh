#!/bin/bash
# setup.sh — Link collaborative Claude Code config into a project directory.
#
# Usage: cd <project-dir> && ~/claude-research-config/setup.sh
#
# Creates .claude/ in the current directory with symlinks to the repo's
# rules, hooks, and skills. Also copies a template settings.json (hooks
# config) that you can customize per project.
#
# Safe to re-run — only creates links that don't already exist.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(pwd)"

echo "Setting up Claude Code config in: $PROJECT_DIR"
echo "Linking to: $SCRIPT_DIR"
echo ""

# Create .claude/ if needed
mkdir -p "$PROJECT_DIR/.claude"

# Symlink rules, hooks, skills
for dir in rules hooks skills agents; do
    if [ -d "$SCRIPT_DIR/$dir" ]; then
        if [ -e "$PROJECT_DIR/.claude/$dir" ]; then
            echo "  .claude/$dir already exists — skipping"
        else
            ln -s "$SCRIPT_DIR/$dir" "$PROJECT_DIR/.claude/$dir"
            echo "  .claude/$dir → $SCRIPT_DIR/$dir"
        fi
    fi
done

# Copy settings.json template (don't overwrite existing)
if [ -e "$PROJECT_DIR/.claude/settings.json" ]; then
    echo "  .claude/settings.json already exists — skipping"
else
    cp "$SCRIPT_DIR/settings.project.json" "$PROJECT_DIR/.claude/settings.json"
    echo "  .claude/settings.json copied (template — edit for project-specific hooks)"
fi

# Create .workspace/ if needed
mkdir -p "$PROJECT_DIR/.workspace/memory"
mkdir -p "$PROJECT_DIR/.workspace/plans"

echo ""
echo "Done. Open Claude Code in this directory and type /start to begin."
