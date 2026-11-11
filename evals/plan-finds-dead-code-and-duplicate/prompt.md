---
description: Plan-only run on the fixture puts the dead function and the duplicate helper in the apply set.
runs: 1
max_turns: 80
timeout_seconds: 1800
allowed_tools: [Read, Glob, Grep, Skill, Agent, TodoWrite]
---

/entropy-reducer:reduce-entropy . --plan-only
