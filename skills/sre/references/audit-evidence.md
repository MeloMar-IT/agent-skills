# Audit evidence and control assurance

Use this reference to prepare an assessment, design evidence collection, answer an audit request, or evaluate whether an operational control works. Pair it with [enterprise governance](enterprise-governance.md), [regulatory applicability](compliance-applicability.md), and the relevant technical playbook. Produce evidence-backed findings; do not declare certification or compliance from a completed template, an AI answer, or a dashboard.

## Contents

- [Define the assessment and control](#define-the-assessment-and-control)
- [Use a proportionate starter control catalog](#use-a-proportionate-starter-control-catalog)
- [Build a traceable evidence record](#build-a-traceable-evidence-record)
- [Establish population completeness and test coverage](#establish-population-completeness-and-test-coverage)
- [Protect evidence and its collection](#protect-evidence-and-its-collection)
- [Automate collection without automating false assurance](#automate-collection-without-automating-false-assurance)
- [Handle findings and audit requests](#handle-findings-and-audit-requests)
- [Report assurance honestly](#report-assurance-honestly)
- [Sources and boundaries](#sources-and-boundaries)

## Define the assessment and control

Identify the commissioning party, purpose, legal entities, services, locations, assessment period, authoritative criteria, assessor, access scope, and reporting audience. Establish whether the task is an engineering self-check, management monitoring, second-line challenge, internal audit, external assurance, or certification assessment. Preserve the required independence; a control owner checking their own work can provide useful evidence but cannot silently become an independent auditor.

Separate three questions: **design** (does the control address the relevant risk?), **implementation** (is it deployed for the stated scope?), and **operation** (did it operate as intended during the period?). Define each conclusion and its evidence. A current configuration snapshot cannot establish a year's operating effectiveness. A policy expresses intent; a ticket status expresses workflow state; neither proves the protected outcome.

For each control, record the risk and objective, authoritative requirement and version, applicability rationale, accountable control owner, executor, technical mechanism, inherited dependencies, scope, trigger/frequency, expected outcome, assessment procedure, evidence source, retention/access rules, exception route, and review trigger. Set parameters from approved requirements and risk rather than inventing a universal cadence or threshold. Use [control-register.md](../assets/control-register.md).

Use examination, interviews, and tests as complementary assessment methods. Inspect the actual configuration and records, ask participants how work happens, and exercise the relevant mechanism within authorized scope. Match the method to the claim: observing a denied unauthorized deployment can support a prevention claim; a report listing approvals alone cannot. NIST SP 800-53A provides a customizable assessment approach; adopting these methods does not make the whole NIST catalog mandatory. [A1]

## Use a proportionate starter control catalog

The following IDs are **local example identifiers**, not official ISO, NIST, SOC, or statutory control numbers. Tailor scope and parameters before adoption. Reuse a verified common control across mapped obligations while preserving differences in entities, periods, criteria, and evidence.

| Example ID / objective | Mechanism to examine | Evidence and useful effectiveness check |
| --- | --- | --- |
| SRE-G01: Scope and accountability | Reconciled service/dependency inventory, accepted owners, criticality and business impact | Compare inventory with active accounts/resources and business services; identify unowned or excluded services. |
| SRE-G02: Privileged access | Attributable identities, least privilege, time-limited elevation, required separation of duties, emergency access | Inspect grants and actual use; test relevant denied paths and revocation; review break-glass and orphaned access. |
| SRE-G03: Controlled change | Protected source, scoped authorization, tested immutable artifact, controlled deployment and verification | Trace a sample from request to actual runtime state; include manual, failed, rollback and emergency changes. |
| SRE-G04: Configuration and exposure | Versioned baseline, drift detection, patch/dependency and secret/certificate lifecycle | Verify identified assets, actual versions, known exceptions and remediation; test detection of an authorized sample deviation. |
| SRE-G05: Service detection and response | User-oriented indicators, alerts, routing, coverage and telemetry health | Verify measurement population, detection gaps, delivery and responder action; retain normal and failure observations. |
| SRE-G06: Incident accountability | Timeline, action authority, classification, reporting decision and learning | Trace relevant incidents and near misses; verify classification and notification handling against the applicable playbook. |
| SRE-G07: Recoverability | Scenario-specific recovery objectives, backup/key isolation, restore, reconciliation and failback | Inspect observed recovery time/data age and usable business outcomes; distinguish tested dependencies from exclusions. |
| SRE-G08: Data handling | Classification, approved collection/egress/access, transfer conditions, retention and deletion | Trace data through operational tools and evidence stores; test relevant access/redaction/deletion paths and legal holds. |
| SRE-G09: Supplier dependence | Responsibility split, scoped assurance, incident cooperation, concentration and exit | Evaluate actual service/subcontractor coverage, customer responsibilities, exceptions, portability and tested continuity assumptions. |
| SRE-G10: Evidence integrity | Attributable logs, reliable collection, protected storage, controlled retention and access | Reconcile source and destination counts/coverage; test collection failure and detection of unauthorized alteration or deletion. |
| SRE-G11: AI-assisted operations | Approved use and data boundaries, tool-enforced capabilities, versioned evaluations, bounded execution | Trace human request through model/tool identities and authorization to verified outcome; test prohibited targets and revocation. |
| SRE-G12: Risk treatment and improvement | Owned findings, expiring exceptions, funded remediation and effectiveness review | Check overdue/expired items and repeat incidents; retest the changed safeguard before concluding the issue is resolved. |

Technical controls can serve several objectives. Identify their shared failure modes: the same identity provider, pipeline, cloud account, or log administrator may undermine multiple apparently separate safeguards.

## Build a traceable evidence record

Use [audit-evidence-record.md](../assets/audit-evidence-record.md). Include:

1. **Claim and scope:** control/objective, service and legal entity, environment, period, population, inclusion/exclusion rules, and required property.
2. **Provenance:** authoritative source, query/filter and time interval, event and collection times with offsets, collector identity, resource IDs, relevant software/policy versions, access constraints, and original evidence reference.
3. **Method and coverage:** examine/interview/test, sample selection, expected result, actual result, dependencies or simulations, and whether observation was contemporaneous or reconstructed.
4. **Integrity and handling:** digest/signature where useful, trusted source/time reference, transformation/redaction steps, classification, storage/access location, retention rule and legal hold if applicable.
5. **Assessment:** assessor and review role, finding, uncertainty, limitation, residual risk, action owner, due date, exception reference, and retest evidence.

Trace consequential changes through request, rationale, existing or new authorization, approver/delegation identity where required, approved scope/version, code/configuration revision, built artifact identity, executing human/workload identity, exact target, time, actual result, recovery, and independent outcome observation. Record policy versions and what decision they supported. A late approval or reconstructed record must be labeled as such; never backdate it or recast it as contemporaneous approval.

For AI-assisted work, retain the approved task, relevant redacted inputs/evidence references, model/skill/tool versions when observable, capability grant, tool arguments/results needed for accountability, interventions, and verification. Mark unavailable vendor version information unknown. Preserve a concise decision rationale; do not request hidden model reasoning or indiscriminately archive raw prompts, credentials, or customer payloads. Use [AI governance](ai-governance.md).

## Establish population completeness and test coverage

Define the full population independently of the records being tested. For release controls, reconcile deployment/runtime or cloud audit events with pipeline runs and change records; a report containing only approved tickets omits unrecorded deployments. For access, reconcile directories, local accounts, cloud/workload identities, grants and actual use where relevant. For incidents, consider independent impact signals and support records as well as formally declared incidents.

Record totals, time boundaries, regions, excluded systems, collection failures, duplicate treatment, late events, and retention gaps. Keep event time separate from ingestion time and account for clock uncertainty. Explain what is unobservable. Treat missing data as unknown coverage, not zero events or successful operation.

Choose full-population analytics when reliable and proportionate; otherwise document a risk-based sample and what inference it supports. Include relevant entities, regions, platforms, control owners, standard/normal/emergency changes, unsuccessful attempts, failures, out-of-hours activity and exceptions. Do not claim statistical confidence from an arbitrary sample size. Let the responsible assessor define the assurance methodology and expansion criteria.

Distinguish a valid zero-event period from failed collection. A control triggered only by an event may have no actual instances to inspect; assess design/readiness separately and report operation as not observed for that period. A demonstration does not fabricate a historical occurrence. Verify any cross-framework mapping against the exact applicable text and assessment purpose before reusing evidence.

## Protect evidence and its collection

Assign evidence ownership and least-privilege access. Separate the ability to perform sensitive operations from the ability to erase their records where required and feasible. Use protected centralized or appropriately regional storage, tamper-evident or immutable retention where justified, monitored access, and a tested retrieval process. Audit privileged log configuration, export, retention changes and deletion as well as ordinary access.

Preserve originals and record transformations; retain a redacted working copy when needed. A checksum can show that collected bytes changed, but cannot establish that the original source was truthful, complete, or collected at the claimed time. Bind integrity checks to trusted provenance, access controls and timestamps. For security investigations, follow the organization's forensic preservation and chain-of-custody procedure with accountable custody transfers.

Derive retention from verified legal, contractual, operational and investigative needs. Resolve conflicts with the relevant data/records/legal owners, apply legal holds when authorized, and remove evidence according to the approved schedule when no hold applies. Avoid universal retention periods and indefinite raw-data collection. Minimize personal data and secrets, control remote access/exports, and check permitted locations and cross-border transfer arrangements before centralizing records.

Evidence capture must not create an outage: bound query load, permissions, data volume and collection time; monitor the collector itself. Plan protected temporary records and later reconciliation when primary logging is unavailable. A consequential action requiring an enforced audit path must follow its approved emergency policy; do not silently bypass the control because evidence collection failed.

## Automate collection without automating false assurance

Integrate evidence capture into source control, delivery, identity, infrastructure, incident and recovery workflows. Reuse stable service/control/change IDs and machine-readable records. Select an existing system of record and link evidence rather than duplicating sensitive exports into multiple ticketing or reporting tools. OSCAL can represent assessment plans, observations, findings, risks and remediation when the organization's tooling benefits from it; it is an optional interchange choice, not a certification. [A2]

Version and review collection queries, parsers, policy rules and mappings. Test them against missing, duplicate, delayed, malformed, unauthorized and contradictory records. Check that permissions and pagination cover the intended population. Keep denied actions and exceptions visible. Protect collectors and credentials, detect stale feeds, and reconcile counts after a source/schema/version change.

Treat an automatic pass as the result of a specific rule on a specific population at a time. Validate the rule's assumptions and false-negative paths. A disabled or bypassed policy engine can produce a deceptively clean report. Keep evidence of enforcement separate from evidence that a reporting rule ran. Preserve independent review for the required assurance purpose.

## Handle findings and audit requests

Agree the requested objective, period, population, format, classification, recipient and authorized access before disclosure. Prepare an indexed, minimal evidence package with links to originals, collection method, scope, findings and limitations. Resolve privacy, contractual or privileged-material constraints through the actual owner; do not label documents legally privileged without authority. Draft responses freely and transmit only with explicit authorization and verified recipients.

For a finding, state the criterion, observed condition, evidence, affected scope, consequence and uncertainty. Separate a missing record from a confirmed failed control without erasing the risk from either. Avoid reconstructing a convenient causal narrative or claiming the issue is isolated without checking population evidence. Preserve management disagreement and the assessor's independent conclusion.

Assign remediation ownership, a target date, interim measures and a measurable closure test. Use [risk-exception.md](../assets/risk-exception.md) when the authorized risk owner accepts a permitted temporary deviation; an exception does not erase the finding, waive a binding obligation, or alter the audit opinion. Reopen or escalate expired exceptions, failed controls and ineffective fixes. Close corrective work only after the required retest and decision, retaining historical evidence.

## Report assurance honestly

Report each material control as supported for the stated scope/period, deficient, partially evidenced, not tested/unknown, or not applicable with a documented rationale. Preserve the assessor's formal rating scheme where supplied. Avoid reducing the result to a single percentage that hides missing critical services or a failed recovery capability.

Include population and coverage denominators, evidence freshness, inherited-control dependencies, recurring deficiencies, overdue actions, expiring exceptions, and untested recovery scenarios. Show critical gaps and the decision/funding required. Distinguish management representations from independently checked evidence. State what the assessment supports and what it does not establish.

## Sources and boundaries

Primary sources checked 3 November 2026. This playbook is an original practical design; the example catalog is not a licensed standard or formal crosswalk.

- **A1:** [NIST SP 800-53A Rev. 5, assessment methodology and maintained releases](https://csrc.nist.gov/pubs/sp/800/53/a/r5/final); [publication](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53Ar5.pdf), including examine/interview/test methods. Use the applicable release and tailored assessment plan.
- **A2:** [NIST OSCAL Assessment Results](https://pages.nist.gov/OSCAL/learn/concepts/layer/assessment/assessment-results/) and [assessment layer](https://pages.nist.gov/OSCAL/learn/concepts/layer/assessment/). Validate the actual schema/version before implementing an export.

Use [compliance-applicability.md](compliance-applicability.md) for requirement selection and source limitations. A skilled AI can help prepare and analyze evidence; the appointed accountable functions retain their decisions and assurance responsibilities.
