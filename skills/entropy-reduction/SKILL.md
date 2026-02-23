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

Orchestrates a multi-agent workflow to analyze a codebase and find ways to achieve the same
functionality with less code — without changing UI/UX, switching languages, or introducing risk.

## When to Use

- User wants to reduce codebase size without changing behavior
- User wants to find and remove dead code
- User wants to consolidate duplicate logic
- User wants to simplify verbose patterns
- User wants a code reduction plan with LOC metrics

## How It Works

**Always invoke via the `/reduce-entropy` command**, which enters plan mode automatically.

### Agent Deployment Strategy

| Phase | Agent | Model | Purpose |
|-------|-------|-------|---------|
| 1. Familiarization | codebase-reviewer | **haiku** | Fast read-through, LOC counting, architecture mapping |
| 2. Analysis | entropy-analyzer | **sonnet** | Deep analysis of reduction opportunities |
| 3. Safety | safety-auditor | **sonnet** | Validate each change is safe and performant |
| 4. UI Guard | ui-guardian | **haiku** | Verify zero UI/UX impact |

**Never use opus.** Haiku for fast/simple tasks, sonnet for deep analysis.

### Language Agnostic

This skill works with any programming language. If the agents encounter an unfamiliar language,
they will use WebSearch to learn its syntax, idioms, and best practices before analyzing.

**Never recommend changing the programming language.** Reduce entropy within the existing stack.

### Output

The final deliverable is a structured plan showing:
- Total LOC before and after
- Every proposed reduction with file, line numbers, savings, confidence, and risk
- Performance/memory impact estimates
- Safety audit results
- Confirmation of zero UI/UX changes

The plan is presented to the user for approval before any changes are made.
