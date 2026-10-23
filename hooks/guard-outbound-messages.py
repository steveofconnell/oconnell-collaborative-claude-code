#!/usr/bin/env python3
"""PreToolUse hook (Bash and mcp__*): no message goes to a person unless its exact text
was shown in a popup (AskUserQuestion) and the user answered Send.

Covers:
  - Bash commands that send through the Messages app (osascript, tell application "Messages").
  - MCP tools that send or post a message (name contains send, post, reply, publish).
    Email-sending tools are refused outright (see rules/outbound-messages.md).

A send is allowed only when
  1. every message body in the command is, character for character after whitespace
     normalisation, the preview of an option labelled "Send" that the user chose;
  2. the recipient's phone number in the command appears in that popup's question;
  3. the approval has not already been used: each popup approves one send.

The body must sit inline in the command as a quoted literal after `send`; a variable
or a file cannot be checked and is refused. An unsent compose window (open "sms:...")
is not a send and is not checked.

Refusal is exit code 2 with the reason on stderr. A refusal means: show the text in the
popup, and send only after the answer. Do not retry another way.

See rules/outbound-messages.md.
"""
import json
import re
import sys

EMAIL_TOOL = re.compile(r"(send_email|send_message_email|gmail.*send|outlook.*send|mail.*send)", re.I)
SEND_TOOL = re.compile(r"(send|post|reply|publish)", re.I)
READ_ONLY = re.compile(r"(search|read|get|list|draft|download|label|filter|modify|delete)", re.I)
BODY_KEYS = {"body", "text", "message", "content", "comment", "note"}


def norm(s):
    return re.sub(r"\s+", " ", s.replace("\\\"", '"').replace("\\'", "'")).strip()


def digits(s):
    return re.sub(r"\D", "", s)


def deny(reason):
    sys.stderr.write("BLOCKED by guard-outbound-messages: " + reason +
                     " Show the exact text in a popup (AskUserQuestion, Send/Revise) and send "
                     "only after the answer Send. Do not retry another way.\n")
    sys.exit(2)


def load_transcript(path):
    entries = []
    try:
        with open(path) as f:
            for line in f:
                try:
                    entries.append(json.loads(line))
                except ValueError:
                    pass
    except OSError:
        pass
    return entries


def blocks(entry):
    c = (entry.get("message") or {}).get("content")
    return c if isinstance(c, list) else []


def approvals(entries):
    """Return (approved, prior_commands). approved: list of (question, preview) the user sent."""
    asked = {}
    approved = []
    prior = []
    for e in entries:
        for b in blocks(e):
            if b.get("type") == "tool_use" and b.get("name") == "AskUserQuestion":
                asked[b["id"]] = (b.get("input") or {}).get("questions", [])
            elif b.get("type") == "tool_use":
                inp = b.get("input") or {}
                prior.append(norm(json.dumps(inp)))
            elif b.get("type") == "tool_result" and b.get("tool_use_id") in asked:
                content = b.get("content")
                if isinstance(content, list):
                    content = " ".join(x.get("text", "") for x in content if isinstance(x, dict))
                content = content or ""
                for q in asked[b["tool_use_id"]]:
                    if re.search(re.escape('"' + q.get("question", "") + '"=') + r'"Send"', content):
                        for o in q.get("options", []):
                            if o.get("label", "").startswith("Send") and o.get("preview"):
                                approved.append((q["question"], norm(o["preview"])))
    return approved, prior


def messages_bodies(cmd):
    """Literal strings following `send` in an AppleScript block, and the recipients.
    Backslash-escaped quotes (from osascript -e '...') are treated as plain quotes; a body
    that itself contains double quotes cannot be parsed and is refused."""
    c = cmd.replace('\\"', '"')
    bodies = re.findall(r'\bsend\s+"([^"]*)"\s+to\b', c)
    bare = re.findall(r'\bsend\s+(?!")(\S+)', c)
    numbers = re.findall(r'participant\s+"([^"]+)"', c) + re.findall(r'buddy\s+"([^"]+)"', c)
    return bodies, bare, numbers


def check(bodies, recipients, transcript):
    approved, prior = approvals(load_transcript(transcript))
    used_pool = list(approved)
    for body in bodies:
        nb = norm(body)
        match = None
        for a in used_pool:
            q, prev = a
            if prev == nb:
                if all(digits(r)[-10:] in digits(q) for r in recipients if digits(r)):
                    match = a
                    break
        if not match:
            deny("this text, to this recipient, was not shown in a popup that you answered Send.")
        sent_before = sum(1 for p in prior if nb in p)
        total_approvals = sum(1 for a in approved if a[1] == match[1] and a[0] == match[0])
        if sent_before >= total_approvals:
            deny("the approval for this text has already been used; each popup approves one send.")


def main():
    data = json.load(sys.stdin)
    tool = data.get("tool_name", "")
    inp = data.get("tool_input") or {}
    transcript = data.get("transcript_path", "")

    if tool == "Bash":
        cmd = inp.get("command", "")
        if not re.search(r'application\s+\\?"Messages\\?"', cmd):
            return 0
        bodies, bare, numbers = messages_bodies(cmd)
        if bare:
            deny("the message body is not an inline quoted literal after `send`, so it cannot be checked.")
        if not bodies:
            return 0
        if not numbers:
            deny("no recipient (participant \"...\") found in the command.")
        check(bodies, numbers, transcript)
        return 0

    if tool.startswith("mcp__"):
        if READ_ONLY.search(tool.split("__")[-1]) and not re.search(r"send", tool.split("__")[-1], re.I):
            return 0
        name = tool.split("__")[-1]
        if EMAIL_TOOL.search(tool) or re.fullmatch(r"send_email|send_mail", name, re.I):
            deny("Claude never sends email; open an Outlook web compose link or use the clipboard.")
        if not SEND_TOOL.search(name):
            return 0
        bodies = []

        def walk(o, key=""):
            if isinstance(o, dict):
                for k, v in o.items():
                    walk(v, k.lower())
            elif isinstance(o, list):
                for v in o:
                    walk(v, key)
            elif isinstance(o, str) and key in BODY_KEYS and o.strip():
                bodies.append(o)

        walk(inp)
        if not bodies:
            deny("a send/post tool call with no message text field to check.")
        check(bodies, [], transcript)
    return 0


if __name__ == "__main__":
    sys.exit(main())
