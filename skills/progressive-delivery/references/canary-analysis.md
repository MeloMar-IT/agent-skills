# Canary analysis

## Level and bounds

Use one level. Default one-sided 95% (z = 1.645, z² ≈ 2.706), because the gate asks only "is the canary worse?". If an organisation requires two-sided 95% (z = 1.96), recompute everything with that z.

Wilson bounds for e errors in n requests, p = e/n:

    (p + z²/2n ± z·√(p(1−p)/n + z²/4n²)) / (1 + z²/n)

With 0 errors the upper bound is z²/(n+z²), about 2.71/n. The exact Clopper–Pearson bound at the same level is 1 − 0.05^(1/n), about 3.0/n (rule of three). For 0 errors in 600 requests: Wilson 0.449%, exact 0.498%; Wilson at z = 1.96 gives 0.636%. Never quote "about 3/n" together with z = 1.96.

Wald (`p ± z·√(p(1−p)/n)`) is wrong here: at 0 errors the interval has zero width, so 0 errors in 50 requests "passes" a 0.1% limit.

## Comparing with a control

- Same definitions in both counts: same SLI, health checks and synthetic probes removed from both. Rate = errors / (requests − probes).
- Sample sizes may differ a lot (48k against 192k, 9000 against 1000). What must match is the definitions, not the size.
- Bound both rates. Newcombe hybrid score interval for d = p_canary − p_control, with Wilson (l, u) per rate:
  - upper = d + √((u₁−p₁)² + (p₂−l₂)²)
  - lower = d − √((p₁−l₁)² + (u₂−p₂)²)
- PASS if upper ≤ margin; FAIL if lower > margin; otherwise INCONCLUSIVE. No canary requests: INCONCLUSIVE.
- No ratio gate such as `canary <= 1.1 × control`: it fails whenever the control has zero errors.
- Using only the control's point estimate is acceptable only when the control is large. A small control (1 error in 1000) is noisy: bound it too.

Check: canary 0/400 against control 10/10000 is INCONCLUSIVE (Wald says PASS); canary 25/9000 against 0/1000 with margin 0.1% is INCONCLUSIVE (Wald says FAIL). Run `scripts/canary_stats.py compare 25 9000 0 1000 --margin 0.001`.

## Strata

When the canary's traffic mix differs from the control's (route, tenant, region), compare each stratum separately. A pooled rate can hide one bad route. A release fails if any stratum FAILs.

## Peeking

Checking the gate repeatedly and promoting at the first PASS raises the false-pass rate. Decide PASS only at the planned end of the bake. A FAIL may stop the step early.

## Bake time

- Minimum volume: smallest n where 0 errors passes your gate, z²(1−L)/L. L = 0.1%: 2704 requests with Wilson z = 1.645; 2995 with the exact bound. Script: `volume --limit 0.001`.
- Bake minutes = warm-up minutes + ⌈n / canary requests per minute⌉, never below a floor for slow effects (memory, caches, cron jobs). Warm-up is not analysed.
- 6000 rpm, 1% canary (60 rpm), L = 0.1%: 46 minutes plus 5 warm-up = 51. At 5%: 10 + 5 = 15. At 25%: 2 + 5 = 7, so the 10-minute floor applies. The rule of three gives 50 minutes of analysis at 1%.
- This is a floor that holds only when the canary has zero errors. Any error needs more volume: recompute from the observed counts.
- Check the plan against the gate in use. A rule-of-three plan paired with a Wilson z = 1.96 gate never reaches PASS in the planned time.
