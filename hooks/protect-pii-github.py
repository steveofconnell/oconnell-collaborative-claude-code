#!/usr/bin/env python3
"""
Hook: PreToolUse (Bash)

Blocks `git push` to GitHub (or any non-exempt remote) when the outgoing commits
contain PII or secrets. Pushes to EXEMPT remotes — Overleaf by default — are
allowed through untouched, because manuscripts legitimately carry subject data
and Overleaf is an accepted destination.

Policy in one line: PII may reach Overleaf via its git integration; PII must not
reach GitHub.

This is the Claude-Code-side analogue of protect-rawdata.sh: it fires whenever
Claude runs a Bash command. It does NOT fire when you push manually in a
terminal (a git pre-push hook would be needed for that — separate layer).

Config files (optional, in the same dir as this hook, i.e. ~/.claude/hooks/):
  pii-allow-remotes.txt  — regexes of remote URLs that are exempt (one per line).
                           Defaults to 'overleaf\\.com' if absent.
  pii-allowlist.txt      — regexes; any added line matching one is ignored.

Per-line escape hatch: put the marker  pii-allow  on the offending line.

Exit codes: 0 = allow; 2 = block (reason on stderr, fed back to Claude).
"""

import json
import os
import re
import shlex
import subprocess
import sys

HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_EXEMPT = [r"overleaf\.com"]

# --- PII detection (kept in sync with pii-guard/pii_scan.py) ----------------
PLACEHOLDER_WORDS = (
    "doe", "jane", "john", "example", "sample", "test", "tester", "foo", "bar",
    "baz", "placeholder", "lastname", "firstname", "yourname", "username",
    "user", "name", "recording", "interview", "audio", "filename", "yourfile",
    "subject", "respondent", "anon", "anonymous", "redacted", "dummy",
)
PLACEHOLDER_RE = re.compile("|".join(PLACEHOLDER_WORDS), re.IGNORECASE)
MEDIA_EXT = r"(?:m4a|mp3|wav|aac|flac|aiff|ogg|m4v|mov|mp4|avi|wma)"
EMAIL_PLACEHOLDER_DOMAINS = {
    "example.com", "example.org", "example.net", "email.com", "domain.com",
    "test.com", "sample.com",
}
EMAIL_PLACEHOLDER_LOCAL_PREFIXES = (
    "your", "spouse", "user", "name", "you", "example", "test", "sample",
    "noreply", "no-reply", "someone", "first.last", "firstname",
)
HOME_PATH_PLACEHOLDERS = {"yourname", "username", "user", "you", "name", "<user>"}


def _placeholderish(text):
    return bool(PLACEHOLDER_RE.search(text))


def _judge_always(_m):
    return True


def _judge_email(m):
    local, _, domain = m.group(0).partition("@")
    if domain.lower() in EMAIL_PLACEHOLDER_DOMAINS:
        return False
    return not local.lower().startswith(EMAIL_PLACEHOLDER_LOCAL_PREFIXES)


def _judge_media(m):
    return not _placeholderish(m.group(0))


def _judge_home_path(m):
    return m.group(1).lower() not in HOME_PATH_PLACEHOLDERS


RULES = [
    ("media-recording", re.compile(r"[\w./-]*\.%s\b" % MEDIA_EXT, re.I), _judge_media,
     "audio/video file reference — use a placeholder like doe_jane/DOEJANE_15Jan2026.m4a"),
    ("email", re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"), _judge_email,
     "email address"),
    ("us-phone", re.compile(r"(?<!\d)(?:\+?1[ \-.])?\(?\d{3}\)?[ \-.]\d{3}[ \-.]\d{4}(?!\d)"),
     _judge_always, "phone number"),
    ("ssn", re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)"), _judge_always, "US SSN"),
    ("gps-coords", re.compile(r"(?<![\d.])-?\d{1,3}\.\d{4,},\s*-?\d{1,3}\.\d{4,}(?![\d.])"),
     _judge_always, "GPS coordinates"),
    ("home-path", re.compile(r"/Users/([A-Za-z0-9._\-]+)"), _judge_home_path,
     "real macOS home path — use $HOME or /Users/<user>"),
    ("private-key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |PGP |DSA )?PRIVATE KEY-----"),
     _judge_always, "private key material"),
    ("aws-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b"), _judge_always, "AWS access key id"),
    ("api-token", re.compile(
        r"\b(?:sk-ant-[A-Za-z0-9_\-]{20,}|ghp_[A-Za-z0-9]{36}|AIza[0-9A-Za-z_\-]{35}|"
        r"xox[baprs]-[0-9A-Za-z\-]{10,})\b"), _judge_always, "API token / secret"),
]


def _load_patterns(fname, fallback):
    path = os.path.join(HOOK_DIR, fname)
    out = []
    if os.path.isfile(path):
        with open(path, encoding="utf-8", errors="replace") as fh:
            for raw in fh:
                line = raw.split("#", 1)[0].strip()
                if not line:
                    continue
                try:
                    out.append(re.compile(line))
                except re.error:
                    out.append(re.compile(re.escape(line)))
    return out or [re.compile(p) for p in fallback]


def _allowlisted(line, allow):
    return "pii-allow" in line or any(p.search(line) for p in allow)


