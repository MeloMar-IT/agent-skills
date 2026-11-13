# Story anatomy

| Section | Holds | Common mistake |
|---|---|---|
| Context | Why, who asked, known facts with evidence labels | Inventing usage numbers |
| Scope | One bullet per file path | Naming a directory or "the code" |
| Out of scope | Requested extras, later work | Leaving extras in Scope |
| Acceptance criteria | Numbered observable results | Vague words, time units not given |
| Verification | One backticked command per check | Manual checks, network, clocks |
| Unknowns | Open questions, each marked | Guessing to look complete |

Closing lines: `Depends on:`, `Risk:`, `Approval:`, `Labels:`.

## Handling vague requests

Request: "Thumbnails look dull. Make them better, and maybe WebP someday."

- Outcome: a `--quality N` flag in `src/resize.py`. Scope: `src/resize.py`, `tests/test_resize.py`.
- Out of scope: WebP output.
- Unknowns: the valid range of N if not stated; what "better" means.
- Criteria: `--quality 50` writes a JPEG smaller than the `--quality 95` output for the same input; no flag keeps today's bytes.
- "Dull" and "better" are not criteria; park them under Unknowns.

## Rules of thumb

- A number you were not given does not appear. Write "target not stated" under Unknowns.
- If the request implies two outcomes, write two stories (see splitting.md).
- Keep prose short; the Foundry reads the whole text and acts on it literally.
