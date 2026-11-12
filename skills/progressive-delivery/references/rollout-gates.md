# Rollout gates

- Every step has a weight, a warm-up period that is not analysed, a bake time and a gate. The last step (weight 1.0) needs no bake.
- Bake time per step comes from request volume at that weight (see canary-analysis.md), not round numbers.
- Before the planned end of the bake: FAIL on any route rolls back; otherwise keep waiting, even if the gate already says PASS.
- INCONCLUSIVE at the end of a bake: extend once, up to a cap computed from the observed rate and volume. After that, hold and escalate, or roll back. Never promote because there is "no evidence of harm".
- Route canary traffic sticky per user or session, so one user does not flip between versions.
- A canary is a mixed-version state. Before step 1, check that old and new versions can read each other's shared state (queues, caches, database). Use the `sre` skill (`references/changes.md`) for expand/contract and for the rollback-or-roll-forward decision: roll back only if the old version can read the new state.
- Tool mapping: Argo Rollouts, Flagger and similar controllers express these as steps, pauses and analysis templates; the rules above stay the same.
