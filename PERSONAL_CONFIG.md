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

### Multi-Project Launcher (`open-projects.sh`)

The author runs a single shell command (`open-projects`) that opens every active research project simultaneously, each in its own iTerm2 tab, with Claude Code already running. This is the single biggest quality-of-life improvement in the setup. Features worth replicating:

**Per-project color-coded tabs.** Each project gets a distinct background and foreground color (dark red for the admin window, dark blue for one project, dark green for another, etc.). When you have 4-5 tabs open, you can identify which project you're looking at instantly without reading the tab title. The colors are set via iTerm2 AppleScript (`set background color`, `set foreground color`) and also remap ANSI black to visible gray so dark-colored terminal output remains legible against the dark backgrounds.

**Bypass permissions mode.** Each tab launches Claude Code with `--permission-mode bypassPermissions`, which skips all tool permission prompts. This is appropriate when you trust the config and want to work fast — Claude can read, write, search, and run commands without interruption. You should only do this after you are comfortable with what Claude Code does and have protective hooks (like `protect-rawdata.sh`) in place to block the operations that truly should not happen. Start with the default permission mode and graduate to bypass once you trust the guardrails.

**Auto-start.** Each tab runs `claude '/start'`, which triggers the full session startup sequence (config discovery, latest handoff, memory load, academic integrity acknowledgment). By the time you switch to a tab, it's already briefed and waiting for instructions.

**Staggered launch.** Tabs open with a configurable delay between them (default 5 seconds) to avoid concurrent startup contention — multiple Claude instances hitting the same MCP servers or API simultaneously can cause timeouts.

**Self-bootstrapping.** The script checks for all dependencies on every run. On a fresh device, it installs iTerm2 (via Homebrew), creates all `~/.claude/` symlinks, sets up keyboard shortcuts, and adds the shell alias — before launching any projects. The second run just opens projects.

**Caffeinate tab.** The last tab runs `caffeinate -di` to prevent the machine from sleeping during long Claude sessions.

**Project list from config.** The script reads the `## Active Projects` section of your global `CLAUDE.md` to determine which directories to open. Adding or removing a project is a one-line edit.

To build your own version, the core pattern is:
1. Read a list of project directories from a config file
2. For each, use AppleScript (macOS) or your terminal's equivalent to create a new tab
3. Set the tab title, colors, and initial command (`cd <project> && claude`)
4. Add a shell alias so you can launch everything with one word

### `~/.claude/settings.local.json` (Permissions)

Controls which tools Claude can use without asking. This is personal risk tolerance — start restrictive and open up as you build trust. The default (prompting for everything) is fine for getting started.

### `open-projects.sh` (Multi-Project Launcher)

A script that opens Claude Code in multiple project directories simultaneously, each in its own terminal tab. Useful if you work across several projects daily. Not necessary for single-project collaboration.

### Gmail / Calendar MCP Servers

I connect Gmail and Google Calendar via MCP servers so Claude can triage my inbox and check my schedule at session startup. This requires OAuth credentials and is entirely optional. The collaborative skills (`/start`, `/close`) work fine without it — they just skip the email and calendar steps.

### Institutional Templates (`templates/`)

The author maintains templates for recurring institutional submissions (IRB applications, grant forms, etc.) specific to his university. These are excluded from the repo because they are institution-specific, but the `templates/` directory is a useful pattern. Build your own for any multi-field form you submit more than once — IRB protocols, grant budget justifications, data management plans. Having a template means Claude can fill it in from project details rather than starting from scratch.

### Calendar Check Rule (`rules/calendar-check.md`)

A rule that ensures all five of the author's Google Calendars (personal, work, spouse, two kids' activities) are queried in parallel whenever checking availability. Contains personal email addresses and calendar IDs. If you use Google Calendar MCP, create your own version listing your calendars.

### Remove Skill (`skills/remove/`)

A skill for removing completed items from a personal Google Doc to-do list. Contains the specific document ID. If you track tasks in a Google Doc, create your own version with your doc ID.

### Slide Deck Examples (`skills/slides/examples/`)

The `/slides` skill includes calibration examples from the author's own conference and seminar presentations. These are excluded from the repo. The skill works without them — it falls back to the rhetorical rules in the SKILL.md itself — but having real examples improves output quality. To build your own: collect 3-5 of your best slide decks (tex + pdf) and place them in `skills/slides/examples/`.

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
