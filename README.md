# Claude Code for Academic Research

> [!IMPORTANT]
> **The shared history was cleaned and rewritten on 2026-05-28.** If you cloned before
> then, a plain `git pull` will fail ("unrelated histories"). Run the one-time updater
> below — it adopts the new history, clears any old content from your clone, and
> re-registers the shared hooks (raw-data protection, the PII/secret push guard, and the
> publish guard):
> ```bash
> cd ~/claude-research-config
> git fetch origin && git checkout origin/main -- tools/update.sh && bash tools/update.sh
> ```
> Safe and idempotent: it stashes any local changes first, and only touches this clone —
> never your sync folder or personal config.

A shared configuration for [Claude Code](https://claude.ai/code) tailored to collaborative academic research in economics. Provides rules, hooks, and session protocols that enforce data integrity, academic standards, and reproducible workflows.

## What's Here

| Directory | Purpose |
|-----------|---------|
| `rules/` | Behavioral rules auto-loaded by Claude Code — academic integrity, data protection, a **generic** applied-econ writing-style guide (plus a template for building your own voice profile), project structure, data pipeline conventions, script architecture guardrails, task management |
| `hooks/` | Lifecycle hook scripts — blocks writes to raw data directories, monitors context usage, preserves state before context compression, and blocks `git push` of PII/secrets to non-Overleaf remotes |
| `tools/` | Publish guard — a personal-content scanner and `pre-push` hook that block your identity, institution, and project names from reaching the shared repo (activated by `setup.sh` via `core.hooksPath`) |
| `skills/` | Slash commands — `/start` (session startup), `/close` (handoff document), `/review-paper` (simulated referee report), `/slides` (beamer decks), `/verify-bib` (citation integrity check), `/figurenotes` (table/figure notes), `/qa-loop` (adversarial critic-fixer), and others |
| `agents/` | Fresh-context reviewer agents — writing quality review, methodology audit |
| `templates/` | Reusable institutional templates (IRB submissions, etc.) |

## Collaborator Setup

If a coauthor pointed you here, run this **once on each of your machines** — not inside the shared project folder:

```bash
# 1. Install Claude Code (https://claude.ai/code) if you haven't already

# 2. Clone this repo somewhere local (outside any shared Dropbox folder)
git clone https://github.com/steveofconnell/oconnell-collaborative-claude-code.git ~/claude-research-config

# 3. Run setup — full bootstrap (Homebrew, iTerm2, Rectangle, sync folder, launcher)
bash ~/claude-research-config/setup.sh

# 4. Open Claude Code in the shared project directory
cd /path/to/shared-project
claude
# then type: /start
```

`setup.sh` is opinionated: by default it installs the full toolchain the rest of this config assumes. Specifically, it:

- Picks a **cross-device sync folder** (default `~/Dropbox/.claudeconfig`) and moves your personal config there. Your `~/.claude/` becomes a set of symlinks into that folder, so the same `CLAUDE.md`, settings, learned preferences, and project list follow you across every device that has Dropbox (or iCloud/OneDrive) synced.
- Installs **Homebrew** if missing.
- Installs **iTerm2**. Required — the multi-project launcher uses iTerm2 AppleScript to set per-project background colors. Native Terminal.app does not support this.
- Installs **Rectangle** and imports a default keybinding set for window snapping.
- Installs the **iTerm2 "Claude" Dynamic Profile** and tab-switching shortcuts (Option+Cmd+Left/Right).
- Installs `open-projects.sh` into your sync folder, adds an `open-projects` shell alias, and seeds an example tab-color config.
- Symlinks the shared `rules/`, `hooks/`, `skills/`, `agents/` from the cloned repo into `~/.claude/`, so `git pull` updates them.

If you want a stripped-down install (no Homebrew/iTerm/Rectangle/launcher — just the rules and skills), pass `--minimal`:

```bash
bash ~/claude-research-config/setup.sh --minimal
```

`--minimal` only symlinks the shared subdirs and exits. You manage your own `CLAUDE.md`, settings, and launcher (or do without).

## How It Works

There are three locations involved, and each owns a distinct kind of config:

| Location | What lives there | How it's shared |
|---|---|---|
| **Cloned repo** (`~/claude-research-config/`) | Shared rules, hooks, skills, agents | Same on every collaborator's machine; updates via `git pull` |
| **Sync folder** (`~/Dropbox/.claudeconfig/` by default) | Your personal `CLAUDE.md`, `settings.json`, `settings.local.json`, `open-projects.sh`, color config, iTerm/Rectangle plists | Shared across **your own** devices via Dropbox; not shared with collaborators |
| **`~/.claude/`** on each machine | Symlinks pointing into the two locations above | Per-machine; rebuilt by `setup.sh` |

`setup.sh` keeps this layout consistent on a fresh device: it points `~/.claude/CLAUDE.md`, `~/.claude/settings.json`, etc. at the sync folder, and points `~/.claude/rules/`, `~/.claude/skills/`, etc. at the repo.

**What stays purely local on each machine** (never symlinked, never synced):

- `~/.claude/projects/`, `sessions/`, `history.jsonl`, `todos/` — Claude Code's volatile state. Symlinking these breaks Claude Code.

**What appears in the shared project folder** (the Dropbox folder you and your coauthor work in):

- The project's research files
- `CLAUDE.md` — project-specific instructions written by the PI, synced to all collaborators
- `.workspace/` — handoffs, memory, project TODOs

No `.claude/` directory, no per-project copies of these tools. Each collaborator's machine is set up once via `setup.sh` and stays that way.

To pick up routine updates after the maintainer pushes new rules or skills:
```bash
cd ~/claude-research-config && git pull && bash setup.sh
```

If `git pull` ever reports divergent or unrelated histories (e.g., after a history
cleanup), run the updater instead — it re-syncs cleanly and clears old content from your
clone:
```bash
git fetch origin && git checkout origin/main -- tools/update.sh && bash tools/update.sh
```

Re-running `setup.sh` is idempotent — every step checks whether the work is already done.

## What the Config Enforces

### Data Integrity
- **Raw data is read-only.** A hook blocks all writes to `1rawdata/` directories. Raw data must never be modified — all transformations happen in processing scripts.
- **No fabricated data.** When reading values from scans, PDFs, or images, Claude must report confidence levels and flag illegible values rather than guessing.
- **Source documentation required.** Every raw data file needs a `source.txt` documenting provenance.

### Academic Standards
- **No fabricated citations.** Every reference must be verified. Claude will say "I cannot verify this" rather than constructing a plausible-looking entry.
- **No plagiarism.** All prose is original composition. No close paraphrasing.
- **No AI attribution.** Work product belongs to the authors. Claude never inserts its own name into any output.

### Reproducibility
- **No hardcoded data in scripts.** All data lives in files, not embedded in code.
- **Script outputs trace to manuscripts.** When a script produces values cited in a paper, the connection is documented.
- **Standard folder structure.** `1rawdata/` → `2processing/` → `3data/` → `4code/` → `5manuscript/`. Self-documenting and consistent across projects.

### Session Continuity
- **`/start` and `/close` are mandatory.** Every session begins with `/start` and ends with `/close`. These are not optional conveniences — they are the mechanism by which collaborators stay informed of each other's work. Skipping `/close` means the next person opens the project with no idea what happened. Skipping `/start` means working without context from prior sessions.
- **Handoff documents identify their author.** Every handoff records who ran the session, what was done, what files were touched, and what's next. When you `/start` a project and the last handoff was written by a coauthor, you see exactly what they did and where they left off.
- **Project memory.** Key decisions, references, and context persist across sessions in `.workspace/memory/`.

## What Belongs in the Shared Project Folder

```
shared-project/
├── CLAUDE.md          # Project-specific instructions (written by the PI, syncs to all)
├── .workspace/
│   ├── HANDOFF_*.txt  # Session handoffs (one per session, syncs to all)
│   ├── memory/        # Memory files (managed by Claude, syncs to all)
│   └── TODO.md        # Project task list
├── 1rawdata/          # Source data (protected — read-only)
├── 2processing/       # Cleaning/construction scripts
├── 3data/             # Analysis-ready datasets
├── 4code/             # Analysis scripts
└── 5manuscript/       # Drafts, tables, figures
```

No `.claude/` folder. No per-project config. Config is each person's own business, set up globally on their machine.

## Personal Configuration

The author also uses personal configuration files (global identity, writing voice profile, sound notifications, email integration, multi-project launcher) that are not included in this repo. See **[PERSONAL_CONFIG.md](PERSONAL_CONFIG.md)** for descriptions and setup guidance — you are encouraged to create your own versions.

## Acknowledgments

This configuration draws inspiration and some rules, skills, and workflow patterns directly from [Pedro Sant'Anna's](https://psantanna.com/) Claude Code setup and [Claude Blattman's](https://claudeblattman.com/) work.

## License

MIT
