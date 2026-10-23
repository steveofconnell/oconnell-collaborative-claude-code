# Outbound Messages to People

Applies to: every message sent to a person on the user's behalf from any tool: text
(Messages, SMS, iMessage), chat (Slack, Teams), a course-site inbox, or a comment addressed
to someone. Always-on.

## Email

Claude does not send email under any approval. The hook refuses email-sending tools. For a
message the user sends himself or herself, open a web-mail compose link with the approved
text, or put the body on the clipboard and name the recipient and thread.

## Requirements

1. **No send without an approved draft.** A message goes out only after its full text has
   been shown in the structured popup (AskUserQuestion) with the draft in the option
   preview, and the user has chosen the option labeled **Send**. "Reply to them" and "let
   him know" authorize a draft, never a send. One popup per message; one message per popup.
   The other option is **Revise**, and the revised draft goes back through the popup.
2. **Drafted in the user's voice**, following `writing-voice-core.md`.
3. **The send command carries the approved text verbatim and inline**, for example
   `send "..." to participant "+1..."` in an `osascript` block. A variable or a file cannot
   be checked and is refused.

## Enforcement

`hooks/guard-outbound-messages.py` (PreToolUse on Bash and on `mcp__*` tools) reads the
session transcript and allows a send only when the message text equals, after whitespace
normalisation, the preview of an option labeled Send that the user chose; the recipient's
number appears in that popup's question; and the popup has not already approved an earlier
send. It covers `osascript` sends through the Messages app and MCP tools whose names contain
send, post, reply or publish. A refusal means: show the text in the popup and send only after
the answer. It is not a prompt to retry another way.

An unsent compose window (a `sms:` link or a web-mail compose link) is not a send and is not
checked.

## Limits

A number that is not on iMessage cannot be reached from a Mac without an SMS relay to a
phone. Put the text on the clipboard and name the recipient.
