# AI operating contract: [use case / version / status]

Use [ai-governance.md](../references/ai-governance.md). This record describes the agreed design and evidence; permissions and limits must be enforced in the actual execution environment.

## Purpose, ownership and data

- Intended use, business outcome, users and excluded uses:
- Accountable business owner, technical operator, data/control owners and escalation:
- Legal entities, environments and service criticality:
- Model/provider/deployment, skill/tool/retrieval versions and update policy:
- Input/output/memory/log data classes and approved purposes:
- Processing, support, backup and retention locations; transfer and deletion conditions:
- Provider use for training/feedback, subprocessors and contractual evidence:
- Applicability assessment and unresolved constraints:

## Identity, authority and limits

| Capability | Exact target and permitted action | Human/agent/workload identity | Existing grant / approval condition / expiry | Enforcing system | Limit / denied case / evidence |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

- Operating mode and allowed transition to greater authority:
- Delegation, required separation of duties and approval binding to scope/artifact:
- Combined target, concurrency, retry, rate, time, cost and data-export budgets across agents:
- Credential issue/revoke path, egress and retrieval authorization:
- Changes that invalidate a prior grant; revalidation rules:
- Emergency access path and accountable retrospective review:
- Unknown or partially completed actions and reconciliation before retry:

## Evidence and outcome checks

- Request, authority, policy/version, tool invocation, target, identity, result and verification records:
- Redaction, access, retention, integrity and evidence-store failure behavior:
- Independent business/security invariants and acceptance criteria:
- Permitted/denied target tests, prompt-injection tests, dependency checks and partial-failure scenarios:
- Actual test environment, results, substitutions and remaining limits:
- Assessor/reviewer, required independent challenge and commissioning decision:

## Operation, recovery and retirement

- Monitoring, drift/degradation thresholds and stop conditions:
- Tested disable/revoke path and manual fallback:
- In-flight operation accounting and recovery owner:
- Version changes, regression evaluation and staged expansion conditions:
- Incident classification/escalation and supplier cooperation:
- Review triggers, expiring exceptions and funded improvements:
- Retirement, credential removal, memory/data disposal and retained evidence:

Preserve existing valid authorization. Record unknown authority explicitly and prepare the concrete missing decision. Do not treat model confidence, a generated approval, or another agent's agreement as an access grant.
