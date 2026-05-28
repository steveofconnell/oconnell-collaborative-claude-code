# Personal Configuration

After running `setup.sh`, your sync folder (default `~/Dropbox/.claudeconfig/`) contains stub versions of every personal config file. They work as-is, but most are barebones — you'll get more out of the setup by customizing them. This document describes what each one is for and what to change.

It also describes a few personal files that `setup.sh` does **not** create because they contain credentials, institution-specific content, or are entirely optional.

## Files Created by `setup.sh` (Customize These)

### `<sync-folder>/CLAUDE.md`

Your global config. Loaded for every Claude Code session, on every device that shares the sync folder. The seeded version contains only an empty `## Active Projects` section. Add to it:

- **Identity** — who you are, your role, your field. Lets Claude tailor responses to your domain expertise.
- **Accuracy and sourcing standards** — rules about citations, quoting, flagging uncertainty.
- **Writing style** — voice profile, anti-patterns to avoid (see "Writing Voice Profile" below).
- **Learned preferences** — things you correct Claude on repeatedly. These accumulate over months of use.
- **Active projects** — paths to your project directories. The `open-projects` launcher reads this section.
- **Memory storage override** — if you want memory files to live in the project directory (so they sync with the project), say so here.

### `<sync-folder>/settings.json`

Hooks and UI. The seeded version has sound notification hooks (Sosumi when Claude needs input, Tink when it finishes). Useful additions:

- A status line script (model name, cost, context usage)
- Pre/post-tool hooks (the seeded set is in this repo's `hooks/` and is auto-loaded; this file is for your *personal* hooks)

### `<sync-folder>/settings.local.json`

Auto-trusted tools. Default is empty (Claude prompts for every tool use). Open up gradually as you build trust. Personal risk tolerance.

### `<sync-folder>/open-projects.config.sh`

Per-project iTerm tab colors. The seeded example has placeholder project names — replace them with your own. Each entry returns `bg_r,bg_g,bg_b;fg_r,fg_g,fg_b` (RGB 0-255). With distinct dark backgrounds per project, you can identify the right tab in a glance even with five or six projects open.

### `<sync-folder>/open-projects.sh`

Installed verbatim from the repo's `installer/` directory. You generally don't customize this file directly — re-running `setup.sh` overwrites it on `git pull`. If you do want to customize it, fork the repo or just edit the copy in your sync folder and accept that it'll be overwritten.

## Files `setup.sh` Does *Not* Create

### Gmail / Calendar MCP Servers

The `/start` and `/email-triage` skills can integrate with Gmail and Google Calendar via MCP servers. Setting up MCP servers requires OAuth credentials specific to your Google account, so this isn't automated. The skills work fine without them — they skip the email and calendar steps gracefully.

If you want to enable the integration:
1. Follow [Anthropic's MCP setup docs](https://modelcontextprotocol.io/) to install Gmail and Google Calendar MCP servers
2. The skills will auto-detect them on next session

### Calendar Check Rule

The maintainer's `rules/calendar-check.md` is excluded from the repo (it lists personal and family Google Calendar IDs). If you use Google Calendar MCP, create your own `<sync-folder>/rules/calendar-check.md` listing your calendar addresses. The format:

```markdown
# Calendar Checks

When checking the user's calendar, query ALL of:

1. **Primary:** your.email@gmail.com
2. **Work:** your.work@institution.edu
3. **Family:** spouse.email@gmail.com
```

### Institutional Templates

`templates/` is excluded from the repo because the maintainer's templates are institution-specific (IRB applications, grant forms). Build your own for any multi-field form you submit more than once. Having a template means Claude can fill it in from project details rather than starting from scratch.

Add a `<sync-folder>/rules/templates.md` describing where your templates live and when to use them, so Claude knows about them.

### Slide Deck Examples

`skills/slides/examples/` is excluded — the maintainer's deck examples are personal academic presentations. The `/slides` skill works without them but produces better output with calibration examples. To set up your own:
1. Collect 3-5 of your best slide decks (tex + pdf)
2. Place them in `<sync-folder>/skills-overrides/slides/examples/` (or fork the repo and add them there)

### Writing Voice Profile

The shared `rules/academic-writing-voice.md` is a generic style guide for applied economics. The maintainer also has a detailed personal voice profile built from analyzing his own published papers. To build your own:

1. Collect 5–10 of your published papers (PDFs or tex files)
2. In a Claude Code session, ask: "Analyze the writing in these papers — sentence structure, paragraph structure, vocabulary, rhetorical moves, anti-patterns — and produce a style rule for me to save."
3. Save the result as `<sync-folder>/rules/your-writing-voice.md`

This is one of the highest-value personal customizations.

## Personalizing the Shipped Skills

Several skills ship generic, with placeholders where the maintainer's own details used to be.
Each runs out of the box but produces sharper, tailored output once you supply your particulars.
The pattern is always the same: **the repo ships the mechanism; your particulars live in your
personal config (sync folder), never in the repo** — where the publish guard (`tools/`) would
block them anyway. Each item below is a short session you run once.

### `/expense-folio` — your reimbursement profile
Ships with placeholder cards, institution, and policies. To make it yours, write a short profile
into your personal config containing: the reimbursement header block (name, department, employer),
your card list (corp vs. personal, by last-4), your expense-archive folder path, and your
institution's rules (per-diem day threshold, receipt minimum, required backups). Tell `/expense-folio`
to use it, or paste it at the start of a folio session. Keep this in the sync folder — cards and
employer details are personal.

### `/verify-bib` — your library proxy
Paywalled citation PDFs are fetched through your institution's library proxy. Set your proxy prefix
(commonly `https://proxy.library.<institution>.edu/login?url=`) in your personal config; if none is
set, the skill simply skips the proxy fallback.

### `/referee-paper` — your reviewing voice
Ships with a default report structure and standards. To match your own: collect 5–10 of your past
referee reports and ask Claude — *"Extract my referee-report structure, comment style, and standards
from these, and produce a rule I can save"* — then keep the result in your personal config and set
your name in the signature block.

### `/setup-project` — your author default
New-project scaffolding asks for author name(s). Add your name to the identity section of your
`<sync-folder>/CLAUDE.md` and the skill will default to it instead of prompting.

### Already covered above
- **Writing-voice profile** (used by `/review-writing` and the writing-reviewer agent) — see
  "Writing Voice Profile."
- **`/slides` calibration decks** — see "Slide Deck Examples."
- **Calendar, institutional templates** — see "Calendar Check Rule" and "Institutional Templates."

## Cross-Device Sync — How It Works

The pattern `setup.sh` puts in place is:

```
~/.claude/CLAUDE.md            -> <sync-folder>/CLAUDE.md
~/.claude/settings.json        -> <sync-folder>/settings.json
~/.claude/settings.local.json  -> <sync-folder>/settings.local.json
~/.claude/open-projects.sh     -> <sync-folder>/open-projects.sh
~/.claude/rules/               -> <repo>/rules/
~/.claude/skills/              -> <repo>/skills/
~/.claude/hooks/               -> <repo>/hooks/
~/.claude/agents/              -> <repo>/agents/
```

Edit any sync-folder file on one machine; it's immediately available on every other machine the moment Dropbox finishes syncing. Edit a repo file and `git push`; collaborators pick up the change with `git pull && bash setup.sh`.

`~/.claude/projects/`, `sessions/`, `history.jsonl`, and `todos/` stay local on each machine. They contain volatile per-session state and would corrupt if synced concurrently from two machines.
