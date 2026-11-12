---
name: progressive-delivery
description: "Plans and checks progressive delivery: canary analysis with one-sided confidence bounds, canary bake time from request volume, percentage rollout bucketing, feature flags defaults and two-phase flag cleanup, and rollout gates. Use when code, config or plans for canaries, feature flags or staged rollouts change; for incidents, SLOs or broad change review use sre."
metadata:
  capabilities: [canary-analysis, canary-bake-time, percentage-rollout, feature-flags, flag-cleanup, rollout-gates]
---

# Progressive delivery

Mechanics of canaries, percentage rollouts, feature flags and rollout gates. Incidents, postmortems, SLOs and error budgets, change governance, schema migration (expand/migrate/contract) and the rollback-or-roll-forward decision belong to the `sre` skill (`skills/sre/references/changes.md`): use it for those.

| Task | Read |
| --- | --- |
| Canary verdict code, bounds, comparison with control, bake time | [canary-analysis.md](references/canary-analysis.md) |
| Percentage bucketing, flag defaults, flag cleanup | [feature-flags.md](references/feature-flags.md) |
| Step weights, warm-up, inconclusive results, mixed-version state | [rollout-gates.md](references/rollout-gates.md) |

## Rules that decide most tasks

1. **One confidence level everywhere.** Default: one-sided 95%, z = 1.645 (z² ≈ 2.706). Bounds are Wilson score bounds. Never Wald `p ± z·√(p(1−p)/n)`: with 0 errors its width is 0, so it passes any sample. With z = 1.96, recompute every number; never mix levels.
2. **Compare with a control using the Newcombe interval**, bounding both rates, on the same definitions (same SLI, probes and health checks removed from both). Sample sizes may differ. No ratio gates (`canary <= 1.1 * control` fails when control has 0 errors). Verdict: PASS if upper bound ≤ margin, FAIL if lower bound > margin, else INCONCLUSIVE. No requests is INCONCLUSIVE.
3. **Bake time comes from volume.** Smallest n where 0 errors passes your own gate is z²(1−L)/L: for L = 0.1% that is 2704 requests (exact bound: 2995). Bake minutes = warm-up + ⌈n / canary requests per minute⌉, never below the floor. At 6000 rpm and 1%: 46 minutes plus warm-up. This is a floor that holds only with 0 errors; check that 0 errors at the planned volume PASSes the gate actually in use.
4. **Decide PASS only at the planned end of the bake.** Peeking and promoting on the first PASS raises false passes. FAIL may stop early.
5. **Bucketing is a stable hash**, `sha256(flag_key:salt:unit_id)` mod 10000, on iff `bucket < round(percent * 10000)`. Never Python `hash()`, never per-request randomness, never `percent * 100` in floats (0.07 × 100 = 7.000000000000001). Salt per flag. A missing unit id is never hashed: it gets the documented fallback, never another unit's id.
6. **Two-phase flag cleanup** is needed exactly when production serves a value that differs from what a missing key evaluates to (check each reader's own default argument, and keys built from strings: a killed flag read with `default=True` still needs its `false` definition). Then: phase 1 hard-codes the served behaviour and keeps the definition; phase 2 deletes the definition after every reader runs phase-1 code. Otherwise remove code and definition together. Record phase 2 in the follow-up list.
7. **INCONCLUSIVE is not PASS.** Extend once, then hold, escalate or roll back.

## Numbers come from the script

`scripts/canary_stats.py` (standard library, offline) has `bound`, `compare`, `volume`, `bake` and `wald`. Run it to get bounds and plans instead of computing by hand. Copy the formulas into the project; never import the script from project code.
