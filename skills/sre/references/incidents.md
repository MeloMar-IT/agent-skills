# Incident response and investigation

## Contents

- [Establish control and impact](#establish-control-and-impact)
- [Build the evidence record](#build-the-evidence-record)
- [Run mitigation and diagnosis together](#run-mitigation-and-diagnosis-together)
- [Investigate with competing hypotheses](#investigate-with-competing-hypotheses)
- [Handle security and data-integrity signals](#handle-security-and-data-integrity-signals)
- [Communicate and hand over](#communicate-and-hand-over)
- [Verify recovery and close](#verify-recovery-and-close)
- [Sources](#sources)

## Establish control and impact

For a multinational event, record entity-specific impact and use [compliance-applicability.md](compliance-applicability.md) for verified classification and notification playbooks. Maintain distinct awareness/classification timestamps and accountable reporting owners while recovery continues. Use [audit-evidence.md](audit-evidence.md) for protected evidence capture and known collection gaps; do not invent one worldwide reporting clock.

Start with the affected user journey, observed harm, first known occurrence, current trajectory, and immediate decision. Separate an alert firing from a confirmed customer incident. Apply the organization's severity policy; if unavailable, describe impact and propose a provisional priority without pretending a universal SEV mapping exists. Include partial failures, correctness failures, unavailable dependencies, and missed batch deadlines, not only total unavailability.

Resolve the exact service, environment, tenant/account/subscription, region, cluster or host, and permitted access. Use existing authorization. Do not require a completed questionnaire before beginning useful, authorized investigation; mark missing facts and choose safe bounded observations. If tools or access are missing, request specific evidence with collection instructions and explain what each item will distinguish. Never claim to have queried a system that was not accessible.

Record a short initial state:

| Field | Required content |
| --- | --- |
| Impact | Journey, population, failed/slow/incorrect operations, known exclusions |
| Timing | Earliest evidence, detection, declaration, timezone, uncertainty |
| Scope | Affected and unaffected regions, versions, tenants, hosts, request types |
| Status | Expanding, stable, recovering, or unknown; supporting evidence |
| Objective | Immediate harm to reduce and recovery conditions |
| Authority | Existing incident lead, applicable runbook, authorized action scope |
| Coordination | Incident record, workstreams, next update time |

Use an incident commander to coordinate decisions, an operations lead to coordinate changes, and a communications lead to prepare updates. Combine roles for small teams, but make the combination explicit. Assign a scribe when possible. Do not independently assume human command authority or send notifications. Draft an incident declaration and escalation request if needed; send only when the user has explicitly authorized communication through the relevant channel.

## Build the evidence record

Use an append-only investigation log or retain revision history. Distinguish four categories: **observed**, **reported**, **inferred**, and **unknown**. Attach evidence IDs to material conclusions. Preserve the exact query, scope, time range, aggregation, relevant version, and collection time so another engineer can reproduce the observation.

| Evidence ID | Event time / original timezone | Collected at UTC | Source and scope | Observation | Limits |
| --- | --- | --- | --- | --- | --- |
| E-001 | Original timestamp; normalized timestamp if trustworthy | Timestamp | Query/log/deployment/audit reference | Measured fact | Sampling, clock skew, gaps, retention |

Keep original timestamps alongside normalized UTC. Check host clock offset, collector delay, timezone assumptions, and daylight-saving transitions. Mark an ordering uncertain when differences are within clock uncertainty. Separate event time from ingestion time and command completion from the time its effect became visible. Do not invent minute-by-minute precision from coarse graphs.

Collect narrowly: known resource, incident interval plus a justified baseline, selected fields, bounded rows/log bytes, and query timeout. Prefer existing telemetry before enabling more collection. Avoid whole-environment dumps, secrets, session tokens, unbounded logs, and high-cardinality searches. Record permission-denied, empty, stale, and partially successful results as collection outcomes, not evidence of health. Capture volatile evidence before a restart when feasible, without delaying an urgent authorized mitigation solely to perfect documentation.

## Run mitigation and diagnosis together

Maintain two coordinated workstreams. Mitigation reduces harm; diagnosis improves the explanation. A mitigation can be justified before causal certainty, and a successful mitigation does not prove a hypothesis.

For each candidate intervention, state target, expected benefit, supporting evidence, known hazards, blast radius, prerequisites, existing authority, success threshold, abort threshold, and observation period. Explain whether reversal is actually valid. Restoring a backup, forcing failover, draining a node, restarting a singleton, increasing retries, or clearing a cache can worsen an outage. Treat them as consequential changes, not diagnostic reads.

Compare credible options: pause a harmful rollout, disable a specific feature, isolate a failing cohort, shed nonessential load, reduce amplification, route around a dependency with verified capacity, or use a documented recovery path. Check that the alternative preserves authorization, correctness, and agreed degraded-service behavior. Do not improvise bypasses of security or transaction controls to make availability graphs green.

Apply authorized changes in a coordinated sequence with a single action owner. Avoid simultaneous experiments on the same dependency. After every intervention, record the exact action and result; compare impact and guardrails before continuing. Stop the sequence on unexpected effects. Do not repeatedly retry a failing operation without understanding idempotency and partial completion.

## Investigate with competing hypotheses

Model the path of one affected operation: client, edge, DNS/TLS, load balancer, application, dependency, storage, and response. Locate the first boundary where observed behavior diverges from expectation. Compare an affected instance with a meaningfully similar unaffected one before collecting every possible metric.

Maintain a short ranked table:

| Hypothesis | Supporting evidence | Contradicting evidence | Discriminating check | Predicted results | Status |
| --- | --- | --- | --- | --- | --- |
| Candidate mechanism | Evidence IDs | Evidence IDs or missing data | Scoped low-risk check | Outcome if true versus false | Untested / weakened / supported / rejected |

Prefer checks that separate competing explanations. State the predicted result before running a check. Update the ranking after evidence arrives; do not quietly abandon falsified theories. Use qualitative confidence tied to evidence strength rather than invented numerical probabilities. A nearby deployment is a lead, not proof; open `changes.md` when investigating that lead.

| Observation | First distinctions to resolve |
| --- | --- |
| Errors increased | User operations versus retries; local versus downstream failure; one cohort versus all |
| Latency increased | Queueing versus execution versus network time; changed mix; tail versus average |
| Traffic disappeared | Demand loss, routing failure, telemetry loss, deliberate load shedding |
| CPU or memory rose | Workload growth, throttling, leak, retries, GC, noisy neighbor, changed limits |
| Queue lag increased | Producer rate, consumer capacity, poison messages, partition skew, offset interpretation |
| Recovery followed restart | State/cache/connection reset, traffic change, instance replacement, unrelated dependency recovery |

Revisit the architecture when evidence conflicts with the model. Identify common dependencies and shared failure domains. Test common causes before assuming independent faults. For intermittent failures, preserve distributions and cohort labels rather than averaging them away. Use reproduction in an isolated environment when it answers a concrete question; do not inject failures into production during an incident without explicit scope and authority.

## Handle security and data-integrity signals

Escalate suspected compromise, unauthorized access, or integrity loss through the organization's security response process. Preserve relevant evidence and access history in an approved restricted location. Record collector, time, source, transformation, and access controls; hash exported artifacts when integrity tracking is required. Avoid editing originals or distributing raw sensitive logs in general incident updates.

Protect ongoing evidence collection when selecting containment. Do not promise forensic completeness from ordinary logs. Verify whether writes continued, whether duplicates or omissions occurred, and whether suspect data propagated to replicas, caches, reports, or backups. Keep integrity assessment open after availability recovers when necessary; a reachable database is not evidence that its data is correct.

## Communicate and hand over

Draft updates in this order: current impact, change since last update, actions and observed results, remaining uncertainty, next decision, next update time. State the next update time instead of inventing a repair ETA. Keep customer wording separate from internal technical detail and protect identifiers. Distinguish proposed, executing, completed, and verified actions.

Hand over explicitly: incoming owner, current impact, completed and in-flight actions, rejected hypotheses, remaining hypotheses, exact environments, safety constraints, access gaps, next checks, and communication obligations. Obtain acknowledgement through an authorized channel. Recheck fatigue, staffing, and whether critical knowledge is concentrated in one person.

## Verify recovery and close

Define recovery with user-visible evidence and dependency health. Check representative end-to-end journeys, successful operation counts, latency tails, errors, saturation, and affected cohorts. Check backlog age and drain rate, replication health, and delayed work. Validate correctness and reconciliation for stateful operations; avoid generating duplicate business transactions as a health test.

Choose an observation window based on failure periodicity, traffic patterns, deployment convergence, cache TTLs, queue drainage, and detection delay. Do not assert a fixed universal monitoring period. Confirm that a healthy dashboard is not explained by missing traffic, disabled alerting, changed denominators, or suppressed telemetry. Record residual risk and temporary mitigations, with owners and expiration/review conditions.

Close the active incident when the agreed recovery conditions hold and ownership of remaining work is explicit. Preserve a concise incident record: impact, timeline, evidence, interventions, recovery proof, unresolved questions, and follow-up owners. Route substantial incidents, near misses, recurring faults, and surprising successful recoveries to `learning.md`. Keep recurrence investigation separate from declaring immediate recovery.

## Sources

Use these primary references for the underlying practices; the tables and operational decision sequence above are original synthesis.

- [Google SRE: Managing Incidents](https://sre.google/sre-book/managing-incidents/) — coordination and clear response roles.
- [Google SRE: Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/) — iterative hypotheses and discriminating evidence.
- [Google SRE Workbook: Incident Response](https://sre.google/workbook/incident-response/) — response practice and preparation.
- [Google SRE Workbook: Postmortem Culture](https://sre.google/workbook/postmortem-culture/) — learning after recovery.
