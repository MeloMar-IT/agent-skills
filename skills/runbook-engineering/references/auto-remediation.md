# Auto-remediation guardrails

## What to automate
Only steps that were proven by hand, are idempotent and low-risk. Never automate data destruction. Anything that needs judgment stays a human step.

## Rules for the script
1. Dry run by default: print the plan, change nothing. State changes need `--execute`.
2. `--max-targets N` caps the blast radius. If candidates exceed N, act on none, print why, exit non-zero and let a human decide. Never cut the list to the first N.
3. Select candidates from live state (for example `get pods -o json`) and filter with every condition of the runbook step (label, status, threshold). Re-select right before acting, not from an earlier listing.
4. Act one target at a time. Stop at the first failed action; no blind retries, no continuing with the rest.
5. Exit 0 only when the work is complete or it was a dry run. Anything else (cap exceeded, failed action, selection error, partial) exits non-zero so the alert pipeline escalates.
6. Log the plan and every action and result to stdout/stderr, with target names.
7. Kill switch and rate limiting belong to the scheduler or alert pipeline. Do not add hidden local state (lock files, counters) unless asked.
8. Use only the tool the task names; parse its structured output (JSON), not human text. Name the target (context, namespace) on every call.

## Shape
```
cands = select()                       # live state, all filters
if len(cands) > cap: log; exit 2       # act on none
log plan
if not execute: exit 0
cands = select()                       # re-select
if len(cands) > cap: log; exit 2
for t in cands:
    if not act(t): log; exit 1         # stop at first failure
exit 0
```

## Other tools
- Ansible: `serial: 1` (or a small number), `max_fail_percentage: 0`, `--check` for the dry run, `any_errors_fatal: true`.
- Rundeck: `keepgoing: false`, thread count 1, a dry-run option defaulting to true, node filter that is explicit (never `.*`).
- Kubernetes: PodDisruptionBudgets limit voluntary disruption; they do not stop `delete` of an unhealthy pod, so keep the cap in the script as well.

Version note: flag names differ between tool versions; check `--help` of the installed one.
