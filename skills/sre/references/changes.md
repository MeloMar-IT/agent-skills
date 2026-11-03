# Change assessment and change investigation

## Contents

- [Choose the work mode](#choose-the-work-mode)
- [Establish intended and actual change](#establish-intended-and-actual-change)
- [Review a proposed change](#review-a-proposed-change)
- [Design rollout and recovery](#design-rollout-and-recovery)
- [Investigate a change-associated failure](#investigate-a-change-associated-failure)
- [Assess causal confidence](#assess-causal-confidence)
- [Produce a reviewable decision](#produce-a-reviewable-decision)
- [Sources](#sources)

## Choose the work mode

For enterprise controls, use [enterprise-governance.md](enterprise-governance.md) to establish actual preauthorization, assessed-change and emergency paths. Use [audit-evidence.md](audit-evidence.md) to trace authority, artifact, executing identity, target, time and outcome. Keep retrospective review distinct from prior approval and preserve valid existing delegation.

Distinguish **pre-change review**, **post-change investigation**, and **authorized execution**. A review request authorizes analysis and preparation; do not silently turn it into a production rollout. Preserve execution authority already granted in the session and avoid redundant permission requests. Follow local change policy and emergency procedures. If the user requests execution, complete the applicable review, establish concrete success and stop conditions, and proceed within the authorized scope.

Scale review depth to credible failure impact, novelty, irreversibility, observability, and dependency reach. Do not assign a risk score by intuition alone or impose the same process on every change. State the assumptions behind a recommendation. Treat exhausted error budget or uncertain recovery as inputs to the service's policy, not a universal automatic ban.

## Establish intended and actual change

Identify the business purpose, owner, affected journeys, target environment, relevant versions, change record, artifacts, and planned timing. Determine the effective deployed state instead of assuming a merged commit equals a production change. Record artifact digest/build ID, rendered configuration version, dependency versions, schema version, flag state, and observed rollout timestamps where relevant.

Inspect this inventory selectively:

| Change surface | Evidence to seek |
| --- | --- |
| Application | Commits, build provenance, image digest, rollout/rollback history, runtime settings |
| Configuration and flags | Effective values, resolved defaults, flag targeting, propagation and reload behavior |
| Infrastructure | IaC plan and applied result, drift, instance shape, quotas, placement, autoscaling policies |
| Platform | Node/OS/runtime upgrades, admission policy, CNI/CSI, service mesh, scheduler changes |
| Data | Schema/index/stored procedure changes, migrations, backfills, retention, volume and distribution |
| Access and connectivity | IAM/RBAC, certificate rotation, trust stores, secrets versions, DNS, routes, firewall/NAT |
| Dependencies and time | Managed-service maintenance, upstream API behavior, clock changes, expiry, recurring jobs |
| Workload | Tenant onboarding, traffic mix, batch overlap, client retries, load tests, unusual input |

Distinguish desired, rendered, applied, and effective state. Inspect references to mutable external configuration and data; reverting a repository revision may not restore them. Redact sensitive values and compare safe hashes, versions, or selected fields rather than exporting secrets or full state files.

## Review a proposed change

Trace the critical journey and relevant failure domains. Ask what can fail during the transition as well as after completion. Check capacity while old and new versions coexist, whether healthy instances can serve displaced traffic, and whether control-plane failure prevents rollback. Account for dependencies that cannot scale or fail over with the application.

Write the invariants first: authorized users only, no lost or duplicate committed operations, supported schema compatibility, valid quorum, capacity margin, bounded latency, and acceptable data freshness as applicable. Tie each invariant to evidence or a planned check. Validate behavior at boundaries: empty selections, partial results, repeated requests, stale state, timeouts after partial completion, and resumed jobs. Treat an empty target set as empty, not as permission to operate on everything.

Check readiness through relevant evidence: schema/contract checks, integration behavior, representative load, failover/restore rehearsal where needed, and known regression coverage. Distinguish tests that ran from tests merely proposed. Explain important untested paths. Prefer a few checks tied to identified hazards over a large checklist unrelated to the change.

For automation, review target selection, identity, least privilege, concurrency, idempotency, rate bounds, timeout, cancellation, audit output, partial-success reporting, and recovery after interruption. Dry-run must reflect the actual target set and side effects; do not assume a dry-run label means no writes or no external calls. Verify environment and client-version semantics before relying on it.

## Design rollout and recovery

Create a compact action card before a consequential change:

| Item | Required decision |
| --- | --- |
| Target and artifact | Exact scope, revision, owner, prerequisite state |
| Blast radius | Initial cohort and maximum expansion before another gate |
| Success | User-visible and technical checks with explicit thresholds |
| Abort | Conditions that pause expansion or trigger the approved recovery path |
| Observation | Duration and sample size justified by workload and propagation |
| Recovery | Tested rollback/roll-forward/isolation procedure and known limits |
| Authority | Existing approval and any specific remaining authorization |

Choose canary or staged cohorts that represent actual risky behavior: regions, request classes, tenant sizes, stateful paths, and long-lived connections. Compare rates with compatible denominators and account for low volume. A few successful synthetic requests do not establish safety for a rare migration path. Assess both absolute service limits and difference from a suitable control.

Check control contamination: shared caches, schemas, flags, dependencies, quotas, or routing may affect both canary and control. A shared configuration change can make an apparently isolated canary global. Consider delayed effects such as compaction, memory growth, certificate expiry, queue buildup, and scheduled work. Do not approve immediate expansion solely because process startup succeeded.

Plan state transitions explicitly. For a schema or protocol migration, assess mixed-version reads/writes, backfill idempotency, dual-write divergence, and when removal of old fields becomes safe. Prefer an expand/migrate/contract sequence when appropriate. If rollback cannot read the new state, select a validated forward repair or containment approach. A backup is useful only with a tested restore path, accepted recovery point, and a way to account for valid writes made afterward. Do not recommend restoring over production merely because a backup exists.

During execution, compare actual progress with the action card, gate each expansion, and record outputs. Re-evaluate after an abort or partial success rather than continuing a stale plan. Remove temporary permissions, flags, resources, and monitoring changes only after verification and owner agreement.

## Investigate a change-associated failure

First use `incidents.md` if user impact is active. Bound the investigation around the first trustworthy symptom and a suitable earlier baseline, then widen when evidence requires it. Include deployments that began before the incident and changes whose effect appears only after expiry, restart, or workload exposure.

Build a change ledger:

| Change ID | Requested / applied / effective time | Actual scope | Mechanism that could explain the symptom | Evidence for and against |
| --- | --- | --- | --- | --- |
| Candidate | Preserve timezone and clock uncertainty | Cohorts and versions | Specific causal prediction | Evidence references and gaps |

Compare affected with unaffected instances, and before with after, while accounting for traffic mix, load, region, tenant distribution, dependency state, and observation gaps. Inspect runtime artifacts and effective configuration. Look for partial rollout, stale caches, old processes, failed reconciliation, or automatic rollback that makes the current state differ from the incident state.

Trace the proposed mechanism from change to internal behavior to user harm. For example, a timeout increase may increase concurrent work and pool occupancy; the useful check compares timeout behavior, in-flight requests, pool waits, and completed operations. Do not stop at “deployment at 10:00, errors at 10:01.”

## Assess causal confidence

Separate **temporally associated**, **plausible mechanism**, **supported contributor**, and **demonstrated mechanism**. Record what would lower confidence as well as what supports the explanation. A rollback followed by recovery supports a connection but may coincide with traffic reduction, cache expiry, or upstream recovery. A rollback that fails does not necessarily exonerate the change: irreversible data, persistent configuration, or delayed convergence may remain.

Prefer reproduction with the relevant versions, data shape, configuration, and workload in an isolated environment. Do not deliberately reintroduce a known harmful change to production just to establish certainty. State the limits when reproduction is impractical. Keep multiple contributing changes where the evidence supports an interaction; avoid selecting one convenient culprit to satisfy a template.

## Produce a reviewable decision

For a pre-change review, return purpose and scope, material hazards, checks completed, gaps, rollout gates, recovery limits, and a reasoned proceed/modify/defer recommendation. Distinguish the recommendation from actual approval.

For an investigation, return verified change timeline, intended-versus-actual differences, cohort comparison, supported mechanism, alternative explanations, mitigation results, and remaining evidence. For execution, add the actual action log and user-visible verification. Assign follow-up owners and measurable outcomes when authority permits; otherwise propose them explicitly. Feed missing safeguards and recurrent patterns into `learning.md`.

## Sources

- [Google SRE Workbook: Canarying Releases](https://sre.google/workbook/canarying-releases/) — evaluating bounded rollout cohorts.
- [Google SRE Workbook: Configuration Design and Best Practices](https://sre.google/workbook/configuration-design/) — effective configuration, tracking, and recovery.
- [Google SRE: Release Engineering](https://sre.google/sre-book/release-engineering/) — repeatable release artifacts and workflows.
- [Google SRE: Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/) — testing proposed mechanisms rather than relying on coincidence.
