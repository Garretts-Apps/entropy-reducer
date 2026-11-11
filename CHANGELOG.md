# Changelog

## 1.2.0

- **The workflow is now a skill.** `commands/reduce-entropy.md` and the pointer skill
  `skills/entropy-reduction/` are merged into `skills/reduce-entropy/SKILL.md`. Invocation
  is unchanged: `/reduce-entropy` (`/entropy-reducer:reduce-entropy`), or a plain request
  such as "remove the dead code here".
- **End-to-end evals.** `evals/` has a fixture app with seeded entropy and four
  `claude plugin eval` cases: the plan finds the dead function and the duplicate, keeps a
  dynamically referenced function, leaves UI markup alone, and the skill triggers on a
  plain-language request. See the README for how to run them; each run costs model usage.
- **Two workflow fixes the evals exposed.** Every phase's agents now run however small the
  scope is (the orchestrator used to do the analysis itself on a small codebase and present
  an unaudited plan), and when plan mode is unavailable, as in a non-interactive session,
  the workflow stays read-only and gives the plan as its final message.
- `scripts/validate.py` checks the skill instead of the command, and fails if a stale
  command or pointer skill reappears.

## 1.1.0

Reworked the workflow so that what reaches the plan is proven rather than asserted.

- **Evidence is required.** Analyzers must attach the reference search, duplicate diff, or
  edge-case walk-through behind every finding, and must rule out dynamic usage (reflection,
  dependency injection, route tables, templates, config) and library public API before
  calling code dead.
- **The audit is independent.** The safety auditor re-derives the evidence instead of
  trusting it, and rejects findings whose cited lines no longer match the file.
- **The UI guard judges effect, not file type.** Previously any edit in a UI file — or in a
  utility a component imported — was excluded, which vetoed nearly every finding in a
  frontend codebase. It now clears changes that provably cannot reach what a user sees and
  flags the rest.
- **Applying is verified.** The apply phase surfaces a dirty working tree, records a test and
  build baseline before the first edit, applies one finding at a time, and reverts any
  finding that regresses against the baseline. Nothing is committed.
- **Scope is controlled.** Preflight uses `git ls-files`, skips generated, vendored, and
  build output, shards large codebases, and asks before analyzing an oversized scope.
- **Cross-shard duplication** gets its own analyzer pass; finding IDs are prefixed per
  analyzer so they no longer collide.
- **Explicit non-goals:** no code golf, no deleting tests, comments, error handling, or
  logging, no new dependencies.
- New flags: `--plan-only`, `--types`, `--include-caution`.
- Added `scripts/validate.py` and a CI workflow that checks manifests, frontmatter, and
  version consistency.
- README install instructions now use the real marketplace name.
- Agent and skill descriptions are short what-plus-when statements; the multi-line
  example blocks are gone (agents are dispatched by name, so they only cost context).
- The plugin version is declared once, in `plugin.json`.
- `allowed-tools` lists current tool names; CI also runs `claude plugin validate`.

## 1.0.0

Initial release.
