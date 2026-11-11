# entropy-reducer

A Claude Code plugin that reduces code entropy — the same observable behavior from less code, with proof.

## What it does

A team of specialized agents analyzes your codebase and produces a plan for removing code without:

- changing any UI/UX behavior
- switching programming languages, frameworks, or build systems
- adding dependencies
- removing tests, error handling, logging, or comments to move the number
- introducing bugs or performance regressions

Fewer lines is how the result is measured, not the goal. The goal is less to read, maintain, and get wrong — so code golf and style-only edits are excluded by design.

## Usage

```
/reduce-entropy [path] [--plan-only] [--types dead-code,duplicate,...] [--include-caution]
```

| Argument | Effect |
|----------|--------|
| `path` | Directory to analyze. Defaults to the current working directory. |
| `--plan-only` | Produce the plan and stop. Nothing is ever edited. |
| `--types` | Restrict to finding types: `dead-code`, `duplicate`, `consolidation`, `verbose-pattern`, `over-abstraction`, `redundant-definition`, `unused-import`, `config`, `boilerplate`. |
| `--include-caution` | Include CAUTION-rated findings in the apply set (they are opt-in otherwise). |

Installed as a plugin, the full name is `/entropy-reducer:reduce-entropy`. You can also just ask — "reduce entropy in `src/`", "remove the dead code here" — and Claude starts the same workflow.

## How it works

The whole workflow is one skill, [`skills/reduce-entropy/SKILL.md`](skills/reduce-entropy/SKILL.md), which orchestrates the four agents in [`agents/`](agents/):

| Phase | Agent | Model | What happens |
|-------|-------|-------|--------------|
| 0. Preflight | orchestrator | Sonnet | Scopes files (`git ls-files`, minus generated/vendored/build output), fixes one line-count method, detects test and build commands, shards large codebases |
| 1. Review | codebase-reviewer | Haiku | Maps each shard: file inventory, public surface, dynamic references, leads |
| 2. Analyze | entropy-analyzer | Sonnet | Finds reductions per shard plus a cross-shard duplication pass — each finding with evidence |
| 3. Audit | safety-auditor | Sonnet | Independently re-verifies every finding: APPROVED, CAUTION, or REJECTED |
| 4. Guard | ui-guardian | Haiku | Clears only changes with no observable UI/UX effect |
| 5. Plan | orchestrator | Sonnet | Presents the apply set, opt-in list, and exclusions for your approval |
| 6. Apply | orchestrator | Sonnet | Baseline → apply one finding at a time → verify → revert on regression |

Agents within a phase run in parallel.

### Why you can trust the plan

- **Evidence or exclusion.** A finding needs proof: a repository-wide reference search for dead code (including reflection, dependency injection, route tables, templates, and config), a diff of the copies for duplicates, an edge-case walk-through for rewrites. In a library, exported symbols are treated as live.
- **Independent audit.** The auditor re-derives the evidence rather than trusting the analyzer, and rejects any finding whose cited lines no longer match the file.
- **Effect-based UI guard.** The guard asks whether a user could perceive a difference — not whether the file is a component — and flags anything it cannot rule out.

### What you get

**The plan** (before anything changes): scope and line count with the counting method, each proposed reduction with file, lines, savings, and evidence, CAUTION findings as opt-in, everything excluded and why, and the exact commands that will verify the result.

**The result** (after you approve): which findings were applied, which were reverted and why, measured before/after lines against the projection, and verification status against the pre-change baseline.

**Always starts in plan mode.** Nothing changes until you approve. If your working tree has uncommitted changes you are asked before anything is applied, and the plugin never commits, stashes, or resets on your behalf.

## Language support

Works with any programming language. Agents research an unfamiliar language before analyzing it, and never recommend changing the language.

Line counts use `scc` or `cloc` when installed (code lines only) and fall back to `wc -l`; the method is stated in every report so numbers are reproducible. Static tools such as `knip`, `ts-prune`, `vulture`, `deadcode`, `staticcheck`, or `jscpd` are used as additional evidence when present, but none are required.

## Model usage

- **Haiku** for fast passes (review, UI guard)
- **Sonnet** for orchestration, analysis, and audit
- **Never Opus** — cost-efficient by design

## Install

```
/plugin marketplace add Garretts-Apps/entropy-reducer
/plugin install entropy-reducer@entropy-reducer
```

For local development:

```bash
claude --plugin-dir ./entropy-reducer
```

## Development

```bash
python3 scripts/validate.py
```

Checks that the manifests parse and the version is declared once, that every agent has valid frontmatter with a pinned Haiku/Sonnet model and read-only tools, and that the skill, README, and changelog stay in sync. CI runs it, plus Claude Code's own `claude plugin validate .`, on every push and pull request.

### Evals

`evals/` holds an end-to-end suite for [`claude plugin eval`](https://code.claude.com/docs/en/plugin-evals). The cases run the workflow against a small fixture app with seeded entropy; [`evals/fixture/README.md`](evals/fixture/README.md) is the answer key.

| Case | Asserts |
|------|---------|
| `plan-finds-dead-code-and-duplicate` | the apply set names the dead function and the duplicated helper in both files |
| `plan-keeps-dynamically-referenced-function` | a function reached only through `getattr` is not in the apply set |
| `plan-excludes-ui-change` | two render functions whose markup differs are not merged |
| `skill-triggers` | a plain-language request invokes the skill |

```bash
claude plugin eval . --scaffold --ablation none -j 2
```

`--scaffold` lets each case copy the fixture into its workspace. `--ablation none` skips the no-plugin baseline, which means little for cases that call the skill by name. The three plan cases use `--plan-only` and are granted read-only tools, so nothing is edited. Graders are regexes and a tool-call check; none calls a judge model. `skill-triggers` is capped at four turns on purpose: it only checks that the skill fires, so its run ends with a "maximum number of turns" note and still passes.

**Every run makes real model calls on your account.** Each plan case is a full multi-agent run. Cases run once by default; pass `--runs 3` for a steadier score at three times the cost. The evals are not part of CI because they need credentials. Reports go to `evals/results/`, which is git-ignored.

See [CHANGELOG.md](CHANGELOG.md) for release notes.

## License

MIT
