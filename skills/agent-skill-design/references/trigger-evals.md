# Trigger evals

Trigger evals test the description: given a user query and the library's skills, should this skill load?

## Format

`evals/triggers.json`, a JSON list:

```json
[
  {"query": "shrink these product photos to 800px wide", "should_trigger": true},
  {"query": "tag my holiday photos by camera model", "should_trigger": false}
]
```

Each entry has a string `query` and a boolean `should_trigger`.

## Rules

- Realistic phrasings, the way users talk: file names, typos of habit, short and long forms.
- Roughly balanced positives and negatives, at least eight of each for a skill with several neighbours.
- Some positives never use the skill's own name or its main keyword (paraphrases).
- Negatives are near-misses: they share keywords with the skill but belong to a named neighbour. Cover every neighbour with at least one. An unrelated query ("what is the weather") proves nothing.
- No duplicates, ignoring case.
- Run the set before and after every description change and compare.
- Do not copy queries from the examples in other documents into the evals of the skill they came from; examples and evals should not leak into each other.

## Worked example: a calendar skill with neighbours

Skill `calendar-events`; neighbours `inbox-triage` (mail), `task-board` (to-dos), `spreadsheet-sync` (sheets).

```json
[
  {"query": "move Thursday's design review to 3pm Berlin time", "should_trigger": true},
  {"query": "add a weekly standup on Mondays, ends after 10 times", "should_trigger": true},
  {"query": "write an RRULE for the last Friday of every month", "should_trigger": true},
  {"query": "summarise the mail thread about the calendar invite", "should_trigger": false},
  {"query": "turn tomorrow's calendar meetings into to-do cards", "should_trigger": false},
  {"query": "export my calendar events into a spreadsheet tab", "should_trigger": false}
]
```

Each negative shares "calendar" or "event" with the skill and is owned by one neighbour.

## Reading results

- A negative that triggers: add a "not for ... (use <neighbour>)" clause or sharpen the verbs.
- A positive that does not trigger: add the user's words to "Use when".
- Change one thing, re-run, compare.
