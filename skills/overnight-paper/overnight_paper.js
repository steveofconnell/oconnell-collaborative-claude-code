export const meta = {
  name: 'overnight-paper',
  description: 'Autonomous overnight loop that improves a whole research project toward a better paper: data sourcing, scripts, analysis, tables/figures, technical text, and rhetoric. Runs in an isolated git worktree, compounds output-neutral changes, propagates result-moving changes through the pipeline as proposals, and stops at convergence.',
  whenToUse: 'Unattended overnight development of a research project at any stage. Invoked via the /overnight-paper skill, which sets up the worktree and passes args.',
  phases: [
    { title: 'Round 1' },
    { title: 'Round 2' },
    { title: 'Wrap' },
  ],
}

// ---------------------------------------------------------------------------
// args (set by the /overnight-paper skill):
//   worktreePath : absolute path to the dedicated git worktree (REQUIRED)
//   branch       : the work branch name, for log messages
//   maxRounds    : hard cap on rounds (default 6; use 2 for a test run)
//   staleStop    : stop after this many consecutive no-material rounds (default 2)
//   objective    : one-line statement of what "better" means for THIS paper
//                  (e.g. "tighten the identification argument and finish the results section")
//
// SCOPE: the whole artifact graph inside worktreePath — raw data (read-only) ->
// 2processing/ -> 3data/ -> 4code/ -> production tables/figures -> 5manuscript/ text.
// 1rawdata/ is never written. The loop NEVER merges; you merge in the morning.
// ---------------------------------------------------------------------------

const WT = args && args.worktreePath
if (!WT) throw new Error('worktreePath is required (the /overnight-paper skill sets this up)')
const MAX = (args && args.maxRounds) || 6
const STALE_STOP = (args && args.staleStop) || 2
const OBJECTIVE = (args && args.objective) || 'make the paper better across all layers'

// The single authority principle, applied at every layer (data -> rhetoric).
const RULES = `
THE ONE TEST for tiering every change: does it alter what the paper CLAIMS or SHOWS?

GREEN (apply now, compounds across rounds) — changes that CANNOT move a reported
  number, result, or claim: prose tightening, voice-rule enforcement, output-neutral
  refactors (identical output before/after), figure/table formatting and notes,
  fixing cross-references and paths, docstrings, README/dependency docs, regenerating
  an output from code whose logic did not change.
YELLOW (PROPOSE only — make it in the worktree, show before/after, never merge):
  ANY change that moves a reported number (even an obviously-correct bug fix —
  if a result moves, it is YELLOW); changes a specification, sample, estimator,
  fixed-effect structure, clustering, weighting, or functional form; alters a claim;
  adds new substantive/argument-bearing prose or a new section; acquires new raw
  data; corrects a data VALUE; or adds a new software dependency.
RED (never do — flag only): fabricate a citation or value; write to 1rawdata/;
  overwrite an existing (non-missing) data value; write an empirical claim not
  traceable to a real output (use a TKTK marker); insert a citation that cannot be
  verified against the project .bib (use TKTK [cite: ...]).

PROPAGATION: a change is not done when a file is edited — push it forward through the
  pipeline. If code changes, regenerate affected outputs and re-sync the manuscript's
  numbers and prose, then present the whole cascade as ONE coupled change.
SPECIFICATION INTEGRITY: never run a specification search and keep the best; never
  touch the sample. Alternative specifications may only be PROPOSED, with everything
  tried disclosed. The specification and sample are the author's decisions.
VOICE: match the author's published voice; reject lateral rewrites (different words,
  no real improvement) and any edit that trades the author's voice for generic polish.
GROUNDING: every empirical claim traces to a real output file; every citation is real.
`

const FINDINGS = {
  type: 'object',
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          title: { type: 'string' },
          detail: { type: 'string' },
          layer: { type: 'string', enum: ['data', 'processing', 'analysis', 'tables_figures', 'technical_text', 'rhetoric'] },
          location: { type: 'string' },
          material: { type: 'boolean', description: 'a real improvement a careful author would make, not a lateral rewrite or nitpick' },
          tier: { type: 'string', enum: ['green', 'yellow', 'red'] },
          value: { type: 'string', enum: ['high', 'medium', 'low'] },
        },
        required: ['title', 'detail', 'layer', 'location', 'material', 'tier', 'value'],
      },
    },
  },
  required: ['findings'],
}

const REVISION = {
  type: 'object',
  properties: {
    changes: { type: 'array', items: { type: 'object', properties: {
      file: { type: 'string' }, summary: { type: 'string' },
      movedResult: { type: 'boolean' },
    }, required: ['file', 'summary', 'movedResult'] } },
    committed: { type: 'boolean' },
  },
  required: ['changes', 'committed'],
}

