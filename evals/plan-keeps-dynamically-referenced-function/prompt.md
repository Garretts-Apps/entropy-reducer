---
description: Plan-only run on the fixture never proposes removing export_ndjson, which is reached only through getattr.
runs: 1
max_turns: 80
timeout_seconds: 1800
allowed_tools: [Read, Glob, Grep, Skill, Agent, TodoWrite]
---

/entropy-reducer:reduce-entropy . --plan-only
