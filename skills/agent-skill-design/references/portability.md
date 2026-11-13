# Portability

Port a skill only when asked to run it on another client. A skill that stays on one client keeps that client's keys.

## Portable keys

`name`, `description`, `license`, `compatibility`, `metadata`. `allowed-tools` is experimental in the open spec and clients handle it differently, so treat it as non-portable: describe the tool limits in the body too.

## Client-only keys: what to do when porting

Move each key's intent into the body, then remove the key. Never drop a side-effect guard without a replacement. Lint with `python3 scripts/check_skill.py <skill-folder> --portable`: without that flag KEY-CLIENT is only a WARN.

| Key | Intent | Rewrite in the body |
|---|---|---|
| `disable-model-invocation: true` | The model must not start the skill on its own | Must-rule: "Run only when the user explicitly asks for it." Put it first in the body, and add "Confirm before any step with side effects." |
| `user-invocable: false` | Only the model loads it, not a slash command | Sentence: "This skill is background knowledge for other skills; do not offer it as a command." |
| `argument-hint: [file]` | What argument the user gives | Section "Input": "The user gives `<file>`; ask for it if missing." |
| `model: <name>` | Preferred model | Sentence in the body naming the needed capability (for example "needs strong long-context reading"), no model name. |
| `allowed-tools: ...` | Tool limits | Must-rule: "Use only: <tools>." plus the reason. |

## Steps

1. List the frontmatter keys; mark each as portable or client-only.
2. For each client-only key, write its rewrite from the table into the body.
3. Remove the key only after the rewrite exists.
4. Run the linter with `--portable`; fix every ERROR.
5. Keep behaviour unchanged: same workflow, same guards.

## Example

Before (Claude Code only):

```
---
name: calendar-purge
description: Deletes cancelled events from .ics files. Use when cleaning a calendar export; not for editing live events (use calendar-events).
disable-model-invocation: true
---
```

After porting: the key is gone and the body starts with "Run only when the user explicitly asks for it. Show the list of events to delete and wait for confirmation before deleting."
