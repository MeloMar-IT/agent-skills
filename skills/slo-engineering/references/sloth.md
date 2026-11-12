# Sloth (prometheus/v1)

Docs: https://sloth.dev

Minimal valid spec:

```yaml
version: "prometheus/v1"
service: "search"
slos:
  - name: "requests-availability"
    objective: 99.9
    sli:
      events:
        error_query: sum(rate(search_requests_total{job="search",route="/search",code=~"5.."}[{{.window}}]))
        total_query: sum(rate(search_requests_total{job="search",route="/search"}[{{.window}}]))
    alerting:
      name: SearchAvailability
      page_alert:
        labels: {severity: page}
      ticket_alert:
        labels: {severity: ticket}
```

Rules:
- Top level: `version`, `service`, `slos[]`; each SLO has `name` and `objective` (percent number, `99.5`).
- `sli.events.error_query` counts BAD events; `total_query` counts all events. Alternative: `sli.raw.error_ratio_query`, which must return a ratio.
- Every range selector is `[{{.window}}]`, never a fixed `[5m]`.
- Alerts live in `alerting.page_alert` and `alerting.ticket_alert`.
- Default period is 30 days. A 28-day SLO needs the generator's period option (`--default-slo-period=28d`, or set in the spec's SLO period setting); check how the repo runs the generator.

Latency SLI, threshold 0.3 s with bucket `0.3` present:

```yaml
error_query: |
  sum(rate(search_request_duration_seconds_count{job="search",route="/search"}[{{.window}}]))
  -
  sum(rate(search_request_duration_seconds_bucket{job="search",route="/search",le="0.3"}[{{.window}}]))
total_query: sum(rate(search_request_duration_seconds_count{job="search",route="/search"}[{{.window}}]))
```
