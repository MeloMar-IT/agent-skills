# Prometheus SLO rules

Links:
- Prometheus 3 migration (le/quantile as floats): https://prometheus.io/docs/prometheus/latest/migration/
- Alerting on SLOs: https://sre.google/workbook/alerting-on-slos/

## Event populations
Numerator = denominator selector + one discriminating matcher. Bad status codes come from the contract (5xx bad, 4xx good: `code!~"5.."` for good).

## Latency SLIs
- Threshold must be an exact bucket boundary in the instrumentation. Read the bucket list in code.
- Missing: add the bucket, note history starts at deploy. A nearby boundary needs the owner's approval.
- good = `_bucket{le="T"}`, total = `_count` (or `le="+Inf"`), bad = total - good.
- Never `histogram_quantile` or averaged percentiles as a ratio SLI.

## Exact label strings
Prometheus 3 stores classic-histogram `le` and summary `quantile` as floats: `le="1"` is exposed as `le="1.0"`.
- An integer selector silently matches nothing after the upgrade, so short-window ratios are empty and alerts never fire.
- Long windows spanning the upgrade count good events only from the new period, so the budget looks spent.
- Rules whose window spans the change match both strings: `le=~"1|1\\.0"` (PromQL string escaping). Prometheus regexes are fully anchored; keep it tight so `10`, `0.1`, `2.5` do not match.
- Windows entirely after the change can use `le="1.0"`.

## Multiwindow multi-burn-rate
Burn = budget fraction x period / long window. Short = long/12. AND long with short at one threshold; OR the tiers.

| Period | 1h/5m | 6h/30m | 3d/6h |
|---|---|---|---|
| 28d | 13.44 | 5.6 | 0.933 |
| 30d | 14.4 | 6 | 1 |

Threshold in PromQL: `burn * (1 - SLO)`, e.g. `> (13.44 * 0.01)` for a 99% SLO.

```yaml
- alert: CheckoutBudgetBurnPage
  expr: slo:error_ratio_rate1h > (13.44 * 0.005) and slo:error_ratio_rate5m > (13.44 * 0.005)
```

- Ratio of sums: `sum(rate(bad)) / sum(rate(total))`, never `avg` of per-instance ratios. Keep matching `by` labels on both sides.
- Low traffic: add `and sum(rate(total[1h])) > N` or use longer windows.
- No data is not 100% good: guard with `absent()` or a data-presence alert.
- Run `promtool check rules` when installed.
