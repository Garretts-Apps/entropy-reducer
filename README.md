# entropy-reducer

A Claude Code plugin that reduces code entropy — achieving the same functionality with less code, safely.

## What It Does

Deploys a team of specialized agents to analyze your codebase and produce a plan for reducing lines of code without:
- Changing any UI/UX behavior
- Switching programming languages
- Introducing bugs or performance regressions

## How It Works

```
/reduce-entropy [path]
```

The plugin runs 4 phases:

| Phase | Agent | Model | What It Does |
|-------|-------|-------|-------------|
| 1. Review | codebase-reviewer | Haiku | Reads entire codebase, maps architecture, counts LOC |
| 2. Analyze | entropy-analyzer | Sonnet | Finds duplicate code, dead code, verbose patterns, over-abstraction |
| 3. Audit | safety-auditor | Sonnet | Validates each reduction is safe and performant |
| 4. Guard | ui-guardian | Haiku | Ensures zero UI/UX impact |

### Output

A structured reduction plan showing:
- Total LOC before and after
- Every proposed reduction with file, lines, savings, confidence, and risk level
- Performance and memory impact estimates
- Safety audit verdicts
- Confirmation of zero UI/UX changes

**Always starts in plan mode** — nothing is changed until you approve.

## Language Support

Works with any programming language. If the agents encounter an unfamiliar language, they research it before analyzing.

Never recommends changing the programming language.

## Model Usage

- **Haiku** for fast tasks (review, UI guard)
- **Sonnet** for deep analysis (entropy analysis, safety audit)
- **Never Opus** — cost-efficient by design

## Install

```
/plugin install entropy-reducer@your-marketplace
```

Or for local development:
```
claude --plugin-dir ./entropy-reducer
```
