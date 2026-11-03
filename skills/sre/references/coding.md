# Software engineering and operational coding

Use this reference to read, implement, debug, refactor, review, or improve service code, operational tools, controllers, integrations, and configuration programs. Produce working changes when requested. Connect every change to an operational outcome and preserve the repository's conventions. Use [software-testing.md](software-testing.md) for verification and [cloud-delivery.md](cloud-delivery.md) for deployment and infrastructure execution.

## Contents

- [Establish the development context](#establish-the-development-context)
- [Implement a reviewable change](#implement-a-reviewable-change)
- [Choose and use the language](#choose-and-use-the-language)
- [Build reliable API clients and automation](#build-reliable-api-clients-and-automation)
- [Apply reliability patterns selectively](#apply-reliability-patterns-selectively)
- [Debug, profile, and refactor](#debug-profile-and-refactor)
- [Review, secure, and deliver](#review-secure-and-deliver)
- [Sources and maintenance](#sources-and-maintenance)

## Establish the development context

1. Identify the requested behavior, users, inputs, outputs, failure consequences, and independently supplied acceptance criteria. Determine whether the task concerns a one-time diagnostic, maintained CLI, service, library, operator, pipeline, or migration. Do not infer a complete implementation from a language name.
2. Inspect repository instructions, ownership, current work, entry points, architecture, configuration, tests, dependency manifests, lockfiles, and CI. Preserve unrelated edits. Read the relevant call sites and contracts before changing shared behavior. Trace source to built artifact and runtime configuration when investigating production code.
3. Establish the actual interpreter/compiler, target OS and architecture, SDK/provider versions, database dialect, deployment constraints, and supported compatibility matrix. Use installed help and version-matched official documentation for unfamiliar APIs. Do not invent packages, flags, methods, or minimum versions. Record an unverified interface instead of presenting plausible code as executable.
4. Retain existing authorization. File edits, isolated builds, and scoped tests are ordinary development work; a request to investigate or develop does not itself authorize production migrations, broad remediation, package publication, or deployment. Inspect build hooks, test fixtures, and tooling that could contact real services before execution. Apply the scope already authorized without asking again.

## Implement a reviewable change

Define a small contract: valid inputs; invalid-input behavior; output and exit status; state transitions; ordering and concurrency assumptions; deadlines; compatibility; and observable completion. Identify business invariants separately from the implementation, such as no duplicate charge, no cross-tenant access, and no silent record loss.

Prefer the smallest coherent change using existing abstractions. Keep decision logic separate from time, randomness, filesystem, process, and network effects so meaningful tests can control them. Avoid introducing a framework or dependency for a trivial function. Explain a new dependency's operational cost and maintenance owner when it is justified.

Validate external data at boundaries. Reject unsafe ambiguity rather than silently substituting broad defaults. Preserve error causes and distinguish validation failures, authorization failures, transient dependency failures, cancellation, and unknown outcomes. Return machine-readable results and useful human diagnostics without exposing credentials or customer data. Keep logs bounded and metrics cardinality controlled.

Build real implementations, not placeholder success responses. Handle resource cleanup, shutdown, work draining, and interrupted execution. Document limitations where the environment prevents verification. Add meaningful tests proportional to risk; do not create tests merely to repeat implementation details or to inflate coverage.

## Choose and use the language

Prefer the maintained language and libraries already used by the owning team. Compare deployment footprint, runtime availability, performance needs, integration support, security updates, and on-call readability before proposing a new language. Read and repair an existing estate without demanding a rewrite.

| Language or format | Apply these engineering practices |
|---|---|
| **Python** | Use the project's packaging and environment conventions. Write readable typed interfaces where helpful, explicit exception handling, context-managed resources, and bounded concurrency. For subprocesses, prefer argument sequences with `shell=False`, explicit working directory, timeout, and return-code handling; account for platform-specific process-tree cleanup and bounded output. Verify actual `subprocess` behavior in the [Python documentation](https://docs.python.org/3/library/subprocess.html). |
| **Go** | Pass request contexts through supported operations, release cancellation resources, and bound goroutines, queues, and client concurrency. Check and wrap errors with context; close resources and define shutdown ownership. Cancellation requests do not wait for work to stop: verify completion separately. Consult the [context contract](https://pkg.go.dev/context). Check target platform and native dependencies instead of promising every build is fully static or portable. |
| **Bash and POSIX shell** | Match the required shell and available tools. Quote expansions; use Bash arrays where appropriate; handle whitespace, globbing, empty input, leading dashes, and pipeline status. Avoid `eval` and parsing presentation output when structured output exists. Clean up task-owned temporary resources safely. Do not treat `set -e` as comprehensive error handling; its [conditional and pipeline exceptions](https://www.gnu.org/s/bash/manual/html_node/The-Set-Builtin.html) require explicit failure handling. |
| **PowerShell** | Use structured objects, parameter validation, explicit error handling, and suitable native-process exit checks. Distinguish Windows PowerShell from PowerShell and verify OS/module compatibility. Implement `SupportsShouldProcess` and guard each mutation correctly for truthful [`-WhatIf` behavior](https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-shouldprocess). Treat [execution policy](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies) as an operational safeguard, not a security boundary. |
| **JavaScript and TypeScript** | Follow the repository's module, runtime, and build conventions. Validate runtime payloads even with static types. Await asynchronous failures, propagate supported cancellation, respect stream backpressure, and bound buffers and parallel work. Profile event-loop delay; `async` does not make expensive synchronous work nonblocking. Use the [Node.js execution model](https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop) when diagnosing starvation. |
| **Java and C#/.NET** | Read service frameworks, thread/task lifecycles, pools, dependency injection, and runtime settings. Profile allocation, retained memory, GC pauses, locks, and pool exhaustion. Close/dispose resources and propagate supported interruption or cancellation; [.NET cancellation is cooperative](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads). Do not rely on old Java Security Manager advice: it is [permanently disabled from JDK 24](https://docs.oracle.com/en/java/javase/24/security/security-manager-is-permanently-disabled.html). |
| **Ruby** | Support existing Ruby services, scripts, gems, and Chef or Puppet-related code. Respect the runtime and dependency lockfile; inspect exception handling, dynamic dispatch, templates, and DSL evaluation. Prefer explicit, testable behavior over opaque metaprogramming. Preserve configuration-tool resource semantics when modifying Ruby-backed automation. |
| **SQL** | Confirm dialect, parameter-binding rules, schema, query plan, isolation level, locks, and transaction boundaries. Parameterize values and allowlist dynamic identifiers. Bound result sets and mutations, preserve tenant predicates, and design schema/data migrations for mixed application versions. Treat [`EXPLAIN ANALYZE`](https://www.postgresql.org/docs/current/sql-explain.html) in PostgreSQL as query execution, including writes; use [data-services.md](data-services.md) for operational review. |
| **Rust, C, and C++** | When relevant to the actual system, read and debug native code, FFI, ownership/lifetime assumptions, allocation, unsafe sections, synchronization, ABI, and build flags. Use applicable profilers, sanitizers, and debuggers within permitted overhead. Do not equate language-level memory safety with correct distributed behavior or assume native dependencies inherit that safety. |
| **YAML, JSON, HCL, and Bicep** | Distinguish serialization syntax from schema and domain correctness. Use parsers, types, units, schemas, API-version checks, and rendered diffs; reject unknown fields where the contract requires it. Treat HCL expressions, templates, and [Bicep](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview) as programs with evaluation and deployment semantics. Read existing Terraform, ARM/CloudFormation, Pulumi, Ansible, Puppet, Chef, and Salt artifacts in their own tool context. A valid file does not prove a safe or effective deployment. |

## Build reliable API clients and automation

Design automation to remain understandable when stopped halfway through a task. Make its target, intended changes, actual effects, and recovery path observable.

1. **Resolve identity and scope.** Validate endpoint, account, tenant, project, region, cluster, namespace, resource identifiers, and effective credentials. Use existing credential providers and least privilege; preserve TLS verification. Do not log tokens or embed production credentials in examples. Verify ownership and target selectors before acting.
2. **Read complete, bounded inventory.** Handle documented pagination, filtering, ordering, and continuation tokens. Detect repeated tokens or unexpected hosts; preserve authentication boundaries. Distinguish empty results from access denial, truncated results, stale caches, and failed enumeration. Stop mutation when selection is unexpectedly empty or broad; make any intentional empty-success contract explicit.
3. **Separate planning from mutation.** Produce a plan containing exact targets, preconditions, proposed operations, limits, and observable success criteria. Implement a genuine dry run that does not invoke mutating calls or side-effecting callbacks. State preview limitations, including eventual consistency and changes between preview and application.
4. **Validate preconditions again.** Use resource versions, conditional writes, transactions, or equivalent conflict detection when supported. Do not overwrite a concurrent operator's changes. Apply the approved scope; require a new decision only when the proposed action exceeds existing authorization or materially changes risk.
5. **Bound every dependency.** Set an overall operation budget and suitable connection/request deadlines. Propagate cancellation where supported, stop launching new work after cancellation, and account for work already accepted remotely. Bound concurrency, queue size, pages, bytes, and output; avoid exhausting the dependency while collecting evidence.
6. **Retry deliberately.** Classify retryable conditions using the API contract. Respect documented rate-limit guidance and delay signals; apply capped backoff and jitter within a total budget. Inspect SDK retries so layers do not multiply attempts. Do not retry validation or permission failures blindly. AWS's [timeout and retry guidance](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) explains why side effects and synchronized retries need special treatment.
7. **Handle ambiguous completion.** A timeout is not proof that a write failed. Use documented operation IDs, status queries, conditional operations, or stable idempotency keys with understood scope and retention. Reconcile the remote result before resubmitting an irreversible operation. Do not promise exactly-once effects from retries alone.
8. **Make repeats and overlaps safe.** Define idempotency for the intended state and input, then test it. Separate sequential repeat safety from concurrent reentrancy. Use appropriate atomic claims, leases, fencing, or transactions when multiple workers can act. Do not use a local lock as proof of exclusive ownership across hosts.
9. **Record partial outcomes.** Track succeeded, failed, skipped, and unknown targets without claiming overall success prematurely. Checkpoint only when durable semantics support resumption; avoid storing secrets. Define compensation or forward recovery for each irreversible boundary. Provide bounded cancellation, progress, audit identifiers, and a documented resume procedure.
10. **Verify the outcome.** Check intended state and user-facing behavior, not only exit zero or an accepted HTTP request. Summarize residual failures and cleanup. Route operational rollout and rollback decisions through [changes.md](changes.md).

## Apply reliability patterns selectively

Start with an observed failure mechanism and a measurable requirement. Use the ebook's patterns as design options; require a benefit, precondition, failure test, and operational owner before adding complexity.

| Pattern | Establish before adopting it |
|---|---|
| Circuit breaker | Define which dependency and failures it isolates, when it opens, bounded recovery probes, and safe fallback semantics. Test half-open concurrency and oscillation. A fallback must preserve authorization and data correctness. |
| Bulkhead and load shedding | Allocate meaningful concurrency/resource budgets and priority rules. Test overload isolation and starvation. Separate thread pools do not establish independent infrastructure or database capacity. |
| Failover and leader election | Define failure detection, quorum or ownership rules, stale-writer fencing, replication lag, and reconciliation. Test partition and failback behavior. Election alone does not make a single writer safe. |
| Graceful degradation and caching | Identify which features can be reduced, permissible staleness, visibility to users, and recovery. Never bypass security or transaction correctness to improve apparent availability. |
| Sharding | Justify the partition key with measured workload and growth. Model hotspots, resharding, cross-partition operations, and recovery; do not assume balanced traffic or free isolation. |
| Immutable deployment and self-healing | Establish artifact identity, bounded replacement rate, persistent-state compatibility, cooldowns, stop conditions, and verification. Replacement or restart cannot by itself establish repaired data integrity. |

Avoid copying old library recommendations without checking maintenance, runtime support, and security posture. For example, the ebook mentions Hystrix; its [maintainers state it is in maintenance mode](https://github.com/Netflix/Hystrix). Prefer the existing supported implementation when suitable; do not replace a library solely because another is fashionable.

## Debug, profile, and refactor

Trace an actual request or job from input through state and dependency boundaries. Match the deployed artifact, configuration, and feature flags to the source under investigation. Form competing hypotheses and identify evidence that would distinguish them. Use a minimal reproducer or regression case when feasible; correlate logs, traces, metrics, stack samples, and change history without treating temporal correlation as proof.

Profile the suspected resource under a representative workload before optimizing. Distinguish CPU work, I/O wait, lock contention, allocation/retention, garbage collection, queueing, connection limits, and downstream latency. Bound sampling duration and overhead; review dumps for sensitive material. Compare the same workload and correctness checks before and after a change. Do not optimize a mean while worsening tail latency, errors, or resource limits.

For refactoring, preserve documented interfaces and observable behavior. Separate structural cleanup from a behavior change when it improves review. Add characterization tests for poorly understood behavior, but reconcile inherited behavior with independent requirements rather than preserving a known defect. Maintain compatibility during staged migrations; include cancellation and error paths, not only successful requests.

## Review, secure, and deliver

Review the diff as both maintainer and operator: correctness, tenant boundaries, injection, path handling, permission scope, races, deadlines, resource limits, error reporting, compatibility, observability, dependency health, and failure recovery. Inspect generated code and configuration with the same standard as human changes. Never assume a library exists or a test passed because generated text says so.

Use the repository's formatter, linter, type checker, relevant build, and risk-based tests. Inspect install scripts, plugins, downloaded binaries, and untrusted CI contributions before granting credentials or execution. Respect dependency locks and trusted registries; assess a dependency change's transitive effects, supported versions, licensing constraints, and rollback. Keep secrets out of code, fixtures, diffs, artifacts, and logs.

Use small coherent commits and reviewable branches under existing Git conventions. Preserve other contributors' work; do not rewrite shared history or bypass required checks. Make pipeline stages and artifact promotion traceable. Treat build runners, caches, package stores, and deployment credentials as operated dependencies with owners and recovery procedures. A successful build or canary establishes only the properties it measured.

Deliver the changed files with the problem, behavior change, interfaces, usage, configuration, exact verification performed, results, and remaining uncertainty. Document ownership, failure modes, rollback or forward recovery, and operational checks. Distinguish tests actually executed from proposed checks; distinguish local verification from production evidence. Continue through the authorized development task rather than stopping at a code suggestion when implementation was requested.

## Sources and maintenance

This module adapts the user-supplied *Essential SRE Articles* by Marcel Koert, chapters 9 (build/deployment/integration), 12 (reliability patterns), 14 (programming languages), and 15 (infrastructure as code), into executable working practices. The language histories and tool lists are context, not version guarantees. The linked primary documentation supplies specific API and runtime qualifications. Recheck version-sensitive details against the actual host; do not prescribe a universal runtime, library, cloud tool, or deployment method.
