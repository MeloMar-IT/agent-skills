# claude-skills

A library of agent skills. Each skill is a folder in `skills/` with a `SKILL.md`.

## Install in Claude Code

```
/plugin marketplace add MeloMar-IT/claude-skills
/plugin install claude-skills@claude-skills
```

After pushing changes: `/plugin marketplace update`.

## Add a skill

1. Create `skills/<name>/SKILL.md` with `name` and `description` frontmatter.
2. Put long reference material in `skills/<name>/references/`.
3. Commit and push.
