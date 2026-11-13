# Readiness triage

Check in this order; the first failure decides, and the reason names it.

1. Template: all sections and the four closing lines present.
2. No `TBD`, no open Unknown, no "to be decided".
3. Every Verification entry is offline and deterministic, and would run correctly: read each command, including grep patterns starting with `-` without `-e`/`--` (exit 2 whatever the work).
4. File count in Scope within the repo limit.
5. High risk: `Approval:` records an approval already given by the owner of the affected system (as listed in the owner file; a different listed owner does not count), with a date. `pending` fails.

Low risk with `Approval: not required` passes step 5. Ready means the text is complete; a person still reviews and sets the label. Output exactly what was asked (for example JSON keyed by issue number with `ready` and a short `reason`).
