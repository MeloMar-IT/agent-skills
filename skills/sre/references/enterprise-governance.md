# Enterprise SRE governance for multinational organizations

Use this reference to design, assess, or improve the operating model around SRE across legal entities, business units, countries, and shared platforms. Make authority, obligations, control operation, and residual risk visible. Apply [compliance-applicability.md](compliance-applicability.md) for jurisdiction and framework scope, [audit-evidence.md](audit-evidence.md) for assurance, and [ai-governance.md](ai-governance.md) for AI access and execution.

## Contents

- [Establish the enterprise scope](#establish-the-enterprise-scope)
- [Combine a global baseline with local overlays](#combine-a-global-baseline-with-local-overlays)
- [Assign ownership and preserve independent assurance](#assign-ownership-and-preserve-independent-assurance)
- [Connect service criticality to decisions](#connect-service-criticality-to-decisions)
- [Engineer usable control operation](#engineer-usable-control-operation)
- [Govern changes and emergencies proportionately](#govern-changes-and-emergencies-proportionately)
- [Manage exceptions and accumulated risk](#manage-exceptions-and-accumulated-risk)
- [Govern shared services and suppliers](#govern-shared-services-and-suppliers)
- [Operate across regions and disruptions](#operate-across-regions-and-disruptions)
- [Report assurance and drive improvement](#report-assurance-and-drive-improvement)
- [Primary sources and limits](#primary-sources-and-limits)

## Establish the enterprise scope

Start with business services and the legal entities responsible for providing them. Identify customers, jurisdictions, business processes, operating hours, information classifications, contractual commitments, regulators where applicable, and accountable owners. Do not infer the current employer, regulated status, or risk appetite from conversation history. Mark unknowns and continue useful assessment without manufacturing an enterprise policy.

Map each critical journey to applications, platforms, data stores, people, facilities, cloud accounts, identity, communications, and external dependencies. Include control planes needed to deploy, observe, access, and recover the service. Record where production data, telemetry, backups, support access, and AI processing occur. A hosting region alone does not describe the complete data path.

Reconcile service catalogs, cloud inventories, configuration records, financial ownership, and actual runtime evidence. Investigate orphaned assets and conflicting owners. Preserve identifiers that connect the business service, legal entity, system, control, change, incident, supplier, and evidence record. Document inventory coverage and freshness; an incomplete catalog cannot support a complete assurance claim.

## Combine a global baseline with local overlays

Propose a common minimum baseline of control outcomes, definitions, evidence fields, and escalation rules. Let regional teams select suitable implementations within that baseline. Keep centrally maintained objectives separate from local procedures and technology choices. Use NIST CSF 2.0's GOVERN function as a useful organizing reference for context, responsibilities, policy, oversight, and supply-chain risk; it does not prescribe one implementation or establish legal compliance. [E2]

For every overlay, record the applicable entity, jurisdiction, service, data category, obligation source/version, responsible interpreter, additional control, and effective date. Use [regulatory-applicability.md](../assets/regulatory-applicability.md). Distinguish legal and contractual requirements from adopted standards and internal choices. Do not apply every framework everywhere or assume a headquarters policy settles subsidiary obligations. Resolve conflicting requirements through the designated legal, privacy, security, and business owners; selecting whichever rule appears stricter may not resolve the conflict.

Version policies and maintain a controlled change path. Assess affected services, tooling, contracts, evidence, and training before changing a baseline. Make obsolete guidance discoverable as superseded. Keep proposed policies visibly proposed until the authorized body adopts them; writing a document does not enact governance.

## Assign ownership and preserve independent assurance

Adapt the IIA Three Lines Model to actual responsibilities. Confirm delegated authority and reporting arrangements rather than assigning powers from job titles. Use these distinctions when designing the operating model: [E1]

| Role | Establish the practical responsibility |
| --- | --- |
| Governing body and senior management | Set direction, resource the operating model, oversee material exposure, and establish delegation and escalation. |
| Accountable business/service risk owner | Decide service priorities and residual business risk within delegated authority; obtain specialist interpretation of obligations. |
| First-line engineering and operations | Build and operate services and controls, observe failures, retain evidence, and remediate defects. SRE commonly contributes here. |
| Second-line risk, compliance, and specialist roles | Set or interpret applicable expectations, advise, monitor, and challenge management's risk decisions and control performance. |
| Internal audit | Provide independent assessment and advice without taking ownership of operational decisions it will assess. |

Name the control owner, operator, evidence custodian, reviewer, and escalation recipient where known. Mark vacancies and proposed assignments explicitly. Separate incompatible duties where the applicable control requires it; enforce separation through identity and workflow, including service accounts. Having two named roles does not establish independence when the same person or credential performs both.

Keep engineering self-assessment distinct from independent assurance. Disclose overlapping advisory and assurance responsibilities and use suitable safeguards. Do not make internal audit the normal release approver or substitute its review for management ownership. Coordinate evidence requests to avoid repeated collection while preserving each reviewer's scope and judgment.

## Connect service criticality to decisions

Derive criticality from business impact over time: customer harm, safety, transaction correctness, financial exposure, contractual duties, and interruption of dependent functions. Include low-volume but consequential services. Assess aggregate dependence on shared platforms; a component supporting many entities may create more exposure than any individual consumer suggests.

Agree the critical business operations, tolerable disruption, minimum viable service, recovery objectives, acceptable data loss, and degraded modes with the authorized owners. Keep business impact tolerances, recovery time/recovery point objectives, contractual service levels, and engineering SLOs separately defined and connected. An availability error budget does not authorize data loss or override an obligation.

Translate classification into proportionate coverage, access controls, release checks, recovery evidence, supplier assurance, and escalation. Treat tier names, review intervals, and example thresholds as policy proposals unless an applicable source prescribes them. Reassess after acquisitions, migrations, market entry, outsourcing, major incidents, or a change in business use.

## Engineer usable control operation

For each material risk, specify the unwanted outcome, preventive/detective/recovery mechanism, scope, owner, execution trigger, expected evidence, failure detection, and remediation path. Use [control-register.md](../assets/control-register.md) and [audit-evidence.md](audit-evidence.md) to distinguish design adequacy from actual operation. Map one effective control to several obligations where justified, without assuming their scopes or evidence requirements are identical.

Prefer controls integrated into normal work: expiring privileged access, protected deployment workflows, tested artifact provenance, drift detection, bounded automation, independent audit-log storage, recoverable backups, and measured restore exercises. Verify implementation and exceptions in the real environment. A policy checkbox, enabled setting, or product purchase is insufficient evidence of effectiveness.

Treat the control infrastructure as a service. Identify owners and failure behavior for identity, policy evaluation, deployment gates, evidence collection, time synchronization, and log retention. Decide which actions must stop if a required control becomes unavailable, and which may use an existing emergency path. Test that path and preserve trustworthy records. Do not silently convert failed evidence collection into a successful control result.

## Govern changes and emergencies proportionately

Use the established change policy and [changes.md](changes.md). Honor authorization already present; request another decision only when scope, authority, or material risk requires it. A multinational operating model does not imply a committee approval for every deployment.

- **Standard/preauthorized work:** Define eligible operations, bounded targets, prerequisites, tested procedure, monitoring, evidence, and recovery. Confirm the current request fits that authorization. Reassess the classification when the procedure or risk changes.
- **Assessed changes:** Route material risk to the appropriate technical, business, security, or data authority. Record the actual artifact and effective deployment, decision conditions, staged exposure, stop criteria, and verification. Use independent review where required by the control.
- **Emergency changes:** Use the existing emergency delegation, scope limits, named identity, contemporaneous record, and recovery checks. Capture any unavailable evidence and required subsequent review. A retrospective review must not be represented as prior approval.

Coordinate simultaneous changes to shared components across entities and time zones. Give incident command a clear operational remit and a route to decisions outside it. Keep restoration decisions, legal notification decisions, and external statements assigned to their authorized owners. Draft communications freely within the task; sending them remains subject to existing communication authority.

## Manage exceptions and accumulated risk

Record the precise control deviation, affected services/entities, cause, credible consequences, evidence, available alternatives, compensating measures, accountable risk owner, authorized decision, expiry, remediation funding, and conditions that terminate the exception. Use [risk-exception.md](../assets/risk-exception.md). Preserve whether acceptance is proposed, granted, rejected, expired, or superseded. An internal exception cannot waive law or unilaterally rewrite a contract.

Verify that compensating controls address the same failure mechanism and remain effective for the exception's duration. Expiry must trigger a defined response: remediation, escalation, restriction, or a newly justified decision. Avoid automatic renewal and permission that survives an expired exception. Keep emergency access expiry technically enforced where feasible.

Aggregate related exceptions. Several individually accepted deviations can share a cloud dependency, weak identity boundary, unsupported platform, or unavailable recovery team. Present cumulative exposure to the appropriate authority. Escalate when residual risk exceeds delegated limits or an owner cannot fund the required treatment; do not hide that gap inside an SRE backlog.

## Govern shared services and suppliers

For each inherited control, identify the provider, consuming services, responsibility split, configuration prerequisites, evidence source, reporting period, exceptions, and local checks. Verify the consumer actually satisfies its part. A platform's assurance report does not automatically cover every tenant configuration, subsidiary, region, or later change.

Build a critical-dependency view across internal shared services, contractors, software and model providers, managed services, cloud platforms, and relevant subcontractors. Trace concentration through common identity, DNS, control planes, network routes, support teams, and upstream suppliers. Two contracts or regions do not establish independent failure domains. Use the NIST supply-chain guide to organize supplier requirements through the relationship lifecycle. [E3]

Work with procurement and legal owners on service scope, security expectations, notification cooperation, evidence and audit access, recovery support, material changes, sub-outsourcing, data handling, and termination. Record relevant subprocessor arrangements where personal data is involved. Distinguish desired terms from signed obligations and verify which party can actually provide the required logs or assistance.

Review supplier assurance against scope, period, exclusions, findings, and customer responsibilities. Seek additional evidence for material gaps. Exercise joint incident and recovery paths where authorized. Maintain a feasible exit route: data and configuration export, identity and key transition, replacement capacity, knowledge transfer, retention/deletion duties, and continuity during migration. Test critical assumptions; contractual exit rights alone do not establish an executable exit.

## Operate across regions and disruptions

Design follow-the-sun coverage around demonstrated competence, permitted access, language, holidays, local working arrangements, and sufficient overlap. Confirm acknowledgement of handovers, outstanding decisions, active changes, evidence locations, and next ownership. Never infer that another region has taken responsibility because its working day has begun.

Plan for regional disruption and common dependencies affecting the whole group. Include communications, staffing, facilities, third parties, identity, recovery credentials, telemetry, and evidence access. Verify lawful and technically available recovery locations through the relevant owners. Use [reliability-engineering.md](reliability-engineering.md) for exercises and business continuity; ISO 22301 supplies a management-system reference, not proof that a particular recovery design works. [E4]

During a major event, maintain one coordinated operational timeline with entity-specific impact and obligation records. Preserve local reporting clocks and contacts through [compliance-applicability.md](compliance-applicability.md). Keep regional facts distinct when a group-level statement would hide a different impact, recovery condition, or required decision.

## Report assurance and drive improvement

Provide decision-oriented reporting: exposure, affected business services/entities, evidence strength, known gaps, accepted exceptions, overdue treatment, accountable owner, and resources or decisions needed. Include trends and distributions in service harm, recovery capability, privileged access, control failures, repeated incidents, and supplier concentration. Pair improvement claims with a baseline and comparable population.

Show denominators: inventoried versus expected services, tested versus eligible controls, evidence available versus required, and recovery scenarios exercised versus planned. Separate effective, ineffective, not tested, insufficient evidence, and genuinely not applicable. Define the rule behind an overall rating; do not average away a critical failure or convert missing information into green status. Avoid ranking people by incident count or rewarding suppressed reporting.

Introduce the model through a representative pilot. Establish owners and scope, select material controls, connect evidence to normal workflows, test meaningful failure cases, and review with engineering and assurance stakeholders. Expand after resolving gaps in usability, coverage, access, and ownership. Propose a risk-based review cadence and revise it after incidents or material change; do not invent a universal quarterly obligation.

Finish with the operating-model decisions, control and ownership gaps, prioritized improvements, evidence needed, and explicit unresolved choices. Use [reliability-review.md](../assets/reliability-review.md) for the management review. Close findings after the responsible reviewer verifies the changed condition, including operation over a relevant period where needed. Use incidents, audits, near misses, and operator feedback to improve the controls and remove procedures that add work without reducing a material risk.

## Primary sources and limits

Primary pages checked 3 November 2026. The procedures above are original operational recommendations; apply the organization's adopted framework, licensed standard, contracts, and confirmed obligations. Do not claim certification, legal compliance, or an audit opinion from using this skill.

- **E1:** IIA, [current Statements of Position](https://www.theiia.org/en/resources/statements-of-position/) and [Three Lines Model, 2026](https://www.theiia.org/globalassets/site/resources/statements-of-position/tlm_assurance_advice_support_effective_gov_en.pdf). The July 2026 statement replaces the former position paper; it distinguishes operational ownership, specialist challenge, and independent audit while allowing context-appropriate arrangements.
- **E2:** NIST, [Cybersecurity Framework 2.0](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf). Use its governance outcomes as a common organizing language, adapted to enterprise context.
- **E3:** NIST, [CSF 2.0 Supply Chain Risk Management Quick-Start Guide, SP 1305](https://www.nist.gov/publications/nist-cybersecurity-framework-20-quick-start-guide-cybersecurity-supply-chain-risk). Use it to structure supplier requirements and lifecycle considerations.
- **E4:** ISO, [ISO 22301:2019 public overview](https://www.iso.org/standard/75106.html), including the listed amendment and revision status. The public description supports the management-system scope; consult the adopted licensed text for exact requirements.
