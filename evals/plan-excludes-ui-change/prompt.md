---
description: Plan-only run on the fixture keeps the two render functions, whose markup differs, out of the apply set.
runs: 1
max_turns: 80
timeout_seconds: 1800
allowed_tools: [Read, Glob, Grep, Skill, Agent, TodoWrite]
---

/entropy-reducer:reduce-entropy . --plan-only
