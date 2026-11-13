# Game day plan: <name>

- Date, duration, type: tabletop | live
- Hypothesis: When <failure> happens, <expected behaviour> within <time>.
- Runbooks under test (path, owner):
- Scope and blast radius (environment, services, users affected; why acceptable):
- Preconditions (backups, on-call informed, no other change running):
- Steps (inject, observe, expected signal):
- Abort criteria (any one stops the exercise; who decides):
- Observer (records times, deviations, unclear steps; does not fix):
- Rollback (exact steps to restore, who runs them):

## Outcome
- Hypothesis held? yes | no
- Runbook defects found (step, problem, fix owner, due date):
- Runbooks walked through: set `last_reviewed` to the exercise date and `status` to `active`, or `needs-review` while fixes are open.
