# Change review: [change / service]

Review mode: [prospective review / post-change investigation]

## Intent, scope and evidence

- Desired user/business outcome; owner and schedule:
- Exact environment/resources and observed versions:
- Reviewed artifact/revision/digest and effective-state evidence:
- Dependencies, flags, config, schema, identity, network and platform changes:
- Service health, SLO/budget, capacity and data state before the change:
- Existing authorization; applicable review or release gates:
- Legal entities/services affected; standard/preauthorized, assessed or emergency path:
- Actual authority/delegation, scope/conditions, policy version and required separation of duties:

## Risk and validation

| Failure scenario | Evidence / uncertainty | Users/data affected | Prevent/detect/contain control | Validation result | Owner |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

Record compatibility across mixed old/new code and data, state migrations, controller interactions, expected load and recovery capacity.

## Concrete execution plan

| Step | Exact target/action | Preconditions | Expected result | User-facing gate / observation | Stop and recovery action |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

- Canary/control population and confounders:
- Minimum meaningful exposure and relevant business cycle:
- Quantitative stop/progress criteria and evidence owner:
- Rollback prerequisites, point of no return and forward repair:
- Data loss/reconciliation and backup/restore evidence:
- Communication draft, authorized recipients and cadence:
- Traceable request, approval/standing grant, artifact, executing identity, target and result evidence:
- Evidence capture failure handling and authorized emergency alternative, where required:

## Post-change investigation — if applicable

| Candidate change | Actual applied time/cohort | Proposed failure mechanism | Supporting / contrary evidence | Next discriminating check |
| --- | --- | --- | --- | --- |
| | | | | |

Distinguish first bad time from deployment time. Record expected-but-absent effects and unaffected populations. A rollback that helps is evidence, not automatic proof of the whole causal story.

## Decision

[Proceed within existing authority / conditional / blocked by specific evidence gap / not recommended].

State reasons, exact unresolved decisions, accountable risk owner, verification result, and residual risk. Do not label a plan "approved" unless the approval exists.

Preserve valid preauthorization without adding a new gate. Record any retrospective review as retrospective; link a permitted, scoped [risk exception](risk-exception.md) where applicable.
