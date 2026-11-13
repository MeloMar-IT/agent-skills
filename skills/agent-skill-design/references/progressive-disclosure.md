# Progressive disclosure

Three layers load at different times: name and description (always), SKILL.md body (when the skill triggers), references, scripts and assets (only when the body says to read or run them). Put each fact in the cheapest layer that still reaches the agent when it matters.

## What stays in SKILL.md

- The workflow, in order.
- Must-rules: "always", "never", "needs", ordering constraints, side-effect guards.
- Decision rules: when to choose A over B.
- A link line per reference saying when to read it.

## What moves to references/

Flag tables, error catalogues, long examples, history, lookup data. About 500 lines per file is an upper limit; far below it is better.

## Splitting a long file: procedure

1. List every section and classify it: workflow, must-rule, lookup, trivia.
2. Scan the whole file, especially the end, for must-rules. Lines like "Always ...", "Never ...", "X needs Y" often sit in a "Notes" section among trivia. Copy those into SKILL.md first, as short bullets.
3. Move each lookup section into its own file under `references/` (flat, no subfolders). Give files names that say what they hold.
4. Link each from SKILL.md: "Read [references/x.md](references/x.md) when ...".
5. Verify nothing was lost: every ID, table row and flag appears somewhere in SKILL.md plus the references, counted across both. A few critical IDs may stay in SKILL.md; the rest may live in references. Compare counts before and after.
6. Keep frontmatter unchanged unless asked.

## Worked example: a calendar skill

Before: one `SKILL.md` with the workflow, a 40-row time-zone table, a 30-recipe RRULE cookbook and a "Notes" section at the end:

```
## Notes
- Always store event times in UTC with the original zone name.
- Never edit an event that has an ORGANIZER you do not own.
- COUNT and UNTIL cannot both appear in one RRULE.
```

After:

- `SKILL.md`: workflow plus those three notes as must-rules, and two link lines.
- `references/timezones.md`: the time-zone table.
- `references/rrule-cookbook.md`: the recipes.

A plain split that moves the whole "Notes" section out hides the three rules from every run. Moving them up is the point.

## Reference hygiene

- One level deep: SKILL.md links references; references do not link other references.
- No unlinked reference files.
- Do not duplicate the same table in two places.
