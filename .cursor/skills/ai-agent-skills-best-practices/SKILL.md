---
name: ai-agent-skills-best-practices
description: Best practices for writing and using AI agent skills in Cursor. Use when authoring a new SKILL.md, improving an existing skill, trying to get better results from an existing skill, or when the user asks about skill structure, skill invocation, or how to work with Cursor agent skills effectively.
---

# AI Agent Skills — Best Practices

## What skills are

Skills are markdown files (`SKILL.md`) that give the agent specialized instructions for a task. The agent reads a skill when it judges it relevant, then follows the instructions inside. Skills live in:

| Scope | Path |
|-------|------|
| Personal | `~/.cursor/skills/<skill-name>/SKILL.md` |
| Project | `.cursor/skills/<skill-name>/SKILL.md` |

Never place skills inside `~/.cursor/skills-cursor/` — that directory is reserved for Cursor internals.

---

## Writing skills

### Description is the entry point

The `description` field in the YAML frontmatter is what the agent reads to decide whether to use the skill. Make it:

- **Third person** — it is injected into the system prompt, not shown to you.
- **Specific** — mention concrete nouns (file types, task names, tool names).
- **Trigger-inclusive** — list the user phrases that should activate it.

```yaml
# Good
description: >-
  Compile LaTeX .tex files to PDF using latexmk. Use when the user asks to
  compile TeX, build a PDF, or says changes are saved and wants a build.

# Bad — too vague
description: Helps with documents.
```

### Keep SKILL.md short (under 500 lines)

The context window is shared. Every line in a skill competes with conversation history and other tools. Ask of each paragraph: "Does the agent already know this?" If yes, cut it.

Put detailed reference material in a separate file and link to it:

```markdown
## Additional resources
- Full API reference: [reference.md](reference.md)
```

### Set the right degree of constraint

| Task type | Freedom level | Format |
|-----------|--------------|--------|
| Fragile, exact operations | Low | Runnable scripts + exact commands |
| Preferred patterns | Medium | Pseudocode or templates |
| Judgment-based tasks | High | Prose principles |

### Use examples for output quality

When output format matters, show a concrete before/after example rather than describing the format in prose. One good example beats three paragraphs of rules.

### Avoid time-sensitive content

Don't write "use the v2 API until March 2026". Use an `## Old patterns (deprecated)` section instead so the skill stays accurate without future edits.

---

## Using skills effectively

### Phrase your request to match the description

Skills are triggered by the agent matching your request to the skill description. If the skill isn't being picked up, use the exact nouns the description lists.

```
# If the skill says "Use when the user asks to compile TeX or build a PDF"
→ Say: "compile the TeX" or "build the PDF"
→ Not: "turn it into a document"
```

### Tell the agent the skill exists if it misses it

If you know a relevant skill exists and the agent doesn't invoke it, say so explicitly:

> "Use the add-references skill to look that up."

### Chain skills deliberately

For multi-step workflows, invoke skills in sequence rather than combining everything into one prompt. For example:

1. "Add the reference for [paper] using the add-references skill."
2. "Compile the file using the compile-tex-after-save skill."

Chaining makes each skill's scope clear and reduces ambiguity.

### Check skill output before accepting

Skills can execute shell commands or modify files. Before accepting changes:

- Review the diff in the editor.
- If the skill ran a build, check the terminal output for errors.

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Skill description is vague | Add specific trigger phrases and task names |
| SKILL.md exceeds 500 lines | Move reference content to `reference.md` |
| Skill not triggered | Rephrase request using terms from the description, or mention the skill by name |
| Skill does too many unrelated things | Split into two focused skills |
| Instructions assume outdated APIs | Use a deprecated section; avoid dates |
