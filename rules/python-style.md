---
description: "Python coding style — PEP 8 base, house defensive-practice conventions, paths/IO and reproducibility rules"
paths:
  - "**/*.{py,ipynb}"
---

# Python Coding Style

Applies to: all `.py` files and Python written inline (notebooks, one-off probes),
every project.

The base is **PEP 8** (https://peps.python.org/pep-0008/) and, where PEP 8 is
silent, the **Google Python Style Guide**
(https://google.github.io/styleguide/pyguide.html). Both are conventional and
widely followed; nothing below is idiosyncratic except the sections marked as
house conventions, which state the reasoning that makes them worth keeping.

## The override that beats every rule here

**Match the file you are editing.** A codebase that is internally consistent is
worth more than one that is individually correct file by file. If the surrounding
scripts use `os.path` and `%`-formatting, a new script in that folder uses
`os.path` and `%`-formatting, even though the general preference below is
`pathlib` and f-strings. Raise the inconsistency if it matters; do not resolve it
unilaterally in the middle of unrelated work.

## Formatting

- 4-space indentation, never tabs. Maximum line length 79 characters for code and
  72 for docstrings and comments, per PEP 8. If a project already runs `black`
  (88 characters), follow the project.
- Two blank lines between top-level definitions, one between methods.
- Spaces around binary operators and after commas; none immediately inside
  brackets or before a comma.
- One import per line. Order: standard library, third party, local, separated by
  blank lines. No wildcard imports.
- Prefer implicit line continuation inside brackets over backslashes.

## Naming

- `snake_case` for functions, variables, methods, and modules.
- `CapWords` for classes. `UPPER_SNAKE_CASE` for module-level constants.
- A single leading underscore marks something internal to the module.
- Names describe the thing, not its type: `n_groups`, not `groups_int`. This is
  the Python side of the project-wide rule against cryptic names, and it means no
  `df2`, `tmp`, `x1` surviving into committed code.
- Avoid `l`, `O`, `I` as single-character names; they are unreadable in most
  fonts.

## Structure

- One script, one task, matching the folder-level pipeline rules in
  `project-structure.md` and the three-question test in `script-architecture.md`.
- Put executable logic in functions and use the standard entry-point guard:

  ```python
  def main():
      ...

  if __name__ == "__main__":
      main()
  ```

  This is what makes a script importable for testing and prevents work running on
  import.
- Module-level constants go at the top, after imports, in `UPPER_SNAKE_CASE`.
  Paths, thresholds, and expected-state values belong there, never buried inline.
- Use `# ====` section banners inside long scripts, per `script-architecture.md`.

## Docstrings and comments

- Every script gets a module docstring naming the file, what it does, and
  explicit **Input** and **Output** blocks listing paths. This is a house
  convention and it is the single most useful thing in the file: it lets a
  collaborator see what a script consumes and produces without reading it.
- Public functions get a docstring stating what they return, not how they work.
- Inline comments record the **reasoning and provenance of judgment calls**: why
  this threshold, where this figure came from, which decision it implements, what
  was rejected. A comment restating the code is noise; a comment recording why the
  code is that way is the point.

## Paths and I/O

- Never hardcode absolute paths or a user's home directory. Resolve from the
  script's own location:

  ```python
  ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  ```

  or `Path(__file__).resolve().parents[1]` with `pathlib`. Never `os.chdir`.
- Always use a context manager (`with open(...)`) for files.
- Specify the encoding explicitly on text I/O: `encoding="utf8"`. Use
  `encoding="utf-8-sig"` when a byte-order mark may be present.
- Use `newline=""` when reading or writing CSV, which the `csv` module requires
  for correct handling of embedded newlines.

## Dependencies

- Prefer the standard library. `csv`, `json`, `collections`, `itertools`,
  `statistics`, `re` and `pathlib` cover most data-processing work, and every
  dependency avoided is one the replicator does not have to install.
- Reach for pandas, numpy, polars or pyarrow when the work genuinely calls for it
  (reshaping, joins across large tables, numerical work), not by reflex for a
  loop over a few thousand rows.
- Any new third-party package is added to `README_replication.md` in the same
  change that introduces it, per `data-pipeline.md`.
- Never hardcode credentials. Read them from the environment with a documented
  fallback and name the variable in the script header.

## Errors and defensive practice

These are house conventions, adapted from the Stata patterns in
`stata-style.md` because the reasoning is language-independent.

- **Fail loudly on a violated precondition.** A missing input file raises with an
  actionable message naming what to run first, rather than producing an empty
  output:

  ```python
  if not os.path.exists(INVENTORY):
      raise SystemExit("Run 02_inventory.py first: %s missing" % INVENTORY)
  ```
- **Assert expected state.** Pin the row counts, file counts and shares that the
  script depends on, so a change upstream fails the run instead of silently
  producing a different dataset under the same name. Comment each one with where
  the figure came from and when it was verified.
- **Count before and after anything that changes row counts.** Print the ledger.
  A filter that silently drops rows is the most common way a result goes wrong
  without anyone noticing.
- **Flag, do not delete.** Build `*_flag` columns and filter at the analysis step
  rather than dropping observations during processing. Deleting early destroys
  the evidence needed to check the decision later.
- Never use a bare `except:`. Catch the specific exception. Never swallow an
  exception silently; if it is genuinely ignorable, comment why.
- No mutable default arguments (`def f(x=[])`). Use `None` and build inside.

## Data handling

- Never hardcode data values (numbers, records, tables) in a script; they belong
  in files under `1rawdata/` or `3data/` with provenance. See `data-pipeline.md`.
  A hand-entered dict of *decisions* (task labels, PI calls on specific files) is
  not data and is fine, provided it is commented with its source.
- Imputation targets missing values only, and the missing-value test appears
  explicitly in the expression. Corrections require authorization and go to a new
  column. See `data-pipeline.md`.
- Check whether a directory has a `pii.txt` marker before reading any data file
  in it, per `data-integrity.md`.

## Testing and reproducibility

- Set a seed for anything stochastic and state it at the top.
- Scripts should be idempotent: running twice produces the same output, and
  rerunning after a partial failure is safe.
- For work over ~20 minutes, flush results periodically and skip already-completed
  items on restart, per the global learned preference. For work measured in
  seconds, say so in the docstring rather than building checkpointing that earns
  nothing.
- Where a project has tests, use `pytest`, name files `test_*.py`, and keep them
  outside the numbered pipeline folders.
