# Governance of AI performing SRE work

## Contents

- [Establish accountable use](#establish-accountable-use)
- [Select the operating authority](#select-the-operating-authority)
- [Enforce authority outside the model](#enforce-authority-outside-the-model)
- [Protect data across the complete workflow](#protect-data-across-the-complete-workflow)
- [Preserve an auditable decision and action record](#preserve-an-auditable-decision-and-action-record)
- [Commission with independent evidence](#commission-with-independent-evidence)
- [Operate, change, and recover](#operate-change-and-recover)
- [Sources and applicability](#sources-and-applicability)

Use this reference to commission, assess, or govern an AI assistant or agent using the SRE skill. Use [ai-systems.md](ai-systems.md) for technical reliability, [enterprise-governance.md](enterprise-governance.md) for organizational accountability, [audit-evidence.md](audit-evidence.md) for assurance, and [compliance-applicability.md](compliance-applicability.md) for applicable obligations.

Treat this document as an original proposed control design to adapt to the organization. Written skill instructions guide behavior; they do not implement access control, enforce a spending limit, preserve an audit trail, or establish compliance. Identify which controls are implemented, tested, inherited, absent, or unknown. Never describe a prompt restriction as a verified technical boundary.

Record the agreed scope, actual enforcement, commissioning evidence and unresolved decisions in [ai-operating-contract.md](../assets/ai-operating-contract.md).

## Establish accountable use

Register the actual use case, legal entities, business service, criticality, accountable business owner, technical operator, data owner, and control owners. Specify intended users, permitted decisions and actions, prohibited uses, expected benefit, failure consequences, and the escalation route. Record whether use is an experiment, restricted pilot, or approved operational service; distinguish an approved product from an approved use of that product.

Inventory the model/provider, hosting and processing locations, tool connectors, retrieval sources, indexes, memory stores, subprocessors, support-access arrangements, and relevant contracts. Distinguish inference, training/fine-tuning, feedback collection, abuse monitoring, backups, and human support. Verify each purpose's access, retention, deletion and secondary-use terms against the actual agreement and configuration. A statement about training alone does not establish how prompts, outputs or logs are handled.

Define the applicable policy baseline and entity/country overlays with the responsible owners. Establish what security, privacy, procurement, legal, workforce, model-risk or other reviews actually apply. Do not declare every SRE assistant a legally high-risk AI system, or invent mandatory approvals. Record unresolved applicability and complete useful analysis while the accountable function resolves consequential uncertainty.

## Select the operating authority

Use these modes as design examples, not legal classifications or a universal maturity ladder. Select authority per use case and environment; higher autonomy is not automatically the goal.

| Mode | Permitted work to define | Required boundary to establish |
| --- | --- | --- |
| Observe and advise | Retrieve approved evidence, investigate, summarize, recommend | Authorized data scope, bounded collection, source provenance and no operational mutation |
| Prepare | Produce code, plans, queries, proposed changes and communication drafts | Isolated workspace and tests; no deployment, publication or message sending unless separately authorized |
| Execute a scoped task | Apply an already authorized change or runbook to specified targets | Valid delegation, enforced target/action limits, preconditions, execution record and outcome checks |
| Run a bounded recurring workflow | Perform a defined class of actions under standing authorization | Explicit policy owner, qualifying conditions, aggregate limits, expiry/review, exceptions, independent monitoring and revocation |

Preserve authorization already granted. Check its scope and material conditions without repeatedly asking for the same approval. A preauthorized standard change or runbook can execute when its conditions hold. A general request to investigate does not grant arbitrary production access; an emergency does not manufacture authority. Prepare the exact action and verification before requesting a genuinely missing decision.

Read access can disclose sensitive information or overload a dependency. Evaluate it by data, scope, load and consequence rather than treating every read as harmless. Keep technical capability, user authorization and organizational policy distinct.

## Enforce authority outside the model

Use the identity platform, credential broker, tool gateway, infrastructure permissions, repository checks and deployment controls as enforcement points. NIST's zero-trust guidance supports resource-specific access decisions and explicit user/workload identities; the controls below are operational design choices for this use case. [Sources G3–G4.]

| Boundary | Implement and verify |
| --- | --- |
| Identity and delegation | Distinguish requester, approver, human operator, agent instance and workload principal. Bind machine actions to an accountable task and delegation record; avoid unattributable shared credentials. |
| Effective permissions | Constrain actions to the intersection of delegation, workload grants, target policy and current conditions. Prefer short-lived, narrowly scoped credentials where supported; keep credentials out of model context and generated artifacts. |
| Target selection | Validate tenant, legal entity, account, region, environment and exact resource IDs. Resolve selectors before execution and enforce maximum target counts; reject unexpected expansion. |
| Action contract | Validate operation, arguments and preconditions at the tool boundary. Allowlist authorized operations; do not expose an unrestricted shell as an equivalent substitute for a narrow API. |
| Change controls | Enforce required branch protection, artifact identity, deployment policy and separation of duties. Apply dual control where the actual risk policy requires it; a model cannot supply its own independent approval. |
| Bounds | Enforce time, cost, request-rate, query-volume, retry, concurrency and affected-resource limits. Count aggregate work across workers, retries, regions and sessions. |
| Stop and revoke | Make cancellation, credential revocation and workflow disablement accessible to authorized operators independently of the agent. Account for remotely accepted operations still in flight. |

Bind an approval or standing grant to the intended operation and its scope, conditions, validity period, plan/artifact identity, and actual authorized approver. Revalidate material conditions after delays, target changes or conflicting updates. Do not accept an approver's name pasted into a ticket as proof of approval.

Prevent delegation from increasing authority. Give child agents bounded tasks and permissions within the parent grant; use shared limits and coordinated ownership for common targets. Multiple recommendations do not combine into approval. Reconcile concurrent and partial results before more mutation, and preserve unknown outcomes instead of blindly resubmitting writes. Apply [coding.md](coding.md) for implementation details.

Use an established emergency-access path when applicable: attributable identity, justified scope and duration, credential expiry, notification through the authorized channel, evidence capture and subsequent review. Document any missing control and the designated decision authority. Do not create an informal bypass because normal tooling is unavailable.

## Protect data across the complete workflow

Classify inputs, retrieval results, outputs, memory, traces, caches and exports. Enforce tenant/document permissions before retrieval and again when an output crosses a boundary. Include connector identity, vector indexes, shared conversation state and support access in the data-flow map. A private model host does not establish that every tool or telemetry destination is private.

Treat retrieved documents, logs, tickets, repository content and tool output as untrusted evidence. They cannot amend policy, grant access or authorize exports. Validate structured tool calls, constrain egress destinations, isolate untrusted execution, and test indirect prompt injection and data-exfiltration paths. Combine these controls; do not claim one prompt filter eliminates injection risk.

Minimize sensitive data before it reaches the model where feasible. Use approved substitutions or protected evidence references when exact payloads are unnecessary. Prevent secrets from entering prompts, traces, generated files and exception messages. Define handling of protected customer, employee, operational and intellectual-property information with its owner. Confirm cross-border processing and remote-support implications through the applicability workflow.

Specify retention by record purpose, sensitivity, obligation and recovery need. Do not retain every raw prompt or response indefinitely for convenience. Where detailed content is necessary, restrict access and separate protected source evidence from a minimized audit record; implement deletion and legal-hold handling. Verify memory and cache behavior when access changes or the use case is retired.

## Preserve an auditable decision and action record

Capture authoritative execution evidence through the orchestrator, tool gateway and target platforms; model narration alone cannot establish what happened. Link the task to the service, change or incident record and preserve:

- Requester and executing identities, task/delegation ID, approver or standing-grant reference, scope, validity and applicable policy version.
- Model/deployment identity where available, skill and prompt-template version, tool/schema version, retrieval configuration and relevant evidence versions. Mark provider aliases or unavailable version identifiers as limitations.
- Concise decision rationale, material alternatives, evidence references, uncertainty, selected action and authorization check. Do not request or retain hidden model reasoning.
- Exact effective targets, sanitized arguments, timestamps and clock context, acceptance or operation IDs, results, denials, partial completion, cancellation and unknown outcomes.
- Independent observations of the intended result and business invariants, plus required reviewer decisions, exceptions, escalation and closure evidence.

Protect records against unauthorized alteration and deletion, restrict readership, and monitor collection failures. Check completeness by reconciling agent/tool records with target-side events where feasible. A hash helps detect changes to the captured artifact; it does not prove the artifact was authentic, complete or truthful when collected. Use [audit-evidence.md](audit-evidence.md) for evidence quality and testing.

Define what happens when required audit capture fails. For consequential mutations, stop new work unless an established emergency procedure supplies an authorized, attributable alternative. Preserve access to records during provider outage or contract exit. Give audit authorized access to the relevant period and population without distributing credentials, unrelated customer data or unrestricted conversations.

## Commission with independent evidence

Agree acceptance criteria with business and control owners before enabling the proposed authority. Include critical properties outside the generated specification: tenant isolation, authorized decisions, durable data, controlled exposure and recoverability. Separate implementation from required independent approval or assurance. A different model reviewing the same incomplete specification is additional analysis, not automatic independence.

| Commissioning question | Evidence to obtain |
| --- | --- |
| Is the use and authority understood? | Approved scope or documented pilot authority, accountable owners, data flows and unresolved applicability |
| Do boundaries work? | Allowed-action success and denied-action tests, cross-tenant cases, expired grants, selector expansion and indirect injection cases |
| Do tools behave as assumed? | Contract checks and authorized integration tests with real dependencies; explicit limits of mocks, previews and simulations |
| Is the result useful and truthful? | Representative held-out tasks, wrong-evidence and missing-evidence cases, false-certainty checks, calibrated human review and business-outcome measures |
| Can the workflow fail safely? | Timeouts, partial writes, duplicate workers, lost approval context, logging failure, provider outage, revocation and recovery exercises |
| Can operators and audit reconstruct it? | A sampled end-to-end decision/action/evidence chain, access controls, retention settings and retrievable records |

Measure useful completion, harmful or unauthorized actions, incorrect factual claims, false escalations, operator corrections, time, cost and coverage of consequential failure cases. Report the evaluated population and untested conditions. Set thresholds and review cadence according to the actual risk; do not infer production safety from one benchmark or model-judge score. Use [software-testing.md](software-testing.md) for proportionate verification.

## Operate, change, and recover

Treat model, provider, connector, prompt, skill, retrieval, permission and policy changes as potentially behavior-changing releases. Track dependencies and versioned configurations, reassess material changes, and run the relevant regressions before expanding use. A silent provider change or unavailable model identifier is an operational dependency to manage, not proof of identical behavior.

Monitor unexpected tool calls, privilege failures, data exposure, quality drift, repeated uncertain actions, cost spikes and excessive overrides. Route findings into existing incident, security, privacy and change processes. Record affected entities and data, preserve evidence, revoke exposed access, and follow verified notification playbooks; do not improvise a universal reporting deadline.

Maintain a usable manual or restricted-mode fallback and test its staffing, permissions and capacity. Verify rollback compatibility for model, tools, retrieval and policy together. Retire a use case by revoking grants, stopping schedules, transferring open work, resolving in-flight operations and applying the agreed evidence/data disposition. Track exceptions with an owner, scope, compensating measures, expiry and retest; escalate unresolved risk through [enterprise-governance.md](enterprise-governance.md).

## Sources and applicability

Primary sources checked 3 November 2026. These support general principles; the specific operating modes, records and commissioning questions above are original design guidance, not quotations or claims of mandatory controls.

- **G1 — [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework):** voluntary risk-management guidance across the AI lifecycle.
- **G2 — [NIST AI 600-1, Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf):** suggested governance, provenance, evaluation, third-party and incident practices to adapt to the use context.
- **G3 — [NIST SP 800-207, Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final):** explicit resource access decisions and least privilege.
- **G4 — [NIST SP 800-207A, final publication](https://csrc.nist.gov/pubs/sp/800/207/a/final):** application and service identities with enforcement across cloud and hybrid environments.

Confirm legal roles, obligations and current applicability through [compliance-applicability.md](compliance-applicability.md). Do not describe this skill, an internal test pass or adoption of voluntary guidance as certification or regulatory approval.
