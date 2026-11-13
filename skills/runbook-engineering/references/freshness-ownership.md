# Freshness and ownership

Report the two properties separately for each runbook: `stale` and `owned`.

## Freshness
- Interval in days: a repo policy or the runbook's own `review_interval_days` wins. Otherwise 90 for `severity: page`, 180 for everything else.
- Stale when (today minus `last_reviewed`) is greater than the interval. Exactly at the interval is not stale.
- A missing, unparseable or future date is stale.
- Use the date the user gives as "today"; otherwise the current date.
- A git commit date is not a review date. A review means someone walked the runbook against the current system. Do not infer `last_reviewed` from git or file times.

## Ownership
- Owned only when `owner` names a team that exists in the registry: teams file, CODEOWNERS or service catalog.
- A person, a placeholder (`TBD`, `none`, empty, missing) or a team not in the registry is unowned.
- A person on a team is still unowned: people leave; teams stay.

## Reporting
- A table: file, severity, age in days, interval, stale, owned, reason.
- If asked for a machine-readable file, use exactly the requested shape and keys.
- Fixing: assign owners through the team, never invent a team or date. Setting `status: needs-review` on stale runbooks is fine; do not bump `last_reviewed` without a real review.
