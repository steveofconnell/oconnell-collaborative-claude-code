# Claude Code for Academic Research

A shared configuration for [Claude Code](https://claude.ai/code) tailored to collaborative academic research in economics. Provides rules, hooks, and session protocols that enforce data integrity, academic standards, and reproducible workflows.

## What's Here

| Directory | Purpose |
|-----------|---------|
| `rules/` | Behavioral rules auto-loaded by Claude Code — academic integrity, data protection, writing standards, project structure, data pipeline conventions, script architecture guardrails, task management |
| `hooks/` | Lifecycle hook scripts — blocks writes to raw data directories, monitors context usage, preserves state before context compression |
| `skills/` | Slash commands — `/start` (session startup), `/close` (handoff document), `/review-paper` (simulated referee report), `/slides` (beamer decks), `/verify-bib` (citation integrity check), `/figurenotes` (table/figure notes), `/qa-loop` (adversarial critic-fixer), and others |
| `agents/` | Fresh-context reviewer agents — writing quality review, methodology audit |
| `templates/` | Reusable institutional templates (IRB submissions, etc.) |

## Quick Start — Collaborator Setup

If a coauthor pointed you here and you're joining a shared project:

```bash
# 1. Install Claude Code (https://claude.ai/code) if you haven't already

# 2. Clone this repo
git clone https://github.com/steveofconnell/oconnell-collaborative-claude-code.git ~/claude-research-config

# 3. In the shared project directory, link the config
cd /path/to/shared-project
~/claude-research-config/setup.sh

# 4. Start working
claude
# then type: /start
```

The `setup.sh` script creates symlinks from the project's `.claude/` directory into this repo. You get all rules, hooks, and skills automatically. Updates propagate when you `git pull`.

## Quick Start — New Project

To set up a new research project with this config:

```bash
mkdir ~/Dropbox/MyNewProject
cd ~/Dropbox/MyNewProject
~/claude-research-config/setup.sh
claude
# then type: /setup-project
```

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
- **Intermediate handoffs.** During long sessions, Claude writes checkpoint handoffs (same format, letter-suffixed filenames like `HANDOFF_2026-04-06b.txt`) after sustained blocks of work. These are not session closes — they are continuity insurance. If a session ends unexpectedly or a coauthor opens the project mid-stream, there is a recent record of what happened.
- **Project memory.** Key decisions, references, and context persist across sessions in `.workspace/memory/`.

## Personal Configuration

The author also uses personal configuration files (global identity, writing voice profile, sound notifications, email integration, multi-project launcher) that are not included in this repo. See **[PERSONAL_CONFIG.md](PERSONAL_CONFIG.md)** for descriptions and setup guidance — you are encouraged to create your own versions.

## File Structure in a Configured Project

After running `setup.sh`, your project looks like:

```
my-project/
├── CLAUDE.md                    # Project-specific instructions (you write this)
├── MEMORY.md                    # Project memory index (managed by Claude)
├── .claude/
│   ├── settings.json            # Hooks config (copied, editable per project)
│   ├── rules/   → repo/rules/  # Symlink
│   ├── hooks/   → repo/hooks/  # Symlink
│   ├── skills/  → repo/skills/ # Symlink
│   └── agents/  → repo/agents/ # Symlink
├── .workspace/
│   ├── TODO.md                  # Project task list
│   ├── SESSION_LOG.md           # Running session log
│   ├── memory/                  # Memory files
│   ├── handoffs/                # Session handoff documents
│   ├── plans/                   # Active plans
│   ├── scratch/                 # Exploratory scripts, intermediate data
│   ├── reference/               # Source PDFs, text extractions, codebooks
│   ├── notes/                   # Working prose: memos, outlines, lit notes
│   └── logs/                    # Pipeline run logs, build logs
├── 1rawdata/                    # Source data (protected — read-only)
├── 2processing/                 # Cleaning/construction scripts
├── 3data/                       # Analysis-ready datasets
├── 4code/                       # Analysis scripts
└── 5manuscript/                 # Drafts, tables, figures
```

## Updating

```bash
cd ~/claude-research-config
git pull
```

All linked projects pick up the changes immediately via symlinks.

## Acknowledgments

This configuration draws inspiration and some rules, skills, and workflow patterns directly from [Pedro Sant'Anna's](https://psantanna.com/) Claude Code setup and [Claude Blattmann's](https://github.com/claudeblattmann) work.

## License

MIT
