#!/usr/bin/env bash
# personal-content-scan.sh — block personal content from being published to this
# shared repo. Run manually (`bash tools/personal-content-scan.sh`) or automatically
# via the pre-push hook (tools/pre-push; activated with `git config core.hooksPath tools`).
#
# The repo is meant to be a GENERIC, shareable config. Personal identity, institution,
# family, project names, and author-specific voice/preferences belong in your private
# sync folder, never here. This scanner is the gate that keeps them out.
#
# IMPORTANT: the patterns that identify YOUR personal content are NOT stored in this
# file — putting them here would publish the very identifiers you are trying to keep
# out. Put them in tools/personal-content-patterns.txt (one extended-regex per line);
# that file is gitignored and stays on your machine. Without it the scanner only checks
# a couple of generic examples and warns that it is unconfigured.
#
# Allowlist genuinely-needed references (the repo URL, acknowledgments) in
# tools/personal-content-allow.txt, or put the marker `personal-allow` on the line.
#
# Exit 0 = clean; exit 1 = personal content found (pre-push aborts the push).
set -uo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
ALLOW="$ROOT/tools/personal-content-allow.txt"
PATTERNS_FILE="$ROOT/tools/personal-content-patterns.txt"

# Case-insensitive regexes that should not appear in published files.
# Loaded from the private (gitignored) patterns file; falls back to generic examples.
PATTERNS=()
if [ -f "$PATTERNS_FILE" ]; then
  while IFS= read -r p; do
    [ -z "$p" ] && continue
    case "$p" in \#*) continue ;; esac
    PATTERNS+=("$p")
  done < "$PATTERNS_FILE"
fi
if [ "${#PATTERNS[@]}" -eq 0 ]; then
  echo "personal-content-scan: NOTE — no tools/personal-content-patterns.txt found (or empty)."
  echo "  The guard is unconfigured. Create that file with one extended-regex per line —"
  echo "  your name, institution, handles, family, and project names — to activate it."
  echo "  See PERSONAL_CONFIG.md. Proceeding with generic example patterns only."
  PATTERNS=(
    "\\byour-?name\\b"
    "\\byour-?institution\\b"
  )
fi

# Files that legitimately reference the maintainer (docs about the repo itself).
# One path per line in the allow file; lines may also carry `personal-allow`.
default_allow_paths='README.md|PERSONAL_CONFIG.md|tools/personal-content-scan.sh|tools/personal-content-allow.txt'

extra_allow=""
[ -f "$ALLOW" ] && extra_allow="$(grep -vE '^\s*#' "$ALLOW" 2>/dev/null | grep -vE '^\s*$' | paste -sd'|' -)"
allow_paths="$default_allow_paths"
[ -n "$extra_allow" ] && allow_paths="$allow_paths|$extra_allow"

hits=0
while IFS= read -r f; do
  [ -f "$f" ] || continue
  case "$f" in
    *.png|*.jpg|*.jpeg|*.pdf|*.plist) continue ;;
  esac
  # skip allowlisted paths
  printf '%s\n' "$f" | grep -qE "^($allow_paths)$" && continue
  for p in "${PATTERNS[@]}"; do
    while IFS= read -r line; do
      [ -z "$line" ] && continue
      # per-line escape hatch
      printf '%s' "$line" | grep -qi 'personal-allow' && continue
      if [ $hits -eq 0 ]; then
        echo ""
        echo "X personal-content-scan: blocked — personal content found in tracked files:"
        echo ""
      fi
      echo "  $f: $line"
      hits=$((hits+1))
    done < <(grep -inE "$p" "$f" 2>/dev/null)
  done
done < <(git ls-files)

if [ "$hits" -gt 0 ]; then
  echo ""
  echo "  This repo is meant to be generic. Move personal content to your private"
  echo "  sync folder, or allowlist a genuine reference (tools/personal-content-allow.txt"
  echo "  or a 'personal-allow' marker on the line). Bypass (not recommended): git push --no-verify"
  echo ""
  exit 1
fi

echo "personal-content-scan: clean."
exit 0
