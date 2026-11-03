# SLO contract and budget policy: [service / user journey]

## User outcome and ownership

- Users, journey, consequence of failure, service owner and decision owner:
- Related SLA/contract and nonnegotiable correctness/security constraints:
- Baseline and rationale for the target:

## Measurement contract

| Field | Definition |
| --- | --- |
| Eligible event / denominator | |
| Good event / numerator, latency or freshness threshold | |
| Observation point and coverage gaps | |
| Error/retry/duplicate and client-failure semantics | |
| Exclusions and justification | |
| Target, rolling/calendar period, timezone | |
| Event-based versus time-based measurement | |
| Source/query/version and grouping | |
| Low traffic, missing/stale data and uncertainty | |
| Independent validation and known failure cases | |

## Budget and alerts

- Allowance, observed bad events/time, consumption, remaining budget:
- Exact interval, sample size, units and calculation assumptions:
- Page/ticket windows and thresholds, routing, deduplication:
- No-data/low-traffic behavior and independent checks:
- Alert/routing test results and runbook:

## Decisions

| Condition | Delivery/reliability decision | Owner | Exception path | Return-to-normal criterion |
| --- | --- | --- | --- | --- |
| | | | | |

Do not use budget as permission for data loss, security violations, or unmet contractual requirements. Review objectives and exclusions with owners; do not silently redefine success after an incident.

Next review date and known measurement improvements:
