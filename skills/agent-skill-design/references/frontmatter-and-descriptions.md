# Frontmatter and descriptions

The description is the only text an agent sees when choosing a skill. Routing quality depends on it.

## Fields

- `name`: same as the folder; lower-case letters, digits, single hyphens; at most 64 characters.
- `description`: at most 1024 characters, one line, third person.
- Optional portable keys: `license`, `compatibility`, `metadata` (for example `capabilities: [..]`, `technologies: [..]`).

## Description recipe

1. Start with a verb in third person: "Resizes", "Renders", "Schedules".
2. Say what it does in a few concrete words.
3. "Use when" plus the words and file names users actually type.
4. End with "not for <other job> (use <neighbour>)", naming the nearest overlapping skill.
5. The neighbour's description names this skill back.

Avoid "I can ...", "you", "helps with", and vague nouns such as "helper", "utility", "tool".

## Before and after (image-resize and neighbours)

Before, for `image-resize`:

```
description: Image helper.
```

After:

```
description: Resizes and recompresses PNG and JPEG files with scripts/resize.py. Use when shrinking photos, making thumbnails of a given width, or batch-converting to WebP; not for cataloguing or tagging photos (use photo-catalog) or video frames (use video-thumbnails).
```

Neighbour `photo-catalog`, after:

```
description: Indexes photo folders by date, camera and tag. Use when sorting, tagging or searching a photo library; not for changing image size (use image-resize) or SVG files (use svg-icons).
```

## Before and after (calendar)

Before: `description: "I can help you with your calendar events and invites."`

After:

```
description: Creates and edits calendar events, invites and recurring rules in .ics files. Use when adding a meeting, moving an event across time zones or writing an RRULE; not for reading mail threads about meetings (use inbox-triage).
```

## YAML scalar notes

- A single-line plain or quoted value is the safest form for linters and other clients.
- A description containing `: ` or starting with a quote needs quoting. In single quotes a literal quote is doubled (`''`). In double quotes it is escaped as a backslash plus a quote.
- Long folded blocks (`>`) are read by most parsers, but a linter that reads line by line may see an empty value; prefer one line.

## Checks before you finish

- Does it start with a verb ending in "s"?
- Does it contain "Use when" and a "not for ... (use ...)" clause?
- Would a user's own phrasing ("shrink these photos") match its words?
- Is every neighbour you named a real skill, and does it name this one back?
