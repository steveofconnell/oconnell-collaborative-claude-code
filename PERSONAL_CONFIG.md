# Personal Configuration (Not in This Repo)

The files in this repository are the **collaborative** parts of a Claude Code setup for academic research. They work on their own. But the author also uses several personal configuration files that are excluded from git because they contain identity, credentials, or machine-specific settings.

You are encouraged to create your own versions of these. They make the experience substantially better.

## Personal Files You Should Create

### `~/.claude/CLAUDE.md` (Global Config)

Your identity and preferences. Claude Code loads this automatically for every project. Mine includes:

- **Who I am** — name, institution, field, role. This lets Claude tailor responses to my expertise level and domain.
- **Accuracy and sourcing standards** — rules about never guessing, always citing, flagging uncertainty. Especially important for academic work.
- **Writing style** — detailed analysis of my published writing voice (sentence structure, vocabulary, rhetorical patterns, anti-patterns to avoid). Built from reading my own papers. You should do the same: feed Claude several of your published papers and ask it to extract your voice profile.
- **Learned preferences** — accumulated over many sessions. Things like "never add trailing summaries," "minimize prompts," "keep the work moving forward." These build up naturally as you correct Claude's behavior.
- **Active projects** — list of current project directories.
- **Memory storage override** — I redirect memory files to the project directory (not `~/.claude/projects/...`) so they sync across devices via Dropbox.

### `~/.claude/settings.json` (Hooks and UI)

Mine includes sound notification hooks — a chime when Claude needs input, a different sound when it finishes. Small thing, big quality-of-life improvement when you're working in another window.

```json
{
  "hooks": {
    "Notification": [{"hooks": [{"type": "command", "command": "afplay /System/Library/Sounds/Sosumi.aiff"}]}],
    "Stop": [{"hooks": [{"type": "command", "command": "afplay /System/Library/Sounds/Tink.aiff"}]}]
  }
}
```

Also includes a status line showing model, cost, and context usage. See the repo's hook scripts for the research-relevant hooks (rawdata protection, context monitoring) — those are tracked in git.

### `~/.claude/settings.local.json` (Permissions)

Controls which tools Claude can use without asking. This is personal risk tolerance — start restrictive and open up as you build trust. The default (prompting for everything) is fine for getting started.

### `open-projects.sh` (Multi-Project Launcher)

A script that opens Claude Code in multiple project directories simultaneously, each in its own terminal tab. Useful if you work across several projects daily. Not necessary for single-project collaboration.

### Gmail / Calendar MCP Servers

I connect Gmail and Google Calendar via MCP servers so Claude can triage my inbox and check my schedule at session startup. This requires OAuth credentials and is entirely optional. The collaborative skills (`/start`, `/close`) work fine without it — they just skip the email and calendar steps.

### Institutional Templates (`templates/`)

The author maintains templates for recurring institutional submissions (IRB applications, grant forms, etc.) specific to his university. These are excluded from the repo because they are institution-specific, but the `templates/` directory is a useful pattern. Build your own for any multi-field form you submit more than once — IRB protocols, grant budget justifications, data management plans. Having a template means Claude can fill it in from project details rather than starting from scratch.

### Writing Voice Profile

The `academic-writing-voice.md` rule in this repo contains a generic style guide for applied economics writing. The author also has a detailed personal voice profile built from analyzing his own published papers. If you want Claude to write in your voice rather than generic academic prose:

1. Collect 5-10 of your published papers (PDFs or tex files)
2. Ask Claude to analyze your sentence structure, paragraph structure, vocabulary, rhetorical moves, and anti-patterns
3. Save the analysis as a rule file in your `~/.claude/rules/`

This is one of the highest-value personal customizations you can make.

## Cross-Device Sync

I keep all personal config in a Dropbox folder and symlink `~/.claude/` to it, so every machine reads the same files. If you work on multiple devices, consider a similar setup with Dropbox, iCloud Drive, or any file sync service. The key symlinks:

```
~/.claude/CLAUDE.md         → <your-sync-folder>/CLAUDE.md
~/.claude/settings.json     → <your-sync-folder>/settings.json
~/.claude/settings.local.json → <your-sync-folder>/settings.local.json
~/.claude/rules/            → <your-sync-folder>/rules/
~/.claude/skills/           → <your-sync-folder>/skills/
~/.claude/hooks/            → <your-sync-folder>/hooks/
```

## Setup for Collaborating on a Shared Project

If you're here because a coauthor pointed you to this repo:

1. Install [Claude Code](https://claude.ai/code) if you haven't already
2. Clone this repo: `git clone https://github.com/steveofconnell/oconnell-collaborative-claude-code.git ~/claude-research-config`
3. In the shared project directory, run: `~/claude-research-config/setup.sh`
4. Open Claude Code in the project: `cd <project> && claude`
5. Type `/start` to begin a session, `/close` to end one

The setup script creates symlinks from the project's `.claude/` directory to this repo. You get all the research rules, hooks, and skills automatically. Updates propagate when you `git pull`.
