# Example: one outcome from a vague request

Request: "Thumbnails should be crisp. WebP would be nice. And it must be quick!"

```
## Context
Requested: a way to choose JPEG quality in the resizer (reported). The CLI has no quality flag today (observed in src/resize.py).

## Scope
- src/resize.py
- tests/test_resize.py

## Out of scope
- WebP output

## Acceptance criteria
1. `--quality N` (1-100) sets JPEG quality; no flag gives today's output.
2. `--quality 0` exits 2.

## Verification
- `python3 -m unittest tests.test_resize`
- `grep -q -e "--quality" src/resize.py`

## Unknowns
- Speed target for resizing: not stated.

Depends on: none
Risk: low
Approval: not required
Labels: none
```

Why: WebP is parked, speed sits in Unknowns instead of criteria, no label is proposed. The story's own tests must include the new `--quality` cases so the first check fails today.
