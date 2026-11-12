# Pyrra

Docs: https://github.com/pyrra-dev/pyrra

Minimal valid ratio SLO:

```yaml
apiVersion: pyrra.dev/v1alpha1
kind: ServiceLevelObjective
metadata:
  name: orders-availability
  namespace: monitoring
spec:
  target: "99.5"
  window: 28d
  indicator:
    ratio:
      errors:
        metric: http_requests_total{job="orders",handler="/api/orders",code=~"5.."}
      total:
        metric: http_requests_total{job="orders",handler="/api/orders"}
```

Rules:
- `spec.target` is a quoted percent string. The CRD field is a string; an unquoted number is rejected.
- Ratio: `indicator.ratio.errors.metric` and `total.metric`. Latency: `indicator.latency.success.metric` and `total.metric` (success = `_bucket{le="T"}`, total = `_count`).
- Metrics are plain counter selectors. Never `sum`, `rate`, `increase` or a `[5m]` range: Pyrra adds them.
- Errors selector = total selector plus the discriminating matcher.
- `grouping` gives one SLO per label value.
- Latency `le` must match the exposed string exactly (see prometheus-slo-rules.md).
