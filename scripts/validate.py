#!/usr/bin/env python3
"""Validate the entropy-reducer plugin layout. Stdlib only.

Checks the invariants that break silently when edited by hand:
  * manifests parse, plugin.json / marketplace.json agree on the name, and the
    version is declared once (plugin.json)
  * every agent has frontmatter whose name matches its filename, a description,
    a pinned model from the allowed set, and a tools list
  * the reduce-entropy skill (the whole workflow) has the frontmatter Claude
    Code needs, and no stale command or pointer skill sits beside it
  * every agent is dispatched by the skill
  * the README documents /reduce-entropy and every agent, and the changelog
    has an entry for the current version

Exit 0 when everything holds, 1 otherwise.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALLOWED_MODELS = {"haiku", "sonnet"}  # the plugin's "never opus" rule
errors = []


def fail(msg: str) -> None:
    errors.append(msg)


def frontmatter(path: Path) -> dict:
    """Top-level keys of a leading `---` block. Block scalars keep their text."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        fail(f"{path.relative_to(ROOT)}: missing frontmatter")
        return {}
    fields, key = {}, None
    for line in m.group(1).splitlines():
        top = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if top:
            key = top.group(1)
            value = top.group(2).strip()
            fields[key] = "" if value in ("|", ">", "|-", ">-") else value.strip("\"'")
        elif key and line.strip():
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields


def load_json(rel: str) -> dict:
    try:
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        fail(f"{rel}: {e}")
        return {}


def main() -> int:
    plugin = load_json(".claude-plugin/plugin.json")
    market = load_json(".claude-plugin/marketplace.json")
    entries = market.get("plugins") or [{}]
    entry = entries[0]
    for field in ("name", "version"):
        if not plugin.get(field):
            fail(f"plugin.json: missing {field}")
    if plugin.get("name") != entry.get("name"):
        fail(f"name mismatch: plugin.json={plugin.get('name')!r} "
             f"marketplace.json={entry.get('name')!r}")
    # The version lives in plugin.json only. When the marketplace entry
    # repeats it, Claude Code silently uses plugin.json and the two drift.
    if "version" in entry:
        fail("marketplace.json: remove `version` from the plugin entry; plugin.json owns it")
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(plugin.get("version", ""))):
        fail(f"plugin.json: version {plugin.get('version')!r} is not semver")

    agents = {}
    for path in sorted((ROOT / "agents").glob("*.md")):
        fm = frontmatter(path)
        rel = path.relative_to(ROOT)
        agents[path.stem] = fm
        if fm.get("name") != path.stem:
            fail(f"{rel}: name {fm.get('name')!r} does not match filename")
        if not fm.get("description"):
            fail(f"{rel}: empty description")
        elif len(fm["description"]) > 300:
            fail(f"{rel}: description is {len(fm['description'])} chars (max 300); "
                 "agent descriptions are loaded into every session")
        if fm.get("model") not in ALLOWED_MODELS:
            fail(f"{rel}: model {fm.get('model')!r} not in {sorted(ALLOWED_MODELS)}")
        if not fm.get("tools"):
            fail(f"{rel}: no tools list")
        elif re.search(r"\b(Edit|Write|MultiEdit|NotebookEdit)\b", fm["tools"]):
            fail(f"{rel}: analysis agents must stay read-only, found a write tool")
    if not agents:
        fail("agents/: no agents found")

    skill_rel = "skills/reduce-entropy/SKILL.md"
    skill_path = ROOT / skill_rel
    skill = skill_path.read_text(encoding="utf-8") if skill_path.is_file() else ""
    if not skill:
        fail(f"{skill_rel} missing")
    else:
        fm = frontmatter(skill_path)
        # The directory name is the invocation name: /entropy-reducer:reduce-entropy.
        if fm.get("name") != skill_path.parent.name:
            fail(f"{skill_rel}: name {fm.get('name')!r} does not match its directory")
        for field in ("description", "allowed-tools"):
            if not fm.get(field):
                fail(f"{skill_rel}: missing {field}")
        if len(fm.get("description", "")) > 250:
            fail(f"{skill_rel}: description is {len(fm['description'])} chars (max 250); "
                 "skill descriptions are loaded into every session")
        for tool in ("EnterPlanMode", "ExitPlanMode"):
            if tool not in fm.get("allowed-tools", ""):
                fail(f"{skill_rel}: allowed-tools lacks {tool}")
        if fm.get("model") not in ALLOWED_MODELS:
            fail(f"{skill_rel}: model {fm.get('model')!r} not allowed")
        # README promises natural-language triggering, so the model must be
        # able to invoke the skill.
        if fm.get("disable-model-invocation", "false").lower() == "true":
            fail(f"{skill_rel}: disable-model-invocation must stay off")
        for name in agents:
            if name not in skill:
                fail(f"agent {name} is never dispatched by the skill")

    # The workflow lives in the skill only; a leftover command or pointer
    # skill would register a second, diverging /reduce-entropy.
    for stale in ("commands/reduce-entropy.md", "skills/entropy-reduction"):
        if (ROOT / stale).exists():
            fail(f"{stale}: remove it; the workflow lives in {skill_rel}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for needle in ["/reduce-entropy", *agents]:
        if needle not in readme:
            fail(f"README.md does not mention {needle}")
    changelog = ROOT / "CHANGELOG.md"
    if plugin.get("version") and (
            not changelog.is_file()
            or f"## {plugin['version']}" not in changelog.read_text(encoding="utf-8")):
        fail(f"CHANGELOG.md has no entry for {plugin['version']}")

    for e in errors:
        print(f"FAIL  {e}")
    if errors:
        return 1
    print(f"OK    entropy-reducer {plugin['version']}: "
          f"{len(agents)} agents, 1 skill")
    return 0


if __name__ == "__main__":
    sys.exit(main())
