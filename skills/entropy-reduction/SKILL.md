---
name: entropy-reduction
description: |
  Use this skill when the user mentions "reduce entropy", "simplify code", "reduce code",
  "less code", "code reduction", "remove dead code", "deduplicate", "consolidate code",
  "code cleanup without changes", or wants to achieve the same functionality with fewer
  lines of code. Also applies when user says "entropy reducer" or "reduce-entropy".
---

# Entropy Reduction Skill

## What This Skill Does

Orchestrates a multi-agent workflow that finds ways to get the same observable behavior from
less code — without changing UI/UX, switching languages, adding dependencies, or taking
unverified risks — and applies only what survives an independent audit.

## When to Use

- The user wants a smaller codebase with identical behavior
- The user wants dead code found and removed
- The user wants duplicate logic consolidated
- The user wants verbose patterns simplified
- The user wants a reduction plan with line-count metrics

Not for: feature work, bug fixes, performance tuning, restyling, or framework migrations.

## How It Works

**Run the `/reduce-entropy` command** — it holds the full workflow and enters plan mode first.

```
/reduce-entropy [path] [--plan-only] [--types dead-code,duplicate,...] [--include-caution]
```

| Phase | Agent | Model | Purpose |
|-------|-------|-------|---------|
| 0. Preflight | orchestrator | sonnet | Scope files, pick one line-count method, detect tests and tooling, shard |
| 1. Familiarization | codebase-reviewer | **haiku** | Map each shard: inventory, public surface, leads |
| 2. Analysis | entropy-analyzer | **sonnet** | Find reductions per shard, plus one cross-shard pass — each with evidence |
| 3. Audit | safety-auditor | **sonnet** | Independently re-verify every finding; APPROVED / CAUTION / REJECTED |
| 4. UI guard | ui-guardian | **haiku** | Clear only changes with no observable UI/UX effect |
| 5. Plan | orchestrator | sonnet | Present the apply set, opt-in list, and exclusions for approval |
| 6. Apply | orchestrator | sonnet | Baseline, apply one finding at a time, verify, revert on regression |

**Never use opus.** Haiku for fast passes, sonnet for analysis and audit.

## Principles

- **Evidence or exclusion.** Every finding carries proof — a repo-wide reference search, a
  diff of the duplicates, an edge-case walk-through. No proof, no plan entry.
- **Two sets of eyes.** The auditor re-derives the evidence rather than trusting the analyzer,
  and rejects findings whose cited lines no longer match the file.
- **Observable behavior is the contract.** Same outputs, errors, side effects, public API, and UI.
- **Fewer lines is the measurement, not the goal.** No code golf, no deleting tests, comments,
  error handling, or logging to move the number.
- **The user's work is protected.** Nothing changes before approval; a dirty working tree is
  surfaced before applying; nothing is committed.
- **Language-agnostic, language-faithful.** Agents research unfamiliar languages before
  analyzing, and never recommend changing the language, framework, or build system.

## Output

Before approval — a plan showing scope and line count (with the counting method), the apply
set with per-finding evidence, CAUTION findings as opt-in, everything excluded and why, and
the exact commands that will verify the result.

After approval — which findings were applied, which were reverted and why, the measured
before/after line count against the projection, and the verification status against the
pre-change baseline.
