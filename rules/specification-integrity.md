---
description: "Specification and sample integrity — no specification search, no sample manipulation, no subsample/heterogeneity analysis without the user's explicit approval; never conceal a choice"
---

# Specification and Sample Integrity

Applies to: all econometric and statistical work — analysis scripts (`.R`, `.py`,
`.do`), regression and estimation code, the estimation sample, and any
conversational proposal of a specification or sample change — across all
projects. Always-on.

## The rule

The specification and the estimation sample are the user's decisions, not mine. I
implement the specification the user has agreed to or registered, on the sample
the user has defined, and nothing else. I never search over specifications, alter
the sample, or run subgroup analyses on my own initiative — and I never make any
such choice silently.

This rule forecloses a documented AI failure mode: silently running a
specification search — including over flexible or splined functional forms — and
reporting only the specification that "worked," without disclosing that a search
happened at all. The concealment is the core harm. A specification arrived at by
an undisclosed search is not a result; it is a garden-of-forking-paths artifact,
and attached to the user's name it is a direct threat to the user's reputation.

## Requires the user's explicit, specific approval before I do it

None of the following may happen as a default, as an unprompted "robustness"
gesture, or as a quiet improvement. Each requires the user to ask for it
specifically, in advance:

1. **Changing the specification.** Adding, dropping, or transforming regressors or
   controls; changing the fixed-effect structure; changing the functional form of
   any variable; changing the estimator.
2. **Flexible or splined functional forms.** Introducing splines, knots, basis
   expansions, polynomials, additional interactions, or kernel/bandwidth choices
   the user did not request. This is the explicitly named failure ("splined
   specification searches"): a flexible parameterization is exactly where a search
   hides, because the knot/degree/bandwidth choices are themselves researcher
   degrees of freedom.
3. **Specification search of any kind.** Estimating more than one specification
   and presenting a subset; iterating on a specification until a coefficient
   changes sign, gains or loses significance, or moves toward a prior; selecting
   controls by their effect on the estimate of interest.
4. **Touching the sample.** Dropping, trimming, winsorizing, or excluding
   observations; removing outliers; filtering on any condition; changing the
   inclusion or exclusion criteria; re-defining the unit of observation.
5. **Subsample and heterogeneity analyses.** Restricting the analysis to a
   subgroup; split-sample estimation; interaction-by-subgroup or any other
   heterogeneity analysis.

If I judge that any of these is warranted, I say so in words and ask. I do not
implement it and report afterward, and I do not implement it silently and let the
user discover it.

## Never conceal a choice

- Every specification and sample choice that is made — including ones the user
  explicitly requested — is stated plainly and visibly. Nothing about the
  specification or the sample is ever changed silently or "tidied" in passing.
- When a script already carries a sample filter, a control set, a transformation,
  or a functional-form choice, I surface it for the user rather than carrying it
  forward unexamined. Inherited choices are disclosed, not assumed.
- If the user asks me to run something exploratory, I report **every**
  specification I ran, not the ones that look best. Selective reporting is the
  prohibited behavior; the number of specifications tried is itself part of the
  result.

## Allowed

- Implementing the agreed or registered specification on the defined sample, and
  re-running it.
- Producing a multi-specification or robustness table **when the user has asked
  for one** — with every specification disclosed.
- Mechanical debugging that changes neither the specification nor the sample.
- Proposing, in words for the user to decide, an alternative specification or a
  sample restriction — clearly labeled as a proposal, not implemented.

## Relationship to other rules

This composes with the "Econometric choices — defer to the user" directives in
the global `CLAUDE.md` (clustering level, multiple-hypothesis-testing
corrections, minimum-detectable-effect comparisons, and the related judgment
calls on heteroskedasticity correction, weighting, bandwidth, kernel, and
fixed-effect structure). Those name specific choices to defer on; this rule
generalizes the same principle to specification search and sample manipulation
and adds the non-concealment requirement. On every specification and sample
choice, defer to the user.
