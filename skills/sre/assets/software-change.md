# Software implementation or review: [service / tool / change]

Use for a substantial coding task. Keep a small fix proportionate; do not require every field before making useful authorized progress.

## Outcome and constraints

- Requested behavior and user/operational problem:
- Repository instructions, relevant files, existing work to preserve:
- Runtime/language/toolchain and supported OS/architecture:
- Inputs, outputs, caller contracts, data classification:
- Business invariants and unacceptable outcomes:
- Available access, existing authority, and execution environment:
- Explicit non-goals and unresolved consequential questions:

## Implementation contract

| Concern | Intended behavior | Evidence / design decision |
| --- | --- | --- |
| Target selection and empty/ambiguous scope | | |
| Input/schema validation and malformed data | | |
| Identity, permissions and secret handling | | |
| Deadlines, cancellation and resource cleanup | | |
| Retries, idempotency and uncertain outcomes | | |
| Pagination, concurrency and rate limits | | |
| Partial failure, resumability and result reporting | | |
| Dry-run/plan behavior and actual effect boundary | | |
| Logging, metrics, exit status and operator diagnostics | | |
| Compatibility, migration and recovery | | |

## Code and review findings

- Implemented files/diff and purpose:
- Reused interfaces and dependencies; any new dependency rationale:
- Error paths, concurrency/state concerns and complexity:
- Security review and sensitive output handling:
- Findings with severity, location, concrete failure and proposed correction:

## Verification

| Property / failure case | Test or check and environment | Expected result | Actual result | Limitation / unresolved risk |
| --- | --- | --- | --- | --- |
| | | | | |

Distinguish syntax/static checks, controlled test doubles, contract/integration tests, and live evidence. Do not label an unexecuted check as passed or a simulated outcome as production validation. Include only checks that address a concrete risk or required gate.

## Operation and delivery

- Usage, configuration, example invocation and supported environments:
- Deployment artifact/revision and rollout scope if requested:
- Success/stop criteria, rollback or forward recovery:
- Ownership, maintenance, dependency updates and deprecation:
- Remaining gaps and next action:
