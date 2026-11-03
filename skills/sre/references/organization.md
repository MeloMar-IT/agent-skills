# SRE organization and ways of working

## Contents

- [Establish the engagement](#establish-the-engagement)
- [Cover the service lifecycle](#cover-the-service-lifecycle)
- [Build sustainable on-call](#build-sustainable-on-call)
- [Measure and remove toil](#measure-and-remove-toil)
- [Recover an overloaded team](#recover-an-overloaded-team)
- [Develop people and knowledge](#develop-people-and-knowledge)
- [Lead adoption and collaboration](#lead-adoption-and-collaboration)
- [Run a production review](#run-a-production-review)
- [Sources](#sources)

Apply these original operational instructions using the actual organization's constraints. They extend the public Google guidance; they are not a transcription of an unread second-edition chapter. Read incidents.md for incident command, learning.md for reviews, and reliability-engineering.md for objectives and risk decisions.

Use [soft-skills.md](soft-skills.md) for listening, stakeholder communication, disagreement, negotiation, feedback, mentoring, and decision-bias countermeasures. Use [essential-sre-insights.md](essential-sre-insights.md) for the supplied ebook's chapter map and qualifications. Apply these behaviors throughout an engagement rather than treating people skills as a separate meeting activity.

## Establish the engagement

For multinational or regulated-service work, use [enterprise-governance.md](enterprise-governance.md) for legal-entity ownership, global/local requirements, control decision rights, shared services, suppliers and management oversight. Use [audit-evidence.md](audit-evidence.md) to distinguish engineering self-checks from the required independent assurance. Apply only confirmed obligations and actual delegations.

Start with the service's critical user journeys, business consequences, current owners and operating constraints. Establish what reliability improvement is needed and why the existing arrangement cannot deliver it. Treat SRE as an engineering contribution to reliability, DevOps as shared delivery/operations practices, and platform engineering as reusable capabilities serving internal users. Assign responsibilities explicitly where these overlap.

Draft a short charter containing mission, supported services, customer outcomes, engagement type, decision rights, staffing assumptions, escalation paths and review date. Select consulting, embedded, shared-platform or direct operational support according to the problem. Do not silently make SRE the owner of every production issue.

Record a named accountable service owner and the roles responsible for development, operations, security, data, suppliers and business risk. Mark proposed assignments as proposals. Give each accepted risk an owner, rationale, compensating measures, expiry/review date and trigger for reconsideration. Escalate disagreement to the authorized decision maker with options and consequences; do not decide business risk by technical seniority alone.

Define entry conditions, measurable outcomes and an exit or transfer path. Include access, observability, documentation, operational load, recovery capability, development participation and backlog funding. Avoid indefinite support commitments without corresponding resources. [Engagement source: G1.]

## Cover the service lifecycle

Use stage-appropriate evidence rather than imposing a single checklist everywhere:

| Stage | Required work and decision |
| --- | --- |
| Discovery/design | Identify users, risks, dependencies, ownership and constraints; influence architecture before commitments harden. |
| Build | Add instrumentation, failure handling, testability, deployment controls and operability. |
| Limited release | Measure real journeys; qualify capacity, recovery, on-call readiness and launch conditions. |
| General operation | Review objectives, changes, incidents, toil, dependencies and service evolution. |
| Migration/transfer | Agree overlapping ownership, evidence preservation, data correctness, rollback and acceptance. |
| Retirement | Identify remaining consumers; retain required evidence/data; remove access and dependencies through authorized change. |

For legacy systems, map what can actually be observed and changed. Use targeted improvements around the existing system before recommending replacement. For a solo SRE or small team, reduce scope, share operational responsibility and make support hours explicit. Never present one person's permanent availability as a sustainable service design.

## Build sustainable on-call

Derive coverage from user impact, response requirements, support agreements and available expertise. Model primary coverage, escalation, backup, leave, sickness, training, handovers and recovery time. Test the schedule against realistic absences. Record unsupported hours or simultaneous-incident limits instead of concealing them.

Measure actionable pages, distinct incidents, interrupted nights, time spent responding and follow-up work. Separate alert volume from incident count. Review whether the recipient can take useful action within the required time. Fix duplicate, unactionable and misrouted pages while preserving detection of consequential failures.

Require reliable escalation, access and an experienced backup before independent shifts. Give responders a clear way to declare overload and request relief. Reserve engineering time and apply agreed compensation/rest arrangements. Set local workload limits; Google's staffing examples and percentage targets are not universal quotas. Include fatigue and psychological safety in operational reviews without diagnosing individuals. [On-call source: G2.]

## Measure and remove toil

Sample operational work over a representative period. Record task, frequency, duration, variability, trigger, required expertise, failure risk and growth driver. Distinguish recurring service maintenance from valuable one-off engineering, necessary judgment and administrative work; do not label all operations as toil.

Prioritize by recurring effort, user risk, interruption cost and expected growth. First remove unnecessary work or fix its generating defect; then simplify, standardize or automate what remains. Estimate annual hours avoided using observed frequency and duration, subtract maintenance and exception handling, and include implementation cost. State uncertainty and measure actual savings after rollout. Treat reduced hours as capacity recovered, not automatically as cash saved.

Give automation an owner, bounded scope, failure behavior, observability, safe retries and a manual recovery route. Check whether work moved to developers, customers or another team. Do not celebrate closing tickets faster while their underlying demand keeps growing. [Toil source: G3.]

## Recover an overloaded team

Identify whether overload comes from incidents, support queues, release churn, unclear ownership, staffing gaps or unbounded engagement. Separate demand arrival rate from throughput and examine aging work. Preserve essential incident coverage while making the capacity gap visible.

Establish one intake route and a rotating interruption role where staffing permits. Limit concurrent work; negotiate deferral or transfer with owners. Protect a small improvement stream aimed at the largest recurring demand source. Request temporary development assistance with explicit outcomes and an end date. Reassess demand, backlog age, paging and engineering capacity regularly. Do not merely add a dashboard or tell people to work more efficiently.

## Develop people and knowledge

Build a competency map spanning service architecture, diagnostics, programming, observability, changes, data recovery, incident coordination and communication. Hire against demonstrable problem solving and collaboration rather than tool-name accumulation. Use consistent, job-relevant assessment and record evidence against the role's criteria.

Onboard through an architecture walkthrough, dependency map, previous incidents, bounded diagnostic tasks, shadowing, supervised response and practiced handover. Establish readiness by demonstrated ability to diagnose, escalate and recover safely; avoid a fixed number of weeks as the sole gate. Keep mentors available and refresh knowledge after major changes.

Reward lasting reliability improvements, useful incident learning, documentation, mentoring and reduced toil. Preserve technical and leadership growth paths. Review concentration of expertise and planned succession before one departure becomes an operational failure. [Training source: G4.]

## Lead adoption and collaboration

Choose a concrete pilot, establish a baseline and agree success measures with product and engineering leaders. Identify whose work changes, what incentives conflict and what training or access is needed. Review feedback and revise the approach before wider adoption. Distinguish organizational change from the technical change workflow. [Adoption source: G5.]

Agree shared dependency objectives, support boundaries, contact paths and joint recovery responsibilities. For vendors, retain evidence required for support cases and clarify which telemetry and actions remain outside local control. Use explicit handovers with current impact, evidence, actions, risks and next ownership. Draft communications when requested; send or publish only within the user's authorization.

## Run a production review

Use a short recurring agenda: customer outcomes and budget trends; recent incidents and near misses; high-risk changes; capacity/recovery readiness; overdue corrective work; operational load; ownership gaps and decisions needed. Examine distributions and affected cohorts before averages. Do not rank individuals by incident count or reward suppressing reports.

Produce a prioritized backlog with expected outcome, supporting evidence, owner, effort range, dependency, review date and completion test. Balance immediate risk reduction with durable improvements. Close actions on verified results, not ticket status. Retire obsolete work and record consciously accepted residual risk.

## Sources

Primary pages checked 2026-11-03:

- **G1:** [SRE engagement](https://sre.google/workbook/engagement-model/).
- **G2:** [On-call practice](https://sre.google/workbook/on-call/).
- **G3:** [Toil reduction](https://sre.google/workbook/eliminating-toil/).
- **G4:** [Onboarding and development](https://sre.google/sre-book/accelerating-sre-on-call/).
- **G5:** [Organizational change](https://sre.google/workbook/organizational-change/).
