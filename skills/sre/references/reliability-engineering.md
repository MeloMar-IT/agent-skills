# Reliability engineering, design, and recovery

## Contents

- [Outcomes and risk](#outcomes-and-risk)
- [SLI and SLO contract](#sli-and-slo-contract)
- [Budget arithmetic](#budget-arithmetic)
- [Dependency and distributed-system design](#dependency-and-distributed-system-design)
- [Capacity, performance, and overload](#capacity-performance-and-overload)
- [Testing and disaster recovery](#testing-and-disaster-recovery)
- [Readiness and deliverable](#readiness-and-deliverable)
- [Primary sources](#primary-sources)

## Outcomes and risk

Start with the business operation and the losses it cannot tolerate. Separate availability, latency, correctness, durability, freshness, security, and recoverability. A service can be available while returning the wrong balance or permanently losing accepted writes.

Identify the risk owner, users, service tier, contractual commitments, operating hours, dependencies, growth, and constraints. Distinguish an internal objective from a contractual SLA. Do not interpret an error budget as permission to violate integrity, authorization, privacy, or other nonnegotiable requirements.

Use a risk register with scenario, consequence, existing safeguards, evidence of effectiveness, uncertainty, proposed treatment, accountable owner, and review date. Label qualitative estimates. Do not convert ordinal likelihood/severity labels into precise probabilities or monetary forecasts without defensible data. Compare the expected benefit of reliability work with cost, delivery delay, complexity, and operating burden. Offer sensitivity ranges when assumptions dominate.

## SLI and SLO contract

1. Select a small number of critical user journeys and identify the observation point nearest the user that is reliable and affordable. Include client-side failure where server metrics miss failed attempts.
2. Define eligible events, good events, exclusions and why they are justified, deduplication/retry semantics, measurement source/query, grouping, freshness, and missing-data behavior. Establish whether a failed request that never reaches the service enters the denominator.
3. Define the target, evaluation window, timezone, rolling versus calendar treatment, and the owner authorized to change them. Use actual business requirements and a measured baseline; do not invent 99.99% because it sounds mature.
4. Segment important tenants, regions, client types, or journeys without exploding telemetry cardinality. Examine whether aggregate success hides a persistently failing minority.
5. Validate counts against an independent sample and real failure cases. Check double-counting, retries, ingestion delay, incorrect labels, counter resets, and exclusion bias.
6. Agree on decisions driven by the budget: release progression, reliability work, escalation, exceptions, and criteria to resume normal delivery. Preserve urgent remediation/security fixes through an explicit exception path.

| Service behavior | Candidate good-event definition | Common blind spot |
| --- | --- | --- |
| API operation | Eligible operation completed correctly within its deadline | Counting each retry as a new user attempt; HTTP 200 with an error payload |
| Interactive journey | User completed the end-to-end action within a latency threshold | Healthy backend with broken login, DNS, or client |
| Queue or streaming job | Accepted item processed correctly before freshness deadline | Fast acknowledgement followed by lost or duplicated processing |
| Batch/report | Scheduled output correct and available before its business deadline | Process exit 0 with missing input or incomplete output |
| Storage | Accepted data remains readable, correct, and durable for defined retention | Availability measured without recovery or checksum validation |
| Platform | Consumer workload obtains and retains the promised capability | Control-plane health masking broken workloads |

Measure latency with distributions and deadline success ratios. Do not average instance p99 values. Do not conflate a percentile objective with a mean or with availability. For low-traffic journeys, report sample size and uncertainty; use suitable longer windows, business-event checks, or synthetic probes while preserving the user-event definition.

Define incident-duration metrics by their actual start and end events: impact, detection, acknowledgement, mitigation, service recovery, and data reconciliation can occur at different times. Expand and define "MTTR" before reporting it. Retain distributions and affected cohorts when averages conceal prolonged harm. Keep internal SLO measurement and contractual SLA measurement distinct, and derive dependency targets from the actual failure model rather than allocating arbitrary percentages by perceived component importance.

## Budget arithmetic

For an event-based SLO over one precisely defined observation window:

```text
S = target fraction, for example 0.999 for 99.9%
N = eligible events; B = bad events (0 <= B <= N)
observed SLI = (N - B) / N                       when N > 0
allowed bad-event budget = N * (1 - S)
budget consumed = B / [N * (1 - S)]              when denominator > 0
remaining budget = N * (1 - S) - B               may be negative
window burn rate = (B_window / N_window) / (1 - S)
```

Use `scripts/slo_budget.py` from the skill root for deterministic offline calculations. Example: one million events, 1,500 bad events, and a 99.9% target produce 99.85% observed success, a 1,000-event allowance, 150% consumption, and a 500-event deficit. This is illustrative arithmetic, not observed service data.

Do not turn no traffic or missing metrics into perfect service. At a 100% target the allowable budget is zero and normal burn-rate division is undefined. Treat that case explicitly rather than fabricating a finite result.

For a time-based availability SLO only, allowed bad time is `(1-S) * eligible time`. A 99.9% objective over exactly 30 eligible days allows 43.2 minutes of bad time. That is not automatically the outage allowance of a request-based SLO. Exclusions, partial failures, and variable traffic change the interpretation.

For an alert window `w` and SLO period `T`, the common approximation `burn * w/T` assumes compatible, steady exposure. With event-based measurement and variable traffic, calculate actual contribution as bad events in the interval divided by the full evaluation-period event allowance, when that denominator is known. Label future traffic and exhaustion forecasts as assumptions. A rolling window can regain budget as old errors age out; do not claim it is a permanently shrinking account.

Use multi-window alert design in observability.md. A budget policy is a decision agreement, not merely a dashboard.

## Dependency and distributed-system design

Draw the user path, write path, dependency graph, failure domains, and administrative/control dependencies. Include DNS, identity, certificate authorities, secrets, time, configuration, telemetry, deployment, and recovery access. Mark hard versus optional dependencies and where graceful degradation is possible.

| Design question | Evidence or decision required |
| --- | --- |
| Redundancy and isolation | Identify common regions, racks, power, network, software/config, credentials, and control planes; demonstrate failure-domain separation. |
| Frontend/global load balancing | Review health semantics, DNS caching, traffic steering, affinity, cross-region state, draining, cold caches, and reserve capacity at the destination. |
| Internal balancing | Check discovery freshness, endpoint readiness, uneven request cost, connection reuse, locality, queue depth, and one overloaded shard hidden by averages. |
| Timeouts and cancellation | Allocate an end-to-end deadline; ensure downstream work stops when its caller no longer needs it. |
| Retries | Require bounded attempts, jitter/backoff, a retry budget, and idempotency or duplicate suppression; account for retries at every layer. |
| Bulkheads and fallback | Isolate tenants and dependencies; test whether fallback adds load or changes correctness and whether it can itself fail. |
| State and consensus | Identify the actual algorithm, membership, voting/quorum rules, fencing, leader behavior, recovery authority, and partition semantics. |
| Simplicity | Prefer understandable components with clear ownership and fewer coupled control loops; explain the operational cost of new layers. |

Do not apply `A_total = product(A_i)` without a stated dependency/independence model. Redundant components can fail together. Do not use an availability estimate as proof of durability or failover correctness. Do not equate replica count with tolerated failures across all database products.

For recurring work, define scheduling ownership, timezone/DST semantics, missed-run handling, deadline, overlap policy, leases/fencing, idempotent work units, retry limits, and completion evidence. A scheduler firing once does not prove a task executed exactly once. For pipelines, verify source completeness, watermarks, late data, reconciliation, backpressure, and safe replay; route to data-services.md.

## Capacity, performance, and overload

1. Characterize workload with arrival rate, burst shape, concurrency, request size/cost, tenant skew, read/write mix, cache hit ratio, and batch overlap. Use observed distributions; label forecasts.
2. Find the limiting resource or dependency using utilization, saturation, errors, queue delay, and service time together. Averages and CPU alone are insufficient.
3. Estimate per-unit sustainable throughput at the required latency and correctness. Include CPU throttling, memory/GC, storage latency/IOPS/throughput, network limits, connection pools, quotas, and licensing constraints.
4. Calculate capacity in the intended degraded mode: node/zone loss, maintenance, resynchronization, rollout surge, cache warming, and recovery traffic. Distinguish available quota from actual reserved capacity and successful provisioning.
5. Model autoscaling delay and hysteresis. The scaling signal may arrive after a queue has become unrecoverable; evaluate minimum capacity and admission control.
6. Validate the model with representative, authorized tests. Document bottlenecks, confidence limits, and the next failure threshold. Revisit after material workload or implementation changes.

Expose forecast uncertainty and provisioning lead times, and compare prior forecasts with actual demand before revising assumptions. Treat illustrative growth percentages, latency targets, and capacity multipliers as examples, not requirements for the current service.

Use `L = lambda * W` only for a stable system with consistently defined boundaries, units, and averages. An unbounded growing queue violates the steady-state assumption. An illustrative backlog `Q` drains in `Q/(mu-lambda)` only if effective service rate `mu` exceeds incoming rate `lambda` and the rates remain stable.

Under overload, compare admission control, per-tenant fairness, priority queues, shedding optional work, bounded queues, reduced concurrency, and more capacity. Avoid solving overload by unbounded queuing or retries. Check whether removing unhealthy instances overloads survivors and whether health checks share the failing bottleneck. Recovery may need load reduction before instance restoration.

## Testing and disaster recovery

Build a test portfolio around actual failure mechanisms: unit/contract tests for invariants; integration tests for dependencies; end-to-end correctness; load/soak tests for limits and leaks; failover/restore tests for recovery; and controlled experiments for resilience. A test that repeats the implementation's assumptions cannot validate an omitted business invariant. Get critical invariants from the accountable owner, including authorization and data correctness.

Use [software-testing.md](software-testing.md) for software verification, test design, performance evidence, and the limits of each type of check.

For each experiment, specify the hypothesis, steady-state user outcome, environment, exact injection, blast radius, permissions, observability, abort criteria, recovery steps, and owner. Validate those prerequisites before executing. Fault injection, traffic replay, and load generation can change live behavior and require explicit scope. Use assets/resilience-experiment.md; do not run a chaos experiment merely because a playbook mentions it.

Define RTO as the maximum tolerable restoration time and RPO as the maximum tolerable data loss expressed in time, for a particular business service and scenario. Include detection, decision, access, provisioning, data recovery, reconciliation, and user validation in the measured recovery timeline. Record achieved values separately from objectives and vendor claims.

Check backup coverage, retention, immutability/isolation, encryption/key availability, catalogs, dependencies, corruption detection, and restore performance. Replication propagates some failures; snapshots may depend on the failed storage. Require demonstrated recovery into an isolated target before claiming backup effectiveness. Validate business-level records, permissions, replay/idempotency, lag, and data gaps after restoration.

Exercise loss of the control plane, identity, credentials, DNS, telemetry, and primary region, not only one application process. Verify that recovery documentation and access remain available during the failure. Plan failback, conflict reconciliation, traffic return, and a controlled removal of emergency changes. For compromise, use security-approved isolation and trusted rebuilds; do not blindly restore compromised state.

### Choose recovery exercises by the question they answer

For each exercise, record the failure scenario, business process, included/excluded dependencies, workload, objectives, authorized scope, stop criteria, recovery owner, and evidence required. A passing exercise supports the tested scenario under its recorded conditions; it does not establish readiness for every disaster.

| Exercise | Useful evidence | What it does not establish alone |
| --- | --- | --- |
| Tabletop | Roles, decisions, communications, missing assumptions and dependencies | Restorable backups, working failover, or achievable recovery time |
| Isolated restore | Backup readability, keys, restoration procedure and recovered-data validity | Live routing, production capacity, or full application recovery |
| Replication check | Checked lag, completeness, and consistency | Protection from replicated corruption or whole-service readiness |
| Partial/application failover | Selected journeys and dependency recovery | Full-estate recovery or independence from shared services |
| Regional/live failover | User behavior and recovery under the selected failure and load | Untested failure combinations, dependencies, or future capacity |
| Combined-failure exercise | Specific interactions, fallback limits and propagation | General safety beyond the tested scenario |

Partial tests may affect shared resources. A maintenance window does not replace authorized scope, independent recovery capability, or stop conditions. Prefer the least risky exercise that resolves the material uncertainty. Rehearse recovery from the exercise itself.

### Preserve business continuity and qualify failback

Identify the minimum viable service, priority journeys, business impact over time, acceptable degraded modes, and verified manual workarounds. Include people, suppliers, identity, communications, and control-plane dependencies. Establish a communication path available when the primary environment is unavailable.

For manual or degraded operation, define permitted transactions, durable records, duplicate prevention, data protection, and later reconciliation. Assign actual owners where known and propose roles otherwise. Verify restored business operations and correctness before declaring full recovery; define who decides when failback is safe, how writes remain authoritative during transition, and how temporary work is reconciled.

These exercise distinctions and continuity prompts adapt chapter 16 of the supplied *Essential SRE Articles*; see [the source map and qualifications](essential-sre-insights.md).

## Readiness and deliverable

Use assets/readiness-review.md for launches, migrations, and acceptance. Return decisions as evidence-backed blockers, conditional acceptance with owner/date, and optional improvements. Avoid an unweighted checklist that gives ten minor successes the same importance as an untested restore.

Deliver the service outcomes/SLO contract, architecture and failure assumptions, capacity envelope, recovery evidence, top risks, prioritized changes, and residual uncertainty. For a short request, deliver only the relevant subset.

## Primary sources

Use these as foundations and recheck version-sensitive details. The procedures above are an original operational synthesis.

- Google: [risk](https://sre.google/sre-book/embracing-risk/), [SLO definitions](https://sre.google/sre-book/service-level-objectives/), and [implementing SLOs](https://sre.google/workbook/implementing-slos/).
- Google: [concrete system design](https://sre.google/workbook/non-abstract-design/), [overload](https://sre.google/sre-book/handling-overload/), [cascading failures](https://sre.google/sre-book/addressing-cascading-failures/), [critical state](https://sre.google/sre-book/managing-critical-state/), and [reliability testing](https://sre.google/sre-book/testing-reliability/).
- Microsoft: [reliability targets](https://learn.microsoft.com/en-us/azure/well-architected/reliability/metrics) and [disaster recovery design](https://learn.microsoft.com/en-us/azure/well-architected/design-guides/disaster-recovery).
