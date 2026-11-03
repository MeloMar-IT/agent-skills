# Incident working record: [ID / service / symptom]

Status: [investigating / mitigating / recovering / monitoring / resolved — verified or unverified]

## Current situation

- User/business impact; affected and unaffected cohorts:
- Data integrity, security, safety or contractual concerns:
- Local severity and why; incident lead:
- First known bad / last known good / detection time:
- Original timezone, UTC normalization and clock uncertainty:
- Current mitigation, result and residual risk:
- Next action, owner and next update time:
- Existing authorization and any unresolved action boundary:

## Roles and coordination

| Role or workstream | Owner | Responsibility / handover |
| --- | --- | --- |
| Coordination | | |
| Operations/recovery | | |
| Investigation | | |
| Communications/scribe | | |

Combine roles for a small incident. Do not invent assigned people.

## Entity impact and notification tracking — when applicable

- Affected legal entities, business services, countries and classified data:
- Verified obligation/playbook, policy/source version and classification owner:
- Distinct occurrence, detection, awareness and classification/materiality times:

| Obligation / entity | Trigger / threshold / clock basis | Deadline / stage / timezone | Decision owner / authorized sender | Draft / submitted / acknowledged status and evidence |
| --- | --- | --- | --- | --- |
| | | | | |

Use [regulatory-applicability.md](regulatory-applicability.md). Retain uncertain facts and route missing decisions promptly. Work recovery in parallel; do not invent one global deadline, reset clocks at handover, or send notices without authority.

## Evidence ledger

| ID | Event time / observed time | Source, target, query and interval | Fact / reported claim | Limits, redaction and freshness |
| --- | --- | --- | --- | --- |
| E1 | | | | |

## Timeline and actions

| Time with offset | Event/action and actor | Evidence ID | Before state | Result / verification |
| --- | --- | --- | --- | --- |
| | | | | |

## Hypothesis register

| ID | Explanation and predicted observation | Supporting evidence | Contradictions / alternatives | Confidence | Next disconfirming test / owner |
| --- | --- | --- | --- | --- | --- |
| H1 | | | | | |

## Proposed intervention

- Exact target and operation; authority:
- Expected benefit, side effects and blast radius:
- Preconditions, timeout, stop conditions:
- Rollback/forward recovery and state compatibility:
- User-visible verification and observation period:

## Recovery and handover

- Journey, SLI, dependency, data and backlog checks:
- Representative workload and remaining degraded redundancy:
- Active changes/silences, expiry and owner:
- Hypotheses still open; next responders and escalation:
- Evidence location, learning review decision and next steps:

## Communication draft

[Time] [Confirmed impact and affected scope]. [Current action and verified progress]. [Known uncertainty]. Next update: [time/owner].

Label as draft until actually sent under explicit authorization.