def _iter_added(diff):
    path, n = None, 0
    for line in diff.splitlines():
        if line.startswith("+++ "):
            p = line[4:].strip()
            path = None if p == "/dev/null" else re.sub(r"^b/", "", p)
        elif line.startswith("@@"):
            m = re.search(r"\+(\d+)", line)
            n = int(m.group(1)) if m else 0
        elif line.startswith("+") and not line.startswith("+++"):
            yield path, n, line[1:]
            n += 1
        elif line.startswith(("-", "---")):
            continue
        elif line.startswith(" "):
            n += 1


def _scan(diff, allow):
    hits = []
    for path, lineno, text in _iter_added(diff):
        if _allowlisted(text, allow):
            continue
        for name, regex, judge, hint in RULES:
            for m in regex.finditer(text):
                if judge(m):
                    hits.append((path, lineno, name, m.group(0).strip(), hint))
    return hits


# --- git helpers ------------------------------------------------------------
def git(cwd, *args):
    try:
        r = subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True)
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None


def looks_like_url(tok):
    return "://" in tok or re.match(r"^[\w.+-]+@[\w.-]+:", tok or "")


def parse_push(cmd):
    """Return (is_push, repo_dir_override, remote_token) from a shell command."""
    try:
        toks = shlex.split(cmd)
    except ValueError:
        toks = cmd.split()
    repo_override, remote_tok = None, None
    is_push = False
    i = 0
    while i < len(toks):
        t = toks[i]
        if t == "git":
            # scan this git invocation up to a shell separator
            j = i + 1
            seen_push = False
            while j < len(toks) and toks[j] not in ("&&", "||", ";", "|"):
                if toks[j] == "-C" and j + 1 < len(toks):
                    repo_override = toks[j + 1]
                    j += 2
                    continue
                if toks[j] == "push":
                    seen_push = True
                    j += 1
                    continue
                if seen_push and not toks[j].startswith("-") and remote_tok is None:
                    remote_tok = toks[j]
                j += 1
            if seen_push:
                is_push = True
                break
        if t == "cd" and i + 1 < len(toks) and repo_override is None:
            repo_override = toks[i + 1]
        i += 1
    return is_push, repo_override, remote_tok


def empty_tree(cwd):
    return git(cwd, "hash-object", "-t", "tree", "/dev/null") or \
        "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    if data.get("tool_name") != "Bash":
        sys.exit(0)
    cmd = (data.get("tool_input") or {}).get("command", "") or ""
    if "push" not in cmd or "git" not in cmd:
        sys.exit(0)

    is_push, repo_override, remote_tok = parse_push(cmd)
    if not is_push:
        sys.exit(0)

    cwd = data.get("cwd") or os.getcwd()
    repo = cwd
    if repo_override:
        repo = repo_override if os.path.isabs(repo_override) \
            else os.path.normpath(os.path.join(cwd, repo_override))
    toplevel = git(repo, "rev-parse", "--show-toplevel")
    if not toplevel:
        sys.exit(0)  # not a git repo we can reason about — let git itself handle it
    repo = toplevel

    # --- resolve the destination remote URL ---
    remote_name, remote_url = None, None
    if remote_tok and looks_like_url(remote_tok):
        remote_url = remote_tok
        remote_name = remote_tok
    elif remote_tok:
        remote_name = remote_tok
        remote_url = git(repo, "remote", "get-url", remote_tok)
    else:
        up = git(repo, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{push}") \
            or git(repo, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
        remote_name = up.split("/", 1)[0] if up and "/" in up else "origin"
        remote_url = git(repo, "remote", "get-url", remote_name)

    exempt = _load_patterns("pii-allow-remotes.txt", DEFAULT_EXEMPT)
    if remote_url and any(p.search(remote_url) for p in exempt):
        sys.exit(0)  # Overleaf (or other exempt) — PII allowed through

    # --- non-exempt destination: compute outgoing commits and scan ---
    branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD") or "HEAD"
    base = None
    for ref in ("%s/%s" % (remote_name, branch), "%s/HEAD" % remote_name,
                "%s/main" % remote_name, "%s/master" % remote_name):
        if remote_name and git(repo, "rev-parse", "--verify", "-q", ref) is not None:
            base = ref
            break
    if base is None:
        base = empty_tree(repo)

    diff = git(repo, "diff", "--unified=0", "%s..HEAD" % base)
    if diff is None:
        diff = git(repo, "diff", "--unified=0", "HEAD") or ""

    allow = _load_patterns("pii-allowlist.txt", [])
    hits = _scan(diff, allow)
    if not hits:
        sys.exit(0)

    where = remote_url or remote_name or "a non-Overleaf remote"
    lines = [
        "BLOCKED: this push targets %s and the outgoing commits contain PII/secrets." % where,
        "Policy: PII may go to Overleaf, never to GitHub.",
        "",
        "Findings in commits about to be pushed:",
    ]
    for path, lineno, name, snippet, hint in hits[:30]:
        lines.append("  %s:%s [%s]  %s" % (path or "?", lineno, name, snippet))
        lines.append("      -> %s" % hint)
    lines += [
        "",
        "Resolve by one of:",
        "  - remove/redact the PII and amend the commit(s), or",
        "  - if it is a false positive, add  pii-allow  to that line, or add a",
        "    regex to ~/.claude/hooks/pii-allowlist.txt, or",
        "  - if this content is meant for Overleaf, push to the Overleaf remote.",
    ]
    sys.stderr.write("\n".join(lines) + "\n")
    sys.exit(2)


if __name__ == "__main__":
    main()
