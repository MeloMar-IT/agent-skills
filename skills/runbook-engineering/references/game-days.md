# Game days

Use [assets/game-day-plan.md](../assets/game-day-plan.md). Every plan has a hypothesis, scope and blast radius, abort criteria, an observer and a rollback.

## Tabletop or live
- Tabletop: talk through the runbook with a scenario. Cheap, safe; finds unclear steps and missing access. Use first, and for destructive or production-only scenarios.
- Live: inject the failure in a staging environment, or in production with a small blast radius, a named abort owner and on-call informed. Use when the tabletop is clean and the step has never run for real.

## Run
1. Pick one runbook and one failure. State the hypothesis with a time.
2. Someone who did not write the runbook follows it literally; the author watches.
3. The observer records time per step, questions asked, deviations, steps that did not work.
4. Abort on any abort criterion; roll back by the written steps.

## Feed back
- List every defect with owner and due date.
- Update the runbook; set `last_reviewed` to the exercise date only if the walk-through covered the whole runbook, and set `status: needs-review` while fixes are open.
- Re-test fixed steps in the next exercise.
