---
name: slo-engineering
description: "Writes, fixes and reviews SLOs as code: OpenSLO v1, Sloth and Pyrra specs, Prometheus SLI recording rules and multiwindow burn-rate alerts — target units per tool, good/bad event queries, histogram-bucket latency thresholds, exact label values, 28-day thresholds. Use when an SLO, SLI, error budget or burn-rate alert file or query is created, converted, debugged or reviewed; for incidents, postmortems or SLO policy use the sre skill."
metadata:
  version: 1
  capabilities: [slo, sli, error-budget, burn-rate-alerts, openslo, sloth, pyrra, latency-sli]
  technologies: [prometheus, promql, kubernetes]
---

# SLO engineering (SLOs as code)

Tool-level work only. SLI choice, budget policy, incidents and postmortems belong to the `sre` skill.

## Check these first

| Trap | Rule |
|---|---|
| Target units differ per tool | OpenSLO `target: 0.995` (or `targetPercent: 99.5`); Sloth `objective: 99.5`; Pyrra `spec.target: "99.5"` (quoted string); PromQL budget fraction `0.005` |
| Numerator not a subset of denominator | Same `job`, `handler`, `route` matchers in both; they differ only by the discriminating matcher |
| Wrong "bad" definition | Take it from the contract. 5xx bad, 4xx good: bad `code=~"5.."` or good `code!~"5.."`, never good `code=~"2.."` |
| Counting bad as good | Sloth `error_query` and OpenSLO `bad` count bad events; `good` counts good ones |
| Latency threshold not a bucket | `le` must be an existing bucket boundary in the instrumentation code; check the bucket list first |
| `histogram_quantile` as SLI | Never. Use good = `_bucket{le="T"}`, total = `_count` |
| Prometheus 3 `le="1"` is now `le="1.0"` | Short windows go empty; windows spanning the upgrade need both strings |
| Fixed range in Sloth | Always `[{{.window}}]`, never `[5m]` |
| Wrapping Pyrra metrics | Plain selectors only: no `sum`, `rate`, `increase`, `[5m]` |
| 28-day thresholds | 13.44, 5.6, 0.933 (not 14.4, 6, 1, which are for 30 days) |

## Workflow

1. Read the agreed SLO (README, ticket): target, window, population selectors, which results are bad. Do not change target, threshold or population without the owner.
2. Read the instrumentation (code, exposition, existing rules) for metric names, labels and bucket boundaries.
3. Write or fix the file using the tool reference:
   - [OpenSLO](references/openslo.md)
   - [Sloth](references/sloth.md)
   - [Pyrra](references/pyrra.md)
   - [Prometheus rules, latency, labels, burn rates](references/prometheus-slo-rules.md)
4. Latency threshold missing from the buckets: add the bucket to the instrumentation and say its history starts at deploy. Moving to a nearby boundary needs the owner's approval. Write the SLI against the new bucket.
5. Burn-rate alerts: burn = budget fraction x period / long window; short window = long/12; AND long with short at the same threshold, OR the tiers. 28 days: 13.44 (1h/5m), 5.6 (6h/30m), 0.933 (3d/6h). Thresholds in PromQL are `burn * (1 - SLO)`. Ratio of sums, not an average of ratios; same `by` labels both sides. Low traffic: add a minimum-event guard or use longer windows.
6. Budget sanity: no data is not 100% good; a rolling window regains budget as errors age out; a 100% target has no budget.
7. Verify against the instrumentation. Run `promtool check rules`, `sloth validate` or `oslo validate` if installed; never download tools. Report what you could not run.
