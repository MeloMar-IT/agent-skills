# Observability and actionable alerting

## Contents

- [Start from a question](#start-from-a-question)
- [Build and validate the evidence](#build-and-validate-the-evidence)
- [Metrics and queries](#metrics-and-queries)
- [Logs, traces, and profiles](#logs-traces-and-profiles)
- [Alert policy](#alert-policy)
- [Investigate the monitoring system](#investigate-the-monitoring-system)
- [Deliverable and sources](#deliverable-and-sources)

## Start from a question

Identify the decision the operator or service owner needs to make. For each panel, alert, or query, state the question, signal, population, time window, baseline, and what action an answer changes. Avoid a wall of every available metric.

Use the existing stack where suitable: Prometheus/Grafana, OpenTelemetry, Loki/Tempo/Pyroscope, Elastic, Dynatrace, Zabbix, Azure Monitor, or a provider equivalent. Discover metric/log schemas, instrumentation versions, permissions, and retention before proposing exact queries. Do not invent metric names or assume a tool proves causality.

Use black-box evidence for the experienced outcome and white-box evidence for the mechanism. Examine the four golden signals—latency, traffic, errors, saturation—then use request rate/errors/duration for a service and utilization/saturation/errors for a resource when those views help. Include correctness, freshness, and durability evidence where the journey requires them.

Organize a service view around user impact and SLO/budget, then affected cohorts and dependencies, then diagnostic detail. Preserve links to runbooks, changes, incident history, and service ownership. Label units and sample size. Put a visible freshness indicator on data that can silently stop updating.

## Build and validate the evidence

1. Map the user operation through client, edge, proxy, service, queues, stores, and third parties. Mark which attempts each signal misses and which retries it counts.
2. Check collection/ingestion delay, scrape interval, aggregation, downsampling, clock offsets, retention, and access filtering. Preserve the query and evaluation interval alongside a screenshot.
3. Compare baseline, failure, and recovery intervals, plus unaffected cohorts. Normalize workload, release version, geography, tenancy, and cache state before inferring a change effect.
4. Correlate signals with request/trace IDs or stable resource IDs when available. A correlation is a lead; test the suspected mechanism.
5. Check monitoring overhead and failure isolation. Instrumentation must not create an outage or expose credentials, personal data, prompt bodies, or business payloads.

If no relevant data exists, return a ranked instrumentation gap with the decision it prevents, the smallest useful addition, and its cost/privacy implications. Do not manufacture a dashboard or claim a diagnostic succeeded without data.

## Metrics and queries

Define units, label sets, sampling scope, and metric semantics first. Use counters for cumulative events, gauges for instantaneous state, and appropriate distributions for latency or size. Check resets and stale series. With Prometheus counters, apply `rate` before aggregating instances so resets are handled within each series.

The following is illustrative PromQL only. Replace metric names, labels, and error semantics from the observed schema before use:

```promql
sum(rate(service_requests_total{service="checkout",outcome="bad"}[5m]))
/
sum(rate(service_requests_total{service="checkout"}[5m]))
```

Both numerator and denominator must describe the same eligible event population. Missing `bad` series can mean zero errors or missing instrumentation; establish the exporter contract before filling values. A zero denominator is no traffic, not proof of health. Handle absent series and stale collection separately. Do not indiscriminately `clamp_min` denominators or replace every missing result with zero.

For classic histograms, aggregate compatible buckets with the `le` label preserved before calculating a quantile. Do not average per-instance p95/p99, mix incompatible buckets, or discard slow requests through sampling. For native histograms, verify server, client, remote storage, and query support for the actual versions. Consider distribution error and bucket resolution around the SLO threshold. Use a threshold success ratio directly when that is the defined SLI.

Inspect per-cohort trends before broad aggregation. Use bounded labels such as known service and region; avoid arbitrary user IDs, full URLs, request IDs, or error strings as metric labels. Estimate active-series growth before changing cardinality. Review recording rules for evaluation cost, correctness, data lag, and ownership.

## Logs, traces, and profiles

Give telemetry an explicit operational, user-experience, security, audit, or recovery purpose. Define retention, sampling, access, and cost accordingly. Reduce unnecessary collection while preserving useful normal baselines and the surrounding context needed to investigate failures; an event without an error marker is not automatically worthless.

For real-user monitoring, session replay, and client capture, establish approved scope, field masking, minimization, access, and retention before collection. Synthetic journeys that submit forms or invoke business APIs need controlled identities/data, bounded rates, and cleanup or reconciliation for their side effects. Keep low-rate journey probes distinct from load generation and failure injection. Measure collection, ingestion, evaluation, and notification delay rather than describing the entire path as "real time" without evidence. These additions operationalize the supplied ebook's chapters 7 and 13; see [the source map](essential-sre-insights.md).

| Signal | Use it to answer | Preserve/check |
| --- | --- | --- |
| Structured logs | What happened for a bounded operation or component? | Timestamp and timezone, severity semantics, stable IDs, release/version, redaction, duplicates and dropped records |
| Distributed traces | Where did an end-to-end operation spend time or fail? | Parent/child propagation, async links, retries, sampling policy, missing spans and clock skew |
| Profiles | Which code paths consume CPU, allocate memory, wait on locks, or retain objects? | Runtime/build symbols, sampling overhead, representative workload, sensitive stack/heap contents |
| Events and audit trails | Which actual configuration, identity, scheduling, or administrative changes occurred? | Actor/automation, exact resource, effective version, event time versus ingestion time |
| Synthetic/real-user checks | Does the user path work from the relevant location? | Test-account behavior, safe side effects, geography, DNS/TLS/auth coverage, and client sampling bias |

Bound log queries by service/resource, interval, fields, and row/byte limits. Expand scope only when the first result warrants it. Keep raw evidence in an approved location; share minimal excerpts. Avoid credentials and payloads in logs. OpenTelemetry baggage crosses process boundaries and can reach other services; propagate only approved metadata and configure redaction before export.

Trace samples are not automatically a statistically unbiased SLO denominator. Tail sampling can deliberately overrepresent errors. A missing trace does not prove no request occurred. Heap dumps, continuous profilers, eBPF tools, packet capture, and verbose logging can change performance or disclose data; use the least intrusive appropriate method with established authority.

## Alert policy

An alert needs an owned user consequence or near-term threat, a specific action, useful evidence, an escalation path, and a valid runbook. Page when timely human intervention is necessary. Use tickets for durable work and dashboards for context. Resource saturation may justify early warning when time to failure demands action, but avoid paging on arbitrary utilization alone.

For error-budget alerts, express the error ratio and target consistently. A multi-window condition combines the same burn threshold over a long window and a shorter confirmation window. Combine different urgency conditions with OR. Align grouping labels and vector matching; incompatible label sets can silently discard an alert.

For a 30-day SLO period, Google's published starting examples include a 14.4 burn rate over 1 hour and 5 minutes, or 6 over 6 hours and 30 minutes. These are examples, not universal service thresholds. Derive settings from response time, traffic, business impact, and desired budget protection; document assumptions for variable traffic and low volume. Avoid a long `for` duration that accidentally hides repeated severe bursts. Validate firing and clearing behavior with representative historical data or controlled tests.

Explicitly design for no data, low traffic, partial telemetry loss, scheduled activity, multi-region failure, and alert delivery failure. A minimum-volume condition can suppress critical failures on a low-traffic service; pair statistical constraints with independent journey checks and an agreed response policy.

Route by service ownership and urgency. Deduplicate related symptoms and prevent repeated pages without hiding independent failures. If using inhibition, test that its parent alert and routing remain reliable. Time-bound silences with an owner, reason, and expiry. Acknowledge is not resolve; recovery requires evidence.

Validate query syntax with the actual backend and use tooling such as `promtool` for Prometheus rules when available. Test cases should cover a real failure pattern, recovery, absent metrics, label mismatch, and low traffic. Do not claim a rule has been deployed, delivered a page, or passed testing merely because it parses.

## Investigate the monitoring system

When the service appears healthy or broken only in one tool, compare an independent user-path check. Trace telemetry through instrumentation, local agent/collector, scrape/receiver, processor, queue, exporter, network, storage, query layer, alert evaluator, router, and recipient delivery.

Look for collector restarts, queue saturation, dropped samples, backpressure, authentication/expiry, changed labels, cardinality bursts, storage quotas, retention/downsampling changes, and broken notification integrations. Check whether the same incident removed service telemetry and triggered a false recovery. Establish a tested out-of-band path for a major monitoring or identity outage.

Review alert burden using pages per shift, actionable fraction, repeated symptoms, missed incidents, delivery delay, time to useful diagnosis, and interrupted sleep. Improve the highest-impact signal or runbook before adding more telemetry. Do not rank individuals by page response times without context.

## Deliverable and sources

Return the question answered, exact query/source/window, observation, interpretation and uncertainty, recommended action, and a verification step. For a design task, provide the minimal dashboards, SLI definitions, alert rules, and runbook links with explicit dependencies and untested assumptions.

Primary foundations:

- Google [monitoring](https://sre.google/workbook/monitoring/) and [SLO-based alerting](https://sre.google/workbook/alerting-on-slos/).
- Prometheus [histograms](https://prometheus.io/docs/practices/histograms/) and [query functions](https://prometheus.io/docs/prometheus/latest/querying/functions/); check current behavior against the deployed version.
- OpenTelemetry [signals](https://opentelemetry.io/docs/concepts/signals/), [baggage](https://opentelemetry.io/docs/concepts/signals/baggage/), and [sensitive data](https://opentelemetry.io/docs/security/handling-sensitive-data/).
