# OpenSLO v1

Spec: https://github.com/OpenSLO/OpenSLO

Minimal valid SLO (availability, rolling 28 days):

```yaml
apiVersion: openslo/v1
kind: SLO
metadata:
  name: checkout-availability
spec:
  service: checkout
  indicator:
    metadata:
      name: checkout-success
    spec:
      ratioMetric:
        counter: true
        bad:
          metricSource:
            type: Prometheus
            spec:
              query: sum(http_requests_total{job="checkout",handler="/api/checkout",code=~"5.."})
        total:
          metricSource:
            type: Prometheus
            spec:
              query: sum(http_requests_total{job="checkout",handler="/api/checkout"})
  timeWindow:
    - duration: 28d
      isRolling: true
  budgetingMethod: Occurrences
  objectives:
    - displayName: Checkout requests succeed
      target: 0.995
```

Rules:
- An inline `indicator` has its own `metadata.name` and `spec.ratioMetric`; or use `indicatorRef`.
- `ratioMetric`: `counter`, exactly one of `good` or `bad`, and `total`. Each is `metricSource` with `type` and `spec.query`.
- `target` is a fraction in [0,1) (`0.995`); `targetPercent: 99.5` is the percent alternative. Never `target: 99.5`.
- `timeWindow` is a list with one item: `duration` + `isRolling: true`, or a `calendar` with `startTime` and `timeZone`.
- `budgetingMethod`: `Occurrences`, `Timeslices` or `RatioTimeslices`. Timeslice methods need `timeSliceWindow`; `Timeslices` also needs `timeSliceTarget` (`RatioTimeslices` has no per-slice target) in the objective.
- Numerator and `total` use the same population selectors.
