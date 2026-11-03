# Cloud, delivery, automation, and secure operations

## Contents

- [Establish the actual environment](#establish-the-actual-environment)
- [Cloud investigation](#cloud-investigation)
- [Infrastructure and configuration as code](#infrastructure-and-configuration-as-code)
- [Delivery and platform engineering](#delivery-and-platform-engineering)
- [Engineer operational software](#engineer-operational-software)
- [Security and reliability together](#security-and-reliability-together)
- [Deliverable and sources](#deliverable-and-sources)

## Establish the actual environment

Identify tenant/account/subscription/project, environment, region/zone, resource ID, owner, identity, command context, and provider/API versions. Separate SaaS/PaaS/IaaS responsibility and managed versus customer-operated control planes. Do not assume a managed service owns application correctness, tenant access, backup retention, recovery testing, or all upgrade decisions.

Prefer the existing Azure/AWS/GCP, Azure DevOps/GitHub/GitLab/Jenkins, Terraform/Bicep/Ansible, Helm/GitOps, and monitoring tools when they fit. Verify actual access and schema. Adapt to on-premises, air-gapped, hybrid, small-team, and regulated constraints. Read access in one account does not authorize a fleet-wide survey.

## Cloud investigation

Build a resource/dependency map before following dashboards across unrelated services. Collect a bounded view of relevant resource health, provider incident history, audit/activity events, platform maintenance, quota usage, provisioning failures, and workload telemetry for the same time interval. A provider-wide status page can miss a tenant-specific problem and cannot establish the health of the application.

| Suspected mechanism | Distinguishing evidence |
| --- | --- |
| Capacity or provisioning | Allocation error versus quota limit; regional/zone/SKU availability; reservation and actual instances; startup delay |
| Throttling | Specific API/identity/resource limits, returned retry guidance, request rate, concurrent clients, and retry amplification |
| Network path | Effective routing/NSG/security groups/firewall, private endpoints, NAT/SNAT, DNS view, load balancer health, MTU and egress |
| Identity | Expired credentials, workload federation trust, token audience/issuer/time, role/policy changes, propagation, KMS access |
| Platform event | Exact affected resource, maintenance/upgrade timestamps, region/zone, version, and unaffected comparison |
| Shared service | Registry, DNS, identity, keys, configuration, telemetry or artifact store unavailable during recovery |
| Serverless behavior | Concurrency, timeout, cold starts, retries, duplicate deliveries, dependency saturation and per-invocation limits |

Correlate autoscaling, replacement, and traffic movement with downstream capacity. More instances may exhaust a database pool or quota. Check whether the intended recovery region can provision and serve representative load with its dependencies. Do not equate multi-zone placement with resilience to a common software rollout or identity failure.

Route resource symptoms to the relevant technical reference. Include cost as a constraint—idle resilience, egress, logging, storage, reserved capacity, and recovery tests—but avoid recommending a cheaper architecture without evaluating failure impact.

## Infrastructure and configuration as code

Compare five states: reviewed intent, generated plan/manifests, approved artifact, applied changes, and observed effective runtime state. Record immutable revisions, provider/module/plugin versions, input source, identity, workspace/backend, and resource scope. Include drift from manual edits and independent reconcilers. A merged pull request does not prove deployment, convergence, or correctness.

Review for replacements/deletions, dependency ordering, state migration, force-new attributes, identity/network changes, controller interactions, secret exposure, default changes, and expanded selectors. An empty or missing selector must fail closed rather than expand to all resources.

Treat Terraform state and plan files as sensitive. `terraform plan` can refresh/query providers, acquire locks, invoke configured tooling, and consume privileges; a plan is not an assurance of zero side effects in an untrusted project. Inspect configuration and provider trust before running it. Do not expose raw plan JSON/state to the conversation. Use an approved backend with controlled access and recovery; do not disable state locks as a convenience. Review a fresh concrete plan before apply; stale plans or changed state require reassessment.

For Bicep/ARM, inspect the relevant deployment mode, what-if limitations, dependencies, replacement semantics, and effective policy. For Ansible/Rundeck, inspect inventory, limits, connection identity, privilege escalation, serial/batch policy, idempotency, and actual module check-mode support. A dry run can skip precisely the operation whose side effects matter.

For Helm, separate chart version, rendered manifests, effective values, hooks, controller behavior, and the deployed image digest. Values can contain secrets. For GitOps, establish reconciliation ownership and whether an emergency edit will be immediately reverted. Coordinate a scoped pause only when authorized and define how reconciliation resumes. For all tools, retain rollback prerequisites and a forward repair route for irreversible state changes.

## Delivery and platform engineering

Trace source revision → build → tests → signed/verified artifact → promotion → effective deployment → user outcome. Identify exactly which source, dependencies, base image, configuration, flags, schema, and secrets version a release uses. Compare artifact digests rather than mutable tags. Build once and promote immutable artifacts when appropriate.

Choose rollout scope and gates using changes.md. Separate deployment from feature exposure; define ownership and expiry for temporary flags. Evaluate config schema validation, compatible defaults, unknown-field handling, staged propagation, and partial application. Test failed or delayed config distribution and its last-known-good behavior.

Match tests to critical properties: authorization boundaries, API contracts, backward/forward schema compatibility, idempotency, timeouts, resource limits, disaster recovery, and actual user journeys. Treat a green pipeline as evidence of its tests only. Add independent business invariants where generated tests merely repeat an incomplete specification.

Treat the internal platform as a product with consumers, SLOs, documented contracts, paved deployment paths, and escape/escalation routes. Measure consumer success and the burden transferred to application teams. Validate self-service guardrails, tenancy/isolation, quotas, documentation, and deprecation/migration paths. Avoid forcing all workloads into one platform when compatibility and operating cost do not justify it.

## Engineer operational software

For implementation, debugging, refactoring, language-specific concerns, and code review, load [coding.md](coding.md). For choosing and interpreting verification, load [software-testing.md](software-testing.md). Use the workflow below to connect the implementation to its operational consequences.

Before automating, remove unnecessary work and simplify the process. Specify inputs and invariants, explicit target allowlists, least-privilege credentials, dry-run behavior, idempotency, bounded concurrency/retries, deadlines, partial-failure handling, and a kill switch. Record what was actually changed and make reruns safe or detect unsafe repetition.

Design evidence and action paths separately. Record the selected inventory snapshot, verify resources still match preconditions before changing them, and stop on unexpected scope expansion. Use safe structured arguments, strict input validation, and no shell evaluation of log content or user-controlled filenames. Avoid placing secrets in command arguments, telemetry, or errors.

Test meaningful failure cases: stale inventory, empty selectors, access denied, unavailable control plane, request accepted but response lost, duplicate work, partial completion, expired credentials, and changed state between planning and execution. Provide bounded retry with jitter and deduplication or compensation where needed. A retry of an irreversible operation needs explicit semantics.

Assign an owner, review path, version, supported environments, monitoring, rollback/disable path, and retirement criteria to operational code. Monitor the automation itself. High privilege plus broad scope plus an incorrect assumption can turn a small failure into a fleet incident.

## Security and reliability together

For group/shared-service controls, use [enterprise-governance.md](enterprise-governance.md) and [audit-evidence.md](audit-evidence.md) to establish retained customer responsibilities, assurance scope, actual access/change enforcement, evidence coverage and supplier concentration. Evaluate data/support locations and cross-border arrangements through [compliance-applicability.md](compliance-applicability.md).

Model sensitive assets, trust boundaries, adversaries, accidental misuse, and potential consequences. Map each threat to a preventive, detective, containment, and recovery mechanism. Include privileged insiders and compromised automation identities without assuming malice in an ordinary reliability incident.

Apply least privilege and short-lived credentials where feasible. Use workload identity, scoped APIs, audited administrative access, separation of duties appropriate to risk, and a tested emergency access process. Breakglass must retain accountability, expiry, and review; do not assume it permits disabling safeguards. Check whether responders can authenticate when the primary identity or key service fails.

Inventory certificate authorities/trust stores, certificate issuance/renewal/distribution/reload, key rotation, encryption key recovery, secret expiry, and ownership. A renewed certificate in a vault is not evidence that every process serves it. Verify trust and identity through the real client path; do not suppress validation errors to restore an apparently green metric.

Review secure coding, input validation, memory safety where relevant, dependency provenance, pinned artifacts, vulnerability handling, signing/attestation, and build isolation according to the platform. Verify security fixes against compatibility and canary evidence. For DoS/abuse, evaluate admission limits, fair quotas, upstream protection, legitimate-user impact, and backend amplification; a WAF alone is not a capacity strategy.

Treat security telemetry, debugging access, and evidence retention as services with privacy and availability requirements. On suspected compromise, engage the security owner; distinguish containment, eradication, trusted rebuild, credential rotation, data reconciliation, and return to service. Do not restore compromised keys or images from a convenient backup. Assess false positive and fail-open/fail-closed consequences for each control rather than choosing one policy universally.

## Deliverable and sources

Return the exact environment, responsibility boundaries, observed/effective changes, relevant evidence, ranked failure explanations or risks, and a staged action with verification and recovery. Link unresolved provider behavior to the correct version-specific documentation or a scoped vendor escalation draft.

Primary sources:

- [Azure reliability framework](https://learn.microsoft.com/en-us/azure/well-architected/reliability/), [AWS reliability pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html), and [Google Cloud reliability framework](https://docs.cloud.google.com/architecture/framework/reliability).
- HashiCorp [plan behavior](https://developer.hashicorp.com/terraform/cli/commands/plan) and [sensitive state/plan data](https://developer.hashicorp.com/terraform/language/manage-sensitive-data).
- Google [configuration design](https://sre.google/workbook/configuration-design/), [canary releases](https://sre.google/workbook/canarying-releases/), and [secure/reliable design, implementation and operation](https://google.github.io/building-secure-and-reliable-systems/raw/toc.html). Use relevant chapters rather than treating the table of contents as detailed evidence.
