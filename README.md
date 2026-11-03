# agent-skills

A tool-agnostic library of agent skills. Each skill is a folder in `skills/` with a `SKILL.md`
(plain Markdown with `name` and `description` frontmatter), so any LLM agent that reads the
Agent Skills format, or can be pointed at the files, can use them.

## Use with other tools

Copy or symlink the folders in `skills/` into the tool's skills directory (for example
`~/.claude/skills/`, `~/.codex/skills/`), or load the `SKILL.md` text as instructions.

## Install in Claude Code

```
/plugin marketplace add MeloMar-IT/agent-skills
/plugin install agent-skills@agent-skills
```

After pushing changes: `/plugin marketplace update`.

## Add a skill

1. Create `skills/<name>/SKILL.md` with `name` and `description` frontmatter.
2. Put long reference material in `skills/<name>/references/`.
3. Commit and push.