const VERDICT = {
  type: 'object',
  properties: {
    pass: { type: 'boolean' },
    violations: { type: 'array', items: { type: 'string' } },
    consistent: { type: 'boolean', description: 'text numbers == tables == script outputs == data' },
  },
  required: ['pass', 'violations', 'consistent'],
}

// Lenses span the whole artifact graph.
const LENSES = [
  { key: 'pipeline', focus: 'data processing and analysis CODE: bugs, reproducibility gaps, output-neutral refactors, and result-moving fixes (the latter are proposals)' },
  { key: 'outputs', focus: 'production tables and figures: correctness vs source scripts, legibility, notes, and whether any output is stale relative to current code/data' },
  { key: 'technical_text', focus: 'technical content of the manuscript: every number/claim traceable to an output, results and methods complete and grounded, gaps marked TKTK' },
  { key: 'rhetoric', focus: 'argument, framing, structure, exposition, and academic voice — genuine elevation only, no lateral rewrites' },
]

const changelog = []
const quarantine = []
let stale = 0
let round = 0

while (round < MAX && stale < STALE_STOP) {
  round++
  const ph = `Round ${round}`
  phase(ph)

  // 1. Finder panel — independent lenses over the whole project, in parallel
  const reviews = await parallel(LENSES.map(l => () =>
    agent(
      `You are improving a research project toward this objective: "${OBJECTIVE}". ` +
      `It lives in the git worktree at ${WT} (raw data, 2processing/, 3data/, 4code/, ` +
      `production tables/figures, and 5manuscript/). Lens: ${l.focus}. Find the highest-value ` +
      `improvements available right now. Be strict about MATERIAL (a real improvement) vs a ` +
      `lateral rewrite or nitpick.\n${RULES}`,
      { label: `find:${l.key}`, phase: ph, schema: FINDINGS }
    )
  ))
  const findings = reviews.filter(Boolean).flatMap(r => r.findings || [])
  const material = findings.filter(f => f.material)
  if (material.length === 0) {
    stale++
    log(`${ph}: no material improvement found (stale ${stale}/${STALE_STOP})`)
    continue
  }
  stale = 0

  const green = material.filter(f => f.tier === 'green')
  const yellow = material.filter(f => f.tier === 'yellow')
  yellow.forEach(f => quarantine.push({ round, ...f }))
  log(`${ph}: ${green.length} green to apply, ${yellow.length} yellow proposed for sign-off`)

  // 2. Reviser — apply ONLY green; propagate through the pipeline; commit the round
  if (green.length > 0) {
    const rev = await agent(
      `Apply ONLY these GREEN improvements to the worktree at ${WT}. They must be output-neutral ` +
      `(cannot move any reported number). PROPAGATE each change forward: if you touch code, ` +
      `regenerate affected outputs and re-sync the manuscript. If applying any item would in fact ` +
      `move a result, STOP that item and report it as movedResult:true instead of applying it. ` +
      `When done: \`git add -A && git commit -m "round ${round}: improvements toward better paper"\` ` +
      `inside ${WT}.\nGREEN items:\n${JSON.stringify(green, null, 2)}\n${RULES}`,
      { label: `revise:r${round}`, phase: ph, schema: REVISION }
    )

    // 3. Verifier — integrity + voice + CROSS-LAYER CONSISTENCY; revert on failure
    const ver = await agent(
      `In the worktree at ${WT}, inspect this round's diff (\`git show HEAD\`). Confirm NO violation ` +
      `of the rules below, AND that the project is cross-layer CONSISTENT: every number in the text ` +
      `matches its table, every table matches its source script's current output, every figure matches ` +
      `current data, and no green change silently moved a result or touched a specification/sample. ` +
      `Return pass:false with violations if any check fails.\n${RULES}`,
      { label: `verify:r${round}`, phase: ph, schema: VERDICT }
    )

    if (ver && (ver.pass === false || ver.consistent === false)) {
      log(`${ph}: verifier REJECTED — reverting. ${(ver.violations || []).join('; ')}`)
      await agent(
        `In the worktree at ${WT}, run \`git reset --hard HEAD~1\` and confirm the tree is clean.`,
        { label: `revert:r${round}`, phase: ph }
      )
    } else if (rev) {
      ;(rev.changes || []).forEach(c => {
        changelog.push({ round, ...c })
        if (c.movedResult) quarantine.push({ round, title: `result-moving fix held back: ${c.file}`, detail: c.summary, tier: 'yellow', layer: 'analysis' })
      })
    }
  }
}

phase('Wrap')
return {
  branch: (args && args.branch) || '(unknown)',
  worktreePath: WT,
  objective: OBJECTIVE,
  rounds: round,
  converged: stale >= STALE_STOP,
  stoppedReason: stale >= STALE_STOP ? 'converged (stale rounds)' : 'hit maxRounds',
  changelog,
  quarantine,
}
